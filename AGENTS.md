# AGENTS.md — GCC PowerPC Backend Development

Standing instructions for every task. Do not modify for task-specific work.

---

## Directory Name

`.ai/` in every file of this framework is a placeholder for this framework's own
directory. Its real name is `.` + the assistant in use: `.claude`, `.bob`, `.copilot`, ...
(or `rs6000-ai-workflows` when cloned under its repository name).
Resolve it as the directory that contains this file; `bin/env-check.sh` prints it as
`framework=`. Substitute that path wherever a file says `.ai/`.

---

## Repository

GCC trunk (version 17.0.0). C/C++ source. GNU Autotools build system.
Focus: **rs6000 (PowerPC/POWER) backend** exclusively.

Out of scope: Ada, COBOL, D, Go, Fortran, JIT frontend, libstdc++, libgomp,
libquadmath, libsanitizer, libffi, libobjc, zlib.

---

## Primary Directories

| Path | Purpose |
|------|---------|
| `gcc/config/rs6000/` | All rs6000 backend source and machine descriptions |
| `gcc/testsuite/gcc.target/powerpc/` | PowerPC-specific DejaGnu tests |
| `gcc/doc/` | GCC documentation (Texinfo) |
| `gcc/` | Compiler middle-end (optabs, recog, combine, simplify-rtx, ira, lra) |

---

## Host Gate (run first, every session)

```sh
sh .ai/bin/env-check.sh     # read-only
```
Obey the `policy=` line it prints. Every `configure`, `make`, test or compiler
command in any skill, workflow or template is conditional on it.

| Policy | Meaning | Allowed | Forbidden |
|--------|---------|---------|-----------|
| `NO_BUILD` | not a Power host, no PowerPC compiler | read, grep, edit, git, host-independent `contrib/` scripts | configure, make, bootstrap, `make check`, building a cross compiler, compiling tests |
| `COMPILE_ONLY` | not a Power host, PowerPC compiler already exists | the above, plus that compiler with `-S` on single files | configure, make, bootstrap, `make check`, running test binaries |
| `ASK_FIRST` | Power host | everything, after the user approves that specific action | starting any build or test run unasked |

- The host's own `gcc`/`cc` does not target PowerPC. Never use it to check rs6000 code generation.
- Never install packages or build a cross compiler unless the user asks.
- Forbidden step: do not attempt it and do not substitute something else. Write the exact commands under "Run on a Power host:" for the user, and continue with the work that is allowed.
- Never report a build or test as done unless it ran in this session. Record it as `NOT RUN (host)` in `TASK.md`.
- `ASK_FIRST`: ask once per action, naming the command. Approval of an incremental build does not cover a bootstrap or `make check`.
- Script unavailable: run `uname -sm`. Anything other than `ppc64le`, `ppc64` or `AIX` is `NO_BUILD`.

---

## Coding Philosophy

- **Minimal changes.** Fix only what is broken. Do not refactor surrounding code.
- **Correctness first.** A correct slow implementation beats a fast incorrect one.
- **Follow existing patterns.** Find a similar existing implementation and follow it.
- **No dead code.** Remove or never add unreachable paths.
- **No style changes** in patches that fix correctness or add features.

## GCC Coding Style

- GNU coding style: 2-space indentation steps; each 8 leading columns is one tab. Check with `contrib/check_GNU_style.py <patch>`.
- Function definitions: return type on its own line.
- 80-column line limit (soft); machine descriptions may exceed it minimally.
- Use `gcc_assert` for invariants, not `assert`.
- Prefer `rtx_insn *`, `rtx`, `tree` types over raw pointers.
- Use `HOST_WIDE_INT` and `poly_int` where appropriate for target-dependent sizes.

## Patch Philosophy

- One logical change per patch.
- Preserve backward compatibility unless explicitly breaking it.
- Document non-obvious decisions in comments at the point of use.
- Keep unrelated cleanups in a separate patch.
- Patches must bootstrap and pass regression tests on a Power host before submission. Under `NO_BUILD` that is the user's step: hand over the commands.

## Testing Philosophy

- Every functional change requires at least one new DejaGnu testcase.
- Tests live in `gcc/testsuite/gcc.target/powerpc/`.
- Tests must be self-contained and not depend on external state.
- Use `dg-require-effective-target` to guard ISA-specific tests.
- Use `scan-assembler` to verify code generation; use execution tests for correctness.
- A test that can be compile-only should be compile-only.

## Documentation Philosophy

- Every new user-visible builtin requires an entry in `gcc/doc/extend.texi`.
- Every new option requires an entry in `gcc/doc/invoke.texi`.
- Follow existing Texinfo formatting exactly (spacing, node structure, `@deftypefn`).
- Keep documentation in sync with implementation in the same patch.

---

## Default Development Workflow

0. Run the Host Gate check.
1. Read `repo-map.md` to locate relevant files.
2. Search the repository for similar existing implementations before writing new code.
3. Read only the functions needed — not entire files.
4. Load only the skills relevant to the current task.
5. Implement the minimal correct change.
6. Write or update the testcase.
7. Update documentation if required.
8. Build and test only as the Host Gate allows; otherwise list the commands for the user.
9. Write the commit message using the `commit-message` skill.

---

## General Rules

- Search before asking. Inspect the repository before making assumptions.
- Read only what is needed. Prefer `FindSymbol` and `grep` over full file reads.
- Never modify `AGENTS.md`, skills, templates, or workflows for a specific task.
- All task-specific notes go in `.ai/work/<task-name>/`.
- When a result is uncertain, re-inspect the source.
