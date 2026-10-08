# Repository Map — GCC PowerPC (rs6000) Backend

Quick reference for locating code. All paths relative to repository root.
Use this before searching the repository.

---

## rs6000 Backend — Core Source

| File | Lines | Purpose |
|------|-------|---------|
| `gcc/config/rs6000/rs6000.cc` | 29397 | Main backend: target hooks, ISA selection, costs, predicates, RTL helpers |
| `gcc/config/rs6000/rs6000.h` | 2495 | Target machine header: register classes, modes, macros |
| `gcc/config/rs6000/rs6000-internal.h` | — | Internal declarations shared across rs6000 source files |
| `gcc/config/rs6000/rs6000-protos.h` | — | Function prototypes exposed to the rest of GCC |
| `gcc/config/rs6000/rs6000-opts.h` | — | Option struct declarations |
| `gcc/config/rs6000/rs6000.opt` | 699 | Compiler options (`-m` flags) |
| `gcc/config/rs6000/rs6000-cpus.def` | 265 | CPU names, ISA feature masks, tune flags |

## rs6000 Backend — Calling Conventions and ABI

| File | Lines | Purpose |
|------|-------|---------|
| `gcc/config/rs6000/rs6000-call.cc` | 3004 | Calling conventions, argument passing, return values |
| `gcc/config/rs6000/rs6000-logue.cc` | 5705 | Function prologue/epilogue, frame layout, save/restore sequences |
| `gcc/config/rs6000/rs6000-c.cc` | 2176 | C/C++ language frontend hooks, pragma handling |

## rs6000 Backend — Builtins

| File | Lines | Purpose |
|------|-------|---------|
| `gcc/config/rs6000/rs6000-builtin.cc` | 3747 | Builtin expansion, TARGET_EXPAND_BUILTIN hook |
| `gcc/config/rs6000/rs6000-builtins.def` | 4097 | Builtin function definitions (name, type, attrs, expander) |
| `gcc/config/rs6000/rs6000-overload.def` | — | Overloaded builtin resolution tables |
| `gcc/config/rs6000/rs6000-gen-builtins.cc` | 3035 | Build-time tool: generates builtin tables from .def files |

## rs6000 Backend — Machine Description

| File | Lines | Purpose |
|------|-------|---------|
| `gcc/config/rs6000/rs6000.md` | 15881 | Top-level machine description: includes all other .md files |
| `gcc/config/rs6000/predicates.md` | 2178 | RTL predicates for instruction patterns |
| `gcc/config/rs6000/constraints.md` | 291 | Constraint definitions |
| `gcc/config/rs6000/altivec.md` | — | VMX/Altivec instruction patterns |
| `gcc/config/rs6000/vsx.md` | — | VSX (POWER7+) instruction patterns |
| `gcc/config/rs6000/vector.md` | — | Generic vector patterns |
| `gcc/config/rs6000/power10.md` | — | Power10 (ISA 3.1) instruction patterns |
| `gcc/config/rs6000/power9.md` | — | Power9 (ISA 3.0) instruction patterns |
| `gcc/config/rs6000/power8.md` | — | Power8 (ISA 2.07) instruction patterns |
| `gcc/config/rs6000/mma.md` | — | MMA (matrix multiply assist) patterns |
| `gcc/config/rs6000/crypto.md` | — | Cryptographic instruction patterns |
| `gcc/config/rs6000/dfp.md` | — | Decimal floating point patterns |
| `gcc/config/rs6000/htm.md` | — | Hardware Transactional Memory patterns |
| `gcc/config/rs6000/sync.md` | — | Atomic/sync instruction patterns |
| `gcc/config/rs6000/fusion.md` | — | Instruction fusion patterns |
| `gcc/config/rs6000/pcrel-opt.md` | — | PC-relative addressing patterns |
| `gcc/config/rs6000/rs6000-modes.def` | 82 | Machine mode definitions |

## rs6000 Backend — Optimizations

| File | Lines | Purpose |
|------|-------|---------|
| `gcc/config/rs6000/rs6000-string.cc` | 2925 | String/memory operation expansion (memcpy, strlen, etc.) |
| `gcc/config/rs6000/rs6000-p8swap.cc` | 2806 | Power8 vector element swap optimization pass |
| `gcc/config/rs6000/rs6000-pcrel-opt.cc` | 910 | PC-relative load/store optimization pass |
| `gcc/config/rs6000/rs6000-passes.def` | — | Registration of custom rs6000 RTL passes |

## rs6000 Backend — Platform/ABI Targets

| Subdirectory/file | Purpose |
|-------------------|---------|
| `gcc/config/rs6000/linux.h`, `linux64.h`, `linuxaltivec.h` | Linux (BE/LE) target headers |
| `gcc/config/rs6000/aix.h`, `aix71.h`, `aix72.h`, `aix73.h` | AIX target headers |
| `gcc/config/rs6000/darwin.h` | Darwin/macOS target header |
| `gcc/config/rs6000/sysv4.h`, `eabi.h` | Embedded ABI target headers |
| `gcc/config/rs6000/rs6000-linux.cc` | Linux-specific target hooks |

