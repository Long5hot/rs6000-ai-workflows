# Workflow: Implement Feature

Use this workflow when implementing a new rs6000 backend feature.
Load the `implement-feature` skill before starting.

---

## Step 1: Read the specification

- Identify the ISA spec section or user request.
- Note the instruction mnemonic(s), operand types, and conditions.
- Record in the task workspace.

## Step 2: Search for existing similar implementation

```sh
# Example: find similar instruction patterns
grep -r "define_insn.*xvbf16" gcc/config/rs6000/
# Example: find similar builtin definitions
grep -n "BU_P10" gcc/config/rs6000/rs6000-builtins.def | head -20
```

- Read the similar implementation completely.
- Note which files it touches — your implementation will touch the same files.

## Step 3: Identify the minimal change set

Using the similar implementation as a guide, list every file to be changed.
Record this list in `TASK.md` under "Affected Files".

## Step 4: Implement in order

Follow this order to avoid forward references:

1. `rs6000-cpus.def` — ISA mask (if new ISA feature)
2. `rs6000.h` — TARGET macro
3. `rs6000.opt` — option (if user-facing)
4. Feature `.md` file — instruction pattern
5. `predicates.md` — new predicate (if needed)
6. `rs6000-builtins.def` — builtin entry
7. `rs6000-overload.def` — overload entry (if overloaded)
8. `rs6000-builtin.cc` — expansion case
9. `rs6000.cc` — initialization or hook update (if needed)
10. Documentation
11. Test

## Step 5: Incremental build check

After each major change:
```sh
make -C gcc/ -j$(nproc) 2>&1 | head -50
```

Catch errors early; do not accumulate build errors.

## Step 6: Write the test

Follow the `dejagnu` skill.
Verify the test actually triggers the new code path by examining the assembly.

```sh
gcc -O2 -mcpu=powerXX <flags> test.c -S -o /tmp/test.s
grep "<expected-instruction>" /tmp/test.s
```

## Step 7: Write documentation

Follow the `documentation` skill.
Update `extend.texi` and/or `invoke.texi` as needed.

## Step 8: Final validation

```sh
# Run the new test
make check-gcc RUNTESTFLAGS="powerpc.exp=<test>.c"

# Run the full PowerPC suite
make check-gcc RUNTESTFLAGS="powerpc.exp"

# Full bootstrap (required before submission)
make bootstrap -j$(nproc)
```

## Step 9: Write the commit message

Follow the `commit-message` skill.
Record the final commit message in `TASK.md`.

## Step 10: Submit

Post to `gcc-patches@gcc.gnu.org`.
CC the rs6000 maintainers.
Record the mailing list URL in `TASK.md`.
