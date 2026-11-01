# Research — Skin maps from an image model (Krea 2 or similar): what one can give the library's maker

**Opened:** 2026-11-01 · **Mode:** research. It gathers and commits to nothing. **Mnemonic:** `AIS` (ids `F-AIS-n`, `Q-AIS-n`, `RD-AIS-n`). **Status:** parked, see the Status footer.
**Requested by:** the lead, 2026-11-01, asked in the platform's character-quality research and carried here to continue it from the library's side. Verbatim: *"There are enought public domain photos of humans of all ages and there are powerful AI images models like Krea2.. What would it take to train one of those models to output skin maps to our spec... in face... woudl we even need to train on images..."*
**Altitude:** a **design** question from the library's side: what an image model could supply to the library's skin maps, inside the library's rulings, and which rulings the lead would have to reopen for more. The licence reading (Pass 2) is the one **audit** pass.
**Measured at:** `a9a621e` (this checkout after merging `origin/main` `4f17d4d`), 2026-11-01.

**Extends, does not replace:**
- [`261014_R_SkinMaps.md`](261014_R_SkinMaps.md) Pass 6, *the AI route*: the generators, the Apache-2.0 models, and the design sketch F-SKM-32 that RD-SKM-5 took;
- [`261026_R_SyntheticSkinAndEyes.md`](261026_R_SyntheticSkinAndEyes.md): RD-SYN-1, and Pass 3's *"later, an AI detail layer"*;
- [`../../specs/Authoring/SkinMaps.md`](../../specs/Authoring/SkinMaps.md) §Sources and licence, and the pigment maker it describes (Phase23).

