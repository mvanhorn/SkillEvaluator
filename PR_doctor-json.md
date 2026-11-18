Title: feat(doctor): add --json readiness output

## Summary

`doctor`, `health-check`, and `tier3 doctor` print the same readiness rows
as one JSON object when `--json` is passed, so a CI job can read which
scanner or credential failed without scraping a terminal table. Default
table output, probes, row text, and exit codes are unchanged: 0 when no
row fails, 1 when any row fails (`warn` does not fail). Click usage
errors still exit 2 and print to stderr, not JSON. Guided installation
is not part of this change.

Refs #42

## Verification

- [ ] I am familiar with the [Contributing Guidelines](../CONTRIBUTING.md)
- [x] Added or updated focused tests
- [x] Updated documentation for user-visible changes
- [x] Ran `make lint`
- [ ] Ran `make test`
- [x] Ran `make build`
- [ ] Did not add credentials, private datasets, or proprietary benchmark content

## Release Impact

- [ ] No user-visible release note needed
- [x] Updated `CHANGELOG.md`

### Commands run

Platform: Linux 6.12.113+ x86_64, Python 3.13.18.

Baseline on untouched upstream `affe1acc3d0a24877c5d508d96ac69663a7fd92a`:

- `uv run make lint` — All checks passed
- `uv run ruff format --check` on the Python files later touched — 5 files already formatted
- `uv run make build` — Successfully built `skillevaluator-1.0.1.tar.gz` and `skillevaluator-1.0.1-py3-none-any.whl`

On `feat/doctor-json`:

- `uv run make lint` — All checks passed
- `uv run ruff format --check src/skillevaluator/doctor.py src/skillevaluator/cli.py src/skillevaluator/tier3/commands.py tests/test_doctor.py tests/test_cli.py` — 5 files already formatted
- `uv run pytest tests/test_doctor.py tests/test_cli.py (doctor/health-check/json cases) tests/golden/test_cli_surface.py` — 110 passed
- `uv run pytest tests/test_cli.py` — 185 passed, 2 failed; the same two fail on untouched upstream (`test_quickstart_quality_check_matches_documented_result[90-1]`, `test_validate_code_integrity_reports_only_static_test_evidence`)
- `uv run pytest tests/reporting/` — 2811 passed, 86 skipped, 15 failed; the failures are Rich wrap-width assertions that also fail on untouched upstream in this environment (console width 80)
- `uv run make build` — Successfully built `skillevaluator-1.0.1.tar.gz` and `skillevaluator-1.0.1-py3-none-any.whl`
- `./fern/node_modules/.bin/fern check` — Found 0 errors and 1 warning
- Full `uv run make test` (39690 selected) was started on the frozen upstream tip and had not finished in this environment; it was not re-run to completion on this branch. The hung Harbor Windows-transfer case from earlier reports was not observed here because that full run did not complete.

## Demo

![demo](https://raw.githubusercontent.com/mvanhorn/pr-demo-assets/main/osc-bulk-1118/doctor-json/preview.gif)

Full recording (MP4): https://raw.githubusercontent.com/mvanhorn/pr-demo-assets/main/osc-bulk-1118/doctor-json/out.mp4
