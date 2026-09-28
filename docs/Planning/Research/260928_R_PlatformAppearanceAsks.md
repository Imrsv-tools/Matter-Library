# Research — What the platform's Appearance work needs from the library

**Opened:** 2026-09-28 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `AP` (ids `AP-Qn`, `AP-Fn`). **Passes 1–4** were written from the platform's side; **Passes 5–6** are the library's review of them against its own tree (2026-09-28).
**Requested by:** the IMRSV platform's **Phase 66 (Appearance)** — the Creator-facing character work (choose and change
garments, hair and skin tone, per mark), planned 2026-09-28. The lead asked for this doc so the library can start now.

**Question (lead, 2026-09-28, condensed):** put in the Matter Library what the platform's Appearance phase needs from it,
so the library can start on it while the platform builds its side.

**Extends, does not replace:** `260927_R_CharacterMaterials_MPFB2.md` (CM-Q3 hair, CM-Q5 colour on layers, CM-Q9 region
slots, CM-Q10 skin master), `Phase07_CharacterMaterials.md` (its close and deferral ledger), `PlatformDependencies.md`
(M1, P4, P15–P19).

**Public-repo note.** The platform's planning is private. It is summarised here by what it needs from the library — no
platform paths or code. *(The phase is named at the lead's request.)*

---

## Pass 1 — What the platform has ruled, as it touches the library

- **Every character material is a Matter article bound by identity.** No side-lined direct-master binding. The six
  Fitzpatrick skins, lips, nails, eye tissues, enamel, gum, tongue, the three fabrics and the hair fibre from Phase07 are
  what the platform's dressed test character already wears.
- **Hair:** card hair now, strands later, on **one high-quality hair material**; hair colour is **a tint on that one
  material** (lead: *"tint one hair material but we need to make this material really good"*). The same material must shade
  strands when the platform adds them (lead: *"can the same material be used when we switch to groom"*).
- **Skin:** the Creator **picks one of the six skin tones**, and **the lips and nails change with it** (lead: *"either way
  yes — lips etc need to change as well"*). The lead's real wish is a proper tone control aligned with the library; that is
  deferred (Pass 3, A4).
- **Makeup is out of the platform phase** — it needs the colour channel on layers (CM-Q5), which stays with Phase08.
- **Fabrics:** garments from the CC0 MakeHuman system pack are bound to the existing `Cotton_Jersey`, `Denim_Indigo` and
  `Leather_Brown` articles. No new fabric is asked for now.

## Pass 2 — What the platform found in the library's consumer rows (checked against its live code, 2026-09-28)

| Row | Library says | The platform's live code |
|---|---|---|
| **P4** — route by the article's declared master token | OPEN | **Delivered** — the platform routes every article by its own `master_material` token |
| **P15** — one slot per substance | OPEN | **Delivered as meshes** — the character is one mesh per substance (Body, Lips, Nails, Sclera, Iris, Pupil, Teeth, Gums, Tongue, Eyebrows, Eyelashes, Hair, garments). This also answers **CM-Q9**. |
| **P16** — carry coat / fuzz / anisotropy | OPEN | **Still open** for coat and fuzz (skin reads less oily than in the library's renders). **Anisotropy for hair is no longer needed** if hair moves to a hair shading model (A1). |
| **P17** — supply a card's cut-out map at binding | OPEN | **Delivered** — carried from the article to the bound material |
| **P18** — real-scale detail UV set, per-slot `uv_scale` stopgap | OPEN, stopgap named as Studio's | **Stopgap delivered in the platform's import**, not Studio: each character mesh's `uv_scale` comes from its measured UV density. The real-scale UV set is still open. |

## Pass 3 — The asks

**A1 — A `Hair` master (the 8th token).** *Needed for the platform's hair leg.*
- **Why:** the Masked-card hair reads as plastic on the platform's character (its own finding, 2026-09-27), and the lead
  wants one really good hair material that also serves strands later. `MasterSet.md`'s Masked row already says *"a
  dedicated `Hair` master only if Masked hair looks wrong"* — the platform reports that it does.
- **What the platform will build on its side:** an Unreal master using Unreal's hair shading model with the
  "used with hair strands" flag on, masked (cards need the cut-out, P17), two-sided, taking the frozen Creator ports —
  **`base_color_tint` as the hair-colour tint**. It routes an article to it when the article declares `master_material =
  "Hair"`.
- **What the library would decide and author (its discovery):** the `Hair` token and its settings row in `MasterSet.md`;
  the hair article's MaterialX side (CM-Q3: Masked-style OpenPBR cards, or `chiang_hair_bsdf` — whether Storm renders it
  is still unverified); re-routing `Hair_DarkBrown_Clean_Base_s001_v01` (today `Masked`) — and brows / lashes if the
  library judges them hair too; the validator's token set; the Blender proxy for the new master.
- **Stock-viewer parity matters:** the platform promises the dressed character *"looks the same in any USD viewer"*. A
  hair article whose MaterialX side does not render in Storm would break that promise.

**A2 — Tone-matched lips and nails for the six skin tones.** *Needed for the skin leg.*
- **Why:** there is one `Lips_Natural` and one `Nail_Natural` beside six `Skin_Fitzpatrick*`. Picking skin tone *N* must
  also re-bind the lips and nails.
- **The platform needs a deterministic pairing,** so its skin-tone control can find the three articles for tone *N* without
  a hand-kept table. Suggested: `Lips_FitzpatrickI…VI` and `Nail_FitzpatrickI…VI` (the skin family's naming), or a
  machine-readable tone-family field in the release. The library chooses.

**A3 — Reconcile the consumer rows** (Pass 2): mark P4, P17 and the P18 stopgap delivered (the stopgap in the platform's
import); P15 delivered as one mesh per substance; P16 open for coat and fuzz only, if A1 lands.

**A4 — Recorded, not asked now: a real skin-tone control.** The lead's wish is a small Creator-facing tone control (base
tone, melanin, redness — already on the Phase07 skin wish-list). It is a change to the **frozen** Creator vocabulary
(`LCDSchema.md`) and every consumer's masters, so the platform picks one of six tones for now.

## Pass 4 — Sequencing with the platform

- **Order matters for A1.** The platform fails loud on an unknown master token (no silent fallback), so an article
  re-routed to `Hair` renders as the missing material until the platform's Hair master exists. Ship A1 as a **candidate
  release**; the platform takes it when its Hair master lands. Until then, hair stays on `Masked`.
- **A2 is additive:** new articles break nothing, and the platform can take them whenever they land.
- The platform's sittings for skin and hair wait on A1 and A2; everything else in its phase proceeds without them.

## Pass 5 — The library's review: the asks checked against the tree (2026-09-28)

**Examined:** `MasterSet.md` (tokens, Masked row, settings table), `LCDSchema.md` (the Creator tier, §Cut-out map), `PlatformDependencies.md` (P15–P19, M1), `260927_R_CharacterMaterials_MPFB2.md`, `Phase07_CharacterMaterials.md` (L1–L4, D-E, the close), the character and textile articles and their recipes, `tools/parity/rig.py` `CHARACTER_CAST`, `tools/parity/scene/build_character.py` `MESHES`, Learnings S8 and S9, and every place in `tools/` and `blender/` that lists the master tokens.

**Verified as the doc states:** the 19 Phase07 articles and their masters; one `Lips_Natural` and one `Nail_Natural` beside six `Skin_Fitzpatrick*`; `Hair_DarkBrown_Clean_Base_s001_v01` declares `Masked`; `MasterSet.md`'s Masked row carries *"a dedicated `Hair` master only if Masked hair looks wrong"*; `base_color_tint` is a frozen Creator port. **Not verifiable here:** everything in Pass 2 (the platform's live code is private). It is recorded as *reported by the platform, 2026-09-28*.

- **AP-F1 — A tint can only darken, so the one hair material cannot reach most hair colours as authored.** `base_color_tint` is a **multiply, 0–1 per channel** (`LCDSchema.md`, frozen). `Hair_DarkBrown` is authored at linear `(0.090, 0.052, 0.030)`, so tinting it gives only darker browns and black, never blonde, red or grey. *"Tint one hair material"* works only if that material is authored at the **lightest** hair colour and tinted down. The same limit applies to the fabrics: `Leather_Brown` `(0.16, 0.07, 0.03)` cannot become tan, and `Denim_Indigo` (a texture × the tint) cannot become a lighter wash. `Cotton_Jersey` `(0.78, 0.77, 0.74)` is already light, so it tints to any colour. **Bearing on AP-Q4:** Unreal's hair shading model takes a base colour *(from knowledge, not verified this pass)*, so a light base with a tint is the LCD-true route. A melanin parameter would be a MaterialX- and Blender-side convenience that each consumer converts back to a colour. The one physical cost is that a multiply changes only the albedo. Real dark hair differs from light hair in more than colour, because it transmits less light.
- **AP-F2 — A `Hair` master can be a settings-only master, which keeps the article on OpenPBR.** `MasterSet.md` defines a master as *a graph plus a settings block*, and CM-Q10 has already measured a settings-only question (the Subsurface method). The fibre highlight already rides `specular_roughness_anisotropy` (C3, Phase07 7.6). So A1's MaterialX side can **keep the article's OpenPBR graph under a new token**. Its settings row would be masked coverage, a *hair* shading model, and two-sided. Stock-viewer parity then holds by construction, and **AP-Q1's `chiang_hair_bsdf` probe stops gating A1**: it becomes a later quality question. **For discovery to argue:** D-E refused an `Eye` master under the LCD principle (*"if one target can do something the others can't, don't rely on it"*). The difference is that D-E refused **inputs** the other targets lack (iris depth). A settings-only `Hair` master adds no input; it is how one renderer shades the same article. **Also note:** the "plastic" finding is Unreal-side. The library's own Storm vs Blender hair measured ΔE 1.34 / 1.71 (Phase07 7.6), and Phase06's Unreal column has not reported yet. This fits the governing insight, since Unreal is the renderer that forces masters.
- **AP-F3 — Brows and lashes are the same article as the hair today.** `CHARACTER_CAST` binds `Hair_DarkBrown` to Hair, Brows and Lashes. Re-routing it to `Hair` moves all three. So AP-Q2 is really *"split the article or not"*. Colour does not force a split: each card mesh already gets its own Material instance for its cut-out map (P17), so brows can be tinted apart from the hair either way.
- **AP-F4 — The token set lives in more places than "the validator's".** The master tokens are listed in `tools/converters/assemble_mtlx.py` (`KNOWN_MASTERS`), `tools/validators/validate_material.py`, `tools/converters/recipe.schema.json`, `blender/masters/build_masters.py`, `tools/parity/scene/build_scene.py` and `tools/parity/JOB_FORMAT.md`, beside `MasterSet.md` §Master tokens. **"The Blender proxy" is retired:** `matter_proxy.py` was retired at Phase05 step 5.5, and the Blender side of a master is `blender/masters/build_masters.py`.
- **AP-F5 — A3 needs two corrections before it lands.**
  - **P16 carries three things, not two.** It is coat, fuzz **and `subsurface_scatter_anisotropy`** (skin; Storm ignores it, S8, but Blender honours it). Only `specular_roughness_anisotropy` becomes conditional on A1. Pass 3's *"P16 open for coat and fuzz only"* drops the skin input.
  - **P17's wording reads backwards.** Pass 2 says the cut-out map is *"carried from the article to the bound material"*. P17's map is the **mesh's** alpha, supplied at binding; the article's `cutout_tex` is empty by design (`LCDSchema.md` §Cut-out map, D1). Before marking P17 DONE, confirm that the platform supplies the mesh's map rather than copying something from the article.
- **AP-F6 — A2's pairing, the options measured.** (a) **Naming**: twelve new articles, `Lips_FitzpatrickI…VI` and `Nail_FitzpatrickI…VI`. The names fit the `Identity.md` grammar and its 63-character limit. But the platform would then parse names for a relationship, and a name is identity, not data. (b) **A field in the served catalog**: `serve_to_stage.py` already projects each article's `status` and `master` (Phase07 L4), so a tone-family key is the same pattern, and it follows R14's rule that release data carries what a consumer must not derive. (c) **One light lips / nail article and a tint per tone**: no new articles, but it needs a per-tone table, which the platform declined. The physics favours tone-matching both. Lip pigment follows skin melanin, and a nail's colour is mostly the nail bed seen through translucent keratin.

## Pass 6 — Wardrobe: what MakeHuman's CC0 garments are made of (2026-09-28)

**Why:** the lead framed the platform's need as *"refinement … to address wardrobe"*. Pass 1 says *"no new fabric is asked for now"*, so this pass checks that claim against the garments themselves.

**Examined:** the pinned `makehuman_system_assets_cc0.zip`, from the rig's cache (`library/parity/_sources/`, git-ignored). Its sha256 begins `b542127a8e25547c`, which matches the research's Pass 3 pin. Every garment's `.mhclo` and diffuse atlas was read and laid out on one contact sheet (a disposable probe in `/tmp`, torn down; the script is under §Reproduction). Also read: `build_character.py` `MESHES` and the Phase08 draft list (`260925_R_LibraryCoverage_FirstRelease.md`, the `synthetic/textile` rows).

**The CC0 wardrobe:** 12 outfits (`male_casualsuit01–06`, `female_casualsuit01–02`, `female_sportsuit01`, `female_elegantsuit01`, `male_elegantsuit01`, `male_worksuit01`), 6 shoes (`shoes01–06`) and a fedora (two meshes, one material).

- **AP-F7 — A garment is one mesh carrying several substances.** Each outfit is **one `.mhclo`, one `.mhmat`, one atlas** that holds a top **and** trousers, plus trims and buttons. Each shoe holds an upper, a sole, laces and a lining. **The rig already hit this:**
  - it splits `female_casualsuit01` into Shirt and Trousers with **hand-drawn UV rectangles** (`build_character.py`, the `Trousers` rect rule);
  - it binds **all** of `shoes01`, sole included, to `Leather_Brown`.

  So the platform's *"P15 delivered as meshes (… garments)"* means one mesh per **garment**, not per **substance**. The wardrobe inherits L1's question once per garment. Each outfit needs a **per-garment substance split** (a UV-region rule or face sets) before two fabrics can be bound. That split is garment-bound data, which makes it a **fit** (CM-Q6), not matter. Without it, one fabric covers both the shirt and the jeans.
- **AP-F8 — The substances in the wardrobe, and the library's coverage.** *Identified by eye from the albedo atlases; not measured.*

  | Substance | Seen in | The library today | Phase08 draft list |
  |---|---|---|---|
  | Cotton jersey (tees, trims) | casual outfits, sports top | `Cotton_Jersey` ✓ (light, so it tints) | — |
  | Denim, stonewashed (dark to light) | 6 outfits; the work overalls are lighter | `Denim_Indigo` ✓, one dark wash that cannot tint lighter (AP-F1) | row 3 |
  | Smooth leather (brown, black) | `shoes01`, `03`, `04` | `Leather_Brown` ✓; black by tint, tan impossible | `Leather_Natural` (row 9, a lighter base) |
  | **Rubber** (soles) | **every shoe** | — | `Rubber_Natural` (polymer row 1) |
  | Wool suiting | `male_elegantsuit01` | — | `Tweed` (row 5) is a wool, but not suiting |
  | Cotton twill / canvas (olive vest, cargo) | `male_casualsuit05`, work overalls | — | `Canvas` (row 2) |
  | Synthetic stretch knit (sport leggings) | `female_sportsuit01` | — | **not listed** |
  | Yarn-dyed stripe shirting / knit | `female_elegantsuit01`, `male_casualsuit03`, `05` | — | **not listed**; a woven stripe sits on the matter / pattern line |
  | Silk (tie) | `male_elegantsuit01` | — | `Satin` (row 12) |
  | Felt (hat) | fedora | — | `Felt` (row 7) |
  | Synthetic mesh and foam (trainers) | `shoes05`, `06` | — | `Nylon_Ripstop` (row 8) is the nearest |
  | Buttons, rivets (metal, plastic) | work overalls, elegant suits | `ABS_*` for plastic; no clean brass or steel | metal rows |

  **The Phase08 list's blockers are stale for textiles.** Its `C2` / `C2 + C3` status on Suede, Velvet and Satin predates Phase07, which built coat, fuzz and specular anisotropy (7.3, 7.6). Those rows are no longer blocked.
- **AP-F9 — Prints, trims, logos, fades and baked AO are garment-bound pixels.** Examples on the sheet: the tee's logo and orange trim, denim whiskers and fades, and the AO maps shipped with 11 of the 20 garments. Under D1 they are the garment's fit, not matter. The platform's own research put them in *"a garment overlay or mask over a tileable fabric"* (research Pass 2, item 4). That is **the same colour-on-layers need as makeup (CM-Q5)**, which Pass 1 moves out of the platform phase. **So a Phase 66 wardrobe built from substance articles renders plain garments:** a blue tee with no logo or trim, jeans with no fade. CM-Q5 now has five needs pointing at one contract change: makeup, region tone, freckles, dust colour, and garment prints.
- **AP-F10 — Fabric scale on a garment atlas.** A garment's atlas is its primary UV set, and S9 shows a second UV set is not an LCD option (Storm reads `st` for every index). The platform's per-mesh `uv_scale` stopgap (P18) is therefore what makes a 1 cm weave read at weave size on clothing. A garment atlas's islands differ in texel density, so one `uv_scale` per mesh is approximate. The rig avoids the problem by storing each part's UVs in metres.
- **AP-F11 — "Wardrobe per scene mark" splits cleanly.** Changing a garment means changing the mesh and its bindings, which is platform-side. Changing a garment's **colour** is `base_color_tint` on a fabric article, library-side, **provided the article is authored light** (AP-F1).

### Proposed additions to the asks (for the lead; not decided)

- **A5 — Wardrobe fabrics.** Pull forward the Phase08 textile rows the CC0 wardrobe uses, as Phase07 did with cotton, denim and leather: **Rubber** (every shoe needs it), **Canvas**, a **light Leather**, **Felt** and **Satin**. Add the two the draft list lacks: a **synthetic stretch knit** and a **wool suiting**. Author every tintable fabric **light** (AP-F1), and consider a lighter denim wash.
- **A6 — Who owns the per-garment substance split** (AP-F7): the platform, extending P15 from the body to garments, or a library fit set (CM-Q6). The rig's rect rule is a working example of the data either side would hold.
- **A7 — Garment prints and trims** (AP-F9): accept plain garments for Phase 66, or bring CM-Q5 (colour on layers) forward, which serves makeup at the same time.
- **A1, refined** (AP-F1, AP-F2): a settings-only `Hair` token over the existing OpenPBR graph, with the hair article **re-authored at a light base** so that one tint reaches every hair colour.

### Reproduction (the contact sheet)

Run on the rig's cached pack (re-fetch it at the research's Pass 3 pin if the cache is gone). Nothing in the repo is written.

