# Matter Library — Release Model & Distribution

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

How a Matter [library release](../../Glossary.md) is **settled, staged, frozen, qualified, approved, activated, and rolled back**.
A **Spec** — the control-boundary contract for release distribution.

> Original status line: "the control-boundary contract for production distribution. Shipped."
>
> **Drift (2026-09-23):** the machinery is built and exercised, but the library is not in production: `matterlib-0.1.0` is a **pilot release** (approved to prove the machinery, not shipped to users) — owned by the release-bundle / consumer-contract phase (R7).

> Companion specs: the runtime resolution surface is [RuntimeCatalog](../Contract/RuntimeCatalog.md); the authoring manifest
> is [Manifest](../Contract/Manifest.md); the compressed-texture toolchain + parity is [CompressedDistribution](../Tooling/CompressedDistribution.md).
>
> *Consumer-side (IMRSV): the compressed-texture wire transport — see [Consumers](../Consumers.md).*

---

## The distinction that organizes everything

Four independent records, never conflated:

| Record | Where | Keyed by | Answers |
|---|---|---|---|
| **Manifest** (`*.lock.yaml`) | `library/releases/` | authoring | which articles + statuses are IN the release |
| **Freeze record** (`*.freeze.json`) | `library/releases/` | qualification | the sha256 hash-lock of the COMPLETE frozen payload |
| **Approval artifact** (`*.approval.json`) | `library/releases/` | promotion | this release is immutable + eligible for PRODUCTION ACTIVATION |
| **Active-release selector** (`active-release.json`) | the install root | activation/rollback | which approved release an install currently serves |

*(Updated 2026-09-23, measured: `library/releases/` holds `matterlib-0.0.1.{lock.yaml,catalog.json}` and `matterlib-0.1.0.{lock.yaml,catalog.json,freeze.json,approval.json}`; the approval's `payload_sha256` and `payload_digest` match the freeze record.)*

**Approval ≠ activation.** Promotion creates the approval artifact (the sole promotion flip). Activation
writes the selector. Rollback re-points the selector; it never revokes or rewrites approval.

**The runtime is status-blind at RESOLUTION** — it resolves by identity + active release and never gates on
per-entry `status`. Approval/hash data lives at the control boundary ONLY; none of it enters the [runtime
catalog](../Contract/RuntimeCatalog.md) schema. (A consumer may still read `status` for broken-material suggestion *ranking* — resolution-blind ≠
status-unread.)

---

## The lifecycle

```
 author/settle → stage(.dds) → FREEZE(hash-lock) → qualify(isolated install) → PROMOTE(approval) → [publish] → ACTIVATE(selector) → [ROLLBACK / RECOVER]
```

1. **Settle statuses** — every included article is promoted to `status: approved` in the manifest BEFORE
   the freeze. Promotion never mutates the manifest afterward, so the approved release stays
   byte-identical to the qualified candidate.
2. **Stage** (`tools/releases/stage_release.py build <ver>`) — assemble the self-contained per-release
   `{png, .dds}` snapshot at `library/staging/matterlib-<ver>/` (the `.dds` are offline BCn derivatives,
   [CompressedDistribution](../Tooling/CompressedDistribution.md)). The staging tree is a **gitignored reproducible build artifact**
   (deterministic encoder + the freeze hash-lock give integrity without committing the large binaries).
   **The authored `MatterLibrary/textures` source tree is NEVER written with `.dds`** — it stays the open
   source of truth AND the fail-loud fixture for the uncompressed path by construction.
   *(Updated 2026-09-23, measured: `stage_release.py` subcommands are `build` and `verify`; `.gitignore` ignores `library/staging/`.)*
3. **Freeze** (`tools/releases/freeze_release.py compute <ver> --staging <dir>`) — sha256 the COMPLETE payload
   (catalog + manifest + every `.mtlx` + the source textures the lock names + `.dds`) into `*.freeze.json`:
   *(Corrected 2026-09-25, Phase03: freeze and staging took EVERY PNG under `MatterLibrary/textures/`, so one draft texture broke every frozen release; they now take the lock's textures, which reproduces `matterlib-0.1.0`'s recorded digest exactly.)*
   `payload_sha256{catalog, manifest, mtlx_set, source_textures_set, dds_set}` + a single binding
   `payload_digest`. CI re-verifies the frozen payload matches on later builds (`freeze_release.py verify <record>`).
4. **Qualify** — run the full validator/build/test wall against the frozen candidate in an **isolated
   candidate qualification install** (NOT production), plus a deployed audience-proof gate.
   *Consumer-side (IMRSV): the Unreal `-game` audience-proof gate — see [Consumers](../Consumers.md).*
5. **Promote** (`tools/releases/promote_release.py <ver> --approver <who>`) — the SOLE promotion flip. Re-asserts
   atomic version-surface agreement (release-record · all-approved · freeze-present · catalog byte-current ·
   Stage-fixture-sync · **freeze-matches** the on-disk payload) then CREATES `*.approval.json`
   `{release, approved_at, approver, payload_sha256, payload_digest, freeze_record}` REFERENCING the frozen
   hashes (never re-mutating the payload). First exposes `approved` — never before the deployed gate passes.
   A validator only CHECKS (`tools/releases/validate_approval.py`); a promoter CREATES.

   > **Drift (2026-09-23):** promotion gates on "Stage-fixture-sync" — equality with a copy held in a consumer's (IMRSV Stage's) fixture mirror — and on a consumer's deployed gate, so a producer release depends on a consumer checkout; under R1 the producer's gate must be self-contained and consumers verify the published release on their side — owned by the release-bundle / consumer-contract phase (R1).

