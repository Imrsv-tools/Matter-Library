# Workflow Feedback — MatterSitePipeline / howdy → research → quick-fix / cold start

| | |
|---|---|
| **Verb** | `howdy → research → quick-fix` (one session). `/howdy`, then lead-directed work: an opinion and a doc in a sibling repo, rulings recorded in both repos, a `/research` run (the material pipeline) and a seeded one (skin maps), seeds for six phases, and a lead-directed `/quick-fix` to home the loose ends. |
| **Unit** | research slug: the library's website, the material pipeline, skin maps |
| **Mode** | cold start |
| **Outcome** | done. Recorded and committed: `42e26fa`, `a05d485`, `ad838eb`, `3caf294`, `9b5b9f4`, `b79d5fc`, `37cea68` here; `7aa8ab9` and `d85a0a7` in the platform's web repo. Six phases seeded. The last two commits in each repo are not pushed (the lead: "not yet"). |
| **Shape** | doc-only |
| **Confidence** | Ran fully: `/howdy`, `/research` (two docs), the seeding landing, a lead-directed `/quick-fix`. **Not exercised:** `/discovery`, `/plan`, `/execute`; no probe ran. |
| **Date** | 2026-10-14 |

---

## Items, ranked

### 1 — A recorded ruling's gloss was carried as the ruling, and nearly drove a wrong recommendation `[doc-gap]`

**Grounding.** `260929_R_CharacterMaps.md` MAP-RD2 holds the lead's verbatim words (*"no bespoke one image one mesh solutions"*) and an agent's gloss beside them (*"a picture painted to one mesh's UV layout is not"*). The gloss also retired the skin-atlas options. This run quoted the row, verbatim, as research.md asks, and framed the lead's move to skin maps as *"reopens MAP-RD2"*. It recommended a "no body skin map" rule on that basis. The lead: *"No it does not reverse my one image one mesh ruling....That has been mis understadd … it is more about locking mesh then it is about materials"*. The gloss had been wrong for two weeks. Quoting it faithfully only repeated it.

**Proposed fix.** In research.md's "A tension with an earlier ruling quotes the ruling": *"Quote the lead's words, not the row. Where a recorded ruling carries an agent's interpretation beside the verbatim words (a 'this retires…', 'so X is not allowed'), the tension is with the interpretation, and the question to the lead is whether the interpretation is what they meant. Ask that before building a recommendation on it."*

**Where it'd live.** `research.md` (portable).

---

### 2 — Backticks in a double-quoted `python3 -c` emptied doc text, and only a readback caught it `[self-error-doc-could-prevent]`

**Grounding.** The run rewrote a research doc's Status footer with `python3 -I -c "…"`. The new text held markdown backticks (`` `261014_R_SkinMaps.md` ``, `` `/execute Phase11` ``). Bash ran each as a command and substituted nothing: four phrases vanished, and the call printed `ok`. Seen only because stderr showed `command not found` and the footer was read back. The rule exists in `.claude/CLAUDE.md`, but under §Git (*"inside `-m "…"` a backtick is command substitution … The same holds for ANY double-quoted argument"*). This was a doc edit, not a commit, and §Editing says nothing about it.

**Proposed fix.** In §Editing: *"A script that writes doc text takes the text from a file or a quoted heredoc (`<<'EOF'`), never inside a double-quoted `-c` argument. Markdown is full of backticks, and each one is a command the shell runs."* Or a pointer from §Editing to the §Git line.

**Where it'd live.** `.claude/CLAUDE.md` §Editing (local; possibly portable).

---

### 3 — No rule covers the lead's own ruling landing in a sibling, private repo as well as this public one `[doc-gap]`

**Grounding.** The lead asked whether the platform's web repo should build the library's website, then said *"go ahead"*. The ruling binds both repos. The run improvised:
- recorded it upstream in this public repo first (RD-WS-1 to 4), with platform ids and paths left out;
- mirrored it in the private repo under its own ids (RD-MLS-1 to 4);
- cross-referenced each to the other.

`LOCAL_DELTAS.md` §Separation covers only the reverse direction: *"A consumer's ruling that arrives by its own id … record it here by date and content, never by the id"*.

**Proposed fix.** One row in §Separation: *"A ruling the lead makes in a session working both repos: record it here first (public: content and date, no consumer ids or paths), then in the consumer's own decision record under its own ids, each pointing at the other by file name."*

**Where it'd live.** `LOCAL_DELTAS.md` §Separation (local).

---

### 4 — The public-repo scan checked for ids, and a private fact slipped past it `[self-error-doc-could-prevent]`

**Grounding.** Before each public commit the run grepped its new lines for the platform's id patterns (`RD-LAND`, `IMRSV_Web`, …). One draft quoted the platform server's size (*"4 vCPU and shared … 7.6 GiB"*) from the private repo's docs. No grep pattern matched it, and it was caught only by re-reading the paragraph before staging.

**Proposed fix.** In §Separation, after the id-grep line: *"The grep finds ids, not facts. A sentence written from a private doc (hardware, cost, staff, schedules) is re-read for what it discloses, not only searched for ids."*

**Where it'd live.** `LOCAL_DELTAS.md` §Separation, or `.claude/CLAUDE.md` *"The repo is PUBLIC"* (local).

---

### 5 — A recommendation resting on a count was offered before the count was taken `[self-error-doc-could-prevent]`

**Grounding.** The run recommended reviewing by verdict, saying it *"clears the backlog in minutes"*. When it measured (`wishlist.verdict` over the 35 rows), by-verdict kept 11 and left 24 for the lead. The first sweep was also wrong the other way: it counted "moves nothing" as a flag, which `/matter-batch` §3 already says is expected on matte matter. The lead had accepted the recommendation one message earlier.

**Proposed fix.** In research.md's discipline: *"A recommendation whose premise is a count you can take in one call is measured before it is offered. Read the measuring tool's own rules (its skill or docstring) before scoring with it."*

**Where it'd live.** `research.md` (portable).

---

## Keep these

- **The five-beat handback**: held across about fifteen stops of a long, multi-verb session. The lead answered numbered questions by number every time.
- **"Extend, don't duplicate"**: `260926_R_BigPicture_NimbleSetup.md` already mapped the loop. Reading it first kept the pipeline research to what was new: thumbnails, metadata, the console, the service.
- **`git show --stat` read-back after every commit**: confirmed nine commits' file lists and counts while another session committed to the same trunk throughout.
- **The fork tests for "a tension quotes the ruling"**: even with item 1's flaw, quoting MAP-RD2 is what let the lead see the misreading in one message.
- **`/retro` step 0 ("document first")**: the lead's *"lets get everything homed"* turned it into a pass that routed five findings and five Glossary terms before this deposit.

## Dead weight

None.

## Open questions

1. **Does "push all" mean every commit on `main`, or only this session's?** On a shared trunk a push sends both. This run pushed five sibling commits on the lead's "push all", and said so in the handback first. Lead decision, or a one-line rule.
2. **The platform's web repo got a doc and two commits from this session, and has its own `/retro` channel.** Nothing of the method's friction there is filed here. Whether a cross-repo session files one retro or one per repo is unsettled. Refiner's call.
