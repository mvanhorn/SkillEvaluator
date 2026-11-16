Title: feat(reporting): add a JUnit XML report format

## Summary

`skillevaluator` now writes JUnit XML with `-r junit` (file extension
`.junit.xml`) so CI systems that ingest test reports can show each check
group as a test suite. Failures include `file:line` when a finding records a
location. Checks that did not run and scanners that did not complete are
`<skipped>` rather than passing cases, so an incomplete scan cannot look like
an all-passed report. Non-failing findings stay in `<system-out>`. Gate
failures such as a quality score below the required minimum remain
`<failure>` even when finding severity is only a warning. File paths are
relative to the scanned root, using the same resolution rules as the SARIF
reporter. Characters XML 1.0 forbids are stripped.

GitLab can attach the file with `artifacts:reports:junit`. Other `-r` formats
and command exit codes are unchanged.

## Verification

- [ ] I am familiar with the [Contributing Guidelines](../CONTRIBUTING.md)
- [x] Added or updated focused tests
- [x] Updated documentation for user-visible changes
- [x] Ran `make lint`
- [ ] Ran `make test`
- [x] Ran `make build`
- [ ] Did not add credentials, private datasets, or proprietary benchmark content

Commands run on Linux 6.12.113+ x86_64, Python 3.12.3, uv-managed venv:

- `uv run make lint` — All checks passed.
- `uv run pytest` on focused JUnit coverage (`tests/reporting/test_junit_reporter.py`, incomplete-scan JUnit case, non-UTF8 filename parametrize, catalog collision, publisher sparse-checkout) — 25 passed in 1.98s.
- `uv run make test` — 54 failed, 35695 passed, 173 skipped, 19 deselected in 1677.36s. None of the failures are the new JUnit tests. The 21 non-Harbor failures in that set reproduce on untouched `upstream/main` (`cc3563e5`) in this environment (80-column wrapping). Harbor timeout and redaction tests hang or fail here; they were not used to judge this change.
- `uv run make build` — built `skillevaluator-0.9.0.tar.gz` and `skillevaluator-0.9.0-py3-none-any.whl`.
- `./fern/node_modules/.bin/fern check` — 0 errors.

Not verified: GitLab/Jenkins/Azure/CircleCI/Buildkite ingesting the XML in a
live pipeline; Python 3.13 and 3.14; Windows.

## Release Impact

- [ ] No user-visible release note needed
- [x] Updated `CHANGELOG.md`

## Demo

![demo](https://raw.githubusercontent.com/mvanhorn/pr-demo-assets/main/osc-bulk-1116/junit-report/preview.gif)

Full recording (MP4): https://raw.githubusercontent.com/mvanhorn/pr-demo-assets/main/osc-bulk-1116/junit-report/out.mp4
