---
name: implement-feature
description: Checklist for implementing an rs6000 feature or RTL optimization: where it belongs, files to touch, validation.
---
# Skill: implement-feature

## Purpose
Guide the implementation of new backend features and optimizations in the GCC rs6000 backend while following existing GCC conventions, minimizing change scope, and preserving optimization correctness.

## When to Use
- Adding a new instruction pattern
- Enabling a new ISA feature
- Implementing a new option
- Adding new builtins
- Extending an existing optimization
- Adding combine patterns
- Improving instruction recognition
- Adding simplify-rtx support
- Extending RTL optimizations
- Improving register allocation interactions
- Backend cost model improvements

---

# Instructions

## 1. Understand the Existing Implementation

Before writing any code:

### Find similar implementations
Search for the closest existing implementation before introducing anything new.

Examples:

- Instruction patterns
  - `rs6000.md`
  - `altivec.md`
  - `vsx.md`
  - `mma.md`
  - `dfp.md`
  - Other rs6000 feature `.md` files

- Builtins
  - `rs6000-builtins.def`
  - `rs6000-builtin.cc`

- Options
  - `rs6000.opt`
  - `rs6000-cpus.def`

- RTL optimizations
  - Search where similar RTL transformations already exist.

Read the complete implementation first.

The new implementation should closely follow existing GCC coding style and backend conventions.

Do not invent a completely different implementation unless there is a strong technical reason.

---

## 2. Determine the Minimal Change Set

Only modify files directly involved in the feature.

Typical ISA feature:

- `rs6000-cpus.def`
- `rs6000.h`
- `rs6000.opt`
- `rs6000.cc`
- Feature `.md`
- `rs6000-builtins.def`
- `rs6000-builtin.cc`
- `rs6000-overload.def`
- `extend.texi`
- `invoke.texi`
- tests

Typical optimization work:

- `.md` files
- `combine.cc`
- `simplify-rtx.cc`
- `rtlanal.cc`
- `recog.cc`
- `emit-rtl.cc`
- `rtl.h`
- `optabs.cc`
- target hooks
- tests

Do not expand the scope unless absolutely necessary.

---

## 3. Understand the Optimization Pipeline

Before implementing any optimization, determine where it naturally belongs.

Typical RTL flow (dump names; full list in the `rtl-pass-order` skill):

```
GIMPLE → expand → cse1 → fwprop1 → ce1 → cse2 → combine → split1
       → ira → reload (LRA) → split2 → peephole2 → sched2 → final
```

`simplify-rtx.cc` is a library used by combine, cse and fwprop, not a pass.

Determine:

- Which pass currently generates the pattern.
- Which pass can recognize it.
- Whether the optimization should happen before or after register allocation.
- Whether a later pass already performs the optimization.
- Whether an existing canonicalization already exists.

Avoid implementing duplicate optimizations.

---

## 4. For Combine Pass Changes

When modifying `combine.cc`:

Before writing code:

- Read similar transformations.
- Understand why the existing transformation exists.
- Verify that the transformation is target independent or rs6000-specific.

Always verify:

- Does combine already generate the desired RTL?
- Is the RTL canonical?
- Is there an existing combine pattern that can be extended?
- Would a new define_split or define_insn be sufficient instead?

Avoid introducing target-specific logic into generic combine unless absolutely required.

Whenever possible:

- Prefer expressing the optimization through machine description patterns rather than special-case combine logic.

---

## 5. Understand simplify-rtx Interaction

Many combine-generated RTL expressions are immediately simplified.

Before changing combine:

Search whether simplify-rtx already handles the RTL.

Read functions such as:

- `simplify_gen_binary`
- `simplify_gen_unary`
- `simplify_binary_operation`
- `simplify_unary_operation`
- `simplify_subreg`
- `simplify_replace_fn_rtx`
- `simplify_const_unary_operation`
- `simplify_const_binary_operation`

Determine:

- Will simplify-rtx undo the transformation?
- Can simplify-rtx perform the optimization instead?
- Should a new simplification rule be added?

Avoid producing RTL that simplify-rtx immediately rewrites.

---

## 6. Follow Existing Canonical RTL Forms

Always determine the preferred RTL representation.

Search for existing uses of:

- `plus`
- `minus`
- `mult`
- `and`
- `ior`
- `xor`
- `ashift`
- `lshiftrt`
- `ashiftrt`
- `rotate`
- `subreg`
- `zero_extend`
- `sign_extend`
- `truncate`
- `vec_select`
- `vec_concat`
- `parallel`

Use the canonical RTL form expected by GCC (`rtl-canonical-forms` skill). Both the pattern and the code that generates the RTL must use it.

Do not introduce alternate RTL forms unless required.

---

## 7. Determine Whether the Optimization Belongs in the Machine Description

Before modifying C++ code, ask:

Can this optimization be implemented by:

