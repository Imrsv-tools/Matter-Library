# Research — The three Matter items the platform's tracker held (ledger row M2)

**Opened:** 2026-10-13 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each item.
**Mnemonic:** `TI` (ids `TI-Qn`, `TI-Fn`). **Pass 1** is written from the platform's side. The library's review of it against its own tree is a later pass.
**Requested by:** the IMRSV platform's lead, 2026-10-13, at a sort of the platform's tracker: an item about a tool belongs with the tool's owner, not in the platform's tracker.

**Question:** `PlatformDependencies.md` row **M2** says three open Matter items stay in the platform's tracker. What became of each, and what, if anything, is now the library's?

**Extends, does not replace:** `PlatformDependencies.md` row **M2**.

**Public-repo note.** The platform's planning is private. It is summarised here by what it found and what it needs — no platform paths, code, issue numbers or ruling ids.

**Measured at:** `edec589` (2026-10-13).

---

## The short version

- **None of M2's three items is tracked on the platform as a Matter item any more.**
- **Emissive colour:** the library's half is done (row P23). What is left is the platform's own: the two controls are in Studio's material panel and do not yet show to the eye. Nothing is asked of the library.
- **The cross-renderer match:** closed on the platform. The library's parity rig is the matched pipeline the item asked for. Nothing is asked; one question (TI-Q1).
- **The portable export's scale:** closed on the platform. The article is the right size. One idea is offered (A1).

---

## Pass 1 — What became of each

*Written from the platform's side, 2026-10-13.*

- **TI-F1 — Emissive colour.** The item asked whether a Creator may tint an emissive material. The library answered it: a light's colour and brightness are Creator ports (M2's own update of 2026-10-05). Studio has since built the two controls. In the app they responded once and a coloured light washed out; at a second look nothing changed. That is one open item on the platform, about its own drawing of several Creator controls, and it names nothing the library must change.
- **TI-F2 — The cross-renderer match.** The item asked for one view transform applied to both renderers' pictures, and a capture under matched conditions, before any cross-renderer difference is measured. Read here at `edec589`: `tools/parity/` writes one job, runs three drivers on it (Storm, Blender, Unreal) under matched lighting, and uses no tone curve in any of them (`tools/parity/JOB_FORMAT.md`, *Colour*). That is a matched pipeline, by a different road than the item named — it named the AgX parity config, `tools/conformance/build_ocio_parity_config.py`, which is still in the tree.
- **TI-F3 — The portable export's scale.** The item said the built `creator_table_portable.usda` arrived about 100 times too small in Unreal, and guessed the article's units. Read on 2026-10-13 from a package built two days earlier: `metersPerUnit = 1`, a table top 1.2 m by 0.8 m, standing 0.42 m high. The article is right. A metres asset arriving small would be a consumer's handling of units, and the platform's to find. It was not driven again for this note.

### The ask

| # | Need | Why | What exists today |
|---|---|---|---|
| A1 | **A scale reference in the conformance article** — a one-metre cube or a person-height marker beside the table. *An idea, not a need.* | Anyone's eyes can then judge at a glance whether a consumer brought the article in at the right size. The second half of the old scale item, and the only part of the three that is the library's. | The article holds a table top and one leg. |

### Questions for the library

- **TI-Q1 — Is the AgX parity config still used,** now that the rig compares pictures with no tone curve? If not, it may be a file to retire; if so, the platform has no use of it to report.

### What the platform does next

- Nothing waits on the library.
- The platform's tracker no longer holds a Matter item on the library's behalf. A need of the platform's arrives here as a doc like this one.

---

## A suggested ledger note — for the library to write or reword

Not written into `PlatformDependencies.md` from here; that file is the library's.

- **M2** — *reported by the platform, 2026-10-13:* none of the three is tracked there as a Matter item. Emissive colour: answered here (P23); the platform's remaining item is its own. The cross-renderer match: closed there, answered by the parity rig. The portable export's scale: closed there, the article is correctly sized; a scale reference in the article is offered as an idea (`261013_R_PlatformTrackedItemsAsks.md` A1). **The row could close**, with A1 taken or dropped.

---

## Pass 2 — the library's review (2026-10-14)

*From the library's side. Read against this tree at `42e26fa`; nothing was run. The lead tied the platform's asks to the platform's issue-sweep phase, 2026-10-14. That phase's sort of the platform's tracker is where this doc came from. Its plan lists the library as a repo it does not touch, and it asks nothing of the library beyond this doc. Its sky work was split out to the platform's next phase, whose asks are `261013_R_PlatformSkyAsks.md`.*

