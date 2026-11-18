# Calculator bounded-power demo

Real `scripts/calc.py` runs against untouched `upstream/main`
(`affe1acc3d0a24877c5d508d96ac69663a7fd92a`, git worktree `/tmp/se-upstream`)
and against `feat/calculator-bounded-power`.

## What was captured

1. Before: `timeout 10 python ... "9**9**9"` — no output, exit 124 after 10 s.
2. Before: `"(-8)**(1/3)"` — `Error: int() argument must be a string, a bytes-like object or a real number, not 'complex'`.
3. Before: `"10.0**400"` — `Error: (34, 'Numerical result out of range')`.
4. Before: `"1e308*10"` — `Error: cannot convert float infinity to integer`.
5. Before: `"True+True"` — `Result: 2`.
6. After: `"9**9**9"` and `"10**10**10"` — `Error: result is too large`, exit 1 immediately.
7. After: `"(-8)**(1/3)"` — `Error: result is not a real number`.
8. After: `"10.0**400"` and `"1e308*10"` — `Error: result is too large`.
9. After: `"True+True"` — `Error: Unsupported value: bool`.
10. After: `"2**64"`, `"15% of 200"`, `"100 celsius to fahrenheit"`, `"2 ** 10"` unchanged.
11. After: `"2**-2"` → `Result: 0.25`; `"1/0"` → `Error: division by zero`.
12. After: `pytest -n 0 tests/test_reference_calculator.py -q` — 24 passed.

`out.mp4` is an ffmpeg replay of `commands.log` (banner text:
"Replay of real captured command output"). The first nested-power command is
held for 10 s with no result, matching the captured hang. `preview.gif` is
derived from that MP4.

## Commands

See `commands.log` for the exact invocations, exit codes, and captured
stdout/stderr. Media probe output is in `logs/ffprobe.txt`.
