# Authoring Golden Path — how Matter materials get made

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

The **production pipeline** for *creating* Matter materials. This is **distinct from** the **Creator Golden Path** (the end-user consumption flow — assign in Blender → export → use downstream — in [Experience_MatterLibrary](../Experience/Experience_MatterLibrary.md)). Name them apart so production tooling never blurs with end-user experience. Terms follow the [Glossary](../../Glossary.md).

> **Original decision (2026-06-20):** the **open AI-gen pipeline is the golden authoring path** — it bootstraps a proof subset for free; a clean-provenance generator was to be pinned as a later production decision. The **shipped-pixel rule** (below) keeps the two from blurring.
>
> **Drift (2026-09-23):** the "later production decision" assumed a vendor generator would supply shipped pixels; under R13 any generator is admissible only if its output is CC0-dedicable with evidence, and no generator has been selected — owned by the release-bundle / consumer-contract phase (R13).

## The pipeline — A → B → C (+ QC)

No single tool closes text → MaterialX end-to-end; stage C stays scripted.

| Stage | What | Open golden-path tool (v1) | Alternatives |
|-------|------|----------------------------|--------------|
| **A — generate** | a *seamless tileable albedo* from a prompt | **ComfyUI + SDXL with circular-pad** (genuinely tileable); **Material Maker** (MIT, procedural) for simple boring-coverage | Scenario · Adobe Firefly (web) · Midjourney `--tile` · 3D AI Studio |
| **B — decompose** | albedo → PBR maps (normal, roughness, height, …) | **PBRify_Remix** (CC0-trained) | Substance 3D Sampler *Image-to-Material* · GenPBR |
| **C — assemble** | PBR maps → the OpenPBR 1.39 single-file `.mtlx` | **deterministic MaterialX Python SDK** (scripted — the [Assembler](../Tooling/AuthoringHarness.md)) | — (scripted, no tool closes this) |
| **QC** | de-light + tileability check | de-lighting (AI albedos bake in lighting that degrades decomposition) + tileability spot-check at **2×2 / 3×3** | — |

> **Reevaluate (2026-09-23):** the stage-A/B tools and alternatives above are listed as *pipeline options*, not as approved sources of shipped pixels; each must pass the shipped-pixel rule (CC0-dedicable, with evidence) before its output can ship.

**The real bottleneck is stage A.** The original framing was "paid Substance vs open decomposers," but PBRify/Materialize are *decomposers* (albedo → maps), not *generators* — both silently assume a clean tileable albedo already exists. The genuine axis is **where the tileable albedo comes from + the provenance of those pixels**, because the Matter Library distributes textures as part of its content.

## Provenance posture (the deciding axis for a published library)

Original text (kept, annotated):

> Provenance is graded because the library **sells the pixels**:
>
> | Tier | Path | Provenance | Use |
> |------|------|------------|-----|
> | **Cleanest** | Scenario / **Bria**-backed generation | vendor states licensed training data | production candidate |
> | **Clean** | **Adobe Firefly** (+ Substance Image-to-Material) | vendor states licensed stock + public-domain training data | production candidate |
> | **Provenance-clouded** | **ComfyUI-SDXL + PBRify** (the open golden path) | permissive licences, but the training data of the base model is the subject of public litigation (see citations) | **bootstrap only** — fine to learn/proof, not a clean provenance story for shipped pixels |
> | **Zero-risk** | **Material Maker** (MIT, procedural) | fully procedural, no training data | weaker for photoreal; safe anywhere |

> **Drift (2026-09-23):** the Matter Library is a community resource, not a sold product (R9), and content ships under CC0-1.0 (R13); the tiering by vendor indemnification no longer decides anything — the only test is whether an input is **CC0-dedicable, with evidence**. A vendor's commercial licence or indemnification does not by itself make its output CC0-dedicable — owned by the release-bundle / consumer-contract phase (R9, R13).

The **R13 test** that replaces the tiering:

| Input | CC0-dedicable? | Note |
|---|---|---|
| ambientCG textures | **yes** | CC0-1.0 upstream |
| In-house procedural generation (committed, deterministic generator script) | **yes** | the script is the evidence; released CC0-1.0 |
| CC-BY sources | **no** | attribution is a licence term; CC0 cannot carry it |
| "Royalty-free" / vendor-licensed sources | **no** (unless the terms permit a CC0 dedication) | a use licence is not a dedication |
| Generative-model output | *Reevaluate (2026-09-23):* case by case — admissible only where the tool's terms permit a CC0 dedication of the output and that is recorded as evidence | no generative tool is approved today |

## Shipped-pixel rule (HARD)

**No pixel ships unless its provenance is recorded and it is CC0-dedicable, with evidence.** The [Manifest](../Contract/Manifest.md) records `provenance: {source, license, evidence}` per texture; the manifest status lifecycle is where this gate lives — a texture without recorded, CC0-dedicable provenance cannot reach `approved` in a release (enforced by the `provenance_gate` lane of `tools/validators/run_all.py`).

Original text (kept, annotated):

> **Provenance-clouded bootstrap pixels must NOT silently become shipped official-library pixels.** The open ComfyUI-SDXL + PBRify path is sanctioned to *bootstrap and prove*; any texture that bootstrap produces is **flagged for re-generation on a clean-provenance tool** (Scenario-Bria or Adobe Firefly) before it ships in an official Matter Library release. The manifest [status lifecycle](../Contract/Manifest.md) is where this gate lives — a clouded-provenance asset cannot reach `approved` in a shipped release.

