# Research — Thin-walled glass: what the platform saw in Unreal, and what it asks of the library

**Opened:** 2026-10-05 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `TG` (ids `TG-Qn`, `TG-Fn`). **Pass 1** is written from the platform's side. The library's review of it against its own tree is a later pass, as in `261004_R_PlatformSetMaterialAsks.md`.
**Requested by:** the IMRSV platform's work on how Matter materials look in its Unreal app. The platform is about to correct its own thin see-through master, ahead of adopting the library's masters (`PlatformDependencies.md` P20). The lead asked that the correction come back here (lead, 2026-10-05, verbatim: *"that need to get fed back to the library... we don't want a rouge material"*).

**Question:** what must every consumer draw for a thin-walled see-through article, and do the library's own Unreal masters draw it?

**Extends, does not replace:** `PlatformDependencies.md` P20 (*"What Studio finds comes back as an ask in this file"*) · `docs/specs/Ontology/MasterSet.md` (the TranslucentThin and TranslucentThick rows, the settings table, §Opacity floor) · `docs/specs/Contract/LCDSchema.md` §Author tier (`geometry_thin_walled`) · `Phases/Complete/Phase06_UnrealTestRuntime.md` (the open refraction item carried from 6.4).

**Public-repo note.** The platform's planning is private. It is summarised here by what it found and what it needs — no platform paths, code or ruling ids. Engine file names below are Unreal Engine 5.8's own.

