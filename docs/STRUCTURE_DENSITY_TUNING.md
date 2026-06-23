# Structure Density Tuning

Batch E1 responded to earlier feedback that Ascendant Realms was beautiful but too empty, not dangerous enough, and light on scary encounters and structures.

Batch F is installed and verified. It does not add additional structure/worldgen packs; it adds Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences and Walls as travel, environment, and medieval build polish.

Batch G is installed and verified. It adds Create: Structures Arise as the single approved Create structure addon and adds boss/dragon structure pressure through IceAndFire Community Edition and L_Ender's Cataclysm.

Batch H is installed and verified. It adds Villages&Pillages, MSS, MES, and Medieval Buildings End/Nether editions as the civilization and atmosphere structure layer. CTOV is delayed after a swamp-village worldgen crash.

Batch N is installed and validated. It adds Integrated Villages and IDAS as the cohesion structure layer. The current world-integration pass repairs the shared Integrated API workstation/POI processor path that crashed `integrated_villages:airship_village`, `integrated_villages:mossy_mounds`, and `integrated_villages:marketstead_village`, while keeping those structures active for retest.

Latest audit snapshot:

- 623 structures.
- 333 structure sets.
- 1,586 template pools.
- 696 placed features.
- 631 configured features.

This is already a large structure surface. The current step is density and stability tuning, not adding more structure packs.

## Current Sparse Structures State

Sparse Structures is still installed and marked both-side for the private/local testing workflow.

Sparse Structures now has a local tuning config in this repo:

- `mods/sparsestructures.pw.toml`
- `sparsestructures-forge-1.20.1-3.0.jar`
- `config/sparsestructures.json5`
- Side: both

Current tuning:

- Global spread factor is `1.25`.
- Vanilla villages use `minecraft:village_plains` factor `1.0`.
- Pillager outposts use `minecraft:pillager_outpost` factor `1.1`.
- Mansions remain rare at factor `2.0`.

This keeps Sparse Structures as a soft anti-spam guardrail after the previous boost made several village systems crowd the same area.

## E1 Density Decision

Decision: keep Sparse Structures enabled for E1 and increase structure variety by adding:

- MVS - Moog's Voyager Structures
- Moog's Structure Lib
- YUNG's Extras

This was the least destructive first density step. It should create more discoveries without immediately disabling the structure-density guardrail that helped keep Batch B from becoming noisy.

## Current Tuning Pass

Goal: make the world feel much more populated with villages, towns, NPCs, and landmarks while avoiding wall-to-wall structure spam.

Changes:

- Sparse Structures global spread factor is now `1.25`.
- Vanilla village set is back to neutral through `minecraft:village_plains` factor `1.0`.
- Pillager outposts are slightly rarer through `minecraft:pillager_outpost` factor `1.1`.
- Towns and Towers towns changed to spacing/separation `52/24`.
- Towns and Towers towers changed to `48/22`, frequency `0.35`.
- Towns and Towers miscellaneous structures changed to `36/14`.
- Integrated Villages regular villages changed to `64/32` with a `12` chunk village-avoid exclusion zone.
- Integrated Villages now keeps vanilla villages enabled instead of fully replacing them.
- Create: Structures Arise global multipliers raised from `1.0` to `1.15`.
- Standalone Ascendant Guild structures were widened again after the first in-game pass found four generated board structures near one village: Village Hunter Board `192/80`, Roadside Camp `224/96`, Frontier Outpost `288/128`.
- Ascendant Guild structures now use multiple written Supplementaries notice boards and their own loot tables, so they add social context without needing extra structure packs.
- Ascendant Atlas waymarks are now debug-only and no longer naturally generate; the active Atlas test is the finite coordinate runtime, In Control area rules, and density survey.
- Ascendant Atlas adds `/function ascendant_atlas:status` for fresh-world region and ring validation.

Next playtest target:

- A fresh world should show settlements and landmarks noticeably sooner.
- There should be more NPC village life, but villages should still have wilderness gaps between them.
- If structures feel too dense, raise Sparse Structures from `1.25` toward `1.35` before removing any content.
- If villages still feel too rare, tune Integrated Villages and Towns and Towers before adding another village mod.

## Later Tuning Questions

E1 validation passed. Disposable survival throwaway tests are no longer required after every batch. During later full survival tuning, record:

- Are structures still too rare after flying 3000-5000 blocks?
- Are MVS structures appearing?
- Are YUNG's Extras features locatable?
- Are villages still findable without feeling packed wall-to-wall?
- Does Sparse Structures appear to suppress the newly added structures too much?

## Next Tuning Choices

If structures are still too rare:

- Let the first run generate Sparse Structures config files, then inspect exact keys before editing.
- Reduce the Sparse Structures spacing multiplier if the generated config exposes one.
- Exempt specific structure sets only if the generated config supports exemptions clearly.
- Create a temporary test profile with Sparse Structures disabled to compare density.

If structures are too crowded:

- Keep Sparse Structures enabled.
- Avoid adding more structure packs.
- Tune individual structure mods before adding new ones.

Goal: more structures than the Batch D-era baseline, but no structure spam.

Batch G structure tuning questions:

- Does Create: Structures Arise add too much visible structure density near existing MVS/YUNG/Towns and Towers content?
- Do Cataclysm structures appear too close to spawn or villages?
- Do IceAndFire dragon roosts/caves create village griefing or early-game danger spikes?
- Does Sparse Structures suppress the new Batch G structure content too aggressively?

Batch H structure tuning questions:

- Do Villages&Pillages and Towns and Towers overlap in a way that makes settlements too frequent or too large?
- Do Villages&Pillages additions feel natural beside Guard Villagers and Villager Names?
- Do MSS floating structures feel magical or noisy with existing terrain?
- Do MES and Medieval Buildings End/Nether content appear at reasonable progression moments?
- Does Sparse Structures suppress the new Batch H structure content too aggressively?

Batch N/integration retest questions:

- Does the `integrated_api:workstation_processor` replacement prevent the known POI-cast crashes while keeping `airship_village`, `mossy_mounds`, and `marketstead_village` enabled?
- Do Integrated Villages and IDAS add life without crushing Towns and Towers, Villages&Pillages, MVS, Structory, YUNG, Moog, Cataclysm, and Marium placement?
- Are generated villages still readable and usable with Bountiful boards, named villagers, and Guard Villagers?
- Are dungeons and large structures discoverable without creating constant landmark noise?

Do not add more structure packs or village overhauls until Jayden approves another worldgen/structure batch. The approved custom Ascendant Guild and Ascendant Atlas worldgen tests add only standalone pack-owned structures, not another external structure pack. Revisit Sparse Structures only during the later full tuning pass after the larger content stack has proven stable.
