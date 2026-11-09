# Research — The platform's object fade: every master draws an object part-present (2026-11-05)

**Mnemonic:** `POA` — reports `R-POA-n` (for the ledger), asks `Q-POA-n` (for the library).
**Mode:** an asks doc, written from the platform's side. It commits the library to nothing.
**Asked by:** the platform's lead, 2026-11-05. The question: *can a whole object fade in and out on the timeline, e.g. two versions of one character cross-fading between two keyframes?* The lead's rulings the same day: *"seed it — Opacity, dissolve, clean swap, yes at 0"*.
**Public repo:** needs and uses only. No consumer paths, code or tracker numbers.

**Read against:** this repo at `06969c3`:
- `unreal/MatterRuntime/Scripts/build_masters.py` — the master table at `:144-159` and `:772-778`; `bayer4()` at `:340-366`; the Hair coverage at `:718-740`;
- `tools/converters/assemble_mtlx.py:1053-1054`;
- `docs/specs/Ontology/MasterSet.md:210-225`;
- `docs/specs/Contract/LCDSchema.md:75-91`.

**Passes:** the reports and asks below are the platform's (Pass 1, 2026-11-05). The library's reading is Pass 2 (2026-11-09). The open questions and the Status footer belong to the doc.

---

## Reports — for the ledger

**R-POA-1 — The platform's app will give a Character, Prop or Set an Opacity, 0–100 %, that its timeline blends.**
- **One value per object, on the object's root.** It covers every mesh beneath the root: body, garments, hair cards and parts.
- **It is not a material port.** No article and no Creator port changes. A material bound to many objects still fades only the one whose Opacity moves.
- **In the app, a character is one drawn component** whose body, garments and hair are sections, so one value per component reaches every material on it. A prop or set may be several components, and each takes the same value.
- **At 0 the object is as if hidden:** not pressed, no shadow.

**R-POA-2 — The lead ruled a dissolve, never glass.**
- **A part-present object dissolves:** each pixel is either the object or what is behind it.
- **A see-through blend is ruled out:**
  - a character's inner layers show (the far side of the head, teeth, the body under a garment);
  - the skin loses its subsurface look;
  - sections mis-sort;
  - in the headset, which composites over pass-through, the real room shows through a fading character, as it does through glass today.
- **The dissolve keeps a whole object together.** Every layer of one object shares the value and the screen pattern, so at any one pixel all of them are kept or all dropped. A half-faded character never shows its own insides.

**R-POA-3 — Other USD apps will see a clean swap, not a fade.**
- The app bakes the Opacity as data, and bakes the object hidden wherever its Opacity is 0. Another app shows it vanish at the end of a fade-out and appear at the start of a fade-in.
- **The library's articles are NOT asked to read the value.** In a measured check with OpenUSD 26.03 (Storm), an `open_pbr_surface` whose `geometry_opacity` reads a `geompropvalue` primvar from the object's root fades both child meshes cleanly to nothing. Storm then always tags that material *translucent*, even at full presence: `pxr/imaging/hdSt/materialXFilter.cpp`, "A connected value is always considered to differ". So every Matter object would draw through Storm's see-through pass.
- A bound material ignores `primvars:displayOpacity` in Storm.

## Asks — for the library to decide

**Q-POA-1 — Every master can draw an object part-present, as a dissolve.**
- **The need:** from one per-object value, 0–1, keep or drop each pixel against a frame-stable screen pattern. It must hold under FXAA: the app's headset renders FXAA, not TSR.
- **The precedent is the library's own Hair coverage:** `bayer4()` (`build_masters.py:340`), the 4 × 4 ordered threshold on the pixel position, compared at `:736`.
- **The masters affected:**
  - **The solid masters (Opaque, TwoLayer, Emissive, Subsurface)** have no coverage today. A material instance cannot change its parent's blend mode (`MasterSet.md:225` records the same limit for two-sidedness).
  - **Masked and Hair** would combine the value with their own coverage.
  - **The glass masters** may scale their own transmission instead.
- 16 levels of presence are enough. On the desktop, TSR smooths the pattern.