6. **Publish** *(planned)* — the approved, frozen payload is packaged as the **release bundle**: one self-contained, hash-locked, published artifact per release that every consumer installs instead of reading this repo. No spec names its format yet — owned by the release-bundle / consumer-contract phase (R1, R14).

   Original step (kept, annotated): *Deploy — a deploy script writes the immutable versioned install root
   `<runtime root>/MatterLibrary/releases/matterlib-<ver>/` (catalog + materials + textures incl. `.dds`)
   + bootstraps the selector. Multiple versioned installs may coexist.*

   > **Drift (2026-09-23):** deploy was performed by a consumer-side script writing into a consumer's runtime directory; under R1 the producer must not deploy into a consumer — it publishes the release bundle, and each consumer installs it into its own install root — owned by the release-bundle / consumer-contract phase (R1).

   *Consumer-side (IMRSV): the deploy step into the Studio runtime directory — see [Consumers](../Consumers.md).*
7. **Activate** (`tools/releases/activate_release.py activate <ver> --runtime-dir <root>`) — OFFLINE (the consuming
   application stopped). Re-checks install-readiness against the installed root (approval valid · install present ·
   installed catalog sha256 == frozen catalog · every installed `.dds` byte-matches the frozen payload),
   then switches `active-release.json` **atomically via temp-file + `rename()`** — only once the complete
   install is verified ready. A failure before the rename leaves the prior release active. There is no
   in-session active-release change: the next fresh consumer process reads the new selector.
   *(Updated 2026-09-23, measured: `activate_release.py` subcommands are `activate`, `resolve-check` and `recover-unapproved`; the switch is `os.replace` of a temp file.)*
   *Consumer-side (IMRSV): Studio cache invalidation on process restart — see [Consumers](../Consumers.md).*

   > **Reevaluate (2026-09-23):** `activate_release.py` lives in this repo but writes into an install root that a consumer owns; whether it stays a producer tool shipped with the release bundle or becomes a consumer-owned installer is open — owned by the release-bundle / consumer-contract phase (R1).

---

## Install-root layout + the active-release selector

The contract for an install root (any consumer that installs Matter releases side by side):

```
<root>/active-release.json                                  {"active_release":"matterlib-<ver>"}
<root>/releases/matterlib-<ver>/matterlib-<ver>.catalog.json   (+ materials/ + textures/ incl. .dds)
<root>/recovery-audit.jsonl                                 (written only by pilot recovery)
```

- Each `releases/matterlib-<ver>/` is **immutable** once installed; multiple versions coexist.
- The selector is a single JSON object with one key, `active_release`, naming a directory under `releases/`. It is written only by activation / pilot recovery, atomically (temp-file + `rename()`).
- A selector naming a release that is not (fully) installed resolves to **nothing** from that root rather than
  silently serving a different release (atomic-activation safety).

