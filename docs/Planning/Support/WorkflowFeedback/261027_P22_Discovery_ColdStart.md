# Workflow Feedback — P22 / discovery / cold start

| | |
|---|---|
| **Verb** | `discovery` |
| **Unit** | `P22` (*Skin Maps Beyond Colour*) |
| **Mode** | cold start (numbered as it opened), then Pass 2 on the lead's answer |
| **Outcome** | done — numbered (`49da20e`), the Brief written (`e44c57c`), Pass 2 (`54be38b`). The lead's `/retro` argument opened Q-P22-2 (`5a987d0`), recorded and unresolved |
| **Shape** | doc-only |
| **Confidence** | Ran fully: the numbering act, Pass 1 (product docs, research, learnings, the tree grep, the consumer sweep at its origin), the gate baseline, the Brief, Pass 2. **Not exercised:** anything built. The runtime look view's feasibility was read in the game mode, not built. The platform's per-map cost was read along `base_color_map`'s path, not traced end to end. |
| **Date** | 2026-10-27 |

*Step 0: the lead's `/retro` argument ("And irt sounds like we just test the skins in studio directly?") was landed in the phase doc as Q-P22-2 before this file was written.*

---

## Items, ranked

### 1 — A ledger status word was taken for the consumer's current state, and a lead fork was built on it `[self-error-doc-could-prevent]`

**Grounding.** Pass 1's Q-P22-1 rested on *"Studio still draws with masters of its own (P20 OPEN)"*, read from `PlatformDependencies.md`'s status column. In Pass 2, after the lead asked "what does it take to get Studio to see the new maps?", one grep of the platform's code at its origin showed the opposite: Studio binds Matter textures by the library's own slot names and builds its masters from this repo's `build_masters.py`. P20 is OPEN only for its close notes. Both options of the first fork were priced on the false premise, and the lead spent a round trip on it. `discovery.md` already says *"key this on the ARTIFACT, never on the status word"*, but only for a phase doc's own status. The four-point capability rule says *"probe it from the account side"*, but only for hosted services.

**Proposed fix.** Under §Forking test 3 (DELIVERABLE), add: *"When an option's premise is what a consumer can or cannot do today, read the consumer at its origin (its code, or its newest phase log) before putting the fork. A ledger status word is a dated claim about a row, not a measurement of the consumer."*

**Where it'd live.** `discovery.md` §Forking test 3, likely portable. Or `LOCAL_DELTAS.md` §Separation, beside *"fetch, then read at origin"*.

---

### 2 — The first fork's options both skipped the engine sitting on this machine, so the lead had to propose it `[self-error-doc-could-prevent]`

**Grounding.** Q-P22-1 offered (a) a Blender close-up and (b) waiting for Studio. The library's own Unreal runtime, the closest stand-in for Studio and installed on this very machine, was not an option. The lead: *"why not update our UE matter test tool to use the new maps first and shoe screensshots from that?"*. I took Blender because Phase21 had judged there. The *"FOR EACH CLICK, CHECK THAT ITS SURFACE CAN SHOW THE THING JUDGED"* rule checks a chosen surface. It does not ask for the candidate surfaces to be listed first.

**Proposed fix.** In First human test, add: *"Before choosing the surface, list every surface on the step's machine that renders the way the consumer does (the same engine, the same masters), and choose the closest that can show the property. A previous phase's surface is a candidate, not a default."*

**Where it'd live.** `discovery.md` §The Brief, First human test (portable). Its Matter instance is item 3.

---

### 3 — For a character material, the lead's real surface is Studio, and LOCAL_DELTAS points elsewhere `[doc-gap]`

**Grounding.** `LOCAL_DELTAS.md`'s *"the lead's real surface"* row lists *"Blender, USDLiveView, or a rig sheet"*. Its *"artifact a person reaches"* row says anything worn on a body is shown *"on the character or a close camera in the lead's Blender"*. I followed that, and the lead rejected it twice, the second time plainly: *"I think trying to judge if it look plastic in studio using Blender is not the way"*, then *"sounds like we just test the skins in studio directly?"*. RD-CMT-4 (2026-10-27, the look verdict for a character material is made in Studio's look-dev scene) already said where. The rows predate it.

**Proposed fix.** In the two rows: *"A character material's look is judged in Studio (RD-CMT-4). Until Studio can draw what the phase adds, the stand-in is the library's Unreal runtime in a shadowed view, never Blender. Blender and Storm stay tool-agreement columns on the rig."* Hold the exact wording for the lead's answer to Q-P22-2, which settles whether Studio is the only look surface or the last one.

**Where it'd live.** `LOCAL_DELTAS.md` (the real-surface and artifact rows), local.

---

## Keep these

- **The numbering as its own commit before Pass 1** — a sibling sees the number at once, and the 7/9 read-back made the move auditable.
- **The consumer sweep at its origin (`LOCAL_DELTAS.md` §Separation)** — in Pass 2 it gave the per-map list of what Studio needs in a few greps. It is also what overturned item 1.
- **Running the gate baseline in the background while reading** — 18/18 recorded at the measured SHA at no cost to wall time.
- **Grepping the doc for each superseded position after a ruling** — Pass 2's sweep found no stale "Blender" or "own masters" lines left standing.

## Dead weight

None.

## Open questions

1. **Lead:** Q-P22-2 (the phase doc): test the skins only in Studio, the runtime first with Studio last, or as Pass 2 has it? It decides whether the close waits on platform work.
2. **Lead, not methodology — a public-repo leak, already pushed in `4438c1f`:** line 5 of `docs/Planning/Research/261026_R_SyntheticSkinAndEyes.md` names a private platform repository's file path. Said in two handbacks and never fixed: a one-line quick fix, the lead's to order.
3. **Not methodology:** `PlatformDependencies.md` P20's row reads as if Studio had not adopted the library's masters. It has, on Desktop (F-P22-8), and the row stays OPEN for its close notes. A dated note on the row would stop the next reader repeating item 1. The 22.1 ledger work can carry it.
