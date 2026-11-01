# Phase24 — One Validated Skin

**Status:** SEEDED (2026-11-01). Numbered on the lead's word. In OMF's session: *"today's hm08, Matter Library hosts it … it will seed the phase"*. Here: *"Just ONE set please we need to stop genearting 5 shades... let's get one complete set build and tested,,, then we can add variety."* **Split the same day** (the lead: *"Split and seed"*, RD-OVS-6). The image model's skin is [`Phase25_AiSkinStructure.md`](Phase25_AiSkinStructure.md), which runs against this phase's judge. **`/discovery Phase24` opens Pass 1** and confirms or rewrites this doc.
**Written on:** the machine with Unreal, at `de4f5d9`.
**Seeded from:** [`../Research/261101_R_OneValidatedSkin.md`](../Research/261101_R_OneValidatedSkin.md) (OMF's input and protocol; the library's Pass 2; the lead's answers RD-OVS-1 … 6) · [`Complete/Phase23_SyntheticSkinSets.md`](Complete/Phase23_SyntheticSkinSets.md) (the maker, the look view's reference column, F-P23-2) · [`../../specs/Authoring/SkinMaps.md`](../../specs/Authoring/SkinMaps.md).

## Outcome

**One young woman's skin, complete (colour, shine, lips and nails), stands beside the scanned skin on the same body, and the lead cannot tell them apart at set distances, or names, part by part, what still differs. It is served as one finished set, ready for Studio when Studio can take it.**

*(Drafted from OMF's proposed Outcome, widened to the lead's "one complete set build and tested". Discovery confirms the words.)*

## Why this is a phase

- **It replaces breadth with one finished thing.** Phase21–23 made 6 tones × 3 people, and the lead's last word on them was *"they look totally fake but better"* (Phase22). Nothing has been judged against a real skin on the same body in one sitting with a fixed ruler.
- **It builds the judge every later skin is measured by,** Phase25's image-model skin first.
- **It decides the expensive things once, for one subject,** before variety multiplies them: what a complete skin set contains, the lips inside the body's skin, and the maker working at 8K.

## The one set — what "complete" means here

| Piece | What it is | Today |
|---|---|---|
| **Body skin** | One article on hm08, its lips included (the lips worn on the skin, as the bar's are). Its own colour map, **at 8K** (RD-OVS-2). | 2048², one per tone, lips separate (`Lips_*`), 6 × 3 |
| **Its shine set** | Its own roughness (a glossier lip zone and the T-zone), relief normal, cavity and scatter, made for this subject | Four maps shared by every skin |
| **Nails** | One nail article matched to the subject | One per tone |
| **The tone** | **The bar's own measured face average** (RD-OVS-1), not a Fitzpatrick article's | Six measured tones |
| **Held fixed** | the female hm08 body at its default age (RD-OVS-3), its eyes, card hair and brows, the look view's light, the views and distances, one atlas | — |
| **The subject's pigment fields** | Melanin and blood, kept beside the set as the maker's output. They are not shipped this phase; *Skin Layers* and Phase25 need them. | Internal to the maker |

**One tone, one person, one set.** No other tone, no other structure, no new draft articles.

## The plan — three steps, each ending in the lead's look

1. **The judge, at 8K** (OMF protocol steps 1–5):
   - In the library's look view (Unreal) on the machine with Unreal, three columns on one body at one size, 8K (OVS-8, RD-OVS-2):
     - **A**, the scanned bar: colour, specular and scatter from the platform's fit to hm08; local only, never in the tree (RD-P23-10);
     - **B**, today's III skin, shown at the same size;
     - **C**, the candidate.
   - The fixed views: face front, three-quarter and profile; close-ups of an eye, the lips, and the cheek with the nose; at ~1 m and ~40 cm.
   - **Click 1, the ruler:** A must read real and B fake in the lead's words, or nothing after counts.
2. **C, the pigment maker tuned to the bar, at 8K.**
   - One structure fitted to the bar's face region by region (Phase23's profiles as the screen), at the bar's tone.
   - Its own shine set, with the lips in.
   - The maker and its checks run at 8K. Today they assume 2048² (the maker, the look view's resampling, the recipe checks).
   - **Click 2:** A · B · C, iterated until C passes or the gap is named by part.
3. **The set finished and served:**
   - its nails, its provenance;
   - served to the dev install and published as a dev snapshot;
   - **click 3: the set on the character in the lead's Blender,** with everything held fixed.
   - Studio's look follows when the platform draws the shine maps (P33, P34). The lead asks the platform to bring that forward (RD-OVS-4).

## Scope — as known at seeding

**In (candidate):** the three steps above; the maker, its shine maker and the look view at 8K; the lips inside the body skin for this subject; the subject's own shine set.

**Not now** (each has a home):
- **the image model's skin:** [Phase25](Phase25_AiSkinStructure.md), against this judge;
- **picture size, loading and performance tests, and a size per layer:** later phases (RD-OVS-2);
- **other tones, people and ages:** re-runs of the passed recipe (*Variety*, after);
- **marks and makeup on this subject:** *Skin Layers*, from this set's pigment fields;
- **the body's verdict:** the bar is a face scan, so the claim is the face (OVS-7);
- **a new body:** OMF's work. The re-bake onto it is the later test;
- **eyes:** *Eyes in the Shader*, held fixed here;
- **retiring the existing `Lips_*` articles and the 18 skins:** they stay as they are (§Don't Delete Spec Functionality);
- **Studio's side:** the platform's skin phase.

## Rulings carried

- **2026-11-01, OMF's session (recorded by date and content in the OVS doc):** OMF keeps the approach to realism; validate on one subject on today's hm08; this library hosts the phase.
- **RD-OVS-1 … 6 (the lead, 2026-11-01):**
  - the bar's tone;
  - start at 8K, and test sizes later;
  - the default age;
  - the lead asks the platform for the Studio side;
  - the lead supplies Krea 2 and FLUX.2 [klein];
  - the split.
- **RD-SKM-2:** no photograph of a person in what ships. The bar stays local (RD-P23-10).
- **RD-RO-2:** CC0. **RD-P21-3:** the average held to the tone.

## Questions for discovery

The lead's answers of 2026-11-01 (RD-OVS-1 … 4) close Q-P24-1 … 4 as drafted. What remains is discovery's own:
- what the 8K maker costs in memory and time, and which steps change for it;
- how the look view's three columns are built at 8K;
- where the subject's pigment fields are kept.

## Pointers

- `PlatformDependencies.md` P33 (a draft in the look-dev scene), P34 (draw the shine maps), P35 (keep the structure).
- The platform's character model of 2026-11-01 (lips in the body, nails separate, one merged makeup layer) arrives as its own asks. This phase does the lips for its one subject only.
