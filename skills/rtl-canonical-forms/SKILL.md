---
name: rtl-canonical-forms
description: The canonical RTL contract - both md patterns and RTL generators must use the canonical shape; use when a pattern never matches or when writing/reviewing RTL-producing code.
---
# Skill: rtl-canonical-forms

Source: `gcc/doc/md.texi` node "Insn Canonicalizations"; operand order:
`commutative_operand_precedence` in `gcc/rtlanal.cc`.

## The contract (both sides)
- `recog` matches structurally. It never reorders or rewrites RTL to fit a pattern.
- **Patterns** (`define_insn`, `define_split`, `define_peephole2` input): write only the canonical form.
- **Generators** (`define_expand`, `gen_rtx_*` in backend C++, combine, simplify-rtx, any pass): emit only the canonical form. `simplify_gen_binary` simplifies and orders commutative operands; raw `gen_rtx_*` does neither.
- Pattern does not match because the generator emitted non-canonical RTL: fix the generator. Do not add a second, non-canonical pattern.
- Pattern is non-canonical: fix the pattern; passes are not meant to produce that shape.
- Two shapes, no documented rule: pick one in the generator (target-independent code) and match that; do not match both.

## Canonical forms
| Case | Canonical form |
|------|----------------|
| Commutative / comparison op with constant | constant is operand 2 |
| Associative ops (`and ior xor plus mult smin smax umin umax`) | chain to the left: `(plus (plus x y) z)` |
| One operand is `neg not mult plus minus` | that operand is first |
| `neg` with `mult plus minus` | pushed inward: `(mult (neg a) b)`; `(minus a (mult b c))` |
| `x - const` | `(plus x (const_int -n))` |
| x + y + const | `(plus (plus x y) const)` |
| andc | `(and (not a) b)` — `not` first |
| nand | `(ior (not a) (not b))` |
| nor | `(and (not a) (not b))` |
| xor with not | only `(xor x y)` or `(not (xor x y))` |
| Bit(s) == 0 test | `zero_extract`, not `and` / `sign_extract` |
| Left shift inside a `mem` address | `mult` by power of 2 |
| `compare`, first operand a CC reg | constant second |
| Insn that also sets CC | `compare` set is first in the `parallel` |
| `vec_merge` const mask | constant operand second, else mask LSB set |
| `(ltu (plus a b) b)` | `(ltu (plus a b) a)`; same for `geu` |
| `(sign_extend:M1 (mult:M2 (sign_extend x) (sign_extend y)))` | `(mult:M1 (sign_extend:M1 x) (sign_extend:M1 y))`; same for `zero_extend` |

## Check
- What combine tried: `-fdump-rtl-combine-details`, search `Failed to match this instruction`.
- rs6000 models: `grep -n 'define_expand "\(nor\|nand\|andn\|eqv\)<mode>3"' -A6 gcc/config/rs6000/rs6000.md`.
- Target-independent simplification belongs in `gcc/simplify-rtx.cc`; test ≥2 architectures.
