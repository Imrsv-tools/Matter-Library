# LCD Schema — two-tier parameter discipline

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

> **Status: FROZEN — names, types, ops, AND ranges.** This schema is the frozen cross-consumer LCD contract: the interface-input vocabulary **and** its value ranges/defaults, confirmed empirically by authoring the 7-article proof subset. Consumers build against these verbatim.
>
> **What "frozen" means here:** version-stable cross-consumer binding — the *current* ports/types/ops/ranges are fixed so the four consumers (MaterialX, a USD runtime, Unreal, Blender) bind them verbatim within a version. It does **NOT** mean permanently closed. **The LCD schema is expected to EVOLVE** — new dimensions may be added over time as we see opportunity. Read "frozen" throughout this doc as *"the current, stable LCD schema,"* not *"the final one."*

The **[LCD](../../Glossary.md) (Least Common Denominator)** discipline exposes **only what all targets can honor** — MaterialX/OpenPBR, UE (legacy/Substrate masters), Blender Principled BSDF. The control set *is* the cross-renderer contract: name/type/range agreed once. The set is deliberately **small** — "a few fun things, not all the things."

> **Drift (2026-09-23):** the Unreal target is **Unreal 5.8+ with Substrate** (Blender 5.1+), which retires the "legacy UE material model for v1" framing; the LCD vocabulary itself is unchanged — owned by the release-bundle / consumer-contract phase (R15, R6).

## The two tiers (one vocabulary, two audiences)

Conflating these is how parameter surfaces bloat. Same named OpenPBR inputs; two audiences.

| Tier | Who sets it | What | When |
|------|-------------|------|------|
| **Author tier (full LCD)** | a material *author* | maps + base values: base color, metallic, roughness, IOR, normal, SSS color/radius, emissive, … — **baked into the `.mtlx` values** | authoring time |
| **Creator subset (adjustable)** | a *[Creator](../../Glossary.md)* in a consuming application (Blender, IMRSV Studio, …) | the "fun things" a consumer exposes + the composition overrides via standard `inputs:` opinions | composition time, round-trips |

The **author tier** is the master's full param schema ([MasterSet](../Ontology/MasterSet.md)). The **Creator subset** ([Creator tier](../../Glossary.md)) is the chain's adjustment contract ([Identity](../Ontology/Identity.md)) — and a Creator tweak is a plain USD `inputs:` override on the bound material prim, never a new material.

## Author tier — the carrier contract

> **This tier was named here from the start and was specified late.** The consequence: **six of the seven masters could not express their defining behavior anywhere in the chain** — the values were absent from the producer schema and from everything downstream. A master that cannot carry the one property it exists for is inert. This table is that contract.

**The author tier is NOT Creator-adjustable** (it is baked article data, per the two-tier table above). It therefore never round-trips as a composition override — it travels **article → producer → consumer → master**, and is re-read on load.

**Carriage rule — which lane a value takes is decided by ONE question: does OpenPBR have an input for it?**

| Lane | When | How it is carried | Validator impact |
|---|---|---|---|
| **A — OpenPBR-expressible** | the value IS an `open_pbr_surface` input | authored **on the shader node**, under its **OpenPBR name** (the pattern `specular_ior` / `transmission_weight` / `emission_*` already use) | none — no nodegraph interface input, so `lcd-as-input` is untouched |
| **B — not expressible** | OpenPBR has **no** such input — only the **Masked cutoff** and the **TwoLayer layer-2 set** | a **named author-tier interface input** on the nodegraph | ⚠ requires `lcd-as-input` to be a **two-tier vocabulary** (`LCD_PORTS ∪ AUTHOR_TIER_PORTS`) — it previously rejected *any* interface input outside the frozen 8, which is literally why the cutoff and layer-2 set were **unauthorable** |

