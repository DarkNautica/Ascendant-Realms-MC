# Structure Density And Region Audit

Generated: 2026-06-18T01:57:55+00:00

This report reviews live structure-set spacing from the generated worldgen audit. It is documentation and policy only. No live structure set was rewritten by this generator.

## Summary

- Structure sets with policy rows: 330
- Entries marked dense, dangerously dense, or missing spacing data: 151
- Structure/tag rows skipped because they were not direct generated structures: 149
- Village/town overlap risks: 5
- Recommended reductions: 45
- Recommended region locks: 21
- Needs test entries: 177

## Density Policy

- `common`: appears often or has a low spacing value. Good only for tiny ambient pieces, buried/underground features, or intentional structure families.
- `uncommon`: moderate overworld landmarks.
- `rare`: major dungeons, towns, and larger ruins.
- `very_rare`: boss arenas, dragons, and large regional anchors.
- `unique`: reserved for dimension or capstone anchors.

## Dense Or Missing-Spacing Entries

| Structure | Mod | Spacing | Separation | Risk | Action |
| --- | --- | --- | --- | --- | --- |
| bettermineshafts:mineshaft_acacia | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_region_lock |
| bettermineshafts:mineshaft_desert | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_reduce |
| bettermineshafts:mineshaft_dripstone | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_reduce |
| bettermineshafts:mineshaft_ice | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_reduce |
| bettermineshafts:mineshaft_jungle | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_reduce |
| bettermineshafts:mineshaft_lush | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_reduce |
| bettermineshafts:mineshaft_mesa | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_reduce |
| bettermineshafts:mineshaft_mushroom | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_reduce |
| bettermineshafts:mineshaft_oak | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_reduce |
| bettermineshafts:mineshaft_overgrown | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_region_lock |
| bettermineshafts:mineshaft_red_desert | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_reduce |
| bettermineshafts:mineshaft_spruce | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_region_lock |
| bettermineshafts:mineshaft_spruce_snowy | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_reduce |
| minecraft:buried_treasure | Minecraft | 1 | 0 | dangerously_dense | should_reduce |
| minecraft:mineshaft | YUNG's Better Mineshafts | 1 | 0 | dangerously_dense | should_region_lock |
| minecraft:mineshaft_mesa | Minecraft | 1 | 0 | dangerously_dense | should_reduce |
| minecraft:nether_fossil | Minecraft | 2 | 1 | dangerously_dense | should_reduce |
| terralith:underground/frosted_dungeon | Terralith | 9 | 6 | dangerously_dense | should_reduce |
| betterdungeons:small_dungeon | YUNG's Better Dungeons | 10 | 6 | dangerously_dense | should_region_lock |
| iceandfire:cyclops_cave | Ice And Fire Community Edition | 10 | 6 | dangerously_dense | should_reduce |
| iceandfire:hydra_cave | Ice And Fire Community Edition | 10 | 6 | dangerously_dense | should_reduce |
| mes:ruined_pillar | moogs_structures | 10 | 7 | dangerously_dense | should_reduce |
| terralith:underground/giant_bee_hive | Terralith | 11 | 3 | dangerously_dense | should_reduce |
| terralith:underground/mining_outpost | Terralith | 11 | 3 | dangerously_dense | should_reduce |
| terralith:underground/oak_cabin | Terralith | 11 | 3 | dangerously_dense | should_reduce |
| terralith:underground/old_refinery | Terralith | 11 | 3 | dangerously_dense | should_reduce |
| terralith:underground/sunken_tower | Terralith | 11 | 3 | dangerously_dense | should_reduce |
| iceandfire:pixie_village | Ice And Fire Community Edition | 12 | 8 | dangerously_dense | should_reduce |
| mvs:medium_bamboo_cart | moogs_structures | 12 | 8 | dangerously_dense | should_reduce |
| mes:enderpin_spikes | moogs_structures | 13 | 8 | dense | should_keep |
| mvs:pile | moogs_structures | 13 | 7 | dense | should_keep |
| humancompanions:acacia_house | Human Companions | 15 | 10 | dense | should_keep |
| humancompanions:birch_house | Human Companions | 15 | 10 | dense | should_keep |
| humancompanions:dark_oak_house | Human Companions | 15 | 10 | dense | should_keep |
| humancompanions:oak_birch_house | Human Companions | 15 | 10 | dense | should_keep |
| humancompanions:oak_house | Human Companions | 15 | 10 | dense | should_keep |
| humancompanions:sandstone_house | Human Companions | 15 | 10 | dense | should_keep |
| humancompanions:spruce_house | Human Companions | 15 | 10 | dense | should_keep |
| humancompanions:terracotta_house | Human Companions | 15 | 10 | dense | should_keep |
| iceandfire:fire_dragon_roost | Ice And Fire Community Edition | 15 | 6 | dense | should_reduce |
| iceandfire:ice_dragon_roost | Ice And Fire Community Edition | 15 | 6 | dense | should_reduce |
| iceandfire:lightning_dragon_roost | Ice And Fire Community Edition | 15 | 6 | dense | should_reduce |
| mowziesmobs:wrought_chamber | Mowzie's Mobs | 15 | 5 | dense | should_keep |
| betterdungeons:small_nether_dungeon | YUNG's Better Dungeons | 16 | 10 | dense | should_keep |
| mvs:haystack | moogs_structures | 16 | 7 | dense | should_keep |
| aquamirae:outpost | Aquamirae | 18 | 10 | dense | should_keep |
| iceandfire:fire_dragon_cave | Ice And Fire Community Edition | 18 | 12 | dense | should_reduce |
| iceandfire:ice_dragon_cave | Ice And Fire Community Edition | 18 | 12 | dense | should_reduce |
| iceandfire:lightning_dragon_cave | Ice And Fire Community Edition | 18 | 12 | dense | should_reduce |
| mvs:acacia_tree | moogs_structures | 18 | 13 | dense | should_keep |
| mvs:bench | moogs_structures | 18 | 14 | dense | should_keep |
| mvs:birch_tree | moogs_structures | 18 | 13 | dense | should_keep |
| mvs:cherry_tree | moogs_structures | 18 | 13 | dense | should_keep |
| mvs:dark_oak_tree | moogs_structures | 18 | 13 | dense | should_keep |
| mvs:jungle_palm_tree | moogs_structures | 18 | 13 | dense | should_keep |
| mvs:jungle_tree | moogs_structures | 18 | 13 | dense | should_keep |
| mvs:oak_tree | moogs_structures | 18 | 13 | dense | should_keep |
| mvs:spruce_tree | moogs_structures | 18 | 13 | dense | should_keep |
| mvs:stone_rock | moogs_structures | 18 | 13 | dense | should_keep |
| terralith:rubble_desert | Terralith | 18 | 12 | dense | should_keep |
| terralith:rubble_forest | Terralith | 18 | 12 | dense | should_keep |
| terralith:rubble_jungle | Terralith | 18 | 12 | dense | should_keep |
| terralith:rubble_mesa | Terralith | 18 | 12 | dense | should_keep |
| terralith:rubble_mountain | Terralith | 18 | 12 | dense | should_keep |
| terralith:rubble_taiga | Terralith | 18 | 12 | dense | should_keep |
| mvs:horse_campsite | moogs_structures | 19 | 17 | dense | should_keep |
| supplementaries:way_sign | Supplementaries | 19 | 10 | dense | should_keep |
| aquamirae:surface/arch | Aquamirae | 20 | 8 | dense | should_keep |
| aquamirae:surface/spiral | Aquamirae | 20 | 8 | dense | should_keep |
| iceandfire:siren_island | Ice And Fire Community Edition | 20 | 14 | dense | should_reduce |
| minecraft:end_city | supplementaries-1.20-3.1.43-forge | 20 | 11 | dense | should_keep |
| minecraft:ocean_ruin_cold | Minecraft | 20 | 8 | dense | should_keep |
| minecraft:ocean_ruin_warm | Minecraft | 20 | 8 | dense | should_keep |
| idas:abandoned_vineyard | Integrated Dungeons and Structures | 21 | 12 | dense | should_region_lock |
| idas:abandonedhouse | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:apothecary_abode | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:bearclaw_inn | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:beekeepers_house | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:botanist | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:brickhouse | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:castle | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:desert_ruins | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:dig_site/dig_site | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:dig_site/dig_site_desert | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:enchantingtower | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:farmhouse | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:fishermans_lodge | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:haunted_manor | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:hermits_hollow | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:hunters_cabin | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:mason_house | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:redhorn_guild | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:ruined_church | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:ruined_fort | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:ruined_well | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:the_log | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:treetop_tavern | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:tudor_pub | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:wacky_wares | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:winter_wagon | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:witches_treestump | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| idas:wizard_tower | Integrated Dungeons and Structures | 21 | 12 | dense | needs_test |
| mvs:small_tower_well | moogs_structures | 23 | 15 | dense | should_keep |
| structory:swamp_ruin | Structory | 23 | 10 | dense | needs_test |
| minecraft:ancient_city | supplementaries-1.20-3.1.43-forge | 24 | 8 | dense | should_keep |
| minecraft:shipwreck | Minecraft | 24 | 4 | dense | should_keep |
| minecraft:shipwreck_beached | Minecraft | 24 | 4 | dense | should_keep |
| mvs:acacia_well | moogs_structures | 24 | 18 | dense | should_keep |
| mvs:birch_well | moogs_structures | 24 | 18 | dense | should_keep |
| mvs:dark_oak_well | moogs_structures | 24 | 18 | dense | should_keep |
| mvs:desert_well | moogs_structures | 24 | 18 | dense | should_keep |
| mvs:jungle_well | moogs_structures | 24 | 18 | dense | should_keep |
| mvs:oak_well | moogs_structures | 24 | 18 | dense | should_keep |
| mvs:rocky_well | moogs_structures | 24 | 18 | dense | should_keep |
| mvs:small_acacia_lantern | moogs_structures | 24 | 12 | dense | should_keep |
| mvs:small_bamboo_lantern | moogs_structures | 24 | 12 | dense | should_keep |
| mvs:small_birch_lantern | moogs_structures | 24 | 12 | dense | should_keep |
| mvs:small_campfire_lantern | moogs_structures | 24 | 12 | dense | should_keep |
| mvs:small_cherry_lantern | moogs_structures | 24 | 12 | dense | should_keep |
| mvs:small_copper_well | moogs_structures | 24 | 18 | dense | should_keep |
| mvs:small_dark_oak_lantern | moogs_structures | 24 | 12 | dense | should_keep |
| mvs:small_jungle_lantern | moogs_structures | 24 | 12 | dense | should_keep |
| mvs:small_mangrove_lantern | moogs_structures | 24 | 12 | dense | should_keep |
| mvs:small_oak_lantern | moogs_structures | 24 | 12 | dense | should_keep |
| mvs:small_spruce_lantern | moogs_structures | 24 | 12 | dense | should_keep |
| mvs:small_well | moogs_structures | 24 | 18 | dense | should_keep |
| mvs:snowy_well | moogs_structures | 24 | 18 | dense | should_keep |
| mvs:spruce_well | moogs_structures | 24 | 18 | dense | should_keep |
| mvs:well | moogs_structures | 24 | 18 | dense | should_keep |
| villagesandpillages:village_witch | Villages & Pillages | 24 | 16 | dense | should_keep |
| ascendant_atlas:crownlands_waymark | active-instance-openloader:ascendant_realms_atlas | None | None | missing_spacing_data | should_keep_debug_only |
| ascendant_atlas:frostmarch_waymark | active-instance-openloader:ascendant_realms_atlas | None | None | missing_spacing_data | should_keep_debug_only |
| ascendant_atlas:stoneback_waystation | active-instance-openloader:ascendant_realms_atlas | None | None | missing_spacing_data | should_keep_debug_only |
| ascendant_atlas:sunreach_waymark | active-instance-openloader:ascendant_realms_atlas | None | None | missing_spacing_data | should_keep_debug_only |
| ascendant_atlas:verdant_crossing | active-instance-openloader:ascendant_realms_atlas | None | None | missing_spacing_data | should_keep_debug_only |
| irons_spellbooks:ancient_battleground | Iron's Spells 'n Spellbooks | None | None | missing_spacing_data | needs_test |
| irons_spellbooks:catacombs | Iron's Spells 'n Spellbooks | None | None | missing_spacing_data | needs_test |
| irons_spellbooks:citadel | Iron's Spells 'n Spellbooks | None | None | missing_spacing_data | needs_test |
| irons_spellbooks:evoker_fort | Iron's Spells 'n Spellbooks | None | None | missing_spacing_data | needs_test |
| irons_spellbooks:mangrove_hut | Iron's Spells 'n Spellbooks | None | None | missing_spacing_data | needs_test |
| ... | 11 more rows in JSON |  |  |  |

## Source Family Notes

- Moog structures are high-volume. Keep the best ambient finds, but test clutter before raising global density.
- YUNG mineshafts use very low structure-set spacing by design. Treat underground density separately from visible surface clutter.
- IDAS common structures are varied but numerous; region locks and loot tiering matter more than adding more packs.
- Integrated Villages and Towns and Towers should be tested for village/town overlap before any settlement work.
- Aquamirae surface structures are already widened through the world-integration datapack and should remain frozen-ocean themed.