**Q-POA-2 — A copy fading in takes the opposite pattern.**
- **Why:** in a cross-fade of two copies in the same place, if both keep a pixel when the threshold is below their own value (one at *p*, the other at *1 − p*), then at ½ they keep the same half of the pixels. The other half shows neither, so the room shows through mid-way.
- **The fix:** if the copy fading in keeps a pixel when the threshold is *above* its complement, every pixel shows exactly one of the two. Unreal's own level-of-detail cross-fade works this way.
- **What reaches the material:** the app knows which copy is rising. It can pass that as a second per-object value, or as the sign of the first. That is the library's call.

**Q-POA-3 — Full presence costs nothing extra.**
- The headset frame is already tight.
- **Option (a):** a masked twin of each solid master, used only while an object is part-present. Its costs are a material swap at a fade's start and end, and a first-use shader compile to avoid.
- **Option (b):** the solid masters masked always, which costs every solid object all the time.
- **The platform's preference is (a), but the design is the library's.**

**Q-POA-4 — How the value is read.**
- The platform's suggestion is Unreal's per-component *Custom Primitive Data* (one float, read by every material on the component, no per-material write).
- A material parameter works too, if the library prefers.
- The platform's app needs the index or parameter name, fixed in the master spec.

---

## Pass 2 — the library's reading (2026-11-09)

**Altitude:** a design reading of the asks — what each master would do, and the cost. No file or build targets; the build is the lead's to start.

**Examined:**
- this repo at `e2ffaac`: the Unreal master builder (the master table, `bayer4()`, the Masked and Hair coverage, the blend settings); `MasterSet.md` §Material-settings intent; the assembler's opacity output; every tool that reads the master tokens;
- Unreal 5.8's own source on the machine with Unreal: the material instance's property overrides, how an instance with overrides is compiled, Custom Primitive Data's upload, the default mask clip;
- the platform's side, read in place on 2026-11-09: its object-fade work went into discovery that day, and its record of the lead's rulings (local commits, not yet pushed).

### Seeds checked

- **F-POA-1 — The ask's citations hold, at new line numbers.** Three commits since `06969c3` changed the builder (compressed-texture switches). Nothing changed in the logic the ask cites. At `e2ffaac`: the master table is at `:152-166`, `bayer4()` at `:353`, the Hair coverage at `:755-768`, the blend settings at `:800-804`.
- **F-POA-2 — An instance CAN change its parent's blend mode. The ask's premise is too strong, and so is `MasterSet.md`'s two-sided note.**
  - Unreal 5.8 gives a material instance property overrides, including **blend mode, two-sidedness and the mask clip** (`MaterialInstanceBasePropertyOverrides.h`: `bOverride_BlendMode`, `bOverride_TwoSided`, `bOverride_OpacityMaskClipValue`).
  - An instance with an override gets **its own compiled shaders** (`MaterialInstance.cpp`, `InitStaticPermutation`). They are compiled when the instance is built, in the editor or the cook. **An instance made at run time cannot do this.**
  - So the limit is real only for **live** instances. An instance **asset** built next to its master can be masked where the master is opaque.
  - `MasterSet.md` says two-sidedness *"is a static shader property"* that Unreal *"cannot vary per material instance"*. That is the same overstatement. Its trade still holds (no per-prim two-sidedness in the article). But the rejected alternative, *"7 → 14 masters"*, would only be instances. **A `Drift` note is owed in that spec.** It is a spec edit, so it is not made here (offer 1 below).
- **F-POA-3 — An unset Custom Primitive Data slot reads 0.** A component that never sets any slot has all of them zeroed (`PrimitiveUniformShaderParametersBuilder.h`, `CustomPrimitiveData()`: *"Clear to 0"*). **So the value must mean "how far faded out", not "how present".** A presence value would default to 0, and every Masked and Hair object would vanish in any runtime that never sets it. That includes the library's own runtime and the rig.
- **R-POA-3's Storm measurements are the platform's and are not re-run here.** The library agrees with its conclusion: no article reads the value.

### The library's answers — proposals, for the lead to rule

