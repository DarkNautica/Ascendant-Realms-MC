# Atlas Terrain/Noise Control Plan

Generated: 2026-06-17

Status: natural density-bias v2 tested after failed Option C post-generation block-fill prototype and insufficient v1 natural-bias pass. Terrain is not signed off; 1 inner-west water point remains for visual review.

## Goal

Fix south/west land-water coherence so Sunreach and Stoneback remain land-first while preserving rivers, oases, small lakes, mountain lakes, coastlines, Verdant Coast ocean identity, Frostmarch frozen-ocean identity, and Tectonic-style terrain.

Terrain is not signed off until Jayden validates a fresh-world visual test.

## Current Proof

| Check | Current result |
| --- | --- |
| Atlas biome source | Active through `ascendant_atlas_regions:regional_multi_noise`. |
| Overworld chunk generator | Still `minecraft:noise`. |
| Noise settings key | Still `minecraft:overworld`. |
| Tectonic/Terratonic terrain path | Still active through datapack worldgen resources. |
| Terralith biome entries | Still used by Atlas pools. |
| Helper-only land/water bias | Tested and failed for basin terrain. |
| Post-generation block-fill terrain correction | Rejected; it created artificial shelves. |
| Natural Atlas land-bias density function | Synced and tested in source and active helper `E9597A745`; v2 stronger outer-ring bias reduced failures to 1 inner-west review point. |
| Biome-pool leakage | False for the main south/west water issue. |
| Sea level 62/63 | Normal; not the root problem. |

## Immediate Sync/Test Gate

The synced helper jar now includes `AtlasTerrainCorrection`, `/ascatlas dump_terrain_noise_policy`, and `terrain_wrapper_test_latest.json`, but terrain mutation is disabled after the shelf-artifact failure. Helper `E9597A745` also registers `ascendant_atlas_regions:atlas_land_bias`, and the Atlas OpenLoader datapack now overrides `minecraft:overworld/continents` to apply a south/west/southwest land-first continentalness bias before Tectonic generates terrain. The v1 natural pass produced no visible fill shelves but still reported 7 `ocean_leak` and 2 `basin_leak` samples. The v2 stronger outer-ring pass reports 1 `ocean_leak`, 0 `basin_leak`, and 27 preserved water features. Visual review of `/tp @s -2000 71 0` is the next gate.

Jayden should rerun these commands in a fresh creative validation world or wholly fresh chunks:

```mcfunction
/ascatlas dump_terrain_noise_policy
/ascatlas dump_biome_pools
/ascatlas sample_grid 12000 2000
/ascatlas sample_surface_grid 12000 2000
/ascatlas sample_land_water 30000 5000
```

Do not rerun the lag-heavy `/ascatlas classify_water_bodies 30000 5000` command for this pass. Use `sample_land_water` plus manual teleport review instead.

## Required Fix Shape

The fix must operate below biome selection:

- Atlas biome source remains responsible for region identity.
- Tectonic/Terratonic remains responsible for the base terrain feel.
- A new region-aware terrain/noise layer must prevent ocean-scale basins in land-first Atlas regions.
- Legitimate water must remain.
- The change must be feature-flagged and reversible.
- The change must not fill finished chunks with helper-selected replacement blocks; land must come from natural Tectonic/Terralith terrain generation.

## Technical Options

### Option 1: Keep Biome-Source-Only Atlas

Risk: low

Tectonic feel: preserved

Status: tested and insufficient

Files/classes touched: none beyond the existing helper.

Why it fails: a valid land biome can still be placed over ocean-shaped terrain because the chunk generator owns height, water, and aquifers.

Decision: keep this as the biome identity layer, but do not treat it as the basin fix.

### Option 2: Tectonic Config Tuning

Risk: low

Tectonic feel: preserved

Status: no useful knob found

Files touched:

- `config/tectonic.json`

Finding: the active config only exposes `legacy_mode`. No safe public control was found for ocean basin frequency, continentalness, sea level, aquifers, or height.

Decision: not viable with the current config surface.

### Option 3: Datapack Density Override Prototype

Risk: medium