> **Drift (2026-09-23):** "re-generation on a clean-provenance tool (Scenario-Bria or Adobe Firefly)" names vendors whose output is not shown to be CC0-dedicable; under R13 a bootstrap texture is replaced by a CC0-dedicable input (e.g. ambientCG or in-house procedural), not by a vendor generator, and "official library" reads as "library release" (R9) — owned by the release-bundle / consumer-contract phase (R13).

### Policy actually used for `matterlib-0.1.0` (the pilot release)

*(Updated 2026-09-23, measured: `library/provenance/matterlib-0.1.0-textures.md`, the header and `textures[].provenance` entries of `library/releases/matterlib-0.1.0.lock.yaml`.)*

- Every texture in the [pilot release](../../Glossary.md) `matterlib-0.1.0` is one of two classes: **ambientCG (CC0-1.0)** — Limestone_Veined, Concrete_Smooth_Worn, Copper_Verdigris — or **in-house procedural** (deterministic fixed-seed generation by a committed script: `tools/converters/gen_uvgrid.py`, `gen_article_textures.py`, `gen_shared_textures.py`), released CC0-1.0.
- **No generative-vendor pixels** and no ComfyUI-SDXL bootstrap pixels are in the shipped set; the audit recorded in the provenance file found none.
- ambientCG entries carry `evidence: {url, sha256_scope: shipped_source_set, sha256, files[]}` — the sha256 attests the *shipped* (processed) source set, not the upstream download (`tools/validators/source_provenance.py`). Procedural entries point `evidence` at their generator script.
- The policy was vendor-neutral and auditable, and the lock header records Adobe as excluded: no generative vendor is a standing dependency (see [CompressedDistribution](../Tooling/CompressedDistribution.md) §No standing generative-vendor dependency).

This is compatible with R13 as it stands; the R13 consequences not yet built (a CC0 dedication affirmation in `CONTRIBUTING.md`, a credits record) are *(planned)*.

## Future-toolchain note *(planned)*

Parts of this pipeline may later be **built into the Matter Library toolset** (the Matter Manager / `tools/`) to support material creation in-house: a batch generate→decompose→assemble→QC harness, provenance tagging, the tileability/de-light checks as automated gates. **This is where future "agentic generation" work starts** — any such generator must emit provenance records that satisfy the shipped-pixel rule by construction. Recorded so the toolchain is anticipated, not retrofitted. Stage C (+ the structural QC gates) exists today: see [AuthoringHarness](../Tooling/AuthoringHarness.md).

*Shipped (Phase03, 2026-09-25): the first cut of agentic generation.* The `/matter-generate` skill (`.claude/skills/matter-generate/`) turns a brief into a draft article: Physically Based constants, an ambientCG scan or generated textures, every relevant wear layer, a recipe checked by the `recipe` lane, a render, and provenance for every new texture under `library/provenance/sources/`. The batch harness, the decomposer and the automated tileability/de-light gates above remain *(planned)*.

## Provenance source citations

So the provenance rule is **auditable against links, not memory** (web research, 2026-06-20). Statements are the sources' own claims, recorded neutrally; none of them establishes CC0-dedicability by itself.

- **PBRify_Remix (decomposer)** — the project states its models are trained exclusively on CC0 content (ambientCG, Poly Haven): https://github.com/Kim2091/PBRify_Remix
- **ambientCG** — a CC0-1.0 PBR texture library: https://ambientcg.com
- **Bria (generation)** — the vendor states its training data is licensed: https://bria.ai/ · https://bria.ai/licensed-training-catalog
- **Scenario (tileable PBR generation)** — seamless albedo/normal/metallic/roughness generation: https://www.scenario.com/features/generate-textures
- **Adobe Firefly** — the vendor describes its training data and commercial terms: https://business.adobe.com/products/firefly-business/firefly-ai-approach.html
- **Stable Diffusion training-data litigation** — Andersen v. Stability AI (N.D. Cal.), a public case concerning LAION-trained models: https://copyrightalliance.org/andersen-v-stability-ai-copyright-case/
- **Substance 3D Sampler** — Adobe removed the generative features (incl. Text-to-Texture) from Sampler, announced 2025-09-18, service ending in older versions 2026-03-05; Sampler is therefore a **decompose-only** tool in this pipeline (stage B, *Image-to-Material*), **not** a stage-A generator. Sources: https://experienceleague.adobe.com/en/docs/substance-3d-sampler/using/release-notes/all-changes · https://www.cgchannel.com/2025/08/adobe-releases-substance-3d-sampler-5-1/

## Status

**Golden path documented; staged open-first.** This spec records the path, the provenance posture and the shipped-pixel rule. Stage C and the structural QC gates are built ([AuthoringHarness](../Tooling/AuthoringHarness.md)); stages A→B as in-repo tooling are *(planned)*.

## History

- 2026-06-20: the golden path was defined with a vendor provenance tier table framed around the library selling its pixels; web research that day confirmed Adobe's removal of generative features from Substance 3D Sampler and reclassified Firefly as a production candidate.
- 2026-07: the `matterlib-0.1.0` provenance audit found every shipped texture to be ambientCG CC0 or in-house procedural; no bootstrap or vendor-generated pixels shipped.
- 2026-09-23: brought home; the shipped-pixel rule restated per R9/R13 (CC0-dedicable, with evidence); the tier table and vendor commentary kept and annotated as Drift.
