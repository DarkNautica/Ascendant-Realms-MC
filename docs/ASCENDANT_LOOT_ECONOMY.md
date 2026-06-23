# Ascendant Loot Economy System

Generated: 2026-06-17T02:04:15+00:00

## Status

This is the active loot and reward economy control scaffold. It audits installed mod jar loot tables, repo OpenLoader/datapack loot tables, live Bountiful reward pools, Loot Integrations behavior, the gear rarity registry, structure tiers, mob tiers, boss tiers, magic/spell sources, accessory/relic sources, and canonical material rewards.

No broad loot rewrites are enabled by this pass. Candidate notes live under `kubejs/server_scripts_disabled/review/ascendant_loot/` and are ignored by Minecraft.

## Core Rules

- Crownlands/Hearthlands and early village loot cannot award legendary, mythic, or ascendant gear.
- Early villages cannot award boss-tier or dragon-tier materials.
- Common dungeons may award common, uncommon, and rare items; dangerous dungeons may reach epic when the structure tier supports it.
- Boss-tier content must reward above random chests, with epic to mythic rewards depending on boss tier.
- Structure loot must match the structure danger tier in `config/ascendant_loot/structure_loot_tiers.json`.
- Bounties pay Guild Marks, Hunter Seals, or rank-appropriate rewards from `config/ascendant_loot/bounty_reward_pools.json`.
- Magic items and spells use the same rarity budget as gear, with boss/outer-region spell loot reserved for higher ranks.
- Relics and accessories are rare by default and should be tied to exploration, bosses, or ranked contracts.
- Loot policy must support `config/ascendant_index/gear_registry.json`, not contradict it.

## Machine Policy Files

- `config/ascendant_loot/loot_policy.json`: full loot-source audit and source-level assignments.
- `config/ascendant_loot/structure_loot_tiers.json`: every indexed structure mapped to reward tier, danger tier, rank tier, and rarity ceiling.
- `config/ascendant_loot/mob_drop_tiers.json`: every indexed mob mapped to drop tier and bounty/drop guardrails.
- `config/ascendant_loot/boss_reward_tiers.json`: boss and dragon reward tiers.
- `config/ascendant_loot/bounty_reward_pools.json`: live Bountiful reward pools with rank/danger ceilings.
- `config/ascendant_loot/loot_rarity_budget.json`: shared context, rank, and ring rarity ceilings.

## Audit Summary

| Metric | Count |
| --- | --- |
| Loot tables audited | 4354 |
| Installed mod jars scanned | 174 |
| Repo datapack/OpenLoader loot tables | 30 |
| High-rarity low-tier warnings | 30 |
| High-rarity village/basic warnings | 38 |
| Structure reward entries | 617 |
| Mob drop entries | 757 |
| Boss reward entries | 69 |
| Bountiful reward pools | 6 |

## Loot Integrations

`config/lootintegrations.json` is present and currently allows extra modded loot injection with `moddedItemWeight = 3`. That means random containers can receive additional modded items outside the original loot table. The scaffold treats this as a control risk: do not raise that weight, and do not rely on original chest tables alone for progression safety.

## Current Risk Notes

- Any source with `recommended_action = manual_review` needs human review before a real rewrite.
- Any village or settlement source showing epic-or-better output must be reduced or gated before terrain/civilization signoff.
- Boss and dragon drops should be preserved or improved, not flattened into generic chest loot.

## High-Rarity Low-Tier Examples

| Source | Context | Flagged Items |
| --- | --- | --- |
| born_in_chaos_v1:entities/infernal_spirit | mob | born_in_chaos_v1:smoldering_infernal_ember (legendary) |
| born_in_chaos_v1:entities/lord_pumpkinhead_head | mob | born_in_chaos_v1:smoldering_infernal_ember (legendary) |
| born_in_chaos_v1:entities/mr_pumpkin | mob | born_in_chaos_v1:smoldering_infernal_ember (legendary) |
| born_in_chaos_v1:entities/pumpkin_bruiser | mob | born_in_chaos_v1:smoldering_infernal_ember (legendary) |
| born_in_chaos_v1:entities/pumpkin_dunce | mob | born_in_chaos_v1:smoldering_infernal_ember (legendary) |
| born_in_chaos_v1:entities/pumpkinhead | mob | born_in_chaos_v1:soul_cutlass (mythic), born_in_chaos_v1:smoldering_infernal_ember (legendary) |
| born_in_chaos_v1:entities/senor_pumpkin | mob | born_in_chaos_v1:smoldering_infernal_ember (legendary) |
| born_in_chaos_v1:entities/skeleton_thrasher | mob | born_in_chaos_v1:skullbreaker_hammer (legendary) |
| born_in_chaos_v1:entities/skeleton_thrasher_not_despawn | mob | born_in_chaos_v1:skullbreaker_hammer (legendary) |
| born_in_chaos_v1:entities/supreme_bonescaller_stage_2 | mob | born_in_chaos_v1:death_totem (legendary) |
| born_in_chaos_v1:entities/zombie_clown | mob | born_in_chaos_v1:intoxicating_dagger (legendary) |
| born_in_chaos_v1:entities/zombie_clown_not_despawn | mob | born_in_chaos_v1:intoxicating_dagger (legendary) |
| iceandfire:chest/village_scribe | village | iceandfire:dragonbone (mythic) |
| irons_spellbooks:entities/citadel_keeper | mob | minecraft:netherite_scrap (mythic) |
| irons_spellbooks:entities/dead_king | mob | irons_spellbooks:necronomicon_spell_book (legendary) |
| cataclysm:entities/deepling_priest | mob | cataclysm:athame (legendary) |
| cataclysm:entities/deepling_warlock | mob | cataclysm:athame (legendary) |
| cataclysm:entities/netherite_ministrosity | mob | cataclysm:netherite_effigy (mythic) |
| cataclysm:entities/netherite_monstrosity | mob | cataclysm:music_disc_netherite_monstrosity (mythic) |
| mowziesmobs:entities/umvuthana_misery | mob | mowziesmobs:umvuthana_mask_misery (legendary) |
