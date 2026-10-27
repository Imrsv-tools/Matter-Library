# Workflow Feedback — CharSkins / research → quick-fix (lead-directed) / cold start

| | |
|---|---|
| **Verb** | `research`, with lead-directed graduations to `quick-fix` (six) and a machine set-up the lead asked for |
| **Unit** | `CharSkins` — research `261026_R_SyntheticSkinAndEyes` (Passes 4–6), `261026_R_CharacterTestBenchInputs` (Pass 2), `261027_R_CharacterMaterials` (new, CMT) |
| **Mode** | cold start; one long session over two days (2026-10-26 → 27) |
| **Outcome** | done. The synthetic test set rendered and judged over three rounds; the 3D-authoring rule in `SkinMaps.md`; the character-materials plan with RD-CMT-1 … 4; Roadmap and ledger (P33); the machine with Unreal set up to render all three tools (official Blender via `MATTER_BLENDER`); the gate 18/18 here; four Learnings. Pushed to `71ca1d6`; `2ddf888` and this retro are local. |
| **Shape** | behavior-touching (two conformance scripts, a skin maker, an eye maker) + doc |
| **Confidence** | Ran fully: research, quick-fix, the rig, the makers, the gate, both conformance scripts, a push. **Not exercised:** the library machine (nothing re-checked there); Studio itself (the lead's looks were reported, not watched). |
| **Date** | 2026-10-27 |

---

## Items, ranked

### 1 — Nothing tells a session to close what it opened on a shared machine, or to leave a note of it `[doc-gap]`

**Grounding.** `serve_to_stage.py` restarts the Stage daemon by default. This session ran it three times (2026-10-26 and 27) and left the daemon running. A platform session in the IMRSV repo then found it, judged it *"belongs to a separate Claude session (ML_R_CharSkins) so I'll leave it alone"*, and had to reason its way around it before its own Unreal build. The lead stepped in twice: *"you need to close stage when you are done (if you open it) another session is also working here"*, then *"It is getting crowded now so we shoudl start adding notes to keep our work clean,,, when done, close stage, same with the app or other things not needed so other sessions taht might be needing to jump in can"*. `LOCAL_DELTAS.md` names Stage only as *"the artifact a person reaches"*, and its live-state home is *"None: there is no live infrastructure"*, so no verb says to stop the daemon afterwards. (The `pkill -f` ban in `.claude/CLAUDE.md` §Git covers how to stop a process, not when.) The rule is now in this session's memory only.

**Proposed fix.** One rule: *"On a shared machine, close what you opened when the work is done — the Stage daemon (`serve_to_stage.py` restarts it), Studio, a viewer, a Blender GUI, a background task — by PID, and only if the lead is not using it. Say in the handback what you opened and closed, and note anything shared you changed (a served catalog, a restarted daemon, a machine setting) in the commit or the doc's footer."* Optionally, `serve_to_stage.py` prints its daemon's PID and the stop command.

**Where it'd live.** Upstream (portable: any project whose sessions share a machine); `LOCAL_DELTAS.md` for the Stage specifics (the "artifact a person reaches" row, and the live-state row, which could become "the running daemons, noted in the handback").

---

### 2 — The push-by-SHA shape in `.claude/CLAUDE.md` breaks in zsh when the SHA is a variable `[doc-gap]`

**Grounding.** Following §Git's push row (*"push your tip by value: `git push origin <sha>:refs/heads/main`"*) with `S=$(git rev-parse HEAD); git push origin $S:refs/heads/main` pushed nothing. zsh read `$S:r` as the `:r` (root) modifier, so the refspec became `<sha>efs/heads/main` (`src refspec … does not match any`). It was caught by the exit code, and `"${S}:refs/heads/main"` worked. Recorded as Learnings CC3.

**Proposed fix.** In the §Git table's `git push` row, write the variable form braced: `git push origin "${SHA}:refs/heads/main"`, with *"(zsh: a bare `$SHA:r…` is a modifier)"*.

**Where it'd live.** `.claude/CLAUDE.md` §Git (the refiner's lane); upstream if the row is carried there.

---

### 3 — `LOCAL_DELTAS.md` §Two machines was edited twice by this run, lead-directed; the table may want a rethink `[doc-gap]`

