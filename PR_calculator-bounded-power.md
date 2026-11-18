Title: fix(calculator): bound powers and report non-real or oversized results

## Summary

The calculator reference skill evaluated `**` with `operator.pow` and no size
check. On upstream `main` (`affe1acc`), `timeout 10 python scripts/calc.py "9**9**9"`
exits 124 after computing a ~370-million-digit integer. `(-8)**(1/3)` reaches
`int()` as a complex value, `10.0**400` and `1e308*10` fail with overflow or
infinity conversion errors, and `True+True` prints `Result: 2` because `bool`
passes the `(int, float)` constant check.

`safe_eval` now rejects Boolean and other non-int/float constants, estimates
integer powers with `abs(exp) * log10(abs(base))` against `MAX_RESULT_DIGITS`
(1000) at every `**` (including nested right-associative powers), and reports
`Error: result is too large` or `Error: result is not a real number` on stderr
with exit code 1. Documented examples, `2**64`, `2**-2`, and the division-by-zero
message are unchanged. Conversion and percentage regexes are not modified.

Reproduced on upstream `affe1acc`: `timeout 10 python scripts/calc.py "9**9**9"` exits 124; `(-8)**(1/3)`, `10.0**400`, and `1e308*10` fail with conversion errors; `True+True` prints `Result: 2`.

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

Platform: Linux 6.12.113+ x86_64, Python 3.13.18 (uv), on top of upstream `affe1acc`.

- Baseline (untouched `upstream/main` worktree):
  - `uv run make lint` — All checks passed.
  - `PYTHONUNBUFFERED=1 PYTEST_ADDOPTS='--deselect tests/test_harbor_secure_docker_environment.py::test_windows_transfer_repeated_cancellation_reaps_process_and_removes_partial_output' uv run make test` — 57 failed, 39461 passed, 171 skipped, 20 deselected, 65 warnings in 1908.70s. The deselected test hung on untouched `upstream/main` in a past run; the 57 failures match Docker-client, 80-column wrapping, NeMo Gym, and related gaps in this environment.
  - `uv run make build` — Successfully built `skillevaluator-1.0.1.tar.gz` and `skillevaluator-1.0.1-py3-none-any.whl`.
- This branch:
  - `uv run make lint` — All checks passed.
  - `uv run ruff format --check` on `scripts/calc.py` and `tests/test_reference_calculator.py` — 2 files already formatted.
  - `uv run pytest -n 0 tests/test_reference_calculator.py` — 24 passed in 0.53s.
  - `uv run pytest -n 0 tests/test_reference_calculator.py tests/test_cli.py tests/golden` — 392 passed in 12.05s.
  - `uv run pytest -n 0 tests/reporting tests/test_reference_calculator.py` — 15 failed, 2835 passed, 86 skipped in 147.44s. The 15 failures reproduce on untouched `upstream/main` (80-column wrapping).
  - `PYTHONUNBUFFERED=1 PYTEST_ADDOPTS='--deselect tests/test_harbor_secure_docker_environment.py::test_windows_transfer_repeated_cancellation_reaps_process_and_removes_partial_output' uv run make test` — 57 failed, 39475 passed, 171 skipped, 20 deselected, 65 warnings in 1896.72s. The 57 failures are the same nodeids as the baseline (plus 14 passes from the new calculator cases). `make test` is therefore left unticked.
  - `uv run make build` — Successfully built `skillevaluator-1.0.1.tar.gz` and `skillevaluator-1.0.1-py3-none-any.whl`.

Not verified: `./fern/node_modules/.bin/fern check` (no `docs/*.mdx` change); Python 3.12/3.14 as the gate Python; Windows; a live Docker client for the Harbor secure-environment tests.

## Demo

![demo](https://raw.githubusercontent.com/mvanhorn/pr-demo-assets/main/osc-bulk-1118/calculator-bounded-power/preview.gif)

Full recording (MP4): https://raw.githubusercontent.com/mvanhorn/pr-demo-assets/main/osc-bulk-1118/calculator-bounded-power/out.mp4
