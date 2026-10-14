# Workflow Feedback — P16 / discovery / cold start + Pass 2

| | |
|---|---|
| **Verb** | `discovery` |
| **Unit** | `P16` (*Every Entry Says What It Is*) |
| **Mode** | `cold start`, then a second pass in the same session. The lead asked for it after Phase15 closed (*"Things shifted a bit and P15 just finished... do another discovery pass"*). |
| **Outcome** | `done`. The Brief is ready in the build lane. The lead answered both of its calls (MatterBot; stamp in the served copy), and Pass 2 re-cut the Brief on what Phase15 landed (`191eaa8`, `2ff6118`, `71c3b85`, `11a30cd`). |
| **Shape** | `doc-only` (phase doc and Roadmap line; probes in `/tmp` only) |
| **Confidence** | Ran fully: discovery, Pass 1 and Pass 2, including two probes and the cross-session exchange with Phase15's discovery. **Not exercised:** execute. The items about execute's first act are inferential. |
| **Date** | `2026-10-14` |

Step 0: nothing from this run lived only in chat. Both rulings, the probes, the answer to *"What is the consumer in this case?"* and the Phase15 split are all in the phase doc.

---

## Items, ranked

### 1 — `retro.md` says *"You cannot message another session"*, but this harness can, and that channel is what made a concurrent discovery work `[doc-gap]`

**Grounding.**
- `/discovery P16` ran while two `P15_D1` sessions ran Phase15's discovery. The two phases write the same five places: `imrsv_metadata`, the `.hdr` header, the dev catalog's entries, the site file and `build_snapshot.py`.
- I committed a §Shared-with-Phase15 split and sent it with `SendMessage`. Phase15's session answered within the hour with a gap I had wrong: it builds **no** `.hdr` stamp, so my stamp must also write its `group`, `when` and `sky`. It also accepted A10.
- Both Briefs converged with no lead round trip.
- `retro.md` §TERMINAL step 1 still says *"You cannot message another session"*, and `discovery.md` names no such channel at all. Followed literally, the gap would have surfaced at execute, as a missing header write.

