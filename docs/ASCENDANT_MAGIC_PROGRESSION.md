# Ascendant Magic Progression

Generated: 2026-06-17T04:18:12+00:00

## Status

This is the active magic progression audit/control scaffold. It does not add new magic mods, does not rewrite spells, and does not enable hard gates.

The goal is to make Iron's Spells and all indexed magic items obey the same Atlas region, Guild rank, rarity, loot, recipe, and material logic used by weapons, armor, loot, and recipes.

## Summary

| Metric | Count |
| --- | --- |
| Indexed spells | 113 |
| Indexed magic items | 273 |
| Magic loot sources | 154 |
| Magic recipe entries | 206 |
| High-tier low-tier loot warnings | 23 |
| High-tier low-tier recipe warnings | 16 |
| Unreviewed magic recipe candidates | 55 |

## Core Rules

- Frost and ice magic lean Frostmarch and cold northern regions.
- Fire, sun, blaze, and desert heat magic lean Sunreach, southern arid regions, and Nether-adjacent routes.
- Nature, poison, water, and storm magic lean Verdant Coast and eastern wet regions.
- Earth, force, gravity, metal, and battle evocation lean Stoneback/highland or dangerous structure routes.
- Dark, void, eldritch, ancient, necromantic, and blood magic lean outer, corrupted, Nether, End, or high-rank content.
- Beginner magic should be discoverable, but it should not drown the player in every school at once.
- High-tier spells should require dangerous structures, bosses, rare materials, or Guild rank progress.
- Spell loot must not bypass the rarity budget or recipe progression scaffold.

## Machine Policy Files

- `config/ascendant_magic/spell_progression_registry.json`
- `config/ascendant_magic/magic_item_progression_registry.json`
- `config/ascendant_magic/school_region_policy.json`
- `config/ascendant_magic/magic_loot_policy.json`
- `config/ascendant_magic/magic_recipe_policy.json`

## School And Region Policy

| School | Atlas Affinity | Spells | Magic Items | Progression Note |
| --- | --- | --- | --- | --- |
| fire | sunreach, south_east_wilds, nether_front | 15 | 20 | Fire magic can appear early as basic utility but high-damage fire spells belong in Sunreach, Nether, boss, or high-rank routes. |
| ice | frostmarch, north_west_marches, north_east_marches | 12 | 20 | Frost magic should lean north and stay away from warm starter-region snow logic. |
| lightning | verdant_coast, stoneback_highlands, south_east_wilds | 10 | 8 | Lightning fits stormy coastal/eastern regions and highland storms; strong chain effects need mid-game or better sources. |
| nature | verdant_coast, south_east_wilds, hearthlands | 11 | 11 | Nature magic can be accessible early through Verdant/Hearthlands utility, with poison and control escalating into mid-game. |
| holy | hearthlands, crownlands, outer_rim | 7 | 11 | Basic support should be discoverable, while major healing and radiant combat should be rank-gated. |
| blood | outer_rim, south_west_wilds, nether_front | 5 | 7 | Blood magic should be rare outside dangerous mobs, cult sites, bosses, or high-rank contracts. |
| ender | end_expanse, outer_rim, stoneback_highlands | 6 | 3 | Mobility-breaking spells should arrive after players have proven exploration and rank progress. |
| eldritch | outer_rim, end_expanse, north_east_marches | 3 | 20 | Eldritch magic is late-game by tone even when individual utility spells are low rarity. |
| evocation | stoneback_highlands, outer_rim, hearthlands | 12 | 13 | Basic evocation is a beginner combat route, but summoning/weapon swarms should move into mid/high ranks. |
| void | outer_rim, end_expanse, nether_front | 5 | 6 | Void magic should be high-rank, dangerous-structure, or boss-tier unless it is a small utility spell. |
| arcane | hearthlands, crownlands, outer_rim | 27 | 154 | Arcane is the bridge school: starter-safe in basic forms, but late-game when tied to ancient knowledge or rare materials. |
| utility | hearthlands, crownlands, all_regions | 0 | 0 | Utility items can be broad, but progression-critical crafting stations and rare books must respect rank and material tiers. |

## Current Risk Notes

- Per-spell school assignment is an audit heuristic where the Iron's Spells jar exposes school labels but not per-spell school JSON in this scan.
- Any high-tier spell or magic item in low-tier loot remains a warning until a narrow loot rewrite is approved.
- Magic recipe candidates remain disabled review notes only.
- This scaffold should be reviewed alongside `docs/ASCENDANT_LOOT_ECONOMY.md` and `docs/RECIPE_PROGRESSION_AUDIT.md` before enabling gates.
