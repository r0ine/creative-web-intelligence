import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('video_to_web', ROOT / 'tools/v6/video_to_web.py')
converter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(converter)


class VideoInputTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.source = self.root / 'source.mp4'
        self.source.write_bytes(b'local video fixture')
        self.destination = self.root / 'export'

    def test_existing_directory_is_preserved(self):
        self.destination.mkdir()
        marker = self.destination / 'keep.txt'
        marker.write_text('keep')
        with self.assertRaisesRegex(ValueError, 'zaten var'):
            converter.convert_video(self.source, self.destination)
        self.assertEqual(marker.read_text(), 'keep')

    def test_invalid_options_fail_before_launching_ffmpeg(self):
        for options in ({'frames': 4}, {'frames': True}, {'width': 9000}, {'quality': 0}, {'start': float('nan')}, {'budget_kb': 0}):
            with self.subTest(options=options), patch.object(converter, 'run_ffmpeg') as launch:
                with self.assertRaises(ValueError):
                    converter.convert_video(self.source, self.destination, **options)
                launch.assert_not_called()

    def test_missing_ffmpeg_has_an_actionable_error(self):
        with patch.object(converter.shutil, 'which', return_value=None):
            with self.assertRaisesRegex(ValueError, '--ffmpeg'):
                converter.find_ffmpeg()

    def test_duration_parser_handles_long_clips_and_refuses_unknown_duration(self):
        with patch.object(converter, 'run_ffmpeg', return_value=subprocess.CompletedProcess([], 0, '', 'Duration: 01:02:03.50, start: 0')):
            self.assertEqual(converter.video_duration('ffmpeg', self.source), 3723.5)
        with patch.object(converter, 'run_ffmpeg', return_value=subprocess.CompletedProcess([], 0, '', 'Duration: N/A')):
            with self.assertRaises(ValueError):
                converter.video_duration('ffmpeg', self.source)

    def test_failed_encoding_does_not_leave_an_export(self):
        with patch.object(converter, 'find_ffmpeg', return_value=Path('ffmpeg')), patch.object(converter, 'video_duration', return_value=8), patch.object(converter, 'run_ffmpeg', side_effect=ValueError('decode failed')):
            with self.assertRaisesRegex(ValueError, 'decode failed'):
                converter.convert_video(self.source, self.destination)
        self.assertFalse(self.destination.exists())
        self.assertEqual(list(self.root.iterdir()), [self.source])


@unittest.skipUnless(os.environ.get('CWI_TEST_FFMPEG'), 'CWI_TEST_FFMPEG ayarlı değil; FFmpeg entegrasyonu atlandı')
class VideoEncodingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scratch = tempfile.TemporaryDirectory()
        cls.root = Path(cls.scratch.name)
        cls.source = cls.root / 'source.mp4'
        cls.binary = Path(os.environ['CWI_TEST_FFMPEG'])
        converter.run_ffmpeg(cls.binary, ['-f', 'lavfi', '-i', 'testsrc2=size=320x180:rate=24:duration=2',
                                         '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(cls.source)])

    @classmethod
    def tearDownClass(cls):
        cls.scratch.cleanup()

    def test_actual_export_contains_exact_frames_and_content_hashes(self):
        destination = self.root / 'converted'
        manifest = converter.convert_video(self.source, destination, ffmpeg=self.binary, frames=24, width=240)
        self.assertEqual(len(manifest['frames']), 24)
        self.assertEqual(manifest['frameCount'], 24)
        self.assertLessEqual(manifest['sequenceBytes'], 1_500_000)
        for record in [*manifest['frames'], manifest['poster'], manifest['background']]:
            path = destination / record['file']
            self.assertEqual(record['sha256'], converter.sha256(path))
            self.assertEqual(record['bytes'], path.stat().st_size)
        self.assertEqual(json.loads((destination / 'manifest.json').read_text(encoding='utf-8')), manifest)
        self.assertEqual(manifest['review']['temporalArtifacts'], 'pending')

    def test_budget_failure_leaves_no_destination(self):
        destination = self.root / 'too-large'
        with self.assertRaisesRegex(ValueError, 'bütçesini aşıyor'):
            converter.convert_video(self.source, destination, ffmpeg=self.binary, frames=24, budget_kb=1)
        self.assertFalse(destination.exists())

    def test_segment_cannot_extend_past_source(self):
        with self.assertRaisesRegex(ValueError, 'dışına taşmamalı'):
            converter.convert_video(self.source, self.root / 'past-end', ffmpeg=self.binary, start=1, duration=3)


if __name__ == '__main__':
    unittest.main()
