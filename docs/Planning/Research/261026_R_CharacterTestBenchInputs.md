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

## What the library can send back

Its judgement of the synthetic skins **on the bench's cast**, rather than on the single default shape; and, once CTB-Q1 is ruled, the bake step's inputs, so OMF's render-mesh work knows what it must carry.

## Status

- **Passes:** 1, the input as written from OMF's side.
- **Next:** the library's own review of these asks, a later pass, as with earlier input docs.
- **Open:** CTB-Q1 … Q4.
