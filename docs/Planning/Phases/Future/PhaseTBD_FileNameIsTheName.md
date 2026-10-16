# PhaseTBD — The File Name Is the Name

**Status:** SEEDED (2026-10-16) — not numbered. A pointer-shell written by `/research` on the lead's word: *"Seed a phase for what needs doing here and make it next"*. It is placed first in `## Future` by that word. `/discovery` fills it. **Starting discovery is a deliberate gate, the lead's call, never a slide.**

## Outcome

**Wherever a person meets a Matter material or HDRI (the website, Studio, USDLiveView), it is called by its file name's own words, the same in every app. HDRIs are named without *PureSky*, and every scene keeps its sky.**

## Why this is a phase

The library stopped publishing a second name on 2026-10-16 (RD-LBL-1). That half is done and published in `matterlib-0.2.0-dev.9`. What is left is not one sitting, and it is not the library's alone:
- **the HDRI rename's cutover** (RD-LBL-5, RD-LBL-7): built and off. It must land on the same day as the platform's rename of every reference, or scenes lose their sky;
- **each consumer showing the file name's own words** instead of a name of its own (ledger P30);
- **a gate gap the work exposed:** the one-command check does not run the tools' own test files, so a broken `test_hdri.py` stayed green (F-LBL-13).

It is one thing a person can see: the same name for a material and an HDRI in three apps, and every scene still lit by its sky.

## Scope — as ruled at research (2026-10-16)

The authority until this phase writes its specs: [`261015_R_MaterialLabels.md`](../../Research/261015_R_MaterialLabels.md) §Resolved (RD-LBL-1 to RD-LBL-7), Passes 4 and 5.

- **The rule** (RD-LBL-1): the file name is the name. A consumer shows `display_name`, its underscores as spaces or as breaks between its sections. It never drops or reorders a token. There is no `label`; the summaries and search words stay (RD-LBL-3).
- **The HDRI published name** (RD-LBL-5):
  - the source files keep their names;
  - everything published drops *PureSky*: the catalog id, the served file, `MATTER_ID`, the thumbnail, the site file and the default (`IndustrialSunset02`);
  - built behind `library/hdris.yaml` `published_drop_variant`, unset (`dc9bde6`).
- **The cutover, in order** (Pass 5):
  1. the platform renames its references (ledger P31);
  2. the library sets `published_drop_variant: PureSky` and commits;
  3. `serve_to_stage.py` re-serves the dev install, and the old HDRI thumbnails under `thumbnails/hdris/` are removed;
  4. a dev snapshot is published, at the lead's word.
- **The consumers' half** (ledger P30, P31): the website, Studio and USDLiveView show the file name's words; every repo that names an HDRI takes the new name on the day.
- **First human test (a draft for discovery):** the lead opens one material and one HDRI on the website, in Studio and in USDLiveView, and reads the same name in each, with no *PureSky* on the HDRI. Then he opens a saved scene that used the default sky, and it is still lit by it.

## Open questions (settle during this phase)

- **The gate gap:** should `run_all.py` run the tools' own test files (`tools/**/test_*.py`) as a lane, so a broken test cannot stay green? It is a lane change, and a lane is a lead ruling.
- **The cutover day:** when the platform's rename is ready (P31). The lead names it.
- **Blender's asset library:** it names each asset by its article name. Check, at discovery, that it shows the file name's words and nothing derived.

## Depends on

The platform's rename (ledger P31) for the cutover, and the platform's P30 for the consumers' half. The library's own half needs nothing.

## Discovery Log

*(empty — `/discovery` fills it)*
