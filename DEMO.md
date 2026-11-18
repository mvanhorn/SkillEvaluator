# Demo: GitHub Actions annotations (`-r github`)

This recording is a replay of real captured command output. Exact commands,
exit codes, and stdout/stderr are in `commands.log`.

## Environment

- Platform: Linux 6.12.113+ x86_64
- Python: 3.13.18 (uv-managed)
- Package: skillevaluator 1.0.1
- Feature branch: `feat/github-annotations` from upstream `affe1acc3d0a24877c5d508d96ac69663a7fd92a`
- Before: the same CLI from a worktree at that untouched tip

Skills used only for this demo (temp directories, not in the product tree):

- `seeded` — invalid `name`, short description, lint findings
- `payload` — `name` contains a newline plus `::add-mask::` and `::stop-commands::`
- `many` — sixteen scripts with destructive commands so security emits more than 10 errors

## What the recording shows

1. **Before.** `skillevaluator validate … -r github` on untouched main exits 2:
   `'github' is not one of 'cli', 'json', 'html', 'markdown', 'sarif', 'junit'`.
2. **After, seeded failures.** `-r cli,github` with `--checks schema,quality,pii,lint`
   prints `::error` (including `file=SKILL.md`), `::warning`, and a summary
   `::notice` that 4 more findings were not annotated. Exit 1.
3. **After, planted payload.** Schema-only `-r github` prints one `::error` line
   containing `%0A::add-mask::planted-secret` and `::stop-commands::tok`. Exit 1.
   No new workflow command starts.
4. **After, cap.** `-r github --checks security` prints 10 `::error` lines with
   `file=` and `line=`, an incomplete-scan `::warning`, and
   `55 more were not annotated`. Exit 1.

## Media

| File | Spec |
| --- | --- |
| `out.mp4` | 1920x1080, 30 fps, H.264, yuv420p, 33.77 s |
| `preview.gif` | 1280x720, 10 fps, 941637 bytes |
| `commands.log` | Real CLI capture, including before/after |
| `logs/ffprobe.txt` | ffprobe for both media files |

Hold times: each key moment about 3 s or longer; final frame about 5.5 s.
