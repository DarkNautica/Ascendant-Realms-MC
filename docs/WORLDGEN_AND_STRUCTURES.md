# Worldgen And Structures

## Batch N Cohesion Layer

Status: installed and validated; density tuning active.

Batch N adds:

- Integrated Villages: `integrated_villages-1.3.2+1.20.1-forge.jar`
- IDAS: `idas_forge-1.13.0+1.20.1.jar`
- Integrated API: `integrated_api-1.7.2+1.20.1-forge.jar`
- Supplementaries: `supplementaries-1.20-3.1.43-forge.jar`
- Quark: `Quark-4.0-462.jar`
- Zeta: `Zeta-1.0-31.jar`

Why Integrated Villages moved into the active install:

- CTOV was delayed after a swamp-village placement crash.
- Villages still feel bland.
- Integrated Villages may connect villages with Create, Farmer's Delight, Supplementaries, and the existing civilization stack better than another standalone village overhaul.

Overlap to test:

- Towns and Towers
- Villages & Pillages
- Guard Villagers
- Bountiful boards
- Villager Names
- MVS
- Structory
- YUNG structures
- Moog structures
- Cataclysm and Marium structures

Batch N worldgen test:

- Use a fresh creative test world.
- Locate multiple village types.
- Locate several dungeon/large structure types.
- Watch for feature-placement crashes, broken blocks, or severe density spikes.
- Batch N passed boot/join/stability. Final survival structure density tuning is now active.

Goal: a beautiful vanilla+++ medieval fantasy world that feels cohesive, not structure spam.

Status: Batch B installed and validated through Packwiz for Minecraft 1.20.1 Forge 47.4.20. Batch E1 added and validated structure density through MVS - Moog's Voyager Structures and YUNG's Extras. Batch F is installed and validated; it adds travel/environment/build polish. Batch G is installed and validated and adds Create: Structures Arise as the single approved Create structure addon. Batch H is installed and validated and adds village/landmark depth through Villages&Pillages, MSS, MES, and Medieval Buildings editions. Batch N added and validated Integrated Villages and IDAS. The Ascendant Guild standalone worldgen pilot remains active, and Ascendant Atlas now provides the finite-world coordinate runtime, In Control areas, and density tuning. CTOV is delayed after a `ctov:medium/village_swamp` feature-placement crash. Batch J is installed and validated; Alex's Caves was delayed with the T.O Magic crash chain and is not active.

## Ascendant Atlas Worldgen Layer

Status: active finite-world coordinate runtime, generated contracts, coordinate-aware biome source, and validator coverage.

The previous custom-worldgen implementation only covered the Ascendant Guild pilot. The broader Atlas layer is now present and testable:

- Control contracts: `config/ascendant_atlas/`.
- Runtime proof map: `config/ascendant_atlas/runtime.json`.
- In Control coordinate areas: `config/incontrol/areas.json`.
- KubeJS runtime bridge: `kubejs/server_scripts/ascendant_atlas_runtime.js`.
- Status test function: `/function ascendant_atlas:status`.
- Road/bridge policy: `config/ascendant_atlas/road_bridge_policy.json`.
- Worldgen region manifest: `config/ascendant_atlas/worldgen_regions.json`.
- Helper mod source: `local-mods/ascendant-atlas-regions/`.
- Helper mod jar: `mods/ascendant-atlas-regions-0.1.0.jar`.
- Active Overworld override: `config/openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json`.
- Core policy files: `config/ascendant_core/materials.json`, `ore_generation.json`, `recipe_policy.json`, `loot_policy.json`, `mob_policy.json`, `progression_tiers.json`, `dimension_policy.json`, `structure_rewards.json`, `vendor_policy.json`, and `unification_policy.json`.
- Datapack path: `config/openloader/data/ascendant_realms_atlas/`.
- Source mirror: `openloader/data/ascendant_realms_atlas/`.
- Generator: `scripts/generate-ascendant-atlas.py`.
- Biome-source generator: `scripts/generate-ascendant-atlas-worldgen.py`.

