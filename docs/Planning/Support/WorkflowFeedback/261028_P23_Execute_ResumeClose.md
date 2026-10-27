# Workflow Feedback — P23 / execute / resume run 3 + close

| | |
|---|---|
| **Verb** | `execute` (resume, then the close in-session on the lead's word) |
| **Unit** | `P23` (Synthetic Skin Sets) |
| **Mode** | `resume run 3, then close` — a separate session from `261027_P23_Execute_Resume.md` (not a continuation); resumed at 23.2.11 from `14db2f9` |
| **Outcome** | `done` — 23.2.11–13 and 23.3 built; click 3 SAT (*"looks good"*); closed (`85ee1ac`), pushed, `matterlib-0.2.0-dev.14` published, the stale `dev.13` draft deleted |
| **Shape** | `behavior-touching` (the skin maker, 12 new articles, 18 maps) |
| **Confidence** | Ran fully: BUILD, TRY (click 3), the close (A⁻ → E), the snapshot publish. **Not exercised:** a Studio sitting (the platform's), row C (no issues). |
| **Date** | 2026-10-28 (the run began 2026-10-27) |

---

## Items, ranked

### 1 — A close recorded a snapshot as published that never left draft; nothing checked the release's state `[doc-gap]`

**Grounding.** Phase22's close (`1974012`) wrote *"the dev snapshot `matterlib-0.2.0-dev.13`"* into its CLOSE row and the Roadmap. At this run's close, `gh release list` showed `dev.13` as **Draft**: 353 of 451 assets uploaded, no tag on the remote, `publishedAt: null`. So every consumer had `dev.12` (2026-10-20) for a week of phases that each believed they had shipped. `build_snapshot.py --publish` creates the release with `gh release create`, which keeps it a draft until every asset is up; an interrupted upload leaves a draft. Found only because this close listed the releases to claim the next id.

**Proposed fix.** In `LOCAL_DELTAS.md`'s publishing-producer row (or `execute_close.md` row E's backing, if the refiner judges it portable: *"a publish is a claim about a remote; read the remote"*): after `--publish`, read `gh release view <tag> --json isDraft,assets` and record `isDraft: false` and the asset count with none un-uploaded, before writing the id into a close. Optionally `build_snapshot.py --publish` could end by asserting the same itself.

**Where it'd live.** `LOCAL_DELTAS.md` (the release-lifecycle / producer row), and possibly `build_snapshot.py` (a tool change, not the refiner's).

---

### 2 — A variation set was batched to the GPU before anyone measured that its members differ `[self-error-doc-could-prevent]`

**Grounding.** 23.3.1 built three skin structures and sent them through the look view, the rig and the thumbnails as one GPU batch (after a 40-minute wait for the GPU). Looking at the click-3 grid before handing it over, the three rows read alike; measured, `Skin2`/`Skin3` moved the face a mean ΔE of 0.6–1.7 from `Skin` against 4–12 between tones, and both moved by the same amount (a noise reseed, not a person). The Brief's §First human test said *"A structure differs in its mottling, sun pattern and regional redness at centimetre scale"*, a place but no size. One rebuild with every lever at strength (the memory `look-work-build-the-full-set`) reached 1.6–2.2. The 18-skin look launch costs ~1.5 min, so the check was cheap from the start.

**Proposed fix.** In `execute.md` §TRY's *"Can the surface show it?"*, or discovery's First human test: *"for a click that judges DIFFERENCE between items (people, variants, a set), state the difference the click needs as a number against a reference step (here: a fraction of a tone step), and measure it on the cheapest render before the batch."*

**Where it'd live.** `execute.md` §TRY or `discovery.md` §First human test; the refiner's call which.

---

### 3 — An equality check twice failed on its own instrument: a per-item clip, then texels that never render `[self-error-doc-could-prevent]`

**Grounding.** The maker measures that every structure renders `Skin`'s colour in the lips' zone (RD-P23-5). First failure (max 3.09 sRGB levels): each structure clipped its brightest 0.1 % at its own peak, and the brightest skin sits beside the lips; the zone was identical in ratio but not after the clip. Second (1.66): the zone included texels past the island's edge, which the bleed grows from outside the zone and which never draw. Each cost a ~4-minute maker run. Same family as `execute.md`'s *"a comparison whose sides cannot differ agrees by construction"*, inverted: sides that differ only in a stage the property does not pass through.

**Proposed fix.** Beside that row: *"An equality check runs over what RENDERS, after every stage that renders it (clip, quantise, bleed), and over nothing else."*

**Where it'd live.** `execute.md` §Verify before edit (the ad-hoc check row).

---

### 4 — `build_snapshot.py --publish` refuses an unbuilt folder, but Phase22's resume block named `--publish` as the one command `[doc-gap]`

**Grounding.** Phase22's Resume (in its closed doc) says *"then `build_snapshot.py --publish`"*. Run that way here, it failed in seconds with *"nothing built … build first"*. It is two runs: `--tag <t>` (build), then `--tag <t> --publish`. Cheap to recover, but the next close will hit it too if it copies the line.

**Proposed fix.** `LOCAL_DELTAS.md`'s producer row names both commands; or the tool's `--publish` builds when the folder is missing.

**Where it'd live.** `LOCAL_DELTAS.md`; possibly the tool.

---

### 5 — The GPU was held by another session's back-to-back benchmarks; asking once and a 3-minutes-idle watcher worked `[doc-gap]`

**Grounding.** At 21:46–22:56 another session ran Unreal `-csvGpuStats` probes back to back (each a fresh process, short gaps). `LOCAL_DELTAS.md` §Two machines says ask once for the batch; the lead chose *"Wait for it"*. A plain `ps` check would have caught a gap between two benchmark runs and launched into the next. What worked: a background until-loop that ends only after `ps -ef | grep "[U]nrealEditor"` is empty for 180 s straight, then the whole batch in one script (10 min).

**Proposed fix.** One line in §Two machines: *"Waiting for the GPU: wait for it to be idle for a few minutes running, not for one empty `ps`; another session's probes come back to back."*

**Where it'd live.** `LOCAL_DELTAS.md` §Two machines.

---

## Keep these

- **The gate caught a real physical fault** (G6: a light tone asked for an albedo of 1.21) before anything was shown; fixing the maker, not the threshold, was the right read.
- **Looking at the sheet yourself before handing it over** (`execute.md` §TRY) stopped a click on near-identical rows.
- **The pre-push read of `origin/main..HEAD`** (`.claude/CLAUDE.md` §Git, the push row) named the sibling commit `bec3056` riding under mine, and the grep of the push range for local paths found an existing practice, not a new leak.
- **`git commit -- <both rename paths>`** after the `git mv`: the index held the pre-finalize blob (row B's trap) and the pathspec commit took the finalized file; verified with `git grep "COMPLETE (closed" HEAD`.
- **Listing the releases to claim the next id** is what surfaced item 1.

## Dead weight

None.

## Open questions

1. **Is `dev.13`'s failure a tool defect?** `gh release create` with ~450 files in one call stopped part-way and the run's exit was evidently not noticed. `dev.14` (478 files, the same call) succeeded. Whether `build_snapshot.py` should upload in batches, as its resume path already does, is a tool question, not the refiner's.
2. **The structures are a complexion, not a face** (the lead: *"looks good"*). If characters need to read as different people at a glance, the lever is the mesh (a body morph), outside this library's skin work. Recorded for whoever orders the next character phase.
