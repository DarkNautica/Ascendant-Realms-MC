# Magic Loot And Recipe Audit

Generated: 2026-06-17T04:18:12+00:00

This audit links indexed spells and magic items to the current loot economy and recipe progression scaffolds. It is intentionally review-only: no KubeJS recipe rewrites, loot rewrites, spell edits, or rank gates are enabled.

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

## Rarity Distribution

| Rarity | Count |
| --- | --- |
| epic | 78 |
| uncommon | 67 |
| rare | 201 |
| legendary | 37 |
| mythic | 3 |

## School Distribution

| School | Count |
| --- | --- |
| holy | 18 |
| evocation | 25 |
| ice | 32 |
| void | 11 |
| fire | 35 |
| arcane | 181 |
| nature | 22 |
| lightning | 18 |
| eldritch | 23 |
| ender | 9 |
| blood | 12 |

## High-Tier Magic In Low-Tier Loot

| Item/Spell | Rarity | Source | Context | Source Rank | Source Ceiling |
| --- | --- | --- | --- | --- | --- |
| irons_spellbooks:ancient_knowledge_fragment | legendary | irons_spellbooks:chests/additional_ancient_city_loot | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:ancient_knowledge_fragment | legendary | irons_spellbooks:chests/additional_end_city_loot | structure | e_rank_to_b_rank | rare |
| irons_spellbooks:ancient_knowledge_fragment | legendary | irons_spellbooks:chests/additional_library_loot | structure | e_rank_to_b_rank | rare |
| irons_spellbooks:ancient_knowledge_fragment | legendary | irons_spellbooks:chests/additional_treasure_loot | structure | e_rank_to_b_rank | rare |
| irons_spellbooks:ancient_knowledge_fragment | legendary | irons_spellbooks:chests/catacombs/crypt_loot | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:ancient_knowledge_fragment | legendary | irons_spellbooks:chests/catacombs/dead_king_vault | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:ancient_knowledge_fragment | legendary | irons_spellbooks:chests/catacombs/wall_loot | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:ancient_knowledge_fragment | legendary | irons_spellbooks:chests/magic_bookshelf_loot | structure | e_rank_to_b_rank | rare |
| irons_spellbooks:ancient_knowledge_fragment | legendary | idas:chests/archmages_tower/archmages_tower_treasure | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:ancient_knowledge_fragment | legendary | irons_spellbooks:chests/catacombs/crypt_loot | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:ancient_knowledge_fragment | legendary | idas:chests/archmages_tower/archmages_tower_treasure | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:ancient_knowledge_fragment | legendary | irons_spellbooks:chests/catacombs/crypt_loot | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:dead_king_phylactery_shard | legendary | irons_spellbooks:chests/catacombs/crypt_loot | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:dead_king_phylactery_shard | legendary | irons_spellbooks:chests/catacombs/dead_king_vault | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:dead_king_phylactery_shard | legendary | irons_spellbooks:spawners/catacombs/ominous_zombie_spawner | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:dead_king_phylactery_shard | legendary | irons_spellbooks:spawners/catacombs/regular_zombie_spawner | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:legendary_ink | mythic | irons_spellbooks:magic_items/great_ink | generic | manual_review | rare |
| irons_spellbooks:legendary_ink | mythic | irons_spellbooks:magic_items/reward_ink | generic | manual_review | rare |
| irons_spellbooks:legendary_spell_book | mythic | idas:chests/archmages_tower/archmages_tower_treasure | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:legendary_spell_book | mythic | idas:chests/archmages_tower/archmages_tower_treasure | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:music_disc_dead_king_lullaby | legendary | irons_spellbooks:chests/catacombs/pot | dungeon | d_rank_to_b_rank | epic |
| irons_spellbooks:necronomicon_spell_book | legendary | irons_spellbooks:entities/dead_king | mob | unranked_to_c_rank | uncommon |
| soulsweapons:chungus_staff | legendary | soulsweapons:gameplay/chungus_bartering | generic | manual_review | rare |

## High-Tier Or Review Magic Recipes

| Item/Spell | Rarity | Recipe | Status | Proposed Replacement |
| --- | --- | --- | --- | --- |
| fantasy_armor:wandering_wizard_chestplate | legendary | fantasy_armor:wandering_wizard_chestplate | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| iceandfire:dragon_stick | mythic | iceandfire:dragon_stick | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| iceandfire:pixie_wand | legendary | iceandfire:pixie_wand | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| irons_spellbooks:legendary_ink | mythic | irons_spellbooks:alchemist_cauldron/empty_legendary_ink | bypass | Add boss, dragon, structure, or Guild-rank proof materials; keep disabled until reviewed. |
| irons_spellbooks:legendary_ink | mythic | irons_spellbooks:create_compat/create_fill_legendary_ink | bypass | Add boss, dragon, structure, or Guild-rank proof materials; keep disabled until reviewed. |
| irons_spellbooks:dead_king_phylactery | legendary | irons_spellbooks:dead_king_phylactery | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| irons_spellbooks:hellrazor | legendary | irons_spellbooks:decrepit_scythe_repair | too_cheap | Raise ingredients to match boss/dragon/rank tier or convert to loot-only progression. |
| irons_spellbooks:dragonskin_spell_book | legendary | irons_spellbooks:dragonskin_spell_book | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| irons_spellbooks:infernal_sorcerer_chestplate | legendary | irons_spellbooks:infernal_sorcerer_chestplate | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| irons_spellbooks:netherite_mage_boots | legendary | irons_spellbooks:netherite_mage_boots | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| irons_spellbooks:netherite_mage_chestplate | legendary | irons_spellbooks:netherite_mage_chestplate | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| irons_spellbooks:netherite_mage_helmet | legendary | irons_spellbooks:netherite_mage_helmet | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| irons_spellbooks:netherite_mage_leggings | legendary | irons_spellbooks:netherite_mage_leggings | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| irons_spellbooks:netherite_spell_book | legendary | irons_spellbooks:netherite_spell_book | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| soulsweapons:chungus_staff | legendary | soulsweapons:chungus_staff | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |
| soulsweapons:dragon_staff | legendary | soulsweapons:dragon_staff | needs_manual_review | Confirm JEI path matches Guild rank and Atlas ring before enabling changes. |

## Candidate Output

Candidate guidance is written to `kubejs/server_scripts_disabled/review/ascendant_magic/magic_progression_candidates.js`. It is disabled by path and contains comments only, so it cannot change live recipes or loot.
