# Research — Testing drafts in USDLiveView (build it, put it where the viewer looks)

> **Question (lead, 2026-09-25, verbatim):** "We need to be using USDLiveView and actually publishing these materials to test them.. that is the entire point of USDLiveView.. You are putting things in inaccessible temp places and playing games with locations... we are building a tool to generate and test materials... So build them and put them in the right place so we can use them in USDLiveView and test them quickly... can you research what we need to do in the project to do this?"
>
> **Grounded on:** the lead's box, 2026-09-25, read-only. This repo's tree at `de7f538`, plus the consumer-side behaviour of USDLiveView and the Stage runtime it drives. Both are consumers (R1). **Only consumer-side facts are recorded here.** Their internals are private and are not cited.
>
> **Terms:** *install root*, *runtime catalog*, *projector*, *active-release selector*, *pilot release* are as in `docs/Glossary.md`. One new term is **proposed**, not adopted: **draft install** (Pass 4). It enters the Glossary only if `/discovery` takes it up.

## Pass 1 — Where the materials go today

**Examined:** `tools/preview_generators/make_preview.py`, its README, `.claude/skills/matter-generate/SKILL.md` §6/§6a, and the Phase03 doc's review-surface passes.

**Finding:** everything the maintainer is shown lives **outside the repo, in a temp directory**:
- `make_preview.py` writes `<Stem>_preview.usda` (and the PNG) to `--out-dir`, else `$MATTER_PREVIEW_DIR`, else `<tmp>/matter-preview/`. The README says it outright: "Nothing is written into the repo." Phase03 Pass 2 chose that on purpose: previews are "review material, not library content".
- Each slider setting is a **separate scene file** (`--set overlay1_density=1` → `<Stem>_preview_overlay1_density-1.usda`), so a layer review means juggling one temp file per setting.
- The skill (§6a) opens those temp scenes as `IMRSV_MATTER_SOURCE=<repo>/MatterLibrary <USDLiveView checkout>/usdliveview <scene.usda>`: a per-box checkout path plus an env var, typed by the agent.

**So the lead's complaint is accurate on the tree.** The article itself (`.mtlx`, textures) is written to its right place in `MatterLibrary/`. **What the maintainer actually looks at** is a throwaway wrapper scene in `/tmp`, reached through an agent-typed command.

## Pass 2 — What USDLiveView can do now vs what we use

**Examined:** USDLiveView's roadmap, its materials spec and its launcher, as consumer-facing surfaces.

**Finding: we use USDLiveView as a dumb file viewer, and it is much more than that now.**

| USDLiveView capability | State (2026-09-25) | Needs | Do we use it? |
|---|---|---|---|
| Open a `.usd`/`.usda` and render it (Storm, the same OpenUSD 26.03 + MaterialX stack as our preview) | done (its Phase 01/02) | nothing | **yes**: the temp preview scene |
| **Installed Materials browser**: search + Class filter, then Apply to a clicked mesh | done (its Phase 03) | **Stage** running, and the article in **Stage's installed catalog** | **no** |
| **Creator parameter sliders** (tint, UV scale/offset/rotation, overlay/mask density, roughness bias), live, saved in the composition, undo/redo | **done (its Phase 04, COMPLETE 2026-09-25)** | Stage, a **composition Stage has loaded**, and the article's material bound through Stage | **no** |
| Fly / orbit / frame | done (its Phase 05) | nothing | yes |

- **Stale in this repo (a finding, not fixed here):** the skill §6a says "USDLiveView has no slider controls yet (its own Phase 04)". The Phase03 doc's out-of-scope table says the same ("parked"). **Both went stale on 2026-09-25.** The `--set`-scene workaround exists only because of that claim.
- **The browser and the sliders both go through Stage.** The viewer authors nothing itself: listing, applying and parameter edits are Stage operations. An edit writes the override on the bound material instance in the carrier-rule form (value on the Material input, `NG_*` input connected), so any USD tool renders the saved result. That is our own LCDSchema §Carrier rule.
- **Our preview scene cannot use the sliders even with Stage up.** It binds the article under `/World/Library/Materials/…`, not as a Stage material instance in a Stage-loaded composition. USDLiveView's slider smoke test drives a real `.imrsv` test composition (on a throwaway copy, because every edit saves).

**Hypothesis:** "test quickly in USDLiveView" means **the full loop**: open a test composition → pick the draft in the browser → apply it → drag the sliders. That loop needs the draft to be **in Stage's installed catalog**, and today nothing puts it there.

