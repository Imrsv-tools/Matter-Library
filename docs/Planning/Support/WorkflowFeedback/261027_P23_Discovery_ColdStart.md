# Workflow Feedback — P23 / discovery / cold start

| | |
|---|---|
| **Verb** | `discovery` (seed, then Pass 1, in one session) |
| **Unit** | `P23` — Synthetic Skin Sets |
| **Mode** | `cold start` |
| **Outcome** | `done` — numbered and seeded (`4398f05`), then Pass 1 wrote the Brief (`4d8c23e`): lane build, three steps, no lead question open |
| **Shape** | `doc-only` (two scratch probes outside the tree) |
| **Confidence** | Ran fully: discovery's cold start, numbering, seed, Pass 1, the Brief, the lane check. **Not exercised:** `/execute`; item 3's premise test is still untested, since its click has not been sat. |
| **Date** | `2026-10-27` |

---

## Items, ranked

### 1 — A bare `/discovery <N>` on a research-only head entry hit seed-and-stop, and the lead had to send a second message to open Pass 1 `[doc-gap]`

**Grounding.** The lead typed `/discovery P23`. The head of `## Future` was *Synthetic Skin Sets*, status `RESEARCH`, with no phase doc. `discovery.md` §Cold start step 1: *"no phase doc → this invocation SEEDS and STOPS"*. Its exception is the lead *"opening it in the same breath: an invocation that both names a phase to seed **and** asks for discovery to start"*. Read literally, a bare `/discovery` cannot meet that exception, since otherwise it would swallow the rule. So the run seeded, committed and stopped with `▶ /discovery P23`. The lead's reply was *"yes. synth skin"*: they had meant to start discovery all along.

Every earlier `/discovery <N>` that numbered and opened in one go (Phase15, 20, 21, 22, per `git log`) had a seed doc already, so the rule never fired before. It fires exactly when the Roadmap entry is research-only, which is now the common case: four of the five character phases are `RESEARCH`.

**Proposed fix.** In §Cold start step 1, decide the bare case explicitly. *"`/discovery <N>` that numbers the head of `## Future` IS the deliberate opening: seed, commit the seed, and continue into Pass 1. Seed-and-stop applies when the entry is not the head, or the lead says 'seed'."* Or the reverse, if the stop is wanted. Either way, the lead should not have to discover which.

**Where it'd live.** `discovery.md` §Cold start step 1 (portable: upstream).

---

### 2 — The Brief claimed a new name shape was safe from a spec sentence; the code that parses names was found afterwards `[self-error-doc-could-prevent]`

**Grounding.** RD-P23-4 puts a skin's structure on the Material token (`Skin2_FitzpatrickIV_…`). The first draft of F-P23-3 said *"Taxonomy reads the part from the file, not the token"*, from Taxonomy's *"the group lives in the file"*. The run had grepped the validators and `groups.py` and found nothing keyed on the token.

Only a later grep for `split("_")[0]` across `tools/` found `tools/thumbnails/showcase.py` `character_family`. It looks up the Material token in `CHARACTER_FAMILIES` and **raises `SystemExit`** on an unknown family, so 23.3's thumbnails would have stopped on `Skin2`. The Brief was corrected before its commit. `discovery.md`'s risk-lane rule (*"whatever ENUMERATES that tree is a control"*) and backlog row 86 cover **adding files**. Neither covers **adding a new name shape** that existing code parses.

**Proposed fix.** Add one clause to the risk-lane bullet: *"A phase that introduces a new name SHAPE (a token never seen in that position) greps for code that PARSES names (`split("_")`, prefix lookups, family tables) before the Brief calls the shape safe. A spec sentence about where a field is read is not evidence about every reader."*

**Where it'd live.** `discovery.md` §The Brief, Risk lane; or this project's `LOCAL_DELTAS.md`, if names-as-keys is judged local.

---

### 3 — A premise that discovery cannot probe without a tool change was scheduled as click 1 with its branches decided; the doc has no shape for this `[doc-gap]`

**Grounding.** §Forking test 1: *"a ruling closes its axis, not an untested premise beneath it: … probe that on the real fixture before the Brief says no open decisions."* The phase's premise (F-SYN-1: colour at skin scale is the lever) was observed in Studio's light, on a skin with no shine maps. Phase22 has since changed the shine.

Probing it means rendering the Emily picture in the library's look view, which needs a reference column in `look.py`. That is a source edit, which discovery may not make. The run made it step 23.1 / click 1, with three branches decided in the Brief (proceed · stop and go to the lead · reopen RD-P21-5), and wrote *"Open for the lead: None"*. That reads as compliant, but the doc gives no sanction for it, and a reader could take it as the Brief claiming no open decisions over an untested premise.

**Proposed fix.** One sentence under test 1: *"If the probe needs a build discovery may not make, make it step 1's click, with every branch's consequence written into the Brief (proceed / stop / which ruling reopens). That is an open premise with a decided route, not an open decision."*

**Where it'd live.** `discovery.md` §Forking to the lead, test 1.

---

## Keep these

- **§Discovery discipline, *where rulings live*:** searching the closed and live phase docs before seeding found RD-P22-14. It made this phase *"the phases where we are actually trying to implement the learning from emily"*, and that framing shaped click 1.
- **The capability probe against this project's artifact:** running the committed `chromophore_lut.json` through `Lut.melanin_for` at six tones gave F-P23-1, which no doc stated. The model reaches only III–IV, and VI is 20.5 against 4.5 in red/blue. That turned a seed question into a decision.
- **"A fixture's state is read from its data, never inferred from its name":** measuring the Emily picture's average (red/blue 1.24, paler than any tone) showed that "Emily vs ours" mixes tone and detail, so click 1 holds her picture to tone III as well.
- **Reading a live sibling's uncommitted diff, read-only, before forking:** Phase22's close was landing mid-pass. Its diff answered Q-P23-8 and recorded the lead's lifting of the Studio wait, and the Roadmap edit waited for the sibling's commit instead of racing it.
- **`.claude/CLAUDE.md`'s public-repo rule, *"re-read every sentence you wrote from a private source"*:** the id grep was clean, but a re-read removed a clause about a private library's contents.

## Dead weight

None.

## Open questions

- The seed commit `4398f05` reached origin inside the Phase22 session's close push, minutes after this run's handback said *"unpushed: 1 commit"*. Nothing was wrong (the lead said push there), but a handback's push state can go stale through a sibling. Is that worth a line anywhere, or is it accepted?
