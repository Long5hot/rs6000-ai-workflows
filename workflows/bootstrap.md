# Workflow: Bootstrap Validation

Use this workflow to validate a change before submission.
Load the `bootstrap` skill before starting.

---

## Step 1: Determine the rebuild scope

Consult the incremental rebuild table in the `bootstrap` skill.
Identify the minimum set of targets to rebuild.

For changes touching only `.md` files:
```sh
make -C gcc/ insn-recog.o insn-output.o insn-attrtab.o -j$(nproc)
```

For changes touching `.cc` or `.h` files:
```sh
make -C gcc/ -j$(nproc)
```

For any change before submission: full bootstrap.

## Step 2: Run an incremental build

```sh
make -j$(nproc) 2>&1 | tail -20
```

Fix any build errors before proceeding.

## Step 3: Run the PowerPC test suite

```sh
make check-gcc RUNTESTFLAGS="powerpc.exp" 2>&1 | grep -E "FAIL|ERROR|PASS|XFAIL"
```

Compare the result against the baseline (unpatched tree).
Record any new FAILs in the task workspace.

## Step 4: Full bootstrap

```sh
cd <build-directory>
# If not already configured:
../gcc-src/configure --enable-languages=c,c++ --disable-multilib \
    --prefix=/tmp/gcc-test

make bootstrap -j$(nproc) 2>&1 | tail -50
```

A successful bootstrap produces three identical compilers (stage1, stage2, stage3).
If stage 2 ≠ stage 3, there is a codegen correctness bug.

## Step 5: Post-bootstrap regression test

```sh
make -k check 2>&1 | grep "FAIL\|ERROR" | grep -v "^XFAIL" > /tmp/new-results.txt
```

Compare against a baseline results file:
```sh
diff /tmp/baseline-results.txt /tmp/new-results.txt
```

Any line appearing only in `new-results.txt` is a new failure — investigate before submitting.

## Step 6: Record the result

In `TASK.md`:
```
## Bootstrap

- [x] Incremental build passes
- [x] Full bootstrap passes
- [x] Regression suite: N new failures (list them, or: no new failures)
```

## Escalation

If a stage 2/3 comparison failure occurs:
1. Identify which compilation unit differs: `make compare` shows the diverging file.
2. Compile that file with `-fdump-rtl-final` at stage 2 and stage 3.
3. Diff the two dumps to find the diverging instruction.
4. Follow the `regression-analysis` workflow from step 5.