- `define_insn`
- `define_expand`
- `define_split`
- `define_peephole2`
- splitters
- predicates
- constraints
- output templates

Prefer `.md` implementations whenever practical.

Avoid C++ logic when machine descriptions already provide the correct abstraction.

---

## 8. Writing Instruction Patterns

Follow the `rtl-patterns` skill.

Guidelines:

- Reuse predicates whenever possible.
- Add predicates only when necessary.
- Keep constraints minimal.
- Use existing constraint letters.
- Reuse iterators.
- Reuse mode iterators.
- Reuse code iterators.

Pattern naming:

- `<isa>_<mnemonic>`
- `<operation><mode>`
- Match surrounding naming conventions.

Always add appropriate `TARGET_*` guards.

---

## 9. ISA Features

For new ISA support:

- Add `OPTION_MASK_*`
- Add `TARGET_*`
- Guard every pattern
- Update CPU feature masks
- Verify interactions with existing ISA levels

Do not leave partially guarded code.

---

## 10. Builtins

Follow the `rs6000-builtins` skill.

Verify:

- builtin definition
- overloads
- expansion
- documentation
- folding
- argument handling
- pass-by-reference semantics where applicable

---

## 11. Register Allocation Considerations

Before introducing new RTL:

Consider:

- register classes
- earlyclobber
- matching constraints
- secondary reloads
- LRA behaviour
- hard register requirements
- register pressure

Avoid generating RTL that increases unnecessary reloads.

---

## 12. Cost Model

When introducing new instructions or optimizations:

Determine whether:

- instruction costs
- scheduling
- pipeline types
- DFA descriptions
- latency
- throughput

need updating.

Search existing similar instructions first.

---

## 13. Testing

Follow the `dejagnu` skill.

Minimum:

- compile test
- `scan-assembler`

Preferred:

- execution test
- optimization test

For optimization work also verify:

- optimization triggers
- optimization does not regress
- expected RTL appears
- expected instruction appears

Useful options:

```
-fdump-rtl-expand
-fdump-rtl-combine
-fdump-rtl-cse1
-fdump-rtl-fwprop1
-fdump-rtl-ira
-fdump-rtl-reload
-fdump-rtl-final
```

Inspect the dumps to verify that:

- combine produced the expected RTL
- simplify-rtx did not undo it
- LRA (pass `reload`) preserved it
- final emitted the intended instruction

---

## 14. Validation

Host Gate (`AGENTS.md`): build and test only on a Power host, after the user approves.
Otherwise list the commands for the user.

Examples:

```
make -C gcc rs6000.o
```

If machine descriptions changed, `make -C gcc` in the build dir regenerates and rebuilds the `insn-*.cc` files.

Run:

```
make check-gcc RUNTESTFLAGS="powerpc.exp=<test>"
```

For optimization work:

Run nearby optimization tests to ensure no regressions.

---

# Relevant Source Files

Backend:

- `gcc/config/rs6000/rs6000.cc`
- `gcc/config/rs6000/rs6000.md`
- `gcc/config/rs6000/*.md`
- `gcc/config/rs6000/predicates.md`
- `gcc/config/rs6000/constraints.md`
- `gcc/config/rs6000/rs6000-builtins.def`
- `gcc/config/rs6000/rs6000-builtin.cc`
- `gcc/config/rs6000/rs6000-overload.def`
- `gcc/config/rs6000/rs6000.opt`
- `gcc/config/rs6000/rs6000.h`
- `gcc/config/rs6000/rs6000-cpus.def`

RTL Optimization:

- `gcc/combine.cc`
- `gcc/simplify-rtx.cc`
- `gcc/recog.cc`
- `gcc/rtlanal.cc`
- `gcc/emit-rtl.cc`
- `gcc/optabs.cc`
- `gcc/ira*.cc`
- `gcc/lra*.cc`
- `gcc/final.cc`

Documentation:

- `gcc/doc/extend.texi`
- `gcc/doc/invoke.texi`

Testing:

- `gcc/testsuite/gcc.target/powerpc/`

---

# Expected Output

- Minimal patch affecting only the required files.
- At least one new test.
- Documentation updates where applicable.
- Proper commit message following the `commit-message` skill.
- Explanation of why the chosen implementation location is correct.
- Description of how the optimization interacts with combine, simplify-rtx, LRA, and final instruction selection.

---

# Common Pitfalls

- Implementing an optimization in combine that simplify-rtx immediately removes.
- Adding target-specific logic to generic optimization passes without necessity.
- Introducing non-canonical RTL.
- Forgetting `TARGET_*` guards.
- Creating duplicate optimizations already handled elsewhere.
- Using new predicates when existing ones are sufficient.
- Missing LRA implications.
- Breaking instruction recognition due to incorrect constraints.
- Writing tests that never trigger the optimization.
- Forgetting to inspect RTL dumps when debugging optimization behavior.
- Changing unrelated files instead of following the minimal change principle.
