# Phase02 — One-Command Check

**Status:** 🎉 COMPLETE (closed 2026-09-23). **Automatic pull-request checks are PARKED by the lead** (*"that is really advanced and I don't want it"*), so the close is no longer provisional on CI. The Outcome's last clause is carried to the Contribution Path phase, and the dormant workflow is kept for it (§Execution Log, CLOSE). Numbered by the lead (`/discovery Phase 2`, 2026-09-23): the entry at the head of the Roadmap's `## Future`. **Lane: `build`.**

## Outcome

**Anyone can clone the library on a fresh machine, run one command, and see every material and release validate, with the result also checked automatically on every pull request.**

*(Verbatim from the Roadmap entry, written at Phase01 step 1.5.)*

---

## The Brief

### First human test

There is no running service. The surfaces are a terminal and the repo's GitHub pull-request page. Prerequisites: `git`, `git-lfs`, and `uv` (Lead call 1).

1. `git clone https://github.com/Imrsv-tools/Matter-Library /tmp/ml && cd /tmp/ml`
2. `uv run tools/validators/run_all.py` → the summary lists **every lane as `PASS`, `SKIP (<why>)` or `FAIL`**, with counts. On a box without the encoder, `compression` and `staging` read `SKIP (pinned encoder V4.5.52 absent)`. The exit code is 0. *(step 2.1)*
3. Append one byte to any texture under `MatterLibrary/textures/` and run the command again → the **release-verify** lane `FAIL`s and names `matterlib-0.1.0` and the texture set. The exit code is 1. `git checkout -- MatterLibrary` → green again. *(step 2.2)*
4. Open any pull request at `https://github.com/Imrsv-tools/Matter-Library/pulls` → a **structural-gate** check is green, and its log shows every lane `PASS` with **zero `SKIP`**. The encoder lanes ran. *(step 2.3; needs the lead's push, because the repo is public)*

Each click is reachable by the step its note names. Step 2.1's test is clicks 1–2; each later step adds its own click.

### In now

- **A pinned core environment** a newcomer gets in one step (`pyproject.toml` + `uv.lock`, Lead call 1).
- **Tri-state lane reporting.** Today every skip path does `return True`, so a skip reports `PASS` (read in `run_all.py`, 2026-09-23). A local run may skip, and the report says so. CI runs **strict**, where any `SKIP` is a failure. That is how the gate is demonstrated both ways.
- **`fixture_sync` leaves the gate.** It reads a consumer's tree outside this repo (it probed `../IMRSV_Studio/…` from a `/tmp` clone). Ruled by R1, and `PlatformDependencies.md` P8 names "this repo (removes it)". **Don't Delete:** `check_fixture_sync.py` stays as a standalone tool the consumer can run with `--fixture-root`. The lane's intent is recorded in `AuthoringHarness.md` as moved to the consumer side (P8).
- **A release-verify lane** (Lead call 3, the mechanism only): each committed `*.freeze.json` re-verifies against the tree. The encoder-built `dds_set` is included when staging exists, and otherwise names what it could not check.
- *(Parked by the lead at close, 2026-09-23 — see Status.)* **CI on GitHub**, running the gate strictly on every pull request and every push to `main`, with the pinned encoder installed. Locally the encoder stays optional: its lanes `SKIP` and name `COMPRESSONATORCLI` (Lead call 2).
- **Routed hygiene**, each discharging a dated marker:
  - Every hardcoded home path in `tools/conformance/` (9 files) and `tools/generators/gen_asset_library.py` goes. They point at a **retired** platform checkout (`…/IMRSV_GITrepos/IMRSV_Platform/…`), so they are broken on the lead's box too. The repo root derives from `__file__`; the USD install and conda env come from environment variables with documented defaults.
  - `library/provenance/matterlib-0.1.0-textures.md` platform phase ids (Phase01 §Deferral ledger).
  - The USD recipe comments that describe a consumer's build (`USDValidationToolchain.md` Drift).
  - The add-on's `(5, 1, 1)` against the installed Blender **5.1.0** (measured 2026-09-23; `Experience_MatterLibrary.md` Reevaluate).
  - The dated "fails at import / no CI / skip reports green" claims (sites in §Build map).

### Not now

- The contribution gate (source → `candidate`) and CODEOWNERS → Contribution Path.
- The **immutability rule** (a changed file under a shipped `vNN` is rejected by `vNN` semantics) → Version Management. This phase's release-verify lane is the hash mechanism that rule can build on. It does not decide the `0.x` question.
- A parity-render gate in CI → Parity Baselines. Building OpenUSD or running Blender or Unreal in CI → not planned. The one command is the structural gate. Its import graph touches only `validators/`, `converters/`, `compressors/` and `releases/` (read 2026-09-23), so the USD and Blender tiers are outside it.
- Any contract or schema change → Release Bundle and Consumer Contract.

### Reuse check — what the stack already provides

| Need | Native answer | Custom layer? |
|---|---|---|
| MaterialX in Python | PyPI `MaterialX==1.39.5`: wheels for CPython **3.9–3.14** on Linux x86_64, macOS arm64 and Windows. **No macOS Intel wheel.** (PyPI JSON, 2026-09-23.) | none |
| Pinned env + lock | `pyproject.toml` (PEP 621) + a lockfile | none (`uv`, Lead call 1) |
| The encoder | AMD's own `compressonatorcli-4.5.52-Linux.tar.gz` release asset, sha256 `70c9cdb27a19875df03766f349864951a749a44c0f5c001c33903944465f6b97`. `compress_textures.py` already reads `$COMPRESSONATORCLI`. | a download + checksum step, nothing else |
| CI | GitHub Actions, `actions/checkout` with `lfs: true`, `actions/cache` for the LFS objects and the encoder | none |
| Freeze re-verify | `freeze_release.verify_freeze(root, rec[, staging])` already exists. The gate calls it only on a freshly computed record, never on the committed one. | a lane calling it, no new logic |
| Tri-state results | none in `run_all.py` | **yes.** The gap: the method's "a gate you cannot demonstrate both ways is not a gate". A skip indistinguishable from a pass fails that. |

**Standards materially touched:** the GitHub Actions security model for public repos (below). Nothing else: no contract, schema or naming change.

### Decisions that bind

- **R1 (producer, never reads a consumer's tree)** → `fixture_sync` leaves the gate.
- **P8** → this phase removes the lane. `AuthoringHarness.md` §Drift's "owned by the release-bundle phase" is the outlier and gets corrected at execute. Both are derived docs from Phase01, not a lead-vs-lead conflict.
- **Don't Delete Spec Functionality** → the fixture-sync tool survives, with its intent recorded. Nothing aspirational is pruned.
- **Git LFS for textures** (`_Architecture.md`) → CI checks out LFS. It must: a pointer-only clone runs today's gate **green** (measured), and only the release-verify lane catches it.
- **Public repo; publication is lead-gated** → the CI workflow reaches GitHub only through the lead's push.

### Risk lane — `build`, verified

**The control:** the new workflow's trigger and token scope. There is **no `.github/` directory** today (checked 2026-09-23), so no existing control is amended. The workflow uses `on: pull_request` and `push: main`, **never `pull_request_target`**, with `permissions: contents: read` and **no secrets**. A fork PR then runs with a read-only token and no secret access, which is GitHub's own sandbox for this case. The one supply-chain edge is the encoder download: pinned URL plus a sha256 check, and the step fails on mismatch. Any later request for a secret or a write token in this workflow **raises the lane to `high-rigor`**.

### Step list

1. **2.1 — One command, truthful report.** Pinned env; `run_all.py` reports `PASS`/`SKIP`/`FAIL` with counts and a `--strict` mode where `SKIP` fails; `fixture_sync` out of the gate. *First clickable result:* clicks 1–2.
2. **2.2 — The release validates.** The release-verify lane re-verifies every committed freeze record. It must demonstrably fail on a changed texture and on a pointer-only (no-LFS) checkout. *First clickable result:* click 3.
3. *(Parked by the lead at close, 2026-09-23 — built, never run.)* **2.3 — Checked on every pull request.** The Actions workflow runs strict, with LFS and the checksummed encoder, both cached. Lead push. *First clickable result:* click 4.
4. **2.4 — The other tiers run from any clone.** The hardcoded-path removal and the rest of the routed hygiene, plus the docs flips. *First clickable result:* `tools/conformance/check_asset_library.sh` from `/tmp/ml` finds its repo without an edit (Blender 5.1 present).

No split signal: one journey (the same gate, at a desk and on a PR). Step 2.1 is small.

### Compact build map

- **New:** `pyproject.toml` (+ lock) at the root, deps `MaterialX==1.39.5`, `pyyaml`, `numpy`, `Pillow`, Python pinned to **3.12**, which matches the conda env and the probe. `.github/workflows/gate.yml`.
- **`tools/validators/run_all.py`:** lane functions return a result enum or tuple instead of `bool`; summary and exit logic; `--strict`; drop the `fixture_sync` entry; add `release_verify`. `approval_binds_freeze` already has the staging-present branch. Keep the two lanes distinct.
- **`tools/validators/check_fixture_sync.py`:** stays; module docstring points to P8.
- **`tools/conformance/*`, `tools/generators/gen_asset_library.py`:** replace the absolute constants. `render_leg_probe.py` and `check_conformance.sh` also default their output to a dead `~/.claude/jobs/…` path.
- **Docs flipped at close:** `docs/ToolingConventions.md` (§Entry points, §Gates and CI), `docs/specs/Tooling/AuthoringHarness.md` (Todo, lane table, fixture-sync Drift), `docs/specs/_Architecture.md` §Governance Drift, `CONTRIBUTING.md` (the dated `run_all` gap), `USDValidationToolchain.md` Drift, `Experience_MatterLibrary.md` Reevaluate, `PlatformDependencies.md` P8 status. **The lane count stays 16: `fixture_sync` out, `release_verify` in (Lead call 3).** `.ai/AI_Orientation.md` and `.ai/commands/LOCAL_DELTAS.md` carry the same stale claims but are the Refiner's lane → **`/retro` item at close**, not an execute edit.
- **Measured baseline** for the executor (2026-09-23, fresh clone, throwaway 3.12 venv with the four deps): exit 0, 13 lanes ran, 3 skipped (`fixture_sync`, `compression`, `staging`). With `COMPRESSONATORCLI` pointed at the unpacked asset: all encoder lanes ran, exit 0, **~80 s wall / ~14 min CPU** on the lead's box. A GitHub runner has fewer cores, so expect minutes. `stage_release.py build 0.1.0` followed by `verify_freeze` against the **committed** freeze gave **zero drift, `.dds` included**: the pinned encoder reproduces the shipped release byte for byte. Without staging, the committed freeze drifts only on `dds_set` (+ digest). Pointer-only, it also drifts on `source_textures_set`.

---

## Lead calls — RESOLVED (2026-09-23)

The lead, verbatim: *"go with the recommendations"*. Each call below records the recommendation that was accepted.

1. **Environment form (research Q7) → `pyproject.toml` + `uv.lock` for the core tier; the one command is `uv run tools/validators/run_all.py`.** Plain `pip install` from the same `pyproject` stays possible. The conda `environment.yml` is unchanged and serves the USD build only. *(Rejected: extending the conda env, which is heavy for CI and couples the core to the USD tier; `requirements.txt` + venv, which is two commands with no lock.)*
2. **Encoder lanes → always in CI (strict, checksummed download, cached); optional locally, where they `SKIP` and name `COMPRESSONATORCLI`.** *(Rejected: auto-fetching the encoder locally.)* Asked in the same exchange whether any of this should be hosted, the answer was no: CI runs on GitHub's throwaway runners, not a self-hosted one. The one hosting dependency is AMD's release asset. It is pinned and cached, and if it disappears the fallback is a copy attached to one of this repo's own releases (MIT).
3. **Release-verify lane → in this phase, as the mechanism only** (hash re-verify of committed freeze records). The `vNN` immutability rule and the `0.x` question stay in Version Management.

## Discovery Log

- **Lead ruling (2026-09-23):** *"go with the recommendations"* → §Lead calls. The Brief is complete.
- **Pass 1 (2026-09-23) — specs top-down + capability probes.** Read `_Architecture.md` → `AuthoringHarness.md` → `run_all.py` in full, plus the research doc (Pass 7, seed 2, Q7), `ToolingConventions.md` and `PlatformDependencies.md`. Probed against **this project's artifacts**, all in `/tmp`, repo untouched: a 3.12 venv + four deps runs the gate green; the public GitHub clone delivers all 30 LFS textures (~35 MB); the pinned Linux encoder runs every lane and reproduces the committed 0.1.0 freeze exactly. **Seed corrections:** "16 vs 13 + 9b lanes" was a false alarm (the docstring groups lanes; `main()` has 16 `results` keys). Seed Q3 ("how far does fresh machine reach") failed test 1: the import graph answers it for the one command, and Phase01's ledger had already routed the path fixes here. It is now scope, not a question. Seed Q2 passed test 3 once the asset was downloaded and run. **Learnings:** `docs/Learnings/` holds no domain yet, so there was nothing to read. That is a discharged read, not a skipped one.

## Execution Log

| Step | Commit | Result | Next |
|---|---|---|---|
| 2.1 | `6625731` | Fresh clone: 15 lanes, 13 PASS / 2 SKIP, exit 0; `--strict` exit 1 without the encoder, 15 PASS / 0 SKIP with it. **Lead sitting (clicks 1–2), verbatim: *"mark a good and continue"*.** ✅ | 2.2 |
| 2.2 | the 2.2 commit | `release_verify` (16 lanes). Three throwaway-clone arms, predicted and observed: one byte appended to `Dust01_overlay_s001.png` → the **only** red lane, naming that file · a pointer-only (no-LFS) clone → **only** red lane, 30 files changed · pinned encoder, `--strict` → 16 PASS / 0 SKIP, the **complete payload incl. `.dds`**, no staging left behind. Finding while building: the freeze record hashes `.dds` **paths**, so the set can only be re-verified at `library/staging/matterlib-<V>/`; the lane builds there only when absent, and removes only what it built. | lead click 3, then 2.3 |
| 2.2 sitting | — | **Lead, click 3, verbatim: *"mark as good and continue... to be fair... I am not really sure what the goal is of this phase but seems like we shuld do it so we can get back to working on the library again"*.** ✅ | 2.3 |
| 2.3 | the 2.3 commit | `.github/workflows/gate.yml`: `pull_request` + `push: main`, `contents: read`, no secrets, actions pinned by SHA (checkout v7.0.1, cache v6.1.0, setup-uv v10.2.0), LFS cached by object set, encoder download cached and sha256-checked every run, `uv run --locked … --strict`. Pre-push: the pinned encoder encodes and reports `V4.5.52` in a stock `ubuntu:24.04` container. ▶ SCAFFOLD COMPLETE — the first CI run is owed (needs the lead's push). | lead push → CI run |
| 2.3 push | — | Lead: *"go for it"*. Pushed `b30efc4..b96cf9d`. The workflow registered ("Structural gate", active), but **no run started: GitHub Actions is disabled on the repository** (`actions/permissions` → `enabled: false`). ▶ still owed: enable Actions, then the first run. | lead: enable Actions |
| 2.4 | `02df570` | No absolute path to the retired checkout remains in `tools/` or `blender/` (`git grep` → 0). **Click, from a fresh clone at another path:** `check_asset_library.sh` (Blender 5.1.0, 11 articles) and `check_conformance.sh` (USD 26.03) → exit 0, 110 PASS / 0 FAIL, clone left clean. Add-on declares `(5, 1, 0)`, measured enabling on 5.1.0. Docs flipped. Promotion's own fixture-sync dependency kept as a narrowed Drift (release-bundle phase). `.ai/AI_Orientation.md` and `LOCAL_DELTAS.md` still say "16 lanes / fails at import" → **`/retro` item at close** (Refiner's lane). ✅ | close, after the first CI run |
| 2.3 Actions | — | The lead enabled Actions for the repo. The repo still read `enabled: false`: the **org** policy was `enabled_repositories: none` (read with the lead's `admin:org` login). A dispatched run (`35902233653`) sat queued with no job and was closed by GitHub. Changing the org policy from this session was refused by the auto-mode classifier (org permission grant), which is correct. ▶ SCAFFOLD COMPLETE — first run owed. | lead ruling |

### CLOSE — DONE (2026-09-23)

**The lead's ruling, verbatim.** Offered *"1. Turn the switch on … 2. Skip it for now and get back to the library. Close Phase 2 with the automatic GitHub check marked 'ready, waiting for the switch'"*, the lead replied: **"2"**.

**Acceptance, against the Outcome sentence:** *"Anyone can clone the library on a fresh machine, run one command, and see every material and release validate, with the result also checked automatically on every pull request."*
- **Clone, one command, every material and release validates:** met. Fresh clone → `uv run tools/validators/run_all.py` → 16 lanes, 14 PASS / 2 SKIP, exit 0 (re-run at close, after a sibling session's commits). The two skips are the encoder lanes, named as such. With the pinned encoder: 16 PASS, including the full `.dds` release payload.
- **Checked automatically on every pull request: NOT met.** The workflow exists and is correct as far as anything short of a run can show, but it has never run: the org policy disables Actions. **Disposition: `ALREADY ROUTED`** (the lead ruled "2" with this gap stated in the message). The `🎉` headline says so.

**Deferral ledger:**

| Open thread | Disposition |
|---|---|
| Automatic PR checks (CI) | ~~ALREADY ROUTED: lead "2"; owed a first run.~~ **Superseded the same day, PARKED by the lead**, verbatim: *"so hold on... close is blocked becuase of this git check thing? that is really advanced and I don't want it"*. Intent kept (Don't Delete): `.github/workflows/gate.yml` stays, dormant (the org Actions policy disables all repositories). Whether to turn it on belongs to the Contribution Path phase, whose Outcome already promises "an automatic verdict". |
| `promote_release.py` still runs the consumer fixture-sync check | **deferred as an ADDITION**: a pre-existing dependency of promotion, not a surface this phase authored (the Brief scoped `fixture_sync` out of the **gate**). Recorded as a narrowed Drift in `AuthoringHarness.md` → Release Bundle and Consumer Contract. |
| Stage adopting the fixture-sync check (P8) | platform-side; `PlatformDependencies.md` P8 reads "half done". |
| `.ai/AI_Orientation.md` and `.ai/commands/LOCAL_DELTAS.md` still say "16 lanes / fails at import" | **Refiner's lane** → `/retro`. |
| A sibling session's research commit (`6834943`) rode this phase's push | disclosed to the lead in the same turn; scanned, no private detail → `/retro` ("list the outgoing commits before every push"). |
