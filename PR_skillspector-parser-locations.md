Title: fix(security): show where SkillSpector parse limits apply in incomplete scans

## Summary

Incomplete SkillSpector scans already carried `parser_diagnostic` on
`static_parse_limit` ledger rows (span, `cause`, and `check`), but the
security check dropped that object. JavaScript helpers such as
`scripts/admission.mjs` therefore appeared as a path with no line and no
reason, even though the scanner named lines 74-170 as
`runtime_dependent` / `command_string_runtime`.

The incomplete-analysis error now labels those rows from a well-formed
diagnostic (`path:74-170`, or `path:11` for a single line), adds sanitized
`cause` and `check` to the bracket context, and, when every parse-limit
row is `runtime_dependent`, appends a short hint to review the reported
lines and prefer fixed argument lists. JSON `skillspector_completeness`
keeps a bounded copy of the diagnostic (no source text or byte offsets).
AE1 suggestions use the same span when the reason has no line of its own
and the evidence includes one. Rows that already have `start_line` are
unchanged. The check stays `INCOMPLETE`. These diagnostics never turn an
incomplete scan into a pass.

Refs #784

## Verification

- [ ] I am familiar with the [Contributing Guidelines](../CONTRIBUTING.md)
- [x] Added or updated focused tests
- [x] Updated documentation for user-visible changes
- [x] Ran `make lint`
- [x] Ran `make test`
- [x] Ran `make build`
- [ ] Did not add credentials, private datasets, or proprietary benchmark content

## Release Impact

- [ ] No user-visible release note needed
- [x] Updated `CHANGELOG.md`

### Commands run

Platform: Linux 6.12.113+ x86_64, Python 3.13.18.

Untouched `upstream/main` (`affe1acc3d0a24877c5d508d96ac69663a7fd92a`):

- `uv run make lint` — All checks passed
- `uv run make test` — hung in `tests/test_harbor_secure_docker_environment.py::test_windows_transfer_repeated_cancellation_reaps_process_and_removes_partial_output` (~29%); killed (EXIT 143). Same hang as in a previous environment.
- `uv run python -m pytest -n auto --tb=line --deselect tests/test_harbor_secure_docker_environment.py::test_windows_transfer_repeated_cancellation_reaps_process_and_removes_partial_output` — 50 failed, 39468 passed, 171 skipped, 65 warnings. Failures are missing Docker client, Rich markup wrapping, and NeMo Gym process-group.
- `uv run make build` — Successfully built `skillevaluator-1.0.1.tar.gz` and `skillevaluator-1.0.1-py3-none-any.whl`
- `./fern/node_modules/.bin/fern check` — Found 0 errors (1 Fern CLI upgrade warning)
- `uv run ruff format --check src/skillevaluator/validators/security.py` — would reformat (pre-existing wrapping)

This branch:

- `uv run make lint` — All checks passed
- `uv run ruff format --check` on the Python files this change adds or edits except `security.py` — 7 files already formatted
- `uv run python -m pytest tests/validators/test_skillspector_parser_locations.py tests/validators/test_skillspector_diagnostics.py tests/validators/test_skillspector_reference_diagnostics.py tests/validators/test_skillspector_hook_surface.py tests/reporting/test_tier3_validate_cases.py` — 261 passed
- `uv run python -m pytest -n auto --tb=line --deselect tests/test_harbor_secure_docker_environment.py::test_windows_transfer_repeated_cancellation_reaps_process_and_removes_partial_output` — 50 failed, 39494 passed, 171 skipped, 65 warnings. The 50 failures are the same set as untouched `upstream/main`. The extra 26 passes are the new parser-location tests. `tests/test_cli.py`, `tests/reporting/`, and `tests/golden/` are in this run.
- `uv run make build` — Successfully built `skillevaluator-1.0.1.tar.gz` and `skillevaluator-1.0.1-py3-none-any.whl`
- `./fern/node_modules/.bin/fern check` — Found 0 errors (same Fern CLI upgrade warning as baseline)

Not verified: serial `make test` without the deselect (it hung on untouched `upstream/main`); live and integration markers (excluded by default); paid or credentialed checks.

## Demo

![demo](https://raw.githubusercontent.com/mvanhorn/pr-demo-assets/main/osc-bulk-1118/skillspector-parser-locations/preview.gif)

Full recording (MP4): https://raw.githubusercontent.com/mvanhorn/pr-demo-assets/main/osc-bulk-1118/skillspector-parser-locations/out.mp4
