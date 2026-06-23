# Structure Density Implementation Report

Generated: 2026-06-18T01:57:55+00:00

This report converts the density audit into review-only implementation candidates. No candidate is live. No OpenLoader structure-set override was written by this generator.

## Summary

- Structure sets with density policy: 330.
- Dense/dangerously dense structure entries: 130.
- Village/town overlap-risk structure sets: 5.
- Disabled candidate override rows: 70.

## Candidate Overrides

| Structure Set | Current Spacing | Current Separation | Candidate Spacing | Candidate Separation | Fix Type |
| --- | --- | --- | --- | --- | --- |
| block_factorys_bosses:sandworm_nest | 45 | 30 | 96 | 48 | boss_or_dragon_should_be_rare |
| block_factorys_bosses:yeti_hideout | 30 | 25 | 96 | 48 | boss_or_dragon_should_be_rare |
| cataclysm:abandoned_structures | 30 | 20 | 96 | 48 | boss_or_dragon_should_be_rare |
| cataclysm:amethyst_nest | 32 | 8 | 96 | 48 | boss_or_dragon_should_be_rare |
| cataclysm:desert_structures | 30 | 20 | 96 | 48 | boss_or_dragon_should_be_rare |
| iceandfire:cyclops_cave | 10 | 6 | 96 | 48 | boss_or_dragon_should_be_rare |
| iceandfire:dragon_cave | 18 | 12 | 96 | 48 | boss_or_dragon_should_be_rare |
| iceandfire:dragon_roost | 15 | 6 | 96 | 48 | boss_or_dragon_should_be_rare |
| iceandfire:gorgon_temple | 32 | 12 | 96 | 48 | boss_or_dragon_should_be_rare |
| iceandfire:graveyard | 28 | 14 | 96 | 48 | boss_or_dragon_should_be_rare |
| iceandfire:hydra_cave | 10 | 6 | 96 | 48 | boss_or_dragon_should_be_rare |
| iceandfire:mausoleum | 32 | 12 | 96 | 48 | boss_or_dragon_should_be_rare |
| iceandfire:pixie_village | 12 | 8 | 96 | 48 | boss_or_dragon_should_be_rare |
| iceandfire:siren_island | 20 | 14 | 96 | 48 | boss_or_dragon_should_be_rare |
| idas:idas_ocean | 35 | 29 | 96 | 48 | boss_or_dragon_should_be_rare |
| idas:idas_rare | 45 | 20 | 96 | 48 | boss_or_dragon_should_be_rare |
| betterdungeons:small_dungeons | 10 | 6 | 32 | 12 | dungeon_density_review |
| bettermineshafts:mineshafts | 1 | 0 | 32 | 12 | dungeon_density_review |
| idas:idas_common | 21 | 12 | 32 | 12 | dungeon_density_review |
| minecraft:mineshafts | 1 | 0 | 32 | 12 | dungeon_density_review |
| mvs:small_tower_well | 23 | 15 | 32 | 15 | dungeon_density_review |
| terralith:underground | 11 | 3 | 32 | 12 | dungeon_density_review |
| terralith:underground_dungeon | 9 | 6 | 32 | 12 | dungeon_density_review |
| aquamirae:outpost | 18 | 10 | 28 | 10 | general_visible_density_review |
| aquamirae:surface | 20 | 8 | 28 | 10 | general_visible_density_review |
| betterdungeons:small_nether_dungeons | 16 | 10 | 28 | 10 | general_visible_density_review |
| humancompanions:companion_house | 15 | 10 | 28 | 10 | general_visible_density_review |
| mes:enderpin_spikes | 13 | 8 | 28 | 10 | general_visible_density_review |
| mes:ruined_pillar | 10 | 7 | 28 | 10 | general_visible_density_review |
| minecraft:ancient_cities | 24 | 8 | 28 | 10 | general_visible_density_review |
| minecraft:buried_treasures | 1 | 0 | 28 | 10 | general_visible_density_review |
| minecraft:end_cities | 20 | 11 | 28 | 11 | general_visible_density_review |
| minecraft:nether_fossils | 2 | 1 | 28 | 10 | general_visible_density_review |
| minecraft:ocean_ruins | 20 | 8 | 28 | 10 | general_visible_density_review |
| minecraft:pillager_outposts | 32 | 8 | 32 | 10 | general_visible_density_review |
| mowziesmobs:wrought_chambers | 15 | 5 | 28 | 10 | general_visible_density_review |
| mvs:acacia_tree | 18 | 13 | 28 | 13 | general_visible_density_review |
| mvs:bench | 18 | 14 | 28 | 14 | general_visible_density_review |
| mvs:birch_tree | 18 | 13 | 28 | 13 | general_visible_density_review |
| mvs:cherry_tree | 18 | 13 | 28 | 13 | general_visible_density_review |
| mvs:dark_oak_tree | 18 | 13 | 28 | 13 | general_visible_density_review |
| mvs:haystack | 16 | 7 | 28 | 10 | general_visible_density_review |
| mvs:horse_campsite | 19 | 17 | 28 | 17 | general_visible_density_review |
| mvs:jungle_palm_tree | 18 | 13 | 28 | 13 | general_visible_density_review |
| mvs:jungle_tree | 18 | 13 | 28 | 13 | general_visible_density_review |
| mvs:medium_bamboo_cart | 12 | 8 | 28 | 10 | general_visible_density_review |
| mvs:oak_tree | 18 | 13 | 28 | 13 | general_visible_density_review |
| mvs:pile | 13 | 7 | 28 | 10 | general_visible_density_review |
| mvs:small_acacia_lantern | 24 | 12 | 28 | 12 | general_visible_density_review |
| mvs:small_bamboo_lantern | 24 | 12 | 28 | 12 | general_visible_density_review |
| mvs:small_birch_lantern | 24 | 12 | 28 | 12 | general_visible_density_review |
| mvs:small_campfire_lantern | 24 | 12 | 28 | 12 | general_visible_density_review |
| mvs:small_cherry_lantern | 24 | 12 | 28 | 12 | general_visible_density_review |
| mvs:small_dark_oak_lantern | 24 | 12 | 28 | 12 | general_visible_density_review |
| mvs:small_jungle_lantern | 24 | 12 | 28 | 12 | general_visible_density_review |
| mvs:small_mangrove_lantern | 24 | 12 | 28 | 12 | general_visible_density_review |
| mvs:small_oak_lantern | 24 | 12 | 28 | 12 | general_visible_density_review |
| mvs:small_spruce_lantern | 24 | 12 | 28 | 12 | general_visible_density_review |
| mvs:spruce_tree | 18 | 13 | 28 | 13 | general_visible_density_review |
| mvs:stone_rock | 18 | 13 | 28 | 13 | general_visible_density_review |
| structory:ruin_quiet | 23 | 10 | 28 | 10 | general_visible_density_review |
| supplementaries:way_signs | 19 | 10 | 28 | 10 | general_visible_density_review |
| terralith:rubble | 18 | 12 | 28 | 12 | general_visible_density_review |
| towns_and_towers:other | 32 | 16 | 32 | 16 | general_visible_density_review |
| towns_and_towers:towns | 48 | 24 | 48 | 24 | general_visible_density_review |
| villagesandpillages:village_witch | 24 | 16 | 28 | 16 | general_visible_density_review |
| integrated_villages:regular_villages | 64 | 32 | 64 | 32 | water_structure_density_review |
| minecraft:shipwrecks | 24 | 4 | 36 | 12 | water_structure_density_review |
| mvs:other_wells | 24 | 18 | 36 | 18 | water_structure_density_review |
| towns_and_towers:towers | 48 | 24 | 48 | 24 | water_structure_density_review |

## Implementation Boundary

- Candidate files live under `config/ascendant_structures/candidates/` and are not loaded by Minecraft.
- A future live override must be copied into `config/openloader/data/ascendant_structure_overrides/` only after manual review.
- First approved changes should be small spacing/separation adjustments for obvious spam families, not broad disables.
