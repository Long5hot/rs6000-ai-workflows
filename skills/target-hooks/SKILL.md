---
name: target-hooks
description: Find, implement, add or document a target hook/macro (target.def, tm.texi.in, generated tm.texi) for rs6000.
---
# Skill: target-hooks

## Where things live
| What | File |
|------|------|
| Hook declaration + doc string | `gcc/target.def` (`DEFHOOK (name, "doc", ret, (args), default)`) |
| Default implementation | `gcc/targhooks.cc` |
| rs6000 implementation | `gcc/config/rs6000/rs6000.cc`: `#undef TARGET_X` / `#define TARGET_X rs6000_x` |
| Old-style macros | `gcc/config/rs6000/rs6000.h`; documented by hand in `gcc/doc/tm.texi.in` |
| Doc placement | `gcc/doc/tm.texi.in`: one `@hook TARGET_X` line |
| `gcc/doc/tm.texi` | GENERATED. Never edit by hand. |

## Read a hook's contract (do not load tm.texi: 13k lines)
```sh
grep -n 'deftypefn.*TARGET_X\b' gcc/doc/tm.texi     # then read only that block
grep -n 'TARGET_X$' -A3 gcc/config/rs6000/rs6000.cc
```

## Add or change a hook
1. Edit `DEFHOOK` in `target.def` (doc string is Texinfo, lines end `\n\`).
2. New hook: add `@hook TARGET_X` in `tm.texi.in`; add default in `targhooks.cc`/`.h`.
3. Build. It stops with "copy it to .../doc/tm.texi": run
   `cp <build>/gcc/tm.texi <src>/gcc/doc/tm.texi`, rebuild.
4. Commit `target.def`, `tm.texi.in`, `tm.texi` together; ChangeLog entry for `doc/tm.texi` is `Regenerate.`

## Pitfalls
- Hand-editing `tm.texi` is caught by the build ("You should edit tm.texi.in").
- A middle-end hook change affects every target: test ≥2 architectures.
