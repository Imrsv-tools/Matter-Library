# Workflow Feedback — P26 / execute / resume run 2 + close

| | |
|---|---|
| **Verb** | `execute` (26.2, then the close on the lead's *"Close Phase26"*) |
| **Unit** | `P26` (Makeup on the Skin) |
| **Mode** | `resume run 2` (session `ML_P26_E2`, started by `ML_P26_E1`'s retro) + `close`. *Not a continuation of `261102_P26_Execute_ColdStart.md`: a distinct run; its items are not re-filed here.* |
| **Outcome** | `done` — 26.2 built and sat (clicks 4–5 *"yes"*), the pieces served to Stage, the phase closed and pushed (`eb308cc`) |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: Build → Try (one sitting, two clicks) → the close, rows A⁻ to E. **Not exercised:** Strengthen (nothing to repair), the repair ladder, the high-rigor lane. |
| **Date** | `2026-11-02` |

---

## Items, ranked

### 1 — `look.py`'s default output folder holds no composition, so a second makeup look overwrote the first sitting's pictures `[doc-gap]`

**Grounding.** 26.1's sitting was rendered by `look.py <II> --also <VI> --makeup red_lips_hand_tattoo.json --lips-skin` into `library/parity/Look__Skin_FitzpatrickII_…__makeup__lipsskin/`. 26.2's render with `--makeup first_handful.json` got **the same folder name** (`__makeup` is appended, not the composition's name). It overwrote 26.1's `new__face.png`, `also1__face.png`, etc. The `CLICK1–3_*.png` composites survived only because `look.py` deletes just `work/`. To compare *with gloss* against *without*, I had to re-render the 26.1 look into an explicit `--out`. A second phase making looks will hit this.

**Proposed fix.** A `/quick-fix` on `tools/parity/look.py` (and `rig.py`'s same suffix): name the default folder `…__makeup_<composition stem>`. Until then, one line in `docs/Learnings/` or the tool's docstring: *"pass `--out` when rendering a second makeup composition on the same skin."*

**Where it'd live.** a `/quick-fix` on `look.py` / `rig.py` (code), or `docs/Learnings/` until then.

---

### 2 — `.claude/CLAUDE.md` §Codebase search says to use the Grep/Glob tools, and this session had none `[doc-gap]`

**Grounding.** My first message named *"the main session's Grep/Glob/Read tools"* as the search mode, as the rule asks. At the close, a `Grep` call returned *"No such tool available: Grep. Grep is not available in this session — search file contents with `grep` via the Bash tool instead."* Every earlier search had already run through Bash (auto mode, where the §"session's mode does not prompt" clause applies), so nothing broke. But the mode I announced was one the session could not have used.

**Proposed fix.** In §Codebase search: *"Name the mode from the tools you HAVE. Some harness builds offer no Grep/Glob tool: then the shapes rule applies, or the non-prompting clause in auto mode."* Or the refiner records which harness shapes lack the tools.

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search (the refiner decides portable vs local; probably portable).

---

### 3 — The Brief's reuse check said the pieces follow the HDRIs' group, and missed that the group list is shared with the site file `[doc-gap]`

**Grounding.** RD-P26-8: *"additive, as the HDRIs' group was"*. But `groups.GROUPS` is one list read by both the dev catalog and the site file. `test_build_snapshot.py` asserts `B.GROUPS is G.GROUPS` and the exact three ids. Appending `makeup` there would have put a group whose `pieces` list does not exist into the website's file. Found by grepping `GROUPS` before editing (`execute.md` §Verify, *a shape many tools parse*). It was resolved as `DEV_GROUPS` (dev catalog only), recorded as F-P26-8 and marked *(planned)* in SiteFile. Same class as the sibling retro's item 2 (a Brief's claim about readers, made without opening the readers).

**Proposed fix.** Fold into that item: discovery's reuse check names, for each "follow peer X", **every reader of X**, by grep, not only the peer's writer.

**Where it'd live.** `discovery.md` (the reuse check), merged with `261102_P26_Execute_ColdStart.md` item 2.

---

### 4 — At the close I summarised the lead's verdicts as "yes at all five clicks", and click 1 was "The lips are red" `[self-error-doc-could-prevent]`

**Grounding.** The Roadmap entry I wrote first said *the lead: "yes" at all five clicks*. Re-reading the phase doc's verbatim record caught it before the commit. The same gloss went into `MakeupPieces.md`'s banner, and I fixed both. `AI_WorkingAgreement.md` says *"quote the words, not the gloss"*, but a one-line summary in a derived doc does not feel like quoting.

**Proposed fix.** One clause in `execute_close.md` row B: *"An italic context line that cites the lead's verdicts quotes them as recorded. 'yes ×N' only when N were literally 'yes'."*

**Where it'd live.** `execute_close.md` row B (or decline: the WorkingAgreement rule already covers it).

---

## Keep these

- **The cross-session message from `ML_P26_E1`** (the status line owed, the local runtime's path, the labelled-picture style). It arrived early in this run and saved a rediscovery. The prior retro's item 1 (one labelled picture per question) gave two clean one-word answers this time.
- **Measure before the sitting.** The gloss click went out with its numbers (lip colour ≤ 2/255 moved; highlight peak 170 → 255, 131 → 255). Checking the composites caught a clipped header line before the lead saw it.
- **`LOCAL_DELTAS.md` §Two machines: serve on the lead's word while platform sessions are live.** `ListAgents` showed two idle P119 sessions, so the serve waited for one word (*"yes, serve"*) instead of re-serving under them.
- **"The lead's close IS the push go", plus `.claude/CLAUDE.md`'s push row.** The push carried 10 sibling commits under mine. The rule said exactly what to do (push by value, name them first in the handback), with no extra question.
- **Row B's "resolve each link against the tree".** It found the two `../Research/` links the move broke.

## Dead weight

None.

## Open questions

1. The phase closed with **no published Unreal runtime carrying the makeup slots**. `unreal-runtime-v7` refuses a format-5 job, so the rig's Unreal column on another machine cannot show makeup until one is published. That is the lead's word, offered in the close handback, unanswered when `/retro` arrived. Re-raise at the next phase that renders makeup on the library machine.
