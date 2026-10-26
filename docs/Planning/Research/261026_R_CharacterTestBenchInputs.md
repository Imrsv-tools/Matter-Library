# Research input — a shared character test bench, and what it asks of the library

**Opened:** 2026-10-26 · **Mnemonic:** `CTB` (ids `CTB-n`, `CTB-Qn`) · **Mode:** research input from the Open Morphology Foundation (OMF). It commits the library to nothing; the library's own discovery rules each ask.
**Origin:** OMF research `261026_R_CharacterTestBench.md` (OMF `.ai/planning/research/`), which holds the method, numbers and sources. The lead's direction, verbatim: *"we can also inform those various repos of imprvement to streamline flows... they are us and we are them... so we shoudl refine to make them great"*, and *"3) Yes"* to handing the per-repo improvements over as input docs.
**Public-repo note.** Only what the library needs is here: no platform paths, ruling ids or private facts.
**Measured at:** this repo's `4438c1f` (2026-10-26).

---

## What the bench is (one paragraph)

The bench is one test flow for a character, built from three parts:
- **shape**: the body, made by OMF from a person's measurements;
- **surface**: skin, eyes and layers, from this library;
- **render**: the app's look-dev settings.

Each round changes one of the three and holds the other two fixed. A fixed cast of eight people (six adults from a public anthropometric survey, two children) is built every round. Each character gets **one scorecard row**: automatic checks (contract, measurement error, plausibility, pose deformation), the same fixed camera stills, and **one verbatim lead verdict**. That is the shape of this library's own batch records, so the row format is borrowed from here.

## What it found that matters to the library

- **CTB-1 — One body is shared.** OMF's body cage is MakeHuman hm08, vertex for vertex (13,348 of hm08's 13,380 body vertices; the 32 left are eyelid vertices). So OMF can hand over **differently shaped hm08 bodies with hm08's own UVs**, and every fitted article here (the `MakeHuman_Body_v01` skins, lips and eyes) applies to them unchanged.
- **CTB-2 — Those bodies exist now.** OMF's first spike made 16 of them: 8 people × 2 shape methods, as full hm08 `base.obj` files (19,158 v, MakeHuman's own faces, UVs and groups). They are in OMF's gitignored `data/external_not_committed/character_bench/`, available on request.
- **CTB-3 — hm08 is the test body, not the final one** (the lead's ruling, 2026-10-26). Measured on hm08 at 1.75 m with the 2048 atlas, the ears, lips and hands are several times too coarse:

  | Region | Median edge | Texture density |
  |---|---|---|
  | ears | 3.3 mm | ≈17 px/cm |
  | lips | 2.8 mm | ≈15 px/cm |
  | hands | 4.0 mm | ≈12 px/cm |
  | whole body | — | ≈12 px/cm |

  The recommended future is **two levels**: an hm08-class cage for identity, fit and garments, plus a **regionally dense render mesh** bound to it, with **its own UV layout** (head on its own 4K or a UDIM; enlarged ears, hands and lips).

## The asks (each is the library's to rule)

| Id | Ask | Why |
|---|---|---|
| **CTB-Q1** | **Author skins in 3D or on the cage, and treat each UV-space map as a baked cache, as a rule from now on.** No map painted directly in hm08 UV space. | A new render mesh then costs a re-bake (a re-run) instead of a re-paint. A painted map moved between layouts loses detail, and nobody publishes how much. The synthetic-skin pipeline (`261026_R_SyntheticSkinAndEyes.md`, *"maps are authored in 3D"*) already leans this way; this asks to make it the rule. |
| **CTB-Q2** | `tools/parity/rig.py --character --body <hm08 obj/usd>`: the same UVs, any shape. | Today the character scene is pinned to one hm08 *shape*, so a skin is never judged on a heavy, small, male, female or child body. Because the UV hash is unchanged, this needs no new `PART_MESHES` entry. |
| **CTB-Q3** | Plan for a **`Body_v02` part mesh** (the render mesh) when it exists: its own UV hash and kit. Fit-set pictures are re-baked from the 3D-authored sources. | The library already says *"a version is a UV layout"*; this names the expected next version early. |
| **CTB-Q4** | Record bench verdicts in the **batch-row form** (Verdict line + verbatim Review line). | It lets a verdict made on a character in the app be read here, and the reverse. |

### The lead's answer (2026-10-26)

On OMF's question *"Make 'author skins in 3D or on the cage, bake per UV layout' a Matter Library rule now?"* the lead answered **"yes"**.
- **CTB-Q1 is lead-ruled.** The library writes it into its own skin-maps authoring spec at its next skin session, in its own words.
- In the same answer, the lead adopted the **two-level body** (cage + regionally dense render mesh) as OMF's base-mesh strategy. So CTB-Q3's `Body_v02` is now expected, not hypothetical.

## What the library can send back

Its judgement of the synthetic skins **on the bench's cast**, rather than on the single default shape; and, once CTB-Q1 is ruled, the bake step's inputs, so OMF's render-mesh work knows what it must carry.

## Pass 2 — The library's review of the four asks (2026-10-26, on the machine with Unreal)

**Asked by the lead,** verbatim: *"There was lots of reserach today about the look of characters, skins etc including feedback from OMF and som test skins... can you look into this and lets prepare to share the tests that will come int"*.
**Examined:**
- OMF's `261026_R_CharacterTestBench.md` **read at OMF's origin `4e8f558`**. This machine's OMF clone was 1,062 commits behind; it was fetched, not pulled.
- The platform's own input doc on the bench, read at its origin the same day.
- `tools/parity/scene/build_character.py`, `tools/parity/job.py`, `tools/parity/drivers/unreal.py`, `tools/converters/groups.py` (`PART_MESHES`), `gen_skin_maps.py`, `gen_synth_skin.py`, `docs/specs/Authoring/SkinMaps.md`, the batch summary form (`/matter-batch` §6) and `library/batches/`.

**Since Pass 1, on OMF's side (2026-10-26):**
- The bench's child-body defect is fixed (OMF's own quick-fix). All eight first-generator bodies now pass its pose check.
- **The render face's expressions come from ICT-FaceKit** (MIT, scan-built), ruled by the lead. That is OMF's and the platform's; it asks nothing of the library.

