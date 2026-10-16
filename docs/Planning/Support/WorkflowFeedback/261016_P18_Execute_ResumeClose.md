# Workflow Feedback — P18 / execute / resume → close

| | |
|---|---|
| **Verb** | `execute` (a resume of the suspended run, then the close on the lead's *"Click 4 passed, go to the close"*) |
| **Unit** | `P18` (Character Materials, Their Own Library) |
| **Mode** | resume run 2 → close |
| **Outcome** | `done`. 18.4 landed: units, CONTRIBUTING §3.1, a `sUKN` parser defect fixed, dev.8 built and published at the lead's word, P28 and M11. Click 4 passed. The close was conformed and committed (`0142235`), and a sibling session pushed it before the lead's *"push"* |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: execute BUILD/TRY for 18.4, push, publish, the close (rows A⁻ to D). **Not exercised:** the push itself (a sibling carried it), row C (no issues), B⁺ (not a Wave). |
| **Date** | `2026-10-16` |

*Not a continuation of `261015_P18_DiscoveryExecute_ColdStart.md`.* That file is the first session (discovery through click 3). This is the second session, from the Resume block. Its item 3 recurred here and is noted as item 4, without restating it.

---

## Items, ranked

### 1 — The first article to use a value the grammar always allowed broke two parsers silently; the "shape many tools parse" row did not fire because nothing looked new `[doc-gap]`

**Grounding.** `sUKN` has been in the closed scale-tag set (NamingConventions, `recipe.schema.json`, `validate_material.SCALE_TAGS`) since adoption. The two fitted articles (18.2, 18.3) were the first in the tree to use it. `project_runtime_catalog.SCALE_RE` and `working_tree.SCALE_RE` were `_(s\d+)$`, so both articles projected as off-grammar: a version-less `payload_path`, an empty `scale`, and `_sUKN` left in `display_name`. All gates passed, and two sittings passed over it. It surfaced only at 18.4, when `serve_to_stage.py`'s payload guard refused the eye. The dev catalog and the site file would otherwise have shipped the wrong path to Stage. `execute.md` §Verify's visible-data row covers *"changing the SHAPE of data many tools parse"* with examples (*a new element type, an empty value, a new name sharing a prefix*). I did not read the first use of a grammar-legal value as a shape change, and nothing in the row says it is one.

**Proposed fix.** Add to that row's parenthetical: *"…or **the first instance of a value the grammar always allowed but nothing on disk used** (a closed set's rarely-used member): every parser was written against the values on disk, not the grammar. Grep the parsers of that field before the first commit that uses it."*

**Where it'd live.** `execute.md` §Verify before edit (the visible-data / shape row). Possibly also `discovery.md` §Risk lane, since the Brief chose `sUKN` (RD-P18-8) and could have priced it there.

---

### 2 — The click's surface was a page I PUBLISHED, and I read it as its reader would only after the publish `[self-error-doc-could-prevent]`

**Grounding.** Click 4 judged *"an outside contributor could start from here"* on dev.8's GitHub release page. I built, counted, diffed and pushed, then published on the lead's word. Only then did I read `NOTES.md`, the page's body: it listed every file and said nothing about the kits, the fitted materials or how to contribute. The page could not show what the click was about. Recovery was cheap but not free: a notes generator change, a full ~3 min rebuild to regenerate the text, a `SHA256SUMS` comparison to prove the assets unchanged, `gh release edit`, and a second commit. GitHub lets you edit a release's text; a release asset would not have been so forgiving. §TRY's *"ask whether the surface can SHOW the thing the click is about"* is the right rule, but it reads as *before the sitting*. When the surface is something you publish, *before the sitting* comes after the irreversible step.

**Proposed fix.** In §TRY, beside the surface rule: *"When the click's surface is something you PUBLISH (a release page, a hosted file), read it as its reader will **before you ask for the publish word**, from the built folder: the publish is the irreversible step, and the sitting comes after it."*

**Where it'd live.** `execute.md` §TRY (the fixture/surface paragraph).

---

### 3 — I scheduled a wakeup outside `/loop` as a "fallback" for a build that notified normally, and it cost the lead two empty turns `[self-error-doc-could-prevent]`

**Grounding.** While dev.8 built in the background, I called `ScheduleWakeup` (1800 s) as a fallback. The build notified on completion as designed. Later the wakeup's prompt (*"Check the dev.8 build … and continue"*) arrived twice, both times after the work was done and the handback was out, each time needing a reply that said nothing. The tool is for `/loop` dynamic mode. `execute.md` rule 3 already says *"the completion notification is your wake signal"*, and its one exception is a broken wake signal (a task reported `stopped`/`killed`). Neither held here. The harness's own text on that tool (*"schedule a long fallback … so the loop survives"*) read like general advice, and I applied it outside a loop.

**Proposed fix.** One clause in rule 3: *"…and do not schedule a timed wakeup as a fallback outside `/loop`: a working notification needs none, and a stray wakeup arrives as a turn the lead must read."*

**Where it'd live.** `execute.md` §Three rules, rule 3. Or memory, if the Refiner judges it harness-specific.

---

### 4 — Recurrence: context reported at the first handback only, not at later act boundaries `[self-error-doc-could-prevent]`

**Grounding.** The same lapse as `261015_P18_DiscoveryExecute_ColdStart.md` item 3, in a fresh session. I reported *"Context so far is light, well under the 400k ceiling"* at the first 18.4 handback, and nothing at the push ask, click 4 or the close. The lead did not have to ask this time. This is one more data point for that item's fix (a fixed slot in `Stopping:`), not a new proposal.

**Where it'd live.** As that item.

---

## Keep these

- **Read back every commit (`git show --stat`) against the intended file list and count.** Five commits all matched. When the harness reported the phase doc *"modified on disk"*, the diff showed only my hunks and led to the sibling commit `57e23df` that had edited the same Resume block; I checked that its line survived my anchored edit.
- **"Never break the lead's running environment."** Stage had been up since the day before and a USDLiveView session was live, so I re-served with `--no-restart` instead of the tool's default restart.
- **Compare the SET, not the tally.** dev.8's 580 against dev.7's 572 was diffed name by name: exactly the eight expected additions, nothing dropped. The same diff on the published release found that `NOTES.md` is the page body, not an asset.
- **The serve's payload guard (`cannot serve … expected payload`).** It was the only check that caught item 1, and it now carries a `CAUGHT:` line.
- **`merge-base --is-ancestor` before pushing.** It showed the close commit already on `origin/main` (a sibling had pushed it), so no push was run and the handback did not claim one.
- **Claim live namespace values at use.** P28 and `dev.8` were each read from the ledger and `gh release list` at the moment of use, not taken from the Resume block.

## Dead weight

None.

## Open questions

1. **A sibling's push carried this phase's `🎉` commit before the lead said *"push"* to this session** (lead / Refiner). That follows from the shared-tree design: `CLAUDE.md` §Git's push row says a foreign commit *under* yours cannot be left behind, so the sibling had to carry it. The effect is that the close's one human gate (`execute_close.md` row E) was spent by another session's go, and this session's *"Four commits wait to go up"* was false by the time the lead answered. Is that acceptable as is, or should a close's handback say *"a sibling's push may carry this; the gate then only confirms it"*?