**Grounding.** The lead: *"you are on the machine with UE - so any adjustments can be made direclty.. if something is missing.. let's set that up now too"*, then *"delete the stale staging folder"*. Two cells became false, and were struck with their dates, citing the lead's words (`3789158`, `71ca1d6`):
- "cannot render Blender parity": now renders all three columns;
- "`run_all.py` … 2 FAIL": now 18/18.

**The table's premise is now thin.** The machine with Unreal does everything the library machine does: Blender parity, thumbnails, conformance, the masters and the runtime. What still differs is mostly history: the tracked `MatterLibrary.blend` has only been regenerated there, and the lead's Blender sittings happen there.

**Proposed fix.** The refiner re-reads the two struck cells for wording, and decides whether §Two machines should say *"either machine runs every lane; the machine with Unreal also builds and publishes the runtime"* instead of a can / cannot grid.

**Where it'd live.** `LOCAL_DELTAS.md` §Two machines.

---

### 4 — A maker that re-writes unchanged pictures makes LFS churn; nothing checks for it `[doc-gap]`

**Grounding.** Round 2 re-ran `gen_synth_skin.py` to change the freckles only. Nine maps whose **pixels were identical** were re-encoded with different bytes; `git status` showed them modified, and `git diff` showed new LFS pointers. This run compared the pixels against `HEAD` by hand and restored the nine (Learnings G2). A batch run would have committed nine "changed" textures with nothing changed.

**Proposed fix.** The fit makers (`gen_skin_maps.py`, `gen_synth_skin.py`, `gen_synth_eyes.py`) leave a file untouched when its decoded pixels equal what is on disk. Or `quick-fix.md` / `/matter-batch` §commit adds: *"after a regenerate, `git diff --stat` the textures; a picture you did not mean to change gets a pixel compare against `HEAD` before it is staged."*

**Where it'd live.** A tool change (a `/quick-fix` on the makers), or `/matter-batch` §5; Learnings G2 already holds the fact.

---

### 5 — A stray `cd` in a Bash call moved the session's directory `[self-error-doc-could-prevent]`

**Grounding.** A rig probe was written as `cd /tmp >/dev/null 2>&1; timeout 600 uv run --directory <repo> …`. The `cd` was reflex, not needed, and the harness reported the working directory changed to `/tmp`. It was caught on the next call and moved back; nothing ran in the wrong place, since every path was absolute.

**Proposed fix.** None to the doc: the rule is stated (`.claude/CLAUDE.md` §Codebase search, *"never `cd`"*) and it held after the slip. Filed for the tally only.

**Where it'd live.** n/a (a tally entry).

---

## Keep these

- **Read a sibling's docs at its origin, never pull** (`research.md` §Seeds decay; `LOCAL_DELTAS.md` §Separation). The OMF clone here was 1,062 commits behind and the platform docs 43 ahead with a live edit; reading at `origin/main` gave current rulings with no risk to either tree.
- **Measure a heavy step before pricing it** (`research.md` §Disposable probes). One 13-second smoke render showed that all 25 drafts were about 7 minutes, not 40; the lead was never asked to approve a cost that wasn't real.
- **Count-asserting scripted edits** (§Editing: replace an anchor only when it occurs exactly once). About fifteen batch edits across docs, recipes and maps; zero silent no-ops, and the one quoting error failed loudly before writing.
- **`git show --stat` after every commit, `git diff --cached --stat` before.** It confirmed the file and line counts on all eleven commits; one would have caught round 2's nine byte-churned maps if they had slipped through.
- **Cite private sources by role and date** (the Asset Workshop's research pattern, adopted for CMT), then grep the doc for private ids before committing. It caught one private SHA in the bench pass.
- **The batch row's Verdict / Review lines for an ad-hoc test set.** The lead's words landed verbatim per article, round by round, and two later rounds updated the same rows.

## Dead weight

None.

## Open questions

1. **Number Phase22 … 26 now, or as each starts?** (lead) Recorded as `261027_R_CharacterMaterials.md` F-CMT-9; the next step there is `/discovery Phase22 Skin Maps Beyond Colour`.
2. **Should §Two machines become "either machine runs every lane"?** (refiner, with the lead) Item 3.
3. **Is the character's Storm-vs-Blender ΔE of 3.3–3.9 on a synthetic skin normal?** It was the first Blender column measured on this machine (Storm vs Unreal is 2.3). The library machine's number for the same article would say. (unresolved; agent)
