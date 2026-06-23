# Structure Testing Checklist

Generated: 2026-06-18T01:57:56Z

Use this after Jayden accepts the current Atlas terrain enough to test structures. Always use a fresh world or ungenerated chunks.

## Setup

1. Create a fresh creative validation world.
2. Keep the current Atlas terrain validation reports for reference.
3. Open `docs/STRUCTURE_VISUAL_REVIEW_ROUTE.md` for the route overview.
4. Open `config/ascendant_structures/structure_locate_commands.md` for copy-ready commands.
5. For each find, record coordinates, Atlas region, visible biome, structure ID, nearby structures, and a screenshot if it fails.

## Current Review Route

- Route file: `config/ascendant_structures/structure_visual_review_route.json`.
- Locate commands: `config/ascendant_structures/structure_locate_commands.md`.
- Priority queue: `config/ascendant_structures/structure_review_priority_queue.json`.
- Results template: `docs/STRUCTURE_DIRECTOR_REVIEW_RESULTS_TEMPLATE.md`.
- Unique locate commands: 154.
- Priority queue entries: 70.

## Recommended Order

1. `highest_risk_first_20`
2. `water_ship_seafloor_top_10`
3. `sky_floating_top_10`
4. `boss_dungeon_top_10`
5. `village_town_overlap_top_10`
6. `beginner_region_risks_top_10`
7. Section sweeps for beginner, dungeon, water, sky, settlement, boss/dragon, and region-fit checks.

## What To Check

- Region fit: structure palette and biome should match Frostmarch, Sunreach, Verdant Coast, Stoneback, Crownlands, or outer-region identity.
- Density: one structure can be exciting; repeated fields of similar landmarks are clutter.
- Water fit: ships, sea-floor ruins, ocean monuments, Aquamirae, sirens, and sunken structures should be water/coast/frozen-ocean content, not inland spam.
- Sky fit: floating islands and airships should feel rare and intentional.
- Settlement fit: villages/towns should not overlap, stack, or erase wilderness gaps.
- Danger fit: bosses, dragons, and high-tier dungeons should not dominate starter regions.
- Loot fit: chest/reward tier should match danger tier; do not judge exact loot rewrites yet.

## Do Not Do During This Test

- Do not add new structure mods.
- Do not inject villages, Hunter Boards, Guild Halls, or NPC placement.
- Do not enable all candidate overrides.
- Do not move review candidates into OpenLoader.
- Do not rewrite loot or recipes.
