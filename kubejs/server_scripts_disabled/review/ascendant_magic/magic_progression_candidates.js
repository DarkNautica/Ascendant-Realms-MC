// Ascendant Magic progression candidate notes.
// Disabled review-only file. It lives under kubejs/server_scripts_disabled and is not loaded by Minecraft.
// Do not move this into kubejs/server_scripts until Jayden approves narrow, source-specific magic gates or rewrites.

// High-tier magic in low-tier loot candidates:
// - Review loot source irons_spellbooks:chests/additional_ancient_city_loot exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/additional_end_city_loot exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in structure / e_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/additional_library_loot exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in structure / e_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/additional_treasure_loot exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in structure / e_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/catacombs/crypt_loot exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/catacombs/dead_king_vault exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/catacombs/wall_loot exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/magic_bookshelf_loot exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in structure / e_rank_to_b_rank.
// - Review loot source idas:chests/archmages_tower/archmages_tower_treasure exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/catacombs/crypt_loot exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source idas:chests/archmages_tower/archmages_tower_treasure exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/catacombs/crypt_loot exposing irons_spellbooks:ancient_knowledge_fragment (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/catacombs/crypt_loot exposing irons_spellbooks:dead_king_phylactery_shard (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/catacombs/dead_king_vault exposing irons_spellbooks:dead_king_phylactery_shard (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:spawners/catacombs/ominous_zombie_spawner exposing irons_spellbooks:dead_king_phylactery_shard (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:spawners/catacombs/regular_zombie_spawner exposing irons_spellbooks:dead_king_phylactery_shard (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:magic_items/great_ink exposing irons_spellbooks:legendary_ink (mythic) in generic / manual_review.
// - Review loot source irons_spellbooks:magic_items/reward_ink exposing irons_spellbooks:legendary_ink (mythic) in generic / manual_review.
// - Review loot source idas:chests/archmages_tower/archmages_tower_treasure exposing irons_spellbooks:legendary_spell_book (mythic) in dungeon / d_rank_to_b_rank.
// - Review loot source idas:chests/archmages_tower/archmages_tower_treasure exposing irons_spellbooks:legendary_spell_book (mythic) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:chests/catacombs/pot exposing irons_spellbooks:music_disc_dead_king_lullaby (legendary) in dungeon / d_rank_to_b_rank.
// - Review loot source irons_spellbooks:entities/dead_king exposing irons_spellbooks:necronomicon_spell_book (legendary) in mob / unranked_to_c_rank.
// - Review loot source soulsweapons:gameplay/chungus_bartering exposing soulsweapons:chungus_staff (legendary) in generic / manual_review.

// High-tier or risky magic recipe candidates:
// - Review recipe fantasy_armor:wandering_wizard_chestplate for fantasy_armor:wandering_wizard_chestplate (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe iceandfire:dragon_stick for iceandfire:dragon_stick (mythic): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe iceandfire:pixie_wand for iceandfire:pixie_wand (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe irons_spellbooks:alchemist_cauldron/empty_legendary_ink for irons_spellbooks:legendary_ink (mythic): Add boss, dragon, structure, or Guild-rank proof materials; keep disabled until reviewed.
// - Review recipe irons_spellbooks:create_compat/create_fill_legendary_ink for irons_spellbooks:legendary_ink (mythic): Add boss, dragon, structure, or Guild-rank proof materials; keep disabled until reviewed.
// - Review recipe irons_spellbooks:dead_king_phylactery for irons_spellbooks:dead_king_phylactery (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe irons_spellbooks:decrepit_scythe_repair for irons_spellbooks:hellrazor (legendary): Raise ingredients to match boss/dragon/rank tier or convert to loot-only progression.
// - Review recipe irons_spellbooks:dragonskin_spell_book for irons_spellbooks:dragonskin_spell_book (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe irons_spellbooks:infernal_sorcerer_chestplate for irons_spellbooks:infernal_sorcerer_chestplate (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe irons_spellbooks:netherite_mage_boots for irons_spellbooks:netherite_mage_boots (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe irons_spellbooks:netherite_mage_chestplate for irons_spellbooks:netherite_mage_chestplate (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe irons_spellbooks:netherite_mage_helmet for irons_spellbooks:netherite_mage_helmet (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe irons_spellbooks:netherite_mage_leggings for irons_spellbooks:netherite_mage_leggings (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe irons_spellbooks:netherite_spell_book for irons_spellbooks:netherite_spell_book (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe soulsweapons:chungus_staff for soulsweapons:chungus_staff (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
// - Review recipe soulsweapons:dragon_staff for soulsweapons:dragon_staff (legendary): Confirm JEI path matches Guild rank and Atlas ring before enabling changes.
