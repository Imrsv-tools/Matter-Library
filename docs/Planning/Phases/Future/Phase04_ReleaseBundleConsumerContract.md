# Phase04 — Release Bundle and Consumer Contract

**Status:** DISCOVERY — Pass 1 done 2026-09-25, **held on a sequencing fork** (§Lead calls, L1). Seeded 2026-09-25 when the lead's `/discovery P4` numbered the head of the Roadmap's `## Future`.

## Outcome

**A consumer can download one versioned, verifiable release of the library and use it without ever touching this repository.**

Concretely, at close:
- a published `matterlib-X.Y.Z` release bundle that someone on a machine with no clone of this repo can fetch, verify, install, activate and render from;
- a written consumer contract saying what the bundle contains and what a consumer may rely on, including the master contract as data.

## Why this is a phase

The release machinery exists and has cut a pilot (`matterlib-0.1.0`: lock → catalog → freeze → approval, `tools/releases/`). **What has never existed is the thing a consumer takes.** R1 says consumers take releases and never the checkout, and R14 says this repo ships a release bundle plus the master contract as data. The specs already assign this phase a dozen `Drift` / `(planned)` / `Reevaluate` markers (Pass 1 F7).

**Expensive to unwind:** the bundle layout, the trust anchor a consumer verifies against (F3), and the catalog `schema_version` bump that carries the master token. Once a consumer installs against them, changing any of these is a breaking change across the boundary. Publishing is irreversible because the repo is public.

## Lead calls

**L1 — Is this still the next phase? (open; NOT resolved by discovery. Two lead positions disagree.)**

- **The Roadmap order** (re-thought 2026-09-23, rulings R5/R11): *"The first phases make the library stand alone, be versioned and published, and be consumed by IMRSV."* This entry heads `## Future`, and `/discovery P4` numbered it.
- **The lead, 2026-09-25** (`260925_R_DraftsInUSDLiveView.md` Pass 5, verbatim): *"Why so much overhead? Make a material, serve it to stage. no versioning, no faffing around. we are VERY pre release right now ... we have 200 materials to build and test before we have our first versionable library ... nobody is using it, just us."* And: *"I mean moving forward with this project."* The dev loop that ruling asked for is already built (`tools/releases/serve_to_stage.py`, `9dabea1`), so no consumer is waiting on a bundle to see new materials.

The options, independent of each other:
- **(a) Keep P4 as is.** Build the bundle machinery now and prove it on a pilot, e.g. `0.1.0` re-published as a bundle and marked pilot. The first *real* publish happens later, when the library is ready.
- **(b) Re-sequence.** Library Coverage becomes P4 (the ~200 materials), and this doc returns to `PhaseTBD` with its Pass 1 kept. The bundle waits for a library worth versioning.
- **(c) Narrow P4 to the contract without the publish.** Master token as data, the catalog schema bump, and an activation that doesn't need the repo. Packaging and publishing are deferred.

*Discovery's read:* (b) matches the 2026-09-25 words most literally, and F4 means a (a) pilot bundle would first need the DDS encoder reinstalled. But the choice is the lead's.

**L2 — The first release for users: its version and contents.** Version Management hands this to this phase. **It is folded into L1:** under (a) or (c) it is a later publish decision, and under (b) it moves with this doc. *(At seed time discovery recommended "publish today's articles as `0.2.0`". That recommendation is **withdrawn**: it contradicts the 2026-09-25 ruling above.)*

## Scope (provisional — subject to L1)

**In (the specs assign these to this phase, dated 2026-09-23 unless noted):**
- **Publish:** the bundle's format and packaging (`ReleaseModel.md` step 6 `(planned)`; no spec names the format).
- **Master token as data:** the per-article token in the lockfile and catalog under a `schema_version` bump (`RuntimeCatalog.md` §Planned; `MasterSet.md` Drift). This phase also **ratifies the two token rules** written while bringing the spec home: "adding is additive; removing or renaming is semver-major" and "`system` is reserved". No validator enforces the reservation yet (`MasterSet.md` Reevaluate).
- **A self-contained producer gate:** `promote_release.py` still runs the fixture-sync check against `<repo parent>/<Stage fixture>` (F5; `PlatformDependencies.md` P8, second half).
- **Deploy becomes publish** (`ReleaseModel.md` Drift on deploy).
- **Activation without the repo:** where `activate_release.py` lives, and what it verifies (F2, F3; `ReleaseModel.md` Reevaluate).
- **The consumer contract, written down:** `Consumers.md` §What every consumer binds to, with its Drift closed.
- **Release tags** `matterlib-X.Y.Z` (`Manifest.md` / `_Architecture.md` Drift; `git tag -l` empty, 2026-09-25).
- **The `imrsv:matterlibRelease` naming tension:** `_Architecture.md` Reevaluate assigns it here, while `Manifest.md` says "the contract phase". It is in scope because the pin names a release, and the bundle is what makes a release a thing.

**Not now:**
- **Consumer-side adoption** (P1–P4, P7, P10): the **IMRSV Consumes Releases** phase, on the platform's line.
- **The Blender add-on installing from a release**, including its hard-coded `MATTERLIB_RELEASE`: **Blender from a Release**.
- **Browsing with previews:** **See the Library**.
- **A second release built from the first**, and immutability in `0.x` (research Q5): **Version Management**.
- **A reference UE masters package:** **Unreal Reference Masters**.
- **Filling the library:** **Library Coverage**.
- **CODEOWNERS on `library/releases/`:** **Contribution Path**. `Manifest.md`'s Drift still names this phase, but Version Management's later "Moved" annotation is the deliberate one; the pointer gets conformed at execute.

