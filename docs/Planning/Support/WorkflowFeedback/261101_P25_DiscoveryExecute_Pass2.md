# Workflow Feedback — P25 / discovery → execute / Pass 2 (re-discovery, then 25.1 again)

| | |
|---|---|
| **Verb** | `discovery` (Pass 2, re-discovery after 25.1.8) **then** `execute` (25.1 on Pass 2's Brief), one session |
| **Unit** | `P25` |
| **Mode** | cold start of Pass 2 (session `ML_P25_D2`); **not** a continuation of `261101_P25_DiscoveryExecute_ColdStart.md` (a different run, same unit and day) |
| **Outcome** | `derailed` at click 1: the Brief landed (`18c840f`, `fd20ab7`, `c6b890d`), 25.1 built `paint_uv.py` (`eff0196`) and sat click 1; the lead: *"Nope... we have to figure out how we get MUCH closer to the last image"*. The lead then made the phase open research and testing (Pass 3 opening, recorded); `ML_P25_D3` started on `/discovery Phase25`. |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: discovery Pass 2 (with two premise probes), execute BUILD and TRY to one sitting. **Not exercised:** STRENGTHEN, the close, `/plan`. |
| **Date** | `2026-11-01` |

**A correction is owed to the live `ML_P25_D3` run** (sent by message, 2026-11-01): the phase doc's 25.1.9 row, the Pass 3 opening's "Kept from Pass 2" line, and the comment in `tools/converters/fit/paint_uv.py` `cmd_paint` say *"ComfyUI served a cached result for a re-used name"*. **That diagnosis is wrong:** the identical outputs were Krea at denoise 0.9 ignoring its input (25.1.10 proved it: plain, cued and filled sources byte-identical at 0.9, different at 0.6 and 0.75). The hashed upload is harmless, not a fix. Not edited here because D3 is live on the doc.

---

## Items, ranked

### 1 — The click-1 sheet left out the picture the lead had just praised; the lead made the comparison himself `[self-error-doc-could-prevent]`

**Grounding.** Mid-execute the lead wrote *"WOW! If we could make uv_a_s90_Seed7.png or uv_a_s45_seed7.png to work... we would be in great shape!"*. That flat picture became the target, but the sheet I built for click 1 was A · C · D-views · D-map, the Brief's reference (D-views) from before the praise. The lead added it as *"the 5th image"* in a screenshot and judged against it: *"we have to figure out how we get MUCH closer to the last image"*. `execute.md` §TRY says to measure the change *"against the reference the lead has accepted (the gap left)"*; a reference accepted **during the run** was not read as one.

**Proposed fix.** `execute.md` §TRY, beside the reference sentence: *"A picture the lead praises mid-run is the reference from that moment: put it on the sitting's sheet beside the candidate, and say how far the candidate is from it before you show."*

**Where it'd live.** `execute.md` §TRY (portable).

---

### 2 — A diagnosis was committed before the experiment that tested it, and it was wrong `[self-error-doc-could-prevent]`

**Grounding.** Two Krea runs returned byte-identical pictures from different inputs. I concluded "ComfyUI caches by upload name", changed `paint` to upload under a hash, and wrote the cause into the ledger and a code comment. The same identity held under the new name. A three-strength check (plain vs cued source at 0.6, 0.75, 0.9) then showed the real cause: Krea ignores its input at 0.9. The wrong claim reached a commit and the next session's brief (see the header). It also made a discovery finding (F-P25-11, *"cues in the source do not help"*) true for a trivial reason: at 0.9 no input can help. `execute.md` §Verify's ad-hoc row (*"confirm it can fail"*) covers checks, not causes.

**Proposed fix.** `execute.md` §Verify, a row or a clause: *"A cause you name for a surprising result is a hypothesis until a run varies only that cause. Vary the input itself first: if two different inputs give an identical output, the stage ignores its input, whatever else is true."*

**Where it'd live.** `execute.md` §Verify (portable) · a stack fact for the image-model domain: *"Krea 2 Turbo in ComfyUI, 8 steps, simple scheduler: at denoise 0.9 the init latent has no effect (byte-identical output)."*

---

### 3 — Six unlabelled windows opened at once for the lead `[self-error-doc-could-prevent]`

**Grounding.** The lead had asked earlier for full-resolution pictures, not shrunk sheets. At click 1 I opened six full-size view files at once. The lead: *"Please don't fill up my screen with a bunch of images I ahve no context for"*. One labelled side-by-side at 1:1 (four titled columns, one view), opened alone with a sentence on what to judge, was what worked next. `LOCAL_DELTAS.md`'s "artifact a person reaches" row says a sheet is opened with `xdg-open`, and says nothing about how many or with what labels. (Saved to memory; the rule belongs in the tree.)

**Proposed fix.** In that row: *"Show one labelled picture at a time: the views compared side by side at 1:1, each column titled, opened alone, with one sentence on what to judge. A shrunk sheet hides the detail; a batch of unlabelled windows hides the question."*

**Where it'd live.** `LOCAL_DELTAS.md`, the "artifact a person reaches" row (local).

---

### 4 — Second sighting: discovery → execute in one session ran past the ceiling with no reading to act on `[doc-gap]`

**Grounding.** The earlier P25 retro's item 2 (still in the inbox) has the same shape. Pass 2's Brief was written with no meter reading; the first reading (300k) came early in execute, and the run reached ~440k at the sitting. The lead had to say *"carry on research"* to a session already past the 400k ceiling, and it handed to `ML_P25_D3`.

**Proposed fix.** As the earlier item; this is the second sighting.

**Where it'd live.** `discovery.md` §Hand-off, or the context meter (workstation).

---

### 5 — A SHA quoted to the lead from memory was wrong `[self-error-doc-could-prevent]`

**Grounding.** The handback for the size ruling named commit `93f3a4d`; the commit was `c6b890d`, caught only by the next run's tree record. `.claude/CLAUDE.md`'s git table says *"capture your SHA once, by value"*; I wrote the handback before reading the SHA back.

**Proposed fix.** None new: the rule exists. A tally for whether the handback rule should say *"every SHA in a handback is pasted from `git log`, never typed"*.

**Where it'd live.** `_RefinementBacklog.md` tally.

---

## Keep these

- **A premise probe at discovery** (route 5 in minutes on Krea through ComfyUI) turned a four-route question into a measured answer, and the lead's *"VERY interesting test"* followed.
- **A positive control for a new gate** (features drawn at hm08's own places) exposed the lip detector's rim bug before any candidate was scored.
- **Looking at every picture before trusting the gate:** FLUX's second face scored 3.4 mm, and the eye saw it.
- **Offering, then starting the next session at the ceiling** (`claude --bg --name ML_P25_D3`) instead of continuing past 400k.

## Dead weight

None.

## Open questions

1. The Roadmap entry still reads `BRIEF READY` while the phase doc reads `IN EXECUTION` (research and testing). Left for `ML_P25_D3`, which is live on the unit, not fixed from here.