**The seeds, and how old they are** (read 2026-11-01 in the platform's documentation clone, which is 12 commits ahead of its origin):
- **The platform's character-quality research, its pass of 2026-11-01** (*"Skin maps from an image model (Krea 2)?"*, web). That pass was an **uncommitted edit** in the clone, so it is at no origin and may still change. Pass 1 audits it.
- **The platform's first-skin-set research, 2026-11-01.** Committed in the clone, not pushed. It covers the platform's half of drawing the finished skins and does not touch image models. Its one library-facing item, whether the skin list should show the 12 draft skins, is not this question.

---

## Current picture (for the lead)

**No training is needed to try it, and the library's rulings already allow the most useful part:**
- **What is allowed today:** the image model supplies the **skin-scale detail** (the mottling, blotching and flecks), as amounts of melanin and blood. The maker keeps the tone, the face's placed regions, the lips and the groin. That is RD-SKM-5's tone-free detail layer. The maker already keeps this detail apart, in two fields, so an image model can replace its procedural noise there (F-AIS-5).
- **A whole AI-made map** may be made and judged **as a comparison only, never shipped** (RD-SYN-1). So the platform's cheap test can run without reopening anything.
- **Shipping a whole AI map, or training on photos of people, reopens rulings.** Those calls are yours (Q-AIS-1, Q-AIS-2).
- **Krea 2 can be used,** but its licence has three conditions an Apache-2.0 model does not have: a $1M company revenue limit for commercial use, a required content filter, and a ban on removing watermarks. **FLUX.2 [klein] 4B is Apache-2.0**, ungated, and fits this machine's GPU without tricks (F-AIS-3, F-AIS-4).
- **A model draws colour only.** The roughness, normal, cavity and scatter maps stay the maker's (Phase22). Nothing here changes them.

**Offered first:** a **disposable probe** on the machine with Unreal. FLUX.2 [klein] 4B draws close-ups of skin with no face, the maker turns them into a melanin and blood detail field, and one tone is rendered three ways side by side: today's skin, the skin with AI detail, and a whole AI face projected as the comparison arm. Cost: a ~16 GB download, minutes of GPU time, nothing in the repo. It waits for your go (Q-AIS-4).

---

## The library's rulings this touches (quoted)

- **RD-SKM-2** (the lead, 2026-10-14: *"1b or c I want to explore that option"*): the first skin map is made by the library or AI-generated, **never taken from MakeHuman's photo atlases**. The words chose between three sources: (a) photos whose consent is unrecorded, (b) library-made, (c) AI. They say nothing about training data.
- **The consent sentence in the spec** (*"No photographs or scans of real people unless their rights and consent are documented"*, `SkinMaps.md` §Sources) is labelled *Ruled (RD-SKM-2; F-SKM-15)*. Its words come from **F-MP-19**, which `261014_R_SkinMaps.md` F-SKM-15 records as *"a finding from the lead-supplied guidance, not yet a ruling"*. The lead's choice of (b) or (c) over (a) is the ruling.
- **RD-SKM-5** (the lead, 2026-10-14: *"a"*, to F-SKM-32's option): the library-made map ships first, and **AI joins later only as a fine-detail layer on top**. It is tone-free and normalised to an average of 1, so it cannot move the tone, the lips or the groin. **A fully AI-made map and a paid cloud service are not taken.**
- **RD-SYN-1** (the lead, 2026-10-26: *"1) yes"*, to *"not yet: AI for the detail layer and content, a whole-face AI map only as a comparison arm"*): AI makes **no whole skin map**. **A whole-face AI map is only ever a judged comparison, never shipped.**
- **RD-RO-2** (the lead, 2026-10-14: *"material are CC0"*): CC0 only. The spec adds that the model must allow CC0 output (F-SKM-30).

---

## Pass 1 — The platform's pass, audited from the library's side (2026-11-01)

**Examined:** the platform's pass of 2026-11-01 (see the seeds above), checked against the primary sources and this repo.

- **F-AIS-1 — The pass's direction holds. Four of its claims are corrected or narrowed:**
  - **The licence threshold** is **company-wide annual revenue under US $1,000,000** (§2.3, read). The licence text sets no seat count. The "50 seats" figure appears only in secondary write-ups.
  - **The "Krea" name rule** (§3.1(b)) binds **a model you distribute**, such as a fine-tune. It does not bind the pictures. The library would never ship a model, so it only matters if a fine-tune is ever shared.
  - **AvatarTex's ~80 maps** were **professionally made face textures** on another face layout (HiFi3D++). The authors used a FLUX LoRA on them to *make a 20,000-map dataset*. The LoRA and the dataset are not released (read: arXiv 2511.06721). So the method is proven, but nothing can be reused.
  - **SMPL-GPTexture** (arXiv 2504.13378) works on the SMPL template, whose licence is research-only (F-SKM-29). **The method itself is not tied to it:** generate front and back views, fit the body, project, inpaint. For the library it would fit hm08, the approved mesh (RD-SKM-1).
- **F-AIS-2 — The pass says where this work belongs,** in line with a platform ruling the lead made on 2026-10-25: characters' skins, eyes, makeup, hair and wardrobe are **made outside Studio** and placed in the Asset Library or the Matter Library, and Studio only refines them. That matches this repo's role as a producer (R1). Nothing here changes.
  - *Not checked:* the pass's other method citations (MV2UV, SMPLitex, TexDreamer, UVMap-ID, UV-IDM). The library's Pass 6 had already found the SMPL ones research-only.

## Pass 2 — The licences, read (audit, 2026-11-01)

**Examined:** the Krea 2 Community License PDF the model card links to (the jsDelivr copy at `krea-ai/krea-2@db3984f`, text extracted locally), Krea's Acceptable Use Policy page (2026-06-22), and the Hugging Face API records and files for `krea/Krea-2-Raw`, `krea/Krea-2-Turbo`, `black-forest-labs/FLUX.2-klein-4B` and `…-klein-base-4B`.

- **F-AIS-3 — Krea 2's pictures are the user's, so they can be released as CC0. Using the model brings four conditions:**
  - **The weights are out.** Raw and Turbo are on Hugging Face with their files, created 2026-06-18, behind a click-through licence (`gated: auto`). The model card says the training data mixes *"publicly available data, data licensed from third-party providers, and synthetic data"*. That is the same unknown-sources question F-SKM-30 raised about every general model.
  - **Outputs:** *"You own all Outputs you generate, subject to your compliance with this Agreement. Krea claims no ownership of Outputs"* (§5.3). Nothing in the text limits how a picture is licensed onward, so a CC0 dedication is open, provided the conditions below were met when it was made.
  - **(1) Commercial use needs the revenue limit.** *"Commercial Use"* covers any use *"in connection with any business … including … distribution of products"* (§1). Commercial use of the model **or its Outputs** is allowed only if the user's whole company is under US $1M a year (§2.3). Above that, an Enterprise License is required first. The limit binds whoever runs the model, not people who later download a CC0 picture. *(This reading of the licence is not legal advice.)*
  - **(2) A content filter is required** (§4.2) when the model is deployed. A full-body projection needs unclothed views of a person, and a stock nudity classifier would block them. The use policy forbids sexual or intimate content of **real** people and anything involving minors. It says nothing about synthetic adult anatomy or body references for 3D. So the body route under Krea 2 needs a filter set up for that use. The face route does not hit it.
  - **(3) No removing watermarks** (§4.1(c)). Neither the model card nor the licence describes a watermark. If one exists, the maker's filtering and re-baking of the picture could count as removing it. *Unverified either way.*
  - **(4) Disclose AI** where the law or a platform requires it (§4.3). The library already plans this: its origin field says *AI-assisted* and names the model (`SkinMaps.md` §Sources, F-MP-18).
- **F-AIS-4 — FLUX.2 [klein] 4B is Apache-2.0, with no such conditions.**
  - Both the distilled `FLUX.2-klein-4B` and the fine-tunable `FLUX.2-klein-base-4B` are `apache-2.0`, **not gated**, with a `LICENSE.md` in each repo (created 2026-01-14). The larger 9B and [dev] models are non-commercial.
  - It joins the Apache-2.0 models F-SKM-30 listed (FLUX.1 [schnell], Qwen-Image, Z-Image-Turbo).
  - **Sizes against this machine** (measured 2026-11-01; the machine with Unreal has a 24 GB GPU and 95 GB free on `/home`):
    - FLUX.2 [klein] 4B: **16 GB** of weights, which fits as is;
    - Krea 2 Turbo: **36 GB**, of which the 12B transformer is **26 GB in bf16**. That exceeds the GPU, so it needs CPU offload or an fp8 copy.
  - **The F-SKM-30 blocker is gone on this machine.** The 8 GB laptop could not run these models, and *The Library Service* was re-scoped to have no GPU (RD-SV-2). The machine with Unreal can run them.

## Pass 3 — Where an image model fits the pigment maker (code read, 2026-11-01)

**Examined:** `tools/converters/fit/gen_synth_skin.py` (`compose`, the `DETAIL` and `FACE` tables, the chromophore `Lut`).

- **F-AIS-5 — The maker already keeps the skin-scale detail apart, as two pigment fields. That is RD-SKM-5's slot.**
  - In `compose`, the skin-scale detail is built separately as **`Md` (melanin) and `Bd` (blood)**. These are procedural noise on the body in 3D: the 7–25 mm "coarse" mottling, the 1–2.5 mm "fine" detail and the ~1 mm flecks.
  - They are added as **an amount of pigment** after the face's placed regions: `M *= max(Fm + Md − 1, 0.3·Fm)`, and the same for `B` with `Fb + Bd`.
  - Both average about 1 and carry no tone. The tone comes from the `Lut`'s operating melanin, and the regions come from `FACE`.
  - **So an image model's job, inside the rulings, is to replace the noise in `Md` and `Bd`.** The tone, the face's regions, the lips, the groin and the calibration stay the maker's untouched (RD-P21-3, RD-SKM-4).
- **F-AIS-6 — How a picture becomes those two fields (a design sketch):**
  1. Generate a close-up of skin with no face, in flat light. RD-SYN-1 already lists faceless close-ups as acceptable content.
  2. Remove the light: divide by a heavily blurred copy, which also removes the picture's own tone.
  3. Invert each pixel through the maker's chromophore table to melanin and blood. The table already maps (melanin × blood × oxygen) to colour, so the inverse is a nearest lookup.
  4. Keep only the detail bands (the 1–25 mm the noise covers) and normalise to a mean of 1.
  5. Place the result on the body in 3D, as tiles or as a texture lookup on the body's positions, the same way the noise is placed today.
  - The output is then tone-free by construction. Without step 3 the layer could only scale lightness and would lose the melanin and blood split that makes a fleck brown and a blotch red.
- **F-AIS-7 — Which parts of the face's gap to the bar each route can close.**
  - Phase23's open gap names two things: **the ring under the eye and the cheek blotching** (carried to *Skin Layers*).
  - **The blotching** is centimetre-scale pigment variation, which is the `Md`/`Bd` band. **An AI detail layer may supply it today** (RD-SKM-5).
  - **The ring under the eye** is a placed region (`under_eye`, the `FACE` table). That is regional colour, which RD-SKM-5 keeps with the library. **Only a whole map would draw it from the model,** and shipping one needs Q-AIS-1.

## Pass 4 — The lead's three questions, answered from the library's side (2026-11-01)

- **F-AIS-8 — "Would we even need to train?"** **Not to try it, and not for the detail layer.**
  - A general model already draws convincing skin close-ups. The detail layer needs no layout, so it needs no fine-tune.
  - **Training only matters for drawing straight into hm08's layout** (the platform's Route 2). The library cares about that only if a whole AI map ships (Q-AIS-1).
  - **The training data's problem is that the library's own maps teach only the layout.** The maker can produce any number of hm08 maps, since each structure is a seed, so a layout-only fine-tune needs no outside pictures. But they would teach the model the maker's look, not realism. Realism has to come from the base model's own knowledge (projection) or from photos of people (Q-AIS-2).
- **F-AIS-9 — "Public domain photos of humans" means out of copyright, not consent.**
  - The library has turned down photo sources whose people gave no recorded consent (RD-SKM-2's choice against MakeHuman's photos). The spec's consent sentence comes from F-MP-19 (see the rulings above).
  - **No ruling's words cover training on photos.** The pictures would not ship, but they would be inputs to what ships, and the spec asks for the provenance of every input (`SkinMaps.md` §Sources). This is new ground for the lead (Q-AIS-2), not a conflict with anything ruled.
- **F-AIS-10 — "Krea 2 or similar":** both work technically. **For a CC0 library, the Apache-2.0 model is the plainer choice:** no revenue limit, no filter duty, no watermark question, and it fits the GPU. Krea 2 stays open if the lead prefers its look and can answer the revenue limit in one line (Q-AIS-3).

## Open questions

| Id | Question (as the lead would see it) | Recommendation |
|---|---|---|
| Q-AIS-1 | **Should a whole AI-made skin map ever ship**, if it beats the pigment maker in a judged comparison? Today RD-SKM-5 and RD-SYN-1 say no: only a comparison. | **Keep the rulings for now.** Run the probe first. If the comparison arm is clearly better at what the detail layer cannot reach (the ring under the eye, the regional colour), reopen it with the pictures in front of you. |
| Q-AIS-2 | **May photos of people (public domain or not) be used to train a model whose output ships**, with no consent recorded? No ruling's words cover training. | **No, by the same reasoning that excluded MakeHuman's photos.** The detail layer needs no training at all, and a layout fine-tune can train on the maker's own maps. |
| Q-AIS-3 | **Krea 2 or an Apache-2.0 model** (FLUX.2 [klein] 4B) for the library's pictures? Krea 2 needs the generating company under US $1M revenue a year for commercial use (F-AIS-3). | **FLUX.2 [klein] 4B.** It is CC0-clean with no conditions and fits the GPU. Krea 2 only if your one-line answer on the revenue limit allows it and you prefer its look. |
| Q-AIS-4 | **Run the disposable probe** on the machine with Unreal? | **Yes, on your go.** Cost: ~16 GB download into scratch (95 GB free), minutes on the 24 GB GPU (first check that no Unreal editor holds it), nothing in the repo, torn down after. The result is parked in a `_Spike_` doc beside this one, with its script inline. |

## Resolved

*Nothing yet.*

## Status

- **Passes captured:** 4 (2026-11-01):
  - Pass 1: the platform's pass audited;
  - Pass 2: the licences read;
  - Pass 3: where a picture enters the pigment maker;
  - Pass 4: the lead's three questions.
- **Current direction:** an image model supplies **only the skin-scale detail** (`Md`, `Bd`), as melanin and blood, on top of the pigment maker. That is allowed now by RD-SKM-5 and RD-SYN-1, needs no training, and an Apache-2.0 model is enough. A whole AI map stays a comparison arm.
- **Found:** Krea 2's pictures belong to the user and can be released as CC0, under a $1M revenue limit, a filter duty and a watermark clause (F-AIS-3). FLUX.2 [klein] 4B has none of these (F-AIS-4). The maker already keeps the detail apart as pigment (F-AIS-5). The consent sentence in the spec comes from a finding, not the lead's words (rulings above).
- **Unverified:** whether Krea 2 embeds a watermark. The platform's pass is an uncommitted edit, at no origin. MV2UV, SMPLitex, TexDreamer, UVMap-ID and UV-IDM were not re-read. The licence reading is not legal advice.
- **Open with the lead:** Q-AIS-1 to Q-AIS-4.
- **Owed:** the platform's pass could point back here once the session editing it commits. That is the platform's doc, so it was not touched.
- **▶ Next:** your word on Q-AIS-4 (*"run the probe"*) and Q-AIS-3. Resume with `/research SkinMapsFromAnImageModel`.

## Sources

- Krea 2 Community License, PDF linked from the model card: `https://cdn.jsdelivr.net/gh/krea-ai/krea-2@db3984fbc6e13b34c0064990fc2d95ac64d00058/assets/hf_samples/LICENSE.pdf` (read 2026-11-01); the same text at `https://krea.ai/krea-2-licensing` (dated 2026-06-22).
- Krea Acceptable Use Policy: `https://krea.ai/krea-2-use-policy` (2026-06-22).
- Hugging Face model records: `krea/Krea-2-Raw`, `krea/Krea-2-Turbo`, `black-forest-labs/FLUX.2-klein-4B`, `black-forest-labs/FLUX.2-klein-base-4B` (API and files, read 2026-11-01).
- AvatarTex, arXiv 2511.06721; SMPL-GPTexture, arXiv 2504.13378 (abstracts and secondary summaries, 2026-11-01).
