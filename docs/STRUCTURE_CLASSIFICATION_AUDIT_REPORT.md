# Structure Classification Audit Report

Generated: 2026-06-18T01:57:55+00:00

## Summary

- Structures with evidence rows: 579.
- Strong confidence rows: 543.
- Medium confidence rows: 33.
- Weak confidence rows: 3.
- Manual-review rows: 13.
- Name-only final classifications: 0.
- Water roles without non-name evidence: 0.
- Frozen-ocean roles without cold/frozen evidence: 0.
- Sky roles without height evidence: 0.

## Ice And Fire Correction

| Structure | Class | Water Role | Regions | Confidence | Manual Review | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| iceandfire:cyclops_cave | dragon_tier_zone | none | boss_theme_region,coastal_only,frostmarch,frostmarch_if_frozen | 96 | False | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:fire_dragon_cave | dragon_tier_zone | none | boss_theme_region,north_west_marches,outer,south_west_wilds | 96 | False | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:fire_dragon_roost | dragon_tier_zone | none | boss_theme_region,north_west_marches,outer,south_west_wilds | 100 | True | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:gorgon_temple | dragon_tier_zone | none | boss_theme_region,coastal_only,frostmarch,frostmarch_if_frozen | 100 | False | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:graveyard | dragon_tier_zone | none | boss_theme_region,frostmarch,north_east_marches,outer | 100 | True | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:hydra_cave | dragon_tier_zone | none | boss_theme_region,coastal_only,frostmarch_if_frozen,outer | 96 | False | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:ice_dragon_cave | dragon_tier_zone | none | boss_theme_region,frostmarch,north_east_marches,outer | 96 | False | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:ice_dragon_roost | dragon_tier_zone | none | boss_theme_region,frostmarch,north_east_marches,outer | 100 | True | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:lightning_dragon_cave | dragon_tier_zone | none | boss_theme_region,outer,south_east_wilds,south_west_wilds | 96 | False | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:lightning_dragon_roost | dragon_tier_zone | none | boss_theme_region,outer,south_east_wilds,south_west_wilds | 100 | True | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:mausoleum | dragon_tier_zone | none | boss_theme_region,frostmarch,north_east_marches,outer | 100 | False | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:pixie_village | dragon_tier_zone | none | boss_theme_region,frostmarch,frostmarch_if_snowy,north_east_marches | 96 | False | Registry class `dragon_tier_zone` is used as medium evidence. |
| iceandfire:siren_island | dragon_tier_zone | ocean | boss_theme_region,coastal_only,frostmarch,frostmarch_if_frozen | 96 | False | Registry class `dragon_tier_zone` is used as medium evidence. Water role comes from biome/block evidence: ocean. |

## IDAS Override Handling

- iceandfire:gorgon_temple locate evidence is recorded as IDAS replacement idas:labyrinth; the active generated result looked good.
- iceandfire:graveyard locate evidence is recorded as IDAS replacement idas:haunted_manor; placement still needs follow-up if it looks wrong.


## Manual Review Queue Preview

| Structure | Class | Water | Sky | Confidence | Risk Flags |
| --- | --- | --- | --- | --- | --- |
| iceandfire:fire_dragon_roost | dragon_tier_zone | none | none | 100 | manual_water_island_placement_issue |
| iceandfire:graveyard | dragon_tier_zone | none | none | 100 | manual_followup_required |
| iceandfire:ice_dragon_roost | dragon_tier_zone | none | none | 100 | manual_water_island_placement_issue |
| iceandfire:lightning_dragon_roost | dragon_tier_zone | none | none | 100 | manual_water_island_placement_issue |
| idas:abandoned_vineyard | dangerous_dungeon | none | none | 100 | manual_water_island_placement_issue |
| idas:haunted_manor | dangerous_dungeon | none | none | 100 | manual_followup_required |
| integrated_villages:pirate_village | settlement | ocean | none | 100 | water_structure_can_overlap_land_first_region |
| irons_spellbooks:evoker_fort | uncategorized_structure | none | none | 27 |  |
| irons_spellbooks:mangrove_hut | landmark_or_ruin | none | none | 28 |  |
| irons_spellbooks:mountain_tower | dangerous_dungeon | none | none | 28 |  |
| mvs:rare_well | landmark_or_ruin | ocean | none | 100 | water_structure_can_overlap_land_first_region |
| mvs:well | landmark_or_ruin | ocean | none | 100 | water_structure_can_overlap_land_first_region |
| towns_and_towers:pillager_outpost_ocean | settlement | ocean | none | 100 | water_structure_can_overlap_land_first_region |
