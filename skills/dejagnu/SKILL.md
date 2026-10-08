# Skill: dejagnu

## Purpose
Write, modify, and maintain GCC DejaGnu testcases for the rs6000/PowerPC backend.

## When to Use
- Writing a new testcase for a feature, bugfix, or optimization
- Debugging a failing testcase
- Understanding how a testcase works
- Ensuring correct use of effective-target keywords

---

## Test File Structure

```c
/* { dg-do compile } */
/* { dg-options "-O2 -mcpu=power9" } */
/* { dg-require-effective-target powerpc_p9vector_ok } */

#include <altivec.h>

vector int foo (vector int a, vector int b)
{
  return vec_add (a, b);
}

/* { dg-final { scan-assembler-times "vadduwm" 1 } } */
```

Key directives:
- `dg-do` — test action: `compile`, `assemble`, `run`, `link`
- `dg-options` — additional compiler flags
- `dg-require-effective-target` — skip if the target does not support the feature
- `dg-final` — post-test check (scan-assembler, scan-tree-dump, etc.)

---

## Instructions

### Choosing the test type

| Scenario | dg-do |
|----------|-------|
| Verify codegen (instruction emitted) | `compile` |
| Verify assembly instruction count | `compile` |
| Verify no invalid instructions | `compile` |
| Verify correct runtime result | `run` |
| Verify correct runtime on hardware | `run` with effective-target |

Prefer `compile` tests for codegen verification — they run on any host.
Use `run` tests when correctness (not codegen) is what needs to be validated.

### Effective-target keywords (common)

| Keyword | Meaning |
|---------|---------|
| `powerpc_altivec_ok` | AltiVec/VMX supported |
| `powerpc_vsx_ok` | VSX (POWER7+) supported |
| `powerpc_p8vector_ok` | POWER8 vector extensions |
| `powerpc_p9vector_ok` | POWER9 vector extensions |
| `powerpc_p10_ok` | POWER10 (ISA 3.1) supported |
| `powerpc_mma_ok` | MMA (matrix multiply assist) |
| `powerpc_htm_ok` | Hardware Transactional Memory |
| `powerpc64_ok` | 64-bit mode |
| `ilp32` | 32-bit ILP32 ABI |
| `lp64` | 64-bit LP64 ABI |
| `has_arch_ppc64` | 64-bit PowerPC architecture |

The full list is in `gcc/testsuite/lib/target-supports.exp`.
Always check the existing keyword before writing a new one.

### Scanning for assembly

```c
/* { dg-final { scan-assembler "xxland" } } */
/* { dg-final { scan-assembler-times "vadduwm" 2 } } */
/* { dg-final { scan-assembler-not "lvx" } } */
```

- `scan-assembler "<regex>"` — check pattern appears at least once
- `scan-assembler-times "<regex>" N` — check exact count
- `scan-assembler-not "<regex>"` — check pattern is absent
- Patterns are regexes; escape special characters (`.`, `*`, etc.)

### Scanning tree dumps

```c
/* { dg-options "-O2 -fdump-tree-optimized" } */
/* { dg-final { scan-tree-dump "vec_cond" "optimized" } } */
```

Use for GIMPLE-level checks. The dump name (`"optimized"`) is the pass name suffix.

### Writing robust tests

- **Do not hard-code register names** unless the test specifically validates register assignment.
- **Use `-O2` by default** for optimization tests; `-O0` only if testing unoptimized expansion.
- **Parameterize ISA** with `-mcpu=powerXX` rather than individual `-mfoo` flags where possible.
- **One feature per test** — keep tests focused; don't combine multiple independent features.
- **Name files descriptively** — `power10-mma-outer-product.c`, not `test1.c`.
- **Add a comment** at the top briefly explaining what the test validates.
- **Match the minimal instruction** — scan for the specific new instruction, not a generic pattern that would match even without your change.

### Debugging a failing test

1. Run the test manually:
   ```sh
   gcc -O2 -mcpu=power9 <options> test.c -S -o test.s
   grep "vadduwm" test.s
   ```
2. Verify the effective-target is satisfied for your test machine.
3. Check that the `dg-options` flags match what you intend.
4. If `scan-assembler` fails, inspect the `.s` output to see what was actually generated.
5. For `run` failures, add `fprintf(stderr, ...)` temporarily to debug values.

### Running tests

```sh
# Run a single test
make check-gcc RUNTESTFLAGS="powerpc.exp=my-test.c"

# Run all PowerPC tests
make check-gcc RUNTESTFLAGS="powerpc.exp"

# Run with a specific compiler
make check-gcc RUNTESTFLAGS="--target_board=unix/-mcpu=power10 powerpc.exp=my-test.c"
```

---

## Relevant Source Files
- `gcc/testsuite/gcc.target/powerpc/` — all PowerPC testcases
- `gcc/testsuite/lib/target-supports.exp` — effective-target definitions
- `gcc/testsuite/gcc.dg/dg.exp` — DejaGnu framework library

---

## Expected Output
- One `.c` file per feature or fix in `gcc/testsuite/gcc.target/powerpc/`.
- File includes: `dg-do`, `dg-options`, `dg-require-effective-target` (if ISA-specific), `dg-final` scan.
- Test must pass on the intended target and be skipped (not fail) on unsupported targets.

---

## Common Pitfalls
- Missing `dg-require-effective-target` — test fails on architectures that don't support the ISA.
- `scan-assembler` regex that accidentally matches unintended instructions.
- Using `scan-assembler-times` with a count that depends on optimization level or unrolling.
- `dg-do run` without ensuring the test can be cross-compiled and executed on the test board.
- Hard-coding a register number that changes with register allocation decisions.
- Not using `volatile` on variables whose computation could be optimized away.
