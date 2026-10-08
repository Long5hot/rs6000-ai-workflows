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
<subsystem>: <short summary line (≤65 characters)>

<body: motivation and overview>

<implementation details>

<testing description>

gcc/ChangeLog:

	* config/rs6000/<file>.cc (<function>): <change description>.
	* config/rs6000/<file>.md (<pattern>): <change description>.
	* doc/extend.texi (<builtin>): Document new builtin.

gcc/testsuite/ChangeLog:

	* gcc.target/powerpc/<test>.c: New test.
```

---

## Rules

### Subject line
- Start with the subsystem: `rs6000:`, `middle-end:`, `IRA:`, etc.
- Keep under 65 characters.
- Use imperative mood: "Add", "Fix", "Implement", not "Added", "Fixed".
- Do not end with a period.
- Be specific: "rs6000: Add Power10 vec_extracth builtin" not "rs6000: Fix bug".

### Body
- First paragraph: state **what** changed and **why** (motivation).
- Second paragraph (optional): state **how** it was implemented.
- Third paragraph: state **how** it was tested.
- Separate paragraphs with blank lines.
- Wrap at 72 characters.
- Do not duplicate the ChangeLog entries in the body.

### ChangeLog entries
- One `ChangeLog:` section per top-level directory changed.
- For rs6000 work: `gcc/ChangeLog:` and `gcc/testsuite/ChangeLog:`.
- Format: `\t* <file> (<symbol>): <action>.`
- Use a tab (`\t`) for indentation — not spaces.
- Use the actual function, pattern, or macro name as the symbol.
- For new files: `* <file>: New file.`
- For new tests: `* gcc.target/powerpc/<test>.c: New test.`
- For documentation: `* doc/extend.texi (<@node or builtin>): Document.`
- Actions: "New function.", "New pattern.", "Add case for ...", "Fix ...", "Document.", "Removed.", "Update to ...", "Handle ...".

---

## Example: Adding a builtin

```
rs6000: Implement __builtin_mma_xvf64gerpp for Power10

Power10 introduces the XVBF16GER2PP instruction for accumulating
BF16 outer products.  This patch implements the corresponding GCC
builtin __builtin_mma_xvbf16ger2pp and adds the instruction pattern.

The builtin is guarded by TARGET_MMA and TARGET_POWER10 and follows
the existing MMA builtin convention using ACC and VSR operands.

Tested with a full bootstrap and regression test on powerpc64le-linux-gnu
with no new failures.

gcc/ChangeLog:

	* config/rs6000/rs6000-builtin.cc (rs6000_expand_builtin):
	Handle RS6000_BIF_MMA_XVBF16GER2PP.
	* config/rs6000/rs6000-builtins.def (BU_MMA_2): New entry for
	__builtin_mma_xvbf16ger2pp.
	* config/rs6000/mma.md (mma_xvbf16ger2pp): New pattern.
	* doc/extend.texi (__builtin_mma_xvbf16ger2pp): Document.

gcc/testsuite/ChangeLog:

	* gcc.target/powerpc/mma-xvbf16ger2pp.c: New test.
```

---

## Example: Fixing a regression

```
rs6000: Fix incorrect vec_sel codegen on LE POWER9

vec_sel was emitting xxsel with swapped operands in little-endian mode
when one operand was loaded from memory.  The issue was in the
rs6000_expand_vector_select function which did not account for the
LE byte swap applied to the mask.

Fixed by reversing the mask operand order when TARGET_LITTLE_ENDIAN
is true and the mask has been folded into a constant.

Regression test added to cover the specific RTL shape that triggered
the bug.

gcc/ChangeLog:

	* config/rs6000/rs6000-call.cc (rs6000_expand_vector_select):
	Reverse mask operand order for LE targets.

gcc/testsuite/ChangeLog:

	* gcc.target/powerpc/vec-sel-le-regression.c: New test.
```

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