## Discovery Log

### Pass 1 (2026-09-25): specs top-down, anchored on the Outcome, plus the release tools read against it

**Examined:**
- specs: `_Architecture.md`, `Consumers.md`, `Distribution/ReleaseModel.md`, `Contract/{RuntimeCatalog,Manifest}.md`, `Ontology/MasterSet.md` (§Master tokens / resolution), `Glossary.md` (Release bundle);
- research: `260923_R_StandaloneSetup.md` (R1, R7, R14; Passes 4 and 9; Q5, Q8), `260925_R_DraftsInUSDLiveView.md` (Pass 5);
- code: `tools/releases/{stage,freeze,activate,promote}_release.py` and `serve_to_stage.py`, `tools/validators/check_fixture_sync.py`, an article's texture references.

**Learnings:** `docs/Learnings/` holds only its README, so no domain entries apply (a discharged read). **Grep for the phase's own name:** no code builds or mentions a release bundle; "bundle" in `tools/` is only the OCIO parity config.

**Findings:**
- **F1 — The bundle layout already exists: it is the install-root release directory.** Articles reference textures as `../../../textures/…` relative to `materials/<domain>/<class>/`. The install layout in `ReleaseModel.md` (`releases/matterlib-<ver>/` = catalog + `materials/` + `textures/`, `.dds` included) is exactly the tree those paths need. **Reuse:** the bundle is that directory plus the records a consumer verifies against. It is not a new layout.
- **F2 — Activation needs the repo today.** `activate_release.py` reads the approval and freeze from `<repo>/library/releases/` and imports `validate_approval` and `source_provenance` from `tools/`. A consumer without a clone **cannot activate**, which contradicts the Outcome. It also re-checks only the catalog and `.dds` against the frozen hashes, **not** the `.mtlx` or PNG files, although the freeze record carries per-file sha256 for all of them. The `dds_set` digest folds in staging paths and cannot be recomputed at the install, but the per-file hashes can (the tool already does this for `.dds`).
- **F3 — Moving verification into the bundle moves the trust anchor.** If the approval and freeze travel *inside* the bundle, a tampered bundle can carry a matching tampered approval: it becomes self-attesting. "Verifiable" needs an anchor outside the bundle, such as the digest committed in this public repo, recorded on the tag or release, or an artifact attestation. **This is the one integrity-control amendment in the phase** (lane: F8).
- **F4 — The DDS cannot be rebuilt on this box today** (measured 2026-09-25): the pinned encoder `compressonatorcli V4.5.52` is not on `PATH`, and `library/staging/` is absent, so the frozen `0.1.0` `.dds` set exists only as hashes in its freeze record. `stage_release.py` asserts that the encoder is deterministic at the pin, but that is unverified here. Any bundle carrying `.dds` depends on reinstalling the encoder first.
- **F5 — `promote_release.py` still gates on a consumer checkout:** `check_fixture_sync.default_fixture_root` = `<repo parent>/<Stage fixture>` (P8, confirmed).
- **F6 — Size (measured):** `MatterLibrary/textures/` is 46 MB today (40 LFS files; the `0.1.0` freeze names 30 PNG and 30 DDS). *Unverified extrapolation:* around 170 articles lands in the low GB with DDS included. That matters for the host's per-asset limit, which is an external fact to confirm before offering a host choice.
- **F7 — The spec markers owned here** are listed in §Scope · In. There are more than the seed listed: token-rule ratification, the `imrsv:` pin tension, and CODEOWNERS (routed out, see §Not now).
- **F8 — Lane (provisional, controls read):** the controls are `promote_release.py` (the sole approval flip), `freeze_release.py` (the hash-lock) and `activate_release.py` `check_install_ready` (the refuse-if-tampered gate). Packaging, tags and the token-in-catalog bump are **`build`**. Re-homing `check_install_ready`'s trust anchor (F3) amends an integrity control on a public artifact, so it is **`high-rigor` for that step**. The final lane is ruled in the Brief, after L1.
- **F9 — The 2026-09-25 ruling bears on this phase's premise** → L1.

**Superseded seed questions** (compressed from the seed): Q1 host → F1 and F6 (the layout is settled; the host is still open behind a size check). Q2 DDS → F2 and F4. Q3 first-test consumer → still a hypothesis (stock `usdview` with the search path pointed at an install), but F2 means activation must first stop needing the repo. Q4 → L2. Q5 (committed generated artifacts) → still open, and most likely Blender from a Release's for the `.blend`. Q6 → F8. Q7 (Creator ports) → P12's third overlay has landed; re-check `LCDSchema.md` against the Coverage thread at Pass 2.

## Discovery Status

- **Passes captured:** 1.
- **Current working direction:** held on L1. If (a) or (c): Pass 2 settles the trust anchor (F3) and the first human test, then the Brief.
- **Open decisions:** L1 (sequencing; L2 folds into it).
- **Checks to carry forward:** F4 (encoder on this box) before any `.dds`-bearing step; the host's per-asset limit (F6); the `LCDSchema.md` vs Coverage `## Resolved` check (Q7).

## Execution Log

_(populated during execution)_
