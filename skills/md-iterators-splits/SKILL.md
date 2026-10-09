---
name: md-iterators-splits
description: rs6000 .md iterators, attributes, define_insn_and_split and per-alternative ISA gating; use to write one pattern covering many modes/codes.
---
# Skill: md-iterators-splits

Reference: `gcc/doc/md.texi` nodes "Iterators", "Insn Splitting", "Insn Attributes".
Reuse existing iterators; list them with
`grep -n 'define_\(mode\|code\|int\)_\(iterator\|attr\)' gcc/config/rs6000/<file>.md`.

## Iterators
```
(define_mode_iterator GPR [SI (DI "TARGET_POWERPC64")])   ; per-mode condition
(define_mode_attr wd [(QI "b") (HI "h") (SI "w") (DI "d") ...])
(define_code_iterator any_extend [sign_extend zero_extend])
(define_int_iterator  UNSPEC_X [UNSPEC_A UNSPEC_B])
```
- In patterns: `:GPR` mode, `<MODE>` upper, `<mode>` lower, `<wd>` attr, `<GPR:mode>` to disambiguate.
- Common: `GPR` `P` `SDI` `INT` `SFDF` (rs6000.md), `VEC_A` (vector.md), `VSX_F` `VSX_L` `VI2` (vsx.md), `VM` (altivec.md).
- Name starting `@` (`"@foo<mode>"`) also generates `gen_foo (mode, ...)`.
- Name starting `*` is unnamed: no `gen_` function.

## define_insn_and_split
```
(define_insn_and_split "*name"
  [<pattern>]
  "<insn condition>"
  "#"                              ; "#" = must split
  "&& reload_completed"            ; leading && = insn condition AND this
  [<new insns>]
  { <prep C>; }                    ; optional; DONE / FAIL allowed
  [(set_attr "type" "...") (set_attr "length" "8")])
```
- `"&& 1"` splits as early as possible; `reload_completed` if hard regs are needed.
- `length` = bytes of the unsplit insn (4 per non-prefixed instruction).

## Attributes
- `type`: scheduling class; copy from a similar insn.
- `isa`: gates one alternative: `any p5 p6 p7 p7v p8 p8v p9 p9v p9kf p9tf p10 future mma dmf`.
  `[(set_attr "isa" "*,p9v")]` — one value per alternative, `*` = default.
- Whole-pattern gate stays in the condition string (`TARGET_...`).

## Pitfalls
- A conditional iterator mode ANDs with the pattern condition; do not repeat it.
- Every split output must match some `define_insn`.
- `.md` edits regenerate `insn-*.cc`; rebuild with `make -C gcc` in the build dir.
