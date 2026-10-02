---
name: matter-batch
description: Work the next rows of the Matter Library wish list (library/wishlist.yaml). For each row, build the material the /matter-generate way (or, for a re-judge row, take the article on disk), put it through the parity rig in Storm, Blender and Unreal, read its own sheet, fix and re-run up to 3 times, commit it as a draft, and write a batch summary the maintainer reviews to keep or redo each row.
---

# /matter-batch — work the wish list

You are running **one batch** of the build loop (Phase11 Library Coverage). The argument is how many rows (default **5**) or the row names to take. Rows come from `library/wishlist.yaml`, worked by `tools/converters/wishlist.py`.

**The loop:** take a row → build it → rig it → read the sheet → fix and re-run (up to 3 rig runs) → mark it → commit it → next row. Then write the batch summary. **The maintainer judges sheets, not scenes,** and says keep or redo; you record it.

## Hard rules

- **Build by `/matter-generate` §1–5. Read that skill; do not work from memory.** Its rules hold here (recipe, never MaterialX · say what you could not do · run from the repo root with `uv run`), **except two, which this skill replaces:**
  - **You commit each built row as `draft`, locally** (lead, 2026-10-02, RD-P11-2). **Never push.** Never touch `library/releases/`.
  - **The judge is the rig, not the Storm preview,** and there is no USDLiveView hand-off (`/matter-generate` §6a). Its §6 critique is still written, from the rig's sheet.
- **Never overwrite what exists, except your own `redo` row**, which is rebuilt in place (`v01`; no versioning before the first release).
- **Never fudge a recipe to make the tools agree.** A difference a renderer causes (Storm draws see-through matter as transparency, not refraction; Phase05) is reported, not hidden. Fix the material only where the material is wrong.
- **The list says `kept`, never "approved".** Only `wishlist.py keep` writes an article's status.
- **Shared tree** (`.claude/CLAUDE.md` §Git): stage **explicit paths** only, `git status -s` and `git diff --cached --stat` before each commit, `git show --stat <sha>` after. A file you did not write is another session's.
- **No Claude co-author trailer.**

## 1. Take the rows

```sh
uv run tools/converters/wishlist.py next 5      # redo rows first, then the proving batches, then list order
uv run tools/converters/wishlist.py show <name>
```

Name the batch `<YYMMDD>-<n>` (the next free `n` for today in `library/batches/`). Say which rows you took, in one line each.

## 2. Build (a `build` or `redo` row)

Run `/matter-generate` §1–5 with **the row as the brief**: its name, slot, master, lane, scale, layer set and note are the research's draft, a reference, not an authority (§1 there). **A `redo` row carries the maintainer's note: that note is the brief's first line**, and the summary says what you changed for it.

- **Wear layers:** the row's four columns are overlays 1 · 2 · 3 · mask. A layer not in `MatterLibrary/textures/shared/` is made first (`/matter-generate` §3a), once, and shown dialled up on the rig's sheet (the sweep does this). **`Dust01` is a deposit** (`color_port`; `/matter-generate` §3).
- **The mask's channel design wins over the row's slot order.** A mask's `G`/`B`/`A` gate overlays 1/2/3 and each is drawn for a kind of layer (its generator's docstring says which: a damage band, a deposit band, handling marks). Put each overlay in the slot whose gate fits it, keeping overlay 1 the damage layer, and say on the summary when you reordered the row.
- **A layer near-invisible in the render** (on matter it cannot change much: roughening on a rough surface) is judged on a glossier row where one exists, or from the rig's own "where they differ" column; say which.
- **The recipe carries `"status": "draft"`** (after `name`).
- **A scan with no physical size** (`import_ambientcg.py` prints `meters_per_tile 0`; common for stone): set `meters_per_tile` by judgement from the feature size (grain, bands), record it as a `judgement` source, and say so on the summary.
- **A planned name that differs from the row's** (the skill's §1 re-plans it): `wishlist.py mark <old> queued --name <new>` before you continue. **A different way of making it** (no scan names the matter, so L3 becomes L2): `--lane L2`, and say why on the summary.
- **The gate:** `uv run tools/validators/validate_recipe.py <recipe>` per row; the full `run_all.py` once before the batch's last commit (§6).

A **`rejudge`** row skips this step: the article on disk is the subject.

## 3. Rig it, read it

```sh
uv run tools/parity/rig.py <stem> --sweep        # 4–10 minutes, three tools, ONE rig at a time (one GPU)
uv run tools/converters/wishlist.py verdict <stem>
uv run tools/parity/crop_sheet.py <stem> defaults "wear 3 at 1" "<a label>"   # the sheet's rows, readable
```

**Run the rig in the background and wait for its completion notice; do not poll it.** The whole sheet (`library/parity/<stem>/sheet.png`) is too tall to read: **Read the crops** of the rows that matter (the defaults, every layer at 1, any row `verdict` flags). Judge:
- **Does it read as the matter?** Colour, gloss, translucency, texture size against the floor's ruler.
- **The verdict per slider:** *moved alike* in all three is the bar. **ONE-SIDED** or **UNEVEN** names a tool that disagrees: find whether the material (fix it) or a renderer's known limit (report it) is the cause.
- **Seams and scale:** `verdict` prints both, and every slider that **moved nothing in any tool**. A seam flag the render does not show (a generator that tiles by construction, a ratio just over the check's threshold) is reported as a **flag, not confirmed**, with what you looked at; never shift a texture to pass the check.
- **None of these changes the status word** (`approved` = the three tools agree, the Glossary's), but each goes on the summary's **Verdict** line, plainly: a seam, a failed ruler, a declared slider that does nothing (a damage layer on matte matter: overlays can only roughen), a renderer that draws the matter differently (see-through matter). **Whether to keep over it is the maintainer's call;** your job is that they cannot miss it.

## 4. Fix and re-run — at most 3 rig runs per row

Fix the **recipe** (or the layer you made) and re-assemble (`build_proof_subset.py <recipe>`), then re-rig. After the third rig run, stop: mark the row `stuck` with why, in one sentence a person can act on.

## 5. Mark and commit the row

```sh
uv run tools/converters/wishlist.py mark <stem> built --batch <batch>     # or: stuck --why "…"
```

A **re-judge** row is marked `built` too (ready for review) once its sheet is read.

**One row at a time, through its commit.** While a rig runs you may read and plan the next row, but **write nothing for it** (no `mark`, no import, no `CREDITS.md` row) until this row is committed: `library/wishlist.yaml` and `CREDITS.md` are shared by every row, and an early edit rides into this row's commit. **New files are `git add`-ed by path first** (`git commit -- <paths>` refuses untracked files). Commit **this row's files and the list**, explicit paths: the recipe, the `.mtlx`, any base textures, a layer's script, PNG and provenance record, a scan's provenance and `CREDITS.md` row, `library/wishlist.yaml`. Message: `Batch <batch>: <stem> built as draft (<one-line verdict>)`. A `rejudge` row commits only the list. A `stuck` row commits its files too, as a draft, so the maintainer can see what failed.

## 6. The batch summary

Run `uv run tools/validators/run_all.py` (0 FAIL; the SKIPs are reported; its activation lane prints intended `[FAIL]` lines from negative controls, so read the SUMMARY line). Then write **`library/batches/<batch>.md`** and commit it with the list. **A batch touches no planning doc;** a phase running the loop records its own ledger.

```markdown
# Batch <batch> — <date>

<N> rows: <n> built, <n> stuck, <n> re-judged. Gate: <PASS/SKIP/FAIL counts>. Rig time: <minutes>.

## <stem> — built | stuck | re-judged · <slot> · <master> · <lane>
- **Made from:** <Physically Based entry / ambientCG asset id / generator script / judgement>; layers <1 · 2 · 3 · mask>, <any made here>.
- **Critique:** <4–8 lines, /matter-generate §6, written from the sheet>.
- **Verdict:** <all moved alike in Storm, Blender and Unreal | the rows that did not, and why>. Seams <ok/…>, scale <ok/…>. A keep sets <approved|candidate>.
- **Tries:** <n>; <what each fix changed>.
- **Sheet:** `library/parity/<stem>/sheet.png`
- **Review:** —
```

## 7. The review (the maintainer's)

Open each summary and each sheet for the maintainer. **They look and say keep or redo; they type no command.** Record each verdict:

```sh
uv run tools/converters/wishlist.py keep <stem>                  # recipe status: approved (all three alike) or candidate
uv run tools/converters/wishlist.py redo <stem> --note "<their words>"
```

Write their words, verbatim, on the row's **Review** line in the summary, and commit the recipes, the list and the summary together. A redo row is first in the next batch.

## Hand back

- **The batch:** `library/batches/<batch>.md`, one line per row (built / stuck / re-judged, the verdict).
- **What to look at first:** a stuck row, or a sheet that disagrees.
- **Next:** `wishlist.py counts`, and the next rows `next` would take.
