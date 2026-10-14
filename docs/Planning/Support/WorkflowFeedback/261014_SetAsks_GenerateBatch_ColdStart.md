# Workflow Feedback — SetAsks / matter-generate → quick-fix → research → matter-batch / cold start

| | |
|---|---|
| **Verb** | `/matter-generate` (five times) → a lead-directed `quick-fix` → a lead-directed `research` pass → `/matter-batch` (one session, every step lead-directed) |
| **Unit** | `SetAsks`: the platform's generated architectural Set, `docs/Planning/Research/261004_R_PlatformSetMaterialAsks.md` |
| **Mode** | cold start |
| **Outcome** | done. **Five draft articles** (`LED_CoolWhite`, `Concrete_Polished`, `PowderCoat_Textured`, `Terrazzo_Polished`, `Aluminium_Raw`; `d32245c`, `b1e6765`), **the one-mesh profile gate** (`4135e25`), **the Blender library rebuilt twice** (57 → 87 → 88 articles; `fad6b0c`, `194031d`), **Pass 2** of the ask doc (`f11ffcb`), **ledger row M5** (`21ed149`), **batch `261004-1`** sweeping the five (`4c9e261` … `8fded09`), the sweep recorded on M5 and the doc (`89e4fc8`). All pushed on the lead's word. Stage on this machine re-served (89 articles). |
| **Shape** | behavior-touching (five articles, a gate, the Blender library), plus docs |
| **Confidence** | Ran fully: `/matter-generate` §1–6, a quick fix with its negative cases, a research pass and its footer, `/matter-batch` §1–6, `serve_to_stage.py`. **Not exercised:** `/matter-generate` §6a (`$MATTER_TEST_COMPOSITION` unset), `/matter-batch` §7 (no review given), `/discovery`, `/plan`, `/execute`. |
| **Date** | Run 2026-10-04 → 05; deposited 2026-10-14 (the session sat idle in between) |

---

## Items, ranked

### 1 — Nothing says how a draft reaches a consumer on another machine, and two consumer copies lagged the tree for days `[doc-gap]`

