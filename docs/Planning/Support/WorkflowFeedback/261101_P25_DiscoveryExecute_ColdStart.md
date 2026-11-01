# Workflow Feedback — P25 / discovery → execute / cold start

| | |
|---|---|
| **Verb** | `discovery` (Pass 1, Brief ready) **then** `execute` (25.1, in the same session, on the lead's `/execute Phase25`) |
| **Unit** | `P25` |
| **Mode** | cold start (one session, both verbs) |
| **Outcome** | `derailed` (premise rejected at the sitting): the Brief landed (`b52fe46`, `3df2ce1`); 25.1 built the project-and-bake route and was shown twice. Second verdict: *"you are cuting pasting, patching, matching, blending, when I think we should be trying to figure out how it can generate a full map"*. Four routes recorded in the phase doc (`28b3c02`); `ML_P25_D2` started on `/discovery Phase25`. |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: discovery Pass 1, execute stages 2–3 (build, two sittings). **Not exercised:** STRENGTHEN beyond the fixes, the close, `/plan`. |
| **Date** | `2026-11-01` |

Not a continuation of another file.

---

## Items, ranked

### 1 — The Brief inherited the spike's METHOD as the phase's route, and the lead rejected the method two sittings and ~2 h of build later `[self-error-doc-could-prevent]`

**Grounding.** The seed and the spike proved one route (render the head, have the model repaint each view, project the pictures back). The Brief took it as given: the reuse check said *"the projection exists as the spike's scripts … it moves into tools/"*, and no line asked whether the lead's claim (RD-AIS-2, *"prove … these system can generate really good looking skinmaps"*) was about that route or about whole maps however made. Execute built it at 8K with masks, a gate, fills and a neck match; each fix to a stitching defect was itself stitching. The lead at the second showing: *"this is still comeing too much from 'Let's make a 3D model have a realistic skin' and not 'figure out how to wrap a realistc skin on a 3D model'"*, and named two routes (an edit LoRA; painting onto a 3D object inside ComfyUI) that discovery never listed. The spike's own doc had flagged seams as open (F-AIS-13); the Brief treated them as fixes, not as a property of the route.

**Proposed fix.** In `discovery.md` §The Brief, beside the reuse check: *"When the Outcome is a claim to prove ('show X can be done') and the seed carries a method from a spike, list the candidate routes in one line each and say why this one. A spike's route is a hypothesis about the method, not the method. Where the spike's open defects are properties of the route (seams from stitching), name that as the route's risk in the First human test."*

**Where it'd live.** `discovery.md` §The Brief (portable).

---

### 2 — Discovery's "past ~250k, execute runs fresh" had no reading to act on: the context meter's first reading is at 300k `[doc-gap]`

**Grounding.** `discovery.md` §Hand-off: *"Past about 250k of context at BRIEF READY, that verb runs in a FRESH session: say the reading and offer to start it."* This session wrote BRIEF READY with no reading in hand (the meter, `~/.claude/hooks/context_meter.py`, prints its first plain reading at 300k); the lead typed `/execute Phase25` here, the first reading arrived at ~307k on execute's first tool call, and 25.1 ran to ~465k. Both sittings and every fix landed past the 450k judgment band.

**Proposed fix.** Either the meter reads from 200k (`LOCAL_DELTAS`/workstation), or `discovery.md` says how to tell without one: *"No reading below the meter's first? Count the large reads (each research doc, each 30 KB+ command doc) — two research docs, a closed phase and three command docs is past 250k."*

**Where it'd live.** `discovery.md` §Hand-off, or the context meter's first band (workstation; unsure which is the Refiner's).

---

### 3 — A probe's prompt went into a shipped tool unread, and it asked for the CG look the lead rejected `[self-error-doc-could-prevent]`

**Grounding.** `gen_views_model.py` carried the spike's prompt words: *"photorealistic human skin"*, *"matte skin with no shine"*, *"like a cross-polarised flat scan"*. The lead at the first showing: *"ths looks like a 3d animation skin... did you say that? if you did... don't... We want a human skin"*. The prompt did not say 3D, but those three phrases pull toward a render and a retouched face; replaced by *"raw documentary photograph … unretouched … no retouching, no airbrushing … not a 3D render, not CGI"*, the front view showed pores and uneven tone at the same strength (25.1.7).

**Proposed fix.** A learning, first sighting: *"For a real-skin picture from an image model, 'photorealistic' and 'flat/matte/no shine' pull toward CG and retouching; ask for an unretouched photograph and name what to exclude."* Tally; promote on a second sighting.

**Where it'd live.** `_RefinementBacklog.md` stack-facts tally (a future `docs/Learnings/` image-model domain).

---

### 4 — On the machine with Unreal, ComfyUI now shares the GPU too, and its idle models block an 8K look view `[doc-gap]`

**Grounding.** `LOCAL_DELTAS.md` §Two machines: *"The machine with Unreal shares its GPU with the lead's other Unreal work. Before any launch: `ps -ef | grep "[U]nrealEditor"`."* The lead's ComfyUI (installed 2026-11-01, not this run's) held 16 of 24 GB with models cached between runs; the 8K judge needs ~7 GB. `POST /free {"unload_models": true, "free_memory": true}` released it without stopping the server (they reload on the next request); `nvidia-smi` took a few seconds to show the drop (13.6 GB, then 1.7 GB).

**Proposed fix.** Add to the GPU line: *"and ComfyUI (port 8188): before an Unreal launch, `POST /free` with `unload_models` unloads its cached models without stopping the server; read `nvidia-smi` again after a few seconds."*

**Where it'd live.** `LOCAL_DELTAS.md` §Two machines (local).

---

### 5 — Stack facts, single sightings each `[doc-gap]`

- **Krea 2 Turbo img2img (ComfyUI, KSampler denoise)** keeps hm08's features only up to ~0.5; 0.65 doubles the ears' edge, 0.8 moves the eyes. **FLUX.2 [klein] 4B edit** reframes a close-up as a whole head (silhouette overlap 0.71–0.94) and drifts features at side views.
- **A silhouette-overlap gate needs its background from the render's own mask,** not the picture's border: a frame-filling close-up put skin on the border and false-skipped two good views (0.64, 0.20 → 0.999 once fixed).
- **The project environment has no SciPy;** the spike's scripts used it. `gsm.blur` (three box passes) and cumulative-sum boxes cover dilation, erosion and the feather.

**Proposed fix.** Tally; promote on a second sighting.

**Where it'd live.** `_RefinementBacklog.md` stack-facts tally.

---

## Keep these

- **Stopping on a verdict that rejects the premise** (`execute.md` §TRY: *"A verdict that rejects the step's premise ends the act"*): recorded verbatim, 25.2/25.3 named as reached, no third round of patches.
- **"A reading that disagrees with the picture indicts the instrument":** the gate skipped two Krea close-ups that looked aligned; the instrument was wrong (item 5).
- **Looking at every sheet before the showing:** the broken FLUX column (a second face stamped on the cheek) and the eye ring were caught by the agent before the lead, and FLUX never reached a sitting.
- **Cross-session messaging at discovery:** the AIModels session answered where the models were and in what form, which moved the generation step to ComfyUI before execute.

## Dead weight

None.

## Open questions

1. **A wrong-session message from the lead** (a Studio UI request) arrived mid-run; answered by naming the live Studio sessions, nothing done. No item: handled by the existing rules.
2. **Whether 25.1's tools stay** (`project_views.py`, `gen_views_model.py`, `look.py --candidate`) is the re-discovery's call; the judge column and the generation script are route-independent, the bake is not.
