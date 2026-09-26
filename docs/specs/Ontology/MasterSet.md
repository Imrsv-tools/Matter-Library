# Matter Master Set — v1 baseline

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

The **master set** defines **what a Matter material can BE**. Under runtime-instanced masters, a Matter material is not arbitrary MaterialX node soup — it is a **template instance**: *"master X + these textures + these LCD parameter values."* The master set is therefore the **authoring contract**: a community contribution must "conform to a Matter template," caught at authoring/CI time, never discovered at runtime.

This spec is the **producer side** of the master contract: the masters, their tokens, how an article's master is chosen, the overlay/maskset model, the blend formula and each master's settings intent. How a given consumer implements a master (its asset names, material settings enums, instance model, wire format) is consumer-side and lives in [Consumers](../Consumers.md).

> **Governing insight:** only **a renderer that partitions shader space forces the split.** Blender Principled BSDF and MaterialX `open_pbr_surface` are each one über-shader; with only those targets ONE master would suffice. Masters exist because **Unreal partitions shader space by blend mode / domain** (opaque vs masked vs translucent are different compiled graphs). So the set is *"how such a renderer forces us to partition OpenPBR space"* — every master is a **window onto the same canonical OpenPBR model**, which is what keeps cross-renderer [parity](../../Glossary.md) honest.

## v1 baseline = 7 masters + 1 system material

