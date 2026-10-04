# Research — Thin-walled glass: what the platform saw in Unreal, and what it asks of the library

**Opened:** 2026-10-05 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `TG` (ids `TG-Qn`, `TG-Fn`). **Pass 1** is written from the platform's side. The library's review of it against its own tree is a later pass, as in `261004_R_PlatformSetMaterialAsks.md`.
**Requested by:** the IMRSV platform's work on how Matter materials look in its Unreal app. The platform is about to correct its own thin see-through master, ahead of adopting the library's masters (`PlatformDependencies.md` P20). The lead asked that the correction come back here (lead, 2026-10-05, verbatim: *"that need to get fed back to the library... we don't want a rouge material"*).

**Question:** what must every consumer draw for a thin-walled see-through article, and do the library's own Unreal masters draw it?

**Extends, does not replace:** `PlatformDependencies.md` P20 (*"What Studio finds comes back as an ask in this file"*) · `docs/specs/Ontology/MasterSet.md` (the TranslucentThin and TranslucentThick rows, the settings table, §Opacity floor) · `docs/specs/Contract/LCDSchema.md` §Author tier (`geometry_thin_walled`) · `Phases/Complete/Phase06_UnrealTestRuntime.md` (the open refraction item carried from 6.4).

**Public-repo note.** The platform's planning is private. It is summarised here by what it found and what it needs — no platform paths, code or ruling ids. Engine file names below are Unreal Engine 5.8's own.

**Measured at:** `387bd45` (2026-10-05).

---

## The short version

- **A thin-walled article must not shift what is seen through it, at any angle.** That is OpenPBR's own wording for thin-walled mode. The library's contract names the flag and does not say what a consumer must draw for it.
- **The platform's Unreal app got this wrong, and it showed only from the side.** Clear glass on a cube looked right head-on and bent the scene behind it "like a prism" at an angle. Its thin master and its solid master bend alike.
- **In Unreal the bend and the rough blur are separate.** The bend can be removed alone; the frosted blur stays. Unreal's "thin surface" switch does not remove it.
- **The platform will fix its own thin master on that basis.** This doc is so the same rule lands in the library's contract and its Unreal masters, and the two do not drift apart.
- **Three questions for the library's Unreal masters** follow from the same reading: whether its thin master bends in a live view, why its solid master bends nothing in its pictures, and whether its rig can show either.

---

## Pass 1 — What the platform found

*Written from the platform's side, 2026-10-05.*

### What "right" is

- **TG-F1 — OpenPBR says a thin wall does not deflect.** Its §Thin-walled mode treats the base as *"an infinitesimally thin sheet of dielectric"* that produces *"a reflected lobe and un-deflected refracted lobe"*, and calls it the convenient way *"to render windows"*. Six of the library's nine see-through articles are thin-walled: `Glass_Clear`, `Glass_Green`, `Glass_Frosted`, `Glass_Reeded`, `Acrylic_Clear`, `Cornea_Clear`. Three are solid: `LeadCrystal_Clear`, `Sapphire_Natural`, `Diamond_Brilliant`.
- **TG-F2 — The library's contract stops at the producer.** `LCDSchema.md` calls `geometry_thin_walled` *"the OpenPBR thin-vs-thick discriminator … at the producer"*; `MasterSet.md` calls TranslucentThin a *"thin-surface model"* and gives both masters the same settings row (refraction: index of refraction). Neither says what a consumer draws differently for thin.
- **TG-F3 — Of the three tools, only Blender shows the difference.** On the library's own test scene, defaults: through `Glass_Clear` the wall's grid runs straight through the ball and the cube; through `Diamond_Brilliant` the ball inverts the wall and the cube displaces it. Storm bends nothing for either. The library's Unreal pictures bend nothing for either (its own open item for diamond).

### What the platform's Unreal app did

- **TG-F4 — Thin glass bent, and only an angled view showed it.** `Glass_Clear` on a 2 m cube with a patterned object behind it, in a live view: straight through, fine; from the side, the scene behind shifts like a prism. `Diamond_Brilliant` on the same cube bends far more. The article's values arrived as authored (index 1.52, thin-walled true; index 2.417, thin-walled false). The app's thin and solid masters wire the article's index into Unreal's refraction the same way, and nothing consumed the thin-walled flag.
- **TG-F5 — A ball hides this, and a head-on flat face hides it too.** On a ball the bend is everywhere, so a thin glass and a gem look alike. On a flat face seen head-on there is no bend at all. A flat face seen at an angle is the view that separates the two.

### What Unreal 5.8 does (read from the engine source; not yet run)

