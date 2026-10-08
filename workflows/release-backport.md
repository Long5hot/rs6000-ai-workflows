# Workflow: Release Backport

Use this workflow when backporting a trunk fix to a GCC release branch.
Load the `regression-analysis` skill if the backport is for a regression fix.

---

## Step 1: Verify the backport is appropriate

GCC release branch policy:
- **Allowed**: regression fixes, serious correctness bugs, ICE fixes.
- **Not allowed**: new features, optimizations, non-critical cleanups.
- When in doubt: ask the Release Manager (RM).

Confirm that the upstream commit message describes a fix that meets these criteria.

## Step 2: Identify the upstream commit

```sh
git log --oneline --grep="<keywords>" gcc/config/rs6000/
```

Record the commit hash and subject in `TASK.md`.

## Step 3: Dependency analysis

Check whether the upstream fix depends on other trunk commits that are not on the branch:

```sh
git log <trunk-commit>^..HEAD --oneline -- gcc/config/rs6000/ | head -20
```

For each dependency:
- Is it already on the release branch?
- Must it be backported first?
- Can the backport be adapted to avoid the dependency?

Record the dependency table in `TASK.md`.

## Step 4: Apply the patch

```sh
git checkout releases/gcc-XX
git cherry-pick <trunk-commit>
```

If conflicts occur:
- Resolve manually.
- Document each conflict resolution in `TASK.md`.
- The resolution must be functionally equivalent to the trunk fix.

## Step 5: Test the backport

```sh
# Build
make -j$(nproc)

# Run relevant tests
make check-gcc RUNTESTFLAGS="powerpc.exp=<affected-test>.c"

# Run the full PowerPC suite
make check-gcc RUNTESTFLAGS="powerpc.exp"
```

Compare results against the release branch baseline (before the backport).
No new failures should be introduced.

## Step 6: Bootstrap (if required)

Release branch patches that touch core files should be bootstrapped.
Follow the `bootstrap` workflow.

## Step 7: Write the commit message

The backport commit message should:
- Reference the upstream commit: `Backported from trunk: <commit-hash>`
- State the original commit message subject.
- Note any conflict resolutions.

Example:
```
rs6000: Fix vec_sel mask order on LE (backport)

Backport of trunk commit abc123:
  rs6000: Fix incorrect vec_sel codegen on LE POWER9

No conflicts.

gcc/ChangeLog:

	* config/rs6000/rs6000-call.cc (rs6000_expand_vector_select):
	Reverse mask operand order for LE targets.

gcc/testsuite/ChangeLog:

	* gcc.target/powerpc/vec-sel-le-regression.c: New test.
```

## Step 8: Submit for approval

Post to `gcc-patches@gcc.gnu.org` with `[BACKPORT GCC-XX]` in the subject.
CC the Release Manager and rs6000 maintainers.
Include the test results summary.
Record the mailing list URL in `TASK.md`.
