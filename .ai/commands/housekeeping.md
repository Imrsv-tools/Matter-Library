# housekeeping — Maintenance Checks

Run after doc/plan updates or at phase closure.

## Checks

1. `.ai/context.md` names the correct active phase (or "no active phase" between phases).
2. `Readme.md`, `FolderStructure.txt`, and on-disk content agree on taxonomy + filename
   grammar. Drift is **tagged** (`(planned)`, `Todo`, date), never silently deleted.
3. Every seeded `.mtlx` validates against the locked filename grammar + metadata schema.
4. `build_plan.md` phase ordering and statuses are current.
5. Aspirational design preserved — nothing pruned just to match disk.
6. At phase closure: update the phase doc with outcomes, update `build_plan.md`, then have the
   platform bump this submodule's SHA.

## Commit Discipline

- Commit planning + doc updates before any implementation (rollback baseline).
- Code/doc commits land in this submodule; platform references this repo as an external track.
