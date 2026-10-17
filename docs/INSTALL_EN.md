# Installation and usage

Creative Web Intelligence is a collection of design guidance, local checks, and runnable examples. It does not require a package manager or an API key. Run commands from the repository root.

## Requirements

- Git, Node.js 22 or newer, and Python 3.11 or newer.
- FFmpeg only if you want to convert a video into WebP frames.
- A current Chromium, Firefox, or Safari browser. The live 3D example requires WebGL.

```sh
git clone https://github.com/r0ine/creative-web-intelligence.git
cd creative-web-intelligence
python tools/v8/validate_v8.py
```

The validator also checks earlier catalogs and runs the v7 Node tests. Use the corresponding executable names if Python or Node are installed under different names on your system.

## Run the local examples

```sh
node tools/v6/serve_preview.mjs
```

The server binds only to `127.0.0.1:22222`. If that port is occupied, it leaves the other process alone; set `CWI_PREVIEW_PORT` to an available port. Stop the server with `Ctrl+C`. Open the examples over local HTTP rather than `file://`, because they use JavaScript modules.

| Example | URL |
| --- | --- |
| Reference comparison | `http://127.0.0.1:22222/examples/v7/reference-compare/` |
| Mobile/3D scroll | `http://127.0.0.1:22222/examples/v6/mobile-scroll/` |
| Media studio | `http://127.0.0.1:22222/examples/v6/media-studio/` |
| One-screen reference preview | `http://127.0.0.1:22222/examples/v6/reference-first/reference-preview.html` |

## Install as Codex skills

```sh
python tools/v7/install_codex_skill.py
```

This copies the main library to `~/.codex/skills/creative-web-intelligence` and the shortcut to `~/.codex/skills/crative-web`. It updates files in existing skills with those names and avoids installing the nested shortcut twice. Pass an absolute path with `--skills-dir` if Codex uses another skills directory. In a new chat, write:

```text
/crative-web Design a mobile page with native scrolling. Use 3D only to explain the product's construction, and make a short visual reference before building the full page.
```

For another coding assistant, provide the repository's `SKILL.md` and `START_HERE_V8.md` as context. The `/crative-web` shortcut only works in environments that support installed skills.

## Workflow

1. For a new site, clarify the brief with `reference-engine/BRIEF_TO_REFERENCE.md`. Make one small working preview and a short note before the full build. Do not restart this step for a minor edit.
2. If no source was supplied, choose one starting reference with the v8 advisor. Inspect its card and verify desktop/mobile behavior before reusing code. Check compatibility and licensing:

```sh
python tools/v8/source_advisor.py --surface portfolio --framework next --motion 3d
python tools/v8/source_advisor.py --source ibelick/motion-primitives
python tools/v8/source_advisor.py --check greensock/gsap framer/motion --framework react
```

3. Explain palette, geometry, and motion choices with `quality/V7_VISUAL_CALIBRATION.md`. Choose media with `v6/MEDIA_DECISION_ENGINE.md`.
4. Capture the source and implementation at the same viewport and scroll position, then load both images in the reference comparison tool. Overlay and heatmap views expose structural differences; test behavior and accessibility separately. PNG, JPG, and WebP are supported. Limits are 25 MB per file and 8 million pixels per image. Files stay in the browser.
5. Check CSS for repeated boxes and default motion patterns:

```sh
node tools/v7/audit_visual_defaults.mjs examples/v7/reference-compare
```

Zero findings do not prove good design. Review the actual desktop and mobile pages.

## Scroll, media, and optional video

The mobile/3D example uses native scrolling to control a Three.js scene on desktop, local WebP frames on mobile, and static images when reduced motion or data saving is preferred. Start with `runtime/scroll/README.md` and `runtime/three/README.md` when adapting it, including the example's poster and cleanup behavior.

The media studio filters React Bits, 21st.dev, and other sources by task. The catalog does not embed their source code; verify the selected component's license and dependencies. Video is optional. Clicking the prompt button creates text to paste into ChatGPT manually; it does not connect to ChatGPT or Claude APIs.

To generate the same brief from the CLI:

```sh
node tools/v6/creative_media.mjs prompt examples/v6/video-brief.json
```

If you have a local video and FFmpeg, follow `runtime/media/README.md` to create a poster and scroll frames. A prompt alone does not create a playable asset.

## Tests

```sh
python tools/v8/validate_v8.py
python -m unittest discover -s tests -v
node --test tests/*.test.mjs
```

FFmpeg integration tests are skipped unless `CWI_TEST_FFMPEG` points to its executable. Catalog and comparison tests need no extra packages. To update an installed skill, run `git pull` in the repository and then rerun `install_codex_skill.py`.
