---
name: regression-analysis
description: Classify and root-cause a failing GCC test (new, pre-existing, flaky) from logs, assembly and RTL dumps.
---
# Skill: regression-analysis

## Purpose
Analyze GCC regression test failures: classify them, identify root causes,
and recommend fixes or workarounds.

## When to Use
- Analyzing a test failure after a patch
- Triaging a regression report
- Identifying whether a failure is new, pre-existing, or unrelated

---

## Failure Classification

Every failure falls into one of these categories:

| Class | Description | Action |
|-------|-------------|--------|
| **Newly introduced** | Failure caused by a recent change | Must fix before landing |
| **Pre-existing** | Failure present before the current change | Document; do not block on it |
| **Unrelated** | Caused by infrastructure (timeout, missing lib, wrong board) | Retry or ignore |
| **Flaky** | Non-deterministic failure | Retry; fix the test or underlying instability |
| **Expected** | Marked `xfail` in the test | No action needed |

---

## Instructions

Host Gate (`AGENTS.md`): reproducing, bisecting and dumping need a Power host and the
user's approval. Otherwise analyse the logs and dumps the user provides.

### Step 1: Reproduce the failure

```sh
# Reproduce a single test
make check-gcc RUNTESTFLAGS="powerpc.exp=failing-test.c"
```

Confirm the failure is reproducible before investigating.

### Step 2: Read the failure message

DejaGnu outputs for each failure:
```
FAIL: gcc.target/powerpc/foo.c scan-assembler "xxland"
```

Key failure types:
- `scan-assembler` — instruction not generated
- `scan-assembler-not` — forbidden instruction was generated
- `scan-assembler-times` — wrong count
- `compile` — compilation error or ICE
- `run` — wrong runtime result or crash
- `XPASS` — unexpectedly passed (xfail test now passes, may need updating)

### Step 3: Determine if the failure is newly introduced

```sh
# Build the compiler before the suspect commit
git bisect start
git bisect bad <current-commit>
git bisect good <last-known-good>
# Let bisect guide you, run the test at each step
make -j$(nproc) && make check-gcc RUNTESTFLAGS="powerpc.exp=failing-test.c"
git bisect good/bad
```

If the failure predates the current work, classify as pre-existing.

### Step 4: Inspect the assembly output

```sh
gcc -O2 -mcpu=powerXX <flags> failing-test.c -S -o /tmp/out.s
```

Compare the actual output against what `scan-assembler` expected.
This is the fastest way to understand why a scan failed.

### Step 5: Inspect the RTL

```sh
gcc -O2 -mcpu=powerXX <flags> failing-test.c -S -fdump-rtl-all
ls failing-test.c.*r.*        # one file per pass: <src>.<NNN>r.<pass>
```

Use `-fdump-rtl-final` to see the last RTL before assembly emission.
Use `-fdump-rtl-combine` to see combine output.

### Step 6: Classify and document

In the task workspace, record:
- Test name
- Failure class
- Root cause hypothesis
- Evidence (assembly diff, RTL snippet)
- Recommended action

---

## Common Failure Patterns

| Symptom | Likely cause |
|---------|-------------|
| Instruction not generated | Pattern condition false (`TARGET_xxx`), or combine/peephole folded it away differently |
| Wrong instruction generated | Pattern recognition failure; a more general pattern matched instead |
| ICE during compilation | Assertion failure; check the crash backtrace |
| `unable to find a register to spill` / `insn does not satisfy its constraints` | Register allocation failure; constraint issue |
| Wrong runtime result | Endianness issue, mode bug, or UB in testcase |
| Test times out | Infinite loop in generated code or in the compiler itself |
| All tests fail on a board | Cross-compilation or board connectivity issue |

---

## Relevant Source Files
- `gcc/testsuite/gcc.target/powerpc/` — failing test source
- `gcc/testsuite/lib/target-supports.exp` — effective-target definitions (check if target keyword is correct)
- Relevant `.md` file — pattern that should have matched
- `gcc/config/rs6000/rs6000.cc` — condition predicates, cost functions
- `gcc/config/rs6000/rs6000-cpus.def` — ISA feature flags

---

## Expected Output

Produce a regression report in the task workspace:
```
## Regression Report: <test-name>

**Class:** Newly introduced / Pre-existing / Unrelated / Flaky

**Failure message:**
<paste DejaGnu output>

**Root cause:**
<explanation>

**Evidence:**
<assembly diff, RTL snippet, or bisect result>

**Recommended fix:**
<description or patch pointer>

**Validation:**
<how to confirm the fix>
```

---

## Common Pitfalls
- Reporting a pre-existing failure as newly introduced without bisecting.
- Ignoring `XPASS` failures — they indicate a previously expected failure now passes and the `xfail` annotation needs removing.
- Not checking whether the failure reproduces on the baseline (before the patch).
- Diagnosing from the failure message alone without inspecting the actual assembly.
