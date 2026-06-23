# World Integration Audit

Generated: 2026-06-14 23:15:21 -04:00

Client mods path: `C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (1)\mods`

This audit scans jar data files for structures, world features, biome modifiers, loot tables, recipes, and tags. It does not prove in-game balance by itself; it gives us the inventory to tune against.

## Crash Repair

- `config/openloader/data/ascendant_realms_world_integration` repairs the shared Integrated Villages `integrated_api:workstation_processor` POI-cast crash path with static `minecraft:rule` workstation replacements.
- `integrated_villages:airship_village`, `integrated_villages:mossy_mounds`, and `integrated_villages:marketstead_village` remain enabled for retest.
- Integrated Villages' `minecraft:village` structure tag is repaired because the jar references nonexistent `integrated_villages:swamp_village`.
- Root cause note: inspect processor/template paths before disabling more structures. Use structure removal only as a temporary emergency fallback.

## Summary

| Scope | Count |
| --- | ---: |
| Jars scanned | 172 |
| Jars with world/data integration surfaces | 64 |
| Structures | 623 |
| Structure Sets | 333 |
| Template Pools | 1586 |
| Placed Features | 696 |
| Configured Features | 631 |
| Biome Modifiers | 98 |
| Biome Tags | 614 |
| Loot Tables | 4324 |
| Recipes | 10551 |
| Item Tags | 1065 |
| Entity Type Tags | 145 |

## Per-Mod Integration Surface

