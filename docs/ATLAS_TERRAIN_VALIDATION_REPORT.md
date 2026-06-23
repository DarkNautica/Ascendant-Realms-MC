# Atlas Terrain Validation Report

## 2026-06-18 Random Worldgen Restore

Status: superseded. Jayden rejected the coordinate-directed Atlas terrain approach after visible hard biome/terrain cuts remained. The active terrain direction is now random Tectonic/Terralith generation with Atlas Overworld influence disabled.

Removed source influence files:

- `config/openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json`
- `config/openloader/data/ascendant_realms_atlas/data/minecraft/worldgen/density_function/overworld/continents.json`
- `openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json`
- `openloader/data/ascendant_realms_atlas/data/minecraft/worldgen/density_function/overworld/continents.json`

Do not use the `/ascatlas sample_grid`, `/ascatlas sample_surface_grid`, or `/ascatlas sample_land_water` results as terrain signoff while random mode is active. Those commands were built around the disabled coordinate-aware biome source. Use a fresh world after active sync and visually confirm that normal Tectonic/Terralith terrain no longer has Atlas compass-region cuts.

## 2026-06-17 Hydrology/Gradient Rewrite Pending Fresh-World Proof

- Source helper now has hydrology-first biome selection: climate/continentalness/query-Y context is resolved before ocean/river/wetland biome candidates can win.
- Source helper now has continuous domain-warped region weights instead of hard axis-dominance sector choice.
- New diagnostics are expected in `hydrology_grid_latest.json`, `region_gradient_grid_latest.json`, `transition_transects_latest.json`, and `invalid_ocean_selections_latest.json`.
- This targets the latest visual failures: `minecraft:ocean` on high dry jungle/badlands terrain near `/tp @s 2375 170 1895`, land structures appearing as ocean islands, hard southeast/Sunreach cuts, and abrupt north snow/green transitions.
- Status: not accepted until Jayden validates a fresh world with the new commands.

Status: PENDING FRESH-WORLD RETEST - source helper `E06BE804` adds a southeast transition hotfix after screenshots showed `minecraft:ocean` being located on high jungle/badlands terrain around `/tp @s 2375 141 1895`, water/island structures spawning in the wrong context near `/tp @s 1527 86 1344`, and a hard southeast/Sunreach terrain line near `/tp @s 1178 101 1373`. The hotfix removes ocean biome IDs from the south-east pool, stretches climate-gradient saturation from 3000 to 12000 blocks, adds south-east natural land bias, and softens straight Atlas sector boundaries. Terrain is not signed off until fresh-world visual retest confirms the ocean label, island structures, and hard climate cuts are gone.

Generated: 2026-06-17T22:35:22Z from the latest active `Ascendant Realms (2)` reports. Updated after the v2 natural land-bias validation run.

## Sample Summary

| Metric | Count |
|---|---:|
| Biome-source validation samples | 181 |
| Biome-source completed samples | 181 |
| Biome-source pool mismatches | 0 |
| Biome-source snow outside cold/Frostmarch pools | 0 |
| Biome-source cave-like Y=80 hits | 0 |
| Surface validation samples | 181 |
| Surface completed samples | 181 |
| Normal surface samples | 181 |
| Surface samples at or below y=-60 | 0 |
| Surface samples reporting cave-like biomes | 0 |
| Surface actual biome outside expected pool | 0 |
| Surface accepted transition edge cases | 0 |
| Surface snow outside cold/Frostmarch pools | 0 |
| Surface water blocks in south/west review pools | 12 |
| Surface sample errors | 0 |
| Land/water probe samples | 181/181 |
| Land/water water surface samples | 28 |
| Land-first ocean leaks | 1 |
| Land-first basin leaks | 0 |
| Preserved water feature samples | 27 |
| Land/water manual-review samples | 0 |
| Failed Option C chunks corrected | 80 |
| Failed Option C blocks changed | 990278 |

Biome-source validation: passing.

Surface terrain validation: passing.

Land/water validation: nearly passing but not signed off. The latest completed run found 1 land-first `ocean_leak`, 0 land-first `basin_leak`, and 27 preserved water features. It also confirmed the terrain mutation path was disabled, so the shelf/fill artifact did not return.

Fast no-chunkgen samples are source-level biome-selection evidence only; they are not counted as normal surface-height proof.

## Resolved Surface Mismatch

The previous `/tp @s 10000 147 8000` mismatch is resolved in the latest source and surface reports. It now resolves as `south_east`, with the actual biome in the expected pool. Jayden visually confirmed the area looks pretty good: a small jungle next to canyons and beach terrain. Do not add `minecraft:badlands` broadly to east/Verdant pools.

| x,z | Atlas region | Climate sector | Distance ring | Expected pool | Actual biome | Surface block | Surface Y | Suggested teleport |
|---|---|---|---|---|---|---|---:|---|
| 10000,8000 | `south_east_wilds` | `south_east` | `tier_4_dragon_scars` | `south_east` | `terralith:red_oasis` | `minecraft:grass_block` | 150 | `/tp @s 10000 147 8000` |

## Land/Water Coherence

