# Workflow Feedback — P07 / discovery → execute / cold start, suspended

| | |
|---|---|
| **Verb** | `discovery` → `execute` (one session: discovery Pass 1, the lead's rulings, then `/execute` steps 7.1–7.2) |
| **Unit** | P07 (Character Materials) |
| **Mode** | cold start; suspend-handoff at the 7.2/7.3 boundary (lead: *"how is context... should we handoff?"*) |
| **Outcome** | suspended — Brief complete (L1–L4 ruled); 7.1 ✅ (first skin, lead sitting); 7.2 click 2 ✅, click 3 owed (lead can't test Stage now); a Phase05 rig defect found and fixed |
| **Shape** | behavior-touching |
| **Confidence** | Ran fully: `discovery` (Pass 1, fork-authoring, the rulings pass), `execute` Build/Try on two steps, the commit discipline, `retro`. **Not exercised:** `execute_close`, the repair ladder, high-rigor. |
| **Date** | 2026-09-27 |

Step 0: the handoff state was already on disk (the phase doc's Resume block). Two findings lived only in commit messages and were routed before this file: `tools/parity/JOB_FORMAT.md` (Phase06's contract: units in every file a driver loads; Phase05's F16 is mostly the scale bug) and `docs/Learnings/Blender/Blender.md` B7.

---

## Items, ranked

### 1 — Discovery offered a pre-release process rule to the lead as a fork, when a standing lead ruling already answered it `[self-error-doc-could-prevent]`

**Grounding.** Lead call 4 asked how Studio gets the candidates, because `ReleaseModel.md` requires `approved` before a freeze. The lead replied: *"Here we are with burocracy again… stop working about non-existant version control on an unreleased product that only the two of us know anything about"*. Fork test 1 ("ANSWERED?") should have failed it. The lead had already ruled *"Make a material, serve it to stage. no versioning"* (2026-09-25), and `260926_R_BigPicture_NimbleSetup.md`'s own process note says *"Keep release checks out of content work before the first release"*. I ran test 1 against rulings about the **mechanism** (releases, freezes) and missed the one about the **spirit** (no release ceremony before the first release). This is the second time it has been flagged on this project (the BigPicture note is the first).

**Proposed fix.** In `discovery.md` §Forking, test 1: *"ANSWERED? — including by a lead ruling of the same SPIRIT that names a different mechanism. 'No versioning before the first release' answers every question whose premise is a release rule."* And a local row: *"Before the first release, the release lifecycle (`ReleaseModel.md`, the approval lanes) never gates content work or reaching a consumer; the dev install (`serve_to_stage.py`) is the path."*

**Where it'd live.** `discovery.md` §Forking (test 1; likely portable) · `LOCAL_DELTAS.md` §Weighting (the local row).

---

### 2 — "The knob barely moves the picture" was read as a property of the material, not as a broken instrument `[doc-gap]`

**Grounding.** Phase05's closed doc says of Marble's radius (F13): *"The radius changes Blender's close-up little in this front-lit scene … so matched lighting is not what hides it"*, and closed with F16 open for Phase06. The real cause was the rig: every setting scene lacked `metersPerUnit`, so Blender imported it at 1/100 scale. Every opaque material still matched, because nothing opaque depends on distance. This run hit it at once: a skin scattering 4.8 mm rendered pale white (ΔE 12.8). Fixed, it measured 2.69, and Marble went 3.95 → 2.60. The instrument had only ever been validated on subjects insensitive to the defect. A parameter that *should* have moved the output and didn't was the tell, and it was accepted as physics.

**Proposed fix.** A row in `execute.md` §Verify before edit: *"A parameter that should matter barely moves your measurement → suspect the harness before the subject. Check that the instrument can SEE that parameter (move it by 10x; confirm the harness's own inputs, units and scale) before recording the subject as insensitive."*

**Where it'd live.** `execute.md` §Verify before edit (portable).

---

### 3 — Finding ids are phase-local, but they get cited across phases, and they collided `[doc-gap]`

**Grounding.** I numbered this phase's rig finding **F12** (Phase07's series ran F1–F11 at discovery). `tools/parity/JOB_FORMAT.md`, which the UE agent reads, already lists **Phase05's F12** (bump strength) as an open question for Unreal. The Phase07 commit message and ledger now say "F12" about something else, and the UE machine reads both. `discovery.md` warns that "a shared ID series is a collision surface" for gate ids and ordinals, but not for finding ids, which look private until a hand-off doc cites one.

**Proposed fix.** *"Finding ids are phase-scoped. Any doc outside the phase doc that cites one (a hand-off contract, a tool doc, another phase) qualifies it: `P05-F12`."*

**Where it'd live.** `Methodology/AgenticEngineering_Workflow.md` (id conventions) or `execute.md` §Keep the lead oriented (portable).

---

### 4 — When a probe passes and the harness fails, diff the harness's inputs before varying settings `[self-error-doc-could-prevent]`

**Grounding.** Diagnosing the pale skin took about eight Blender probes varying one thing at a time: subsurface weight, method, the driver's ray-visibility flags, GPU vs CPU, the normal map, transmission visibility, hiding objects. Every probe used `test_scene.usda`; the rig loads each setting's own `scenes/<id>.usda`. Swapping in the file the harness actually loads found it in one run. The method says to re-ask the loop "when you stop authoring and start diagnosing", but not **what** to ask.

**Proposed fix.** *"When the same thing works in your probe and fails in the harness, first make the probe load exactly the harness's inputs (the same files, the same entry point), then vary settings. Bisect by construction, not by hypothesis."*

**Where it'd live.** `execute.md` §Build (beside "re-ask the moment the loop changes character"); portable.

---

## Keep these

- **Pass 1 top-down plus the four-point capability claim.** It found F8 (a new article could never reach Blender, because the library read the frozen release catalog), which is the Outcome's entry path, before any code. Built at 7.2; the lead's click 2 passed on it.
- **"Record a lead ruling in the lead's own words."** L1 arrived as a question (*"what sets us up for the best quality down the road…"*). Quoting it let the answer be argued on the lead's criteria, and the Brief records why.
- **The public-repo rule applied to a lead quote.** A platform phase number in L4 was replaced with a description.
- **The gate registry's `FALSE RED:` convention.** It gave the asset-library verifier's GreyCard failure a place to be recorded instead of a silent tweak.
- **The divergence table's "small surprise: note and proceed".** The rig fix was two lines, noted in the ledger and commit, and the phase kept moving.

## Dead weight

None.

## Open questions

1. **Lead decision:** `run_all.py`'s `approval_binds_freeze` has been red since Phase04 (the pilot re-approval is owed). Under L4 (*"stop working about non-existant version control on an unreleased product"*), should the release lanes be advisory until the first real release, or should the pilot simply be re-approved once? A permanently red gate teaches every run to read "FAIL" as normal.
2. **Owed, not a methodology item:** 7.2's click 3 (USDLiveView through Stage) waits for the lead; Stage was left running on the working tree (`serve_to_stage.py --off` restores it). Both are in the phase doc's Resume block.
