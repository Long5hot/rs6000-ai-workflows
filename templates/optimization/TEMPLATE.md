# Optimization Task Template

Copy this file to `.ai/work/<task-name>/TASK.md` and fill in each section.
Delete this instruction line before use.

---

## Summary

<!-- One sentence: what optimization is being implemented or investigated? -->


## Task Name

<!-- Short identifier: e.g., ira-spill-cost, p10-vec-fma-fusion -->


## Status

<!-- Planning / In progress / Under review / Committed -->


## Performance Issue

<!-- Describe the missed optimization or performance gap.
     What code pattern triggers it?
     What is the current compiler output?
     What is the desired output? -->

### Current codegen

```c
/* Minimal C reproducer */
```

Current assembly:
```asm
```

Expected / desired assembly:
```asm
```


## Benchmark

<!-- Record benchmark results here.
     Always include both baseline and patched numbers.
     Note the benchmark name, workload, and machine configuration. -->

| Benchmark | Baseline | Patched | Delta |
|-----------|----------|---------|-------|
| | | | |

Machine:
CPU:
Flags:


## Root Cause

<!-- What prevents GCC from generating optimal code?
     Which pass is responsible?
     Which pattern or cost is wrong? -->


## Implementation Plan

- [ ] Identify the responsible pass (combine / peephole / IRA / target hook)
- [ ] Find the code pattern in the relevant source file
- [ ] Design the minimal fix
- [ ] Verify correctness (especially for endianness and edge cases)
- [ ] Benchmark before and after
- [ ] Write test


## Implementation Notes

<!-- Notes on the chosen approach. -->


## Correctness Analysis

<!-- Does this optimization change semantics for:
     - NaN / Inf / -0.0?
     - Big-endian vs little-endian?
     - Different modes (V4SF vs V2DF vs ...)?
     - Any UB edge cases?
     -->

- [ ] Endianness checked
- [ ] Floating-point edge cases checked
- [ ] Affected modes enumerated


## Patch

<!-- Paste the patch diff here, or link to a file in this directory. -->


## Testing

- [ ] New test: `gcc/testsuite/gcc.target/powerpc/<test>.c`
- [ ] Test verifies the optimization fires (`scan-assembler`)
- [ ] Test verifies the optimization does not fire when invalid (`scan-assembler-not`)
- [ ] Execution test verifying correctness (if applicable)


## Bootstrap

- [ ] Incremental build passes
- [ ] Full bootstrap passes
- [ ] Regression suite: no new failures (especially no PASS → FAIL regressions)


## Review Notes


## References

- Similar optimization:
- Mailing list thread:
