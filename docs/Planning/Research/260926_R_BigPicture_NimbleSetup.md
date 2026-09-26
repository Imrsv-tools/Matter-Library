# Research — The big picture: what the Matter Library is for, and the quickest way to get it working

**Opened:** 2026-09-26 · **Mode:** research. It gathers and commits to nothing. **Next:** the lead rules on the milestone sequence (§Status). The first phase then goes to `/discovery`.

**Question (lead, 2026-09-26, condensed):** "Phase 4 got too lost in some issues and I feel like this project is not flowing correctly… back up and look at the big picture of what the Matter Library is, the value it brings and assess the best way to get it up and running… we need to be way more nimble." The lead proposed this sequence and asked for review:
1. an **automated test rig** that renders an article in USDLiveView, Blender and Unreal under controlled settings, across the ranges of its parameters, and judges the results side by side;
2. an **AI generation loop** that runs at fixed times against a tracked wish-list, puts each material through the rig until it passes, then moves to the next one;
3. **library versioning** once many materials pass;
4. **library management**: add, remove and supersede materials in a release;
5. then **contribution, credit, usage tracking, and possibly a CMS**.

**Extends, does not replace:** `260923_R_StandaloneSetup.md` (R1–R16; seeds 5, 7, 8, 10), `260923_R_AgenticMaterialGeneration.md`, `260925_R_LibraryCoverage_FirstRelease.md` (the list), `260925_R_DraftsInUSDLiveView.md` (`serve_to_stage.py`), and the Phase04 and Phase05 docs.

---

## Resolved — lead decisions (2026-09-26)

| # | Decision |
|---|---|
| BP1 | **Unreal runs on another machine.** IMRSV Studio is not on the Linux box, where Blender 5.1 and the Stage runtime are. The UE leg of the rig runs remotely. |
| BP2 | **The UE leg is a bespoke UE project owned by this repo.** It carries Matter reference masters that mirror the master contract; it is not IMRSV Studio. This brings forward the Roadmap's *Unreal Reference Masters* (R14 "B later"). |
| BP3 | **Tools are judged against each other; no single renderer counts as the truth.** An article passes when Storm, Blender and UE agree within the per-master bar across the parameter sweep, and each render matches the recipe's own anchors (albedo, roughness, scale). An agent and the lead judge whether it *looks like the matter*. |
| BP4 | **Drafts keep `v01`; their state lives in a status field.** The lifecycle already exists (`draft → candidate → approved → deprecated → retired`, `_Architecture.md` §Versioning). Names never change on passing, so saved test compositions keep working. The v00 → v01 rename is not used. |

---

## Pass 1 — What the library is for, and what has actually been proven

**Examined:** `_Architecture.md`, `Readme.md`, `LCDSchema.md` (through the Glossary), `CompressedDistribution.md` §Parity, `tools/conformance/{codec_ab,render_leg_probe}.py`, `tools/generators/matter_proxy.py`, the Roadmap, and the tree (2026-09-26).

**The value, in one line:** *smart* materials. A creator can move the same few controls (tint, UV, wear-layer densities, roughness bias) in Blender, in an Unreal-based app, or in a USD viewer, and get **the same result** in each. A one-off material that looks right at a single setting in a single tool is not the product. The product is **agreement between tools across the controls' ranges**. The LCD, the master set and the ontology exist only to make that agreement possible.

**What is built (measured on disk):**
- 17 articles (`MatterLibrary/materials/**`) from 17 recipes, 40 texture files, and 9 shared wear layers.
- The structural gate (`run_all.py`, 16 lanes), the recipe → assembler path, the `/matter-generate` skill, the ambientCG importer, and the Physically Based lookup.
- A headless Storm preview (`make_preview.py`) and `serve_to_stage.py`, which serves the working tree to USDLiveView with live sliders.
- The full release lifecycle (stage, freeze, promote, activate) and one pilot release, `matterlib-0.1.0`.
- A Blender add-on and an Asset-Browser library.

**What has never been measured, and it is the value itself:**
- **Cross-renderer parity: no pair has ever been measured.** The ΔE2000 numbers in `CompressedDistribution.md` (Copper 0.69, Limestone 0.23, Concrete 0.43) come from `codec_ab.py`: **one renderer**, PNG against `.dds`. They measure codec loss, not agreement between tools. `render_leg_probe.py` shows only that each Creator scalar *changes* a Storm render.
- **The Blender form cannot pass a parity test by design.** `matter_proxy.py` says so: *"recognizable, not faithful"*, *"NO overlay-network recreation"*. The overlay and mask sliders are exposed but not wired, and TwoLayer (Rust) shows only its base layer. So the smart part of every layered article (8 of 17 today, and every new one under ruling C1) does nothing in Blender.
- **There is no Unreal leg we control.** The UE masters live in the private IMRSV plugin. They are legacy-authored and run under UE's automatic Substrate conversion (StandaloneSetup Q11). No UE install is on this box.

**Finding:** the project has built the **producer machinery** (grammar, gates, releases, freezes, approvals) in depth. Its **central claim**, that articles behave the same across tools, is still untested. That is why the lead's instinct to build the rig first is right: it tests the claim everything else depends on.

## Pass 2 — Where the flow broke (Phase04 as the specimen)

**Examined:** the Phase04 and Phase05 docs, the coverage research's Status and Gut-check sections, and `git log` since 2026-09-23.

**Volume, measured:** 81 commits and about 48,000 words of planning and research docs since 2026-09-23. In that time the library went from 12 to 17 articles.

**The pattern, three times:**
1. **Release machinery sits inside the content loop.** Phase04 was a content fix: wear layers sampled at their own size. Because the fix changed textures that the pilot `matterlib-0.1.0` hash-locks, `release_verify` failed. The phase then needed a re-freeze and a re-approval, and the re-freeze needed a `.dds` encoder that is missing from this box (L1). The pilot is a release **nobody consumes** (R7). The execute rule "gates are frozen" then blocked the phase's own seam and size guards. **A 90-minute content fix was held up by a release nobody uses.**
2. **Design flaws are found one article at a time, late.** The layer-scale defect surfaced only after about 5 articles had been reviewed by eye in Phase03. Phase04's own open hypothesis, *"Dust01 and Scratches01's content was tuned at about 10 cm, so the tag may be what is wrong"*, is exactly what a mechanical scale check would answer. With no rig, every structural question costs a phase.
3. **Decisions are asked for before they bite.** The coverage list (173 rows) waits on 14 naming and structure rulings (N1–N8, S1–S6) before anything is generated. Most only matter for a handful of rows, and each already has a recommended default applied in the draft.

**Finding:** the method is not wrong, but it is applied at the wrong **altitude**. Phases and release ceremony suit *building tools*. Filling a library is a **loop**: generate, test, fix, keep. The loop should run without opening a phase per batch or touching a release. *(A process observation for `/retro` → `/workflow-refiner`. This verb does not edit the method.)*

## Pass 3 — The lead's sequence, reviewed

**Verdict: the order is right.** Rig → generation loop → versioning → management → community is the correct dependency order. The rig validates the master set, the LCD and the ontology **before** 170 articles are built on top of them, so a Phase04-style design change costs one proving set rather than the whole library.

**Five adjustments:**

1. **Start the rig on a proving set of about 6 articles, not the whole library.** One per master family, plus layered and TwoLayer cases: `GreyCard_Neutral18` (calibration), `Copper_Verdigris_Aged` (metal, layered), `Oak_Natural` (scan, layered), `Rust_OnSteel_Flaking` (TwoLayer), `Glass_Clear` (transmission), `Lace_Floral` (Masked), `Neon_Signage` (Emissive). When the rig and the proving set agree, the structure is validated. Generation at volume comes after that.
2. **A faithful Blender form is the rig's biggest hidden item.** Today's proxy would fail every layered article. The architecture already names the fix: *"masters are where per-target gaps are bridged."* So Blender needs **Blender masters**, one node group per master that mirrors the MaterialX graph including the overlay and mask network. The UE side needs the same. A cheaper path may exist and should be probed first: Blender 5.1's USD importer (`import_materials` is present; the fidelity of its MaterialX graph import is **unverified**). *(This supersedes part of the Parking-lot item "automated transformers, after manual parity is proven". The item is kept, not deleted: the masters **are** the hand-built transformer.)*
3. **The UE leg is a remote runner (BP1, BP2).** A bespoke UE 5.8 Substrate project in this repo holds reference masters that mirror `MasterSet.md`, plus a script that builds a material instance from an article's `.mtlx` by its master token, which is what Stage does for Studio. It is run headless on the UE machine (UE's command-line editor with a Python script and a fixed-camera capture) and returns PNGs. *How* the agent reaches that machine is open (Q-C). Fallback: the lead runs one command there per batch.
4. **Take the release out of the content loop until the first real release (M4).** The pilot `0.1.0` should not gate content work. Its lanes skip, or the pilot is marked `Reevaluate`, until the first real release is cut from `approved` articles. *(Don't Delete: the machinery stays; it just stops running in the loop.)*
5. **Resolve naming rulings on contact, not up front.** The loop uses the draft's recommended defaults. A ruling is asked for only when the loop reaches a row it affects, and before that row reaches `approved`. Names are cheap until a release.

**On the lead's other points:**
- **"Work directly in the library structure":** agreed, and BP4 makes it clean. Articles live at their real path from the first draft, `serve_to_stage.py` already serves them, and the status field says how far along each one is.
- **"At fixed times, not always running":** this fits **local** scheduling (cron on the Linux box running a headless agent against the queue). **Cloud routines can't reach** Blender, Stage, the GPU or the UE machine.
- **"Perhaps not pass/fail but ranges":** agreed, and it is the right shape (Pass 4). Each control gets a **response curve** per tool. The report says where the tools diverge (*"overlay1_density agrees to 0.6; above that Blender is 3 ΔE brighter"*), not just a verdict.

## Pass 4 — The rig, sketched (a design hypothesis for `/discovery`, not a plan)

**Scene contract (identical in every tool):**
- **Geometry:** a UV sphere (highlight shape → roughness and specular); a rounded cube (edges → edge wear, normals); a **1 m plane with a 10 cm ruler**, so scale is judged against something of known size; a backplate checker behind see-through matter.
- **Lighting and colour:** one pinned HDRI plus one key light, fixed exposure, the OCIO parity config (`build_ocio_parity_config.py`, already built), a Standard view transform, and fixed resolution and camera.

**Parameter sweep:** each Creator port is moved on its own from the article's defaults across its LCD range (densities 0 / .25 / .5 / .75 / 1; `roughness_bias` −.5 → +.5; tint through 3 colours; UV scale .5 / 1 / 2, rotation 0 / 45 / 90, offset). Then a few combinations (all layers at 1). That is about 25 renders per tool per article.

**What each check validates:**

| Criterion | How it is measured | Catches |
|---|---|---|
| Colour | ΔE2000 on the flat-lit card region; mean albedo against the recipe's Physically Based anchor | wrong colour space, tint math |
| Scale | Feature period on the ruler plane (FFT or autocorrelation) against `meters_per_tile` and each layer's tag | Phase04-class scale defects, including the Dust/Scratches hypothesis |
| Roughness / specular | Highlight width and peak on the sphere | roughness remapping between tools |
| Normals / relief | Shading variance, and the sign of the relief under the key light | the OpenGL-vs-DirectX green-channel flip, a classic Blender↔UE bug |
| Metalness / Fresnel | The edge-to-centre ratio on the sphere | F0 and F82 gaps |
| Transmission / opacity | Checker visibility through the article | Storm's transmission limits; cutout differences |
| Emission | Luminance at fixed exposure | emission units |
| Control response | A metric per sweep step, per tool: is the curve monotonic, and do the curves' slopes agree | sliders that do nothing (the Blender proxy today), clamps, different ranges |
| Mask gating | Overlay density where the mask is 0 against where it is 1 | gate channel mapping |
| UV transform | Pattern registration after scale, offset and rotation | pivot and sign conventions (they differ between tools) |
| Seams | Wrap-edge difference against interior difference | non-tiling textures (the Phase04 guard, reused) |

**Output per article:** a **contact sheet** (columns are tools, rows are sweep steps), a **scorecard** (per criterion, per port: the worst cross-tool ΔE and the value where it crosses the per-master bar), and response-curve plots. An agent reads the contact sheet against a short rubric ("reads as the matter", "scale looks right against the ruler"), and the lead looks at a sheet, not a scene.

**Bars:** the per-master bars that already exist (ΔE < 2 for Opaque, Masked and Emissive; "recognisable" for transmission and subsurface, Decision of record 9).

**Tools per leg:**
- **Storm:** `usdrecord`, the same renderer as USDLiveView, headless. It exists.
- **Blender:** `blender -b` with a Matter test `.blend` and the Blender masters. Cycles for the parity render; EEVEE optionally, as creators preview in it.
- **UE:** the remote runner (Pass 3 item 3).

## Pass 5 — Proposed milestones (the answer)

Each milestone has a user-facing outcome and maps onto Roadmap entries that already exist. Nothing below is committed. Numbering and order are the lead's.

| Milestone | Outcome | Absorbs | Size |
|---|---|---|---|
| **M0. Land Phase04 on content** | Wear layers are the right size, and the phase is closed | Phase04. The pilot re-freeze is dropped: L1 becomes moot under Pass 3 item 4 | hours |
| **M1. Parity rig: Storm + Blender** | For any article, see Storm and Blender side by side across every slider, with a scorecard | *Parity Baselines*; the Blender masters (Pass 3 item 2); the Blender MaterialX-import probe first | a phase |
| **M2. Parity rig: the UE leg** | The same sheet with a third column from our own UE project | *Unreal Reference Masters* (BP2) | a phase |
| **M3. The generation loop** | The library fills itself in scheduled batches; the lead reviews sheets, not scenes | Phase05 *Library Coverage*, re-cut as a loop over a tracked queue (the coverage list as data) | a small phase, then a loop |
| **M4. The first real release** | Creators install a versioned release of `approved` articles | *Release Bundle and Consumer Contract*; *Blender from a Release*; *IMRSV Consumes Releases* | a phase |
| **M5. Library management** | The maintainer adds, supersedes and retires articles between releases in minutes | *Version Management*; *Author a Material End to End* (the Matter Manager) | a phase |
| **M6. Community** | Outsiders contribute and get credit; usage is visible; perhaps a CMS | *Contribution Path*; *See the Library*; the Parking lot's scoring and reputation | later |

**M1 and M2 can overlap.** The UE project's masters can be built while the Blender masters are, since both mirror one `MasterSet.md`.

**Rig before loop, strictly.** The loop's "passes the rig" condition is the rig. Generating before the rig exists repeats Phase03 → Phase04: design flaws found article by article.

---

## Open questions

| # | Question | Recommendation |
|---|---|---|
| Q-A | Close Phase04 on its content fix and **drop** the pilot re-freeze (L1 moot; the pilot's release lanes skip until M4)? | Yes |
| Q-B | Blender's faithful form: probe Blender 5.1's USD MaterialX import first, then build hand-made Blender masters only if the import falls short? | Yes, probe first (about an hour) |
| Q-C | How does an agent reach the UE machine: SSH over Tailscale, a runner the lead starts, or files the lead carries across? And which OS is it? | A pull-based runner (the UE machine pulls, renders, and writes PNGs back) |
| Q-D | Where does the queue live? The coverage list as a tracked data file (for example `library/queue.yaml`) that the loop reads and updates with status | A tracked data file; the research table stays as history |
| Q-E | The proving set: are the 7 in Pass 3 item 1 right? | As listed |
| Q-F | Where do rig outputs live? Images in gitignored scratch, with a small tracked scorecard beside each article or recipe? | Yes; the images are rebuildable |
| Q-G | The status field (BP4): in the recipe and the `.mtlx` `imrsv_metadata`, so the loop, `serve_to_stage.py` and USDLiveView can all see it? | Both (the recipe is authored; the `.mtlx` carries it through) |

**Unverified (to verify before building on it):** Blender 5.1's MaterialX-in-USD import fidelity · UE 5.8 headless capture of a Substrate material on the UE machine · whether USDLiveView surfaces a status field.

## Status

- **Passes captured:** 5 (2026-09-26).
- **Lead rulings:** BP1–BP4 (UE is on another machine; a bespoke UE project; tools judged against each other; `v01` plus a status field).
- **Direction:** the lead's sequence holds. The central claim (smart materials behave the same across tools) has never been measured, and the Blender form cannot pass it by design. So **M1, the Storm + Blender rig on a proving set, is the next real work**, after closing Phase04 on content. Release machinery leaves the content loop until M4.
- **Open:** Q-A to Q-G, each with a recommendation. Nothing is blocked on them except the M1 kickoff.
- **Process note for `/retro`:** filling a library is a loop, not a sequence of phases. Keep release gates out of content work pre-release. Ask naming rulings on contact. *(For the Workflow Refiner; not edited here.)*
- **Next step:** the lead rules on the milestones and Q-A. Then close Phase04 through `/execute`, and open `/discovery` for M1 with the Blender import probe as its first act. **A deliberate gate, not a slide:** no Roadmap entry is changed by this doc.
