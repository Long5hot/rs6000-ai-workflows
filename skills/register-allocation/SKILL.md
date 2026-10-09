---
name: register-allocation
description: Debug IRA/LRA problems on rs6000: spills, constraint failures, register classes, move costs.
---
# Skill: register-allocation

## Purpose
Investigate, debug, and fix register allocation issues in the rs6000 backend,
including IRA, LRA, register class definitions, and spill behavior.

## When to Use
- Investigating spill code generation
- Debugging "no constraint" or "cannot reload" errors
- Fixing hard-register conflicts
- Tuning allocation costs for a register class
- Understanding why a pattern fails to match after allocation

---

## Register Allocation Pipeline

```
RTL after instruction selection
        │
       IRA  (gcc/ira.cc) — global allocator using allocation regions
        │
       LRA  (gcc/lra.cc) — local constraint satisfaction; pass and dump name: reload
        │
 RTL with hard registers
```

rs6000 uses LRA only (`-mlra` is an ignored legacy option). `reload.cc` is not used by rs6000.

---

## rs6000 Register Classes

Defined in `gcc/config/rs6000/rs6000.h` under `enum reg_class` and `REG_CLASS_CONTENTS`.

Key register classes:

| Class | Contents | Typical constraint |
|-------|----------|--------------------|
| `GENERAL_REGS` | GPRs (r0–r31) | `r` |
| `FLOAT_REGS` | FPR / VSR 0–31 | `f` |
| `ALTIVEC_REGS` | VMX / VSR 32–63 | `v` |
| `VSX_REGS` | All VSRs (0–63) | `wa` |
| `LINK_REGS` | LR | — |
| `CTR_REGS` | CTR | — |
| `CR_REGS` | Condition registers | — |
| `CA_REGS` | Carry bit | — |
| `NO_REGS` | None | — |

Subset relations follow from `REG_CLASS_CONTENTS`; query them with `reg_class_subset_p`.

---

## Instructions

### Investigating a spill

1. Compile with `-fdump-rtl-ira` and `-fdump-rtl-reload` (LRA's dump) to observe allocation decisions.
2. Look for pseudo registers that are assigned to memory.
3. Identify which constraint forced an allocation that could not be satisfied.
4. Check whether the live range of the conflicting pseudo spans a hard-register requirement.

### Investigating "no constraint" / reload errors

These typically manifest as:
```
error: unable to find a register to spill
error: insn does not satisfy its constraints:
```

Steps:
1. Find the instruction in the RTL dump that cannot be satisfied.
2. Identify which operand has an unsatisfiable constraint.
3. Check whether the constraint is correct for the register class.
4. Check whether the pattern has enough alternatives to allow the allocator to choose.
5. Adding a memory alternative (`"=m"`) can relieve spill pressure.

### Fixing hard-register constraint conflicts

Hard-register constraints (e.g., `{r3}`, `{v24}`) narrow the allocator's choices.
- Use them only when required by the ABI or instruction encoding.
- Prefer register-class constraints over hard-register constraints.
- If a hard-register is unavoidable, ensure a `clobber` or `use` prevents it from being live across the constraint.

### Tuning allocation costs

IRA allocation costs are computed by `ira-costs.cc`. Target-specific costs are set via:
- `TARGET_REGISTER_MOVE_COST` — cost of moving between register classes.
- `TARGET_MEMORY_MOVE_COST` — cost of load/store for a class.

For rs6000, these are implemented in `rs6000.cc`. Search for `rs6000_register_move_cost`.

### LRA-specific issues

LRA constraint satisfaction is in `gcc/lra-constraints.cc`.
- When LRA generates a reload, it creates a new pseudo and inserts a copy.
- If a reload target has no valid class, LRA may fail with an ICE.
- Adding a memory alternative to the pattern usually fixes this.
- Check `gcc/lra-assigns.cc` for assignment failures.

---

## Relevant Source Files
- `gcc/config/rs6000/rs6000.h` — register class definitions
- `gcc/config/rs6000/rs6000.cc` — `rs6000_register_move_cost`, `rs6000_memory_move_cost`, hard-reg init
- `gcc/config/rs6000/constraints.md` — constraint letters and their register classes
- `gcc/config/rs6000/predicates.md` — operand predicates
- `gcc/ira.cc` — IRA top level
- `gcc/ira-costs.cc` — cost computation
- `gcc/ira-color.cc` — coloring algorithm
- `gcc/lra.cc` — LRA top level
- `gcc/lra-constraints.cc` — LRA constraint satisfaction
- `gcc/lra-assigns.cc` — LRA assignment

---

## Useful Compiler Flags for Debugging

| Flag | Purpose |
|------|---------|
| `-fdump-rtl-ira` | Dump RTL after IRA |
| `-fdump-rtl-reload` | Dump RTL after LRA (the pass is named `reload`; there is no `-fdump-rtl-lra`) |
| `-fdump-rtl-all` | Dump all RTL passes |
| `-fira-verbose=N` | IRA dump verbosity (default 5; N ≥ 10 writes to stderr) |
| `-flra-remat` | Enable/disable LRA rematerialization |

---

## Expected Output
- Identification of the constraint or class causing the allocation failure.
- Minimal patch: either a constraint fix, an additional alternative, or a cost adjustment.
- Test demonstrating the fix (compile test showing no spill, or execution test).

---

## Common Pitfalls
- Patterns with only one alternative force a single register class; adding a memory alternative gives LRA an escape.
- Moving a value between VSR and GPR is expensive; avoid gratuitous cross-class moves.
- Hard-register clobbers in call patterns must cover all ABI-clobbered registers.
- Changing `REG_CLASS_CONTENTS` in `rs6000.h` can shift the cost of all patterns using that class — benchmark before committing.
