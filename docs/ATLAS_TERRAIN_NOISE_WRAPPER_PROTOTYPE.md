# Atlas Terrain Noise Wrapper Prototype

Generated: 2026-06-17

Status: failed prototype, disabled in source. Option C proved the south/west water issue is below biome selection, but Jayden found artificial shelf terrain in Stoneback/Sunreach correction areas. Source helper `E9597A745` disables the post-generation block-fill correction. The current source replacement is the natural `ascendant_atlas_regions:atlas_land_bias` density-function prototype.

## Latest Result

- Active helper in the latest completed in-game run: `82503116`.
- Latest completed in-game run: 181/181 source samples, 181/181 surface samples, 181/181 land/water samples, 0 source mismatches, 0 surface mismatches, 0 cave-like surface biomes, 0 snow-rule violations, 0 land-first `ocean_leak`, 1 land-first `basin_leak`, 1 `needs_manual_review`, and 39 preserved water features.
- Resolved closeout points: `/tp @s 0 71 30000` and `/tp @s 10000 147 8000` looked good in Jayden's visual pass.
- Remaining review points: `/tp @s -25000 71 10000` and `/tp @s 5000 71 10000`.
- The wrapper report recorded 5634 chunks scanned, 80 chunks corrected, 19909 columns corrected, 990278 blocks changed, and no wrapper error.
- Border buffer: source and active `outer_radius_blocks` are now 50000 so terrain visible beyond the 30000-block square border, including corners, should keep directional identity.
- Failure evidence: `/tp @s -29989 120 3` and approximately `/tp @s 703 141 1129` showed artificial corrected stone/terracotta shelves. That invalidates the block-fill approach even with edge softening. Source helper `E9597A745` disables mutation by default and adds the natural land-bias density function.
- Validation caused heavy integrated-server lag during far-chunk generation; use the five-command sequence only for testing.

## Chosen Option

Chosen path: `Option C - region-aware ocean-basin correction pass`.

Decision: rejected for live terrain. Keep this document as failure evidence and rollback context.

Why: the active Overworld still uses `minecraft:noise` with `settings: minecraft:overworld`, and that is how Tectonic/Terratonic stays in the terrain path. A true Option A/B generator wrapper is still the cleanest long-term architecture, but enabling a custom chunk generator immediately would require changing the dimension generator type or codec path and could bypass Tectonic, crash world creation, or fork the noise stack. The current prototype keeps the generator unchanged and adds a feature-flagged correction pass for fresh chunks only.

## What Changed

- New helper class: `AtlasTerrainCorrection`.
- New command: `/ascatlas dump_terrain_noise_policy`.
- New report: `config/ascendant_atlas/reports/terrain_wrapper_test_latest.json`.
- Updated policies:
  - `config/ascendant_atlas/terrain_noise_policy.json`
  - `config/ascendant_atlas/land_water_region_policy.json`
- The helper jar now registers the terrain correction listener alongside the existing Atlas commands.

## Technical Behavior

The failed prototype listened for newly generated Overworld chunks. It skipped existing chunks by default. For each fresh chunk, it:

- confirms the active biome source is `ascendant_atlas_regions:regional_multi_noise`;
- checks the Atlas region at the chunk center;
- acts only in configured land-first regions such as Sunreach, Stoneback, south, southwest, and west;
- skips configured ocean/coastal regions such as Verdant Coast, east, Frostmarch ocean, explicit coast, and outer ocean;
- measures chunk-local surface water ratio and water depth;
- corrected only deep, broad water columns that matched the ocean/basin leak profile;
- avoids overwriting non-air and non-water blocks;
- keeps `minecraft:noise` and `minecraft:overworld` unchanged.

This was not a global water removal pass, but it still failed visually because filling finished chunks with helper-selected blocks does not recreate natural Tectonic/Terralith terrain.

## Tectonic Compatibility

Tectonic compatibility is preserved in the narrow sense that the dimension override is still:

```json
"type": "minecraft:noise",
"settings": "minecraft:overworld",
"biome_source": {
  "type": "ascendant_atlas_regions:regional_multi_noise"
}
```

The prototype did not replace the chunk generator and did not replace noise settings. It was a post-generation correction pass over fresh chunks. That was easy to roll back, but the visual result was unacceptable because it produced artificial shelves instead of natural landforms.

## Risk

Main risks:

- chunk-edge scars if adjacent chunks are not corrected similarly;
- unnatural mesa or highland fill if thresholds are too aggressive;
- lighting or fluid cleanup weirdness because this is post-generation terrain editing;
- validation lag if many large basins are generated at once.

Mitigations:

- fresh chunks only by default;
- feature flag in `terrain_noise_policy.json`;
- high water-ratio and depth requirements;
- maximum lift cap above water so corrected basins cannot become high tablelands;
- no edits outside configured land-first regions;
- no edits to non-air and non-water blocks;
- report written through `terrain_wrapper_test_latest.json`.

## Rollback

Fast rollback:

1. Close Minecraft.
2. Keep `terrain_correction.enabled=false` in `config/ascendant_atlas/terrain_noise_policy.json`.
3. Rebuild and sync helper jar `E9597A745`, or restore a previous helper jar with terrain correction disabled.
4. Create a fresh validation world for retest.

The dimension override does not need rollback for this prototype because it was not changed.

## Test Commands

Run these in a fresh creative validation world after the rebuilt helper jar is synced:

```mcfunction
/ascatlas dump_terrain_noise_policy
/ascatlas dump_biome_pools
/ascatlas sample_grid 12000 2000
/ascatlas sample_surface_grid 12000 2000
/ascatlas sample_land_water 30000 5000
```

Do not use old worlds to judge this. Existing generated chunks are intentionally skipped by the correction pass.

## Manual Spots

Worst known ocean-leak checks:

```mcfunction
/tp @s -25000 71 -5000
/tp @s -20000 71 5000
/tp @s -20000 71 20000
/tp @s -15000 71 15000
/tp @s -5000 71 15000
/tp @s -5000 71 20000
/tp @s 0 71 10000
/tp @s 0 71 12000
/tp @s 0 71 15000
/tp @s 0 71 25000
/tp @s 0 71 30000
/tp @s 5000 71 10000
/tp @s 5000 71 15000
/tp @s 5000 71 20000
/tp @s 15000 71 25000
```

Control spots that should remain acceptable:

```mcfunction
/tp @s 0 71 2000
/tp @s 0 71 20000
/tp @s 10000 71 15000
/tp @s -30000 71 0
```

## Acceptance

Terrain remains blocked until fresh-world validation shows:

- source grid has 0 biome-pool mismatches;
- surface grid has 0 unaccepted biome-pool mismatches;
- cave-like surface biomes remain 0;
- snow outside intended cold regions remains 0;
- `sample_land_water` completes without stalling;
- land-first `ocean_leak` is 0;
- land-first `basin_leak` is 0;
- preserved water features remain;
- Sunreach reads arid and land-first;
- Stoneback reads highland/mountain-first;
- Verdant Coast, coastlines, and Frostmarch frozen water identity remain intact;
- Tectonic terrain still looks like Tectonic.
