# Ascendant Player Progression

Generated: 2026-06-17T04:37:26+00:00

## Status

This is a progression bridge scaffold only. It does not add mods, lock regions, lock recipes, lock skills, change loot, or stop players from reaching existing content.

Rank is public Guild evaluation. Puffish Skills is personal power growth. Loot, gear, magic, bounties, Atlas regions, and boss milestones now have a shared policy spine, but enforcement still needs explicit approval.

## Rank Spine

| Rank | Level Band | Regions | Gear | Magic Tiers | Bounty Work |
| --- | --- | --- | --- | --- | --- |
| Unranked | 1-9 | crownlands | common, uncommon | tier_0_baseline, tier_1_early | none, tutorial, local_errand |
| E-Rank | 10-19 | crownlands, verdant_coast | common, uncommon, rare | tier_1_early, tier_2_regional | village_request, wildlife_control |
| D-Rank | 20-34 | crownlands, verdant_coast, sunreach, stoneback_highlands, frostmarch | uncommon, rare | tier_2_regional | village_request, road_patrol, small_ruin |
| C-Rank | 35-49 | frostmarch, sunreach, verdant_coast, stoneback_highlands, deep_wilds | rare, epic | tier_2_regional, tier_3_advanced | town_guild_board, dungeon_contract, rival_sighting |
| B-Rank | 50-69 | deep_wilds, dragon_scars, frostmarch, sunreach, stoneback_highlands | rare, epic, legendary | tier_3_advanced, tier_4_boss | major_guild_registry, miniboss_contract, arcane_recovery |
| A-Rank | 70-89 | dragon_scars, deep_wilds, nether_front, end_expanse | epic, legendary, mythic | tier_4_boss, tier_5_dragon | realm_threat, dragon_warning, boss_hunt |
| S-Rank | 90-120 | dragon_scars, nether_front, end_expanse, deep_wilds | legendary, mythic, ascendant | tier_5_dragon, tier_6_ascendant | cataclysmic_threat, dragon_tier, ascendant_relic |

## Region Readiness

| Region | Tier | Ranks | Threat | Gear Ceiling |
| --- | --- | --- | --- | --- |
| The Crownlands | 0 | unranked, e_rank | 0-2 | uncommon |
| The Frostmarch | 2 | d_rank, c_rank | 2-4 | legendary |
| Sunreach | 2 | d_rank, c_rank | 2-4 | legendary |
| The Verdant Coast | 2 | d_rank, c_rank | 2-4 | epic |
| The Stoneback Highlands | 2 | d_rank, c_rank | 2-4 | legendary |
| The Deep Wilds | 3 | c_rank, b_rank | 3-5 | mythic |
| The Dragon Scars | 4 | b_rank, a_rank | 4-6 | ascendant |
| The Nether Front | 4 | b_rank, a_rank | 4-6 | mythic |
| The End Expanse | 5 | a_rank, s_rank | 5-6 | ascendant |

## Gear Rank Policy

| Rarity | Minimum Rank | Routine Rank | Role |
| --- | --- | --- | --- |
| common | unranked | unranked | baseline survival, tools, and low-risk rewards |
| uncommon | unranked | e_rank | starter upgrades and safe village rewards |
| rare | e_rank | d_rank | regional gear, early dungeons, and ranked village work |
| epic | c_rank | c_rank | real dungeon rewards, elite drops, and specialized builds |
| legendary | b_rank | b_rank | major structure, boss-adjacent, and high-rank contract rewards |
| mythic | a_rank | a_rank | dragon, boss, and outer-region rewards |
| ascendant | s_rank | s_rank | capstone and ascendant-class rewards only |

## Magic Rank Policy

| Magic Tier | Minimum Rank | Routine Rank | Ceiling Rank |
| --- | --- | --- | --- |
| tier_0_baseline | unranked | unranked | e_rank |
| tier_1_early | unranked | e_rank | d_rank |
| tier_2_regional | d_rank | d_rank | c_rank |
| tier_3_advanced | c_rank | c_rank | b_rank |
| tier_4_boss | b_rank | b_rank | a_rank |
| tier_5_dragon | a_rank | a_rank | s_rank |
| tier_6_ascendant | s_rank | s_rank | s_rank |
| not_craftable_or_not_found | manual_review | manual_review | manual_review |

## Design Rules

- Rank should feel like evaluation, not checklist grinding.
- The player should always have several valid goals at the same time.
- C/B/A/S rank should require real world achievements, not just XP.
- Prefer guidance, rank display, reward pacing, and quest language before hard gates.
- Terrain/water acceptance still comes before civilization, road, village, Hunter Board, or Guild Hall placement work.
