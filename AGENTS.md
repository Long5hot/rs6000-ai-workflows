# AGENTS.md — GCC PowerPC Backend Development

Standing instructions for every task. Do not modify for task-specific work.

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
| `gcc/` | Compiler middle-end (optabs, recog, ira, lra, reload) |

---

## Coding Philosophy

- **Minimal changes.** Fix only what is broken. Do not refactor surrounding code.
- **Correctness first.** A correct slow implementation beats a fast incorrect one.
- **Follow existing patterns.** Find a similar existing implementation and follow it.
- **No dead code.** Remove or never add unreachable paths.
- **No style changes** in patches that fix correctness or add features.

## GCC Coding Style

- GNU coding style: 2-space indentation, no tabs in C code.
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
- Patches must bootstrap and pass regression tests on the target architecture.

## Testing Philosophy

- Every functional change requires at least one new DejaGnu testcase.
- Tests live in `gcc/testsuite/gcc.target/powerpc/`.
- Tests must be self-contained and not depend on external state.
- Use `dg-require-effective-target` to guard ISA-specific tests.
- Use `scan-assembler` to verify code generation; use execution tests for correctness.
- A test that can be compile-only should be compile-only.

## Documentation Philosophy

- Every new builtin requires a `@item` entry in `gcc/doc/extend.texi`.
- Every new option requires an entry in `gcc/doc/invoke.texi`.
- Follow existing Texinfo formatting exactly (spacing, node structure, `@deftypefn`).
- Keep documentation in sync with implementation in the same patch.

---

## Default Development Workflow

1. Read `repo-map.md` to locate relevant files.
2. Search the repository for similar existing implementations before writing new code.
3. Read only the functions needed — not entire files.
4. Load only the skills relevant to the current task.
5. Implement the minimal correct change.
6. Write or update the testcase.
7. Update documentation if required.
8. Write the commit message using the `commit-message` skill.

---

## General Rules

- Search before asking. Inspect the repository before making assumptions.
- Read only what is needed. Prefer `FindSymbol` and `grep` over full file reads.
- Never modify `AGENTS.md`, skills, templates, or workflows for a specific task.
- All task-specific notes go in `.ai/work/<task-name>/`.
- When a result is uncertain, re-inspect the source.
