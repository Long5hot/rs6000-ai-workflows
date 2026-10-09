---
name: review-patch
description: Review an rs6000 patch: predicates, constraints, modes, TARGET guards, builtins, tests, docs.
---
# Skill: review-patch

## Purpose
Review GCC patches targeting the rs6000 backend for correctness, completeness,
regression risk, and submission readiness.

## When to Use
- Reviewing a patch before posting to gcc-patches@gcc.gnu.org
- Evaluating a patch received for comment
- Self-reviewing before committing

---

## Instructions

### 1. Understand the patch scope
- Read the patch header and commit message.
- Identify which files are modified.
- Use `repo-map.md` to understand the role of each modified file.
- Do not read unmodified files unless the patch references them.

### 2. Read the affected functions
- Use `FindSymbol` to locate changed functions. Read their full bodies.
- Read only the context needed to evaluate correctness.

### 3. Correctness checks

**Predicates:**
- Verify every `match_operand` and `match_operator` uses the correct predicate.
- Cross-check predicates against `predicates.md`.
- Ensure predicates are not overly broad (would accept invalid RTL) or overly narrow (would reject valid RTL).

**Constraints:**
- Verify constraints match the predicate intent.
- Check `constraints.md` for constraint letter meanings.
- Ensure alternative constraints are consistent (no alternative is always worse than another in a way that causes reloads).

**RTL correctness:**
- Verify mode consistency across all operands.
- Verify each new `UNSPEC_*` name is added to a `define_c_enum "unspec"` list and is not already used (`grep -n UNSPEC_<NAME> gcc/config/rs6000/*.md`).
- Check that `define_expand` patterns set up RTL correctly before calling `emit_insn`.
- Verify scratch registers are declared with correct constraints.

**Register allocation impact:**
- Check whether new patterns introduce hard-register constraints that could increase spill pressure.
- Verify that register classes referenced match `rs6000.h` definitions.

**TARGET guard:**
- Every new pattern that is ISA-specific must be guarded by a `TARGET_xxx` predicate in the condition field.
- Cross-check against `rs6000-cpus.def` and `rs6000.h` for the correct flag.

**Builtin-specific:**
- Verify the `.def` entry's prototype matches the modes of the pattern it names, and that it sits in the correct `[stanza]`.
- Verify overload entry in `rs6000-overload.def` if applicable.
- Verify documentation in `gcc/doc/extend.texi`.

### 4. Optimization impact
- Consider whether the change affects patterns that feed into existing optimizations.
- Consider peephole interactions.
- Consider combine pass interactions (operand constraints must match what combine will generate).

### 5. Bootstrap risk
- Changes to `rs6000.cc`, `rs6000.h`, or core `.md` files require a full bootstrap.
- Any patch needs a full bootstrap and regression test before submission; an incremental build is only a first check.
- Flag any changes that alter fundamental data structures or enum values.

### 6. Test coverage
- Verify at least one new test exists in `gcc/testsuite/gcc.target/powerpc/`.
- Test must use `dg-require-effective-target` if ISA-specific.
- Test must include a `scan-assembler` or execution check; `dg-do compile` with no scan is insufficient for new codegen paths.
- Check that the test actually exercises the new code path (verify the expected instruction appears).

### 7. Documentation
- Verify `extend.texi` is updated for new builtins.
- Verify `invoke.texi` is updated for new options.
- Check that documentation matches the implementation exactly (types, argument order, restrictions).

---

## Relevant Source Files
- `gcc/config/rs6000/rs6000.cc` — main backend
- `gcc/config/rs6000/rs6000.md` and feature `.md` files — instruction patterns
- `gcc/config/rs6000/predicates.md` — predicates
- `gcc/config/rs6000/constraints.md` — constraints
- `gcc/config/rs6000/rs6000-builtin.cc` — builtin expansion
- `gcc/config/rs6000/rs6000-builtins.def` — builtin definitions
- `gcc/config/rs6000/rs6000-overload.def` — overload tables
- `gcc/config/rs6000/rs6000.h` — register classes, TARGET flags
- `gcc/config/rs6000/rs6000-cpus.def` — ISA masks
- `gcc/doc/extend.texi` — builtin documentation
- `gcc/doc/invoke.texi` — option documentation

---

## Expected Output

Produce a structured review with sections:
1. **Summary** — what the patch does
2. **Correctness** — any issues found (predicates, constraints, modes, guards)
3. **Register allocation** — impact assessment
4. **Optimization** — impact assessment
5. **Tests** — coverage assessment, gaps
6. **Documentation** — completeness
7. **Bootstrap risk** — low / medium / high with rationale
8. **Verdict** — OK / Needs changes / Not OK

---

## Common Pitfalls
- Forgetting to guard a pattern with `TARGET_xxx`.
- Using a constraint that permits more register classes than the predicate allows.
- Adding a `define_expand` that emits patterns not recognized by any `define_insn`.
- Missing `rs6000-overload.def` entry for a new overloaded builtin.
- Writing a test that compiles but does not scan for the expected output.
- `.def` prototype types that do not match the named pattern's modes.