*(Updated 2026-09-23, measured: `tools/converters/assemble_mtlx.py` defines `LCD_PORTS` (the 8 Creator ports) and a separate `AUTHOR_TIER_PORTS` = `opacity_cutoff`, `layer_blend_balance`, `layer_blend_contrast`, `layer2_base_color`, `layer2_roughness`, `layer2_metalness`; `tools/validators/validate_material.py` checks `lcd-as-input` against their union.)*

**Per-master defining carriers (producer side).** Names are frozen across every layer of the chain; the producer-side names are:

| Master | Defining property | Producer input(s) | Lane |
|---|---|---|---|
| **Opaque** | base PBR | *(base PBR)* | — |
| **Masked** | opacity **cutoff** | `geometry_opacity` · **`opacity_cutoff`** | A · **B** |
| **TranslucentThin** | **IOR** | `specular_ior` · `transmission_weight` · `transmission_color` · **`geometry_thin_walled = true`** | A |
| **TranslucentThick** | **absorption** colour + depth | *(as Thin)* + **`transmission_depth`** · **`geometry_thin_walled = false`** | A |
| **Subsurface** | **SSS** colour + radius | `subsurface_weight` · `subsurface_color` · `subsurface_radius` *(float)* · `subsurface_radius_scale` *(color3)* | A |
| **TwoLayer** | **two real layers** + blend | `layer2_{base_color,roughness,metalness,normal}_tex` + consts · **`layer_blend_balance`** · **`layer_blend_contrast`** | **B** |
| **Emissive** | **emission** colour + intensity | `emission_color` · `emission_luminance` | A |

*Consumer-side (IMRSV): the same carriers' wire-field, runtime-domain, Unreal material-instance parameter and Unreal pin names for each master — see [Consumers](../Consumers.md).*

⭐ **`geometry_thin_walled` is the OpenPBR thin-vs-thick discriminator** — it is what makes TranslucentThick *not* TranslucentThin **at the producer**. Without it the two masters are the same material described twice.

*Consumer-side (IMRSV): the Unreal material-instance naming rule (snake_case reserved for the 8 Creator ports, PascalCase for every author-tier parameter — the tier boundary made visible) — see [Consumers](../Consumers.md).*

## Creator-adjustable subset — FROZEN interface-input vocabulary

**The frozen cross-consumer vocabulary = the interface-input port names** (what the four consumers — MaterialX, a USD runtime, Unreal, Blender — bind). A Creator tweak is a **tint multiply / bias add / set applied on top of** the OpenPBR input, not the raw input itself — so each port is *purpose-named* (the `_tint`/`_bias` suffixes denote tweak-on-top), while the **Affects (OpenPBR)** column names the value the port modifies. **Names / types / ops AND ranges/defaults are FROZEN — confirmed empirically against the 7-article proof subset.**

| Interface input (frozen name) | Type | Affects (OpenPBR) | Op | Range / default |
|---|---|---|---|---|
| `base_color_tint` | color3 | `base_color` | multiply | 0–1 per channel / `(1,1,1)` |
| `uv_scale` | vector2 | `place2d.scale` | set | >0 / `(1,1)` |
| `uv_offset` | vector2 | `place2d.offset` | set | any / `(0,0)` |
| `uv_rotation` | float (deg) | `place2d.rotate` | set | 0–360 / `0` |
| `overlay1_density` | float | overlay-1 mix | set | 0–1 / `0` |
| `overlay2_density` | float | overlay-2 mix | set | 0–1 / `0` |
| `maskset_blend` (×≤1) | float | maskset blend | set | 0–1 / `0` |
| `roughness_bias` | float | `specular_roughness` | add | −0.5…+0.5 / `0` |

*(Updated 2026-09-23, measured: `LCD_PORTS` in `tools/converters/assemble_mtlx.py` carries exactly these 8 names, types and defaults.)*

