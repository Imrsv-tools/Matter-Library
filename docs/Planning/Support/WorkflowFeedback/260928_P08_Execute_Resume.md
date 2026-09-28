# Workflow Feedback — P08 / execute / resume run 2 → suspend-handoff

| | |
|---|---|
| **Verb** | `/execute P8` |
| **Unit** | P08 (Character Appearance for Studio) |
| **Mode** | resume run 2 (from the first hand-off's Resume block) → suspend-handoff (the lead: *"yes push and we will handoff"*) |
| **Outcome** | suspended at a step boundary. 8.1 (the Hair rework), 8.2 (per-tone lips and nails) and 8.3 (rubber soles, natural leather, light-wash denim, the rig's sole split) all passed their sittings and were pushed. 8.4 and the close remain; Resume block written. |
| **Shape** | behavior-touching (assembler, validator, Blender master, rig, the character build, 18 articles, specs) |
| **Confidence** | Ran fully: BUILD → TRY → STRENGTHEN over three steps and four sittings; three lead-authorised pushes. **Not exercised:** the close, `execute_repair.md`, the high-rigor lane. |
| **Date** | 2026-09-28 |

This is **not** a continuation of `260928_P08_ResearchDiscoveryExecute_ColdStart.md`. It is the next session on the same unit, from that run's Resume block. `_RefinementBacklog.md` was read first: item 1 below is a recurrence of a **held** item, not a new one.

---

## Items, ranked

### 1 — Recurrence, and costly: unlabelled multi-file output produced a false learning, a spec note and a withdrawn field `[self-error-doc-could-prevent]`

**Grounding.** I was bisecting a Storm-vs-Blender gap on `Hair_Natural` with one variable per `/tmp` variant, and read two scorecards with `grep -h '^| defaults' <sw1> <ss0>`. I paired the rows with the files by the order I had typed them, and got it backwards. On that misreading I:
- blamed `specular_weight`;
- withdrew the field from the assembler and the recipe schema;
- wrote **Learnings Blender B10** ("Principled's Specular IOR Level is not OpenPBR's `specular_weight`");
- added a note to `LCDSchema.md` citing B10.

All of it was uncommitted, then caught by `execute.md` §BUILD's *"look at the output before reading the number"*: a picture grid showed the agreeing pair was the other row. `grep -H` reversed the finding (the translucency, not `specular_weight`). I retracted B10 and the note before anything landed. It happened a second time the same way (the nail bisect), and I used `-H` from then on.

This is exactly the backlog's **held CLAUDE.md patch item 5** (*"output from several files without per-line names (`grep -h`, stacked `head`) pairs with its inputs only by the order you assumed — label it (`grep -H`)"*). It is held waiting on the lead, so no agent can read it yet, and it bit a run the same day.

**Proposed fix.** Apply held patch item 5. The run is evidence for its priority: the cost was not a wrong number but a false *durable learning*, nearly committed to a public repo.

**Where it'd live.** `.claude/CLAUDE.md` §Git (the held patch); recurrence count in `_RefinementBacklog.md`.

---

### 2 — I asked the lead to approve a sitting whose fixture could not show the thing, having called the defect "cosmetic" `[self-error-doc-could-prevent]`

**Grounding.** 8.3's click 5 judges *rubber soles distinct from leather uppers*.
- My sole split (a 1.5 cm height band) visibly stair-stepped on the rig sheet. I wrote it off in the handback as *"the rig's own fixture, not the material; I can smooth it if it bothers you"*, and asked *"Does click 5 pass?"*.
- The lead asked to see it in Blender, then: *"I am not quite sure what I am approving...."* with a screenshot. The near shoe had **no rubber at all**: the band had missed its whole sole slab and heel.
- A ring probe showed the shoe is loop-modelled (the underside island plus 4 loops of 44 faces). A `grow: 4` rule fixed it in one step, and the lead passed it at once: *"OH Yeah.. that looks great pass"*.

`execute.md` §TRY already says *"ask whether the surface's SCALE … can show the thing the click is about"*. I asked it about scale and not about my own fixture's defect, which sat **on** the property being judged.

**Proposed fix.** A line in `execute.md` §TRY: *"A fixture defect ON the property the click judges is not cosmetic, and naming it in the handback does not discharge it: fix it, or do not ask for the click. Test: could the lead approve or reject this click from what the surface shows?"*

**Where it'd live.** `execute.md` §TRY.

---

### 3 — The Brief named picture sheets as the sitting surface; LOCAL_DELTAS names a running viewer; the lead chose the viewer `[doc-gap]`

**Grounding.**
- Phase08's Brief (discovery's output) says the lead *"judges the rig's picture sheets"*. So for clicks 4 and 5 I composed comparison PNGs and opened them with `xdg-open`.
- `LOCAL_DELTAS.md` (*"the artifact a person reaches"*) names USDLiveView (served via `serve_to_stage.py`) or the installed Blender library for a draft article, and says *"a picture pasted in chat is not the sitting"*.
- For click 5 the lead asked *"can you open this in blender?"*, and found the defect (item 2) in one look. The same happened at 8.1: the only sitting where he found a problem himself was the live Blender one.

The Brief quietly overrode the delta, and I followed the Brief.

**Proposed fix.** In `discovery.md` §The Brief (first human test): *"Name the surface from LOCAL_DELTAS' 'artifact a person reaches' row. A rig sheet is supporting evidence beside it, not the sitting."* In `LOCAL_DELTAS.md`: the character in Blender is a sanctioned sitting surface for anything worn on the body.

**Where it'd live.** `discovery.md` §The Brief; `LOCAL_DELTAS.md` (the artifact row).

---

### 4 — Opening a scene in the lead's LIVE Blender has traps no doc names; two bit this run `[doc-gap]`

**Grounding.**
- **(a)** The rig's Blender driver's `setup_scene` begins with `bpy.ops.wm.read_factory_settings`. In the lead's GUI session that resets his preferences in memory (the MCP add-on, the Matter library path), and Blender can save them on exit. I noticed before running it and wrote a launcher without it.
- **(b)** Re-running my launcher in his session bound materials by exact object name. A re-import names objects `<part>.001`, so the articles went onto stray objects left from an earlier run, and the visible parts kept the USD importer's empty material (0 nodes, Learnings B6). The whole character rendered **black**, found by screenshot.
- **(c)** I also refreshed his scene while my own background rig run was rewriting the setting scene it reads, and imported stale UVs.

Recorded for the next run in Phase08's Resume block. No doc says how to drive the lead's live tool.

**Proposed fix.** A Blender learning: *"In the lead's live session: never `read_factory_settings`; build into a new scene; bind to THAT scene's objects by base name; delete the previous scene's objects; do not refresh from a file a background process is still writing; confirm by screenshot, never by a 'status ok'."* Or a committed `tools/parity/open_character.py` so the launcher is not re-authored in `/tmp` each run (that one would be a phase decision).

**Where it'd live.** `docs/Learnings/Blender/` (an entry); possibly a tool (a product decision, see Open questions).

---

### 5 — The churn check turned up the lead's ruling that dissolved my YOUR CALL `[keep — grounding for an existing rule]`

**Grounding.** At a suspend I was about to ask the lead to set a parity bar for Hair (Storm vs Blender 2.8, where it was 0.7). `git log` after my commit showed a sibling's `7df7222`: the lead's restated LCD ruling (*"picture ΔE between tools is a diagnostic, not a bar; judge the nod"*). §Divergence's *"same class as the lead ruled → apply autonomously"* then removed the question, and I told the lead in one line.

**Proposed fix.** None. This is evidence that `execute.md`'s *"at every suspend also run `git log`"* earns its keep. Listed under Keep.

**Where it'd live.** n/a.

---

## Keep these

- **Bisect one variable at a time, and look at the pictures before the numbers** (`execute.md` §BUILD, §Verify: *"a comparison whose sides cannot differ"*, *"look at the output before reading the number"*). Together they:
  - found the nail's coat (7.9 → 2.8, radius irrelevant);
  - placed the hair gap in the translucency lobe;
  - caught item 1's misreading before it landed.
- **Prove a refactor didn't move shipped output.** `gen_fabrics.py`'s `twill()` was parameterised, and all three `Denim_Twill` maps re-hashed byte-identical.
- **Confirm an ad-hoc check can fail** (§Verify). The validator's new Hair branch was run on the old article and failed all four rules. A sed-built variant was grep-checked before each render (one ambiguous count was re-checked directly).
- **Push discipline.** Before every push: list `origin/main..main`, name the sibling commits it would carry, scan the outgoing diff for private-shaped strings with a positive control, then `merge-base --is-ancestor` after. Three pushes, one of which carried four sibling commits, named to the lead.
- **`git show --stat` read-back after every commit.** It caught a schema edit that had silently joined two lines, and a learnings file left one newline short (restored to HEAD).
- **The act is the unit; the lead drives each one.** Four sittings in ~1 h 50 min, each finding or passing something real, with no step drained ahead of its sitting.

## Dead weight

None.

## Open questions

1. **Product, for a phase:** a committed `tools/parity/open_character.py` (open the rig's character with a cast in the lead's live Blender), rather than a `/tmp` launcher per run? Item 4's traps would then live in code. A lead decision.
2. **Owed quick-fixes, found and left alone (not this verb's errand):**
   - `docs/specs/Ontology/Taxonomy.md` line ~53 still says *"today 4 Domains and 9 Classes are populated"*. It has been stale since the `biological` classes, and `synthetic/polymer` landed this run.
   - `tools/conformance/codec_ab.py`'s `TIGHT_CLASSES` comment still reads *"Hair = Masked's graph"*. I left it because editing `tools/conformance/` requires a `check_exporter.sh` baseline, and that script is red for its environment (the first P08 retro, open question 3).
3. **The rig's Hair bar:** `GRADED` still includes Hair, with a 2.0 bar that `Hair_Natural` now exceeds (2.77 close-up). The sibling's `7df7222` records *"make 'Moved' the criterion"* as a Todo on the rig, so it is not mine to change. The rig's scorecard will print OVER for Hair until that Todo lands.
