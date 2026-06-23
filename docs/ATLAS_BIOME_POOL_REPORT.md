# Atlas Biome Pool Report

Generated: 2026-06-17T10:55:51Z

Biome pool classification was data-driven from the previous Atlas Overworld dimension override plus `docs/generated/worldgen_content_audit.json`. Biome names are not treated as truth. As of 2026-06-18 this report is historical because Atlas worldgen influence is disabled and random Tectonic/Terralith generation is restored.

## Pool Summary

| Pool | Atlas region | Entries | Unique biomes | Terralith unique | Water/sea unique | Snow-allowed unique | Snow outside intended cold |
|---|---|---:|---:|---:|---:|---:|---:|
| `center` | `hearthlands` | 216 | 19 | 11 | 0 | 0 | 0 |
| `north` | `frostmarch` | 360 | 20 | 12 | 1 | 16 | 0 |
| `south` | `sunreach` | 346 | 24 | 16 | 1 | 0 | 0 |
| `east` | `verdant_coast` | 202 | 20 | 8 | 11 | 0 | 0 |
| `west` | `stoneback_highlands` | 180 | 19 | 14 | 3 | 0 | 0 |
| `north_east` | `north_east_marches` | 562 | 40 | 20 | 12 | 16 | 0 |
| `north_west` | `north_west_marches` | 540 | 39 | 26 | 4 | 16 | 0 |
| `south_east` | `south_east_wilds` | 544 | 43 | 24 | 11 | 0 | 0 |
| `south_west` | `south_west_wilds` | 526 | 43 | 30 | 4 | 0 | 0 |
| `outer` | `outer_rim` | 940 | 69 | 47 | 6 | 17 | 0 |

## Missing Biomes

Configured biome IDs missing from the audit: 0.

See `config/ascendant_atlas/reports/missing_biomes.json` for the exact list.

## Data-Driven Warning Example

`terralith:gravel_desert` is not safe to classify from its name. The audit records temperature `0.14`, climate bucket `frozen_or_snow`, terrain bucket `water_or_sea`, and flags `aquatic_features, cold, desert_features, has_spawns, ice_features, land_noise, mountain_features, snow_precipitation, tree_features`. That is why Atlas reports use biome JSON/audit data for snow and climate behavior.

## Pool JSON

The full resolved pool list with temperature, precipitation, snow allowance, terrain bucket, source jar, and flags is written to `config/ascendant_atlas/reports/biome_pools_resolved.json`.
