---
name: rtl-pass-order
description: Actual RTL pass order and -fdump-rtl names; use to pick the pass an optimization belongs in and the dump to read.
---
# Skill: rtl-pass-order

Source of truth: `gcc/passes.def` (order), `gcc/doc/passes.texi` (descriptions).
Dump flag = `-fdump-rtl-<name>`; file = `<src>.<NNN>r.<name>`.

## Order (dump names, main passes only)
```
expand → vregs → subreg1 → [swaps] → cse1 → fwprop1 → cprop → ce1 → cse2
→ dse1 → fwprop2 → combine → late_combine → ce2 → split1 → sched1
→ ira → reload → postreload → late_combine → split2 → ree
→ pro_and_epilogue → dse2 → peephole2 → ce3 → cprop_hardreg
→ [pcrel_opt] → sched2 → final
```
`[...]` = rs6000 passes from `gcc/config/rs6000/rs6000-passes.def`.
Repeated passes take a numeric suffix in the dump name: `cprop1`, `late_combine1`, `late_combine2`.

## Facts
- `simplify-rtx.cc` is a library, not a pass; combine, cse, fwprop call it.
- LRA runs as pass `reload`: dump is `-fdump-rtl-reload`. There is no `-fdump-rtl-lra`.
- rs6000 is LRA-only (`-mlra` is an ignored legacy option).
- `define_split` runs in `split1`..`split5` and inside combine; `define_peephole2` only in `peephole2` (hard regs; `match_scratch` allowed).
- Pseudos before `ira`; hard registers after `reload`.

## Which dump
| Question | Flag |
|----------|------|
| What RTL did expand make | `-fdump-rtl-expand` |
| Why did combine not merge | `-fdump-rtl-combine-all` (`Failed to match`) |
| Spills / reloads | `-fdump-rtl-ira -fdump-rtl-reload`, `-fira-verbose=5` |
| Which pattern emitted an insn | `-dp` (pattern name in asm comment) |
| Final RTL | `-fdump-rtl-final` |
| Everything | `-fdump-rtl-all` (large; avoid) |