## Pass 3 — What Stage actually serves (probe: read the install root)

**Examined:** the Stage runtime's install root on this box (`$IMRSV_STAGE_RUNTIME/MatterLibrary/`), and Stage's library-discovery behaviour as a consumer-side fact.

**Findings:**
- **Stage finds its library ONLY beside its own executable**: `<runtime>/MatterLibrary/`, selector-first → `releases/<active>/<active>.catalog.json` + that release's `materials/`. Its only fallback is a legacy flat dev-fixture layout (a catalog file with a fixed `matterlib-0.1.0` name). **No environment variable points Stage at a Matter checkout.** (`IMRSV_MATTER_SOURCE` only affects the viewer's own search path.)
- **Stage does not check approval.** It serves whatever release the selector names, provided that release's catalog exists. Approval, freeze and hash checks all live in *our* `activate_release.py`, which **refuses** an unapproved release.
- **Measured on this box:** the selector names `matterlib-0.1.0`, installed 2026-09-23. It holds **12** articles. The repo holds **17**. **Missing from what Stage serves, so invisible in the USDLiveView browser:** `Earthenware_Natural_Clean_Base_s01_v01`, `Glass_Green_Clean_Base_s01_v01`, `GreyCard_Neutral18_Clean_Base_s01_v01`, `Oak_Natural_Clean_Base_s1_v01`, `ABS_Glossy_Clean_Base_s01_v01`. That is every article Phase03 produced. The other 12 `.mtlx` are byte-identical to the checkout (`diff -rq`).
- **The only route in today is the full release lifecycle**: settle statuses → stage → freeze → qualify → promote (approval) → deploy → activate. That is built for shipping an immutable release, not for a maintainer looking at a draft. Using it per draft would burn a release id on every look and break "immutable once installed".
- **A viewer-side trap for edited articles (latent, P7):** with `IMRSV_STAGE_RUNTIME` set, the viewer's launcher puts *every* installed release's folders on the search path **before** `IMRSV_MATTER_SOURCE`. A **new** name resolves from the checkout. But an article that is **also** in a release (for example a re-assembled `ABS_Matte`, or one whose shared layer PNG was regenerated) resolves `@Name.mtlx@` to the **released** copy and its released textures. The maintainer would be reviewing the old one. Our preview scene avoids this only because it references the `.mtlx` by absolute path.

## Pass 4 — What the project needs (options, not a choice)

The gap has two halves: **where the review scene lives** (small) and **how a draft reaches Stage's catalog** (the real one).

### A. Review scenes in a stable place (small; view-only)

The preview `.usda` (and PNG) go to a **fixed, in-repo, gitignored folder** instead of `<tmp>` (for example `library/preview/`, beside the existing gitignored `library/staging/`). The skill prints one path. `$MATTER_PREVIEW_DIR`/`--out-dir` stay as overrides.
- It fixes "inaccessible temp places" and nothing else. **No browser, no sliders.**
- It sits inside the Phase03 rule "never written into the repo" if the folder is gitignored: nothing is *committed*. It does reverse Pass 2's "temp location" choice, so it needs the lead's word.
- Size: a `/quick-fix` (`make_preview.py` default + README + skill §6/§6a).

### B. A **draft install** into the Stage runtime's install root (the real loop)