**Grounding.** The lead's ask was *"added to the library for a building test and pushed back so they can be used in blender on another system"*. `/matter-generate` ends at an uncommitted draft (its hard rule: *never commit, never push*), and no skill names the rest. I found the steps one at a time:
- **The Blender library was 27 articles behind.** `blender/asset_library/MatterLibrary.blend` held 57 articles; the tree held 84. None of Phase11's 26 drafts could be picked in Blender until `tools/conformance/check_asset_library.sh blender/asset_library` regenerated it.
- **Then a check of my own:** every image path in the rebuilt `.blend` relative (F-P10-17's concern). Nothing in the gate says to look.
- **Then the push:** 58 LFS objects, 64 MB.
- **On the other machine:** `git lfs pull`, and the Asset Library path with *Append (Reuse Data)*. Only the Readme says so.
- **Stage's catalog was 7 days stale.** This machine's dev install listed 36 articles; the tree had 89. `/matter-batch` hands nothing to Stage (it replaces §6a), so seven batches went by without a re-serve.

**Proposed fix.** One short section, *"When the lead wants it usable elsewhere"*, in `/matter-generate` (and pointed at from `/matter-batch`'s hand back):
1. Commit the paths.
2. Run `check_asset_library.sh blender/asset_library`, and confirm no absolute image path.
3. Re-serve Stage (`serve_to_stage.py --no-restart` updates the catalog only).
4. Push on the lead's word.
5. Hand back the other machine's two steps.

**Where it'd live.** `.claude/skills/matter-generate/SKILL.md` §7 · `.claude/skills/matter-batch/SKILL.md` hand back · and it is a data point for the backlog's **Open 5** (who regenerates the `.blend`, and when): here, the session that built the articles, twice, on the lead's ask.

---

### 2 — A wish-list row built by `/matter-generate` outside a batch has no honest state `[doc-gap]`

**Grounding.** I built four `queued` rows (and later a fifth) with `/matter-generate` and rigged them at defaults only. `built` means swept and refined (RD-P11-4), so marking them `built` would have claimed a sweep that had not run. Leaving them `queued` + `build` would have had `/matter-batch next` build over a stem that exists. I improvised `kind: rejudge, state: queued` plus a dated note naming the run. It worked: the lead's next ask was *"run the sweep on the five re-judge rows"*, and the batch took them as re-judges. But the move is mine, written nowhere.

**Proposed fix.** In `/matter-generate` §1, beside the wish-list sentence: *"A row you build here becomes `kind: rejudge`, `state: queued`, with a note naming this run, so a batch sweeps it rather than rebuilding it."* Or a `drafted` state in `wishlist.py`, if the refiner prefers a word to a convention.

**Where it'd live.** `.claude/skills/matter-generate/SKILL.md` §1 · `tools/converters/wishlist.py` (states)

---

### 3 — `/matter-generate` §6's preview cannot judge scale, and it misled on a fine-scale article `[doc-gap]`

**Grounding.** `make_preview.py` lays one tile across the sphere. For `PowderCoat_Textured` (a 1 cm tile of 0.2 mm bumps) it drew stucco-sized lumps, a look the material never has at real size. What settled it was the rig at defaults: `uv run tools/parity/rig.py <stem>`, about 30 seconds per article with no sweep. It draws at real size with a ruler, and in Blender and Unreal too. It also showed the white LED's Unreal difference a day before the sweep did.

**Proposed fix.** §6, one line: *"The preview lays ONE tile across the sphere: it judges colour and gloss, never scale. For scale, and to see Blender and Unreal, run `rig.py <stem>` (defaults only, under a minute)."*

**Where it'd live.** `.claude/skills/matter-generate/SKILL.md` §6

---

### 4 — I wrote a rig-scene size from memory, and it was wrong `[self-error-doc-could-prevent]`

**Grounding.** In the batch summary I wrote *"the rig's floor is 2 m"*, to say a 3 m floor tile's repeat cannot be judged there. `tools/parity/scene/build_scene.py` says `FLOOR = 1.0` (1 m × 1 m). I caught it only because I checked the claim before committing. The number carried a real judgement: whether the rig can show a floor's repeat at all.

**Proposed fix.** `/matter-batch` §3 names the scene once: *"the floor is 1 m square, the sphere 0.18 m in radius, the cube 0.30 m, the ruler 10 cm in 1 cm cells, the close-up about 0.5 m from the cube. A repeat larger than about 1 m cannot be judged here."*

**Where it'd live.** `.claude/skills/matter-batch/SKILL.md` §3

---

### 5 — *"A batch touches no planning doc"* left two lines saying the batch was still owed `[doc-gap]`

**Grounding.** Two lines named this batch's rows as owed: ledger row M5 (*"Open: the slider sweep"*) and the ask doc's footer (*"the slider sweep is not run"*). Both were written in this run, before the batch. The rule kept me off them, so I named both in the handback and the lead had to ask for them as a separate step (`89e4fc8`, a two-line change). The backlog already absorbed the same shape for a quick fix leaving a research footer stale. This is the batch's version.

**Proposed fix.** `/matter-batch` hand back: *"grep `docs/Planning` for the batch's stems; a line that names one as owed is listed in the hand back as a one-line offer."* That keeps the rule and saves the lead the question.

**Where it'd live.** `.claude/skills/matter-batch/SKILL.md` §Hand back

---

### 6 — Both skills say *"Never push"* outright, and the lead asked to push at five steps `[doc-gap]`

**Grounding.** `/matter-generate` (*never commit, never push*) and `/matter-batch` (*never push*) say it without a condition. In this run the lead asked for a push after every unit of work. Each time I had to reason that a direct ask overrides a skill's hard rule, and say so in the commit message. The project's actual rule is narrower: a push is lead-gated (`LOCAL_DELTAS` §Weighting).

**Proposed fix.** *"Never push unasked; on the lead's word, push by `.claude/CLAUDE.md` §Git's push row."* The same for *never commit* in `/matter-generate`.

**Where it'd live.** `.claude/skills/matter-generate/SKILL.md` and `.claude/skills/matter-batch/SKILL.md`, the hard-rule lines

---

## Keep these

- **The merge row for a diverged trunk** — the pull met 56 unpushed local commits and one remote one. A merge kept the SHAs that `Phase11_LibraryCoverage.md` cites; a rebase would have broken them.
- **`git diff --cached --stat` before, `git show --stat <sha>` after** — every one of 17 commits read back as intended. It also made amending my own unpushed commit safe (a wrong catalog count in its message): I checked `rev-parse HEAD` and an empty index first.
- **`/matter-batch`'s "one row at a time, through its commit"** — five clean list-only commits while the next rig ran. Nothing of one row rode into another's.
- **"Never fudge a recipe to make the tools agree"** — the LED's Unreal gap was measured on all three emitters (0.75, 1.00, 1.12 of Storm and Blender) and reported, not tuned away.
- **`research.md`'s "reconcile the footer"** — Pass 2, M5 and the sweep each left the ask doc's Status saying what was true then. The earlier wording stayed as dated notes.
- **Generate to `/tmp` and look first** (`/matter-generate` §2b) — the concrete's first pass showed its repeat plainly in a 2×2 tiling, and the second pass fixed it before anything landed.

## Dead weight

None.

## Open questions

1. **Lead:** keep or redo on batch `261004-1`'s five rows. Nothing was reviewed in this session, and Phase12 has since changed `LED_CoolWhite` (light colour and brightness are ports now).
2. **Lead:** SM-Q5, what a Set records as its release while it uses drafts. Open since Pass 2; the platform's Pass 3 says it still records `matterlib-0.1.0`.
3. **Product, not methodology:** why Unreal draws a white emitter at 0.75 of Storm and Blender, a warm one at 1.12 and Neon at 1.00 (batch `261004-1`). Not run to ground. Whether it survives Phase12's emission ports is unchecked.
4. **Open, owned by nobody yet:** the platform's A8, a gate form for a Set root that assembles part files (ask doc, Pass 3). It arrived after this run's last act.
