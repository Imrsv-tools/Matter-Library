# Workflow Feedback — P25 / discovery / Pass 3 (ears and prompt)

| | |
|---|---|
| **Verb** | `discovery` |
| **Unit** | `P25` |
| **Mode** | resume run (`ML_P25_D4`; Pass 3 continued from `ML_P25_D3`'s hand-off). **Not a continuation** of `261101_P25_Discovery_Pass3.md` (that is `ML_P25_D3`'s run); a distinct run on the same unit and day, hence the `Pass3Ears` mode. |
| **Outcome** | done — the ears found by silhouette (F-P25-21), projected through the profile camera (F-P25-22, RD-P25-17), then ruled a colour gradient on OMF's finer ear (RD-P25-18); the middle prompt measured (F-P25-24); the hand-off rewritten; `ML_P25_D5` started on it. |
| **Shape** | doc-only in the tracked tree (the phase doc, probe scripts beside it); every picture git-ignored |
| **Confidence** | Ran fully: the discovery read, probes, look-view launches, ComfyUI generation, the phase-doc commits, a cross-session reply. **Not exercised:** a Brief rewrite (the phase is research-mode; only a supersession banner was added), `run_all.py` (no tool under `tools/` changed). |
| **Date** | 2026-11-01 |

---

## Items, ranked

### 1 — Five matchers built before looking at the target in the space I was fitting in `[self-error-doc-could-prevent]`

**Grounding.** The hand-off asked for a shape-based ear finder. I built and ran, in turn, an appearance correlation on hm08's side-lit shading in UV, the same on its depth, a fixed-template variant, an aspect-search variant, and an outline (chamfer) match — each failing on the check picture — before I carried hm08's profile render into the island frame and looked. That one picture showed the premise was wrong: the ear pad holds the ear's front **and** back, the front squeezed narrow (F-P25-21). Every earlier matcher was fitting to the wrong target. Later the same pattern cost a smaller loop: I took the ear's "front" from the mesh's normals before checking what it selected (it took the back too).

**Proposed fix.** One sentence where fitting work starts: *"Before fitting a picture to a region of the mesh, carry the mesh's own view of that region into the space you fit in (render → frame), and look at it — the fit's target is a measurement, not an assumption."*

**Where it'd live.** A `docs/Learnings/` entry for the image-to-mesh fitting this phase is building (no domain fits yet — the refiner's call), or `discovery.md` §"Confirmed" requires the confirming artifact.

---

### 2 — A research-mode phase has no document shape; findings pile under a Brief that never converges `[doc-gap]`

**Grounding.** The lead made Pass 3 *"research and testing until the result is great"*. `discovery.md` assumes a Brief that converges; this phase instead grows a numbered findings list (F-P25-13 … 24 now, the doc ~90 KB) under a Brief that still described the rejected route — `ML_P25_D3` filed that as its item 1, and I discharged it with a supersession banner at `0d3c8a8` rather than a rewrite. The route changed four times in this one session (pad fit → silhouette fit → profile projection → gradient), and the only current-state summary is the hand-off's "Next, in order", rewritten by hand at the close.

**Proposed fix.** A named mode in `discovery.md`: when the lead declares a phase research-and-testing, the doc carries (a) one **"Current route"** box at the top, replaced (not appended) at every ruling, naming the RD ids in force and those superseded, and (b) the findings list below it; the Brief is written only when a route is built.

**Where it'd live.** `discovery.md` (portable: any project can have a lead-declared exploratory phase).

---

### 3 — The flat-colour render is the instrument that separates the mesh from the map `[doc-gap]`

**Grounding.** The lead could not tell *"a shadow or the mapping not on the ear"*. Rendering the same view with one constant skin colour answered it in one launch: the mesh shows almost no ear, so everything read as ear structure is painted; and it showed a pink patch above the ear was not the colour map at all (it appeared on the flat render too) — a defect I had been about to "fix" in the field.

**Proposed fix.** In `execute.md` §TRY (or the look-judging learnings): *"When a look defect could be the geometry's shading or the map's colour, render the map as one flat colour beside it before changing either."*

**Where it'd live.** `docs/Learnings/` (the look-judging domain), or `execute.md` §TRY.

---

## Keep these

- **The lead's one-labelled-picture rule, applied as one labelled native-pixel composite per question** (crops side by side, each labelled) — the lead judged each in one look and ruled four times this session.
- **Cross-session messaging for a peer's correction:** `ML_P25_D3`'s note arrived mid-run, was applied at the next edit of the doc, and answered by `SendMessage` naming the commit.
- **Recording the lead verbatim with a separate *"Read as"*:** the gradient proposal arrived as a question (*"thoughts?"*) and was recorded as not ruled until *"yes, gradient route"*.
- **The `ps -ef | grep "[U]nrealEditor"` check before each look-view launch** caught a platform `-nullrhi` run; generation (ComfyUI only) went ahead, the launch waited for it to exit.

## Dead weight

none

## Open questions

- Is "one camera per region with its own geometry, matched by shape, carried by the mesh's UV" (F-P25-23's pipeline lesson; RD-P25-15, -17) now a library pattern worth a spec line in `docs/specs/`, or does it stay phase-local until the body islands test it?
- No channel exists from this library to OMF (the Deferred row says so); whether OMF asks belong in `PlatformDependencies.md` under a new section is a lead or refiner call.
