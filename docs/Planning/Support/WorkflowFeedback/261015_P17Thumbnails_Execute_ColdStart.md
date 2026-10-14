# Workflow Feedback — P17 (Thumbnails) / execute → close / cold start

| | |
|---|---|
| **Verb** | `execute`, then the close (`execute_close.md`) in the same session at the lead's *"close"* |
| **Unit** | `P17` (Thumbnails; not the Library Service, which minted `P17` ids first) |
| **Mode** | cold start, through the close |
| **Outcome** | done: 17.1 – 17.5 as planned, 17.6 added at the lead's word (JPEG and the dev install), `dev.6` and `dev.7` published, closed and pushed (`2fb1995`) |
| **Shape** | behavior-touching |
| **Confidence** | Ran fully: execute (Build, Try with five clicks, Strengthen) and the close (A⁻ – E). **Not exercised:** `execute_highrigor.md`, `execute_repair.md`, the issue-close coda (no issues). |
| **Date** | 2026-10-15 (the run began 2026-10-14) |

---

## Items, ranked

### 1 — A published file format was closed "by recommendation" without asking what every consumer reads, and shipped wrong `[doc-gap]`

**Grounding.** The Brief (discovery Pass 1) closed RD-P17-3 as *"WebP at 1024 in the snapshot… closed with a recommendation, unless you say otherwise"*. Its consumer sweep, F-P17-15, read only the website's asks and concluded *"No other consumer has asked for material thumbnails"*: an absence claim, recorded as a fact. Execute carried WebP into `dev.6` without re-asking. The lead, minutes after the publish: *"you snuck that fancy foramt in instead of jpeg or png... so studio can't use any of these thumbnails becuase we are not just building a website.. thes things are for blender, unreal engine, and ALSO the web"*. The platform had to write an ask (Unreal 5.8 has no WebP reader). It cost a second publish (`dev.7`), a second push and a re-render of the whole snapshot. HDRIs, the precedent in the same repo, were already JPEG in the dev install.

**Proposed fix.** In discovery's consumer sweep, for any artifact a phase publishes (a file format, an image, a schema), list **every consumer the library names** (`docs/specs/Consumers.md`) and **what each one can read**, with the reading's source. *"No consumer asked"* is an absence claim: it may close a *scope* question, never a *format* one. In execute, the row *"changing the SHAPE of data many tools parse"* should name file formats explicitly: **a format choice on something published is a shape change for every reader, including readers outside this repo.**

**Where it'd live.** `discovery.md` (the consumer sweep, the reuse check); `execute.md` §Verify before edit (the shape row). Possibly `LOCAL_DELTAS.md`, which names this project's consumers (Blender, Unreal, the website).

---

### 2 — The look was approved on two mid-tone fixtures, and the extremes surfaced 42 GPU-minutes later `[self-error-doc-could-prevent]`

**Grounding.** Click 1 judged the showcase look on `Oak_Natural` and `StainlessSteel_Polished`. The lead kept it as scene v1 (*"it looks great!"*). At click 4, after all 82 were made, whites sat in Khronos PBR Neutral's shoulder (RGB 237–245; marble's veins gone), and clean clear acrylic and reeded glass were invisible on the pane. Both are properties of the *look and subjects*, and both were knowable at click 1 with two more fixtures. The fix (exposure −0.5) was then a scene v2 and a 42-minute re-make, so the lead deferred it (*"this is fine for now"*). `execute.md` §TRY already has *"ask what your fixture distribution makes impossible to see"*. I read it as being about seeded data and did not apply it to a render look.

**Proposed fix.** One clause in §TRY: *"For a look (lighting, tone curve, exposure), the first click's fixtures include the extremes the look must hold: near-white and near-black albedo, a mirror, a clean clear surface. Two mid-tones prove only the middle."*

**Where it'd live.** `execute.md` §TRY (the fixture-distribution paragraph); possibly the matching discovery line where First human test fixtures are chosen.

---

### 3 — Two `git log` ranges printed in one call were read as one, and the lead was told a foreign push range that was false `[self-error-doc-could-prevent]`

**Grounding.** Before the 17.5 push I ran `git log origin/main..HEAD` and `git log HEAD..origin/main` in one call with no separator. The second command's two lines (the platform's *Platform sky asks* passes, already on origin) read as the tail of the first. I told the lead *"16 commits… nine are from other sessions"* and asked approval for that list. The push was refused (non-fast-forward); I fetched, saw the truth, merged and corrected myself in the handback. Afterwards I printed `--- incoming:` between the two ranges, and that worked. `.claude/CLAUDE.md` already says *"output from several files without per-line names… label it"*, but about `grep -h` and stacked `head`, not about git ranges.

**Proposed fix.** In the §Git trap table, a row: *"two `git log` ranges (unpushed / incoming) in one call → print a label between them (`echo --- incoming`), or run them as two calls. Unlabelled, the incoming range reads as part of the push."*

**Where it'd live.** `.claude/CLAUDE.md` §Git (the trap table), or upstream if the Refiner judges it portable (likely).

---

