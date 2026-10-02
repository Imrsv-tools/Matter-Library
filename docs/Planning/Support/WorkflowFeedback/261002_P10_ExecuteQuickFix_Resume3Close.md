# Workflow Feedback — P10 / execute → quick-fix / resume run 3 + close

| | |
|---|---|
| **Verb** | `execute → quick-fix` (one session: Phase10 run 3 and its close, then `/quick-fix F-P10-17` on the lead's word). A compound, like the sanctioned `discovery → plan` arc; it is not that arc, so the Refiner may prefer two files. |
| **Unit** | `P10` (Coloured Wear Layers), then F-P10-17 |
| **Mode** | resume run 3 (the library machine, after run 2 on the UE machine) · close · quick-fix cold |
| **Outcome** | `done`: pulled `unreal-runtime-v3`, click 6 passed, Phase10 closed and pushed (`fd490e4`); F-P10-17 fixed and pushed (`610243e`). |
| **Shape** | `behavior-touching` (the exporter, the loader, a conformance check, the library `.blend`) |
| **Confidence** | Ran fully: execute §TRY (click 6), `execute_close` A⁻ through E, quick-fix with a RED check. **Not exercised:** `execute_close` C (no issue-sourced phase), B⁺ (no Wave). |
| **Date** | 2026-10-02 |

Not a continuation. It follows `261001_P10_DiscoveryExecute_ColdStart.md` (runs 1 and 2's material, still undrained) and does not repeat its items. Item 1 is a sibling of that file's "check a handoff's command names".

---

## Items, ranked

### 1 — A command handed to the lead to paste must be paste-ready: no `<placeholder>` `[self-error-doc-could-prevent]`

**Grounding.** At the close's row A, the owed lead act, I handed the promote command as `promote_release.py 0.1.0 --approver <your name> --force`, copied in shape from `LOCAL_DELTAS.md`'s publishing row (`--approver <maintainer>`) and the phase doc's Resume. The lead pasted it as given; bash read `<your` as an input redirect: `bash: your: No such file or directory`. Nothing ran, and it cost a round trip. The value was one `grep` away: `library/releases/matterlib-0.1.0.approval.json` records the approver from the previous promote. The second hand-over used it and worked first time.

**Proposed fix.** In `execute_close.md` row A, beside *"goes to the lead … with the exact command"*: *"**Exact means paste-ready.** No angle-bracket placeholder: in a shell, `<word>` is a redirect, and the command fails before it runs. Resolve every value from the tree (the last record of the same act names it), or say in prose what to type in its place."* Locally, `LOCAL_DELTAS.md`'s publishing row could say where the approver lives (the previous `*.approval.json`).

**Where it'd live.** `execute_close.md` row A (portable); a clause in `LOCAL_DELTAS.md`'s publishing row (local).

---

### 2 — A `.blend` is compressed: a `grep` of it returns 0 for everything `[doc-gap]`

**Grounding.** To check the rebuilt library `.blend` held no author path, I ran `grep -c -a -F '/home/'` on it: `0`. The same count on the committed copy, which I knew had the path on 57 materials, was also `0`, and so was a count for an article name that must be inside. The file is compressed, so the check could not fail. Only reading it inside Blender (`blender --background <file> --python <scan>`) separated them: 57 path properties before, 0 after. `execute.md`'s *"confirm it can fail"* row is what made me test the old file. That rule worked; the Blender fact is what was missing.

**Proposed fix.** A learning: *"A saved `.blend` is compressed: `grep`, `strings` and `cmp` see nothing inside it, and a zero from them is a zero by construction. Read its data with `blender --background <file> --python <script>`."*

**Where it'd live.** `docs/Learnings/Blender/` (local; a stack fact, not method).

---

### 3 — The close's owed lead act was missed in the "running quietly" line; it landed only as the `▶` `[doc-gap]`

**Grounding.** Row A says the owed lead act goes to the lead *"at the START of the close"*, and §Running it says *"ONE progress line for the whole close"*. I put the promote command in that one progress line and went on with the docs. The lead did not run it until it was the `▶` of the handback, one message after the docs commit. That cost nothing here, since the docs work went on in parallel, but the gate ran once red while waiting. On a close whose acts are serial, it would be a stall that nobody notices.

**Proposed fix.** Row A: *"Hand it as the `▶` of a short message of its own, and carry on with the docs while the lead runs it. A command inside the progress line reads as narration."*

**Where it'd live.** `execute_close.md` row A, or §Running it.

---

## Keep these

- **The rebase pre-check at the pull** (`log --stat origin/main...HEAD`, both sides editing the Phase10 doc). The two local doc commits rebased cleanly onto the UE machine's three, and the Resume fix from my side was confirmed still present.
- **Confirm a check can fail** (`execute.md` §Verify). It caught item 2. It also gave the quick fix two real REDs: the new unit check fails against `HEAD`'s exporter copied to `/tmp`, and the widened 6b names a quoted `/home/...` path that `HEAD`'s version passes.
- **Baseline `check_exporter.sh` before editing `blender/addons/`** (`LOCAL_DELTAS`). That gave a same-set comparison: 62 PASS and the same five inherited reds, before and after.
- **Quick-fix's fifth verdict, "the lead already routed it here".** Four files and a library rebuild would otherwise have stopped at the gate; I stated the signal in one line and went on.
- **The `ALREADY ROUTED` and FIX dispositions in row A0/A.** F-P10-17 was named in the close handback and the `🎉` body, and fixed the next turn, so the close carried no deferral it owned.
- **The tripwire on backgrounded work.** I broke it once (a peek at Oak's rig output seconds after launching it, empty). The rule is right as written.

## Dead weight

None.

## Open questions

1. **`check_exporter.sh`'s PASS count: 62 today, 64 recorded at Phase10 10.2.** The same scenarios ran and the same reds were present, and I compared only my own before/after (62 = 62), so the quick fix is unaffected. What moved the count between 2026-10-01 and today is unexplained. Not this run's to chase. A Refiner question only if the count is meant to be stable; otherwise a note for whoever next baselines it.
2. **History still carries the old author path.** Earlier commits of `blender/asset_library/MatterLibrary.blend`, on GitHub too, carry the absolute path on every material. The quick fix did not rewrite history; whether to is the lead's call, recorded in `610243e`'s body. Not a method item.
