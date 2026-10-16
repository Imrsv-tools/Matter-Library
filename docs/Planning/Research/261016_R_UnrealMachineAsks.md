# Research — the asks only the machine with Unreal can settle (2026-10-16)

**Mnemonic:** `UEA` (ids `Q-UEA-n` · `F-UEA-n` · `RD-UEA-n`).
**Altitude:** an **audit** of open asks, not a design. Which of the library's open rows need **the machine with Unreal**, measured against the tree and the engine's source, and in what order. It commits to nothing.
**Asked by the lead (2026-10-16):** *"can you pull the latest? we are on the machine that has UE so we can address the matter library requests that need refinements to the US items"*. Read as **UE items**: the session was started on the machine with Unreal, and nothing in the tree is called "US".

## Pass 1 — the sweep (2026-10-16)

**Examined.** `main` fast-forwarded `e8421df..79a8a82` (7 commits, the tree clean, nothing of this machine's ahead). `unreal/RUNTIME.json` against `git log 47954ea..HEAD -- unreal/`. The ledger `PlatformDependencies.md` (every `M` row; P16, P28, P29). The Status footers of the consumer-ask docs: `261005_R_PlatformThinGlassAsks.md`, `261005_R_PlatformMasterAdoptionAsks.md`, `261011_R_AssetToolingAsks.md`, `261013_R_PlatformSkyAsks.md`, `261013_R_PlatformTrackedItemsAsks.md`, `261014_R_GroupsPlatformAsks.md`, `261014_R_PlatformMaterialPicturesAsks.md`, `261015_R_MaterialLabels.md`. The open issues here (#4, #5). On the platform's side, fetched and read at origin: its current materials phase, which went into discovery on 2026-10-15.

**What the platform's side says, in plain words (its discovery, 2026-10-15).** The lead ruled there that *every* material item comes into that phase and only the lead parks one. Among them are the library's open rows P11–P23, P28, M3 / M4, M6 and M8, the scale view (P29), and the grid wandering on a cheek in Unreal (the library's #5). From the library, it waits on two things: whether the diamond bends under the `index` build (MA-Q7, which it plans to answer by a look of its own), and whether its masters are current with the library's builder.

**Findings.**

- **F-UEA-1 — no runtime is owed.** The pin is `unreal-runtime-v4` (source `47954ea`). Since then `unreal/` has two commits: `4901203` (the pin itself) and `e8421df` (`MATTER_MASTERS_INSTANCED`, off by default). The masters draw nothing new at their defaults (`LOCAL_DELTAS.md`, the second producer's row; MA-RD1).
- **F-UEA-2 — the platform's "masters' source not in the library's history" is answered already.** The instanced switch is published as `e8421df` (authored 2026-10-10, committed 2026-10-16; `git merge-base --is-ancestor e8421df origin/main` holds), and it is documented in `fb47b74` and ledger M7's 2026-10-16 update. The library commit the platform's build recorded is not in this history (`git cat-file` refuses it), so it was a local commit, landed later as `e8421df`. That last part is *inferred from the dates*. Rebuilding from the published builder now keeps the instanced usage. Nothing is owed here beyond what M7 says.
- **F-UEA-3 — the platform's masters predating the emission repair is the platform's rebuild, not the library's work.** The builder at `HEAD` carries both the coat change and the emission repair (`unreal-runtime-v4`). It bears on the coloured LED washing out. Whether the library's two LED articles should get a dark body like Neon's is held on the platform's side until that rebuild. It is not posed to the library yet.
- **F-UEA-4 — P16's library half is in the masters.** The builder passes coat, fuzz and both anisotropies to Epic's function (`build_masters.py` head and defaults). What is open is whether Studio has *seen* them, which is the platform's.
- **F-UEA-5 — this machine's two red gate lanes (#4) are as recorded.** `library/staging/matterlib-0.1.0/` is from 2026-09-24. That is box input, not a regression (`LOCAL_DELTAS.md` §Two machines). It needs nothing from Unreal.

**The rows that need this machine.** These are the library's own faults, seen in its own rig, which the platform's phase now leans on:

| Item | Fault | Ledger / issue |
|---|---|---|
| The scale grid wanders on a large-UV surface in Unreal | runtime mesh precision | #5 (F-P19-9), rides P29 |
| The solid see-through master bends nothing | master | M6, MA-Q7 |
| The solid see-through master shows its see-through colour faint and flat, not deepening with thickness | master | M6 (its 2026-10-05 addendum) |

**Not this machine's, and why.** Face winding on sheets (M8, AT-Q4) is a ruling. Regenerating the Blender asset file (M8) is the library machine's job. Skin reading as plastic is not a fault the rig shows: skin agrees across the three tools there, and it is *Skin Maps*' ground. Blue teeth and the fitted article's own picture (P28) are on the platform's side, where Stage draws it.

## Pass 2 — the grid's wander, measured in the engine source (2026-10-16)

**Examined.** `unreal/MatterRuntime/Source/MatterRuntime/MatterRuntimeGameMode.cpp:273-293`, and Unreal 5.8.0's source on this machine: `Plugins/Runtime/ProceduralMeshComponent/.../ProceduralMeshComponent.cpp:134`, `Runtime/Engine/Private/StaticMesh.cpp:1377` (`InitFromDynamicVertex`), `Runtime/Engine/Private/Rendering/StaticMeshVertexBuffer.cpp:68, 489-490`, and `Runtime/GeometryFramework/Public/Components/MeshRenderBufferSet.h:100`.

- **F-UEA-6 — #5's hypothesis holds in the source.** The runtime builds every mesh with `UProceduralMeshComponent::CreateMeshSection`. Its scene proxy fills the vertex buffers through `FStaticMeshVertexBuffers::InitFromDynamicVertex`, which never sets full precision. `FStaticMeshVertexBuffer` starts at `bUseFullPrecisionUVs(false)`, so UVs go to the GPU as `PF_G16R16F`, half floats. Above 128 a half float steps in 1/8, which is #5's measured threshold (the cheek reaches 137 tiles). **`UProceduralMeshComponent` has no switch for it.** *Read from the source, not run.*
- **F-UEA-7 — Unreal's other runtime mesh component stores full precision unconditionally.** `UDynamicMeshComponent` (GeometryFramework) builds its buffers in `FMeshRenderBufferSet`, whose constructor calls `SetUseFullPrecisionUVs(true)` **and** `SetUseHighPrecisionTangentBasis(true)`. Moving the runtime's meshes onto it is the candidate repair. *Inferred, not built:* the higher-precision tangent basis may also shift the Unreal pictures of normal-mapped articles slightly. So the repair re-runs the whole library's Unreal column, not only the scale view.
- **F-UEA-8 — the platform will likely meet the same wander.** Unreal stores mesh UVs as half floats unless a mesh asks for more. A consumer's scale view in Unreal, on a mesh whose UVs pass 128, wanders the same way unless its meshes are built at full precision. *Unreal's default, not checked in the platform's code.* That is the platform's to check. It belongs with P29 when this lands.

**Who else reads what the repair would change.** The rig's Unreal driver speaks to the runtime only through job files (`tools/parity/JOB_FORMAT.md`), and those do not change. The platform does not run this runtime: it builds the masters into its own project (M7). The one other writer of the pin is `unreal/publish.sh`, which is the lead's act. No contract rule names the mesh component.

## Pass 3 — the diamond's bend: what a probe on this machine needs (2026-10-16)

**Examined.** `build_masters.py:59, 91, 657-670` (`MATTER_MASTERS_REFRACTION=index`: the article's index on the solid master's Refraction input, 1.0 on the thin one). `tools/parity/drivers/unreal.py:33-40, 509-523` (the rig takes `$MATTER_UNREAL_EDITOR`, an editor-mode run of the masters built here). `.gitignore:38` (`unreal/MatterRuntime/Content/` is ignored, so a masters build touches no tracked file). The rig's side view for see-through articles (thin-glass doc, Pass 3). `ps -ef | grep "[U]nrealEditor"`: nothing running at 2026-10-16.

- **F-UEA-9 — the library can answer MA-Q7 itself, without waiting on the platform's look.** Build the masters with `index`, run the rig on `Diamond_Brilliant` in editor mode with `--no-blender`, then rebuild at the defaults. Look at the side view in both runs: does the wall behind the face sit in a different place? It is a disposable probe: no tracked file changes, and the masters go back to their defaults afterwards. **If it bends**, `index` becomes the solid master's default. That changes what the masters draw, so a new runtime is owed, the same publish as F-UEA-7's.
- **F-UEA-10 — the solid master's flat colour rides the same probe.** All three articles on it (`Diamond_Brilliant`, `Sapphire_Natural`, `LeadCrystal_Clear`) can be read from the same two runs. Whether the colour deepens with thickness under `index` is unmeasured. It may be a second, separate fault in Epic's function (TG-Q5).

## Status

- **Passes captured:** 3, all 2026-10-16. A sweep, the grid's wander read in the engine source, and the diamond probe's shape.
- **Current direction.** Three faults need this machine. All three are the library's own faults, and the platform's materials phase now leans on them: the grid's wander (#5), and the solid see-through master's bend and colour (M6). **Both repairs can end in one new runtime, `unreal-runtime-v5`, published at the lead's word.** Nothing else in the ledger is owed from this machine (F-UEA-1 to F-UEA-5).
- **The offer, cheapest first.**
  1. **The diamond probe** (F-UEA-9, F-UEA-10). Two masters builds and two rig runs of one article. No tracked change. It answers MA-Q7 for both repos.
  2. **#5 as a `/quick-fix`** (F-UEA-6, F-UEA-7). The runtime's meshes move to `UDynamicMeshComponent`; a runtime build; the scale-view command from #5 re-run; the whole Unreal column re-run against the v4 pictures.
  3. **One runtime publish** carrying whichever of the two landed. `unreal/publish.sh 5` is the lead's.
- **Open questions:** none for the lead. Q-UEA-1, *does `index` bend the diamond?*, is answered by the probe.
- **Not run:** everything in Pass 2 is read from the source. Nothing was built, launched or rendered.
- **Owed to the platform, once landed:** F-UEA-8 as a note on P29; MA-Q7's answer on M6.
