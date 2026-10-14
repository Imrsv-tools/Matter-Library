# Matter Library — Roadmap

Lightweight phase guide. Three sections: **`## Active`** (live work) → **`## Future`** (sequenced seeds + the backlog) → **`## Complete`** (closed phases, newest at the bottom).

> **Entry format — keep it scannable.** Each entry is just: the **heading** (name + status), a one-line **`Outcome`**, and **doc pointer(s)**. The **`Outcome` is what the USER can DO when the phase is done** — the *point* of the work, in plain non-technical language (no code symbols, no implementation detail, never tech-for-tech's-sake). **Always challenge it — "is there a user-facing result?"**: default to the user-facing outcome; a pure-infra / refactor phase MAY instead state a system-capability outcome, but the challenge is never skipped. If an `Outcome` already exists, don't rewrite it unless asked. The doc pointer is the phase doc if it exists, else the known relevant docs. **ALL technical content — scope, rename maps, root-cause, hazards — lives in the phase doc, never here.** This index exists so anyone can skim the phases in seconds.
>
> **Status vocabulary:** `RESEARCH` (no phase doc yet — the pointers are the raw material) → `SEEDED` (phase doc written) → `ACTIVE` (being worked; `ACTIVE (parked on <ref>)` while it waits on another repo) → `COMPLETE`. A `TBD` entry is simply one the lead has not numbered — it may hold a perfectly settled position, since **order is position in the list, never an ordinal**. Numbering is the lead's call: sometimes one as work starts, sometimes a whole span when committing to a Wave (Workflow §Phase Numbering). **An entry an agent adds goes LAST in `## Future`, with one italic line saying what added it** — a place in the list is an order, and the order is the lead's.

> **Re-thought 2026-09-23 (Phase01 step 1.5)** around the library and the tools that make it usable, grow it and generate it (lead rulings R5/R11, `docs/Planning/Research/260923_R_StandaloneSetup.md`). The first phases make the library stand alone, be versioned and published, and be consumed by IMRSV. The pre-standalone plan is archived at `docs/Planning/Phases/Complete/PreStandalone/build_plan.md`; every planned idea in it is carried below or in the Parking lot.

==================================================================================
## Active

### Phase15 — Matter, Character and HDRI — BRIEF READY, lane build; one lead question (Q-P15-1, where Character's folder sits) before `/execute` *(discovery 2026-10-14; added 2026-10-14 by `/research` on the lead's "yes record it and seed all three", the first of three in that order, RD-DS-5; **numbered Phase15 the same day, ahead of Scale Grids:** *"Lets make these the next phases (Before the scaled grid)"*, RD-DS-6; the library's half, with the site's and the platform's asked through the ledger)*
**Outcome:** the website, Studio and USDLiveView each show Matter, Character and HDRI as three separate things to browse, each by its own taxonomy, from what the library publishes.
- `docs/Planning/Phases/Phase15_MatterCharacterHdri.md` · research `docs/Planning/Research/261014_R_DownstreamPicture.md`

### Phase16 — Every Entry Says What It Is — BRIEF READY, one lead call open, executes after Phase15 *(discovery opened 2026-10-14, "/discovery P16"; added 2026-10-14, the same word, second of the three, RD-DS-3: materials work like assets, the facts inside the file; numbered Phase16 the same day, RD-DS-6)*
**Outcome:** every material and HDRI says who contributed it, its licence, its name and its place in the taxonomy, from inside its own file; Studio, USDLiveView and the website read it, and Forseti can tell who gave what and how each one is doing.
- `docs/Planning/Phases/Phase16_EveryEntrySaysWhatItIs.md` · research `docs/Planning/Research/261014_R_DownstreamPicture.md`

### Phase17 — The Library Service — SEEDED *(**numbered Phase17 2026-10-14, ahead of Scale Grids**, RD-DS-7; added 2026-10-14 by `/research` on the lead's "I guess that is ALSO a new pahse to seed", RD-MP-11; *Thumbnails* and the team's console build on it; **2026-10-14: a material arrives as one package, tested and pictured on upload, RD-RO-1; its spec is defined beside the phases above it**)*
**Outcome:** the library's work (the test rig, the build loop, thumbnails, the dev catalog the site's staging reads) runs on a permanent machine instead of the lead's laptop, and the IMRSV team reaches it from wherever they are.
- `docs/Planning/Phases/Phase17_LibraryService.md`

