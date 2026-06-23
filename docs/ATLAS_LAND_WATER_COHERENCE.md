# Atlas Land/Water Coherence

## 2026-06-18 Random Worldgen Restore

Status: superseded by rollback. Jayden chose to return to random Tectonic/Terralith generation instead of continuing Atlas north/south/east/west terrain influence.

The land/water reports remain useful evidence, but they are no longer the active closeout path. The active fix is to remove Atlas Overworld worldgen influence:

- no Atlas Overworld dimension override
- no Atlas `minecraft:overworld/continents` land-bias override
- no coordinate-directed hydrology/biome steering as the terrain baseline

Structure and road tuning should be performed against fresh random terrain after active sync.

## 2026-06-17 Hydrology-First Closeout Direction

The rejected block-fill prototype remains disabled. The new fix is not terrain painting.

Atlas now filters biome choices by hydrology context before selecting a Terralith biome parameter point. Ocean biomes are no longer valid on high inland/highland/mountain terrain just because an east or southeast region has ocean entries in its broader pool.

Structure Director diagnostics now read the same hydrology class, so land-only structures can be evaluated against `inland_lowland`, `inland_highland`, and `mountain` rather than only raw local water ratio.

Fresh-world proof is still required. The next validation must focus on `/tp @s 2375 170 1895`, the island-structure examples near `/tp @s 1527 86 1344`, and the southeast/Sunreach transition near `/tp @s 1178 101 1373`.

Generated: 2026-06-17T14:55:30Z

Status: southeast transition hotfix v3 pending fresh-world validation. Option C post-generation block-fill correction is rejected and disabled in source. V2 kept source/surface validation clean, changed 0 blocks through the rejected correction path, and reduced land/water failures to 1 remaining automated `ocean_leak` at `/tp @s -2000 71 0`. V3 responds to screenshots showing `minecraft:ocean` on high southeast jungle/badlands terrain and hard climate cuts near the southeast/Sunreach transition.

This pass is terrain-only. It does not touch mobs, ores, recipes, roads, bridges, villages, structures, Hunter Boards, Guild Halls, NPCs, settlements, loot rewrites, recipe gates, magic gates, or rank enforcement.

## Current Finding

- Sea level 62/63 is normal and is not the bug.
- Biome-pool leakage remains false in the land/water report.
- The terrain/noise correction path must not use post-generation block filling. The source helper now disables that mutation path and registers `ascendant_atlas_regions:atlas_land_bias`.
- New v3 source fix: `data/minecraft/worldgen/density_function/overworld/continents.json` adds Atlas south/west/southwest/south-east continentalness bias before Tectonic generates terrain, so land-first regions become natural landforms instead of filled-in ocean basins.
- South-east pool fix: `south_east` now excludes ocean biome IDs and keeps only land, river, oasis, wetland, jungle, savanna, and badlands transition entries. This targets the high-land `minecraft:ocean` locate result around `/tp @s 2375 141 1895`.
- Gradient fix: helper climate saturation now uses `world_radius_blocks: 12000` instead of `3000`, so north/south transitions should progress over travel distance instead of snapping near spawn.
- Sector-line fix: helper region selection now uses softened low-frequency dominance boundaries instead of perfectly straight sector lines.
- Latest land/water probe: 181/181 samples, 28 water surface samples, 1 land-first ocean leak, 0 land-first basin leaks, 0 needs-manual-review samples, and 27 preserved water-feature samples.
- Previous basin closeout point resolved: `/tp @s 0 71 30000` is now land surface in the report and looked good in Jayden's visual pass.
- Previous surface mismatch resolved: `/tp @s 10000 147 8000` now resolves as `south_east` and looked good in Jayden's visual pass.
- Remaining automated warning: `/tp @s -2000 71 0` in inner Stoneback/highlands, `minecraft:windswept_forest`, surface water at Y63, local water 96%, nearby land 4%, classified as `ocean_like_local_basin`.
- Shelf-artifact result: `/tp @s -29989 120 3` and approximately `/tp @s 703 141 1129` previously showed artificial Stoneback/Sunreach stone or terracotta shelf terrain. Synced helper `E06BE804` keeps post-generation block filling disabled, and Jayden did not find weird fills in the latest pass.
- Near-north gradient evidence: `/tp @s -310 153 -509` looked like a snow patch followed by greener terrain farther north. Synced helper `E06BE804` stretches climate saturation to 12000 blocks and keeps `center_radius_blocks: 500`.
- Active helper during the latest completed in-game report: `E9597A745`. Source and active `Ascendant Realms (2)` are now synced to helper `E06BE804` for the v3 southeast transition hotfix. Source and active `Ascendant Realms (2)` already use a `50000`-block biome-source visual buffer so it covers the 30000-block square world border edges and corners.

