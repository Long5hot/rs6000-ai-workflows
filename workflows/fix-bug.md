# Workflow: Fix Bug

Trigger: "fix bug <N>", "fix PR <N>", "fix <N>". Work through every step without
asking the user to paste anything. Ask only when the Host Gate requires approval or
the report is truly ambiguous about what is wrong.

---

## Step 1: Fetch and set up

```sh
sh .ai/bin/env-check.sh
python3 .ai/bin/bz.py <N>
mkdir -p .ai/work/pr<N> && cp .ai/templates/bug/TEMPLATE.md .ai/work/pr<N>/TASK.md
```
Use `templates/regression/` instead when the summary says `Regression` or names a first bad revision.
Record in `TASK.md`: summary, keywords, target, component, policy line.
Already `RESOLVED FIXED`: say so, show the fixing commit, stop.

## Step 2: Extract the reproducer

- Testcase in a comment → write `.ai/work/pr<N>/pr<N>.c` (use `-c <n> --full` if cut). Attachment → `bz.py <N> -a <id>`.
- From the comments take: options and `-mcpu`, expected vs actual output, first bad revision, any analysis or proposed fix by maintainers.
- Read `see_also` bugs as context only.

## Step 3: Classify and load skills

| Keyword / symptom | Start with |
|-------------------|------------|
| `ice-on-valid-code`, `ice-on-invalid-code` | the function and assert named in the backtrace; `rtl-patterns` or `rs6000-builtins` |
| `wrong-code` | `rtl-patterns`, `rtl-canonical-forms`; check BE/LE and modes |
| `missed-optimization` | `rtl-pass-order`, `rtl-canonical-forms`, `optimization`; `match-pd` if GIMPLE |
| `testsuite-fail` | `dejagnu`, `regression-analysis`; decide: compiler bug or test needs updating |
| LRA / constraint error | `register-allocation` |
| first bad revision given | `git show <rev>` first; the bug is usually in or exposed by that change |

## Step 4: Locate and find the root cause

1. `repo-map.md` → candidate files. `git grep` for the pattern, builtin, function or error text from the report.
2. Read only the functions involved.
3. Write the root cause in one sentence in `TASK.md` before editing anything. No root cause, no patch.
4. Evidence needs compiler output (assembly, RTL dumps): Host Gate. Not allowed here → use the dumps quoted in the bug, or ask the user for the specific dump (`rtl-pass-order` skill names the flag).

## Step 5: Fix

- Minimal change at the root cause; follow the nearest similar code.
- Target-independent file (`combine.cc`, `simplify-rtx.cc`, `match.pd`): the change must be right for every target.
- GNU style: tabs for each 8 columns, 80 columns.

## Step 6: Test

- Add `gcc/testsuite/gcc.target/powerpc/pr<N>.c` (`dejagnu` skill) from the reproducer: fails before the fix, passes after.
- Existing test with a wrong expectation: fix that test instead of adding one.

## Step 7: Validate (Host Gate)

| Policy | Do |
|--------|----|
| `NO_BUILD` | run nothing; write the commands under "Run on a Power host:" |
| `COMPILE_ONLY` | compile `pr<N>.c` with `-S` and check the output; list the rest for the user |
| `ASK_FIRST` | ask, then incremental build → new test → `make check-gcc RUNTESTFLAGS="powerpc.exp"`; bootstrap + full regtest needs its own approval |

Commands to hand over:
```sh
make -C gcc -j$(nproc)
make check-gcc RUNTESTFLAGS="powerpc.exp=pr<N>.c"
make bootstrap -j$(nproc) && make -k check -j$(nproc)
contrib/compare_tests <baseline-build> <patched-build>
```

## Step 8: Finish

1. Style: `git diff | contrib/check_GNU_style.py -` (`contrib-git-tools` skill; skip if modules are missing and say so).
2. Commit message (`commit-message` skill): subject ends `[PR<N>]`, ChangeLog has `PR <component>/<N>`. Put it in `TASK.md`. Do not commit, push or send mail unless asked.
3. Report: root cause, what changed (files), new test, what was validated and what was NOT RUN, commands for the user.

## Stop and report instead of patching when

- The root cause cannot be established from the report and the source.
- The fix needs a design decision (ABI, new option, behaviour change for other targets).
- A maintainer in the bug rejected the approach you would take.
