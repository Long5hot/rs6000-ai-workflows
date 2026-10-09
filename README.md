# GCC PowerPC Backend — AI Development Framework

This framework is a permanent development assistant for GCC PowerPC (rs6000) backend work.
It is designed to be reused across branches, worktrees, bug fixes, features, and backports
without regeneration.

---

## Installation and Directory Name

Clone into the root of the GCC checkout, named `.` + the assistant you use:

```sh
git clone <this-repo-url> .bob        # or .claude, .copilot, ...
```

All files write the path as `.ai/`. That is a placeholder for whatever name you chose;
`AGENTS.md` tells the assistant to substitute the real directory, and
`bin/env-check.sh` prints it as `framework=`. Nothing needs editing after a rename.

---

## Design Principles

- **Retrieval over loading.** Read only the files and functions needed for the current task.
- **Minimal tokens.** Avoid loading entire files. Prefer targeted symbol lookups.
- **No duplication.** Repository knowledge lives in the repository. This framework holds only pointers and workflow guidance.
- **Separation of concerns.** Permanent knowledge lives in `skills/`. Task-specific work lives in `work/`.
- **Focused scope.** This framework covers the rs6000 backend only. Frontend, runtime library, and unrelated compiler middle-end content is explicitly excluded.

---

## Directory Layout

```
.ai/
├── README.md            — This file. Framework overview and usage guide.
├── AGENTS.md            — Concise standing instructions for every task.
├── repo-map.md          — Quick reference map of rs6000-relevant source files.
├── bin/env-check.sh     — Host detection: prints the build/test policy for this machine.
│
├── skills/              — Reusable skill documents. One per topic.
│   ├── review-patch/
│   ├── implement-feature/
│   ├── rs6000-builtins/
│   ├── rtl-patterns/
│   ├── optimization/
│   ├── register-allocation/
│   ├── dejagnu/
│   ├── regression-analysis/
│   ├── bootstrap/
│   ├── documentation/
│   ├── commit-message/
│   ├── patch-submission/
│   ├── rtl-canonical-forms/
│   ├── md-iterators-splits/
│   ├── match-pd/
│   ├── target-hooks/
│   ├── option-files/
│   ├── rtl-pass-order/
│   ├── contrib-git-tools/
│   └── test-results/
│
├── templates/           — Empty task templates. Never fill in task-specific data here.
│   ├── bug/
│   ├── feature/
│   ├── optimization/
│   ├── backport/
│   ├── regression/
│   └── investigation/
│
├── workflows/           — Step-by-step workflow guides.
│   ├── new-task.md
│   ├── implement-feature.md
│   ├── review-patch.md
│   ├── regression.md
│   ├── bootstrap.md
│   └── release-backport.md
│
└── work/                — Task workspaces. One subdirectory per task.
    └── <task-name>/     — All notes, findings, and drafts for that task only.
```

---

## Host Gate

Most development happens on a non-Power machine (e.g. macOS arm64) where GCC for
PowerPC cannot be built or tested. `bin/env-check.sh` detects the host and prints a
policy (`NO_BUILD`, `COMPILE_ONLY`, `ASK_FIRST`). `AGENTS.md` makes every assistant run
it first and obey it: no builds off Power, and on Power only after asking.

---

## How to Start a New Task

1. Read `workflows/new-task.md`.
2. Determine the task type (Bug / Feature / Optimization / Regression / Backport / Investigation).
3. Copy the matching template from `templates/<type>/` into `work/<task-name>/`.
4. Work entirely inside `work/<task-name>/`. Never modify framework files.

---

## How Skills Are Used

Skills are loaded on demand — only when relevant to the current task.

| Task type              | Suggested skills to load                          |
|------------------------|---------------------------------------------------|
| Implement builtin      | `rs6000-builtins`, `rtl-patterns`, `dejagnu`      |
| Review patch           | `review-patch`, `rtl-patterns`                    |
| Fix register bug       | `register-allocation`, `rtl-patterns`             |
| Write optimization     | `optimization`, `rtl-patterns`                    |
| Fix regression         | `regression-analysis`, `bootstrap`                |
| Write tests            | `dejagnu`                                         |
| Write/update docs      | `documentation`                                   |
| Write commit message   | `commit-message`                                  |
| Post / ping a patch    | `patch-submission`                                |
| Pattern never matches  | `rtl-canonical-forms`, `rtl-pass-order`           |
| Multi-mode pattern     | `md-iterators-splits`                             |
| Edit `match.pd`        | `match-pd`                                        |
| Add / read target hook | `target-hooks`                                    |
| Add `-m` option        | `option-files`, `documentation`                   |
| ChangeLog / style check| `contrib-git-tools`                               |
| Compare test results   | `test-results`                                    |

Do not pre-load all skills. Load only what the current task requires.

---

## Extending the Framework

- **Add a skill:** Create `skills/<topic>/SKILL.md` following the format of existing skills.
- **Add a template:** Create `templates/<type>/TEMPLATE.md` with empty placeholders only.
- **Add a workflow:** Create `workflows/<name>.md` following the existing format.
- **Never add task-specific content** to `skills/`, `templates/`, or `workflows/`.
- All task-specific information goes in `work/<task-name>/`.

---

## Important Notes

- This framework covers **GCC 17** (trunk as of this writing).
- Primary target: `gcc/config/rs6000/` and `gcc/testsuite/gcc.target/powerpc/`.
- For file locations, consult `repo-map.md` before searching the repository.
- When uncertain about an implementation, search the repository — do not assume.
