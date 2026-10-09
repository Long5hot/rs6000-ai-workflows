---
name: contrib-git-tools
description: GCC contrib/ helpers for commits - ChangeLog skeleton (mklog), commit message check (gcc-verify), GNU style check, revision names (gcc-descr), backport; works on any host.
---
# Skill: contrib-git-tools

Host-independent (no GCC build needed). From the Host Gate output (`AGENTS.md`):
- `git_gcc_aliases=no` → use the "Direct" column.
- `py_*=no` → the script cannot run. Tell the user the missing modules; do not install them yourself:
  `pip3 install unidiff termcolor requests GitPython`.

`contrib/gcc-git-customization.sh` installs the aliases but is interactive (asks name,
email, remote). Never run it; ask the user to.

| Task | Alias | Direct |
|------|-------|--------|
| ChangeLog skeleton from a diff | `git diff \| git gcc-mklog` | `git diff \| contrib/mklog.py` |
| ... with PR lines | `git gcc-mklog -b 122431 <patch>` | `contrib/mklog.py -b 122431 <patch>` |
| Commit with generated skeleton | `git gcc-commit-mklog -b 122431` | — (alias only) |
| Check commit message + ChangeLog | `git gcc-verify [-n N] [-p] [<rev>]` | `contrib/gcc-changelog/git_check_commit.py ...` |
| GNU style check of a commit | `git gcc-style [<rev>]` | `git show <rev> \| contrib/check_GNU_style.py -` |
| GNU style check of the working tree | — | `git diff \| contrib/check_GNU_style.py -` |
| Hash → `rN-M-gHASH` name | `git gcc-descr [--short\|--full] [<rev>]` | `contrib/git-descr.sh ...` |
| `rN-M` name → hash | `git gcc-undescr r17-4418` | `contrib/git-undescr.sh r17-4418` |
| Backport to a release branch | `git gcc-backport <hash>` | `git cherry-pick -x <hash>` |
| Old SVN revision → commit | `git svn-rev <NNN>` | — |

## Notes
- `mklog.py` options: `-b PRs` (comma separated), `-s` no function names, `-p` fetch PR titles (network), `-c <msgfile>` append to a commit message file, `-a` append to the patch file.
- `mklog` output is a skeleton: the `PR` component and every description after the colon must be written by hand.
- `gcc-verify` defaults to `HEAD`; `-n 3` checks the last 3 commits; `-p` prints the resulting ChangeLog entries.
- Style checks: line length, 8 spaces instead of tab, space before tab, trailing whitespace, sentence spacing, space before `(`, braces on own line, trailing operators.
- Formatting only touched lines: copy `contrib/clang-format` to `.clang-format` (do not commit it), then `git diff -U0 --no-color | clang-format-diff -p1` prints a suggested patch. The GNU style check decides.
- The customization script also sets `sendemail.to=gcc-patches@gcc.gnu.org` and a `.md` diff hunk header (`define...` names).

## Other contrib scripts (rarely needed)
| Script | Use |
|--------|-----|
| `download_prerequisites` | fetch GMP/MPFR/MPC/ISL into the source tree before a build (Power host; network) |
| `update-copyright.py` | yearly copyright bump; not for normal patches |
| `check-params-in-docs.py` | compare `--help=params` with `params.texi` (needs a built compiler) |
| `mdcompact/mdcompact.el` | Emacs: convert `define_insn` to compact syntax |
| `vimrc`, `vim-gcc-dev/` | Vim settings for GNU style; syntax for `match.pd`, RTL and GIMPLE dumps |
