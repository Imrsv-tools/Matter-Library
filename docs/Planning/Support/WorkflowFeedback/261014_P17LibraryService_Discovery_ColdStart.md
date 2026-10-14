# Workflow Feedback — P17 (The Library Service) / Discovery / Cold start

| | |
|---|---|
| **Verb** | `discovery`, plus a lead-directed renumber at its end (*"Make this phase TBD, move the others forward…"*) |
| **Unit** | `P17`: **The Library Service**, now `Phases/Future/PhaseTBD_LibraryService.md`. Later the same evening `P17` means Thumbnails, which has its own retro (`261014_P17Thumbnails_Discovery_ColdStart.md`). This file is **not** a continuation of that one. |
| **Mode** | cold start |
| **Outcome** | `derailed`, then rerouted by the lead. **Pass 1** wrote a full high-rigor Brief (`7ab55ce`). Hetzner had no GPU server, so **Pass 2** priced alternatives (`8ba3dfa`). The lead: *"stay local for now"* (`830538d`), then the phase went back to TBD and the others were renumbered (`cd478d9`). The retro's own fix is `2b9e56c`. |
| **Shape** | doc-only |
| **Confidence** | Ran fully: discovery's reads, the consumer sweep, the web pricing reads, the renumber. **Not exercised:** `/plan`, or anything on a server (none exists). |
| **Date** | 2026-10-14 |

---

## Items, ranked

### 1 — I wrote a full Brief on a machine nobody had ordered, and checked its price but not whether it could be ordered `[self-error-doc-could-prevent]`

**Grounding.**
- The phase's every click needed a rented GPU server, a lead act and a monthly cost.
- Pass 1 still wrote the whole Brief first: four clicks, three steps, a high-rigor lane call, a build map, about 270 lines. The rental went in as `Blockers` item 1 at the very end.
- I read the GEX45's price from Hetzner's **press release**, because the product page rendered no price. I never looked at whether it could be **ordered**.
- The lead's next message: *"no gpus avaiable"*. Then, after a priced list of alternatives: *"We have to rethink and stay local for now"*. Then: *"Make this phase TBD"*.
- Three passes and four commits. The Brief is now kept, but on hold.
- `discovery.md` already says, for a hosted entry path: *"put the clause to the lead with what keeping it running costs them"*. I did. **What it does not say is WHEN, or that availability is part of the probe.**

**Proposed fix.** *"Where the phase's doer is something the lead must rent or buy, put its availability (read from the order page, not an announcement) and its running cost to the lead FIRST, at kickoff, before writing steps or a lane. A Brief built on an unordered machine is the most expensive thing discovery can produce, and the cheapest question to ask."*

**Where it'd live.** `discovery.md`, the Brief's *"RECONCILE THE DOER"* clause and the capability rule's hosted-service sentence.

---

### 2 — A second repro of "two phases own one id scope", in a new shape: the number was handed to a different phase `[doc-gap]`

**Grounding.**
- The P15 retro (item 1) and `_RefinementBacklog.md` (*"Ids minted under a phase number that moved"*) cover a phase **moving** to a new number.
- Here the lead handed **this phase's number to another phase**: *"Thumbnails become Phase 17"*. The Library Service had already published `Q-P17-1…7` and `F-P17-1…7` in commit messages.
- With no rule, I improvised: the receiving phase starts at 8 in each series. That is written into both docs and the Roadmap.
- It works, but it is a convention nobody ruled on, and a reader must know it to resolve `Q-P17-3` against the right doc.

**Proposed fix.** Fold into the P15 item's fix. Whichever form lands (a name stem until the number is stable, or "the number's ids continue"), state what the **receiving** phase does when a number changes hands.

**Where it'd live.** `NamingConventions.md` §Planning ids.

---

### 3 — The cause of the Thumbnails retro's item 4 was this run, and it is fixed `[self-error-doc-could-prevent]`

**Grounding.**
- In Pass 3 I wrote, in `261014_R_MaterialPipeline.md` RD-MP-14: *"Not decided by it … Both are Phase17's Q-P17-7"*.
- RD-DS-8 closed Q-P17-7 eight minutes later. My supersession sweep was mechanical, as the rule requires, but it grepped **for the old position** (Hetzner, flat, rented, the phase numbers). It never grepped for **pointers that defer to the question id**.
- The Thumbnails discovery spent three reads on it.
- Fixed in `2b9e56c`: RD-MP-14 now names RD-DS-8.

**Proposed fix.** The Thumbnails retro's item 4 wording stands. This adds a second repro: **the sweep must grep the closed question's own id**, not only the superseded position.

**Where it'd live.** `discovery.md` §Supersession hygiene.

---

### 4 — A tree-wide `git grep -o -E '.{0,40}X'` stalled past the 2-minute timeout; the same search over the eight named files was instant `[self-error-doc-could-prevent]` *(minor)*

**Grounding.**
- To list path references with context, I ran a leading bounded wildcard with `-o` over the whole tree, which holds LFS objects and `.blend` files.
- It went to the background. I had to find its PID and stop it.
- A `-n` listing of files by name, already run, had given the eight files.

**Proposed fix.** One learning line: *"For context around a match, grep the named files, or `-n` then `sed -n`. A leading `.{0,N}` with `-o` over the whole tree can run for minutes."*

**Where it'd live.** `docs/Learnings/ClaudeCode/` or `GitHub/`. `unsure`.

---

## Keep these

- **§Git's "not separable → rebuild against `HEAD`, commit from the index".** The Phase16 build session rewrote its status line, the same line as one of my path fixes, minutes before my commit. The rebuild committed exactly my change and left its edit in the working tree, verified by `git diff --stat` afterwards.
- **`git show --stat` read-back against the intended counts.** It confirmed every commit: 218/58, 43/10, 33/5, 55/45, 1/1.
- **The batch-edit rule: replace an anchor only when it occurs exactly once, else abort.** 23 anchored edits across 8 files went through in one pass, with no misses and no silent no-ops.
- **The consumer sweep, including the sibling clones' unpushed commits.** It found the website side's view on hosting quickly. A grep for private ids, node names and IPs before each commit kept the private network's details and the web server's specs out of this public repo.
- **"Is this your fork" and recording the lead's words verbatim.** Each of the lead's three short replies landed as a quoted ruling (RD-MP-14, RD-DS-8), with my reading of it kept apart and marked as mine.

## Dead weight

None.

## Open questions

1. **The lane for a future library service** (lead decision). I called it high-rigor (a public-IP box, root access, an upload door). The lead never weighed that, because the phase was held first. Whoever reopens it should put the lane to the lead along with the server.
2. **Prices and availability decay fast.** The GEX45 price and the Scaleway price are dated 2026-10-14 in the phase doc, and Hetzner's stock was the lead's own observation. A future run must re-read both from the order pages before reusing any number in F-P17-1 or F-P17-7.