- **CTB-4 — The ids collide across the three docs; quote an ask by content.**
  - This doc's CTB-Q1 … Q4 are not the platform input doc's CTB-Q1 … Q6: there, Q1 is the platform's article builder.
  - Nor are they OMF's `F-CTB-n` findings.
  - **Watch word:** in this repo **scorecard** already means the rig's per-part ΔE file (`library/parity/<run>/scorecard.md`). OMF's "scorecard row" is a different thing, so here it is **the bench's row**.
- **CTB-5 — CTB-Q1 (ruled): what the rule changes on disk.**
  - **The spec still says the opposite in one place.**
    - `SkinMaps.md` defines a map as *"drawn on the approved human mesh's UV layout"*.
    - Its *How to make one* offers a contributor path: *"Your own picture, painted (or made) as the absolute skin colour on hm08's atlas"*.
    - The ruling is owed to that spec in the library's own words. It is a durable spec, so it lands by a **lead-directed `/quick-fix`**, not from here.
  - **Neither skin maker is layout-free yet.**
    - `gen_skin_maps.py` (the six shipped maps) and `gen_synth_skin.py` (the test set) both work in 3D: each texel's position and normal, noise in 3D, anatomy from hm08's joint helpers.
    - But **both read six pictures drawn in hm08's UV space**: MPFB2's face, lips, ears, eyelids and areolae masks, and the thickness map `sss.png` (`gen_synth_skin.py` loads them as `masks` and `sss`).
    - So a re-bake onto another layout first needs **those six carried onto the body**. One way is to sample each at every hm08 vertex: as vertex weights they ride the cage to any layout.
    - **That is the bake step's input list OMF asked for** ("What the library can send back"): the body's 3D positions and normals, hm08's joint helpers, and these six region fields.
  - **Q-CTB-5 — Does the rule bind a contributor's painted picture?** (the lead's)
    - The spec's contributor path is a picture made on hm08's atlas, and a community painter has nothing else to paint on.
    - **Recommendation:** keep accepting it, **recorded as bound to its layout**: it fits `MakeHuman_Body_v01` only and is not carried to the next body. The library's own makers follow the rule.