**F-POA-4 — Q-POA-1: every master can, by one rule.** Keep a pixel when its 4 × 4 threshold `t` is below *(how present the object is) × (the master's own coverage)*. `t` depends only on the screen pixel, so every material on one object keeps or drops the same pixels together. A layer drops a pixel on its own only where its own coverage says so (a hair card's edge, a cut-out). That is R-POA-2's *"a whole object together"*.

| Master | How it fades | At full presence |
|---|---|---|
| **Hair** | its soft coverage × presence, against the same `bayer4()` threshold it uses today | the same pixels as today |
| **Masked** | its alpha test stays, and a second test against `t` is added: a pixel is kept only if both pass | the same pixels as today |
| **Opaque, TwoLayer, Emissive, Subsurface** | the same test, wired to the opacity mask (an opaque material ignores it). A **masked instance** of each master turns it on (F-POA-6) | the master itself, still opaque |
| **TranslucentThin, TranslucentThick** | no opacity mask in a see-through blend mode. **The same dither, not a smooth scale:** a dropped pixel draws no glass, so an eye's cornea or a pair of glasses dissolves in the same pattern as the body. The ask's alternative, scaling transmission, would fade the glass smoothly while the body dissolves | unchanged |

- **The mask clip:** Unreal's default is **0.3333** (`Material.cpp`). The builder sets 0.5 only on Masked and Hair. **The masked instances must carry 0.5 too**, or the test is off by a third.
- **Hypotheses, unmeasured:**
  - a dropped glass pixel may still bend what is behind it on TranslucentThick (the refraction is a separate output), so it must be zeroed there too;
  - a masked object's shadow takes the same test in the shadow map's pixels, so a part-present object casts a thinned shadow (at 0 the platform hides it anyway).

**F-POA-5 — Q-POA-2: the opposite pattern is exact, and one signed value carries it.**
- The complement of the 4 × 4 threshold, `1 − t`, is the same 16 levels in mirror order: `(k + ½)/16` ↔ `(15 − k + ½)/16`. So the copy fading in still has 16 levels.
- A copy fading out at presence `p` keeps `t < p`. The copy fading in, at `1 − p`, keeps `t ≥ p`. **Every pixel shows exactly one of them.** One test is strict and the other is not, so a threshold equal to the value goes to exactly one copy.
- **The value, proposed:** one float, `object_fade` = how far the object has faded **out**:
  - `0` = fully there. This is the default, so every runtime that never writes it draws exactly as today (F-POA-3);
  - `1` = gone;
  - **a negative value = the copy fading in**, which takes the opposite pattern. The app writes `1 − Opacity` for the copy fading out and `−(1 − Opacity)` for the copy fading in.
- The name avoids *opacity*, which is already an OpenPBR input (`geometry_opacity`) on Masked.

**F-POA-6 — Q-POA-3: option (a), and cheaper than the ask expected.**
- **"The masked twin" is four instance assets, not four more masters:** one per solid master, its blend mode overridden to masked and its clip to 0.5 (F-POA-2). They have no graph of their own and no parameter of their own. They take every parameter from their master, so an article's values carry over when the part's material is re-parented to the instance.
- **At full presence:**
  - the solid masters stay opaque, so there is **no added cost**;
  - Masked and the glass masters gain the threshold arithmetic, which Hair already pays: a few operations, with no new texture and no new pass.
- **While fading:** a part draws masked (a mask in the depth pass, and no early depth rejection). The cost in the headset is **unmeasured**.
- **First use:** each masked instance has its own compiled shaders. The platform's known risk applies unchanged: a newly used material draws the engine's default until its shaders are ready, so its start-up precache must include the four instances.
- **The platform runs the library's builder itself**, so the instances reach it with its next masters build.

**F-POA-7 — Q-POA-4: Custom Primitive Data, agreed.**
- One float on the component reaches every section's material, with no per-material write.
- **It also settles the scatter case on the library's side:** a scatter's points are slots of one instanced component, so they take one value together. That matches a scatter being keyed as one object.
- **The index** is fixed in `MasterSet.md`, beside the name. Proposed: **slot 0**, reserved for the library on any component that draws a library material. The platform reports no use of per-component data on its scene objects (2026-11-09). If a consumer wants slot 0 for itself, now is the cheap time to say so.
- **A material parameter cannot be the fallback:** a parameter bound to Custom Primitive Data reads only the component's data.