### 4 — Asked how a consumer behaves, I answered "I can't see its side" while its repo and docs were on disk `[self-error-doc-could-prevent]`

**Grounding.** The lead asked whether Studio and the website need to do anything to get new pictures. I said the website side was *"the platform's, and I can't see it from here"*. The website's checkout (`../IMRSV_Web`) was a sibling folder, and its research doc *"Matter Thumbnails Arrive"* already answered it: an hourly mirror reads each new snapshot unaided. I found that out only when the lead pointed me at the doc, and had to correct my answer. `LOCAL_DELTAS.md` §Separation already sanctions reading a consumer's docs at origin, read-only.

**Proposed fix.** Under §Separation: *"Asked how a consumer behaves, read its docs at origin first (read-only, `git -C <its checkout> show origin/main:<path>`); 'I cannot see it' is true only after looking."*

**Where it'd live.** `LOCAL_DELTAS.md` §Separation (the consumers' checkouts are this project's shape).

---

### 5 — Publishing a dev snapshot needs a push mid-phase, and no row says so `[doc-gap]` (port gap)

**Grounding.** `build_snapshot.py --publish` refuses unless the target commit is on `origin/main`. So 17.5 and 17.6 each needed a push at the lead's word, mid-execute, plus the close's own push: three push questions in one phase. `execute.md` says push is asked for once, at the close. `LOCAL_DELTAS.md` carves out only *"a hand-off to the other machine"*. The lead handled it fine (*"push and publish"*), but the doc reads as if I broke the rule.

**Proposed fix.** In `LOCAL_DELTAS.md`'s push row: *"A publish (a dev snapshot, a runtime) needs its commit on origin first: ask once for 'push and publish' together, naming the push range. That word covers both."*

**Where it'd live.** `LOCAL_DELTAS.md` (the *"push is asked for once per phase"* row).

---

### 6 — A cache keyed on a version number the agent bumps by hand let stale pictures read "fresh" `[doc-gap]` (a learning, possibly portable)

**Grounding.** The Brief's record keyed staleness on `SCENE_VERSION`. Within an hour of 17.1 I tuned the look three times without bumping it, and the stale check said *"fresh"* about pictures of the old look (F-P17-17). I caught it only because I noticed the risk while re-rendering. The fix hashes the inputs as sent (look, subject, the Blender-side scripts, the cast), with the version kept as the human label. It paid off later: the 17.3 cast change and the 17.6 sort change re-made exactly the affected pictures, and none else.

**Proposed fix.** A learning, or a line in the plan/execute guidance on caches: *"A staleness key built from a constant someone must remember to bump will be wrong the first time they are busy. Key on a hash of the inputs as used; keep the version as a name."*

**Where it'd live.** `docs/Learnings/` (a tooling domain), or upstream if the Refiner sees it as portable.

---

## Keep these

- **"Look at the output before reading the number", and showing a sheet only after looking at it myself.** It caught every fixture defect before the lead saw it: the ghost around the polished-steel cube, Loam rendered pink (a sky-facing face gets a stop more light), hair behind the teeth, an invisible tongue, the cloth "mound", the twice-drawn pane. None of them could have gone red in a gate.
- **Bisect by construction (`execute.md` §BUILD).** The mirror ghost was found by hiding the cube, then the backdrop, then a diffuse swap, after denoiser and caustics toggles proved innocent. Four renders, no guessing.
- **"A present lead is for seeing, not approving."** Five clicks, each a one-line verdict (*"they all suit"*, *"they all work"*), and step boundaries without a stop. The lead stayed in the loop at low cost.
- **The shape row in §Verify before edit.** It made me grep who reads `groups.py` before flipping Matter's `shown`, which found the dev catalog. That kept a false *"thumbnails served"* out of the dev install until 17.6 made it true.
- **Pushing your own tip by value, with the range read first.** It made the 16-vs-14 misreading recoverable: the refused push and the re-read range showed the truth before anything wrong went public.
- **One quiet progress line for the close.** The close ran ~10 rows and came back as one handback.

## Dead weight

None.

## Open questions

1. **For the lead (and the platform), not the Refiner:** I suggested in chat that the platform's deploy re-serve the dev install whenever a new `matterlib-*-dev.*` tag appears, so Studio picks up new thumbnails without a hand-run `serve_to_stage.py`. The lead did not take it up. It is recorded here because it lives nowhere else; it would be an ask in the platform's own docs if wanted.
2. **For the next `/matter-batch` or the Refiner:** the batch skill should run `make_thumbnails.py` before its review page (RD-MP-4). It was deferred at the close because `.claude/skills/matter-batch/SKILL.md` holds another session's uncommitted edit (Phase17's deferral ledger). Is a skill file the Refiner's lane, like `.ai/commands/`? `.claude/CLAUDE.md` §Lanes does not list skills either way.
3. **The run ran well past the 60–90-minute target.** The scope alarm is *"phase too big"*: one phase held a full-library GPU run (48 min), a publish, a format redo and a second publish. Thumbnails could have split at 17.4 / 17.5. The Brief's split signal considered Matter vs Character, not make vs publish.