## Active Terrain Stack

| Layer | Active value | Evidence |
|---|---|---|
| Overworld dimension type | `minecraft:overworld` | `config/openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json` |
| Chunk generator | `minecraft:noise` | The dimension override still uses vanilla noise generation. |
| Noise settings key | `minecraft:overworld` | Atlas does not replace the full noise settings JSON. |
| Continentalness override | `minecraft:overworld/continents` plus `ascendant_atlas_regions:atlas_land_bias` | Source v3 prototype biases natural terrain generation in south/west/southwest/south-east land-first sectors. |
| Biome source | `ascendant_atlas_regions:regional_multi_noise` | The helper owns regional biome selection. |
| Tectonic role | terrain/noise shape layer | Tectonic remains in the Overworld path through `minecraft:overworld` settings. |
| Terralith role | primary biome table provider | Active pools include Terralith entries and audit-backed climate data. |

## Option C Correction Result

| Metric | Value |
|---|---:|
| Chunks scanned | 5634 |
| Eligible chunks | 80 |
| Chunks corrected | 80 |
| Columns corrected | 19909 |
| Blocks changed | 990278 |
| Water columns detected | 36757 |
| Deep water columns detected | 21940 |
| Skipped existing chunks | 37 |
| Skipped non-land-first chunks | 5266 |
| Skipped below threshold | 251 |

The improvement was large, but this result is not accepted because the same prototype created artificial shelves. Keep this table only as evidence that the issue is below biome selection and that brute-force terrain filling is visually wrong.

## Natural Terrain Prototype

| Item | Value |
|---|---|
| Source helper hash | `E06BE804` |
| Active helper after sync | `E06BE804` |
| Helper density type | `ascendant_atlas_regions:atlas_land_bias` |
| Datapack hook | `data/minecraft/worldgen/density_function/overworld/continents.json` |
| Mechanism | Coordinate-aware continentalness bias in south/west/southwest/south-east land-first sectors. V3 also removes south-east ocean biome IDs and softens straight sector boundaries. |
| Finished-block replacement | No |
| Tectonic preserved | Intended; still uses `minecraft:overworld` settings. |
| Validation status | Pending fresh-world test. |

## Closeout Diagnosis

- `/tp @s 0 71 30000`: resolved in the latest report as land surface, `terralith:red_oasis`, surface Y82, `minecraft:light_gray_terracotta`, local water 0%, nearby land 100%. Jayden visually confirmed it looks good.
- `/tp @s 10000 147 8000`: resolved in the latest source and surface reports as `south_east`, `terralith:red_oasis`, surface Y150, and in the expected pool. Jayden visually confirmed it looks good with a small jungle, canyons, and beach terrain.
- The far west/south/southwest v1 leak set is resolved by v2. The only remaining automated warning is inner-west `/tp @s -2000 71 0`.
- The current active fix is v2 natural land bias, not a block-fill pass. Visually inspect `/tp @s -2000 71 0` before deciding whether to accept it as a mountain-lake edge case or tune a narrow v3 inner-west bias.
- No broad patch was made: `minecraft:badlands` was not added to all east/Verdant pools, no water was removed globally, and sea level was not changed.
- V3 also does not remove Verdant Coast ocean identity. Pure east/far coast remains the ocean/coastal route; south-east is now the land-first transition between Sunreach and Verdant.

## Southeast Screenshot Failures

