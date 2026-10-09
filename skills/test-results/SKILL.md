---
name: test-results
description: Compare, summarize and re-run DejaGnu results with contrib/ scripts (compare_tests, dg-cmp-results, test_summary, repro_fail, test_recheck).
---
# Skill: test-results

Inputs are `.sum` / `.log` files from `make check` in a build directory.
Running tests is subject to the Host Gate in `AGENTS.md`. Comparing existing
`.sum` files works on any host (plain shell/awk).

## Compare baseline vs patched
```sh
contrib/compare_tests <baseline-build-dir> <patched-build-dir>     # all *.sum under both
contrib/compare_tests base/gcc.sum new/gcc.sum                      # two files
contrib/dg-cmp-results.sh "" base/gcc.sum new/gcc.sum               # PASS->FAIL only
contrib/dg-cmp-results.sh -v "" base/gcc.sum new/gcc.sum            # + FAIL->PASS
```
- `compare_tests` exit status: 0 nothing of interest; non-zero = differences. Add `-strict` to also count new/missing tests.
- `dg-cmp-results.sh` first argument is the variant (`""` = first variant; write `/` as `\/`).
- Baseline and patched must use the same configure options, `RUNTESTFLAGS` and source revision.
- Results live in `<build>/gcc/testsuite/gcc/gcc.sum`, `.../g++/g++.sum`, etc.

## Summarize a run
```sh
contrib/test_summary -t | more
```
Prints a shell script containing the summary (configure line, FAIL/XPASS list, totals).
`-t` keeps the log files in place. Never pipe it to `sh`: that e-mails the report to
gcc-testresults and renames the logs.

## Merge parallel results
`contrib/dg-extract-results.sh [-t tool] sum-file... > merged.sum` (`make check -jN` already does this).

## Re-run failures (Power host, ask first)
| Script | Does |
|--------|------|
| `contrib/test_recheck -n <build-dir>` | list the commands that would re-run only failed tests; drop `-n` to run |
| `contrib/repro_fail <pattern> <file.log>` | re-execute the exact compile command of one test from a `.log`; `--debug` runs it under gdb |
| `make check-gcc RUNTESTFLAGS="powerpc.exp=<test>.c"` | re-run named tests |

## Known-failure manifest
`contrib/testsuite-management/validate_failures.py --build_dir=<build>`: compare failures
against a manifest. `--produce_manifest` writes one from a baseline run; later runs then report only new failures.

## Lint tests
`contrib/dg-lint/dg-lint <test files>` detects common DejaGnu directive mistakes.
Needs `libgdiagnostics.so` from a GCC build; skip when it is not available.

## Report format for the user
New FAILs (test + line), FAIL→PASS, new UNRESOLVED/ERROR, totals before/after. Do not list unchanged results.
