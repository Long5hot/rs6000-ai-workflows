# Regression Task Template

Copy this file to `.ai/work/<task-name>/TASK.md` and fill in each section.
Delete this instruction line before use.

---

## Summary

<!-- One sentence: what regression is being investigated? -->


## Task Name

<!-- Short identifier: e.g., pr120384-regress, vec-add-regression -->


## Status

<!-- Investigating / Root cause found / Fix in progress / Fixed / Closed -->


## Failing Testcase

<!-- Paste the test name and failure message from DejaGnu. -->

Test:
```
FAIL: gcc.target/powerpc/<test>.c <scan>
```

Failure detail:
```
```

How to reproduce:
```sh
make check-gcc RUNTESTFLAGS="powerpc.exp=<test>.c"
```


## Expected Behavior

<!-- What should happen? What did this test verify before the regression? -->


## Observed Behavior

<!-- What actually happens now? -->

Actual assembly / output:
```
```


## Failure Classification

<!-- Mark one: -->

- [ ] Newly introduced (caused by a recent change)
- [ ] Pre-existing (was failing before the current work)
- [ ] Unrelated (infrastructure, board, or environment)
- [ ] Flaky (non-deterministic)


## Bisect Log

<!-- Record git bisect results. -->

Bad commit:
Good commit:
Bisect result:

```sh
git bisect start
git bisect bad <commit>
git bisect good <commit>
```


## Investigation Log

### <!-- YYYY-MM-DD -->

-


## Root Cause

<!-- Describe the root cause once identified. -->

Responsible file:
Responsible function / pattern:
Nature of the bug:


## Fix

<!-- Describe the fix. Paste the diff or link to a file in this directory. -->


## Validation

- [ ] Failing test now passes
- [ ] No new failures introduced by the fix
- [ ] Bootstrap passes
- [ ] `make check-gcc RUNTESTFLAGS="powerpc.exp"` passes


## References

- Bugzilla: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=
- Suspect commit:
- Mailing list thread:
