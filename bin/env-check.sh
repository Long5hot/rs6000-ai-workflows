#!/bin/sh
# Print the facts that decide what an assistant may run in this checkout.
# Read-only: builds nothing, installs nothing, changes nothing.
# Optional: export GCC_BUILD_DIR=/path/to/build to name the build directory.

here=$(cd "$(dirname "$0")/.." && pwd)
src=$(dirname "$here")
[ -f "$src/gcc/BASE-VER" ] || src=$(git rev-parse --show-toplevel 2>/dev/null)

os=$(uname -s)
arch=$(uname -m)
native=no
case "$arch" in ppc64le | ppc64 | ppc | powerpc*) native=yes ;; esac
[ "$os" = AIX ] && native=yes

build=none
target=none
for d in "$GCC_BUILD_DIR" "$src"/../build* "$src"/../obj* "$src"/../*-build \
	 "$src"/build* "$src"/obj*; do
  if [ -n "$d" ] && [ -x "$d/gcc/xgcc" ]; then
    build=$(cd "$d" && pwd)
    target=$("$d/gcc/xgcc" -dumpmachine 2>/dev/null)
    break
  fi
done

cross=none
for t in powerpc64le-linux-gnu powerpc64le-unknown-linux-gnu \
	 powerpc64-linux-gnu powerpc64-unknown-linux-gnu powerpc-linux-gnu; do
  if command -v "$t-gcc" >/dev/null 2>&1; then
    cross=$(command -v "$t-gcc")
    break
  fi
done

have () { python3 -c "import $1" >/dev/null 2>&1 && echo yes || echo no; }
aliases=no
git -C "$src" config --get alias.gcc-verify >/dev/null 2>&1 && aliases=yes

echo "host=$os $arch"
echo "native_power=$native"
echo "source=$src"
echo "framework=$here   (written as .ai/ in the docs)"
echo "build_dir=$build"
echo "build_target=$target"
echo "cross_compiler=$cross"
echo "git_gcc_aliases=$aliases"
echo "py_style_check=$(have 'unidiff, termcolor')"
echo "py_mklog=$(have 'unidiff, requests')"
echo "py_gcc_verify=$(have 'unidiff, git')"

usable=no
case "$target" in powerpc* | rs6000*) usable=yes ;; esac
[ "$cross" != none ] && usable=yes

if [ "$native" = yes ]; then
  echo "policy=ASK_FIRST: this is a Power host. Ask the user before any configure, make, bootstrap or make check."
elif [ "$usable" = yes ]; then
  echo "policy=COMPILE_ONLY: not a Power host. The existing PowerPC compiler may be run with -S on single files. Never configure, make, bootstrap or run make check here."
else
  echo "policy=NO_BUILD: not a Power host and no PowerPC compiler exists here. Never configure, build or test GCC. Edit and analyse only; give the user the exact commands to run on a Power host."
fi
