# Workflow Feedback — DownstreamPicture / research → quick-fix / cold start

| | |
|---|---|
| **Verb** | `research`, with lead-directed graduations: a `quick-fix` (docs only), three seeds, and two renumbers of the Roadmap |
| **Unit** | `DownstreamPicture` (`docs/Planning/Research/261014_R_DownstreamPicture.md`, mnemonic `DS`) |
| **Mode** | cold start, from a `/research` with no doc named: *"Somehow we are getting lost in a folder issue... so I am backing up and pasting a request here.... Cna you make sense of where we are in the overall libary and what you need the downstream tools to incorpoerate"* |
| **Outcome** | done. Four passes, RD-DS-1 to RD-DS-7. The consumer ledger and the install layout brought up to date (`d27c2a9`). Three phases seeded, then numbered, then re-sequenced with two existing ones: Phase15 – 20. One merge of a consumer's ask (`bbbb6ab`). Everything pushed except the footer reconciliation `87118d7` and this file. |
| **Shape** | doc-only, plus one disposable probe (an `.hdr` header written in `/tmp`, loaded in Blender, torn down) |
| **Confidence** | Ran fully: research, the convergence merge, the quick fix, the seeding and both renumbers, pushes by SHA. **Not exercised:** any build. USD's own image reader on the stamped `.hdr` (no Python binding for `Hio` in the toolchain). |
| **Date** | 2026-10-14 |

---

## Items, ranked

### 1 — I put two design questions to the lead that he had already answered, on a sibling artifact in another repo `[self-error-doc-could-prevent]`

**Grounding.** Pass 3 ended on Q-DS-1, *"How do creator, licence, credit and tags reach the engines?"*, with three options. I recommended (b), serving the site file beside the catalog, which is a sidecar in all but name. Q-DS-2 asked whether Character is a group each article declares. The lead: *"I am confused by these questions and the cycal why you are asking thime. What do you mean how does the credit reach the engines? hwo does the name readh then egnies? … use existing solutions … I thought we solves this with assets and compositions... same thing. 2) I have no idea what you are asking here... what is the use case?"*

He had ruled the general case on 2026-10-11 in the platform's research on asset credit: no file beside an asset, and the asset's own file says what it is. The web side ruled it too, earlier. I found that ruling only **after** his correction, by grepping the platform docs for how an asset carries its licence. The sweep `LOCAL_DELTAS.md` §Separation prescribes looks for rulings **about the library**. This one was about **assets**, the library's sibling, so the sweep could not see it. Q-DS-2 had no use case behind it at all: nothing in the library today is a generic biological material.

**Proposed fix.** In `research.md` §The research discipline, beside *"Name the altitude"*:

> **Before you put a design question to the lead, look for his ruling on the same question for a sibling artifact.** Here: how the platform's assets and compositions do it, read in the consumers' docs. If he has ruled it there, the question becomes *"the same way?"*, or no question at all. **State the use case in the question.** If you cannot name one, it is not a question for the lead.

**Where it'd live.** `research.md` (portable). Possibly a one-line pointer in `LOCAL_DELTAS.md` §Separation naming *assets and compositions* as the library's sibling.

---

### 2 — Numbering every phase on "make these the next phases" turned a re-sequence half an hour later into ten files of renames `[self-error-doc-could-prevent]`

**Grounding.**
- At 19:11, on *"Lets make these the next phases (Before the scaled grid)"*, I numbered all three seeds Phase15 – 17. I moved their docs out of `Future/`, and renumbered Scale Grids from 15 to 18 (`d71a30d`, 8 files).
- At 19:20, *"Actually lets pull the library service and thumbnails before Scale grids as well"* forced a second renumber: 17 → 19, 18 → 20, and two more docs moved (`4b0b67b`, 10 files).
- In between, another session committed a note in the Scale Grids doc that said **Phase17** for Character Materials. Within the hour that number meant The Library Service. I could only annotate it, not fix it.
- The Roadmap already says *"order is position in the list, never an ordinal"*. Position alone would have carried *"next, before Scale Grids"*.
- The lead asked for **order**. Only Phase15 needed a number, because only it was about to be opened, and a session did open it minutes later.

**Proposed fix.** In the Workflow's §Phase Numbering, or `research.md` §Landing:

> **"Make these next" is an order, not a numbering.** Move the entries by position. Number only the head, the one a verb is about to open, unless the lead names numbers. Every number given early is a rename the next re-sequence pays for, and a word that silently changes meaning in every live session's notes.

This complements the P15 discovery retro's item 1 (`261014_P15_Discovery_ColdStart.md`, about minted ids after a renumber). That item is about the cost after a renumber; this one is about not making the renumber.

