# Research — The big picture: what the Matter Library is for, and the quickest way to get it working

**Opened:** 2026-09-26 · **Mode:** research. It gathers and commits to nothing. **Next:** `/discovery Phase05` on this machine (§Status).

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
| BP5 | **Phase04 is closed on its content fix** (lead, 2026-09-26: "Closing P4 now"; `a383e86`). The proposed sequence (Pass 5) is accepted as the working plan. |
| BP6 | **The UE machine runs Linux, and an agent can work there with its own clone of this repo.** Git is the channel between the two machines. This machine does everything it can; the UE work happens there. |
| BP7 | **The UE leg is a standalone packaged runtime,** not an editor-driven project. It is built on the UE machine, then runs headless on any Linux machine with a GPU, this one included (Pass 7). |
| BP8 | **"You build them."** The agent makes the materials by whatever works: measured values, free scans, code-generated textures, image-generation models. **Licensing and provenance do not block the seed library** (lead, 2026-09-26: "we are trying to prove a concept"). The tools keep noting where each texture came from automatically; nothing is added on top. This unparks what earlier docs called "generative imagery". |
| BP9 | **Phase05 and Phase06 are seeded, and they run one after the other, not in parallel** (lead, 2026-09-26: *"we can do all of Phase 5 here, commit and push, then I can move to the other system for Phase 6, and once we have the UE runtime we can move back here for phase 7 and on"*). Library Coverage is renumbered Phase05 → Phase07. |

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
4. **Take the release out of the content loop until the first real release (the first release).** The pilot `0.1.0` should not gate content work. Its lanes skip, or the pilot is marked `Reevaluate`, until the first real release is cut from `approved` articles. *(Don't Delete: the machinery stays; it just stops running in the loop.)*
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

## Pass 5 — Proposed phases (the answer)

Each proposed phase has a user-facing outcome and maps onto Roadmap entries that already exist. Nothing below is committed. Numbering and order are the lead's.

| Phase | Outcome | Absorbs | Size |
|---|---|---|---|
| **Phase04. Land it on content** | Wear layers are the right size, and the phase is closed | Phase04. The pilot re-freeze is dropped: L1 becomes moot under Pass 3 item 4 | hours |
| **Phase05. Parity rig: Storm + Blender** | For any article, see Storm and Blender side by side across every slider, with a scorecard | *Parity Baselines*; the Blender masters (Pass 3 item 2); the Blender MaterialX-import probe first | a phase |
| **Phase06. Parity rig: the UE leg** | The same sheet with a third column from our own UE project | *Unreal Reference Masters* (BP2) | a phase |
| **Phase07. The generation loop** | The library fills itself in scheduled batches; the lead reviews sheets, not scenes | *Library Coverage* (then numbered Phase05), re-cut as a loop over a tracked queue (the coverage list as data) | a small phase, then a loop |
| **Later. The first real release** | Creators install a versioned release of `approved` articles | *Release Bundle and Consumer Contract*; *Blender from a Release*; *IMRSV Consumes Releases* | a phase |
| **Later. Library management** | The maintainer adds, supersedes and retires articles between releases in minutes | *Version Management*; *Author a Material End to End* (the Matter Manager) | a phase |
| **Later. Community** | Outsiders contribute and get credit; usage is visible; perhaps a CMS | *Contribution Path*; *See the Library*; the Parking lot's scoring and reputation | later |

**Phase05 and Phase06 can overlap.** The UE project's masters can be built while the Blender masters are, since both mirror one `MasterSet.md`.

**Rig before loop, strictly.** The loop's "passes the rig" condition is the rig. Generating before the rig exists repeats Phase03 → Phase04: design flaws found article by article.


## Pass 6 — The lead's second round (2026-09-26)

**Answers:** Phase04 is closed (BP5). The UE machine is Linux with an agent (BP6). The UE leg is a standalone runtime (BP7). The agent builds materials by any means, and licensing doesn't block (BP8). The lead also said plainly that the process vocabulary is getting in the way: *"I don't know the magic words you are using here… how many times do I need to say stop with the bureaucracy."* **From here this doc uses plain words:** "tools" for Blender, UE and USDLiveView; "sliders" for the Creator controls; "ways to make a material" instead of lanes.

**What this settles:** Q-A (yes, done) · Q-B (probe Blender's import first) · Q-C (an agent on the UE machine, git between the two). **A new simplification:** both machines are Linux, so the UE runtime is built and run natively. No cross-compiling, and the same package runs here.

## Pass 7 — The Matter UE runtime (what it is, and what is hard)

**What it is:** a small packaged Unreal 5.8 app (Substrate on) that does one job. Given a material's `.mtlx`, a list of slider settings and the test scene, it renders one PNG per setting and exits. No editor, no window. It is the third column of the rig, and it doubles as the public Unreal reference the Roadmap already wanted (*Unreal Reference Masters*).

**What goes inside it:**
- **The 7 masters, built in Unreal to mirror `MasterSet.md`.** Every input a material can set (textures, colours, the slider values, the wear-layer sizes from Phase04) is a parameter on the master. A packaged app can't compile new shaders, so everything must be a parameter; that is already what a master *is*.
- **A loader.** It reads the `.mtlx` (plain XML): which master to use, which textures, which constant values, and the default slider values. It loads the PNGs as textures at runtime and sets them on an instance of the master. IMRSV does the same thing privately; this is our public version.
- **The test scene** (Pass 8) and a fixed camera. It renders the whole slider sweep in one launch, so the load cost is paid once.

**Built only on the UE machine, and run anywhere:** writing the masters (ideally by an editor script that reads `MasterSet.md`'s data, so they can be rebuilt rather than hand-clicked) and packaging. After that, the package is copied to any Linux GPU box, this one included. The package is hundreds of MB, so it lives outside git (a release download, or copied across).

**Where it is likely to hurt (check each early, on the UE machine):**
- **Texture settings at runtime.** Colour textures must load as sRGB and data textures (roughness, normals, the wear layers) as linear. The normal-map green channel must be the right way up. These are the classic reasons Blender and Unreal disagree; the rig's normal and colour checks exist to catch them.
- **Repeatable frames.** Auto-exposure, temporal anti-aliasing and Lumen noise change a render from frame to frame. Turn auto-exposure off, let frames settle before capture, or use Unreal's path tracer for the parity renders.
- **Substrate in a packaged Linux (Vulkan) build.** Expected to work, but **unverified**. It is the first thing to prove with a single grey sphere.
- **Capture without an editor.** The editor's movie-render tools don't ship in a packaged app. The runtime reads the frame back itself and writes the PNG.

**The order on the UE machine:** grey sphere in a packaged build → one master and one material loaded from `.mtlx` → the sweep → all 7 masters. Parity numbers can come from the editor build while the packaging is sorted out; the editor is the development loop, and the package is the deliverable.

## Pass 8 — One plan, two machines

**The seam that makes this work: a render job.** The rig defines one simple job format: *this material, these slider settings, this scene, write PNGs here*. Each tool gets a small driver that takes a job and returns PNGs: Storm (here), Blender (here), and the UE runtime (built there, run anywhere). The comparison, contact sheets and scorecards never care which tool made a picture. So the rig is built here first with an empty UE column, and the column fills in when the runtime arrives.

**The scene is authored once.** A USD file holds the geometry (a sphere, a rounded cube, a 1 m plane with a ruler), the camera and the lights. Storm reads it directly, Blender imports it, and the UE runtime has it built in from the same file. **The lighting is calibrated before any material is judged:** the grey card, the UV grid, and a plain grey sphere must match across the tools first. Otherwise every material fails for reasons that aren't the material's fault. The grey card and UV grid articles already exist for exactly this.

**What happens where:**

| This machine (now) | The UE machine |
|---|---|
| Phase05: the Blender import probe → Blender masters if needed → the scene → the Storm and Blender drivers → contact sheets and scorecards → the proving set passing on two tools | Phase06: the grey sphere proof → the 7 masters → the loader → the sweep → the package |
| Phase07: start the generation loop on two tools (the UE column fills in later) | runs the UE column of the proving set while the package isn't ready yet |
| receives the package, and from then on runs all three columns here | back to Studio work; the package is rebuilt only when a master changes |

**Momentum rule (a proposal):** a material that passes on Storm and Blender is **candidate**. It becomes **approved** only once the UE column agrees too. So the loop doesn't wait for the UE runtime, and nothing is called finished without it.

## Pass 9 — Building the materials, plainly (the generation loop)

**The list:** one file in the repo, the wish list. Each line is a material we want, plus a note or two ("dusty concrete, board-formed"). Anyone adds to it at any time. The 173-row table in `260925_R_LibraryCoverage_FirstRelease.md` seeds it. Names use that table's defaults, and they can be changed freely until the first release.

**The run, at fixed times:** a scheduled job on this machine (for example nightly) takes the next few materials from the list. For each one it:
1. **builds the material by whatever works best:** measured values, a free scan, a texture generated in code, or an image model (BP8);
2. **runs it through the rig**, reads its own contact sheet, fixes what's off, and runs it again, up to a set number of tries;
3. **marks it on the list:** *ready for review*, or *stuck, with why*.

**Each morning:** a short summary lists what was built, the contact sheets, and what got stuck. The lead looks at sheets, not scenes. **Keep** marks it approved (subject to the UE column); **redo** sends a note back to the list. USDLiveView stays available for a closer look at any one material.

**What the loop needs that doesn't exist yet:** the list file, the rig (Phase05), a small driver script the scheduler calls, and the status field (BP4). The `/matter-generate` skill already does the building half, one material at a time.

## Pass 10 — After the library works (the later phases (first release, management, community)), plainly

- **A release is a download, not the git repo.** Creators get one bundle per version from the project's releases page. That also avoids the download limits on the repo's large-file storage: textures are 46 MB for 17 materials today, so a few hundred MB to a couple of GB for 170 (a rough estimate).
- **Blender:** the add-on and the material library ship as one Blender extension that installs from a file or a link.
- **Unreal:** the runtime's masters and loader become the public Unreal package: *Unreal Reference Masters*, by then already built and tested.
- **USD tools:** unzip the bundle and point USD's search path at it (as today).
- **Managing the library:** one command, and later a small screen, to add, replace or retire a material in the next release. The version rules already exist; what's missing is making it quick.
- **Contributors:** they submit through a pull request, and the rig is the automatic reviewer. It needs a GPU, so one of our two machines acts as the build runner. Credit goes in `CREDITS.md`.
- **Tracking use and changes:** download counts come free with releases. A creator's slider changes are already saved in their scene, so "share my version back" could turn a tweak into a new variant. Anything beyond that would be opt-in.
- **A CMS:** first a browsable website built from each release (pictures and names; the Roadmap's *See the Library*). A real CMS only if working through git becomes the bottleneck. Git stays the source either way.


## Pass 11 — Seeded, one machine at a time (2026-09-26)

**The lead's ruling (BP9) replaces Pass 8's "in parallel" with a simpler order:** Phase05 is done entirely on this machine and pushed; Phase06 is done on the UE machine and pushed; work comes back here for Phase07 on, with all three tools available.

**What changes:**
- **Phase05's hand-off matters most.** The render-job format and the test scene must be written down well enough for the agent on the UE machine to build against them without asking. That is in the Phase05 stub's Notes.
- **Pass 8's momentum rule (candidate on two tools, approved on three) matters less.** By Phase07 all three tools exist, so the build loop can require all three from the start. It stays a fallback in case the runtime slips.
- **Roadmap (updated with this pass):** Phase05 *Test Rig* (takes over *Parity Baselines*' build) · Phase06 *Unreal Test Runtime* (builds the masters *Unreal Reference Masters* will later publish) · Phase07 *Library Coverage* (renumbered, and marked Reevaluate for its re-cut as the build loop). Nothing was removed; the two RESEARCH entries stay, each pointing at the phase that builds its core.
- **Wording:** earlier drafts of this doc used "M0–M6" for proposed phases. They are now the real phase numbers.


## Pass 12 — Considerations raised in conversation, routed here (2026-09-26)

Said to the lead in chat before Phase05 started; recorded so the phases that need them can find them.
- **Phase07: prove the build loop on about 30 materials before the full list,** and size each nightly batch deliberately: it uses this machine's GPU and the maintainer's usage allowance.
- **Phase06: passing our own Unreal runtime shows a material can work in Unreal, not that IMRSV Studio matches.** An occasional Studio spot check covers that (already in the Phase06 stub).
- **Two machines, one repo:** keep the Unreal work in its own folder, and pull before every commit (already in the Phase06 stub).
- **Real refraction in USDLiveView** needs a path-tracing renderer inside USDLiveView, which is USDLiveView's own project, not this one (Phase05 Pass 2, F9). Not yet raised as an ask in `PlatformDependencies.md`; the lead decides whether to.

---

## Open questions

| # | Question | Recommendation |
|---|---|---|
| ~~Q-A~~ | ~~Close Phase04 without re-freezing the pilot?~~ **Done (BP5).** | — |
| ~~Q-B~~ | ~~Probe Blender's import first?~~ **Yes (BP5).** | — |
| ~~Q-C~~ | ~~How does an agent reach the UE machine?~~ **An agent there, with git between the machines (BP6).** | — |
| Q-D | The wish list: a plain file in the repo (Pass 9)? | Yes; decided at Phase07 |
| Q-E | The proving set: the 7 in Pass 3 item 1? | As listed |
| Q-F | Rig pictures go in an ignored scratch folder, with a small scorecard kept beside each material? | Yes |
| Q-G | The status field is written in both the recipe and the `.mtlx`? | Yes |
| Q-H | Two-tool pass = candidate, three-tool pass = approved (Pass 8)? | Yes |

None of these blocks Phase05. Each can be settled when its phase starts, using the recommendation.

**Unverified:** how faithfully Blender 5.1's USD import brings in MaterialX · Substrate in a packaged Linux Unreal build · runtime texture colour settings in Unreal · the texture-size estimate for 170 materials.

## Status

- **Passes captured:** 11 (2026-09-26).
- **Lead rulings:** BP1–BP9. Unreal work happens on the UE machine (Linux, with an agent) as a standalone runtime. Materials are judged by the tools agreeing with each other. Drafts keep `v01` with a status field. Phase04 is closed. The agent builds materials by any means, and licensing doesn't block the seed library. Phase05 and Phase06 are seeded and run one after the other.
- **The plan:** **Phase05 (this machine):** the Blender and USDLiveView test rig, starting with the Blender import check, and closing with a push. **Phase06 (UE machine):** the packaged Unreal test runtime, starting with one grey sphere. **Phase07 (back here):** Library Coverage, expected to be re-cut as the nightly build loop. The later phases (first release, management, community) are sketched in Pass 10.
- **Open:** Q-D to Q-H, each with a recommendation and none blocking.
- **Process note for `/retro`:** the lead has asked repeatedly for less ceremony and plainer words (Pass 6). Filling a library is a loop, not a sequence of phases. Keep release checks out of content work before the first release. *(For the Workflow Refiner; this doc doesn't edit the method.)*
- **Next step:** `/discovery Phase05` on this machine.
