# How to Use This Framework with IBM Bob

This document explains how to set up and use the `.ai/` framework
in any GCC PowerPC worktree so that IBM Bob is immediately productive
and consumes the minimum number of tokens.

---

## Prerequisites

- IBM Bob is available in your editor or IDE.
- This `.ai/` directory exists at the root of your GCC checkout.
- To reuse the framework in a new worktree or branch:
  ```sh
  cp -r /path/to/original-gcc/.ai /path/to/new-gcc-worktree/
  ```
  Nothing in `.ai/` is branch-specific. It copies cleanly.

---

## One-Time Setup: Bob Custom Instructions

Add the following to **Bob → Settings → Custom Instructions**.
This makes the framework automatic — you do not need to repeat
these instructions at the start of every conversation.

```
For GCC PowerPC backend tasks in this workspace:

- Always read .ai/AGENTS.md at the start of a conversation if not already loaded.
- Always consult .ai/repo-map.md before searching the repository.
- Load skills from .ai/skills/ on demand only. Never pre-load all skills.
- Store all task-specific notes in .ai/work/<task-name>/TASK.md.
- Never modify .ai/AGENTS.md, skills/, templates/, or workflows/.
- Read only the functions needed — never entire source files.
- Use FindSymbol and grep rather than reading whole files.
- Search the repository before asking questions.
```

---

## Starting a New Task (Step by Step)

### Step 1 — Open a new Bob conversation

Tell Bob:

```
Read .ai/AGENTS.md. I am starting a new task: <one sentence description>.
```

Bob reads ~100 lines and is oriented on the project, coding style,
and workflow. This is the full standing context cost.

---

### Step 2 — Identify the task type

Choose the type that fits your work:

| Type | Use when |
|------|----------|
| **Bug** | Fixing a correctness, crash, or code quality defect |
| **Feature** | New ISA support, builtin, or option |
| **Optimization** | Improving generated code quality |
| **Regression** | A test that was passing now fails |
| **Backport** | Bringing a trunk fix to a release branch |
| **Investigation** | Understanding behavior without a fixed deliverable |

---

### Step 3 — Create the task workspace

Tell Bob:

```
Create a workspace for this task using the <type> template.
Task name: <short-hyphenated-name>
```

Bob will copy `.ai/templates/<type>/TEMPLATE.md` to
`.ai/work/<task-name>/TASK.md` and fill in the summary.

You can also do it manually:

```sh
cp .ai/templates/bug/TEMPLATE.md .ai/work/pr120384/TASK.md
```

---

### Step 4 — Load the relevant skills

Tell Bob which skills to load based on the task type.
Use only what the current task needs:

| Task | Skills to load |
|------|---------------|
| Implement builtin | `rs6000-builtins`, `rtl-patterns`, `dejagnu` |
| Review a patch | `review-patch`, `rtl-patterns` |
| Fix register bug | `register-allocation`, `rtl-patterns` |
| Write optimization | `optimization`, `rtl-patterns` |
| Fix regression | `regression-analysis`, `bootstrap` |
| Write tests only | `dejagnu` |
| Write/update docs | `documentation` |
| Write commit message | `commit-message` |

Example prompt:

```
Load the rs6000-builtins and dejagnu skills. Then implement the builtin.
```

Bob reads the two skill files (~100 lines each) and proceeds.

---

### Step 5 — Work the task

Bob will:
1. Consult `repo-map.md` to find relevant files without a repository-wide search.
2. Use `FindSymbol` and `grep` to read only the functions needed.
3. Write all findings and decisions into `.ai/work/<task-name>/TASK.md`.
4. Never read unrelated files or frontends.

You can guide Bob by being specific:

```
Search rs6000-builtins.def for an existing Power10 vector builtin to model after.
```

```
Read only the rs6000_expand_builtin function in rs6000-builtin.cc.
```

```
Write the scan-assembler test following the dejagnu skill.
```

---

### Step 6 — Resume a task in a new conversation

At the start of the next session, tell Bob:

```
Read .ai/AGENTS.md and .ai/work/<task-name>/TASK.md. Continue from where we left off.
```

Bob reads ~200 lines total and is fully oriented.
No re-explaining. No re-investigating already-resolved questions.

Before ending a session, ask Bob to update `TASK.md`:

```
Update TASK.md with the current status, root cause, and next step.
```

---

## Framework File Reference

| File | When to reference it |
|------|---------------------|
| `.ai/AGENTS.md` | Start of every conversation |
| `.ai/repo-map.md` | Before any file search |
| `.ai/skills/<name>/SKILL.md` | When the task requires that topic |
| `.ai/work/<task>/TASK.md` | At start of follow-up conversations |
| `.ai/workflows/<name>.md` | For structured multi-step tasks |
| `.ai/templates/<type>/TEMPLATE.md` | When creating a new task workspace |

---

## Token Budget in Practice

| What Bob reads | Approximate lines |
|----------------|------------------|
| `AGENTS.md` (always) | ~100 |
| `repo-map.md` (always) | ~145 |
| One skill file | ~100–130 |
| Task workspace (`TASK.md`) | ~50–80 |
| A single function via `FindSymbol` | ~30–100 |
| **Total per session** | **~400–550** |

Compare this to loading `rs6000.cc` in full: **29,397 lines**.

The framework keeps Bob productive at roughly **1–2% of the token cost**
of an unstructured session on the same codebase.

---

## Rules That Must Always Be Followed

- **Never modify** `.ai/AGENTS.md`, `skills/`, `templates/`, or `workflows/`
  for a specific task. These are permanent framework files.
- **All task-specific content** belongs in `.ai/work/<task-name>/`.
- **One workspace per task.** Never reuse a workspace for a different task.
- **Copy the framework** to a new worktree at the start of new branches.
  Do not regenerate it — it is already correct.

---

## Copying to a New Worktree

```sh
# Create a new worktree for a release branch
git worktree add ../gcc-gcc14 releases/gcc-14

# Copy the framework
cp -r .ai ../gcc-gcc14/

# Remove any task workspaces that are not relevant to the new branch
rm -rf ../gcc-gcc14/.ai/work/*

# Start working
cd ../gcc-gcc14
```

The framework requires no modification for the new branch.
Only the task workspaces under `work/` are branch-specific.
