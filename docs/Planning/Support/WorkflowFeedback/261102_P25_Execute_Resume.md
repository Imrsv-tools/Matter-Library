# Workflow Feedback — P25 / execute / resume

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P25` |
| **Mode** | `resume run 2` (session `ML_P25_E2`, from `ML_P25_E1`'s hand-off by message) |
| **Outcome** | `suspended` — 25.1.19 (the inner-corner line, the lead: yes), 25.2 built and click 2 sat (D's lips restored on the lead's word), the lead's re-ruling that AI-generated skins ship; 25.3 handed to `ML_P25_E3` |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: execute's Build → Try → Strengthen, three sittings, the always-on gate, the remake-identical proofs. **Not exercised:** the close, a push, a publish, a Stage re-serve. |
| **Date** | `2026-11-02` |

*A distinct run from `261102_P25_Execute_ColdStart.md` (`ML_P25_E1`), not a continuation of it.*

---

## Items, ranked

### 1 — A standing rule that the phase's own Outcome contradicts reached the lead as a shipping-time blocker, and the lead called it ridiculous `[doc-gap]`

**Grounding.** Phase25 is *AI Skin Structure*; its Outcome says that if D wins, *"the maker turns it into a calibrated skin structure"*. `SkinMaps.md` §Sources still said *"A fully AI-made map is not accepted. **Ruled** (RD-SKM-5)"*, reinforced by RD-SYN-1. The Brief handled the conflict by scheduling it: *"`SkinMaps.md` §Sources … only by the lead's re-ruling at 25.3"*. So after three sittings, I put it to the lead in `Blockers` as the gate to 25.3. The lead: *"What is this ridiculous RULE?! we are literally building complete AIGenerated skins right now... that is what we are doing."* The lead had in effect overruled the rule by opening the phase (split and seeded on their word, run through three discovery passes). Nobody asked them to strike it then, so the question arrived as a surprise at the end. The spec line and both research rulings were superseded the same turn (`0efb427`).

**Proposed fix.** In discovery: *"If the phase's Outcome is something a standing ruling forbids, put that ruling to the lead for a re-ruling **before BRIEF READY**, in the lead's words, and land it upstream then. A Brief must not schedule a re-ruling of its own premise for a later step: the lead hears it as the method doubting a decision they already made by opening the phase."*

**Where it'd live.** `discovery.md` (the Brief's carried-rulings check) — portable.

---

### 2 — The click on an infrastructure step did not say what the step buys, so the lead read it as another look tweak `[self-error-doc-could-prevent]`

**Grounding.** Click 2 (25.2, D as a structure) asked: *"is D as a structure still the skin you picked at click 1 … or has it lost something you want back?"* The lead answered, then asked: *"What do we get from strcture? what do you keep trying to improve?"* After two look-tuning clicks, a third showing of the same face read as more tuning. 25.2 is a conversion whose payoff the lead never sees in the picture: shippability, and the later tone and marks work. `execute.md` §TRY says *"Say in one sentence what to compare and what *right* looks like"*. Nothing says to state what the step is FOR when a step's success is "nothing visible changed".

**Proposed fix.** In §TRY, after that sentence: *"When the step's success is that the picture does NOT change (a conversion, a refactor, a format move), open the ask with one line on what the step buys the lead, so the click reads as a check, not a proposal."*

**Where it'd live.** `execute.md` §TRY — portable.

---

### 3 — A tool that imports the maker must set its size first; the symptom is one printed line `[self-error-doc-could-prevent]`

**Grounding.** The new `project_face.py structure` imported `gen_skin_maps` without setting `MATTER_SKIN_N`. The maker read its size at import as 2048, so the ear gradient was painted onto an 8K atlas through 2048 indices. The only sign was a printed `head fields at 2048: 1086953 texels`; the run exited 0 and wrote a wrong picture. `paint_uv.py put` sets the variable first (its line 479), and I did not read that guard before copying `put`'s call. This is the Verify table's *"Editing an EXISTING function → read its call site and its guard"*, applied to a call I copied rather than edited.

**Proposed fix.** A Learnings entry under a skin or tooling domain: *"`gen_skin_maps` / `gen_synth_skin` read the map size from `MATTER_SKIN_N` at import. A tool working at a subject's size sets it before the first import (`os.environ.setdefault(\"MATTER_SKIN_N\", \"8192\")`, as `put` and `brow_cards` do). Tell: the head fields print \"at 2048\"."* Optionally the Verify row could read *"editing — or copying a call to — an existing function"*.

**Where it'd live.** `docs/Learnings/` (project-specific); the Verify-row wording in `execute.md` is portable.

---

### 4 — Running the maker in place rewrites a committed provenance line every time `[doc-gap]`

**Grounding.** Both remake proofs (`--subject Tone34 --fields`, and the 18 skins) left the served maps byte-identical but changed `library/provenance/sources/fit/makehuman/skin.yaml`. The writer drops the duplicated `gen_skin_shine.py` that the committed `evidence:` line carries. I restored the file twice, since it isn't this phase's. Every "remake identical" proof on this tree therefore shows a dirty provenance file. The next agent will either restore it as I did, or commit a provenance change under a phase that doesn't own it.

**Proposed fix.** A `/quick-fix`: commit the de-duplicated `evidence:` line once, so a remake leaves the tree clean. Product work, not methodology.

**Where it'd live.** The backlog §product questions, or the lead's quick-fix list.

---

## Keep these

- **Pass 1's own rule for click 2** (*"if every region is within 1 ΔE … click 2 is not called"*) — it decided whether to show, with no question to the lead. When the measure came out over the line, the sitting found the one thing that mattered (the lips).
- **"A reading that disagrees with the picture indicts the instrument"** — the round trip said the face core was 1.5 ΔE, but the picture looked browner. A heat map located the difference in features (lips, brows, lids, nostrils) instead of the skin, before the lead saw it.
- **Measure a fix's premise before building it** — testing whether D's lips fit the skin model (they miss by 27 %) sent them through the lip layer instead of a pigment route that would have failed after a 15-minute chain.
- **The cross-session hand-off by message** from `ML_P25_E1`: the first item, the files and the look-view workaround arrived exactly; the run started on the defect in minutes.
- **`/retro` step 0's offer** — the next session was named by the namer and started before the deposit.

## Dead weight

None.

## Open questions

1. **Runtime owed after Phase26 (product, the lead's or the platform's).** Phase26 committed makeup inputs to every skin article, and the pinned `unreal-runtime-v7` refuses them. Every Phase25 look-view launch since has drawn the article as it was at `3d594fb` through a scratch driver. I did not check whether a dated *runtime owed* line for this exists in `PlatformDependencies.md`. Until a v8 is published, any phase judging a skin in the look view needs the same workaround.
2. **The reading recorded beside the AI ruling** (`SkinMaps.md`): *"a raw picture pasted in as the colour map is still not the route … because a painted map cannot change tone"*. It is marked as mine and strikable. It has not been put to the lead as a question.
