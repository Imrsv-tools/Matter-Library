# Workflow Feedback — AiSkin (SkinMapsFromAnImageModel → OneValidatedSkin) / research / cold start

| | |
|---|---|
| **Verb** | `research` (with a disposable probe, and two lead-directed seeds: Phase24, then Phase25) |
| **Unit** | `SkinMapsFromAnImageModel` (AIS); continued into OMF's `OneValidatedSkin` (OVS) |
| **Mode** | cold start |
| **Outcome** | done: AIS Passes 1–6; a spike proving a whole head skin map from an image model on hm08 (scripts and pictures beside it); OVS Pass 2 and RD-OVS-1 … 6; Phase24 and Phase25 seeded; pushed (`a7bb775`). |
| **Shape** | doc-only in the repo (the probe ran in scratch; its scripts are committed beside the spike doc) |
| **Confidence** | Ran fully: research orient, web audit, the disposable probe (FLUX.2 [klein]), seeding, converging a diverged trunk twice, push by value. **Not exercised:** the Krea 2 arm (no login; scripted only), `/discovery`. |
| **Date** | 2026-11-01 |

---

## Items, ranked

### 1 — "Read the seed at origin" cannot be followed when the seed is in a sibling's clone that is ahead, behind, and dirty at once `[doc-gap]`

**Grounding.** `research.md` §The research discipline says a seed read from a clone is *"read at origin (`git show origin/<branch>:<path>`)"*. This run's seeds were in the platform's documentation clone, in three states at once:
- the named pass (CHQ Pass 21, the first time) was an **uncommitted edit** in the working tree, so it was at no origin;
- the sibling doc (FirstSkinSet) was **committed locally and unpushed**;
- later the clone was **21 ahead and 2 behind**. OMF's review of the pass was on origin only, and the platform's phase seed and its rulings were local only.

Following the rule literally would have read nothing for the first and missed half the update for the third. I read each where it lived (`git diff` for the working tree, `git show HEAD:` for local, `git show origin/main:` for pushed) and wrote in the landing which was which (*"an uncommitted edit, at no origin"*).

**Proposed fix.** *"Read each seed where it lives, and say where: `origin/<branch>` for what is pushed, the clone's `HEAD` for a local commit, the working tree for an uncommitted edit (never stage or touch it). Run `git rev-list --left-right --count HEAD...origin/<branch>` first. A diverged clone can hold one part of the update on each side."*

**Where it'd live.** `research.md` §The research discipline (the *seeds decay* bullet). Portable.

---

### 2 — Numbering and seeding from research: the lead's words that number a phase may come from another session and another repo `[doc-gap]`

**Grounding.** `research.md` §Landing seeds a numbered phase *"when the lead says 'seed Phase `<NN>`'"*. Phase24 was numbered from a combination of sources:
- the lead's words recorded in OMF's input (*"today's hm08, Matter Library hosts it … it will seed the phase"*);
- the platform's phase doc (*"Matter will Seed its Phase 24"*, read in that clone);
- here, *"what is the next pahse number"* then *"lets come up with a plan"*.

None of them is the literal phrase. I seeded and said so in the Status line. The lead then answered the seed's questions and said *"Split and seed"*, which was literal for Phase25. It worked, but it was a judgement the doc does not cover, and *"lets come up with a plan"* sits close to the commitment line (*"never slide into `/plan`"*). I kept the seed's plan at click level (steps that each end in the lead's look, no file targets) and named the hand-off to `/discovery`.

**Proposed fix.** In §Landing: *"The numbering act may arrive in the lead's words in a consumer's or producer's session (a quoted 'this library seeds Phase N'). Quote it in the seed's Status line with where it was said. 'Plan it' asked inside research means a seed whose plan is phases and clicks, never steps with file targets. Name `/discovery` as the next verb."*

**Where it'd live.** `research.md` §Landing (seeded phases). Probably portable.

---

### 3 — A side-by-side strip misread as misalignment; an overlay showed it was aligned `[self-error-doc-could-prevent]`

**Grounding.** After the first generation, I compared renders and generated views as a strip of separately framed thumbnails. I told the lead the front view *"moved the features"*. A 50 % overlay of the same two pictures showed eyes, nose, mouth and ears on hm08's own, so I had misread it. I corrected it in the next message, but a claim had already gone to the lead on a picture that could not answer the question.

**Proposed fix.** A learning: *"Alignment between two pictures is judged by an overlay or a difference, never by a side-by-side. A side-by-side answers 'which looks better', not 'where is it'."*

**Where it'd live.** `docs/Learnings/` (a rig or probe domain). It is the inverse of backlog row 108 (*a probe's printed numbers hid two artefacts its picture showed*). Possibly `execute.md` §Verify's instrument rows.

---

### 4 — The probe's load was priced in the doc before the lead's go; I treated that plus *"I want to prove the concept"* as the go `[doc-gap]`

**Grounding.** `research.md` §Disposable probes: *"'Run the probe' is consent to the question, not to any load."* The load had already been put to the lead in Q-AIS-4 (*"~16 GB download, minutes on the 24 GB GPU … on your go"*). The lead's answer was *"I want to prove the concept"*, not *"run the probe"*. I ran FLUX (16 GB, the priced load) and wrote the Krea arm without downloading it (36 GB, not priced before), asking for the login instead. It held up, but the rule does not say whether a priced question answered with intent counts as the go.

**Proposed fix.** *"A load you priced in the question, answered with the lead's intent to proceed, is consented. A bigger load found after (a second model, a larger download) is priced again before it runs."*

**Where it'd live.** `research.md` §Disposable probes (*Price a heavy step*).

---

## Keep these

- **The round-trip check before the real run.** Baking today's own renders back reproduced today's map to 0.65 % (p95). So when the generated faces came back, the projection was not a suspect, and only the model's output was judged.
- **Reproduction committed beside the result doc, machine paths stripped.** The scripts were copied out of scratch with `REPO` derived from `__file__` and `OUT` from an env var, then re-run from their new location to prove it. The public-repo rule and the *reproduction must survive the box* rule were both satisfied.
- **Quoting the ruling's own words found that the spec's consent sentence is a finding, not a ruling.** RD-SKM-2's words are *"1b or c I want to explore that option"*. The *"rights and consent"* text came from F-MP-19, a finding. That changed Q-AIS-2 from a conflict to new ground.
- **`.claude/CLAUDE.md` §Git's diverged-trunk row and push-by-value.** Two merges with disjoint paths and an empty index, then `git log origin/main..HEAD` read line by line, then `git push origin <sha>:refs/heads/main`.

## Dead weight

None.

## Open questions

1. **The platform's character-quality doc owes a back-link to this library's AIS doc and spike** (its 2026-11-01 pass names the image-model question). It is the platform's doc, held by another session's edits, so not touched. *(For the lead or the platform's next session; not a Refiner item.)*
2. **Is `RD-OVS-n` right for rulings landed in a doc whose author declared ids as `OVS-n` / `OVS-Qn`?** I minted `RD-OVS-` for the lead's answers in its `## Resolved`, following `NamingConventions.md`'s `RD-` shape. OMF's findings stay `OVS-n`. *(Refiner: is a mixed mnemonic in one doc fine?)*