**Measured at:** `387bd45` (2026-10-05). **Pass 2** (the library's side) is measured at `c70e32e` (2026-10-05).

---

## The short version

- **A thin-walled article must not shift what is seen through it, at any angle.** That is OpenPBR's own wording for thin-walled mode. The library's contract names the flag and does not say what a consumer must draw for it.
- **The platform's Unreal app got this wrong, and it showed only from the side.** Clear glass on a cube looked right head-on and bent the scene behind it "like a prism" at an angle. Its thin master and its solid master bend alike.
- **In Unreal the bend and the rough blur are separate.** The bend can be removed alone; the frosted blur stays. Unreal's "thin surface" switch does not remove it.
- **The platform will fix its own thin master on that basis.** This doc is so the same rule lands in the library's contract and its Unreal masters, and the two do not drift apart.
- **Three questions for the library's Unreal masters** follow from the same reading: whether its thin master bends in a live view, why its solid master bends nothing in its pictures, and whether its rig can show either.
- **Update 2026-10-05 (Pass 2, the library's side):** in the library's Unreal pictures **neither** see-through master shifts the wall, measured to the pixel, while frosted glass does blur it. The two masters are wired alike, so whatever removes the bend is common to both. That leaves three possible states, and in two of them one master is wrong; one throwaway master on the machine with Unreal decides which. The rule itself (A1) has a home in `MasterSet.md`, whose settings table today gives thin and solid the same refraction cell. A5 is confirmed as described. Nothing was built or changed.
- **Update 2026-10-05 (after Pass 2): the rule is written.** At the lead's word, a quick fix put it into `MasterSet.md` §Material-settings intent and recorded the ledger row, `PlatformDependencies.md` M6 (§Resolved). The masters, the rig and the Blender driver are unchanged.

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

## Pass 2 — The library's review: what its own pictures and code show

*Written from the library's side, 2026-10-05, at `c70e32e`. This machine has no Unreal install: the pinned packaged runtime (`unreal-runtime-v3`) is here; the engine, its source and its editor are not.*

**Examined:** `unreal/MatterRuntime/Scripts/build_masters.py` (the two see-through masters) · `unreal/MatterRuntime/Source/MatterRuntime/MatterRuntimeGameMode.cpp` (the capture) and `Config/DefaultEngine.ini` · `tools/parity/drivers/unreal.py`, `drivers/blender_render.py`, `scene/build_scene.py`, `job.py` · the rig's stored pictures of `Glass_Clear`, `Glass_Frosted`, `LeadCrystal_Clear` and `Diamond_Brilliant`, made 1 – 2 October · `MasterSet.md`, `LCDSchema.md`, `Consumers.md`, `PlatformDependencies.md` P20 · Phase06's log (6.4 and the close) · Phase11's findings and batch summaries · `docs/Learnings/Unreal/Unreal.md` · MaterialX 1.39.5's own `open_pbr_surface.mtlx` in the pinned toolchain.

**Not examined, and not run:** the engine source. TG-F6 – TG-F9 stay the platform's reading; nothing here checks them directly. No picture was rendered for this pass: every measurement below is on pictures the rig had already made.

### Findings

- **TG-F1 holds.** Six articles declare `TranslucentThin` and three `TranslucentThick`, the nine Pass 1 names.
- **TG-F10 — In the library's Unreal pictures neither see-through master shifts the wall, at any angle the ball offers.** The wall's vertical grid lines, where they cross the ball in the wide view (512 px, rows 206 – 226), fall at these columns:

  | Article (index, master) | Storm (cannot refract) | Unreal | Blender |
  |---|---|---|---|
  | `Glass_Clear` (1.52, thin) | 131 · 166 · 200 | 131 · 166 · 200 | 131 · 166 · 200 |
  | `LeadCrystal_Clear` (solid) | 131 · 166 · 200 | 131 · 166 · 200 | 138 · 170 · 199 |
  | `Diamond_Brilliant` (2.417, solid) | 200 (the others too faint to find) | 131 · 166 · 200 | 181 (one line, the wall inverted) |

  Unreal's lines sit exactly where Storm's do, for the thin article and for both solid ones. Blender leaves the thin article's lines in place and moves the solid ones. A ball shows every angle from head-on to grazing, so this is not the head-on blind spot of TG-F5. *(A fourth peak at 180 on `Glass_Clear`, in all three tools alike, is the sun's glint on the ball. The script is under §Reproduction.)* The Unreal job files show the index reached the master as authored (`specular_ior` 2.417 on Diamond).
- **TG-F11 — So in the library's pictures the thin master already does what A1 asks:** no shift, and the rough blur kept. `Glass_Frosted` in Unreal is drawn with the wall blurred to nothing through it (looked at; batch `261002-2` says the same). **That is the capture, not a live view.** The runtime draws only through one scene capture, so nothing on this machine can show the masters live.
- **TG-F12 — The two masters are wired alike, as A2 reads.** In `build_masters.py` both take Epic's `MF_Substrate_OpenPBR_Translucent`, connect its `Refraction (IOR)` output to the material's Refraction input, and set the index-of-refraction method, per-pixel surface lighting, coloured transmittance and two-sided. They differ in two things only: the constant fed to the function's `geometry_thin_walled` input (1 or 0), and `is_thin_surface` on the thin one. Since neither bends, **whatever removes the bend is common to both, and is not the thin flag.**
- **TG-F13 — Nothing in the runtime turns the bend off.** The capture's source is linear scene colour. The show flags it clears are ambient occlusion, screen-space and Lumen reflections, Lumen global illumination, shadows, fog, atmosphere, bloom, motion blur, eye adaptation and anti-aliasing. None is refraction, distortion or translucency, and `DefaultEngine.ini` sets no refraction variable. Whether a scene capture drops the shift by an engine default is not readable here.
- **TG-F14 — The frost in the capture moves A3's first suspect.** A3 says to look first at whether the capture includes Unreal's distortion pass. By TG-F7 the rough blur is drawn in that same pass. The library's capture draws the blur (TG-F11). If TG-F7 is right, the capture does run the pass and the shift it writes is zero, which points at **what reaches the Refraction input** (the output of Epic's function), not at the capture. This rests on TG-F7, which is read and not run.
- **TG-F15 — Three states fit what is measured, and two of them leave one master wrong.**

  | What Epic's function hands the Refraction input | What the capture does with the shift | Thin master, live | Solid master, live | The rig's Unreal column |
  |---|---|---|---|---|
  | index 1, whatever the flag | draws it | right: no shift | **wrong: bends nothing** | truthful |
  | the article's index, whatever the flag | drops it | **wrong: bends like a solid**, the platform's own fault | right | blind to bend |
  | 1 for thin, the index for solid | drops it | right | right | blind to bend |

  TG-F14 leans to the first row. The platform's live bend (TG-F4) does not pick a row: its master is a classic graph that wires the index itself **and** it was seen live, so two things differ from the library's pictures at once.
