# Atlas Water Review

Generated: 2026-06-17T10:55:51Z

Status: Automated Atlas validation passed. Manual water/visual review pending.

This report is focused only on generated surface samples where `surface_block_id` is `minecraft:water`. It does not tune roads, villages, structures, Hunter Boards, Guild Halls, NPCs, settlements, or civilization content.

## Summary

- Total water samples: 59
- South/west target-region water samples: 36
- Manually reviewed water samples: 2
- Manually reviewed target water samples: 2
- Visually confirmed ocean leaks: 1
- Issue type: terrain/noise ocean leak
- Biome-pool leakage: False
- Terrain/noise water placement: True
- Assessment: Automated Atlas validation passed, but manual review confirmed 1 south/west ocean-leak samples. This is terrain/noise water placement, not biome-pool leakage.

South should be allowed rare rivers and oases. West should be allowed mountain lakes and rivers. A sample is only a terrain blocker if the area visually reads wet/oceanic instead of arid/highland. Sea level around 62/63 is normal; the blocker is broad ocean-like basins where arid/highland regions should read as land-first.

## Water Samples By Region

| Region | Count |
|---|---:|
| `south_east_wilds` | 2 |
| `south_west_wilds` | 5 |
| `stoneback_highlands` | 17 |
| `sunreach` | 14 |
| `verdant_coast` | 21 |

## Water Samples By Biome ID

| Biome ID | Count |
|---|---:|
| `minecraft:badlands` | 6 |
| `minecraft:beach` | 2 |
| `minecraft:deep_lukewarm_ocean` | 7 |
| `minecraft:deep_ocean` | 6 |
| `minecraft:desert` | 1 |
| `minecraft:eroded_badlands` | 5 |
| `minecraft:lukewarm_ocean` | 2 |
| `minecraft:ocean` | 2 |
| `minecraft:river` | 1 |
| `minecraft:savanna` | 1 |
| `minecraft:stony_peaks` | 1 |
| `minecraft:warm_ocean` | 1 |
| `minecraft:windswept_forest` | 1 |
| `minecraft:windswept_hills` | 1 |
| `terralith:alpine_highlands` | 2 |
| `terralith:amethyst_canyon` | 1 |
| `terralith:arid_highlands` | 2 |
| `terralith:ashen_savanna` | 1 |
| `terralith:desert_canyon` | 1 |
| `terralith:desert_spires` | 1 |
| `terralith:forested_highlands` | 2 |
| `terralith:fractured_savanna` | 1 |
| `terralith:highlands` | 3 |
| `terralith:red_oasis` | 2 |
| `terralith:rocky_mountains` | 5 |
| `terralith:temperate_highlands` | 1 |

## Water Samples By Ring

| Distance ring | Count |
|---|---:|
| `tier_1_inner_wilds` | 2 |
| `tier_2_outer_marches` | 10 |
| `tier_3_ancient_frontiers` | 22 |
| `tier_4_dragon_scars` | 19 |
| `tier_5_corrupted_rim` | 6 |

## Water Samples By Classification

| Classification | Count |
|---|---:|
| `acceptable_coastline` | 22 |
| `acceptable_mountain_lake` | 16 |
| `acceptable_oasis` | 2 |
| `acceptable_river` | 2 |
| `needs_manual_review` | 16 |
| `ocean_leak` | 1 |

## Classification Values

Allowed values: `acceptable_river`, `acceptable_lake`, `acceptable_oasis`, `acceptable_mountain_lake`, `acceptable_coastline`, `sampler_edge_case`, `region_identity_problem`, `ocean_leak`, `wet_biome_wrong_region`, `needs_manual_review`.

## Water Sample Detail

