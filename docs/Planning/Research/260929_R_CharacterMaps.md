# Research — The maps we have, and how to make characters look their best in Studio (skin, eyes, hair)

**Opened:** 2026-09-29 · **Mode:** research. It gathers and commits to nothing; a phase's discovery rules each question.
**Mnemonic:** `MAP` (ids `MAP-Fn`, `MAP-Qn`, `MAP-RDn`). **Ruled so far (2026-09-29):** MAP-RD1–RD5 (§Resolved); they
retire Passes 4–6's picture-per-mesh options for skin and eyes, and contain card hair as the one exception (Pass 7).

**Question (lead, 2026-09-29, verbatim):** *"yesterday phase 66 found issues with hair and shared thoughts... the hair looks
"OK" now after removing whatever this over specualr thing was .... you need to do soem reserach about the maps we have
availabel so we can make our chacters looks as good as they can in Studio... Skin, Eyes, any other refinements to hair."*

**Extends, does not replace:** `260928_R_HairStrandColourMap.md` (HS-Q1–Q6, the platform's asks; Matter-Library#3) ·
`260928_R_HairAndNailRendering.md` (H1–H5, HR-Q4 "card maps") · `260927_R_CharacterMaterials_MPFB2.md` (CM2 "substance
in Matter, fit beside it", Pass 3's inventory, Pass 6b's "neutral-toned albedo-variation map", CM-Q5, CM-Q6) ·
`Phase07_CharacterMaterials.md` (L1 split, L2 cut-out, F13) · `Phase08_CharacterAppearance.md` (RD-P08-5 "author light") ·
`LCDSchema.md` §Cut-out map.

**Public-repo note.** The platform's planning is private. It is summarised here by what it found and what it renders, never
by its paths, issue numbers or commits.

---

## Resolved — lead decisions (2026-09-29)

Asked and answered in the session that wrote Passes 1–6, after the lead read them. Verbatim.

| # | Decision |
|---|---|
| MAP-RD1 | **The library prepares every material and every asset; consumers only consume.** Lead: *"Shouldn't the matter library prepare all materials and Studio just consumes? that way other UE scenarios usig our masters should also be close"*, and *"what needs to travel are parameters.. the libery has all the assets anyone needs"*. An exported character carries **material names and settings only**. This is P20 (Studio adopts the library's Unreal masters) taken to its end: meaning is defined once, by the library, for every renderer. |
| MAP-RD2 | **No picture that fits only one mesh** (*"no bespoke one image one mesh solutions"*). A library texture that fits any mesh following a known layout, placed by settings, is fine (*"eyes need images to look good"*); a picture painted to one mesh's UV layout is not. This retires, for skin and eyes, every Pass 4–6 option that supplied a mesh's own picture at binding (S-a, S-b, S-c's masks, E-a). |
| MAP-RD3 | **Card hair is contained as the one exception, and nothing more is invested in cards** (option 1; *"yes 1"*, after *"GAD I hate hair cards... it is like the worst "game engine" fix of all"*). Each hairstyle keeps its own strand picture, as the platform ships it today; the library's hair article stays one general article with the tint. The matte look the lead approved at the platform's sitting is where cards stop. |
| MAP-RD4 | **Strands are the real hair path, as a phase of their own** (*"and what you say"*, accepting the recommendation). The picture-per-mesh problem does not exist for strands: the hair is geometry and the library ships one material. |
| MAP-RD5 | **Where the effort goes instead** (the same *"what you say"*): eyes by a **library iris texture placed by the existing `uv_scale` / `uv_offset` settings** (Pass 7); skin stays general and gains what already exists but does not reach Studio (coat, fuzz, glow); the wet eye highlight by **coat first**, not the cornea. |

## Pass 1 — Where Studio's character stands after the platform's Appearance phase (read 2026-09-29)

**Examined:** the platform's closed Appearance phase (Phase 66) and its sitting findings, its Unreal learnings, its
character recipe, and this repo's HS thread (all pulled 2026-09-29).

- **Hair.** What made it read as hair was **MakeHuman's own colour picture on a matte master**, not a hair shading model
  (HS-F1, HS-F2). The "over-specular thing" the lead removed was Unreal's hair shading model on flat cards: with no
  per-strand tangent, every card lit as one block and its sheen read as a glossy sheet; the fix was a tangent weld plus a
  **matte** default-lit master (specular 0, roughness 1). The picture now rides as a second mesh-supplied map,
  `cutouts/<mesh>_color.png` → `inputs:strand_color_map`, which **replaces** the article's base colour; the Creator's
  tint **multiplies after** (HS Pass 2). Lead, live: *"OK! That is HAIR!"*, then *"Looks great"*.
- **Skin.** A tone is picked from the six `Skin_Fitzpatrick*` articles; the scale fault (pores drawn ~170× too large)
  is fixed, and lips and nails follow the tone (lead: *"skintones are good"*, *"lips and nails follow"*). The skin is
  **one flat tone plus a 1 cm pore tile** — nothing else reaches the body.
- **Eyes.** The eyeball is cut into Sclera / Iris / Pupil **along whole faces** (the iris by the picture's brightness, the
  pupil by a measured UV circle), each bound to a flat-colour article. **The cornea shell was dropped** by the lead at the
  platform's previous character phase (*"turn off the cornea for now"*: the milky, mirror-like shell hid the iris). So the eye has no wet
  surface to catch a highlight, and no picture detail at all.
- **Carried but not rendered.** Coat, fuzz and scatter anisotropy are still not carried by the platform (`PlatformDependencies.md`
  P16: its skin *"reads less oily than the library's renders"*); the skin's glow was flagged as a calibration (the
  platform's previous character phase, in its words *"skin glow wants more"*). Studio adopting the library's Unreal masters is P20.

## Pass 2 — The inventory: every map we can reach (measured 2026-09-29)

**Examined:** every image and `.mhmat` in the pinned CC0 system-assets pack (`makehuman_system_assets_cc0.zip`, sha256
`b542127a…0107`, cached in `library/parity/_sources/`); MPFB2's CC0 `data/textures/` (clone `3edf9df`); this repo's
`MatterLibrary/textures/`; the platform character's `cutouts/`.

| Part | In the CC0 pack / MPFB2 | Used by the library today | Reaches Studio today |
|---|---|---|---|
| **Skin** | 22 photo atlases on hm08, 2048² RGB, **albedo only** (young/middle/old × African/Asian/Caucasian × F/M, + 2 "special suit"). MPFB2: **`sss.png`** (2048² greyscale on hm08: a thickness / scatter weight, bright at ears, nose, lips, fingers; median 0.30, max 0.48); **10 region masks** (face, lips, ears, eyelids, finger/toenails, areolae, inside-mouth, crotch, genitals), 2048² greyscale on hm08 | none of them; the six skins are a constant tone + `Skin_Pores` (1 cm normal + roughness, tiled) | tone + pores (at the corrected `uv_scale`) |
| **Eyes** | 9 eye pictures, 1024² RGBA: **radial iris fibres, a dark limbal ring, sclera veins**, brown / light brown / blue / blue-green / deep blue / green / grey / ice / light blue. Alpha is all opaque (not a cut-out). A high-poly eye **with a cornea shell** | the rig splits the eye by the brown picture; articles are constants: `Iris_Brown` `(0.06, 0.006, 0.001)` Opaque, no coat; `Sclera_Natural` Subsurface, no coat; `Cornea_Clear` (TranslucentThin, the rig only) | the flat colours; no cornea |
| **Hair** | 10 styles, 2048² RGBA pictures (strands, gaps, root-to-tip, **highlights painted in**). **`short02` — the built-in hair — also ships `short02_normal.png` (2048² RGB)**, which its own `.mhmat` switches off (`shaderConfig normal False`). No other style has one | `cutout_map` (alpha) only; colour, roughness, anisotropy constants | alpha as soft cover + the picture's RGB **replacing** the colour |
| **Brows / lashes** | 12 + 4 pictures, 512² RGBA; the `.mhmat` reuses the picture as a bump | `cutout_map` only | alpha + RGB (see MAP-F3) |
| **Teeth / gums / tongue** | one 2048² atlas for teeth + gums, one 1024² tongue picture | the rig splits by the atlas; articles are constants | flat colours |

- **MAP-F1 — There is almost no "PBR set" to find.** Beyond albedo pictures the whole CC0 pool holds **one** normal map
  for hair (`short02`), **one** thickness map for skin (MPFB2 `sss.png`), and the region masks. No skin normal,
  roughness, specular or cavity map exists in it (CM Pass 3 said so for skins; this pass confirms it for every part).
  Clothes are the exception (normal on 15, AO on 11), and they are garment-bound. **So "the maps we have" are the pictures,
  and the realism has to come from reading them well, plus what the library already tiles (pores, weaves).**

## Pass 3 — What the pictures carry (looked at, contact sheet in §Reproduction)

- **Hair pictures are albedo + depth + baked light in one.** Dark gaps between strands, lighter roots or tips, and on
  `bob01` red highlights painted on the crown. That is HR-Q4's whole card-map family (root-to-tip, strand variation,
  depth) **already present, merged into one RGB picture**.
- **Each hair picture is a dyed colour.** Linear luminance, median over the covered pixels: afro01 0.001 · braid01 0.003 ·
  short01 0.012 · bob01 0.015 · long01 0.017 · short04 0.017 · short03 0.036 · short02 0.049 · ponytail01 0.049 ·
  **bob02 0.294** (the only blonde). Brows (`eyebrow001`) 0.002 and lashes (`eyelashes01`) 0.001: near black. The
  platform's built-in hair map (`Hair_color.png`, from short02) measures 0.054 over the whole map.
- **Eye pictures carry exactly what the flat articles lack:** the iris's radial fibres and crypts, the dark limbal ring
  that makes an iris read as round and wet, and fine red sclera veins with a warm falloff towards the corners.
- **Skin atlases carry the face:** darker lips, nostrils, eye sockets, knuckles, nipples, redder ears and cheeks, and some
  **baked shading** (creases, under the nose). They also carry things that are not skin: painted scalp stubble and beard
  shadow (the African male atlases), and a small MakeHuman mark in unused UV space.

## Pass 4 — Probe: REPLACE vs MODULATE, on hair, skin and eye pictures (2026-09-29, disposable)

**Why:** HS-Q2 asks the library how the strand colour map enters the graph. The platform chose **replace** (the picture
becomes the base colour, the tint multiplies after). A tint that multiplies **only darkens** (Phase08 F-P08-1,
RD-P08-5). This probe measures what each reading gives a Creator.

- **REPLACE:** `picture × tint`.
- **MODULATE:** the picture's **structure** only (its luminance ÷ its own 95th percentile, so the brightest strand is ≈ 1
  and gaps and roots fall below), `× the article's light base × tint`. For skin, luminance ÷ its mean, over each library
  tone. For the eye, the iris region's structure over a blue and a green base (the iris found by geometry, as Studio's
  Iris mesh is).

Flat 2D swatches, no lighting — a colour-reach test, not a render. Picture: `260929_R_CharacterMaps_probe.jpg`.

| Hair | Tint | REPLACE (median L) | MODULATE (median L) |
|---|---|---|---|
| bob01 | blonde | 0.014 | **0.133** |
| bob01 | auburn | 0.005 | 0.044 |
| long01 | blonde | 0.015 | **0.092** |
| afro01 | blonde | 0.001 | **0.065** |
| any | black | ≤ 0.001 | 0.003–0.006 |

- **MAP-F2 — Under REPLACE, "one hair material in any colour" holds for one style of ten.** Every style but bob02 is
  painted dark, and a multiply cannot lift it: blonde on bob01 is 0.014 (a dark brown), on afro01 0.001 (black). Under
  MODULATE every style reaches blonde, auburn and black, and keeps its strands, gaps and root-to-tip (the sheet's rows 1–3).
  **This is the same finding as F-P08-1 (a tint only darkens), one level down:** RD-P08-5 made the *article* light; replace
  puts a dark picture back in front of it.
- **MAP-F3 — The brow and lash pictures are black** (median linear luminance over covered pixels: `eyebrow001` 0.002,
  `eyelashes01` 0.001; the platform's `Eyebrows_color.png` and `Eyelashes_color.png`, made from them, measure 0.000 over the
  whole map). Under REPLACE the hair tint cannot move them at all, although the lead ruled at the platform's
  sitting that brows and lashes **follow the hair tint**. *Measured on the files; not seen in Studio — unverified there.*
- **MAP-F4 — The skin atlases work as a tone-free detail layer, read by luminance.** Luminance ÷ its mean spans 0.46–1.48
  (p5–p95) on the face, and over Skin I, IV and VI it gives each tone its lips, nostrils, sockets and cheek variation with
  no colour cast (row 4). *A per-channel ratio was tried first and cast the dark tones olive, because it carries the source
  skin's own chroma; rejected.* The atlas's baked shading and painted stubble come along, so the choice of source atlas and a
  strength matter (MAP-Q4).
- **MAP-F5 — The eye pictures work as an iris structure, and give any eye colour.** The brown picture's iris luminance
  over a blue or green base keeps the fibres and the limbal ring (row 5). The nine CC0 colours are also usable as they are.

## Pass 5 — The contract shape these findings point at

> **Retired 2026-09-29 by MAP-RD2 / RD3** (kept for the record). This pass designs a family of maps a mesh supplies at
> binding. The lead ruled out pictures that fit only one mesh, and contained card hair as the one exception with no
> further investment, so no such family is built. MAP-F6's fact (a map sampled on `st` outside `place2d`) still holds.

- **MAP-F6 — A mesh-supplied map coexists with the tiled detail on the character's one UV set.** §Cut-out map samples the
  mesh's map **on `st` directly, not through `place2d`**, while the article's tiled textures go through `place2d` and the
  binding's `uv_scale` (≈ 0.0065 on the raw hm08 atlas, the P18 stopgap). So on the Body a hm08 detail map and the 1 cm
  pores can both be correct at once — no second UV set (which Storm cannot read, S9) and no wait on P18's real-scale UVs.
- **MAP-F7 — One family, not three special cases.** Hair's colour, skin's detail, the eye's iris structure and skin's
  thickness are all **a picture that belongs to the mesh, supplied at binding, never in the article** (D1, CM2) — the
  cut-out map's pattern. HS-Q6 already asks whether the strand colour opens a "card maps" family; the evidence here says
  the family is wider than cards: it is the character's **fit** (the Glossary's word under *Cut-out map*), in the
  character's own USD, which is where the platform already keeps its fit data.
- **MAP-F8 — MODULATE needs a normalised map, and the normalising is data preparation, not graph work.** A MaterialX graph
  cannot take a percentile, so the map is written already normalised (greyscale, brightest strand ≈ 1; skin centred on 1),
  by whoever writes the mesh's maps today (the platform's character generator writes `<mesh>_color.png` from the same
  source). The article then multiplies: `base = article_base × shade_map × tint`, and an empty map's default of 1 leaves
  the article's colour — the cut-out's `default = 1` rule, so never magenta.