*Consumer-side (IMRSV): runtime install-discovery (selector-first lookup, legacy flat-catalog fallback for the dev fixture tree) — see [Consumers](../Consumers.md).*

---

## Rollback vs Pilot recovery

Two distinct operations on the selector — never conflated:

| | **Rollback** | **Pilot recovery (break-glass)** |
|---|---|---|
| Target | a **previously *approved*** release | a coexisting, installed but **un-approved** release (e.g. the `matterlib-0.0.1` schema pilot, documented "NEVER approved") |
| Command | `activate_release.py activate <ver>` | `activate_release.py recover-unapproved <ver> --runtime-dir <root> --reason <text> --confirm` |
| Gate | the full approval + frozen-hash re-check | offline · target must be an installed immutable release · exact id + `--reason` + `--confirm` · loud warning + audit record (`recovery-audit.jsonl`) |
| Approval | required | **NONE created; the historical manifest is never mutated** |
| Status | mechanism covered structurally (only one approved release, `matterlib-0.1.0`, exists — no second approved release to roll *between* yet) | proven live (2026-07, tooling committed 2026-07-19) — recovered 0.1.0 → 0.0.1 and forward |

Both are OFFLINE selector re-points (no rebuild, installs coexist). Normal `activate` continues to REJECT
unapproved releases; recovery is the separate, audited escape hatch.

A composition pinned (the [release pin](../Contract/CreatorAssetProfile.md) `imrsv:matterlibRelease`) to a release the consumer has rolled/recovered PAST must fail loud, never silently mis-resolve against a different release.
*Consumer-side (IMRSV): `ReleaseConflict` behaviour and the broken-material scan — see [Consumers](../Consumers.md).*

---

## Integrity guarantees (the gates)

`tools/validators/run_all.py` (the [structural gate](../Tooling/AuthoringHarness.md)) pins, among others:

- **`freeze_lock`** — the complete-payload hash-lock is deterministic + tamper-detecting.
- **`approval_gate`** — a real/fixture `*.approval.json` is well-formed (`validate_approval.py`; fixtures `tools/releases/fixtures/approval_{valid,shallow}.approval.json`).
- **`approval_binds_freeze`** — a PROMOTED approval references the release's ACTUAL frozen hashes
  (`payload_sha256`+`payload_digest` == the freeze record) AND that freeze still verifies against the
  on-disk payload — i.e. *the approved release IS the frozen candidate, byte-for-byte* (validate_approval
  sees shape only).
- **`activation`** — `activate_release.py` verifies install-readiness + switches the selector atomically
  (a corrupt install is REFUSED and the prior selector is unchanged); the break-glass separation holds
  (normal `activate` rejects unapproved; `recover-unapproved` requires `--confirm`).

*(Updated 2026-09-23, measured: lane names match the `results` keys in `tools/validators/run_all.py` `main()`.)* The full lane list is in [AuthoringHarness](../Tooling/AuthoringHarness.md) §Tools.

## Deliberate rejected alternatives

- The compile-time catalog repoint (rollback = source change + rebuild) — RETIRED for the selector.
- Approval as a manifest `status` mutation — REJECTED (a blanket per-row runtime status-gate breaks
  `deprecated`/pinned-historical back-compat); approval is the external control-boundary artifact instead.
- A missing/corrupt compressed artifact has TWO policies at two lifecycle points: the release/acceptance
  gate MUST fail (prove the compressed path ran, the fallback did not); the audience runtime may fall back
  visibly to the consumer's uncompressed path — never silent black.

## History

- 2026-07: the release model (four records, freeze/approve/activate, selector-based install roots) was designed and built inside the IMRSV platform, replacing a compile-time catalog pointer.
- 2026-07-19: `matterlib-0.1.0` was frozen and approved (`approved_at` in its approval artifact); pilot recovery was proven live (0.1.0 → 0.0.1 and forward) against a consumer's install root.
- 2026-09-23: brought home; consumer-side deploy, install-discovery, cache invalidation, `ReleaseConflict` and the audience gate moved to [Consumers](../Consumers.md); annotated against R1 (producer does not deploy into consumers) and R7 (0.1.0 is a pilot).
