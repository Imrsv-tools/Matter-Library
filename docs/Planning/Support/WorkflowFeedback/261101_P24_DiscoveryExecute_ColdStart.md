# Workflow Feedback — P24 / discovery → execute / cold start

| | |
|---|---|
| **Verb** | `discovery → execute` (one session: discovery Pass 1, then `/execute Phase24` on the lead's word in the same window) |
| **Unit** | `P24` |
| **Mode** | `cold start`, ending in a suspend-handoff (execute suspended at 24.2 at ~380k context; `ML_P24_E1` started on the lead's yes) |
| **Outcome** | `suspended` — Brief committed (`91f5eb9`); 24.1 built and click 1 sat (*"A reads real, B reads fake"*, `22588a5`); 24.2.1–24.2.2 landed (`557811a`); the 8K composer and click 2 owed |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: discovery Pass 1, execute 24.1 and the start of 24.2. **Not exercised:** the close, any push, click 2/3. |
| **Date** | `2026-11-01` |

Not a continuation: no earlier retro for this run.

---

## Items, ranked

### 1 — Discovery and execute in one session left execute ~300k of context in hand; it suspended before the second click `[doc-gap]`

**Grounding.** Discovery Pass 1 ended near 300k (the context meter's first reading fired during it). The lead's next message was `/execute Phase24` in the same window. Execute built the judge and sat click 1 by ~330k, then hit the 8K memory problem (24.2.3) and had to suspend at ~370–380k with the core of 24.2 unbuilt. The `/retro` step 0 then started a fresh `ML_P24_E1`, which is what should have happened at the Brief.

**Proposed fix.** In `discovery.md` §Hand-off: *"If this session's context is past ~250k at BRIEF READY, the ▶ is a FRESH session (`claude --bg --name <namer --next> "/execute …"`), offered as `/retro` step 0 offers it — execute's first sittings need the budget more than discovery's reading does."*

**Where it'd live.** `discovery.md` §Hand-off (portable).

---

### 2 — The machine's hardware went into a public phase doc draft; caught by re-reading, not by a rule I was holding `[self-error-doc-could-prevent]`

**Grounding.** The Brief's "Measured at" line first read *"an RTX 4090 with 24 GB; 61 GB of RAM, 32 cores"*, and RD-P24-7 and F-P24-4 quoted the RAM and GPU memory. `.claude/CLAUDE.md` names hardware as a private fact, but the phase-doc header shape copied from Phase23 (*"Measured at … on the machine with Unreal (…)"*) invites listing what the machine is. Removed before the commit by a deliberate re-read; a sizing decision (RD-P24-7) genuinely needed *how much* memory, so the wording became relative ("about a third of the box's memory").

**Proposed fix.** Where `LOCAL_DELTAS.md` §Two machines says to name a machine by its role, add: *"…and size by proportion, never by its parts: 'a third of the box's memory', not a GB figure or a GPU model. The repo is public."*

**Where it'd live.** `LOCAL_DELTAS.md` §Two machines (local), or `.claude/CLAUDE.md`'s PUBLIC line.

---

### 3 — A float32 mean over 16M texels drifted ~7 % and passed silently `[self-error-doc-could-prevent]`

**Grounding.** `bar_maps.py`'s first run held the bar's colour to its tone with `col[face].mean(0)` on float32; the check it printed (rendered face mean) came back 0.527 / 0.295 / 0.182 against a tone of 0.513 / 0.274 / 0.186. Only the self-check line exposed it. The axis-0 reduction over an (M, 3) array does not get NumPy's pairwise summation. Fixed with `mean(0, dtype=np.float64)` (`22588a5`).

**Proposed fix.** A learning: *"Any mean over a large float32 array, especially along axis 0 of an (M, k) array, takes `dtype=np.float64`; at 8K a float32 mean is off by percent, not by rounding. Print the check that would show it."* Its domain is new (Python/NumPy tooling); the maker moving to float32 above 2048 (24.2.2) makes it live for the next session.

**Where it'd live.** `docs/Learnings/` — a new domain, or `MaterialX.md` if the refiner prefers no new domain.

---

### 4 — The Brief's "one lens" for every view could not show 8K at the close-ups; the fix was found at build `[doc-gap]`

**Grounding.** RD-P24-4 said *"one lens for all of them"* and the "can the surface show it" line claimed 0.04 mm a pixel at the eye close-up. Building it: the eye at 40 cm through the rig's 50 mm lens spans ~0.29 m of frame, ~0.19 mm a pixel, coarser than an 8K texel. Execute made the close-ups "the 40 cm view magnified" (same position, narrower view), which keeps one perspective. The discovery check had done the arithmetic on the framing it wanted, not on the lens it fixed.

**Proposed fix.** In `discovery.md`'s *CAN THE SURFACE SHOW IT* clause: *"Do the arithmetic from the camera you fixed (position, lens, pixels), not from the framing you want."*

**Where it'd live.** `discovery.md` First human test (portable).

---

### 5 — Phase23's "the bar is paler than any tone" was a reading of a multiplier picture; caught by reading the picture's compose record `[doc-gap]`

**Grounding.** F-P23-2 averaged the composed picture and called the bar paler and less red than any tone. The picture's compose record shows it is the bar's albedo divided by the platform's skin at the time. The bar's own albedo sits between III and IV, and it fits IV's skin response, not III's (24.2.4). The rule *"a fixture's state is READ from its data, never inferred from its name"* exists; this is its picture-level twin: a picture's meaning is read from how it was made.

**Proposed fix.** Extend that sentence: *"…nor from its pixels alone: read how a picture was made (its compose or bake record) before measuring it."*

**Where it'd live.** `discovery.md` First human test (portable).

---

## Keep these

- **Probing the maker's cost at discovery** (F-P24-2): the ×16 estimate from 2048 matched the 4096 measurement (12.4 GB), so 24.2 did not waste a run finding the wall.
- **Reading the control's code for the lane check** (G8's `picture_errors`, the runtime's `LoadTexture`): both produced build-map facts (the size rule's shape; one 8K picture ≈ 0.7 GB of GPU memory).
- **Proving byte-identity at 2048 in-process** before committing a maker change: no regenerated pictures, no LFS churn (Learnings G2's trap avoided rather than cleaned up).
- **The ruler first:** click 1 took one launch, and it fixed the views before any candidate existed.

## Dead weight

None.

## Open questions

1. **For the live `ML_P24_E1` run (it owns `Phase24_OneValidatedSkin.md`; not landed here):** two features of the bar seen at click 1 that click 2 must not read as gaps in C: **a pale patch inside A's left nostril, and a faint rectangle just under A's left eye** (both in the bar's own pictures), plus the bright line between the lips in every column (the mouth mesh). Suggested home: the 24.1.2 ledger row.
2. **Lead's, not the refiner's:** after Phase24 the Roadmap runs *Eyes in the Shader* before *Skin Layers*; the OVS research's Pass 2 had proposed *Skin Layers* on this subject first. Raised in chat; the lead has not ruled.