- **In Unreal:** the platform carries the picture on its base-colour **texture** channel, whose resolve is replace
  (*"white-when-textured"*). MODULATE needs its master to multiply instead — a consumer-side change the library would
  raise as an ask, and the same one for every master that takes a map (P20 makes it one master set).

## Pass 6 — What else would lift each part (by the available maps; options, not decisions)

> **Dispositions 2026-09-29 (§Resolved):** H-a, H-b **retired** (MAP-RD3: no more card work) · H-c kept as recorded ·
> H-d → strands (MAP-RD4) · S-a, S-b, S-c's masks **retired** (MAP-RD2: hm08-only pictures) · S-d **kept** (MAP-RD5) ·
> E-a **replaced** by a library iris texture placed by settings (Pass 7) · E-b **kept** (coat first) · E-c answered by Pass 7.

**Hair**
- **H-a — MODULATE the strand map** (MAP-F2): the library's answer to HS-Q2. Keeps the matte look the lead approved, and
  restores "any colour".
- **H-b — `short02`'s normal map**, supplied at binding like the others: strand relief under a key light on the built-in
  hair, at no specular cost. It is the only style that has one; the other nine would need one derived from their picture
  (a height-from-luminance normal is standard and cheap).
- **H-c — A faint, tinted highlight, only when the lead asks.** The lead ruled matte (*"turn off anything specular"*). A
  real hair highlight needs the per-strand tangent Epic's cards bake and MakeHuman's do not (HS-F2). Recorded, not
  proposed.
