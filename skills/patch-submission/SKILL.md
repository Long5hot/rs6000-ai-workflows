---
name: patch-submission
description: Format, verify and mail a GCC patch to gcc-patches (subject tags, versions, pings, series, testing statement, ChangeLog check).
---
# Skill: patch-submission

Use after the commit exists. Message body rules: `commit-message` skill.

## Subject
`[PATCH] <component>: <title> [PR<n>]` — e.g. `[PATCH] rs6000: Fix vec_permx wrong-code [PR125138]`

| Case | Tag | Thread |
|------|-----|--------|
| New version | `[PATCH v2]` | new thread; list changes since v1 |
| Series | `[PATCH 1/3]` | replies to `[PATCH 0/3]` cover (cover is not committed) |
| No reply | prefix `[PING n]` | reply in the same thread |

## Email body
- What and why. One logical change per patch; split refactor from fix.
- Testing line: `Bootstrapped and regtested on powerpc64le-linux-gnu with no regressions.` Write it only if that run happened; otherwise leave `<TESTING: to be filled by user>`. Add `powerpc64-linux-gnu` (BE) when endian-sensitive.
- Non-target change (middle-end, match.pd, combine): test on ≥2 architectures.
- Branch, if not trunk.
- Body wrap 72. ChangeLog lines: checker limit 100, keep ≤80.

## ChangeLog block
```
gcc/ChangeLog:
	PR target/122431
	* config/rs6000/altivec.md (*altivec_vsl<VI_char>_const_1): New
	define_insn.

gcc/testsuite/ChangeLog:
	PR target/122431
	* gcc.target/powerpc/pr122431-1.c: New test.
```
- Indent is one TAB. Paths relative to the ChangeLog's directory.
- PR component = Bugzilla component: backend bugs are `target`, never `rs6000`.
- Optional author line before the block: `YYYY-MM-DD  Name  <email>`.

## Commands
Aliases missing or Python modules missing: see `contrib-git-tools` skill. Never send mail
or run the interactive customization script yourself; give the commands to the user.
```sh
git gcc-commit-mklog                  # commit with generated ChangeLog skeleton
git gcc-verify                        # check HEAD message (git_check_commit.py)
git gcc-style                         # GNU style check of HEAD
git format-patch -1
git send-email --to=gcc-patches@gcc.gnu.org --cc=<maintainer> 0001-*.patch
```
Maintainers: `grep -n 'rs6000/powerpc port' MAINTAINERS`.
Backport: `git gcc-backport <hash>` (= `cherry-pick -x`), retest on the branch.
