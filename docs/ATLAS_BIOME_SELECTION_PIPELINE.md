# Atlas Biome Selection Pipeline

Last updated: 2026-06-17.

## Active Pipeline

Ascendant Atlas still uses:

- `minecraft:noise` generator
- `settings: minecraft:overworld`
- `ascendant_atlas_regions:regional_multi_noise` biome source
- Terralith biome parameter tables
- Tectonic-style terrain shape underneath the Overworld settings path

The helper no longer asks one hard coordinate sector to pick a biome blindly.

## Selection Flow

1. Minecraft calls the Atlas biome source with quart coordinates.
2. The helper converts quart coordinates to block coordinates with `quart << 2`.
3. The helper samples the real Minecraft climate target.
4. The helper applies long Atlas climate biasing.
5. The helper classifies hydrology.
6. The helper calculates continuous region weights with deterministic domain warp.
7. Candidate biome entries are gathered from the primary region plus secondary weighted regions.
8. Hydrology-incompatible biome entries are rejected.
9. The closest compatible Terralith parameter point wins.

## Why This Matters

The previous selector still behaved like softened slices. It could make east/southeast terrain choose an ocean biome over high land, which broke both map labels and structure context. The new path separates "what the terrain physically is" from "what regional flavor should color it."

## New Commands

- `/ascatlas hydrology_here`
- `/ascatlas biome_decision_here`
- `/ascatlas region_weights_here`
- `/ascatlas sample_transect <x1> <z1> <x2> <z2> <step>`
- `/ascatlas dump_gradient_policy`
- `/ascatlas dump_hydrology_registry`

Required regression point:

- `/tp @s 2375 170 1895`
- `/ascatlas hydrology_here`
- `/ascatlas biome_decision_here`
- `/ascatlas region_weights_here`
- `/ascstructure here`

Expected result: high inland jungle/badlands terrain must not be labelled `minecraft:ocean`.
