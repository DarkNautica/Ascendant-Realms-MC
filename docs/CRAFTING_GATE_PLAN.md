# Crafting Gate Plan

Generated: 2026-06-17T02:11:41+00:00

This is a planning scaffold only. It does not enable hard gates yet.

## Gate Ladder

| Rarity | Guild Rank | Atlas Ring | Recipe Tier | Material Tier |
| --- | --- | --- | --- | --- |
| common | unranked | center | tier_0_baseline | mundane |
| uncommon | e_rank | center_to_inner | tier_1_early | mundane_to_regional |
| rare | d_rank | inner_to_middle | tier_2_regional | regional |
| epic | c_rank_to_b_rank | middle | tier_3_advanced | refined_or_structure |
| legendary | b_rank_to_a_rank | outer | tier_4_boss | boss_or_rank_proof |
| mythic | a_rank_to_s_rank | outer_to_edge | tier_5_dragon | dragon_or_capstone |
| ascendant | s_rank | edge | tier_6_ascendant | ascendant_capstone |

## Rules

- Legendary, mythic, and ascendant gear cannot be craftable from basic vanilla-only materials.
- High-tier magic should require high-tier materials, boss drops, structures, or rank progression.
- Duplicate material recipes should prefer canonical materials from `config/ascendant_core/materials.json`.
- Endgame weapons should not be craftable before their loot/danger tier.
- Storage and QoL remain useful, but high-tier upgrades need review if they trivialize exploration pacing.
- Food recipes stay generous unless they directly break combat balance.

## Live Enforcement

No hard gates are enabled. Candidate rewrites are generated under `kubejs/server_scripts_disabled/review/ascendant_recipes/` and in `config/ascendant_recipes/candidate_recipe_rewrites.json`.
