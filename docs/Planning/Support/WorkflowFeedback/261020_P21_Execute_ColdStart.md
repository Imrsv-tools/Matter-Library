# Workflow Feedback — P21 / execute / cold start

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P21` (Skin Maps) |
| **Mode** | `cold start` (suspend-handoff at 21.2, for a fresh session to take 21.3) |
| **Outcome** | `suspended`. 21.1 and 21.2 ✅ with the lead's clicks 1–3; 21.3 next in a fresh session (the phase doc's Resume block). An Unreal runtime request was filed in M7, and the run pushed at the lead's word (`2e145eb`). |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: execute stages 2–4 for two steps, three sittings with the lead present, two gate runs, a push. **Not exercised:** the close; `execute_repair.md`; the Unreal build (no engine on this machine). |
| **Date** | `2026-10-20` |

---

## Items, ranked

### 1 — A Character sitting scene is hand-built in `/tmp` every phase; the rig's own light cannot show what skin sittings judge `[doc-gap]`

**Grounding.** `LOCAL_DELTAS.md` (the *artifact a person reaches* row) says a scene for the lead is *"built headless from the factory scene into its own file and that file is opened"*. No tool does that for the character.

This run wrote `/tmp/p21_sitting_build.py` and `/tmp/p21_sitting_view.py` from scratch, then needed five fixes before the lead saw anything:
- a stale object reference after removing the imported lights (`ReferenceError`);
- the two characters 0.75 m apart, so today's arm crossed the new hand camera;
- the view script's area split leaving three panes, not four, with cameras in the wrong panes (repaired live through the Blender MCP);
- AgX in place of the rig's Standard view;
- a front sun that flattened the face.

The rig's own Blender job was the obvious base, and is unusable for this judgement. Its lighting is *matched* by design (no shadows, no bounce, `blender_render.setup_scene`), which F-P21-1's "does it still read as plastic?" cannot be judged under.

B11's "render the exact view headless and look at it before opening it" caught the overlap and the light. That rule worked; the missing piece is the tool.

**Proposed fix.** Two parts:
- (product) promote the builder to `tools/parity/sitting.py`: two rig jobs side by side, a face and a hand camera each, a real light, and a four-pane view;
- (method) one clause in the RUN row: *"a sitting that judges how a material reads, not whether the tools agree, needs a real light: the rig's matched light has no shadows or bounce by design."*

**Where it'd live.** `LOCAL_DELTAS.md`, the RUN or *artifact* row (the clause). The tool is product work: an issue or the next Character phase's Brief.

---

### 2 — A probe's "works in all three tools" rode into a Brief and was false for Storm. It surfaced only because a ΔE moved; corroborates `c73cff0`'s by-eye parity item `[doc-gap]`

**Grounding.** The Brief's reuse check cites F-SKM-22/F-SKM-27: `base_color_map` *"proven in all three tools by the probe"*. At 21.2 the lips' Storm–Blender ΔE rose from ~3 to 4.4–6.2. The cause, measured with a uniform sRGB-128 map against a 255 one: Storm read every picture supplied through an interface input RAW. Its ratio was 0.52–0.60, against Blender's 0.28–0.41, and 0.275 once the USD asset carried `colorSpace`.

The probe's own Storm render had the same washed-out lips. It was judged by eye beside a Blender column that looked right. The defect is older than Phase09: the eyes' iris ΔE of 15.8 had been on every character scorecard.

The Verify row *"your evidence is a RECORD claiming something happened"* covers it in principle. Nothing pointed at a parity *claim inherited from a probe* as such a record.

**Proposed fix.** Fold into `c73cff0`'s item ("by-eye parity measured first") as a second grounding. Its form: *"a parity claim from a probe that was judged by eye is a record, not a measurement; before a Brief cites it, the rig's per-part ΔE for the input in question must have been read. A persistent large ΔE on one part (the iris's 15.8) is an open defect, not a baseline."*

**Where it'd live.** `execute.md` §Verify (the record row), or `discovery.md`'s reuse check. The Refiner decides; it pairs with `c73cff0`.

---

### 3 — I used `cd /tmp` once, in the first heredoc Python call `[self-error-doc-could-prevent]`

**Grounding.** `cd /tmp && python3 - <<'EOF' …` to hash the probe's cached sources. The ban (`.claude/CLAUDE.md` §Codebase search: never `cd`) was known. The reflex was to keep a scratch script's working directory out of the repo. The shell reset and nothing ran in the repo; it was reported to the lead at once. Every later scratch script was written to `/tmp/*.py` and run by absolute path, which needs no `cd`.

**Proposed fix.** One sentence beside the ban: *"A scratch script needs no cd: write it to `/tmp/<name>.py` and run it by absolute path; a heredoc into the interpreter needs none either."* Low value; the rule is clear, and the slip was a reflex.

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search, or nowhere (decline is fine).

---

## Keep these

- **§Verify (iii), a selector reading TREE STATE.** `test_build_snapshot.py` pinned the working tree's fitted articles to a list of two and went red the moment 21.1 fitted Skin/Lips IV. Recognised at once as a selector, not a regression; held to the recipes and marked `FALSE RED:` in its header.
- **"Confirm it can fail" / "the instrument before the subject".** Running the uniform-map pair through *Blender* as well as Storm turned "Storm reads raw" from a hypothesis into a measurement: the instrument separated 0.275 from 0.55.
- **"Bisect by construction" (§Build).** The green-lips test map (Storm samples the right place) and then the uniform maps (Storm reads the wrong colour space) separated two causes in two renders.
- **Exact-once anchored script edits** (`.claude/CLAUDE.md` §Editing). About ten multi-anchor edits across `job.py`, `rig.py`, the drivers, `build_character.py` and twelve recipes, each aborting on any count other than one. Zero misses.
- **Ask whether the lead is available; walk one act at a time.** Clicks 1–2 ran in one short sitting; the tint was set and reverted live through the MCP while the lead watched. The lead's *"still reads plastic"* landed at the step that could use it.
- **The context line at each act boundary.** Offered the handoff at about 350k, before the lead had to ask.
- **§Git's push row.** Two of the lead's other-session commits sat under this run's tip. They were named before the push, the public-repo check was run on the retro among them, and the tip was pushed by value.

## Dead weight

None.

## Open questions

1. **(Lead, product)** Should the sitting builder (item 1) become a tool now, or wait for the next Character phase? The scratch copy is not kept.
2. **(Refiner)** Does F-P21-9's Storm learning belong only in `docs/Learnings/Storm/` (21.3 owes it there), or also as a rig rule? Any USD writer that supplies a colour picture must author `colorSpace`. Today `job.MAP_COLORSPACE` is the only enforcement, and no gate checks it.
