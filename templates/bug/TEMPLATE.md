# Bug Task Template

Copy this file to `.ai/work/<task-name>/TASK.md` and fill in each section.
Delete this instruction line before use.

---

## Summary

<!-- One sentence: what is the bug? -->


## Task Name

<!-- Short identifier: e.g., pr120384, vec-sel-le-bug -->


## Status

<!-- In progress / Under review / Fixed / Closed -->


## Affected Files

<!-- List files that are relevant to this bug. -->

- [ ] `gcc/config/rs6000/`
- [ ] `gcc/testsuite/gcc.target/powerpc/`
- [ ] `gcc/doc/`


## Root Cause

<!-- Describe the root cause once identified.
     Leave blank until investigation is complete. -->


## Investigation Log

<!-- Date-stamped notes. Add new entries at the top. -->

### <!-- YYYY-MM-DD -->

-


## Reproduction

```sh
# Minimal compiler invocation to reproduce the bug.
gcc -O2 -mcpu=XXXX <flags> test.c -S
```

Expected output:
```
```

Actual output:
```
```


## Implementation Plan

<!-- Steps to fix, in order. Check off as completed. -->

- [ ]
- [ ]
- [ ]


## Patch

<!-- Paste the patch diff here once written, or link to a file in this directory. -->


## Testing

<!-- List all testcases. -->

New test:
- [ ] `gcc/testsuite/gcc.target/powerpc/<test>.c`

Existing tests to re-run:
- `make check-gcc RUNTESTFLAGS="powerpc.exp=<test>.c"`


## Bootstrap

<!-- Record bootstrap result. -->

- [ ] Incremental build passes
- [ ] Full bootstrap passes
- [ ] Regression suite: no new failures


## Review Notes

<!-- Notes from the patch review cycle. -->


## References

<!-- Bug report URL, mailing list thread, upstream commit, etc. -->

- Bugzilla: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=
- Thread:
