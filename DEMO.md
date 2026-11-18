# Demo: SkillSpector parser locations in incomplete scans

Replay of real captured command output. The scan stays incomplete by design.

## What changed

Tier 1 security on `TheColliery/CoalFace` `skills/coalface` at
`f7574dfb45ec5eb7bb4861ea2a9efb020a66cf86` is `INCOMPLETE` because SkillSpector
2.13.4 records `static_parse_limit` on `scripts/admission.mjs` and
`scripts/machine-reading.mjs`. Those ledger rows have `start_line: null`. The
scanner JSON already has `parser_diagnostic` with the span, `cause`, and
`check`. SkillEvaluator dropped that object.

After this change the incomplete-analysis error names
`scripts/admission.mjs:74-170 [...runtime_dependent command_string_runtime...]`
and, when every parse-limit row is `runtime_dependent`, adds a short hint.
JSON `skillspector_completeness` keeps a bounded copy of `parser_diagnostic`.
The check remains `INCOMPLETE`.

## Commands

See `commands.log`. Before: untouched `upstream/main` at `affe1acc`. After:
`feat/skillspector-parser-locations`.

1. `uv run skillevaluator tier1 .../skills/coalface --no-llm --checks security -r cli -r json`
   before: `scripts/admission.mjs [static; static_parse_limit; analyzers=...]`
   after: `scripts/admission.mjs:74-170 [static; static_parse_limit; runtime_dependent command_string_runtime; analyzers=...]`
2. `sed -n '74,80p'` and `sed -n '143,147p'` on `scripts/admission.mjs`: the
   parser span starts at line 74; `spawnSync(process.execPath, ...)` is line 145.
3. JSON `results[0].skillspector_completeness.records[0].ledger_exceptions`
   includes `parser_diagnostic` with `cause`, `check`, `start_line`, `end_line`,
   `unchecked_scope`, `full_input_checked`, and no source offsets.

## Media

- `out.mp4`: 1920x1080, 30 fps, H.264, yuv420p, ~37 s
- `preview.gif`: 1280x720, 10 fps, under 5 MB
