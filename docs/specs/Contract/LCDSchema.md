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
| **Creator subset (adjustable)** | a *[Creator](../../Glossary.md)* in a consuming application (Blender, IMRSV Studio, …) | the "fun things" a consumer exposes + the composition overrides via standard, **connected** `inputs:` opinions ([§Carrier rule](#carrier-rule-no-imrsv-attrs)) | composition time, round-trips |

The **author tier** is the master's full param schema ([MasterSet](../Ontology/MasterSet.md)). The **Creator subset** ([Creator tier](../../Glossary.md)) is the chain's adjustment contract ([Identity](../Ontology/Identity.md)) — and a Creator tweak is a value on the bound material prim's `inputs:<port>`, **connected from the article's nodegraph** so that any USD tool resolves it ([§Carrier rule](#carrier-rule-no-imrsv-attrs)), never a new material.

## Author tier — the carrier contract

> **This tier was named here from the start and was specified late.** The consequence: **six of the seven masters could not express their defining behavior anywhere in the chain** — the values were absent from the producer schema and from everything downstream. A master that cannot carry the one property it exists for is inert. This table is that contract.

**The author tier is NOT Creator-adjustable** (it is baked article data, per the two-tier table above). It therefore never round-trips as a composition override — it travels **article → producer → consumer → master**, and is re-read on load.

**Carriage rule — which lane a value takes is decided by ONE question: does OpenPBR have an input for it?**

| Lane | When | How it is carried | Validator impact |
|---|---|---|---|
| **A — OpenPBR-expressible** | the value IS an `open_pbr_surface` input | authored **on the shader node**, under its **OpenPBR name** (the pattern `specular_ior` / `transmission_weight` / `emission_*` already use) | none — no nodegraph interface input, so `lcd-as-input` is untouched |
| **B — not expressible** | OpenPBR has **no** such input — only the **Masked cutoff** and the **TwoLayer layer-2 set** | a **named author-tier interface input** on the nodegraph | ⚠ requires `lcd-as-input` to be a **two-tier vocabulary** (`LCD_PORTS ∪ AUTHOR_TIER_PORTS`) — it previously rejected *any* interface input outside the frozen 8, which is literally why the cutoff and layer-2 set were **unauthorable** |

*(Updated 2026-09-23, measured: `tools/converters/assemble_mtlx.py` defines `LCD_PORTS` (the 8 Creator ports) and a separate `AUTHOR_TIER_PORTS` = `opacity_cutoff`, `layer_blend_balance`, `layer_blend_contrast`, `layer2_base_color`, `layer2_roughness`, `layer2_metalness`; `tools/validators/validate_material.py` checks `lcd-as-input` against their union. **Since then:** `cutout_map` (2026-09-27) and `base_color_map` (2026-09-30), the mesh-supplied maps.)*

**Per-master defining carriers (producer side).** Names are frozen across every layer of the chain; the producer-side names are:

| Master | Defining property | Producer input(s) | Lane |
|---|---|---|---|
| **Opaque** | base PBR | *(base PBR)* · *(optional, as on Masked, Hair and Subsurface)* **`base_color_map`**, the mesh's picture supplied at binding ([§Base colour map](#base-colour-map-the-meshs-picture-supplied-at-binding), 2026-09-30) | — · **B** |
| **Masked** | opacity **cutoff** | `geometry_opacity` · **`opacity_cutoff`** · *(optional)* **`cutout_map`**, the mesh's own cut-out supplied at binding ([§Cut-out map](#cut-out-map-the-meshs-supplied-at-binding), 2026-09-27) | A · **B** |
| **Hair** *(2026-09-28, Phase08)* | **light through the card, softly covered** *(reworked 2026-09-28 from "as Masked: opacity cutoff", settings-only; [MasterSet](../Ontology/MasterSet.md))* | `geometry_opacity` ← **`cutout_map`** unthresholded (**no `opacity_cutoff`**) · **`geometry_thin_walled = true`** · **`subsurface_weight`** · **`subsurface_color` connected to `base_color_out`** · `subsurface_scatter_anisotropy` · `specular_roughness_anisotropy` for the fibre's highlight · *(2026-09-30, Phase09 9.1)* **`base_color_map`**, the hairstyle's picture, and **`specular_weight = 0`**: card hair is **matte** (the lead at Phase09 click 1: the shine *"gives away these are flat sheets"*; *"until we get proper hair... this will need to be the way"*) | A · **B** |
| **TranslucentThin** | **IOR** | `specular_ior` · `transmission_weight` · `transmission_color` · **`geometry_thin_walled = true`** | A |
| **TranslucentThick** | **absorption** colour + depth | *(as Thin)* + **`transmission_depth`** · **`geometry_thin_walled = false`** | A |
| **Subsurface** | **SSS** colour + radius | `subsurface_weight` · `subsurface_color` · `subsurface_radius` *(float)* · `subsurface_radius_scale` *(color3)* | A |
| **TwoLayer** | **two real layers** + blend | `layer2_{base_color,roughness,metalness,normal}_tex` + consts · **`layer_blend_balance`** · **`layer_blend_contrast`** | **B** |
| **Emissive** | **emission** colour + intensity | `emission_color` · `emission_luminance` | A |

*Consumer-side (IMRSV): the same carriers' wire-field, runtime-domain, Unreal material-instance parameter and Unreal pin names for each master — see [Consumers](../Consumers.md).*

**Optional lane-A carriers — coat, fuzz and scatter anisotropy** *(added 2026-09-27, Phase07 step 7.3; additive)*. Real `open_pbr_surface` inputs under their OpenPBR names, so they take lane A like every value above. None defines a master: they are the optional params [MasterSet](../Ontology/MasterSet.md) row 1 already names (*"sheen, clearcoat"*), which skin needs (an oily sheen, a fine grazing-angle fuzz, forward scatter). **An article authors each only when it sets it**, so an article that sets none of them is byte-identical to before, and a consumer that does not read one renders that article exactly as before.

| Carrier | Producer input(s) (OpenPBR) | Masters | Blender master socket → Principled BSDF |
|---|---|---|---|
| **Coat** | `coat_weight` · `coat_color` · `coat_roughness` · `coat_ior` | any | `Coat Weight` · `Coat Color` → **Coat Tint** · `Coat Roughness` · `Coat IOR` |
| **Fuzz** | `fuzz_weight` · `fuzz_color` · `fuzz_roughness` | any | `Fuzz Weight` / `Fuzz Color` / `Fuzz Roughness` → **Sheen** Weight / Tint / Roughness |
| **Scatter anisotropy** | `subsurface_scatter_anisotropy` *(−1…1; > 0 = forward)* | Subsurface | `Subsurface Anisotropy` *(Blender honours 0…1, random-walk methods only)* |
| **Specular anisotropy** *(carrier C3, added 2026-09-27 at Phase07 step 7.6)* | `specular_roughness_anisotropy` *(0…1)* | any | `Anisotropy` → Principled **Anisotropic** = a ÷ 0.9 and **Roughness** × (2(1−a) ÷ (1+(1−a)²))^¼, with the **UV-map** tangent. That matches OpenPBR's lobe (its axis ratio and its area) exactly up to a = 0.9, and is the identity at a = 0 |

**The anisotropy tangent is the mesh's UV `U` direction.** OpenPBR's `geometry_tangent` defaults to `Tworld`, derived from texcoord 0, and the highlight stretches **along** it. A card mesh whose strands run along `V` therefore gets the fibre's band across the strands. That is a requirement on the mesh (the platform's side), not on the article.

Defaults are OpenPBR's (weight 0; coat IOR 1.6; fuzz roughness 0.5). The coat sits on the **geometry** normal, not the article's normal map, as OpenPBR's `geometry_coat_normal` defaults to it. *Consumer-side:* an Unreal master gains the matching parameters when it is built (Phase06), and IMRSV's extractor must read them to show them ([PlatformDependencies](../../Planning/PlatformDependencies.md) M1).

⭐ **`geometry_thin_walled` is the OpenPBR thin-vs-thick discriminator** — it is what makes TranslucentThick *not* TranslucentThin **at the producer**. Without it the two masters are the same material described twice. *(2026-10-05: what a **consumer** draws for each is owned by [MasterSet](../Ontology/MasterSet.md) §Material-settings intent: a thin-walled article does not deflect the view at any angle, and a solid one bends it by its index.)*

*Consumer-side (IMRSV): the Unreal material-instance naming rule (snake_case reserved for the Creator ports, PascalCase for every author-tier parameter — the tier boundary made visible) — see [Consumers](../Consumers.md).*

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
| `overlay3_density` | float | overlay-3 mix | set | 0–1 / `0` *(added 2026-09-25)* |
| `maskset_blend` (×≤1) | float | maskset blend | set | 0–1 / `0` |
| `roughness_bias` | float | `specular_roughness` | add | −0.5…+0.5 / `0` |
| `overlay1_color` · `overlay2_color` · `overlay3_color` | color3 | `base_color` where a **deposit** overlay lies | set (the deposit's colour; it covers by the overlay's effect) | 0–1 per channel / `(0.413, 0.386, 0.308)` *(added 2026-10-01, Phase10)* |
| `transmission_color` | color3 | `transmission_color` | set (the colour seen through the surface; the Creator's value replaces the article's) | 0–1 per channel / `(1,1,1)`; an article starts at its own authored colour *(added 2026-10-05, Phase12)* |

*(Updated 2026-10-05, Phase12: **`transmission_color` added**, the third evolution, additive as the first two. It is the first port that **sets an OpenPBR input an author otherwise fixes on the shader** (lane A). On an article that declares it, the value sits on a nodegraph interface input under the same name, the shader's input is connected to it, and the article's own colour is where the port starts. Only an article on a see-through master may declare it (TranslucentThin, TranslucentThick). An article that does not declare it keeps the value on the shader and assembles byte-identically. It reverses the 2026-09-25 ruling that a see-through colour is its own authored article (the lead, 2026-10-05; `docs/Planning/Phases/Phase12_GlassAndLightColour.md`, RD-GLC-2). `LCD_PORTS` now carries 13. **In the library's targets:** the assembler, the Blender masters (v9; v10 since step 12.3, where the solid master works its absorption out from the port), the Blender exporter's travel list *(step 12.2, 2026-10-05; was "planned")* and the rig's Unreal driver; the library's Unreal masters already carried the parameter under this name, so the pinned runtime is unchanged. **Planned in the same phase:** the see-through articles other than Glass_Clear and Diamond_Brilliant, and the emission pair `emission_color` and `emission_luminance`. A consumer that does not yet know the port renders the article's own colour, as before. **Why not the Material input USD already makes:** reading a `.mtlx`, usdMtlx puts every valued shader input on the Material, so a stock tool could override this one with no port at all; that exposure exists only while the value sits on the shader, and it is not how any other Creator port is declared or carried.)*

*(Updated 2026-10-01, Phase10: **`overlay1_color`…`overlay3_color` added**, the second evolution, additive as the first: an article declares `overlayN_color` only when overlay N is a **deposit** (today `Dust01`), and an article with no deposit assembles byte-identically. The default is Physically Based's Sand (CC0; `0.44, 0.386, 0.231`) desaturated halfway to its own luminance, since household dust is greyer than sand. What the cover does: [MasterSet](../Ontology/MasterSet.md) §Overlay semantic. `LCD_PORTS` now carries 12. A consumer that does not yet know the ports renders dust colourless, as before. **Shipped in every library target (Phase10 close, 2026-10-01):** the assembled articles, the Blender masters (v8) and the library's Unreal masters (`unreal-runtime-v3`, which take `overlayN_color` and the switch `overlayN_deposit`); the platform's side is `PlatformDependencies.md` P22.)*

*(Updated 2026-09-23, measured: `LCD_PORTS` in `tools/converters/assemble_mtlx.py` carries exactly these 8 names, types and defaults.)*

*(Updated 2026-09-25: **`overlay3_density` added**, the first evolution of this vocabulary. The overlay cap rose from 2 to 3 (lead; [MasterSet](../Ontology/MasterSet.md) §Overlay/MaskSet model). The change is additive: no existing name, type, op or range moved, an article declares the port only when it carries a third overlay, and every shipped article assembles byte-identically (the `determinism` lane). `LCD_PORTS` now carries 9. A consumer that does not yet know the port does not render overlay 3 until it adds it: `PlatformDependencies.md` P12.)*

**What the ports mean is what MaterialX computes** *(stated 2026-09-24; lead ruling: "the number we see in [a consuming application] is the number we see in a stock USD viewer")*. The article is the reference implementation, and a consumer that renders these ports conforms to it; none may reinterpret them.
- **UV placement is MaterialX `place2d`** (`ND_place2d_vector2`: pivot at the UV origin, scale → rotate → offset). `uv_scale` **divides** the texture coordinate, so `2` makes the texture **twice as large** (fewer repeats) and `0.5` repeats it twice. `uv_rotation` turns the texture **counter-clockwise** by that many degrees about the UV origin (the texture's bottom-left in USD `st` space). `uv_offset` is **subtracted** from the coordinate after the rotation. *(This corrects nothing in the table: `place2d.scale` was always the target. It rules out the other USD 2D convention, UsdPreviewSurface's `UsdTransform2d`, which multiplies by scale and adds the translation, and renders the same saved value as the opposite picture.)*
- **`roughness_bias` is added, then the total is clamped to [0, 1]** (the article's `roughness_biased_clamped` node, since 2026-09-24). OpenPBR does not clamp `specular_roughness`, so without it a negative total renders rough in a stock viewer and glossy in a consumer that clamps. The op stays `add`; the clamp is the article's, and every consumer matches it.

**Notes:**
- **UV placement has two layers — only the numeric one is consumer-side.** The **mesh UV unwrap / layout authored in Blender is the PRIMARY placement**, and it travels with the geometry as USD **primvars** (it is geometry, not a material param — **Blender is the authoritative UV-authoring environment**). The numeric **`place2d` transform** (`uv_scale`/`uv_offset`/`uv_rotation`) lands on the article's `place2d` node, reached through the nodegraph interface like every other Creator port ([§Carrier rule](#carrier-rule-no-imrsv-attrs)), never a custom prim attr; Blender mapping-node edits do NOT export, so **that numeric transform is a last-mile NUDGE only** (e.g. in IMRSV Studio) — never a replacement for the Blender-authored UV set.
- **The mesh's UV unit must be the article's tile** *(stated 2026-09-28, Phase08 F-P08-8; it was only implied until then)*. An article is authored at real size: one UV unit = one tile = its `meters_per_tile` (in `imrsv_metadata`; skin 0.01 m). A mesh whose UVs are in another unit draws the detail at the wrong size: on MakeHuman's own atlas, one UV unit ≈ 1.69 m of body, so a 1 cm skin detail renders ~170× too large, as large worm-like furrows. **Either** the mesh carries real-scale UVs in the article's tiles (metres ÷ `meters_per_tile`; the character's detail UV set, [PlatformDependencies](../../Planning/PlatformDependencies.md) P18), **or** the binding sets **`uv_scale = meters_per_tile ÷ (metres per UV unit)`**. ⚠ **`uv_scale` divides** (`place2d`, above), so a detail that must shrink takes a value **below 1**: ≈ 0.006 on the raw hm08 atlas, never 170. A cut-out card is the exception: its `cutout_map` is sampled on the mesh's own atlas, not through `place2d` (§Cut-out map).
- **Overlay intensity** ×≤3 (`overlay1_density`/`overlay2_density`/`overlay3_density`; the third added 2026-09-25, an additive change — library semver-minor) is the **layered-materials marquee** (dust, scratches). A deposit's colour (`overlayN_color`, 2026-10-01) is the Creator's too, so desert dust or soot is one setting away (the lead's ruling RD-P10-1, `Phase10_ColouredWearLayers.md`).
- **`maskset_blend`** supersedes the earlier `mask_*` placeholder — named for the **maskset concept** (not the v1 single-channel limit) so multi-channel masks don't force a cross-consumer rename.
- **Names use OpenPBR-aligned terms** so the same word means the same thing in MaterialX, the Unreal instance param, and the Blender node-group input.

**✓ Ranges/defaults confirmed against the 7-article proof subset (ABS · Limestone · Concrete · Copper · UVGrid · Glass · IMRSV_MissingMaterial) and frozen.** Per-material authored *start values* may differ from the schema default within the frozen range (e.g. the aged-copper article authors `base_color_tint` = `(0.95, 0.64, 0.54)` and `maskset_blend` = `0.35`) — the range/default here is the contract; a material's authored starting value is data.

## Carrier rule (no `imrsv:` attrs)

Every adjustable — **all 9 Creator ports, UV placement included** — is a **standard `inputs:<port>` value on the bound material prim, connected from the article's nodegraph interface input**:

```usda
def "Copper_Verdigris_Aged_Base_s01_v01_Instance_1" (
    prepend references = @Copper_Verdigris_Aged_Base_s01_v01.mtlx@</MaterialX/Materials/Copper_Verdigris_Aged_Base_s01_v01>
)
{
    color3f inputs:base_color_tint = (1, 0, 0)          # the Creator's value
    over "NG_Copper_Verdigris_Aged_Base_s01_v01"
    {
        color3f inputs:base_color_tint.connect = </…/Copper_Verdigris_Aged_Base_s01_v01_Instance_1.inputs:base_color_tint>
    }
}
```

This is UsdShade's documented pattern for exposing a parameter on a Material (`usdShade/overview.dox` §Exposing parameters on containers) — standard `UsdShade`, readable by any tool. **No `imrsv:` custom attrs.** The rules:

- **Why the connection is required.** When USD reads a `.mtlx`, usdMtlx exposes only the **surface shader's** inputs on the Material; the article's Creator ports stay on its nodegraph `NG_<id>` (a child of the Material once the reference composes). An **unconnected** Material input is in no connection chain, so it drives nothing: **an override without the connection is inert in every stock USD tool** (usdview, `usdrecord`, any Hydra delegate). It is not *invalid*, so no stock USD validator flags it. The article cannot fix this itself, because MaterialX forbids extra inputs on the fixed `<surfacematerial>` nodedef ([§Render-role texture nodes](#render-role-texture-nodes--assembler-owned-node-name-contract)).
- **Resolution is USD's, for every consumer.** The effective value of a port is `UsdShadeInput(NG_<id>.inputs:<port>).GetValueProducingAttributes()`: the outermost authored value in the chain wins. A value on the Material input overrides the article; a connected Material input **with no value** lets the article's start value flow through unchanged, so a writer may author the connection up front. No consumer applies a resolution rule of its own.
- **Only a port the article declares.** An article declares the Creator ports it uses (the UV grid declares 4 of the 8). An override on a port its nodegraph does not declare has nothing to connect to and is inert, so **a writer refuses it** rather than authoring it.
- **Typed from the nodegraph input.** The Material input takes the article's declared type: `base_color_tint` is `color3f`, never `float3`; the UV ports are `float2`/`float`.
- **Every writer authors the connection with the value:** the Blender exporter (`blender/addons/imrsv_lcd_export`, since 2026-09-24) and every consuming application that writes overrides. The `NG_<id>` name is deterministic ([MaterialXTemplate](MaterialXTemplate.md): the full stem, including `_vNN`) and the connection is path-based, so it is authored even when the `.mtlx` reference does not resolve at write time.
- **Checked by** `tools/conformance/check_lcd_carrier.py` ([USDValidationToolchain](../Tooling/USDValidationToolchain.md) §Checks), which fails any Material-level Creator input that is unconnected, undeclared or mistyped.

Per-object adjustment requires **per-object material instances** (separate material prims per object, e.g. `<name>_Instance_<N>`) since input overrides on a shared material affect every prim bound to it.

## Cut-out map (the mesh's, supplied at binding)

*(Added 2026-09-27, Phase07 step 7.6, ruling L2: "a cut-out map the mesh supplies when the material is bound". Additive: no existing port, name, type or range moved, and every existing article assembles byte-identically.)*

Hair, brows and lashes are cards whose strands are the **transparency of the mesh's own texture**. That picture belongs to the mesh, not to the substance ([D1](../../Glossary.md): matter only, never assemblies), so it is **never part of the article**. A Masked article that accepts one **declares the input**, and the mesh supplies the map when the article is bound.

- **The input:** `cutout_map`, a nodegraph interface input of type `filename` (USD `asset`). It is an **author-tier, lane-B** input (`AUTHOR_TIER_PORTS`; OpenPBR has no such input), **Masked and Hair only** *(Hair since 2026-09-28)*, and it is **not a Creator port**. The article's value is **empty**.
- **Carried by the [Carrier rule](#carrier-rule-no-imrsv-attrs), unchanged:** `asset inputs:cutout_map = @<the mesh's map>@` on the bound Material, with `NG_<id>.inputs:cutout_map` connected to it. Each mesh has its own map, so **each binding needs its own Material instance**, as any per-object adjustment does. *(Measured 2026-09-27, OpenUSD 26.03 + MaterialX 1.39.5, `usdrecord`: the map set on the Material and connected reaches the image in Storm.)*
- **With no map supplied the card is solid, never magenta.** The article's `cutout_tex` image has `default = 1`, which MaterialX returns for an empty file. *(Measured in Storm the same day.)*
- **Where the map is sampled:** texcoord 0 (the mesh's `st`), **directly, not through `place2d`**. The map is drawn on the mesh's own UVs, so the Creator's UV nudges must not move it. It is one channel: MaterialX reads a `float` image's **first** channel, so a texture's alpha is supplied as an image of its own. White is strand, black is gap. A **Masked** article thresholds it with `opacity_cutoff` like any Masked source; a **Hair** article takes it as **soft coverage**, unthresholded, and declares no `opacity_cutoff` *(2026-09-28, Phase08 8.1 rework)*.
- **Why not a second UV set:** Storm reads `st` for every `texcoord` index (measured 2026-09-27: index 1 over an authored `primvars:st1` rendered identically to index 0). A dedicated UV set would work in Blender and Unreal and silently not in USD viewers, which fails the LCD principle.
- **Consequence for a card mesh:** its primary UVs are the atlas its map is drawn on. A tiling detail on the same article would be sampled on that atlas too, so the hair article carries none (its colour, roughness and anisotropy are constants). How this meets the character's real-scale detail UV set (Phase07 F13, platform side) is recorded in [PlatformDependencies](../../Planning/PlatformDependencies.md).
- **One opacity source per article:** its own `opacity_tex` (a pattern of the substance, like Lace) **or** the mesh's `cutout_map`, never both. The assembler refuses both.
- **Render-role node:** `cutout_tex` (an `image`) has **no `file` value in the article**. Its file comes from the binding. A consumer that enumerates image `file` values must skip an empty one (as `validate_material.py`, the rig and the Blender loader do) and read the Material's `inputs:cutout_map` instead.

## Base colour map (the mesh's picture, supplied at binding)

*(Added 2026-09-30, Phase09 step 9.1, RD-P09-1; research `260929_R_CharacterMaps.md` MAP-RD1, MAP-RD3 as amended. Additive: no existing port, name, type or range moved, and every other article assembles byte-identically.)*

A hairstyle's strands, and an eye's iris and veins, are a **picture drawn on the mesh's own layout**. Like the cut-out, it belongs to the mesh, never to the article (D1, CM2); unlike the cut-out, it **shades the article's colour**. The library holds the pictures in its **fit set** (`MatterLibrary/textures/fit/<family>/`, [Glossary](../../Glossary.md) *fit set*), and a consumer supplies one when it binds the article.

- **The input:** `base_color_map`, a nodegraph interface input of type `filename` (USD `asset`), **author tier, lane B** (`AUTHOR_TIER_PORTS`), **not a Creator port**, empty in the article. **Opaque, Masked, Hair and Subsurface** take it; the masters whose base is layered (TwoLayer), light (Emissive) or seen through (Translucent\*) do not.
- **The formula:** `base = base_color_const × base_color_map × base_color_tint`. The picture **multiplies** (it modulates, never replaces: a replaced colour only darkens under the tint, MAP-F2). It is the picture's normalised **structure**, prepared by the library (brightest strand ≈ 1), so the article's own light colour and the tint set the colour on every style.
- **Carried and sampled as the cut-out is:** the [Carrier rule](#carrier-rule-no-imrsv-attrs) (`asset inputs:base_color_map` on the bound Material, `NG_<id>.inputs:base_color_map` connected to it; one Material instance per binding); texcoord 0 directly, **not through `place2d`**. Colour space `srgb_texture`, a `color3` image.
- **With no picture supplied the article reads as its own colour, never magenta:** the image's `default` is white.
- **Render-role node:** `base_color_map_tex` (an `image`) has **no `file` value in the article**; a consumer that enumerates image files skips it and reads the Material's `inputs:base_color_map` (as it does `cutout_tex`).
- **Not a modulator in [MasterSet](../Ontology/MasterSet.md)'s sense:** it is colour on the mesh's layout, not packed data on the article's tile, so the overlay and maskset rules do not apply to it.
- **On Subsurface, the scattered colour follows the picture too** *(Phase09 9.2, F-P09-5)*: an article whose `subsurface_color` is connected to its base scatters the picture's colour; otherwise the picture keeps only `1 − subsurface_weight` of its strength (Learnings MaterialX M4). `Eye_Natural` is the first such article.
- **Shipped in every target (Phase09, 2026-09-30):** the assembled articles (Storm and any MaterialX reader), the Blender masters, and **the library's Unreal masters' own `base_color_map_tex`** (Opaque, Masked, Hair, Subsurface; `unreal-runtime-v2`), which a consumer uploads **linear** (the runtime decodes sRGB on the CPU; `PlatformDependencies.md` P20, P21). The library's fit set for MakeHuman holds each hairstyle's picture and cut-out, the brows' and lashes', and nine eye pictures (`MatterLibrary/textures/fit/makehuman/`).

*(Corrected 2026-09-24, Matter-Library#1. This rule used to read "a standard `inputs:` override on the bound material prim (or a `place2d` nodegraph input for UV)". It named the carrier but not the connection that makes it resolve, so every Creator tuning was invisible outside the one consumer that read the Material input with its own rule. Measured on OpenUSD 26.03 + MaterialX 1.39.5 with `usdrecord`: the unconnected override renders byte-identical to no override; connected with no value, byte-identical to no override; connected with a value, identical to setting the nodegraph input directly. No port name, type, op or range changed.)*

## Render-role texture nodes — assembler-owned node-name contract

The overlay/mask **textures** (distinct from their Creator-adjustable `overlay1_density`/`overlay2_density`/`overlay3_density`/`maskset_blend` *scalars* above) are **fixed per article** — only the blend amount is Creator-adjustable, the bitmap is not. They therefore are **NOT** material-level `inputs:` and are **NOT** in the Creator subset. MaterialX rejects extra inputs on the fixed `<surfacematerial>` nodedef (`sdk-validate` "Node interface error"), so a fixed texture path can only live **inside the nodegraph**, on an `<image>` node's `file` input. So that a consumer can find those paths, the producer (the [assembler](../Tooling/AuthoringHarness.md)) and every consumer agree on a **fixed render-role node name** per role:

| Render role | Nodegraph `<image>` node name (FROZEN) | Color space |
|---|---|---|
| Overlay 1 | `overlay1_tex` | **linear** (packed data) ⚠ *corrected* |
| Overlay 2 | `overlay2_tex` | **linear** (packed data) ⚠ *corrected* |
| Overlay 3 | `overlay3_tex` | **linear** (packed data) *(added 2026-09-25)* |
| Maskset | `maskset_tex` | linear (coverage mask) |

⚠ **Colour-space correction.** The overlay rows previously said **"sRGB (albedo)"**. That was wrong, and it contradicted the owning ontology: [MasterSet](../Ontology/MasterSet.md) defines an [overlay](../../Glossary.md) as a **packed data texture** (R/G = normal XY · B = roughness bias · A = mask density). Annotated as sRGB albedo, the assembler duly **mixed the overlay bitmap over base colour** — painting packed normal/roughness data on as if it were paint, and corrupting every channel through the sRGB transfer curve on the way in. **All three render-role textures are data and load `lin_rec709`.** Neither an overlay nor a [maskset](../../Glossary.md) may ever contribute colour — both are **modulators** ([MasterSet §Overlay/MaskSet model](../Ontology/MasterSet.md)).

*(Updated 2026-09-23, measured: every render-role `<image>` in the live articles — `overlay1_tex`/`overlay2_tex` in Concrete, Glass and Copper, `maskset_tex` in Glass, Copper and Rust — declares `colorspace="lin_rec709"`; overlays are `color4` (alpha = mask density), the maskset `color3`; the assembler's `DATA_COLORSPACE` is `lin_rec709`. `srgb_texture` appears only on base-colour albedo images.)*

**This is a spec correction, NOT a vocabulary reopen.** No Creator port name, type, op or range changes; the frozen interface-input vocabulary above is untouched. What changed is a **wrong colour-space annotation** on a texture-role table.

- **Producer:** `tools/converters/assemble_mtlx.py` emits these `<image>` nodes by these exact names (the contract pins them).
- **Consumer:** a consumer reads each named node's `inputs:file` from the bound material's nodegraph (`…/NG_<name>/<role>_tex`).
- These node names are **part of the LCD render contract**: renaming a render-role node is a cross-consumer break, the same discipline as the frozen interface-input names. The *blend* of each layer stays Creator-adjustable via its scalar port above; the *texture* is author-tier data.
- **Since Phase04 (2026-09-26) each of these nodes is a MaterialX `tiledimage`, not an `image`.** It carries two more fixed author-tier values beside `file`, and they are part of the render contract too: `realworldimagesize` (the layer's own size in metres, from its scale tag) and `realworldtilesize` (the article's `meters_per_tile`). A consumer that rebuilds layer sampling itself samples each layer at **UV × realworldtilesize ÷ realworldimagesize**, where UV is taken after the Creator's `place2d` ([MasterSet §Scale](../Ontology/MasterSet.md)). A USD/MaterialX viewer gets this from the stdlib `tiledimage` with no extra work. No Creator port, name, type or range changed. *(The IMRSV consumer's side is [PlatformDependencies](../../Planning/PlatformDependencies.md) P13.)*

*Consumer-side (IMRSV): how IMRSV's material extractor carries the three render-role texture paths (and any material-prim `inputs:<role>_texture` override that takes precedence) to its renderer — see [Consumers](../Consumers.md).*

> **Drift (2026-09-23):** under R14 the render-role names, the Creator port vocabulary and the author-tier carriers are published **as data** in each release (the [master contract](../../Glossary.md), *(planned)*), not only as this document — owned by the release-bundle / consumer-contract phase (R14).

## Status

**Creator subset: FROZEN — names/types/ops + ranges/defaults.** The interface-input port vocabulary **and** its value ranges/defaults are frozen as the cross-consumer contract, confirmed empirically by authoring the 7-article proof subset. No wire/ABI contract is frozen here. The **carrier** (how an override is authored so it resolves) was corrected on 2026-09-24 without reopening the vocabulary: see [§Carrier rule](#carrier-rule-no-imrsv-attrs).

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
- 2026-09-24: the Carrier rule was corrected to require the connection from the article's nodegraph (Matter-Library#1), after a generic USD viewer showed every Creator tuning was inert outside the one consumer that read the Material input directly. In the same change, the UV ports were stated as MaterialX `place2d` semantics and the articles began clamping the biased roughness to [0, 1], both on lead rulings that the article's MaterialX meaning is the contract every consumer matches. No port name, type, op or range changed.
- 2026-09-27: the optional lane-A carriers coat, fuzz and scatter anisotropy were added to the author tier (Phase07 step 7.3), for skin. Additive: every existing article assembles byte-identically, and the Creator vocabulary is untouched.
- 2026-09-27: for hair (Phase07 step 7.6), the lane-A carrier specular anisotropy (C3) and the Masked lane-B input `cutout_map` were added: the mesh's cut-out, supplied at binding through the Carrier rule. Additive in the same way.
- 2026-09-28: the `Hair` master (Phase08 step 8.1) takes Masked's carriers unchanged, `cutout_map` included. No port, name, type or range moved.
- 2026-09-28 (the same step, reworked): `Hair` takes `cutout_map` as soft coverage and **no `opacity_cutoff`**, and carries thin-walled translucency on lane A (`geometry_thin_walled`, `subsurface_weight`, `subsurface_scatter_anisotropy`, and `subsurface_color` connected to `base_color_out`). No Creator port, name, type or range moved.
- 2026-09-28: the rule that a mesh's UV unit is the article's tile, and the `uv_scale` formula for a mesh that breaks it, were written down (Phase08 F-P08-8). A skin on MakeHuman's raw atlas had rendered its pores as large furrows in the platform's Studio and in a Blender probe. No port, name, type or range moved.
- 2026-09-30: the lane-B input `base_color_map` (Phase09 step 9.1): the mesh's picture, supplied at binding and multiplied into the base colour, on Opaque, Masked, Hair and Subsurface ([§Base colour map](#base-colour-map-the-meshs-picture-supplied-at-binding)); and `specular_weight` on lane A, authored only when set (card hair: 0, matte). No Creator port, name, type or range moved.
- 2026-10-05: the `geometry_thin_walled` note gained a pointer to the consumer rule, which MasterSet owns (a thin-walled article does not deflect the view; a solid one bends it). The platform's Unreal app had carried the flag and bent thin glass anyway. No port, name, type or range moved.
