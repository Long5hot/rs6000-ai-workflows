---
name: documentation
description: Document an rs6000 builtin (extend.texi) or -m option (invoke.texi) in the Texinfo form the PowerPC sections actually use.
---
# Skill: documentation

Both files are huge (32k / 38k lines): grep for the node, read only nearby entries, copy their form exactly.

| File | Content | Note |
|------|---------|------|
| `gcc/doc/extend.texi` | builtins, attributes, pragmas | PowerPC builtins grouped by ISA node |
| `gcc/doc/invoke.texi` | options | node "RS/6000 and PowerPC Options" |
| `gcc/doc/md.texi` | constraints, pattern names | PowerPC constraints table |
| `gcc/doc/tm.texi` | target hooks | GENERATED: see `target-hooks` skill |

## Builtin (extend.texi)
Find the node: `grep -n '^@node.*PowerPC' gcc/doc/extend.texi`
(e.g. "PowerPC AltiVec Built-in Functions Available on ISA 3.1"). Add next to related builtins.

`vec_*` overloads — prototype list, then prose:
```texinfo
@smallexample
@exdent int vec_test_lsbb_all_ones (vector signed char);
@exdent int vec_test_lsbb_all_ones (vector unsigned char);
@end smallexample
@findex vec_test_lsbb_all_ones

The builtin @code{vec_test_lsbb_all_ones} returns 1 if the least significant
bit in each byte is equal to 1.  It returns 0 otherwise.
```
`__builtin_*` functions:
```texinfo
@defbuiltin{{long long} __builtin_darn (void)}
@defbuiltinx{int __builtin_darn_32 (void)}
Description.  State the required ISA / option.
@enddefbuiltin
```
- Multi-word return types go in an extra brace pair: `{{long long} name (args)}`.
- One prototype per accepted type combination; must match `rs6000-overload.def` / `rs6000-builtins.def`.

## Option (invoke.texi)
Find: `grep -n '@node RS/6000 and PowerPC Options' gcc/doc/invoke.texi`
```texinfo
@opindex mfoo
@opindex mno-foo
@item -mfoo
@itemx -mno-foo
Generate (do not generate) foo instructions.  The @option{-mfoo}
option requires that the option @option{-mcpu=power10} (or later)
is enabled.
```
- `@opindex` lines go BEFORE `@item`; one per spelling, without the leading `-`.
- Valued option: `@item -mbar=@var{value}`; literal values in `@samp{}`; state the default.
- Also add the option to the summary list (`grep -n '@emph{RS/6000 and PowerPC Options}' gcc/doc/invoke.texi`).
- Name must equal the record name in `rs6000.opt`. Then regenerate `rs6000.opt.urls` (`option-files` skill).

## Markup
`@code{}` code/types, `@var{}` metasyntactic names, `@option{}` options, `@samp{}` literal values. Two spaces after a sentence-ending period.

## Consistency checklist
- [ ] Return and parameter types in `extend.texi` match the builtin's real signature.
- [ ] The ISA requirement is stated (`-mcpu=power10`, `-mvsx`, ...).
- [ ] The entry is under the correct ISA node, next to related entries.
- [ ] One `@opindex` per option spelling, before `@item`.
- [ ] The option name in `invoke.texi` equals the record name in `rs6000.opt`; the summary list is updated.
- [ ] Restrictions (endianness, 64-bit only, alignment) are documented.

## Check
- Build the manuals in the build dir: `make -C gcc info`. Fix every warning in the touched region.
- Same patch as the implementation; ChangeLog: `* doc/extend.texi (<node name>): Document ...`.

## Relevant files
- `gcc/doc/extend.texi`, `gcc/doc/invoke.texi` — search, never read whole.
- `gcc/config/rs6000/rs6000.opt` — source of truth for option names.
- `gcc/config/rs6000/rs6000-builtins.def`, `rs6000-overload.def` — builtin names and signatures.

## Expected output
- `extend.texi` and/or `invoke.texi` updated in the right node, in the form of the adjacent entries.
- No new Texinfo warnings.

## Pitfalls
- `@opindex` after `@item` (old style; not used any more).
- Prototype types differing from the implementation.
- Entry placed under the wrong ISA node.
- Citing removed options (`-mpower8-vector`, `-mpower9-vector`, `-mpower10`); use `-mcpu=powerN`.
