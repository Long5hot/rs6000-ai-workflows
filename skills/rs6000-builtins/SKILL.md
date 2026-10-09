---
name: rs6000-builtins
description: Add, change or debug an rs6000 built-in function or vec_* overload (.def stanza syntax, expansion, folding, docs, test).
---
# Skill: rs6000-builtins

Authoritative syntax: the header comments of `gcc/config/rs6000/rs6000-builtins.def`
and `rs6000-overload.def` (type abbreviations, attributes, const-int ranges). Read them.

## Layers
| Layer | File | Notes |
|-------|------|-------|
| Definitions | `rs6000-builtins.def` | one entry per non-overloaded builtin |
| Overloads | `rs6000-overload.def` | maps `vec_*` + argument types to a builtin ID |
| Generator | `rs6000-gen-builtins.cc` | build-time; writes `rs6000-builtins.cc/.h`, `rs6000-vecdefines.h` |
| Overload resolution | `rs6000-c.cc` | `altivec_resolve_overloaded_builtin` |
| GIMPLE folding | `rs6000-builtin.cc` | `rs6000_gimple_fold_builtin` |
| RTL expansion | `rs6000-builtin.cc` | `rs6000_expand_builtin` |
| Pattern | `.md` files | the `define_insn`/`define_expand` named in the entry |

Generated enums: `RS6000_BIF_<ID>`, `RS6000_OVLD_<ID>`.

## Builtin entry (`rs6000-builtins.def`)
```
[power10]
  const vbq __builtin_altivec_cmpge_1ti (vsq, vsq);
    CMPGE_1TI vector_nltv1ti {}
```
- `[gate]` stanza header enables every entry below it. Gates: `always power5 power6 power6-64 altivec cell vsx power7 power7-64 power8-vector power9-vector power9 power9-64 ieee128-hw dfp crypto htm power10 power10-64 mma future-vsx future-altivec dm`.
- Line 1: `[const|pure|fpmath] <ret> <name> (<args>);`
- Line 2: `<ID> <pattern> {<attrs>}` — braces required even when empty.
- Types must match the modes of `<pattern>`.

## Overload entry (`rs6000-overload.def`)
```
[VEC_ADD, vec_add, __builtin_vec_add]
  vsc __builtin_vec_add (vsc, vsc);
    VADDUBM  VADDUBM_VSC
```
- Header: `[<OVLD_ID>, <abi-name or SKIP>, <builtin-name>]`.
- Per instance: prototype, then `<BIF_ID> [<unique instance id>]`. The second token is required when one `<BIF_ID>` serves several signatures.
- `<BIF_ID>` must exist in `rs6000-builtins.def`.

## Add a builtin
1. Write or find the pattern (`rtl-patterns` skill).
2. Add the entry under the right stanza, next to similar entries.
3. Expansion is automatic: `rs6000_expand_builtin` uses the entry's pattern. Edit `rs6000-builtin.cc` only for special handling (existing attribute, or a `case RS6000_BIF_<ID>:`).
4. Overloaded: add instances in `rs6000-overload.def`.
5. Document in `gcc/doc/extend.texi` (`documentation` skill); test (`dejagnu` skill).
6. Rebuild with `make -C gcc` in the build dir; the generator reruns automatically.

## Investigate a builtin
```sh
grep -n -A1 '__builtin_altivec_vaddubm ' gcc/config/rs6000/rs6000-builtins.def   # ID + pattern
grep -n 'RS6000_BIF_VADDUBM' gcc/config/rs6000/rs6000-builtin.cc                # folding / special handling
grep -n '"<pattern>"' gcc/config/rs6000/*.md
```

## Pitfalls
- Wrong stanza: builtin enabled under the wrong ISA.
- Prototype types not matching the pattern's modes.
- Duplicate builtin name or ID (each must be unique).
- Blank lines are allowed only between entries, not inside one.
