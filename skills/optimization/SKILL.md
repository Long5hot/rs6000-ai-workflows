# Skill: optimization

## Purpose
Implement, evaluate, or debug compiler optimizations in the rs6000 backend,
including RTL-level optimizations, GIMPLE lowering, and target-specific passes.

## When to Use
- Adding a new peephole optimization
- Adding a new rs6000-specific RTL pass
- Investigating a missed optimization opportunity
- Evaluating performance impact of a change

---

## Optimization Layers in GCC

```
Source → GENERIC → GIMPLE (SSA) → RTL → Assembly
                      │               │
              GIMPLE passes      RTL passes
              (tree-*.cc)        (rs6000-*.cc, combine, etc.)
```

For rs6000 backend work, optimizations typically happen at:
- **RTL level**: peepholes, define_peephole2, target-specific passes.
- **Target lowering**: rs6000-string.cc (memcpy/strlen), rs6000-p8swap.cc (P8 vector swap elimination).
- **Instruction selection**: combine pass interacts with patterns to fold operations.

---

## Instructions

### Writing a peephole optimization

Use `define_peephole2` for RTL-level peepholes:
```
(define_peephole2
  [(set (match_operand:MODE 0 ...)
        (match_operand:MODE 1 ...))
   (set (match_operand:MODE 2 ...)
        (match_operand:MODE 3 ...))]
  "<condition>"
  [(set (match_dup 2)
        ...)]
  {
    /* Optional C code to set up operands or test profitability. */
  })
```

Rules:
- Peephole patterns fire after reload, so operands are fully allocated.
- The replacement sequence must use only the registers present in the input.
- Peepholes must not increase code size unless under a profile/cost guard.

### Writing a target-specific pass

1. Define the pass struct in the relevant `.cc` file (model after `rs6000-p8swap.cc`).
2. Register the pass in `rs6000-passes.def`.
3. Place it at the correct point in the pass pipeline. Consult `gcc/passes.def` for anchor points.
4. Guard the pass with `TARGET_xxx` so it only runs when the feature is enabled.

### Evaluating a missed optimization

1. Reproduce with `-O2 -mcpu=powerXX` and the appropriate `-m` flags.
2. Use `-fdump-rtl-combine` to see what combine attempted.
3. Use `-fdump-rtl-peephole2` to see what peepholes matched.
4. Use `-dp` (debug assembly) to see which pattern was selected.
5. If combine did not fold: check whether the RTL shape matches an existing pattern. If not, add a pattern (see `rtl-patterns` skill).
6. If a peephole did not fire: check the peephole condition and the instruction sequence.

### Profitability

Before adding an optimization:
- Benchmark with a representative workload (SPEC CPU, application microbenchmark).
- Measure both positive and negative cases.
- Document the benchmark in the task workspace.
- Do not add an optimization that regresses a common case to improve a rare case.

### Correctness validation

- Every optimization must be proven correct for all affected modes.
- For vector operations, check both big-endian and little-endian.
- For floating-point, check NaN, Inf, and -0.0 behavior.
- Write a test that fails without the optimization and passes with it.

---

## Relevant Source Files
- `gcc/config/rs6000/rs6000.cc` — cost functions, target hooks, optimization flags
- `gcc/config/rs6000/rs6000-string.cc` — string/memory operation expansions
- `gcc/config/rs6000/rs6000-p8swap.cc` — P8 swap elimination pass
- `gcc/config/rs6000/rs6000-pcrel-opt.cc` — PCrel optimization pass
- `gcc/config/rs6000/rs6000-passes.def` — pass registration
- `gcc/config/rs6000/rs6000.md` and feature `.md` files — peephole patterns
- `gcc/combine.cc` — combine pass (reference for how RTL fusion works)
- `gcc/passes.def` — pass pipeline anchors
- `gcc/doc/passes.texi` — pass documentation

---

## Expected Output
- New or modified peephole / pass.
- Correctness test (execution test preferred).
- Performance benchmark result (in task workspace, not in the patch).
- Documentation update if a new option or tuning parameter is added.

---

## Common Pitfalls
- Peepholes that increase code size unconditionally.
- Optimizations that are correct for one endianness but wrong for the other.
- Missing NaN/Inf handling for floating-point rewrites.
- Passes that fire when `TARGET_xxx` is not set.
- Combine interactions: a new pattern may prevent combine from matching a higher-level fold.
- Forgetting to benchmark the common case — a micro-optimization that slows typical code.
