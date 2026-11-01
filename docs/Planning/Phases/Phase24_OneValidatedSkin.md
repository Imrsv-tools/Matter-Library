# Phase24 — One Validated Skin

**Status:** SEEDED (2026-11-01). Numbered on the lead's word. In OMF's session: *"today's hm08, Matter Library hosts it … it will seed the phase"*. Here, after asking for the next phase number: *"lets come up with a plan for getting a full set of skins completed and testable for the full concept... Just ONE set please we need to stop genearting 5 shades... let's get one complete set build and tested,,, then we can add variety."* This doc is the plan at seed altitude. **`/discovery Phase24` opens Pass 1** and confirms or rewrites it.
**Written on:** the machine with Unreal, at `5098900` + the merge of OMF's input.
**Seeded from:** [`../Research/261101_R_OneValidatedSkin.md`](../Research/261101_R_OneValidatedSkin.md) (OMF's input and protocol, and the library's Pass 2: this plan) · [`../Research/261101_R_SkinMapsFromAnImageModel.md`](../Research/261101_R_SkinMapsFromAnImageModel.md) (RD-AIS-1, RD-AIS-2) · [`../Research/261101_R_Spike_SkinMapFromImageModel.md`](../Research/261101_R_Spike_SkinMapFromImageModel.md) (the AI route, proven on hm08's head) · [`Complete/Phase23_SyntheticSkinSets.md`](Complete/Phase23_SyntheticSkinSets.md) (the maker, the look view's reference column, F-P23-2) · [`../../specs/Authoring/SkinMaps.md`](../../specs/Authoring/SkinMaps.md).

## Outcome

**One young woman's skin, complete (colour, shine, lips and nails), stands beside the scanned skin on the same body, and the lead cannot tell them apart at set distances, or names, part by part, what still differs. It is served for testing as one finished set.**

*(Drafted from OMF's proposed Outcome, widened to the lead's "one complete set build and tested". Discovery confirms the words.)*

## Why this is a phase

- **It replaces breadth with one finished thing.** Phase21–23 made 6 tones × 3 people, and the lead's last word on them was *"they look totally fake but better"* (Phase22). Nothing has been judged against a real skin on the same body in one sitting with a fixed ruler.
- **It is where the two makers meet:** the pigment maker (Phase23) and the image model (the spike), both judged against the same bar.
- **It decides the expensive things once, for one subject,** before variety multiplies them: what a complete skin set contains, the lips inside the body's skin, how an AI-made skin enters the library.

## The one set — what "complete" means here

| Piece | What it is | Today |
|---|---|---|
| **Body skin** | One article on hm08, its lips included (the lips worn on the skin, as the bar's are). Its own colour map. | Colour per tone, lips separate (`Lips_*`), 6 × 3 |
| **Its shine set** | Its own roughness (with a glossier lip zone and the T-zone), relief normal, cavity and scatter, made for this subject | Four maps shared by every skin |
| **Nails** | One nail article matched to the subject | One per tone |
| **Held fixed** | the female hm08 body, its eyes, card hair and brows, the look view's light, the views and distances, one atlas and one picture size for every column | — |
| **The subject's pigment fields** | Melanin and blood, kept beside the set as the maker's output. They are not shipped this phase; *Skin Layers* needs them next. | Internal to the maker |

**One tone, one person, one set.** No other tone, no other structure, no new draft articles.

## The plan — four steps, each ending in the lead's look

1. **The judge** (OMF protocol steps 1–5):
   - In the library's look view (Unreal) on the machine with Unreal, three columns on one body:
     - **A**, the scanned bar: colour, specular and scatter from the platform's fit to hm08; local only, never in the tree (RD-P23-10);
     - **B**, today's skin at the bar's tone;
     - **C**, the candidate rows.
   - The fixed views: face front, three-quarter and profile; close-ups of an eye, the lips, and the cheek with the nose; at ~1 m and ~40 cm.
   - **Click 1, the ruler:** A must read real and B fake in the lead's words, or nothing after counts.
2. **C1, the pigment maker tuned to the bar.** One structure fitted to the bar's face, region by region (Phase23's profiles as the screen), with its own shine set and the lips in. **Click 2:** A · B · C1.
3. **C2, the image model's skin as a structure** (RD-AIS-1: Krea 2 first, FLUX.2 [klein] as the fallback).
   - The spike's projection onto hm08, extended to the body.
   - Masked at the brows, lids and lips; its light removed; inverted to melanin and blood through the maker's skin model.
   - Recomposed and calibrated by the maker like any structure.
   - **Click 3:** A · B · C1 · C2.
   - **If C2 wins, the lead's narrow re-ruling** follows: an AI-made *structure* is accepted (OMF OVS-3; RD-SKM-5 and RD-SYN-1 are otherwise unchanged).
