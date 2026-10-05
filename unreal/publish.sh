#!/usr/bin/env bash
# Publish the built runtime as a GitHub Release on this repo, and pin it (Phase06 D2, D14).
#
#   unreal/publish.sh N        # publishes unreal-runtime-vN from unreal/dist/, writes unreal/RUNTIME.json
#
# The tag series is its own (unreal-runtime-vN), marked PRE-RELEASE so it never shows as the
# repo's "Latest" and never collides with the library's matterlib-X.Y.Z releases. The repo is
# public: a published asset may be downloaded at once, so how often to publish is the lead's
# call (D14: at 6.2 and at the close). The tag is made on HEAD, which must already be pushed.
# Then commit and push unreal/RUNTIME.json: the other machine's driver downloads what it names.
set -euo pipefail

N="${1:?usage: publish.sh N   (publishes unreal-runtime-vN)}"
REPO_SLUG="Imrsv-tools/Matter-Library"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TAG="unreal-runtime-v$N"
ASSET="MatterRuntime-Linux-$TAG.tar.gz"
SRC="$HERE/dist/MatterRuntime-Linux.tar.gz"
HEAD_SHA="$(git -C "$HERE" rev-parse HEAD)"

[[ -f "$SRC" ]] || { echo "no $SRC: run unreal/build.sh package first" >&2; exit 1; }
git -C "$HERE" fetch -q origin main
git -C "$HERE" merge-base --is-ancestor "$HEAD_SHA" origin/main \
  || { echo "HEAD $HEAD_SHA is not on origin/main: push first (the tag names the sources)" >&2; exit 1; }

cp "$SRC" "$HERE/dist/$ASSET"
SHA256="$(sha256sum "$HERE/dist/$ASSET" | cut -d' ' -f1)"
SIZE="$(stat -c %s "$HERE/dist/$ASSET")"

gh release create "$TAG" "$HERE/dist/$ASSET" --repo "$REPO_SLUG" --prerelease --target "$HEAD_SHA" \
  --title "Unreal test runtime v$N" \
  --notes "The Matter Library's Unreal test runtime (Shipping, Linux x86_64, glibc 2.28+), built from $HEAD_SHA by unreal/build.sh. The parity rig's Unreal driver (tools/parity/drivers/unreal.py) downloads it through unreal/RUNTIME.json. Not a library release."

cat > "$HERE/RUNTIME.json" <<EOF
{
  "tag": "$TAG",
  "asset": "$ASSET",
  "sha256": "$SHA256",
  "size": $SIZE,
  "source": "$HEAD_SHA"
}
EOF
echo "published $TAG ($SIZE bytes, sha256 $SHA256); commit and push unreal/RUNTIME.json"
