# Windows Workflow

Recommended project flow in PowerShell/Windows Terminal:

1. clone/copy the intelligence library next to the active project,
2. point the coding agent at `prompts/v3/MASTER_META_PROMPT_V3.md`,
3. if reference media exists, create a reference workspace,
4. optionally extract video frames with FFmpeg,
5. create the creative/full-stack spec,
6. implement in the actual project repository,
7. run browser/dev-server captures and tests from that project,
8. store only analysis/specs that are useful; do not blindly vendor the whole intelligence library into every production bundle.

The intelligence library should normally stay separate from shipped website code.