- Latest completed command source: `in_game_ascatlas_sample_land_water_command`.
- Latest completed command radius/step: 30000 / 5000.
- Latest completed command status: complete, 181/181 samples.
- Prototype mode: `prototype_disabled_no_terrain_mutation`.
- Terrain signoff flag in report: `blocked_until_fresh_world_manual_visual_validation`.
- Land-first samples: 80.
- Water surface samples: 28.
- Preserved water feature samples: 27.
- Land-first ocean leaks: 1.
- Land-first basin leaks: 0.
- Needs manual review: 0.
- Visual shelf result: the rejected correction path is disabled and changed 0 blocks in this run.
- Current fix status: v2 solved the far west/south/southwest rim leaks; only inner-west `/tp @s -2000 71 0` remains.

| x,z | Atlas region | Climate sector | Distance ring | Actual biome | Surface block | Surface Y | Local water % | Nearby land % | Estimated size | Classification | Suggested teleport |
|---|---|---|---|---|---|---:|---:|---:|---|---|---|
| -2000,0 | `stoneback_highlands` | `west` | `tier_1_inner_wilds` | `minecraft:windswept_forest` | `minecraft:water` | 63 | 96.00 | 4.00 | `ocean_like_local_basin` | `ocean_leak` | `/tp @s -2000 71 0` |

## Failed Block-Fill Prototype Evidence

- Report: `config/ascendant_atlas/reports/terrain_wrapper_test_latest.json`.
- Status during the just-completed run: `running`.
- Prototype option: `C_region_aware_ocean_basin_correction_pass`.
- Tectonic-compatible path active: true.
- Generator replaced: false.
- Noise settings changed: false.
- Chunks scanned: 5634.
- Chunks corrected: 80.
- Columns corrected: 19909.
- Blocks changed: 990278.
- Deep water columns detected: 21940.
- Last wrapper error: `None`.

This proved the correction path had major impact, but Jayden's screenshots showed the visual result was unacceptable because it filled finished water basins with helper-chosen stone/terracotta. Treat this as rejected evidence only.

## Natural Density-Bias Prototype

- Source helper hash: `E06BE804`.
- Active helper hash after sync: `E06BE804`.
- New helper type: `ascendant_atlas_regions:atlas_land_bias`.
- New override: `data/minecraft/worldgen/density_function/overworld/continents.json`.
- Mechanism: adds a coordinate-aware continentalness bias in Atlas south/west/southwest/south-east land-first sectors before Tectonic's continent/depth splines generate terrain.
- Latest validated v2 result: 1 `ocean_leak`, 0 `basin_leak`, no source/surface mismatches, and no block mutation.
- Synced v3 hotfix: south-east pool now excludes `minecraft:ocean`, `minecraft:deep_ocean`, `minecraft:lukewarm_ocean`, `minecraft:deep_lukewarm_ocean`, and `minecraft:warm_ocean`; helper gradient saturation is now 12000 blocks; sector lines use a low-frequency softened dominance ratio; and `atlas_land_bias` now supports south-east land bias.
- V3 source tuning: south outer bias `0.86`, south-east outer bias `0.58`, west outer bias `0.82`, and south-west outer bias `0.96`; inner bias remains modest.
- Block mutation: none.
- Tectonic path: still `minecraft:noise` generator with `minecraft:overworld` settings.
- North transition change: gradient saturation now happens over 12000 blocks instead of 3000 so the `-310, -509` screenshot pattern should move toward green/cool/taiga/snow/frozen progression instead of abrupt snow/grass flips.
- Signoff: pending fresh-world validation and Jayden visual review.

## Southeast Hotfix Retest Points

| Issue | Coordinate | Expected after v3 |
|---|---|---|
| `minecraft:ocean` label on high jungle/badlands terrain | `/tp @s 2375 141 1895` | Should no longer locate as `minecraft:ocean`; south-east should be land-first jungle/savanna/badlands/wetland transition. |
| Water/island structure cluster in wrong local context | `/tp @s 1527 86 1344` | Ocean-only/island-only structures should not be encouraged by a south-east ocean biome label. |
| Straight terrain cut between southeast/Sunreach | `/tp @s 1178 101 1373` | Transition should be softer and less ruler-straight in newly generated terrain. |

## Border Visibility Buffer

The latest visual pass found that terrain outside the 30000-block world border can visibly snap to the shared `outer` table. Source now delays the shared outer pool until 50000 blocks while keeping the actual playable border at 30000 blocks. This square-border visual buffer covers cardinal edges and corners; it does not expand the playable world, add content, or change roads/villages/structures.

The buffer has been synced into active `Ascendant Realms (2)`. It still needs an in-game visual check at the world border.

## Accepted Transition Edge Cases

- Accepted transition edge cases in the latest surface report: 0.
- The `stoneback_frostmarch_transition_river` rule remains valid if `minecraft:frozen_river` reappears at a northwest Stoneback/Frostmarch edge over ice/water without snow-rule violations.
- Boundary: do not add `minecraft:frozen_river` to every west/Stoneback pool.
- Signoff: accepted transition edges are not terrain signoff.

| x,z | Classification | Atlas region | Climate sector | Actual biome | Surface block | Surface Y | Reason |
|---|---|---|---|---|---|---:|---|
| none | none | none | none | none | none | none | none |

## Static Validation

