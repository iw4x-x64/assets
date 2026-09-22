#!/usr/bin/env bash

# Build, test and package a release of this project.
#
# This is what the release workflow runs, though nothing in here depends
# on GitHub Actions. The same command can be run on a development
# machine to see exactly what a tagged release would contain before
# pushing the tag:
#
#   .github/scripts/package.sh --linker /path/to/Linker --output
#   /tmp/rel
#
# The result in the output directory is:
#
#   assets/assets-<version>.zip          game data, extracts into the
#   game dir assets/assets-<version>.zip.sha256
#   assets/assets-<version>.tar.gz       source distribution (b dist)
#   assets/assets-<version>.tar.gz.sha256 release-notes.md version
#
# The version is whatever the build2 version module settles on and so is
# never spelled out here. For a release it is the manifest version (for
# example, 0.1.0-a.2). For a snapshot it carries the commit date and id
# (for example, 0.1.0-a.2.20260825183016.0123456789ab), which is also
# why a snapshot of an uncommitted tree is refused below.
#
set -euo pipefail

usage ()
{
  cat <<EOF
usage: $0 --linker <path> --output <dir> [options]

  --linker <path>          open-asset-tools Linker (x64 build)
  --unlinker <path>        Unlinker for 'b test' (default: beside the Linker)
  --output <dir>           where to write the release (must not exist)
  --work <dir>             scratch directory (default: temporary)
  --expect-version <ver>   fail unless the project version is exactly <ver>
  --oat-commit <id>        open-asset-tools commit, recorded in the notes
  --allow-dirty            package an uncommitted tree (never for a release)
EOF
}

fail ()
{
  echo "error: $*" >&2
  exit 1
}

linker=
unlinker=
output=
work=
expect_version=
oat_commit=
allow_dirty=

while [ "$#" -gt 0 ]; do
  case "$1" in
    --linker)         linker="${2:?}";         shift 2 ;;
    --unlinker)       unlinker="${2:?}";       shift 2 ;;
    --output)         output="${2:?}";         shift 2 ;;
    --work)           work="${2:?}";           shift 2 ;;
    --expect-version) expect_version="${2:?}"; shift 2 ;;
    --oat-commit)     oat_commit="${2:?}";     shift 2 ;;
    --allow-dirty)    allow_dirty=true;        shift   ;;
    -h|--help)        usage; exit 0 ;;
    *)                usage >&2; fail "unexpected argument '$1'" ;;
  esac
done

[ -n "$linker" ] || { usage >&2; fail "--linker is required"; }
[ -n "$output" ] || { usage >&2; fail "--output is required"; }

# Resolve everything to absolute paths up front. build2 is given these
# as configuration values and they are interpreted relative to wherever
# it happens to be looking at the time, which is rarely what we mean.
#
linker="$(realpath -e "$linker")" || fail "Linker '$linker' does not exist"
[ -x "$linker" ] || fail "Linker '$linker' is not executable"

if [ -z "$unlinker" ]; then
  unlinker="$(dirname "$linker")/Unlinker"
fi
unlinker="$(realpath -e "$unlinker")" || fail "Unlinker '$unlinker' does not exist"
[ -x "$unlinker" ] || fail "Unlinker '$unlinker' is not executable"

# Refuse to write into an existing output directory.
#
[ ! -e "$output" ] || fail "output directory '$output' already exists"
mkdir -p "$output/assets"
output="$(realpath -e "$output")"

if [ -z "$work" ]; then
  work="$(mktemp -d)"
  trap 'rm -rf "$work"' EXIT
else
  [ ! -e "$work" ] || fail "work directory '$work' already exists"
  mkdir -p "$work"
  work="$(realpath -e "$work")"
fi

src="$(realpath -e "$(dirname "${BASH_SOURCE[0]}")/../..")"
out="$work/build"
stage="$work/stage"

# The version module takes the snapshot id from git and an uncommitted
# tree has none. Such a package would be indistinguishable from any
# other built from the same commit plus some unknown change. See
# "Versioning" in the build system manual.
#
if [ -z "$allow_dirty" ] && [ -n "$(git -C "$src" status --porcelain)" ]; then
  git -C "$src" status --short >&2
  fail "source tree has uncommitted changes (use --allow-dirty for a local trial)"
fi

# Keep build2's own output readable in a CI log: no progress lines, and
# echo the commands so that each Linker invocation is visible.
#
b=(b --no-progress -v)

# Buildspecs are written as op('dir/') rather than 'op: dir/'. build2
# lexes the buildspec itself and the quotes keep a directory with spaces
# in its name as one path.

