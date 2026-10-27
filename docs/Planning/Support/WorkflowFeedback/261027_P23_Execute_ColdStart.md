# Workflow Feedback — P23 / execute / cold start

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P23` (Synthetic Skin Sets) |
| **Mode** | `cold start`, ending in a suspend-handoff |
| **Outcome** | `suspended` — 23.1 done and click 1 sat (colour is the lever); 23.2's maker built (`ba64b45`), but click 2 was not sat (*"We are certainly not at the "bar (c), III" level... also this is taking too long"*). Suspended at 23.2 (`94228f2`). |
| **Shape** | `behavior-touching` (the skin maker, the skin model's table, `look.py`, twelve articles) |
| **Confidence** | Ran fully: BUILD, TRY (two clicks), the divergence row for a failed decided premise (asked once), and the suspend ledger. **Not exercised:** the close, the rig's three-tool sheet (never run this session), 23.3. |
| **Date** | 2026-10-27 |

---

## Items, ranked

### 1 — A measured statistic matched to the reference was treated as the target, and two lever rounds read worse than the build they replaced `[self-error-doc-could-prevent]`

**Grounding.** After click 2 (*"not at the bar (c) level"*) I measured the bar's face in log band-pass (2–10 mm, 1–3 cm, redness). Then I drove noise-based levers until III's numbers matched: 0.037 / 0.053 / 0.054 against the bar's 0.037 / 0.052 / 0.072. Both rounds read worse at the look view (reddish-brown blotches; the cheek flush a dark, hard-edged patch). I caught it by eye each time and reverted (23.2.6). The bar's regional colour is anatomically placed and smooth. A band-pass number measures *how much*, never *where* or *what shape*, so noise can match it and look nothing like it. The same thing happened earlier in 23.2.3: the first texture build matched the bar's fine band and read "blotchy and brown". So the trap fired three times in one session, about 45 minutes of render loops.

**Proposed fix.** One sentence in the look-work guidance: *"A statistic matched to a reference is a hypothesis about the look, not the look. When a number says 'at the bar' and the crop beside the bar says otherwise, the crop wins: change WHAT the lever builds (where, what shape), not how strong it is."* And a measurement rule: compare region by region against the reference's **same** region (its nose, its under-eye, its cheek), not a whole-face spread.

**Where it'd live.** Memory `look-work-build-the-full-set` (it says "build every lever at strength, measure, then show", which is what pushed toward a number). Possibly `execute.md` §Verify, the ad-hoc-check / comparison row: *"a comparison whose sides cannot differ"* has a sibling here, *"a comparison whose metric cannot see the difference"*.

---

### 2 — The click's surface was used as the tuning loop; the lead had to say "this is taking too long" before it narrowed `[self-error-doc-could-prevent]`

**Grounding.** The Brief's click 2 named six tones, today beside new, plus the rig. I re-ran the whole surface on every lever change: the maker (~2 min), twelve articles, six look launches (~15 min), the composite. The lead: *"this is taking too long, stop doing shades I. II. VI"*. One launch with `look.py <III> --also <IV> --also <V> --reference …` was available all along (~6 min). `execute.md` §BUILD already says to re-ask the fastest loop *"the moment the loop changes character"*. Here it changed from building the maker to tuning a look, and I did not re-ask.

**Proposed fix.** In discovery's First human test, or `execute.md` §BUILD: *"The sheet the lead judges is not the loop you tune on. While tuning a look, render the fewest subjects that show the change, in one launch (here: one tone per fit and the reference), and render the full click surface once, when the build is ready."*

**Where it'd live.** `execute.md` §BUILD (the re-ask paragraph). Maybe `discovery.md` First human test, so a Brief names the tuning loop beside the click.

---

### 3 — Discovery decided a pass/fail branch on a premise it could have measured in ten minutes `[doc-gap]`

**Grounding.** RD-P23-3 decided *"the refit passes when … within 15 %"* and a fallback if it fails. Discovery probed only the model's defaults (F-P23-1). The refit itself (a vectorised search over two parameters, 23.2.1) took about ten minutes and failed at four of six tones, VI under every setting. The decided fallback (today's colour at the failing tones) then broke the Outcome's *"one set of pigment maps"*. So the run had to ask the lead mid-execute, and his answer was a third option no doc had written.

**Proposed fix.** In discovery: *"A decision whose pass/fail branch rests on a measurement that takes minutes is measured at discovery, and the decision records the result, not a conditional."*

**Where it'd live.** `discovery.md` (decisions / probing).

---

### 4 — `look.py --today <rev>` drew a re-made picture under the old article's constant `[doc-gap]`

**Grounding.** The Brief's build map for 23.2 named `look.py Skin_Fitzpatrick<Tone> --today 4398f05`. 23.2 re-makes the maps in place, under the same names. `today_article` named today's pictures by absolute path into the working tree, so today's column would have drawn the new map under the old constant. That is a "today" that never existed. It was caught before rendering and fixed in the tool (`ba64b45`): pictures changed since the revision are read from the local LFS store.

**Proposed fix.** None owed in the method: the tool is fixed. A Learnings line for the class: *"a before/after view must take every input as it stood at 'before', including pictures under LFS, or a re-made-in-place file silently joins the 'before' side."*

**Where it'd live.** `docs/Learnings/` (Tooling or Blender/Unreal parity).

---

### 5 — The look view cannot render at `--width 2048`: Unreal asks Vulkan for one 4 GiB block `[doc-gap]`

**Grounding.** The Brief set `--width 2048` for click 1. The look view supersamples ×2, so it captures at 4096², and the runtime dies with `VulkanMemory.cpp … Out Of Memory, trying to allocate 4294967296 bytes` on the RTX 4090. That is a single-allocation limit, not exhaustion: 1.9 GB of 24 was in use. `--width 1536` (a 3072 capture) works.

**Proposed fix.** A Learnings entry under Unreal, and a guard in `look.py`: refuse `width × SUPERSAMPLE > 3072` by name, saying why.

**Where it'd live.** `docs/Learnings/Unreal/`; the guard is a tool change for a phase or quick-fix.

---

## Keep these

- **Click 1 as a premise test** (the Brief's RD-P23-1, `look.py --reference`): it answered "colour is the lever" in about 45 minutes, before any maker was rebuilt.
- **The agent looking at the crop beside the reference before calling a click** (§TRY's "look at that exact view before you hand it over"): it kept three bad builds from the lead.
- **Asking once for a Brief-routed fork, with a recommendation** (AskUserQuestion, three options): one answer, no meeting.
- **RD-P23-10's rule (the private reference's path never in a tracked file), checked by a grep of the diff before each commit.**
- **Reverting an unshown experiment to the last commit, with its diff kept outside the tree and the diagnosis in the ledger**: the tree stayed honest for the next session.

## Dead weight

None.

## Open questions

1. **Lead decision — what is the bar for this phase?** The bar's look comes from placed regional colour (nose, under-eye, cheeks, freckles). That may be a placed-region maker, close to *Skin Layers*' "marks as placed layers". Does P23 build placed face regions, or does it close on the pigment base and hand regions to *Skin Layers*?
2. **For the next `/execute P23` — the Brief's click 2 judge line** *"redness must fall from I to VI"* cannot hold under the lead's borrowed response: redness is equal within each fit group (measured 1.11 vs 1.13). The next run should restate that line against the borrowed design, or put it to the lead.