- **TG-F16 — The contract's settings table gives thin and solid the same refraction cell.** `MasterSet.md` §Material-settings intent: TranslucentThin *"index of refraction"*, TranslucentThick *"index of refraction"*. Read as written, it tells a consumer to bend thin glass, and the platform's app did exactly that. The table calls itself the owner of each master's settings, renderer-neutrally, and the two rules beside it already bind *"every consumer"* (the opacity floor; roughness blurs the transmitted view). The library's own practice already assumes no bend: Phase11's F-P11-16 (*"a thin-walled pane … cannot refract"*), the batch notes (*"the wall seen through it is undistorted"* in all three tools), and Blender's master, which turns the Principled shader's Thin Wall on.
- **TG-F17 — The index still sets the reflection of a thin-walled article, in MaterialX's own graph and in both library masters.** In `open_pbr_surface.mtlx` the reflection lobe and the transmission lobe both take the index from `specular_ior`, whatever the flag. `geometry_thin_walled` switches the subsurface lobe and is handed to the surface constructor; it does not touch the index. The Unreal masters pass `specular_ior` to Epic's function on both see-through masters, and Blender's link the index with Thin Wall on.
- **TG-F18 — The rig's views, measured.** The close view sees the cube's front face about 24° off its normal (pitch −20.2°, yaw −12.5°), so it is not head-on, but it is not steep. The ball in the wide view was enough to show *no bend* (TG-F10). What a ball cannot do is tell thin from solid in a renderer that bends both (TG-F5); a flat face at a steep angle can. `job.py` already adds a view per master (the dim view for Emissive), so there is a shape for one. **Until TG-Q2 is settled the Unreal column shows no bend from any view,** so A4 follows A3.
- **TG-F19 — A5 is as described.** `blender_render.py` `_gpu()` returns a device kind as soon as one device of that kind is listed, and never tests that it can render. It reaches CPU only when no OptiX or CUDA device is listed at all.
- **TG-F20 — The rule narrows an open library item.** F-P11-16 records that reeded, fluted or hammered glass needs refraction through a pane, *"a thick master on a thin mesh, or a new input"*. `Glass_Reeded` is one of the six thin articles. Once A1 is written, *"thin never deflects"* is a rule, so textured see-through glass cannot be reached on TranslucentThin by any consumer. That is F-P11-16's contract work, unchanged in size, with one of its two routes closed.

### Reproduction (TG-F10)

The pictures are git-ignored; `uv run tools/parity/rig.py <article>` makes them.

```python
# uv run python <this>, from the repo root
import numpy as np
from PIL import Image
P = "library/parity/{a}/{t}/defaults.png"
ARTS = ["Glass_Clear_Clean_Base_s01_v01", "LeadCrystal_Clear_Clean_Base_s01_v01",
        "Diamond_Brilliant_Clean_Base_s01_v01"]
def peaks(a, t, rows=(206, 226), xs=(118, 220)):
    im = np.asarray(Image.open(P.format(a=a, t=t)).convert("RGB"), dtype=float)
    prof = im[rows[0]:rows[1]].min(axis=2).mean(axis=0)   # a white line is high in every channel
    return [x for x in range(*xs)
            if prof[x] == prof[x-3:x+4].max() and prof[x] - np.median(prof[x-8:x+9]) > 12]
for a in ARTS:
    for t in ("storm", "unreal", "blender"):
        print(a, t, peaks(a, t))
```

### The asks, as the library finds them

| # | State after this pass |
|---|---|
| A1 | **Written 2026-10-05 (§Resolved, TG-RD1).** *Was, at Pass 2:* **Agreed, not written.** The rule is OpenPBR's and the library's Blender master and its Storm pictures already follow it. Its home is `MasterSet.md` §Material-settings intent (TG-F16): the TranslucentThin row's refraction cell, and a note beside the rough-transmission one. `LCDSchema.md`'s *"at the producer"* line would point there. A contract edit is not research's to make. |
| A2 | **Half answered.** In the capture the thin master does not shift (TG-F10). In a live view: not run, and it cannot be on this machine. |
| A3 | **Not run to ground; narrowed.** Both masters bend nothing, they are wired alike (TG-F12), nothing in the runtime turns the bend off (TG-F13), and the frost points away from the capture (TG-F14). Three states remain (TG-F15). |
| A4 | **Agreed, and it waits for A3** (TG-F18). *(Built 2026-10-05, once A3 was answered: Pass 3, TG-F21.)* |
| A5 | **Confirmed** (TG-F19). A small change to one driver. *(Built 2026-10-05: Pass 3, TG-F23.)* |

### The questions, as far as this pass takes them