echo "==> configuring $src into $out"

# Note the quoting of the install root. build2 parses the value itself
# after the shell is done with it, so the inner quotes keep a path with
# spaces as one name. See README.md for details.
#
"${b[@]}" "configure('$src/'@'$out/')"      \
  "config.assets.linker=$linker"            \
  "config.assets.unlinker=$unlinker"        \
  "config.install.root='$stage/'"

version="$(b "info('$out/')" | sed -n 's/^version: //p')"
[ -n "$version" ] || fail "unable to determine the project version"

echo "==> version $version"

if [ -n "$expect_version" ] && [ "$version" != "$expect_version" ]; then
  fail "project version $version does not match expected $expect_version"
fi

echo "==> building"
"${b[@]}" "update('$out/')"

# Read every fastfile back through the Unlinker.
#
echo "==> testing"
"${b[@]}" "test('$out/')"

echo "==> installing into $stage"
mkdir -p "$stage"
"${b[@]}" "install('$out/')"

# Now the game data archive.
#
# The archive holds exactly what 'b install' puts into a game directory,
# so extracting it into the game directory is equivalent to installing.
# We do not add anything else (licence, readme) for the same reason the
# build does not install those: they would end up next to the game files
# with nobody to consume them. They are in the source distribution.
#
# Normalize what we reasonably can. The fastfiles themselves are
# whatever the Linker writes.
#
count="$(find "$stage" -type f | wc -l)"
[ "$count" -gt 0 ] || fail "installation produced no files"

epoch="$(git -C "$src" log -1 --format=%ct)"
find "$stage" -exec touch -h -d "@$epoch" {} +

zip="assets-$version.zip"

echo "==> archiving $count files into $zip"
(
  cd "$stage"
  find . -type f -printf '%P\n' | LC_ALL=C sort | \
    TZ=UTC zip -X -D -q -9 "$output/assets/$zip" -@
)

# Verify the archive, both its integrity and that it contains every file
# we installed.
#
unzip -tq "$output/assets/$zip" >/dev/null || fail "$zip failed its integrity check"

entries="$(unzip -Z1 "$output/assets/$zip" | wc -l)"
[ "$entries" -eq "$count" ] || fail "$zip has $entries entries, expected $count"

# And the source distribution. The version module fixes the snapshot
# part of the version in the distributed manifest, so the result names
# the same version as the archive above.
#
echo "==> preparing source distribution"
"${b[@]}" "dist('$out/')"                     \
  "config.dist.root=$work/dist/"            \
  "config.dist.archives=tar.gz"             \
  "config.dist.checksums=sha256"

tarball="assets-$version.tar.gz"
[ -f "$work/dist/$tarball" ] || fail "b dist did not produce $tarball"
mv "$work/dist/$tarball" "$output/assets/"

# Write both checksum files the same way, with the bare file name. That
# way `sha256sum -c` works from the directory the files were downloaded
# to.
#
(
  cd "$output/assets"
  for f in "$zip" "$tarball"; do
    sha256sum "$f" > "$f.sha256"
  done
)

# Record what built this, which is the first thing one wants to know
# when a fastfile from a release later refuses to load.
#
linker_version="$("$linker" --version 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | head -n 1)"
build2_version="$(b --version | head -n 1)"
commit="$(git -C "$src" rev-parse HEAD)"

case "${version#+*-}" in
  *-*) kind="pre-release" ;;
  *)   kind="release"     ;;
esac

{
  echo "IW4 x64 fastfiles for IW4x, $kind $version."
  echo
  echo "## Installing"
  echo
  echo "Extract \`$zip\` into the game directory. It contains only"
  echo "\`zone/iw4x/x64/\`, laid out exactly as \`b install\` would install it."
  echo
  echo "\`$tarball\` is the source distribution of the same version."
  echo
  echo "## Verifying"
  echo
  echo '```sh'
  echo "sha256sum -c $zip.sha256 $tarball.sha256"
  echo '```'
  echo
  echo "## Build"
  echo
  echo "| | |"
  echo "|---|---|"
  echo "| Source | \`$commit\` |"
  if [ -n "$oat_commit" ]; then
    echo "| open-asset-tools | \`$oat_commit\` |"
  fi
  echo "| Linker | $linker_version |"
  echo "| build2 | $build2_version |"
  echo "| Fastfiles | $count |"
} > "$output/release-notes.md"

echo "$version" > "$output/version"

echo "==> done"
(cd "$output/assets" && ls -l)
