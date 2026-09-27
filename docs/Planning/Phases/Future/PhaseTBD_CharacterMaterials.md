# PhaseTBD — Character Materials

**Status:** TBD — not numbered. Seeded 2026-09-27 from `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md` on the lead's ruling CM3 (*"fold the skins into Phase07, the rest its own phase"*). Discovery has not opened, and the handoff to `/discovery` is a deliberate gate the lead opens, never a slide. It follows Phase07, which builds the first six skin articles.

## Outcome

**A Creator can dress a character from the library: skin with its lips, nails and fine detail, eyes, teeth and hair. It looks right in Blender, in a USD viewer and in Unreal, and it works on any character, not only the one it was made on.**

Concretely at close: the remaining character substances are in the `biological` Domain (ruling CM1); the contract changes they need are ruled and built; and the MakeHuman body shows the complete set side by side in the test rig.

## Why this is a phase

It is where character matter stops being "Subsurface with a skin tone" and needs the calls that are expensive to unwind:
- whether layers may carry colour;
- whether hair and eyes get masters of their own;
- where body-specific ("fit") data lives.

Phase07 can build the six skins without any of these (research Pass 6d). Everything past them needs at least one.

## Scope (to settle at discovery; the research's recommendations, not decisions)

**In:**
- **Articles in `biological/{tissue,keratin,bone}`:** lip and gum/tongue mucosa, nail, sclera, cornea, iris, enamel, hair fibre (research Pass 6a).
- **Skin realism inputs:** subsurface scatter anisotropy and fuzz (lane A), with the matching Blender proxy inputs. Coat (carrier C2) is Phase07's, unless discovery moves it here.
- **The contract calls:**
  - a colour channel on layers, for region tone, freckles and makeup (CM-Q5, ruled together with Phase07 question 10);
  - a Hair master or Masked cards (CM-Q3);
  - an Eye master or a composed eye (CM-Q4);
  - a Skin master only if the rig shows marble and skin need different renderer settings (CM-Q10).
- **Fit sets:** the hm08-bound region masks and detail maps, and where they live (CM-Q6). The term goes into the Glossary before any spec uses it.

**Not now (unless discovery pulls them in):**
- Garment and hair-card atlases: they are mesh assets (research Pass 6b).
- The platform's slot binding and character generator (platform side; `PlatformDependencies.md` M1, CM-Q9).
- CC-BY MakeHuman packs (CM-Q8: local testing only, never committed).

## Open questions (carried from the research)

CM-Q3, CM-Q4, CM-Q5, CM-Q6, CM-Q8, CM-Q9, CM-Q10. See the research doc's §Open questions. **Discovery reads the research's §Resolved (CM1–CM3) and Pass 8 first.**

## Sources (pointers, not copies)

- `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md`: the whole thread.
- `docs/Planning/Phases/Future/Phase07_LibraryCoverage.md`: the six skins (question 1, CM3) and question 10 (layer colour).
- `docs/specs/Ontology/{Taxonomy,MasterSet}.md` · `docs/specs/Contract/LCDSchema.md` · `docs/Planning/PlatformDependencies.md` (M1).

## Discovery Log

_(numbered passes accrue here: examined → finding → decision / hypothesis / open question)_

## Discovery Status

- **Passes captured:** — (seed only)

## Execution Log

_(populated during execution)_
