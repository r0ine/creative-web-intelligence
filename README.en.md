# Creative Web Intelligence

Creative Web Intelligence helps coding agents and designers make specific choices about composition, typography, color, motion, scroll, 3D, and media. It includes decision guidance, local checks, and runnable examples. The current release is v9.

v9 is about understanding the user. When someone says a result "doesn't feel right", the agent asks **where** before changing anything; if the answer is "overall", it starts with the most visible surfaces (background, first screen, dominant color, display type) and keeps what the user liked ([revision workflow](reference-engine/REVISION_FEEDBACK.md), Turkish). As the library grows, [rule precedence](v9/RULE_PRECEDENCE.md) records which director wins in each domain and how eight known cross-version contradictions are resolved; the validator fails when new rules are added without being registered.

**Languages:** [Türkçe](README.md) · English

Start with the [English installation and usage guide](docs/INSTALL_EN.md). The short version:

```sh
git clone https://github.com/r0ine/creative-web-intelligence.git
cd creative-web-intelligence
python tools/validate_all.py
node tools/v6/serve_preview.mjs
```

Open `http://127.0.0.1:22222/examples/v7/reference-compare/` to compare a source screenshot with an implementation screenshot at the same dimensions. The tool runs locally in the browser and does not upload either image. The [mobile/3D scroll example](examples/v6/mobile-scroll/index.html) and [media studio](examples/v6/media-studio/index.html) are served by the same command.

The recommended process begins with [brief interpretation and a small reference preview](reference-engine/BRIEF_TO_REFERENCE.md). Before building the whole site, record the chosen visual direction and ask only questions that change the outcome. Use [v7 visual calibration](quality/V7_VISUAL_CALIBRATION.md) to justify color, shape, and motion choices; run the [local CSS audit](tools/v7/audit_visual_defaults.mjs) to catch repeated boxes and default animation patterns. A zero-warning audit is not a visual quality score.

The [v8 source advisor](README_V8.en.md) indexes 46 supplied GitHub links, selects one starting reference, and checks for conflicting templates, UI foundations, motion engines, 3D dependencies and license uncertainty. Read the [source intelligence guide](source-intelligence/V8_SOURCE_INTELLIGENCE.md) before adopting upstream code. Its five review lenses separate README facts from visual questions that still require inspection.

The [optional video and pointer workflow](v8/OPTIONAL_VIDEO_POINTER_WORKFLOW.md) is for CLI agents: finish the site without video, generate a prompt only on explicit request, and add a supplied clip later. The [experience planner](tools/v8/experience_plan.mjs) keeps scroll as the main camera path and pointer motion as a small offset.

Video is optional. The media studio can prepare a prompt to paste into ChatGPT, but there is no ChatGPT or Claude API integration. React Bits, 21st.dev, and other sources are guides for selecting components; their code is not bundled into this library. Check the license of each component you use.

Install the library and `/crative-web` shortcut as Codex skills with `python tools/v7/install_codex_skill.py`. The full workflow, browser URLs, test commands, and update instructions are in the [English guide](docs/INSTALL_EN.md). See the [v9 release notes](RELEASE_NOTES_V9.en.md) and [v8 release notes](RELEASE_NOTES_V8.en.md) for what changed.
