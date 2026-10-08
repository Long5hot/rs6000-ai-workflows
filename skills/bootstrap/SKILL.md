# Skill: bootstrap

## Purpose
Plan, execute, and validate a GCC bootstrap for rs6000 changes,
and diagnose bootstrap failures.

## When to Use
- Before submitting a patch that touches core backend files
- After a change that causes a build error
- When determining the minimum rebuild scope for a change

---

## Bootstrap Levels

| Level | What runs | When to use |
|-------|-----------|-------------|
| **Incremental build** | `make -j N` | Quick check after small changes |
| **Stage 1 only** | `make stage1` or `make all-gcc` | Compiler-only changes, no self-hosting check |
| **Full bootstrap** | `make bootstrap` | Required before submitting any patch |
| **Bootstrap + regtest** | `make bootstrap && make -k check` | Full validation for significant changes |

For rs6000-only changes, a full bootstrap with `--target=powerpc64le-linux-gnu`
(or your native target) is the minimum acceptable validation.

---

## Incremental Rebuild Guide

Use this to quickly rebuild after changing specific files:

| Changed file | Rebuild command |
|-------------|-----------------|
| `rs6000.cc` | `make -C gcc/ rs6000.o` |
| `rs6000.md` or any `.md` file | `make -C gcc/ insn-recog.o insn-output.o insn-attrtab.o` |
| `rs6000-builtin.cc` | `make -C gcc/ rs6000-builtin.o` |
| `rs6000-builtins.def` | `make -C gcc/ s-rs6000-builtins` then rebuild affected objects |
| `predicates.md` | `make -C gcc/ insn-recog.o` |
| `constraints.md` | `make -C gcc/ insn-recog.o` |
| `rs6000.opt` | `make -C gcc/ options.o` |
| `rs6000-cpus.def` | `make -C gcc/ rs6000.o` |
| `rs6000.h` | `make -C gcc/` (header change may require broader rebuild) |

For header changes (`rs6000.h`, `rs6000-internal.h`), prefer a full `make -C gcc/` to catch all dependencies.

---

## Instructions

### Before submitting a patch

1. **Run incremental build** to catch obvious errors:
   ```sh
   make -j$(nproc)
   ```

2. **Run the relevant test subset:**
   ```sh
   make check-gcc RUNTESTFLAGS="powerpc.exp"
   ```

3. **Run a full bootstrap** on the target architecture:
   ```sh
   cd <build-dir>
   ../configure --enable-languages=c,c++ --disable-multilib
   make bootstrap -j$(nproc)
   ```

4. **Run the full regression suite:**
   ```sh
   make -k check
   ```
   Compare results against the baseline (unpatched tree) using `contrib/compare_tests`.

### Diagnosing a bootstrap failure

Bootstrap failures occur in stage 2 or stage 3. The failure message identifies which file failed.

**Stage 2 build error (compiler-built-by-stage1 failing to compile stage2):**
- Usually a C/C++ syntax error or ABI issue introduced in the patch.
- Fix the error; rerun from stage 2: `make stage2`.

**Stage 2/3 comparison failure (`make compare`):**
- Stage 2 and stage 3 compilers produce different binaries.
- This means the compiler miscompiles itself — a correctness bug in your patch.
- Bisect to the offending change. Inspect the RTL diff between stage 2 and stage 3.
- Use `-fdump-rtl-final` on the differing compilation unit to compare.

**Common bootstrap failure causes:**
| Symptom | Cause |
|---------|-------|
| Stage 1 build error | Syntax or type error in a `.cc` or `.h` file |
| Stage 2 ICE | Compiler miscompiles a source file |
| Stage 2/3 binary diff | Optimization or codegen bug |
| Link failure | Missing symbol, wrong ABI |
| Wrong behavior at run time | RTL mode error, endianness, or undefined behavior |

### Validate only the affected language

For rs6000-only changes, a C+C++ bootstrap is sufficient:
```sh
../configure --enable-languages=c,c++ --disable-multilib
```

Adding Fortran or other frontends is not necessary unless the change touches them.

---

## Relevant Source Files
- `gcc/config/rs6000/rs6000.cc` — most likely source of stage 2/3 miscompilations
- `gcc/config/rs6000/rs6000.md` + feature `.md` files — pattern changes affecting codegen
- `Makefile.in`, `gcc/Makefile.in` — build rules
- `config.log` — configuration errors
- `gcc/stage1/`, `gcc/stage2/`, `gcc/stage3/` — stage output directories

---

## Expected Output
- Bootstrap result: pass or fail.
- If fail: specific failure stage, error message, and root cause.
- Regression count comparison (new failures vs baseline).

---

## Common Pitfalls
- Submitting without bootstrap because "it's a small change" — small `.md` or `.h` changes can cause stage 2/3 divergence.
- Running bootstrap without `-disable-multilib` on a host that supports multilib — multilib failures may be pre-existing.
- Not comparing regression results against baseline — a new failure may exist that bootstrap alone does not reveal.
- Forgetting to run the PowerPC test suite specifically: `make check-gcc RUNTESTFLAGS="powerpc.exp"`.
