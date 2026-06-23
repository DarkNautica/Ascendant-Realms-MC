# Recipe Progression Audit

Generated: 2026-06-17T02:11:41+00:00

This audit scans active installed jar recipes plus repo OpenLoader/datapack recipes. It assigns each major output a rarity, Guild rank, Atlas ring, recipe tier, and review status. No active recipe rewrites are enabled by this pass.

## Summary

| Metric | Count |
| --- | --- |
| Recipe outputs audited | 8075 |
| Installed mod jar recipes | 7609 |
| Repo datapack/OpenLoader recipes | 18 |
| High-risk recipes | 109 |
| Candidate rewrites generated | 109 |
| Indexed gear/magic/relic policies | 1723 |

## Status Counts

| Status | Count |
| --- | --- |
| bypass | 28 |
| duplicate | 56 |
| needs_manual_review | 324 |
| okay | 7642 |
| too_cheap | 25 |

## Domain Counts

| Domain | Count |
| --- | --- |
| accessory_or_relic | 29 |
| armor_or_shield | 548 |
| create_component | 1414 |
| food_economy | 337 |
| general | 5084 |
| magic_or_spell | 100 |
| material | 239 |
| storage_qol | 81 |
| weapon | 243 |

## Recipe Assignment Preview

Only the first 350 rows are shown here; the complete machine-readable audit is in `config/ascendant_recipes/recipe_progression_policy.json`.

