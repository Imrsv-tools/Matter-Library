# Workflow Feedback — P15 (Matter, Character and HDRI) / discovery → execute → close / cold start

| | |
|---|---|
| **Verb** | `discovery → execute` (one session: discovery, then `/execute` on the lead's word, through the close) |
| **Unit** | `P15`, *Matter, Character and HDRI*, **not** Scale Grids. The file `261014_P15_Discovery_ColdStart.md` is a **distinct run** on Scale Grids, which held the number Phase15 earlier the same day. This file does not continue it. |
| **Mode** | `cold start` → `close` |
| **Outcome** | `done`. Brief `cc6905b`; 15.1 `16b57f8`; 15.3's ledger ask `9acc014`; 15.2 `9e6f914`; `dev.4` published; `🎉` `c474572`, pushed. Three sittings, all passed. |
| **Shape** | `behavior-touching` (30 articles moved; tools, gates, Blender library, dev catalog, site file) |
| **Confidence** | Ran fully: discovery, execute (build, try, strengthen), the close, the push, a GitHub publish, cross-session messages. **Not exercised:** `/plan`, the repair ladder. |
| **Date** | `2026-10-14` |

Step 0 was complete before this file: every finding and recommendation from the run is in the phase doc, ledger rows P25, P27 and M11, or the Roadmap. Nothing was routed only in chat except the items below.

---

## Items, ranked

### 1 — Two discoveries on adjacent phases ran at once and each assumed the other owned the same work `[doc-gap]`

**Grounding.** Phase16's discovery was live at the same time as this one. Each Brief touches the same five places: the `imrsv_metadata` block, the `.hdr` header, the catalog entry and its `schema_version`, the site file, and `build_snapshot.py`.
- **Phase16's split table** gave *"the taxonomy in the `.hdr` header"* to Phase15.
- **My draft RD-P15-4** gave every header write to Phase16.

Nothing in `discovery.md` asked me to look. I found out only because Phase16's session sent a cross-session message after it committed. I reconciled it in RD-P15-4, plus a reply message. Had neither of us messaged, the HDRI taxonomy would never have been written into the header, and both Briefs would have read as complete.

The same pass also caught a renumbering mid-discovery: Phase17 became Phase19 (RD-DS-7). I saw it only because my `Write` was refused on a changed file.

**Proposed fix.** In `discovery.md` §Working in a shared tree:

> *"When another phase in the same sequence is in discovery or execution and shares a surface with yours, read its shared-surface section before you write the Brief. Record who owns each shared item **in both directions**, and tell its session the split."*

**Where it'd live.** `discovery.md` §Working in a shared tree (portable).

---

### 2 — `retro.md` says *"You cannot message another session"*; in this harness you can `[doc-gap]`

**Grounding.** `retro.md` §`/retro` IS TERMINAL step 1 builds its *"deposit the correction HERE"* rule on that sentence. This run, though:
- received a peer's message (Phase16's session);
- replied to it with `SendMessage`;
- found live sessions with `ListAgents`;
- sent 15.3's consumer asks to the website's and USDLiveView's sessions.

The sentence is false wherever these tools exist. It also hides a real channel for the case it was written for: handing a correction to a live run.

**Proposed fix.** *"If the harness offers cross-session messaging (`ListAgents` / `SendMessage`), send the correction to the live run **and** keep it in this retro. Without that tool, the retro is the only channel."*

**Where it'd live.** `retro.md` (portable; harness-conditional).

---

### 3 — Receiving end of the shared ID range: this phase's findings had to start at `F-P15-9` `[doc-gap]`

**Grounding.** When this phase was numbered Phase15, Scale Grids (now Phase20) already used `F-P15-1` to `F-P15-8`. I adapted by starting at `F-P15-9`, with a note at the top of the doc. The `D-1…D-8` ids it also minted did not collide with my `RD-P15-n`. This is the same issue as item 1 of `261014_P15_Discovery_ColdStart.md`, seen from the phase that received the number. The one addition: the adaptation works, but `F-P15-1` still resolves to the wrong file. The scope means "which file to open" (NamingConventions §Planning ids), so after a renumber the id points at this doc.

