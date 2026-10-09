# Workflow: Regression Analysis

Use this workflow when investigating a failing GCC test.
Load the `regression-analysis` skill before starting.

---

Host Gate (`AGENTS.md`): Steps 1, 3, 4 and 7 run a build or the compiler. Without a Power
host, work from the `.sum`/`.log`/dump files the user provides and ask for missing ones.

## Step 1: Reproduce the failure

```sh
make check-gcc RUNTESTFLAGS="powerpc.exp=<failing-test>.c"
```

Confirm the failure is reproducible. If it is not, classify as **flaky** and stop.

## Step 2: Read the failure message

Identify the failure type:
- `scan-assembler` — instruction not generated or wrong count
- `compile` — compilation error or ICE
- `run` — wrong runtime result or crash
- `XPASS` — unexpected pass (xfail needs removal)

## Step 3: Inspect the actual output

```sh
# For scan-assembler failures:
gcc -O2 -mcpu=XXXX <options-from-test> <test>.c -S -o /tmp/out.s
cat /tmp/out.s
```

Compare actual output against what the test expected.

## Step 4: Determine if the failure is newly introduced

If unsure whether the failure predates the current work:

```sh
git stash
make -j$(nproc)
make check-gcc RUNTESTFLAGS="powerpc.exp=<test>.c"
git stash pop
```

If it fails on the clean tree: **pre-existing**. Document and move on.
If it passes on the clean tree: **newly introduced** by the current work.

For bisection across multiple commits:
```sh
git bisect start
git bisect bad HEAD
git bisect good <last-known-good>
```

## Step 5: Identify the responsible code

Based on the failure type:

| Failure | Where to look |
|---------|--------------|
| Wrong instruction | Pattern conditions in `.md` file; combine interactions |
| Missing instruction | Pattern not matching; predicate too narrow |
| ICE | Stack trace; the crashing function |
| Wrong runtime result | RTL mode error; endianness; UB in test |
| Reload/LRA error | Constraint or register class issue |

Use `repo-map.md` to locate the relevant file.
Use `FindSymbol` to read the relevant function.

## Step 6: Formulate root cause hypothesis

Write a one-sentence root cause hypothesis in `TASK.md`.
Collect evidence (assembly diff, RTL dump, bisect result).

## Step 7: Fix and validate

- Implement the minimal fix.
- Re-run the failing test.
- Run the full PowerPC suite: `make check-gcc RUNTESTFLAGS="powerpc.exp"`
- Ensure no new failures are introduced.

## Step 8: Write the commit message

Follow the `commit-message` skill.
Include the root cause in the commit message body.
