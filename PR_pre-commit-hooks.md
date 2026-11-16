Title: feat: add pre-commit hooks for offline Tier 1 skill checks

## Summary

SkillEvaluator now ships three pre-commit hooks so a skill repository can
run the same offline Tier 1 checks that already exist as CLI commands
(`quality-check`, `validate --tiers 1 --checks schema`, `lint-scripts`)
on every commit that touches a skill.

Hooks map each staged path to the nearest ancestor that contains
`SKILL.md`, skip files outside a skill tree, skip deleted skills, and
print one compact `PASS`/`FAIL` line per skill. They stay fully offline:
no doctor, no security-scan, no default `validate`, no rubric, and no
Tier 2/3 work. Consumers can raise the quality bar with
`args: ["--min-score", "85"]`.

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

Platform: Linux 6.12 x86_64, Python 3.12.3.

- `uv run make lint` — All checks passed
- `PYTHONUNBUFFERED=1 PYTEST_ADDOPTS='--deselect tests/test_harbor_secure_docker_environment.py::test_windows_transfer_repeated_cancellation_reaps_process_and_removes_partial_output' uv run make test` — 53 failed, 35695 passed, 170 skipped, 20 deselected. `tests/test_precommit.py` (13 functions) passed. The deselected test hung on untouched `upstream/main` in this environment; the other failures match the same environment gaps on `upstream/main` (no Docker client, Rich markup, NeMo Gym process-group).
- `uv run make build` — Successfully built `skillevaluator-0.9.0.tar.gz` and `skillevaluator-0.9.0-py3-none-any.whl`
- `./fern/node_modules/.bin/fern check` — Found 0 errors

## Demo

https://github.com/mvanhorn/SkillEvaluator/tree/demo/pre-commit-hooks