| Item ID | Recipe ID | Mod | Domain | Rarity | Guild Rank | Status |
| --- | --- | --- | --- | --- | --- | --- |
| farmersdelight:barbecue_stick | alexsdelight:barbecue_on_a_stick | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:bison_burger | alexsdelight:bison_burger | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:bunfungus_sandwich | alexsdelight:bunfungus_sandwich | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:acacia_blossom_soup | alexsdelight:cooking/acacia_blossom_soup | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:kangaroo_pasta | alexsdelight:cooking/kangaroo_pasta | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:kangaroo_stew | alexsdelight:cooking/kangaroo_stew | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:lobster_pasta | alexsdelight:cooking/lobster_pasta_recipe | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:gongylidia_bruschetta | alexsdelight:gongylidia_bruschetta | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:maggot_salad | alexsdelight:maggot_salad_recipe | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:maggot_salad | alexsdelight:maggot_salad_recipe_2 | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_bison | alexsdelight:smelting/bison_campfire | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_bison | alexsdelight:smelting/bison_cook | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:bison_patty | alexsdelight:smelting/bison_patty_campfire | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:bison_patty | alexsdelight:smelting/bison_patty_cook | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:bison_patty | alexsdelight:smelting/bison_patty_smoke | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_bison | alexsdelight:smelting/bison_smoke | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_bunfungus | alexsdelight:smelting/bunfungus_campfire | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_bunfungus | alexsdelight:smelting/bunfungus_cook | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_bunfungus_drumstick | alexsdelight:smelting/bunfungus_cook_drumstick | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_bunfungus_drumstick | alexsdelight:smelting/bunfungus_drumstick_campfire | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_bunfungus | alexsdelight:smelting/bunfungus_smoke | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_bunfungus_drumstick | alexsdelight:smelting/bunfungus_smoke_drumstick | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_catfish_slice | alexsdelight:smelting/catfish_slice_campfire | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_catfish_slice | alexsdelight:smelting/catfish_slice_cook | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_catfish_slice | alexsdelight:smelting/catfish_slice_smoke | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_centipede_leg | alexsdelight:smelting/centipede_leg_campfire | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_centipede_leg | alexsdelight:smelting/centipede_leg_cook | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_centipede_leg | alexsdelight:smelting/centipede_leg_smoke | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_kangaroo_shank | alexsdelight:smelting/kangaroo_shank_campfire | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_kangaroo_shank | alexsdelight:smelting/kangaroo_shank_cook | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_kangaroo_shank | alexsdelight:smelting/kangaroo_shank_smoke | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_loose_moose_rib | alexsdelight:smelting/singular_cooked_moose_rib_campfire | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_loose_moose_rib | alexsdelight:smelting/singular_cooked_moose_rib_cook | alexsdelight | food_economy | common | unranked | okay |
| alexsdelight:cooked_loose_moose_rib | alexsdelight:smelting/singular_cooked_moose_rib_smoke | alexsdelight | food_economy | common | unranked | okay |
| alexsmobs:kangaroo_burger | alexsmobs:kangaroo_burger | Alex's Mobs | food_economy | common | unranked | okay |
| alexsmobs:animal_dictionary | alexsmobs:animal_dictionary | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:banana_slug_slime | alexsmobs:banana_slug_slime | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:banana_slug_slime_block | alexsmobs:banana_slug_slime_block | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:banner_pattern_australia_0 | alexsmobs:banner_pattern_australia_0 | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:banner_pattern_australia_1 | alexsmobs:banner_pattern_australia_1 | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:banner_pattern_bear | alexsmobs:banner_pattern_bear | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:banner_pattern_brazil | alexsmobs:banner_pattern_brazil | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:banner_pattern_new_mexico | alexsmobs:banner_pattern_new_mexico | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:bison_carpet | alexsmobs:bison_carpet | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:bison_fur_block | alexsmobs:bison_fur_block | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:bison_fur | alexsmobs:bison_fur_from_block | Alex's Mobs | general | common | unranked | okay |
| minecraft:brown_wool | alexsmobs:bison_fur_to_wool | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:blood_sprayer | alexsmobs:blood_sprayer | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:boiled_emu_egg | alexsmobs:boiled_emu_egg | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:boiled_emu_egg | alexsmobs:boiled_emu_egg_campfire | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:boiled_emu_egg | alexsmobs:boiled_emu_egg_smoke | Alex's Mobs | general | common | unranked | okay |
| minecraft:bone_meal | alexsmobs:bonemeal_from_fish_bones | Alex's Mobs | food_economy | common | unranked | okay |
| alexsmobs:centipede_leggings | alexsmobs:centipede_leggings | Alex's Mobs | armor_or_shield | uncommon | e_rank | okay |
| alexsmobs:chorus_on_a_stick | alexsmobs:chorus_on_a_stick | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cockroach_wing | alexsmobs:cockroach_wing | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_catfish | alexsmobs:cooked_catfish | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_catfish | alexsmobs:cooked_catfish_campfire | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_catfish | alexsmobs:cooked_catfish_smoke | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_kangaroo_meat | alexsmobs:cooked_kangaroo_meat | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_kangaroo_meat | alexsmobs:cooked_kangaroo_meat_campfire | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_kangaroo_meat | alexsmobs:cooked_kangaroo_meat_smoke | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_lobster_tail | alexsmobs:cooked_lobster_tail | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_lobster_tail | alexsmobs:cooked_lobster_tail_campfire | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_lobster_tail | alexsmobs:cooked_lobster_tail_smoke | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_moose_ribs | alexsmobs:cooked_moose_ribs | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_moose_ribs | alexsmobs:cooked_moose_ribs_campfire | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:cooked_moose_ribs | alexsmobs:cooked_moose_ribs_smoke | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:crocodile_chestplate | alexsmobs:crocodile_chestplate | Alex's Mobs | armor_or_shield | uncommon | e_rank | okay |
| alexsmobs:dimensional_carver | alexsmobs:dimensional_carver | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:echolocator | alexsmobs:echolocator | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:emu_leggings | alexsmobs:emu_leggings | Alex's Mobs | armor_or_shield | uncommon | e_rank | okay |
| alexsmobs:enderiophage_rocket | alexsmobs:enderiophage_rocket | Alex's Mobs | general | rare | d_rank | okay |
| alexsmobs:endolocator | alexsmobs:endolocator | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:falconry_glove | alexsmobs:falconry_glove | Alex's Mobs | accessory_or_relic | rare | d_rank | okay |
| alexsmobs:falconry_hood | alexsmobs:falconry_hood | Alex's Mobs | armor_or_shield | uncommon | e_rank | okay |
| alexsmobs:falconry_hood | alexsmobs:falconry_hood_alt | Alex's Mobs | armor_or_shield | uncommon | e_rank | okay |
| alexsmobs:fish_oil | alexsmobs:fish_oil | Alex's Mobs | general | common | unranked | okay |
| minecraft:flint_and_steel | alexsmobs:flint_n_steel_dropbear_claw | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:flying_fish_boots | alexsmobs:flying_fish_boots | Alex's Mobs | armor_or_shield | uncommon | e_rank | okay |
| alexsmobs:frontier_cap | alexsmobs:frontier_cap | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:frontier_cap | alexsmobs:frontier_cap_alt | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:froststalker_helmet | alexsmobs:froststalker_helmet | Alex's Mobs | armor_or_shield | epic | c_rank_to_b_rank | needs_manual_review |
| alexsmobs:gustmaker | alexsmobs:gustmaker | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:hemolymph_blaster | alexsmobs:hemolymph_blaster | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:hummingbird_feeder | alexsmobs:hummingbird_feeder | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:kangaroo_burger | alexsmobs:kangaroo_burger | Alex's Mobs | food_economy | common | unranked | okay |
| minecraft:leather | alexsmobs:kangaroo_hide_to_leather | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:komodo_spit_bottle | alexsmobs:komodo_spit_bottle | Alex's Mobs | general | common | unranked | okay |
| minecraft:slime_ball | alexsmobs:komodo_spit_to_slime | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:maraca | alexsmobs:maraca | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:moose_headgear | alexsmobs:moose_headgear | Alex's Mobs | general | uncommon | e_rank | okay |
| alexsmobs:mosquito_larva | alexsmobs:mosquito_larva | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:mosquito_repellent_stew | alexsmobs:mosquito_repellent_stew | Alex's Mobs | food_economy | common | unranked | okay |
| alexsmobs:pocket_sand | alexsmobs:pocket_sand | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:pupfish_locator | alexsmobs:pupfish_locator | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:rainbow_glass | alexsmobs:rainbow_glass | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:roadrunner_boots | alexsmobs:roadrunner_boots | Alex's Mobs | armor_or_shield | uncommon | e_rank | okay |
| alexsmobs:rocky_chestplate | alexsmobs:rocky_chestplate | Alex's Mobs | armor_or_shield | uncommon | e_rank | okay |
| alexsmobs:sculk_boomer | alexsmobs:sculk_boomer | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:shark_tooth_arrow | alexsmobs:shark_tooth_arrow | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:shield_of_the_deep | alexsmobs:shield_of_the_deep | Alex's Mobs | armor_or_shield | uncommon | e_rank | okay |
| alexsmobs:sopa_de_macaco | alexsmobs:sopa_de_macaco | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:spiked_turtle_shell | alexsmobs:spiked_turtle_shell | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:squid_grapple | alexsmobs:squid_grapple | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:stink_ray | alexsmobs:stink_ray | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:straddle_helmet | alexsmobs:straddle_helmet | Alex's Mobs | armor_or_shield | uncommon | e_rank | okay |
| alexsmobs:straddle_saddle | alexsmobs:straddle_saddle | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:straddleboard | alexsmobs:straddleboard | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:straddlite_block | alexsmobs:straddlite_block | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:straddlite | alexsmobs:straddlite_from_block | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:tarantula_hawk_elytra | alexsmobs:tarantula_hawk_elytra | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:tarantula_hawk_wing | alexsmobs:tarantula_hawk_wing | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:tendon_whip | alexsmobs:tendon_whip | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:transmutation_table | alexsmobs:transmutation_table | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:vine_lasso | alexsmobs:vine_lasso | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:void_worm_beak | alexsmobs:void_worm_beak | Alex's Mobs | general | common | unranked | okay |
| alexsmobs:void_worm_effigy | alexsmobs:void_worm_effigy | Alex's Mobs | general | common | unranked | okay |
| amendments:dragon_charge | amendments:dragon_charge | amendments | general | common | unranked | okay |
| aquamirae:abyssal_amethyst | aquamirae:abyssal_amethyst | Aquamirae | general | common | unranked | okay |
| aquamirae:abyssal_boots | aquamirae:abyssal_boots | Aquamirae | armor_or_shield | uncommon | e_rank | okay |
| aquamirae:abyssal_brigantine | aquamirae:abyssal_brigantine | Aquamirae | general | common | unranked | okay |
| aquamirae:abyssal_heaume | aquamirae:abyssal_heaume | Aquamirae | general | common | unranked | okay |
| aquamirae:abyssal_leggings | aquamirae:abyssal_leggings | Aquamirae | armor_or_shield | uncommon | e_rank | okay |
| aquamirae:abyssal_tiara | aquamirae:abyssal_tiara | Aquamirae | general | common | unranked | okay |
| minecraft:bone_meal | aquamirae:bone_meal_from_anglers_fang | Aquamirae | food_economy | common | unranked | okay |
| minecraft:bone_meal | aquamirae:bone_meal_from_remnants_saber | Aquamirae | food_economy | common | unranked | okay |
| minecraft:bone_meal | aquamirae:bone_meal_from_sharp_bones | Aquamirae | food_economy | common | unranked | okay |
| aquamirae:cooked_spinefish | aquamirae:cooked_spinefish | Aquamirae | general | common | unranked | okay |
| aquamirae:cooked_spinefish | aquamirae:cooked_spinefish_from_campfire | Aquamirae | general | common | unranked | okay |
| aquamirae:cooked_spinefish | aquamirae:cooked_spinefish_from_smoking | Aquamirae | general | common | unranked | okay |
| minecraft:cyan_dye | aquamirae:cyan_dye_from_elodea | Aquamirae | general | common | unranked | okay |
| aquamirae:divider | aquamirae:divider | Aquamirae | general | common | unranked | okay |
| aquamirae:fin_cutter | aquamirae:fin_cutter | Aquamirae | general | common | unranked | okay |
| minecraft:green_dye | aquamirae:green_dye_from_wisteria | Aquamirae | general | common | unranked | okay |
| aquamirae:luminescent_bubble | aquamirae:luminescent_bubble | Aquamirae | general | common | unranked | okay |
| aquamirae:luminescent_lamp | aquamirae:luminescent_lamp | Aquamirae | general | common | unranked | okay |
| aquamirae:maze_rose | aquamirae:maze_rose | Aquamirae | general | common | unranked | okay |
| aquamirae:oxygen_tank | aquamirae:oxygen_tank | Aquamirae | general | common | unranked | okay |
| aquamirae:poisoned_blade | aquamirae:poisoned_blade | Aquamirae | weapon | uncommon | e_rank | okay |
| aquamirae:poisoned_chakra | aquamirae:poisoned_chakra | Aquamirae | weapon | uncommon | e_rank | okay |
| aquamirae:poseidons_breakfast | aquamirae:poseidons_breakfast | Aquamirae | general | common | unranked | okay |
| aquamirae:remnants_saber | aquamirae:remnants_saber | Aquamirae | weapon | uncommon | e_rank | okay |
| aquamirae:sea_casserole | aquamirae:sea_casserole | Aquamirae | general | common | unranked | okay |
| aquamirae:sea_stew | aquamirae:sea_stew | Aquamirae | food_economy | common | unranked | okay |
| minecraft:stick | aquamirae:stick_from_oxygelium | Aquamirae | general | common | unranked | okay |
| aquamirae:terrible_boots | aquamirae:terrible_boots | Aquamirae | armor_or_shield | uncommon | e_rank | okay |
| aquamirae:terrible_chestplate | aquamirae:terrible_chestplate | Aquamirae | armor_or_shield | uncommon | e_rank | okay |
| aquamirae:terrible_helmet | aquamirae:terrible_helmet | Aquamirae | armor_or_shield | uncommon | e_rank | okay |
| aquamirae:terrible_leggings | aquamirae:terrible_leggings | Aquamirae | armor_or_shield | uncommon | e_rank | okay |
| aquamirae:terrible_sword | aquamirae:terrible_sword | Aquamirae | weapon | uncommon | e_rank | okay |
| aquamirae:three_bolt_boots | aquamirae:three_bolt_boots | Aquamirae | armor_or_shield | uncommon | e_rank | okay |
| aquamirae:three_bolt_leggings | aquamirae:three_bolt_leggings | Aquamirae | armor_or_shield | uncommon | e_rank | okay |
| aquamirae:three_bolt_suit | aquamirae:three_bolt_suit | Aquamirae | general | common | unranked | okay |
| aquamirae:treasure_pouch | aquamirae:treasure_pouch | Aquamirae | accessory_or_relic | rare | d_rank | okay |
| aquamirae:whisper_of_the_abyss | aquamirae:whisper_of_the_abyss | Aquamirae | weapon | uncommon | e_rank | okay |
| artifacts:eternal_steak | artifacts:eternal_steak_campfire | Artifacts | accessory_or_relic | rare | d_rank | okay |
| artifacts:eternal_steak | artifacts:eternal_steak_furnace | Artifacts | accessory_or_relic | rare | d_rank | okay |
| artifacts:eternal_steak | artifacts:eternal_steak_smoker | Artifacts | accessory_or_relic | rare | d_rank | okay |
| block_factorys_bosses:big_chain | block_factorys_bosses:big_chain | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:cannonball | block_factorys_bosses:cannonball | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:coin_pile | block_factorys_bosses:coin_pile | Bosses'Rise | general | common | unranked | okay |
| minecraft:bone | block_factorys_bosses:corpse_to_bones | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:dragon_bones_boots | block_factorys_bosses:dragon_bones_boots | Bosses'Rise | armor_or_shield | mythic | a_rank_to_s_rank | needs_manual_review |
| block_factorys_bosses:dragon_bones_chestplate | block_factorys_bosses:dragon_bones_chestplate | Bosses'Rise | armor_or_shield | mythic | a_rank_to_s_rank | needs_manual_review |
| block_factorys_bosses:dragon_bones_leggings | block_factorys_bosses:dragon_bones_leggings | Bosses'Rise | armor_or_shield | mythic | a_rank_to_s_rank | needs_manual_review |
| block_factorys_bosses:kraken_trident | block_factorys_bosses:kraken_trident | Bosses'Rise | weapon | mythic | a_rank_to_s_rank | needs_manual_review |
| block_factorys_bosses:tall_candles_cross | block_factorys_bosses:lighting/candles_extra | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:ship_lantern | block_factorys_bosses:lighting/ship_lantern | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:candles | block_factorys_bosses:lighting/small_candles | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:under_world_tall_candle_cross | block_factorys_bosses:lighting/underworld_candles_extra | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:underwold_candles | block_factorys_bosses:lighting/underworld_small_candles | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:underwold_wall_torch | block_factorys_bosses:lighting/underworld_wall_torch | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:wall_torch | block_factorys_bosses:lighting/wall_torch | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:net | block_factorys_bosses:net | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:plank | block_factorys_bosses:plank/plank | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks | block_factorys_bosses:plank/plank_block | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_broken | block_factorys_bosses:plank/sawmill/oak_planks_broken | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_cracked | block_factorys_bosses:plank/sawmill/oak_planks_cracked | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_straight | block_factorys_bosses:plank/sawmill/oak_planks_straight | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_variation | block_factorys_bosses:plank/sawmill/oak_planks_variation | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_wet_broken | block_factorys_bosses:plank/sawmill/wet_oak_planks_broken | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_wet_cracked | block_factorys_bosses:plank/sawmill/wet_oak_planks_cracked | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_wet_straight | block_factorys_bosses:plank/sawmill/wet_oak_planks_straight | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_wet_variation | block_factorys_bosses:plank/sawmill/wet_oak_planks_variation | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_wet | block_factorys_bosses:plank/wet_plank_block | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_wet_broken | block_factorys_bosses:plank/wet_plank_block_broken | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_wet_cracked | block_factorys_bosses:plank/wet_plank_block_cracked | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_wet_straight | block_factorys_bosses:plank/wet_plank_block_straight | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:big_oak_planks_wet_variation | block_factorys_bosses:plank/wet_plank_block_variation | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:prison_door | block_factorys_bosses:prison_door | Bosses'Rise | general | common | unranked | okay |
| minecraft:bone | block_factorys_bosses:remains_to_bones | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:rope_roll | block_factorys_bosses:rope_roll | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:rusty_prison_door | block_factorys_bosses:rusty_prison_door | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:guardrail | block_factorys_bosses:ship_rail | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:tall_candles | block_factorys_bosses:tall_candles | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:underworld_tall_candles | block_factorys_bosses:underworld_tall_candles | Bosses'Rise | general | common | unranked | okay |
| block_factorys_bosses:undying_tentacle | block_factorys_bosses:undying_tentacle | Bosses'Rise | general | common | unranked | okay |
| born_in_chaos_v1:argillite_lamp | born_in_chaos_v1:argillite_lamp_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:armor_plate_from_dark_metal | born_in_chaos_v1:armor_plate_from_dark_metal_k | Born in Chaos  | armor_or_shield | uncommon | e_rank | okay |
| born_in_chaos_v1:dark_metal_armor_helmet | born_in_chaos_v1:armor_plate_from_dark_metal_k_2 | Born in Chaos  | armor_or_shield | uncommon | e_rank | okay |
| born_in_chaos_v1:dark_metal_armor_chestplate | born_in_chaos_v1:armor_plate_from_dark_metal_k_3 | Born in Chaos  | armor_or_shield | uncommon | e_rank | okay |
| born_in_chaos_v1:dark_metal_armor_leggings | born_in_chaos_v1:armor_plate_from_dark_metal_k_4 | Born in Chaos  | armor_or_shield | uncommon | e_rank | okay |
| born_in_chaos_v1:dark_metal_armor_boots | born_in_chaos_v1:armor_plate_from_dark_metal_k_5 | Born in Chaos  | armor_or_shield | uncommon | e_rank | okay |
| born_in_chaos_v1:black_argillite | born_in_chaos_v1:black_argilite_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_brick | born_in_chaos_v1:black_argillite_brick_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_brick_stairs | born_in_chaos_v1:black_argillite_brick_st_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_brick_wall | born_in_chaos_v1:black_argillite_brick_wall_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_brick_wall | born_in_chaos_v1:black_argillite_brick_wall_k_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_brick_wall | born_in_chaos_v1:black_argillite_brick_wall_k_3 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_button | born_in_chaos_v1:black_argillite_button_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_column | born_in_chaos_v1:black_argillite_column_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_column | born_in_chaos_v1:black_argillite_column_k_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_column_slab | born_in_chaos_v1:black_argillite_column_slab_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_column_slab | born_in_chaos_v1:black_argillite_column_slab_k_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillitepressureplate | born_in_chaos_v1:black_argillite_pressure_plate_k | Born in Chaos  | create_component | rare | d_rank | okay |
| born_in_chaos_v1:black_argillite_stairs | born_in_chaos_v1:black_argillite_sk | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_stairs | born_in_chaos_v1:black_argillite_sk_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_slab | born_in_chaos_v1:black_argillite_sl_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_slab | born_in_chaos_v1:black_argillite_sl_k_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_wall | born_in_chaos_v1:black_argillite_wk | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_wall | born_in_chaos_v1:black_argillite_wk_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_brick_slab | born_in_chaos_v1:blackargillitebrickslk | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_brick_slab | born_in_chaos_v1:blackargillitebrickslk_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_brick_stairs | born_in_chaos_v1:blackargillitebrickstk_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_column_slab | born_in_chaos_v1:blackargillitecolumnslabk_3 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:bone_handle | born_in_chaos_v1:bone_handle_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:bone_heart | born_in_chaos_v1:bone_heart_k | Born in Chaos  | general | common | unranked | okay |
| minecraft:bone | born_in_chaos_v1:bundleof_bones_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:bundle_of_bones | born_in_chaos_v1:bundleof_bones_l | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:carrot_sword | born_in_chaos_v1:carrotsword_craft | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| born_in_chaos_v1:carved_black_argillite | born_in_chaos_v1:carved_black_argillite_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:chipped_black_argillite_brick | born_in_chaos_v1:chipped_black_argillite_brick_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:chipped_black_argillite_brick | born_in_chaos_v1:chipped_black_argillite_brick_k_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:chipped_black_argillite_brick | born_in_chaos_v1:chipped_black_argillite_brick_k_3 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:cobweb_cover | born_in_chaos_v1:cobwebcover_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:creepy_cookies_with_milk | born_in_chaos_v1:creepy_cookies_with_milk_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:creepy_nutcracker | born_in_chaos_v1:creepy_nutcracker_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:spooky_snowman_head | born_in_chaos_v1:creepy_snowman_head_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:cultivated_pumpkin | born_in_chaos_v1:cultivated_pumpkin_k | Born in Chaos  | general | common | unranked | okay |
| minecraft:pumpkin_seeds | born_in_chaos_v1:cultivated_pumpkink_2 | Born in Chaos  | general | common | unranked | okay |
| minecraft:pumpkin_pie | born_in_chaos_v1:cultivated_pumpkink_3 | Born in Chaos  | food_economy | common | unranked | okay |
| born_in_chaos_v1:dark_atrium | born_in_chaos_v1:dark_atrium_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:dark_grid | born_in_chaos_v1:dark_grid_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:dark_metal_block | born_in_chaos_v1:dark_metal_block_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:dark_metal_nugget | born_in_chaos_v1:dark_metal_nugget_craft | Born in Chaos  | material | common | unranked | okay |
| born_in_chaos_v1:dark_metal_ingot | born_in_chaos_v1:dark_metal_nugget_craft_2 | Born in Chaos  | material | common | unranked | okay |
| born_in_chaos_v1:dark_metal_nugget | born_in_chaos_v1:dark_metal_nugget_craft_4 | Born in Chaos  | material | common | unranked | okay |
| born_in_chaos_v1:dark_metal_ingot | born_in_chaos_v1:dark_metalngot_k | Born in Chaos  | material | common | unranked | okay |
| born_in_chaos_v1:dark_ritual_dagger | born_in_chaos_v1:dark_ritual_dagger_k | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| born_in_chaos_v1:dark_stained_glass | born_in_chaos_v1:dark_stained_glass_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:dark_stained_glass_panel | born_in_chaos_v1:dark_stained_glass_panel_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:dark_charge | born_in_chaos_v1:darkcharge_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:dark_metal_ingot | born_in_chaos_v1:darkmetalblockk_2 | Born in Chaos  | material | common | unranked | okay |
| born_in_chaos_v1:dark_upgrade | born_in_chaos_v1:darkupgradek | Born in Chaos  | storage_qol | common | unranked | okay |
| born_in_chaos_v1:death_totem | born_in_chaos_v1:death_totem_k | Born in Chaos  | general | legendary | b_rank_to_a_rank | too_cheap |
| minecraft:diamond | born_in_chaos_v1:diamond_thermite_shard_k | Born in Chaos  | general | epic | c_rank_to_b_rank | okay |
| born_in_chaos_v1:eternal_candy | born_in_chaos_v1:eternalcandy_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:evilometer | born_in_chaos_v1:evilometer_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:fel_lamp | born_in_chaos_v1:fel_lamp_k | Born in Chaos  | general | common | unranked | okay |
| minecraft:torch | born_in_chaos_v1:fire_dust_k_1 | Born in Chaos  | general | common | unranked | okay |
| minecraft:soul_torch | born_in_chaos_v1:fire_dust_k_2 | Born in Chaos  | general | common | unranked | okay |
| minecraft:soul_torch | born_in_chaos_v1:fire_dust_k_3 | Born in Chaos  | general | common | unranked | okay |
| minecraft:campfire | born_in_chaos_v1:fire_dust_k_4 | Born in Chaos  | general | common | unranked | okay |
| minecraft:fire_charge | born_in_chaos_v1:fire_light_dust_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:fired_black_argillite | born_in_chaos_v1:fired_black_argillite_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_brick | born_in_chaos_v1:fired_black_argillite_k_1 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_brick_stairs | born_in_chaos_v1:fired_black_argillite_k_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:black_argillite_brick_slab | born_in_chaos_v1:fired_black_argillite_k_3 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:flaming_evil_pumpkin | born_in_chaos_v1:flaming_evil_pumpkin_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:fried_maggot | born_in_chaos_v1:fried_maggot_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:fried_maggot | born_in_chaos_v1:fried_maggot_k_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:fried_maggot | born_in_chaos_v1:fried_maggot_k_3 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:frostbitten_blade | born_in_chaos_v1:frostbitten_blade_craft | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| minecraft:bone_meal | born_in_chaos_v1:fused_bone_k | Born in Chaos  | food_economy | common | unranked | okay |
| minecraft:bone | born_in_chaos_v1:gnawed_bones_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:darkwarblade | born_in_chaos_v1:great_dark_crusher_k | Born in Chaos  | weapon | legendary | b_rank_to_a_rank | too_cheap |
| born_in_chaos_v1:great_reaper_axe | born_in_chaos_v1:great_reaper_ax_k | Born in Chaos  | weapon | legendary | b_rank_to_a_rank | too_cheap |
| born_in_chaos_v1:green_stained_glass | born_in_chaos_v1:green_stained_glass_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:green_stained_glass_panel | born_in_chaos_v1:green_stained_glass_panel_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:hound_trap | born_in_chaos_v1:houndtrapk | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:icy_sweetness | born_in_chaos_v1:icy_sweetness_craft | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| born_in_chaos_v1:infernal_evil_pumpkin | born_in_chaos_v1:infernal_evil_pumpkin_k_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:infernal_evil_pumpkin | born_in_chaos_v1:infernal_evil_pumpkink | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:intoxicatind_bomb | born_in_chaos_v1:intoxicatind_bomb_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:intoxicating_dagger | born_in_chaos_v1:intoxicating_dagger_k | Born in Chaos  | weapon | legendary | b_rank_to_a_rank | too_cheap |
| born_in_chaos_v1:lord_pumpkinheads_lamp | born_in_chaos_v1:lordpumpkinheadslampk | Born in Chaos  | general | common | unranked | okay |
| minecraft:orange_dye | born_in_chaos_v1:marigolds_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:mint_candy | born_in_chaos_v1:mint_candy_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:mint_ice_cream | born_in_chaos_v1:minticecream_k | Born in Chaos  | general | common | unranked | okay |
| minecraft:leather | born_in_chaos_v1:monster_skin_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:mossy_black_argillite_brick | born_in_chaos_v1:mossy_black_argillite_brick_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:nightmare_mantleofthe_night_boots | born_in_chaos_v1:nightmare_boots_k | Born in Chaos  | armor_or_shield | uncommon | e_rank | okay |
| born_in_chaos_v1:nightmare_mantleofthe_night_helmet | born_in_chaos_v1:nightmare_mask_k | Born in Chaos  | armor_or_shield | uncommon | e_rank | okay |
| born_in_chaos_v1:nightmare_mantleofthe_night_leggings | born_in_chaos_v1:nightmare_pantsk | Born in Chaos  | armor_or_shield | uncommon | e_rank | okay |
| born_in_chaos_v1:nightmare_mantleofthe_night_chestplate | born_in_chaos_v1:nightmare_robe_k | Born in Chaos  | armor_or_shield | uncommon | e_rank | okay |
| born_in_chaos_v1:nightmare_scythe | born_in_chaos_v1:nightmare_scythe_k | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| minecraft:bone_meal | born_in_chaos_v1:nightmarestalkerskullk | Born in Chaos  | food_economy | common | unranked | okay |
| born_in_chaos_v1:nut_hammer | born_in_chaos_v1:nut_hammer_craft | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| born_in_chaos_v1:orange_stained_glass | born_in_chaos_v1:orange_stained_glass_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:orange_stained_glass_panel | born_in_chaos_v1:orange_stained_glass_panel_k | Born in Chaos  | general | common | unranked | okay |
| minecraft:blue_ice | born_in_chaos_v1:permafrost_shard_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:phantom_bomb | born_in_chaos_v1:phantom_bomb_k | Born in Chaos  | general | common | unranked | okay |
| minecraft:gunpowder | born_in_chaos_v1:phantom_powder_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:pileof_dark_metal | born_in_chaos_v1:pileof_dark_metal_d | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:pieceofdarkmetal | born_in_chaos_v1:pileof_dark_metal_k_2 | Born in Chaos  | food_economy | common | unranked | okay |
| born_in_chaos_v1:pile_of_skulls | born_in_chaos_v1:pileof_skulls_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:shattered_skull | born_in_chaos_v1:pileof_skulls_k_2 | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:pumpkin_bullet | born_in_chaos_v1:pumpkin_bullet_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:purple_stained_glass | born_in_chaos_v1:purple_stained_glass_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:purple_stained_glass_panel | born_in_chaos_v1:purple_stained_glass_panel_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:rotten_soil | born_in_chaos_v1:rotten_soil_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:rotten_infernal_pumpkin | born_in_chaos_v1:rotteninfernalpumpkin_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scarlet_stained_glass | born_in_chaos_v1:scarlet_stained_glass_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scarlet_stained_glass_panel | born_in_chaos_v1:scarlet_stained_glass_panel_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scorched_log | born_in_chaos_v1:scorched_log_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scorched_planks_button | born_in_chaos_v1:scorched_planks_button_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scorched_planks_door | born_in_chaos_v1:scorched_planks_door_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scorched_planks_fence_gate | born_in_chaos_v1:scorched_planks_fence_gate_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scorched_planks_fence | born_in_chaos_v1:scorched_planks_fence_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scorched_planks | born_in_chaos_v1:scorched_planks_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scorched_planks_pressure_plates | born_in_chaos_v1:scorched_planks_pressure_plates_k | Born in Chaos  | create_component | rare | d_rank | okay |
| born_in_chaos_v1:scorched_planks_slab | born_in_chaos_v1:scorched_planks_slab_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scorched_planks_stairs | born_in_chaos_v1:scorched_planks_stairs_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scorched_planks_trapdoor | born_in_chaos_v1:scorched_planks_trapdoor_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:scorched_wood | born_in_chaos_v1:scorched_wood_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:staff_of_magic_arrows | born_in_chaos_v1:seedof_chaos_k_1 | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| born_in_chaos_v1:sharpened_dark_metal_sword | born_in_chaos_v1:sharpened_darketal_sword_k | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| minecraft:bone_meal | born_in_chaos_v1:shattered_skull_k_1 | Born in Chaos  | food_economy | common | unranked | okay |
| born_in_chaos_v1:shell_mace | born_in_chaos_v1:shellmace_k | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| born_in_chaos_v1:skullbreaker_hammer | born_in_chaos_v1:skull_crusher_k | Born in Chaos  | weapon | legendary | b_rank_to_a_rank | too_cheap |
| born_in_chaos_v1:smoked_flesh | born_in_chaos_v1:smoked_flesh_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:smoked_monster_flesh | born_in_chaos_v1:smoked_monster_flesh_k | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| born_in_chaos_v1:smoked_monster_flesh | born_in_chaos_v1:smoked_monster_flesh_k_2 | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| born_in_chaos_v1:smoked_fish | born_in_chaos_v1:smokedfish_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:fel_soil | born_in_chaos_v1:smoldering_infernal_ember_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:smoldering_scorched_log | born_in_chaos_v1:smoldering_scorche_log_k | Born in Chaos  | accessory_or_relic | rare | d_rank | okay |
| born_in_chaos_v1:smoldering_scorched_wood | born_in_chaos_v1:smoldering_scorched_wood_k | Born in Chaos  | accessory_or_relic | rare | d_rank | okay |
| minecraft:soul_sand | born_in_chaos_v1:solsendk | Born in Chaos  | general | common | unranked | okay |
| minecraft:soul_soil | born_in_chaos_v1:solsoil_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:soul_cutlass | born_in_chaos_v1:soul_saber_k | Born in Chaos  | weapon | mythic | a_rank_to_s_rank | too_cheap |
| born_in_chaos_v1:spider_bite_sword | born_in_chaos_v1:spider_bite_craft | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| born_in_chaos_v1:spiny_shell_armor_chestplate | born_in_chaos_v1:spiny_shell_chestplate_k | Born in Chaos  | armor_or_shield | uncommon | e_rank | okay |
| born_in_chaos_v1:spiny_shell_armor_helmet | born_in_chaos_v1:spiny_shell_helm_k | Born in Chaos  | armor_or_shield | uncommon | e_rank | okay |
| born_in_chaos_v1:spiny_shell_trap | born_in_chaos_v1:spinyshelltrap_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:spiritual_sword | born_in_chaos_v1:spiritual_divider_k | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| born_in_chaos_v1:spiritual_dust | born_in_chaos_v1:spiritual_dust_k | Born in Chaos  | material | common | unranked | okay |
| born_in_chaos_v1:spiritual_gingerbread | born_in_chaos_v1:spiritual_gingerbread_craft | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:bonescaller_staff | born_in_chaos_v1:staffofthe_summoner_k | Born in Chaos  | weapon | epic | c_rank_to_b_rank | needs_manual_review |
| born_in_chaos_v1:stained_black_argillite_brick | born_in_chaos_v1:stained_black_argillite_brick_k | Born in Chaos  | general | common | unranked | okay |
| born_in_chaos_v1:stimulating_bomb | born_in_chaos_v1:stimulating_bomb_k | Born in Chaos  | general | common | unranked | okay |