## rs6000 Backend — Intrinsic Headers (installed with compiler)

| File | Purpose |
|------|---------|
| `gcc/config/rs6000/altivec.h` | VMX intrinsics |
| `gcc/config/rs6000/htmintrin.h`, `htmxlintrin.h` | HTM intrinsics |
| `gcc/config/rs6000/amo.h` | Atomic memory operation intrinsics |
| `gcc/config/rs6000/ppc-asm.h` | Assembly macros for PPC |

---

## Compiler Middle-End (relevant to rs6000 work)

| File | Lines | Purpose |
|------|-------|---------|
| `gcc/optabs.cc` | 8693 | Optab infrastructure: mapping operations to instruction patterns |
| `gcc/optabs.def` | — | Optab definitions |
| `gcc/optabs-tree.cc` | — | Tree-level optab interface |
| `gcc/recog.cc` | 4808 | Instruction recognition, constraint checking |
| `gcc/reload.cc` | 7381 | Classic reload pass |
| `gcc/reload1.cc` | — | Reload pass second phase |
| `gcc/ira.cc` | 6295 | Integrated Register Allocator (top level) |
| `gcc/ira-costs.cc` | — | IRA cost computation |
| `gcc/ira-build.cc` | — | IRA allocno/region construction |
| `gcc/ira-conflicts.cc` | — | IRA conflict graph |
| `gcc/ira-color.cc` | — | IRA coloring |
| `gcc/lra.cc` | 2718 | LRA (Local Register Allocator) top level |
| `gcc/lra-constraints.cc` | — | LRA constraint satisfaction |
| `gcc/lra-coalesce.cc` | — | LRA coalescing |
| `gcc/lra-remat.cc` | — | LRA rematerialization |
| `gcc/expmed.cc` | — | Expand medium-level operations |
| `gcc/expr.cc` | — | RTL expression expansion |
| `gcc/emit-rtl.cc` | — | RTL emission utilities |
| `gcc/rtl.h` | — | RTL data structure definitions |
| `gcc/rtl.def` | — | RTL operation definitions |
| `gcc/passes.def` | — | Pass registration |
| `gcc/target.def` | — | Target hook definitions |
| `gcc/targhooks.cc` | — | Default target hook implementations |

---

## Test Suite

| Path | Purpose |
|------|---------|
| `gcc/testsuite/gcc.target/powerpc/` | ~2400 PowerPC-specific DejaGnu tests |
| `gcc/testsuite/lib/target-supports.exp` | `effective-target` keyword definitions |
| `gcc/testsuite/gcc.dg/` | Generic middle-end tests (sometimes relevant) |

---

## Documentation

| File | Lines | Purpose |
|------|-------|---------|
| `gcc/doc/extend.texi` | 32097 | Language extensions: builtins, attributes, pragmas |
| `gcc/doc/invoke.texi` | 38344 | Compiler invocation: all `-m` options |
| `gcc/doc/md.texi` | 12505 | Machine description language reference |
| `gcc/doc/tm.texi` | 13078 | Target macro and hook reference |
| `gcc/doc/rtl.texi` | 5292 | RTL language reference |
| `gcc/doc/passes.texi` | — | Compiler pass documentation |
| `gcc/doc/gimple.texi` | — | GIMPLE IR reference |

---

## Useful Search Anchors

| What to search for | Where to grep |
|--------------------|---------------|
| Builtin name (e.g. `__builtin_altivec_`) | `rs6000-builtins.def`, `rs6000-builtin.cc` |
| Instruction pattern (e.g. `define_insn "altivec_vaddubm"`) | `altivec.md`, `vsx.md`, `rs6000.md` |
| Predicate (e.g. `altivec_register_operand`) | `predicates.md` |
| Constraint (e.g. `"wa"`, `"v"`) | `constraints.md` |
| TARGET flag (e.g. `TARGET_VSX`) | `rs6000.h`, `rs6000-opts.h`, `rs6000-cpus.def` |
| ISA mask (e.g. `OPTION_MASK_POWER10`) | `rs6000-cpus.def`, `rs6000.h` |
| Target hook (e.g. `TARGET_EXPAND_BUILTIN`) | `rs6000.cc` (search `#undef TARGET_`) |
| Optab (e.g. `vec_add_optab`) | `optabs.def`, `optabs.cc` |
| Effective target keyword | `gcc/testsuite/lib/target-supports.exp` |

---

## ISA Feature Generations

| ISA level | CPU | Key features |
|-----------|-----|-------------|
| ISA 2.06 | POWER7 | VSX, 64-bit vector registers |
| ISA 2.07 | POWER8 | VSX2, HTM, 64-bit integer vector ops |
| ISA 3.0 | POWER9 | VSX3, DFP, vector count, scalarize |
| ISA 3.1 | POWER10 | MMA, prefixed instructions, PCrel, masks |
