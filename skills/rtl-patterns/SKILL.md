---
name: rtl-patterns
description: Write or debug rs6000 define_insn/define_expand patterns: predicates, constraints, conditions, UNSPECs.
---
# Skill: rtl-patterns

## Purpose
Write, modify, and debug RTL instruction patterns for the rs6000 machine description.

## When to Use
- Writing a new `define_insn` or `define_expand`
- Debugging pattern recognition failures
- Fixing constraint or predicate errors
- Understanding how an instruction is selected and emitted

---

## Pattern Anatomy

### define_insn
```
(define_insn "<name>"
  [(set (match_operand:<MODE> 0 "<predicate>" "<output-constraint>")
        (unspec:<MODE>
          [(match_operand:<MODE> 1 "<predicate>" "<input-constraint>")
           (match_operand:<MODE> 2 "<predicate>" "<input-constraint>")]
          UNSPEC_<NAME>))]
  "<condition>"
  "<template>"
  [<attributes>])
```

- **name**: used by `gen_<name>()` in C code. Must be unique across all `.md` files.
- **predicate**: validates the operand's RTL form. Defined in `predicates.md`.
- **constraint**: controls register allocation. Defined in `constraints.md`. The output constraint uses `=` prefix.
- **condition**: C expression evaluated at compile time. Use `TARGET_xxx` flags.
- **template**: assembler string. Use `%0`, `%1`, etc. for operands; `%x0` for a VSX register (`wa`) operand.
- **UNSPEC**: a name from a `define_c_enum "unspec"` list (each of `rs6000.md`, `vsx.md`, `altivec.md`, ... has one). Values are assigned automatically.

### define_expand
```
(define_expand "<name>"
  [(set (match_operand:<MODE> 0 "<predicate>")
        ...)]
  "<condition>"
{
  /* C code to emit RTL. */
  emit_insn (gen_<underlying_insn> (operands[0], operands[1]));
  DONE;
})
```

- Use `define_expand` when the operation cannot be expressed as a single RTL template.
- Constraints are not used in `define_expand`; omit them.
- End the C body with `DONE;` when it emitted all the RTL itself. Without `DONE`, the RTL template is emitted after the C code runs. `FAIL` is allowed only for patterns documented as allowed to fail.
- All emitted patterns must match a `define_insn`.

---

## Instructions

### Writing a new define_insn

1. **Find a similar pattern.** Search the relevant `.md` file (e.g., `vsx.md`, `altivec.md`) for a pattern doing a similar operation. Use it as a template.

2. **Choose the correct predicate.** Check `predicates.md` for an existing predicate that matches your operand type. Prefer reuse over writing a new predicate.

3. **Choose the correct constraint.** Check `constraints.md`. Common rs6000 constraints:
   - `v` — Altivec registers (VSR 32–63)
   - `wa` — any VSX register (VSR 0–63)
   - `r` — general-purpose register
   - `b` — base register (GPR except r0)
   - `d` — floating-point register (FPR, VSR 0–31)

4. **Set the condition.** Use the most specific `TARGET_xxx` flag. Do not leave the condition as `""` for ISA-specific patterns.

5. **Add the UNSPEC name.** `grep -n UNSPEC_xxx gcc/config/rs6000/*.md`; if it is new, add it to the `define_c_enum "unspec"` list of the `.md` file that uses it.

6. **Verify mode consistency.** Every operand's mode must be consistent. Mismatched modes cause silent codegen failures.

### Writing a new define_expand

Use a `define_expand` when:
- The operation requires multiple RTL instructions.
- The operation requires scratch registers.
- Mode conversion is required before the underlying insn.
- Operand preparation (e.g., force_reg) is needed.

The `define_expand` name is what `optabs` and GCC internals call. The underlying `define_insn` name is internal.

### Debugging pattern recognition failures

1. Check the **condition** — is `TARGET_xxx` true for the configuration being tested?
2. Check the **predicate** — does the operand pass the predicate?
3. Check the **constraint** — is the assigned register in the correct class?
4. Use `-fdump-rtl-all` to inspect RTL at various pass stages.
5. Use `-dp` to annotate assembly output with the pattern name used.

---

## Predicates Reference (frequently used)

| Predicate | Accepts |
|-----------|---------|
| `register_operand` | any register |
| `nonimmediate_operand` | register or memory |
| `memory_operand` | memory reference |
| `const_int_operand` | integer constant |
| `gpc_reg_operand` | register that is not special (the usual rs6000 register predicate) |
| `altivec_register_operand` | Altivec register |
| `vsx_register_operand` | VSX register |
| `vfloat_operand` | vector register for floating-point vectors (Altivec or VSX) |
| `vlogical_operand` | vector register for logical operations |

See `predicates.md` for the full list and definitions.

---

## Constraints Reference (frequently used)

| Constraint | Register class |
|-----------|---------------|
| `r` | GPR r0–r31 |
| `b` | base register: GPR except r0 |
| `d` (`f` is the same) | FPR f0–f31 (= vs0–vs31) |
| `v` | Altivec v0–v31 (= vs32–vs63) |
| `wa` | any VSX register vs0–vs63; print with `%x<n>` |
| `wd wf wi ws ww` | legacy aliases of `wa`; do not use in new code |
| `I` | signed 16-bit constant |
| `K` | unsigned 16-bit constant |
| `L` | signed 16-bit constant shifted left 16 |
| `J` | unsigned 16-bit constant shifted left 16 |
| `eI` | signed 34-bit constant (prefixed instructions) |

Full list with descriptions: `gcc/doc/md.texi`, table "PowerPC and IBM RS6000"; definitions in `constraints.md`.

---

## Relevant Source Files
- `gcc/config/rs6000/rs6000.md` — top-level machine description and UNSPEC list
- `gcc/config/rs6000/predicates.md` — all predicate definitions
- `gcc/config/rs6000/constraints.md` — all constraint definitions
- `gcc/config/rs6000/altivec.md`, `vsx.md`, `vector.md`, `mma.md`, `crypto.md`, `dfp.md`, `htm.md` — feature patterns (`power8.md`, `power9.md`, `power10.md` are scheduling descriptions, not instruction patterns)
- `gcc/config/rs6000/rs6000.cc` — helper RTL generation functions
- `gcc/recog.cc` — instruction recognition logic
- `gcc/doc/md.texi` — machine description language reference

---

## Expected Output
- New or modified `define_insn` / `define_expand` in the appropriate `.md` file.
- New or modified predicate in `predicates.md` (if needed).
- New `UNSPEC_*` name added to a `define_c_enum` list, if one is needed.

---

## Common Pitfalls
- Reusing an existing `UNSPEC_*` name for a different operation.
- Writing a non-canonical RTL shape (see `rtl-canonical-forms` skill).
- Mode mismatch between `define_expand` operands and `define_insn` operands.
- Using `""` condition on an ISA-specific pattern (pattern fires unconditionally).
- Forgetting `=` on the output constraint.
- Using a predicate that accepts memory when the pattern does not handle it.
- Not rebuilding after pattern changes (`make -C gcc` in the build dir regenerates the `insn-*.cc` files).
