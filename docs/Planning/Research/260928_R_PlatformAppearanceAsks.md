# Research — What the platform's Appearance work needs from the library

**Opened:** 2026-09-28 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
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

## Open questions (for the library's discovery)

| # | Question | Why it matters |
|---|---|---|
| AP-Q1 | Hair's MaterialX side: OpenPBR cards, or `chiang_hair_bsdf` (CM-Q3)? Does Storm render it? | Stock-viewer parity (A1) |
| AP-Q2 | Do brows and lashes move to `Hair` too, or stay `Masked`? | They are hair fibre (`MasterSet.md` coverage line) |
| AP-Q3 | How is a tone's lips / nails pairing expressed — naming or a release field? | The platform's skin-tone control reads it (A2) |
| AP-Q4 | Is `base_color_tint` alone the right hair-colour control, or does the Hair master want a melanin-style parameter (a vocabulary change)? | The lead's "one tinted hair material" |

## Status

- **Passes captured:** 1–4 (2026-09-28) — what the platform ruled, its row check, the asks (A1–A4), sequencing.
- **Decided:** nothing here; the library's discovery rules A1–A3.
- **Asked of the library:** A1 (Hair master + hair article), A2 (tone-matched lips and nails), A3 (row reconcile).
  **Recorded only:** A4 (a real tone control).
- **Unverified, recorded as such:** Storm's rendering of `chiang_hair_bsdf`; how Unreal's hair shading model maps to the
  MaterialX hair parametrisation.
- **Next step:** the lead routes A1–A3 into a library phase; the platform builds its Hair master and skin-tone control in
  parallel.
