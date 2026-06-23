# Ascendant Realms World Integration

OpenLoader loads this datapack globally from `config/openloader/data/` for local client and dedicated server testing.

Current active overrides:

- Bypasses Integrated Villages' `integrated_api:workstation_processor` through static `minecraft:rule` replacements for workstation placeholder blocks.
- Restores `integrated_villages:airship_village`, `integrated_villages:mossy_mounds`, and `integrated_villages:marketstead_village` for retest instead of keeping them disabled.
- Repairs Integrated Villages' broken `minecraft:village` structure tag by removing only the nonexistent `integrated_villages:swamp_village` entry.
- Extends Mowzie's Mobs biome tags conservatively so its structures and magical forest mobs can appear in compatible modded overworld biomes.
- Repairs Human Companions' `windswept_gravelley_hills` biome typo to `windswept_gravelly_hills` so oak/spruce companion houses keep their intended mountain-biome coverage.
- Adds a `c:bosses` entity tag bridge for IceAndFire CE so its gorgon-immunity tag can reference common boss entities cleanly.
- Neutralizes IDAS optional Biomes O' Plenty / BYG biome hooks because those biome mods are not installed in this Forge 1.20.1 proof target.
- Replaces IDAS optional Ars Nouveau archmage/enchanting loot and spawner hooks with pack-native Iron's Spells / vanilla equivalents.
- Overrides broken optional Every Compat, Alex's Delight, and Spartan Shields compat recipes/advancements with valid disabled placeholders when their target optional mods/items are absent.

The crash path is a shared workstation/POI processor path, not a reason to remove each village one by one. If placement crashes return, inspect the failing processor/template path first and only disable an exact structure as a temporary emergency fallback.