Full Atlas worldgen v1 now uses `ascendant_atlas_regions:regional_multi_noise`. The helper chooses a Terralith biome table by X/Z region, then applies a north/south climate gradient before delegating to normal multi-noise selection inside that table. North trends cold to colder to frozen and keeps regular cold/frozen ocean options without deep-ocean variants, while south trends warm coast to dry stone/sand to desert and badlands and keeps regular warm/lukewarm ocean options without deep-ocean variants. The shared outer-biome table is delayed until 30000 blocks so the 3000-block proof boundary keeps its north/south/east/west identity. The Hearthlands center table excludes ocean/island and snowy grove picks so spawn stays mild and mostly dry aside from normal rivers. The dimension keeps `settings: "minecraft:overworld"`, so Tectonic remains responsible for terrain/noise shape.

The world-integration datapack also overrides `aquamirae:surface` from its jar default `spacing: 4, separation: 0` to `spacing: 20, separation: 8`. Aquamirae arches and spirals should read as occasional frozen-ocean landmarks, not dense clutter around every cold-water test route.

Debug-only Atlas structures:

- `ascendant_atlas:crownlands_waymark`
- `ascendant_atlas:frostmarch_waymark`
- `ascendant_atlas:sunreach_waymark`
- `ascendant_atlas:verdant_crossing`
- `ascendant_atlas:stoneback_waystation`

These structure assets are kept as source/debug material but are no longer registered in structure sets, so they should not naturally generate in fresh worlds. The current test should focus on the live runtime, villages, roads, bridges, and spawn guardrails.

Hard boundary: coordinate-aware biome-source shaping is now handled by the local helper. Datapacks can add structures, tags, loot, and features, and KubeJS/In Control can handle coordinate scoreboards and spawn guardrails. Terrain-aware road-to-bridge substitution still needs later helper code or a curated map workflow because datapacks cannot inspect final road/river/cliff crossings after worldgen.

## Ascendant Guild Standalone Pilot

Status: active, pending in-game client/server validation.

Open Loader now adds three custom Ascendant Guild structures:

- `ascendant_guild:hunter_board_village_standard`
- `ascendant_guild:roadside_hunter_camp`
- `ascendant_guild:frontier_guild_outpost`

This is not a third-party village-pool injection yet. Test these with `/locate`, fresh chunk generation, generated NPC spawn sets, and a dedicated server stability pass before adding them directly into vanilla or modded village pools.

## Primary Terrain Stack

Recommended first test:

- Terralith
- Tectonic

Installed in Batch B. Tectonic's selected filename is `tectonic-mod-1.19.3-v2.2.1.jar`, but Modrinth version metadata marks that exact file as `ALL 1.20.1`.

Reason: this pair gives large visual gains while keeping a mostly vanilla-compatible biome identity.

## Biome Stack Decision

Delay Biomes O' Plenty for the first worldgen proof.

Reason: Biomes O' Plenty is compatible-looking, but it changes the biome palette heavily and may require many Dynamic Trees/structure/season compatibility decisions. Terralith + Tectonic better matches the "vanilla+++" direction first.

## Seasons

Recommended:

- Serene Seasons

Installed in Batch B with GlitchCore.

Test crop growth, snow behavior, and shader appearance before adding heavy weather/ambience mods.

## Village And Settlement Structures

First structure set should be restrained:

- Towns and Towers
- Structory
- YUNG's Better Dungeons
- YUNG's Better Mineshafts
- YUNG's Better Strongholds
- YUNG's Bridges

Installed in Batch B. Towns and Towers pulled Cristel Lib. YUNG's structures use YUNG's API, which is now both-side because Batch B makes it part of the server worldgen path.

Batch H installed and validated:

- Villages&Pillages
- MSS - Moog's Soaring Structures
- MES - Moog's End Structures
- Medieval Buildings [End Edition]
- Medieval Buildings [Nether Edition]

Still delay:

- Biomes O' Plenty
- Dynamic Trees
- YUNG's Better Caves
- Additional structure packs beyond the current Batch H/N stack

Reason: Batch H and Batch N already increase civilization, landmark, village, and dungeon density. Do not add more village/worldgen systems until the current integration retest passes.

## Batch E1 Density Additions

Installed and validated:

- MVS - Moog's Voyager Structures
- Moog's Structure Lib
- YUNG's Extras

Reason: earlier short survival feedback found the world beautiful but too empty and light on structures. E1 adds more discoveries without disabling Sparse Structures yet.

## Batch F Exploration And Build Polish

Status: installed and validated.

Batch F adds world-facing polish without adding new worldgen/village overhaul packs:

- Small Ships for travel/exploration tools.
- Snow! Real Magic for environmental behavior.
- Handcrafted for furniture and medieval settlement detail.
- Macaw's Bridges.
- Macaw's Fences and Walls.

Batch F client creative/system testing and dedicated server boot/join validation passed. Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences/Walls are stable enough for the next batch.

Do not add additional worldgen, Biomes O' Plenty, Dynamic Trees, or YUNG's Better Caves until Jayden approves another worldgen/structure batch after the current Batch N and integration retests.

## Batch G Create Structure Addon

Status: installed and verified.

Installed:

- Create: Structures Arise

Reason: Batch G allows at most one Create structure addon. Create: Structures Arise has a clean Minecraft 1.20.1 Forge/NeoForge target and was selected as the single optional Create structure addon.

Do not install Create: Structures, additional Create structure addons, Biomes O' Plenty, Dynamic Trees, YUNG's Better Caves, or extra village overhauls beyond the current Integrated Villages/IDAS test until Jayden approves a later batch.

## Batch H Civilization And Landmark Structures

Status: installed and validated.

Installed:

- Villages&Pillages
- MSS - Moog's Soaring Structures
- MES - Moog's End Structures
- Medieval Buildings [End Edition]
- Medieval Buildings [Nether Edition]

Reason: Batch H responds to the living-world/civilization goal without adding new boss packs, dragon addons, RPG Series modules, Biomes O' Plenty, Dynamic Trees, Ars Nouveau, Theurgy, or extra Create addons. CTOV is delayed because it crashed during swamp-village generation.

Validation focus:

- Check village frequency and variety without assuming final survival balance.
- Confirm structure generation does not crash dedicated server startup or join.
- Watch whether Sparse Structures suppresses or spaces H structures too aggressively.
- Avoid stress-generating huge distances during the first H server test.

## Batch J World/Content Note

Status: installed and validated.

Alex's Caves was added by the T.O Magic dependency chain, then removed when T.O Magic crashed against Cataclysm `3.30` with missing `DungeonEyeItem`. It is not active for the current Batch J test set and should stay delayed unless separately approved and verified later.

## World Integration Audit And Crash Repair

Status: staged and validated.

The latest world-integration audit scanned the active CurseForge instance at:

```text
C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)\mods
```

Summary:

- 172 jars scanned.
- 64 jars had world/data integration surfaces.
- 623 structures.
- 333 structure sets.
- 1,586 template pools.
- 696 placed features.
- 631 configured features.
- 98 biome modifiers.
- 614 biome tags.
- 4,324 loot tables.
- 10,551 recipes.
- 1,065 item tags.
- 145 entity type tags.

Integrated Villages workstation processor repair:

- Crash feature: `integrated_villages:airship_village`.
- Additional crash features: `integrated_villages:mossy_mounds` and `integrated_villages:marketstead_village`.
- Crash symptom: `Holder$Reference` could not be cast to `PoiType` during structure/feature placement.
- Latest reproduced crash seed: `3740828705519225665`.
- Latest generated crash chunk: `-33,-26`.
- Previous reproduced crash seed: `4571938849163387743`, structure center chunk `15,9`, approximately `x=240, z=144`; the player was still near spawn at `x=8.60, z=10.96` while nearby chunks generated.
- Earlier reproduced crash seed: `-8696758597753506463`, chunk `14,27`, approximately `x=224, z=432`.
- Root cause found in the Integrated Villages jar: these structures share Integrated API processor lists that run `integrated_api:workstation_processor`, which can place villager POI/job-site blocks during worldgen. That is the exact path where Minecraft crashed while updating POIs.
- Secondary data issue found in the Integrated Villages jar: its `data/minecraft/tags/worldgen/structure/village.json` references nonexistent `integrated_villages:swamp_village`, which also breaks Supplementaries village destination tags.
- Current action: `config/openloader/data/ascendant_realms_world_integration` is the active OpenLoader path. It overrides the Integrated Villages processor lists with static `minecraft:rule` workstation placeholder replacements, restores `integrated_villages:airship_village`, `integrated_villages:mossy_mounds`, and `integrated_villages:marketstead_village` for retest, keeps them in village tags/structure sets, and repairs the `minecraft:village` structure tag by removing only nonexistent `integrated_villages:swamp_village`.

