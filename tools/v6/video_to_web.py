"""Yerel videodan web arka planı, poster ve kaydırma kareleri üretir."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run_ffmpeg(binary, arguments):
    completed = subprocess.run(
        [str(binary), '-nostdin', '-hide_banner', *arguments],
        capture_output=True, encoding='utf-8', errors='replace', timeout=180,
    )
    if completed.returncode:
        raise ValueError(f'FFmpeg işlemi tamamlanamadı:\n{completed.stderr[-2500:]}')
    return completed


def find_ffmpeg(explicit=None):
    candidate = explicit or shutil.which('ffmpeg')
    if not candidate or not Path(candidate).is_file():
        raise ValueError('FFmpeg bulunamadı. PATH’e ekle veya --ffmpeg ile çalıştırılabilir dosyanın yolunu ver.')
    return Path(candidate).resolve()


def video_duration(binary, source):
    metadata = run_ffmpeg(binary, ['-i', str(source), '-t', '0', '-f', 'null', '-'])
    match = re.search(r'Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)', metadata.stderr)
    if not match:
        raise ValueError('Video süresi okunamadı. Süresi belirli bir MP4 veya WebM dosyası kullan.')
    hours, minutes, seconds = map(float, match.groups())
    duration = hours * 3600 + minutes * 60 + seconds
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('Video süresi geçersiz.')
    return duration


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path, base):
    return {'file': path.relative_to(base).as_posix(), 'bytes': path.stat().st_size, 'sha256': sha256(path)}


def convert_video(source, destination, *, ffmpeg=None, frames=48, width=720,
                  start=0, duration=None, quality=76, budget_kb=1500):
    source = Path(source).resolve()
    destination = Path(destination).resolve()
    if not source.is_file():
        raise ValueError('Kaynak video bulunamadı.')
    if destination.exists():
        raise ValueError('Çıktı klasörü zaten var; yeni bir klasör adı seç.')
    if type(frames) is not int or not 12 <= frames <= 120:
        raise ValueError('Kare sayısı 12–120 arasında olmalı.')
    if type(width) is not int or not 240 <= width <= 1920:
        raise ValueError('Uzun kenar 240–1920 piksel arasında olmalı.')
    if type(quality) is not int or not 1 <= quality <= 100:
        raise ValueError('WebP kalitesi 1–100 arasında olmalı.')
    if not math.isfinite(start) or start < 0 or not math.isfinite(budget_kb) or budget_kb <= 0:
        raise ValueError('Başlangıç ve bütçe geçersiz.')
    binary = find_ffmpeg(ffmpeg)
    available = video_duration(binary, source)
    if duration is None:
        duration = available - start
    if not math.isfinite(duration) or duration <= 0 or duration > 20 or start + duration > available + 0.05:
        raise ValueError('Seçilen bölüm 0–20 saniye içinde olmalı ve kaynak videonun dışına taşmamalı.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cwi-video-', dir=destination.parent) as scratch:
        staging = Path(scratch) / 'export'
        frame_directory = staging / 'frames'
        frame_directory.mkdir(parents=True)
        # Uzun kenarı sınırla; portre ve yatay videolar aynı bellek bütçesine sığar.
        scale = f"scale=w='min(iw,{width})':h='min(ih,{width})':force_original_aspect_ratio=decrease:force_divisible_by=2,setsar=1"
        segment = ['-ss', str(start), '-i', str(source), '-t', str(duration), '-map', '0:v:0', '-an']
        run_ffmpeg(binary, [*segment, '-vf', f'{scale},fps={frames / duration:.10f}',
                           '-frames:v', str(frames), '-c:v', 'libwebp', '-quality', str(quality),
                           '-start_number', '0', str(frame_directory / 'frame-%03d.webp')])
        extracted = sorted(frame_directory.glob('frame-*.webp'))
        if len(extracted) != frames:
            raise ValueError(f'{frames} kare bekleniyordu, {len(extracted)} üretildi. Daha uzun bir bölüm seç.')
        frame_bytes = sum(path.stat().st_size for path in extracted)
        if frame_bytes > budget_kb * 1000:
            raise ValueError(f'Kareler {frame_bytes / 1000:.1f} KB; {budget_kb:g} KB bütçesini aşıyor. Uzun kenarı, kare sayısını veya kaliteyi azalt.')
        poster = staging / 'poster.webp'
        shutil.copyfile(extracted[0], poster)
        background = staging / 'background.mp4'
        run_ffmpeg(binary, [*segment, '-vf', f'{scale},fps=24', '-c:v', 'libx264',
                           '-pix_fmt', 'yuv420p', '-crf', '26', '-preset', 'fast', '-movflags', '+faststart', str(background)])
        manifest = {
            'version': 1, 'kind': 'video-frame-sequence',
            'source': {'name': source.name, 'sha256': sha256(source), 'startSeconds': start, 'durationSeconds': duration},
            'frameCount': frames, 'maxDimension': width,
            'sampleIntervalSeconds': duration / frames,
            'sequenceBytes': frame_bytes, 'budgetKb': budget_kb,
            'frames': [dict(file_record(path, staging), timeSeconds=round(index * duration / frames, 6)) for index, path in enumerate(extracted)],
            'poster': file_record(poster, staging), 'background': file_record(background, staging),
            'review': {'temporalArtifacts': 'pending', 'mobileComposition': 'pending', 'loopContinuity': 'pending'},
        }
        (staging / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        # Başarısız üretim hedefte yarım dosyalar bırakmaz; mevcut klasörler değiştirilmez.
        staging.rename(destination)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--ffmpeg', type=Path)
    parser.add_argument('--frames', type=int, default=48)
    parser.add_argument('--width', type=int, default=720, help='Uzun kenarın üst sınırı')
    parser.add_argument('--start', type=float, default=0)
    parser.add_argument('--duration', type=float)
    parser.add_argument('--quality', type=int, default=76)
    parser.add_argument('--budget-kb', type=float, default=1500)
    arguments = parser.parse_args()
    try:
        manifest = convert_video(arguments.source, arguments.destination, ffmpeg=arguments.ffmpeg,
                                 frames=arguments.frames, width=arguments.width, start=arguments.start,
                                 duration=arguments.duration, quality=arguments.quality, budget_kb=arguments.budget_kb)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(error, file=sys.stderr)
        return 2
    print(f"{manifest['frameCount']} WebP kare: {manifest['sequenceBytes'] / 1000:.1f} KB\nÇıktı: {arguments.destination.resolve()}")
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    sys.exit(main())
