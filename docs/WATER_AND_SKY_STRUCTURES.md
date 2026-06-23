# Water And Sky Structures

Generated: 2026-06-18T01:57:55+00:00

This separates structures that need water, coast, sea-floor, wetland, or sky rules. These should never be judged as ordinary land structures.

## Summary

- Water structures: 22.
- Sea-floor structures: 4.
- Ship/ocean-surface structures: 13.
- Sky structures: 14.
- Water structures outside explicit water-region policy: 0.
- Sky structures common or near spawn: 2.

## Water Structures

| Structure | Mod | Water Role | Layers | Regions | Action |
| --- | --- | --- | --- | --- | --- |
| create_structures_arise:pillager_boat | Create: Structures Arise | ocean | sea_surface | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | should_keep |
| iceandfire:siren_island | Ice And Fire Community Edition | ocean | sea_surface | boss_theme_region,coastal_only,frostmarch,frostmarch_if_frozen | should_reduce |
| idas:iceandfire/sirens_cove | Integrated Dungeons and Structures | ocean | sea_surface | boss_theme_region,coastal_only,frostmarch,frostmarch_if_frozen | should_reduce |
| idas:sunken_ship/sunken_ship | Integrated Dungeons and Structures | sea_floor | sea_floor | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | needs_test |
| idas:sunken_ship/sunken_ship_coral | Integrated Dungeons and Structures | ocean | sea_surface | coastal_only,frostmarch_if_frozen,verdant_coast | needs_test |
| idas:sunken_ship/sunken_ship_ruins | Integrated Dungeons and Structures | sea_floor | sea_floor | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | needs_test |
| integrated_villages:pirate_village | Integrated Villages | ocean | sea_surface | coastal_only,crownlands,frostmarch,frostmarch_if_frozen | needs_test |
| minecraft:mineshaft | YUNG's Better Mineshafts | river_or_wetland | river_or_wetland | coastal_only,crownlands,frostmarch,frostmarch_if_frozen | should_region_lock |
| minecraft:monument | Minecraft | sea_floor | sea_floor | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | should_keep |
| minecraft:ruined_portal_ocean | Minecraft | ocean | sea_surface | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | should_keep |
| minecraft:shipwreck | Minecraft | ocean | sea_surface | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | should_keep |
| mowziesmobs:frostmaw_spawn | Mowzie's Mobs | river_or_wetland | river_or_wetland | coastal_only,crownlands,frostmarch,frostmarch_if_frozen | should_keep |
| mowziesmobs:monastery | Mowzie's Mobs | river_or_wetland | river_or_wetland | coastal_only,crownlands,frostmarch,frostmarch_if_frozen | should_keep |
| mowziesmobs:umvuthana_grove | Mowzie's Mobs | river_or_wetland | river_or_wetland | coastal_only,crownlands,frostmarch,frostmarch_if_frozen | should_keep |
| mowziesmobs:wrought_chamber | Mowzie's Mobs | river_or_wetland | river_or_wetland | coastal_only,crownlands,frostmarch,frostmarch_if_frozen | should_keep |
| mss:palm_island | moogs_structures | ocean | sea_surface | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | should_keep |
| mvs:ocean_tower | moogs_structures | sea_floor | sea_floor | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | should_keep |
| mvs:rare_well | moogs_structures | ocean | sea_surface | frostmarch,north_east_marches,north_west_marches,south_west_wilds | should_keep |
| mvs:small_ship | moogs_structures | ocean | sea_surface | coastal_only,frostmarch,frostmarch_if_frozen,north_east_marches | should_keep |
| mvs:well | moogs_structures | ocean | sea_surface | frostmarch,north_east_marches,north_west_marches,south_west_wilds | should_keep |
| structory:boat | Structory | ocean | sea_surface | coastal_only,frostmarch_if_frozen,verdant_coast | needs_test |
| towns_and_towers:pillager_outpost_ocean | Towns and Towers | ocean | sea_surface | coastal_only,crownlands,frostmarch_if_frozen,hearthlands | needs_test |

## Sky Structures

| Structure | Mod | Sky Role | Regions | Spacing | Action |
| --- | --- | --- | --- | --- | --- |
| cataclysm:acropolis | cataclysm | rare_high_sky | boss_theme_region,coastal_only,frostmarch_if_frozen,outer | 80 | should_keep |
| create_structures_arise:createairdrop | Create: Structures Arise | rare_low_sky | frostmarch,north_east_marches,north_west_marches,south_west_wilds | 90 | should_keep |
| create_structures_arise:createminiskyvillage | Create: Structures Arise | rare_high_sky | crownlands,frostmarch,frostmarch_if_snowy,hearthlands | 120 | should_keep |
| create_structures_arise:pillagersteampunkairship | Create: Structures Arise | rare_high_sky | frostmarch,north_east_marches,north_west_marches,south_west_wilds | 150 | should_keep |
| integrated_villages:airship_village | Integrated Villages | rare_low_sky | crownlands,frostmarch,hearthlands,north_east_marches | 115 | needs_test |
| medievalend:ship | Medieval Buildings [The End Edition] | rare_low_sky | atlas_region_matching_biome_tag | None | needs_test |
| mss:arena | moogs_structures | rare_low_sky | boss_theme_region,frostmarch,north_east_marches,north_west_marches | 158 | should_keep |
| mss:diorite_house | moogs_structures | rare_low_sky | frostmarch,north_east_marches,north_west_marches,south_west_wilds | 126 | should_keep |
| mss:large_tower | moogs_structures | rare_low_sky | frostmarch,north_east_marches,north_west_marches,south_west_wilds | 120 | should_keep |
| mss:white_house | moogs_structures | rare_low_sky | frostmarch,north_east_marches,north_west_marches,south_west_wilds | 125 | should_keep |
| terralith:mage_tower_autumn | Terralith | rare_high_sky | coastal_only,frostmarch_if_frozen,verdant_coast | 28 | should_keep |
| terralith:mage_tower_spring | Terralith | rare_high_sky | coastal_only,frostmarch_if_frozen,verdant_coast | 28 | should_keep |
| terralith:mage_tower_summer | Terralith | rare_high_sky | coastal_only,frostmarch_if_frozen,south_west_wilds,sunreach | 28 | should_keep |
| terralith:mage_tower_winter | Terralith | rare_high_sky | coastal_only,frostmarch_if_frozen,verdant_coast | 28 | should_keep |
