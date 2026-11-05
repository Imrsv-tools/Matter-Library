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

**Passes:** the reports and asks below are the platform's (Pass 1, 2026-11-05). The library's reading is owed (Pass 2), then the open questions and the Status footer, which belong to the doc.

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

## Open questions

| # | Question | Why it matters | Library review |
|---|---|---|---|
| Q-POA-1 … 4 | above | the platform's object-fade phase depends on them; it starts after its timeline-looks phase lands | owed |

## Status

**Passes captured:** Pass 1 (the platform's reports R-POA-1 … 3 and asks Q-POA-1 … 4, 2026-11-05).
**Owed:**
- the library's reading (Pass 2);
- a ledger row, under the next free `M` id once the ledger is listed (M15 at the time of writing — provisional).
**▶ Next:** a session at this repo's root runs `/research` on this doc.
