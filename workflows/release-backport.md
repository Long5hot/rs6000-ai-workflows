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
git show --stat <trunk-commit>          # files the fix touches
# trunk commits to those files that the branch does not have:
git log --oneline releases/gcc-XX..<trunk-commit> -- <files>
```

For each dependency:
- Is it already on the release branch?
- Must it be backported first?
- Can the backport be adapted to avoid the dependency?

Record the dependency table in `TASK.md`.

## Step 4: Apply the patch

```sh
git checkout releases/gcc-XX
git gcc-backport <trunk-commit>   # = git cherry-pick -x; alias from contrib/gcc-git-customization.sh
```

If conflicts occur:
- Resolve manually.
- Document each conflict resolution in `TASK.md`.
- The resolution must be functionally equivalent to the trunk fix.

## Step 5: Test the backport

Host Gate (`AGENTS.md`): Power host only, after the user approves.

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

Keep the original commit message unchanged, including its ChangeLog block.
`git gcc-backport` appends `(cherry picked from commit <hash>)`; keep that line.
If conflicts were resolved by hand, adjust the ChangeLog entries to match the branch.
Check with `git gcc-verify`.

## Step 8: Submit for approval

Ask for approval on `gcc-patches@gcc.gnu.org`; name the target branch in the mail (`patch-submission` skill).
CC the Release Manager and rs6000 maintainers.
Include the test results summary.
Record the mailing list URL in `TASK.md`.