- **TG-Q1 — Does the thin master shift the view from the side today?** In the rig's capture, no. In a live view, unknown. The quickest answer is on the platform's side: `build_masters.py` writes the masters into any Unreal 5.8 project with Substrate on (P20), so the platform can put `M_Matter_TranslucentThin` on its own cube and look from the side.
- **TG-Q2 — Is the solid master's missing bend the master, or the capture?** Open. One throwaway master decides it, on the machine with Unreal: the solid master's settings, with a plain number (2.4) wired straight to Refraction in place of the function's output, captured on the rig's ball. If the ball bends, the capture is sound and the function's output is the cause (TG-F15, first row). If it does not, the capture drops the shift, and the two masters must be judged live.
- **TG-Q3 — Where does the rule live?** `MasterSet.md` §Material-settings intent is the candidate (TG-F16). The choice is the lead's. **Ruled 2026-10-05: there** (TG-RD1).
- **TG-Q4 — Does reflection keep the article's index on a thin wall?** Yes (TG-F17). The platform's assumption matches the library's masters.

### New questions

- **TG-Q5 — What does Epic's function return on its `Refraction (IOR)` output, for each value of `geometry_thin_walled`?** It decides between the rows of TG-F15. Readable on the machine with Unreal (Learnings Unreal T2), or by TG-Q2's probe.
- **TG-Q6 — Is textured see-through glass still a thin article once A1 is written?** (TG-F20.) It belongs with F-P11-16's contract work, not here.

---

## Pass 3 — The side view and the driver's fallback, built (2026-10-05)

*Written from the library's side. The lead, verbatim: "yes, do 1 and 2 and push", where 1 was A5 and 2 was A4. Built as a quick fix outside this doc. A4 no longer waited: the platform's look had shown the missing bend is the master and not the capture (the Status update below), so the rig's Unreal column can be trusted to show bend or its absence.*