### Phase18 — Thumbnails — SEEDED *(**numbered Phase18 2026-10-14, ahead of Scale Grids**, RD-DS-7; added 2026-10-14 by `/research` on the lead's "Seed all the TBD phases we discovered here", RD-MP-2 to RD-MP-6; runs on The Library Service; the library's half of See the Library)*
**Outcome:** every kept material has thumbnails that show it at its best, on a subject that suits it (skin on a hand and a face, hair on a head, glass in front of a backdrop), ready for the website and the team's console.
- `docs/Planning/Phases/Phase18_Thumbnails.md`

### Phase19 — Character Materials, Their Own Library — SEEDED *(**renumbered Phase19 the same evening, after Thumbnails, whose per-part picture rig it builds on**, RD-DS-7; added 2026-10-14, the same word, third of the three, RD-DS-4; Skin Maps and Skin Maps Beyond Colour are its first instances; numbered Phase17 the same day, RD-DS-6)*
**Outcome:** a contributor can craft a set of teeth, a skin or an eye that fits the character's own part mesh, keep their name on it, and see it pictured on that part.
- `docs/Planning/Phases/Phase19_CharacterLibrary.md` · research `docs/Planning/Research/261014_R_DownstreamPicture.md`

### Phase20 — Scale Grids — BRIEF READY, after Phase15 – 19 *(**renumbered Phase20 later the same evening**, RD-DS-7; numbered Phase15 and opened by the lead 2026-10-14, "/discovery P15"; **renumbered Phase18 the same day**, when the lead put the three above ahead of it, RD-DS-6; its discovery Pass 1 is kept; added 2026-10-14 by `/research` on the lead's "can be it's own phase": one material per UV scale, all aligned, to test that UVs are applied to scale, RD-SP-1)*
**Outcome:** anyone applying UVs can swap every object in a scene to the scale grid of its own material and see at once whether a metre is a metre: a wrong scale is obvious.
- `docs/Planning/Phases/Phase20_ScaleGrids.md`

*Material-making runs as a standing process outside the phase line: `/matter-batch` over the wish list.*
*(**Held 2026-10-14 until Phase15 – 19 are done**, the lead: "get the entire chain established recategorized, documented and working correctly before we add more materials", RD-DS-7.)*

==================================================================================
## Future

> **Re-sequenced 2026-09-26 (lead):** the test rig comes before building materials at volume. Phase05 runs on this machine and is pushed; Phase06 runs on the UE machine; work returns here for Phase07 on. Why: `docs/Planning/Research/260926_R_BigPicture_NimbleSetup.md`.
>
> **Re-sequenced 2026-09-27 (lead):** Character Materials becomes **Phase07** and runs here straight after Phase05, **at the same time as Phase06** on the UE machine. Its materials ship as candidates (uncalibrated) until the Unreal column exists: *"I would rather have everything in and 'uncalibrated' yet then a bunch of magenta."* Library Coverage becomes Phase08. Why: `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md` (CM4).
>
> **Re-sequenced 2026-09-28 (lead):** Character Appearance for Studio becomes **Phase08** and runs next on this machine. Library Coverage is **un-numbered**: *"we have many other little things to get in here befoer we build out the full library."* Before 2026-09-28, "Phase08" means Library Coverage. Why: `docs/Planning/Research/260928_R_PlatformAppearanceAsks.md`.

