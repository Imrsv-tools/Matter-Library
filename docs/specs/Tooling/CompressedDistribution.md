# Tooling — Compressed Distribution & Parity

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

The offline [BCn](../../Glossary.md) compression toolchain, the frozen role→format contract, and the calibrated visual/codec
[parity](../../Glossary.md) gates. A **Spec** for the tools that turn authored PNG source into validated compressed release
derivatives.

> Original status line: "Shipped."
>
> **Drift (2026-09-23):** the toolchain is built and was exercised on the `matterlib-0.1.0` pilot release; the library is not in production — owned by the release-bundle / consumer-contract phase (R7).

> The release lifecycle that consumes these outputs is [ReleaseModel](../Distribution/ReleaseModel.md).
>
> *Consumer-side (IMRSV): the runtime wire that carries compressed textures — see [Consumers](../Consumers.md).*

---

## Compression toolchain

| Tool | Path | Role |
|---|---|---|
| Encoder (pinned) | `compressonatorcli` **V4.5.52** (located via `$COMPRESSONATORCLI`, else a per-user default) | the BCn encoder — pinned for deterministic output |
| Compressor | `tools/compressors/compress_textures.py` | source PNG tree → mip-complete BCn `.dds`, per the role table below |
| Staging producer | `tools/releases/stage_release.py` | assembles the self-contained per-release `{png, .dds}` snapshot |
| Freeze | `tools/releases/freeze_release.py` | hash-locks the complete payload incl. `.dds` (`dds_set`) |

*(Updated 2026-09-23, measured: `PINNED_VERSION = "V4.5.52"` and the `COMPRESSONATORCLI` override in `tools/compressors/compress_textures.py`; the compressor fails if the encoder is absent or not the pinned version.)*

**Determinism gate:** byte-identical `.dds` across two runs at the pinned encoder + flags (`run_all.py`
`compression` lane). **Output validation:** dimensions · role↔BC-format agreement · complete mip chain ·
colour-space/normal/alpha policy per role; a corrupt/mismatched `.dds` is rejected (`compression_negative`
lane, RED fixtures in `tools/compressors/fixtures/`). The staging tree is a **gitignored reproducible build artifact** — never committed,
never written into the authored `MatterLibrary/textures` source tree.

## Frozen role → BC-format contract (14 texture roles)

Keyed by role **name**. All roles use full mip chains. `specular` is a scalar (no texture field), so it is explicitly RULED OUT.

| Role | BC format | Colour space |
|---|---|---|
| `diffuse_texture` | **BC7** | sRGB |
| `normal_texture` | **BC5** | linear (16-bit src → 8-bit BC5; parity-sensitive, codec-A/B gated) |
| `metallic_texture` | **BC4** | linear (single-channel) |
| `roughness_texture` | **BC4** | linear |
| `opacity_texture` | **BC4** | linear |
| `emissive_texture` | **BC7** | sRGB |
| `ambient_occlusion_texture` | **BC4** | linear |
| `overlay1_texture` | **BC7** | linear |
| `overlay2_texture` | **BC7** | linear |
| `overlay3_texture` *(consumer wire field, added 2026-09-25; see PlatformDependencies P12)* | **BC7** | linear |
| `maskset_texture` | **BC7** | linear |
| `layer2_base_color_texture` | **BC7** | sRGB |
| `layer2_roughness_texture` | **BC4** | linear |
| `layer2_metalness_texture` | **BC4** | linear |
| `layer2_normal_texture` | **BC5** | linear |

*Consumer-side (IMRSV): the stable numeric role ordering (bits 0–13) in the consumer's wire struct and the `compressed_roles_mask` — see [Consumers](../Consumers.md).*

