Title: feat(reporting): add a GitHub Actions annotations report format

## Summary

`-r github` prints GitHub Actions workflow commands on stdout so a job that
runs `skillevaluator validate` or `tier1` itself can put findings on the pull
request diff and the run summary without uploading SARIF. The format writes
no file, needs no extra permission, and combines with other formats, for
example `-r cli,github,sarif`.

A CLI-only workflow currently has the terminal table, Markdown, or SARIF.
SARIF inline comments need a code scanning upload, which private
repositories without code scanning cannot use.

none

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

Platform: Linux 6.12.113+ x86_64, Python 3.13.18 (uv), `python3` 3.12.3.

Baseline on untouched `upstream/main` `affe1acc3d0a24877c5d508d96ac69663a7fd92a`:

- `uv run make lint` — All checks passed
- `uv run python -m pytest tests/reporting` — 15 failed, 2943 passed, 86 skipped in 143.81s. Failures are Rich markup, 80-column terminal polish, and token-usage wrapping
- `uv run make build` — Successfully built `skillevaluator-1.0.1.tar.gz` and `skillevaluator-1.0.1-py3-none-any.whl`
- `PYTHONUNBUFFERED=1 PYTEST_ADDOPTS='--deselect tests/test_harbor_secure_docker_environment.py::test_windows_transfer_repeated_cancellation_reaps_process_and_removes_partial_output' uv run make test` — 57 failed, 39461 passed, 171 skipped, 20 deselected, 65 warnings in 1627.79s. Failures are this environment (no Docker client, Rich markup / 80-column wrapping, NeMo Gym process-group). The deselected test hung on untouched main here.

This branch:

- `uv run ruff format --check` on the touched Python files — 11 files already formatted (plus `tests/reporting/test_reporters.py` after the non-UTF-8 wiring case)
- `uv run make lint` — All checks passed
- `uv run python -m pytest tests/reporting/test_github_reporter.py tests/reporting/test_incomplete_scans.py tests/reporting/test_plugin_reports_runtime_composition.py tests/reporting/test_reporters.py tests/test_cli.py tests/golden/test_cli_surface.py` — 389 passed in 3.43s
- `uv run python -m pytest tests/reporting tests/test_cli.py tests/golden` — 15 failed, 3203 passed, 86 skipped in 136.88s. The 15 failures are the same names as the baseline reporting suite
- `uv run make build` — Successfully built `skillevaluator-1.0.1.tar.gz` and `skillevaluator-1.0.1-py3-none-any.whl`
- `./fern/node_modules/.bin/fern check` — Found 0 errors and 1 warning (Fern CLI upgrade notice)
- `PYTHONUNBUFFERED=1 PYTEST_ADDOPTS='--deselect tests/test_harbor_secure_docker_environment.py::test_windows_transfer_repeated_cancellation_reaps_process_and_removes_partial_output' uv run make test` — 58 failed, 39484 passed, 171 skipped, 20 deselected, 65 warnings in 1627.84s. Passed count is +23 versus baseline: 24 new GitHub-annotation tests, minus one existing test that failed here only (`tests/test_nvidia_build_bridge.py::test_dynamic_bridge_ignores_prebound_old_port_and_checker_authenticates_health`, `Address already in use` from running the two suites at the same time). That test passed in 2.39s when re-run alone. The other failures match the baseline.

Not verified: a live GitHub Actions job annotating a pull request; Python 3.12 and 3.14; Windows.

## Demo

![demo](https://raw.githubusercontent.com/mvanhorn/pr-demo-assets/main/osc-bulk-1118/github-annotations/preview.gif)

Full recording (MP4): https://raw.githubusercontent.com/mvanhorn/pr-demo-assets/main/osc-bulk-1118/github-annotations/out.mp4
