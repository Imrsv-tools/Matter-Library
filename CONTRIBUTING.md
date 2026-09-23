# Contributing to the Matter Library

Thank you for helping build the Matter Library, a community material library that anyone can use. This page covers **what you agree to when you contribute**, **what we can and cannot accept**, and **how a material gets in**.

> **Status (2026-09-23):** the project is still being built, not in production. The contribution path works, but it is not yet push-button: the validation gate needs a local toolchain (see §Checks), and continuous integration (CI) is not wired up yet. Expect a maintainer to help you through your first contribution.

## 1. What you agree to

**Materials, textures and their data are dedicated to the public domain under [CC0-1.0](LICENSE-CONTENT.md).** Code is licensed under [Apache-2.0](LICENSE). When you open a pull request, you agree that:

- **Content** you contribute (`.mtlx` articles, textures, recipes, release and provenance data; the full list is in [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md)) is dedicated under **CC0-1.0**. You keep **no rights** in it, and neither does the project.
- **Code** you contribute (tools, the Blender add-on, docs) is licensed under **Apache-2.0**, the same terms as the rest of the code.
- **You have the right to make that dedication.** It is your own work, or it is derived only from sources that are themselves CC0-dedicable (§2).

Put this line in your pull request description; it is your affirmation:

> I dedicate the content in this pull request to the public domain under CC0-1.0 and license the code under Apache-2.0. I have the right to do so, and every third-party input I used is CC0-dedicable.

**Credit is given, not traded.** We list contributors in [`CREDITS.md`](CREDITS.md), and we ask users of the library to credit it. Neither is a condition of the licence: CC0 means no one is *required* to credit anyone.

## 2. What we can accept — the shipped-pixel rule

**No pixel ships in a release unless its source is recorded and it is CC0-dedicable, with evidence.** ([AuthoringGoldenPath](docs/specs/Authoring/AuthoringGoldenPath.md))

| Source | Accepted? |
|---|---|
| **Your own photographs or scans**, processed by you | ✅ Yes |
| **Procedural textures** from a committed generator script (the script is the evidence) | ✅ Yes |
| **CC0 libraries** such as [ambientCG](https://ambientcg.com), recorded with the source URL and a hash of what you shipped | ✅ Yes |
| **CC-BY, CC-BY-SA, "royalty-free", "free for commercial use" or other non-CC0 licences** | ❌ No: they carry conditions CC0 cannot pass on |
| **Textures from a generative-AI tool** | ⚠️ Only if the tool's terms let you dedicate its output under CC0, and the provenance is recorded. Maintainers judge this case by case; when in doubt, don't. |
| **Anything you are not sure you have the rights to** | ❌ No |

## 3. How a material gets in

Every article follows the same contract. **Read these first:**
- [`docs/specs/Ontology/Identity.md`](docs/specs/Ontology/Identity.md): how to name it.
- [`docs/specs/Ontology/Taxonomy.md`](docs/specs/Ontology/Taxonomy.md): where it goes.
- [`docs/specs/Ontology/MasterSet.md`](docs/specs/Ontology/MasterSet.md): which master it is.
- [`docs/specs/Contract/MaterialXTemplate.md`](docs/specs/Contract/MaterialXTemplate.md): what the `.mtlx` must contain.

1. **Name it.** Use `Material_Variant_Condition_Detail_sNN_vNN`: ≤63 characters of `[A-Za-z0-9_]`, with a real-world scale tag. A new article starts at `v01`.
2. **Place it.** It goes under `MatterLibrary/materials/<domain>/<class>/`; its textures go under `MatterLibrary/textures/base/<domain>/<class>/…`, or `shared/` for overlays and masks. **Textures are tracked with Git LFS**, so install `git lfs` before you commit them.
3. **Write a recipe, not a `.mtlx`.** Articles are *generated*: add `tools/converters/recipes/<Stem>.json` (copy the closest existing recipe), then run `python tools/converters/build_proof_subset.py tools/converters/recipes/<Stem>.json` to assemble the article deterministically. Don't hand-edit the generated `.mtlx`.
4. **Record provenance** for every new texture: source, licence (`CC0-1.0`), and evidence (a URL and a hash, or the generator script). See `library/provenance/`.
5. **Run the checks** (§Checks) and include the output in your pull request.
6. **Open a pull request.** Include the affirmation line from §1, a render or screenshot of the material, and the check output.

**Changing an existing material?** Once a material version has shipped in a release it is **frozen**. Make a new version (`vNN+1`); never edit the old file in place ([Manifest](docs/specs/Contract/Manifest.md) §Immutability).

## 4. Checks

```bash
python tools/validators/run_all.py
```

This is the structural gate: name, schema, the OpenPBR template, the parameter contract, determinism, and release records.

> **Known gap (measured 2026-09-23):** the gate needs the **MaterialX 1.39.5** Python module, which is not bundled yet. Install it with `pip install MaterialX==1.39.5`, or use the conda recipe in `tools/usd-toolchain/`. Compression and staging lanes also need `compressonatorcli` and skip without it. Making this one command on a fresh machine, and running it in CI, is planned work (see `docs/Planning/Roadmap.md`).

## 5. From contribution to release

A merged pull request adds your article to the **source collection**. It gets a status (`draft` → `candidate` → `approved`) when a **maintainer** adds it to a release manifest in `library/releases/`, and it reaches users only when a curated **library release** that includes it is approved, after review, parity checks and curation. Merging is not a promise of inclusion; releases are curated ([ReleaseModel](docs/specs/Distribution/ReleaseModel.md)).

## 6. Code and docs

- Tools live in `tools/`, the Blender add-on in `blender/addons/`, and the specs in `docs/specs/`.
- Vocabulary is fixed in [`docs/Glossary.md`](docs/Glossary.md): use the established term, or propose a change there first.
- Naming rules are in [`docs/NamingConventions.md`](docs/NamingConventions.md).
- The project records design ahead of what is built: **never delete a specified capability because it isn't built yet.** Mark it `(planned)` or `Drift` with a date instead.

## 7. Where to talk

Open an issue on [GitHub](https://github.com/Imrsv-tools/Matter-Library/issues) for questions, proposals or problems.
