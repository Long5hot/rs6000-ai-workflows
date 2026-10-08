# Feature Task Template

Copy this file to `.ai/work/<task-name>/TASK.md` and fill in each section.
Delete this instruction line before use.

---

## Summary

<!-- One sentence: what feature is being implemented? -->


## Task Name

<!-- Short identifier: e.g., dmf-builtins, power11-vec-add -->


## Status

<!-- Planning / In progress / Under review / Committed -->


## Motivation

<!-- Why is this feature needed?
     Cite ISA spec, user request, or performance motivation. -->


## Affected Files

<!-- Identify the minimal set of files to change. -->

- [ ] `gcc/config/rs6000/rs6000-cpus.def` — ISA mask (if new ISA feature)
- [ ] `gcc/config/rs6000/rs6000.h` — TARGET macro
- [ ] `gcc/config/rs6000/rs6000.opt` — option (if user-facing)
- [ ] `gcc/config/rs6000/rs6000.cc` — backend hooks
- [ ] `gcc/config/rs6000/<feature>.md` — instruction patterns
- [ ] `gcc/config/rs6000/predicates.md` — predicates (if new)
- [ ] `gcc/config/rs6000/rs6000-builtins.def` — builtin definitions
- [ ] `gcc/config/rs6000/rs6000-overload.def` — overload entries
- [ ] `gcc/config/rs6000/rs6000-builtin.cc` — builtin expansion
- [ ] `gcc/doc/extend.texi` — builtin documentation
- [ ] `gcc/doc/invoke.texi` — option documentation
- [ ] `gcc/testsuite/gcc.target/powerpc/<test>.c` — test


## Implementation Plan

<!-- Steps in order. -->

- [ ] Find similar existing implementation to model after
- [ ] Add ISA mask / TARGET macro (if applicable)
- [ ] Add instruction pattern(s)
- [ ] Add builtin definition and expansion (if applicable)
- [ ] Write test(s)
- [ ] Write documentation
- [ ] Bootstrap and regression test


## Design Notes

<!-- Design decisions, tradeoffs, alternatives considered. -->


## Similar Implementation

<!-- What existing code did you model this after? -->

File:
Function / pattern:


## Patch

<!-- Paste the patch diff here, or link to a file in this directory. -->


## Testing

- [ ] New test: `gcc/testsuite/gcc.target/powerpc/<test>.c`
- [ ] `scan-assembler` checks the new instruction
- [ ] Execution test (if correctness validation needed)
- [ ] Run: `make check-gcc RUNTESTFLAGS="powerpc.exp=<test>.c"`


## Bootstrap

- [ ] Incremental build passes
- [ ] Full bootstrap passes
- [ ] Regression suite: no new failures


## Documentation Checklist

- [ ] `extend.texi` updated (for builtins)
- [ ] `invoke.texi` updated (for options)
- [ ] Signature matches implementation
- [ ] ISA requirement stated


## Review Notes


## References

- ISA specification:
- Mailing list thread:
- Related PR:
