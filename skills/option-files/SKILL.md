---
name: option-files
description: Add or change an rs6000 -m option (.opt record syntax, ISA mask bits, invoke.texi entry, opt.urls regeneration).
---
# Skill: option-files

Reference: `gcc/doc/options.texi`. File: `gcc/config/rs6000/rs6000.opt`.

## Record = 3 parts, blank line between records
```
mpcrel
Target Mask(PCREL) Var(rs6000_isa_flags)
Generate (do not generate) pc-relative memory addressing.
```
`Mask(PCREL) Var(rs6000_isa_flags)` generates `OPTION_MASK_PCREL` and `TARGET_PCREL`.

| Property | Meaning |
|----------|---------|
| `Target` | target option (always for `-m`) |
| `Mask(N)` / `InverseMask(N)` | flag bit in `Var`, or `target_flags` |
| `Var(v)` `Init(n)` | backing variable and default |
| `Save` | saved/restored in `cl_target_option` |
| `Joined` / `Separate` / `JoinedOrMissing` | takes argument: `-mfoo=x` / `-mfoo x` |
| `RejectNegative` | no `-mno-` form |
| `Negative(other)` | this option turns off `other` |
| `Enum(name)` | argument from an `Enum`/`EnumValue` record set |
| `UInteger` `IntegerRange(a,b)` | numeric argument |
| `Undocumented` | deliberately undocumented; hidden from `--help` |
| `WarnRemoved` / `Ignore` | removed option, warns on use / option is ignored |
| `Alias(opt)` | synonym |
| `Condition(c)` | accepted only if preprocessor condition `c` is true |

## Checklist for a new option
1. Record in `rs6000.opt` (model on a neighbour).
2. ISA flag: add to the mask sets in `rs6000-cpus.def` (`ISA_*_MASKS*`, `POWERPC_MASKS`) so `-mcpu=` handles it; add to `rs6000_opt_masks[]` in `rs6000.cc` to allow it in `target` attribute/pragma.
3. `gcc/doc/invoke.texi`, node "RS/6000 and PowerPC Options", plus the option summary list:
   ```texinfo
   @opindex mfoo
   @opindex mno-foo
   @item -mfoo
   @itemx -mno-foo
   Text.  State default and required ISA.
   ```
   `@opindex` lines go BEFORE `@item`.
4. Regenerate `rs6000.opt.urls`: `make -C gcc regenerate-opt-urls` in the build dir (needs HTML docs built); commit it.
5. Rebuild: `make -C gcc` (options.h regenerates; most objects recompile).

Naming and wording rules: `gcc/doc/ux.texi` "Guidelines for Options".
