# Ascendant Structure Tiering

Generated: 2026-06-18T01:57:55+00:00

This is a control scaffold for structure authorship. It does not add structure mods, does not inject village pools, and does not rewrite live structure sets. Classifications use `docs/generated/worldgen_content_audit.json` first, including biome tags, structure sets, sampled block palettes, start pools, and generation steps, with `config/ascendant_index/structure_registry.json` as the fallback index.

## Summary

- Structures classified: 579
- Structure sets with density policy: 330
- Worldgen audit structures: 645
- Structure templates indexed by audit: 4972
- Structure/tag rows skipped because they were not direct generated structures: 149
- High-priority manual review entries: 173
- Dense or dangerously dense entries: 130
- Boss/dungeon entries allowed in beginner regions: 21
- Untiered loot review entries: 198

## Counts

- Structure classes: `{'boss_arena': 22, 'dangerous_dungeon': 111, 'dragon_tier_zone': 16, 'end_landmark': 30, 'landmark_or_ruin': 121, 'nether_landmark': 16, 'settlement': 109, 'uncategorized_structure': 154}`
- Recommended actions: `{'defer_until_guild_phase': 3, 'needs_test': 177, 'should_keep': 328, 'should_keep_debug_only': 5, 'should_reduce': 45, 'should_region_lock': 21}`
- Manual review priorities: `{'high': 173, 'low': 258, 'medium': 148}`
- Density classes: `{'common': 130, 'rare': 156, 'uncommon': 163, 'unique': 19, 'unknown': 21, 'very_rare': 90}`

## Policy Rules

- Hearthlands and Crownlands are beginner-friendly. Boss arenas, dragon zones, and high-tier dungeons should be middle, outer, edge, dimension-locked, or tightly region-themed.
- Aquamirae content stays ocean, cold ocean, frozen ocean, and Frostmarch themed. Its surface set is already widened and should not be treated as inland clutter.
- Towns and Towers, Integrated Villages, IDAS, Structory, and Moog structures are kept for authored variety, but their density and overlap risks need review before more structure volume is added.
- Region locking is preferred over blanket disabling. Density reduction is preferred when a good structure is simply too frequent.
- Village injection remains untouched in this pass.

## High Priority Review