Tectonic feel: intended to preserve Tectonic because it biases the input continentalness signal before Tectonic's own splines run.

Rollback: remove or disable the datapack override and recreate fresh chunks.

Selected target:

- `minecraft:worldgen/density_function/overworld/continents`

Why this target: Tectonic's `tectonic:overworld/continents` spline reads vanilla `minecraft:overworld/continents`, and Tectonic depth/aquifer functions then use that value. Adding the Atlas bias there gives land-first sectors natural terrain pressure without replacing the generator or filling finished chunks.

Decision: selected as the current source prototype. It requires the helper density type `ascendant_atlas_regions:atlas_land_bias` and must be tested in a fresh world.

### Option 4: Custom Noise Settings Preset

Risk: high

Tectonic feel: uncertain

Files touched:

- OpenLoader dimension override
- custom `worldgen/noise_settings`
- custom density functions

Problem: a copied/forked `minecraft:overworld` preset can accidentally bypass Tectonic/Terratonic updates or permanently fork the terrain stack.

Decision: avoid unless the wrapper path proves impossible.

### Option 5: Region-Aware Chunk Generator Wrapper

Risk: high, but most correct

Tectonic feel: best if delegate-based

Potential files/classes touched:

- `local-mods/ascendant-atlas-regions/src/main/java/...`
- helper generator registration
- new generator codec/serializer
- Atlas region math utilities
- `config/ascendant_atlas/terrain_noise_policy.json`
- `config/ascendant_atlas/land_water_region_policy.json`
- Overworld dimension override only after the wrapper is ready

Target behavior:

- Delegate base generation to the active noise generator and `minecraft:overworld` settings.
- Use Atlas region/ring/sector math at chunk or block coordinates.
- Treat Sunreach and Stoneback as land-first outside explicit coastline/ocean sectors.
- Reject or lift ocean-scale basins in land-first sectors.
- Preserve rivers, oases, small lakes, mountain lakes, coastlines, frozen seas, and Verdant Coast ocean identity.
- Add debug/report mode before any live mutation.
- Avoid neighborhood scans during normal chunk generation.

Decision: preferred implementation path, but not safe to rush as a live rewrite.

### Option 6: Feature-Flagged Fresh-Chunk Terrain Correction

Risk: medium-high

Tectonic feel: mostly preserved if thresholds remain conservative

Files/classes touched:

- `local-mods/ascendant-atlas-regions/src/main/java/.../AtlasTerrainCorrection.java`
- `local-mods/ascendant-atlas-regions/src/main/java/.../AscendantAtlasRegions.java`
- `local-mods/ascendant-atlas-regions/src/main/java/.../AtlasCommands.java`
- `config/ascendant_atlas/terrain_noise_policy.json`
- `config/ascendant_atlas/land_water_region_policy.json`

Target behavior:

- Keep the active generator as `minecraft:noise` with `minecraft:overworld` settings.
- Listen for fresh Overworld chunk loads.
- Act only in configured land-first south/west regions.
- Correct only broad/deep water columns matching the ocean/basin leak signature.
- Preserve rivers, oases, small lakes, mountain lakes, coastlines, Verdant Coast water, and Frostmarch frozen seas by policy and thresholds.
- Skip old chunks by default.

Decision: rejected after visual testing. It changed finished chunks after generation and created artificial Stoneback/Sunreach shelves.

## Least-Risky Prototype From This Pass

This pass implements Option 3 as the current live source prototype:

- `config/ascendant_atlas/terrain_noise_policy.json`
- `config/ascendant_atlas/land_water_region_policy.json`
- `config/openloader/data/ascendant_realms_atlas/data/minecraft/worldgen/density_function/overworld/continents.json`
- `openloader/data/ascendant_realms_atlas/data/minecraft/worldgen/density_function/overworld/continents.json`
- `local-mods/ascendant-atlas-regions/src/main/java/.../AtlasLandBiasDensityFunction.java`
- `local-mods/ascendant-atlas-regions/src/main/java/.../AscendantAtlasRegions.java`
- `local-mods/ascendant-atlas-regions/src/main/java/.../RegionalMultiNoiseBiomeSource.java`
- `local-mods/ascendant-atlas-regions/src/main/java/.../AtlasTerrainCorrection.java`
- `/ascatlas terrain_probe <x> <z>`
- `/ascatlas terrain_probe_here`
- `/ascatlas sample_land_water <radius> <step>`
- `/ascatlas cancel_land_water_sample`
- `/ascatlas dump_land_water_policy`
- `/ascatlas dump_terrain_noise_policy`
- `config/ascendant_atlas/reports/terrain_noise_probe_latest.json`
- `config/ascendant_atlas/reports/land_water_coherence_latest.json`
- `config/ascendant_atlas/reports/terrain_wrapper_test_latest.json`
- this plan document
- the terrain/noise research document
- the Tectonic integration risk document

The prototype is intentionally conservative and fresh-world/fresh-chunk-only for validation. It does not change finished chunks after creation. It biases natural continentalness in south/west/southwest land-first regions, preserves the `minecraft:noise` generator, and keeps `settings: minecraft:overworld` so Tectonic remains in the terrain path.

## Next Code Prototype Recommendation

If the natural density-bias prototype fails, roll it back and add a feature-flagged helper-side terrain/noise wrapper in debug mode first:

1. Register a wrapper generator type without enabling it in the active dimension override.
2. Make it delegate to the normal `minecraft:noise` generator with `minecraft:overworld` settings.
3. Load `terrain_noise_policy.json` and `land_water_region_policy.json`.
4. Add a dry-run report that classifies chunks as land-first, coast-allowed, or water-allowed without mutating terrain.
5. Only after dry-run reports look correct, test terrain adjustment in a disposable fresh world.

## Test Plan

After the helper patch sync:

```mcfunction
/ascatlas dump_terrain_noise_policy
/ascatlas dump_biome_pools
/ascatlas sample_grid 12000 2000
/ascatlas sample_surface_grid 12000 2000
/ascatlas sample_land_water 30000 5000
```

For this probe prototype:

```mcfunction
/ascatlas dump_biome_pools
/ascatlas sample_grid 12000 2000
/ascatlas sample_surface_grid 12000 2000
/ascatlas dump_land_water_policy
/ascatlas terrain_probe_here
/ascatlas sample_land_water 30000 5000
```

Manual visual checks must include Sunreach and Stoneback water points from the water review report plus the screenshot coordinates:

```mcfunction
/tp @s -29989 120 3
/tp @s 703 141 1129
/tp @s -310 153 -509
```

The goal is not "no water." The goal is no ocean-scale or basin-scale leaks in land-first regions, no block-fill shelves, and no near-north snow/grass ping-pong that breaks the Frostmarch gradient.

## Acceptance Criteria

- Source validation: 0 biome-pool mismatches.
- Surface validation: 0 biome-pool mismatches.
- Cave-like surface biomes: 0.
- Snow outside intended cold regions: 0.
- East/west snowy mismatches: 0.
- Land-first south/west ocean leaks: 0.
- Land-first south/west basin leaks: 0.
- Rivers, oases, small lakes, mountain lakes, coastlines, Verdant Coast seas, and Frostmarch frozen seas remain.
- Tectonic-style terrain still looks intact.
- Validation tools do not cause severe tick/server lag.

## Rollback Plan

For the current pass:

- Remove the `data/minecraft/worldgen/density_function/overworld/continents.json` override from both Atlas OpenLoader copies.
- Restore the previous helper jar if the custom density function causes a launch issue.
- Keep `terrain_correction.enabled=false`; do not roll back to post-generation block filling.

For a future code prototype:

1. Close Minecraft.
2. Restore the previous helper jar.
3. Restore the current Overworld override to `minecraft:noise` + `minecraft:overworld` + `ascendant_atlas_regions:regional_multi_noise`.
4. Remove or disable any candidate datapacks.
5. Test only in fresh worlds or ungenerated chunks.

## Current Verdict

Terrain remains pending. Helper `E9597A745` implements the real terrain/noise prototype and v2 density tuning is tested, but it is not accepted until Jayden visually reviews `/tp @s -2000 71 0` and the old shelf coordinates.