- **CTB-6 — CTB-Q2 (`rig.py --character --body`): one sitting, with two readers to carry it.**
  - **The pattern exists.** `build_character.py --hair <style> --out <path>` already writes a variant character scene and leaves the rig's committed scene alone.
  - **What follows the body for free:**
    - eyes, teeth, tongue, hair, brows and lashes are fitted onto the body's vertices (`fit_proxy` over MakeHuman's `.mhclo`);
    - the cameras are framed from the body's measured bounds, so a child is framed as an adult is.
  - **What must carry it:**
    1. **Storm** reads the scene file (`job.CHARACTER_SCENE`, sub-layered into every character job).
    2. **The Unreal column builds its own mesh.** It calls `build_character.load_parts()` (`drivers/unreal.py`), so the body has to travel in the job, not only in a scene file.
    3. **Four makers share `load_parts` / `source`** and must not see the bench body: `make_kits.py`, `gen_skin_maps.py`, `gen_synth_skin.py`, `gen_fit_makehuman.py`.
  - **The check is already there.** A bench body must carry `MakeHuman_Body_v01`'s layout hash (`make_kits.layout_sha256`), and `--body` refuses any other, as a kit does.
  - **Not on this machine.** OMF's 16 bodies sit in OMF's git-ignored `data/external_not_committed/character_bench/` on the machine that made them; this machine's OMF clone has no such folder. They are OMF's and stay out of this public repo. **The hand-over is a copy into the same path in this machine's OMF clone**, so one path names them on both machines.
  - **What it gives and doesn't:** a skin seen on that shape in Storm and Unreal, plus Blender on the library machine. The rig compares tools. **Judging the skin on the body stays the lead's.**
- **CTB-7 — CTB-Q3 (`Body_v02`): nothing to build until the mesh exists.**
  - The library already treats a new layout as a new part mesh (`PART_MESHES`, *Mesh version*).
  - **The cost when it comes:**
    - a `PART_MESHES` entry with its layout hash and kit (`make_kits.py`);
    - the rig's character scene for it;
    - the maps re-made by the makers, once CTB-5's six region pictures are on the body;
    - the recipe gate's G8 against the new hash.
  - OMF seeded the render-mesh work on its own Roadmap. **The library seeds nothing until that mesh has a layout.**
- **CTB-8 — CTB-Q4 (the batch-row form): the form exists, but the review page cannot take the test set.**
  - A batch summary row ends in **Verdict** (the tools' agreement) and **Review** (the lead's words, verbatim): `library/batches/<batch>.md`.
  - `review_pages.py` and `wishlist.py keep / redo` work on **wish-list rows**. The 25 synthetic drafts are not rows (`library/wishlist.yaml` has no `Synth`), so their verdicts are recorded on rows of that form in `261026_R_SyntheticSkinAndEyes.md` Pass 4.
  - **A bench row coming from OMF or the platform** names the article stem, the body and the lead's words verbatim. The library copies the words onto its row with the date, by content.
- **CTB-9 — No ledger row.** `PlatformDependencies.md` holds asks between the library and its **consumers** (its own header). OMF is a sibling producer, and its asks here are the library's own tooling.

## Resolved

- **2026-10-26 — CTB-Q1, ruled "yes" by the lead** on OMF's question *"Make 'author skins in 3D or on the cage, bake per UV layout' a Matter Library rule now?"*. Owed: the rule in `SkinMaps.md` (CTB-5), by a lead-directed `/quick-fix`.
- **2026-10-26 — the two-level body** (an identity cage + a regionally dense render mesh with its own UV layout), adopted in the same answer as OMF's base-mesh strategy. For the library this makes `Body_v02` expected (CTB-7).

## Status

- **Passes:**
  - Pass 1: the input as written from OMF's side.
  - Pass 2: the library's review of the four asks.
- **Ruled:** CTB-Q1 (see Resolved).
- **Owed:**
  - the CTB-Q1 rule in `SkinMaps.md`, by a lead-directed `/quick-fix` (CTB-5);
  - the bench bodies copied to the machine with Unreal, OMF's side (CTB-6).
- **Open:**
  - Q-CTB-5, the contributor's painted picture (the lead's);
  - CTB-Q2, `rig.py --character --body`: one sitting, offered as a `/quick-fix` (CTB-6);
  - CTB-Q3, waits for the render mesh (CTB-7);
  - CTB-Q4, answered by the rows in `261026_R_SyntheticSkinAndEyes.md` Pass 4 (CTB-8).
- **▶ Next:** the lead's pick among the offers; the test set's first look (`261026_R_SyntheticSkinAndEyes.md`).
