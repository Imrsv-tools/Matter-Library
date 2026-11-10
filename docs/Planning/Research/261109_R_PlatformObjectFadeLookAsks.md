# Research — The object fade, seen in the platform's app: a moiré on the desktop, steps in the headset (2026-11-09)

**Mnemonic:** `OFL` — reports `R-OFL-n` (for the ledger), asks `Q-OFL-n` (for the library).
**Mode:** an asks doc, written from the platform's side. It commits the library to nothing.
**Asked by:** the platform's lead, 2026-11-09, after the first look at the object fade in the platform's app on the
desktop and in the headset. It follows `261105_R_PlatformObjectOpacityAsks.md` (`POA`) and the library's Phase29, which
built that ask.
**Public repo:** needs and uses only. No consumer paths, code or tracker numbers.

**Read against:** this repo at `33666ab`:
- `unreal/MatterRuntime/Scripts/build_masters.py` — `bayer4()` at `:355`, the fade terms at `:388-400`;
- `docs/specs/Ontology/MasterSet.md` §Object fade (`:243-257`).

---

## Reports — for the ledger

**R-OFL-1 — On the desktop, temporal anti-aliasing does NOT smooth the 4 × 4 dissolve. It shows a moiré.**
- The platform's desktop view uses TSR. A wall at 50 % presence, drawn with the masters as built in Phase29, reads as a
  crawling interference pattern, not as a soft or an even fade. **It grows while the view is still**, which fits TSR
  settling its history on a pattern its own sub-pixel jitter keeps re-sampling.
- The lead, verbatim: *"opacity has a VERY noticable pattern to it... it is not a clean opacity more a moray pattern
  that gets worse as you stay still"*.
- **This corrects the platform's earlier ask** (`POA`, Q-POA-1: *"On the desktop, TSR smooths the pattern"*). It does
  not. `MasterSet.md:257` predicted "a see-through fade"; what TSR made of it is worse than that.

**R-OFL-2 — In the headset (FXAA, one sample per pixel) the dissolve reads far better, but a slow fade steps.**
- The lead: *"Opacity is WAY better in VR... when it is fading in and out it is not super smooth and the pattern
  appears a bit"*.
- **Why (the platform's reading):** a 4 × 4 threshold has 17 coverage levels. A slow fade walks through them, and each
  level is a visibly different regular pattern, so the eye sees the pattern change in steps.
- FXAA also draws the one-pixel pattern part-way. The platform measured that on a grey card at 50 %, every pixel of the
  dissolve lands between the card and the backdrop (18 and 26 on a 0 – 47 scale). That is a property of FXAA on any
  one-pixel pattern, not of this one.

**R-OFL-3 — The cross-fade is right and must stay right.**
- Two copies of one character in one place, one fading out at `f` and one fading in at `−(1 − f)`: **no holes** at
  50 / 50 and 25 / 75, on the desktop and in the headset. The platform's picture test measures it (holes 0.000 of 6400
  outline pixels). It also proves the colour pass tests the mask (`MasterSet.md:254`).

**R-OFL-4 — For information, no ask:** the first fade of a copy in a development run drew it whole for a moment, then
right. The platform reads it as that run compiling the masked instance's shaders on first use (`POA` F-POA-6 named
the risk). It is the platform's to check, and a packaged build compiles shaders ahead of time.

## Asks — for the library to decide