| Check | Result | Evidence |
|---|---|---|
| Helper registers regional biome source | PASS | Entrypoint uses Forge DeferredRegister for `ascendant_atlas_regions:regional_multi_noise`. |
| Overworld override uses Atlas biome source | PASS | `ascendant_atlas_regions:regional_multi_noise` |
| Tectonic terrain shape is not bypassed | PASS | generator `minecraft:noise`, settings `minecraft:overworld` |
| Natural Atlas land-bias density function registered | PASS STATIC / PENDING IN-GAME | Source and active helper `E06BE804` register `ascendant_atlas_regions:atlas_land_bias`, and the active OpenLoader datapack includes the v3 south-east bias fields. |
| Terralith biome entries are still used | PASS | Active pools still include Terralith biome IDs. |
| No missing configured biome IDs | PASS | `config/ascendant_atlas/reports/missing_biomes.json` reports 0 missing IDs. |
| Coordinate math handles quart coords | PASS | Helper converts biome-source quart coordinates to block coordinates before Atlas region selection. |
| Old worlds are invalid tests | PASS | The correction is fresh-chunk-only; old chunks can preserve old water basins. |
| Alex's Mobs first-login book crash path | FIXED FOR RETEST | `giveBookOnStartup=false` is synced in source and active instance. |

## Command Surface

Required next fresh-world retest:

```mcfunction
/ascatlas dump_terrain_noise_policy
/ascatlas dump_biome_pools
/ascatlas sample_grid 12000 2000
/ascatlas sample_surface_grid 12000 2000
/ascatlas sample_land_water 30000 5000
```

Manual screenshot retest points:

```mcfunction
/tp @s -29989 120 3
/tp @s 703 141 1129
/tp @s -310 153 -509
```

Do not rerun `/ascatlas classify_water_bodies 30000 5000` for this pass unless we specifically need the older water-body report again; it is lag-heavy and the newer `sample_land_water` report is the current terrain proof.

## Source-Level Grid

This is the fast no-chunkgen biome-source proof. It must stay separate from surface terrain evidence.

Current authoritative per-sample data is in `config/ascendant_atlas/reports/sample_grid_source_latest.json`, `config/ascendant_atlas/reports/sample_grid_surface_latest.json`, and `config/ascendant_atlas/reports/land_water_coherence_latest.json`. If any table below appears stale after a live run, prefer those JSON reports.

