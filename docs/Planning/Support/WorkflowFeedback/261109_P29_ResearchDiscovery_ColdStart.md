# Workflow Feedback — P29 (object opacity) / research → quick-fix → discovery / cold start

| | |
|---|---|
| **Verb** | `research → quick-fix → discovery` (one session: the lead redirected a no-topic `/research` sweep to one ask, then directed a quick-fix plus a seed, then opened discovery) |
| **Unit** | `P29` (from `261105_R_PlatformObjectOpacityAsks.md`) |
| **Mode** | cold start |
| **Outcome** | done. Pass 2 `4ed5d5c`; quick-fix M15 + MasterSet Drift `96ae48c`; seed `07ae7a1` (pushed on the lead's word); Brief `30503c9` (local). `ML_P29_E1` was started on `/execute P29` |
| **Shape** | doc-only |
| **Confidence** | Ran fully: research landing, a lead-directed quick-fix, seeding, discovery to BRIEF READY, cross-session messaging with the consumer's live discovery. **Not exercised:** any build or probe in Unreal (the Brief's claims about the masters are read from engine source, not run). |
| **Date** | 2026-11-09 |

---

## Items, ranked

### 1 — A claim about what an ENGINE cannot do travelled through three docs, and only reading the engine's own source caught it `[doc-gap]`

**Grounding.** The consumer's ask said *"A material instance cannot change its parent's blend mode (MasterSet.md:225 records the same limit for two-sidedness)"*. The claim stood in our own normative spec (MasterSet's two-sided note), in the ask, and in the consumer's phase doc. It also drove the ask's cost model: *"a masked twin of each solid master"*, read as four more graphs. One `grep` of the installed engine's `MaterialInstanceBasePropertyOverrides.h` (`bOverride_BlendMode`, `bOverride_TwoSided`) plus `MaterialInstance.cpp` `InitStaticPermutation` showed that an instance **asset** can override both. That changed the design (four instances, not four masters) and owed a spec `Drift`. `research.md` §Seeds decay covers *"a claim about ANOTHER SYSTEM's capability … checked against that system's own status (its roadmap)"*, which is about a consumer's feature state, not a third-party engine's limits. Nothing said to read the engine. The headers were on disk the whole time (`~/Documents/Unreal/…/Engine/Source`).

**Proposed fix.** In §Seeds decay: *"A claim that an engine or library CANNOT do something is checked against its source or headers when they are on disk: grep the type the limit is about. A limit copied between docs is one claim, however many docs carry it."*

**Where it'd live.** `research.md` §Seeds decay (portable). Possibly `discovery.md` §Discovery discipline beside *"N derived docs agreeing … is usually one claim copied N times"*, which is the same failure.

---

### 2 — Messaging the consumer's LIVE discovery session closed a cross-repo question in minutes; the consumer path in §Separation does not mention it `[doc-gap]`

**Grounding.** The design needed the consumer to confirm that Custom Primitive Data slot 0 was free on its components. `ListAgents` showed the consumer's discovery session (`P127_D1`) live on the same ask. One `SendMessage` (the approach, the ownership split, one question) got back a code-backed answer: slot 0 is free; one other writer, on non-library components. The consumer also corrected its own premise on its side. Q-P29-5 closed before the Brief commit instead of sitting as a held question. `discovery.md` §Working in a shared tree sanctions messaging only for *a sibling phase in this repo*. `LOCAL_DELTAS.md` §Separation (how a consumer's ask arrives and is answered) routes everything through docs and the ledger.

**Proposed fix.** One clause in the consumer path: *"If the consumer's session on the ask is live (`ListAgents`), message it the library's answer, the ownership split and any question only it can answer, and record its reply here by date and content (no private paths). The committed docs stay the record."* Portable as a generalisation of the sibling-phase rule: *a session on the other side of a shared surface, in this repo or a consumer's*.

**Where it'd live.** `discovery.md` §Working in a shared tree (portable), referenced from `LOCAL_DELTAS.md` §Separation.

---

### 3 — The first message named a search mode the session did not have `[self-error-doc-could-prevent]`

**Grounding.** The first message said *"Search mode: Grep/Glob/Read tools"*, per `.claude/CLAUDE.md` §Codebase search (*"Your FIRST message names your search mode"*). The first `Grep` call failed: *"No such tool available: Grep … use grep via the Bash tool"*. The mode was corrected mid-run. The rule says to name the mode but not to check the tool list first, and its wording (*"Use the main session's Grep / Glob / Read tools directly"*) presumes they exist.

**Proposed fix.** *"Name the mode after checking which tools this session lists. Without Grep/Glob, say so and name the fallback."*

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search (or its upstream twin).

---

## Keep these

- **`discovery.md`'s "for each click, check that its surface can show the thing judged"**: it caught that the rig and the look view average 4×4 / 2×2 samples per pixel, which turns the 4×4 dissolve into the see-through fade the lead ruled out. Both clicks are now native resolution (F-P29-1). Without the rule, click 1 would have shown a wrong look as a pass.
- **`research.md`'s "the ruling lands in `## Resolved` FIRST, the derived doc second"**: RD-POA-1 went into the research doc in the quick-fix commit, so the seed commit and the ledger row both cite a ruling already on disk.
- **The cold-start rule that a lead's opening in the same breath turns seed-and-stop into seed-and-continue** (`discovery.md` Cold start 1): "this will be the next phase we do" + "go ahead with discovery" ran straight through without a wasted stop.
- **A pushed-before-reading check for the consumer**: the lead's question *"are the docs updated so phase 127 knows your approach"* had the true answer *"not until pushed: it reads origin"*. The consumer's own phase doc said it re-checks origin, and the push went out on one question.
- **`LOCAL_DELTAS.md` §Separation's "never carry private detail"**: the consumer's reply named its file paths. A grep of the staged Brief for its id and path patterns kept them out of the public repo.

## Dead weight

None.

## Open questions

*(Not methodology: product and lead items routed here because the lead redirected the sweep and then ended the session.)*

1. **The no-topic sweep was cut short by the lead's redirect** ("the one we need to start with is the one for opacity"). Not yet read: Asset-Workshop's **12 unpushed commits** (2026-11-04 → 11-08, Analog Galaxy / House942, some name "Matter") and Asset-Library's **5** (2026-11-01 → 11-08). The lead said there are *"requests from platform and asset library"*. **A lead item:** the next `/research` with no doc named picks them up.
2. **`run_all.py`'s `tool_tests` fails whenever the WorkingDrive is unmounted.** `library/parity` is a link onto it (made 2026-11-02, with an uncommitted `.gitignore` line, `library/parity` without the slash), and `test_gen_skin_shine.py` `mkdir`s it (FileExistsError on the dangling link). Phase27's close hit the same thing. **A lead item:** commit the `.gitignore` line, or make the tools tolerate a missing drive. The Brief tells the executor to remount first.
3. **`30503c9` (the Brief) is not pushed.** The consumer already has its decisions by message. Push when the lead says.