| Coordinate | Symptom | V3 expected result |
|---|---|---|
| `/tp @s 2375 141 1895` | `minecraft:ocean` was located on high jungle/badlands terrain, inviting an ocean/boat structure into the wrong context. | No ocean biome label in south-east; terrain should read as land-first jungle/savanna/badlands/wetland transition. |
| `/tp @s 1527 86 1344` | Island/water structures appeared where the terrain should not be water-only structure context. | Ocean-only structure context should not be selected from south-east biome identity. |
| `/tp @s 1178 101 1373` | Southeast/Sunreach terrain changed in a straight, hard line. | Sector line should be softer and less straight in fresh terrain. |

## Water Samples By Classification

| Classification | Count |
|---|---:|
| `acceptable_coastline` | 13 |
| `acceptable_lake` | 5 |
| `acceptable_mountain_lake` | 4 |
| `acceptable_oasis` | 3 |
| `acceptable_river` | 2 |
| `land_surface` | 153 |
| `ocean_leak` | 1 |

## Remaining Leak Detail

| x,z | Region | Climate sector | Distance ring | Actual biome | Surface block | Surface Y | Local water % | Nearby land % | Estimated size | Classification | Suggested teleport |
|---|---|---|---|---|---|---:|---:|---:|---|---|---|
| -2000,0 | `stoneback_highlands` | `west` | `tier_1_inner_wilds` | `minecraft:windswept_forest` | `minecraft:water` | 63 | 96.00 | 4.00 | `ocean_like_local_basin` | `ocean_leak` | `/tp @s -2000 71 0` |

## Shelf Artifact Detail

| x,z | Region | Symptom | Status |
|---|---|---|---|
| -29989,3 | Stoneback/far west edge | Artificial stone shelf and shear wall after basin correction. | Synced helper `E06BE804` disables block-fill correction and adds natural land-bias density; retest in a fresh world. |
| 703,1129 | Sunreach/inner south | Artificial terracotta shelf near structures and water. | Synced helper `E06BE804` disables block-fill correction and adds natural land-bias density; retest in a fresh world. |
| -310,-509 | Near-north Hearthlands/Frostmarch edge | Snow patch then greener terrain farther north felt backwards. | Synced helper `E06BE804` stretches climate saturation to 12000 blocks and keeps center radius 500; retest in a fresh world. |

## Border Visibility Buffer

Jayden's visual pass found the biome identity can visibly snap outside the 30000-block world border. Source now sets the helper biome-source `outer_radius_blocks` to 50000 while leaving the playable/runtime world radius at 30000 and the world border diameter at 60000. The higher cutoff is intentional because the world border is square while the helper cutoff is radial; 50000 covers the cardinal edges, corners, and visible terrain just beyond the barrier so those areas keep the same directional Atlas identity.

The 50000-block buffer is synced into active `Ascendant Realms (2)`, and Jayden visually confirmed the border snap problem is fixed. Only recheck border edges/corners if a new world shows a fresh snap.

## Player Data Error Note

The new-world bounce was not caused by Atlas terrain correction. Logs showed an Alex's Mobs first-login item grant colliding with title/advancement handling. `config/alexsmobs.toml` now has `giveBookOnStartup=false` in both source and the active CurseForge instance, and `scripts/sync-active-client-files.ps1` now syncs that file.

## Acceptance Criteria

- Source validation remains 0 biome-pool mismatches.
- Surface validation remains 0 unaccepted biome-pool mismatches.
- Cave-like surface biomes remain 0.
- Snow outside intended cold regions remains 0.
- Land-first `ocean_leak` becomes 0 or the only remaining point is manually accepted as a legitimate Stoneback mountain-lake edge case.
- Land-first `basin_leak` remains 0.
- Rivers, oases, mountain lakes, coastlines, Verdant Coast water, and Frostmarch frozen water remain.
- Manual review confirms Sunreach is arid/land-first and Stoneback is highland/mountain-first.
- Tectonic terrain still looks intact.

## Next Retest Commands

```mcfunction
/ascatlas dump_terrain_noise_policy
/ascatlas dump_biome_pools
/ascatlas sample_grid 12000 2000
/ascatlas sample_surface_grid 12000 2000
/ascatlas sample_land_water 30000 5000
```

Manual follow-up points after the commands:

```mcfunction
/tp @s -25000 71 10000
/tp @s 5000 71 10000
```