| x,z | Atlas region | Climate sector | Distance ring | Expected pool | Actual biome ID | Surface block | Surface Y | Temperature | Precipitation | Snow allowed | South/west target | Classification | Manual status | Manual note | Suggested teleport |
|---|---|---|---|---|---|---|---:|---:|---|---|---|---|---|---|---|
| -12000,-6000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | `minecraft:water` | 63 | 0.3 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -12000 71 -6000` |
| -12000,-2000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:forested_highlands` | `minecraft:water` | 63 | 0.36 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -12000 71 -2000` |
| -12000,0 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:highlands` | `minecraft:water` | 63 | 0.4 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -12000 71 0` |
| -12000,10000 | `south_west_wilds` | `south_west` | `tier_5_corrupted_rim` | `south_west` | `terralith:red_oasis` | `minecraft:water` | 63 | 2.0 | rain | False | True | `acceptable_oasis` | pending | pending | `/tp @s -12000 71 10000` |
| -10000,-6000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | `minecraft:water` | 63 | 0.3 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -10000 71 -6000` |
| -10000,-2000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:forested_highlands` | `minecraft:water` | 63 | 0.36 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -10000 71 -2000` |
| -10000,0 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:highlands` | `minecraft:water` | 63 | 0.4 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -10000 71 0` |
| -10000,2000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | `minecraft:water` | 63 | 0.3 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -10000 71 2000` |
| -10000,6000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | `minecraft:water` | 63 | 0.3 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -10000 71 6000` |
| -10000,8000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `minecraft:stony_peaks` | `minecraft:water` | 63 | 1.0 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -10000 71 8000` |
| -10000,10000 | `south_west_wilds` | `south_west` | `tier_5_corrupted_rim` | `south_west` | `minecraft:eroded_badlands` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s -10000 71 10000` |
| -10000,12000 | `south_west_wilds` | `south_west` | `tier_5_corrupted_rim` | `south_west` | `minecraft:eroded_badlands` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s -10000 71 12000` |
| -8000,-6000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:amethyst_canyon` | `minecraft:water` | 63 | 0.95 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s -8000 71 -6000` |
| -8000,-4000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:alpine_highlands` | `minecraft:water` | 63 | 0.45 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -8000 71 -4000` |
| -8000,0 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:highlands` | `minecraft:water` | 63 | 0.4 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -8000 71 0` |
| -8000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s -8000 71 10000` |
| -8000,12000 | `sunreach` | `south` | `tier_5_corrupted_rim` | `south` | `minecraft:eroded_badlands` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s -8000 71 12000` |
| -6000,-4000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:rocky_mountains` | `minecraft:water` | 63 | 0.3 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -6000 71 -4000` |
| -6000,2000 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `minecraft:windswept_hills` | `minecraft:water` | 63 | 0.2 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -6000 71 2000` |
| -6000,6000 | `south_west_wilds` | `south_west` | `tier_3_ancient_frontiers` | `south_west` | `minecraft:badlands` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s -6000 71 6000` |
| -4000,0 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:alpine_highlands` | `minecraft:water` | 63 | 0.45 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -4000 71 0` |
| -4000,2000 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `minecraft:windswept_forest` | `minecraft:water` | 63 | 0.2 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -4000 71 2000` |
| -4000,4000 | `south_west_wilds` | `south_west` | `tier_2_outer_marches` | `south_west` | `minecraft:badlands` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s -4000 71 4000` |
| -4000,6000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:badlands` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s -4000 71 6000` |
| -2000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:desert` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s -2000 71 8000` |
| -2000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:red_oasis` | `minecraft:water` | 63 | 2.0 | rain | False | True | `acceptable_oasis` | pending | pending | `/tp @s -2000 71 12000` |
| 0,2000 | `sunreach` | `south` | `tier_1_inner_wilds` | `south` | `terralith:ashen_savanna` | `minecraft:water` | 63 | 1.0 | rain | False | True | `acceptable_river` | reviewed | Manual review: savanna/clay desert with a cool river system; visually good. | `/tp @s 0 71 2000` |
| 0,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:desert_canyon` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s 0 71 8000` |
| 0,10000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:arid_highlands` | `minecraft:water` | 63 | 1.6 | rain | False | True | `ocean_leak` | reviewed | Manual review: badlands ocean-floor look with large ocean above it. | `/tp @s 0 71 10000` |
| 2000,2000 | `south_east_wilds` | `south_east` | `tier_1_inner_wilds` | `south_east` | `minecraft:savanna` | `minecraft:water` | 63 | 1.2 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 2000 71 2000` |
| 2000,6000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `minecraft:badlands` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s 2000 71 6000` |
| 2000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:fractured_savanna` | `minecraft:water` | 63 | 1.1 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s 2000 71 8000` |
| 4000,0 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:beach` | `minecraft:water` | 63 | 0.8 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 4000 71 0` |
| 4000,4000 | `south_east_wilds` | `south_east` | `tier_2_outer_marches` | `south_east` | `minecraft:eroded_badlands` | `minecraft:water` | 63 | 2.0 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 4000 71 4000` |
| 4000,6000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:badlands` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s 4000 71 6000` |
| 6000,-2000 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:warm_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 6000 71 -2000` |
| 6000,0 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:river` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_river` | pending | pending | `/tp @s 6000 71 0` |
| 6000,2000 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:deep_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 6000 71 2000` |
| 6000,4000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:deep_lukewarm_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 6000 71 4000` |
| 8000,-6000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:deep_lukewarm_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 8000 71 -6000` |
| 8000,0 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:deep_lukewarm_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 8000 71 0` |
| 8000,2000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:deep_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 8000 71 2000` |
| 8000,4000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:deep_lukewarm_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 8000 71 4000` |
| 8000,6000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:deep_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 8000 71 6000` |
| 8000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:badlands` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s 8000 71 10000` |
| 8000,12000 | `sunreach` | `south` | `tier_5_corrupted_rim` | `south` | `terralith:arid_highlands` | `minecraft:water` | 63 | 1.6 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s 8000 71 12000` |
| 10000,-2000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:lukewarm_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 10000 71 -2000` |
| 10000,0 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:deep_lukewarm_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 10000 71 0` |
| 10000,6000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:beach` | `minecraft:water` | 63 | 0.8 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 10000 71 6000` |
| 12000,-6000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:deep_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 12000 71 -6000` |
| 12000,-4000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:deep_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 12000 71 -4000` |
| 12000,-2000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:deep_lukewarm_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 12000 71 -2000` |
| 12000,0 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:deep_lukewarm_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 12000 71 0` |
| 12000,2000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:lukewarm_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 12000 71 2000` |
| 12000,6000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 12000 71 6000` |
| 12000,8000 | `verdant_coast` | `east` | `tier_5_corrupted_rim` | `east` | `minecraft:deep_ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 12000 71 8000` |
| 0,9000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:desert_spires` | `minecraft:water` | 63 | 2.0 | rain | False | True | `needs_manual_review` | pending | pending | `/tp @s 0 71 9000` |
| 9000,0 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:ocean` | `minecraft:water` | 63 | 0.5 | rain | False | False | `acceptable_coastline` | pending | pending | `/tp @s 9000 71 0` |
| -9000,0 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:temperate_highlands` | `minecraft:water` | 63 | 0.5 | rain | False | True | `acceptable_mountain_lake` | pending | pending | `/tp @s -9000 71 0` |
