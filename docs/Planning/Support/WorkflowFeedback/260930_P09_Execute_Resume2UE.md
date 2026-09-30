# Workflow Feedback — P09 / execute / resume run 2 (the UE machine)

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P09` (step 9.3) |
| **Mode** | resume run 2, on the UE machine (run 1 was the library machine) |
| **Outcome** | done for 9.3 — the Unreal masters take `base_color_map`, the white Unreal eye fixed on Subsurface, the Eye spike failed and the lead kept Subsurface, `unreal-runtime-v2` published and pinned (`6f73780`, `6122d63`, pushed). Click 5 and the close remain, on the library machine. |
| **Shape** | behavior-touching |
| **Confidence** | Ran fully: pull, build (editor target, masters commandlet, package), editor-mode and packaged renders, the spike, commit, push, publish. **Not exercised:** click 5 on the library machine (the v2 download there), the close. |
| **Date** | 2026-09-30 |

Step 0: every in-chat finding is on disk — the lead's ruling and the Studio hand-off addition in the phase doc's Resume
block and 9.3 row; U11 and U12 in `docs/Learnings/Unreal/Unreal.md`; the two process findings that lived only in chat
or a commit message are items 2 and 3 below.

---

## Items, ranked

### 1 — A new shape of data reaching an engine input can hang the GPU, and the "is it new?" check is the kernel log `[doc-gap]`

**Grounding.** 9.3 multiplied a texture into Unreal's `subsurface_color` for the first time (before, it was always an
article constant). The first render lost the device (`VK_ERROR_DEVICE_LOST`; the kernel's Xid 109 + 31 from
UnrealEditor; breadcrumbs in `SubsurfaceScattering`) — the eye picture's black pupil texel made the scatter colour
exactly 0. What classified it quickly was `journalctl -k | grep -i xid` since Phase06's start: **no Xid in any Phase06
editor run**, so the fault was new, not the box; then a one-variable bisect (a `1e-4` floor, the job otherwise identical)
rendered clean. This is `execute.md`'s "a shape many tools parse" row (a value range no earlier instance had), but the
"reader" was a GPU pass, and the failure mode — a hang on a shared desktop with a freeze history — is harsher than any
the row imagines. Nothing in the carried docs says where to look after a device loss.

**Proposed fix.** For this project's Unreal work: *"After a `VK_ERROR_DEVICE_LOST`, read `journalctl -k | grep -i xid`
back to the last known-good Unreal run before relaunching; a new Xid is your change until a one-variable bisect says
otherwise. A master input that can now be driven by a texture (black texels, 0) needs the range it can reach checked
against what the engine pass assumes."* U11 records the specific floor.

**Where it'd live.** `LOCAL_DELTAS.md` (the RUN row, Unreal side) or `docs/Learnings/Unreal/` (U11 exists; the method
half is the refiner's call).

---

### 2 — The gate of record reads differently per machine, and nothing says so `[doc-gap]`

**Grounding.** `run_all.py` on the UE machine: 14 PASS, **0 SKIP, 3 FAIL** (`approval_binds_freeze`, `release_verify`,
`activation`). Run 1's commits on the library machine: 14 PASS, 2 SKIP, 1 FAIL. The two extra reds read this box's local,
untracked `library/staging/matterlib-0.1.0/` (`.dds` files the frozen record does not list, a `matterlib-PRIOR`
selector); the other machine SKIPs those lanes. I had to establish the attribution from the lane output (no release
path in my diff) — `execute.md`'s "whose defect is this? is a measurement" row, done by hand because no baseline per
machine exists. The attribution now lives only in `6f73780`'s message.

**Proposed fix.** Record the per-machine baseline: *"On the UE machine `release_verify` and `activation` run (local
staging residue) and fail; on the library machine they SKIP. Compare the SET per machine."* Or clean the residue (a
lead call: it may be a deliberate local test tree).

**Where it'd live.** `LOCAL_DELTAS.md` (the RUN row) / `docs/ToolingConventions.md` §Gates; the residue itself is an
Open question.

---

### 3 — `unreal/build.sh` and `publish.sh` are not executable, though their headers say to run them bare `[doc-gap]`

**Grounding.** `UE=… unreal/build.sh editor` → `permission denied`, exit 126 (both files are tracked `100644`). Re-issued
as `bash unreal/build.sh editor`. The headers' usage lines (`unreal/build.sh [editor|masters|package|all]`,
`unreal/publish.sh N`) and the phase's step list name the bare form.

**Proposed fix.** `git update-index --chmod=+x` on both (a `/quick-fix`), or make the usage lines say `bash unreal/…`.

**Where it'd live.** A `/quick-fix` on `unreal/` (not methodology).

---

### 4 — The masters commandlet's own result lines are not on its stdout `[self-error-doc-could-prevent]`

**Grounding.** `build_masters.py` logs `MATTER built …` / `RESULT ok` with `unreal.log` (Log verbosity), which
`-stdout` did not show; a grep of the task output found 0 `RESULT ok` and read like a failure until I found them in
`unreal/MatterRuntime/Saved/Logs/MatterRuntime.log`. The spike script used `unreal.log_warning` and its lines showed.

**Proposed fix.** `build_masters.py` `log()` → `unreal.log_warning`, or a line in `build.sh` naming where the result is
(`Saved/Logs/MatterRuntime.log`).

**Where it'd live.** `unreal/` code (a `/quick-fix`) or `docs/Learnings/Unreal/` T-series.

---

## Keep these

- **One clearance for the whole Unreal sequence (Phase06 D1), asked once with the steps named** — the lead answered one
  question; every build and GPU launch after it ran without a round-trip, and D1's check-for-a-running-Unreal was still
  done first.
- **The spike's failure path written in the plan (RD-P09-7: "the token is not added and the finding goes to the lead")** —
  two attempts, then a clean stop; the lead ruled in one line on a three-row picture.
- **Bumping the job format when a master's input moves** — a `v1` package now refuses a picture job loudly instead of
  silently rendering the eye without its picture on whichever machine still has the old pin.
- **"Is it current?" on the package** — the packaged Shipping build's face view against the editor's (same means, max
  diff 9/255) before publishing a public, irreversible release.
- **The deliverable-surface rule** — *"Can I see it?"* was answered by the rig's sheet (`--score-only` from the renders on
  disk) and a labelled close-up opened on the lead's desktop, not a published page.

## Dead weight

None.

## Open questions

1. **Lead:** is `library/staging/matterlib-0.1.0/` on the UE machine a deliberate local tree, or residue to clean? It is
   what turns two gate lanes red there (item 2).
2. **Refiner:** item 1's method half — does "check the kernel log after a device loss" belong in the portable method
   (any GPU project) or only here?
