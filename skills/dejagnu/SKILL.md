---
name: dejagnu
description: Write, run or debug a PowerPC DejaGnu test (dg directives, effective targets, -mdejagnu-cpu, anchored assembler scans).
---
# Skill: dejagnu

Tests: `gcc/testsuite/gcc.target/powerpc/`. Keywords: `gcc/testsuite/lib/target-supports.exp`.
Directive reference: `gcc/doc/sourcebuild.texi` (its PowerPC keyword list is incomplete; trust `target-supports.exp`).

## Compile test (codegen)
```c
/* { dg-do compile } */
/* { dg-options "-O2 -mdejagnu-cpu=power9 -mvsx" } */
/* { dg-require-effective-target powerpc_vsx } */

/* What this test verifies.  */
#include <altivec.h>

vector int
foo (vector int a, vector int b)
{
  return vec_add (a, b);
}

/* { dg-final { scan-assembler-times {\mvadduwm\M} 1 } } */
```

## Run test
```c
/* { dg-do run { target power10_hw } } */
/* { dg-options "-O2 -mdejagnu-cpu=power10" } */
```
Fail with `abort ()`; return 0 on success.

## Rules
- CPU: `-mdejagnu-cpu=powerN` in `dg-options`, not `-mcpu=`.
- Scans: brace-quoted and word-anchored, `{\mxxland\M}`. An unanchored `"xxland"` also matches `xxlandc`.
- `dg-do compile` + scan for codegen; `dg-do run` only when the result needs executing.
- One feature per test. Name `pr<N>.c` for a PR, otherwise descriptive.
- Do not scan for register numbers unless the test is about them.

## Choosing the test type
| Scenario | `dg-do` |
|----------|---------|
| Verify an instruction is (or is not) emitted | `compile` + scan |
| Verify an instruction count | `compile` + `scan-assembler-times` |
| Verify a run-time result | `run`, guarded by a `*_hw` effective target |

Prefer `compile` tests for code generation: they run on any PowerPC test machine.
Use `run` tests when correctness, not code generation, is what must be validated.

## Writing robust tests
- `-O2` by default; `-O0` only when testing unoptimized expansion.
- Select the ISA with `-mdejagnu-cpu=powerN` rather than individual `-m` feature flags where possible.
- One feature per test; do not combine independent features.
- Descriptive file name (`pr<N>.c` for a PR); a comment at the top saying what the test validates.
- Scan for the specific new instruction, not a generic pattern that would match without the change.
- Do not hard-code register names unless the test is about register assignment.
- Make sure the computation under test cannot be optimized away (use function arguments and return values; `volatile` or `__attribute__((noipa))` where needed).

## Effective targets
| Compile-time | Meaning |
|--------------|---------|
| `powerpc_altivec` | AltiVec enabled |
| `powerpc_vsx` | current options generate VSX |
| `power10_ok` | target supports `-mcpu=power10` |
| `powerpc_htm_ok` | target supports `-mhtm` |
| `has_arch_pwr8` `has_arch_pwr9` `has_arch_pwr10` | `-mcpu` in effect is at least that |
| `has_arch_ppc64` `powerpc64` | 64-bit instructions / executing them |
| `lp64` `ilp32` `int128` | ABI / type availability |
| `powerpc_pcrel` `powerpc_prefixed_addr` | PC-relative / prefixed insns generated |
| `be` `le` | endianness; `{ target le }`, `{ xfail be }` |

| Run-time (hardware) | Executes |
|---------------------|----------|
| `vmx_hw` | AltiVec |
| `vsx_hw` | VSX |
| `p8vector_hw` | power8 vector |
| `p9vector_hw` | power9 vector |
| `power10_hw` | power10 |

Before using any other keyword: `grep -n 'proc check_effective_target_<kw> ' gcc/testsuite/lib/target-supports.exp`.

## Scan directives
```c
/* { dg-final { scan-assembler {\mxxland\M} } } */
/* { dg-final { scan-assembler-times {\mvadduwm\M} 2 } } */
/* { dg-final { scan-assembler-not {\mlvx\M} } } */
/* { dg-final { scan-assembler-times {\mvstribr\M} 1 { target le } } } */
/* { dg-final { scan-tree-dump "pattern" "optimized" } } */   /* needs -fdump-tree-optimized */
/* { dg-final { scan-rtl-dump "pattern" "combine" } } */      /* needs -fdump-rtl-combine */
```

## Run
Host Gate (`AGENTS.md`): Power host only, after the user approves. Otherwise give the commands to the user.
Build directory:
```sh
make check-gcc RUNTESTFLAGS="powerpc.exp=my-test.c"
make check-gcc RUNTESTFLAGS="powerpc.exp"
make check-gcc RUNTESTFLAGS="--target_board=unix/-mcpu=power10 powerpc.exp=my-test.c"
```
Results (in the build directory): `gcc/testsuite/gcc/gcc.sum` and `gcc.log`.

## Debug a failure
1. (Needs a PowerPC compiler: Host Gate.) Compile by hand with the test's `dg-options` (replace `-mdejagnu-cpu=` with `-mcpu=`) and `-S`; read the `.s`.
2. `UNSUPPORTED`: the effective target is false on this machine.
3. Wrong count in `scan-assembler-times`: check for unrolling/vectorization or a looser regex.

## Expected output
- One `.c` file per feature or fix in `gcc/testsuite/gcc.target/powerpc/`.
- It contains `dg-do`, `dg-options`, `dg-require-effective-target` (if ISA-specific) and a `dg-final` scan or a run check.
- It passes on the intended target and is skipped (`UNSUPPORTED`), not failed, elsewhere.

## Pitfalls
- Unknown effective-target keyword: the test errors instead of being skipped.
- Missing `dg-require-effective-target`: the test fails on targets without the ISA.
- A scan regex that also matches other instructions (anchor with `\m...\M`).
- A hard-coded register number that changes with allocation decisions.
- Count that depends on optimization level or endianness without a selector.
- `dg-do run` with no `*_hw` guard: fails on older hardware.
