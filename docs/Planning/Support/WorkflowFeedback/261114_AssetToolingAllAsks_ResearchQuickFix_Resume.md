# Workflow Feedback — AssetToolingAllAsks / research → quick-fix ×3 → seed / resume

| | |
|---|---|
| **Verb** | `research → quick-fix → seed` (one session: a gather of the asset tooling's asks, two lead rulings, three lead-directed quick fixes, an unnumbered seed, a push) |
| **Unit** | `AssetToolingAllAsks` (`261114_R_AssetToolingAllAsks.md`) |
| **Mode** | resume. The same session (`ML_R_VariousQuestions`) deposited `261109_P29_ResearchDiscovery_ColdStart.md` five days earlier. **This is a distinct run, not a continuation of that file:** a new unit and a new day, with work in between |
| **Outcome** | done. Gather `13cdc90` + rulings `30a1aa1`; Blender asset file rebuilt `322685c`; wish list `cc32fcc` + `1101e06`; seed `3469575`. All pushed (`0deb76d..3469575`). `ML_Batch_AssetAsks` was started on `/matter-batch` |
| **Shape** | behavior-touching (a generated Blender file, the wish list's order) |
| **Confidence** | Ran fully: the gather, the asset-library gate, `run_all.py`, the wish-list tool's `next` / `brief` / `counts` and its test, a by-SHA push. **Not exercised:** the batch itself (running in its own session); the seeded phase's discovery |
| **Date** | 2026-11-14 |

---

## Items, ranked

### 1 — A consumer's research says "send the asks"; its ask doc arrives later and asks for more. I gathered from the research `[doc-gap]`

**Grounding.**
- The asset tooling's research on historical rooms (in its own clone, 2 unpushed commits) recorded its lead's ruling: *"yes we can (and should) make material requests"*, the asks to go *"by its channel"*. I followed `LOCAL_DELTAS.md` §Separation (*"list each sibling clone's unpushed commits … read in place"*), read that research, and gathered its Matter pass into `261114_R_AssetToolingAllAsks.md`.
- 25 minutes later the asset tooling's session committed its **ask doc** into this repo (`afd5d1b`, `261114_R_AssetToolingHistoricalRoomAsks.md`). It asked for six finishes the research's Matter pass never named: Aswan granite, Egyptian calcite, painted softwood, cotton tape, a candle flame, tinplate. It also had two new questions.
- The gather then needed a second pass, and a second wish-list commit.

§Separation treats an unpushed sibling commit as a ruling to surface. It does not say that a ruling to *send* asks means an ask doc is still being written, which then supersedes the research.

**Proposed fix.** In §Separation, after the unpushed-commits clause: *"A consumer's research that rules to send asks is not the ask. If its ask doc is not in this repo yet, say 'ask doc owed', or message the consumer's live session (`ListAgents`) for it, before gathering from the research."*

**Where it'd live.** `LOCAL_DELTAS.md` §Separation; possibly portable as a `research.md` §Seeds decay clause (*a consumer's research is a seed of its ask, not the ask*).

---

### 2 — A compressed file answers every grep with 0: an absence that looks like a finding `[doc-gap]`

**Grounding.** To check which article names `blender/asset_library/MatterLibrary.blend` carried, `grep -a -c <name>` returned **0 for every name**, including ones the file must hold. The file is zstd-compressed (magic `28 b5 2f fd`); after `zstd -dc` the real counts appeared (the retired names 3, the replacements 0). Had only the "missing" names been searched, 0 would have read as *"not in the file"*. `.claude/CLAUDE.md` §Codebase search names one way grep lies (a NUL byte makes it skip a file). A compressed binary is a second way, and Blender 5 saves `.blend` compressed by default.

**Proposed fix.** One clause beside the NUL-byte trap: *"A compressed file (a `.blend` saved compressed, `.gz`, `.zst`) answers every content grep with nothing. Read its first bytes before trusting an absence, and decompress to a stream to search it. Include a name that must be present as a control."*

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search (portable); or a `docs/Learnings/Blender/` entry for the `.blend` specifics.

---

### 3 — `/retro` step 0 says a namer exit 2 means "no offer"; the lead had asked for the session by name of the work `[doc-gap]`

**Grounding.** The lead's message: *"seed, push, /retro and kick off a session for these materials"*. `session_name.py --next "/matter-batch"` exits 2 (*"not a command I name"*), and `retro.md` step 0 reads *"exit 2 = not a command it names: no offer"*. The lead had already asked, so I started it under a plain name (`ML_Batch_AssetAsks`). Read literally, step 0 says not to start a session the lead explicitly asked for.

**Proposed fix.** *"exit 2: the namer does not name this verb. Do not offer one on your own; if the lead asked for it, start it under a plain descriptive name."* Possibly also teach the namer `/matter-batch` (a project skill; the prefix machinery exists).

**Where it'd live.** `retro.md` step 0 (portable); the namer upstream (`workstation/claude/hooks/session_name.py`) if the lead wants batch sessions named.

---

## Keep these

- **`.claude/CLAUDE.md` §Editing: a batch edit replaces an anchor only when it occurs exactly once and aborts otherwise.** My first wish-list script crashed on its own bug (it searched lines it had already set to None). Because it wrote only after every assertion passed, `git diff` showed the file untouched, and the fixed run landed 17 insertions / 8 deletions exactly as counted.
- **The push row's "read every line of `origin/main..HEAD`, then push your tip by value"**: it showed a sibling's commit (`afd5d1b`, the asset tooling's ask) under mine, so the handback named it before the lead said push.
- **Running an existing gate into scratch before touching a tracked generated file** (`check_asset_library.sh <scratch>`): the tracked `.blend` was replaced only after 146 articles conformed and the catalog file came out byte-identical.
- **`research.md`'s "the ruling lands in `## Resolved` FIRST"**: RD-ATA-1 and RD-ATA-2 were committed (`30a1aa1`) before either quick fix, so both quick-fix commits cite a ruling already on disk.

## Dead weight

None.

## Open questions

*(Product, not methodology.)*

1. **`_RefinementBacklog.md` open question 5** (*"Which machine regenerates the tracked `MatterLibrary.blend`, and when?"*) has a data point. It had gone 30 days stale (2026-10-15 → 11-14), the machine with Unreal regenerated it in 22 s with `check_asset_library.sh`, and four separate asks were that one fact. A rule (*"regenerate it in any commit that renames, adds or retires an article"*) would have prevented all four.
2. **The wish list has no way to say "the lead's priority"** except moving lines. `next` orders redo rows, then Phase11's `proving` batches, then list order. Today's order was set by moving rows to the top. A future re-sequencing would do the same, and the list's line order is now carrying a ruling (RD-ATA-1) that is invisible in the file.
3. **The WorkingDrive is still unmounted.** `run_all.py`'s `tool_tests` fails on `library/parity` (third session running), and the uncommitted `.gitignore` line is still in the tree.