| Structure | Mod | Class | Regions | Spacing | Loot | Action |
| --- | --- | --- | --- | --- | --- | --- |
| idas:abandonedhouse | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:apothecary_abode | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,south_west_wilds,sunreach,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:bearclaw_inn | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:beekeepers_house | Integrated Dungeons and Structures | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands | 21 | dangerous_dungeon | needs_test |
| idas:botanist | Integrated Dungeons and Structures | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands | 21 | dangerous_dungeon | needs_test |
| idas:brickhouse | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:castle | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:desert_ruins | Integrated Dungeons and Structures | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | 21 | dangerous_dungeon | needs_test |
| idas:dig_site/dig_site | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:dig_site/dig_site_desert | Integrated Dungeons and Structures | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | 21 | dangerous_dungeon | needs_test |
| idas:enchantingtower | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,south_west_wilds,sunreach,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:farmhouse | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:fishermans_lodge | Integrated Dungeons and Structures | dangerous_dungeon | coastal_only,frostmarch_if_frozen,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:haunted_manor | Integrated Dungeons and Structures | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | 21 | dangerous_dungeon | needs_test |
| idas:hermits_hollow | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:hunters_cabin | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:mason_house | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:redhorn_guild | Integrated Dungeons and Structures | settlement | crownlands,hearthlands,region_compatible_settlement,south_east_wilds | 21 | settlement_basic | needs_test |
| idas:ruined_church | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:ruined_fort | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:ruined_well | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:the_log | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:treetop_tavern | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:tudor_pub | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:wacky_wares | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:winter_wagon | Integrated Dungeons and Structures | dangerous_dungeon | frostmarch,north_east_marches,north_west_marches,south_west_wilds | 21 | dangerous_dungeon | needs_test |
| idas:witches_treestump | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,south_west_wilds,sunreach,verdant_coast | 21 | dangerous_dungeon | needs_test |
| idas:wizard_tower | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,south_west_wilds,sunreach,verdant_coast | 21 | dangerous_dungeon | needs_test |
| structory:swamp_ruin | Structory | landmark_or_ruin | atlas_region_matching_biome_tag | 23 | minor_ruin | needs_test |
| aquamirae:outpost | Aquamirae | settlement | coastal_only,crownlands,frostmarch,frostmarch_if_frozen | 18 | settlement_basic | should_keep |
| aquamirae:surface/arch | Aquamirae | uncategorized_structure | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | 20 | review | should_keep |
| aquamirae:surface/spiral | Aquamirae | uncategorized_structure | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | 20 | review | should_keep |
| betterdungeons:small_nether_dungeon | YUNG's Better Dungeons | nether_landmark | nether_only | 16 | dangerous_dungeon | should_keep |
| block_factorys_bosses:dragon_tower | Bosses'Rise | dragon_tier_zone | boss_theme_region,outer,south_east_wilds,south_west_wilds | 96 | dragon_tier_zone | should_keep |
| block_factorys_bosses:kraken_ship | Bosses'Rise | boss_arena | boss_theme_region,coastal_only,frostmarch_if_frozen,outer | 52 | boss_arena | should_keep |
| block_factorys_bosses:underworld_arena | Bosses'Rise | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | 48 | boss_arena | should_keep |
| cataclysm:acropolis | cataclysm | boss_arena | boss_theme_region,coastal_only,frostmarch_if_frozen,outer | 80 | boss_arena | should_keep |
| cataclysm:ancient_factory | cataclysm | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | 112 | boss_arena | should_keep |
| cataclysm:burning_arena | cataclysm | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | 80 | boss_arena | should_keep |
| cataclysm:cursed_pyramid | cataclysm | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | 80 | boss_arena | should_keep |
| cataclysm:frosted_prison | cataclysm | boss_arena | boss_theme_region,frostmarch,north_east_marches,north_west_marches | 80 | boss_arena | should_keep |
| cataclysm:ruined_citadel | cataclysm | boss_arena | boss_theme_region,outer | 50 | boss_arena | should_keep |
| cataclysm:soul_black_smith | cataclysm | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | 60 | boss_arena | should_keep |
| cataclysm:sunken_city | cataclysm | boss_arena | boss_theme_region,coastal_only,frostmarch,frostmarch_if_frozen | 100 | boss_arena | should_keep |
| humancompanions:acacia_house | Human Companions | landmark_or_ruin | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | 15 | minor_ruin | should_keep |
| humancompanions:birch_house | Human Companions | landmark_or_ruin | south_east_wilds,verdant_coast | 15 | minor_ruin | should_keep |
| humancompanions:dark_oak_house | Human Companions | landmark_or_ruin | south_east_wilds,verdant_coast | 15 | minor_ruin | should_keep |
| humancompanions:oak_birch_house | Human Companions | landmark_or_ruin | south_east_wilds,verdant_coast | 15 | minor_ruin | should_keep |
| humancompanions:oak_house | Human Companions | landmark_or_ruin | south_east_wilds,verdant_coast | 15 | minor_ruin | should_keep |
| humancompanions:sandstone_house | Human Companions | landmark_or_ruin | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | 15 | minor_ruin | should_keep |
| humancompanions:spruce_house | Human Companions | landmark_or_ruin | frostmarch,north_east_marches,south_east_wilds,verdant_coast | 15 | minor_ruin | should_keep |
| humancompanions:terracotta_house | Human Companions | landmark_or_ruin | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | 15 | minor_ruin | should_keep |
| mes:enderpin_spikes | moogs_structures | end_landmark | end_only | 13 | end_landmark | should_keep |
| minecraft:ancient_city | supplementaries-1.20-3.1.43-forge | landmark_or_ruin | atlas_region_matching_biome_tag | 24 | review | should_keep |
| minecraft:end_city | supplementaries-1.20-3.1.43-forge | landmark_or_ruin | atlas_region_matching_biome_tag | 20 | review | should_keep |
| minecraft:ocean_ruin_cold | Minecraft | landmark_or_ruin | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | 20 | review | should_keep |
| minecraft:ocean_ruin_warm | Minecraft | landmark_or_ruin | coastal_only,frostmarch_if_frozen,verdant_coast | 20 | review | should_keep |
| minecraft:shipwreck | Minecraft | landmark_or_ruin | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | 24 | review | should_keep |
| minecraft:shipwreck_beached | Minecraft | landmark_or_ruin | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | 24 | review | should_keep |
| mowziesmobs:wrought_chamber | Mowzie's Mobs | uncategorized_structure | coastal_only,crownlands,frostmarch,frostmarch_if_frozen | 15 | review | should_keep |
| mss:arena | moogs_structures | boss_arena | boss_theme_region,frostmarch,north_east_marches,north_west_marches | 158 | boss_arena | should_keep |
| mvs:acacia_tree | moogs_structures | uncategorized_structure | crownlands,hearthlands,north_west_marches,south_west_wilds | 18 | review | should_keep |
| mvs:acacia_well | moogs_structures | landmark_or_ruin | crownlands,hearthlands,north_west_marches,south_west_wilds | 24 | minor_ruin | should_keep |
| mvs:bench | moogs_structures | uncategorized_structure | frostmarch,north_east_marches,north_west_marches,south_west_wilds | 18 | review | should_keep |
| mvs:birch_tree | moogs_structures | uncategorized_structure | south_east_wilds,verdant_coast | 18 | review | should_keep |
| mvs:birch_well | moogs_structures | landmark_or_ruin | south_east_wilds,verdant_coast | 24 | minor_ruin | should_keep |
| mvs:cherry_tree | moogs_structures | uncategorized_structure | south_east_wilds,verdant_coast | 18 | review | should_keep |
| mvs:dark_oak_tree | moogs_structures | uncategorized_structure | south_east_wilds,verdant_coast | 18 | review | should_keep |
| mvs:dark_oak_well | moogs_structures | landmark_or_ruin | south_east_wilds,verdant_coast | 24 | minor_ruin | should_keep |
| mvs:desert_well | moogs_structures | landmark_or_ruin | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | 24 | minor_ruin | should_keep |
| mvs:haystack | moogs_structures | uncategorized_structure | frostmarch,north_east_marches,north_west_marches,south_west_wilds | 16 | review | should_keep |
| mvs:horse_campsite | moogs_structures | settlement | crownlands,frostmarch,hearthlands,north_east_marches | 19 | settlement_basic | should_keep |
| mvs:jungle_palm_tree | moogs_structures | uncategorized_structure | south_east_wilds,verdant_coast | 18 | review | should_keep |
| mvs:jungle_tree | moogs_structures | uncategorized_structure | south_east_wilds,verdant_coast | 18 | review | should_keep |
| mvs:jungle_well | moogs_structures | landmark_or_ruin | south_east_wilds,verdant_coast | 24 | minor_ruin | should_keep |
| mvs:oak_tree | moogs_structures | uncategorized_structure | frostmarch,north_east_marches,north_west_marches,south_west_wilds | 18 | review | should_keep |
| mvs:oak_well | moogs_structures | landmark_or_ruin | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | 24 | minor_ruin | should_keep |
| mvs:pile | moogs_structures | uncategorized_structure | frostmarch,north_east_marches,north_west_marches,south_west_wilds | 13 | review | should_keep |
| mvs:rocky_well | moogs_structures | landmark_or_ruin | frostmarch,north_east_marches,north_west_marches,south_east_wilds | 24 | minor_ruin | should_keep |
| mvs:small_acacia_lantern | moogs_structures | uncategorized_structure | crownlands,hearthlands,north_west_marches,south_west_wilds | 24 | review | should_keep |
| ... | 93 more rows in JSON |  |  |  |