```bash
mkdir -p /tmp/wardrobe_probe && cd /tmp/wardrobe_probe
unzip -o -q -j <repo>/library/parity/_sources/makehuman_system_assets_cc0.zip 'clothes/*_diffuse.png' -d .
cat > sheet.py <<'EOF'
from PIL import Image, ImageDraw
import glob
files = sorted(glob.glob("*_diffuse.png")); T, cols = 512, 5
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * T, rows * (T + 24)), "white"); d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB"); im.thumbnail((T, T))
    x, y = (i % cols) * T, (i // cols) * (T + 24)
    sheet.paste(im, (x, y + 24)); d.text((x + 4, y + 4), f.replace("_diffuse.png", ""), fill="black")
sheet.save("sheet.jpg", quality=85)
EOF
uv run --with pillow python sheet.py
```

## Open questions (for the library's discovery)

| # | Question | Why it matters | Library review (Passes 5–6) |
|---|---|---|---|
| AP-Q1 | Hair's MaterialX side: OpenPBR cards, or `chiang_hair_bsdf` (CM-Q3)? Does Storm render it? | Stock-viewer parity (A1) | **No longer gates A1** if the `Hair` token is settings-only over the OpenPBR graph (AP-F2); Chiang becomes a later quality probe |
| AP-Q2 | Do brows and lashes move to `Hair` too, or stay `Masked`? | They are hair fibre (`MasterSet.md` coverage line) | They are the **same article** today (AP-F3); the question is whether to split it |
| AP-Q3 | How is a tone's lips / nails pairing expressed — naming or a release field? | The platform's skin-tone control reads it (A2) | Three options measured (AP-F6); a served-catalog field follows the `status` / `master` precedent |
| AP-Q4 | Is `base_color_tint` alone the right hair-colour control, or does the Hair master want a melanin-style parameter (a vocabulary change)? | The lead's "one tinted hair material" | The tint works **only on a light base**; today's hair is dark and can only darken (AP-F1) |
| AP-Q5 | Who owns a garment's substance split: the platform (P15 extended) or a library fit set (CM-Q6)? | Every CC0 outfit is one mesh with several fabrics (AP-F7) | Open; the rig's rect rule is a worked example |
| AP-Q6 | Which wardrobe fabrics come forward from Phase08, and are the two missing from its list (stretch knit, wool suiting) added? | Rubber alone is on every shoe (AP-F8) | Open (A5) |
| AP-Q7 | Garment prints and trims: plain for Phase 66, or CM-Q5 brought forward? | Without it garments render plain (AP-F9) | Open (A7); a lead call |
| AP-Q8 | Does the platform's P17 supply the **mesh's** cut-out map, as P17 specifies? | Pass 2's wording says *"from the article"* (AP-F5) | Confirm before marking P17 DONE |

