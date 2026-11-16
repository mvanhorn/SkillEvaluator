# JUnit report demo

Real `quality-check -r cli,junit` runs against the packaged text-analyzer
skill, plus the same XML rendered by `junit2html`.

## What was captured

1. `quality-check` on the original starter skill (`--min-score 80`) — exit 0,
   six JUnit cases, zero failures. Warning findings appear in `<system-out>`.
2. The generated `skillevaluator-quality.junit.xml` for that pass.
3. `quality-check` on a shortened copy of the same skill — exit 1, quality
   score 72.8/100 below the 80 threshold. The gate failure is a `<failure>`
   named `gate_failure`.
4. The generated fail XML.
5. `junit2html` rendering of both XML files (offline scratch venv).
6. Browser screenshots of the pass report, the fail report, and the fail
   report scrolled to the gate failure.

`out.mp4` is a Playwright recording of a replay of `commands.log` (banner
text: "Replay of real captured command output") followed by the `junit2html`
pages. `preview.gif` is derived from that MP4.

## Commands

See `commands.log` for the exact invocations, exit codes, and captured
stdout/stderr. Media probe output is in `logs/ffprobe.txt`.