**F-POA-8 — What does not change.**
- No article, no Creator port, no `.mtlx`, no Blender master and no Storm output. The value is not a Creator port and not in the frozen port vocabulary.
- **At its default (`object_fade` = 0), every master draws exactly the pixels it draws today.** By the lead's 2026-10-05 ruling (a builder change that alters nothing at its defaults needs no new runtime), the change owes no runtime. The masked instances are new assets that the default path never uses.
- The tools that read the master tokens (assembler, validators, rig, thumbnails, Blender loader) see no new token: an instance is not a master.
- **To show it in the library's own runtime,** its Unreal driver would need to write the value to a mesh. That is a small addition to the build.

### The platform's side, recorded by date and content

- **2026-11-09** — the platform's object-fade work entered discovery. **It waits on this reading for one decision:** whether its runtime swaps a part's material at a fade's start and end. **Under F-POA-6 it does**, for the four solid masters only.
- **2026-11-09, the platform's lead** — an object's **effect** (an edge glow, a colour wash or an outline) is the platform's own overlay material, drawn over the whole outline at any Opacity, even 0. **It asks nothing of the library.** At Opacity 0, and when hidden, the object is gone for clicks and for walking through. Both are the platform's.
- **The platform's own record repeats the premise F-POA-2 corrects** (an instance cannot change its parent's blend mode). The ledger row carries the correction to it.

## Open questions

| # | Question | Why it matters | Library review |
|---|---|---|---|
| Q-POA-1 | every master can draw an object part-present | the platform's object-fade work | **answered, proposal:** F-POA-4 — the glass masters dither too |
| Q-POA-2 | the opposite pattern for the copy fading in | a clean cross-fade | **answered, proposal:** F-POA-5 — one signed `object_fade`, 0 = fully there |
| Q-POA-3 | full presence costs nothing extra | the headset frame | **answered, proposal:** F-POA-6 — (a), as four masked instances; the cost while fading is unmeasured |
| Q-POA-4 | how the value is read | the platform's runtime writes it | **answered, proposal:** F-POA-7 — Custom Primitive Data, slot 0 |
| Q-POA-5 | **for the lead:** take F-POA-4 … 7 as the design, and in which lane is it built? | the platform's decision on the material swap waits on it | open — the offers below |
| Q-POA-6 | the glass hypotheses (does a dropped pixel still bend the view? the shadow) and the headset cost while fading | the build's own checks | open — measured when it is built |

## Status

**Passes captured:**
- Pass 1 — the platform's reports R-POA-1 … 3 and asks Q-POA-1 … 4 (2026-11-05);
- Pass 2 — the library's reading, F-POA-1 … 8 (2026-11-09).

**Current direction (proposals, not yet ruled):**
- every master dissolves against the 4 × 4 screen threshold that Hair already uses;
- the four solid masters get one masked instance each, which the platform swaps to while an object is part-present;
- the value is one Custom Primitive Data float, slot 0, `object_fade`: how far faded out, 0 by default, negative for the copy fading in;
- nothing changes at the default, so no runtime is owed;
- articles, ports, Blender and Storm are untouched.

**Correction owed:** `MasterSet.md`'s two-sided note overstates Unreal's limit (F-POA-2). A `Drift` note is owed there.

**Ledger row:** not yet written. The next free id is **M15**: the ledger lists M1 … M14 (checked 2026-11-09).

**Offers, for the lead:**
1. **A `/quick-fix` now, docs only:** the M15 row (the asks, this reading, and the premise correction for the platform), plus the dated `Drift` note in `MasterSet.md`.
2. **The build, as a small phase:** the masters' fade, the four masked instances, the value fixed in `MasterSet.md`, and the library's Unreal driver writing it, seen in Unreal on a cross-fade pair at half. It fixes a contract the platform codes against, so it is a phase, not a quick fix (`LOCAL_DELTAS.md` §Weighting). It needs the machine with Unreal.

**▶ Next:** the lead rules Q-POA-5. Until then the doc is parked, with no seed.