- **H-d — Better card assets** (HR H4/H5, strands later): still the real ceiling (*"these cards are terrible but they read
  correct"*).

**Skin**
- **S-a — A detail map from a CC0 atlas, by luminance** (MAP-F4), modulating each Fitzpatrick tone. The largest single
  gain available: it gives the face its lips-to-skin transition, sockets, nostrils, knuckles and cheek variation. One
  source atlas per body (the character is one hm08 body); strength matters because of baked shading.
- **S-b — MPFB2's `sss.png` as a scatter weight map** (thin parts glow more: ears, nose, fingers). It answers the
  platform's *"skin glow wants more"* where it matters, instead of raising the glow everywhere.
- **S-c — The region masks** (ears, lips border, eyelids, face): redness and tone per region. This is colour on a layer —
  **CM-Q5**, still unruled. S-a already carries much of it inside the picture, which may make CM-Q5 less urgent for
  characters (makeup still needs it).
- **S-d — The carriers the library already authors:** coat (the oily sheen) and fuzz on skin reach Studio only once P16
  lands. No new map needed; the gap is consumer-side.

**Eyes**
- **E-a — The eye picture on all three parts** (Sclera, Iris, Pupil sample the same map on the eye's own UVs). The picture
  draws the round iris, the limbal ring and the veins, so the **face-stepped cuts between the parts stop showing**.
  Iris colour by MODULATE (any colour, MAP-F5) or by choosing one of nine pictures (a mesh-side choice, like a hairstyle).
- **E-b — A wet highlight without the cornea:** coat on `Iris` and `Sclera` (the library authors coat already; P16 carries
  it). The cornea's own look was "milky, mirror-like" in Studio and is the lead's to revisit.
- **E-c — The iris is a pattern on a disc** (CM-Q4's "on the matter / object line"): E-a settles it the D1 way — the
  pattern is the mesh's picture, the pigment is the article.

**Teeth, gums, tongue:** the same pattern would lift them (the atlas's gum and enamel variation); lower priority than
face and eyes. Phase07 noted the gums read dark maroon in Storm.

**Outside this library's lane:** Studio's lighting (a character's skin and eyes depend on it as much as on any map) and the
cards themselves.

## Pass 7 — The direction after the lead's rulings (2026-09-29)

**What separates an allowed image from a bespoke one** (MAP-RD2): not whether there is a picture, but whether it fits
only one mesh. A **library texture** (the pores, a weave) fits any mesh and ships with the article; only names and settings
travel (MAP-RD1). A **bespoke picture** is painted to one mesh's UV layout and has to travel with that mesh.

**Eyes: a library iris texture, placed by settings.** An iris is a disc, so one texture fits any eye once two numbers say
where the disc sits:
- **The texture:** an iris cut from the CC0 MakeHuman eye pictures (Pass 2: nine colours, CC0 verified in the pack's bytes),
  centred in a square, in the library's texture tree with provenance, like any other texture. It keeps what the flat
  article lacks: the radial fibres and the dark limbal ring (Pass 3, MAP-F5).
- **The placement uses ports the article already has.** `uv_scale` **divides** and `uv_offset` is **subtracted** after it
  (MaterialX `place2d`, `LCDSchema.md`). For an iris of radius `r` centred at `c` on the eye's UVs, drawn at radius `R`
  around the texture's centre: **`uv_scale = r ÷ R`**, **`uv_offset = c × R ÷ r − 0.5`**. On MakeHuman's eye (the pupil
  centres the platform measured, UV `(0.705, 0.700)` and `(0.290, 0.288)`; the iris radius ≈ 0.105 read off the picture,
  **to be measured at the build**) with `R = 0.45`: `uv_scale ≈ 0.233` for both eyes, `uv_offset ≈ (2.52, 2.50)` and
  `(0.74, 0.73)`. Each eye is its own mesh (`Iris_L`, `Iris_R`), so each binding carries its own two numbers — the same
  mechanism as the per-mesh `uv_scale` the platform already writes for the body (P18).
- **No contract change.** The `Iris` article gains a texture and declares `uv_scale` / `uv_offset`, the ordinary article
  shape. The **better end state** is an eye mesh whose iris UVs are laid out on the library's disc, so no numbers are needed;
  until then the settings do it. *(LCDSchema calls the UV ports "a last-mile nudge"; using them as the placement is what P18's
  stopgap already does. Unverified: that Studio's own masters apply the UV ports as `place2d` does, which LCDSchema requires;
  checked at the build.)*
- **The wet look:** coat on `Iris` and `Sclera` (MAP-RD5); it reaches Studio with P16.
- **Optional, same mechanism:** a sclera texture (veins radiating from the iris), placed by the same two numbers.

**Card hair: contained, as it is** (MAP-RD3). The platform keeps each hairstyle's own picture (it replaces the colour; the
tint multiplies after). **The known consequence, recorded so it is not later read as a defect:** MAP-F2 stands — on nine
of ten styles the tint only darkens the painted colour, so blonde and red are out of reach except on `bob02`; and the
brows and lashes probably do not take the tint (MAP-F3). The HS asks (HS-Q1–Q5: the library declaring the strand map so
USD viewers and Blender draw it) are **not pursued** under MAP-RD3.

**Strands: the real hair path** (MAP-RD4). What it needs, from the platform's sizing (2026-09-28; recheck when the platform
next opens hair):
- **Unreal:** it cannot build a groom from strand data outside the editor, so a **runtime groom builder** (engine pieces
  exist, unused that way; unproven) — a disposable spike first; a strand source (the CC0 pack has cards only); Stage
  carrying curves; a VR frame-cost check. All platform-side.
- **The library:** one strand hair material. Its fibre model (MaterialX `chiang_hair_bsdf`, Blender's Principled Hair,
  Unreal's strands) is not `open_pbr_surface`, so it needs the lead to reopen Decision of record 1. Storm drawing
  `chiang_hair_bsdf` is still unverified (CM Pass 4).

**Skin: stays general** (MAP-RD2, RD5): tone, tiled pores, scatter, coat and fuzz, on any body. What lifts it in Studio is
already authored and does not arrive yet: coat and fuzz (P16), the glow's calibration, and Studio adopting the library's
masters (P20).

## Open questions

| # | Question | Why it matters | Research reading |
|---|---|---|---|
| ~~MAP-Q1~~ | ~~Replace or modulate~~ | — | **Retired by MAP-RD3** (no card investment; the platform's replace stays) |
| ~~MAP-Q2~~ | ~~Who normalises the maps~~ | — | **Retired by MAP-RD2 / RD3** (no mesh-supplied maps are built) |
| ~~MAP-Q3~~ | ~~One input family or one per role~~ | — | **Retired by MAP-RD2** |
| ~~MAP-Q4~~ | ~~Which skin atlas, at what strength~~ | — | **Retired by MAP-RD2** (hm08-only pictures) |
| MAP-Q5 | **The library iris: one light iris the tint takes to each colour, or one article per colour from the nine pictures?** | A light, neutral iris reaches any colour darker than itself (F-P08-1), but real irises differ in **pattern** too: brown is dense, blue shows fibres and crypts, hazel has a ring of a second colour round the pupil | One light iris with the tint (the hair and fabric model, RD-P08-5), plus a second article only where a pattern differs; judged on the rig's face view |
| ~~MAP-Q6~~ | ~~Coat on the eye parts, or the cornea~~ | — | **Ruled MAP-RD5: coat first** |
| MAP-Q7 | Brows and lashes: do they take the hair tint in Studio with black pictures (MAP-F3)? | The lead ruled at the platform's sitting that they follow the tint | A platform check; under MAP-RD3 the library builds nothing for it |
| MAP-Q8 | **Iris placement: two settings per eye now, or an iris UV layout the eye mesh follows?** | Settings work today; a layout needs the platform to re-lay the eye | Settings now, the layout when the platform next rebuilds the eye |
| MAP-Q9 | **Seed the strands phase, and who runs its first spike** (a runtime groom in Unreal, platform-side)? | MAP-RD4 | The lead's call; the spike decides whether the phase is real |
| MAP-Q10 | **Reopen Decision of record 1 for a strand hair material?** | A fibre model is not `open_pbr_surface` | The lead's call, at the strands phase |
| MAP-Q11 | **Matter-Library#3** (declare `strand_color_map`): close as not pursued under MAP-RD3? | The issue is open and public | The lead's call |

## Reproduction

`260929_R_CharacterMaps_probe.py` beside this doc (the probe) writes `260929_R_CharacterMaps_probe.jpg` (committed beside
it). Run on the pinned pack — the rig's cache, or re-fetch at the hash in `260927_R_CharacterMaterials_MPFB2.md` Pass 3:

```bash
uv run --with pillow --with numpy python docs/Planning/Research/260929_R_CharacterMaps_probe.py \
  library/parity/_sources/makehuman_system_assets_cc0.zip /tmp/probe.jpg
```

The inventory (Pass 2) was two throwaway readers over the same zip: every image's size and mode (`PIL.Image.open` on each
`zipfile` entry), and every `.mhmat` key per category. The MPFB2 files are at `src/mpfb/data/textures/` in
`makehumancommunity/mpfb2` at `3edf9df`; `sss.png` is read by `entities/material/enhancedskinmaterial.py`. Nothing in the
repo was written by either; the scratch in `/tmp` is torn down.

## Status

- **Passes captured (2026-09-29):** 1 — Studio's character after the platform's Appearance phase; 2 — the map inventory;
  3 — what the pictures carry; 4 — the replace/modulate probe; 5 — the contract shape (retired); 6 — per-part options
  (dispositioned); 7 — the direction after the lead's rulings.
- **Decided (lead, 2026-09-29):** **MAP-RD1** the library prepares every material and asset, consumers only consume, and
  only names and settings travel · **MAP-RD2** no picture that fits only one mesh · **MAP-RD3** card hair contained as the
  one exception, nothing more invested in cards · **MAP-RD4** strands are the real hair path, as their own phase ·
  **MAP-RD5** eyes by a library iris texture placed by settings, skin stays general, coat first for the wet eye.
- **Current direction:** **eyes** — a library iris texture cut from the CC0 pictures, placed on each eye by `uv_scale` /
  `uv_offset` (Pass 7), with coat on iris and sclera; **skin** — general, lifted by what already exists reaching Studio
  (P16, P20, the glow's calibration); **hair** — cards stay as they are (with MAP-F2's known limit), strands as a phase.
- **Unverified, recorded as such:** every probe result is flat 2D colour, not a lit render; MAP-F3's brows in Studio; the
  iris radius (≈ 0.105, read off the picture, measured at the build); that Studio's own masters apply the UV ports as
  `place2d` does; a runtime groom in Unreal (platform sizing, 2026-09-28: unproven).
- **Open questions:** MAP-Q5, Q7–Q11 (Q1–Q4 retired, Q6 ruled). The HS asks (HS-Q1–Q6) are not pursued under MAP-RD3;
  closing Matter-Library#3 is MAP-Q11.
- **Next step:** parked. **The eye is buildable in one sitting as a `/quick-fix`:** cut the iris texture from the CC0 pack
  (with provenance), re-author `Iris_*` with it and the two UV ports plus a coat, add coat to `Sclera_Natural`, and give the
  rig's character job the two numbers per eye, seen on the rig's face view and in Blender. **Strands** would be a phase
  (MAP-Q9), seeded only on the lead's word; the Roadmap's *Hair That Reads as Hair* entry points here.