**Notes:**
- **UV placement has two layers — only the numeric one is consumer-side.** The **mesh UV unwrap / layout authored in Blender is the PRIMARY placement**, and it travels with the geometry as USD **primvars** (it is geometry, not a material param — **Blender is the authoritative UV-authoring environment**). The numeric **`place2d` transform** (`uv_scale`/`uv_offset`/`uv_rotation`) rides the `place2d` nodegraph, not a prim attr; Blender mapping-node edits do NOT export, so **that numeric transform is a last-mile NUDGE only** (e.g. in IMRSV Studio) — never a replacement for the Blender-authored UV set.
- **Overlay intensity** ×≤2 (`overlay1_density`/`overlay2_density`) is the **layered-materials marquee** (dust, scratches).
- **`maskset_blend`** supersedes the earlier `mask_*` placeholder — named for the **maskset concept** (not the v1 single-channel limit) so multi-channel masks don't force a cross-consumer rename.
- **Names use OpenPBR-aligned terms** so the same word means the same thing in MaterialX, the Unreal instance param, and the Blender node-group input.

**✓ Ranges/defaults confirmed against the 7-article proof subset (ABS · Limestone · Concrete · Copper · UVGrid · Glass · IMRSV_MissingMaterial) and frozen.** Per-material authored *start values* may differ from the schema default within the frozen range (e.g. the aged-copper article authors `base_color_tint` = `(0.95, 0.64, 0.54)` and `maskset_blend` = `0.35`) — the range/default here is the contract; a material's authored starting value is data.

## Carrier rule (no `imrsv:` attrs)

Every adjustable is a **standard `inputs:` override** on the bound material prim (or a `place2d` nodegraph input for UV) — standard `UsdShade`, readable by any tool. **No `imrsv:` custom attrs.** Per-object adjustment requires **per-object material instances** (separate material prims per object, e.g. `<name>_Instance_<N>`) since input overrides on a shared material affect every prim bound to it.

## Render-role texture nodes — assembler-owned node-name contract

The overlay/mask **textures** (distinct from their Creator-adjustable `overlay1_density`/`overlay2_density`/`maskset_blend` *scalars* above) are **fixed per article** — only the blend amount is Creator-adjustable, the bitmap is not. They therefore are **NOT** material-level `inputs:` and are **NOT** in the Creator subset. MaterialX rejects extra inputs on the fixed `<surfacematerial>` nodedef (`sdk-validate` "Node interface error"), so a fixed texture path can only live **inside the nodegraph**, on an `<image>` node's `file` input. So that a consumer can find those paths, the producer (the [assembler](../Tooling/AuthoringHarness.md)) and every consumer agree on a **fixed render-role node name** per role:

| Render role | Nodegraph `<image>` node name (FROZEN) | Color space |
|---|---|---|
| Overlay 1 | `overlay1_tex` | **linear** (packed data) ⚠ *corrected* |
| Overlay 2 | `overlay2_tex` | **linear** (packed data) ⚠ *corrected* |
| Maskset | `maskset_tex` | linear (coverage mask) |

⚠ **Colour-space correction.** The overlay rows previously said **"sRGB (albedo)"**. That was wrong, and it contradicted the owning ontology: [MasterSet](../Ontology/MasterSet.md) defines an [overlay](../../Glossary.md) as a **packed data texture** (R/G = normal XY · B = roughness bias · A = mask density). Annotated as sRGB albedo, the assembler duly **mixed the overlay bitmap over base colour** — painting packed normal/roughness data on as if it were paint, and corrupting every channel through the sRGB transfer curve on the way in. **All three render-role textures are data and load `lin_rec709`.** Neither an overlay nor a [maskset](../../Glossary.md) may ever contribute colour — both are **modulators** ([MasterSet §Overlay/MaskSet model](../Ontology/MasterSet.md)).

