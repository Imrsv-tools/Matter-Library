# Workflow Feedback — P08 / research → quick-fix → discovery → execute → research / cold start → suspend-handoff

| | |
|---|---|
| **Verb** | One session, five verbs: `/research` (reviewing a platform-authored research doc) → `/quick-fix` (A3, lead-directed) → `/discovery P8` (seeded and renumbered in the same session) → `/execute P8` → `/research` (lead-directed, mid-step 8.1) |
| **Unit** | P08 (Character Appearance for Studio); research `260928_R_PlatformAppearanceAsks`, `260928_R_HairAndNailRendering` |
| **Mode** | cold start → suspend-handoff (the lead: *"yes to 1 and 2, then hand off"*) |
| **Outcome** | suspended. 8.1 landed the `Hair` token and `Hair_Natural`, then the lead judged the hair unusable; research done and the rework planned in the Resume block. Nothing pushed since `de08ccc`. |
| **Shape** | behavior-touching (tools, Blender masters, one article, contract docs) |
| **Confidence** | Ran fully: research, quick-fix, discovery, execute through its first sitting. **Not exercised:** the close, `/plan`, a Storm probe of the reworked hair. |
| **Date** | 2026-09-28 |

---

## Items, ranked

### 1 — A decision closed by a standing ruling still hid an untested LOOK, and the Brief shipped "no open decisions" `[doc-gap]`

**Grounding.** Discovery closed RD-P08-1 (a *settings-only* `Hair` master) with the four fork tests: Decision of record 1 answers "Chiang or OpenPBR", so no lead call was needed. It did answer that axis. But the decision's real premise was *"an OpenPBR Masked card with anisotropy will read as good hair"*, and nothing tested it. The Brief went out with **"Open decisions: none for the lead."** The first sitting reversed it in one message: *"Hair still looks plastic, no transparency, no SSS... hair is not a thick solid"*. A research detour and a rework followed. The same premise sat under `Nail_Natural` (*"Will be similar issue with nails"*).

**Proposed fix.** In `discovery.md` §Forking, test 1: *"A ruling answers its AXIS, not whether the result will LOOK right. When the Outcome is an appearance and a decision sets how something looks, render it (a cheap probe on the real fixture) before the decision binds, or list it as a YOUR CALL marked 'untested look'."*

**Where it'd live.** `discovery.md` §Forking to the lead (test 1).

---

### 2 — The first human test used a fixture that could not show the property: hair on a cube `[self-error-doc-could-prevent]`

**Grounding.** The Brief's click 2 was *"the new hair article on a cube"*. At the sitting I built four tinted cubes in Blender, and the lead read hair on a solid block (*"hair is not a thick solid"*). A cube cannot show a card's cut-out, its light through the fibre, or its soft edges. `execute.md` §TRY already says *"ASK WHAT YOUR FIXTURE DISTRIBUTION MAKES IMPOSSIBLE TO SEE"*, and I did not apply it, because the Brief (mine) had already named the cube. This recurs `_RefinementBacklog.md`'s *"an instrument that cannot see the thing"* class; this time the fixture was chosen at **discovery**, where no such question is asked.

**Proposed fix.** Carry the §TRY question into `discovery.md` §The Brief, first human test: *"The fixture is the one the substance lives on in use (hair on cards, a nail on a finger, glass with something behind it). A primitive is fine only when the property is colour or scale."*

**Where it'd live.** `discovery.md` §The Brief (First human test); a recurrence for the backlog class.

---

### 3 — Forty-nine corrupted files sat under *"any file you did not touch is another session, live"* for three verbs `[doc-gap]`

**Grounding.** `git status` showed 49 modified texture PNGs from the first command of the session. `.claude/CLAUDE.md` §Git says such a file *"is another session, live, right now"*, so research, quick-fix and discovery each correctly left them alone and said so. Only `/execute`'s baseline turned it into a finding: `run_all.py` had 5 FAIL where Phase07 closed at 1. Measuring showed every tracked texture was a 67–74-byte **8×8 PNG stub** (mtimes 2026-09-23 15:02 and 2026-09-27 20:52), while the real objects sat in the local LFS store. That was no live session: it was corruption. The dev install **symlinks the working tree into Studio**, so the stubs reached the platform for about a day; the platform's "strange pattern" report may be partly this. The lead restored them (*"yes restore the textures"*).

**Proposed fix.** In `.claude/CLAUDE.md` §Git, next to "any file you did not touch is another session": *"Measure before you assume liveness. A foreign modification days older than its last commit, or an LFS-tracked file whose working copy is a few bytes, is not a live edit. Surface it to the lead at kickoff with the measurement (`stat`, `git diff` on the LFS pointer), and never restore it yourself."* A `docs/Learnings/` Git-LFS entry could record the tell: a pointer diff whose `size` collapses (`2105430` → `74`).

