# Workflow Feedback — P15 (now Phase18, Scale Grids) / discovery / cold start

| | |
|---|---|
| **Verb** | `discovery` |
| **Unit** | `P15`, Scale Grids. **Renumbered Phase18 the same evening** by the lead (RD-DS-6, `d71a30d`, another session), after this run's Brief landed |
| **Mode** | `cold start` (the numbering act, `"/discovery P15"`, then Pass 1 in the same response) |
| **Outcome** | `done`. Numbering commit `42ea165`; Brief `1827021` (lane build, no question with the lead); retro step 0 added a re-verify note after the renumber (`3cb1952`) |
| **Shape** | `doc-only` (plus measurements: the 95 articles, the lead's Blender preferences read without saving, three gate baselines, one throwaway probe in a scratch folder) |
| **Confidence** | Ran fully: `discovery`, numbering through the Brief. **Not exercised:** `/execute`, and the first human test (nothing built). Item 3's proposal for execute's cold start is inferential. |
| **Date** | `2026-10-14` |

---

## Items, ranked

### 1 — Renumbering a phase after it has minted ids leaves two phases owning one id scope `[doc-gap]`

**Grounding.** This discovery minted `F-P15-1` to `F-P15-8` as Phase15. A few hours later the lead put three new phases ahead of it (*"Lets make these the next phases (Before the scaled grid)"*). The renumbering commit `d71a30d` moved the doc to `Phase18_ScaleGrids.md` and kept the ids "as minted". A new **Phase15** (*Matter, Character and HDRI*) now exists. It has minted no `P15` id yet (grep, 2026-10-14), but its first finding will be `F-P15-1`, and the repo will then hold two. That is exactly what NamingConventions §Planning ids exists to prevent: *"a bare `F12` cited outside its phase collides"*. Nothing says whether ids follow the doc or the number, so the renumbering run chose and recorded its choice. The rule is silent, not violated.

**Proposed fix.** In NamingConventions §Planning ids (or Workflow §Phase Numbering): *"An id's scope is the phase number. When a phase that has minted ids is renumbered, the renumbering commit re-scopes them (`F-P15-n` → `F-P18-n`) by a scripted, anchored, count-checked substitution in every doc that carries them, and writes the old → new map once in the doc's Status line. Commit messages keep the old ids; the map resolves them."* The alternative, ids frozen as minted, needs a rule that the number's new holder starts its series past the old one, and nobody would remember to apply it.

**Owed now, either way** (Phase18's doc; no verb is live on it as of this deposit): `F-P15-1…8` in `docs/Planning/Phases/Phase18_ScaleGrids.md`, about 20 sites, plus `D-1…D-8` (item 2). Whoever rules item 1 applies it.

**Where it'd live.** `NamingConventions.md` §Planning ids (the method's, carried from upstream), so it is likely portable: upstream.

---

### 2 — I minted `D-1` … `D-8` for agent-closed decisions, outside the id grammar `[self-error-doc-could-prevent]`

**Grounding.** discovery.md's *Decisions that bind* bullet says *"Ids you mint are `Q-P<NN>-n` · `F-P<NN>-n` · `RD-P<NN>-n`"*, and NamingConventions says an agent's closed call is an `RD` *"which says whose call it is on its line"*. I read both and still wrote `D-1…D-8` under a heading that said *Closed at this discovery*. The heading *Decisions that bind* pulled toward "D". `D1` is also already a Glossary term (*matter only, never assemblies*), so `D-1` collides by eye. I did not rename them in step 0: the scope (`P15` or `P18`) is item 1's open question, and renaming now would fix one of two choices before it is ruled.

**Proposed fix.** In discovery.md's Decisions bullet, one clause: *"a call you close yourself is `RD-P<NN>-n` with "agent's call" on its line, never a bare `D-n`."* The owed rename is in item 1.

**Where it'd live.** `discovery.md` §The Brief, the *Decisions that bind* bullet.

---

### 3 — A ready Brief re-sequenced behind other phases has no re-verify trigger, and its `▶` goes stale within the hour `[doc-gap]`

**Grounding.** The Brief was committed at 17:09. It holds dated counts (95 articles, 46 at `s001`), three gate baselines, and a note that Phase14 was executing at the same time. Its handback said `▶ /execute Phase15`. By 19:11 the lead had numbered three phases ahead of it. One of them, **Phase17, *Character Materials, Their Own Library*** (RD-DS-4), may take skin out of Matter. Two of the Brief's five clicks rest on skin being a Matter article with a tile size: the planted 170× raw-atlas skin, and the character in the rig. The renumbering commit carried the status line and pointers faithfully, but named none of this. Nothing in discovery.md or execute.md says a Brief that waits behind other phases must be re-verified, or names which of its claims are perishable. I found it only because retro step 0 made me re-read what had changed on disk. The fix is the dated re-verify block in `3cb1952`.

**Proposed fix.** Two clauses:
- **Workflow §Phase Numbering, re-sequencing:** *"Putting phases ahead of one whose Brief is written: name, in a dated line under its Status, each phase now ahead that could change its fixtures or clicks."*
- **`execute.md` cold start:** *"If any phase closed after the Brief was written, re-measure the Brief's dated counts and baselines before step 1, and re-read the Outcome of each phase that landed in between."*

**Where it'd live.** `Methodology/AgenticEngineering_Workflow.md` §Phase Numbering and `execute.md` §Cold start. Portable.

---

### 4 — Discovery "does not build", yet the four-tests rule asks it to probe a premise; where the throwaway probe lives is unsaid `[doc-gap]` *(low)*

**Grounding.** RD-SP-4 (four line levels, the background in the grid's own colour) rests on how the grid looks. *"A ruling closes its axis, not an untested premise beneath it … probe that on the real fixture"* sent me to draw one grid at 4,096 px and reduce it to screen sizes. The probe found the finest level swamping the background (F-P15-8). I put the script and pictures in a scratch folder outside the repo and recorded the method as the finding, guessing that this squares with *"it does not build"*.

**Proposed fix.** One clause in discovery.md's HARD RULE: *"A premise probe is not a build: throwaway, outside the repo, recorded as a finding with its method; nothing from it is committed."*

**Where it'd live.** `discovery.md` §HARD RULE.

---

## Keep these

- **"A ruling closes its axis, not an untested premise beneath it."** It produced the one finding that changes how the grids are drawn (F-P15-8 → the finest level dim), which would otherwise have surfaced as a sitting surprise.
- **The risk lane's "read the control; a control that cannot start is absent coverage".** Running the three baselines in discovery found that `check_conformance.sh` resolves against the working tree, not the pinned release. That made step 15.4 deliverable with no release, and it confirmed the exporter baseline 15.2 needs.
- **"Probe the entry path from the account side."** Reading the lead's Blender preferences, read-only, showed the Matter add-on is not enabled and the library is registered as Append (F-P15-4). Without it, click 2 would have failed at TRY.
- **Numbering: the head of `## Future`, after a search for newer rulings, with the doc moved out of `Future/` in the numbering commit.** It took P15 correctly at the time and left one clean commit.
- **Pathspec commit plus the `git show --stat` read-back.** During the numbering commit a sibling's staged rename sat in the shared index; the pathspec kept it out, and the read-back confirmed 9/9.
- **The five labelled handback beats.**

## Dead weight

None.

## Open questions

1. **Do minted ids follow a renumbered phase, or stay as minted?** (item 1). A Refiner call, possibly the lead's; the owed rename in Phase18's doc waits on it.
2. **Product, not method, recorded in Phase18's doc (`3cb1952`):** whether clicks 2 and 4 survive Phase17's ruling on character materials. Owed to Phase18's `/execute`, not to the Refiner.