- **TI-F4 — TI-F2 holds.** The rig's colour rule is *"no tone curve. A plain sRGB encode: Storm's `sRGB` colour correction, Blender's `Standard` view transform. In Unreal, turn off the filmic tonemapper and auto-exposure"* (`tools/parity/JOB_FORMAT.md`, the lighting rules). TI-F3 was not driven again here. The golden that is tracked is `tools/conformance/golden/creator_table_lightweight.usda`. `creator_table_portable.usda` is built from it by `tools/conformance/build_portable.py` and is not committed.
- **TI-F5 — TI-Q1 answered: nothing calls the AgX parity config.** `tools/conformance/build_ocio_parity_config.py` is named by no other script in `tools/`. The rig compares pictures with no tone curve (TI-F4), and the codec A/B comparator runs one pinned Storm pipeline of its own (`docs/specs/Tooling/CompressedDistribution.md` §Codec A/B comparator). **Four docs still describe it as a current tool:** `CompressedDistribution.md` §OCIO 2.4-native parity config · `docs/specs/Tooling/AuthoringHarness.md`'s tool table · `docs/ToolingConventions.md`'s `tools/conformance/` row · the Glossary's *OCIO parity config*. Under the library's rule against deleting specified work (`.ai/AI_WorkingAgreement.md` §Project practices), the fix is to **mark it, not remove it**: `Reevaluate (2026-10-14)`: nothing calls it, and the rig compares with no tone curve. Whether to retire it is the lead's call.
- **TI-F6 — A1, the scale reference, is small and is the library's.** The table is the conformance golden above. Today a size is judged by the rig's ruler check, on a material. Nothing is placed in the article itself. A one-metre cube beside the table changes what the golden holds. The conformance checks that read it are baselined before the edit and run again after it (`check_conformance.sh`, `check_exporter.sh`), so the change is a `/quick-fix`. The platform offered it as an idea, not a need.
- **TI-F7 — M2 can close.** All three items are answered or closed on the platform's side (TI-F1 to F3). The library's half of the first one is row P23. The ledger is the library's file. The row's new text is the platform's suggested note, kept almost word for word.
- **TI-F8 — a fourth thread, from the same sort: one platform issue is parked waiting on the library's AP-Q5**, *who owns a garment's substance split* (`260928_R_PlatformAppearanceAsks.md`, still **Open** there). Since then, on the platform's side (2026-10-13), the platform's lead ruled two things. Everything of a character's is one platform phase of its own. Hair and wardrobe items are assets, stored and documented like sets and props, with a version and a licence. That says **where a garment lives** (the platform's asset store, not this library). It does not say **who splits a garment into its substances**. AP-Q5 is not answered here. It is noted so the next pass on that doc starts from the ruling.
- **TI-F9 — one Matter-facing fact in the issue-sweep phase, and nothing asked of the library.** Stage keeps a test fixture that mirrors the library's materials, with a guard that compares the two. On 2026-10-13 that phase measured the fixture **19 files behind the library's checkout**. Stage's own mirror tool updates it. That phase records the fixture as another lane's content and files it at its close. It is Stage's to mend, not the library's.

### What this pass offers (nothing is changed by it)

| Offer | Lane | What it does |
|---|---|---|
| **Close M2** in `PlatformDependencies.md`, with the note above | `/quick-fix` (the ledger) | The row says what the platform reported, and closes. A1 is carried in this doc, not the ledger |
| **Mark the parity config `Reevaluate (2026-10-14)`** in the four docs of TI-F5 | `/quick-fix` (docs) | The docs stop calling an unused tool current, and nothing is deleted |
| **A one-metre cube in the conformance golden** (A1) | `/quick-fix`, with both conformance checks baselined first | A consumer that imports the article at the wrong size shows it at a glance. Or drop it: the platform called it an idea |

## Resolved

The lead, 2026-10-14, on Pass 2's three offers: *"agree with your recommendations, I esspecially like size conformace topics … do the quick fixes"*.

- **RD-TI-1 — M2 closes** in the ledger, with the platform's report.
- **RD-TI-2 — the AgX parity config is marked `Reevaluate (2026-10-14)`**, not deleted. Retiring it stays a later call.
- **RD-TI-3 — A1 is taken:** a one-metre cube goes into the conformance golden.
- **Beyond A1, the lead's own idea:** a series of scale probes, so that *"anything with incorrect scale to the material will be OBVIOUS"*. It is its own design question: `261014_R_ScaleProbes.md`.

## Status

- **Passes:** 1 (the platform's), 2 (the library's, 2026-10-14).
- **Answered:** TI-Q1. Nothing in the tree calls the AgX parity config. The offer is to mark it for reevaluation, not remove it (TI-F5).
- **Open:** A1 (take it or drop it) · M2's close (a ledger quick fix) · AP-Q5, in its own doc (TI-F8).
- **▶ Next:** the lead's word on the three offers above. Each is a quick fix of its own, and none waits on the platform.
