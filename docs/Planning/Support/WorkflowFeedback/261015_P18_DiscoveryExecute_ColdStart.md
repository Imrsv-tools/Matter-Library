# Workflow Feedback — P18 / discovery → execute / cold start

| | |
|---|---|
| **Verb** | `discovery → execute` (one session: `/discovery p18`, the lead's "A on both, then /execute P18", then execute through click 3) |
| **Unit** | `P18` (Character Materials, Their Own Library) |
| **Mode** | cold start → suspend-handoff (the lead: *"you have high context"*) |
| **Outcome** | `suspended` — Brief written and both lead calls answered; 18.1–18.3 landed with clicks 1–3 passed; 18.4 started (WIP commit), Resume block in the phase doc |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: discovery Pass 1, execute BUILD/TRY for three steps, the suspend. **Not exercised:** publish, push, ledger rows, the close. |
| **Date** | `2026-10-15` |

---

## Items, ranked

### 1 — Nothing asks "what fingerprints the file I am about to edit?", so a no-pixel-change edit cost a 45-minute GPU re-render, found after the fact `[self-error-doc-could-prevent]`

**Grounding.** The Brief's build map listed `blender/masters/load_article.py` as changed (it now takes an article's own picture). The thumbnail record's `masters_sha256` hashes the whole `blender/masters/` folder. The edit changed no picture, but it made all 82 published thumbnails stale, and `build_snapshot.py` refuses a stale thumbnail. That surfaced only when 18.3's thumbnail run printed `made (masters_sha256)` for articles I had not touched. The re-render took 51 min wall (2475 s of GPU) on the lead's laptop. The discovery's risk-lane read covered *"whatever ENUMERATES that tree"* (gates), but a staleness key is not a gate. Execute's Verify table covers the inverse case (*"making data VISIBLE … staleness sets"*), not *"editing a file a fingerprint covers"*.

**Proposed fix.** In discovery's Risk lane, beside the enumeration rule: *"For every file the build map changes, grep for what HASHES or fingerprints it (records, caches, `*_sha256`, stale checks) and price what the change re-makes. A re-make the Brief did not price is a surprise at execute."* Optionally mirror it as a Verify-before-edit row in `execute.md`.

**Where it'd live.** `discovery.md` §The Brief (Risk lane), possibly `execute.md` §Verify before edit.

---

### 2 — A new check was proved only on fixtures I made, and went false red on the first real subject one step later `[self-error-doc-could-prevent]`

**Grounding.** G8 (a fitted picture covers its mesh's UV islands) passed the real teeth set and refused my three RED fixtures, and was committed at 18.2. At 18.3 the first real eye picture failed it. MakeHuman's eye pictures paint their background a grey that is also 0.3 % of each eyeball, over my 0.2 % limit taken across the whole layout. All nine CC0 eye pictures were on disk when I wrote G8. Running it over them would have taken seconds and caught it. The rework (per-island counting, a 16-bit island picture, a shared island helper) cost a re-commit of four committed files. Execute's row *"an ad-hoc check … Confirm it can fail"* is the half I did. The other half, *it passes on the population it will meet*, is not written anywhere.

**Proposed fix.** Extend that row: *"…and before committing a check that gates content, run it over every existing real subject of its kind, not only the one fixture that motivated it. A check that has only met your fixtures is unproven in both directions."*

**Where it'd live.** `execute.md` §Verify before edit (the ad-hoc-check row).

---

### 3 — Context was reported once, then not at the next two act boundaries, and the lead had to say it `[self-error-doc-could-prevent]`

**Grounding.** `execute.md` §Keep the lead oriented says to put rough context use in the ledger at each ACT boundary and to offer the handoff past ~400k. I gave a figure at the click-2 handback only. At the click-3 handbacks I gave none, and the lead ended it: *"you have high context"*. This session also carried a full discovery (most of its reads) before execute began, because the lead chained them (*"A on both, then /execute P18"*). The rule exists; it is easy to drop because the five-beat handback has no slot that carries it.

**Proposed fix.** Give the figure a fixed home: *"At every TRY stop, the `Stopping:` line ends with the rough context, e.g. `(~300k)`."* And in `discovery.md` §Hand-off: *"When the lead chains discovery straight into execute in the same session, say the context at the hand-off and offer a fresh session for execute."*

**Where it'd live.** `execute.md` §Keep the lead oriented (or `AI_WorkingAgreement.md`'s handback format) · `discovery.md` §Hand-off.

---

### 4 — Getting a GUI view right for the lead took four launches; three were Blender API traps, now owed as learnings `[doc-gap]`

**Grounding.** Click 1's view went through four launches, each found by an MCP screenshot before the handover. First, everything was selected in edit mode, so an orange sheet covered the teeth and the layout. Second, the layout image was gone, because an image with no user is dropped when the file is saved. Third, the Asset Browser's library and search did not stick, because its `params` exist only after the area has drawn. B10/B11's *"render or look at the exact view before you open it"* is what caught all three, and it worked. The traps themselves are not in Learnings. Routed: the Resume block lists them as learnings owed at the close.

**Proposed fix.** None to the method. Confirm at the close that Blender B16–B18 (or whatever numbers are free) land.

**Where it'd live.** `docs/Learnings/Blender/` (owed at the close; already in the Resume block).

---

## Keep these

- **Discovery's "is this even YOUR fork?" (two lead rulings).** It turned what I would have closed as an agent's call (a fitted picture inside the article) into a held fork: CM2 against RD-DS-1. The lead answered it in one line, *"A on both"*, and the answer re-shaped 18.2–18.4.
- **"Search where rulings live" plus `git log` ordering.** Timestamping F-SKM-10 (14:40) against RD-DS-1/4 (about 18:59) showed the SkinMaps draft's *"Ruled"* label was a finding.
- **Reconcile the doer and the surface per click.** Measuring that the platform builds from the same pinned teeth and eye meshes made click 1's *"is it Studio's mesh too?"* answerable before any code.
- **Look at the exact view before handing it over (B10/B11).** It caught three broken views, none of which reached the lead.
- **One click per step, the lead driving each before the next.** Three clean *"yes, go on"*s, and each step's surprises were found inside its own step.

## Dead weight

None.

## Open questions

1. **A name shared with the platform (lead's call, not the Refiner's).** The platform's planning uses *Character Library* for a phase about poses and expressions; this repo's Phase18 file is `Phase18_CharacterLibrary.md` (character *materials*). It was not raised with the lead in-session. Rename the file, or note the difference in the Glossary?
2. **A stale seed line** (not this run's to fix, routed to Phase18's close deferral ledger): `PhaseTBD_SkinMaps.md` still says *"The lead's answer to Q-SKM-7 comes before /discovery"*, but RD-SKM-5 answered it on 2026-10-14.
