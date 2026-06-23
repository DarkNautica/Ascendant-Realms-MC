# Structure Visual Review Route

Generated: 2026-06-18T01:57:56Z

This is the first in-game Structure Director validation route. It is review-only. It does not add mods, enable live structure overrides, inject Hunter Boards or Guild Halls, place NPCs, alter villages, alter roads or bridges, rewrite loot, rewrite recipes, enable magic gates, or enable rank gates.

## Summary

- Route sections: 7.
- Unique locate commands in route: 154.
- Priority queue entries: 70.
- Unique priority structures: 50.
- Source structure registry rows: 579.
- Structure set policy rows: 330.
- Candidate overrides remain disabled under `config/ascendant_structures/candidates/`.
- Latest field findings, when present: `docs/STRUCTURE_VISUAL_REVIEW_FINDINGS.md`.

## How To Use

1. Create a fresh creative validation world or fly into ungenerated chunks.
2. Open `config/ascendant_structures/structure_locate_commands.md`.
3. Start with `highest_risk_first_20`, then water, sky, boss/dungeon, village/town, and beginner-region queues.
4. For each entry, use the search-origin teleport if listed, run `/locate structure <id>`, then teleport to the returned coordinates.
5. Run `/ascatlas here` at the located structure and record the Atlas region, visible biome, coordinates, screenshots, and pass/fail notes.

## Route Sections

| Section | ID | Entries |
| --- | --- | --- |
| Beginner-region structures | beginner_region_structures | 36 |
| Dungeon structures | dungeon_structures | 42 |
| Water structures | water_structures | 29 |
| Sky structures | sky_structures | 16 |
| Village/town/settlement structures | village_town_settlement_structures | 40 |
| Boss/dragon structures | boss_dragon_structures | 36 |
| Region-fit checks | region_fit_checks | 72 |

## Priority Queues

| Queue | Entries | First IDs |
| --- | --- | --- |
| highest_risk_first_20 | 20 | idas:abandoned_vineyard, iceandfire:fire_dragon_roost, iceandfire:ice_dragon_roost, iceandfire:lightning_dragon_roost, iceandfire:cyclops_cave |
| water_ship_seafloor_top_10 | 10 | idas:sunken_ship/sunken_ship, idas:sunken_ship/sunken_ship_ruins, mvs:ocean_tower, minecraft:monument, iceandfire:siren_island |
| sky_floating_top_10 | 10 | cataclysm:acropolis, mss:arena, integrated_villages:airship_village, medievalend:ship, terralith:mage_tower_autumn |
| boss_dungeon_top_10 | 10 | idas:abandoned_vineyard, iceandfire:fire_dragon_roost, iceandfire:ice_dragon_roost, iceandfire:lightning_dragon_roost, iceandfire:cyclops_cave |
| village_town_overlap_top_10 | 10 | iceandfire:pixie_village, cataclysm:abandoned_village, cataclysm:desert_occupied_village, idas:abandonedhouse, idas:bearclaw_inn |
| beginner_region_risks_top_10 | 10 | idas:abandoned_vineyard, betterdungeons:small_dungeon, bettermineshafts:mineshaft_acacia, bettermineshafts:mineshaft_overgrown, bettermineshafts:mineshaft_spruce |

## First 20 Highest-Risk Checks

