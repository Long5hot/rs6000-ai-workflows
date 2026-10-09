# Workflow: Review Patch

Use this workflow when reviewing an rs6000 backend patch.
Load the `review-patch` skill before starting.

---

## Step 1: Read the patch header

- Read the commit message for intent and scope.
- Note which files are changed.

## Step 2: Identify affected components

Using `repo-map.md`, determine what each changed file does:
- Machine description (patterns, predicates, constraints)?
- Builtin implementation?
- Register allocation / costs?
- Documentation?
- Tests?

## Step 3: Load additional skills if needed

| Changed file type | Load skill |
|-------------------|-----------|
| `.md` patterns | `rtl-patterns` |
| `rs6000-builtin.cc` / `.def` | `rs6000-builtins` |
| `ira*.cc` / `lra*.cc` / `rs6000.h` register classes | `register-allocation` |
| `extend.texi` / `invoke.texi` | `documentation` |
| Test files | `dejagnu` |

## Step 4: Read the changed functions

Use `FindSymbol` to locate each changed function or pattern.
Read only the changed functions — not the entire file.
Compare against what the patch modifies.

## Step 5: Apply the review-patch skill checklist

Work through each section of the `review-patch` skill:
- Correctness (predicates, constraints, modes, TARGET guards)
- Optimization impact
- Register allocation impact
- Bootstrap risk
- Test coverage
- Documentation

## Step 6: Produce the review

Use the section list under "Expected Output" in the `review-patch` skill.
Within each section, mark every item as blocking or suggestion.

Record the review in the task workspace (`TASK.md` or `review-notes.md`).

## Guidance

- Do not comment on formatting unless the patch introduces formatting errors.
- Distinguish between blocking issues (correctness, regression risk) and suggestions.
- If an issue is unclear, note what needs investigation rather than speculating.
- Credit what is done well, but keep it brief.
