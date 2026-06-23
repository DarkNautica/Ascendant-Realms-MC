# Atlas Terrain/Noise Research

Generated: 2026-06-17

Status: investigation complete for the current pass. The research findings first led to the experimental Option C fresh-chunk correction prototype, now documented as failed/disabled in `docs/ATLAS_TERRAIN_NOISE_WRAPPER_PROTOTYPE.md`. Source now implements a natural density-bias prototype at `minecraft:overworld/continents`.

## Scope

This pass investigates why Ascendant Atlas can select correct south/west land biomes while the generated world still contains ocean-scale water basins. It intentionally does not touch roads, bridges, villages, structures, Hunter Boards, Guild Halls, NPC placement, mob ecology, ores, loot, recipes, magic gates, or civilization content.

## Active Overworld Override

Active file:

`config/openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json`

Confirmed active shape:

| Field | Value | Meaning |
| --- | --- | --- |
| Dimension type | `minecraft:overworld` | Normal Overworld dimension behavior. |
| Generator type | `minecraft:noise` | Vanilla-style noise chunk generator remains the chunk generator. |
| Generator settings | `minecraft:overworld` | The active noise-settings key is still `minecraft:overworld`. |
| Biome source | `ascendant_atlas_regions:regional_multi_noise` | Atlas helper owns coordinate-aware biome selection. |
| Terrain/noise owner | Tectonic/Terratonic | The dimension still points at `minecraft:overworld`, which Tectonic/Terratonic overrides by datapack resources. |

Current conclusion: Atlas is active at the biome-source layer, not the chunk/noise layer.

## Helper Mod Boundary

The current local helper jar is `ascendant-atlas-regions-0.1.0.jar`.

Confirmed behavior:

- Registers `ascendant_atlas_regions:regional_multi_noise`.
- Receives quart biome coordinates and converts them to block coordinates before selecting an Atlas region.
- Selects biome pools by Atlas region, climate sector, distance ring, and pool policy.
- Supports `/ascatlas` validation commands.
- Supports land/water probe commands: `/ascatlas terrain_probe`, `/ascatlas terrain_probe_here`, `/ascatlas sample_land_water`, `/ascatlas dump_land_water_policy`, and `/ascatlas dump_terrain_noise_policy`.
- Includes `AtlasTerrainCorrection`, but source helper `E9597A745` disables its post-generation block-fill mutation by default after shelf artifacts were confirmed.
- Registers `ascendant_atlas_regions:atlas_land_bias`, a coordinate-aware density function used by the Atlas datapack to bias south/west/southwest land-first continentalness before Tectonic evaluates terrain.
- Does not replace `minecraft:noise`.
- Does not replace `minecraft:overworld` noise settings.
- Adds a targeted datapack override for `data/minecraft/worldgen/density_function/overworld/continents.json`; it preserves the vanilla shifted continentalness noise and adds only the Atlas land-bias density function.
- Does not lower sea level, change aquifers, or change the final density field.

Why this matters: the helper can prevent a bad biome ID from being selected, but biome selection alone cannot fix an ocean-shaped terrain basin. The rejected Option C prototype was a post-generation correction pass over fresh chunks, not a true terrain generator wrapper, and it failed visually because it filled basins with artificial replacement terrain. The new density-bias prototype acts before terrain is generated.

## Tectonic/Terratonic Path

The active Tectonic config is:

`config/tectonic.json`

The only meaningful public config discovered in the active file/class surface is:

- `legacy_mode`

No direct config knob was found for:

- ocean basin frequency
- continentalness strength
- sea level
- aquifers
- terrain height
- river/lake size

The Tectonic Forge entry point registers an internal server datapack. When Terralith is present, it registers the Terratonic resources instead of plain Tectonic resources. The registered datapack sits at high priority, so it can override `minecraft:overworld` worldgen JSON while the dimension file still says `settings: "minecraft:overworld"`.

Current conclusion: Tectonic is still the terrain/noise shape layer, but the pack is likely using the Terratonic branch because Terralith is installed.

## Important Tectonic/Terratonic Worldgen Targets

The active jars include these relevant worldgen resources:

| Resource | Why it matters |
| --- | --- |
| `data/minecraft/worldgen/noise_settings/overworld.json` | Defines `sea_level`, aquifer behavior, and the noise router. |
| `data/minecraft/worldgen/density_function/overworld/noise_router/continents.json` | Feeds continentalness into terrain shape. |
| `data/minecraft/worldgen/density_function/overworld/noise_router/depth.json` | Feeds vertical terrain depth decisions. |
| `data/minecraft/worldgen/density_function/overworld/noise_router/final_density.json` | Final terrain solid/air shape. High-risk to override. |
| `data/minecraft/worldgen/density_function/overworld/noise_router/fluid_level_floodedness.json` | Influences aquifer/water behavior. |
| `data/minecraft/worldgen/density_function/overworld/noise_router/fluid_level_spread.json` | Influences aquifer/water spread. |
| `data/tectonic/worldgen/density_function/overworld/continents.json` | Tectonic-specific continentalness transform. |
| `data/tectonic/worldgen/density_function/overworld/depth.json` | Tectonic-specific depth transform. |
| `data/tectonic/worldgen/density_function/overworld/aquifer_parameters.json` | Tectonic-specific aquifer control. |

Only `minecraft:overworld/continents` is currently overridden in source. Higher-risk targets such as `final_density`, `depth`, aquifers, and full noise settings remain research-only.

## Sea Level Finding

The active noise settings use normal Overworld sea level behavior. Sea level around 62/63 is expected and should not be treated as the root bug.

The confirmed failure is not "sea level too high." The failure is "land-first Atlas regions can receive ocean-scale basin terrain under valid land biome selections."

## Why Biome Pool Removal Is The Wrong Fix

Current validation says biome-pool leakage is false for the main south/west water issue. That means:

- The selected biome can be valid for Sunreach or Stoneback.
- The surface block can still be `minecraft:water`.
- The terrain shape can still read as an ocean basin.

Removing biome IDs would only hide symptoms and could damage region identity. The fix must affect the land/water terrain decision, not just the biome list.

## Can The Helper Access Noise/Climate Parameters?

At the current biome-source layer, the helper has enough information to choose a biome for a coordinate. It can use region math and the climate target used for biome selection, but it does not own the chunk generator's density field, aquifer fill, or final terrain shape.

For actual land/water correction, the helper would need to expand into one of these:

1. A custom or wrapping chunk generator that delegates to the active noise generator.
2. A controlled datapack/noise-settings override.
3. A controlled density-function override. Source now uses this by adding `ascendant_atlas_regions:atlas_land_bias` to vanilla `minecraft:overworld/continents`.
4. A debug terrain classifier and fresh-chunk correction pass. The classifier exists through `/ascatlas sample_land_water` and writes `terrain_noise_probe_latest.json` plus `land_water_coherence_latest.json`; the correction listener writes `terrain_wrapper_test_latest.json`, but mutation remains disabled.

## Research Verdict

The helper-only biome-source approach cannot solve the south/west ocean basins. Tectonic/Terratonic remains active and is shaping the basins below Atlas biome selection.

The current implemented fix attempt is the least invasive real terrain prototype: a coordinate-aware density-function override at vanilla continentalness. If it fails visual or classifier validation, rollback should be immediate and the next real fix should move to a delegate-based region-aware generator wrapper. Any fix must preserve Tectonic terrain feel, must not globally remove water, and must not return to post-generation block filling.
