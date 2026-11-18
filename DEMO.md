# Demo: doctor --json readiness output

Replay of real captured command output from a clean uv venv at
`/tmp/doctor-json-demo` with an editable install of this checkout
(`skillevaluator[all]`, Python 3.13.18). Table output on untouched
upstream `affe1acc` was captured with `PYTHONPATH=/tmp/se-baseline/src`.

Platform: Linux 6.12.113+ x86_64.

## What the session showed

1. `skillevaluator doctor --tier 1` on upstream main: Rich table, Semgrep
   missing, exit 1.
2. The same command on this branch: the table matches the upstream
   capture byte-for-byte, exit 1.
3. `skillevaluator doctor --tier 1 --json | python -m json.tool`: one
   JSON object on stdout, `command` `doctor`, Semgrep `fail`, exit 1.
4. `SKILLEVALUATOR_SEMGREP_PATH=/nonexistent/semgrep` with the same
   command: Semgrep detail is the malformed-override message, `echo $?`
   prints 1.
5. `jq '.tiers[].checks[] | select(.status=="fail")'` on that JSON:
   one fail row named Semgrep.
6. `skillevaluator health-check --tier all --json`: `command` is
   `health-check`, tiers `1`, `2`, `3` in order, top-level `status`
   `fail`, exit 1.

`out.mp4` is an xfce4-terminal replay of `commands.log` with the banner
"Replay of real captured command output". `preview.gif` is derived from
that MP4 with ffmpeg palettegen/paletteuse.

## Artifacts

- `out.mp4` — 1920x1080, 30 fps, H.264 yuv420p, 38.00 s, 1140 frames
- `preview.gif` — 1280x720, 8 fps, 609 KiB
- `commands.log` — captured stdout/stderr and exit codes
- `logs/ffprobe.txt` — ffprobe for the MP4 and GIF
- `logs/` — lint, build, fern, and focused test output from this checkout
