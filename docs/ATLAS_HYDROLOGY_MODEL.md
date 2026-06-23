# Atlas Hydrology Model

Last updated: 2026-06-17.

2026-06-18 status: historical/superseded. Jayden chose to disable Atlas coordinate-directed worldgen and return to random Tectonic/Terralith generation. This hydrology model records the rejected Atlas helper path and should not be treated as active terrain steering while `config/ascendant_atlas/worldgen_override_policy.json` has `worldgen_override_enabled=false`.

## Purpose

Atlas biome selection now treats hydrology as a first-class terrain context, not a side effect of region names.

The failure that forced this pass was `minecraft:ocean` being selected over high dry jungle/badlands terrain near `/tp @s 2375 170 1895`, which then made ocean/boat structure context look valid where the land clearly was not ocean.

## Current Model

The helper samples Minecraft's active climate target at the queried block position, then derives a hydrology class from:

- continentalness
- erosion
- weirdness
- biome query Y
- exact known water/coast biome IDs
- Terralith parameter entries in the generated hydrology registry

Hydrology classes:

- `deep_ocean`
- `ocean`
- `coast`
- `river`
- `inland_water`
- `inland_lowland`
- `inland_highland`
- `mountain`

## Rule

Biome selection now runs in this order:

1. Sample the active Minecraft climate target.
2. Classify hydrology/terrain context.
3. Compute continuous Atlas region weights.
4. Filter biome candidates by hydrology compatibility.
5. Select the nearest compatible Terralith parameter point.

Ocean biome IDs are allowed only in real ocean/coast hydrology contexts. High inland or mountain terrain should not resolve to `minecraft:ocean`, even if a wet/east region has ocean biomes in its broader table.

## Boundaries

This is not terrain signoff. Jayden still needs a fresh-world visual pass.

This is not a global water removal. Rivers, oases, mountain lakes, coastlines, Verdant Coast water identity, and Frostmarch frozen-ocean identity must remain.

This is not a structure rewrite. Structure Director diagnostics now read Atlas hydrology, but true pre-generation structure veto still requires a deeper generator/mixin hook.