**Proposed fix.** Where the method talks about a sibling session (`discovery.md` §Working in a shared tree; `retro.md`'s *"hand the correction to the live run"*), say:

> If the harness lists peer sessions (`ListAgents`), message the one live on the overlapping unit: name the shared surface, what you claim, and what you leave to it. The committed doc stays the record; the message only points at it.

Keep *"you cannot message"* as the fallback for harnesses without the channel.

**Where it'd live.** `retro.md` §TERMINAL step 1 · `discovery.md` §Working in a shared tree. Probably portable, since it describes the harness and not this project.

---

### 2 — A blocker option worded as a role (*"the copy a consumer receives"*) made the lead ask what it meant: one round trip `[self-error-doc-could-prevent]`

**Grounding.** Blocker 2 offered *"(A) In the copy a consumer receives"*. The lead answered Blocker 1 and asked *"What is the consumer in this case?"*. The concrete answer was in my head and in no option:
- **the folder:** `$IMRSV_STAGE_RUNTIME/MatterLibrary/releases/matterlib-dev/hdris/`, today a link into the repo;
- **the apps:** USDLiveView and Stage → Studio;
- **one exception:** USDLiveView's checkout mode.

Once that was said, the lead picked A in one line.

**Proposed fix.** In `discovery.md` §Forking to the lead, add a fifth check beside the four tests:

> **Each option names the concrete thing it changes:** the path, the app, the file. Never only the role (consumer, producer, the served copy). If the lead would have to ask *"which one?"*, the option is not finished.

**Where it'd live.** `discovery.md` §Forking to the lead, or `AI_WorkingAgreement.md`'s plain-language rule if it is wider than forks.

---

### 3 — I wrote two claims into the phase doc before checking them; both were caught only on read-back `[self-error-doc-could-prevent]`

**Grounding.**
- **(a)** The Pass 1 Discovery Log said *"The tree was searched for this phase's name: only the Roadmap and the research name it"*, written from the Read checklist (item 6) before running the search. The search, run afterwards to make the line true, found more names, and **found `Phase19_CharacterLibrary.md`: a renumber (RD-DS-7) that had landed mid-pass.** The Brief was citing the stale order.
- **(b)** The Pass 2 draft said Phase15's 15.3 message told USDLiveView that *"its support-info ask"* is Phase16's. Phase15's log says only *"L3 is Phase16's"*, and `L3` is not defined in this repo. I had inferred the meaning. A grep showed it unresolvable, and the sentence was weakened before the commit.

Both are the decay rule *"write it down or drop it"* running backwards: written down, but before it was known.

**Proposed fix.** In `discovery.md` Read item 6: *"Run it before writing the Brief, and put its hit list in the Log; the Log records results, never intentions."* And under *"Confirmed requires the confirming artifact in hand"*: *"This covers your own Log lines and paraphrases of another unit's messages."*

**Where it'd live.** `discovery.md` §Read item 6 · §Discovery discipline.

---

### 4 — A Brief written ahead of a precursor that owns its shapes needs a named re-verify trigger `[doc-gap]`

*(Second sighting, next to `261014_P15_Discovery_ColdStart.md` item 3, which is about a ready Brief **re-sequenced** behind others. This is the other case: a Brief written **while** its precursor was undiscovered and unbuilt.)*

**Grounding.**
- Pass 1 had to defer the key spellings, the header prefix and both schema numbers to Phase15. It wrote *"execute's first act: read Phase15's closed Brief"*.
- When Phase15 closed, the lead had to notice and ask for a second pass himself.
- That pass changed real things:
  - click 1's surface (the library is read from the repo, as Append);
  - the write method: one-time insert → re-assembly, after a probe;
  - the build map's real names;
  - a new step act: tell the consumers, as 15.3 did;
  - two Not-now rows.

**Proposed fix.** When a Brief defers decisions to a precursor phase, the Brief and its Roadmap status carry the trigger, for example *"BRIEF READY — re-pass when Phase15 closes"*. The precursor's close then names it in its `Next`.

**Where it'd live.** `discovery.md` §The Brief (alongside the deferral-row rule) · `execute_close.md` (the close lists Briefs waiting on it).

---

### 5 — `cd` again, in a probe command `[self-error-doc-could-prevent]`

*(Second sighting: `261014_DownstreamPicture_Research_ColdStart.md` item 5.)*

**Grounding.** The probe's setup command began with `cd /dev/null`. It failed harmlessly ("Not a directory"), and nothing was hurt. The cause was the same as last time: a habitual prefix while writing a multi-line heredoc setup. The rule was loaded and I still typed it.

**Proposed fix.** None beyond the first sighting's. Recorded so the count is right.

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search (the count only).

---

## Keep these

- **Running a premise probe inside discovery.** Both probes changed the Brief:
  - Storm reading a stamped `.hdr` pixel for pixel cleared the riskiest assumption under the HDRI half (the Storm S2 learning made it a real worry);
  - re-assembling all 95 recipes into `/tmp` (byte-identical, 95 of 95) replaced a bespoke insert script with the existing writer.

  Neither touched the tree.
- **"Search where rulings live" plus "enumerate the peer surfaces".** Measuring Blender's `AssetMetaData` fields found the lead's real test surface (Author and License in the Asset Browser). The phase had none until then.
- **The hosted-cost rule** (*probe from the account side; put the cost to the lead*). It turned an assumed in-repo HDRI rewrite into a lead choice. The metered fact was cited by Phase14's finding id, with no figures in this public repo.
- **The pathspec commit with `git show --stat` read-back.** A sibling had a staged rename in the index during Pass 2, and the explicit-path commit left it alone.

## Dead weight

None.

## Open questions

1. **For the Refiner:** is item 1 portable? It depends on the harness having peer messaging. If the upstream method must work without it, the wording needs both branches.
