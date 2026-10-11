# Research — What the platform's first packaged build of Studio takes from the library

**Opened:** 2026-10-11 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `BI` (ids `BI-Qn`, `BI-Fn`). **Pass 1** is written from the platform's side. The library's review of it against its own tree is a later pass, as `260928_R_PlatformAppearanceAsks.md` Passes 5–6 were.
**Requested by:** the IMRSV platform's work on **its first packaged build of Studio** — the app made by Unreal's Packaging and run from its own folder, with its own copy of the Stage runtime beside it. The hand-over is a step of that work's plan, which the lead accepted on 2026-10-11.

**Question:** when a consumer makes a packaged build, what of the library does that build carry, where does it take it from, and what does the library need to promise for that to keep working?

**Extends, does not replace:** `PlatformDependencies.md` rows **P3** (*ship the library with packaged builds*) and **P19** (*Studio takes the dev install*), and [ReleaseModel](../../specs/Distribution/ReleaseModel.md) for the install layout the build copies.

**Public-repo note.** The platform's planning is private. It is summarised here by what it does with the library and what it needs — no platform paths, code or ruling ids.

**Measured at:** `b43fa65` (2026-10-11), the checkout the dev install served from on the machine that made the build.

---

## The short version

- **A packaged build of Studio now carries a Matter Library install.** One release: the one the install's selector names. It sits beside the build's own Stage runtime, where the runtime looks first.
- **It is assembled when the build is made, from the dev install** (P19) — the consumer's build copies the release folder file by file, **through** the dev install's links into this repo's working tree. What lands in the build is real files; no link, and no path back to a checkout.
- **So P19's planned copy mode is not needed for this.** The consumer does the copying itself, at the one moment a link-free install is wanted.
- **P3 is half-answered, from the consumer's side:** a build does ship a library. It ships the dev install, not a published release bundle, because no bundle exists to take.
- **Three things are asked of the library** — none is a material, none is urgent: a promise that a release folder is self-contained (A1), an identity a build can record for what it carried (A2), and a word on whether a build made for other people may carry drafts and candidates (BI-Q1).

---

## Pass 1 — What the build does, and what it needs

*Written from the platform's side, 2026-10-11.*

### The build, as it touches the library

- **BI-F1 — One release is carried, by name.** The build reads the install's `active-release.json`, takes the release it names, and carries that file plus `releases/<name>/` whole: the catalog, `materials/` and `textures/`. On the day measured the name was `matterlib-dev` and the carried install was **162 MB**; the full dev install on that machine, with two older releases beside it, was 485 MB.
- **BI-F2 — Nothing else of the install is carried:** not the other installed releases, not the audit trail of release activations, not a tool's backup copy of the selector. The runtime was read to consult only the release the selector names.
- **BI-F3 — The copy goes through the links.** In the dev install `materials/` and `textures/` are links into this repo's working tree (`serve_to_stage.py`). The consumer's build walks them as folders and copies each file. In the build they are plain folders of plain files.
- **BI-F4 — Checked with the checkout out of reach.** The build's own Stage runtime was started with this repo's checkout hidden from it, and asked for its library. It listed **88 articles a Creator can pick, of the catalog's 89** — the 89th is the system missing-material article, which is not Creator-selectable and is not listed by design. All 89 files the catalog names were real files inside the build; none was reached through a link; none was listed and missing.
- **BI-F5 — The build records what it carried.** Each build writes a stamp. For the library it holds the release's name and the commit of the checkout the dev install was serving — `matterlib-dev, b43fa65` on the first one — because the dev install has a name and no version of its own.
- **BI-F6 — The first such build is for one machine,** the one that made it. It carries `matterlib-dev`: this repo's working tree as it stood, drafts and candidates included.

### The asks

| # | Need | Why it matters to a packaged build | What exists today |
|---|---|---|---|
| A1 | **A release folder is self-contained, as a rule and not by luck:** every file its catalog names resolves inside `releases/<name>/`, and nothing in it points outside that folder — in a published release and in the dev install alike, once its links are followed. | A build that carries one release folder and nothing else works only while this holds. If an article ever named a file in another release's folder, or beside `releases/`, the build would list it and not find it. | It holds today (BI-F4: 89 of 89). [ReleaseModel](../../specs/Distribution/ReleaseModel.md) calls a staged release *self-contained per release* (step 2) and the planned bundle *self-contained* (step 6); the platform found no line that says it of the dev install once its links are followed. Only those two steps were read for this. |
| A2 | **An identity for an install that a consumer can read from the install itself** — a content version, a hash or the source commit, carried in the served catalog or beside it. | A build's stamp should say what library it carries without the checkout that served it still being there to ask. Today the consumer asks the checkout for its commit (BI-F5), which says nothing about uncommitted work in the tree that was served. | A published release has its name and version, and the planned bundle is *hash-locked* (ReleaseModel step 6) — that would be the identity. The dev install has the name `matterlib-dev` and nothing that changes when its content does. |
| A3 | **P19's copy mode is not needed for packaged builds.** If it is still wanted for another reason, that reason is the library's; this consumer no longer has one. | So the mode is not built on this consumer's account. | P19 lists it as *(planned)*, *"built only if Studio's machine needs it"*. |

### Questions for the library

- **BI-Q1 — May a build that goes to other people carry the dev install?** It holds drafts and candidates, and its content is whatever the working tree was that day. The library's rule is that consumers take releases, never a checkout (R1). The first build stays on the machine that made it, so nothing is breached yet; the question is what a build for others should refuse. The platform can make its build refuse a release named `matterlib-dev` when it is kept for others — if the library says that is the rule.
- **BI-Q2 — When the release bundle exists (P1 – P3), is it installed into the same layout** — a selector and `releases/<name>/` — so that a build carries a bundle's install exactly as it carries the dev install today? If the layout changes, the consumer's build rule changes with it.
- **BI-Q3 — Is the selector's one key a stable thing for a consumer to read?** The build reads `active_release` from `active-release.json` with a pattern, not a JSON reader. [ReleaseModel](../../specs/Distribution/ReleaseModel.md) is where the platform would look for a change.

### What the platform does next

- Nothing waits on the library. The build works today on the dev install.
- When A2 exists, the build's stamp records the install's own identity in place of the checkout's commit.
- BI-Q1's answer decides one refusal in the platform's build tool.

---

## A suggested ledger note — for the library to write or reword

Not written into `PlatformDependencies.md` from here; that file is the library's.

- **P3** — *reported by the platform, 2026-10-11:* a packaged Studio build now carries a Matter Library install — the selector and the one release it names, as real files, copied through the dev install's links when the build is made. Checked with the checkout hidden: 88 Creator-selectable articles listed of 89, every catalog file present. Not verifiable here (private code). **Still open:** the build carries the dev install, not a published release bundle (the row's pairing).
- **P19** — *reported by the platform, 2026-10-11:* the copy mode is not needed for packaged builds; the consumer's build copies through the links itself (`261011_R_PlatformBuildInstallAsks.md` A3).
- **A new row, if the library takes A1 and A2** — *a release folder is self-contained by rule; an install carries an identity a consumer can record.* Owner: Matter Library. Pairs with: the release bundle and the consumer contract.