**Where it'd live.** `.claude/CLAUDE.md` §Git (or `execute.md` §Before you touch step 2); a Learnings entry for the LFS tell.

---

### 4 — No rule for the lead directing `/research` from inside an `/execute` step `[doc-gap]`

**Grounding.** Mid-8.1 the lead said *"YOu need to research how to render hair"*. `research.md` §Landing covers research → `/quick-fix` or `/discovery`, and `execute.md` §Divergence covers *"the lead asks for work that belongs to no phase"*. Neither covers the executor suspending **its own step** to research the step's premise, in the same session. I improvised:
- suspended 8.1 in the ledger with the verdict verbatim;
- announced the lane switch;
- wrote a research doc with a disposable probe run in the lead's live Blender (script committed beside the doc);
- then wrote a Resume block that routes the rework back to 8.1.

It worked; nothing told me the shape.

**Proposed fix.** An `execute.md` §Divergence row: *"The lead directs research on the current step's premise → suspend the step in the ledger with the verdict, name the lane switch, land a research doc (probe script beside it), then resume the step or hand off with the rework in the Resume block. The step stays unpushed until the rework lands."*

**Where it'd live.** `execute.md` §Divergence.

---

### 5 — "Pull" on a diverged trunk with a dirty tree has no row in the git table `[doc-gap]`

**Grounding.** *"can you pull"*: local `main` was 3 ahead (unpushed refiner and retro commits), `origin` 1 ahead, and the tree dirty (item 3's stubs). `git rebase` refuses a dirty tree, and `--autostash` is banned. The table's *"converge a diverged trunk"* row prescribes `git reset --mixed origin/main`, which **drops unpushed local commits**. A rebase would also have rewritten three SHAs a sibling may hold by value (the table's own *"capture your SHA once, by value"*). I used `git merge --no-edit origin/main`: it works on a dirty tree with no overlapping paths and keeps every local SHA an ancestor.

**Proposed fix.** A row: *"Pull with unpushed local commits and a dirty tree → `git merge --no-edit origin/main` (keeps local SHAs as ancestors; refuses only if a dirty path overlaps). Never `reset --mixed` here: it drops the unpushed commits."*

**Where it'd live.** `.claude/CLAUDE.md` §Git, the "looks like a measurement" table (or its converge row).

---

### 6 — A live probe that skipped the harness's UV wrapper produced the defect it then diagnosed `[self-error-doc-could-prevent]`

**Grounding.** The hair probe imported the rig's `character_scene.usda` straight into Blender. The rig divides each part's `st` by `meters_per_tile` in a wrapper layer (`job.py:111`), and I skipped that, so the skin rendered 100× too large as worm-like furrows. The lead saw them and asked about P65's "scale issue", and the accident became F-P08-8 (the mesh-UV rule, now in `LCDSchema.md`). `execute.md` §BUILD already says *"make the probe load EXACTLY the harness's inputs"*. The outcome was lucky, not designed.

**Proposed fix.** None new: the rule exists. A recurrence note for the backlog's probe-vs-harness class.

**Where it'd live.** `_RefinementBacklog.md` (recurrence count).

---

## Keep these

- **Baseline the gates before the first edit, and compare the SET** (`execute.md`). It caught the 49 stub textures, and it proved 8.1 added no red (the same five lanes before and after; the exporter check line-identical).
- **The act is the unit; the lead drives it** (`execute.md` §BUILD). The first sitting after one step found the fundamental hair defect. Draining 8.1–8.4 first would have built twelve lips and nails on the same wrong premise.
- **`git show --stat` read-back after every commit.** Twelve commits, each reconciled; none carried a foreign path.
- **Where rulings live** (`discovery.md`). C4/C5, Decision of record 1 and Phase07's Not now closed four real forks without a round trip. Item 1 is about what a ruling cannot close, not about this rule.
- **Verify a capability in the system's own artefact** (`research.md`). Thin-walled translucency was confirmed in the local `open_pbr_surface.mtlx` and Storm's `mx_translucent_bsdf.glsl`, and Blender's `Thin Wall` in the live node, where the web pages and the manual were silent or stale.
- **The Grep-absent fallback** (`.claude/CLAUDE.md` §Codebase search). Grep was missing all session; single-statement `grep` worked with no friction.

## Dead weight

None.

## Open questions

1. **What wrote the 8×8 stub textures into `MatterLibrary/textures/`** (mtimes 2026-09-23 15:02 for 29 files, 2026-09-27 20:52 for 20)? No session of this run did. The source is untraced; a tool or test writing into the real tree is the likely suspect. **A lead decision:** `/research` or an issue.
2. **Did the platform's "strange pattern" (P65) come from the UV scale, the stub textures, or both?** Only the platform can answer. `PlatformDependencies.md` P18 now carries the formula and the stub window.
3. **`check_exporter.sh` is red for its environment** (its Python cannot import MaterialX), before and after this run. No unit owns it. **A lead decision** whether it is a quick-fix.