**Proposed fix.** Fold into that item's fix. Whatever rule it lands, say what the **receiving** phase does: start after the last used ordinal, or the renumbered phase rewrites its ids.

**Where it'd live.** `NamingConventions.md` §Planning ids / `discovery.md` (with the other file's item 1).

---

### 4 — A composition built for a USDLiveView sitting must carry a Studio file's standard scopes `[self-error-doc-could-prevent]`

**Grounding.** Click 2's fixture `Character30.imrsv` was a minimal USDA with only `Environment`, `Meshes` and `Materials`. Opened through Stage, `stage.log` filled with `Failed to define UsdPrim </Composition/Marks>` and `IMRSV file missing Audience prim … Failed to create Audience prim`. The materials still resolved. I caught it by reading `stage.log` before the handover, then rebuilt the file with `Audience`, `Lights`, `Sounds`, `Cameras` and `Marks` copied from Phase14's sitting file. The second open logged no warnings. A headless `usdrecord` render had passed the first file, because Stage's structure check is not in that path.

**Proposed fix.** In `LOCAL_DELTAS.md`'s *artifact a person reaches* row, or a learning:

> *"A composition built for a USDLiveView sitting copies a Studio file's top-level scopes (Environment, Audience, Meshes, Lights, Sounds, Cameras, Marks, Materials); Stage cannot repair a missing one. Read `stage.log` after opening it."*

**Where it'd live.** `LOCAL_DELTAS.md` (the sitting row), or a new `docs/Learnings/` entry for Stage or USDLiveView. There is no Stage domain yet.

---

### 5 — Whether the lead's *"close"* is also the push go is ambiguous here `[doc-gap]`

**Grounding.** `execute_close.md` row E: *"IF `LOCAL_DELTAS.md` MAKES THE LEAD'S `close` THE PUSH GO, IT IS — do not ask."* LOCAL_DELTAS' push row says *"Otherwise the close's push is the only one"*, which neither grants it nor withholds it. I stopped and asked, so the lead had to type *"Push"* after *"close the phase"*. That was one extra round trip, on a repo where every push is public.

**Proposed fix.** One clause in LOCAL_DELTAS' push row, the lead's choice either way: *"The lead's `close` is / is not the push go."*

**Where it'd live.** `LOCAL_DELTAS.md` (local).

---

## Keep these

- **Discovery read the consumer's code for the entry path** (Stage's search-root walk). That found the two-level limit before the lead's folder choice, so RD-P15-8 was made with Studio's cost on the table rather than discovered at a sitting.
- **Mechanical edits as scripts that abort unless every anchor matches exactly once:** the 30-article move and the 30 wish-list slots. Plus reading the diff counts back afterwards: re-assembly was exactly 90 metadata lines and 24 texture paths.
- **Looking before the handover:** a headless render with the consumer's own search-path rule, then a desktop screenshot of the real windows. That is how the fixture defect (item 4) and a framing problem were seen before the lead's click.
- **CLAUDE.md §Git's push-by-value row.** Three sibling commits landed on top between the close and *"Push"*. Pushing `c474572:refs/heads/main` left them for their own sessions.

## Dead weight

None.

## Open questions

- `tools/releases/hdris.py`'s `stale()` treats every thumbnail as stale whenever `hdris.py` itself changes (its mtime is part of the check). This run kept its HDRI code in `groups.py` to avoid rebuilding 59 thumbnails. Phase16's stamp is planned **inside** `hdris.py` (its build map), so it will trigger that rebuild. That may be intended (a recipe change *should* rebuild), but nothing tells an editor. Learning, code comment, or leave it?