> Source-filename note: role detection keys on the OpenPBR-correct suffix — the metallic map ships as
> `*_metalness_*.png` (canonicalised before the 0.1.0 freeze; `metallic` stays a legacy alias in the compressor's suffix table). The role name stays `metallic_texture`.
> *(Updated 2026-09-23, measured: the suffix→BC table in `compress_textures.py` — `basecolor`/`diffuse`/`emissive`/`overlay`/`overlays`/`masks` → BC7, `metalness`/`metallic`/`roughness`/`opacity`/`ambient_occlusion`/`ao` → BC4, `normal` → BC5.)*

> **Reevaluate (2026-09-23):** role names such as `diffuse_texture` / `metallic_texture` come from a consumer's field naming, not from OpenPBR/LCD vocabulary; whether the published [master contract](../../Glossary.md) *(planned)* carries these names or OpenPBR-named roles is open — owned by the release-bundle / consumer-contract phase (R14).

Measured benefit (Copper article): a BC texture is ~1.3 MiB mip-complete vs ~4 MiB for an uncompressed RGBA8 single-mip texture — no runtime recompress, and shared textures dedupe across instances.
*Consumer-side (IMRSV): the runtime VRAM comparison against the consumer's uncompressed fallback path — see [Consumers](../Consumers.md).*

---

## Parity — calibrated, not pixel-identical

Parity **catches material/compression regressions without pretending different renderers produce
pixel-identical images** (the acceptance invariant). Two gates:

### OCIO 2.4-native parity config
Built by `tools/conformance/build_ocio_parity_config.py` (a machine-local, reproducible artifact written to the builder's default output directory, overridable with `--out`; never committed). It
**supersedes** an earlier header-hacked qualitative-smoke config (which is NEVER
parity-grade). Finding: Blender's shipped config is mathematically faithful under
OCIO 2.4.2 already (AgX/Filmic are LUT-based, version-independent); the only 2.5-isms are silently-ignored
metadata keys — so the builder loads under 2.4.2, drops the 2.5 keys, and re-serialises the canonical 2.4
form (warning-free). Glossary: [OCIO parity config](../../Glossary.md).

### Codec A/B comparator (the earliest objective gate)
`tools/conformance/codec_ab.py` renders a material's authored source PNGs (arm A) vs its release BCn `.dds` decoded
back to pixels (arm B) through ONE pinned Storm pipeline (matched sphere + HDRI dome + backdrop + fixed
camera). Metric = CIE **ΔE2000** over the surface + SSIM + a per-role texture-space codec table.
Cross-renderer-independent; OCIO-safe because both arms share one pinned pipeline. Gate-can-fail: A-vs-A
control ΔE 0.0 (`--self-test`); a materially-wrong injected colour fires the gate (`--red-demo`).
*(Updated 2026-09-23, measured: the tool path — the original said `tools/.../codec_ab.py`; it is `tools/conformance/codec_ab.py`, with `--self-test` and `--red-demo` flags.)*

### Per-class ΔE bars (from real first pairs)
Target ΔE<2 for Opaque/Masked/Emissive; relaxed for transmission/SSS. Set per [master](../Ontology/MasterSet.md) class from the
first calibrated pairs OR a recorded lead decision (`measurement-OR-lead-decision`). Measured first pairs
(render ΔE2000 mean): Copper 0.69 · Limestone 0.23 · Concrete 0.43 — all well under the
bar; the codec is not a parity risk. Cross-renderer *view-transform* (tonemapper) matching is tracked
separately — design-bearing, out of this spec's scope *(planned)*.

## No standing generative-vendor dependency

No generative vendor (e.g. Adobe Firefly, Bria) is a standing dependency. The release gate
judges the actual shipped texture [provenance](../Contract/Manifest.md) (`tools/validators/source_provenance.py`) against the shipped-pixel rule ([AuthoringGoldenPath](../Authoring/AuthoringGoldenPath.md)).

## History

- 2026-07: the BCn toolchain, the role→format table, the OCIO parity config builder and the Codec A/B comparator were built inside the IMRSV platform; the first calibrated pairs (Copper, Limestone, Concrete) were measured then.
- 2026-09-23: brought home; the numeric wire ordering, the compressed-roles mask and the VRAM comparison moved to [Consumers](../Consumers.md).