A producer tool (name illustrative: `tools/releases/install_draft.py`) that, on the maintainer's box:
1. **projects a runtime catalog from the working tree**, taking *every* article under `MatterLibrary/materials/` at its on-disk `vNN` with `status: draft`, reusing the existing projector's field derivation (it projects from a lockfile today, so it needs a working-tree mode or a generated throwaway lock);
2. **writes an install** `releases/matterlib-draft/` (a **distinct, never-released id**, so it can't be mistaken for a release) with that catalog plus `materials/` and `textures/`. Either copied, or **symlinked to the checkout** so a re-assembled article or regenerated layer shows with no re-install (a new article still needs a re-projection);
3. **points the selector at it** (temp-file + rename, like `activate_release.py`), and offers a one-command **revert** to the prior selector value;
4. and the loop is then: **restart Stage** (there is no in-session release change by design, ReleaseModel step 7) → `usdliveview <throwaway copy of a test composition>` → browse → Apply → sliders.

What B runs into, which is why it is a phase and not a quick-fix:
- **R1 (producer doesn't deploy into consumers).** ReleaseModel already carries this as Drift/Reevaluate for `deploy` and `activate_release.py`. A draft install is exactly that shape. **Needs a lead ruling:** a maintainer-box dev tool writing into the maintainer's *own* runtime is sanctioned, and it is not a release.
- **The approval gate.** It must be a separate command that never creates, reads or touches `library/releases/` records, like `recover-unapproved` is kept separate from `activate`. `activate_release.py activate` must keep refusing it.
- **Release pin / ReleaseConflict.** Applying through Stage stamps the composition's release pin (`imrsv:matterlibRelease`) with the draft id, so switching back to `0.1.0` makes that composition conflict **by design**. This is why the test composition must be a throwaway copy, made fresh each session.
- **`.dds`.** A draft has no compressed textures. The USD/Storm path reads the PNGs. Whether Stage's viewer-facing path needs `.dds` at all is **unverified**.
- **Symlinks.** Whether Stage's discovery follows a symlinked `materials/` is **unverified** (probe it before choosing copy vs link).
- **The test composition.** USDLiveView's slider smoke uses a cube-and-cone composition from the Asset Library. Options: reuse that, or have this repo own a small Matter test composition (sphere + cube + plane, UV-grid floor). **An owned one is a consumer-format file in a producer repo (R1 again).**

### C. Align the skill and docs with USDLiveView as it is today (rides with A or B)

- Skill §6a: drop "no slider controls yet" and the `--set`-scene workaround once B exists. §6a becomes "install the draft, restart Stage, open the test composition, pick it".
- Keep the headless PNG (§6): the agent's own look, and the `transmission` limits, are unchanged.
- Phase03's "USDLiveView LCD sliders: other project (parked)" row and AuthoringHarness §Shipped's review line become stale at the same time. Annotate them with a date; do not delete them (the HARD RULE).

### D. Consumer-side asks (for `docs/Planning/PlatformDependencies.md`, not done here)

- **P7 already covers it:** the viewer should honour the active-release selector rather than putting every release on its search path. With a draft install active, that is what makes the viewer and Stage resolve the **same** copy (Pass 3 trap).
- **Possible new ask (Stage):** an env-var override for the Matter install root (for example "serve from this directory"). With it, B would need **no writes into the runtime at all**: this repo owns a draft install root on disk and points Stage at it, which dissolves the R1 tension. Stage-side work, so it stays an ask. Unverified whether Stage would accept it.

| Route | Gives the lead | Size | Blocked on |
|---|---|---|---|
| A | one stable path to open; view only | `/quick-fix` | lead OK to reverse "temp location" |
| A + B + C | **the full loop: browse, apply, sliders, on every draft** | a phase (`/discovery`) | R1 ruling; the test-composition choice; two small probes (symlinks, `.dds`) |
| A + C + D (Stage env override) | the same loop, no writes into the runtime | a phase + a Stage ask | Stage accepting the override |

---

## Status

- **Passes captured:** 4.
- **Current direction:** the preview tooling was designed as a headless-render helper with an optional look (Phase03 Pass 2), and USDLiveView has since grown into the real test bench (browser plus live sliders, 2026-09-25). **The missing piece is a way to get a working-tree draft into Stage's installed catalog without cutting a release**: a *draft install* (B). A is a same-day quick win, but view-only.
- **Open questions (lead):**
  1. **Target loop:** view-only (A), or the full browse/apply/slider loop (B, or D)? Recommendation: A now, then B as a phase.
  2. **R1:** may a maintainer-box dev tool in this repo write a non-release `matterlib-draft` install and the selector into the maintainer's own Stage runtime? Or do we ask Stage for an install-root override (D) instead?
  3. **Preview location (A):** is an in-repo gitignored `library/preview/` right, or another name/place?
  4. **Test composition:** reuse USDLiveView's cube-and-cone smoke composition, or have this repo own one?
- **Stale, found here (not this verb's errand):** skill §6a and the Phase03 out-of-scope row both say USDLiveView has no sliders. That is false since USDLiveView Phase 04 completed on 2026-09-25.
- **Unverified:** whether Stage follows a symlinked install; whether a draft with no `.dds` loads through Stage; whether Stage re-reads the catalog without a restart (restart assumed, per ReleaseModel step 7).
- **Not touched:** the working tree carries another session's uncommitted edits (`Fingerprints01`/`Scuffs01` PNGs and generators). This research read none of it and committed none of it.
- **Next step:** the lead answers Q1–Q4. Then `/quick-fix` for A, and `/discovery` for a draft-install phase if B or D is chosen. **This is a deliberate gate, not a slide.**