4. **The winner finished and served:** its nails, its provenance (*AI-assisted*, model named, if C2), served to the dev install and published as a dev snapshot. **Click 4: the set on the character in the lead's Blender,** with everything held fixed. Studio's look follows when the platform draws the shine maps (P33, P34).

## Scope — as known at seeding

**In (candidate):**
- the four steps above;
- the lips inside the body skin for this subject;
- the subject's own shine set;
- the maker taking an outside pigment field (C2's entry);
- the projection pipeline from the spike, made a library tool.

**Not now** (each has a home):
- **other tones, people and ages:** re-runs of the passed recipe (*Variety*, after);
- **marks and makeup on this subject:** *Skin Layers*. It starts from this set's pigment fields;
- **the body's verdict:** the bar is a face scan, so the claim is the face (OVS-7);
- **a new body:** OMF's work. The re-bake onto it is the later test;
- **eyes:** *Eyes in the Shader*, held fixed here;
- **retiring the existing `Lips_*` articles and the 18 skins:** they stay as they are (§Don't Delete Spec Functionality); retiring them waits for a ruling;
- **Studio's side:** the platform's skin phase, after its links work.

## Rulings carried

- **2026-11-01, OMF's session (recorded by date and content in the OVS doc):** OMF keeps the approach to realism; validate on one subject on today's hm08; this library hosts the phase.
- **RD-AIS-1** (Krea 2 first) · **RD-AIS-2** (prove that whole maps can look really good).
- **RD-SKM-5, RD-SYN-1:** no whole AI map ships. C2 enters as a structure, and a win goes to the lead for the narrow re-ruling.
- **RD-SKM-2:** no photograph of a person in what ships. The bar stays local (RD-P23-10).
- **RD-RO-2:** CC0. **RD-P21-3:** the average held to the tone.

## Questions for discovery

| Id | Question | Recommendation |
|---|---|---|
| Q-P24-1 | **The tone.** Is C held to the bar's own measured face average, or to the nearest Fitzpatrick article (III)? The bar is paler and less red than any library tone (F-P23-2). | **The bar's average.** Then A and C differ only in skin, which is the claim. B stays today's III. |
| Q-P24-2 | **The picture size** (OVS-8). The bar was baked at 8K; the library's skins are 2048². | **Judge at 2048², the bar resampled.** Record the 4K gap as a measured row for OMF's render-body layout. |
| Q-P24-3 | **The subject's age on hm08** (OVS-Q3). | Leave the default unless the lead wants it set. If set, set it once at the start; the UVs do not move. |
| Q-P24-4 | **Testing in Studio.** The platform's skin phase follows its links work, so the finished skins draw magenta in Studio until then. | Ask the platform to bring the shine-map carry forward. Its phase says that part can start early. Until it lands, the library's look view and the lead's Blender are the verdict (RD-P23-9's precedent). |

## Pointers

- `PlatformDependencies.md` P33 (a draft in the look-dev scene), P34 (draw the shine maps), P35 (keep the structure).
- The platform's character model of 2026-11-01 (lips in the body, nails separate, one merged makeup layer) arrives as its own asks. This phase does the lips for its one subject only.