| Master (identity token) | Typical materials, by class (examples, not a routing rule; see [§Master resolution](#master-resolution--the-article-declares-its-master)) | Key extra params | Notes |
|-------------------------|---------------------------|------------------|-------|
| **Opaque** | stone, wood, soil, most mineral, metal, ceramic, cementitious, composite, plastic, polymer, coating, sand — **the ~85% workhorse** | anisotropy, sheen, clearcoat as optional Substrate slab features | brushed metal / velvet / glaze are *params*, not masters |
| **Masked** | textile (lace), perforated metal¹, vegetation | opacity cutoff; possible foliage variant (two-sided + thin transmission) | foliage variant open *(planned)* |
| **TranslucentThin** | window glass, resin, thin plastics | opacity, tint, IOR | thin-surface model; roughness blurs the transmitted view in every consumer (measured, IMRSV #88 RD-8) |
| **TranslucentThick** | gemstones (**Diamond**), liquids, thick glass | IOR, absorption color + depth | real-time refraction (e.g. Unreal) is approximated — parity bar is "close"; roughness blurs the transmitted view in every consumer (measured, IMRSV #88 RD-8) |
| **Subsurface** | **Marble**, jade, wax | SSS color, radius/MFP | Marble alone justifies it |
| **TwoLayer** *(retained)* | paint-on-wood, rust-on-metal | blend balance/contrast, mask controls | **retained as a distinct master**; the collapse-to-6 spike is waived — see [below](#twolayer--resolved-retained) |
| **Emissive** | emissive, virtual, energy (Utility) | emissive color, intensity | animated/procedural ("plasma") out of scope or pre-authored |
| **`IMRSV_MissingMaterial`** *(system — token `system`)* | — (rendered when a Matter identity can't resolve) | — | named-and-deliberate broken-material look; not a real matter master. Historical name kept |

*(Updated 2026-09-23, measured: `MatterLibrary/materials/utility/virtual/IMRSV_MissingMaterial.mtlx` declares `master_material = "system"` in its `imrsv_metadata`; it is magenta (`1.0, 0.0, 1.0`) and is `creator_selectable: false` in the `matterlib-0.1.0` catalog.)*

**Coverage: 19 of 20 taxonomy classes** *(was 18 of 19; `ceramic` added 2026-09-23)*. `atmospheric` (volume materials) is **out of scope** for prop-applied matter — owned by a future Volumes/Effector domain *(planned)* ([Taxonomy](Taxonomy.md)).

**Mapping sanity check.** Against the consumer's earlier keep-set (historical examples; only Glass and Diamond exist in this library — see [Catalog](../Catalog/Catalog.md) for the real articles): Glass→TranslucentThin · Diamond→TranslucentThick · White_Plastic/Gold_Foil/Brass→Opaque · Ceramic→Opaque(+coat). `Diamond` is the first material that doesn't fit TranslucentThin → it is exactly what justifies TranslucentThick; `Marble` justifies Subsurface.

*(Updated 2026-09-23, measured: every master now has at least one article in this repo, read off each `.mtlx`'s `imrsv_metadata.master_material`.)*

| Master token | Articles in `MatterLibrary/materials/` |
|---|---|
| `Opaque` | ABS_Matte · Limestone_Veined · Concrete_Smooth_Worn_Dusty · Copper_Verdigris_Aged · Diagnostic_UVGrid |
| `Masked` | Lace_Floral |
| `TranslucentThin` | Glass_Clear |
| `TranslucentThick` | Diamond_Brilliant |
| `Subsurface` | Marble_Veined_Polished |
| `TwoLayer` | Rust_OnSteel_Flaking |
| `Emissive` | Neon_Signage |
| `system` | IMRSV_MissingMaterial |

## Master tokens

The **canonical master token** used in the manifest / `imrsv_metadata` / name-keyed resolution is the bare identity. The v1 token set is closed:

`Opaque` · `Masked` · `TranslucentThin` · `TranslucentThick` · `Subsurface` · `TwoLayer` · `Emissive` · `system`

- A token is **data**, not an asset name. The Matter Library pins the *token*; each consumer maps token → its own asset. Adding a token is additive; removing or renaming one is a breaking master-contract change (library semver-**major**, see [_Architecture](../_Architecture.md) §Versioning).
- `system` is reserved for the system fallback (`IMRSV_MissingMaterial`); no matter article may declare it.

> **Reevaluate (2026-09-23) — proposed, not yet ruled:** the two rules above ("adding a token is additive; removing or renaming one is semver-major" and "`system` is reserved") were **written while bringing this spec home**. They follow from the Architecture's semver rule and from the live tree, but no one has ratified them, and no validator enforces the `system` reservation. Owned by the release-bundle / consumer-contract phase, which publishes the master contract as data.
- **Where the token lives today:** in each article's `.mtlx`, as `imrsv_metadata.master_material` (see [MaterialXTemplate](../Contract/MaterialXTemplate.md)). *(Updated 2026-09-23, measured: all 12 `.mtlx` files in `MatterLibrary/materials/` carry it; `tools/validators/validate_material.py` reads it for the master-conformance lane.)*
- **Master contract as data** *(planned)*: the per-article master token is carried in the release (runtime catalog / release bundle), so a consumer never derives it itself.

> **Drift (2026-09-23):** R14 has the release carry each article's master token, but the `matterlib-0.1.0` runtime catalog and manifest carry no master field today — owned by the release-bundle / consumer-contract phase (R14).

*Consumer-side (IMRSV): token → Unreal asset naming pin (`M_MasterMaterial_<Token>`) — see [Consumers](../Consumers.md).*

### Master resolution — the article declares its master

**Rule (lead, 2026-09-23):** a master is the LCD and texture structure for a **type of material**, not for a taxonomy class.
- **Every article declares the master that fits what the material physically is**, from the closed master set. Today it is carried as `imrsv_metadata.master_material` in the article's `.mtlx`. Under R14 it is also the per-article master token in release data.
- **The class gives only a typical default** (the "Typical materials" column above). It never overrides the article's declaration.
- **A consumer resolves an article's master from the article's own token, never from its class** (consumer side: [PlatformDependencies](../../Planning/PlatformDependencies.md) P4).
- **No new masters are needed for coverage.** Covering new matter means an article choosing one of the existing masters.

Examples where the material, not its class's typical master, decides: lace (textile) is **Masked**, while cotton and denim (textile) are **Opaque**; sapphire (mineral) is **TranslucentThick**; acrylic (plastic) is **TranslucentThin**; grass ground cover (vegetation) is **Opaque**, while a leaf card is **Masked**.

> **Superseded (2026-09-23), kept for history:** "A material identity resolves to a master by its **taxonomy class**, with **leaf-stem name exceptions** where a single material name is what justifies a whole master. The exceptions are not ad-hoc: the table above already argues masters *by material name* — *"`Marble` alone justifies it"*, *"`Diamond` … is exactly what justifies TranslucentThick"*. Those two are the precedent; the third follows it."
>
> Taken literally, class routing made every textile and vegetation article Masked, which the Masked conformance check would then fail for lacking a cut-out opacity source. Reaching real coverage would have needed dozens of name exceptions. The three exceptions below are kept as the original cases in which the material decided; under the rule above, each is simply an article declaring its master. (Evidence: `docs/Planning/Research/260923_R_AgenticMaterialGeneration.md` Passes 10 and 12.)

| Original exception (leaf stem) | Master | Why the class route was insufficient |
|---|---|---|
| `marble` | **Subsurface** | class `stone → Opaque`; marble is the material that justifies SSS |
| `diamond` | **TranslucentThick** | class `mineral → Opaque`; diamond is the material that justifies absorption+IOR |
| **`rust`** | **TwoLayer** | class `metal → Opaque`. **TwoLayer's own use case in this spec is rust-on-metal** (row 6) — yet without this exception no class and no exception routed to it, so the master was **unreachable**: it existed and nothing could ever bind it. A `rust`-stemmed identity in `engineered/metal` is exactly the article the master exists to serve. |

⚠ **Never add a taxonomy class to reach a master.** The article declares its master, so no class is ever needed for that. Classes are added when the *matter* needs them ([Taxonomy §Growth model](Taxonomy.md#growth-model)).

> **Superseded (2026-09-23), kept for history:** "**Adding a taxonomy *class* to serve one article is the wrong lever** — [Taxonomy](Taxonomy.md) is a closed 19-class ontology, and inventing a class so the code can find a master inverts the ontology to serve the implementation. The name-exception is the sanctioned mechanism, and it is why the existing ones exist."

*(Updated 2026-09-23, measured: the routing agrees with the articles — `Marble_Veined_Polished` (natural/stone) declares `Subsurface`, `Diamond_Brilliant` (natural/mineral) `TranslucentThick`, `Rust_OnSteel_Flaking` (engineered/metal) `TwoLayer`, while `Copper_Verdigris_Aged` in the same class declares `Opaque`.)*

> **Drift (2026-09-23):** the IMRSV consumer still routes by a class → master table compiled into its plugin, and ignores each article's declared token. R14 moves the per-article token into release data, and the consumer switches to it ([PlatformDependencies](../../Planning/PlatformDependencies.md) P4). Owned by the release-bundle / consumer-contract phase (R14).
>
> **Todo (2026-09-23):** nothing in this repo checks that an article's declared master fits its material. `tools/validators/validate_material.py` checks only that the declared master's defining carriers are present and wired. A plausibility check belongs to the authoring-harness work (research: `260923_R_AgenticMaterialGeneration.md` gap G4).

¹ **Perforated metal** declares **Masked** (it cuts holes), even though metal's typical master is Opaque. No such article exists yet *(planned)*.

> **Superseded (2026-09-23), kept for history:** "**`perforated metal` has no resolution route today** — class `metal → Opaque`, and no `Masked` name-exception serves it. … when a perforated-metal article is authored it needs a name-exception (the mechanism above), not a taxonomy change."

## TwoLayer — RESOLVED: retained

**Decision: TwoLayer is retained as a distinct master — the set stays at 7.** The full 7-master set — including both transparent masters (TranslucentThin + TranslucentThick) and TwoLayer — is a product requirement, so the collapse-to-6 GPU cost spike is **waived**. (A measured "stays 7" was always the intended non-change outcome; here it is settled by product requirement rather than by the cost measurement.)

*Historical rationale (why it was ever a swing):* TwoLayer was originally recorded as a **hypothesis** — *"stays a master unless overlay/mask plumbing covers paint-on-wood / rust-on-metal within the VR cost budget."* "Rust-on-metal" as *Opaque + rust MaskSet* and as a *TwoLayer master* are the same picture built two ways, and an overlay/mask cost spike could in principle have collapsed the set to 6. **That collapse is not taken.**

### TwoLayer is TWO REAL LAYERS

**What TwoLayer IS, normatively:** two visibly distinct **opaque** layers — a base and a second surface (rust, peeling paint) — with the **maskset choosing where the second layer sits** and blend controls shaping that boundary. Each layer carries its own **base colour · roughness · metalness · normal**.

**What TwoLayer is NOT:** a glossy varnish over a single surface (a clearcoat). That contradicts this spec twice over: row 1 lists clearcoat as an **Opaque *param*** (*"brushed metal / velvet / glaze are params, not masters"*), and [Implementation posture](#implementation-posture-v1) says a genuine clearcoat model would be a **separate `OpaqueCoat` graph**. **A clearcoat cannot render rust or peeling paint.** The spec is not weakened to preserve such a shortcut.

**Consequence for the master contract:** a consumer that does not evaluate the article's MaterialX graph directly must **rebuild the same blend the producer computed** — so the **layer-2 maps and the blend scalars are part of what an article hands to consumers** (the [TwoLayer blend](#twolayer-blend-v1) below is the formula both sides implement). This makes TwoLayer the largest parameter surface in the master set, a cost the product requirement accepts. The layer-2 carriers are tabled in [LCDSchema §Author tier](../Contract/LCDSchema.md).

> **Reevaluate (2026-09-23):** the "must rebuild the blend" consequence was argued against Unreal's legacy material model, which cannot render two BSDFs into one instance. Under Unreal Substrate (R15) a consumer may be able to express two slabs natively; the blend formula stays the contract either way.

*Consumer-side (IMRSV): how the layer-2 maps and blend scalars reach the Unreal render wire, and the resulting ABI cost — see [Consumers](../Consumers.md).*

## Overlay / MaskSet model

Layered surface effects without redundant textures. Each material may reference **≤1 mask layer** and **≤3 overlay layers** *(raised from 2 on 2026-09-25, lead: "smart, not lean" materials carry all relevant layers; `260925_R_LibraryCoverage_FirstRelease.md` C1/C2)* (the layered-materials marquee capability — e.g. a plastic with a dust layer + scratches).

| Type | Description | RGBA Layout |
|------|-------------|-------------|
| **Overlays** | tiling surface effects (dust, scratches, fingerprints) | R/G = Normal XY · B = Roughness bias · A = Mask density |
| **MaskSets** | multi-mask texture packs for blending (paint, rust, dust) | R/G/B/A = 4 material masks — **see the channel contract below** |

Overlay/mask **intensities are Creator-adjustable** — surfaced as the layered-material controls in the [LCD schema](../Contract/LCDSchema.md)'s Creator tier (`overlay1_density`, `overlay2_density`, `overlay3_density`, `maskset_blend`). Always-carried sampling has a shader cost even at intensity 0 — a cost measurement on the VR budget picks the strategy (accept / variants / dynamic branching).

> **Reevaluate (2026-09-23):** whether that cost measurement was ever run and which strategy it picked is not recorded in this repo; re-measure against the Substrate masters (R15) before relying on "accept".

### ⭐ Both are MODULATORS. Neither is ever albedo. *(normative)*

Both overlays and masksets are **data textures**: they may bend a normal, bias a roughness, or gate a layer — they may **never** contribute colour. Mixing either bitmap *over base colour* paints packed data on as if it were paint. A "did the pixels change?" check passes on that bug, so a gate for this rule must check *what* changed, not *whether* something did.

**MaskSet channel contract (v1).**

| Channel | Meaning (v1) |
|---|---|
| **R** | **layer-2 coverage** — drives the TwoLayer blend |
| **G** | **overlay-1 coverage gate** — *where* overlay 1 may appear |
| **B** | **overlay-2 coverage gate** — *where* overlay 2 may appear |
| **A** | **overlay-3 coverage gate** — *where* overlay 3 may appear *(since 2026-09-25; was "reserved (unused in v1)")*. The maskset loads as `color4` only on an article with 3 overlays, so ≤2-overlay articles are unchanged. |

`maskset_blend` (a frozen Creator port) is the **master strength** of the maskset's whole effect: `0` → the maskset does nothing; `1` → full effect. This gives the maskset a real, correct job on **every** master — not only TwoLayer — which is what makes the port live and semantically correct on an Opaque article that authors it (e.g. `Copper_Verdigris_Aged`).

**Overlay semantic (v1).** An overlay's own channels are already defined above (R/G = normal XY · B = roughness bias · A = mask density). Applied:

```
effect_N   = overlayN_density * overlayN_tex.A * lerp(1, maskset.<G|B|A>, maskset_blend)
normal    += (overlayN_tex.RG * 2 - 1) * effect_N        # then renormalize
roughness += overlayN_tex.B_bias       * effect_N
base_color: UNTOUCHED                                     # an overlay never tints
```

### TwoLayer blend (v1)

**Frozen here because the producer and every consumer that rebuilds it are implementations of ONE formula.** The `.mtlx` and a consumer's master graph (e.g. Unreal's) each compute this independently; if they diverge, the library render and the app render disagree and nothing catches it.

```
m = maskset.R                                   # linear, single channel
c = 1 / max(1e-4, 1 - layer_blend_contrast)     # contrast gain
k = saturate( (m - layer_blend_balance) * c + 0.5 )
t = k * maskset_blend                           # Creator master strength

out_channel = lerp(layer1_channel, layer2_channel, t)     # base colour / roughness / metalness
normal      = normalize( lerp(n1, n2, t) )                # decode BOTH to tangent space FIRST, then blend
```

**Defaults are chosen so the identity falls out:** `layer_blend_balance = 0.5`, `layer_blend_contrast = 0.0` ⇒ `c = 1`, `k = saturate(m)`, `t = m × maskset_blend`. At defaults the blend is exactly *"mask × maskset_blend"* — the plain, intuitive behavior — and balance/contrast are pure shaping on top.

### Scale — every layer is sampled at its OWN real-world size *(normative, Phase04, 2026-09-26)*

Overlays and masksets are **shared** textures with their own physical size, so a layer looks the same size on every article whatever the article's tile size:

- **A layer's size is its scale tag** ([Identity §Scale tags](Identity.md): metres per UV tile). A shared layer is authored at exactly that size; `sUKN` is not allowed on a layer.
- **An article's size is its `meters_per_tile`** (the recipe value, also carried in `imrsv_metadata`), not its coarser tag. An article that carries layers must have `meters_per_tile > 0`.
- **The layer's UV is the article's UV × (article size ÷ layer size)**, taken *after* the Creator's `place2d` (`uv_scale` / `uv_offset` / `uv_rotation`), so the Creator's UV controls still move the whole material together.
- **Producer form:** each layer render-role node is a MaterialX `tiledimage` with `realworldimagesize` = the layer's size and `realworldtilesize` = the article's `meters_per_tile`, fed from `uv_place` ([LCDSchema §Render-role texture nodes](../Contract/LCDSchema.md)). The per-article textures (base, layer 2, opacity) stay at the article's size.

*(Before Phase04 every layer tiled with the article's UVs, so its own tag had no effect: a 1 cm dust layer on a 1 m concrete was stretched 100x. The assembler enforces the two input rules above.)*

### Colour space — overlays and masksets are LINEAR

⚠ **Overlay and maskset textures load LINEAR (`lin_rec709`), never `srgb_texture`.** They are data, not colour. Loading a packed data texture through an sRGB transfer curve corrupts every channel it carries. [LCDSchema](../Contract/LCDSchema.md)'s render-role table follows this rule.

*(Updated 2026-09-23, measured: every `overlay1_tex`, `overlay2_tex` and `maskset_tex` node in `MatterLibrary/materials/` — Concrete, Glass, Copper, Rust — is `colorspace="lin_rec709"`; base-colour images, including Rust's `layer2_base_color_tex`, stay `srgb_texture`.)*

## ⭐ Material-settings intent — a master is a GRAPH **plus** a SETTINGS block *(normative)*

**Why this table exists.** Everything above specifies the master's *graph*. But a master, in any renderer that partitions shader space, is a graph **and** a set of **material settings** — coverage / blend, shading model, two-sidedness, refraction. Unowned settings cannot drift *against* a spec because there is no spec to drift against; they ship correct by inheritance, with nothing holding them there. This table owns them, renderer-neutrally.

**These are not taste. Coverage mode is the master's reason to exist** — per the governing insight above, a partitioning renderer splits shader space by blend mode / domain. A Masked master that does not alpha-test **is not the Masked master**.

| Master | Coverage (blend) | Shading model | Two-sided | Refraction |
|---|---|---|---|---|
| **Opaque** | opaque | default lit | no | none |
| **Masked** | masked (alpha-tested at the cutoff) | default lit | **yes** | none |
| **TranslucentThin** | translucent | default lit | **yes** | **index of refraction** |
| **TranslucentThick** | translucent | default lit | **yes** | **index of refraction** |
| **Subsurface** | opaque | **subsurface** | no | none |
| **TwoLayer** | opaque | **default lit** (two opaque layers, never a clearcoat model) | no | none |
| **Emissive** | opaque | default lit | no | none |

**Notes on the non-obvious cells:**
- **The subsurface shading model on Subsurface is load-bearing** — without it the subsurface colour is inert and Marble cannot bleed at all. It is the shading model, not the graph, that makes the master scatter.
- **Default lit on TwoLayer** — a clearcoat shading model is not this master (see [TwoLayer is two real layers](#twolayer-is-two-real-layers)); a clearcoat cannot render rust.
- **Two-sided on Masked / TranslucentThin / TranslucentThick** is a property **of the master**, not driven per-prim. At least one partitioning renderer (Unreal) cannot vary two-sidedness per material instance — it is a static shader property — so a per-prim two-sided value has nowhere to land on these three. **Trade accepted:** per-prim two-sidedness is lost on exactly the three masters where two-sidedness is *semantically non-negotiable* — a lattice with holes; seeing the far face through glass or a gem. The alternative (pre-baked one-sided/two-sided variants, 7 → 14 masters) was rejected as a poor trade.
- **Roughness on TranslucentThin / TranslucentThick blurs what is seen through the surface** (rough transmission), not only the specular highlight. A consumer whose real-time refraction approximates this must still blur the transmitted view by roughness; how it does so is consumer-side (see [Consumers](../Consumers.md)). The two renderers measured so far change by different mechanisms (a blurred background vs a milky surface), so parity here is judged by eye, not by a pixel ratio.
- **This intent ships as part of the master contract** *(planned, R14)*, so each consumer maps it to its native settings and gates its masters against it. **This table and each consumer's settings gate must move together.**

*Consumer-side (IMRSV): the Unreal realisation of this table (`BLEND_*` / `MSM_*` / `RM_*` values per `M_MasterMaterial_<Token>`) and the gate that asserts it on the cooked assets — see [Consumers](../Consumers.md).*

### Opacity floor — an article states its honest physics; the MASTER survives it *(normative)*

A translucent master that derives coverage as `Opacity = Opacity × (1 − Transmission)` turns an article authoring the physically-honest `transmission = 1.0` (a diamond genuinely transmits ~all light) into opacity of **exactly zero** — the surface disappears, taking its own specular highlights and roughness response with it.

**The fix belongs in the master, not the article.** The translucent masters clamp to **`MIN_TRANSMISSIVE_OPACITY = 0.05`**, so a fully-transmissive article still presents a surface to shade. Every consumer implementation of TranslucentThin / TranslucentThick honours the same floor.

**The rule this encodes:** an article must be free to state its true physics. A master that cannot survive an honest value is the defect — **never fudge the article to protect the master.** (Glass's `transmission = 0.95` predates this and began as exactly such a fudge; with the floor in place it is retained only as an *appearance* choice — a window is not 100% transmissive — and is no longer load-bearing anywhere.)

*(Updated 2026-09-23, measured: `Diamond_Brilliant_Clean_Base_s01_v01.mtlx` authors `transmission_weight = 1.0`; `Glass_Clear_Clean_Base_s01_v01.mtlx` authors `0.95`.)*

## Implementation posture (v1)

- **Legacy material model, not Substrate, for v1:** Substrate's VR story is bad in the 5.6/5.7 window (instanced-stereo + MSAA bugs); the **master contract — names, params, LCD mapping — is the stable artifact**, the implementation swaps later. Legacy shading models (clearcoat/SSS/cloth) may cost **1–2 extra master *graphs*** (e.g. an OpaqueCoat) at *implementation* time — that is an implementation-time master-graph count, **not** a change to this authoring-taxonomy count of 7.

  > **Drift (2026-09-23):** the Unreal target is now 5.8+ with Substrate and Blender 5.1+, which retires "legacy model for v1"; the master contract targets Substrate and parity baselines must measure the Substrate result. The contract-is-the-stable-artifact principle is unchanged — owned by the release-bundle / consumer-contract phase (R15).

- **Runtime-instanced, not baked-per-material:** a consumer carries only the masters (tiny, zero textures, coupled to the LCD schema — they ARE the integration contract); every Matter material is then **data** (master token + LCD params + textures from the release), so the per-material renderer half is derived data and drift is structurally impossible.

  > **Drift (2026-09-23):** this repo is a separate producer; consumers use published releases, never the checkout. This repo ships the release bundle plus the master contract as data, a consumer instantiates at runtime, and an optional reference Unreal masters package *(planned)* may follow — owned by the release-bundle / consumer-contract phase (R1, R14).

*Consumer-side (IMRSV): the Unreal masters' plugin packaging, instance model and wire/ABI consequences — see [Consumers](../Consumers.md).*

## Status

**Baseline chosen.** 7 masters + `IMRSV_MissingMaterial` (token `system`). The master set + its param schemas **is** the producer↔consumer integration contract.

**TwoLayer retained** — the set stays at 7; the collapse-to-6 spike is waived by product decision.

**The author tier is specified**, with these parts owned here:
1. **TwoLayer = two real layers**, not a clearcoat — and the layer-2 maps + blend scalars are part of the contract.
2. **The MaskSet channel contract** (R = layer-2 coverage · G/B = overlay gates · A reserved).
3. **Overlays and masksets are MODULATORS, never albedo**, and load **linear**, never sRGB.
4. **The `rust → TwoLayer` name exception**, without which the TwoLayer master is unreachable. *(Superseded 2026-09-23: articles declare their master, so a rust-on-metal article declares TwoLayer and no exception is needed; see §Master resolution.)*
5. **The material-settings intent** per master (coverage · shading model · two-sided · refraction).
6. **The opacity floor** (`MIN_TRANSMISSIVE_OPACITY = 0.05`) as a normative part of the translucent contract.

The per-master **author-tier** carriers (the values that make each master *be* that master) are tabled in [LCDSchema §Author tier](../Contract/LCDSchema.md); the Creator-adjustable vocabulary stays **FROZEN and unchanged**. Each master has a real, Creator-selectable example article in this repo (table [above](#v1-baseline--7-masters--1-system-material)).

## History

- 2026-06 — the v1 baseline of 7 masters plus the system missing-material was chosen, replacing an earlier 5-master set; TranslucentThick (justified by Diamond) and Subsurface (justified by Marble) were the additions.
- 2026-07 — TwoLayer was retained as a distinct master by product decision, and the planned collapse-to-6 cost spike was waived.
- 2026-07 — the first TwoLayer master implementation was built as a clearcoat over a single surface. It could not render rust or peeling paint, so it was ruled a defect and TwoLayer was specified as two real opaque layers.
- 2026-07 — the assembler, lacking a written maskset channel contract, invented one and mixed maskset and overlay bitmaps over base colour. A "did the pixels change?" check passed on that bug. The fix wrote the channel contract and the modulator rule down.
- 2026-07 — overlays had been annotated as sRGB albedo in the render-role table. That was corrected: overlays and masksets are data, loaded linear.
- 2026-07 — the TwoLayer master was found unreachable: no class and no name exception routed to it. The `rust` name exception was added.
- 2026-07 — no spec owned the masters' material settings. A refractive master shipped with refraction off, and the Masked master shipped one-sided; the one-sided master was caught by eye after every headless gate had passed. The settings table was written so the settings have something to be held against.
- 2026-07 — Diamond, authored with an honest `transmission = 1.0`, rendered as a black/clear mirror with dead roughness because opacity went to zero. The opacity floor was added to the translucent masters, not to the article.
- 2026-07 — all seven masters were shown rendering their defining behaviour in a consumer, each with a real Creator-selectable example article.
- 2026-09-23 — master resolution changed from class routing with name exceptions to "the article declares its master; the class is a typical default" (lead). A master is the structure for a type of material. Class routing would have made ordinary fabrics Masked, and full coverage would have needed dozens of exceptions. No master was added or changed.
- 2026-09-24 — translucent roughness parity was measured in a consumer (IMRSV #88 RD-8) and accepted on eyes-on: roughness visibly frosts Glass and Diamond in both a stock USD viewer and Unreal, in the same direction. The translucent rows and settings notes now say so.
