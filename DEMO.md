# Demo: pre-commit hooks for offline Tier 1 skill checks

Replay of real captured command output from a scratch consumer repo at
`/tmp/precommit-hooks-demo`. The consumer pointed `pre-commit` at this
SkillEvaluator checkout (`rev` `dccfbcacf818230ca63fd2b250719bce1e2f095b`)
and used only the three shipped offline hooks.

Platform: Linux 6.12 x86_64, Python 3.12.3.

## What the session showed

1. `pre-commit try-repo /workspace --all-files --verbose` against the
   starter `text-analyzer` skill (default hook `min-score` 70):
   - `PASS  text-analyzer  lint-scripts`
   - `PASS  text-analyzer  quality  88.8/100`
   - `PASS  text-analyzer  schema`
   - exit 0
2. `pre-commit install` then a first commit of that skill with
   `--min-score 85` in the consumer config: all three hooks Passed.
3. Shorten the skill `description` to `Text statistics.` and try to
   commit: quality Failed with `FAIL  text-analyzer  quality  82.5/100  (min 85)`,
   schema and lint Passed, commit exit 1.
4. Restore a complete description and commit again: all three hooks Passed.
5. `pre-commit run --all-files --verbose` on the fixed tree:
   `PASS  text-analyzer  quality  88.8/100`, schema and lint Passed.

## Artifacts

- `out.mp4` — 1920x1080, 30 fps, H.264 yuv420p, 40.83 s
- `preview.gif` — 1280x720, 8 fps, 1.6 MiB
- `commands.log` — captured stdout/stderr and exit codes
- `logs/ffprobe.txt` — ffprobe for the MP4 and GIF
- `logs/make-lint.txt`, `logs/make-test.txt`, `logs/make-build.txt`,
  `logs/fern-check.txt` — verification from this checkout

The MP4/GIF are labeled "Replay of real captured command output".
The original session is in `commands.log`.