## Full Tier Preview

| Structure | Mod | Class | Regions | Rings | Danger | Loot | Density | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| aquamirae:outpost | Aquamirae | settlement | coastal_only,crownlands,frostmarch,frostmarch_if_frozen | center/inner | 0 | settlement_basic | common | should_keep |
| aquamirae:shelter | Aquamirae | uncategorized_structure | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | inner/middle/outer | 2 | review | uncommon | should_keep |
| aquamirae:ship | Aquamirae | landmark_or_ruin | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | inner/middle | 1 | minor_ruin | uncommon | should_keep |
| aquamirae:surface/arch | Aquamirae | uncategorized_structure | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | inner/middle/outer | 2 | review | common | should_keep |
| aquamirae:surface/spiral | Aquamirae | uncategorized_structure | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | inner/middle/outer | 2 | review | common | should_keep |
| ascendant_atlas:crownlands_waymark | active-instance-openloader:ascendant_realms_atlas | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 2 | review | unknown | should_keep_debug_only |
| ascendant_atlas:frostmarch_waymark | active-instance-openloader:ascendant_realms_atlas | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 2 | review | unknown | should_keep_debug_only |
| ascendant_atlas:stoneback_waystation | active-instance-openloader:ascendant_realms_atlas | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 2 | review | unknown | should_keep_debug_only |
| ascendant_atlas:sunreach_waymark | active-instance-openloader:ascendant_realms_atlas | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 2 | review | unknown | should_keep_debug_only |
| ascendant_atlas:verdant_crossing | active-instance-openloader:ascendant_realms_atlas | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 2 | review | unknown | should_keep_debug_only |
| ascendant_guild:frontier_guild_outpost | active-instance-openloader:ascendant_realms_guild | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 2 | review | unique | defer_until_guild_phase |
| ascendant_guild:hunter_board_village_standard | active-instance-openloader:ascendant_realms_guild | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 2 | review | unique | defer_until_guild_phase |
| ascendant_guild:roadside_hunter_camp | active-instance-openloader:ascendant_realms_guild | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 2 | review | unique | defer_until_guild_phase |
| betterdungeons:skeleton_dungeon | YUNG's Better Dungeons | dangerous_dungeon | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | middle/outer | 3 | dangerous_dungeon | rare | should_region_lock |
| betterdungeons:small_dungeon | YUNG's Better Dungeons | dangerous_dungeon | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | middle/outer | 3 | dangerous_dungeon | common | should_region_lock |
| betterdungeons:small_nether_dungeon | YUNG's Better Dungeons | nether_landmark | nether_only | dimension_locked | 3 | dangerous_dungeon | common | should_keep |
| betterdungeons:spider_dungeon | YUNG's Better Dungeons | dangerous_dungeon | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | middle/outer | 3 | dangerous_dungeon | rare | should_region_lock |
| betterdungeons:zombie_dungeon | YUNG's Better Dungeons | dangerous_dungeon | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | middle/outer | 3 | dangerous_dungeon | rare | should_region_lock |
| bettermineshafts:mineshaft_acacia | YUNG's Better Mineshafts | dangerous_dungeon | crownlands,hearthlands,north_west_marches,south_west_wilds | middle/outer | 3 | dangerous_dungeon | common | should_region_lock |
| bettermineshafts:mineshaft_desert | YUNG's Better Mineshafts | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | middle/outer | 3 | dangerous_dungeon | common | should_reduce |
| bettermineshafts:mineshaft_dripstone | YUNG's Better Mineshafts | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands | middle/outer | 3 | dangerous_dungeon | common | should_reduce |
| bettermineshafts:mineshaft_ice | YUNG's Better Mineshafts | dangerous_dungeon | frostmarch,north_east_marches | middle/outer | 3 | dangerous_dungeon | common | should_reduce |
| bettermineshafts:mineshaft_jungle | YUNG's Better Mineshafts | dangerous_dungeon | south_east_wilds,verdant_coast | middle/outer | 3 | dangerous_dungeon | common | should_reduce |
| bettermineshafts:mineshaft_lush | YUNG's Better Mineshafts | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands | middle/outer | 3 | dangerous_dungeon | common | should_reduce |
| bettermineshafts:mineshaft_mesa | YUNG's Better Mineshafts | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | middle/outer | 3 | dangerous_dungeon | common | should_reduce |
| bettermineshafts:mineshaft_mushroom | YUNG's Better Mineshafts | dangerous_dungeon | south_east_wilds,south_west_wilds,sunreach,verdant_coast | middle/outer | 3 | dangerous_dungeon | common | should_reduce |
| bettermineshafts:mineshaft_oak | YUNG's Better Mineshafts | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | middle/outer | 3 | dangerous_dungeon | common | should_reduce |
| bettermineshafts:mineshaft_overgrown | YUNG's Better Mineshafts | dangerous_dungeon | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | middle/outer | 3 | dangerous_dungeon | common | should_region_lock |
| bettermineshafts:mineshaft_red_desert | YUNG's Better Mineshafts | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | middle/outer | 3 | dangerous_dungeon | common | should_reduce |
| bettermineshafts:mineshaft_spruce | YUNG's Better Mineshafts | dangerous_dungeon | crownlands,frostmarch_if_snowy,hearthlands,south_east_wilds | middle/outer | 3 | dangerous_dungeon | common | should_region_lock |
| bettermineshafts:mineshaft_spruce_snowy | YUNG's Better Mineshafts | dangerous_dungeon | frostmarch,north_east_marches,north_west_marches,south_west_wilds | middle/outer | 3 | dangerous_dungeon | common | should_reduce |
| betterstrongholds:stronghold | YUNG's Better Strongholds | dangerous_dungeon | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | middle/outer | 3 | dangerous_dungeon | very_rare | should_region_lock |
| block_factorys_bosses:dragon_tower | Bosses'Rise | dragon_tier_zone | boss_theme_region,outer,south_east_wilds,south_west_wilds | outer/edge | 5 | dragon_tier_zone | very_rare | should_keep |
| block_factorys_bosses:kraken_ship | Bosses'Rise | boss_arena | boss_theme_region,coastal_only,frostmarch_if_frozen,outer | outer/edge | 5 | boss_arena | rare | should_keep |
| block_factorys_bosses:sandworm_nest | Bosses'Rise | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | outer/edge | 5 | boss_arena | rare | should_reduce |
| block_factorys_bosses:underworld_arena | Bosses'Rise | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | outer/edge | 5 | boss_arena | rare | should_keep |
| block_factorys_bosses:yeti_hideout | Bosses'Rise | boss_arena | boss_theme_region,frostmarch,north_east_marches,north_west_marches | outer/edge | 5 | boss_arena | uncommon | should_reduce |
| born_in_chaos_v1:clown_caravan_plains | Born in Chaos | uncategorized_structure | atlas_region_matching_biome_tag | inner/middle/outer | 2 | review | very_rare | should_keep |
| born_in_chaos_v1:clown_caravan_savanna | Born in Chaos | uncategorized_structure | atlas_region_matching_biome_tag | inner/middle/outer | 2 | review | very_rare | should_keep |
| born_in_chaos_v1:clown_caravan_taiga | Born in Chaos | uncategorized_structure | atlas_region_matching_biome_tag | inner/middle/outer | 2 | review | very_rare | should_keep |
| born_in_chaos_v1:dark_tower_forest | Born in Chaos | dangerous_dungeon | atlas_region_matching_biome_tag | middle/outer | 3 | dangerous_dungeon | very_rare | should_keep |
| born_in_chaos_v1:dark_tower_plain | Born in Chaos | dangerous_dungeon | atlas_region_matching_biome_tag | middle/outer | 3 | dangerous_dungeon | very_rare | should_keep |
| born_in_chaos_v1:dark_tower_taiga | Born in Chaos | dangerous_dungeon | atlas_region_matching_biome_tag | middle/outer | 3 | dangerous_dungeon | very_rare | should_keep |
| born_in_chaos_v1:farm | Born in Chaos | uncategorized_structure | atlas_region_matching_biome_tag | inner/middle/outer | 2 | review | rare | should_keep |
| born_in_chaos_v1:firewell | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | rare | should_keep |
| born_in_chaos_v1:grave_2003wise | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_2_dling | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_d_4rk_devil_x | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | rare | should_keep |
| born_in_chaos_v1:grave_darktitan | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_derivas | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_euthymia | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_feral | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_fubuki_banzai | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_memesus | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_mike_and_rory | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_nino_4416 | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_orion | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_petasi | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_plug | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_rotborne | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_somfunambulist | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_tem_187 | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:grave_the_gentleman_frog | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | rare | should_keep |
| born_in_chaos_v1:gravecarrionexe | Born in Chaos | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| born_in_chaos_v1:infernal_pumpkin | Born in Chaos | uncategorized_structure | atlas_region_matching_biome_tag | inner/middle/outer | 2 | review | uncommon | should_keep |
| born_in_chaos_v1:mound_of_hounds | Born in Chaos | uncategorized_structure | atlas_region_matching_biome_tag | inner/middle/outer | 2 | review | rare | should_keep |
| born_in_chaos_v1:observation_tower_forest | Born in Chaos | dangerous_dungeon | atlas_region_matching_biome_tag | middle/outer | 3 | dangerous_dungeon | rare | should_keep |
| born_in_chaos_v1:observation_tower_plains | Born in Chaos | dangerous_dungeon | atlas_region_matching_biome_tag | middle/outer | 3 | dangerous_dungeon | unique | should_keep |
| cataclysm:abandoned_spire | cataclysm | boss_arena | boss_theme_region,frostmarch,north_east_marches,north_west_marches | outer/edge | 5 | boss_arena | uncommon | should_reduce |
| cataclysm:abandoned_temple | cataclysm | boss_arena | boss_theme_region,frostmarch,north_east_marches,north_west_marches | outer/edge | 5 | boss_arena | uncommon | should_reduce |
| cataclysm:abandoned_village | cataclysm | boss_arena | boss_theme_region,frostmarch,north_east_marches,north_west_marches | outer/edge | 5 | boss_arena | uncommon | should_reduce |
| cataclysm:acropolis | cataclysm | boss_arena | boss_theme_region,coastal_only,frostmarch_if_frozen,outer | outer/edge | 5 | boss_arena | very_rare | should_keep |
| cataclysm:amethyst_nest | cataclysm | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | outer/edge | 5 | boss_arena | uncommon | should_reduce |
| cataclysm:ancient_factory | cataclysm | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | outer/edge | 5 | boss_arena | very_rare | should_keep |
| cataclysm:burning_arena | cataclysm | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | outer/edge | 5 | boss_arena | very_rare | should_keep |
| cataclysm:cursed_pyramid | cataclysm | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | outer/edge | 5 | boss_arena | very_rare | should_keep |
| cataclysm:desert_occupied_village | cataclysm | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | outer/edge | 5 | boss_arena | uncommon | should_reduce |
| cataclysm:desert_site | cataclysm | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | outer/edge | 5 | boss_arena | uncommon | should_reduce |
| cataclysm:frosted_prison | cataclysm | boss_arena | boss_theme_region,frostmarch,north_east_marches,north_west_marches | outer/edge | 5 | boss_arena | very_rare | should_keep |
| cataclysm:ruined_citadel | cataclysm | boss_arena | boss_theme_region,outer | outer/edge | 5 | boss_arena | rare | should_keep |
| cataclysm:soul_black_smith | cataclysm | boss_arena | boss_theme_region,north_west_marches,outer,south_west_wilds | outer/edge | 5 | boss_arena | rare | should_keep |
| cataclysm:sunken_city | cataclysm | boss_arena | boss_theme_region,coastal_only,frostmarch,frostmarch_if_frozen | outer/edge | 5 | boss_arena | very_rare | should_keep |
| create_structures_arise:chocolate_pit | Create: Structures Arise | uncategorized_structure | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle/outer | 2 | review | unique | should_keep |
| create_structures_arise:create_bastion | Create: Structures Arise | nether_landmark | nether_only | dimension_locked | 3 | dangerous_dungeon | very_rare | should_keep |
| create_structures_arise:create_copper_statue | Create: Structures Arise | uncategorized_structure | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle/outer | 2 | review | very_rare | should_keep |
| create_structures_arise:create_dungeon_base | Create: Structures Arise | dangerous_dungeon | frostmarch,north_east_marches,north_west_marches,south_west_wilds | middle/outer | 3 | dangerous_dungeon | unique | should_keep |
| create_structures_arise:create_ruined_castle | Create: Structures Arise | dangerous_dungeon | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | middle/outer | 3 | dangerous_dungeon | very_rare | should_region_lock |
| create_structures_arise:createairdrop | Create: Structures Arise | uncategorized_structure | frostmarch,north_east_marches,north_west_marches,south_west_wilds | inner/middle/outer | 2 | review | very_rare | should_keep |
| create_structures_arise:createcontainer | Create: Structures Arise | uncategorized_structure | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle/outer | 2 | review | very_rare | should_keep |
| create_structures_arise:createcushercrane | Create: Structures Arise | uncategorized_structure | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle/outer | 2 | review | very_rare | should_keep |
| create_structures_arise:createdesertwell | Create: Structures Arise | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| create_structures_arise:createfluidtank | Create: Structures Arise | uncategorized_structure | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle/outer | 2 | review | very_rare | should_keep |
| create_structures_arise:createhouse | Create: Structures Arise | landmark_or_ruin | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| create_structures_arise:createlittleman | Create: Structures Arise | uncategorized_structure | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle/outer | 2 | review | very_rare | should_keep |
| create_structures_arise:createlosttrainstation | Create: Structures Arise | uncategorized_structure | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle/outer | 2 | review | very_rare | should_keep |
| create_structures_arise:createminiskyvillage | Create: Structures Arise | settlement | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | center/inner | 0 | settlement_basic | very_rare | should_keep |
| create_structures_arise:createmonsterroom | Create: Structures Arise | uncategorized_structure | frostmarch,north_east_marches,north_west_marches,south_west_wilds | inner/middle/outer | 2 | review | very_rare | should_keep |
| create_structures_arise:createoldruine | Create: Structures Arise | landmark_or_ruin | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| create_structures_arise:createpickaxestatue | Create: Structures Arise | uncategorized_structure | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle/outer | 2 | review | very_rare | should_keep |
| create_structures_arise:createwitchhut | Create: Structures Arise | landmark_or_ruin | atlas_region_matching_biome_tag | inner/middle | 1 | minor_ruin | very_rare | should_keep |
| create_structures_arise:crimsite_tower | Create: Structures Arise | dangerous_dungeon | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | middle/outer | 3 | dangerous_dungeon | unique | should_region_lock |
| create_structures_arise:darkcastle | Create: Structures Arise | nether_landmark | nether_only | dimension_locked | 3 | dangerous_dungeon | very_rare | should_keep |
| create_structures_arise:deadlordshouse | Create: Structures Arise | nether_landmark | nether_only | dimension_locked | 1 | minor_ruin | rare | should_keep |
| create_structures_arise:honey_pit | Create: Structures Arise | uncategorized_structure | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle/outer | 2 | review | unique | should_keep |
| create_structures_arise:minetrain | Create: Structures Arise | uncategorized_structure | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle/outer | 2 | review | very_rare | should_keep |
| create_structures_arise:obsidiantemple | Create: Structures Arise | nether_landmark | nether_only | dimension_locked | 3 | dangerous_dungeon | rare | should_keep |
| create_structures_arise:pillager_boat | Create: Structures Arise | uncategorized_structure | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | inner/middle/outer | 2 | review | unique | should_keep |
| create_structures_arise:pillagersteampunkairship | Create: Structures Arise | landmark_or_ruin | frostmarch,north_east_marches,north_west_marches,south_west_wilds | inner/middle | 1 | minor_ruin | unique | should_keep |
| create_structures_arise:towerofochrum | Create: Structures Arise | dangerous_dungeon | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | middle/outer | 3 | dangerous_dungeon | unique | should_region_lock |
| create_structures_arise:windmill | Create: Structures Arise | uncategorized_structure | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | inner/middle/outer | 2 | review | very_rare | should_keep |
| humancompanions:acacia_house | Human Companions | landmark_or_ruin | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | inner/middle | 1 | minor_ruin | common | should_keep |
| humancompanions:birch_house | Human Companions | landmark_or_ruin | south_east_wilds,verdant_coast | inner/middle | 1 | minor_ruin | common | should_keep |
| humancompanions:dark_oak_house | Human Companions | landmark_or_ruin | south_east_wilds,verdant_coast | inner/middle | 1 | minor_ruin | common | should_keep |
| humancompanions:oak_birch_house | Human Companions | landmark_or_ruin | south_east_wilds,verdant_coast | inner/middle | 1 | minor_ruin | common | should_keep |
| humancompanions:oak_house | Human Companions | landmark_or_ruin | south_east_wilds,verdant_coast | inner/middle | 1 | minor_ruin | common | should_keep |
| humancompanions:sandstone_house | Human Companions | landmark_or_ruin | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | inner/middle | 1 | minor_ruin | common | should_keep |
| humancompanions:spruce_house | Human Companions | landmark_or_ruin | frostmarch,north_east_marches,south_east_wilds,verdant_coast | inner/middle | 1 | minor_ruin | common | should_keep |
| humancompanions:terracotta_house | Human Companions | landmark_or_ruin | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | inner/middle | 1 | minor_ruin | common | should_keep |
| iceandfire:cyclops_cave | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,coastal_only,frostmarch,frostmarch_if_frozen | outer/edge | 5 | dragon_tier_zone | common | should_reduce |
| iceandfire:fire_dragon_cave | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,north_west_marches,outer,south_west_wilds | outer/edge | 5 | dragon_tier_zone | common | should_reduce |
| iceandfire:fire_dragon_roost | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,north_west_marches,outer,south_west_wilds | outer/edge | 5 | dragon_tier_zone | common | should_reduce |
| iceandfire:gorgon_temple | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,coastal_only,frostmarch,frostmarch_if_frozen | outer/edge | 5 | dragon_tier_zone | uncommon | should_reduce |
| iceandfire:graveyard | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,frostmarch,north_east_marches,outer | outer/edge | 5 | dragon_tier_zone | uncommon | should_reduce |
| iceandfire:hydra_cave | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,coastal_only,frostmarch_if_frozen,outer | outer/edge | 5 | dragon_tier_zone | common | should_reduce |
| iceandfire:ice_dragon_cave | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,frostmarch,north_east_marches,outer | outer/edge | 5 | dragon_tier_zone | common | should_reduce |
| iceandfire:ice_dragon_roost | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,frostmarch,north_east_marches,outer | outer/edge | 5 | dragon_tier_zone | common | should_reduce |
| iceandfire:lightning_dragon_cave | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,outer,south_east_wilds,south_west_wilds | outer/edge | 5 | dragon_tier_zone | common | should_reduce |
| iceandfire:lightning_dragon_roost | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,outer,south_east_wilds,south_west_wilds | outer/edge | 5 | dragon_tier_zone | common | should_reduce |
| iceandfire:mausoleum | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,frostmarch,north_east_marches,outer | outer/edge | 5 | dragon_tier_zone | uncommon | should_reduce |
| iceandfire:pixie_village | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,frostmarch,frostmarch_if_snowy,north_east_marches | outer/edge | 5 | dragon_tier_zone | common | should_reduce |
| iceandfire:siren_island | Ice And Fire Community Edition | dragon_tier_zone | boss_theme_region,coastal_only,frostmarch,frostmarch_if_frozen | outer/edge | 5 | dragon_tier_zone | common | should_reduce |
| idas:abandoned_lighthouse | Integrated Dungeons and Structures | dangerous_dungeon | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | middle/outer | 3 | dangerous_dungeon | uncommon | needs_test |
| idas:abandoned_vineyard | Integrated Dungeons and Structures | dangerous_dungeon | crownlands,hearthlands,north_west_marches,south_west_wilds | middle/outer | 3 | dangerous_dungeon | common | should_region_lock |
| idas:abandonedhouse | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | middle/outer | 3 | dangerous_dungeon | common | needs_test |
| idas:ancient_mines | Integrated Dungeons and Structures | dangerous_dungeon | frostmarch,north_east_marches,north_west_marches,south_east_wilds | middle/outer | 3 | dangerous_dungeon | rare | needs_test |
| idas:ancient_portal/ancient_portal | Integrated Dungeons and Structures | dangerous_dungeon | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | middle/outer | 3 | dangerous_dungeon | rare | should_region_lock |
| idas:ancient_portal/nether_ancient_portal | Integrated Dungeons and Structures | nether_landmark | nether_only | dimension_locked | 3 | dangerous_dungeon | uncommon | needs_test |
| idas:ancient_statue/ancient_statue_desert | Integrated Dungeons and Structures | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | middle/outer | 3 | dangerous_dungeon | uncommon | needs_test |
| idas:ancient_statue/ancient_statue_jungle | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | middle/outer | 3 | dangerous_dungeon | uncommon | needs_test |
| idas:ancient_statue/ancient_statue_plains | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | middle/outer | 3 | dangerous_dungeon | uncommon | needs_test |
| idas:animal_den/forest_den | Integrated Dungeons and Structures | dangerous_dungeon | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | middle/outer | 3 | dangerous_dungeon | uncommon | should_region_lock |
| idas:animal_den/foxhound_den | Integrated Dungeons and Structures | nether_landmark | nether_only | dimension_locked | 3 | dangerous_dungeon | uncommon | needs_test |
| idas:animal_den/polar_bear_den | Integrated Dungeons and Structures | dangerous_dungeon | frostmarch,north_east_marches,south_east_wilds,verdant_coast | middle/outer | 3 | dangerous_dungeon | uncommon | needs_test |
| idas:apothecary_abode | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,south_west_wilds,sunreach,verdant_coast | middle/outer | 3 | dangerous_dungeon | common | needs_test |
| idas:ars_nouveau/archmages_tower | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,south_west_wilds,sunreach,verdant_coast | middle/outer | 3 | dangerous_dungeon | rare | needs_test |
| idas:bazaar | Integrated Dungeons and Structures | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands,sunreach | middle/outer | 3 | dangerous_dungeon | rare | needs_test |
| idas:bearclaw_inn | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | middle/outer | 3 | dangerous_dungeon | common | needs_test |
| idas:beekeepers_house | Integrated Dungeons and Structures | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands | middle/outer | 3 | dangerous_dungeon | common | needs_test |
| idas:botanist | Integrated Dungeons and Structures | dangerous_dungeon | north_west_marches,south_west_wilds,stoneback_highlands | middle/outer | 3 | dangerous_dungeon | common | needs_test |
| idas:brickhouse | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | middle/outer | 3 | dangerous_dungeon | common | needs_test |
| idas:castle | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | middle/outer | 3 | dangerous_dungeon | common | needs_test |
| idas:collectors_museum | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | middle/outer | 3 | dangerous_dungeon | rare | needs_test |
| idas:cottage | Integrated Dungeons and Structures | dangerous_dungeon | south_east_wilds,verdant_coast | middle/outer | 3 | dangerous_dungeon | uncommon | needs_test |
| idas:desert_camp/desert_camp | Integrated Dungeons and Structures | settlement | crownlands,hearthlands,north_west_marches,region_compatible_settlement | center/inner | 0 | settlement_basic | uncommon | needs_test |
| idas:desert_camp/desert_camp_bygwindswept | Integrated Dungeons and Structures | settlement | crownlands,hearthlands,region_compatible_settlement | center/inner | 0 | settlement_basic | uncommon | needs_test |
| idas:desert_camp/desert_camp_orange | Integrated Dungeons and Structures | settlement | crownlands,hearthlands,region_compatible_settlement | center/inner | 0 | settlement_basic | uncommon | needs_test |
| idas:desert_camp/desert_camp_red | Integrated Dungeons and Structures | settlement | crownlands,hearthlands,north_west_marches,region_compatible_settlement | center/inner | 0 | settlement_basic | uncommon | needs_test |
| idas:desert_market/desert_market | Integrated Dungeons and Structures | settlement | crownlands,hearthlands,north_west_marches,region_compatible_settlement | center/inner | 0 | settlement_basic | uncommon | needs_test |
| idas:desert_market/desert_market_orange | Integrated Dungeons and Structures | settlement | crownlands,hearthlands,region_compatible_settlement | center/inner | 0 | settlement_basic | uncommon | needs_test |
| idas:desert_market/desert_market_red | Integrated Dungeons and Structures | settlement | crownlands,hearthlands,north_west_marches,region_compatible_settlement | center/inner | 0 | settlement_basic | uncommon | needs_test |
| ... | 419 more rows in JSON |  |  |  |

Full machine-readable policy:

- `config/ascendant_structures/structure_tier_registry.json`
- `config/ascendant_structures/structure_region_rules.json`
- `config/ascendant_structures/structure_density_policy.json`
- `config/ascendant_structures/structure_loot_linkage.json`
