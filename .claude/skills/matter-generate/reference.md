# A row's reference sheet — what a recipe needs, in one read

Kept beside `/matter-generate` so a row starts from this page and not from the specs
(`MasterSet.md` 50 KB, `Identity.md` 17 KB, `Taxonomy.md` 11 KB, `recipe.schema.json` 11 KB). It
restates their rules and never overrules them: open the spec a section names only for a question
this page does not answer. **Matches the specs as of 2026-10-16.**

**The closed sets are not copied here.** `uv run tools/converters/wishlist.py rules` prints them
from the gate's own tables: the masters, the taxonomy, the scale tags with their lengths, the
overlay cap, the Creator ports, and the overlays and masks on disk. Run it once per session.

## Masters (`MasterSet.md`) — the material decides; the class is only a typical default

| Master | For | The recipe keys it needs, beyond the common ones |
|---|---|---|
| `Opaque` | the ~85% workhorse: stone, wood, soil, most mineral, metal, ceramic, cementitious, composite, plastic, polymer, coating, sand, cotton, denim, grass | `base_color_const` or `base_color_tex` · `roughness_const` or `_tex` · `metalness_const` or `_tex` · `specular_ior`; optional `normal_tex`, `coat_*` (a glaze, a varnish), `fuzz_*` (velvet), `specular_roughness_anisotropy` (brushed) |
| `Masked` | cut-outs: lace, perforated metal, a leaf card | Opaque's keys, plus `opacity_tex` **or** `cutout_map: true`, and `opacity_cutoff` |
| `Hair` | hair fibre on cards (hair, brows, lashes) | `cutout_map: true`, `base_color_map: true`, `thin_walled: true`, `subsurface_weight`, `subsurface_color`, `specular_weight: 0`; never `opacity_cutoff` |
| `TranslucentThin` | window glass, resin, thin or clear plastics | `transmission`, `thin_walled: true`, `specular_ior`; the port `transmission_color` **always** |
| `TranslucentThick` | gems, liquids, thick glass, lead crystal | `transmission`, `specular_ior`, `transmission_depth`; the port `transmission_color` **always** |
| `Subsurface` | marble, jade, wax; skin, a nail over its bed | `subsurface_weight`, `subsurface_color`, `subsurface_radius` (metres) with `subsurface_radius_scale`; `subsurface_scatter_anisotropy` for skin (about 0.8) |
| `TwoLayer` | rust on steel, paint on wood: layer 2 IS the material | `layer2_*` (textures or constants), `maskset_tex`, `layer_blend_balance`, `layer_blend_contrast`; `maskset_blend` must be non-zero |
| `Emissive` | LEDs, neon, virtual lights | `emission_color`, `emission_luminance`; both as ports **always** |
| `system` | reserved for `IMRSV_MissingMaterial`; no article declares it | — |

**Common to every recipe** (`recipe.schema.json`; any other key is refused): `name`, `path`, `master`, `domain`, `class`, `scale_tag`, `meters_per_tile`, `lcd_ports`, `contributor` (`"MatterBot"` for the library's own), `_comment`, `sources`. A batch row adds `status: draft`, `summary` (one public line, 160 chars at most), `search_words` (lowercase, synonyms in), `origin` (`scan`, `procedural` or `measured`, plus `agent-drafted`), and `label` only where the name the tokens derive reads badly. A colour is a `"r, g, b"` string in linear sRGB. A Character article (`group`, `species`, `part`, `fits`) is not a Matter row; Phase15 and Phase18 rule it.

`lcd_ports` (the list: `rules`): the UV ports only with textures; a deposit's `overlayN_color` with its density.

## Taxonomy (`Taxonomy.md`; the classes: `rules`) — the folder only, never the name

Leather is `textile`. Fired clay is `ceramic`; unfired clay is `soil`; cement, concrete and plaster are `cementitious`. `atmospheric` is out of scope. `biological` holds generic living matter only; a picture painted for one part mesh is Character. Never add a class to reach a master. A wall, a floor or a body is not matter (D1): one substance per article.

## The name (`Identity.md`) — `Material_Variant_Condition_Detail_sNN_vNN`

Exactly six tokens, PascalCase, 63 chars at most, `[A-Za-z0-9_]`. Material is the matter or species (`Oak`, not `WhiteOak`, unless the source says so) · Variant the look (`Natural` by default; `Polished`, `Brushed`, `Weathered`) · Condition the damage dialled up (`Clean` for a new draft) · Detail the other layers dialled up (`Base` for a new draft). The name says what is **dialled up**, never which layers are **carried**. A see-through colour or a light's colour is a Creator setting (`transmission_color`, `emission_color`), not a new article. `vNN` is the next free integer for the stem across `tools/converters/recipes/` and `MatterLibrary/materials/`; before the first release a redo rebuilds `v01` in place.

## Scale tags (`NamingConventions.md`; Phase19 D-9; the tags and lengths: `rules`)

`meters_per_tile` is **exactly** the tag's length. A scan at another size (0.4 m, 3 m) is re-made at an option's size or not used, never stretched (gate G9). A param-only article says `s01`.

## Wear layers (lead ruling C1; `MasterSet.md` §Overlay/MaskSet model)

Every article carries all the layers relevant to its matter, every slider at 0, up to the cap (`rules`). Overlay 1 is the damage layer. A reference article in `utility/virtual` carries none. **`Dust01` is a deposit**: its entry also carries `"color_port": "overlayN_color"` and that port goes in `lcd_ports`. A mask's `G`/`B`/`A` channels gate overlays 1/2/3: put each overlay in the slot whose gate fits it (the mask generator's docstring says which), except on `Grime01` and `Crevice01`, which predate that design.

The layers on disk are in `rules`; `brief` checks a row's own and names a missing one, which is made first (`/matter-generate` §3a). Known faint (F-P11-7, F-P11-8): `Scratches01`, `Fingerprints01` and `Scuffs01` move nothing on most matter. Report it; never fudge the recipe.

## Grounding

`uv run tools/converters/lookup_physically_based.py search <word>`, then `show "<Exact Name>"`: copy `used` into the recipe and the `source` record into `sources`, unchanged. No entry: your own values, plus `{"kind": "judgement", "why": "…"}`. A scan: `import_ambientcg.py search`, `info`, `import` (CC0 only).

**Start a row with `uv run tools/converters/wishlist.py brief <row>`**: the row, what is on disk for its stem, which of its layers exist, the nearest recipe for its master (copy its shape) and the Physically Based entries matching its Material token, in one call.
