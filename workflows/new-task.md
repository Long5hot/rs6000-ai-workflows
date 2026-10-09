# Workflow: New Task

Follow these steps every time you start a new task.

---

## Step 0: Host Gate

Run `sh .ai/bin/env-check.sh` (see `AGENTS.md`). Record the `policy=` line in `TASK.md`.

---

## Step 0b: Bug report

If the task has a PR number, fetch it: `python3 .ai/bin/bz.py <N>` (`bugzilla` skill).

---

## Step 1: Determine the task name

Choose a short, lowercase, hyphenated identifier.

Examples:
- `pr120384` — for a Bugzilla PR
- `dmf-builtins` — for a feature
- `ira-spill-cost` — for an investigation
- `vec-sel-le-regress` — for a regression

---

## Step 2: Determine the task type

| Type | Use when |
|------|----------|
| **Bug** | Fixing a correctness, crash, or code quality defect |
| **Feature** | Implementing new ISA support, builtin, or option |
| **Optimization** | Improving generated code quality or compiler performance |
| **Regression** | A test that previously passed now fails |
| **Backport** | Bringing a trunk fix to a release branch |
| **Investigation** | Understanding behavior without a fixed deliverable |

---

## Step 3: Create the task workspace

```sh
mkdir -p .ai/work/<task-name>
cp .ai/templates/<type>/TEMPLATE.md .ai/work/<task-name>/TASK.md
```

Fill in the **Summary** and **Task Name** fields immediately.

---

## Step 4: Load the relevant skills

Refer to the skills table in `README.md` to choose which skills to load.
Load only the skills needed for this task.

Do **not** load skills for topics you will not use in this task.

---

## Step 5: Consult repo-map.md

Before searching the repository, check `repo-map.md` to identify which files
are relevant to the task. This avoids unnecessary wide searches.

---

## Step 6: Work within the task workspace

All task-specific notes, findings, code snippets, and drafts go in:
```
.ai/work/<task-name>/
```

You may create additional files in the workspace:
- `TASK.md` — main task document (from template)
- `notes.md` — scratch notes
- `patch.diff` — working patch
- `benchmark.md` — benchmark results

---

## Rules

- **Never modify** `AGENTS.md`, `README.md`, `repo-map.md`, skills, templates, or workflows.
- **Never mix** information from different tasks in the same workspace.
- **Never reuse** a workspace directory for a different task.
- If a task scope changes significantly, update `TASK.md` to reflect the new scope.