| Mod | Mod ID | Jar | Structures | Sets | Pools | Features | Biome Modifiers | Loot | Recipes | Tags |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Alex's Delight | `alexsdelight` | `alexsdelight-1.5.jar` | 0 | 0 | 0 | 0 | 0 | 2 | 40 | 2 |
| Alex's Mobs | `alexsmobs` | `alexsmobs-1.22.9.jar` | 1 | 0 | 0 | 2 | 2 | 139 | 84 | 189 |
| Amendments | `amendments` | `amendments-1.20-2.2.5.jar` | 3 | 0 | 0 | 0 | 0 | 2 | 2 | 5 |
| Aquamirae | `aquamirae` | `aquamirae-forge-1.20.1-6.4.0.jar` | 8 | 4 | 7 | 10 | 10 | 20 | 54 | 4 |
| Architectury | `architectury` | `architectury-9.2.14-forge.jar` | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| Artifacts | `artifacts` | `artifacts-forge-9.5.19.jar` | 0 | 0 | 0 | 2 | 1 | 61 | 3 | 18 |
| Bosses'Rise | `block_factorys_bosses` | `block_factorys_bosses-2.1.2-forge-1.20.1.jar` | 5 | 5 | 19 | 0 | 0 | 60 | 78 | 25 |
| Born in Chaos  | `born_in_chaos_v1` | `born_in_chaos_[Forge]1.20.1_1.7.5.jar` | 31 | 31 | 31 | 10 | 49 | 172 | 160 | 25 |
| Bountiful | `bountiful` | `Bountiful-6.0.4+1.20.1-forge.jar` | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 0 |
| Citadel | `citadel` | `citadel-2.6.3-1.20.1.jar` | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| Create: Structures Arise | `create_structures_arise` | `create_structures_arise-176.49.48 Forge 1.20.1.jar` | 29 | 28 | 28 | 0 | 0 | 0 | 0 | 18 |
| Create | `create` | `create-1.20.1-6.0.8.jar` | 0 | 0 | 0 | 6 | 3 | 640 | 2782 | 95 |
| Create Big Cannons | `createbigcannons` | `createbigcannons-5.11.4-mc.1.20.1-forge.jar` | 0 | 0 | 0 | 0 | 0 | 163 | 222 | 63 |
| Decorative Blocks | `decorative_blocks` | `decorative_blocks-forge-1.20.1-4.1.3.jar` | 0 | 0 | 0 | 0 | 0 | 52 | 157 | 19 |
| Fantasy Armor | `fantasy_armor` | `fantasy_armor-forge-1.2.4-1.20.1.jar` | 0 | 0 | 0 | 0 | 0 | 0 | 117 | 0 |
| Farmer's Delight | `farmersdelight` | `FarmersDelight-1.20.1-1.3.2.jar` | 0 | 0 | 0 | 19 | 9 | 112 | 530 | 102 |
| Medieval Buildings [The End Edition] | `medievalend` | `forge-medievalend-1.0.1.jar` | 5 | 1 | 5 | 0 | 0 | 9 | 0 | 5 |
| FTB Quests | `ftbquests` | `ftb-quests-forge-2001.4.22.jar` | 0 | 0 | 0 | 0 | 0 | 5 | 7 | 1 |
| Guard Villagers | `guardvillagers` | `guardvillagers-1.20.1-1.6.18.jar` | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 1 |
| Handcrafted | `handcrafted` | `handcrafted-forge-1.20.1-3.0.6.jar` | 0 | 0 | 0 | 0 | 0 | 267 | 634 | 31 |
| Human Companions | `humancompanions` | `humancompanions-1.20.1-1.7.6.jar` | 8 | 1 | 9 | 0 | 0 | 0 | 0 | 10 |
| Ice And Fire Community Edition | `iceandfire` | `IceAndFireCE-1.2.5-1.20.1-forge.jar` | 15 | 9 | 6 | 30 | 0 | 149 | 690 | 113 |
| Integrated Dungeons and Structures | `idas` | `idas_forge-1.13.0+1.20.1.jar` | 92 | 16 | 213 | 0 | 0 | 166 | 1 | 104 |
| Immersive Armors | `immersive_armors` | `immersive_armors-1.7.2+1.20.1-forge.jar` | 0 | 0 | 0 | 0 | 0 | 0 | 50 | 7 |
| Integrated API | `integrated_api` | `integrated_api-1.7.2+1.20.1-forge.jar` | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 48 |
| Integrated Villages | `integrated_villages` | `integrated_villages-1.3.2+1.20.1-forge.jar` | 15 | 4 | 421 | 0 | 0 | 153 | 0 | 62 |
| Iron's Lib | `irons_lib` | `irons_lib-1.20.1-1.1.0.jar` | 0 | 0 | 0 | 0 | 0 | 3 | 2 | 0 |
| Iron's Spells 'n Spellbooks | `irons_spellbooks` | `irons_spellbooks-1.20.1-3.16.1.jar` | 10 | 9 | 54 | 2 | 2 | 122 | 301 | 81 |
| cataclysm | `cataclysm` | `L_Enders_Cataclysm-3.30.jar` | 29 | 19 | 98 | 0 | 1 | 168 | 189 | 77 |
| Lootintegrations mod | `lootintegrations` | `lootintegrations-1.20.1-4.7.jar` | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 1 |
| Majrusz's Progressive Difficulty | `majruszsdifficulty` | `majruszs-difficulty-forge-1.20.1-1.9.10.jar` | 0 | 0 | 0 | 10 | 3 | 38 | 35 | 13 |
| Macaw's Bridges | `mcwbridges` | `mcw-bridges-3.1.2-mc1.20.1forge.jar` | 0 | 0 | 0 | 0 | 0 | 145 | 402 | 0 |
| Macaw's Lights and Lamps | `mcwlights` | `mcw-lights-1.1.5-mc1.20.1forge.jar` | 0 | 0 | 0 | 0 | 0 | 140 | 154 | 0 |
| Macaw's Fences and Walls | `mcwfences` | `mcw-mcwfences-1.2.1-mc1.20.1forge.jar` | 0 | 0 | 0 | 0 | 0 | 180 | 244 | 4 |
| Medieval Buildings [The Nether Edition] | `medieval_nether` | `medieval_buildings_nether_edition-1.20.1-1.0.2-forge.jar` | 5 | 1 | 5 | 0 | 0 | 10 | 0 | 5 |
| Minecraft Comes Alive | `mca` | `minecraft-comes-alive-7.6.16+1.20.1-universal.jar` | 0 | 0 | 0 | 0 | 0 | 26 | 419 | 17 |
| (unknown) | `moogs_structures` | `MoogsEndStructures-1.20-2.0.3.jar` | 24 | 24 | 57 | 0 | 0 | 8 | 0 | 1 |
| (unknown) | `moogs_structures` | `MoogsSoaringStructures-1.20-2.1.0.jar` | 35 | 35 | 91 | 0 | 0 | 15 | 0 | 15 |
| (unknown) | `moogs_structures` | `MoogsVoyagerStructures-1.20-5.0.6.jar` | 130 | 116 | 152 | 0 | 0 | 29 | 0 | 24 |
| Mowzie's Mobs | `mowziesmobs` | `mowziesmobs-1.8.2.jar` | 4 | 4 | 44 | 0 | 1 | 26 | 12 | 24 |
| Quark | `quark` | `Quark-4.0-462.jar` | 16 | 0 | 0 | 14 | 0 | 835 | 1602 | 118 |
| Scaling Health | `scalinghealth` | `ScalingHealth-1.20.1-8.0.2+9.jar` | 0 | 0 | 0 | 8 | 1 | 13 | 10 | 2 |
| Serene Seasons | `sereneseasons` | `SereneSeasons-forge-1.20.1-9.1.0.2.jar` | 0 | 0 | 0 | 0 | 0 | 1 | 4 | 9 |
| Simply Swords | `simplyswords` | `simplyswords-forge-1.56.0-1.20.1.jar` | 0 | 0 | 0 | 0 | 0 | 1 | 424 | 32 |
| Create Slice & Dice | `sliceanddice` | `sliceanddice-forge-3.6.0.jar` | 0 | 0 | 0 | 0 | 0 | 3 | 11 | 3 |
| Small Ships | `smallships` | `smallships-forge-1.20.1-2.0.0-b1.4.jar` | 0 | 0 | 0 | 0 | 0 | 0 | 77 | 5 |
| Snow! Real Magic! | `snowrealmagic` | `SnowRealMagic-1.20.1-Forge-10.7.0.jar` | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 0 |
| Sophisticated Backpacks | `sophisticatedbackpacks` | `sophisticatedbackpacks-1.20.1-3.24.53.1877.jar` | 0 | 0 | 0 | 0 | 0 | 15 | 147 | 2 |
| Sophisticated Core | `sophisticatedcore` | `sophisticatedcore-1.20.1-1.3.50.2005.jar` | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| Marium's Soulslike Weaponry | `soulsweapons` | `soulslike-weaponry-1.3.1-1.20.1-forge.jar` | 6 | 2 | 4 | 4 | 5 | 37 | 236 | 32 |
| Spartan Shields | `spartanshields` | `SpartanShields-1.20.1-forge-3.1.1.jar` | 0 | 0 | 0 | 0 | 0 | 0 | 157 | 24 |
| Structory | `structory` | `Structory_1.20.x_v1.3.5.jar` | 15 | 5 | 59 | 0 | 0 | 39 | 0 | 9 |
| Supplementaries | `supplementaries` | `supplementaries-1.20-3.1.43-forge.jar` | 12 | 1 | 2 | 8 | 3 | 178 | 480 | 108 |
| Terralith | `terralith` | `Terralith_1.20.x_v2.5.4.jar` | 34 | 7 | 44 | 1054 | 0 | 51 | 11 | 140 |
| Titles | `titles` | `Titles-1.20.1-3.8.3.jar` | 0 | 0 | 0 | 0 | 0 | 4 | 2 | 0 |
| Towns and Towers | `t_and_t` | `Towns-and-Towers-1.12-Fabric+Forge.jar` | 63 | 3 | 185 | 0 | 0 | 14 | 0 | 65 |
| Villages & Pillages | `villagesandpillages` | `villagesandpillages-forge-mc1.20.1-1.0.2.jar` | 1 | 1 | 7 | 0 | 0 | 3 | 0 | 1 |
| Weather2 | `weather2` | `weather2-1.20.1-2.8.3.jar` | 0 | 0 | 0 | 0 | 0 | 8 | 18 | 0 |
| YUNG's Better Dungeons | `betterdungeons` | `YungsBetterDungeons-1.20-Forge-4.0.4.jar` | 6 | 5 | 33 | 0 | 1 | 8 | 0 | 5 |
| YUNG's Better Mineshafts | `bettermineshafts` | `YungsBetterMineshafts-1.20-Forge-4.0.4.jar` | 16 | 1 | 0 | 0 | 0 | 0 | 0 | 13 |
| YUNG's Better Strongholds | `betterstrongholds` | `YungsBetterStrongholds-1.20-Forge-4.0.3.jar` | 3 | 1 | 12 | 0 | 0 | 10 | 0 | 1 |
| YUNG's Bridges | `yungsbridges` | `YungsBridges-1.20-Forge-4.0.3.jar` | 0 | 0 | 0 | 24 | 1 | 0 | 0 | 5 |
| YUNG's Extras | `yungsextras` | `YungsExtras-1.20-Forge-4.0.3.jar` | 0 | 0 | 0 | 124 | 3 | 3 | 0 | 3 |
| Zeta | `zeta` | `Zeta-1.0-31.jar` | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

## Follow-Up Checks

- Run this after each CurseForge import using the active instance mods folder.
- Confirm mob-heavy mods with few/no biome modifiers are controlled through their config files or In Control caps.
- Confirm structure-heavy mods with many structure sets are represented in config/sparsestructures.json5, dedicated mod configs, or documented density policy.
- Confirm loot-heavy mods feed Loot Integrations, Bountiful contracts, the skill tree, or delayed KubeJS scripts.
