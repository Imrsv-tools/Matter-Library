# Workflow Feedback — P22 / execute / resume 2

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P22` (*Skin Maps Beyond Colour*) |
| **Mode** | `resume run 2`. A distinct run from `261027_P22_Execute_Resume.md` (the session that sat click 2), not a continuation: launched from the Resume at `89eedca`. |
| **Outcome** | `done` for this run's act. The shine was brought down (`ea9eabc`, RD-P22-17), the thickness probe passed (`42336e5`), and `scatter_map` was built in all three tools (`857ea01`, RD-P22-18). Click 3 is owed on the scatter sheet; 22.4 is next. |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: BUILD (a maker change, a contract input through every tool, two runtime C++ changes), measured probes, the gates, the commit discipline, the handoff. **Not exercised:** a sitting. The lead did not judge either sheet in this run, so whether the shine pass satisfies *"over the top"* is unknown. 22.4 and the close were not run. |
| **Date** | 2026-10-27 |

Step 0: the handoff state (Resume, ledger 22.2.5 … 22.3.3, P34, RD-P22-17/18) was committed in `857ea01` before this file.

---

## Items, ranked

### 1 — "Can the surface show it?" was answered by naming a camera, and the look view's light could not show the property `[doc-gap]`

**Grounding.** The Brief's click 3 said: *"Can the surface show it? The look view's backlit camera, today's beside the new."* The first Unreal probe (radius ×1/×3/×10, anisotropy 0) showed no glow through the ear, and that nearly went down as "Unreal cannot carry it". The cause was the fixture. The look rim cast no shadows, and Unreal draws light through thin parts from the light's shadow depth, so no material could have glowed. After the fix (`rim_shadows`), a second fixture fault sat on the same judged area: parts hidden from a view still cast shadows, so the hidden hair's dithered cards shadowed the head behind the ear. Both were found only because the run rendered a **known-positive control** (radius ×10) and a **known-negative one** (no subsurface) beside the subject, and looked at the picture.

**Proposed fix.** In `execute.md` §TRY's *"ask whether the surface … can SHOW the thing the click is about"*, add: **for a light-transport property, render a control at an exaggerated strength (and one with the effect off) before measuring the subject. If the exaggerated control does not move, the surface is at fault, not the material.** In discovery's First human test, "can the surface show it" names the mechanism the renderer needs (here, shadow-casting backlight), not only the camera.

**Where it'd live.** `execute.md` §TRY and `discovery.md` First human test (portable). The Unreal fact (transmission needs a shadow-casting light; hidden-from-capture parts still cast shadows) goes in the repo's Learnings, Unreal domain (local).

---

### 2 — A reading that moved the WRONG way was an instrument fault too, and the doc names only "barely moves" `[doc-gap]`

**Grounding.** The shine measurement was the variant's luminance minus a diffuse-only render (coat 0, specular 0). Turning the coat off *raised* the measured shine (face 4.9 → 8.9), the opposite of the picture. In OpenPBR a coat also dims the base's reflection beneath it, so "minus diffuse" cannot isolate a coat. The run caught this, switched to the highlight statistics (p99, highlight area), and read the pictures. The rule that fired, *"a parameter that should matter and barely moves the reading indicts the instrument before the subject"*, covers a reading that doesn't move, not one that moves backwards.

**Proposed fix.** Extend that row in `execute.md` §Verify: **a reading that moves opposite to what the picture shows indicts the instrument the same way.** Check what the reference subtracts.

**Where it'd live.** `execute.md` §Verify (portable).

---

### 3 — A headless Unreal test from another session is not the lead's GPU work, and the rule has one answer for both `[doc-gap]`

**Grounding.** Before the runtime build, `ps` showed an `UnrealEditor-Cmd … -ExecCmds=Automation RunTests … -nullrhi`: a platform session's unit test, CPU-only. `LOCAL_DELTAS.md` §Two machines says: if one is running, *"ask once for the whole batch"*. The lead had said "keep working", and the process was a seconds-long headless test, so the run waited for its PID to exit (a background `ps -p` loop) and then built. That kept the rule's intent (don't fight the lead's Studio for the GPU) without a question the lead would not want.

**Proposed fix.** In `LOCAL_DELTAS.md` §Two machines: **a `-nullrhi` automation run is not GPU contention. Wait for its PID to exit (bounded), then launch. Ask only for an interactive editor or Studio.**

**Where it'd live.** `LOCAL_DELTAS.md` (local).

---

### 4 — A maker's self-check repeated the constant it guards as a literal, so changing the constant failed the run `[self-error-doc-could-prevent]`

**Grounding.** Moving the roughness map's held average from 0.5 to 0.62 meant updating the unit test (found by grep). The maker also carried its own `abs(avg - 0.5)` check, a second copy of the literal, and the first re-make died on it (~1.5 min lost). The edit had grepped the test for the literal but not the maker.

**Proposed fix.** A learning, local: **a maker's check names the constant (`SKIN_ROUGHNESS`), never its value. Before re-running after changing a constant, grep the changed files for the old literal.**

**Where it'd live.** `docs/Learnings/` (local), or nowhere if the Refiner judges it too small.

---

## Keep these

- **Every lever in ONE Unreal launch, from a scratch probe that reuses the sheet's own job** (`look_job.json`: its meshes, lights and cameras): 11 variants in ~2 minutes. It answered "which lever is the shine" with numbers and pictures before anything was built. That was the ColdStart retro's "a column per lever", scaled up.
- **Measure direction, not only visibility** (the earlier Resume retro's item 4): highlight peak and highlight area against today *and* click 2, which showed today and click 2 had the same shine. Where no accepted reference can be shown, the physical one (measured skin roughness) was named instead, and the retro item's fallback worked.
- **Commit at the probe boundary before building the mechanism** (`42336e5`), so the verdict and the fixture fix are on disk if the build had to stop.
- **Byte-identity checks on the untouched outputs:** the lips' article, and the other three maps' hashes recorded before re-running the maker.
- **`git show --stat` read-back:** 13 / 4 / 21 files across the three commits, each reconciled.

## Dead weight

None.

## Open questions

- **The look-sheet measurement is still a scratch script** (`measure_shine.py`, `compose_and_measure.py` in the job's tmp), as the previous Resume retro flagged. Three sittings have now relied on it; it belongs in `look.py` (a quick fix).
- **The lips are now the glossiest part of the face** (coat 0.3 at 0.2 on a skin with none, RD-P22-8). Not judged, and not changed.
- **Blender's hand shows faint light lines along the mesh's edges under subsurface,** in today's skin too (22.3.1). Not this phase's; it may be the mesh's normals or Cycles' random walk on hm08. Unfiled.
- **Context:** the run handed back at ~385k, under the ceiling. 22.4 is a fresh session's.
