# Phase04 — Release Bundle and Consumer Contract

**Status:** SEED (phase doc written 2026-09-25; discovery has not opened). Numbered by the lead's `/discovery P4`, resolved to the head of the Roadmap's `## Future`.

## Outcome

**A consumer can download one versioned, verifiable release of the library and use it without ever touching this repository.**

Concretely, at close: a published `matterlib-X.Y.Z` release bundle that someone on a machine with no clone of this repo can fetch, verify against its own hashes, install into an install root, activate, and render from; and a written consumer contract saying what that bundle contains and what a consumer may rely on. That contract includes the master contract as data.

## Why this is a phase

The release machinery exists and has cut a pilot (`matterlib-0.1.0`: lock → catalog → freeze → approval, `tools/releases/`). **What has never existed is the thing a consumer takes.** Every consumer today reads this repo's checkout: IMRSV's Stage fixture mirror, the three-source deploy assembly, the Blender add-on's `parents[3]` root, and USDLiveView's search root (`260923_R_StandaloneSetup.md` Pass 4). R1 says consumers take releases and never the checkout, and R14 says this repo ships a release bundle plus the master contract as data. This phase is where both become real.

It is the root of most of `## Future`: IMRSV Consumes Releases, Blender from a Release and See the Library all start from a published release, and `PlatformDependencies.md` P1–P4, P7 and P10 pair with it.

**Expensive to unwind:** the bundle layout and the catalog `schema_version` bump that carries the master token. Once a consumer installs against them, changing either is a breaking change on the other side of the boundary. Publishing is also irreversible: the repo is public.

## Scope

**In (the specs already assign these to this phase, as `Drift` / `(planned)` dated 2026-09-23):**
- **Publish:** the release bundle's format and packaging. `ReleaseModel.md` lifecycle step 6 is `(planned)`, and no spec yet names the format.
- **The master token as data:** the per-article master token in the lockfile and the runtime catalog, under a `schema_version` bump (`RuntimeCatalog.md` §Planned: the per-article master token; R14).
- **A self-contained producer gate:** promotion stops depending on a consumer's checkout (`ReleaseModel.md` step 5 Drift; `PlatformDependencies.md` P8, whose remaining half is `promote_release.py` still running the fixture-sync check).
- **Deploy becomes publish:** the producer stops writing into a consumer's runtime directory (`ReleaseModel.md` Drift on deploy).
- **Where `activate_release.py` lives:** it is a producer tool that writes into a consumer-owned install root (`ReleaseModel.md` Reevaluate).
- **The consumer contract, written down:** `docs/specs/Consumers.md` §What every consumer binds to, with its Drift closed.
- **Release tags:** the `matterlib-X.Y.Z` git tag, moved here from Version Management. No tag exists yet (measured 2026-09-25: `git tag -l` is empty).

**Not now:**
- **Consumer-side adoption.** Stage, the deploy tooling, packaged builds, plugin routing and USDLiveView all belong to the platform (P1–P4, P7, P10) and to the **IMRSV Consumes Releases** phase, numbered on the platform's line. This phase records the asks and does not edit consumer repos.
- **The Blender add-on installing from a release.** That is **Blender from a Release**, including the add-on's hard-coded `MATTERLIB_RELEASE = "matterlib-0.1.0"` in `blender/addons/imrsv_lcd_export/lcd_usd_edit.py`.
- **Browsing a release with previews:** **See the Library**.
- **A second release built from the first** (carry-forward, `deprecated` / `retired`, immutability enforced by a gate, semver bumps): **Version Management** (`PhaseTBD_VersionManagement.md`).
- **A reference UE masters package:** **Unreal Reference Masters** (R14 "B later").
- **Filling the library:** **Library Coverage**.

## Seed-vs-docs questions (for discovery; the four fork tests were run as each was written)

1. **The bundle's format and host.** The research hypothesis is a GitHub Release asset laid out as `releases/matterlib-<ver>/` (catalog, lock, `.mtlx`, PNG, pre-compressed DDS, freeze, approval, and a small manifest of supported versions: Pass 4 and Pass 9, option A). Not ruled. *Discovery work first: measure the payload size (LFS textures plus DDS) against the host's asset limits before offering a choice (test 3).*
2. **DDS in a verifiable bundle.** The `.dds` files are gitignored staging output, and `activate_release.py` re-verifies catalog and DDS hashes but **not** the `.mtlx` or PNG (Pass 9). Does the bundle hash-lock every file, and are the DDS files produced deterministically enough to verify on the consumer's side? *Discovery reads `freeze_release.py` / `stage_release.py` first.*
3. **The first human test's consumer.** "A consumer" must be someone who can be reached without editing a consumer repo. A stock `usdview` on a fresh machine, pointed at an activated install, is the cheapest candidate: it needs no change from us or the platform, and `Consumers.md` §USD viewers already specifies it. *Hypothesis to confirm at Pass 1, not a lead fork.*
4. **Which version is the first release for users?** `matterlib-0.1.0` is a pilot (R7). Version Management records that the first release for users, and its number, is "a lead decision owned by the release-bundle phase" ("Create whatever version we need; we are unreleased", lead 2026-09-23). **A genuine lead call.** It interacts with Library Coverage: does the first published bundle carry today's articles, or wait for coverage? That wait would put the publish, not the machinery, behind that phase.
5. **Committed generated artifacts** (research Q8): keep committing `MatterLibrary.blend` and `*.catalog.json`, or build them into the bundle only? Open since 2026-09-23. It may fall to Blender from a Release for the `.blend`.
6. **The risk lane.** Discovery must verify it against the tree, per the rule. Publishing on a public repo is the method's "public edge" and is irreversible. The counter-hypothesis is that the publish is a single lead-run, lead-gated action with no service behind it. *Name and read the controls (promote / approval / freeze) before ruling.*
7. **The contract on the Creator-port set that ships.** The overlay cap is already 3 (P12, 2026-09-25) and the Creator tier has 9 ports. Confirm that the `schema_version` bump for the master token doesn't also have to absorb an unratified contract change still in flight from the Library Coverage research. *Discovery checks the Coverage thread's `## Resolved` against `LCDSchema.md` / `MasterSet.md`.*

**Outside this phase (recorded so it isn't re-asked):** immutability after promotion in `0.x` (research Q5) belongs to Version Management.

## Sources (pointers, not copies)

- `docs/Planning/Research/260923_R_StandaloneSetup.md`: R1, R7, R14; Pass 4 (independence model and coupling list); Pass 9 (options A/B/C, recommendation); Q5, Q8.
- `docs/specs/Distribution/ReleaseModel.md`: lifecycle, install-root layout and selector, integrity gates, and the Drift / Reevaluate markers above.
- `docs/specs/Contract/RuntimeCatalog.md` · `docs/specs/Contract/Manifest.md` · `docs/specs/Consumers.md`.
- `docs/Planning/PlatformDependencies.md`: P1–P4, P7, P8, P10, P12.
- On disk (2026-09-25): `library/releases/matterlib-0.0.1.*`, `matterlib-0.1.0.{lock.yaml,catalog.json,freeze.json,approval.json}`; `tools/releases/{stage,freeze,promote,activate}_release.py`, `validate_approval.py`, `serve_to_stage.py`.

## Discovery Log

_(numbered passes accrue here: examined → finding → decision / hypothesis / open question)_

## Discovery Status

- **Passes captured:** — (seed only)
- **Current working direction:** —
- **Open decisions:** Q4 (the first release for users) is the one known lead call.
- **Checks to carry forward:** the risk lane (Q6) must be verified against the tree, not inferred.

## Execution Log

_(populated during execution)_
