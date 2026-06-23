# Atlas Worldgen Failures

Generated: 2026-06-17T14:55:30Z

This file tracks terrain-foundation blockers only. It intentionally does not add Hunter Boards, Guild structures, decorative Atlas structures, village injection, road tuning, loot rewrites, recipe gates, magic gates, rank gates, mobs, or ores.

## 2026-06-18 Superseding Decision

Jayden rejected the coordinate-directed Atlas terrain approach after fresh screenshots still showed hard biome/terrain cuts. The current response is not another Atlas terrain patch. The active source now removes the Atlas Overworld dimension override and Atlas continentalness/land-bias override so normal random Tectonic/Terralith generation returns.

The failures below are historical evidence explaining the rollback. Do not resume north/south/east/west terrain influence unless Jayden explicitly asks for it.

| Issue | Severity | Evidence | Next action |
|---|---|---|---|
| `SOURCE_LEVEL_SAMPLE_PRESENT` | Info | `/ascatlas sample_grid 12000 2000` produced 181/181 source-level samples with 0 mismatches. | Keep this as biome-source evidence until the biome source changes. |
| `SURFACE_SAMPLE_PRESENT_ZERO_MISMATCHES` | Info | `/ascatlas sample_surface_grid 12000 2000` produced 181/181 generated-surface samples with 0 unaccepted mismatches. The old 10000,8000 axis-tie mismatch now resolves as `south_east` and looked good in Jayden's visual pass. | Keep the strict axis-dominance tie rule; do not broadly add badlands to east pools. |
| `OPTION_C_TERRAIN_CORRECTION_REJECTED` | High | Post-generation block-fill pass reduced water in reports, but created artificial Stoneback/Sunreach shelves. | Keep the report as evidence only. Do not use post-generation block filling as the terrain fix. |
| `NATURAL_LAND_BIAS_V1_INSUFFICIENT` | High | Helper `E9597A745` with first natural land-bias pass produced clean source/surface reports and no visible fill shelves, but land/water still reported 7 `ocean_leak` and 2 `basin_leak` samples. | Treat v1 as visually safer but too weak at the far west/south/southwest rim. |
| `NATURAL_LAND_BIAS_V2_NEAR_PASS` | Medium | Active OpenLoader `minecraft:overworld/continents` uses stronger outer-ring bias: south `0.86`, west `0.82`, south-west `0.96`. The v2 report has 0 source mismatches, 0 surface mismatches, 0 basin leaks, and 1 remaining `ocean_leak`. | Visually inspect `/tp @s -2000 71 0`; accept narrowly if it reads as a legitimate Stoneback mountain lake, otherwise tune inner-west bias. |
| `SOUTH_EAST_OCEAN_LABEL_ON_LAND` | Critical | Jayden located `minecraft:ocean` at roughly `/tp @s 2375 141 1895`, but the visible terrain was high jungle/badlands land with a boat/ocean structure. | Source helper now uses hydrology-first biome compatibility filtering so high inland/highland terrain rejects ocean biome candidates. Fresh-world retest required. |
| `SOUTH_EAST_ISLAND_STRUCTURES_WRONG_CONTEXT` | Critical | Jayden found more island/water structures around `/tp @s 1527 86 1344` that should not be on land-first terrain. | Structure Director diagnostics now include Atlas hydrology, but true structure veto is still not available. Retest after biome labels stop lying about ocean context. |
| `STRAIGHT_SECTOR_TERRAIN_CUTS` | Critical | Jayden found a hard line between southeast wilds/Sunreach near `/tp @s 1178 101 1373`, matching a region-boundary style cutoff instead of a natural gradient. | Source helper now uses continuous domain-warped region weights and blended land bias. Validate with transects before signoff. |
| `V1_LAND_FIRST_OCEAN_LEAKS` | Fixed for retest | V1 leak coordinates at the far west/south/southwest rim were gone in the v2 land/water report. | Keep the coordinates historical; only revisit if the next fresh-world run regresses. |
| `V1_LAND_FIRST_BASIN_LEAKS` | Fixed for retest | V1 basin coordinates `/tp @s -25000 71 -5000` and `/tp @s -25000 71 30000` were gone in the v2 land/water report. | Keep basin-leak target at 0. |
| `V2_INNER_STONEBACK_WATER_REVIEW` | High | V2 remaining automated leak: `/tp @s -2000 71 0`, `stoneback_highlands`, `minecraft:windswept_forest`, local water 96%, nearby land 4%, classified as `ocean_like_local_basin`. | Jayden visual review required before changing terrain again. |
| `BORDER_VISIBLE_OUTER_POOL_SNAP` | Fixed for retest | Jayden visually observed that terrain immediately outside the 30000-block border could snap to unrelated outer-pool terrain. | Source and active client now use `outer_radius_blocks: 50000`; Jayden visually confirmed the border problem is fixed. Recheck only if a fresh world shows a new snap. |
| `STONEBACK_CORRECTION_SHELF_EDGE` | Fixed for retest | Jayden visually observed an artificial stone shelf/shear wall at `/tp @s -29989 120 3` after the rejected block-fill pass, then reported no weird fills in the natural-bias pass. | Keep checking this coordinate after v2 to ensure the shelf artifact stays gone. |
| `SUNREACH_CORRECTION_TERRACOTTA_SHELF` | Fixed for retest | Jayden visually observed an artificial terracotta shelf near `/tp @s 703 141 1129` after the rejected block-fill pass, then reported no weird fills in the natural-bias pass. | Keep checking this coordinate after v2 to ensure the shelf artifact stays gone. |
| `NEAR_NORTH_GRADIENT_PATCHINESS` | High | Jayden visually observed near `/tp @s -310 153 -509` that the minimap read as a snow patch followed by greener terrain farther north. | Use northward transects and region-weight reports to verify broad cold progression; local elevation may explain pockets, but repeated warm/cold reversal remains a failure. |
| `PLAYER_DATA_CREATE_WORLD_BOUNCE_FIXED_FOR_RETEST` | Medium | The improper-player-data bounce came from Alex's Mobs first-login book grant colliding with title/advancement handling; `giveBookOnStartup=false` is synced in source and active instance. | Confirm the next fresh world does not bounce back to the menu on first join. |
| `VALIDATION_LAG_EXPECTED` | Medium | The rejected correction report scanned thousands of chunks and changed large numbers of blocks during far validation. | Use validation commands only for testing and wait for them to finish; the natural density prototype should not perform block mutation during normal play. |
| `VISUAL_TERRAIN_REVIEW_PENDING` | High | The reports cannot judge whether the terrain visually matches the intended region. | Jayden must inspect Sunreach/Stoneback and the two flagged coordinates before signoff. |
| `OLD_WORLDS_INVALID` | Medium | Already-generated chunks can preserve old water basins and old biome decisions. | Use fresh worlds or fully ungenerated chunks for all Atlas terrain judgments. |
| `ROAD_TUNING_NOT_INCLUDED` | Low | Roads/bridges are intentionally not tuned in this terrain-first pass. | Document road issues only after terrain validation passes. |

## Terrain Signoff Gate

Atlas terrain does not pass until a fresh world creates cleanly, the five `/ascatlas` validation commands complete, source validation has 0 mismatches, surface validation has 0 unaccepted mismatches, land/water reports 0 land-first `ocean_leak` and 0 land-first `basin_leak`, legitimate rivers/oases/mountain lakes/coastlines remain, Tectonic terrain remains visually intact, Terralith biomes are present, snow stays blocked outside intended cold regions, and Jayden visually confirms Sunreach and Stoneback read correctly.