- **TG-F6 — The bend is a screen shift of the surface's view-space direction times (index − 1).** `Shaders/Private/DistortionCommon.ush`, the index-of-refraction branch. Head-on, a flat face has no sideways direction, so nothing shifts. This matches TG-F4 exactly.
- **TG-F7 — The rough blur is a separate channel, written from roughness alone.** `Shaders/Private/DistortAccumulatePS.usf` writes a variance beside the shift; on the Substrate path it is written even when the shift is zero, and `DistortApplyScreenPS.usf` blurs by it. So **an index of 1.0 on the Refraction input removes the bend at every angle and keeps the frosted blur.**
- **TG-F8 — Turning the refraction method off loses the blur.** A translucent material whose method is "none" is not drawn in the distortion pass at all (`Materials/Material.cpp`, `bUsesDistortion`).
- **TG-F9 — "Is Thin Surface" does not touch the bend.** Nothing in the three distortion shaders reads it. It changes how transmittance and subsurface are evaluated for a Substrate slab.

### The asks

| # | Need | Why |
|---|---|---|
| A1 | **The contract says what a consumer draws for thin-walled:** the view through a thin-walled article is not deflected at any angle; its roughness still blurs that view; a solid article bends by its index. In `LCDSchema.md` §Author tier or `MasterSet.md`, wherever the library keeps consumer obligations. | Today a consumer can carry the flag, ignore it, and conform. The platform's app did. |
| A2 | **The library's Unreal TranslucentThin master is checked from the side, in a live view.** `build_masters.py` connects the refraction output and sets index-of-refraction for both see-through masters alike, and marks the thin one a thin surface. By TG-F9 that mark does not remove the bend; whether Epic's OpenPBR function returns an index of 1 for a thin wall is not visible from the script. | If it bends, the masters the platform is to adopt carry the same fault it is about to fix in its own. |
| A3 | **The solid master's "bends nothing" is run to ground** (the item carried from Phase06 6.4, and the 2026-10-02 notes on diamond and lead crystal). A classic translucent master with the same refraction method and the article's index bends visibly in the platform's live view (TG-F4). The library's pictures come from a scene capture; whether that capture includes Unreal's distortion pass is the first place to look. | Otherwise the Unreal column cannot judge any see-through article's bend, thin or solid — and a consumer adopting the solid master may lose a bend it has today. |
| A4 | **The rig gives see-through articles a view that can show bend:** a flat face seen at an angle, with the wall behind it (TG-F5). | The wide and close views look at the cube nearly head-on. |
| A5 | **The Blender driver falls back to CPU when a listed graphics device cannot render.** It falls back only when no device is listed. On the platform's machine a CUDA device is listed and its kernels cannot be built, so the driver fails; forced to CPU it renders an article's defaults in about seven seconds. | Blender is the one column that shows bending (TG-F3), and it was not run on that machine for any scorecard. |

### Questions for the library

- **TG-Q1 —** Does the library's Unreal thin master shift the view from the side today (A2)?
- **TG-Q2 —** Is the solid master's missing bend the master, or the capture (A3)?
- **TG-Q3 —** Where does the consumer rule of A1 live — the schema, the master set, or `Consumers.md`?
- **TG-Q4 —** For a thin-walled article, should a consumer's reflection still use the article's index (OpenPBR keeps the Fresnel), with only the transmitted view un-deflected? The platform assumes yes.

### A suggested ledger row (the library authors it, or not)

> **Thin-walled see-through articles are drawn un-deflected by every consumer** (the platform's finding, 2026-10-05). The platform corrects its own thin see-through master first — no shift at any angle, the rough blur kept — and takes the library's masters under P20 once the library's thin master is shown to do the same and its solid master is shown to bend. The rule itself belongs in the library's contract (A1). Owner: Matter Library (the contract; the Unreal masters; the rig) · the platform's Unreal plugin (its own master until P20). Pairs with P20 · *Unreal Reference Masters*.

---

## Status

- **Passes captured:** 1 (the platform's side).
- **Asks:** A1 – A5, all open. **Questions:** TG-Q1 – TG-Q4, all open.
- **What was added, and what was not.** This doc only. No article, master, tool, spec or ledger row is changed by it.
- **Not run:** TG-F6 – TG-F9 are read from the engine source; the platform's corrected master has not been built or seen. TG-F3's Blender pictures are for the shape of light only — that machine's Blender colour setup does not load.

▶ **Next:** the library reviews Pass 1 against its tree — A2 and A3 first, since they decide whether its Unreal masters can be adopted as they stand — and records the ledger row or declines it.
