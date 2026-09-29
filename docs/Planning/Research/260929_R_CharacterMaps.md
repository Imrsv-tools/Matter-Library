# Research — The maps we have, and how to make characters look their best in Studio (skin, eyes, hair)

**Opened:** 2026-09-29 · **Mode:** research. It gathers and commits to nothing; a phase's discovery rules each question.
**Mnemonic:** `MAP` (ids `MAP-Fn`, `MAP-Qn`, `MAP-RDn`). **Ruled so far (2026-09-29):** MAP-RD1–RD6 (§Resolved); they
retire Passes 4–6's picture-per-mesh options for skin, make card hair the one exception (supported properly: its picture
shades a light article), put the whole eyeball picture in the library, and add an `Eye` master (Pass 7).

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
| MAP-RD3 | **Card hair is the one exception to MAP-RD2** (option 1; *"yes 1"*, after *"GAD I hate hair cards... it is like the worst "game engine" fix of all"*). Each hairstyle has its own strand picture; the library's hair article stays one general article with the tint. The matte look the lead approved at the platform's sitting is where card *quality* stops. **Amended the same day (lead: *"yes on hair"*): the exception is supported properly in the library.** The hair article takes the hairstyle's picture as an input and uses its light-and-dark **structure to shade the article's own light colour** (Pass 4's MODULATE), not to replace it. So every renderer draws the picture (Blender and USD viewers as well as Studio), and the tint reaches every colour on every style (MAP-F2). This answers the HS asks the library's way. *(Was: "nothing more is invested in cards", which had shelved this; corrected because it left the tint broken on 9 of 10 styles.)* |
| MAP-RD4 | **Strands are the real hair path, as a phase of their own** (*"and what you say"*, accepting the recommendation). The picture-per-mesh problem does not exist for strands: the hair is geometry and the library ships one material. |
| MAP-RD5 | **Where the effort goes instead** (the same *"what you say"*): skin stays general and gains what already exists but does not reach Studio (coat, fuzz, glow); the wet eye highlight by **coat**, not the cornea. **Eyes, amended the same day (lead: *"for the eyes.. whatever makes the eyes look best is what we would like"*):** not an iris-only texture but **the whole eyeball picture** (iris, limbal ring, sclera veins) in the library, bound to all three eye parts and placed by the existing `uv_scale` / `uv_offset` settings (Pass 7). Every MakeHuman eye shares one layout, so the picture lives in the library like the hair's. *(Was: "a library iris texture", Pass 7's first version.)* **The placement mechanism is superseded by Pass 8** (the picture is sampled on the eye's own UVs, as the hair's is); the ruling's intent is unchanged. The lead leans to **separate pictures per colour** (MAP-Q5, Pass 8). |
| MAP-RD6 | **Leverage Unreal where it can do better: an `Eye` master** (lead: *"This is a case to leverage UE where we can - but indeed adding mesh is not the time. I like the eye master idea"*). Unreal's eye shading (refraction through the cornea, a concave iris, depth) is used for Studio's eyes; Blender and USD viewers render the same article with what they have. **No new eye geometry now** (no cornea shell, lid shadow or tear line). This **reopens Phase07's D-E** (*"no `Eye` master; the eye is composed from existing masters"*, refused then under *"if one target can do something the others can't, don't rely on it"*), on the later LCD reading that each Unreal master leans on Unreal's best features (`PlatformDependencies.md` P20). |

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

> **Narrowed 2026-09-29 by MAP-RD2 / RD3** (kept for the record). This pass designs a family of maps a mesh supplies at
> binding. The lead ruled out pictures that fit only one mesh, with card hair the one exception, so **the family is one
> member: the hair picture**, read by MODULATE (MAP-F8 applies to it). MAP-F6's fact (a map sampled on `st` outside
> `place2d`) still holds. The eye's picture is not in this family: it is a library texture placed by settings (Pass 7).

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

> **Dispositions 2026-09-29 (§Resolved):** H-a **kept** (MAP-RD3 as amended: the direction for hair) · H-b open (a
> normal map for one style; not ruled) · H-c kept as recorded · H-d → strands (MAP-RD4) · S-a, S-b, S-c's masks **retired**
> (MAP-RD2: hm08-only pictures) · S-d **kept** (MAP-RD5) · E-a **reshaped**: the whole eyeball picture as a library texture
> placed by settings (MAP-RD5, Pass 7) · E-b **kept** (coat) · E-c answered by Pass 7 · **new: an `Eye` master (MAP-RD6).**

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