| Structure | Mod | Region | Layer | Density | Danger | Loot | Action | Locate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| idas:abandoned_vineyard | Integrated Dungeons and Structures | crownlands | surface_land | common | 3 | dangerous_dungeon | should_region_lock | /locate structure idas:abandoned_vineyard |
| iceandfire:fire_dragon_roost | Ice And Fire Community Edition | boss_theme_region | surface_land | common | 5 | dragon_tier_zone | should_reduce | /locate structure iceandfire:fire_dragon_roost |
| iceandfire:ice_dragon_roost | Ice And Fire Community Edition | boss_theme_region | surface_land | common | 5 | dragon_tier_zone | should_reduce | /locate structure iceandfire:ice_dragon_roost |
| iceandfire:lightning_dragon_roost | Ice And Fire Community Edition | boss_theme_region | surface_land | common | 5 | dragon_tier_zone | should_reduce | /locate structure iceandfire:lightning_dragon_roost |
| iceandfire:cyclops_cave | Ice And Fire Community Edition | boss_theme_region | coastal_surface | common | 5 | dragon_tier_zone | should_reduce | /locate structure iceandfire:cyclops_cave |
| betterdungeons:small_dungeon | YUNG's Better Dungeons | crownlands | surface_land | common | 3 | dangerous_dungeon | should_region_lock | /locate structure betterdungeons:small_dungeon |
| bettermineshafts:mineshaft_acacia | YUNG's Better Mineshafts | crownlands | surface_land | common | 3 | dangerous_dungeon | should_region_lock | /locate structure bettermineshafts:mineshaft_acacia |
| bettermineshafts:mineshaft_overgrown | YUNG's Better Mineshafts | crownlands | surface_land | common | 3 | dangerous_dungeon | should_region_lock | /locate structure bettermineshafts:mineshaft_overgrown |
| bettermineshafts:mineshaft_spruce | YUNG's Better Mineshafts | crownlands | surface_land | common | 3 | dangerous_dungeon | should_region_lock | /locate structure bettermineshafts:mineshaft_spruce |
| iceandfire:siren_island | Ice And Fire Community Edition | boss_theme_region | sea_surface | common | 5 | dragon_tier_zone | should_reduce | /locate structure iceandfire:siren_island |
| iceandfire:graveyard | Ice And Fire Community Edition | boss_theme_region | surface_land | uncommon | 5 | dragon_tier_zone | should_reduce | /locate structure iceandfire:graveyard |
| minecraft:mineshaft | YUNG's Better Mineshafts | coastal_only | river_or_wetland | common | 2 | review | should_region_lock | /locate structure minecraft:mineshaft |
| iceandfire:hydra_cave | Ice And Fire Community Edition | boss_theme_region | surface_land | common | 5 | dragon_tier_zone | should_reduce | /locate structure iceandfire:hydra_cave |
| iceandfire:pixie_village | Ice And Fire Community Edition | boss_theme_region | surface_land | common | 5 | dragon_tier_zone | should_reduce | /locate structure iceandfire:pixie_village |
| idas:haunted_manor | Integrated Dungeons and Structures | north_west_marches | surface_land | common | 3 | dangerous_dungeon | needs_test | /locate structure idas:haunted_manor |
| irons_spellbooks:mountain_tower | Iron's Spells 'n Spellbooks | atlas_region_matching_biome_tag | surface_land | unknown | 3 | dangerous_dungeon | needs_test | /locate structure irons_spellbooks:mountain_tower |
| iceandfire:fire_dragon_cave | Ice And Fire Community Edition | boss_theme_region | surface_land | common | 5 | dragon_tier_zone | should_reduce | /locate structure iceandfire:fire_dragon_cave |
| iceandfire:ice_dragon_cave | Ice And Fire Community Edition | boss_theme_region | surface_land | common | 5 | dragon_tier_zone | should_reduce | /locate structure iceandfire:ice_dragon_cave |
| iceandfire:lightning_dragon_cave | Ice And Fire Community Edition | boss_theme_region | surface_land | common | 5 | dragon_tier_zone | should_reduce | /locate structure iceandfire:lightning_dragon_cave |
| irons_spellbooks:pyromancer_tower | Iron's Spells 'n Spellbooks | crownlands | surface_land | unknown | 3 | dangerous_dungeon | should_region_lock | /locate structure irons_spellbooks:pyromancer_tower |

## Review Questions

- Does it belong in this biome/region?
- Is it too close to spawn?
- Is it too common?
- Is it buried, floating, or clipping?
- Does terrain support it naturally?
- Does water structure actually sit in appropriate water?
- Does sea-floor structure actually sit on sea floor?
- Does sky structure feel rare/special or spammy?
- Does boss structure feel too early?
- Does village/town structure overlap or compress?
- Does loot/danger appear appropriate?

## Boundaries

- Do not enable candidate overrides from this route.
- Do not move files into OpenLoader from this route.
- Do not inject villages, roads, bridges, Hunter Boards, Guild Halls, NPCs, loot rewrites, recipe gates, magic gates, or rank gates.
- Use this route to gather evidence, not to make automatic decisions.