**Where it'd live.** `Methodology/AgenticEngineering_Workflow.md` §Phase Numbering (portable).

---

### 3 — The freshest lead ruling about the library was in a sibling clone's UNPUSHED commits, which a read at origin cannot see `[doc-gap]`

**Grounding.**
- The lead's *"pasting a request here"* pasted nothing; the request lived elsewhere.
- What answered it was the lead's *Matter | Character | HDRI* ruling (RD-DS-1 here). It was recorded in a USDLiveView research doc that existed only as **five local, unpushed commits** in that clone (18:06 – 18:21).
- `research.md` §Seeds decay says *"read what the finding rests on at origin (`git show origin/<branch>:<path>`)"*. `LOCAL_DELTAS.md` §Separation says *"fetch, then read at origin"*. Followed literally, both miss it.
- I found it only by running `git log origin/main..HEAD` in the USDLiveView clone after the fetch.

**Proposed fix.** In `LOCAL_DELTAS.md` §Separation, the sweep line:

> … rulings about the library recorded on their side and not here (fetch, then read at origin, **and list each sibling clone's unpushed commits, `git log origin/main..HEAD`, read in place, never pulled: a ruling made in the last hour is often only there**).

**Where it'd live.** `LOCAL_DELTAS.md` §Separation (local: the sibling clones are this machine's layout). The *read at origin* clause in `research.md` might want the same carve-out (portable).

---

### 4 — Which sibling repos are private is not written anywhere, so the public-repo rule has to be measured each time `[doc-gap]`

**Grounding.** My first draft of the research doc named a USDLiveView research doc by filename and said how many commits sat unpushed there. I checked visibility with `gh repo view` only before committing. USDLiveView and the website's repo are both **PRIVATE** (measured 2026-10-14), so both details came out. `.claude/CLAUDE.md` says *"the repo is PUBLIC … never carry private platform detail"*. But USDLiveView appears in this repo's public specs often enough to read as public.

**Proposed fix.** One dated row in `LOCAL_DELTAS.md` §Separation: *"Private as of 2026-10-14 (`gh repo view --json visibility`): USDLiveView, the website's repo, the platform docs and Stage. Their file paths, ids and commit counts stay out of this repo; their rulings and asks come in by content."*

**Where it'd live.** `LOCAL_DELTAS.md` (local).

---

### 5 — I used `cd /tmp` in one command, against the hard rule `[self-error-doc-could-prevent]` *(low)*

**Grounding.** `cd /tmp && rm -rf /tmp/dev3chk && mkdir … && gh release download … -D /tmp/dev3chk`. The `-D` flag already made the `cd` unnecessary. The harness reset the shell's working directory afterwards, so no later command ran in the wrong place.

**Proposed fix.** None to the docs. The rule is clear and prominent; this was attention, not wording. Recorded so the Refiner can count it if the same slip recurs elsewhere.

**Where it'd live.** n/a.

---

## Keep these

- **Push your tip by value when foreign commits sit on top** (`.claude/CLAUDE.md` §Git, the push row). On the last push five sibling commits had landed above mine, Phase15 executing among them. `git push origin 4b0b67b:refs/heads/main` sent exactly the four the lead approved.
- **Pathspec commit plus `git show --stat` read-back, with the shared index in mind.** During the retro, the Phase15 executor had 30 staged renames in the index. The pathspec commits kept them out, and the read-back confirmed it.
- **Measure before claiming:**
  - the live dev install (`ls`, the catalog's counts);
  - the `.hdr` header probe;
  - the web's mirror read at its origin (accepts schema 1 only);
  - USDLiveView's launcher read at its origin, which turned P7 DONE.

  Each replaced a claim I would otherwise have repeated from a doc. Two docs were stale on exactly those points.
- **Converge first** (`LOCAL_DELTAS.md` §Separation): the refused pull was the platform's ask (HDRI Pass 3). Merging it before writing put A9 and A10 in this research's frame from the start.
- **One `AskUserQuestion` with a recommended option** for the one real ordering fork (where Character goes). The lead answered in one click.
- **Annotate, don't rewrite, another session's text.** I added a dated reading line under the sibling's Scale Grids note rather than editing its "Phase17".

## Dead weight

None.

## Open questions

1. **A path in another retro deposit is stale.** `261014_P15_Discovery_ColdStart.md` cites `Phase18_ScaleGrids.md`, which is `Phase19_ScaleGrids.md` since `4b0b67b`. It is the retro lane's file, so I left it; for the Refiner at drain.
2. **Product, not method (the lead's):** Q-DS-3 to Q-DS-5 in the research doc. They cover whether a build for others may carry the dev install, the dev install's identity, and where the fit pictures live in a real release. None blocks Phase15 – 20.