**Eyes: the whole eyeball picture, placed by settings** (MAP-RD5 as amended; *"whatever makes the eyes look best"*).
*(First written as an iris-only texture; replaced the same day, because the whole eye looks better: the picture draws the
round iris edge across the face-stepped cuts between the parts, and carries the sclera's veins.)*
- **The texture:** one eyeball from the CC0 MakeHuman eye pictures (Pass 2: nine colours, CC0 verified in the pack's
  bytes) — iris, limbal ring and sclera veins — centred in a square, in the library's texture tree with provenance. It
  carries what the flat articles lack (Pass 3, MAP-F5). How the iris colour varies (one light picture with the tint, or a
  picture per colour) is MAP-Q5.
- **Bound to all three eye parts** (`Sclera_*`, `Iris_*`, `Pupil_*`), which share the eye's UVs, so one pair of numbers
  places the picture on all three and they meet seamlessly.
- **The placement uses ports the articles already have.** `uv_scale` **divides** and `uv_offset` is **subtracted** after
  it (MaterialX `place2d`, `LCDSchema.md`). For an iris of radius `r` centred at `c` on the eye's UVs, drawn at radius `R`
  around the texture's centre: **`uv_scale = r ÷ R`**, **`uv_offset = c × R ÷ r − 0.5`**. On MakeHuman's eye (the pupil
  centres the platform measured, UV `(0.705, 0.700)` and `(0.290, 0.288)`; the iris radius ≈ 0.105 read off the picture,
  **to be measured at the build**) with the texture's iris at `R = 0.45`: `uv_scale ≈ 0.233` for both eyes, `uv_offset ≈
  (2.52, 2.50)` and `(0.74, 0.73)`. Each eye's parts carry their own two numbers — the same mechanism as the per-mesh
  `uv_scale` the platform already writes for the body (P18). *(A whole-eye texture needs `R` small enough that the sclera
  around the iris fits inside the square; the build picks it.)*
- **No contract change for the picture.** The articles gain a texture and declare `uv_scale` / `uv_offset`, the ordinary
  article shape. *(LCDSchema calls the UV ports "a last-mile nudge"; using them as the placement is what P18's stopgap
  already does. Unverified: that Studio's own masters apply the UV ports as `place2d` does, which LCDSchema requires;
  checked at the build.)*
- **The wet look:** coat on the iris and sclera (MAP-RD5); it reaches Studio with P16, or with the `Eye` master below.

**Eyes in Unreal: an `Eye` master** (MAP-RD6). A new master token whose MaterialX graph is the composed eye above (picture
+ coat, `open_pbr_surface`), and whose **settings row gives Unreal's eye shading** — the governing insight's own test for a
master (Unreal partitions shader space for eyes). Blender and USD viewers render the same article with what they have.
*From knowledge, not verified here — checked where the Unreal masters are built (Phase06 / Unreal Reference Masters, P20):*
Unreal's eye model shades **one eyeball surface** and computes the cornea's refraction and the iris's depth in the shader,
from an iris mask and radius — so it likely wants **one `Eye` article bound on all three parts** rather than three
articles, and it needs **no new geometry** (MAP-RD6: *"adding mesh is not the time"*). Open: MAP-Q12, Q13.

**Card hair: the one exception, supported properly** (MAP-RD3 as amended). Each hairstyle's picture shades the hair
article instead of replacing its colour:
- **The article:** `base = the article's light base × the hairstyle's prepared picture × base_color_tint`. An empty
  picture reads as 1 (white), so with none supplied the article is its plain colour — never magenta, as with the cut-out.
- **The picture:** prepared by the library (MAP-RD1: the library prepares the assets): each hairstyle's colour picture
  turned into a normalised greyscale **structure** (brightest strand ≈ 1; Pass 4's method), held in the library keyed to
  the hairstyle, next to its cut-out. The binding names it — a setting, as `cutout_map` is (HS-Q1's input; its name is ruled
  at the build, HS-Q6).
- **What it fixes:** Blender and USD viewers draw the strands too (HS-Q4, HS-Q5), the tint reaches blonde, red and black on
  every style (MAP-F2), and the brows and lashes take the tint (MAP-F3), because the colour now comes from the article.
- **Consumer side:** Studio's Hair master **multiplies** the picture into the colour instead of replacing it — an interim
  ask of the platform until Studio adopts the library's masters (P20).

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

## Pass 8 — The eye quick-fix, stopped at the balloon check (2026-09-29)

**What happened:** the lead directed the eye work as a `/quick-fix` (*"do the eye quick-fix"*). Its mid-flight balloon
check fired before anything was changed: the placement Pass 7 proposed is a contract rule, not a recipe edit. Nothing was
built or committed. **Examined:** the nine CC0 eye pictures (pixels), the rig's `build_character.py` and `job.py`, the
iris and sclera recipes, the platform's character recipe (its per-mesh `uv_scale`).

- **MAP-F9 — Eight of the nine eye pictures are one photograph, recoloured.** Iris luminance correlation between them is
  0.91–1.00; only **brown** is a different photograph (0.74–0.79 against the rest). So "separate pictures per colour" gives
  **two real iris patterns**, each colour with its own painted variation (e.g. blue-green's two tones), which a single
  tint cannot make. Still the higher-quality choice (the lead's lean on MAP-Q5), for that narrower reason.
- **MAP-F10 — Placing a picture by `uv_scale` / `uv_offset` clashes with three existing things.**
  - The platform's import already writes `uv_scale` on **every** character mesh from its measured UV density (the P18
    stopgap that fixed the skin's pore size), so it would overwrite an eye part's placement.
  - `LCDSchema.md` §Notes rules *one UV unit = one tile*; a placed, non-tiling picture needs a different rule.
  - The rig's character job takes defaults only (F-P08-4) and rescales each part's `st` by that part's own density, so
    the sclera, iris and pupil would each need different numbers.
- **MAP-F11 — The simpler route is the hair's mechanism.** Every MakeHuman eye shares one layout, so the library holds
  the eye picture **in that layout** and the article samples it **on the mesh's own `st`, outside `place2d`** — as
  `cutout_map` is (§Cut-out map). No placement numbers, no clash with the density `uv_scale`, and the rig keeps the eye
  parts' source `st` as it already does for the hair's cut-out parts. **It is the same contract addition as the hair
  picture input (MAP-RD3)**: one input kind serves both. *(Supersedes Pass 7's "placed by settings" and its numbers; kept
  above as the record. The rig's measured iris radius is 0.118 UV, `build_character.py`, not the 0.105 read off the
  picture.)*
- **MAP-F12 — The rig's eye is not Studio's eye.** The rig still has the cornea shell, and `Sclera_Natural`'s recipe
  relies on it for the wet shine (*"a glossy sclera under it would double the highlight"*); Studio dropped the shell. Eye
  work should be judged on a rig eye that matches Studio's (no shell). Coat on the eye parts reaches Studio only once P16
  carries coat, or with the `Eye` master.

**Routed:** the eye picture joins the hair picture and the `Eye` master in one phase, seeded 2026-09-29 on the lead's word
(*"yes 1, seed the phase"*): `docs/Planning/Phases/Future/Phase09_HairAndEyeMasters.md`.

## Open questions

| # | Question | Why it matters | Research reading |
|---|---|---|---|
| ~~MAP-Q1~~ | ~~Replace or modulate~~ | — | **Answered by MAP-RD3 as amended: modulate** (the hairstyle's picture shades a light article). *(Briefly marked "retired" the same day, before the amendment.)* |
| ~~MAP-Q2~~ | ~~Who normalises the maps~~ | — | **Answered by MAP-RD1: the library prepares them** (for hair, the one member of the family) |
| ~~MAP-Q3~~ | ~~One input family or one per role~~ | — | **Answered by MAP-RD2 / RD3:** one input, on the Hair article only; the eye's picture is an ordinary article texture |
| ~~MAP-Q4~~ | ~~Which skin atlas, at what strength~~ | — | **Retired by MAP-RD2** (hm08-only pictures) |
| MAP-Q5 | **The eye picture's colour: one light picture the tint takes to each colour, or a picture per colour from the nine?** | A light, neutral iris reaches any colour darker than itself (F-P08-1), but real irises differ in **pattern** too: brown is dense, blue shows fibres and crypts, hazel has a ring of a second colour round the pupil | **Lead leans to separate pictures** (2026-09-29). MAP-F9: 8 of 9 are one photograph recoloured, brown is a second, so that is two real patterns with painted colour variation. Ruled at the phase's discovery, on the rig's face view |
| ~~MAP-Q6~~ | ~~Coat on the eye parts, or the cornea~~ | — | **Ruled MAP-RD5: coat**; no new geometry (MAP-RD6) |
| ~~MAP-Q7~~ | ~~Brows and lashes: do they take the hair tint?~~ | — | **Answered by MAP-RD3 as amended:** they will, once their colour comes from the article (Pass 7) |
| ~~MAP-Q8~~ | ~~Eye placement: settings per eye, or an eye UV layout?~~ | — | **Answered by MAP-F11: neither** — the picture is held in the MakeHuman eye's own layout and sampled on the mesh's `st`, as the hair's cut-out is |
| MAP-Q9 | **Seed the strands phase, and who runs its first spike** (a runtime groom in Unreal, platform-side)? | MAP-RD4 | The lead's call; the spike decides whether the phase is real |
| MAP-Q10 | **Reopen Decision of record 1 for a strand hair material?** | A fibre model is not `open_pbr_surface` | The lead's call, at the strands phase |
| MAP-Q11 | **Matter-Library#3** (declare `strand_color_map`) | The issue is open and public | **Pursued, the library's way** (MAP-RD3 as amended): the input is declared, read as modulate, not replace; the lead comments on the issue |
| MAP-Q12 | **The `Eye` master: one `Eye` article on all three eye parts, or keep Sclera / Iris / Pupil as three articles on it?** | Unreal's eye model likely shades one eyeball surface (from knowledge) | One article, if Unreal's model confirms it; checked where the Unreal masters are built |
| MAP-Q13 | **Who builds the `Eye` master's Unreal side, and when does Studio get it?** | Studio renders with its own masters until P20 | Phase06 / Unreal Reference Masters build it; an interim platform ask if Studio needs it sooner |

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
  3 — what the pictures carry; 4 — the replace/modulate probe; 5 — the contract shape (narrowed to hair); 6 — per-part
  options (dispositioned); 7 — the direction after the lead's rulings; 8 — the eye quick-fix stopped at its balloon check
  (the eye rides the hair's input).
- **Decided (lead, 2026-09-29):** **MAP-RD1** the library prepares every material and asset, consumers only consume, and
  only names and settings travel · **MAP-RD2** no picture that fits only one mesh · **MAP-RD3** card hair is the one
  exception, **supported properly**: its picture shades a light hair article, so every renderer draws it and the tint
  reaches every colour · **MAP-RD4** strands are the real hair path, as their own phase · **MAP-RD5** eyes: whatever looks
  best — the whole eyeball picture in the library, placed by settings, with coat; skin stays general · **MAP-RD6** an `Eye`
  master using Unreal's eye shading, no new eye geometry now (reopens Phase07's D-E).
- **Current direction:** **eyes** — the whole eyeball picture (CC0; two real patterns, MAP-F9) held by the library in the
  MakeHuman eye's layout and sampled on the eye parts' own `st` (MAP-F11), with coat, and an `Eye` master whose Unreal side
  uses the engine's eye shading; **hair** — the hairstyle's picture, prepared by the library, shades the light `Hair`
  article (the HS asks and Matter-Library#3, answered the library's way); **both ride one new input kind**; strands as a
  phase; **skin** — general, lifted by what already exists reaching Studio (P16, P20, the glow's calibration).
- **Unverified, recorded as such:** every probe result is flat 2D colour, not a lit render; how Unreal's eye model wants
  the eye bound (MAP-Q12, from knowledge); a runtime groom in Unreal (platform sizing, 2026-09-28: unproven).
- **Open questions:** MAP-Q5, Q9–Q13 (Q1–Q3, Q7 and Q8 answered, Q4 retired, Q6 ruled).
- **Next step:** parked; the work is routed.
  - **Seeded 2026-09-29 (lead: *"yes 1, seed the phase"*), numbered Phase09 the same day (*"make it Phase09"*): `docs/Planning/Phases/Future/Phase09_HairAndEyeMasters.md`** —
    the one picture input kind (hair and eyes), the hair picture read as modulate, the eye picture, and the `Eye` token with
    its settings row; the Unreal sides with Phase06 / Unreal Reference Masters (P20). It opens by the lead's `/discovery`.
  - **Strands:** a phase of its own (MAP-Q9), seeded only on the lead's word; the Roadmap's *Hair That Reads as Hair*
    entry holds it.
  - *(The eye `/quick-fix` offered earlier was attempted and stopped at its balloon check: Pass 8.)*
