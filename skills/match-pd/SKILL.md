---
name: match-pd
description: Write or debug GIMPLE/GENERIC simplifications in gcc/match.pd (syntax, flags, predicates, testing).
---
# Skill: match-pd

Reference: `gcc/doc/match-and-simplify.texi`. `gcc/match.pd` → `genmatch` →
`gimple-match-*.cc`, `generic-match-*.cc`. Target-independent: test ≥2 architectures.

## Syntax
```
(simplify
 (bit_and:c (bit_not @0) @1)        ; match
 (if (INTEGRAL_TYPE_P (type))       ; optional C condition; `type` = result type
  (bit_xor @0 @1)))                 ; replacement
```
| Syntax | Meaning |
|--------|---------|
| `@0` `@name` | capture; same capture twice = equal operands |
| `@@0` | match by value (through conversions) |
| `pred@0` | operand must satisfy predicate (`integer_zerop`, `INTEGER_CST`) |
| `:c` | also match commuted |
| `:s` | fail if marked expr has >1 use and result is not a single op |
| `op!` (result) | apply only if this result expr folds to a simple operand |
| `cond^` | also match PHI |
| `convert?` `convert1?` `convert2?` | optional conversion |
| `{ C expr }` | C code yielding a tree that is a valid GIMPLE operand (e.g. a constant), not an expression |
| `(for op (plus minus) ...)` | repeat per operator; lists iterate in parallel |
| `(define_operator_list N a b)` | named operator list |
| `(switch (if c1 r1) (if c2 r2) default)` | chained conditions |
| `(with { tree t = ...; } ...)` | C locals; `(convert:t @0)` sets result type |
| `(match (name @0) pattern)` | define predicate, usable as `gimple_name` |
| `#if GIMPLE` / `#if GENERIC` | restrict IR |

Constants are already canonicalized to operand 2 before matching.

## Workflow
1. `grep -n` match.pd for the operator; extend a nearby pattern or `for` list.
2. Rebuild: `make -C gcc` in the build dir.
3. Confirm it fires: `-fdump-tree-all-folding`, search `Applying pattern match.pd:<line>`.
4. Test in `gcc/testsuite/gcc.dg/` with `scan-tree-dump "optimized"`; add a target test if codegen matters.

## Pitfalls
- Missing `:s` duplicates work when the inner expr has other uses.
- Check `TYPE_OVERFLOW_*`, `HONOR_NANS`, saturating/fixed-point types before arithmetic rewrites.