## Status

- **Passes captured:** 1–4 (2026-09-28, the platform's side): what the platform ruled, its row check, the asks
  (A1–A4), sequencing. **5–6 (2026-09-28, the library's review):** the asks checked against the tree (AP-F1–F6), and
  the CC0 wardrobe read garment by garment (AP-F7–F11).
- **Decided:** nothing here; the library's discovery rules the asks.
- **Asked of the library:** A1 (Hair master and hair article), A2 (tone-matched lips and nails), A3 (row reconcile).
  **Proposed by the review, not yet asked:** A5 (wardrobe fabrics), A6 (who owns a garment's substance split), A7
  (garment prints). **Recorded only:** A4 (a real tone control).
- **Current direction (the review's reading, not a ruling):**
  - A1 can be a **settings-only `Hair` token** over the existing OpenPBR graph, which keeps stock-viewer parity;
  - the hair article must be **re-authored light** for *"one tinted hair material"* to reach every colour;
  - A3 lands only after its two corrections (P16 keeps skin's scatter anisotropy; P17's source confirmed);
  - the wardrobe gap is **not** "no new fabric". It is the per-garment split (A6), five to seven fabrics (A5), and
    plain garments without CM-Q5 (A7).
- **Unverified, recorded as such:**
  - Storm's rendering of `chiang_hair_bsdf`;
  - how Unreal's hair shading model maps to the MaterialX hair parametrisation, and that it takes a base colour (from
    knowledge);
  - everything in Pass 2, which is the platform's report of its private code, 2026-09-28;
  - the wardrobe substances in AP-F8, which were identified by eye from albedo atlases.
- **Next step:** the lead reads A5–A7 and routes the set into a library phase (by `/discovery`). The platform builds its
  Hair master and skin-tone control in parallel. **One piece fits a single sitting:** A3's row reconcile in
  `PlatformDependencies.md`, with AP-F5's corrections, as a `/quick-fix` once AP-Q8 is confirmed.
