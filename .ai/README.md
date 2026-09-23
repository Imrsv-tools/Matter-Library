# `.ai/` — Agent Operational Surface

> **What this folder is for:** the **tool-agnostic operational layer** that helps any AI agent (Claude, Codex, Gemini, …) work in this repo. It holds the *truth* about agent operation — orientation, agreements, and the verbs agents run. Each tool keeps its own thin pointers (`.claude/`, `.codex/`, …) that reference this folder. **`.ai/` is the source of truth for agent operation; tool folders are disposable pointers to it.**
>
> **`.ai/` is THIN — planning is not here.** The full `Planning/` tree (roadmap, phases, research, support) lives at **`docs/Planning/`**, alongside durable product specs, because planning is durable human-discoverable project truth, not agent-operational scratch.

## Accepted contents (the whole allowed set)

| Entry | Kind | What it holds | Status |
|---|---|---|---|
| `AI_Orientation.md` | entrypoint | identity, repo map, build/test | **present** |
| `AI_WorkingAgreement.md` | agreements | the engineering agreements | **present** |
| `README.md` | registry | this file — the accepted-folder list + the rule before adding anything | **present** |
| `commands/` | **verbs** | the procedures agents invoke + `LOCAL_DELTAS.md` | **present** |
| `reference/` | **nouns** | passive facts the verbs look things up in. Create on the first real reference doc. | optional |
| `agents/` · `agent-skills/` | roles / framework config | tool-agnostic role specs / external-skills config. Create only when actually run. | reserved |

## What does NOT belong in `.ai/` (and where it goes instead)

| If it's… | It belongs in… |
|---|---|
| a planning doc (roadmap, phase, research, support) | `docs/Planning/` |
| durable product / architecture specs | `docs/` |
| durable methodology / the carried blueprint | `Methodology/` |
| durable learnings (engineering memory) | `docs/Learnings/` (create on first lesson) |
| a tool's own bindings / hooks / settings | `.claude/` (and future `.codex/`) — **never** `.ai/` |

## Before adding anything to `.ai/` — the checklist

1. **Is it agent-operational truth?** (orientation, a verb, a role, a reference). If it's a **planning doc** → `docs/Planning/`; if it's a durable product record a human browses → `docs/`. Neither belongs in `.ai/`.
2. **Is there already a better home?** Check `docs/Planning/`, `Methodology/`, `docs/` first.
3. **Is it a tool binding?** Hooks, settings, slash wrappers → `.claude/`, not `.ai/`.
4. **New top-level folder?** That's a convention change — register it here first, don't squat.
