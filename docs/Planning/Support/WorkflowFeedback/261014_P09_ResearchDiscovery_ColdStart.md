# Workflow Feedback — P09 (the MAP research → Phase09) / research → quick-fix → discovery / cold start

| | |
|---|---|
| **Verb** | `research → quick-fix (stopped at its balloon check) → research → discovery` — one session, 2026-09-29. Not a sanctioned two-verb arc; each verb was lead-named in turn. |
| **Unit** | `260929_R_CharacterMaps.md` (MAP) → `Phase09_HairAndEyeMasters.md` (P09) |
| **Mode** | cold start |
| **Outcome** | done — the MAP research (Passes 1–8, rulings MAP-RD1–RD6), Phase09 seeded, numbered, and its Brief written and pushed (`b84e6cc`). The eye `/quick-fix` was stopped before any change and promoted into the phase. |
| **Shape** | doc-only (plus one disposable probe script and its picture, committed beside the research) |
| **Confidence** | Ran fully: research, discovery (Passes 1–2, the Brief), the quick-fix gate and balloon valve. **Not exercised:** execute (Phase09 was executed and closed by later sessions). |
| **Date** | Run 2026-09-29; deposited 2026-10-14 (the lead's `/retro`, two weeks later). Step 0 had nothing to land: every output of the run is on `origin/main`. |

---

## Items, ranked

### 1 — A ruling given as *"yes 1... and what you say"* was recorded by reference to my prose, and the half I had not stated shelved work the lead wanted `[self-error-doc-could-prevent]`

**Grounding.** I offered three hair options; option 1 read *"contain the exception, invest nothing more"*. The lead answered *"yes 1... and what you say"*. I recorded MAP-RD3 as *"nothing more invested in cards"* and, from that phrase, marked the platform's hair asks (HS-Q1–Q5, Matter-Library#3) **not pursued** — a consequence the lead never saw stated. Two turns later: *"Wiat... I thought we were making an exception to the no picture that fits only one mesh for hair?"* RD3 had to be amended the same day, and four doc sites swept.

**Proposed fix.** When a lead accepts an option **by reference** ("yes 1", "what you say"), the record lists the option's **consequences as bullets, each marked stated-to-the-lead or inferred**, and the handback names every inferred one: *"I read 'yes 1' as also dropping X — say if not."* An inferred consequence that drops scope is a question, not a ruling.

**Where it'd live.** `research.md` §Landing (*a lead DECISION…*) and `discovery.md` §Record a lead ruling in the LEAD'S OWN WORDS — the existing rule covers the quote, not the consequences the quote is taken to carry.

---

### 2 — Research offered a "one sitting `/quick-fix`" without tracing the change against the other writers of the same value `[self-error-doc-could-prevent]`

**Grounding.** The research Status said *"the eye is buildable in one sitting as a `/quick-fix`"*: place a library eye texture by `uv_scale` / `uv_offset`. The lead directed it. The quick-fix's balloon check then found, before any edit: the platform's import already writes `uv_scale` on **every** character mesh (the P18 stopgap), the contract's *"one UV unit = one tile"* rule, and the rig's defaults-only character job. All three were readable at research time; I had read P18 in Pass 1. The valve worked (nothing was built), but the lead spent a directive, and the offer had been wrong.

**Proposed fix.** `research.md`'s *"lead the landing with the one-sitting offer"* gains one check: **before offering a build as a `/quick-fix`, name every other writer of each value it sets, and every contract rule on that value, and say why none conflicts.** A value with a second writer is a contract question, not a quick fix.

**Where it'd live.** `research.md` §Landing (the ⛔ one-sitting rule).

---

### 3 — The lead was confused three times in a row by contract vocabulary I used instead of his model `[doc-gap]`

**Grounding.** Findings came out as "a mesh-supplied map", "fit", "bespoke one-image-one-mesh", "D1". The lead: *"I guess I am confused"* (he holds that only names and parameters travel), then *"OH! no bespoke one image one mesh solutions are possible... what is needeing that?"*, then *"I am confused still... eyes need images to look good.. what ist eh difference?"*. Each round produced a ruling that the next one partly reversed (MAP-RD2, RD3, RD5 were amended within the hour). What resolved it was stating the distinction **in his terms, with his examples**: a library texture any mesh can use, placed by settings, versus a picture painted on one mesh's UVs — with the eye as the case that can be either.

**Proposed fix.** When a finding turns on a contract concept, explain it **first in the lead's own working model** (what travels, what the library holds, what a Creator picks), with one concrete example per side, and only then name the contract term. A finding the lead has to ask about twice is a sign the explanation, not the ruling, is wrong.

**Where it'd live.** `AI_WorkingAgreement.md` §Working With the Lead, or `research.md` §The research discipline — unsure which; the refiner's call.

---

### 4 — Probe output had two artefacts that would have become findings had I not looked at the picture `[self-error-doc-could-prevent]`

**Grounding.** The replace-vs-modulate probe's first sheet cast dark skin tones olive (a per-channel ratio carried the source skin's chroma) and its eye crop ran off the image, with a saturation mask that caught the sclera. Both were visible only in the rendered sheet, not in the printed numbers. Fixed and re-run before citing.

**Proposed fix.** For a visual probe: **open the output image before writing any finding from it**, and record a rejected variant in one line (it saves the next reader repeating it). This run did both; worth keeping explicit.

**Where it'd live.** `research.md` §Disposable probes (*prove the negative* is the nearest rule).

---

## Keep these

- **The quick-fix gate's "the lead already routed it here: proceed, keep the balloon valve armed".** It let me start without a round trip and still stop cleanly at the first contract decision, with nothing to roll back.
- **Inspect the bytes before recommending.** Measuring the nine eye pictures showed eight are one photograph recoloured, which changed the answer to the lead's "separate pictures are higher quality, right?" from a plain yes to a precise one.
- **Discovery's "fetch before the Brief" on a two-machine project.** The Phase06 plan landed mid-discovery; reading it before writing the Brief settled where the Unreal side is built (Phase06 D13) and one-article-per-eye (F-P06-9), and a Roadmap conflict with Phase06's own Active move was caught at rebase. *(Already filed by the P06 retro, `2c52afc`; corroborating, not re-filing.)*
- **The merge-not-rebase row now in `.claude/CLAUDE.md`.** This run rebased a sibling's unpushed retro commit twice to converge `main`, rewriting its SHA each time; the row added since forbids exactly that. *(Absorbed; no new item.)*

## Dead weight

None.

## Open questions

1. **For the lead (housekeeping, not this run's):** the local `main` on this machine is **11 commits ahead of `origin/main`** at deposit time (2026-10-14), none of them this run's. Pushing them is the lead's call.
2. **For the refiner:** item 3 may belong in `AI_WorkingAgreement.md` rather than a verb; it bit during `/research`, but it is about how findings are presented to the lead in any verb.