This keeps Integrated Villages active while fixing the shared processor path instead of disabling every village that exposes it. If a crash persists, inspect the processor/template path before removing content; use structure disablement only as a temporary emergency fallback.

Latest compatibility-shim extension:

- Human Companions oak/spruce house biome tags now correct the upstream `windswept_gravelley_hills` typo while keeping those structures active.
- IDAS optional BOP/BYG biome tags are disabled only because those biome mods are absent from this Forge 1.20.1 pack.
- IDAS Archmage/Enchanting Tower optional Ars Nouveau spawner and loot hooks are replaced with Iron's Spells / vanilla equivalents so the structures can stay active.
- Iron's Spells malformed/incompatible loot tables are overridden with valid pack-native loot tables rather than removing Iron's Spells structures or loot.

## Structure Density Control

Strong candidate:

- Sparse Structures

Installed in Batch B as the first density-control tool.

Resolved packaging note: Sparse Structures metadata exists and is marked both-side so the private/local client export includes its jar for server materialization.

E1 audit result: no local Sparse Structures config file exists in this repo yet. Do not blindly remove Sparse Structures or guess its config keys. Keep it installed and revisit density during later full survival tuning. See `docs/STRUCTURE_DENSITY_TUNING.md`.

Alternatives:

- Structurify
- Structure Control

Choose one density-control approach for Batch B. Do not stack all three until configs are understood.

## Dynamic Trees

Delay.

Reason: Dynamic Trees is beautiful but has a high compatibility cost with terrain, biome mods, seasons, and structure placement. Add only after terrain and structures are stable.

## Batch B Validation Result

Batch B passed on a new dedicated-server world.

Use the active CurseForge instance path when materializing a server. Current active path:

```text
C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)\mods
```

CurseForge can create duplicate instance folders such as `Ascendant Realms (1)` or `Ascendant Realms (2)`. The materializer must point to the active instance containing the current jars.

Passed evidence:

- Updated client export included Sparse Structures.
- Updated client export included YUNG's Better Mineshafts.
- Updated client export included YUNG's Better Strongholds.
- Updated client export included YUNG's Better Dungeons.
- Updated client export included YUNG's Bridges.
- Materializer copied the full Batch A/B server jar set from the active CurseForge instance path with `-Clean`.
- Client joined localhost.
- Terrain generated.
- Structures generated.
- Disconnect/rejoin worked.
- Server remained stable for 10 minutes.

Real survival tuning is active now that the core feature stack is validated. Final world balance is not complete.

## Missing Module Investigation

These modules were missing from an earlier active client instance during the partial dedicated-server test because they were marked server-only and therefore were excluded from the CurseForge client export/import. Their metadata exists, they are now both-side for this private/local workflow, and the updated client export includes them.

| Module | Packwiz metadata | Modrinth slug | Side metadata | Client export after fix | Active client instance before fix |
|---|---|---|---|---|---|
| Sparse Structures | `mods/sparsestructures.pw.toml` | `sparsestructures` | Both | Included | Missing |
| YUNG's Better Mineshafts | `mods/yungs-better-mineshafts.pw.toml` | `yungs-better-mineshafts` | Both | Included | Missing |
| YUNG's Better Strongholds | `mods/yungs-better-strongholds.pw.toml` | `yungs-better-strongholds` | Both | Included | Missing |
| YUNG's Better Dungeons | `mods/yungs-better-dungeons.pw.toml` | `yungs-better-dungeons` | Both | Included | Missing |
| YUNG's Bridges | `mods/yungs-bridges.pw.toml` | `yungs-bridges` | Both | Included | Missing |

Tectonic verification: `mods/tectonic.pw.toml` uses Modrinth slug `tectonic` and selected file `tectonic-mod-1.19.3-v2.2.1.jar`. Modrinth version metadata for that file lists Forge support and game versions `1.19.3`, `1.19.4`, `1.20`, and `1.20.1`, so this is treated as an expected cross-version filename unless worldgen logs prove otherwise.

## Batch E1 Structure Result

- Create a fresh creative world.
- Fly 3000-5000 blocks.
- Check whether MVS structures appear.
- Check whether YUNG's Extras features appear.
- E1 validation passed.
- If Sparse Structures appears too restrictive during later survival tuning, inspect the generated config before changing anything.

