# Backport Task Template

Copy this file to `.ai/work/<task-name>/TASK.md` and fill in each section.
Delete this instruction line before use.

---

## Summary

<!-- One sentence: what is being backported, and to which release branch? -->


## Task Name

<!-- Short identifier: e.g., pr120384-gcc14-backport -->


## Status

<!-- Planning / In progress / Tested / Submitted / Committed -->


## Target Branch

<!-- Which release branch? -->

Branch: `releases/gcc-XX`
Release: GCC XX.Y


## Upstream Reference

<!-- The trunk commit(s) being backported. -->

Trunk commit:
Commit message subject:
Mailing list thread:


## Justification

<!-- Why is this backport appropriate?
     Is this a regression fix? A serious correctness bug?
     Does it meet GCC release branch criteria? -->


## Dependency Analysis

<!-- Does the upstream commit depend on other trunk changes?
     List any prerequisite commits and whether they are already on the branch. -->

| Dependency | On branch? | Notes |
|------------|------------|-------|
| | | |


## Conflicts

<!-- List any merge conflicts and how they were resolved. -->

| File | Conflict type | Resolution |
|------|---------------|------------|
| | | |


## Patch

<!-- Paste the backport diff here, or link to a file in this directory. -->

Original upstream diff:
```diff
```

Backport diff (after conflict resolution):
```diff
```


## Testing

- [ ] Testcase from upstream commit included (or adapted)
- [ ] Test passes on the release branch
- [ ] No new failures on the release branch
- [ ] Run: `make check-gcc RUNTESTFLAGS="powerpc.exp"`


## Bootstrap

- [ ] Incremental build passes on release branch
- [ ] Full bootstrap passes on release branch (if required by release policy)


## Review Notes

<!-- Notes from the review process. -->


## Approval

<!-- Record RM or maintainer approval. -->

- [ ] Approved by:
- [ ] Committed as:
