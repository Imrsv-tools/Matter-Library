# Makeup Pieces — what a piece is, and how a list of them becomes a character's makeup

> **IN FORCE (2026-11-02, Phase26 *Makeup on the Skin*, [`Phase26_MakeupOnTheSkin.md`](../../Planning/Phases/Complete/Phase26_MakeupOnTheSkin.md)).** Four pieces ship on `MakeHuman_Body_v01`: a red lip colour, a clear lip gloss, a plum eyeshadow and an arrow tattoo. The lead judged them on the light and the dark skin in the library's Unreal look view, and the three tools' agreement on the rig's sheet (*"The lips are red"*, then *"yes"* at the other four clicks). The format was agreed with the platform, whose own merge follows it (RD-P26-5, RD-P26-6). The skin's side, the two pictures a merge writes and how the master mixes them: [LCDSchema §Makeup layer](../Contract/LCDSchema.md#makeup-layer-the-characters-supplied-at-binding).

## What a piece is

A **piece** is one bit of makeup, or one mark a Creator adds to a character: a lip colour, a gloss, an eyeshadow, a tattoo. It is a library entry with a name, a record and one picture. **A composition** (a character's makeup) is a list of pieces with their settings; a **merge** turns that list into the character's two makeup pictures.

A piece is **paint, laid over the skin**. A skin's own freckles, moles and veins are the skin's, never pieces (RD-PSM-1).

## The two kinds

- **A fitted piece** is a coverage shape on one mesh's atlas: a greyscale PNG at the mesh's map size (2048² on `MakeHuman_Body_v01`), white covered, black not. It is **made in 3D on the body and baked per layout** ([SkinMaps §Authored on the body](SkinMaps.md#authored-on-the-body-baked-per-layout--ruled-2026-10-26)), so it fits one mesh version. A lip colour, a gloss, an eyeshadow.
- **A placed piece** is a square **stamp**, an RGBA PNG (RGB a colour multiplier, white for a one-colour piece; A coverage), plus its `size` in metres. It is laid anywhere on the body by a point, a size and a turn. A tattoo, a mark.

## The record

`MatterLibrary/makeup/<Name>.json`, its picture under `MatterLibrary/textures/fit/makehuman/makeup/` (`<Name>_coverage_sUKN.png` for a fitted piece, `<Name>_stamp_sUKN.png` for a stamp). The fields:

| Field | Meaning |
|---|---|
| `name` | `Makeup_<Kind>_<Variant>_vNN` ([Identity](../Ontology/Identity.md) §Makeup pieces) |
| `kind` | `fitted` or `placed` |
| `fits` | a fitted piece's mesh (a [part mesh](../../Glossary.md) id) |
| `coverage` · `stamp` | the picture, relative to the record |
| `size` | a placed piece's default size, metres across |
| `carries` | `colour`, `finish` or both. A clear gloss carries finish only and writes no colour |
| `defaults` | the controls' defaults: `colour` (linear rec709), `strength` (0–1, scales coverage), `finish` (a target roughness, matte 1 to wet 0) |
| `channels_planned` | the channels the format keeps for later: **relief** *(planned, RD-P26-1: a raised scar, with a third slot)* and **pigment** in place of colour *(planned, Skin Layers: a bruise, a flush)* |
| `summary` · `contributor` · `licence` · `origin` · `script` | as any entry's |

**Licence:** CC0. A piece is procedural or hand-made, never from a photograph or a scan (RD-SKM-2); AI may draw a tattoo design only as tone-free content (RD-SYN-1).

## A composition

Stores **no pixels** (R-PSM-5), only names and settings:

```json
{"mesh": "MakeHuman_Body_v01",
 "pieces": [{"piece": "Makeup_LipColour_Full_v01", "colour": [0.45, 0.01, 0.02], "finish": 0.35},
            {"piece": "Makeup_LipGloss_Clear_v01"},
            {"piece": "Makeup_Tattoo_Arrow_v01", "point": [0.4455, 0.2258, 0.2456], "size": 0.042, "turn": 0}]}
```

Each setting defaults to the record's. A placed piece adds `point` (on the rest-pose surface, metres: x to the body's left, y up, z forward), `size` and `turn` (degrees). Examples: `tools/parity/makeup/`.

## The merge

- Pieces lay down **in list order, each over the ones before** (straight-alpha *over*), separately in the colour and the finish picture. A piece writes only what it `carries`.
- A piece's coverage × its `strength` is its alpha; its colour × a stamp's multiplier is its colour.
- Each layer's value is pushed past its edge where coverage is 0, so a filtered lookup at an edge never blends toward black.

**Where a stamp lands** (RD-P26-6):
- It is centred on the covered texel nearest its `point`.
- **Turn 0** points the stamp's up along the body's rest-pose +Y, projected onto the tangent plane there. The turn is **clockwise about the outward normal**, seen from outside.
- A texel takes the stamp only where its rest-pose normal faces the point's (dot > 0) and it lies within half the stamp's size of the tangent plane, so a stamp never prints through a limb or onto a thigh beside the hand.
- A texel's stamp coordinate is its rest-pose position projected into that tangent frame.

**The reference merge** is `tools/converters/fit/merge_makeup.py` (units: `test_merge_makeup.py`). It is the **known answer**: a consumer's live merge must produce the same pictures for the same list (RD-P26-4).

## How to make one

`uv run tools/converters/fit/gen_makeup_pieces.py` makes the library's pieces and the example compositions. A new fitted piece is a function there that writes a coverage from the body's per-texel position, normal and regions (`gen_synth_skin.fields`, `face_landmarks`), as the eyeshadow does from each eye; a new stamp is a drawn RGBA picture. To see one: `tools/parity/look.py <skin> --makeup <composition> --lips-skin` (the look) and `tools/parity/rig.py --character <skin> --makeup <composition>` (the three tools).

## Not yet

- **Relief** and **pigment** pieces, above *(planned)*.
- **Multi-colour stamps:** a stamp's RGB is a multiplier a later piece may use; the first pieces are single-colour.
- **Larger pictures:** 2048² first; 4K and 8K after (RD-P25-20). At the hand view's ~5 px/mm the tattoo's edge steps visibly (~0.75 mm a texel on the back of the hand).
- **Makeup on the `Lips_*` and `Nail_*` articles** (polish is a nail article, Q-PSM-4).
- **The site file listing the pieces** *(planned, 2026-11-02)*: today only the dev catalog lists them ([RuntimeCatalog §Groups](../Contract/RuntimeCatalog.md)).
