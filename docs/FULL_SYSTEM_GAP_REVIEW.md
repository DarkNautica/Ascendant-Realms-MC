# Full System Gap Review

Status: root-cause compatibility pass started.

This review tracks gaps found while keeping the full Ascendant Realms mod stack intact. The goal is to repair integration seams instead of stripping out content.

## Fixed In This Pass

- Player identity fallback: changed the scoreboard display slot from `below_name` to `belowName`, which is the form accepted by the current Minecraft command parser. This should let the level/name fallback function load instead of failing at startup.
- Integrated Villages: kept `airship_village`, `mossy_mounds`, and `marketstead_village` active while replacing the shared `integrated_api:workstation_processor` crash path with static workstation placeholder rules.
- Human Companions: replaced the misspelled `minecraft:windswept_gravelley_hills` biome tag value with `minecraft:windswept_gravelly_hills`.
- IceAndFire CE: added a `c:bosses` bridge tag so its `immune_to_gorgon_stone` tag no longer points at a missing shared boss tag.
- IDAS optional biome hooks: disabled only the absent Biomes O' Plenty / BYG biome tags. This does not remove active Ascendant Realms biomes because those biome mods are not installed.
- IDAS Ars Nouveau hooks: replaced optional Ars Nouveau archmage/enchanting-tower spawner and loot references with Iron's Spells / vanilla equivalents.
- Iron's Spells loot tables: overrode the two loot tables that used loader-incompatible or malformed functions with valid pack-native loot tables.
- Every Compat / Alex's Delight / Spartan Shields optional compat noise: added valid disabled overrides for recipes/advancements that reference absent optional mods or items.
- Missing local textures: staged fallback assets for generated KubeJS Guild currency items and a transparent compatibility texture for the missing `minecraft:textures/models/armor/wizard_layer_1` armor paths.

## Needs Fresh Client/Server Retest

- Confirm no KubeJS startup warning remains from the Runic Grimoire JEI alias. The duplicate subtype registration was removed; if JEI still reports an empty ingredient, disable only the JEI add-item alias and keep the Patchouli/tooltip identity.
- Confirm the generated rarity tooltip line appears directly below native damage/speed/stat lines and before green combat behavior lines.
- Confirm the identity fallback displays player level below names and does not error during datapack load.
- Confirm Integrated Villages can generate repaired village variants without the POI class-cast crash.
- Confirm IDAS Archmage/Enchanting Tower structures still spawn and contain Iron's Spells themed loot instead of broken Ars Nouveau references.
- Confirm Human Companions oak/spruce houses still generate in intended compatible biomes.

## Known Non-Blocking Log Noise To Watch

- EMF may ignore repeatedly recreated Cataclysm/BossesRise head/gauntlet models. That is a visual/performance warning from model allocation behavior, not a reason to remove Cataclysm. If it becomes severe, test an EMF exclusion/config path.
- Oculus, Sodium Dynamic Lights, Supplementaries, and Entity Texture Features patch Embeddium classes. This is expected for shader/dynamic-light/entity-visual stacks; treat as a risk to monitor, not a current failure.
- MCA Reborn still needs deeper clothing/resource validation if logs continue saying clothing or hair entries do not exist.
- Weather2 and structure density tuning remain performance-sensitive and need long-distance exploration testing.

## Recommended Next Fix Layer

1. Run a fresh client boot after importing the updated pack.
2. Compare the new `latest.log` against this review and remove items that are confirmed fixed.
3. If nameplates, skill HUD, or enemy levels still cannot be made clean through existing mods, start the first custom Ascendant helper mod focused only on UI overlays and readable identity.
4. Continue settlement/NPC work through standalone Hunter Board/Guild Outpost structures before injecting into third-party village pools.
