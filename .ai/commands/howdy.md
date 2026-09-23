Session onboarding for **the Matter Library** — the **lightweight front door**. Orient, glance at what's active, and be ready to **talk through ideas or start work**. Deeper reads belong to the working verbs (`/research`, `/discovery`, `/plan`, `/execute`). Howdy stays light so it loads fast and sets up a conversation, not an execution.

## Read (in this order)

1. `.ai/AI_Orientation.md` — identity, repo map, build/test entry points. *(The "where everything lives" core.)*
2. `.ai/commands/LOCAL_DELTAS.md` — where this project diverges from the carried upstream method. *(Read once per session so the other verbs don't surprise you.)*
3. `.ai/AI_WorkingAgreement.md` — the engineering agreements. *(So idea-sparring stays inside the principles.)*
4. **Glance** at `docs/Planning/Roadmap.md` — what's active + seeded. **Glance only — don't open the active phase doc** (that's `/discovery`'s job).

**Not pre-loaded** (pulled by the verb that needs them): the active phase doc, the full `Methodology/AgenticEngineering_Workflow.md`, and any `docs/` specs. Know they exist; reach them in ≤1 hop.

## This is the front door — the working verbs go deeper

Howdy orients; it doesn't work a unit. When the conversation firms into scoped work, escalate:

- **`/research <topic>`** — gather + park a `docs/Planning/Research/YYMMDD_R_*.md` doc; commit to nothing.
- **`/quick-fix <thing>`** — a shallow, self-contained change in one context; the commit is the record.
- **`/discovery <PhaseDoc>`** — gather + structure thinking for a phase.
- **`/plan <Phase>`** — author the implementation plan.
- **`/execute <Phase>`** — run the hardened phase.

Prefer the **smallest** unit that fits. Most work is a `/quick-fix` or a `/research`, not a full phase.

## Search hygiene (avoid permission-prompt spam)

Prefer the **Grep / Glob / Read** tools directly (they never prompt). For big sweeps, fan out **in parallel** with **Bash-less** search agents (prompt them "use ONLY Read/Grep/Glob/LS"). **Never a search agent carrying the Bash tool** — it shells out and prompts on every call. When using Bash directly: literal absolute paths, no `cd`/pipes/redirects, one command per call.

## Output

You read all that to orient **yourself** — **do not parrot it back.** The end output is a **≤2-line orientation + a ready prompt**:

1. **Orientation line** — `📍 <branch> · <clean | N uncommitted> · last: <most recent completed phase, or "no phases closed yet"> · active: <what's in flight — a phase, a live research thread, or "nothing in flight">`. Pull branch + cleanliness from `git -C <repo root> status -sb`; last + active from the Roadmap glance. (`git status -sb` also reports ahead/behind against `origin/main` — that's the cheap signal; **howdy stays light and does not call `gh`**.)
2. **Ready** — hand back with on-ramps: *"Ready — want to **research** something, **spike** a quick idea, or **kick off a phase**?"* At most one clarifying question, only if something essential is missing.
3. **Attention line — ONLY if something's actually off** (dirty tree, an uncommitted snapshot, **commits ahead of `origin/main`** — work that is committed but not pushed does not exist from anywhere else, per `.ai/AI_WorkingAgreement.md` §Working With the Lead). No-news → omit and stay at two lines.

Ultra-minimal one-line form is fine when quiet: *"Caught up — `main`, clean, no phases closed yet, nothing in flight. Where to?"*
