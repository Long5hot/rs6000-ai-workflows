# Skill: documentation

## Purpose
Write and update GCC documentation for rs6000 features, options, and builtins,
following GCC Texinfo conventions.

## When to Use
- Adding a new builtin (`extend.texi`)
- Adding a new `-m` option (`invoke.texi`)
- Documenting a new machine mode or constraint
- Updating existing documentation to match a changed implementation

---

## GCC Documentation Files

| File | Content |
|------|---------|
| `gcc/doc/extend.texi` | Language extensions: builtins, attributes, pragmas |
| `gcc/doc/invoke.texi` | All `-m` options, organized by target |
| `gcc/doc/md.texi` | Machine description language |
| `gcc/doc/tm.texi` | Target macro and hook reference |
| `gcc/doc/rtl.texi` | RTL language reference |

For rs6000 work, `extend.texi` (builtins) and `invoke.texi` (options) are most frequently modified.

---

## Texinfo Style Rules

- Use `@` commands, not HTML or Markdown.
- Indent consistently — 2 spaces inside `@deffn` / `@deftypefn` / `@itemize`.
- Keep lines under 72 characters where possible.
- Do not add trailing whitespace.
- Match the exact spacing and punctuation style of adjacent entries.
- New nodes must be connected in the menu of the enclosing chapter.

---

## Documenting a New Builtin (extend.texi)

Find the PowerPC builtin section:
```
grep -n "@subsystem PowerPC" gcc/doc/extend.texi
```

Format for a new builtin entry:
```texinfo
@deftypefn {Built-in Function} {vector signed int} __builtin_altivec_foo \
  (vector signed int @var{a}, vector signed int @var{b})
Short description of what the builtin does.

This built-in requires @option{-maltivec} or @option{-mvsx}.
@end deftypefn
```

Rules:
- List return type first, then name, then parameters.
- Parameter names use `@var{name}`.
- Options use `@option{-m...}`.
- Code (types, values) uses `@code{...}`.
- Keep descriptions concise (1–3 sentences for a single instruction wrapper).
- Place the new entry in alphabetical order within its ISA section.
- Document restrictions (endianness, required `-m` flags, alignment) explicitly.

---

## Documenting a New Option (invoke.texi)

Find the rs6000/PowerPC option section:
```
grep -n "@item -m.*powerpc\|PowerPC" gcc/doc/invoke.texi | head -20
```

Format for a boolean option:
```texinfo
@item -mfoo
@itemx -mno-foo
@opindex mfoo
@opindex mno-foo
Enable or disable the foo feature.  This option requires @option{-mvsx}.
Available on POWER9 and later.
```

Format for a valued option:
```texinfo
@item -mbar=@var{value}
@opindex mbar
Set the bar parameter to @var{value}.  Valid values are @samp{fast},
@samp{safe}, and @samp{off}.  The default is @samp{fast}.
```

Rules:
- Always include `@opindex` immediately after `@item`.
- Use `@samp{value}` for literal values and enum members.
- State the default explicitly.
- State which hardware or ISA the option requires.
- Maintain alphabetical ordering within the rs6000 options section.

---

## Documentation Consistency Checklist

Before submitting:
- [ ] Return type and parameter types in `extend.texi` match the actual builtin signature.
- [ ] ISA requirement (`-mvsx`, `-mpower10`, etc.) is stated.
- [ ] Alphabetical ordering is preserved in the section.
- [ ] `@opindex` entries added for every new option.
- [ ] No Texinfo syntax errors: run `makeinfo --no-split gcc/doc/extend.texi 2>&1 | head -20`.
- [ ] New option in `invoke.texi` matches the option name in `rs6000.opt` exactly.

---

## Relevant Source Files
- `gcc/doc/extend.texi` — builtin documentation (very large; search for nearby entries)
- `gcc/doc/invoke.texi` — option documentation (very large; search for "PowerPC Options")
- `gcc/config/rs6000/rs6000.opt` — option definitions (source of truth for option names)
- `gcc/config/rs6000/rs6000-builtins.def` — builtin names and signatures

---

## Expected Output
- Updated `extend.texi` with new `@deftypefn` block(s) in the correct location.
- Updated `invoke.texi` with new `@item` block(s) in the correct location.
- No Texinfo syntax errors.

---

## Common Pitfalls
- Mismatching the builtin signature between `extend.texi` and the actual implementation.
- Omitting `@opindex` for a new option.
- Inserting the entry in the wrong position (not alphabetical).
- Using Markdown or HTML instead of Texinfo.
- Forgetting to state the required `-m` flag or minimum CPU.
- Using `@var{}` inconsistently — every parameter name must use `@var{}`.