- **TG-F21 — A4 is built: the rig has a `side` view.** A third camera, `/World/CamSide`, at (0.96, 0.29, 0.74), pitched −8° and yawed 50°: the cube's flat front face from its right, 0.95 m away, 50° off the face's normal at its centre and 43° to 55° across it, with the grid wall behind. Every ray through the face meets the wall, undeflected, inside the wall's width. A job renders it for the two see-through masters only, with the sphere hidden, since from there it sits behind the cube's far edge. All three drivers draw it; the Unreal driver sends the camera with the job, so the pinned runtime is unchanged. The numbers are in `tools/parity/JOB_FORMAT.md`.
- **TG-F22 — What the view shows today** (Glass_Clear and Diamond_Brilliant at their own values, this machine; looked at by the agent, the lead's look not yet taken):

  | Article | Storm | Blender | Unreal |
  |---|---|---|---|
  | Glass_Clear (thin) | the wall's lines run straight through the cube | straight | straight |
  | Diamond_Brilliant (solid) | straight, grey | **moved:** the wall is displaced and repeated inside a blue stone | **straight,** through a pale cube |

  So the thin article is drawn un-deflected by all three, as the rule asks, and the library's own sheet now shows both of the solid master's faults in Unreal in one picture: it bends nothing, and its colour is faint (M6).
  - **The two views that already existed are unchanged:** for both articles, Storm's and Unreal's pictures are the same bytes as before the change, and Blender's are within one 8-bit code.
- **TG-F23 — A5 is built: the Blender driver renders on the first device that can.** It tries OptiX, then CUDA, then the CPU, and the test of each graphics device is a 16-pixel, one-sample render of the job's own scene, because a listed device is not a device that can render (TG-F19). It names its choice in the job's `blender.log`. `MATTER_BLENDER_DEVICE=cpu` or `=gpu` forces it.
  - **Run here, on Glass_Clear's job:** this machine's card: OptiX chosen. Forced to the CPU: it renders, and its three pictures differ from the card's by noise (0.07 to 0.41 of an 8-bit code on average). **Every graphics device made to fail its test render, a stand-in for the platform's card:** the log names OptiX and CUDA as listed and unable to render, the job completes on the CPU, and the pictures are the forced-CPU ones. The same, told it must use the card: it stops and says why. A value it does not know: refused.
  - **Not run on a card that really cannot render.** The stand-in fails the driver's own test, not Cycles. That Cycles reports such a card as a failed render, or writes no picture, is what the test relies on; the platform's machine is where that is shown.
  - **The cost of the CPU here:** about a minute for the three pictures, against about ten seconds.

---

## Resolved

- **TG-RD1 — The consumer rule lives in `MasterSet.md` §Material-settings intent, and the ledger row is recorded (the lead, 2026-10-05).** Pass 2's handback offered both as one quick fix, naming `MasterSet.md`; the lead, verbatim: *"Yep... go ahead and do it"*. Done the same day, as a quick fix outside this doc:
  - `MasterSet.md`: the TranslucentThin refraction cell reads *"no deflection"* (it was *"index of refraction"*, as TranslucentThick), with a note stating the rule for every consumer: no shift at any angle, the rough blur and the tint kept, the reflection still by the article's index, and a solid article bends. The note carries a dated `Drift` line: the library's own Unreal masters are not yet shown to follow it.
  - `LCDSchema.md`: the `geometry_thin_walled` line points to that rule.
  - `PlatformDependencies.md` **M6**: the ask, with A1 written and A2 – A5 open.
  - OpenPBR's wording (TG-F1) was checked against the published specification before it was quoted in the spec: *"an infinitesimally thin sheet of dielectric"*, *"a reflected lobe and un-deflected refracted lobe"*.

---

## Status

- **Passes captured:** 3 (Pass 1 the platform's side; Passes 2 and 3 the library's; all 2026-10-05).
- **Asks:** **A1 is written** (TG-RD1). **A2 is answered:** the thin master draws un-deflected, live in the platform's renderer and in the rig's side view (TG-F22). **A3 is answered as to where, not repaired:** the missing bend is the solid master's (the update below), and the rig now shows it (TG-F22). **A4 and A5 are built** (Pass 3). *(Was, at Pass 2: "The other four stand, none built. A2 half answered … A3 narrowed to three states … A4 agreed, waits for A3. A5 confirmed".)*
- **Questions:** TG-Q4 is answered (yes). TG-Q3 is ruled (`MasterSet.md`, TG-RD1). **Open:** TG-Q1 (live view), TG-Q2 (master or capture), TG-Q5 (what Epic's function returns), TG-Q6 (textured thin glass, with F-P11-16).
- **Current direction.** The library's Unreal masters cannot be called adoptable as they stand: in two of the three states that fit the pictures, one of the two see-through masters is wrong. The frost in the capture leans to the state where the thin master is right and the solid one bends nothing.
- **What was added, and what was not.** The two passes added this doc only. *(Updated 2026-10-05: the rule and the ledger row are written, at the lead's direction and outside this doc — `MasterSet.md`, `LCDSchema.md`, `PlatformDependencies.md` M6; TG-RD1. Was: "No article, master, tool, spec or ledger row is changed by it. The suggested ledger row is not recorded".)* **Not changed:** any article, master or tool.
- **Update 2026-10-05 (from the platform's look, `261005_R_PlatformMasterAdoptionAsks.md` Pass 2 and its MA-F12):** the questions listed open above have moved. **TG-Q2 is answered: it is the master, not the capture.** The library's solid master bends nothing in a live view in the platform's renderer, where the platform's own solid master bends on the same cube. Of TG-F15's three states only the first is left: the thin master right, the solid one wrong, the rig's Unreal column truthful. **TG-Q1 is answered by eye, not by ruler:** the library's thin master read right in that live view. **TG-F7 holds when run:** an index of 1.0 on the Refraction input removes the bend and keeps the rough blur (the platform's own corrected thin master, Unreal 5.8 with Substrate). **Still open:** TG-Q5, what Epic's function puts on its refraction output, which is now the question the solid master's repair starts from; and TG-Q6.
- **Not run:** TG-F6 – TG-F9 are read from the engine source, by the platform; Pass 2 had no engine to check them against, and TG-F14 rests on TG-F7. The platform's corrected master has not been built or seen. TG-F3's Blender pictures are for the shape of light only — that machine's Blender colour setup does not load. Pass 2 rendered nothing; TG-F10 measures the rig's stored pictures of 1 – 2 October.

▶ **Next:** the solid master's repair, on the machine with Unreal: it bends nothing and shows its colour faint and flat (M6). A candidate for the bend is in the builder (`MATTER_MASTERS_REFRACTION=index`, `261005_R_PlatformMasterAdoptionAsks.md`), waiting on the platform's answer about the diamond; the rig's side view is where a repair will be judged here. **From the platform:** run the Blender column on its own machine, which is A5's real test.

*(Superseded 2026-10-05 by Pass 3. Was: "two things. (1) The Blender driver's CPU fallback (A5), small and buildable on any machine with Blender. (2) On the machine with Unreal, TG-Q2's throwaway master, which decides which see-through master to fix; the rig's angled view (A4) follows it. (The rule and the ledger row, listed here first until 2026-10-05, are done: TG-RD1.)")*

*(Superseded 2026-10-05 by Pass 2. Was: "the library reviews Pass 1 against its tree — A2 and A3 first, since they decide whether its Unreal masters can be adopted as they stand — and records the ledger row or declines it.")*
