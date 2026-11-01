# Phase25 — AI Skin Structure

**Status:** SEEDED (2026-11-01). Split out of Phase24 on the lead's *"Split and seed"* (RD-OVS-6). It runs **after Phase24**, against Phase24's judge. **`/discovery Phase25` opens Pass 1** and confirms or rewrites this doc.
**Written on:** the machine with Unreal, at `de4f5d9`.
**Seeded from:** [`../Research/261101_R_SkinMapsFromAnImageModel.md`](../Research/261101_R_SkinMapsFromAnImageModel.md) (RD-AIS-1, RD-AIS-2; Passes 3 and 6) · [`../Research/261101_R_Spike_SkinMapFromImageModel.md`](../Research/261101_R_Spike_SkinMapFromImageModel.md) (the route proven on hm08's head; scripts beside it) · [`../Research/261101_R_OneValidatedSkin.md`](../Research/261101_R_OneValidatedSkin.md) (OVS-3: AI enters as a structure) · [`Phase24_OneValidatedSkin.md`](Complete/Phase24_OneValidatedSkin.md).

## Outcome

**An image model's person becomes a skin structure in the library: projected onto the body, its light removed, turned into pigment and calibrated by the maker. It is judged beside the scanned skin and Phase24's skin on the same body.**

*(Drafted at seeding. Discovery confirms the words.)*

## Why this is a phase

- **The lead's claim to prove:** *"I beleive they will mnake very convicing skin maps if we can instruct them correctly"* (RD-AIS-2). The spike showed it for the head's colour, in a simple render. This phase takes it to the library's standard: the whole body, the library's look view, and the judge.
- **It is the one place the library's AI rules meet a real candidate.** RD-SKM-5 and RD-SYN-1 accept no whole AI map. OMF's OVS-3 says how an AI skin can still enter: as a structure. A win here goes to the lead as that narrow re-ruling.
- **It needs things Phase24 does not:** new models (supplied by the lead, RD-OVS-5), a projection tool, masks, and the maker taking an outside pigment field.

## The plan — as known at seeding

1. **The models, side by side:** Krea 2 first (RD-AIS-1) and FLUX.2 [klein] 4B, on the same views and prompts. The spike's generation and bake scripts are the start.
2. **The structure:**
   - the spike's progressive projection extended from the head to the body;
   - masks at the brows, lids and lips, so painted-in eyebrows and lash lines stay out (F-AIS-13);
   - the light removed;
   - each texel inverted to melanin and blood through the maker's skin model (F-AIS-6);
   - the maker composing from that field in place of its own, at Phase24's tone and 8K, calibrated like any structure.
3. **The judge:** Phase24's look view, with A (the scanned bar), B (today's skin), C (Phase24's skin) and **D (this structure)**. The lead's verdict per view.
4. **If D wins:**
   - the lead's narrow re-ruling (an AI-made structure is accepted);
   - D becomes the one set's skin, with provenance *AI-assisted* and the model named (`SkinMaps.md` §Sources);
   - served as Phase24's set was.

## Scope — as known at seeding

**In (candidate):** the steps above; the projection and inversion as a library tool under `tools/`; the maker taking an outside pigment field.

**Not now:** other tones, people and ages (*Variety*); a raw painted AI map shipped as is (RD-SYN-1: a comparison only); a creator-run generator (Q-AIS-1's framing, recorded, not ruled); training a model (not needed, F-AIS-8; photos of people as training data are Q-AIS-2).

## Rulings carried

- **RD-AIS-1** (Krea 2 first; the revenue limit is no obstacle) · **RD-AIS-2** (prove that whole maps can look really good).
- **RD-OVS-1, -2, -5, -6:** the bar's tone, 8K, the lead supplies the models, the split.
- **RD-SKM-5, RD-SYN-1:** no whole AI map ships. **RD-SKM-2:** no photograph of a person in what ships. **RD-RO-2:** CC0.

## Questions for discovery

- Krea 2 has no image input in its diffusers pipeline: is the spike's img2img start (the render's latent, noised) enough, or does Krea's own tooling offer better?
- How far down the body the projection reaches, and what fills the rest.
- How the lip zone joins: from the model, or from Phase24's.