**Q-OFL-1 — A blue-noise threshold instead of the 4 × 4 ordered one.** *(The lead's ruling, 2026-11-09: "Blue-noise
grain"; the lead asked first, "Is that the only way to do this? a 16 step pattern?")*
- **The need:**
  - many more levels than 16, so a slow fade moves smoothly;
  - no regular grid: a part-present object reads as fine, even grain;
  - still a dissolve, frame-stable on a view that does not average (the headset).
- **The platform's suggestion:** a tiled blue-noise threshold texture (for example 64 × 64, up to 256 levels) on the
  screen pixel, in place of `bayer4()`. The design is the library's.
- **What must hold, unchanged:**
  - `MasterSet.md:248`: a copy fading in uses `1 − t`, so two copies at `f` and `−(1 − f)` keep complementary pixels.
    A tie keeps the pixel;
  - every layer of one object keeps or drops the same pixels together (`POA` R-POA-2: a half-faded character never
    shows its own insides);
  - the value contract: `object_fade`, Custom Primitive Data slot 0, 0 = fully there, negative = fading in. The
    platform's runtime then needs no change beyond rebuilding the masters.
- **The look the lead kept before** (Phase29: the 25 / 75 cross-fade as a regular 4 × 4 grid, *"keep it"*) **is
  replaced by this ruling.** The grid becomes grain.
- **Hair** uses the same threshold for its own soft coverage. Whether Hair moves to the new threshold too is the
  library's call. The platform's record: Hair's fixed pattern also "shows as dots" under TSR.

**Q-OFL-2 — On a view that averages over time, an even fade.** *(The lead's ruling, 2026-11-09: "Even fade on the
desktop" — "on the desktop the pattern shifts slightly every frame, so the desktop's smoothing blends it into an even,
clean fade; the headset keeps its fixed pattern")*
- **The need:** under TSR, the threshold changes from frame to frame so the temporal average converges to an even
  fade at the object's presence, with no moiré. Under FXAA it stays fixed (Q-OFL-1).
- **Still never glass — the platform's hypothesis, to measure:** in any one frame every layer of an object shares the
  pixel's threshold, so the frame shows either the object's front surface or what is behind the object, never the
  object's own insides. The average is "the front surface at p, the room at 1 − p". The skin keeps its look, sections do
  not mis-sort, and the platform's headset never takes this branch.
- **This changes a rule:** `MasterSet.md:257` says averaging "turns the dissolve back into a see-through fade, the look
  this rules out". Under this ruling, an averaged even fade on a temporally anti-aliased view is the wanted look. On a
  one-sample view it is still a dissolve.
- **How a master knows which view it is in** — the library's call. Two shapes the platform can see:
  - (a) from the engine's own view data, if a material can read whether this view's temporal anti-aliasing is on.
    Nothing to set from the consumer, and right per view even when two views draw in one frame;
  - (b) a global value the consumer sets (for example a material parameter collection). Simple, but one value per
    frame: wrong for one of the two views if the platform ever draws a desktop window and the headset together.
- **The cross-fade under averaging:** the copy fading in must take `1 − t` of the SAME per-frame threshold, so the two
  copies stay complementary in every frame (R-OFL-3).

## Questions for the library

| # | Question | Why it matters |
|---|---|---|
| Q-OFL-1 | a blue-noise threshold: which texture, what size, how it tiles, and does Hair follow? | a smooth slow fade in the headset |
| Q-OFL-2 | a per-frame threshold on a temporally averaged view only: how does the master know the view? | the desktop's moiré |
| Q-OFL-3 | do both still meet `MasterSet.md` §Object fade's "fully there costs nothing new"? | the headset frame |

## A suggested ledger row (the library writes its own)

*The platform's app, after first seeing the object fade: the desktop's TSR shows the 4 × 4 dissolve as a moiré (R-OFL-1);
the headset's slow fade steps (R-OFL-2). The lead ruled a blue-noise threshold, and an even fade on a view that averages
over time (Q-OFL-1, Q-OFL-2). The value contract is unchanged.*

## Pass 2 — the library's reading, and what it built (2026-11-10)

*Built in Phase29 step 29.3 ([`../Phases/Complete/Phase29_ObjectOpacityInTheMasters.md`](../Phases/Complete/Phase29_ObjectOpacityInTheMasters.md)); the rule is `MasterSet.md` §Object fade. The lead's rulings for it (2026-11-09): a blue-noise threshold, an even fade on a view that averages over time, and no technique that renders the scene twice.*

- **Q-OFL-1 — the threshold.** A 64 × 64 blue-noise tile (void-and-cluster, every rank 0 … 4095 once), generated by the library's masters build from a fixed seed, so no picture is committed and every build makes the same one: `T_Matter_FadeNoise`, beside the masters. `t = (rank + 0.5) / 4096`, repeated across the screen. In the library's runtime at one sample per pixel: the regular-pattern score of a 50 % dissolve fell from 973 to 88, and a slow fade flips 1 % of an article per 0.01 step, where the 4 × 4 moved in 16 of 100 steps, 6.3 % at once.
- **Hair** keeps its own 4 × 4 coverage dither and takes the fade as a second test on the shared threshold: at full presence it draws exactly as before, and the fade drops the hair with the head under it. Its fixed coverage dots under TSR (the platform's record) are untouched: that is Hair's look fully there, not the fade.
- **Q-OFL-2 — how a master knows the view: the ask's (a).** The masters read the view's own data: `View.TemporalAAParams.y`, the length of the temporal jitter sequence, which Unreal allows above 1 only under TAA or TSR. There, `t` is shifted each frame by `frac(n × 0.618…)`, `n` the view's frame index; everywhere else the shift is exactly 0. Nothing for the consumer to set, and right per view. A copy fading in takes `1 − t` of the same shifted `t`, so the cross-fade stays complementary in every frame. In the library's runtime under TSR, a still view settles to an even fade on all eleven test articles and on the cross-fade.
- **Q-OFL-3 — fully there.** The four solid masters cost nothing new (an opaque blend mode drops the mask). The masters that always test (Masked, Hair, the two glass masters) read one texel of the tile per pixel, where the 4 × 4 test was arithmetic. The headset's frame is where that is measured.
- **The platform's hypothesis under averaging** (*the frame shows the front surface or what is behind it, never the insides*) holds by construction: every layer of one object shares the pixel's threshold in every frame.
- **Not looked at:** a fading object's shadow on a view that averages. The shadow takes the per-frame test too, and a cached shadow (a virtual shadow map's page cache) may hold one frame's pattern.
- **R-OFL-4** is the platform's to check, as it says.
- **Seen in the platform's app** on this build the same night: the desktop under TSR shows an even fade with no moiré and a cross-fade with no holes; the headset shows no steps and the grain holds still.
- **The ledger row:** `PlatformDependencies.md` M15, updated in place. The platform rebuilds its masters; its value, swap and precache are unchanged.

## Status

**Pass 1** — the platform's reports R-OFL-1 … 4 and asks Q-OFL-1 … 2 (2026-11-09).
**Pass 2** — the library's reading, built in Phase29 29.3 and closed 2026-11-10 (above). Q-OFL-1 … 3 answered.
**Next:** nothing owed by the library. The platform's: the headset frame cost, and the shadow on a view that averages (M15).