*(Updated 2026-09-23, measured: every render-role `<image>` in the live articles — `overlay1_tex`/`overlay2_tex` in Concrete, Glass and Copper, `maskset_tex` in Glass, Copper and Rust — declares `colorspace="lin_rec709"`; overlays are `color4` (alpha = mask density), the maskset `color3`; the assembler's `DATA_COLORSPACE` is `lin_rec709`. `srgb_texture` appears only on base-colour albedo images.)*

**This is a spec correction, NOT a vocabulary reopen.** No Creator port name, type, op or range changes; the frozen interface-input vocabulary above is untouched. What changed is a **wrong colour-space annotation** on a texture-role table.

- **Producer:** `tools/converters/assemble_mtlx.py` emits these `<image>` nodes by these exact names (the contract pins them).
- **Consumer:** a consumer reads each named node's `inputs:file` from the bound material's nodegraph (`…/NG_<name>/<role>_tex`).
- These node names are **part of the LCD render contract**: renaming a render-role node is a cross-consumer break, the same discipline as the frozen interface-input names. The *blend* of each layer stays Creator-adjustable via its scalar port above; the *texture* is author-tier data.

*Consumer-side (IMRSV): how IMRSV's material extractor carries the three render-role texture paths (and any material-prim `inputs:<role>_texture` override that takes precedence) to its renderer — see [Consumers](../Consumers.md).*

> **Drift (2026-09-23):** under R14 the render-role names, the Creator port vocabulary and the author-tier carriers are published **as data** in each release (the [master contract](../../Glossary.md), *(planned)*), not only as this document — owned by the release-bundle / consumer-contract phase (R14).

## Status

**Creator subset: FROZEN — names/types/ops + ranges/defaults.** The interface-input port vocabulary **and** its value ranges/defaults are frozen as the cross-consumer contract, confirmed empirically by authoring the 7-article proof subset. No wire/ABI contract is frozen here.

**Author tier: SPECIFIED and SHIPPED.** §Author tier above is the contract (carriage lanes and per-master producer carriers). **The Creator subset was NOT reopened** — no port name, type, op or range moved. The one edit inside the frozen region is a **colour-space correction** on the render-role texture table (overlays are data, not albedo), which fixes an annotation that contradicted [MasterSet](../Ontology/MasterSet.md). All seven masters have been shown carrying and rendering their defining behaviour end to end in a consumer.

⚠ **Two master-side rules constrain what an article may honestly author — both owned by [MasterSet](../Ontology/MasterSet.md), not here:**
- **The [opacity floor](../../Glossary.md)** (`MIN_TRANSMISSIVE_OPACITY = 0.05`). The translucent masters compute `Opacity = Opacity × (1 − Transmission)`, so an honest `transmission = 1.0` would drive opacity to exactly zero. The **master** clamps; **the article is never fudged to protect the master.**
- **`two_sided` is baked into the master, not driven per-prim** (Masked · TranslucentThin · TranslucentThick). Unreal cannot flip `TwoSided` on a Material Instance — it is a static shader property — so a per-prim value has nowhere to land on those three.

**Not in either tier: emissive COLOUR is authored on the article, and is not a Creator control.** `emission_color` / `emission_luminance` are native `open_pbr_surface` inputs (carriage lane **A**), so they sit on the shader node — not in the frozen 8-port Creator vocabulary, and not in `AUTHOR_TIER_PORTS` (which is by definition *"the values OpenPBR has no input for"*). ⇒ **The colour of an emissive article is a property of the article; you change it by authoring a different article.** Widening the Creator vocabulary to expose an emission tint would **reopen the frozen contract**; it stays an open product question.

## History

- Pre-standalone (2026-06 → 2026-07): the Creator vocabulary (8 ports, names, types, ops, ranges) was frozen after the 7-article proof subset was authored against it; `maskset_blend` replaced an earlier `mask_*` placeholder then.
- Pre-standalone: the UV note was corrected once, after early wording had implied the consuming application owned UV placement rather than Blender's mesh unwrap.
- 2026-07-14: the author tier was specified and shipped after six of the seven masters were found unable to carry their defining property; the lane-B split of the validator vocabulary dates from then.
- 2026-07-14: the render-role overlay rows were corrected from sRGB albedo to linear data, after the assembler had mixed overlay bitmaps over base colour because of the wrong annotation.
- 2026-07-14: emissive colour as a Creator control was raised as a product question and left open rather than reopening the frozen vocabulary.
