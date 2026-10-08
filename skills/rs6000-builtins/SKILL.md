# Skill: rs6000-builtins

## Purpose
Implement, modify, or debug rs6000 builtin functions, including overloaded builtins,
expansion code, TARGET guards, and optab connections.

## When to Use
- Adding a new `__builtin_` function for rs6000
- Fixing incorrect builtin expansion
- Adding a new overloaded builtin variant
- Investigating how an existing builtin is implemented

---

## Architecture Overview

The rs6000 builtin system has two layers:

1. **Definition layer** — `.def` files declare every builtin.
   - `rs6000-builtins.def` — non-overloaded builtins (each has a unique name and signature).
   - `rs6000-overload.def` — overloaded builtin resolution tables (maps from generic name + argument types to a specific builtin).

2. **Generation layer** — `rs6000-gen-builtins.cc` is a build-time tool that reads the `.def` files and generates C tables used at compile time.

3. **Expansion layer** — `rs6000-builtin.cc` implements `TARGET_EXPAND_BUILTIN` and `TARGET_RESOLVE_OVERLOADED_BUILTIN`. Each non-overloaded builtin is expanded to RTL here.

4. **Pattern layer** — the expanded RTL must match an instruction pattern in the `.md` files.

---

## Instructions

### Adding a non-overloaded builtin

1. **Locate the relevant section** in `rs6000-builtins.def` (grouped by ISA feature).

2. **Add a `.def` entry:**
   ```
   BU_<ISA>_1 (<ENUM_NAME>, "<builtin-name>", <attrs>, <expander>)
   ```
   Study the existing entries for the exact macro syntax used for the ISA you are targeting.

3. **Add expansion code** in `rs6000-builtin.cc`:
   - Find the `case` for a similar builtin in the large switch on builtin code.
   - Add a new `case RS6000_BIF_<ENUM_NAME>:` block.
   - Use `emit_insn (gen_<pattern_name> (target, op0, ...))` to emit RTL.
   - Ensure mode consistency between the expansion and the pattern.

4. **Ensure the pattern exists** in the relevant `.md` file. If not, write it first
   (see `rtl-patterns` skill).

5. **Add documentation** in `gcc/doc/extend.texi` following the `documentation` skill.

6. **Write a test** following the `dejagnu` skill.

### Adding an overloaded builtin

1. Find an existing overloaded group in `rs6000-overload.def` as a model.

2. Add an `OB_` entry for the generic name.

3. Add `OB_INSTANCE_` entries for each argument-type variant, pointing to
   the corresponding non-overloaded builtin code.

4. Ensure each instance's underlying builtin already exists in `rs6000-builtins.def`.

5. The resolver is auto-generated; no changes to `rs6000-builtin.cc` are needed
   for resolution, only for expansion of each underlying builtin.

### Investigating an existing builtin

1. Search `rs6000-builtins.def` for the builtin name (strip `__builtin_` prefix).
2. Note the enum name and expander.
3. Search `rs6000-builtin.cc` for the enum name to find the expansion code.
4. Search the relevant `.md` file for the pattern name used in `gen_<name>`.

---

## Key Macros and Patterns in .def Files

| Macro prefix | Meaning |
|-------------|---------|
| `BU_ALTIVEC_1` | Altivec, 1 argument |
| `BU_ALTIVEC_2` | Altivec, 2 arguments |
| `BU_VSX_2` | VSX, 2 arguments |
| `BU_P9V_AV_2` | Power9 vector, 2 arguments |
| `BU_P10_AV_2` | Power10 vector, 2 arguments |
| `BU_MMA_*` | MMA builtins |

Always study the existing entries for the target ISA rather than assuming macro names.

---

## TARGET Guards

Every builtin must have an ISA guard. The guard is checked in `rs6000-builtin.cc`
when the builtin is resolved. The `.def` entry typically names the guard via
the ISA macro prefix. Ensure the corresponding `TARGET_xxx` macro is set
for the hardware you are targeting.

---

## Relevant Source Files
- `gcc/config/rs6000/rs6000-builtins.def` — builtin definitions
- `gcc/config/rs6000/rs6000-overload.def` — overload tables
- `gcc/config/rs6000/rs6000-builtin.cc` — expansion logic
- `gcc/config/rs6000/rs6000-gen-builtins.cc` — build-time generator (read-only reference)
- Relevant `.md` file for the ISA (e.g., `power10.md`, `vsx.md`, `altivec.md`)
- `gcc/config/rs6000/rs6000.h` — TARGET macros
- `gcc/config/rs6000/rs6000-cpus.def` — ISA masks
- `gcc/doc/extend.texi` — PowerPC builtin documentation section

---

## Expected Output
- Updated `rs6000-builtins.def` (and `rs6000-overload.def` if overloaded).
- Updated `rs6000-builtin.cc` with expansion case.
- New or updated instruction pattern in the `.md` file.
- New test in `gcc/testsuite/gcc.target/powerpc/`.
- New documentation entry in `gcc/doc/extend.texi`.

---

## Common Pitfalls
- Using the wrong ISA macro prefix in `.def` (check existing entries carefully).
- Mode mismatch between expansion and pattern (e.g., `V16QImode` vs `V4SImode`).
- Forgetting `rs6000-overload.def` entry when adding an overloaded builtin.
- Forgetting to add a `TARGET_xxx` check in the ISA guard.
- Writing expansion that emits patterns not present in the `.md` file.
- Not running `make` before testing — the `.def` tables are code-generated.
