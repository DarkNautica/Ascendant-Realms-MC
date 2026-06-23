# Worldgen Content Audit

Generated: 2026-06-16T20:44:04.132266+00:00

This audit reads active Minecraft, mod jar, and OpenLoader data instead of classifying only by names.

## Counts

- Biomes with JSON: 802
- Structures with JSON: 645
- Structure templates indexed: 4972
- Mobs with JSON spawn evidence: 68

## Current Atlas Region Flags

- `north`: `minecraft:frozen_ocean` (water_biome_in_north)
- `south_west`: `minecraft:windswept_gravelly_hills` (cold_or_snow_biome_in_south), `minecraft:windswept_hills` (cold_or_snow_biome_in_south), `minecraft:windswept_forest` (cold_or_snow_biome_in_south), `terralith:windswept_spires` (cold_or_snow_biome_in_south), `terralith:haze_mountain` (cold_or_snow_biome_in_south), `terralith:scarlet_mountains` (cold_or_snow_biome_in_south), `minecraft:jagged_peaks` (cold_or_snow_biome_in_south), `terralith:rocky_mountains` (cold_or_snow_biome_in_south), `terralith:alpine_grove` (cold_or_snow_biome_in_south), `terralith:yosemite_lowlands` (cold_or_snow_biome_in_south), `terralith:emerald_peaks` (cold_or_snow_biome_in_south)

## North Region Snapshot

- Climate buckets: `{'frozen_or_snow': 213, 'cold': 147, 'warm': 1}`
- Terrain noise buckets: `{'inland_noise': 246, 'coast_or_lowland_noise': 114, 'sea_noise': 1}`
- Water/sea noise entry share: `0.0028`

## Dense Structure Sets To Review

- `bettermineshafts:mineshaft_acacia` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_desert` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_dripstone` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_ice` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_jungle` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_lush` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_mesa` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_mushroom` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_oak` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_overgrown` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_red_desert` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_spruce` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `bettermineshafts:mineshaft_spruce_snowy` via `bettermineshafts:mineshafts` spacing `1`, separation `0`
- `minecraft:buried_treasure` via `minecraft:buried_treasures` spacing `1`, separation `0`
- `minecraft:mineshaft` via `minecraft:mineshafts` spacing `1`, separation `0`
- `minecraft:mineshaft_mesa` via `minecraft:mineshafts` spacing `1`, separation `0`
- `minecraft:nether_fossil` via `minecraft:nether_fossils` spacing `2`, separation `1`
- `terralith:underground/frosted_dungeon` via `terralith:underground_dungeon` spacing `9`, separation `6`
- `betterdungeons:small_dungeon` via `betterdungeons:small_dungeons` spacing `10`, separation `6`
- `iceandfire:cyclops_cave` via `iceandfire:cyclops_cave` spacing `10`, separation `6`

## Data Limits

- Mobs registered only through mod code are not fully visible in JSON. This audit records biome JSON spawns and structure spawn overrides, then marks code-only behavior for in-game/runtime testing.
- Structure block profiles sample the direct start-pool templates first. Deep jigsaw children still need spot checks for major settlement packs.

Full machine-readable output: `docs/generated/worldgen_content_audit.json`