| x,z | Atlas region | Climate sector | Distance ring | Expected pool | Actual biome ID | In expected pool | Sample mode | Surface Y | Surface block | Temperature | Precipitation | Snow allowed | Cave at surface | Visual match | Transition |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| -12000,-12000 | `north_west_marches` | `north_west` | `tier_5_corrupted_rim` | `north_west` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,-10000 | `north_west_marches` | `north_west` | `tier_5_corrupted_rim` | `north_west` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,-8000 | `stoneback_highlands` | `west` | `tier_5_corrupted_rim` | `west` | `terralith:highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,-6000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,-4000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `minecraft:stony_peaks` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,-2000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:temperate_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,0 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:alpine_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,2000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:forested_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,4000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:forested_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,6000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,8000 | `stoneback_highlands` | `west` | `tier_5_corrupted_rim` | `west` | `terralith:temperate_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,10000 | `south_west_wilds` | `south_west` | `tier_5_corrupted_rim` | `south_west` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -12000,12000 | `south_west_wilds` | `south_west` | `tier_5_corrupted_rim` | `south_west` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,-12000 | `north_west_marches` | `north_west` | `tier_5_corrupted_rim` | `north_west` | `terralith:wintry_forest` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,-10000 | `north_west_marches` | `north_west` | `tier_5_corrupted_rim` | `north_west` | `terralith:glacial_chasm` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,-8000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,-6000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,-4000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:alpine_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,-2000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,0 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `minecraft:stony_peaks` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,2000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:alpine_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,4000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:forested_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,6000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,8000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:temperate_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,10000 | `south_west_wilds` | `south_west` | `tier_5_corrupted_rim` | `south_west` | `minecraft:badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -10000,12000 | `south_west_wilds` | `south_west` | `tier_5_corrupted_rim` | `south_west` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,-12000 | `frostmarch` | `north` | `tier_5_corrupted_rim` | `north` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,-8000 | `north_west_marches` | `north_west` | `tier_4_dragon_scars` | `north_west` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,-6000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:forested_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,-4000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:rocky_mountains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,-2000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:rocky_mountains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,0 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:alpine_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,2000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `minecraft:windswept_hills` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,4000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:forested_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,6000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,8000 | `south_west_wilds` | `south_west` | `tier_4_dragon_scars` | `south_west` | `minecraft:badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -8000,12000 | `sunreach` | `south` | `tier_5_corrupted_rim` | `south` | `minecraft:badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:snowy_cherry_grove` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:glacial_chasm` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,-6000 | `north_west_marches` | `north_west` | `tier_3_ancient_frontiers` | `north_west` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,-4000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:painted_mountains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,-2000 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:alpine_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,0 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:rocky_mountains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,2000 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:forested_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,4000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:rocky_mountains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,6000 | `south_west_wilds` | `south_west` | `tier_3_ancient_frontiers` | `south_west` | `minecraft:desert` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:arid_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -6000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:savanna_plateau` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:wintry_forest` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:wintry_forest` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,-6000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,-4000 | `north_west_marches` | `north_west` | `tier_2_outer_marches` | `north_west` | `terralith:glacial_chasm` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,-2000 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:granite_cliffs` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,0 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:forested_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,2000 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:white_cliffs` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,4000 | `south_west_wilds` | `south_west` | `tier_2_outer_marches` | `south_west` | `minecraft:badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,6000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -4000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:wintry_forest` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `terralith:wintry_forest` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,-6000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,-4000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `terralith:glacial_chasm` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,-2000 | `north_west_marches` | `north_west` | `tier_1_inner_wilds` | `north_west` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,0 | `stoneback_highlands` | `west` | `tier_1_inner_wilds` | `west` | `terralith:alpine_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,2000 | `south_west_wilds` | `south_west` | `tier_1_inner_wilds` | `south_west` | `minecraft:savanna` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,4000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `minecraft:badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,6000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:red_oasis` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -2000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,-10000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,-6000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,-4000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `terralith:glacial_chasm` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,-2000 | `frostmarch` | `north` | `tier_1_inner_wilds` | `north` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,0 | `hearthlands` | `center` | `tier_0_hearthlands` | `center` | `minecraft:birch_forest` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,2000 | `sunreach` | `south` | `tier_1_inner_wilds` | `south` | `minecraft:savanna` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,4000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:fractured_savanna` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,6000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:white_mesa` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:savanna_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,10000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:fractured_savanna` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:white_mesa` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:wintry_forest` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `terralith:wintry_forest` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,-6000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,-4000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,-2000 | `north_east_marches` | `north_east` | `tier_1_inner_wilds` | `north_east` | `terralith:cold_shrubland` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,0 | `verdant_coast` | `east` | `tier_1_inner_wilds` | `east` | `minecraft:deep_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,2000 | `south_east_wilds` | `south_east` | `tier_1_inner_wilds` | `south_east` | `terralith:arid_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,4000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:arid_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,6000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:arid_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:white_mesa` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:savanna_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 2000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:arid_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:wintry_forest` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `terralith:glacial_chasm` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,-6000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `terralith:siberian_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,-4000 | `north_east_marches` | `north_east` | `tier_2_outer_marches` | `north_east` | `terralith:wintry_forest` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,-2000 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:beach` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,0 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:deep_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,2000 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:deep_lukewarm_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,4000 | `south_east_wilds` | `south_east` | `tier_2_outer_marches` | `south_east` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,6000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:fractured_savanna` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 4000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:frozen_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,-6000 | `north_east_marches` | `north_east` | `tier_3_ancient_frontiers` | `north_east` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,-4000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,-2000 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,0 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,2000 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:sparse_jungle` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,4000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:lukewarm_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,6000 | `south_east_wilds` | `south_east` | `tier_3_ancient_frontiers` | `south_east` | `minecraft:badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:arid_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 6000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:white_mesa` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,-12000 | `frostmarch` | `north` | `tier_5_corrupted_rim` | `north` | `terralith:wintry_lowlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,-8000 | `north_east_marches` | `north_east` | `tier_4_dragon_scars` | `north_east` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,-6000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:beach` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,-4000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:deep_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,-2000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `terralith:cave/underground_jungle` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,0 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:swamp` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,2000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:jungle` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,4000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:river` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,6000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `terralith:cave/underground_jungle` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,8000 | `south_east_wilds` | `south_east` | `tier_4_dragon_scars` | `south_east` | `terralith:red_oasis` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:desert_canyon` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 8000,12000 | `sunreach` | `south` | `tier_5_corrupted_rim` | `south` | `terralith:white_mesa` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,-12000 | `north_east_marches` | `north_east` | `tier_5_corrupted_rim` | `north_east` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,-10000 | `north_east_marches` | `north_east` | `tier_5_corrupted_rim` | `north_east` | `minecraft:snowy_plains` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,-8000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:swamp` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,-6000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,-4000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:river` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,-2000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:lukewarm_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,0 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:river` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,2000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:river` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,4000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:beach` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,6000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:beach` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,8000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,10000 | `south_east_wilds` | `south_east` | `tier_5_corrupted_rim` | `south_east` | `terralith:volcanic_peaks` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 10000,12000 | `south_east_wilds` | `south_east` | `tier_5_corrupted_rim` | `south_east` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,-12000 | `north_east_marches` | `north_east` | `tier_5_corrupted_rim` | `north_east` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,-10000 | `north_east_marches` | `north_east` | `tier_5_corrupted_rim` | `north_east` | `terralith:wintry_lowlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,-8000 | `verdant_coast` | `east` | `tier_5_corrupted_rim` | `east` | `minecraft:lukewarm_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,-6000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:river` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,-4000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:beach` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,-2000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:deep_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,0 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,2000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:deep_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,4000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:beach` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,6000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:deep_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,8000 | `verdant_coast` | `east` | `tier_5_corrupted_rim` | `east` | `minecraft:ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,10000 | `south_east_wilds` | `south_east` | `tier_5_corrupted_rim` | `south_east` | `terralith:arid_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 12000,12000 | `south_east_wilds` | `south_east` | `tier_5_corrupted_rim` | `south_east` | `terralith:red_oasis` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,-5000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,-9000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:frozen_ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,5000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:arid_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 0,9000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:fractured_savanna` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 5000,0 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:ocean` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 9000,0 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:mangrove_swamp` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -5000,0 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:alpine_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -9000,0 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:temperate_highlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 5000,-5000 | `north_east_marches` | `north_east` | `tier_3_ancient_frontiers` | `north_east` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -5000,-5000 | `north_west_marches` | `north_west` | `tier_3_ancient_frontiers` | `north_west` | `minecraft:snowy_taiga` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| 5000,5000 | `south_east_wilds` | `south_east` | `tier_3_ancient_frontiers` | `south_east` | `minecraft:eroded_badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |
| -5000,5000 | `south_west_wilds` | `south_west` | `tier_3_ancient_frontiers` | `south_west` | `minecraft:badlands` | true | `fast_no_chunkgen_noise_biome_y80` | null | `null` | null | null | null | null | pending_manual_review | pending_manual_review |

## Surface Terrain Grid

This is the generated-terrain proof from the latest copied in-game report.

| x,z | Atlas region | Climate sector | Distance ring | Expected pool | Actual biome ID | In expected pool | Sample mode | Surface Y | Surface block | Temperature | Precipitation | Snow allowed | Cave at surface | Visual match | Transition |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| -12000,-12000 | `north_west_marches` | `north_west` | `tier_5_corrupted_rim` | `north_west` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 86 | `snowrealmagic:fence` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,-10000 | `north_west_marches` | `north_west` | `tier_5_corrupted_rim` | `north_west` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 126 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,-8000 | `stoneback_highlands` | `west` | `tier_5_corrupted_rim` | `west` | `terralith:highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 80 | `minecraft:gravel` | 0.4 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,-6000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 82 | `minecraft:stone` | 0.4 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,-4000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `minecraft:stony_peaks` | true | `chunkgen_surface_motion_blocking_no_leaves` | 78 | `minecraft:stone` | 1.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,-2000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:temperate_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,0 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:alpine_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 249 | `minecraft:grass_block` | 0.45 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,2000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:forested_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 83 | `minecraft:stone` | 0.36 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,4000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:forested_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 79 | `minecraft:stone` | 0.36 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,6000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 77 | `minecraft:gravel` | 0.3 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,8000 | `stoneback_highlands` | `west` | `tier_5_corrupted_rim` | `west` | `terralith:temperate_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 80 | `minecraft:grass_block` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,10000 | `south_west_wilds` | `south_west` | `tier_5_corrupted_rim` | `south_west` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 84 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -12000,12000 | `south_west_wilds` | `south_west` | `tier_5_corrupted_rim` | `south_west` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 164 | `minecraft:brown_terracotta` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,-12000 | `north_west_marches` | `north_west` | `tier_5_corrupted_rim` | `north_west` | `terralith:wintry_forest` | true | `chunkgen_surface_motion_blocking_no_leaves` | 273 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,-10000 | `north_west_marches` | `north_west` | `tier_5_corrupted_rim` | `north_west` | `terralith:glacial_chasm` | true | `chunkgen_surface_motion_blocking_no_leaves` | 112 | `minecraft:snow_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,-8000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:snow_block` | 0.3 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,-6000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 76 | `minecraft:gravel` | 0.3 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,-4000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:alpine_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.45 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,-2000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 129 | `minecraft:snow_block` | 0.3 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,0 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `minecraft:stony_peaks` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 1.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,2000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:alpine_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 78 | `minecraft:stone` | 0.45 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,4000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:forested_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 119 | `minecraft:grass_block` | 0.36 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,6000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:rocky_mountains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 223 | `minecraft:cobbled_deepslate` | 0.3 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,8000 | `stoneback_highlands` | `west` | `tier_4_dragon_scars` | `west` | `terralith:temperate_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,10000 | `south_west_wilds` | `south_west` | `tier_5_corrupted_rim` | `south_west` | `minecraft:badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 124 | `minecraft:orange_terracotta` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -10000,12000 | `south_west_wilds` | `south_west` | `tier_5_corrupted_rim` | `south_west` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 83 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,-12000 | `frostmarch` | `north` | `tier_5_corrupted_rim` | `north` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 150 | `minecraft:grass_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,-8000 | `north_west_marches` | `north_west` | `tier_4_dragon_scars` | `north_west` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 76 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,-6000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:forested_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 123 | `minecraft:grass_block` | 0.36 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,-4000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:rocky_mountains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 285 | `minecraft:cobbled_deepslate` | 0.3 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,-2000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:rocky_mountains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 218 | `minecraft:cobbled_deepslate` | 0.3 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,0 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:alpine_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.45 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,2000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `minecraft:windswept_hills` | true | `chunkgen_surface_motion_blocking_no_leaves` | 79 | `minecraft:grass_block` | 0.2 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,4000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:forested_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.36 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,6000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 125 | `minecraft:grass_block` | 0.4 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,8000 | `south_west_wilds` | `south_west` | `tier_4_dragon_scars` | `south_west` | `minecraft:badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 77 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 77 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -8000,12000 | `sunreach` | `south` | `tier_5_corrupted_rim` | `south` | `minecraft:badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 72 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:snowy_cherry_grove` | true | `chunkgen_surface_motion_blocking_no_leaves` | 142 | `minecraft:snow_block` | 0.1 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:glacial_chasm` | true | `chunkgen_surface_motion_blocking_no_leaves` | 79 | `minecraft:snow_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,-6000 | `north_west_marches` | `north_west` | `tier_3_ancient_frontiers` | `north_west` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 78 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,-4000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:painted_mountains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 142 | `minecraft:magenta_terracotta` | 1.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,-2000 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `minecraft:stony_peaks` | true | `chunkgen_surface_motion_blocking_no_leaves` | 130 | `minecraft:stone` | 1.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,0 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:rocky_mountains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 234 | `minecraft:cobbled_deepslate` | 0.3 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,2000 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:forested_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 113 | `minecraft:grass_block` | 0.36 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,4000 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:rocky_mountains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 144 | `minecraft:snow_block` | 0.3 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,6000 | `south_west_wilds` | `south_west` | `tier_3_ancient_frontiers` | `south_west` | `minecraft:desert` | true | `chunkgen_surface_motion_blocking_no_leaves` | 65 | `minecraft:sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:arid_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 77 | `minecraft:red_sand` | 1.6 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 75 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -6000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:savanna_plateau` | true | `chunkgen_surface_motion_blocking_no_leaves` | 119 | `minecraft:grass_block` | 1.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:wintry_forest` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:wintry_forest` | true | `chunkgen_surface_motion_blocking_no_leaves` | 128 | `minecraft:green_terracotta` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 81 | `minecraft:grass_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,-6000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 66 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,-4000 | `north_west_marches` | `north_west` | `tier_2_outer_marches` | `north_west` | `terralith:glacial_chasm` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,-2000 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:granite_cliffs` | true | `chunkgen_surface_motion_blocking_no_leaves` | 78 | `minecraft:stone` | 0.4 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,0 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:forested_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 159 | `minecraft:grass_block` | 0.36 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,2000 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:white_cliffs` | true | `chunkgen_surface_motion_blocking_no_leaves` | 84 | `minecraft:gravel` | 0.4 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,4000 | `south_west_wilds` | `south_west` | `tier_2_outer_marches` | `south_west` | `minecraft:badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 86 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,6000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 238 | `minecraft:terracotta` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 69 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 68 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -4000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 75 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 151 | `minecraft:grass_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:wintry_forest` | true | `chunkgen_surface_motion_blocking_no_leaves` | 115 | `minecraft:snow_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `terralith:wintry_forest` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,-6000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,-4000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `terralith:glacial_chasm` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,-2000 | `north_west_marches` | `north_west` | `tier_1_inner_wilds` | `north_west` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 148 | `minecraft:grass_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,0 | `stoneback_highlands` | `west` | `tier_1_inner_wilds` | `west` | `terralith:alpine_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 81 | `minecraft:grass_block` | 0.45 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,2000 | `south_west_wilds` | `south_west` | `tier_1_inner_wilds` | `south_west` | `minecraft:savanna` | true | `chunkgen_surface_motion_blocking_no_leaves` | 77 | `minecraft:red_sand` | 1.2 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,4000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `minecraft:badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 71 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,6000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:red_oasis` | true | `chunkgen_surface_motion_blocking_no_leaves` | 124 | `minecraft:terracotta` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 78 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 73 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -2000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 76 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,-10000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,-6000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 155 | `minecraft:grass_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,-4000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `terralith:glacial_chasm` | true | `chunkgen_surface_motion_blocking_no_leaves` | 66 | `minecraft:snow_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,-2000 | `frostmarch` | `north` | `tier_1_inner_wilds` | `north` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 101 | `minecraft:grass_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,0 | `hearthlands` | `center` | `tier_0_hearthlands` | `center` | `minecraft:birch_forest` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.6 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,2000 | `sunreach` | `south` | `tier_1_inner_wilds` | `south` | `minecraft:savanna` | true | `chunkgen_surface_motion_blocking_no_leaves` | 68 | `minecraft:red_sand` | 1.2 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,4000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:fractured_savanna` | true | `chunkgen_surface_motion_blocking_no_leaves` | 69 | `minecraft:red_sand` | 1.1 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,6000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:white_mesa` | true | `chunkgen_surface_motion_blocking_no_leaves` | 113 | `minecraft:white_terracotta` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:savanna_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 121 | `minecraft:brown_terracotta` | 1.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,10000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:fractured_savanna` | true | `chunkgen_surface_motion_blocking_no_leaves` | 74 | `minecraft:red_sand` | 1.1 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:white_mesa` | true | `chunkgen_surface_motion_blocking_no_leaves` | 68 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:wintry_forest` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `terralith:wintry_forest` | true | `chunkgen_surface_motion_blocking_no_leaves` | 195 | `minecraft:snow_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,-6000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 74 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,-4000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 82 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,-2000 | `north_east_marches` | `north_east` | `tier_1_inner_wilds` | `north_east` | `terralith:cold_shrubland` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.14 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,0 | `verdant_coast` | `east` | `tier_1_inner_wilds` | `east` | `minecraft:deep_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,2000 | `south_east_wilds` | `south_east` | `tier_1_inner_wilds` | `south_east` | `terralith:arid_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 1.6 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,4000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:arid_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 1.6 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,6000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:arid_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 97 | `minecraft:red_sand` | 1.6 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:white_mesa` | true | `chunkgen_surface_motion_blocking_no_leaves` | 104 | `minecraft:white_terracotta` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:savanna_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 64 | `minecraft:black_terracotta` | 1.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 2000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:arid_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 75 | `minecraft:red_sand` | 1.6 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `terralith:wintry_forest` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `terralith:glacial_chasm` | true | `chunkgen_surface_motion_blocking_no_leaves` | 89 | `minecraft:packed_ice` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,-6000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `terralith:siberian_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 141 | `minecraft:coarse_dirt` | 0.13 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,-4000 | `north_east_marches` | `north_east` | `tier_2_outer_marches` | `north_east` | `terralith:wintry_forest` | true | `chunkgen_surface_motion_blocking_no_leaves` | 251 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,-2000 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:beach` | true | `chunkgen_surface_motion_blocking_no_leaves` | 76 | `minecraft:sand` | 0.8 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,0 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:deep_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,2000 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:deep_lukewarm_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,4000 | `south_east_wilds` | `south_east` | `tier_2_outer_marches` | `south_east` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,6000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 76 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 72 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:fractured_savanna` | true | `chunkgen_surface_motion_blocking_no_leaves` | 75 | `minecraft:red_sand` | 1.1 | rain | false | false | pending_manual_review | pending_manual_review |
| 4000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 78 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,-12000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 136 | `minecraft:grass_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,-8000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:frozen_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 76 | `minecraft:snow_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,-6000 | `north_east_marches` | `north_east` | `tier_3_ancient_frontiers` | `north_east` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 84 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,-4000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 167 | `minecraft:grass_block` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,-2000 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 207 | `minecraft:grass_block` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,0 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 77 | `minecraft:grass_block` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,2000 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:sparse_jungle` | true | `chunkgen_surface_motion_blocking_no_leaves` | 77 | `minecraft:grass_block` | 0.95 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,4000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:lukewarm_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,6000 | `south_east_wilds` | `south_east` | `tier_3_ancient_frontiers` | `south_east` | `minecraft:badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,8000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `minecraft:badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 72 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:arid_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 70 | `minecraft:red_sand` | 1.6 | rain | false | false | pending_manual_review | pending_manual_review |
| 6000,12000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:white_mesa` | true | `chunkgen_surface_motion_blocking_no_leaves` | 71 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,-12000 | `frostmarch` | `north` | `tier_5_corrupted_rim` | `north` | `terralith:wintry_lowlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 71 | `minecraft:snow_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,-10000 | `frostmarch` | `north` | `tier_4_dragon_scars` | `north` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 162 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,-8000 | `north_east_marches` | `north_east` | `tier_4_dragon_scars` | `north_east` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,-6000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:beach` | true | `chunkgen_surface_motion_blocking_no_leaves` | 82 | `minecraft:sand` | 0.8 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,-4000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:deep_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,-2000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `terralith:rocky_jungle` | true | `chunkgen_surface_motion_blocking_no_leaves` | 177 | `minecraft:andesite` | 0.95 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,0 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:swamp` | true | `chunkgen_surface_motion_blocking_no_leaves` | 69 | `minecraft:grass_block` | 0.8 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,2000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:jungle` | true | `chunkgen_surface_motion_blocking_no_leaves` | 122 | `minecraft:grass_block` | 0.95 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,4000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:river` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,6000 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:river` | true | `chunkgen_surface_motion_blocking_no_leaves` | 239 | `minecraft:grass_block` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,8000 | `south_east_wilds` | `south_east` | `tier_4_dragon_scars` | `south_east` | `terralith:red_oasis` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,10000 | `sunreach` | `south` | `tier_4_dragon_scars` | `south` | `terralith:desert_canyon` | true | `chunkgen_surface_motion_blocking_no_leaves` | 200 | `minecraft:sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 8000,12000 | `sunreach` | `south` | `tier_5_corrupted_rim` | `south` | `terralith:white_mesa` | true | `chunkgen_surface_motion_blocking_no_leaves` | 71 | `minecraft:red_sand` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,-12000 | `north_east_marches` | `north_east` | `tier_5_corrupted_rim` | `north_east` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 67 | `minecraft:stone` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,-10000 | `north_east_marches` | `north_east` | `tier_5_corrupted_rim` | `north_east` | `minecraft:snowy_plains` | true | `chunkgen_surface_motion_blocking_no_leaves` | 80 | `minecraft:grass_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,-8000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:swamp` | true | `chunkgen_surface_motion_blocking_no_leaves` | 88 | `minecraft:grass_block` | 0.8 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,-6000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 122 | `minecraft:grass_block` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,-4000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:river` | true | `chunkgen_surface_motion_blocking_no_leaves` | 64 | `minecraft:grass_block` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,-2000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:lukewarm_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,0 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:river` | true | `chunkgen_surface_motion_blocking_no_leaves` | 73 | `minecraft:grass_block` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,2000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:river` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,4000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:beach` | true | `chunkgen_surface_motion_blocking_no_leaves` | 156 | `minecraft:sand` | 0.8 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,6000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:beach` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.8 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,8000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:badlands` | false | `chunkgen_surface_motion_blocking_no_leaves` | 146 | `minecraft:grass_block` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,10000 | `south_east_wilds` | `south_east` | `tier_5_corrupted_rim` | `south_east` | `terralith:volcanic_peaks` | true | `chunkgen_surface_motion_blocking_no_leaves` | 166 | `minecraft:smooth_basalt` | 1.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 10000,12000 | `south_east_wilds` | `south_east` | `tier_5_corrupted_rim` | `south_east` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 94 | `minecraft:terracotta` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,-12000 | `north_east_marches` | `north_east` | `tier_5_corrupted_rim` | `north_east` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,-10000 | `north_east_marches` | `north_east` | `tier_5_corrupted_rim` | `north_east` | `terralith:wintry_lowlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:ice` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,-8000 | `verdant_coast` | `east` | `tier_5_corrupted_rim` | `east` | `minecraft:lukewarm_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,-6000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:river` | true | `chunkgen_surface_motion_blocking_no_leaves` | 122 | `minecraft:grass_block` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,-4000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:beach` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.8 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,-2000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:deep_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,0 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,2000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:deep_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,4000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:beach` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.8 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,6000 | `verdant_coast` | `east` | `tier_4_dragon_scars` | `east` | `minecraft:deep_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,8000 | `verdant_coast` | `east` | `tier_5_corrupted_rim` | `east` | `minecraft:ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,10000 | `south_east_wilds` | `south_east` | `tier_5_corrupted_rim` | `south_east` | `terralith:arid_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 176 | `minecraft:grass_block` | 1.6 | rain | false | false | pending_manual_review | pending_manual_review |
| 12000,12000 | `south_east_wilds` | `south_east` | `tier_5_corrupted_rim` | `south_east` | `terralith:red_oasis` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,-5000 | `frostmarch` | `north` | `tier_2_outer_marches` | `north` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 82 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,-9000 | `frostmarch` | `north` | `tier_3_ancient_frontiers` | `north` | `minecraft:frozen_ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 76 | `minecraft:snow_block` | 0.0 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,5000 | `sunreach` | `south` | `tier_2_outer_marches` | `south` | `terralith:arid_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 77 | `minecraft:grass_block` | 1.6 | rain | false | false | pending_manual_review | pending_manual_review |
| 0,9000 | `sunreach` | `south` | `tier_3_ancient_frontiers` | `south` | `terralith:fractured_savanna` | true | `chunkgen_surface_motion_blocking_no_leaves` | 75 | `minecraft:red_sand` | 1.1 | rain | false | false | pending_manual_review | pending_manual_review |
| 5000,0 | `verdant_coast` | `east` | `tier_2_outer_marches` | `east` | `minecraft:ocean` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 9000,0 | `verdant_coast` | `east` | `tier_3_ancient_frontiers` | `east` | `minecraft:mangrove_swamp` | true | `chunkgen_surface_motion_blocking_no_leaves` | 129 | `minecraft:mud` | 0.8 | rain | false | false | pending_manual_review | pending_manual_review |
| -5000,0 | `stoneback_highlands` | `west` | `tier_2_outer_marches` | `west` | `terralith:alpine_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 75 | `minecraft:stone` | 0.45 | rain | false | false | pending_manual_review | pending_manual_review |
| -9000,0 | `stoneback_highlands` | `west` | `tier_3_ancient_frontiers` | `west` | `terralith:temperate_highlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 130 | `minecraft:clay` | 0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 5000,-5000 | `north_east_marches` | `north_east` | `tier_3_ancient_frontiers` | `north_east` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 78 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| -5000,-5000 | `north_west_marches` | `north_west` | `tier_3_ancient_frontiers` | `north_west` | `minecraft:snowy_taiga` | true | `chunkgen_surface_motion_blocking_no_leaves` | 109 | `minecraft:grass_block` | -0.5 | rain | false | false | pending_manual_review | pending_manual_review |
| 5000,5000 | `south_east_wilds` | `south_east` | `tier_3_ancient_frontiers` | `south_east` | `minecraft:eroded_badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 63 | `minecraft:water` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |
| -5000,5000 | `south_west_wilds` | `south_west` | `tier_3_ancient_frontiers` | `south_west` | `minecraft:badlands` | true | `chunkgen_surface_motion_blocking_no_leaves` | 128 | `minecraft:terracotta` | 2.0 | rain | false | false | pending_manual_review | pending_manual_review |

## Current Verdict

Terrain is not signed off, but it is close. The latest source and surface grids are clean, block filling stayed disabled, land-first basin leaks are 0, and the far west/south/southwest v1 leak set is gone. The only remaining automated land/water failure is `/tp @s -2000 71 0`; Jayden needs to visually decide whether it reads as an unacceptable inland sea or an acceptable Stoneback mountain lake.

Latest visual update: the border snap itself is fixed, and the no-mutation terrain path did not show the artificial shelf/fill artifact in Jayden's prior pass. The remaining blocker is one inner-west water-coherence point, not fake filled terrain.
