# Preview generators

Renders ONE Matter article on a UV sphere, standalone, with no Stage and no release. The render is review material: `/matter-generate` shows it with its critique, and a maintainer eyeballs it before keeping a draft. It is informal visual parity, not the formal ΔE bar (that is *Parity Baselines*).

## Use

```sh
uv run tools/preview_generators/make_preview.py MatterLibrary/materials/<domain>/<class>/<Stem>.mtlx --render
```

- Writes `<Stem>_preview.usda` and, with `--render`, `<Stem>_preview.png`.
- Output goes to `--out-dir`, else `$MATTER_PREVIEW_DIR`, else `<tmp>/matter-preview/`. **Nothing is written into the repo.**
- The `.usda` is plain USD: open it in USDLiveView or usdview for a closer look (`--view` opens usdview).

## Files

- `preview_wrapper.usda` — the scene template: a UV-sphere mesh with the article bound, a dome plus a key light, and a camera. Slots are listed in its header.
- `make_preview.py` — fills the template and runs `usdrecord`.

## What makes a real article render

Repaired in Phase03 step 3.1 (found in discovery, P3). Before it, the wrapper rendered solid white:

- the article layer has no `defaultPrim`, so the reference names its root (`</MaterialX>`);
- USD 26.03 ignores `material:binding` without `MaterialBindingAPI`;
- an implicit `Sphere` has no UVs, so a textured article rendered one flat colour. The sphere is now a mesh with an `st` primvar and vertex normals.

## Toolchain

Writing the scene needs only the repo's core environment. Rendering needs the USD toolchain (`tools/usd-toolchain/`), found at `$USD_TOOLS_ROOT/inst/usd-26.03` (default `~/usd-tools`). `make_preview.py` sets the toolchain's environment for the `usdrecord` child process only, the same way `activate-usd-tools.sh` does for a shell: `PATH`, `PYTHONPATH`, `LD_LIBRARY_PATH`, `PXR_MTLX_STDLIB_SEARCH_PATHS`, and on Linux Qt on xcb + GLX. If the toolchain is missing, the scene is still written and the script exits 2, saying why.

## Path resolution

- The `.mtlx` is referenced by **absolute** filesystem path, because the scene lives outside the repo.
- Texture `<image>` paths are relative inside the `.mtlx` and resolve against it.
- `PXR_MTLX_STDLIB_SEARCH_PATHS` owns only the MaterialX stdlib nodedefs (`open_pbr_surface`), not asset or texture lookup.