> **Re-sequenced 2026-10-01 (lead):** Library Coverage was numbered **Phase10**, and its discovery Pass 1 proposed colour on wear layers as a phase of its own. The lead: *"If 2 then we need to do that phase now instead."* **Coloured Wear Layers is Phase10**, and Library Coverage is un-numbered again, paused after Pass 1. The same day: *"The fixed times was ONE session... remove taht thought"*: the build loop has no schedule. Why: `docs/Planning/Phases/Complete/Phase11_LibraryCoverage.md` (F-LC-7, F-LC-8; numbered Phase11 on 2026-10-02).

> **Re-sequenced 2026-10-14 (lead):** the order below, top to bottom, is cut from `docs/Planning/Research/261014_R_RoadmapOrder.md` (the lead: *"yep! Good... quickix and push"*). Library work that runs now comes first, then the library service and what runs on it, then the first real release and its consumers; after them the platform's consumer outcomes, the held entries and the withdrawn one. **Nothing is numbered:** numbers are the lead's to assign. *(The same day the lead numbered the head entry, Materials Described, as **Phase13**; it moved to `## Active`. Then HDRIs in the Library, the next entry, as **Phase14** ("/discovery P14"); it moved to `## Active` too. Then Scale Grids, the next entry, as **Phase15** ("/discovery P15"); it moved to `## Active` as well. That evening the lead put three new phases ahead of it, *"Lets make these the next phases (Before the scaled grid)"*: **Phase15 – 17** are *Matter, Character and HDRI*, *Every Entry Says What It Is* and *Character Materials, Their Own Library*, and Scale Grids is **Phase18**. Before then, *Phase15* means Scale Grids; why: `docs/Planning/Research/261014_R_DownstreamPicture.md` RD-DS-6. Later the same evening the lead pulled The Library Service and Thumbnails ahead of Scale Grids too, *"Actually lets pull the library service and thumbnails before Scale grids as well so we can get the entire chain establsihed recategorized, documented and working correctly before we add more materials"*, and put Character after Thumbnails: **Phase17** The Library Service, **Phase18** Thumbnails, **Phase19** Character Materials, **Phase20** Scale Grids (RD-DS-7). In that evening's commits *Phase17* first meant Character Materials and *Phase18* Scale Grids.)*

### Skin Maps — SEEDED *(research opened and the phase seeded 2026-10-14; the lead on today's tone-per-part skin: "it is pretty terrible in fact (the line between lips and face and no variation)... I think we need to plan to move to SkinMaps"; skin maps are made per approved mesh version, today MakeHuman's hm08 on the Manny skeleton, RD-SKM-1; **the industry survey is done (2026-10-14); three questions for the lead and a probe come before discovery**; was "Skin That Reads as Skin" for part of that day)*
**Outcome:** a character's skin varies across the body as real skin does (lips that blend into the face, redder cheeks and knuckles), in Blender, a USD viewer and Unreal, and every character built from the approved human mesh wears it.
- `docs/Planning/Phases/Future/PhaseTBD_SkinMaps.md` · research `docs/Planning/Research/261014_R_SkinMaps.md`

### Skin Maps Beyond Colour — SEEDED *(added 2026-10-14 by `/research` on the lead's "Seed a phase TBD...", "Full skin map set"; builds on Skin Maps, which ships the colour map first)*
**Outcome:** up close, a character's skin catches the light as real skin does (fine wrinkles and creases, oilier and drier areas, light glowing through ears and fingers), in Blender, a USD viewer and Unreal.
- `docs/Planning/Phases/Future/PhaseTBD_SkinMapsBeyondColour.md` · research `docs/Planning/Research/261014_R_SkinMaps.md`

### The Library Console — SEEDED *(added 2026-10-14, the same word, RD-MP-7; runs on The Library Service)*
**Outcome:** the IMRSV team opens one page to review new materials and keep or send back each one, choose which materials go into each library version, and see each material's provenance.
- `docs/Planning/Phases/Future/PhaseTBD_LibraryConsole.md`

### Release Bundle and Consumer Contract — SEEDED *(un-numbered 2026-09-25: the lead re-sequenced the material work ahead of it; discovery Pass 1 kept)*
**Outcome:** a consumer can download one versioned, verifiable release of the library and use it without ever touching this repository.
- `docs/Planning/Phases/Future/PhaseTBD_ReleaseBundleConsumerContract.md`

### Version Management — SEEDED
**Outcome:** a maintainer can cut the next release from the last one — keeping, adding, deprecating and retiring materials — and every earlier release stays exactly reproducible.
- `docs/Planning/Phases/Future/PhaseTBD_VersionManagement.md`

### Blender from a Release — RESEARCH
**Outcome:** a Blender user installs the Matter add-on and library from a release and uses Matter materials without cloning this repository.
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (seed 4) · `docs/specs/Experience/Experience_MatterLibrary.md` §Shipped

### Unreal Reference Masters — RESEARCH *(its masters are first built by Phase06, 2026-09-26; **re-scoped 2026-09-28, lead: "Studio adopts the library masters"**, `PlatformDependencies.md` P20)*
**Outcome:** IMRSV Studio, and any other Unreal user, renders library materials with one package of the Matter masters taken from a release, each master making its materials look as good as Unreal can. *(Was: "an Unreal user outside IMRSV can drop in a package…".)*
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (Pass 9, option B; R14 "B later") · `docs/Planning/Phases/Complete/Phase06_UnrealTestRuntime.md`

### Contribution Path — RESEARCH
**Outcome:** an outside contributor can submit a material and get an automatic verdict, with only maintainers able to put it in a release.
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (seed 8) · `CONTRIBUTING.md` · `docs/Planning/Research/261014_R_MaterialPipeline.md` F-MP-28 (a contributed generator script runs as code on the library service: a sandbox or a maintainer's read before a run) · `261014_R_RoadmapOrder.md` F-RO-23 (a contribution is one material package, tested on upload, RD-RO-1; this entry keeps what is specific to outsiders)

### IMRSV Consumes Releases — RESEARCH *(integration; numbered on the IMRSV platform's line)*
**Outcome:** IMRSV Studio users get Matter materials from an installed release, including in packaged builds, with no copy of this repository involved.
- `docs/Planning/PlatformDependencies.md` (P1–P4, P10)

### See the Library — RESEARCH *(2026-10-14, lead: the library's website is built and run by IMRSV's web platform from published releases; the library publishes a file for the site and a preview set beside each release, RD-WS-1 to RD-WS-4; **a consumer outcome since 2026-10-14:** the library's halves are Materials Described, Thumbnails and the release publish, `261014_R_RoadmapOrder.md` F-RO-6)*
**Outcome:** anyone can browse what is in a release, with a preview image of every material.
- `docs/Planning/Research/261014_R_TheLibrarysSite.md` · `docs/Planning/Research/260923_R_StandaloneSetup.md` (seed 5) · `docs/specs/Catalog/Catalog.md` §Thumbnails · `docs/Planning/PlatformDependencies.md` (P24, M9)

### Hair That Reads as Hair — RESEARCH *(seeded 2026-09-28 from Phase08: the lead on the interim hair: "eventuall this needs to be reseerached and fixed.. this is not usable"; **2026-09-29: cards are the one exception, each style's picture shading one light hair article; strands are the real path**, MAP-RD3/RD4; **held 2026-10-14:** research, after the Skin Maps survey)*
**Outcome:** a character's hair looks like real hair (soft, alive, lit through), in Blender, a USD viewer and Unreal, on cards now and on strands later.
- `docs/Planning/Research/260928_R_HairAndNailRendering.md` (H4 card maps, H5 strands) · `docs/Planning/Research/260929_R_CharacterMaps.md` (Pass 7, MAP-Q9/Q10)

### Author a Material End to End — RESEARCH *(`Reevaluate (2026-10-14)`: The Library Console is its maintainer half, and the Creator's half lives in each consumer, `261014_R_RoadmapOrder.md` F-RO-6)*
**Outcome:** a contributor can go from an idea to a validated material in the library in minutes, using one tool (the first cut of the Matter Manager).
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (seed 7)

### Parity Baselines — RESEARCH *(its build is Phase05 + Phase06, 2026-09-26; publishing the results for anyone to see stays here; `Reevaluate (2026-10-14)`: Materials Described carries the parity verdict per Creator port to the site, `261014_R_RoadmapOrder.md` F-RO-6)*
**Outcome:** anyone can see, for each kind of material, how closely its MaterialX, Blender and Unreal renders match.
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (seed 10) · `docs/specs/Tooling/CompressedDistribution.md` · `docs/Planning/Phases/Complete/Phase05_TestRig.md`

### Two Licences — SEEDED, withdrawn 2026-10-14 *(added 2026-10-14, the same word, RD-MP-1 and RD-MP-8: CC BY 4.0 beside CC0, CC0 the default; **withdrawn the same day, the lead: "material are CC0"**, RD-RO-2; kept so its intent survives)*
**Outcome:** a material can be published under CC0 or CC BY 4.0, and every consumer shows each material's licence and the credit a CC BY material asks for.
- `docs/Planning/Phases/Future/PhaseTBD_TwoLicences.md`

### Parking lot — TBD
**Outcome:** unsequenced ideas, kept so their intent survives (Don't Delete Spec Functionality).
- Automated transformers (MaterialX → Blender / Unreal), after manual parity is proven. Parity-gate automation in CI. A Realm level above Domain. Texture storage beyond Git LFS (asset management, content-addressed pointers). Further engine targets. Personal saved variants, community scoring and contributor reputation (`docs/specs/Experience/Experience_MatterLibrary.md` §Future Layers). The planned roots in `docs/ToolingConventions.md` §Planned roots.

==================================================================================
## Complete

### Pre-standalone — built by IMRSV platform phases (2026-06 → 2026-07) — COMPLETE
**Outcome:** the foundations, the authoring harness, the first 12 materials, the release machinery and the Blender library, all built into this repo by the IMRSV platform's Materials wave.
- `docs/Planning/Phases/Complete/PreStandalone/` (`build_plan.md` §Delivered · `Phase01_Foundations.md` · `Readme_2026-07.md` · `FolderStructure.txt`)

### Phase01 — Standalone Bootstrap — COMPLETE
**Outcome:** anyone can understand, navigate and work on the Matter Library from this repository alone.
- `docs/Planning/Phases/Complete/Phase01_StandaloneBootstrap.md`
*Closed 2026-09-23.*

### Phase02 — One-Command Check — COMPLETE
**Outcome:** anyone can clone the library on a fresh machine, run one command, and see every material and release validate, with the result also checked automatically on every pull request.
- `docs/Planning/Phases/Complete/Phase02_OneCommandCheck.md`
*Closed 2026-09-23; automatic pull-request checks parked by the lead (→ Contribution Path).*

### Phase03 — Agentic Material Generation — COMPLETE
**Outcome:** a maintainer can ask an agent for new materials and receive validated candidates, with recorded provenance, ready for human judgement.
- `docs/Planning/Phases/Complete/Phase03_AgenticMaterialGeneration.md`
*Closed 2026-09-25.*

### Phase04 — Wear Layers at Their Own Scale — COMPLETE
**Outcome:** a wear layer (dust, scratches, scuffs) looks the right size on every material, whatever that material's tile size.
- `docs/Planning/Phases/Complete/Phase04_WearLayersAtTheirOwnScale.md`
*Closed 2026-09-26; the pilot's re-approval is owed by the maintainer.*

### Phase05 — Test Rig: Blender and USDLiveView Side by Side — COMPLETE
**Outcome:** the maintainer can put any material side by side in Blender and USDLiveView, with every slider moved through its range, and see where the two agree and where they drift.
- `docs/Planning/Phases/Complete/Phase05_TestRig.md`
*Closed 2026-09-27; one maintainer re-approval of the pilot covers Phase04 and Phase05.*

### Phase07 — Character Materials — COMPLETE
**Outcome:** a character wears real materials from the library (skin, eyes, mouth, lips, nails, hair and basic clothing fabrics) in Blender and a USD viewer, and in Unreal once it is calibrated. None shows the missing-material magenta, on any character.
- `docs/Planning/Phases/Complete/Phase07_CharacterMaterials.md`
*Closed 2026-09-27; 19 candidates, awaiting the Unreal column (Phase06).*

### Phase08 — Character Appearance for Studio — COMPLETE
**Outcome:** in Studio, a Creator can give a character any hair colour from one good hair material, pick any of six skin tones and have the lips and nails match, and dress it in clothes whose fabrics, soles included, come from the library in any colour.
- `docs/Planning/Phases/Complete/Phase08_CharacterAppearance.md`
*Closed 2026-09-28 on the library side; the hair is an interim, and Studio's check is the platform's.*

### Phase06 — Unreal Test Runtime — COMPLETE
**Outcome:** the test rig's picture sheet gains an Unreal column, rendered by a small Unreal app of our own that runs on any Linux machine with a GPU.
- `docs/Planning/Phases/Complete/Phase06_UnrealTestRuntime.md`
*Closed 2026-09-30; the pinned build is `unreal-runtime-v1`.*

### Phase09 — Hair and Eye Masters — COMPLETE
**Outcome:** a Creator's character has hair that keeps its strands and takes any colour on any hairstyle, and eyes that look real (a photographed iris in the colour they pick, wet, and in Studio shaded by Unreal's own eye model), the same in Blender, a USD viewer and Studio.
- `docs/Planning/Phases/Complete/Phase09_HairAndEyeMasters.md`
*Closed 2026-09-30; the Unreal eye model did not fit (the eye is on Subsurface), and Studio's check is the platform's.*

### Phase10 — Coloured Wear Layers — COMPLETE
**Outcome:** a Creator who turns up a wear layer such as dust or grime sees it in its own colour, not only as a change in shine, and it looks that way in Blender, a USD viewer and Unreal.
- `docs/Planning/Phases/Complete/Phase10_ColouredWearLayers.md`
*Closed 2026-10-01; the pinned build is `unreal-runtime-v3`, and Studio's side is the platform's.*

### Phase12 — Glass and Light Colour — COMPLETE
**Outcome:** a Creator sets the colour of glass and other see-through matter, and the colour and brightness of a light, with a control, in Blender and in Studio; the library then carries one clear glass and one light, not an article per colour.
- `docs/Planning/Phases/Complete/Phase12_GlassAndLightColour.md`
*Closed 2026-10-05 on the library side; the two colour-only articles are kept and marked, and Studio's side is the platform's.*

### Phase11 — Library Coverage — COMPLETE
**Outcome:** the maintainer runs a batch and gets new materials, each already built and checked side by side in USDLiveView's renderer, Blender and Unreal, and keeps or sends back each one from its picture sheet. The library fills toward its full list this way, without a phase per batch.
- `docs/Planning/Phases/Complete/Phase11_LibraryCoverage.md`
*Closed 2026-10-14 by verdict (RD-MP-13): 29 of 35 rows kept, 6 back on the list as redo rows; material-making continues as a standing process.*

### Phase13 — Materials Described — COMPLETE
**Outcome:** every kept material has a name a person reads, a one-line description and search words, and the library publishes everything the website shows about each material in one file beside each release.
- `docs/Planning/Phases/Complete/Phase13_MaterialsDescribed.md`
*Closed 2026-10-14: every material described and published in the dev snapshots `matterlib-0.2.0-dev.1` and `-dev.2`; biological materials are browsed apart (RD-P13-2).*

### Phase14 — HDRIs in the Library — COMPLETE
**Outcome:** a scene's lighting picture (an HDRI) is chosen from the library by name, in the IMRSV app and a USD viewer, and the library is the only place it comes from.
- `docs/Planning/Phases/Complete/Phase14_HdrisInTheLibrary.md`
*Closed 2026-10-14 on the library side: all 59 of Poly Haven's Pure Skies, credited, named by file and served; the app's side is the platform's HDRI phase (M10).*
