# Investigation Task Template

Copy this file to `.ai/work/<task-name>/TASK.md` and fill in each section.
Delete this instruction line before use.

---

## Summary

<!-- One sentence: what is being investigated? -->


## Task Name

<!-- Short identifier: e.g., p10-vec-cost-analysis, regalloc-spill-investigation -->


## Status

<!-- Active / Blocked / Complete / Inconclusive -->


## Question

<!-- What specific question are you trying to answer?
     Be precise: "Why does GCC emit X instead of Y for this pattern on POWER10?" -->


## Context

<!-- Background information.
     What triggered this investigation?
     What is already known? -->


## Reproduction

```sh
# Command to reproduce the behavior under investigation.
```

Relevant output:
```
```


## Investigation Log

<!-- Date-stamped notes. Add new entries at the top.
     Be specific: record what you looked at and what you found. -->

### <!-- YYYY-MM-DD -->

-


## Data / Evidence

<!-- Paste relevant assembly snippets, RTL dumps, benchmark numbers,
     or code references here. -->


## Hypotheses

<!-- List candidate root causes or explanations. -->

1.
2.
3.


## Findings

<!-- Fill in once the investigation concludes.
     What is the answer to the question? -->


## Recommendations

<!-- What action (if any) should be taken as a result?
     Create a separate Bug / Feature / Optimization task if needed. -->

- [ ] No action needed
- [ ] File a bug: (description)
- [ ] Implement fix: (description)
- [ ] Follow-up investigation: (description)


## References

- Related code:
- Mailing list thread:
- Related PR:
