---
name: commit-message
description: Write a GCC commit message: subject with [PRn], body, tab-indented ChangeLog with PR target/N lines.
---
# Skill: commit-message

## Purpose
Write GCC-quality commit messages that follow established GCC conventions
and are suitable for submission to gcc-patches@gcc.gnu.org.

## When to Use
- Before committing or posting a patch
- When writing the cover letter for a patch series

---

## GCC Commit Message Format

```
<subsystem>: <short summary> [PR<number>]

<body: motivation and overview>

<implementation details>

<testing description>

gcc/ChangeLog:

	PR target/<number>
	* config/rs6000/<file>.cc (<function>): <change description>.
	* config/rs6000/<file>.md (<pattern>): <change description>.
	* doc/extend.texi (<node>): Document new builtin.

gcc/testsuite/ChangeLog:

	PR target/<number>
	* gcc.target/powerpc/<test>.c: New test.
```
Omit the `[PR…]` tag and `PR` lines when there is no Bugzilla PR.

---

## Rules

### Subject line
- Start with the subsystem: `rs6000:`, `middle-end:`, `IRA:`, etc.
- Keep it short; most rs6000 subjects are under 75 characters including the PR tag.
- If it fixes a PR, end with `[PR<number>]`.
- Use imperative mood: "Add", "Fix", "Implement", not "Added", "Fixed".
- Do not end with a period.
- Be specific: "rs6000: Add Power10 vec_extracth builtin" not "rs6000: Fix bug".

### Body
- First paragraph: state **what** changed and **why** (motivation).
- Second paragraph (optional): state **how** it was implemented.
- Third paragraph: state **how** it was tested. Only what actually ran; never invent a bootstrap/regtest result (Host Gate, `AGENTS.md`).
- Separate paragraphs with blank lines.
- Wrap at 72 characters.
- Do not duplicate the ChangeLog entries in the body.

### ChangeLog entries
- One `ChangeLog:` section per top-level directory changed.
- For rs6000 work: `gcc/ChangeLog:` and `gcc/testsuite/ChangeLog:`.
- Format: `\t* <file> (<symbol>): <action>.`
- Use a tab (`\t`) for indentation — not spaces. The checker rejects spaces.
- PR line: `\tPR <component>/<number>`, where component is the Bugzilla component (`target` for backend bugs, never `rs6000`).
- Verify with `git gcc-verify` (see `patch-submission` skill).
- Use the actual function, pattern, or macro name as the symbol.
- For new files: `* <file>: New file.`
- For new tests: `* gcc.target/powerpc/<test>.c: New test.`
- For documentation: `* doc/extend.texi (<node name>): Document ...`
- Actions: "New function.", "New pattern.", "Add case for ...", "Fix ...", "Document.", "Removed.", "Update to ...", "Handle ...".

---

## Example (real commit 9b8d4dd3ed3)

```
rs6000: Fix vec_permx wrong-code [PR125138]

The little-endian expansion of vec_permx modified the permute control
vector. When the same control vector was used by multiple vec_permx
calls, later calls used the modified value and produced incorrect
results.

Generate the negated control vector in a new pseudo register instead of
modifying the input operand.

gcc/ChangeLog:

	PR target/125138
	* config/rs6000/vsx.md (xxpermx): Use a temporary register for the
	negated control vector.

gcc/testsuite/ChangeLog:

	PR target/125138
	* gcc.target/powerpc/pr125138.c: New test.
```
(As committed, the headers read `gcc/` and `gcc/testsuite/` — both spellings are accepted — and a `YYYY-MM-DD  Name  <email>` author line precedes them.)

---

## Expected Output
A commit message in the exact format above, ready to paste into `git commit -F`
or the cover letter of a patch series.

---

## Common Pitfalls
- Missing ChangeLog entries (every changed file must be listed).
- Using spaces instead of tabs in ChangeLog entries.
- Exceeding 72 characters in the body without wrapping.
- Vague subject line ("Fix issue" instead of "rs6000: Fix vec_sel mask order on LE").
- Describing implementation in the subject line (save details for the body).
- Forgetting `gcc/testsuite/ChangeLog:` when tests are added.
- Not mentioning the bootstrap/regression test result in the body.
