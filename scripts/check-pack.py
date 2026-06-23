#!/usr/bin/env python3
"""Validate the Ascendant Realms planning repo."""

from __future__ import annotations

import pathlib
import re
import sys
import json
import subprocess
import zipfile
import hashlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
ACTIVE_CURSEFORGE_INSTANCE = pathlib.Path(r"C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)")

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "docs/MOD_CANDIDATES.md",
    "docs/COMPATIBILITY_MATRIX.md",
    "docs/DEPENDENCY_GRAPH.md",
    "docs/VERSION_AND_LOADER_DECISION.md",
    "docs/VISUAL_SHADER_PLAN.md",
    "docs/AI_MODPACK_HANDOFF.md",
    "docs/DOCUMENTATION_CLEANUP_REPORT.md",
    "docs/archive/BATCH_HISTORY.md",
    "docs/WORLDGEN_AND_STRUCTURES.md",
    "docs/WORLDGEN_CONTENT_AUDIT.md",
    "docs/generated/worldgen_content_audit.json",
    "docs/RPG_COMBAT_AND_CLASSES.md",
    "docs/MOBS_BOSSES_AND_DIFFICULTY.md",
    "docs/LOOT_BALANCE_AND_PROGRESSION.md",
    "docs/IDENTITY_AND_TITLES.md",
    "docs/ENEMY_THREAT_UI.md",
    "docs/HUD_AND_PROGRESSION_UI.md",
    "docs/WEATHER_AND_ATMOSPHERE.md",
    "docs/SPAWN_ECOLOGY_PLAN.md",
    "docs/PROGRESSIVE_DIFFICULTY_TUNING.md",
    "docs/ELITE_MOB_TUNING.md",
    "docs/FIRST_PERSON_AND_ANIMATIONS.md",
    "docs/SOUND_AND_MUSIC.md",
    "docs/COHESION_AND_INTEGRATION.md",
    "docs/RECIPE_AND_TAG_UNIFICATION.md",
    "docs/FOOD_AND_HUNTING_INTEGRATION.md",
    "docs/CREATE_AND_FARMERS_DELIGHT_INTEGRATION.md",
    "docs/VILLAGE_AND_CITY_INTEGRATION.md",
    "docs/DUNGEON_AND_LOOT_INTEGRATION.md",
    "docs/ASCENDANT_RANKED_DUNGEONS.md",
    "docs/DUNGEON_PORTAL_SYSTEM.md",
    "docs/ASCENDANT_DUNGEON_HOLOGRAMS.md",
    "docs/ASCENDANT_DUNGEON_DIMENSIONS.md",
    "docs/WORLD_INTEGRATION_AUDIT.md",
    "docs/SYSTEM_ECOSYSTEM_OVERVIEW.md",
    "docs/MAIN_MENU_POLISH.md",
    "docs/UI_CUSTOMIZATION_TOOLING.md",
    "docs/GUILD_HUNTER_SYSTEM_RUNDOWN.md",
    "docs/GUILD_HUNTER_IMPLEMENTATION_STATUS.md",
    "docs/NPC_EQUIPMENT_AND_VISUAL_IDENTITY.md",
    "docs/NPC_VISUAL_VALIDATION_REPORT.md",
    "docs/MCA_MEDIEVAL_SKIN_AUDIT.md",
    "docs/RIVAL_HUNTER_VISUAL_ROSTER.md",
    "docs/UI_CLARITY_AND_FEEDBACK_AUDIT.md",
    "docs/RARITY_TOOLTIP_VISUAL_POLICY.md",
    "docs/MOB_DANGER_UI_POLICY.md",
    "docs/REGION_TITLE_UI_POLICY.md",
    "docs/KEYBIND_REEVALUATION.md",
    "docs/MAGIC_UI_SKILL_HANDOFF.md",
    "docs/ASCENDANT_SETTLEMENTS_UNIFICATION.md",
    "docs/ASCENDANT_NAMEPLATES.md",
    "docs/CUSTOM_NPC_TEST_PLAN.md",
    "docs/MCA_REBORN_MEDIEVAL_VALIDATION.md",
    "docs/CUSTOM_INTEGRATION_PLAN.md",
    "docs/ASCENDANT_CORE_INTEGRATION.md",
    "docs/BATCH_INSTALL_PLAN.md",
    "docs/REJECTED_OR_DELAYED_MODS.md",
    "docs/TESTING_CHECKLIST.md",
    "docs/SERVER_SETUP.md",
    "docs/KNOWN_RISKS.md",
    "docs/STRUCTURE_DENSITY_TUNING.md",
    "docs/DANGER_SPAWN_TUNING.md",
    "docs/DRAGON_AND_BOSS_TUNING.md",
    "docs/SKILL_TREE_DESIGN.md",
    "docs/SKILL_TREE_IMPLEMENTATION_PLAN.md",
    "docs/SKILL_TREE_ATTRIBUTE_MAPPING.md",
    "docs/SKILL_TREE_BALANCE_NOTES.md",
    "docs/SKILL_TREE_TESTING.md",
    "docs/SKILL_TREE_INTEGRATION_HOOKS.md",
    "docs/UNIVERSAL_MOD_INDEX.md",
    "docs/UNIVERSAL_RARITY_AND_INTEGRATION.md",
    "docs/MOB_THREAT_INDEX.md",
    "docs/STRUCTURE_INDEX.md",
    "docs/BOUNTY_TARGET_INDEX.md",
    "docs/BOUNTY_POOL_WORKLIST.md",
    "docs/SKILL_HOOK_REGISTRY.md",
    "docs/SPAWN_TUNING_WORKLIST.md",
    "docs/ASCENDANT_INTEGRATION_MATRIX.md",
    "docs/WEAPON_INDEX.md",
    "docs/ARMOR_INDEX.md",
    "docs/SHIELD_INDEX.md",
    "docs/MAGIC_INDEX.md",
    "docs/ACCESSORY_RELIC_INDEX.md",
    "docs/CUSTOM_HERO_SYSTEM_AUTOMATION.md",
    "docs/ASCENDANT_REALMS_SEAMLESS_INTEGRATION_MASTER_PLAN.md",
    "docs/GENERATED_NPC_SYSTEM.md",
    "docs/ASCENDANT_GUILD_WORLDGEN.md",
    "docs/ASCENDANT_ATLAS_WORLDGEN.md",
    "docs/ATLAS_RANDOM_WORLDGEN_RESTORE.md",
    "docs/MATERIAL_UNIFICATION.md",
    "docs/ORE_AND_WORLDGEN_CONTROL.md",
    "docs/RECIPE_PROGRESSION.md",
    "docs/LOOT_TABLE_CONTROL.md",
    "docs/ASCENDANT_LOOT_ECONOMY.md",
    "docs/LOOT_TABLE_AUDIT.md",
    "docs/STRUCTURE_REWARD_TIER_INDEX.md",
    "docs/RECIPE_PROGRESSION_AUDIT.md",
    "docs/CRAFTING_GATE_PLAN.md",
    "docs/BROKEN_OR_EASY_RECIPE_REPORT.md",
    "docs/ASCENDANT_STRUCTURE_TIERING.md",
    "docs/STRUCTURE_DENSITY_AND_REGION_AUDIT.md",
    "docs/STRUCTURE_CONFLICTS_AND_OVERLAPS.md",
    "docs/ASCENDANT_STRUCTURE_DIRECTOR.md",
    "docs/STRUCTURE_REGION_AND_LAYER_INDEX.md",
    "docs/STRUCTURE_DENSITY_IMPLEMENTATION_REPORT.md",
    "docs/WATER_AND_SKY_STRUCTURES.md",
    "docs/STRUCTURE_LOOT_AND_DANGER_TIERS.md",
    "docs/STRUCTURE_TESTING_CHECKLIST.md",
    "docs/STRUCTURE_VISUAL_REVIEW_ROUTE.md",
    "docs/STRUCTURE_DIRECTOR_REVIEW_RESULTS_TEMPLATE.md",
    "docs/STRUCTURE_VISUAL_REVIEW_FINDINGS.md",
    "docs/ASCENDANT_TRAVEL_NETWORK_AUDIT.md",
    "docs/STRUCTURE_DIRECTOR_LIVE_V1.md",
    "docs/STRUCTURE_DIRECTOR_LIVE_CHANGELOG.md",
    "docs/STRUCTURE_DIRECTOR_ROLLBACK.md",
    "docs/STRUCTURE_DIRECTOR_LIVE_V1_TESTING.md",
    "docs/ROAD_BRIDGE_RIVER_FAILURES.md",
    "docs/TRAVEL_NETWORK_DESIGN_RULES.md",
    "docs/ASCENDANT_REGIONAL_ATMOSPHERE.md",
    "docs/WEATHER_AND_SEASON_REGION_POLICY.md",
    "docs/BIOME_TITLE_AND_AUDIO_POLICY.md",
    "docs/ASCENDANT_MAGIC_PROGRESSION.md",
    "docs/SPELL_REGION_AND_RANK_INDEX.md",
    "docs/MAGIC_LOOT_AND_RECIPE_AUDIT.md",
    "docs/GEAR_BALANCE_OUTLIER_REPORT.md",
    "docs/RARITY_CONSISTENCY_AUDIT.md",
    "docs/GEAR_PROGRESSion_RISK_REGISTER.md",
    "docs/ASCENDANT_PLAYER_PROGRESSION.md",
    "docs/GUILD_RANK_REQUIREMENT_MATRIX.md",
    "docs/SKILL_TREE_INTEGRATION_PLAN.md",
    "docs/MOB_SPAWN_AND_DROP_CONTROL.md",
    "docs/MOB_SPAWN_DENSITY_PASS.md",
    "docs/HOSTILE_DAY_SPAWN_PASS.md",
    "docs/OVERWORLD_MOB_SPAWN_COVERAGE.md",
    "docs/BOUNTIFUL_GUILD_CONTRACTS.md",
    "pack.toml",
    "index.toml",
    "options.txt",
    "config/resourcepackoverrides.json",
    "config/Weather2/Snow.toml",
    "config/snowrealmagic-common.yaml",
    "config/sereneseasons/seasons.toml",
    "config/ascendant_core/spawn_density_policy.json",
    "config/ascendant_core/reports/overworld_mob_spawn_coverage_latest.json",
    "config/ascendant_dungeons/ranked_dungeon_policy.json",
    "config/ascendant_dungeons/dungeon_rank_registry.json",
    "config/ascendant_dungeons/dungeon_portal_policy.json",
    "config/ascendant_dungeons/dungeon_hologram_policy.json",
    "config/ascendant_dungeons/dungeon_spawn_policy.json",
    "config/ascendant_dungeons/dungeon_instance_templates.json",
    "config/ascendant_dungeons/dungeon_dimension_policy.json",
    "config/incontrol/spawner.json",
    ".packwizignore",
    "scripts/refresh-pack.ps1",
    "scripts/export-client-pack.ps1",
    "scripts/export-server-pack.ps1",
    "scripts/materialize-server-mods-from-client.ps1",
    "scripts/check-custom-hero-system.ps1",
    "scripts/sync-active-client-files.ps1",
    "scripts/update-fancymenu-status-assets.ps1",
    "scripts/generate-guild-hunter-data.js",
    "scripts/generate-ascendant-content-registries.ps1",
    "scripts/generate-ascendant-guild-worldgen.py",
    "scripts/generate-ascendant-atlas.py",
    "scripts/generate-ascendant-atlas-worldgen.py",
    "scripts/generate-ascendant-structure-review-route.py",
    "scripts/generate-ascendant-travel-network.py",
    "scripts/generate-ascendant-atmosphere.py",
    "scripts/generate-ascendant-magic-progression.py",
    "scripts/generate-ascendant-gear-balance.py",
    "scripts/generate-ascendant-player-progression.py",
    "scripts/generate-ascendant-npc-visuals.py",
    "scripts/generate-ascendant-ui-clarity.py",
    "scripts/generate-ai-modpack-handoff.py",
    "scripts/audit-worldgen-content.py",
    "scripts/audit-overworld-mob-spawn-coverage.py",
    "scripts/build-ascendant-atlas-regions.ps1",
    "scripts/build-ascendant-nametags.ps1",
    "scripts/generate-structure-director-live-v1.py",
    "scripts/disable-structure-director-live-v1.ps1",
    "scripts/enable-structure-director-live-v1.ps1",
    "scripts/verify-structure-director-live-v1.ps1",
    "scripts/test-customnpcs-identity.js",
    "scripts/customnpcs-identity-audit.py",
    "customnpcs/pack.mcmeta",
    "customnpcs/assets/customnpcs/sounds.json",
    "config/README.md",
    "config/fancymenu/README.md",
    "config/fancymenu/customization/custom_title_screen_layout.txt",
    "config/fancymenu/video_element_controller_metas.json",
    "config/fancymenu/options.txt",
    "config/fancymenu/customizablemenus.txt",
    "config/fancymenu/custom_gui_screens.txt",
    "config/fancymenu/assets/ascendant_realms_title.png",
    "config/fancymenu/assets/minecraft_title.png",
    "config/fancymenu/assets/ascendant_level_bar_spritesheet.png",
    "kubejs/assets/kubejs/textures/gui/ascendant_level_bar_spritesheet.png",
    "config/openloader/README.md",
    "config/openloader/advanced_options.json",
    "config/openloader/data/ascendant_realms_world_integration/pack.mcmeta",
    "config/openloader/data/ascendant_realms_world_integration/data/integrated_villages/tags/worldgen/biome/has_structure/airship_village_biomes.json",
    "config/openloader/data/ascendant_realms_world_integration/data/integrated_villages/tags/worldgen/biome/has_structure/mossy_mounds_biomes.json",
    "config/openloader/data/ascendant_realms_world_integration/data/integrated_villages/tags/worldgen/biome/has_structure/marketstead_village_biomes.json",
    "config/openloader/data/ascendant_realms_world_integration/data/integrated_villages/tags/worldgen/structure/villages.json",
    "config/openloader/data/ascendant_realms_world_integration/data/integrated_villages/worldgen/structure_set/air_villages.json",
    "config/openloader/data/ascendant_realms_world_integration/data/integrated_villages/worldgen/structure_set/regular_villages.json",
    "config/openloader/data/ascendant_realms_world_integration/data/aquamirae/worldgen/structure_set/surface.json",
    "config/openloader/data/ascendant_realms_world_integration/data/minecraft/tags/worldgen/structure/village.json",
    "config/openloader/data/ascendant_realms_identity/pack.mcmeta",
    "config/openloader/data/ascendant_realms_identity/data/minecraft/tags/functions/load.json",
    "config/openloader/data/ascendant_realms_identity/data/minecraft/tags/functions/tick.json",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/load.mcfunction",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/tick.mcfunction",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/level_up.mcfunction",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/npc_test/kit.mcfunction",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/npc_test/fix_rank_examiner.mcfunction",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank/unranked.mcfunction",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank/e_rank.mcfunction",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank/d_rank.mcfunction",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank/c_rank.mcfunction",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank/b_rank.mcfunction",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank/a_rank.mcfunction",
    "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank/s_rank.mcfunction",
    "config/openloader/data/ascendant_realms_codex/pack.mcmeta",
    "config/openloader/data/ascendant_realms_codex/data/ascendant_realms/patchouli_books/ascendant_codex/book.json",
    "config/openloader/data/ascendant_realms_guild/pack.mcmeta",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/functions/npc/list.mcfunction",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/functions/npc/spawn_set/starter_guild_staff.mcfunction",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/functions/npc/spawn_set/roadside_rumor_camp.mcfunction",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/functions/npc/spawn_set/frontier_guild_outpost.mcfunction",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/structures/guild/hunter_board_village_standard.nbt",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/structures/guild/roadside_hunter_camp.nbt",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/structures/guild/frontier_guild_outpost.nbt",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/worldgen/structure/hunter_board_village_standard.json",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/worldgen/structure/roadside_hunter_camp.json",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/worldgen/structure/frontier_guild_outpost.json",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/worldgen/structure_set/hunter_board_village_standard.json",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/worldgen/structure_set/roadside_hunter_camp.json",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/worldgen/structure_set/frontier_guild_outpost.json",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/worldgen/template_pool/guild/hunter_board_village_standard.json",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/worldgen/template_pool/guild/roadside_hunter_camp.json",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/worldgen/template_pool/guild/frontier_guild_outpost.json",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/loot_tables/chests/village_hunter_board.json",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/loot_tables/chests/roadside_hunter_camp.json",
    "config/openloader/data/ascendant_realms_guild/data/ascendant_guild/loot_tables/chests/frontier_guild_outpost.json",
    "config/openloader/data/ascendant_realms_guild/data/bountiful/bounty_decrees/ascendant_guild/village_hunter_board.json",
    "config/openloader/data/ascendant_realms_guild/data/bountiful/bounty_decrees/ascendant_guild/town_guild_board.json",
    "config/openloader/data/ascendant_realms_guild/data/bountiful/bounty_decrees/ascendant_guild/major_guild_registry.json",
    "config/openloader/data/ascendant_realms_guild/data/bountiful/bounty_pools/ascendant_guild/ar_village_hunter_objs.json",
    "config/openloader/data/ascendant_realms_guild/data/bountiful/bounty_pools/ascendant_guild/ar_town_guild_objs.json",
    "config/openloader/data/ascendant_realms_guild/data/bountiful/bounty_pools/ascendant_guild/ar_major_guild_objs.json",
    "config/openloader/data/ascendant_realms_atlas/pack.mcmeta",
    "config/openloader/data/ascendant_realms_atlas/README.md",
    "config/openloader/data/ascendant_realms_core/pack.mcmeta",
    "config/openloader/data/ascendant_realms_core/data/ascendant_core/functions/status.mcfunction",
    "config/openloader/data/ascendant_realms_core/data/ascendant_core/functions/debug/add_structure_clear.mcfunction",
    "config/openloader/data/ascendant_realms_core/data/ascendant_core/functions/debug/add_boss_proof.mcfunction",
    "config/openloader/data/ascendant_realms_core/data/ascendant_core/functions/debug/add_dragon_proof.mcfunction",
    "config/openloader/data/ascendant_realms_core/data/ascendant_core/functions/debug/reset_self.mcfunction",
    "config/openloader/data/ascendant_realms_dungeons/pack.mcmeta",
    "config/openloader/data/ascendant_realms_dungeons/README.md",
    "config/openloader/data/ascendant_realms_dungeons/data/ascendant_dungeons/dimension_type/ranked_dungeon.json",
    "config/openloader/data/ascendant_realms_dungeons/data/ascendant_dungeons/dimension/ranked_dungeon.json",
    "config/ascendant_index/gear_registry.json",
    "config/ascendant_index/mob_registry.json",
    "config/ascendant_index/structure_registry.json",
    "config/ascendant_index/skill_hook_registry.json",
    "config/ascendant_index/spawn_tuning_worklist.json",
    "config/ascendant_index/integration_matrix.json",
    "config/ascendant_core/README.md",
    "config/ascendant_core/core_manifest.json",
    "config/ascendant_core/rank_progression.json",
    "config/ascendant_core/world_regions.json",
    "config/ascendant_core/mob_ecology.json",
    "config/ascendant_core/structure_ecology.json",
    "config/ascendant_core/loot_rarity_rules.json",
    "config/ascendant_core/npc_role_contracts.json",
    "config/ascendant_core/material_unification.json",
    "config/ascendant_core/progression_hooks.json",
    "config/ascendant_core/runtime_rules.json",
    "config/ascendant_core/custom_module_plan.json",
    "config/ascendant_core/materials.json",
    "config/ascendant_core/ore_generation.json",
    "config/ascendant_core/recipe_policy.json",
    "config/ascendant_core/loot_policy.json",
    "config/ascendant_core/mob_policy.json",
    "config/ascendant_core/progression_tiers.json",
    "config/ascendant_core/dimension_policy.json",
    "config/ascendant_core/structure_rewards.json",
    "config/ascendant_core/vendor_policy.json",
    "config/ascendant_core/unification_policy.json",
    "config/ascendant_loot/loot_policy.json",
    "config/ascendant_loot/structure_loot_tiers.json",
    "config/ascendant_loot/mob_drop_tiers.json",
    "config/ascendant_loot/boss_reward_tiers.json",
    "config/ascendant_loot/bounty_reward_pools.json",
    "config/ascendant_loot/loot_rarity_budget.json",
    "config/ascendant_recipes/recipe_progression_policy.json",
    "config/ascendant_recipes/crafting_gate_registry.json",
    "config/ascendant_recipes/high_risk_recipes.json",
    "config/ascendant_recipes/candidate_recipe_rewrites.json",
    "config/ascendant_structures/structure_tier_registry.json",
    "config/ascendant_structures/structure_registry.json",
    "config/ascendant_structures/structure_region_rules.json",
    "config/ascendant_structures/structure_vertical_layer_rules.json",
    "config/ascendant_structures/structure_density_policy.json",
    "config/ascendant_structures/structure_set_overrides.json",
    "config/ascendant_structures/structure_loot_linkage.json",
    "config/ascendant_structures/water_structure_policy.json",
    "config/ascendant_structures/sky_structure_policy.json",
    "config/ascendant_structures/sea_floor_structure_policy.json",
    "config/ascendant_structures/ship_structure_policy.json",
    "config/ascendant_structures/dungeon_structure_policy.json",
    "config/ascendant_structures/boss_structure_policy.json",
    "config/ascendant_structures/village_structure_policy.json",
    "config/ascendant_structures/structure_test_points.json",
    "config/ascendant_structures/structure_visual_review_route.json",
    "config/ascendant_structures/structure_review_priority_queue.json",
    "config/ascendant_structures/structure_visual_review_findings_latest.json",
    "config/ascendant_structures/structure_evidence_registry.json",
    "config/ascendant_structures/structure_classification_confidence.json",
    "config/ascendant_structures/manual_structure_observations.json",
    "config/ascendant_structures/structure_locate_commands.md",
    "config/ascendant_structures/candidates/structure_land_placement_candidates.json",
    "config/ascendant_structures/candidates/structure_region_lock_candidates.json",
    "config/ascendant_structures/candidates/structure_density_candidates.json",
    "config/ascendant_travel/road_policy.json",
    "config/ascendant_travel/bridge_policy.json",
    "config/ascendant_travel/river_crossing_policy.json",
    "config/ascendant_travel/travel_network_candidates.json",
    "config/ascendant_atmosphere/region_atmosphere.json",
    "config/ascendant_atmosphere/weather_policy.json",
    "config/ascendant_atmosphere/audio_policy.json",
    "config/ascendant_atmosphere/title_policy.json",
    "config/ascendant_magic/spell_progression_registry.json",
    "config/ascendant_magic/magic_item_progression_registry.json",
    "config/ascendant_magic/school_region_policy.json",
    "config/ascendant_magic/magic_loot_policy.json",
    "config/ascendant_magic/magic_recipe_policy.json",
    "config/ascendant_balance/gear_outliers.json",
    "config/ascendant_balance/rarity_review_queue.json",
    "config/ascendant_balance/stat_policy.json",
    "config/ascendant_progression/rank_requirement_matrix.json",
    "config/ascendant_progression/skill_unlock_policy.json",
    "config/ascendant_progression/region_progression_policy.json",
    "config/ascendant_progression/gear_rank_policy.json",
    "config/ascendant_progression/magic_rank_policy.json",
    "config/ascendant_atlas/regions.json",
    "config/ascendant_atlas/difficulty_rings.json",
    "config/ascendant_atlas/climate_sectors.json",
    "config/ascendant_atlas/biome_assignments.json",
    "config/ascendant_atlas/settlement_rules.json",
    "config/ascendant_atlas/structure_distribution.json",
    "config/ascendant_atlas/mob_distribution.json",
    "config/ascendant_atlas/loot_distribution.json",
    "config/ascendant_atlas/ore_distribution.json",
    "config/ascendant_atlas/naming_pools.json",
    "config/ascendant_atlas/atlas_manifest.json",
    "config/ascendant_atlas/runtime.json",
    "config/ascendant_atlas/road_bridge_policy.json",
    "config/ascendant_atlas/worldgen_regions.json",
    "config/ascendant_atlas/worldgen_override_policy.json",
    "config/incontrol/areas.json",
    "config/ascendant_progression/progression.json",
    "config/ascendant_guild/README.md",
    "config/ascendant_guild/ranks.json",
    "config/ascendant_guild/rival_hunters.json",
    "config/ascendant_guild/bounty_categories.json",
    "config/ascendant_guild/hunter_boards.json",
    "config/ascendant_guild/npc_roster.json",
    "config/ascendant_guild/npc_loadouts.json",
    "config/ascendant_guild/nameplates.json",
    "config/ascendant_guild/npc_visual_policy.json",
    "config/ascendant_guild/rival_hunter_roster.json",
    "config/ascendant_guild/npc_profession_silhouettes.json",
    "config/ascendant_ui/tooltip_policy.json",
    "config/ascendant_ui/rarity_visual_policy.json",
    "config/ascendant_ui/mob_danger_display_policy.json",
    "config/ascendant_ui/region_title_policy.json",
    "config/ascendant_ui/keybind_policy.json",
    "config/ascendant_ui/death_waypoint_policy.json",
    "config/ascendant_guild/custom_npc_test_profiles.json",
    "config/ascendant_guild/generated_npc_profiles.json",
    "config/ascendant_guild/generated_npc_spawn_sets.json",
    "config/ascendant_guild/live_bountiful_pools.json",
    "config/ascendant_guild/tool_audit.json",
    "config/ascendant_guild/generated_bounty_targets.json",
    "config/ascendant_guild/bounty_pool_worklist.json",
    "config/ascendant_index/rarity_schema.json",
    "config/ascendant_settlements/README.md",
    "config/ascendant_settlements/settlement_unification.json",
    "config/ascendant_settlements/data_scaffold/README.md",
    "config/amendments-client.toml",
    "config/irons_spellbooks-client.toml",
    "config/overflowingbars-client.toml",
    "config/lootbeams-client.toml",
    "config/healthbarplus-client.toml",
    "config/oculus.properties",
    "config/obscuria/loot_journal-client.toml",
    "config/puffish_skills/config.json",
    "config/fancymenu/assets/ascendant_realms_background.mp4",
    "config/travelerstitles-forge-1_20.toml",
    "config/fancymenu/assets/ascendant_menu_status.txt",
    "config/fancymenu/assets/ascendant_pack_meta.json",
    "config/drippyloadingscreen/options.txt",
    "resourcepacks/ascendant-realms-compat-fixes/pack.mcmeta",
    "resourcepacks/ascendant-realms-compat-fixes/assets/minecraft/textures/models/armor/electromancer_layer_1.png",
    "resourcepacks/ascendant-realms-compat-fixes/assets/minecraft/textures/models/armor/frost_troll_layer_1.png",
    "resourcepacks/ascendant-realms-compat-fixes/assets/minecraft/textures/models/armor/frost_troll_layer_2.png",
    "resourcepacks/ascendant-realms-compat-fixes/assets/minecraft/textures/models/armor/plagued_layer_1.png",
    "resourcepacks/ascendant-realms-compat-fixes/assets/minecraft/textures/models/armor/priest_layer_1.png",
    "resourcepacks/ascendant-realms-compat-fixes/assets/minecraft/textures/models/armor/pumpkin_layer_1.png",
    "resourcepacks/ascendant-realms-compat-fixes/assets/iceandfire/textures/models/armor/sea_serpent_scales_deepblue_layer_1.png",
    "resourcepacks/ascendant-realms-compat-fixes/assets/iceandfire/textures/models/armor/sea_serpent_scales_deepblue_layer_2.png",
    "resourcepacks/ascendant-realms-compat-fixes/assets/customnpcs/textures/entity/ascendant_mca/rank_examiner.png",
    "customnpcs/assets/customnpcs/textures/entity/ascendant_mca/rank_examiner.png",
    "resourcepacks/ascendant-realms-travelers-titles/pack.mcmeta",
    "resourcepacks/ascendant-realms-travelers-titles/assets/travelerstitles/lang/en_us.json",
    "resourcepacks/ascendant-dungeon-gates/pack.mcmeta",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/gate/gate.png",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/gate/gate_green.png",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/gate/gate_purple.png",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/gate/gate_gold.png",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/gate/gate_red.png",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/item/gate.png",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/item/gate_green.png",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/item/gate_purple.png",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/item/gate_gold.png",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/item/gate_red.png",
    "resourcepacks/ascendant-dungeon-gates/assets/minecraft/models/item/paper.json",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/models/item/gate_blue.json",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/models/item/gate_green.json",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/models/item/gate_purple.json",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/models/item/gate_gold.json",
    "resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/models/item/gate_red.json",
    "datapacks/README.md",
    "datapacks/ascendant_realms_skills/pack.mcmeta",
    "datapacks/ascendant_realms_skills/data/ascendant_realms/puffish_skills/config.json",
    "openloader/README.md",
    "openloader/data/ascendant_realms_skills/pack.mcmeta",
    "openloader/data/ascendant_realms_skills/data/ascendant_realms/puffish_skills/config.json",
    "openloader/data/ascendant_realms_identity/pack.mcmeta",
    "openloader/data/ascendant_realms_identity/data/minecraft/tags/functions/load.json",
    "openloader/data/ascendant_realms_identity/data/minecraft/tags/functions/tick.json",
    "openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/load.mcfunction",
    "openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/tick.mcfunction",
    "openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/level_up.mcfunction",
    "openloader/data/ascendant_realms_codex/pack.mcmeta",
    "openloader/data/ascendant_realms_codex/data/ascendant_realms/patchouli_books/ascendant_codex/book.json",
    "openloader/data/ascendant_realms_guild/pack.mcmeta",
    "openloader/data/ascendant_realms_guild/data/ascendant_guild/functions/npc/list.mcfunction",
    "openloader/data/ascendant_realms_guild/data/ascendant_guild/functions/npc/spawn_set/starter_guild_staff.mcfunction",
    "openloader/data/ascendant_realms_guild/data/ascendant_guild/structures/guild/hunter_board_village_standard.nbt",
    "openloader/data/ascendant_realms_guild/data/ascendant_guild/worldgen/structure/hunter_board_village_standard.json",
    "openloader/data/ascendant_realms_guild/data/bountiful/bounty_pools/ascendant_guild/ar_village_hunter_objs.json",
    "openloader/data/ascendant_realms_atlas/pack.mcmeta",
    "openloader/data/ascendant_realms_atlas/README.md",
    "kubejs/server_scripts/ascendant_atlas_runtime.js",
    "kubejs/README.md",
    "kubejs/startup_scripts/ascendant_gear_rarity.js",
    "kubejs/startup_scripts/ascendant_guild_items.js",
    "kubejs/client_scripts/ascendant_jei_aliases.js",
    "kubejs/client_scripts/ascendant_rarity_tooltips.js",
    "kubejs/server_scripts/ascendant_recipes.js",
    "kubejs/server_scripts/ascendant_tags.js",
    "kubejs/server_scripts/ascendant_loot_notes.js",
    "kubejs/server_scripts/ascendant_core_integration.js",
    "kubejs/server_scripts/ascendant_progression.js",
    "scripts/generate-ascendant-skill-web.js",
    "scripts/generate-gear-rarity-index.ps1",
    "scripts/generate-universal-mod-index.js",
    "local-mods/ascendant-atlas-regions/README.md",
    "local-mods/ascendant-atlas-regions/src/main/java/com/robbinstech/ascendant_atlas_regions/AscendantAtlasRegions.java",
    "local-mods/ascendant-atlas-regions/src/main/java/com/robbinstech/ascendant_atlas_regions/AtlasLandBiasDensityFunction.java",
    "local-mods/ascendant-atlas-regions/src/main/java/com/robbinstech/ascendant_atlas_regions/RegionalMultiNoiseBiomeSource.java",
    "local-mods/ascendant-atlas-regions/src/main/java/com/robbinstech/ascendant_atlas_regions/AtlasTerrainCorrection.java",
    "local-mods/ascendant-atlas-regions/src/main/resources/META-INF/mods.toml",
    "local-mods/ascendant-atlas-regions/src/main/resources/pack.mcmeta",
    "mods/ascendant-atlas-regions-0.1.0.jar",
    "local-mods/ascendant-nametags/README.md",
    "local-mods/ascendant-nametags/src/main/java/com/robbinstech/ascendant_nametags/AscendantNametags.java",
    "local-mods/ascendant-nametags/src/main/java/com/robbinstech/ascendant_nametags/AscendantNametagsClient.java",
    "local-mods/ascendant-nametags/src/main/resources/META-INF/mods.toml",
    "local-mods/ascendant-nametags/src/main/resources/pack.mcmeta",
    "mods/ascendant-nametags-0.1.0.jar",
]

FORBIDDEN_ACTIVE_SLUGS = [
    "minecolonies",
    "sinytra",
    "connector",
    "optifine",
    "biomes-o-plenty",
    "biomesoplenty",
    "dynamic-trees",
    "yungs-better-caves",
    "theurgy",
    "modonomicon",
    "ars-nouveau",
    "arsnouveau",
    "ice-and-fire-dragons",
    "parcool",
    "lootintegrationaddonyung",
    "lootintegrations-yungs",
    "lootintegrations_yungs",
    "yung-structures-addon-for-loot-integrations",
    "customnametags",
    "custom-name-tags",
    "champions",
    "health-indicators",
    "healthindicators",
    "immersive-storms",
    "immersivestorms",
    "better-clouds",
    "betterclouds",
    "ryoamiclights",
    "ryoamic-lights",
    "hardcore-torches",
    "lanterns-bow",
    "lanterns-belong",
    "simple-clouds",
    "simpleclouds",
    "project-atmosphere",
    "projectatmosphere",
    "integratedplaytime",
    "integrated-playtime",
    "spell-engine",
    "rpg-series",
]

ALLOWED_PACKWIZ_METADATA = {
    "mods/3dskinlayers.pw.toml",
    "mods/advancement-plaques.pw.toml",
    "mods/alexs-delight.pw.toml",
    "mods/alexs-mobs.pw.toml",
    "mods/almost-unify-everything.pw.toml",
    "mods/almostunified.pw.toml",
    "mods/ambientsounds.pw.toml",
    "mods/amendments.pw.toml",
    "mods/appleskin.pw.toml",
    "mods/aquamirae.pw.toml",
    "mods/architectury-api.pw.toml",
    "mods/artifacts.pw.toml",
    "mods/attributefix.pw.toml",
    "mods/auroras.pw.toml",
    "mods/better-combat.pw.toml",
    "mods/beautiful-enchanted-books-mod-edition.pw.toml",
    "mods/biome-music.pw.toml",
    "mods/bookshelf-lib.pw.toml",
    "mods/borninchaos.pw.toml",
    "mods/bossesrise.pw.toml",
    "mods/bountiful.pw.toml",
    "mods/citadel.pw.toml",
    "mods/cloth-config.pw.toml",
    "mods/collective.pw.toml",
    "mods/combat-roll.pw.toml",
    "mods/coroutil.pw.toml",
    "mods/corgilib.pw.toml",
    "mods/creativecore.pw.toml",
    "mods/create.pw.toml",
    "mods/create-big-cannons.pw.toml",
    "mods/create-structures-arise.pw.toml",
    "mods/cristel-lib.pw.toml",
    "mods/cupboard.pw.toml",
    "mods/curios.pw.toml",
    "mods/customnpcs-unofficial.pw.toml",
    "mods/data-anchor.pw.toml",
    "mods/decorative-blocks.pw.toml",
    "mods/drippy-loading-screen.pw.toml",
    "mods/attributes.pw.toml",
    "mods/easy-npc-config-ui.pw.toml",
    "mods/easy-npc-core.pw.toml",
    "mods/embeddium.pw.toml",
    "mods/enchantment-descriptions.pw.toml",
    "mods/enhanced-boss-bars-mod.pw.toml",
    "mods/enhanced-celestials.pw.toml",
    "mods/entity-model-features.pw.toml",
    "mods/entityculling.pw.toml",
    "mods/entitytexturefeatures.pw.toml",
    "mods/every-compat.pw.toml",
    "mods/fallingleavesforge.pw.toml",
    "mods/fancymenu.pw.toml",
    "mods/fantasy_armor.pw.toml",
    "mods/farmers-delight.pw.toml",
    "mods/ferrite-core.pw.toml",
    "mods/fragmentum.pw.toml",
    "mods/ftb-backups-2.pw.toml",
    "mods/ftb-library-forge.pw.toml",
    "mods/ftb-quests-forge.pw.toml",
    "mods/ftb-ranks-forge.pw.toml",
    "mods/ftb-teams-forge.pw.toml",
    "mods/fzzy-config.pw.toml",
    "mods/geckolib.pw.toml",
    "mods/glitchcore.pw.toml",
    "mods/guard-villagers.pw.toml",
    "mods/handcrafted.pw.toml",
    "mods/health-bar-plus.pw.toml",
    "mods/hicudan.pw.toml",
    "mods/human-companions.pw.toml",
    "mods/iceandfire-ce.pw.toml",
    "mods/iceberg.pw.toml",
    "mods/immersive-ui.pw.toml",
    "mods/immersive-armors.pw.toml",
    "mods/immersive-portals-neoforge.pw.toml",
    "mods/elite-holograms.pw.toml",
    "mods/improved-mobs.pw.toml",
    "mods/in-control.pw.toml",
    "mods/integrated-api.pw.toml",
    "mods/integrated-villages.pw.toml",
    "mods/irons-lib.pw.toml",
    "mods/irons-spells-n-spellbooks.pw.toml",
    "mods/item-borders.pw.toml",
    "mods/jei.pw.toml",
    "mods/jupiter.pw.toml",
    "mods/kotlin-for-forge.pw.toml",
    "mods/kambrik.pw.toml",
    "mods/kiwi.pw.toml",
    "mods/konkrete.pw.toml",
    "mods/kubejs.pw.toml",
    "mods/majrusz-library.pw.toml",
    "mods/majruszs-progressive-difficulty.pw.toml",
    "mods/legendary-tooltips.pw.toml",
    "mods/loot-beams.pw.toml",
    "mods/loot-integrations.pw.toml",
    "mods/loot-journal.pw.toml",
    "mods/macaws-bridges.pw.toml",
    "mods/macaws-fences-and-walls.pw.toml",
    "mods/macaws-lights-and-lamps.pw.toml",
    "mods/malfu-combat-animation.pw.toml",
    "mods/medieval-buildings-end-edition.pw.toml",
    "mods/medieval-buildings-nether-edition.pw.toml",
    "mods/melody.pw.toml",
    "mods/mes-moogs-end-structures.pw.toml",
    "mods/l_enders-cataclysm.pw.toml",
    "mods/lionfish-api.pw.toml",
    "mods/mariums-soulslike-weaponry.pw.toml",
    "mods/minecraft-comes-alive-reborn.pw.toml",
    "mods/modernfix.pw.toml",
    "mods/moonlight.pw.toml",
    "mods/moogs-structure-lib.pw.toml",
    "mods/moogs-voyager-structures.pw.toml",
    "mods/mss-moogs-soaring-structures.pw.toml",
    "mods/mowzies-mobs.pw.toml",
    "mods/not-enough-animations.pw.toml",
    "mods/oculus.pw.toml",
    "mods/open-loader.pw.toml",
    "mods/obscure-api.pw.toml",
    "mods/overflowing-bars.pw.toml",
    "mods/particular-reforged.pw.toml",
    "mods/patchouli.pw.toml",
    "mods/perception.pw.toml",
    "mods/playeranimator.pw.toml",
    "mods/polylib.pw.toml",
    "mods/polymorph.pw.toml",
    "mods/presence-footsteps-forge.pw.toml",
    "mods/projectile-damage-attribute.pw.toml",
    "mods/prism-lib.pw.toml",
    "mods/puzzles-lib.pw.toml",
    "mods/quark.pw.toml",
    "mods/rhino.pw.toml",
    "mods/resource-pack-overrides.pw.toml",
    "mods/rpl.pw.toml",
    "mods/resourceful-lib.pw.toml",
    "mods/serene-seasons.pw.toml",
    "mods/shatterbyte-lib.pw.toml",
    "mods/simply-swords.pw.toml",
    "mods/slice-and-dice.pw.toml",
    "mods/scaling-health.pw.toml",
    "mods/skills.pw.toml",
    "mods/silent-lib.pw.toml",
    "mods/small-ships.pw.toml",
    "mods/snow-real-magic.pw.toml",
    "mods/sound-physics-remastered.pw.toml",
    "mods/spark.pw.toml",
    "mods/spiffyhud.pw.toml",
    "mods/sophisticated-backpacks.pw.toml",
    "mods/sophisticated-core.pw.toml",
    "mods/spawn-balance-utility.pw.toml",
    "mods/sparsestructures.pw.toml",
    "mods/spartan-shields.pw.toml",
    "mods/structory.pw.toml",
    "mods/subtle-effects.pw.toml",
    "mods/sodium-dynamic-lights.pw.toml",
    "mods/sodium-options-api.pw.toml",
    "mods/stylish-effects.pw.toml",
    "mods/supplementaries.pw.toml",
    "mods/tenshilib.pw.toml",
    "mods/tectonic.pw.toml",
    "mods/terralith.pw.toml",
    "mods/titles.pw.toml",
    "mods/towns-and-towers.pw.toml",
    "mods/travelers-titles.pw.toml",
    "mods/uranus.pw.toml",
    "mods/villager-names-serilum.pw.toml",
    "mods/villages-and-pillages.pw.toml",
    "mods/visual-workbench.pw.toml",
    "mods/wavey-capes.pw.toml",
    "mods/watermedia.pw.toml",
    "mods/watermedia-binaries.pw.toml",
    "mods/weather-storms-tornadoes.pw.toml",
    "mods/xaeros-minimap.pw.toml",
    "mods/yungs-api.pw.toml",
    "mods/yungs-better-dungeons.pw.toml",
    "mods/yungs-better-mineshafts.pw.toml",
    "mods/yungs-better-strongholds.pw.toml",
    "mods/yungs-bridges.pw.toml",
    "mods/yungs-extras.pw.toml",
    "mods/idas.pw.toml",
    "mods/zeta.pw.toml",
    "resourcepacks/cubic-leaves.pw.toml",
    "resourcepacks/cubic-sun-moon.pw.toml",
    "resourcepacks/embellished-stone-advancements-plaques.pw.toml",
    "resourcepacks/excal.pw.toml",
    "resourcepacks/fresh-animations.pw.toml",
    "resourcepacks/icon-xaeros.pw.toml",
    "resourcepacks/icon-xaeros-x-freshanimations.pw.toml",
    "resourcepacks/simply-swords-reforged.pw.toml",
    "resourcepacks/stoneborn.pw.toml",
    "resourcepacks/medieval-music.pw.toml",
    "resourcepacks/the-rename-compat-project.pw.toml",
    "resourcepacks/vanilla-exp.pw.toml",
    "resourcepacks/visual-travelers-title-biomes-addon.pw.toml",
    "resourcepacks/visual-travelers-titles.pw.toml",
    "shaderpacks/complementary-reimagined.pw.toml",
}

EXPECTED_SIDE = {
    "mods/3dskinlayers.pw.toml": "client",
    "mods/advancement-plaques.pw.toml": "client",
    "mods/alexs-delight.pw.toml": "both",
    "mods/alexs-mobs.pw.toml": "both",
    "mods/almost-unify-everything.pw.toml": "both",
    "mods/almostunified.pw.toml": "both",
    "mods/ambientsounds.pw.toml": "client",
    "mods/amendments.pw.toml": "both",
    "mods/appleskin.pw.toml": "both",
    "mods/aquamirae.pw.toml": "both",
    "mods/architectury-api.pw.toml": "both",
    "mods/artifacts.pw.toml": "both",
    "mods/attributefix.pw.toml": "both",
    "mods/auroras.pw.toml": "client",
    "mods/better-combat.pw.toml": "both",
    "mods/beautiful-enchanted-books-mod-edition.pw.toml": "client",
    "mods/biome-music.pw.toml": "client",
    "mods/bookshelf-lib.pw.toml": "client",
    "mods/borninchaos.pw.toml": "both",
    "mods/bossesrise.pw.toml": "both",
    "mods/bountiful.pw.toml": "both",
    "mods/citadel.pw.toml": "both",
    "mods/cloth-config.pw.toml": "both",
    "mods/collective.pw.toml": "both",
    "mods/combat-roll.pw.toml": "both",
    "mods/coroutil.pw.toml": "both",
    "mods/corgilib.pw.toml": "both",
    "mods/creativecore.pw.toml": "client",
    "mods/create.pw.toml": "both",
    "mods/create-big-cannons.pw.toml": "both",
    "mods/create-structures-arise.pw.toml": "both",
    "mods/cristel-lib.pw.toml": "both",
    "mods/cupboard.pw.toml": "both",
    "mods/curios.pw.toml": "both",
    "mods/customnpcs-unofficial.pw.toml": "both",
    "mods/data-anchor.pw.toml": "both",
    "mods/decorative-blocks.pw.toml": "both",
    "mods/drippy-loading-screen.pw.toml": "client",
    "mods/attributes.pw.toml": "both",
    "mods/easy-npc-config-ui.pw.toml": "both",
    "mods/easy-npc-core.pw.toml": "both",
    "mods/embeddium.pw.toml": "client",
    "mods/enchantment-descriptions.pw.toml": "client",
    "mods/enhanced-boss-bars-mod.pw.toml": "client",
    "mods/enhanced-celestials.pw.toml": "both",
    "mods/entity-model-features.pw.toml": "client",
    "mods/entityculling.pw.toml": "client",
    "mods/entitytexturefeatures.pw.toml": "client",
    "mods/every-compat.pw.toml": "both",
    "mods/fallingleavesforge.pw.toml": "client",
    "mods/fancymenu.pw.toml": "client",
    "mods/fantasy_armor.pw.toml": "both",
    "mods/farmers-delight.pw.toml": "both",
    "mods/fragmentum.pw.toml": "both",
    "mods/ftb-backups-2.pw.toml": "both",
    "mods/ftb-library-forge.pw.toml": "both",
    "mods/ftb-quests-forge.pw.toml": "both",
    "mods/ftb-ranks-forge.pw.toml": "both",
    "mods/ftb-teams-forge.pw.toml": "both",
    "mods/fzzy-config.pw.toml": "both",
    "mods/geckolib.pw.toml": "both",
    "mods/glitchcore.pw.toml": "both",
    "mods/guard-villagers.pw.toml": "both",
    "mods/handcrafted.pw.toml": "both",
    "mods/health-bar-plus.pw.toml": "client",
    "mods/hicudan.pw.toml": "client",
    "mods/human-companions.pw.toml": "both",
    "mods/iceandfire-ce.pw.toml": "both",
    "mods/iceberg.pw.toml": "client",
    "mods/immersive-ui.pw.toml": "client",
    "mods/immersive-armors.pw.toml": "both",
    "mods/immersive-portals-neoforge.pw.toml": "both",
    "mods/elite-holograms.pw.toml": "both",
    "mods/improved-mobs.pw.toml": "both",
    "mods/in-control.pw.toml": "both",
    "mods/integrated-api.pw.toml": "both",
    "mods/integrated-villages.pw.toml": "both",
    "mods/irons-lib.pw.toml": "both",
    "mods/irons-spells-n-spellbooks.pw.toml": "both",
    "mods/item-borders.pw.toml": "client",
    "mods/jei.pw.toml": "client",
    "mods/jupiter.pw.toml": "both",
    "mods/kotlin-for-forge.pw.toml": "both",
    "mods/kambrik.pw.toml": "both",
    "mods/kiwi.pw.toml": "both",
    "mods/konkrete.pw.toml": "client",
    "mods/kubejs.pw.toml": "both",
    "mods/majrusz-library.pw.toml": "both",
    "mods/majruszs-progressive-difficulty.pw.toml": "both",
    "mods/legendary-tooltips.pw.toml": "client",
    "mods/loot-beams.pw.toml": "client",
    "mods/loot-integrations.pw.toml": "both",
    "mods/loot-journal.pw.toml": "client",
    "mods/macaws-bridges.pw.toml": "both",
    "mods/macaws-fences-and-walls.pw.toml": "both",
    "mods/macaws-lights-and-lamps.pw.toml": "both",
    "mods/malfu-combat-animation.pw.toml": "both",
    "mods/medieval-buildings-end-edition.pw.toml": "both",
    "mods/medieval-buildings-nether-edition.pw.toml": "both",
    "mods/melody.pw.toml": "client",
    "mods/mes-moogs-end-structures.pw.toml": "both",
    "mods/l_enders-cataclysm.pw.toml": "both",
    "mods/lionfish-api.pw.toml": "both",
    "mods/mariums-soulslike-weaponry.pw.toml": "both",
    "mods/minecraft-comes-alive-reborn.pw.toml": "both",
    "mods/moonlight.pw.toml": "both",
    "mods/moogs-structure-lib.pw.toml": "both",
    "mods/moogs-voyager-structures.pw.toml": "both",
    "mods/mss-moogs-soaring-structures.pw.toml": "both",
    "mods/mowzies-mobs.pw.toml": "both",
    "mods/not-enough-animations.pw.toml": "client",
    "mods/oculus.pw.toml": "client",
    "mods/open-loader.pw.toml": "both",
    "mods/obscure-api.pw.toml": "both",
    "mods/overflowing-bars.pw.toml": "client",
    "mods/particular-reforged.pw.toml": "both",
    "mods/patchouli.pw.toml": "both",
    "mods/perception.pw.toml": "client",
    "mods/playeranimator.pw.toml": "both",
    "mods/polylib.pw.toml": "both",
    "mods/polymorph.pw.toml": "both",
    "mods/presence-footsteps-forge.pw.toml": "client",
    "mods/projectile-damage-attribute.pw.toml": "both",
    "mods/prism-lib.pw.toml": "client",
    "mods/rpl.pw.toml": "both",
    "mods/quark.pw.toml": "both",
    "mods/rhino.pw.toml": "both",
    "mods/resource-pack-overrides.pw.toml": "client",
    "mods/resourceful-lib.pw.toml": "both",
    "mods/serene-seasons.pw.toml": "both",
    "mods/shatterbyte-lib.pw.toml": "client",
    "mods/simply-swords.pw.toml": "both",
    "mods/slice-and-dice.pw.toml": "both",
    "mods/scaling-health.pw.toml": "both",
    "mods/skills.pw.toml": "both",
    "mods/silent-lib.pw.toml": "both",
    "mods/small-ships.pw.toml": "both",
    "mods/snow-real-magic.pw.toml": "both",
    "mods/sound-physics-remastered.pw.toml": "client",
    "mods/spark.pw.toml": "both",
    "mods/spiffyhud.pw.toml": "client",
    "mods/spawn-balance-utility.pw.toml": "both",
    "mods/sparsestructures.pw.toml": "both",
    "mods/spartan-shields.pw.toml": "both",
    "mods/structory.pw.toml": "both",
    "mods/subtle-effects.pw.toml": "both",
    "mods/sodium-dynamic-lights.pw.toml": "client",
    "mods/sodium-options-api.pw.toml": "client",
    "mods/stylish-effects.pw.toml": "client",
    "mods/supplementaries.pw.toml": "both",
    "mods/tenshilib.pw.toml": "both",
    "mods/tectonic.pw.toml": "both",
    "mods/terralith.pw.toml": "both",
    "mods/titles.pw.toml": "both",
    "mods/towns-and-towers.pw.toml": "both",
    "mods/travelers-titles.pw.toml": "client",
    "mods/uranus.pw.toml": "both",
    "mods/villager-names-serilum.pw.toml": "both",
    "mods/villages-and-pillages.pw.toml": "both",
    "mods/wavey-capes.pw.toml": "client",
    "mods/watermedia.pw.toml": "client",
    "mods/watermedia-binaries.pw.toml": "client",
    "mods/weather-storms-tornadoes.pw.toml": "both",
    "mods/xaeros-minimap.pw.toml": "client",
    "mods/yungs-api.pw.toml": "both",
    "mods/yungs-better-dungeons.pw.toml": "both",
    "mods/yungs-better-mineshafts.pw.toml": "both",
    "mods/yungs-better-strongholds.pw.toml": "both",
    "mods/yungs-bridges.pw.toml": "both",
    "mods/yungs-extras.pw.toml": "both",
    "mods/idas.pw.toml": "both",
    "mods/zeta.pw.toml": "both",
    "resourcepacks/cubic-leaves.pw.toml": "client",
    "resourcepacks/cubic-sun-moon.pw.toml": "client",
    "resourcepacks/embellished-stone-advancements-plaques.pw.toml": "client",
    "resourcepacks/excal.pw.toml": "client",
    "resourcepacks/fresh-animations.pw.toml": "client",
    "resourcepacks/icon-xaeros.pw.toml": "client",
    "resourcepacks/icon-xaeros-x-freshanimations.pw.toml": "client",
    "resourcepacks/simply-swords-reforged.pw.toml": "client",
    "resourcepacks/stoneborn.pw.toml": "client",
    "resourcepacks/medieval-music.pw.toml": "client",
    "resourcepacks/the-rename-compat-project.pw.toml": "client",
    "resourcepacks/vanilla-exp.pw.toml": "client",
    "resourcepacks/visual-travelers-title-biomes-addon.pw.toml": "client",
    "resourcepacks/visual-travelers-titles.pw.toml": "client",
    "shaderpacks/complementary-reimagined.pw.toml": "client",
}

EXPECTED_DOC_PATTERNS = [
    ("docs/VERSION_AND_LOADER_DECISION.md", r"1\.20\.1 Forge"),
    ("docs/VERSION_AND_LOADER_DECISION.md", r"1\.21\.1 NeoForge"),
    ("docs/BATCH_INSTALL_PLAN.md", r"Batch A"),
    ("docs/BATCH_INSTALL_PLAN.md", r"Batch H"),
    ("docs/BATCH_INSTALL_PLAN.md", r"Batch J"),
    ("docs/COMPATIBILITY_MATRIX.md", r"Fresh Animations"),
    ("docs/COMPATIBILITY_MATRIX.md", r"Ice and Fire"),
    ("docs/ASCENDANT_CORE_INTEGRATION.md", r"data-first integration layer"),
    ("docs/ASCENDANT_ATLAS_WORLDGEN.md", r"finite-world coordinate runtime"),
    ("docs/ASCENDANT_ATLAS_WORLDGEN.md", r"road/bridge"),
    ("docs/WORLDGEN_AND_STRUCTURES.md", r"Ascendant Atlas"),
]

FORBIDDEN_DOC_PATTERNS = [
    (
        "docs/ASCENDANT_CORE_INTEGRATION.md",
        r"future helper module for precise biome-source control",
        "The Ascendant Atlas helper exists; current docs must describe whether its worldgen influence is enabled or disabled.",
    ),
    (
        "docs/ASCENDANT_CORE_INTEGRATION.md",
        r"future coordinate-aware region/distance/biome-source control",
        "The Ascendant Atlas helper exists; current docs must describe whether its worldgen influence is enabled or disabled.",
    ),
    (
        "docs/ASCENDANT_CORE_INTEGRATION.md",
        r"not hard biome-source replacement",
        "Atlas coordinate-aware biome-source replacement was implemented and is now disabled by policy.",
    ),
    (
        "docs/SYSTEM_ECOSYSTEM_OVERVIEW.md",
        r"Start the first small Ascendant helper mod only",
        "The first helper mod already exists; only additional helper work remains future.",
    ),
    (
        "config/openloader/data/ascendant_realms_atlas/README.md",
        r"live Atlas implementation is the KubeJS finite-world runtime plus In Control coordinate areas",
        "The Atlas OpenLoader README must mention the current random-worldgen rollback boundary.",
    ),
    (
        "openloader/data/ascendant_realms_atlas/README.md",
        r"live Atlas implementation is the KubeJS finite-world runtime plus In Control coordinate areas",
        "The Atlas OpenLoader README must mention the current random-worldgen rollback boundary.",
    ),
]

README_MAX_CHARS = 12000
README_HANDOFF_SPAM_PATTERNS = [
    r"(?m)^## Batch [A-Z]",
    r"(?m)^## Batch A Installed",
    r"(?m)^- Batch [A-Z].*validation",
    r"(?m)^- Latest multiplayer playtest:",
]

CURRENT_STATUS_BLOCKER_PATTERNS = [
    r"random generation",
    r"worldgen override.*disabled|disabled.*worldgen override",
    r"Tectonic/Terralith|Terralith/Tectonic",
    r"fresh world",
]

DOC_DIST_SOURCE_RE = re.compile(
    r"\b(?:source|read|authoritative|current)\b[^\n]{0,80}`?dist/",
    re.IGNORECASE,
)

DOC_DIST_NEGATION_RE = re.compile(
    r"(ignore|do not treat|not .*source|generated export|can lag)",
    re.IGNORECASE,
)

STALE_CURRENT_HELPER_PATTERNS = [
    (
        re.compile(r"future helper mod(?:ule)? for precise biome-source control", re.IGNORECASE),
        "Atlas biome-source helper already exists; current docs must not call it future work.",
    ),
    (
        re.compile(r"future coordinate-aware region/distance/biome-source control", re.IGNORECASE),
        "Atlas coordinate-aware biome-source control was implemented and is now disabled by random-worldgen policy.",
    ),
    (
        re.compile(r"terrain is signed off|terrain signed off", re.IGNORECASE),
        "Avoid terrain signoff wording unless the current random-worldgen baseline has been validated in a fresh world.",
    ),
]

BATCH_B_REQUIRED_METADATA = {
    "mods/terralith.pw.toml",
    "mods/tectonic.pw.toml",
    "mods/serene-seasons.pw.toml",
    "mods/towns-and-towers.pw.toml",
    "mods/structory.pw.toml",
    "mods/yungs-better-mineshafts.pw.toml",
    "mods/yungs-better-strongholds.pw.toml",
    "mods/yungs-better-dungeons.pw.toml",
    "mods/yungs-bridges.pw.toml",
    "mods/sparsestructures.pw.toml",
    "mods/cristel-lib.pw.toml",
    "mods/glitchcore.pw.toml",
}

BATCH_C_REQUIRED_METADATA = {
    "mods/better-combat.pw.toml",
    "mods/combat-roll.pw.toml",
    "mods/simply-swords.pw.toml",
    "mods/playeranimator.pw.toml",
    "mods/cloth-config.pw.toml",
    "mods/architectury-api.pw.toml",
}

BATCH_D_REQUIRED_METADATA = {
    "mods/attributes.pw.toml",
    "mods/skills.pw.toml",
}

CUSTOM_SKILL_TREE_REQUIRED_FILES = {
    "config/puffish_skills/config.json",
    "datapacks/ascendant_realms_skills/pack.mcmeta",
    "datapacks/ascendant_realms_skills/data/ascendant_realms/puffish_skills/config.json",
}

CUSTOM_SKILL_TREE_CATEGORIES = {
    "ascendant",
}

CUSTOM_SKILL_TREE_MIN_DEFINITIONS = 100
CUSTOM_SKILL_TREE_MAX_CONNECTIONS = 220

GEAR_INDEX_MIN_COUNTS = {
    "weapons": 400,
    "armor": 450,
    "shields": 50,
    "magic_items": 200,
    "spells": 100,
    "accessories_relics": 120,
}

GEAR_INDEX_COLLECTIONS = [
    "weapons",
    "armor",
    "shields",
    "magic_items",
    "spells",
    "accessories_relics",
]

ASCENDANT_UI_TANGIBLE_GEAR_COLLECTIONS = [
    "weapons",
    "armor",
    "shields",
    "magic_items",
    "accessories_relics",
]

GEAR_INDEX_BAD_ID_PATTERN = re.compile(
    r"(spawn_egg|/|_hand$|_model$|_inventory$|_blocking$)",
    re.IGNORECASE,
)

ASCENDANT_RARITY_ORDER = {
    "common": 1,
    "uncommon": 2,
    "rare": 3,
    "epic": 4,
    "legendary": 5,
    "mythic": 6,
    "ascendant": 7,
}

NPC_LOADOUT_SLOT_KEYS = {
    "mainhand",
    "offhand",
    "head",
    "chest",
    "legs",
    "feet",
    "accessory",
    "curio",
}

IMPORTANT_NPC_VISIBLE_SLOT_KEYS = {"mainhand", "head", "chest"}

RIVAL_PROFILE_IDS = {
    "mira_ash",
    "darius_crowe",
    "seren_valehart",
    "kael_vorn",
    "black_hound",
}

ASCENDANT_NPC_VISUAL_JSON_FILES = [
    "config/ascendant_guild/npc_visual_policy.json",
    "config/ascendant_guild/rival_hunter_roster.json",
    "config/ascendant_guild/npc_profession_silhouettes.json",
]

ASCENDANT_NPC_VISUAL_REQUIRED_DOCS = [
    "docs/NPC_VISUAL_VALIDATION_REPORT.md",
    "docs/MCA_MEDIEVAL_SKIN_AUDIT.md",
    "docs/RIVAL_HUNTER_VISUAL_ROSTER.md",
]

ASCENDANT_UI_JSON_FILES = [
    "config/ascendant_ui/tooltip_policy.json",
    "config/ascendant_ui/rarity_visual_policy.json",
    "config/ascendant_ui/mob_danger_display_policy.json",
    "config/ascendant_ui/region_title_policy.json",
    "config/ascendant_ui/death_waypoint_policy.json",
]

ASCENDANT_UI_REQUIRED_DOCS = [
    "docs/UI_CLARITY_AND_FEEDBACK_AUDIT.md",
    "docs/RARITY_TOOLTIP_VISUAL_POLICY.md",
    "docs/MOB_DANGER_UI_POLICY.md",
    "docs/REGION_TITLE_UI_POLICY.md",
    "docs/DEATH_WAYPOINT_UI_POLICY.md",
]

ASCENDANT_UI_REQUIRED_RESOURCE_PACKS = [
    "file/Visual Titles 1.3.zip",
    "file/Visual Travelers Titles Biomes Addon.zip",
    "file/ascendant-realms-travelers-titles",
    "file/ascendant-realms-compat-fixes",
]

ASCENDANT_UI_SYNC_REQUIRED_TOKENS = [
    "config\\ascendant_ui",
    "config\\obscuria",
    "itemborders-common.toml",
    "lootbeams-client.toml",
    "healthbarplus-client.toml",
    "overflowingbars-client.toml",
    "resourcepackoverrides.json",
    "travelerstitles-forge-1_20.toml",
]

ASCENDANT_IMPORTANT_NPC_PROFESSIONS = {
    "guild_clerk",
    "rank_examiner",
    "bounty_master",
    "guild_arcanist",
    "hunter_quartermaster",
    "guard_captain",
    "tavern_keeper",
    "village_elder",
    "rival_hunter",
}

ASCENDANT_GUILD_STRUCTURE_IDS = {
    "hunter_board_village_standard",
    "roadside_hunter_camp",
    "frontier_guild_outpost",
}

ASCENDANT_GUILD_REQUIRED_SKINS = {
    "bounty_master",
    "darius_crowe",
    "guard_captain",
    "guild_arcanist",
    "guild_clerk",
    "hunter_quartermaster",
    "mira_ash",
    "rank_examiner",
    "seren_valehart",
    "tavern_keeper",
    "village_elder",
    "wounded_hunter",
}

ASCENDANT_GUILD_REQUIRED_WALL_LANTERNS = {
    "hunter_board_village_standard": "mcwlights:tavern_wall_lantern",
    "frontier_guild_outpost": "mcwlights:covered_wall_lantern",
}

ASCENDANT_GUILD_MIN_SPACING = {
    "hunter_board_village_standard": 192,
    "roadside_hunter_camp": 224,
    "frontier_guild_outpost": 288,
}

ASCENDANT_GUILD_MIN_NOTICE_BOARDS = {
    "hunter_board_village_standard": 4,
    "roadside_hunter_camp": 2,
    "frontier_guild_outpost": 4,
}

ASCENDANT_GUILD_MIN_LOOT_CONTAINERS = {
    "hunter_board_village_standard": 2,
    "roadside_hunter_camp": 2,
    "frontier_guild_outpost": 2,
}

ASCENDANT_GUILD_BOUNTY_BOARDS = {
    "village_hunter_board": ("ar_village_hunter_objs", 12),
    "town_guild_board": ("ar_town_guild_objs", 8),
    "major_guild_registry": ("ar_major_guild_objs", 8),
}

ASCENDANT_ATLAS_DEBUG_STRUCTURE_IDS = {
    "ascendant_atlas:crownlands_waymark",
    "ascendant_atlas:frostmarch_waymark",
    "ascendant_atlas:sunreach_waymark",
    "ascendant_atlas:verdant_crossing",
    "ascendant_atlas:stoneback_waystation",
}

ASCENDANT_ATLAS_AREA_NAMES = {
    "ar_world_square",
    "ar_hearthlands",
    "ar_frostmarch",
    "ar_sunreach",
    "ar_verdant_coast",
    "ar_stoneback_highlands",
    "ar_north_east_marches",
    "ar_north_west_marches",
    "ar_south_east_wilds",
    "ar_south_west_wilds",
}

ASCENDANT_CORE_POLICY_FILES = [
    "materials.json",
    "ore_generation.json",
    "recipe_policy.json",
    "loot_policy.json",
    "mob_policy.json",
    "progression_tiers.json",
    "dimension_policy.json",
    "structure_rewards.json",
    "vendor_policy.json",
    "unification_policy.json",
]

ASCENDANT_ATLAS_POLICY_FILES = [
    "regions.json",
    "difficulty_rings.json",
    "climate_sectors.json",
    "biome_assignments.json",
    "worldgen_regions.json",
    "settlement_rules.json",
    "structure_distribution.json",
    "mob_distribution.json",
    "loot_distribution.json",
    "ore_distribution.json",
    "naming_pools.json",
    "atlas_manifest.json",
    "runtime.json",
    "road_bridge_policy.json",
    "terrain_noise_policy.json",
    "land_water_region_policy.json",
    "worldgen_override_policy.json",
]

ASCENDANT_ATLAS_REPORT_JSON_FILES = [
    "config/ascendant_atlas/reports/sample_grid_latest.json",
    "config/ascendant_atlas/reports/sample_grid_source_latest.json",
    "config/ascendant_atlas/reports/sample_grid_surface_latest.json",
    "config/ascendant_atlas/reports/water_surface_samples_latest.json",
    "config/ascendant_atlas/reports/water_body_classification_latest.json",
    "config/ascendant_atlas/reports/terrain_noise_probe_latest.json",
    "config/ascendant_atlas/reports/land_water_coherence_latest.json",
    "config/ascendant_atlas/reports/terrain_wrapper_test_latest.json",
    "config/ascendant_atlas/reports/biome_pools_resolved.json",
    "config/ascendant_atlas/reports/missing_biomes.json",
    "config/ascendant_atlas/reports/biome_pools_live_latest.json",
]

ASCENDANT_ATLAS_SNOW_ALLOWED_POOLS = {
    "north",
    "north_east",
    "north_west",
    "outer",
}

ASCENDANT_ATLAS_WATER_REVIEW_POOLS = {
    "south",
    "west",
    "south_west",
}

ASCENDANT_ATLAS_ACCEPTED_TRANSITION_EDGE_CLASSIFICATION = "stoneback_frostmarch_transition_river"
ASCENDANT_ATLAS_FROZEN_MOUNTAIN_RIVER_SURFACE_BLOCKS = {
    "minecraft:ice",
    "minecraft:water",
    "minecraft:packed_ice",
    "minecraft:blue_ice",
    "minecraft:frosted_ice",
}

ASCENDANT_LOOT_JSON_FILES = [
    "config/ascendant_loot/loot_policy.json",
    "config/ascendant_loot/structure_loot_tiers.json",
    "config/ascendant_loot/mob_drop_tiers.json",
    "config/ascendant_loot/boss_reward_tiers.json",
    "config/ascendant_loot/bounty_reward_pools.json",
    "config/ascendant_loot/loot_rarity_budget.json",
]

ASCENDANT_LOOT_LOW_TIER_CONTEXTS = {"village", "settlement", "minor_ruin", "mob"}
ASCENDANT_LOOT_BASIC_CONTEXTS = {"village", "settlement"}

ASCENDANT_RECIPE_JSON_FILES = [
    "config/ascendant_recipes/recipe_progression_policy.json",
    "config/ascendant_recipes/crafting_gate_registry.json",
    "config/ascendant_recipes/high_risk_recipes.json",
    "config/ascendant_recipes/candidate_recipe_rewrites.json",
]

ASCENDANT_MAGIC_JSON_FILES = [
    "config/ascendant_magic/spell_progression_registry.json",
    "config/ascendant_magic/magic_item_progression_registry.json",
    "config/ascendant_magic/school_region_policy.json",
    "config/ascendant_magic/magic_loot_policy.json",
    "config/ascendant_magic/magic_recipe_policy.json",
]

ASCENDANT_MAGIC_REQUIRED_DOCS = [
    "docs/ASCENDANT_MAGIC_PROGRESSION.md",
    "docs/SPELL_REGION_AND_RANK_INDEX.md",
    "docs/MAGIC_LOOT_AND_RECIPE_AUDIT.md",
]

ASCENDANT_BALANCE_JSON_FILES = [
    "config/ascendant_balance/gear_outliers.json",
    "config/ascendant_balance/rarity_review_queue.json",
    "config/ascendant_balance/stat_policy.json",
]

ASCENDANT_BALANCE_REQUIRED_DOCS = [
    "docs/GEAR_BALANCE_OUTLIER_REPORT.md",
    "docs/RARITY_CONSISTENCY_AUDIT.md",
    "docs/GEAR_PROGRESSion_RISK_REGISTER.md",
]

ASCENDANT_PLAYER_PROGRESSION_JSON_FILES = [
    "config/ascendant_progression/rank_requirement_matrix.json",
    "config/ascendant_progression/skill_unlock_policy.json",
    "config/ascendant_progression/region_progression_policy.json",
    "config/ascendant_progression/gear_rank_policy.json",
    "config/ascendant_progression/magic_rank_policy.json",
]

ASCENDANT_PLAYER_PROGRESSION_REQUIRED_DOCS = [
    "docs/ASCENDANT_PLAYER_PROGRESSION.md",
    "docs/GUILD_RANK_REQUIREMENT_MATRIX.md",
    "docs/SKILL_TREE_INTEGRATION_PLAN.md",
]

ASCENDANT_REQUIRED_RANKS = {"unranked", "e_rank", "d_rank", "c_rank", "b_rank", "a_rank", "s_rank"}

ASCENDANT_STRUCTURE_JSON_FILES = [
    "config/ascendant_structures/structure_tier_registry.json",
    "config/ascendant_structures/structure_registry.json",
    "config/ascendant_structures/structure_region_rules.json",
    "config/ascendant_structures/structure_vertical_layer_rules.json",
    "config/ascendant_structures/structure_density_policy.json",
    "config/ascendant_structures/structure_set_overrides.json",
    "config/ascendant_structures/structure_loot_linkage.json",
    "config/ascendant_structures/water_structure_policy.json",
    "config/ascendant_structures/sky_structure_policy.json",
    "config/ascendant_structures/sea_floor_structure_policy.json",
    "config/ascendant_structures/ship_structure_policy.json",
    "config/ascendant_structures/dungeon_structure_policy.json",
    "config/ascendant_structures/boss_structure_policy.json",
    "config/ascendant_structures/village_structure_policy.json",
    "config/ascendant_structures/structure_test_points.json",
    "config/ascendant_structures/structure_visual_review_route.json",
    "config/ascendant_structures/structure_review_priority_queue.json",
    "config/ascendant_structures/structure_visual_review_findings_latest.json",
    "config/ascendant_structures/structure_evidence_registry.json",
    "config/ascendant_structures/structure_classification_confidence.json",
    "config/ascendant_structures/manual_structure_observations.json",
    "config/ascendant_structures/live_structure_policy.json",
    "config/ascendant_structures/live_structure_manifest.json",
    "config/ascendant_structures/live_structure_results.json",
    "config/ascendant_structures/live_test_targets.json",
    "config/ascendant_structures/candidates/structure_land_placement_candidates.json",
    "config/ascendant_structures/candidates/structure_region_lock_candidates.json",
    "config/ascendant_structures/candidates/structure_density_candidates.json",
]

ASCENDANT_TRAVEL_JSON_FILES = [
    "config/ascendant_travel/road_policy.json",
    "config/ascendant_travel/bridge_policy.json",
    "config/ascendant_travel/river_crossing_policy.json",
    "config/ascendant_travel/travel_network_candidates.json",
]

ASCENDANT_TRAVEL_REQUIRED_DOCS = [
    "docs/ASCENDANT_TRAVEL_NETWORK_AUDIT.md",
    "docs/ROAD_BRIDGE_RIVER_FAILURES.md",
    "docs/TRAVEL_NETWORK_DESIGN_RULES.md",
]

ASCENDANT_ATMOSPHERE_JSON_FILES = [
    "config/ascendant_atmosphere/region_atmosphere.json",
    "config/ascendant_atmosphere/weather_policy.json",
    "config/ascendant_atmosphere/audio_policy.json",
    "config/ascendant_atmosphere/title_policy.json",
]

ASCENDANT_ATMOSPHERE_REQUIRED_DOCS = [
    "docs/ASCENDANT_REGIONAL_ATMOSPHERE.md",
    "docs/WEATHER_AND_SEASON_REGION_POLICY.md",
    "docs/BIOME_TITLE_AND_AUDIO_POLICY.md",
]

ASCENDANT_ATMOSPHERE_EXPECTED_REGIONS = {
    "hearthlands",
    "frostmarch",
    "sunreach",
    "verdant_coast",
    "stoneback_highlands",
    "north_east_marches",
    "north_west_marches",
    "south_east_wilds",
    "south_west_wilds",
    "outer_rim",
    "nether_front",
    "end_expanse",
}

ASCENDANT_ATMOSPHERE_WARM_REGIONS = {
    "hearthlands",
    "sunreach",
    "verdant_coast",
    "stoneback_highlands",
    "south_east_wilds",
    "south_west_wilds",
    "nether_front",
    "end_expanse",
}

ALLOWED_LOCAL_JARS = {
    "mods/ascendant-atlas-regions-0.1.0.jar",
    "mods/ascendant-nametags-0.1.0.jar",
}

ASCENDANT_GUILD_BAD_BOUNTY_TOKENS = {
    "abyss_blast",
    "air_combustion",
    "ancient_ancient",
    "arrow",
    "blast",
    "bomb",
    "breath",
    "controlled",
    "customnpcs:",
    "easy_npc:",
    "egg",
    "entity",
    "explosion",
    "geckolib:",
    "humancompanions:",
    "minion",
    "not_despawn",
    "orb",
    "phantom_halberd",
    "projectile",
    "spit",
    "summoned",
    "wave",
}

BATCH_E1_REQUIRED_METADATA = {
    "mods/in-control.pw.toml",
    "mods/mowzies-mobs.pw.toml",
    "mods/geckolib.pw.toml",
    "mods/alexs-mobs.pw.toml",
    "mods/citadel.pw.toml",
    "mods/guard-villagers.pw.toml",
    "mods/moogs-voyager-structures.pw.toml",
    "mods/moogs-structure-lib.pw.toml",
    "mods/yungs-extras.pw.toml",
    "mods/enhanced-boss-bars-mod.pw.toml",
}

BATCH_E2_REQUIRED_METADATA = {
    "mods/artifacts.pw.toml",
    "mods/bountiful.pw.toml",
    "mods/kambrik.pw.toml",
    "mods/loot-beams.pw.toml",
    "mods/loot-journal.pw.toml",
    "mods/fragmentum.pw.toml",
    "mods/villager-names-serilum.pw.toml",
    "mods/collective.pw.toml",
    "mods/loot-integrations.pw.toml",
    "mods/cupboard.pw.toml",
    "mods/curios.pw.toml",
}

BATCH_F_REQUIRED_METADATA = {
    "mods/irons-spells-n-spellbooks.pw.toml",
    "mods/irons-lib.pw.toml",
    "mods/borninchaos.pw.toml",
    "mods/aquamirae.pw.toml",
    "mods/obscure-api.pw.toml",
    "mods/enhanced-celestials.pw.toml",
    "mods/bossesrise.pw.toml",
    "mods/immersive-armors.pw.toml",
    "mods/spartan-shields.pw.toml",
    "mods/small-ships.pw.toml",
    "mods/snow-real-magic.pw.toml",
    "mods/handcrafted.pw.toml",
    "mods/macaws-bridges.pw.toml",
    "mods/macaws-fences-and-walls.pw.toml",
    "mods/corgilib.pw.toml",
    "mods/data-anchor.pw.toml",
    "mods/kiwi.pw.toml",
    "mods/resourceful-lib.pw.toml",
}

BATCH_G_REQUIRED_METADATA = {
    "mods/iceandfire-ce.pw.toml",
    "mods/jupiter.pw.toml",
    "mods/uranus.pw.toml",
    "mods/l_enders-cataclysm.pw.toml",
    "mods/lionfish-api.pw.toml",
    "mods/mariums-soulslike-weaponry.pw.toml",
    "mods/attributefix.pw.toml",
    "mods/projectile-damage-attribute.pw.toml",
    "mods/create.pw.toml",
    "mods/create-big-cannons.pw.toml",
    "mods/rpl.pw.toml",
    "mods/farmers-delight.pw.toml",
    "mods/create-structures-arise.pw.toml",
}

BATCH_H_REQUIRED_METADATA = {
    "mods/villages-and-pillages.pw.toml",
    "mods/mss-moogs-soaring-structures.pw.toml",
    "mods/mes-moogs-end-structures.pw.toml",
    "mods/auroras.pw.toml",
    "mods/beautiful-enchanted-books-mod-edition.pw.toml",
    "mods/perception.pw.toml",
    "mods/shatterbyte-lib.pw.toml",
    "mods/medieval-buildings-end-edition.pw.toml",
    "mods/medieval-buildings-nether-edition.pw.toml",
}

BATCH_J_REQUIRED_METADATA = {
    "mods/fantasy_armor.pw.toml",
    "mods/wavey-capes.pw.toml",
    "mods/xaeros-minimap.pw.toml",
    "mods/advancement-plaques.pw.toml",
    "mods/malfu-combat-animation.pw.toml",
    "resourcepacks/icon-xaeros.pw.toml",
    "resourcepacks/icon-xaeros-x-freshanimations.pw.toml",
    "resourcepacks/the-rename-compat-project.pw.toml",
    "resourcepacks/cubic-leaves.pw.toml",
    "resourcepacks/simply-swords-reforged.pw.toml",
    "resourcepacks/cubic-sun-moon.pw.toml",
    "resourcepacks/embellished-stone-advancements-plaques.pw.toml",
    "resourcepacks/stoneborn.pw.toml",
    "resourcepacks/excal.pw.toml",
    "resourcepacks/vanilla-exp.pw.toml",
}

BATCH_K_REQUIRED_METADATA = {
    "mods/titles.pw.toml",
    "mods/health-bar-plus.pw.toml",
    "mods/scaling-health.pw.toml",
    "mods/silent-lib.pw.toml",
    "mods/sound-physics-remastered.pw.toml",
    "mods/weather-storms-tornadoes.pw.toml",
    "mods/coroutil.pw.toml",
}

BATCH_L_REQUIRED_METADATA = {
    "mods/spawn-balance-utility.pw.toml",
    "mods/majruszs-progressive-difficulty.pw.toml",
    "mods/majrusz-library.pw.toml",
    "mods/improved-mobs.pw.toml",
    "mods/tenshilib.pw.toml",
    "mods/not-enough-animations.pw.toml",
    "mods/ambientsounds.pw.toml",
    "mods/creativecore.pw.toml",
    "mods/presence-footsteps-forge.pw.toml",
    "mods/biome-music.pw.toml",
    "resourcepacks/medieval-music.pw.toml",
}

BATCH_N_REQUIRED_METADATA = {
    "mods/kubejs.pw.toml",
    "mods/rhino.pw.toml",
    "mods/open-loader.pw.toml",
    "mods/almostunified.pw.toml",
    "mods/almost-unify-everything.pw.toml",
    "mods/polymorph.pw.toml",
    "mods/every-compat.pw.toml",
    "mods/moonlight.pw.toml",
    "mods/slice-and-dice.pw.toml",
    "mods/alexs-delight.pw.toml",
    "mods/integrated-villages.pw.toml",
    "mods/idas.pw.toml",
    "mods/integrated-api.pw.toml",
    "mods/supplementaries.pw.toml",
    "mods/quark.pw.toml",
    "mods/zeta.pw.toml",
}

BATCH_M_REQUIRED_METADATA = {
    "mods/sodium-dynamic-lights.pw.toml",
    "mods/sodium-options-api.pw.toml",
    "mods/amendments.pw.toml",
    "mods/macaws-lights-and-lamps.pw.toml",
    "mods/decorative-blocks.pw.toml",
}

WORLD_UI_POLISH_REQUIRED_METADATA = {
    "mods/fancymenu.pw.toml",
    "mods/konkrete.pw.toml",
    "mods/melody.pw.toml",
    "mods/watermedia.pw.toml",
    "mods/watermedia-binaries.pw.toml",
    "mods/immersive-ui.pw.toml",
}

UI_CUSTOMIZATION_TOOLING_REQUIRED_METADATA = {
    "mods/spiffyhud.pw.toml",
    "mods/drippy-loading-screen.pw.toml",
    "mods/item-borders.pw.toml",
    "mods/stylish-effects.pw.toml",
    "mods/overflowing-bars.pw.toml",
    "mods/appleskin.pw.toml",
    "mods/resource-pack-overrides.pw.toml",
}

GUILD_HUNTER_REQUIRED_METADATA = {
    "mods/customnpcs-unofficial.pw.toml",
    "mods/easy-npc-config-ui.pw.toml",
    "mods/easy-npc-core.pw.toml",
    "mods/ftb-library-forge.pw.toml",
    "mods/ftb-quests-forge.pw.toml",
    "mods/ftb-ranks-forge.pw.toml",
    "mods/ftb-teams-forge.pw.toml",
    "mods/human-companions.pw.toml",
    "mods/patchouli.pw.toml",
}

TRAVELERS_TITLES_REQUIRED_KEYS = {
    "travelerstitles.iceandfire.dread_land",
    "travelerstitles.irons_spellbooks.pocket_dimension",
    "travelerstitles.biome.iceandfire.dread_forest",
    "travelerstitles.biome.iceandfire.dread_plain",
    "travelerstitles.biome.terralith.red_oasis",
    "travelerstitles.biome.terralith.skylands_autumn",
    "travelerstitles.biome.terralith.yosemite_cliffs",
}


def rel(path: pathlib.Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def metadata_side(text: str) -> str:
    match = re.search(r'(?m)^side\s*=\s*"([^"]+)"', text)
    return match.group(1) if match else ""


def metadata_filename(text: str) -> str:
    match = re.search(r'(?m)^filename\s*=\s*"([^"]+)"', text)
    return match.group(1) if match else ""


def read_json(path: pathlib.Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def file_sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def directory_content_sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    for child in sorted((p for p in path.rglob("*") if p.is_file()), key=lambda p: p.relative_to(path).as_posix()):
        relative = child.relative_to(path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(child.read_bytes())
    return digest.hexdigest()


def atlas_is_cave_only_biome(biome_id: object) -> bool:
    biome = str(biome_id or "")
    return "/cave" in biome or biome.endswith("_caves")


def atlas_numeric(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def atlas_is_normal_surface_sample(sample: dict) -> bool:
    mode = str(sample.get("sample_mode") or "")
    if mode.startswith("fast_no_chunkgen"):
        return False
    return atlas_numeric(sample.get("surface_y")) is not None


def atlas_has_snow_rule_violation(sample: dict) -> bool:
    return (
        sample.get("snow_allowed") is True
        and str(sample.get("expected_biome_pool") or sample.get("climate_sector") or "") not in ASCENDANT_ATLAS_SNOW_ALLOWED_POOLS
        and str(sample.get("climate_sector") or "") not in ASCENDANT_ATLAS_SNOW_ALLOWED_POOLS
    )


def atlas_accepted_transition_edge_case(sample: dict) -> str | None:
    if str(sample.get("actual_biome_id") or "") != "minecraft:frozen_river":
        return None
    if str(sample.get("surface_block_id") or "") not in ASCENDANT_ATLAS_FROZEN_MOUNTAIN_RIVER_SURFACE_BLOCKS:
        return None
    if atlas_has_snow_rule_violation(sample):
        return None
    x_value = atlas_numeric(sample.get("x"))
    z_value = atlas_numeric(sample.get("z"))
    if x_value is None or z_value is None:
        return None
    if not (x_value < 0 and z_value < 0):
        return None
    if abs(z_value) < max(1000, abs(x_value) * 0.45):
        return None
    atlas_region = str(sample.get("atlas_region") or "")
    expected_pool = str(sample.get("expected_biome_pool") or "")
    climate_sector = str(sample.get("climate_sector") or "")
    if atlas_region not in {"stoneback_highlands", "north_west_marches"} and expected_pool not in {"west", "north_west"} and climate_sector not in {"west", "north_west"}:
        return None
    return ASCENDANT_ATLAS_ACCEPTED_TRANSITION_EDGE_CLASSIFICATION


def atlas_sample_label(sample: dict) -> str:
    return f"{sample.get('x', '?')},{sample.get('z', '?')}"


def atlas_sample_preview(samples: list[dict], limit: int = 5) -> str:
    labels = [atlas_sample_label(sample) for sample in samples[:limit]]
    suffix = "" if len(samples) <= limit else f", +{len(samples) - limit} more"
    return ", ".join(labels) + suffix


def ascendant_loot_preview(values: list[object], limit: int = 8) -> str:
    labels = [str(value) for value in values[:limit]]
    suffix = "" if len(values) <= limit else f", +{len(values) - limit} more"
    return ", ".join(labels) + suffix


def ascendant_loot_source_preview(sources: list[dict], limit: int = 5) -> str:
    return ascendant_loot_preview([source.get("source_id", "<unknown>") for source in sources], limit)


def ascendant_kubejs_item_ids() -> set[str]:
    item_ids: set[str] = set()
    startup_dir = ROOT / "kubejs/startup_scripts"
    if not startup_dir.exists():
        return item_ids
    for script_path in startup_dir.glob("*.js"):
        script_text = read_text(script_path)
        for match in re.finditer(r"event\.create\(['\"]([^'\"]+)['\"]\)", script_text):
            raw_id = match.group(1)
            item_ids.add(raw_id if ":" in raw_id else f"kubejs:{raw_id}")
    return item_ids


def validate_ascendant_loot_economy(errors: list[str], warnings: list[str], gear_items_by_id: dict[str, dict]) -> None:
    loot_reports: dict[str, object] = {}
    for report_name in ASCENDANT_LOOT_JSON_FILES:
        report_path = ROOT / report_name
        if not report_path.exists():
            continue
        try:
            report = read_json(report_path)
            if not isinstance(report, dict):
                errors.append(f"Ascendant loot JSON must be an object: {report_name}")
                continue
            loot_reports[report_name] = report
        except Exception as exc:
            errors.append(f"Ascendant loot JSON is invalid: {report_name}: {exc}")

    loot_policy = loot_reports.get("config/ascendant_loot/loot_policy.json")
    structure_tiers = loot_reports.get("config/ascendant_loot/structure_loot_tiers.json")
    boss_tiers = loot_reports.get("config/ascendant_loot/boss_reward_tiers.json")
    bounty_pools = loot_reports.get("config/ascendant_loot/bounty_reward_pools.json")

    known_item_ids = set(gear_items_by_id)
    known_item_ids.update(ascendant_kubejs_item_ids())
    if isinstance(loot_policy, dict):
        known_item_ids.update(str(item_id) for item_id in loot_policy.get("known_item_ids", []) if item_id)

    structure_ids: set[str] = set()
    structure_registry_path = ROOT / "config/ascendant_index/structure_registry.json"
    if structure_registry_path.exists():
        try:
            structure_registry = read_json(structure_registry_path)
            structure_ids = {
                str(entry.get("structure_id"))
                for entry in structure_registry.get("structures", [])
                if isinstance(entry, dict) and entry.get("structure_id")
            }
        except Exception as exc:
            errors.append(f"Structure registry JSON is invalid for loot validation: {exc}")

    boss_entity_ids: set[str] = set()
    mob_registry_path = ROOT / "config/ascendant_index/mob_registry.json"
    if mob_registry_path.exists():
        try:
            mob_registry = read_json(mob_registry_path)
            for entry in mob_registry.get("mobs", []):
                if not isinstance(entry, dict):
                    continue
                bounty_tier = str(entry.get("bounty_tier") or "")
                threat_tier = str(entry.get("threat_tier") or "")
                entity_id = str(entry.get("entity_id") or "")
                if entity_id and (bounty_tier in {"boss", "dragon"} or threat_tier in {"boss", "dragon_tier"}):
                    boss_entity_ids.add(entity_id)
        except Exception as exc:
            errors.append(f"Mob registry JSON is invalid for loot validation: {exc}")

    if isinstance(loot_policy, dict):
        loot_sources = loot_policy.get("loot_sources", [])
        if not isinstance(loot_sources, list) or not loot_sources:
            errors.append("config/ascendant_loot/loot_policy.json must contain loot_sources.")
            loot_sources = []
        object_sources = [source for source in loot_sources if isinstance(source, dict)]
        if len(object_sources) != len(loot_sources):
            errors.append("config/ascendant_loot/loot_policy.json loot_sources contains non-object entries.")

        summary = loot_policy.get("summary", {})
        if isinstance(summary, dict):
            invalid_json_count = int(summary.get("invalid_json_count", 0) or 0)
            invalid_json_sources = [
                entry
                for entry in summary.get("invalid_json", [])
                if isinstance(entry, dict)
            ]
            if invalid_json_count:
                warnings.append(
                    "Ascendant loot audit found malformed installed loot table JSON: "
                    f"{invalid_json_count} ({ascendant_loot_source_preview(invalid_json_sources)})"
                )

        low_tier_legendary_sources = [
            source
            for source in object_sources
            if str(source.get("loot_context")) in ASCENDANT_LOOT_LOW_TIER_CONTEXTS
            and any(
                ASCENDANT_RARITY_ORDER.get(str(item.get("rarity", "")).lower(), 0)
                >= ASCENDANT_RARITY_ORDER["legendary"]
                for item in source.get("observed_high_rarity_items", [])
                if isinstance(item, dict)
            )
        ]
        if low_tier_legendary_sources:
            warnings.append(
                "Ascendant loot economy found legendary/mythic/ascendant items in low-tier loot pools: "
                f"{len(low_tier_legendary_sources)} ({ascendant_loot_source_preview(low_tier_legendary_sources)})"
            )

        validation = loot_policy.get("validation", {})
        if isinstance(validation, dict):
            village_basic_high = validation.get("high_rarity_village_basic_sources", [])
            if isinstance(village_basic_high, list) and village_basic_high:
                preview = ascendant_loot_source_preview([entry for entry in village_basic_high if isinstance(entry, dict)])
                warnings.append(
                    "Ascendant loot economy found high-rarity gear in village/basic loot: "
                    f"{len(village_basic_high)} ({preview})"
                )

            noncanonical_material_outputs = validation.get("noncanonical_material_outputs", [])
            if isinstance(noncanonical_material_outputs, list) and noncanonical_material_outputs:
                preview = ascendant_loot_preview(
                    [
                        f"{entry.get('observed_item')} for {entry.get('material')}"
                        for entry in noncanonical_material_outputs
                        if isinstance(entry, dict)
                    ]
                )
                warnings.append(
                    "Ascendant loot economy found noncanonical material outputs from the materials registry: "
                    f"{len(noncanonical_material_outputs)} ({preview})"
                )

            bounty_missing_items = validation.get("bounty_missing_item_references", [])
            if isinstance(bounty_missing_items, list) and bounty_missing_items:
                warnings.append(
                    "Ascendant loot economy bounty reward pools reference missing items: "
                    f"{len(bounty_missing_items)} ({ascendant_loot_preview(bounty_missing_items)})"
                )

            reference_checks = validation.get("policy_reference_checks", {})
            if isinstance(reference_checks, dict):
                missing_structure_ids = reference_checks.get("missing_structure_ids", [])
                missing_item_ids = reference_checks.get("missing_item_ids", [])
                if isinstance(missing_structure_ids, list) and missing_structure_ids:
                    warnings.append(
                        "Ascendant loot policy references missing structure IDs: "
                        f"{len(missing_structure_ids)} ({ascendant_loot_preview(missing_structure_ids)})"
                    )
                if isinstance(missing_item_ids, list) and missing_item_ids:
                    warnings.append(
                        "Ascendant loot policy references missing item IDs: "
                        f"{len(missing_item_ids)} ({ascendant_loot_preview(missing_item_ids)})"
                    )

    if isinstance(structure_tiers, dict):
        structure_entries = structure_tiers.get("entries", [])
        if not isinstance(structure_entries, list) or not structure_entries:
            errors.append("config/ascendant_loot/structure_loot_tiers.json must contain entries.")
            structure_entries = []
        object_entries = [entry for entry in structure_entries if isinstance(entry, dict)]
        untiered_structures = [
            entry
            for entry in object_entries
            if not entry.get("reward_tier") or entry.get("reward_tier") == "review"
        ]
        if untiered_structures:
            warnings.append(
                "Ascendant structure loot has no assigned reward tier and needs manual review: "
                f"{len(untiered_structures)} "
                f"({ascendant_loot_preview([entry.get('structure_id') for entry in untiered_structures])})"
            )
        if structure_ids:
            missing_structure_refs = [
                str(entry.get("structure_id"))
                for entry in object_entries
                if entry.get("structure_id") and str(entry.get("structure_id")) not in structure_ids
            ]
            if missing_structure_refs:
                warnings.append(
                    "Ascendant structure loot tier policy references unknown structures: "
                    f"{len(missing_structure_refs)} ({ascendant_loot_preview(missing_structure_refs)})"
                )

    if isinstance(boss_tiers, dict):
        boss_entries = boss_tiers.get("bosses", [])
        if not isinstance(boss_entries, list):
            errors.append("config/ascendant_loot/boss_reward_tiers.json bosses must be a list.")
            boss_entries = []
        tiered_bosses = {
            str(entry.get("entity_id"))
            for entry in boss_entries
            if isinstance(entry, dict) and entry.get("entity_id")
        }
        missing_boss_tiers = sorted(boss_entity_ids - tiered_bosses)
        if missing_boss_tiers:
            warnings.append(
                "Ascendant boss reward tier policy is missing boss reward entries: "
                f"{len(missing_boss_tiers)} ({ascendant_loot_preview(missing_boss_tiers)})"
            )

    if isinstance(bounty_pools, dict):
        pool_entries = bounty_pools.get("entries", [])
        if not isinstance(pool_entries, list):
            errors.append("config/ascendant_loot/bounty_reward_pools.json entries must be a list.")
            pool_entries = []
        missing_bounty_items: set[str] = set()
        for pool in pool_entries:
            if not isinstance(pool, dict):
                continue
            for reward in pool.get("rewards", []):
                if not isinstance(reward, dict):
                    continue
                item_id = reward.get("item_id")
                if item_id and str(item_id) not in known_item_ids:
                    missing_bounty_items.add(str(item_id))
            for item_id in pool.get("currency_items", []):
                if item_id and str(item_id) not in known_item_ids:
                    missing_bounty_items.add(str(item_id))
        if missing_bounty_items:
            missing = sorted(missing_bounty_items)
            warnings.append(
                "Ascendant bounty reward pool references missing item IDs: "
                f"{len(missing)} ({ascendant_loot_preview(missing)})"
            )


def validate_ascendant_recipe_progression(errors: list[str], warnings: list[str], gear_items_by_id: dict[str, dict]) -> None:
    recipe_reports: dict[str, object] = {}
    for report_name in ASCENDANT_RECIPE_JSON_FILES:
        report_path = ROOT / report_name
        if not report_path.exists():
            continue
        try:
            report = read_json(report_path)
            if not isinstance(report, dict):
                errors.append(f"Ascendant recipe JSON must be an object: {report_name}")
                continue
            recipe_reports[report_name] = report
        except Exception as exc:
            errors.append(f"Ascendant recipe JSON is invalid: {report_name}: {exc}")

    recipe_policy = recipe_reports.get("config/ascendant_recipes/recipe_progression_policy.json")
    high_risk_report = recipe_reports.get("config/ascendant_recipes/high_risk_recipes.json")
    candidate_rewrites = recipe_reports.get("config/ascendant_recipes/candidate_recipe_rewrites.json")
    gate_registry = recipe_reports.get("config/ascendant_recipes/crafting_gate_registry.json")

    if isinstance(gate_registry, dict) and gate_registry.get("status") != "candidate_plan_only_no_hard_gates_enabled":
        warnings.append(
            "Ascendant crafting gate registry is no longer marked candidate-only; verify hard gates were approved."
        )

    if isinstance(recipe_policy, dict):
        recipe_entries = recipe_policy.get("major_recipe_entries", [])
        if not isinstance(recipe_entries, list) or not recipe_entries:
            errors.append("config/ascendant_recipes/recipe_progression_policy.json must contain major_recipe_entries.")
            recipe_entries = []
        object_entries = [entry for entry in recipe_entries if isinstance(entry, dict)]
        if len(object_entries) != len(recipe_entries):
            errors.append("config/ascendant_recipes/recipe_progression_policy.json major_recipe_entries contains non-object entries.")

        indexed_policy = recipe_policy.get("indexed_item_policy", [])
        if not isinstance(indexed_policy, list):
            errors.append("config/ascendant_recipes/recipe_progression_policy.json indexed_item_policy must be a list.")
            indexed_policy = []
        indexed_policy_ids = {
            str(entry.get("item_id"))
            for entry in indexed_policy
            if isinstance(entry, dict) and entry.get("item_id")
        }
        missing_indexed_policy = sorted(set(gear_items_by_id) - indexed_policy_ids)
        if missing_indexed_policy:
            warnings.append(
                "Ascendant recipe progression is missing recipe policy for indexed gear/magic/relic items: "
                f"{len(missing_indexed_policy)} ({ascendant_loot_preview(missing_indexed_policy)})"
            )

        validation = recipe_policy.get("validation", {})
        if isinstance(validation, dict):
            high_rarity_low_tier = validation.get("high_rarity_low_tier_recipes", [])
            if isinstance(high_rarity_low_tier, list) and high_rarity_low_tier:
                warnings.append(
                    "Ascendant recipe progression found high-rarity items with low-tier recipes: "
                    f"{len(high_rarity_low_tier)} "
                    f"({ascendant_loot_preview([entry.get('recipe_id') for entry in high_rarity_low_tier if isinstance(entry, dict)])})"
                )

            duplicate_materials = validation.get("noncanonical_duplicate_material_recipes", [])
            if isinstance(duplicate_materials, list) and duplicate_materials:
                warnings.append(
                    "Ascendant recipe progression found noncanonical duplicate-material recipes: "
                    f"{len(duplicate_materials)} "
                    f"({ascendant_loot_preview([entry.get('recipe_id') for entry in duplicate_materials if isinstance(entry, dict)])})"
                )

            missing_item_refs = validation.get("missing_item_references", [])
            if isinstance(missing_item_refs, list) and missing_item_refs:
                warnings.append(
                    "Ascendant recipe progression found recipe references to missing item IDs: "
                    f"{len(missing_item_refs)} "
                    f"({ascendant_loot_preview([entry.get('item_id') for entry in missing_item_refs if isinstance(entry, dict)])})"
                )

            rarity_contradictions = validation.get("rarity_contradictions", [])
            if isinstance(rarity_contradictions, list) and rarity_contradictions:
                warnings.append(
                    "Ascendant recipe progression found recipe output rarity contradictions with gear_registry: "
                    f"{len(rarity_contradictions)} "
                    f"({ascendant_loot_preview([entry.get('item_id') for entry in rarity_contradictions if isinstance(entry, dict)])})"
                )

            unreviewed_candidates = validation.get("unreviewed_rewrite_candidates", [])
            if isinstance(unreviewed_candidates, list) and unreviewed_candidates:
                warnings.append(
                    "Ascendant recipe rewrite candidates are unreviewed and must remain disabled: "
                    f"{len(unreviewed_candidates)} "
                    f"({ascendant_loot_preview([entry.get('recipe_id') for entry in unreviewed_candidates if isinstance(entry, dict)])})"
                )

    if isinstance(high_risk_report, dict):
        summary = high_risk_report.get("summary", {})
        if isinstance(summary, dict):
            high_risk_count = int(summary.get("high_risk_count", 0) or 0)
            if high_risk_count:
                warnings.append(
                    "Ascendant high-risk recipe report requires manual review before enabling rewrites: "
                    f"{high_risk_count}"
                )

    if isinstance(candidate_rewrites, dict):
        if candidate_rewrites.get("enabled_candidates", 0) != 0:
            warnings.append(
                "Ascendant candidate recipe rewrites must not be enabled without explicit approval."
            )
        candidates = candidate_rewrites.get("candidates", [])
        if isinstance(candidates, list):
            enabled_candidates = [
                candidate
                for candidate in candidates
                if isinstance(candidate, dict) and candidate.get("enabled") is True
            ]
            if enabled_candidates:
                warnings.append(
                    "Ascendant recipe rewrite candidate entries are marked enabled: "
                    f"{len(enabled_candidates)} "
                    f"({ascendant_loot_preview([entry.get('recipe_id') for entry in enabled_candidates])})"
                )
        else:
            errors.append("config/ascendant_recipes/candidate_recipe_rewrites.json candidates must be a list.")


def validate_ascendant_magic_progression(errors: list[str], warnings: list[str], gear_items_by_id: dict[str, dict]) -> None:
    magic_reports: dict[str, object] = {}
    for report_name in ASCENDANT_MAGIC_JSON_FILES:
        report_path = ROOT / report_name
        if not report_path.exists():
            continue
        try:
            report = read_json(report_path)
            if not isinstance(report, dict):
                errors.append(f"Ascendant magic JSON must be an object: {report_name}")
                continue
            magic_reports[report_name] = report
        except Exception as exc:
            errors.append(f"Ascendant magic JSON is invalid: {report_name}: {exc}")

    for doc_name in ASCENDANT_MAGIC_REQUIRED_DOCS:
        if any((ROOT / path).exists() for path in ASCENDANT_MAGIC_JSON_FILES) and not (ROOT / doc_name).exists():
            warnings.append(f"Ascendant magic policy exists but is not documented: {doc_name}")

    def validation_list(report: object, key: str) -> list[object]:
        if not isinstance(report, dict):
            return []
        validation = report.get("validation", {})
        if not isinstance(validation, dict):
            return []
        values = validation.get(key, [])
        return values if isinstance(values, list) else []

    spell_registry = magic_reports.get("config/ascendant_magic/spell_progression_registry.json")
    item_registry = magic_reports.get("config/ascendant_magic/magic_item_progression_registry.json")
    school_policy = magic_reports.get("config/ascendant_magic/school_region_policy.json")
    loot_policy = magic_reports.get("config/ascendant_magic/magic_loot_policy.json")
    recipe_policy = magic_reports.get("config/ascendant_magic/magic_recipe_policy.json")

    indexed_spells: set[str] = set()
    indexed_magic_items: set[str] = set()
    gear_registry_path = ROOT / "config/ascendant_index/gear_registry.json"
    if gear_registry_path.exists():
        try:
            gear_registry = read_json(gear_registry_path)
            if isinstance(gear_registry, dict):
                indexed_spells = {
                    str(entry.get("id"))
                    for entry in gear_registry.get("spells", [])
                    if isinstance(entry, dict) and entry.get("id")
                }
                indexed_magic_items = {
                    str(entry.get("id"))
                    for entry in gear_registry.get("magic_items", [])
                    if isinstance(entry, dict) and entry.get("id")
                }
        except Exception as exc:
            errors.append(f"Gear registry JSON is invalid for magic validation: {exc}")

    policy_spell_ids: set[str] = set()
    policy_magic_item_ids: set[str] = set()

    def validate_policy_entries(report: object, key: str, label: str) -> set[str]:
        seen_ids: set[str] = set()
        if not isinstance(report, dict):
            return seen_ids
        if report.get("status") != "audit_control_scaffold_only_no_hard_gates":
            warnings.append(f"Ascendant magic {label} registry is not marked audit/control/no-hard-gates.")
        entries = report.get(key, [])
        if not isinstance(entries, list) or not entries:
            errors.append(f"config/ascendant_magic/{label}_progression_registry.json must contain {key}.")
            return seen_ids
        object_entries = [entry for entry in entries if isinstance(entry, dict)]
        if len(object_entries) != len(entries):
            errors.append(f"config/ascendant_magic/{label}_progression_registry.json {key} contains non-object entries.")
        for entry in object_entries:
            item_id = str(entry.get("id") or "")
            if item_id:
                seen_ids.add(item_id)
            missing_fields = [
                field
                for field in (
                    "id",
                    "school",
                    "rarity",
                    "guild_rank_tier",
                    "atlas_region_affinity",
                    "allowed_loot_tier",
                    "recipe_tier_if_craftable",
                    "intended_acquisition_method",
                    "progression_band",
                )
                if not entry.get(field)
            ]
            if missing_fields:
                warnings.append(
                    f"Ascendant magic {label} entry {item_id or '<missing>'} is missing progression fields: "
                    f"{', '.join(missing_fields)}"
                )
            affinity = entry.get("atlas_region_affinity", [])
            if not isinstance(affinity, list) or not affinity:
                warnings.append(f"Ascendant magic {label} entry lacks Atlas region affinity: {item_id or '<missing>'}")
            acquisition = entry.get("intended_acquisition_method", [])
            if not isinstance(acquisition, list) or not acquisition:
                warnings.append(f"Ascendant magic {label} entry lacks acquisition method: {item_id or '<missing>'}")
            if item_id and item_id not in gear_items_by_id and item_id not in indexed_spells and item_id not in indexed_magic_items:
                warnings.append(f"Ascendant magic {label} policy references missing item/spell ID: {item_id}")
        missing_rank_region = validation_list(report, "missing_rank_or_region_tier")
        if missing_rank_region:
            warnings.append(
                f"Ascendant magic {label} entries lack rank or region tier: "
                f"{len(missing_rank_region)} ({ascendant_loot_preview(missing_rank_region)})"
            )
        missing_acquisition = validation_list(report, "missing_acquisition_method")
        if missing_acquisition:
            warnings.append(
                f"Ascendant magic {label} entries lack acquisition method: "
                f"{len(missing_acquisition)} ({ascendant_loot_preview(missing_acquisition)})"
            )
        return seen_ids

    policy_spell_ids = validate_policy_entries(spell_registry, "spells", "spell")
    policy_magic_item_ids = validate_policy_entries(item_registry, "magic_items", "magic_item")

    missing_spell_policy = sorted(indexed_spells - policy_spell_ids)
    if missing_spell_policy:
        warnings.append(
            "Ascendant magic progression is missing indexed spell policy rows: "
            f"{len(missing_spell_policy)} ({ascendant_loot_preview(missing_spell_policy)})"
        )
    missing_magic_item_policy = sorted(indexed_magic_items - policy_magic_item_ids)
    if missing_magic_item_policy:
        warnings.append(
            "Ascendant magic progression is missing indexed magic-item policy rows: "
            f"{len(missing_magic_item_policy)} ({ascendant_loot_preview(missing_magic_item_policy)})"
        )

    known_magic_ids = indexed_spells | indexed_magic_items | policy_spell_ids | policy_magic_item_ids
    if isinstance(school_policy, dict):
        if school_policy.get("status") != "audit_control_scaffold_only_no_hard_gates":
            warnings.append("Ascendant magic school-region policy is not marked audit/control/no-hard-gates.")
        schools = school_policy.get("schools", [])
        if not isinstance(schools, list) or not schools:
            errors.append("config/ascendant_magic/school_region_policy.json must contain schools.")
            schools = []
        referenced_ids: set[str] = set()
        for school in [entry for entry in schools if isinstance(entry, dict)]:
            school_id = str(school.get("school") or "")
            if not school_id:
                warnings.append("Ascendant magic school policy contains a school without an ID.")
            if not school.get("atlas_region_affinity"):
                warnings.append(f"Ascendant magic school policy lacks Atlas region affinity: {school_id or '<missing>'}")
            for item_id in list(school.get("spells", []) or []) + list(school.get("magic_items", []) or []):
                if item_id:
                    referenced_ids.add(str(item_id))
        missing_refs = sorted(referenced_ids - known_magic_ids)
        reported_missing = validation_list(school_policy, "policy_references_missing_spells_or_items")
        if reported_missing:
            missing_refs = sorted(set(missing_refs) | {str(value) for value in reported_missing})
        if missing_refs:
            warnings.append(
                "Ascendant magic school-region policy references missing spells/items: "
                f"{len(missing_refs)} ({ascendant_loot_preview(missing_refs)})"
            )
        unassigned = validation_list(school_policy, "unassigned_spells_or_items")
        if unassigned:
            warnings.append(
                "Ascendant magic school-region policy leaves spells/items unassigned: "
                f"{len(unassigned)} ({ascendant_loot_preview(unassigned)})"
            )

    if isinstance(loot_policy, dict):
        if loot_policy.get("status") != "audit_control_scaffold_only_no_loot_rewrites":
            warnings.append("Ascendant magic loot policy is not marked no loot rewrites.")
        sources = loot_policy.get("magic_loot_sources", [])
        if not isinstance(sources, list):
            errors.append("config/ascendant_magic/magic_loot_policy.json magic_loot_sources must be a list.")
        high_tier_low = validation_list(loot_policy, "high_tier_spell_in_low_tier_loot")
        if high_tier_low:
            warnings.append(
                "Ascendant magic loot policy found high-tier magic in low-tier loot: "
                f"{len(high_tier_low)} "
                f"({ascendant_loot_preview([entry.get('id') for entry in high_tier_low if isinstance(entry, dict)])})"
            )

    if isinstance(recipe_policy, dict):
        if recipe_policy.get("status") != "audit_candidate_scaffold_only_no_hard_gates":
            warnings.append("Ascendant magic recipe policy is not marked candidate/no-hard-gates.")
        entries = recipe_policy.get("magic_recipe_entries", [])
        if not isinstance(entries, list):
            errors.append("config/ascendant_magic/magic_recipe_policy.json magic_recipe_entries must be a list.")
        high_tier_low = validation_list(recipe_policy, "high_tier_spell_low_tier_recipes")
        if high_tier_low:
            warnings.append(
                "Ascendant magic recipe policy found high-tier spell or magic recipes that need gating/review: "
                f"{len(high_tier_low)} "
                f"({ascendant_loot_preview([entry.get('recipe_id') for entry in high_tier_low if isinstance(entry, dict)])})"
            )
        noncanonical = validation_list(recipe_policy, "spell_recipe_noncanonical_materials")
        if noncanonical:
            warnings.append(
                "Ascendant magic recipe policy found spell recipes using noncanonical material paths: "
                f"{len(noncanonical)} "
                f"({ascendant_loot_preview([entry.get('recipe_id') for entry in noncanonical if isinstance(entry, dict)])})"
            )
        unreviewed = validation_list(recipe_policy, "unreviewed_magic_recipe_candidates")
        if unreviewed:
            warnings.append(
                "Ascendant magic recipe candidates remain unreviewed and must stay disabled: "
                f"{len(unreviewed)} "
                f"({ascendant_loot_preview([entry.get('recipe_id') for entry in unreviewed if isinstance(entry, dict)])})"
            )


def validate_ascendant_balance(errors: list[str], warnings: list[str], gear_items_by_id: dict[str, dict]) -> None:
    balance_reports: dict[str, object] = {}
    for report_name in ASCENDANT_BALANCE_JSON_FILES:
        report_path = ROOT / report_name
        if not report_path.exists():
            continue
        try:
            report = read_json(report_path)
            if not isinstance(report, dict):
                errors.append(f"Ascendant balance JSON must be an object: {report_name}")
                continue
            balance_reports[report_name] = report
        except Exception as exc:
            errors.append(f"Ascendant balance JSON is invalid: {report_name}: {exc}")

    for doc_name in ASCENDANT_BALANCE_REQUIRED_DOCS:
        if any((ROOT / path).exists() for path in ASCENDANT_BALANCE_JSON_FILES) and not (ROOT / doc_name).exists():
            warnings.append(f"Ascendant balance policy exists but is not documented: {doc_name}")

    def validation_list(report: object, key: str) -> list[object]:
        if not isinstance(report, dict):
            return []
        validation = report.get("validation", {})
        if not isinstance(validation, dict):
            return []
        values = validation.get(key, [])
        return values if isinstance(values, list) else []

    def validation_bool(report: object, key: str) -> bool:
        if not isinstance(report, dict):
            return False
        validation = report.get("validation", {})
        if not isinstance(validation, dict):
            return False
        return bool(validation.get(key))

    def validation_count(report: object, key: str) -> int | None:
        if not isinstance(report, dict):
            return None
        validation = report.get("validation", {})
        if not isinstance(validation, dict):
            return None
        value = validation.get(key)
        if isinstance(value, bool):
            return None
        if isinstance(value, int):
            return value
        return None

    stat_policy = balance_reports.get("config/ascendant_balance/stat_policy.json")
    outlier_report = balance_reports.get("config/ascendant_balance/gear_outliers.json")
    review_queue = balance_reports.get("config/ascendant_balance/rarity_review_queue.json")

    known_item_ids = set(gear_items_by_id)
    policy_ids: set[str] = set()

    if isinstance(stat_policy, dict):
        if stat_policy.get("status") != "audit_control_scaffold_only_no_stat_changes":
            warnings.append("Ascendant stat policy is not marked audit/control/no-stat-changes.")
        entries = stat_policy.get("balance_policy_entries", [])
        if not isinstance(entries, list) or not entries:
            errors.append("config/ascendant_balance/stat_policy.json must contain balance_policy_entries.")
            entries = []
        object_entries = [entry for entry in entries if isinstance(entry, dict)]
        if len(object_entries) != len(entries):
            errors.append("config/ascendant_balance/stat_policy.json balance_policy_entries contains non-object entries.")
        missing_progression_entries: list[str] = []
        missing_rarity_entries: list[str] = []
        missing_rank_entries: list[str] = []
        for entry in object_entries:
            item_id = str(entry.get("item_id") or "")
            if item_id:
                policy_ids.add(item_id)
            if not entry.get("progression_tier"):
                missing_progression_entries.append(item_id or "<missing item_id>")
            if not entry.get("rarity"):
                missing_rarity_entries.append(item_id or "<missing item_id>")
            if not entry.get("guild_rank_tier"):
                missing_rank_entries.append(item_id or "<missing item_id>")
        if missing_progression_entries:
            warnings.append(
                "Ascendant balance policy has items with no progression tier: "
                f"{len(missing_progression_entries)} ({ascendant_loot_preview(missing_progression_entries)})"
            )
        if missing_rarity_entries:
            warnings.append(
                "Ascendant balance policy has items with no rarity: "
                f"{len(missing_rarity_entries)} ({ascendant_loot_preview(missing_rarity_entries)})"
            )
        if missing_rank_entries:
            warnings.append(
                "Ascendant balance policy has items with no Guild rank tier: "
                f"{len(missing_rank_entries)} ({ascendant_loot_preview(missing_rank_entries)})"
            )

        missing_policy = sorted(known_item_ids - policy_ids)
        unknown_policy = sorted(policy_ids - known_item_ids)
        generated_missing_policy = [str(value) for value in validation_list(stat_policy, "gear_index_missing_balance_policy")]
        generated_unknown_policy = [str(value) for value in validation_list(stat_policy, "balance_policy_unknown_item_ids")]
        if generated_missing_policy:
            missing_policy = sorted(set(missing_policy) | set(generated_missing_policy))
        if generated_unknown_policy:
            unknown_policy = sorted(set(unknown_policy) | set(generated_unknown_policy))
        if missing_policy:
            warnings.append(
                "Ascendant gear index items are missing balance policy rows: "
                f"{len(missing_policy)} ({ascendant_loot_preview(missing_policy)})"
            )
        if unknown_policy:
            warnings.append(
                "Ascendant balance policy references missing gear_registry item IDs: "
                f"{len(unknown_policy)} ({ascendant_loot_preview(unknown_policy)})"
            )

        generated_missing_progression = [str(value) for value in validation_list(stat_policy, "items_without_progression_tier")]
        if generated_missing_progression:
            warnings.append(
                "Ascendant balance validation found items without progression tier: "
                f"{len(generated_missing_progression)} ({ascendant_loot_preview(generated_missing_progression)})"
            )

        high_stat_low_rarity = [str(value) for value in validation_list(stat_policy, "high_stat_low_rarity")]
        if high_stat_low_rarity:
            warnings.append(
                "Ascendant balance found high-stat items with low rarity or low rank placement: "
                f"{len(high_stat_low_rarity)} ({ascendant_loot_preview(high_stat_low_rarity)})"
            )

        low_stat_high_rarity = [str(value) for value in validation_list(stat_policy, "low_stat_high_rarity_no_special_ability_note")]
        if low_stat_high_rarity:
            warnings.append(
                "Ascendant balance found low-stat high-rarity items with no special ability note: "
                f"{len(low_stat_high_rarity)} ({ascendant_loot_preview(low_stat_high_rarity)})"
            )

        registry_unique_count = validation_count(stat_policy, "gear_registry_unique_item_ids")
        if registry_unique_count is not None and known_item_ids and registry_unique_count != len(known_item_ids):
            warnings.append(
                "Ascendant balance stat policy appears stale against gear_registry unique item count: "
                f"policy={registry_unique_count}, current={len(known_item_ids)}"
            )
        if validation_bool(stat_policy, "outlier_list_stale"):
            warnings.append("Ascendant balance outlier list is marked stale against gear_registry.")

    if isinstance(outlier_report, dict):
        if outlier_report.get("status") != "audit_outlier_report_only_no_stat_changes":
            warnings.append("Ascendant gear outlier report is not marked audit-only/no-stat-changes.")
        outliers = outlier_report.get("outliers", [])
        if not isinstance(outliers, list):
            errors.append("config/ascendant_balance/gear_outliers.json outliers must be a list.")
            outliers = []
        object_outliers = [entry for entry in outliers if isinstance(entry, dict)]
        if len(object_outliers) != len(outliers):
            errors.append("config/ascendant_balance/gear_outliers.json outliers contains non-object entries.")
        outlier_ids = {
            str(entry.get("item_id"))
            for entry in object_outliers
            if entry.get("item_id")
        }
        unknown_outliers = sorted(outlier_ids - known_item_ids)
        if unknown_outliers:
            warnings.append(
                "Ascendant gear outlier report references missing gear_registry item IDs: "
                f"{len(unknown_outliers)} ({ascendant_loot_preview(unknown_outliers)})"
            )
        registry_unique_count = validation_count(outlier_report, "gear_registry_unique_item_ids")
        if registry_unique_count is not None and known_item_ids and registry_unique_count != len(known_item_ids):
            warnings.append(
                "Ascendant gear outlier report appears stale against gear_registry unique item count: "
                f"report={registry_unique_count}, current={len(known_item_ids)}"
            )
        generated_outlier_ids = {str(value) for value in validation_list(outlier_report, "outlier_item_ids")}
        if generated_outlier_ids and generated_outlier_ids != outlier_ids:
            warnings.append("Ascendant gear outlier validation IDs do not match the outlier entry IDs; regenerate the report.")

    if isinstance(review_queue, dict):
        if review_queue.get("status") != "audit_review_queue_only_no_rarity_regeneration":
            warnings.append("Ascendant rarity review queue is not marked no-rarity-regeneration.")
        entries = review_queue.get("review_entries", [])
        if not isinstance(entries, list):
            errors.append("config/ascendant_balance/rarity_review_queue.json review_entries must be a list.")
            entries = []
        object_entries = [entry for entry in entries if isinstance(entry, dict)]
        if len(object_entries) != len(entries):
            errors.append("config/ascendant_balance/rarity_review_queue.json review_entries contains non-object entries.")
        review_ids = {
            str(entry.get("item_id"))
            for entry in object_entries
            if entry.get("item_id")
        }
        unknown_review_ids = sorted(review_ids - known_item_ids)
        if unknown_review_ids:
            warnings.append(
                "Ascendant rarity review queue references missing gear_registry item IDs: "
                f"{len(unknown_review_ids)} ({ascendant_loot_preview(unknown_review_ids)})"
            )
        registry_unique_count = validation_count(review_queue, "gear_registry_unique_item_ids")
        if registry_unique_count is not None and known_item_ids and registry_unique_count != len(known_item_ids):
            warnings.append(
                "Ascendant rarity review queue appears stale against gear_registry unique item count: "
                f"queue={registry_unique_count}, current={len(known_item_ids)}"
            )
        generated_review_ids = {str(value) for value in validation_list(review_queue, "review_item_ids")}
        if generated_review_ids and generated_review_ids != review_ids:
            warnings.append("Ascendant rarity review validation IDs do not match review entries; regenerate the queue.")


def validate_ascendant_player_progression(errors: list[str], warnings: list[str]) -> None:
    progression_reports: dict[str, object] = {}
    for report_name in ASCENDANT_PLAYER_PROGRESSION_JSON_FILES:
        report_path = ROOT / report_name
        if not report_path.exists():
            continue
        try:
            report = read_json(report_path)
            if not isinstance(report, dict):
                errors.append(f"Ascendant player progression JSON must be an object: {report_name}")
                continue
            progression_reports[report_name] = report
        except Exception as exc:
            errors.append(f"Ascendant player progression JSON is invalid: {report_name}: {exc}")

    for doc_name in ASCENDANT_PLAYER_PROGRESSION_REQUIRED_DOCS:
        if any((ROOT / path).exists() for path in ASCENDANT_PLAYER_PROGRESSION_JSON_FILES) and not (ROOT / doc_name).exists():
            warnings.append(f"Ascendant player progression policy exists but is not documented: {doc_name}")

    def validation_list(report: object, key: str) -> list[object]:
        if not isinstance(report, dict):
            return []
        validation = report.get("validation", {})
        if not isinstance(validation, dict):
            return []
        values = validation.get(key, [])
        return values if isinstance(values, list) else []

    def known_atlas_regions() -> set[str]:
        path = ROOT / "config/ascendant_atlas/regions.json"
        if not path.exists():
            return set()
        try:
            atlas = read_json(path)
        except Exception as exc:
            errors.append(f"Atlas regions JSON is invalid for progression validation: {exc}")
            return set()
        if not isinstance(atlas, dict):
            return set()
        return {
            str(entry.get("id"))
            for entry in atlas.get("regions", [])
            if isinstance(entry, dict) and entry.get("id")
        }

    def known_skill_ids() -> set[str]:
        path = ROOT / "config/puffish_skills/categories/ascendant/definitions.json"
        if not path.exists():
            return set()
        try:
            definitions = read_json(path)
        except Exception as exc:
            errors.append(f"Puffish skill definitions JSON is invalid for progression validation: {exc}")
            return set()
        return set(definitions) if isinstance(definitions, dict) else set()

    def known_gear_rarities() -> set[str]:
        path = ROOT / "config/ascendant_index/gear_registry.json"
        if not path.exists():
            return set(ASCENDANT_RARITY_ORDER)
        try:
            registry = read_json(path)
        except Exception as exc:
            errors.append(f"Gear registry JSON is invalid for progression validation: {exc}")
            return set(ASCENDANT_RARITY_ORDER)
        rarities = {
            str(entry.get("id"))
            for entry in registry.get("rarity_tiers", [])
            if isinstance(entry, dict) and entry.get("id")
        } if isinstance(registry, dict) else set()
        return rarities or set(ASCENDANT_RARITY_ORDER)

    def observed_magic_tiers() -> set[str]:
        tiers: set[str] = set()
        for report_name, key in [
            ("config/ascendant_magic/spell_progression_registry.json", "spells"),
            ("config/ascendant_magic/magic_item_progression_registry.json", "magic_items"),
        ]:
            path = ROOT / report_name
            if not path.exists():
                continue
            try:
                registry = read_json(path)
            except Exception as exc:
                errors.append(f"Ascendant magic registry JSON is invalid for progression validation: {report_name}: {exc}")
                continue
            if not isinstance(registry, dict):
                continue
            for entry in registry.get(key, []):
                if not isinstance(entry, dict):
                    continue
                for tier_key in ("allowed_loot_tier", "recipe_tier_if_craftable"):
                    if entry.get(tier_key):
                        tiers.add(str(entry.get(tier_key)))
        return tiers

    atlas_regions = known_atlas_regions()
    skill_ids = known_skill_ids()
    gear_rarities = known_gear_rarities()
    magic_tiers = observed_magic_tiers()

    rank_matrix = progression_reports.get("config/ascendant_progression/rank_requirement_matrix.json")
    skill_policy = progression_reports.get("config/ascendant_progression/skill_unlock_policy.json")
    region_policy = progression_reports.get("config/ascendant_progression/region_progression_policy.json")
    gear_policy = progression_reports.get("config/ascendant_progression/gear_rank_policy.json")
    magic_policy = progression_reports.get("config/ascendant_progression/magic_rank_policy.json")

    if isinstance(rank_matrix, dict):
        if rank_matrix.get("status") != "audit_control_scaffold_only_no_hard_gates":
            warnings.append("Ascendant rank requirement matrix is not marked no-hard-gates.")
        ranks = rank_matrix.get("ranks", [])
        if not isinstance(ranks, list) or not ranks:
            errors.append("config/ascendant_progression/rank_requirement_matrix.json must contain ranks.")
            ranks = []
        object_ranks = [entry for entry in ranks if isinstance(entry, dict)]
        if len(object_ranks) != len(ranks):
            errors.append("config/ascendant_progression/rank_requirement_matrix.json ranks contains non-object entries.")
        rank_ids = {str(entry.get("rank_id")) for entry in object_ranks if entry.get("rank_id")}
        missing_ranks = sorted(ASCENDANT_REQUIRED_RANKS - rank_ids)
        generated_missing_ranks = [str(value) for value in validation_list(rank_matrix, "missing_ranks")]
        if generated_missing_ranks:
            missing_ranks = sorted(set(missing_ranks) | set(generated_missing_ranks))
        if missing_ranks:
            warnings.append(
                "Ascendant rank requirement matrix is missing ranks: "
                f"{len(missing_ranks)} ({ascendant_loot_preview(missing_ranks)})"
            )
        referenced_regions = {
            str(region_id)
            for entry in object_ranks
            for region_id in (entry.get("recommended_regions", []) or [])
        }
        missing_regions = sorted(referenced_regions - atlas_regions)
        generated_missing_regions = [str(value) for value in validation_list(rank_matrix, "rank_policy_references_missing_regions")]
        if generated_missing_regions:
            missing_regions = sorted(set(missing_regions) | set(generated_missing_regions))
        if missing_regions:
            warnings.append(
                "Ascendant rank policy references missing Atlas regions: "
                f"{len(missing_regions)} ({ascendant_loot_preview(missing_regions)})"
            )

    if isinstance(skill_policy, dict):
        if skill_policy.get("status") != "audit_control_scaffold_only_no_hard_skill_gates":
            warnings.append("Ascendant skill unlock policy is not marked no-hard-skill-gates.")
        milestones = skill_policy.get("rank_skill_milestones", [])
        if not isinstance(milestones, list) or not milestones:
            errors.append("config/ascendant_progression/skill_unlock_policy.json must contain rank_skill_milestones.")
            milestones = []
        object_milestones = [entry for entry in milestones if isinstance(entry, dict)]
        referenced_skills = {
            str(skill_id)
            for entry in object_milestones
            for skill_id in (entry.get("referenced_skill_ids", []) or [])
        }
        missing_skills = sorted(referenced_skills - skill_ids)
        generated_missing_skills = [str(value) for value in validation_list(skill_policy, "skill_unlock_policy_references_missing_skill_ids")]
        generated_missing_skills.extend(str(value) for value in validation_list(skill_policy, "missing_skill_ids"))
        if generated_missing_skills:
            missing_skills = sorted(set(missing_skills) | set(generated_missing_skills))
        if missing_skills:
            warnings.append(
                "Ascendant skill unlock policy references missing Puffish skill IDs: "
                f"{len(missing_skills)} ({ascendant_loot_preview(missing_skills)})"
            )

    if isinstance(region_policy, dict):
        if region_policy.get("status") != "audit_control_scaffold_only_no_region_locks":
            warnings.append("Ascendant region progression policy is not marked no-region-locks.")
        readiness = region_policy.get("region_readiness", [])
        if not isinstance(readiness, list) or not readiness:
            errors.append("config/ascendant_progression/region_progression_policy.json must contain region_readiness.")
            readiness = []
        object_readiness = [entry for entry in readiness if isinstance(entry, dict)]
        region_ids = {str(entry.get("region_id")) for entry in object_readiness if entry.get("region_id")}
        missing_regions = sorted(region_ids - atlas_regions)
        generated_missing_regions = [str(value) for value in validation_list(region_policy, "rank_policy_references_missing_regions")]
        generated_missing_regions.extend(str(value) for value in validation_list(region_policy, "policy_references_missing_regions"))
        if generated_missing_regions:
            missing_regions = sorted(set(missing_regions) | set(generated_missing_regions))
        if missing_regions:
            warnings.append(
                "Ascendant region progression policy references missing Atlas regions: "
                f"{len(missing_regions)} ({ascendant_loot_preview(missing_regions)})"
            )
        starter_threat_excess = [str(value) for value in validation_list(region_policy, "starter_region_threat_excess")]
        for entry in object_readiness:
            ranks = {str(value) for value in (entry.get("recommended_ranks", []) or [])}
            threat = entry.get("recommended_mob_threat_range", [])
            if ranks & {"unranked", "e_rank"} and isinstance(threat, list) and len(threat) >= 2:
                try:
                    if int(threat[1]) > 2:
                        starter_threat_excess.append(str(entry.get("region_id") or "<missing>"))
                except (TypeError, ValueError):
                    starter_threat_excess.append(str(entry.get("region_id") or "<missing>"))
        starter_threat_excess = sorted(set(starter_threat_excess))
        if starter_threat_excess:
            warnings.append(
                "Ascendant starter-region threat range exceeds starter rank policy: "
                f"{len(starter_threat_excess)} ({ascendant_loot_preview(starter_threat_excess)})"
            )

    if isinstance(gear_policy, dict):
        if gear_policy.get("status") != "audit_control_scaffold_only_no_gear_gates":
            warnings.append("Ascendant gear rank policy is not marked no-gear-gates.")
        entries = gear_policy.get("rarity_rank_policy", [])
        if not isinstance(entries, list) or not entries:
            errors.append("config/ascendant_progression/gear_rank_policy.json must contain rarity_rank_policy.")
            entries = []
        object_entries = [entry for entry in entries if isinstance(entry, dict)]
        policy_rarities = {str(entry.get("rarity")) for entry in object_entries if entry.get("rarity")}
        missing_rarities = sorted(gear_rarities - policy_rarities)
        generated_missing_rarities = [str(value) for value in validation_list(gear_policy, "gear_rarities_without_rank_policy")]
        if generated_missing_rarities:
            missing_rarities = sorted(set(missing_rarities) | set(generated_missing_rarities))
        if missing_rarities:
            warnings.append(
                "Ascendant gear rarities have no rank policy: "
                f"{len(missing_rarities)} ({ascendant_loot_preview(missing_rarities)})"
            )

    if isinstance(magic_policy, dict):
        if magic_policy.get("status") != "audit_control_scaffold_only_no_magic_gates":
            warnings.append("Ascendant magic rank policy is not marked no-magic-gates.")
        entries = magic_policy.get("magic_tier_rank_policy", [])
        if not isinstance(entries, list) or not entries:
            errors.append("config/ascendant_progression/magic_rank_policy.json must contain magic_tier_rank_policy.")
            entries = []
        object_entries = [entry for entry in entries if isinstance(entry, dict)]
        policy_tiers = {str(entry.get("magic_tier")) for entry in object_entries if entry.get("magic_tier")}
        missing_tiers = sorted(magic_tiers - policy_tiers)
        generated_missing_tiers = [str(value) for value in validation_list(magic_policy, "magic_tiers_without_rank_policy")]
        if generated_missing_tiers:
            missing_tiers = sorted(set(missing_tiers) | set(generated_missing_tiers))
        if missing_tiers:
            warnings.append(
                "Ascendant magic tiers have no rank policy: "
                f"{len(missing_tiers)} ({ascendant_loot_preview(missing_tiers)})"
            )


def validate_ascendant_ranked_dungeons(errors: list[str], warnings: list[str]) -> None:
    required_json = {
        "policy": ROOT / "config/ascendant_dungeons/ranked_dungeon_policy.json",
        "ranks": ROOT / "config/ascendant_dungeons/dungeon_rank_registry.json",
        "portal": ROOT / "config/ascendant_dungeons/dungeon_portal_policy.json",
        "holograms": ROOT / "config/ascendant_dungeons/dungeon_hologram_policy.json",
        "spawn": ROOT / "config/ascendant_dungeons/dungeon_spawn_policy.json",
        "templates": ROOT / "config/ascendant_dungeons/dungeon_instance_templates.json",
        "dimension": ROOT / "config/ascendant_dungeons/dungeon_dimension_policy.json",
    }
    loaded: dict[str, dict] = {}
    for _label, path in required_json.items():
        if not path.exists():
            errors.append(f"Missing Ascendant dungeon policy file: {rel(path)}")
            continue
        try:
            data = read_json(path)
        except Exception as exc:
            errors.append(f"{rel(path)} is invalid JSON: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel(path)} must be a JSON object.")
            continue
        loaded[_label] = data

    if len(loaded) != len(required_json):
        return

    policy = loaded["policy"]
    ranks = loaded["ranks"]
    portal = loaded["portal"]
    holograms = loaded["holograms"]
    spawn = loaded["spawn"]
    templates = loaded["templates"]
    dimension = loaded["dimension"]

    if policy.get("version") != 1:
        errors.append("config/ascendant_dungeons/ranked_dungeon_policy.json must use version 1.")
    if policy.get("system_id") != "ascendant_ranked_dungeons":
        errors.append("config/ascendant_dungeons/ranked_dungeon_policy.json must use system_id ascendant_ranked_dungeons.")

    portal_system = policy.get("portal_system")
    if not isinstance(portal_system, dict) or portal_system.get("primary_mod") != "immersive_portals":
        errors.append("Ascendant ranked dungeons must declare immersive_portals as the primary portal mod.")
    random_spawning = policy.get("random_spawning")
    if not isinstance(random_spawning, dict):
        errors.append("Ascendant ranked dungeon policy must contain random_spawning.")
    elif random_spawning.get("enabled") is not True:
        warnings.append("Ascendant ranked dungeon random spawning is disabled; Jayden requested controlled timed world rifts for spawn testing.")
    elif random_spawning.get("current_limit") != "one_active_rift_per_rank":
        warnings.append("Ascendant ranked dungeon random spawning should use one_active_rift_per_rank so D/C/B/A/S can each exist once.")
    else:
        if random_spawning.get("maximum_active_rifts_global") != 5:
            warnings.append("Ascendant ranked dungeon policy should allow maximum_active_rifts_global=5 for one D/C/B/A/S rift each.")
        if random_spawning.get("maximum_active_rifts_per_rank") != 1:
            warnings.append("Ascendant ranked dungeon policy should enforce maximum_active_rifts_per_rank=1.")

    mod_metadata_path = ROOT / "mods/immersive-portals-neoforge.pw.toml"
    if not mod_metadata_path.exists():
        errors.append("Immersive Portals Packwiz metadata is missing.")
    else:
        text = read_text(mod_metadata_path)
        if metadata_filename(text) != "immersive-portals-3.0.7-all.jar":
            errors.append("Immersive Portals metadata must point at immersive-portals-3.0.7-all.jar.")
        if metadata_side(text) != "both":
            errors.append('Immersive Portals metadata must be side = "both".')

    active_mods = ACTIVE_CURSEFORGE_INSTANCE / "mods"
    if active_mods.exists() and not list(active_mods.glob("immersive-portals-*.jar")):
        warnings.append(
            "Active Ascendant Realms (2) instance does not yet contain immersive-portals-3.0.7-all.jar; "
            "rebuild/sync the client export before in-game dungeon tests."
        )

    rank_entries = ranks.get("rank_registry")
    rank_ids: set[str] = set()
    if not isinstance(rank_entries, list) or not rank_entries:
        errors.append("config/ascendant_dungeons/dungeon_rank_registry.json must contain rank_registry.")
    else:
        rank_ids = {str(entry.get("rank_id", "")) for entry in rank_entries if isinstance(entry, dict)}
        required_ranks = {"d_rank", "c_rank", "b_rank", "a_rank", "s_rank"}
        missing = sorted(required_ranks - rank_ids)
        if missing:
            errors.append("Ascendant dungeon rank registry is missing ranks: " + ", ".join(missing))

    portal_profiles = portal.get("rift_profiles")
    portal_profile_ids: set[str] = set()
    if not isinstance(portal_profiles, list) or not portal_profiles:
        errors.append("config/ascendant_dungeons/dungeon_portal_policy.json must contain rift_profiles.")
    else:
        portal_profile_ids = {str(entry.get("profile_id", "")) for entry in portal_profiles if isinstance(entry, dict)}
    if portal.get("portal_owner") != "immersive_portals":
        errors.append("config/ascendant_dungeons/dungeon_portal_policy.json must use portal_owner immersive_portals.")
    spawn_behavior = portal.get("spawn_behavior")
    if not isinstance(spawn_behavior, dict):
        errors.append("config/ascendant_dungeons/dungeon_portal_policy.json must contain spawn_behavior.")
    else:
        if spawn_behavior.get("item_display_billboard_enabled") is not False:
            warnings.append("Dungeon portal item_display_billboard_enabled should be false so gate art stays fixed-facing.")
        if spawn_behavior.get("item_display_fixed_facing_enabled") is not True:
            warnings.append("Dungeon portal item_display_fixed_facing_enabled should be true.")
        if spawn_behavior.get("api_bridge_mode") != "circular_teleportable_immersive_portal_with_helper_fallback":
            errors.append("Dungeon portal api_bridge_mode must be circular_teleportable_immersive_portal_with_helper_fallback.")
        if spawn_behavior.get("immersive_portals_teleportable_surface_enabled") is not True:
            errors.append("Dungeon portal policy must enable teleportable Immersive Portals surfaces.")
        if spawn_behavior.get("immersive_portals_circular_special_shape_enabled") is not True:
            errors.append("Dungeon portal policy must enable circular Immersive Portals special shapes.")
        if spawn_behavior.get("item_aperture_center_transparent") is not True:
            errors.append("Dungeon portal policy must require transparent-center gate item textures.")
        if int(spawn_behavior.get("entrance_close_delay_after_first_entry_seconds", 0) or 0) < 5:
            errors.append("Dungeon portal policy must keep the entrance open at least 5 seconds after first entry.")
        if spawn_behavior.get("entrance_shrink_out_enabled") is not True:
            errors.append("Dungeon portal policy must enable entrance shrink-out instead of instant disappearance.")
        if spawn_behavior.get("exit_gate_locked_until_boss_defeated") is not True:
            warnings.append("Dungeon portal policy must lock exit gates until the boss is defeated.")
    scale_ranges = portal.get("rank_scale_ranges")
    if not isinstance(scale_ranges, dict):
        warnings.append("config/ascendant_dungeons/dungeon_portal_policy.json is missing rank_scale_ranges for randomized gate sizes.")
    else:
        for rank_id in ["d_rank", "c_rank", "b_rank", "a_rank", "s_rank"]:
            entry = scale_ranges.get(rank_id)
            if not isinstance(entry, dict) or "min" not in entry or "max" not in entry:
                warnings.append(f"Dungeon portal rank_scale_ranges is missing min/max for {rank_id}.")

    hologram_metadata_path = ROOT / "mods/elite-holograms.pw.toml"
    if not hologram_metadata_path.exists():
        errors.append("Elite Holograms Packwiz metadata is missing.")
    else:
        hologram_text = read_text(hologram_metadata_path)
        if metadata_filename(hologram_text) != "EliteHolograms-1.20.1-1.1.0.jar":
            errors.append("Elite Holograms metadata must point at EliteHolograms-1.20.1-1.1.0.jar.")
        if metadata_side(hologram_text) != "both":
            errors.append('Elite Holograms metadata must be side = "both".')
    if holograms.get("hologram_owner") != "elite_holograms":
        errors.append("config/ascendant_dungeons/dungeon_hologram_policy.json must use hologram_owner elite_holograms.")
    if holograms.get("creation_enabled") is not False and holograms.get("creation_scope") != "manual_spawn_test_only":
        warnings.append("Dungeon hologram creation is enabled outside manual_spawn_test_only; confirm Elite Holograms command syntax and cleanup first.")
    rank_styles = holograms.get("rank_styles")
    if not isinstance(rank_styles, dict):
        errors.append("config/ascendant_dungeons/dungeon_hologram_policy.json must contain rank_styles.")
    else:
        missing_styles = sorted({"d_rank", "c_rank", "b_rank", "a_rank", "s_rank"} - set(rank_styles.keys()))
        if missing_styles:
            errors.append("Dungeon hologram policy is missing rank styles: " + ", ".join(missing_styles))
        for rank_id, style in rank_styles.items():
            if not isinstance(style, dict):
                errors.append(f"Dungeon hologram style for {rank_id} must be an object.")
                continue
            lines = style.get("lines")
            if not isinstance(lines, list) or not lines:
                errors.append(f"Dungeon hologram style for {rank_id} must contain lines.")
            title = str(style.get("title", ""))
            if "<gradient:" not in title:
                warnings.append(f"Dungeon hologram style for {rank_id} does not use a MiniMessage gradient title.")

    if active_mods.exists() and not list(active_mods.glob("EliteHolograms-*.jar")):
        warnings.append(
            "Active Ascendant Realms (2) instance does not yet contain EliteHolograms-1.20.1-1.1.0.jar; "
            "rebuild/sync the client export before in-game hologram tests."
        )

    if spawn.get("random_spawning_enabled") is not True:
        warnings.append("config/ascendant_dungeons/dungeon_spawn_policy.json has random_spawning_enabled=false; controlled random rift testing is expected to be active.")
    if spawn.get("autonomous_world_scheduler_enabled") is not True:
        warnings.append("config/ascendant_dungeons/dungeon_spawn_policy.json has autonomous_world_scheduler_enabled=false; timed random rifts will not attempt to spawn.")
    live_scheduler = spawn.get("live_scheduler")
    if not isinstance(live_scheduler, dict):
        warnings.append("config/ascendant_dungeons/dungeon_spawn_policy.json is missing live_scheduler.")
    else:
        if live_scheduler.get("scope") != "one_active_rift_per_rank":
            warnings.append("Dungeon live_scheduler.scope should be one_active_rift_per_rank.")
        if live_scheduler.get("maximum_active_rifts_global") != 5:
            warnings.append("Dungeon live_scheduler.maximum_active_rifts_global should be 5 for one D/C/B/A/S rift each.")
        if live_scheduler.get("maximum_active_rifts_per_rank") != 1:
            warnings.append("Dungeon live_scheduler.maximum_active_rifts_per_rank should be 1.")
        rank_slots = live_scheduler.get("rank_slots")
        if rank_slots != ["d_rank", "c_rank", "b_rank", "a_rank", "s_rank"]:
            warnings.append("Dungeon live_scheduler.rank_slots should list d_rank, c_rank, b_rank, a_rank, and s_rank.")
        if live_scheduler.get("attempt_chance", 0) <= 0:
            warnings.append("Dungeon live_scheduler.attempt_chance is zero; random rifts will never spawn.")
    duration_policy = spawn.get("rift_duration_minutes_by_rank")
    if not isinstance(duration_policy, dict):
        warnings.append("config/ascendant_dungeons/dungeon_spawn_policy.json is missing rift_duration_minutes_by_rank.")
    else:
        missing_durations = [rank for rank in ["d_rank", "c_rank", "b_rank", "a_rank", "s_rank"] if rank not in duration_policy]
        if missing_durations:
            warnings.append("Dungeon rift duration policy is missing ranks: " + ", ".join(missing_durations))
    if spawn.get("manual_spawn_testing_enabled") is not True:
        warnings.append("config/ascendant_dungeons/dungeon_spawn_policy.json has manual_spawn_testing_enabled=false; /ascdungeon spawn tests will remain report-only.")

    if dimension.get("version") != 1:
        errors.append("config/ascendant_dungeons/dungeon_dimension_policy.json must use version 1.")
    if dimension.get("system_id") != "ascendant_ranked_dungeons":
        errors.append("config/ascendant_dungeons/dungeon_dimension_policy.json must use system_id ascendant_ranked_dungeons.")
    if dimension.get("dimension_id") != "ascendant_dungeons:ranked_dungeon":
        errors.append("config/ascendant_dungeons/dungeon_dimension_policy.json must target ascendant_dungeons:ranked_dungeon.")
    if dimension.get("manual_instance_generation_enabled") is not True:
        warnings.append("Dungeon dimension policy has manual_instance_generation_enabled=false; /ascdungeon open_test_rift will be blocked.")
    if dimension.get("autonomous_random_spawning_enabled") is not True:
        warnings.append("Dungeon dimension policy has autonomous_random_spawning_enabled=false; timed random rifts will not run.")
    dimension_portal = dimension.get("portal_behavior")
    if isinstance(dimension_portal, dict):
        if dimension_portal.get("exit_gate_spawns_after_boss_defeat") is not True:
            warnings.append("Dungeon dimension policy should declare exit_gate_spawns_after_boss_defeat=true.")
        if dimension_portal.get("exit_gate_created_during_initial_generation") is not False:
            warnings.append("Dungeon dimension policy should declare exit_gate_created_during_initial_generation=false.")

    dungeon_pack_root = ROOT / "config/openloader/data/ascendant_realms_dungeons"
    dimension_type_path = dungeon_pack_root / "data/ascendant_dungeons/dimension_type/ranked_dungeon.json"
    dimension_path = dungeon_pack_root / "data/ascendant_dungeons/dimension/ranked_dungeon.json"
    for path in [dungeon_pack_root / "pack.mcmeta", dimension_type_path, dimension_path]:
        if not path.exists():
            errors.append(f"Ascendant dungeon dimension datapack file is missing: {rel(path)}")
    dungeon_generation = dimension.get("generation_model", {})
    if isinstance(dungeon_generation, dict):
        if dungeon_generation.get("loot_mode") == "placeholder_vanilla_test_chests":
            warnings.append("Ascendant ranked dungeons still declare placeholder vanilla test chest loot.")
        if dungeon_generation.get("mob_mode") == "rank_scaled_vanilla_hostile_test_mobs":
            warnings.append("Ascendant ranked dungeons still declare vanilla hostile test mobs.")
        if dungeon_generation.get("one_active_instance_per_rank_limit") is not True:
            warnings.append("Dungeon dimension policy should declare one_active_instance_per_rank_limit=true.")
        if dungeon_generation.get("maximum_active_instances_global") != 5:
            warnings.append("Dungeon dimension policy should declare maximum_active_instances_global=5.")
    expected_dungeon_loot = [
        dungeon_pack_root / "data/ascendant_dungeons/loot_tables/chests/ranked_supply.json",
    ]
    for rank_prefix in ["d", "c", "b", "a", "s"]:
        expected_dungeon_loot.extend([
            dungeon_pack_root / f"data/ascendant_dungeons/loot_tables/chests/{rank_prefix}_rank_room.json",
            dungeon_pack_root / f"data/ascendant_dungeons/loot_tables/chests/{rank_prefix}_rank_boss.json",
            dungeon_pack_root / f"data/ascendant_dungeons/loot_tables/entities/{rank_prefix}_rank_mob.json",
            dungeon_pack_root / f"data/ascendant_dungeons/loot_tables/entities/{rank_prefix}_rank_boss.json",
        ])
    for path in expected_dungeon_loot:
        if not path.exists():
            errors.append(f"Ascendant ranked dungeon loot table is missing: {rel(path)}")
            continue
        try:
            loot = read_json(path)
            if not isinstance(loot, dict) or "pools" not in loot:
                errors.append(f"Ascendant ranked dungeon loot table must contain pools: {rel(path)}")
        except Exception as exc:
            errors.append(f"{rel(path)} is invalid JSON: {exc}")
    if dimension_path.exists():
        try:
            dimension_json = read_json(dimension_path)
            if dimension_json.get("type") != "ascendant_dungeons:ranked_dungeon":
                errors.append("Ascendant dungeon dimension must use type ascendant_dungeons:ranked_dungeon.")
            generator = dimension_json.get("generator")
            if not isinstance(generator, dict) or generator.get("type") != "minecraft:flat":
                errors.append("Ascendant dungeon dimension must use a minecraft:flat generator for controlled test instances.")
        except Exception as exc:
            errors.append(f"{rel(dimension_path)} is invalid JSON: {exc}")
    gate_pack_root = ROOT / "resourcepacks/ascendant-dungeon-gates"
    expected_gate_assets = [
        gate_pack_root / "pack.mcmeta",
        gate_pack_root / "assets/ascendant_dungeons/textures/gate/gate.png",
        gate_pack_root / "assets/ascendant_dungeons/textures/gate/gate_green.png",
        gate_pack_root / "assets/ascendant_dungeons/textures/gate/gate_purple.png",
        gate_pack_root / "assets/ascendant_dungeons/textures/gate/gate_gold.png",
        gate_pack_root / "assets/ascendant_dungeons/textures/gate/gate_red.png",
        gate_pack_root / "assets/ascendant_dungeons/textures/item/gate.png",
        gate_pack_root / "assets/ascendant_dungeons/textures/item/gate_green.png",
        gate_pack_root / "assets/ascendant_dungeons/textures/item/gate_purple.png",
        gate_pack_root / "assets/ascendant_dungeons/textures/item/gate_gold.png",
        gate_pack_root / "assets/ascendant_dungeons/textures/item/gate_red.png",
        gate_pack_root / "assets/minecraft/models/item/paper.json",
        gate_pack_root / "assets/ascendant_dungeons/models/item/gate_blue.json",
        gate_pack_root / "assets/ascendant_dungeons/models/item/gate_green.json",
        gate_pack_root / "assets/ascendant_dungeons/models/item/gate_purple.json",
        gate_pack_root / "assets/ascendant_dungeons/models/item/gate_gold.json",
        gate_pack_root / "assets/ascendant_dungeons/models/item/gate_red.json",
    ]
    for path in expected_gate_assets:
        if not path.exists():
            warnings.append(f"Ascendant dungeon gate asset is missing: {rel(path)}")
    for model_path in [
        gate_pack_root / "assets/ascendant_dungeons/models/item/gate_blue.json",
        gate_pack_root / "assets/ascendant_dungeons/models/item/gate_green.json",
        gate_pack_root / "assets/ascendant_dungeons/models/item/gate_purple.json",
        gate_pack_root / "assets/ascendant_dungeons/models/item/gate_gold.json",
        gate_pack_root / "assets/ascendant_dungeons/models/item/gate_red.json",
    ]:
        if model_path.exists():
            try:
                model_text = read_text(model_path)
                if "ascendant_dungeons:gate/" in model_text:
                    errors.append(f"{rel(model_path)} references textures/gate; item-display models must use ascendant_dungeons:item/... so Minecraft stitches the sprite.")
            except Exception as exc:
                warnings.append(f"Could not validate Ascendant dungeon gate model {rel(model_path)}: {exc}")
    options_path = ROOT / "options.txt"
    if options_path.exists() and "file/ascendant-dungeon-gates" not in read_text(options_path):
        warnings.append("options.txt does not enable file/ascendant-dungeon-gates, so ranked dungeon gate item displays will use vanilla paper.")
    overrides_path = ROOT / "config/resourcepackoverrides.json"
    if overrides_path.exists():
        try:
            overrides = read_json(overrides_path)
            default_packs = overrides.get("default_packs", [])
            pack_overrides = overrides.get("pack_overrides", {})
            if "file/ascendant-dungeon-gates" not in default_packs:
                warnings.append("config/resourcepackoverrides.json default_packs does not include file/ascendant-dungeon-gates.")
            gate_override = pack_overrides.get("file/ascendant-dungeon-gates")
            if not isinstance(gate_override, dict) or gate_override.get("required") is not True:
                warnings.append("config/resourcepackoverrides.json must mark file/ascendant-dungeon-gates as required.")
        except Exception as exc:
            warnings.append(f"Could not validate Ascendant dungeon gate Resource Pack Overrides config: {exc}")

    template_entries = templates.get("templates")
    if not isinstance(template_entries, list) or not template_entries:
        errors.append("config/ascendant_dungeons/dungeon_instance_templates.json must contain templates.")
    else:
        for template in template_entries:
            if not isinstance(template, dict):
                errors.append("config/ascendant_dungeons/dungeon_instance_templates.json templates contains non-object entries.")
                continue
            template_id = str(template.get("template_id", "<missing>"))
            allowed_ranks = template.get("allowed_ranks")
            if not isinstance(allowed_ranks, list) or not allowed_ranks:
                errors.append(f"Dungeon template {template_id} has no allowed_ranks.")
            else:
                unknown_ranks = sorted(str(rank) for rank in allowed_ranks if str(rank) not in rank_ids)
                if unknown_ranks:
                    errors.append(f"Dungeon template {template_id} references unknown ranks: {', '.join(unknown_ranks)}")
            profile = str(template.get("portal_profile", ""))
            if not profile:
                errors.append(f"Dungeon template {template_id} has no portal_profile.")
            elif profile not in portal_profile_ids:
                errors.append(f"Dungeon template {template_id} references missing portal_profile {profile}.")
            if not template.get("loot_tier"):
                warnings.append(f"Dungeon template {template_id} has no loot_tier.")
            if not isinstance(template.get("danger_tier"), int):
                warnings.append(f"Dungeon template {template_id} has no numeric danger_tier.")

    sync_script = ROOT / "scripts/sync-active-client-files.ps1"
    if sync_script.exists() and "config\\ascendant_dungeons" not in read_text(sync_script):
        errors.append("scripts/sync-active-client-files.ps1 must sync config\\ascendant_dungeons into the active instance.")


def ascendant_structure_known_ids(errors: list[str]) -> set[str]:
    known_ids: set[str] = set()
    structure_registry_path = ROOT / "config/ascendant_index/structure_registry.json"
    if structure_registry_path.exists():
        try:
            registry = read_json(structure_registry_path)
            for entry in registry.get("structures", []):
                if not isinstance(entry, dict):
                    continue
                structure_id = str(entry.get("structure_id") or "")
                if structure_id and not structure_id.startswith("data/"):
                    known_ids.add(structure_id)
        except Exception as exc:
            errors.append(f"Structure registry JSON is invalid for Ascendant structure validation: {exc}")

    worldgen_audit_path = ROOT / "docs/generated/worldgen_content_audit.json"
    if worldgen_audit_path.exists():
        try:
            audit = read_json(worldgen_audit_path)
            audit_structures = audit.get("structures", {})
            if isinstance(audit_structures, dict):
                for structure_id, entry in audit_structures.items():
                    if not isinstance(entry, dict):
                        continue
                    if entry.get("type") or entry.get("start_pool") or entry.get("structure_sets"):
                        known_ids.add(str(structure_id))
        except Exception as exc:
            errors.append(f"Worldgen content audit JSON is invalid for Ascendant structure validation: {exc}")
    return known_ids


def validate_ascendant_structure_tiering(errors: list[str], warnings: list[str]) -> None:
    structure_reports: dict[str, object] = {}
    for report_name in ASCENDANT_STRUCTURE_JSON_FILES:
        report_path = ROOT / report_name
        if not report_path.exists():
            continue
        try:
            report = read_json(report_path)
            if not isinstance(report, dict):
                errors.append(f"Ascendant structure JSON must be an object: {report_name}")
                continue
            structure_reports[report_name] = report
        except Exception as exc:
            errors.append(f"Ascendant structure JSON is invalid: {report_name}: {exc}")

    known_ids = ascendant_structure_known_ids(errors)
    all_policy_ids: set[str] = set()

    tier_registry = structure_reports.get("config/ascendant_structures/structure_tier_registry.json")
    director_registry = structure_reports.get("config/ascendant_structures/structure_registry.json")
    region_rules = structure_reports.get("config/ascendant_structures/structure_region_rules.json")
    vertical_rules = structure_reports.get("config/ascendant_structures/structure_vertical_layer_rules.json")
    density_policy = structure_reports.get("config/ascendant_structures/structure_density_policy.json")
    set_overrides = structure_reports.get("config/ascendant_structures/structure_set_overrides.json")
    loot_linkage = structure_reports.get("config/ascendant_structures/structure_loot_linkage.json")
    water_policy = structure_reports.get("config/ascendant_structures/water_structure_policy.json")
    sky_policy = structure_reports.get("config/ascendant_structures/sky_structure_policy.json")
    sea_floor_policy = structure_reports.get("config/ascendant_structures/sea_floor_structure_policy.json")
    ship_policy = structure_reports.get("config/ascendant_structures/ship_structure_policy.json")
    dungeon_policy = structure_reports.get("config/ascendant_structures/dungeon_structure_policy.json")
    boss_policy = structure_reports.get("config/ascendant_structures/boss_structure_policy.json")
    village_policy = structure_reports.get("config/ascendant_structures/village_structure_policy.json")
    structure_test_points = structure_reports.get("config/ascendant_structures/structure_test_points.json")
    structure_visual_review_route = structure_reports.get("config/ascendant_structures/structure_visual_review_route.json")
    structure_review_priority_queue = structure_reports.get("config/ascendant_structures/structure_review_priority_queue.json")
    structure_visual_review_findings = structure_reports.get(
        "config/ascendant_structures/structure_visual_review_findings_latest.json"
    )
    structure_evidence_registry = structure_reports.get("config/ascendant_structures/structure_evidence_registry.json")
    structure_classification_confidence = structure_reports.get(
        "config/ascendant_structures/structure_classification_confidence.json"
    )
    manual_structure_observations = structure_reports.get("config/ascendant_structures/manual_structure_observations.json")
    live_structure_policy = structure_reports.get("config/ascendant_structures/live_structure_policy.json")
    live_structure_manifest = structure_reports.get("config/ascendant_structures/live_structure_manifest.json")
    live_structure_results = structure_reports.get("config/ascendant_structures/live_structure_results.json")
    live_test_targets = structure_reports.get("config/ascendant_structures/live_test_targets.json")
    structure_land_placement_candidates = structure_reports.get(
        "config/ascendant_structures/candidates/structure_land_placement_candidates.json"
    )
    structure_region_lock_candidates = structure_reports.get(
        "config/ascendant_structures/candidates/structure_region_lock_candidates.json"
    )
    structure_density_candidates = structure_reports.get(
        "config/ascendant_structures/candidates/structure_density_candidates.json"
    )

    def structure_policy_entries(report: object, key: str, report_name: str, required: bool = True) -> list[dict]:
        if not isinstance(report, dict):
            if required:
                errors.append(f"{report_name} is missing or invalid.")
            return []
        entries = report.get(key, [])
        if not isinstance(entries, list) or (required and not entries):
            errors.append(f"{report_name} must contain {key}.")
            return []
        object_entries = [entry for entry in entries if isinstance(entry, dict)]
        if len(object_entries) != len(entries):
            errors.append(f"{report_name} {key} contains non-object entries.")
        all_policy_ids.update(
            str(entry.get("structure_id"))
            for entry in object_entries
            if entry.get("structure_id")
        )
        return object_entries

    if isinstance(tier_registry, dict):
        if tier_registry.get("status") != "audit_control_scaffold_only_no_live_structure_rewrites":
            warnings.append(
                "Ascendant structure tier registry is not marked audit/control-only; verify live structure rewrites were approved."
            )
        structure_entries = tier_registry.get("structures", [])
        if not isinstance(structure_entries, list) or not structure_entries:
            errors.append("config/ascendant_structures/structure_tier_registry.json must contain structures.")
            structure_entries = []
        object_entries = [entry for entry in structure_entries if isinstance(entry, dict)]
        if len(object_entries) != len(structure_entries):
            errors.append("config/ascendant_structures/structure_tier_registry.json structures contains non-object entries.")
        all_policy_ids.update(
            str(entry.get("structure_id"))
            for entry in object_entries
            if entry.get("structure_id")
        )

        missing_tier_fields = [
            entry.get("structure_id")
            for entry in object_entries
            if not entry.get("structure_class")
            or entry.get("danger_tier") is None
            or not entry.get("guild_rank_tier")
        ]
        if missing_tier_fields:
            warnings.append(
                "Ascendant structure tiering has entries with no tier assignment: "
                f"{len(missing_tier_fields)} ({ascendant_loot_preview(missing_tier_fields)})"
            )

        missing_evidence_fields = [
            entry.get("structure_id")
            for entry in object_entries
            if "confidence" not in entry
            or not entry.get("classification_confidence")
            or not entry.get("classification_reason")
            or "manual_review_required" not in entry
            or "name_only_classification" not in entry
            or not isinstance(entry.get("evidence_source"), list)
        ]
        if missing_evidence_fields:
            errors.append(
                "Ascendant structure tiering entries are missing evidence/confidence fields: "
                f"{len(missing_evidence_fields)} ({ascendant_loot_preview(missing_evidence_fields)})"
            )

        name_only_rows = [
            entry.get("structure_id")
            for entry in object_entries
            if entry.get("name_only_classification") is True
        ]
        if name_only_rows:
            errors.append(
                "Ascendant structure tiering has name-only final classifications: "
                f"{len(name_only_rows)} ({ascendant_loot_preview(name_only_rows)})"
            )

        sensitive_low_confidence = [
            entry.get("structure_id")
            for entry in object_entries
            if (
                entry.get("structure_class") in {"dangerous_dungeon", "boss_arena", "dragon_tier_zone", "settlement"}
                or entry.get("water_role") not in {None, "", "none"}
                or entry.get("sky_role") not in {None, "", "none"}
            )
            and entry.get("classification_confidence") == "weak"
        ]
        if sensitive_low_confidence:
            warnings.append(
                "Ascendant Structure Director has weak-confidence sensitive classifications needing manual review: "
                f"{len(sensitive_low_confidence)} ({ascendant_loot_preview(sensitive_low_confidence)})"
            )

        water_without_evidence = [
            entry.get("structure_id")
            for entry in object_entries
            if entry.get("water_role") not in {None, "", "none"}
            and not any(
                marker in source
                for source in entry.get("evidence_source", [])
                for marker in ("biome_tag_or_selector:strong", "block_palette:strong", "manual_live_observation:strong")
            )
        ]
        if water_without_evidence:
            errors.append(
                "Ascendant Structure Director has water roles without biome/block/manual evidence: "
                f"{len(water_without_evidence)} ({ascendant_loot_preview(water_without_evidence)})"
            )

        frozen_without_evidence = [
            entry.get("structure_id")
            for entry in object_entries
            if entry.get("water_role") == "frozen_ocean"
            and not (
                "frost_cold" in entry.get("biome_families", [])
                or "frozen_ocean" in entry.get("biome_families", [])
            )
        ]
        if frozen_without_evidence:
            errors.append(
                "Ascendant Structure Director has frozen_ocean roles without cold/frozen evidence: "
                f"{len(frozen_without_evidence)} ({ascendant_loot_preview(frozen_without_evidence)})"
            )

        sky_without_evidence = [
            entry.get("structure_id")
            for entry in object_entries
            if entry.get("sky_role") not in {None, "", "none"}
            and not any("structure_json:strong" in source for source in entry.get("evidence_source", []))
        ]
        if sky_without_evidence:
            errors.append(
                "Ascendant Structure Director has sky roles without structure height/JSON evidence: "
                f"{len(sky_without_evidence)} ({ascendant_loot_preview(sky_without_evidence)})"
            )

        beginner_conflicts = [
            entry.get("structure_id")
            for entry in object_entries
            if entry.get("structure_class") in {"dangerous_dungeon", "boss_arena", "dragon_tier_zone"}
            and any(
                str(region) in {"hearthlands", "crownlands", "center"}
                for region in entry.get("atlas_allowed_regions", [])
            )
        ]
        validation = tier_registry.get("validation", {})
        if isinstance(validation, dict):
            reported_conflicts = validation.get("boss_or_dungeon_in_beginner_regions", [])
            if isinstance(reported_conflicts, list):
                beginner_conflicts = sorted(set(str(value) for value in beginner_conflicts) | set(str(value) for value in reported_conflicts))
            no_loot_tier = validation.get("no_loot_tier", [])
            if isinstance(no_loot_tier, list) and no_loot_tier:
                warnings.append(
                    "Ascendant structure tiering has structures with no loot tier or review-only loot tier: "
                    f"{len(no_loot_tier)} ({ascendant_loot_preview(no_loot_tier)})"
                )
        if beginner_conflicts:
            warnings.append(
                "Ascendant structure tiering allows boss/dungeon structures in beginner regions: "
                f"{len(beginner_conflicts)} ({ascendant_loot_preview(beginner_conflicts)})"
            )

    director_entries = structure_policy_entries(
        director_registry,
        "structures",
        "config/ascendant_structures/structure_registry.json",
    )
    if director_entries:
        missing_director_fields = [
            entry.get("structure_id")
            for entry in director_entries
            if not entry.get("vertical_layers")
            or not entry.get("atlas_allowed_regions")
            or not entry.get("density_class")
            or entry.get("danger_tier") is None
        ]
        if missing_director_fields:
            warnings.append(
                "Ascendant structure director rows are missing region/layer/density/tier fields: "
                f"{len(missing_director_fields)} ({ascendant_loot_preview(missing_director_fields)})"
            )

    if isinstance(region_rules, dict):
        rules = region_rules.get("region_rules", [])
        if not isinstance(rules, list) or not rules:
            errors.append("config/ascendant_structures/structure_region_rules.json must contain region_rules.")
            rules = []
        object_rules = [entry for entry in rules if isinstance(entry, dict)]
        if len(object_rules) != len(rules):
            errors.append("config/ascendant_structures/structure_region_rules.json region_rules contains non-object entries.")
        all_policy_ids.update(
            str(entry.get("structure_id"))
            for entry in object_rules
            if entry.get("structure_id")
        )
        missing_region_rules = [
            entry.get("structure_id")
            for entry in object_rules
            if not entry.get("atlas_allowed_regions")
        ]
        validation = region_rules.get("validation", {})
        if isinstance(validation, dict):
            reported_missing = validation.get("no_atlas_region_rules", [])
            if isinstance(reported_missing, list):
                missing_region_rules = sorted(set(str(value) for value in missing_region_rules) | set(str(value) for value in reported_missing))
        if missing_region_rules:
            warnings.append(
                "Ascendant structure tiering has structures with no Atlas region rules: "
                f"{len(missing_region_rules)} ({ascendant_loot_preview(missing_region_rules)})"
            )

    if isinstance(density_policy, dict):
        structure_sets = density_policy.get("structure_sets", [])
        if not isinstance(structure_sets, list) or not structure_sets:
            errors.append("config/ascendant_structures/structure_density_policy.json must contain structure_sets.")
            structure_sets = []
        object_sets = [entry for entry in structure_sets if isinstance(entry, dict)]
        if len(object_sets) != len(structure_sets):
            errors.append("config/ascendant_structures/structure_density_policy.json structure_sets contains non-object entries.")
        validation = density_policy.get("validation", {})
        if isinstance(validation, dict):
            dense_spacing = validation.get("dangerously_dense_or_dense_spacing", [])
            if isinstance(dense_spacing, list) and dense_spacing:
                warnings.append(
                    "Ascendant structure density policy found dense or dangerously dense spacing: "
                    f"{len(dense_spacing)} "
                    f"({ascendant_loot_preview([entry.get('structure_id') for entry in dense_spacing if isinstance(entry, dict)])})"
                )
            overlap_risks = validation.get("village_town_overlap_risks", [])
            if isinstance(overlap_risks, list) and overlap_risks:
                warnings.append(
                    "Ascendant structure density policy found village/town overlap risks: "
                    f"{len(overlap_risks)} "
                    f"({ascendant_loot_preview([entry.get('structure_set') for entry in overlap_risks if isinstance(entry, dict)])})"
                )

    if isinstance(loot_linkage, dict):
        linkage_entries = loot_linkage.get("structure_loot_linkage", [])
        if not isinstance(linkage_entries, list) or not linkage_entries:
            errors.append("config/ascendant_structures/structure_loot_linkage.json must contain structure_loot_linkage.")
            linkage_entries = []
        object_linkage = [entry for entry in linkage_entries if isinstance(entry, dict)]
        if len(object_linkage) != len(linkage_entries):
            errors.append("config/ascendant_structures/structure_loot_linkage.json structure_loot_linkage contains non-object entries.")
        all_policy_ids.update(
            str(entry.get("structure_id"))
            for entry in object_linkage
            if entry.get("structure_id")
        )
        no_loot = [
            entry.get("structure_id")
            for entry in object_linkage
            if not entry.get("loot_tier") or entry.get("loot_tier") == "review"
        ]
        validation = loot_linkage.get("validation", {})
        if isinstance(validation, dict):
            reported_no_loot = validation.get("no_loot_tier", [])
            if isinstance(reported_no_loot, list):
                no_loot = sorted(set(str(value) for value in no_loot) | set(str(value) for value in reported_no_loot))
        if no_loot:
            warnings.append(
                "Ascendant structure loot linkage has structures with no assigned loot tier: "
                f"{len(no_loot)} ({ascendant_loot_preview(no_loot)})"
            )

    vertical_entries = structure_policy_entries(
        vertical_rules,
        "vertical_layer_rules",
        "config/ascendant_structures/structure_vertical_layer_rules.json",
    )
    if vertical_entries:
        missing_vertical_layer = [
            entry.get("structure_id")
            for entry in vertical_entries
            if not entry.get("vertical_layers") or not entry.get("required_terrain")
        ]
        if missing_vertical_layer:
            warnings.append(
                "Ascendant structure vertical layer policy has rows missing layer or terrain requirements: "
                f"{len(missing_vertical_layer)} ({ascendant_loot_preview(missing_vertical_layer)})"
            )
        validation = vertical_rules.get("validation", {}) if isinstance(vertical_rules, dict) else {}
        if isinstance(validation, dict):
            for key, label in [
                ("water_structures_outside_water_regions", "water structures outside water/coast/ocean region policy"),
                ("sea_floor_structures_without_deep_water_rule", "sea-floor structures without deep-water rule"),
                ("sky_structures_common_or_near_spawn", "sky/floating structures common or near spawn"),
            ]:
                values = validation.get(key, [])
                if isinstance(values, list) and values:
                    warnings.append(
                        f"Ascendant structure vertical layer policy found {label}: "
                        f"{len(values)} ({ascendant_loot_preview(values)})"
                    )

    if isinstance(set_overrides, dict):
        candidates = set_overrides.get("candidate_overrides", [])
        if not isinstance(candidates, list):
            errors.append("config/ascendant_structures/structure_set_overrides.json must contain candidate_overrides.")
            candidates = []
        object_candidates = [entry for entry in candidates if isinstance(entry, dict)]
        if len(object_candidates) != len(candidates):
            errors.append("config/ascendant_structures/structure_set_overrides.json candidate_overrides contains non-object entries.")
        live_candidates = [
            entry.get("structure_set")
            for entry in object_candidates
            if entry.get("live_enabled") is True or "candidate_disabled" not in str(entry.get("review_status", ""))
        ]
        if live_candidates:
            warnings.append(
                "Ascendant structure override candidates look live or unreviewed: "
                f"{len(live_candidates)} ({ascendant_loot_preview(live_candidates)})"
            )
    else:
        errors.append("config/ascendant_structures/structure_set_overrides.json is missing or invalid.")

    water_entries = structure_policy_entries(
        water_policy,
        "water_structure_policy",
        "config/ascendant_structures/water_structure_policy.json",
    )
    if water_entries:
        bad_water_regions = [
            entry.get("structure_id")
            for entry in water_entries
            if entry.get("water_role") in {"sea_floor", "ship_or_ocean_surface", "ocean", "frozen_ocean", "coastline"}
            and not any(
                str(region) in {"verdant_coast", "coastal_only", "frostmarch_if_frozen", "frozen_ocean_only", "frostmarch", "north_east_marches", "south_east_wilds"}
                for region in entry.get("atlas_allowed_regions", [])
            )
        ]
        if bad_water_regions:
            warnings.append(
                "Ascendant water structure policy has water structures outside water/coast/ocean regions: "
                f"{len(bad_water_regions)} ({ascendant_loot_preview(bad_water_regions)})"
            )

    sky_entries = structure_policy_entries(
        sky_policy,
        "sky_structure_policy",
        "config/ascendant_structures/sky_structure_policy.json",
    )
    if sky_entries:
        risky_sky = [
            entry.get("structure_id")
            for entry in sky_entries
            if entry.get("density_class") == "common"
            or any(str(region) in {"hearthlands", "crownlands", "center"} for region in entry.get("atlas_allowed_regions", []))
        ]
        if risky_sky:
            warnings.append(
                "Ascendant sky structure policy has common or near-starter sky structures: "
                f"{len(risky_sky)} ({ascendant_loot_preview(risky_sky)})"
            )

    sea_floor_entries = structure_policy_entries(
        sea_floor_policy,
        "sea_floor_structure_policy",
        "config/ascendant_structures/sea_floor_structure_policy.json",
        required=False,
    )
    missing_deep_water = [
        entry.get("structure_id")
        for entry in sea_floor_entries
        if entry.get("required_terrain") != "deep_water_or_ocean_floor"
    ]
    if missing_deep_water:
        warnings.append(
            "Ascendant sea-floor policy has structures without deep-water terrain requirements: "
            f"{len(missing_deep_water)} ({ascendant_loot_preview(missing_deep_water)})"
        )

    structure_policy_entries(
        ship_policy,
        "ship_structure_policy",
        "config/ascendant_structures/ship_structure_policy.json",
        required=False,
    )

    dungeon_entries = structure_policy_entries(
        dungeon_policy,
        "dungeon_structure_policy",
        "config/ascendant_structures/dungeon_structure_policy.json",
    )
    if dungeon_entries:
        starter_dungeons = [
            entry.get("structure_id")
            for entry in dungeon_entries
            if any(str(region) in {"hearthlands", "crownlands", "center"} for region in entry.get("atlas_allowed_regions", []))
        ]
        if starter_dungeons:
            warnings.append(
                "Ascendant dungeon policy has dungeons allowed in beginner regions: "
                f"{len(starter_dungeons)} ({ascendant_loot_preview(starter_dungeons)})"
            )

    boss_entries = structure_policy_entries(
        boss_policy,
        "boss_structure_policy",
        "config/ascendant_structures/boss_structure_policy.json",
    )
    if boss_entries:
        starter_bosses = [
            entry.get("structure_id")
            for entry in boss_entries
            if any(str(region) in {"hearthlands", "crownlands", "center"} for region in entry.get("atlas_allowed_regions", []))
        ]
        if starter_bosses:
            warnings.append(
                "Ascendant boss policy has boss/dragon structures allowed in beginner regions: "
                f"{len(starter_bosses)} ({ascendant_loot_preview(starter_bosses)})"
            )

    structure_policy_entries(
        village_policy,
        "village_structure_policy",
        "config/ascendant_structures/village_structure_policy.json",
    )

    if isinstance(structure_test_points, dict):
        locate_sections = [
            key
            for key in structure_test_points
            if key.endswith("_locate_commands") or key == "priority_locate_commands"
        ]
        if not locate_sections:
            errors.append("config/ascendant_structures/structure_test_points.json must contain locate command sections.")
        elif not any(structure_test_points.get(key) for key in locate_sections):
            errors.append("config/ascendant_structures/structure_test_points.json locate command sections are empty.")
    else:
        errors.append("config/ascendant_structures/structure_test_points.json is missing or invalid.")

    required_route_sections = {
        "beginner_region_structures",
        "dungeon_structures",
        "water_structures",
        "sky_structures",
        "village_town_settlement_structures",
        "boss_dragon_structures",
        "region_fit_checks",
    }
    route_structure_ids: set[str] = set()
    if isinstance(structure_visual_review_route, dict):
        if structure_visual_review_route.get("status") != "manual_visual_review_route_no_live_generation_changes":
            warnings.append(
                "config/ascendant_structures/structure_visual_review_route.json is not marked review-only; "
                "verify no live structure overrides were enabled."
            )
        if structure_visual_review_route.get("live_gameplay_files_changed") is not False:
            warnings.append(
                "config/ascendant_structures/structure_visual_review_route.json must record that no live gameplay files changed."
            )
        sections = structure_visual_review_route.get("sections", [])
        if not isinstance(sections, list) or not sections:
            errors.append("config/ascendant_structures/structure_visual_review_route.json must contain non-empty sections.")
            sections = []
        section_ids = {
            str(section.get("section_id"))
            for section in sections
            if isinstance(section, dict) and section.get("section_id")
        }
        missing_sections = sorted(required_route_sections - section_ids)
        if missing_sections:
            errors.append(
                "config/ascendant_structures/structure_visual_review_route.json is missing route sections: "
                f"{missing_sections}"
            )
        missing_entry_fields: list[str] = []
        route_entries = 0
        locate_commands: set[str] = set()
        for section in sections:
            if not isinstance(section, dict):
                errors.append("config/ascendant_structures/structure_visual_review_route.json sections contains non-object entries.")
                continue
            entries = section.get("entries", [])
            if not isinstance(entries, list) or not entries:
                errors.append(
                    "config/ascendant_structures/structure_visual_review_route.json has an empty section: "
                    f"{section.get('section_id')}"
                )
                continue
            for entry in entries:
                if not isinstance(entry, dict):
                    errors.append("config/ascendant_structures/structure_visual_review_route.json entries must be objects.")
                    continue
                route_entries += 1
                sid = str(entry.get("structure_id", ""))
                if sid:
                    route_structure_ids.add(sid)
                locate_command = str(entry.get("locate_command", ""))
                if locate_command:
                    locate_commands.add(locate_command)
                review_result = entry.get("review_result", {})
                visual_questions = entry.get("visual_questions", [])
                required_fields = [
                    "structure_id",
                    "structure_set_id",
                    "source_mod",
                    "category",
                    "expected_atlas_region",
                    "expected_distance_ring",
                    "expected_vertical_layer",
                    "expected_rarity_density",
                    "expected_danger_tier",
                    "expected_loot_tier",
                    "locate_command",
                    "suggested_tp_command_after_locate",
                ]
                if any(entry.get(field) in (None, "", []) for field in required_fields):
                    missing_entry_fields.append(sid or "<missing id>")
                if not isinstance(visual_questions, list) or len(visual_questions) < 6:
                    missing_entry_fields.append(sid or "<missing id>")
                if not isinstance(review_result, dict) or not {"pass", "fail", "manual_review"}.issubset(review_result):
                    missing_entry_fields.append(sid or "<missing id>")
        if route_entries < 70:
            warnings.append(
                "config/ascendant_structures/structure_visual_review_route.json has fewer than 70 review entries; "
                "verify the first route still covers all requested sections."
            )
        if len(locate_commands) < 50:
            warnings.append(
                "config/ascendant_structures/structure_visual_review_route.json has fewer than 50 unique locate commands."
            )
        if missing_entry_fields:
            errors.append(
                "config/ascendant_structures/structure_visual_review_route.json entries are missing required review fields: "
                f"{len(missing_entry_fields)} ({ascendant_loot_preview(missing_entry_fields)})"
            )
        if known_ids:
            missing_route_ids = sorted(route_structure_ids - known_ids)
            if missing_route_ids:
                warnings.append(
                    "config/ascendant_structures/structure_visual_review_route.json references unknown structure IDs: "
                    f"{len(missing_route_ids)} ({ascendant_loot_preview(missing_route_ids)})"
                )
    else:
        errors.append("config/ascendant_structures/structure_visual_review_route.json is missing or invalid.")

    required_priority_queues = {
        "highest_risk_first_20": 20,
        "water_ship_seafloor_top_10": 10,
        "sky_floating_top_10": 10,
        "boss_dungeon_top_10": 10,
        "village_town_overlap_top_10": 10,
        "beginner_region_risks_top_10": 10,
    }
    if isinstance(structure_review_priority_queue, dict):
        queues = structure_review_priority_queue.get("priority_queues", {})
        if not isinstance(queues, dict) or not queues:
            errors.append("config/ascendant_structures/structure_review_priority_queue.json must contain priority_queues.")
            queues = {}
        for queue_name, minimum_count in required_priority_queues.items():
            queue_entries = queues.get(queue_name, [])
            if not isinstance(queue_entries, list):
                errors.append(f"Structure review priority queue {queue_name} must be a list.")
                continue
            if len(queue_entries) < minimum_count:
                warnings.append(
                    f"Structure review priority queue {queue_name} has {len(queue_entries)} entries; expected at least {minimum_count}."
                )
            for entry in queue_entries:
                if not isinstance(entry, dict):
                    errors.append(f"Structure review priority queue {queue_name} contains non-object entries.")
                    continue
                sid = str(entry.get("structure_id", ""))
                if not sid or not str(entry.get("locate_command", "")).startswith("/locate structure "):
                    errors.append(f"Structure review priority queue {queue_name} has an entry without a locate command.")
                if not isinstance(entry.get("review_result", {}), dict):
                    errors.append(f"Structure review priority queue {queue_name} has an entry without review_result.")
    else:
        errors.append("config/ascendant_structures/structure_review_priority_queue.json is missing or invalid.")

    if isinstance(structure_visual_review_findings, dict):
        if structure_visual_review_findings.get("status") != "field_review_evidence_no_live_generation_changes":
            warnings.append(
                "config/ascendant_structures/structure_visual_review_findings_latest.json is not marked no-live-change evidence."
            )
        findings = structure_visual_review_findings.get("findings", [])
        if not isinstance(findings, list) or not findings:
            errors.append("config/ascendant_structures/structure_visual_review_findings_latest.json must contain findings.")
        else:
            bad_findings = [
                str(entry.get("structure_id", "<missing id>"))
                for entry in findings
                if not isinstance(entry, dict)
                or not entry.get("structure_id")
                or not entry.get("classification")
                or not entry.get("suggested_fix_type")
            ]
            if bad_findings:
                errors.append(
                    "Structure visual review findings are missing required fields: "
                    f"{len(bad_findings)} ({ascendant_loot_preview(bad_findings)})"
                )
    else:
        errors.append("config/ascendant_structures/structure_visual_review_findings_latest.json is missing or invalid.")

    if isinstance(structure_evidence_registry, dict):
        if structure_evidence_registry.get("status") != "evidence_registry_no_live_generation_changes":
            errors.append("config/ascendant_structures/structure_evidence_registry.json must be marked evidence-only.")
        evidence_rows = structure_evidence_registry.get("structures", [])
        if not isinstance(evidence_rows, list) or not evidence_rows:
            errors.append("config/ascendant_structures/structure_evidence_registry.json must contain structures.")
        else:
            bad_evidence_rows = [
                str(entry.get("structure_id", "<missing id>"))
                for entry in evidence_rows
                if not isinstance(entry, dict)
                or not entry.get("structure_id")
                or "final_classification" not in entry
                or "confidence_score" not in entry
                or not isinstance(entry.get("name_hints_weak_only", {}), dict)
            ]
            if bad_evidence_rows:
                errors.append(
                    "Structure evidence registry rows are missing classification/confidence evidence: "
                    f"{len(bad_evidence_rows)} ({ascendant_loot_preview(bad_evidence_rows)})"
                )
    else:
        errors.append("config/ascendant_structures/structure_evidence_registry.json is missing or invalid.")

    if isinstance(structure_classification_confidence, dict):
        if structure_classification_confidence.get("status") != "classification_confidence_no_live_generation_changes":
            errors.append("config/ascendant_structures/structure_classification_confidence.json must be marked confidence-only.")
        summary = structure_classification_confidence.get("summary", {})
        rows = structure_classification_confidence.get("structures", [])
        if not isinstance(summary, dict) or not isinstance(rows, list) or not rows:
            errors.append("config/ascendant_structures/structure_classification_confidence.json must contain summary and structures.")
        elif int(summary.get("name_only_classification") or 0) != 0:
            errors.append(
                "Structure classification confidence summary reports name-only classifications: "
                f"{summary.get('name_only_classification')}"
            )
    else:
        errors.append("config/ascendant_structures/structure_classification_confidence.json is missing or invalid.")

    if isinstance(manual_structure_observations, dict):
        if manual_structure_observations.get("status") != "review_only_live_observation_import_no_generation_changes":
            errors.append("config/ascendant_structures/manual_structure_observations.json must be marked review-only.")
        observations = manual_structure_observations.get("observations", [])
        if not isinstance(observations, list) or len(observations) < 4:
            errors.append("config/ascendant_structures/manual_structure_observations.json must include Jayden's first four structure observations.")
        else:
            missing_observation_fields = [
                str(entry.get("requested_structure_id", "<missing id>"))
                for entry in observations
                if not isinstance(entry, dict)
                or not entry.get("requested_structure_id")
                or not entry.get("actual_structure_id_seen")
                or not entry.get("locate_command")
                or not isinstance(entry.get("visual_issue_tags", []), list)
                or not entry.get("decision")
            ]
            if missing_observation_fields:
                errors.append(
                    "Manual structure observations are missing required fields: "
                    f"{len(missing_observation_fields)} ({ascendant_loot_preview(missing_observation_fields)})"
                )
    else:
        errors.append("config/ascendant_structures/manual_structure_observations.json is missing or invalid.")

    if isinstance(structure_land_placement_candidates, dict):
        if structure_land_placement_candidates.get("status") != "disabled_review_only_not_loaded_by_minecraft":
            errors.append(
                "config/ascendant_structures/candidates/structure_land_placement_candidates.json must stay disabled review-only."
            )
        if structure_land_placement_candidates.get("do_not_move_to_openloader_without_approval") is not True:
            errors.append(
                "config/ascendant_structures/candidates/structure_land_placement_candidates.json must require approval before OpenLoader."
            )
        candidates = structure_land_placement_candidates.get("candidates", [])
        if not isinstance(candidates, list) or not candidates:
            errors.append(
                "config/ascendant_structures/candidates/structure_land_placement_candidates.json must contain candidates."
            )
        else:
            bad_candidates = [
                str(entry.get("structure_id", "<missing id>"))
                for entry in candidates
                if not isinstance(entry, dict)
                or not entry.get("structure_id")
                or entry.get("live_enabled") is not False
                or not entry.get("candidate_fix")
            ]
            if bad_candidates:
                errors.append(
                    "Structure land-placement candidates are missing required review fields: "
                    f"{len(bad_candidates)} ({ascendant_loot_preview(bad_candidates)})"
                )
    else:
        errors.append("config/ascendant_structures/candidates/structure_land_placement_candidates.json is missing or invalid.")

    for candidate_report, report_name in [
        (structure_region_lock_candidates, "config/ascendant_structures/candidates/structure_region_lock_candidates.json"),
        (structure_density_candidates, "config/ascendant_structures/candidates/structure_density_candidates.json"),
    ]:
        if not isinstance(candidate_report, dict):
            errors.append(f"{report_name} is missing or invalid.")
            continue
        if candidate_report.get("status") != "disabled_review_only_not_loaded_by_minecraft":
            errors.append(f"{report_name} must stay disabled review-only.")
        if candidate_report.get("do_not_move_to_openloader_without_approval") is not True:
            errors.append(f"{report_name} must require approval before OpenLoader.")
        candidate_rows = candidate_report.get("candidates", [])
        if not isinstance(candidate_rows, list):
            errors.append(f"{report_name} candidates must be a list.")
        elif report_name.endswith("structure_region_lock_candidates.json") and not candidate_rows:
            warnings.append("Structure region-lock candidate file is empty; verify evidence generation found no review candidates.")

    live_datapack_root = ROOT / "config/openloader/data/ascendant_structure_director_live"
    rollback_manifest = ROOT / "config/ascendant_structures/rollback/pre_structure_director_v1/rollback_manifest.json"
    helper_commands_source = ROOT / "local-mods/ascendant-atlas-regions/src/main/java/com/robbinstech/ascendant_atlas_regions/StructureDirectorCommands.java"
    if isinstance(live_structure_policy, dict):
        live_enabled = live_structure_policy.get("enabled") is True
        if live_enabled:
            if live_structure_policy.get("version") != "structure_director_live_v1":
                errors.append("config/ascendant_structures/live_structure_policy.json must use version structure_director_live_v1.")
            if live_structure_policy.get("rollback_supported") is not True:
                errors.append("Structure Director Live v1 must be rollback_supported.")
            if live_structure_policy.get("evidence_required") is not True:
                errors.append("Structure Director Live v1 must require evidence.")
            if live_structure_policy.get("minimum_live_confidence") != "strong":
                errors.append("Structure Director Live v1 minimum_live_confidence must be strong.")
            if not live_datapack_root.exists():
                errors.append("Structure Director Live v1 is enabled but the OpenLoader live datapack is missing.")
            elif not (live_datapack_root / "pack.mcmeta").exists():
                errors.append("Structure Director Live v1 datapack is missing pack.mcmeta.")
            if not rollback_manifest.exists():
                errors.append("Structure Director Live v1 rollback manifest is missing.")
            if not helper_commands_source.exists():
                errors.append("Structure Director helper commands are required but StructureDirectorCommands.java is missing.")
            else:
                helper_text = read_text(helper_commands_source)
                for command_name in [
                    "status",
                    "rule",
                    "here",
                    "test_context",
                    "dump_live_manifest",
                    "explain_last_denial",
                ]:
                    if f'"{command_name}"' not in helper_text:
                        errors.append(f"Structure Director helper command is missing /ascstructure {command_name}.")
            true_gate = live_structure_policy.get("true_pre_generation_context_veto", {})
            if isinstance(true_gate, dict) and true_gate.get("status") != "available":
                warnings.append(
                    "Structure Director Live v1 has no true pre-generation context veto yet; "
                    "current live controls are datapack/tag/spacing plus helper diagnostics."
                )
            live_rules = live_structure_policy.get("land_water_rules", [])
            if not isinstance(live_rules, list) or not live_rules:
                errors.append("Structure Director Live v1 must include land_water_rules.")
            else:
                required_live_rule_ids = {
                    "dragon_roost_land_context",
                    "dragon_cave_land_or_mountain_cover",
                    "vineyard_land_context",
                    "siren_island_water_context",
                }
                actual_rule_ids = {str(rule.get("rule_id")) for rule in live_rules if isinstance(rule, dict)}
                missing_rule_ids = sorted(required_live_rule_ids - actual_rule_ids)
                if missing_rule_ids:
                    errors.append(
                        "Structure Director Live v1 is missing required land/water rules: "
                        f"{ascendant_loot_preview(missing_rule_ids)}"
                    )
                for rule in live_rules:
                    if not isinstance(rule, dict):
                        errors.append("Structure Director Live v1 land_water_rules contains non-object entries.")
                        continue
                    structure_ids = rule.get("structure_ids", [])
                    if not isinstance(structure_ids, list) or not structure_ids:
                        errors.append(f"Structure Director live rule {rule.get('rule_id', '<missing>')} has no structure_ids.")
                        continue
                    unknown_rule_ids = sorted(str(value) for value in structure_ids if known_ids and str(value) not in known_ids)
                    if unknown_rule_ids:
                        errors.append(
                            f"Structure Director live rule {rule.get('rule_id', '<missing>')} references unknown structures: "
                            f"{ascendant_loot_preview(unknown_rule_ids)}"
                        )
                    allowed_hydrology = rule.get("allowed_hydrology_classes", [])
                    forbidden_hydrology = rule.get("forbidden_hydrology_classes", [])
                    if rule.get("requires_physical_context") is not True:
                        warnings.append(f"Structure Director live rule {rule.get('rule_id', '<missing>')} should require physical land/water context.")
                    if rule.get("center_must_be_water") is True and not allowed_hydrology:
                        warnings.append(f"Water live rule {rule.get('rule_id', '<missing>')} has no allowed_hydrology_classes.")
                    if rule.get("center_must_be_land") is True and not allowed_hydrology:
                        warnings.append(f"Land live rule {rule.get('rule_id', '<missing>')} has no allowed_hydrology_classes.")
                    if rule.get("center_must_be_land") is True and isinstance(forbidden_hydrology, list):
                        if not {"ocean", "deep_ocean"}.issubset(set(str(value) for value in forbidden_hydrology)):
                            warnings.append(f"Land live rule {rule.get('rule_id', '<missing>')} should forbid ocean and deep_ocean hydrology.")
                    if rule.get("center_must_be_water") is True:
                        for sid in structure_ids:
                            evidence_row = next(
                                (
                                    entry for entry in (structure_evidence_registry or {}).get("structures", [])
                                    if isinstance(entry, dict) and entry.get("structure_id") == sid
                                ),
                                {},
                            )
                            classification = evidence_row.get("final_classification", {}) if isinstance(evidence_row, dict) else {}
                            if classification.get("water_role") not in {"ocean", "sea_floor", "river_or_wetland"}:
                                errors.append(f"Water live rule references non-water evidence row: {sid}")
                    if rule.get("center_must_be_land") is True:
                        for sid in structure_ids:
                            evidence_row = next(
                                (
                                    entry for entry in (structure_evidence_registry or {}).get("structures", [])
                                    if isinstance(entry, dict) and entry.get("structure_id") == sid
                                ),
                                {},
                            )
                            classification = evidence_row.get("final_classification", {}) if isinstance(evidence_row, dict) else {}
                            if classification.get("water_role") not in {None, "none", ""}:
                                errors.append(f"Land live rule references water-classified evidence row: {sid}")
            exclusions = live_structure_policy.get("settlement_family_exclusions", [])
            if not isinstance(exclusions, list) or not exclusions:
                errors.append("Structure Director Live v1 must include at least one settlement-family exclusion.")
        elif live_datapack_root.exists():
            errors.append("Structure Director live datapack exists while live_structure_policy.enabled is false.")
    else:
        errors.append("config/ascendant_structures/live_structure_policy.json is missing or invalid.")

    if isinstance(live_structure_manifest, dict):
        if live_structure_manifest.get("enabled") is not True:
            errors.append("config/ascendant_structures/live_structure_manifest.json must be enabled for Live v1.")
        if not live_structure_manifest.get("live_changes"):
            errors.append("Structure Director Live v1 manifest has zero live changes.")
        if live_structure_manifest.get("density_override_count", 0) < 1:
            errors.append("Structure Director Live v1 must activate density overrides.")
        if live_structure_manifest.get("land_water_context_rule_count", 0) < 4:
            errors.append("Structure Director Live v1 must record dragon/vineyard/siren land-water rules.")
        if live_structure_manifest.get("settlement_exclusion_count", 0) < 1:
            errors.append("Structure Director Live v1 must activate at least one settlement overlap reduction.")
        manifest_ids = set(str(value) for value in live_structure_manifest.get("live_structure_ids", []))
        unknown_manifest_ids = sorted(manifest_ids - known_ids) if known_ids else []
        if unknown_manifest_ids:
            errors.append(
                "Structure Director Live v1 manifest references unknown structure IDs: "
                f"{len(unknown_manifest_ids)} ({ascendant_loot_preview(unknown_manifest_ids)})"
            )
        if live_datapack_root.exists():
            live_files = [
                path for path in live_datapack_root.rglob("*.json")
                if path.name != "pack.mcmeta"
            ]
            if not live_files:
                errors.append("Structure Director Live v1 datapack has no live JSON resources.")
            for path in live_files:
                try:
                    resource = read_json(path)
                except Exception as exc:
                    errors.append(f"Structure Director Live v1 JSON is malformed: {rel(path)} ({exc})")
                    continue
                try:
                    datapack_relative = path.relative_to(live_datapack_root).as_posix()
                except ValueError:
                    datapack_relative = path.as_posix()
                if datapack_relative.startswith("data/ascendant_structure_director_live/"):
                    errors.append(f"Structure Director override uses its own namespace instead of original resource path: {rel(path)}")
                if "worldgen/structure_set" in path.as_posix():
                    placement = resource.get("placement", {}) if isinstance(resource, dict) else {}
                    spacing = int(placement.get("spacing", 0) or 0)
                    separation = int(placement.get("separation", 0) or 0)
                    if spacing <= 0 or separation < 0 or separation >= spacing:
                        errors.append(
                            f"Structure Director live structure_set has invalid spacing/separation: "
                            f"{rel(path)} spacing={spacing} separation={separation}"
                        )
        if live_datapack_root.exists() and "datapack_hash" in live_structure_manifest:
            source_hash = directory_content_sha256(live_datapack_root).upper()
            if source_hash != str(live_structure_manifest.get("datapack_hash", "")).upper():
                errors.append(
                    "Structure Director Live v1 datapack hash differs from live_structure_manifest.json. "
                    "Regenerate the live manifest."
                )
    else:
        errors.append("config/ascendant_structures/live_structure_manifest.json is missing or invalid.")

    if isinstance(live_structure_results, dict):
        if live_structure_results.get("version") != "structure_director_live_v1":
            errors.append("config/ascendant_structures/live_structure_results.json must use version structure_director_live_v1.")
    else:
        errors.append("config/ascendant_structures/live_structure_results.json is missing or invalid.")

    if isinstance(live_test_targets, dict):
        targets = live_test_targets.get("targets", [])
        if not isinstance(targets, list) or len(targets) < 4:
            errors.append("config/ascendant_structures/live_test_targets.json must contain dragon/vineyard/siren/settlement tests.")
    else:
        errors.append("config/ascendant_structures/live_test_targets.json is missing or invalid.")

    if ACTIVE_CURSEFORGE_INSTANCE.exists() and isinstance(live_structure_policy, dict) and live_structure_policy.get("enabled") is True:
        active_datapack = ACTIVE_CURSEFORGE_INSTANCE / "config/openloader/data/ascendant_structure_director_live"
        active_policy = ACTIVE_CURSEFORGE_INSTANCE / "config/ascendant_structures/live_structure_policy.json"
        if not active_datapack.exists():
            errors.append("Active Ascendant Realms (2) instance is missing Structure Director Live v1 datapack; run sync while Minecraft is closed.")
        elif live_datapack_root.exists():
            source_hash = directory_content_sha256(live_datapack_root)
            active_hash = directory_content_sha256(active_datapack)
            if source_hash != active_hash:
                errors.append("Active Ascendant Realms (2) Structure Director Live v1 datapack hash is stale; run sync.")
        if not active_policy.exists():
            errors.append("Active Ascendant Realms (2) instance is missing live_structure_policy.json; run sync while Minecraft is closed.")

    live_override_root = ROOT / "config/openloader/data/ascendant_structure_overrides"
    if live_override_root.exists():
        marker_files = [
            path
            for path in live_override_root.rglob("*.json")
            if path.name != "pack.mcmeta"
        ]
        if marker_files:
            warnings.append(
                "Live Ascendant structure override datapack files exist; verify every one has explicit review approval: "
                f"{len(marker_files)} ({ascendant_loot_preview([rel(path) for path in marker_files])})"
            )

    if known_ids:
        missing_policy_ids = sorted(all_policy_ids - known_ids)
        for report in structure_reports.values():
            if not isinstance(report, dict):
                continue
            validation = report.get("validation", {})
            if isinstance(validation, dict):
                reported_missing = validation.get("policy_references_missing_structure_ids", [])
                if isinstance(reported_missing, list):
                    missing_policy_ids = sorted(set(missing_policy_ids) | set(str(value) for value in reported_missing))
        if missing_policy_ids:
            warnings.append(
                "Ascendant structure policy references missing structure IDs: "
                f"{len(missing_policy_ids)} ({ascendant_loot_preview(missing_policy_ids)})"
            )


def validate_ascendant_atmosphere(errors: list[str], warnings: list[str]) -> None:
    atmosphere_reports: dict[str, object] = {}
    for report_name in ASCENDANT_ATMOSPHERE_JSON_FILES:
        report_path = ROOT / report_name
        if not report_path.exists():
            continue
        try:
            report = read_json(report_path)
            if not isinstance(report, dict):
                errors.append(f"Ascendant atmosphere JSON must be an object: {report_name}")
                continue
            atmosphere_reports[report_name] = report
        except Exception as exc:
            errors.append(f"Ascendant atmosphere JSON is invalid: {report_name}: {exc}")

    for doc_name in ASCENDANT_ATMOSPHERE_REQUIRED_DOCS:
        if any((ROOT / path).exists() for path in ASCENDANT_ATMOSPHERE_JSON_FILES) and not (ROOT / doc_name).exists():
            warnings.append(f"Ascendant atmosphere policy exists but is not documented: {doc_name}")

    def validation_list(report: object, key: str) -> list[object]:
        if not isinstance(report, dict):
            return []
        validation = report.get("validation", {})
        if not isinstance(validation, dict):
            return []
        values = validation.get(key, [])
        return values if isinstance(values, list) else []

    region_policy = atmosphere_reports.get("config/ascendant_atmosphere/region_atmosphere.json")
    weather_policy = atmosphere_reports.get("config/ascendant_atmosphere/weather_policy.json")
    audio_policy = atmosphere_reports.get("config/ascendant_atmosphere/audio_policy.json")
    title_policy = atmosphere_reports.get("config/ascendant_atmosphere/title_policy.json")

    seen_region_ids: set[str] = set()
    if isinstance(region_policy, dict):
        if region_policy.get("status") != "audit_control_scaffold_only_no_live_atmosphere_changes":
            warnings.append("Ascendant regional atmosphere policy is not marked audit/control scaffold only.")
        scope = region_policy.get("scope", {})
        if isinstance(scope, dict):
            live_change_keys = [
                key
                for key in (
                    "changes_terrain",
                    "changes_mobs",
                    "changes_ores",
                    "changes_structures",
                    "changes_weather_configs",
                    "changes_audio_configs",
                    "changes_title_resource_pack",
                )
                if scope.get(key)
            ]
            if live_change_keys:
                errors.append(
                    "Ascendant atmosphere policy indicates forbidden live changes: "
                    f"{ascendant_loot_preview(live_change_keys)}"
                )
        regions = region_policy.get("regions", [])
        if not isinstance(regions, list) or not regions:
            errors.append("config/ascendant_atmosphere/region_atmosphere.json must contain regions.")
            regions = []
        object_regions = [entry for entry in regions if isinstance(entry, dict)]
        if len(object_regions) != len(regions):
            errors.append("config/ascendant_atmosphere/region_atmosphere.json regions contains non-object entries.")
        for entry in object_regions:
            region_id = str(entry.get("region_id") or "")
            if region_id:
                seen_region_ids.add(region_id)
            missing_fields = [
                field
                for field in (
                    "region_id",
                    "music_mood",
                    "ambient_sound_mood",
                    "weather_mood",
                    "display_name",
                    "subtitle_flavor",
                    "particle_visual_notes",
                    "season_behavior",
                    "snow_ice_permission",
                    "danger_mood",
                )
                if not entry.get(field)
            ]
            if missing_fields:
                errors.append(
                    f"Ascendant atmosphere region {region_id or '<missing>'} is missing fields: "
                    f"{', '.join(missing_fields)}"
                )
            snow_policy = entry.get("snow_ice_permission", {})
            if (
                isinstance(snow_policy, dict)
                and region_id in ASCENDANT_ATMOSPHERE_WARM_REGIONS
                and snow_policy.get("allow_snow_buildup") is True
            ):
                warnings.append(f"Warm Atlas region allows snow buildup in atmosphere policy: {region_id}")

        missing_regions = sorted(ASCENDANT_ATMOSPHERE_EXPECTED_REGIONS - seen_region_ids)
        if missing_regions:
            warnings.append(
                "Ascendant atmosphere policy is missing region rows: "
                f"{len(missing_regions)} ({ascendant_loot_preview(missing_regions)})"
            )
        missing_region_atmosphere = validation_list(region_policy, "missing_region_atmosphere")
        if missing_region_atmosphere:
            warnings.append(
                "Ascendant atmosphere validation reports missing region atmosphere: "
                f"{len(missing_region_atmosphere)} ({ascendant_loot_preview(missing_region_atmosphere)})"
            )
        missing_region_ids = validation_list(region_policy, "policy_references_missing_region_ids")
        if missing_region_ids:
            warnings.append(
                "Ascendant atmosphere policy references missing region IDs: "
                f"{len(missing_region_ids)} ({ascendant_loot_preview(missing_region_ids)})"
            )
        warm_snow = validation_list(region_policy, "warm_regions_allowing_snow_buildup")
        if warm_snow:
            warnings.append(
                "Ascendant atmosphere warm regions allow snow buildup: "
                f"{len(warm_snow)} ({ascendant_loot_preview(warm_snow)})"
            )

    weather2_snow = read_text(ROOT / "config/Weather2/Snow.toml")
    serene_seasons = read_text(ROOT / "config/sereneseasons/seasons.toml")
    snow_real_magic = read_text(ROOT / "config/snowrealmagic-common.yaml")
    if "Snowstorm_Snow_Buildup_AllowOutsideColdBiomes = false" not in weather2_snow:
        warnings.append("Weather2 snow buildup is not confirmed blocked outside cold biomes.")
    if "generate_snow_ice = false" not in serene_seasons:
        warnings.append("Serene Seasons blanket snow/ice generation may reintroduce warm-region snow.")
    if "snowAndIceMeltInWarmBiomes: true" not in snow_real_magic:
        warnings.append("Snow Real Magic warm-biome snow/ice melt is not enabled.")

    if isinstance(weather_policy, dict):
        if weather_policy.get("status") != "audit_control_scaffold_only_no_weather_config_changes":
            warnings.append("Ascendant weather policy is not marked no weather config changes.")
        validation = weather_policy.get("validation", {})
        if isinstance(validation, dict):
            if validation.get("weather2_allows_outside_cold_snow"):
                warnings.append("Ascendant weather policy says Weather2 allows outside-cold snow.")
            if validation.get("serene_seasons_blanket_snow_enabled"):
                warnings.append("Ascendant weather policy says Serene Seasons blanket snow is enabled.")
            if validation.get("snow_real_magic_warm_melt_disabled"):
                warnings.append("Ascendant weather policy says Snow Real Magic warm melt is disabled.")
        warm_snow = validation_list(weather_policy, "warm_regions_allowing_snow_buildup")
        if warm_snow:
            warnings.append(
                "Ascendant weather policy warm regions allow snow buildup: "
                f"{len(warm_snow)} ({ascendant_loot_preview(warm_snow)})"
            )

    if isinstance(audio_policy, dict):
        if audio_policy.get("status") != "audit_control_scaffold_only_no_audio_config_changes":
            warnings.append("Ascendant audio policy is not marked no audio config changes.")
        audio_regions = {
            str(entry.get("region_id"))
            for entry in audio_policy.get("region_audio_policy", [])
            if isinstance(entry, dict) and entry.get("region_id")
        }
        missing_audio_regions = sorted(ASCENDANT_ATMOSPHERE_EXPECTED_REGIONS - audio_regions)
        if missing_audio_regions:
            warnings.append(
                "Ascendant audio policy is missing region rows: "
                f"{len(missing_audio_regions)} ({ascendant_loot_preview(missing_audio_regions)})"
            )
        missing_ids = validation_list(audio_policy, "policy_references_missing_region_ids")
        if missing_ids:
            warnings.append(
                "Ascendant audio policy references missing region IDs: "
                f"{len(missing_ids)} ({ascendant_loot_preview(missing_ids)})"
            )

    if isinstance(title_policy, dict):
        if title_policy.get("status") != "audit_control_scaffold_only_no_title_resource_pack_changes":
            warnings.append("Ascendant title policy is not marked no title resource pack changes.")
        title_regions = {
            str(entry.get("region_id"))
            for entry in title_policy.get("region_titles", [])
            if isinstance(entry, dict) and entry.get("region_id")
        }
        missing_title_regions = sorted(ASCENDANT_ATMOSPHERE_EXPECTED_REGIONS - title_regions)
        if missing_title_regions:
            warnings.append(
                "Ascendant region title policy is missing region rows: "
                f"{len(missing_title_regions)} ({ascendant_loot_preview(missing_title_regions)})"
            )
        missing_title_policy = validation_list(title_policy, "missing_region_title_policy")
        if missing_title_policy:
            warnings.append(
                "Ascendant region title policy reports missing titles: "
                f"{len(missing_title_policy)} ({ascendant_loot_preview(missing_title_policy)})"
            )
        missing_ids = validation_list(title_policy, "policy_references_missing_region_ids")
        if missing_ids:
            warnings.append(
                "Ascendant title policy references missing region IDs: "
                f"{len(missing_ids)} ({ascendant_loot_preview(missing_ids)})"
            )
        current_title_stack = title_policy.get("current_title_stack", {})
        if isinstance(current_title_stack, dict):
            required_packs = current_title_stack.get("visual_title_resource_packs", {})
            if isinstance(required_packs, dict):
                missing_packs = [name for name, present in required_packs.items() if not present]
                if missing_packs:
                    warnings.append(
                        "Ascendant title policy expected visual/audio resource packs are missing from configured order: "
                        f"{len(missing_packs)} ({ascendant_loot_preview(missing_packs)})"
                    )


def validate_ascendant_travel_network(errors: list[str], warnings: list[str]) -> None:
    travel_reports: dict[str, object] = {}
    for report_name in ASCENDANT_TRAVEL_JSON_FILES:
        report_path = ROOT / report_name
        if not report_path.exists():
            continue
        try:
            report = read_json(report_path)
            if not isinstance(report, dict):
                errors.append(f"Ascendant travel JSON must be an object: {report_name}")
                continue
            travel_reports[report_name] = report
        except Exception as exc:
            errors.append(f"Ascendant travel JSON is invalid: {report_name}: {exc}")

    active_travel_mods = {
        "mods/yungs-bridges.pw.toml": "yungsbridges:bridges",
        "mods/macaws-bridges.pw.toml": "macaws_bridges:palette",
        "mods/integrated-villages.pw.toml": "integrated_villages:path_networks",
        "mods/towns-and-towers.pw.toml": "towns_and_towers:streets",
        "mods/moogs-voyager-structures.pw.toml": "mvs:paths",
        "mods/supplementaries.pw.toml": "supplementaries:way_sign",
    }
    present_expected_sources = {
        source_id
        for mod_path, source_id in active_travel_mods.items()
        if (ROOT / mod_path).exists()
    }
    seen_sources: set[str] = set()

    for doc_name in ASCENDANT_TRAVEL_REQUIRED_DOCS:
        if present_expected_sources and not (ROOT / doc_name).exists():
            warnings.append(f"Travel network docs are missing while road/bridge mods are present: {doc_name}")

    def collect_validation_values(report: object, key: str) -> list[object]:
        if not isinstance(report, dict):
            return []
        validation = report.get("validation", {})
        if not isinstance(validation, dict):
            return []
        values = validation.get(key, [])
        return values if isinstance(values, list) else []

    def validation_number(report: object, key: str) -> int:
        if not isinstance(report, dict):
            return 0
        validation = report.get("validation", {})
        if not isinstance(validation, dict):
            return 0
        value = validation.get(key, 0)
        return value if isinstance(value, int) else 0

    road_policy = travel_reports.get("config/ascendant_travel/road_policy.json")
    bridge_policy = travel_reports.get("config/ascendant_travel/bridge_policy.json")
    crossing_policy = travel_reports.get("config/ascendant_travel/river_crossing_policy.json")
    candidates = travel_reports.get("config/ascendant_travel/travel_network_candidates.json")

    if isinstance(road_policy, dict):
        if road_policy.get("status") != "reconnaissance_only_no_worldgen_changes":
            warnings.append("Ascendant travel road policy is not marked reconnaissance-only; verify road generation changes were approved.")
        scope = road_policy.get("scope", {})
        if isinstance(scope, dict):
            if scope.get("adds_roads") or scope.get("injects_villages") or scope.get("changes_live_generation"):
                errors.append("Ascendant travel road policy indicates live road/village/generation changes are enabled.")
        sources = road_policy.get("road_sources", [])
        if not isinstance(sources, list) or not sources:
            errors.append("config/ascendant_travel/road_policy.json must contain road_sources.")
            sources = []
        object_sources = [entry for entry in sources if isinstance(entry, dict)]
        if len(object_sources) != len(sources):
            errors.append("config/ascendant_travel/road_policy.json road_sources contains non-object entries.")
        for entry in object_sources:
            source_id = str(entry.get("source_id") or "")
            if source_id:
                seen_sources.add(source_id)
            if not source_id or not entry.get("mod_source") or not entry.get("recommendation"):
                errors.append("config/ascendant_travel/road_policy.json has a road source missing source_id, mod_source, or recommendation.")

        missing_policy = collect_validation_values(road_policy, "active_road_bridge_generators_without_policy")
        if missing_policy:
            warnings.append(
                "Ascendant travel has active road/bridge generators without policy: "
                f"{len(missing_policy)} ({ascendant_loot_preview(missing_policy)})"
            )
        cliff_or_floating = collect_validation_values(road_policy, "road_sources_with_known_cliff_or_floating_failures")
        if cliff_or_floating:
            warnings.append(
                "Ascendant travel road sources have known or suspected cliff/floating/bridge-absence failures: "
                f"{len(cliff_or_floating)} ({ascendant_loot_preview(cliff_or_floating)})"
            )
        route_purpose = collect_validation_values(road_policy, "road_sources_with_roads_to_nowhere_risk")
        if route_purpose:
            warnings.append(
                "Ascendant travel road sources may generate without clear route purpose: "
                f"{len(route_purpose)} ({ascendant_loot_preview(route_purpose)})"
            )
        live_changes = collect_validation_values(road_policy, "live_generation_changes_enabled")
        if live_changes:
            errors.append(
                "Ascendant travel road policy has live generation changes enabled without approval: "
                f"{ascendant_loot_preview(live_changes)}"
            )

    if isinstance(bridge_policy, dict):
        if bridge_policy.get("status") != "reconnaissance_only_no_worldgen_changes":
            warnings.append("Ascendant travel bridge policy is not marked reconnaissance-only; verify bridge generation changes were approved.")
        scope = bridge_policy.get("scope", {})
        if isinstance(scope, dict):
            if scope.get("adds_bridges") or scope.get("changes_live_generation"):
                errors.append("Ascendant travel bridge policy indicates live bridge/generation changes are enabled.")
        sources = bridge_policy.get("bridge_sources", [])
        if not isinstance(sources, list) or not sources:
            errors.append("config/ascendant_travel/bridge_policy.json must contain bridge_sources.")
            sources = []
        object_sources = [entry for entry in sources if isinstance(entry, dict)]
        if len(object_sources) != len(sources):
            errors.append("config/ascendant_travel/bridge_policy.json bridge_sources contains non-object entries.")
        for entry in object_sources:
            source_id = str(entry.get("source_id") or "")
            if source_id:
                seen_sources.add(source_id)
            if not source_id or not entry.get("mod_source") or not entry.get("recommendation"):
                errors.append("config/ascendant_travel/bridge_policy.json has a bridge source missing source_id, mod_source, or recommendation.")

        unlinked_bridge_sources = collect_validation_values(bridge_policy, "bridge_sources_without_crossing_strategy")
        if unlinked_bridge_sources:
            warnings.append(
                "Ascendant travel bridge structures are not fully linked to river/water crossing strategy: "
                f"{len(unlinked_bridge_sources)} ({ascendant_loot_preview(unlinked_bridge_sources)})"
            )
        live_changes = collect_validation_values(bridge_policy, "live_generation_changes_enabled")
        if live_changes:
            errors.append(
                "Ascendant travel bridge policy has live generation changes enabled without approval: "
                f"{ascendant_loot_preview(live_changes)}"
            )

    if isinstance(crossing_policy, dict):
        if crossing_policy.get("status") != "reconnaissance_only_no_worldgen_changes":
            warnings.append("Ascendant river crossing policy is not marked reconnaissance-only.")
        rules = crossing_policy.get("rules", [])
        if not isinstance(rules, list) or not rules:
            errors.append("config/ascendant_travel/river_crossing_policy.json must contain rules.")
        ocean_leak_count = validation_number(crossing_policy, "ocean_leak_samples_blocking_route_design")
        if ocean_leak_count:
            warnings.append(
                "Ascendant travel design is still blocked by Atlas water/terrain ocean-leak samples: "
                f"{ocean_leak_count}"
            )
        unlinked_bridge_sources = collect_validation_values(crossing_policy, "bridge_sources_without_crossing_strategy")
        if unlinked_bridge_sources:
            warnings.append(
                "Ascendant river crossing policy still has bridge sources needing linkage review: "
                f"{len(unlinked_bridge_sources)} ({ascendant_loot_preview(unlinked_bridge_sources)})"
            )

    if isinstance(candidates, dict):
        if candidates.get("status") != "disabled_review_only_no_live_generation_changes":
            warnings.append("Ascendant travel candidates are not marked disabled/review-only.")
        candidate_entries = candidates.get("candidates", [])
        if not isinstance(candidate_entries, list):
            errors.append("config/ascendant_travel/travel_network_candidates.json candidates must be a list.")
            candidate_entries = []
        enabled_candidates = [
            entry.get("candidate_id")
            for entry in candidate_entries
            if isinstance(entry, dict) and entry.get("enabled")
        ]
        if enabled_candidates:
            errors.append(
                "Ascendant travel candidates were enabled without approval: "
                f"{len(enabled_candidates)} ({ascendant_loot_preview(enabled_candidates)})"
            )
        live_changes = collect_validation_values(candidates, "live_generation_changes_enabled")
        if live_changes:
            errors.append(
                "Ascendant travel candidate policy has live generation changes enabled without approval: "
                f"{ascendant_loot_preview(live_changes)}"
            )

    missing_present_sources = sorted(present_expected_sources - seen_sources)
    if missing_present_sources:
        warnings.append(
            "Ascendant travel has active road/bridge-related mods with no matching policy source: "
            f"{len(missing_present_sources)} ({ascendant_loot_preview(missing_present_sources)})"
        )


def validate_ascendant_ui_clarity(errors: list[str], warnings: list[str]) -> None:
    reports: dict[str, object] = {}
    for report_name in ASCENDANT_UI_JSON_FILES:
        report_path = ROOT / report_name
        if not report_path.exists():
            continue
        try:
            report = read_json(report_path)
            if not isinstance(report, dict):
                errors.append(f"Ascendant UI policy JSON must be an object: {report_name}")
                continue
            reports[report_name] = report
        except Exception as exc:
            errors.append(f"Ascendant UI policy JSON is invalid: {report_name}: {exc}")

    if reports:
        for doc_name in ASCENDANT_UI_REQUIRED_DOCS:
            if not (ROOT / doc_name).exists():
                warnings.append(f"Ascendant UI policy exists but is not documented: {doc_name}")

    def validation_values(report: object, key: str) -> list[object]:
        if not isinstance(report, dict):
            return []
        validation = report.get("validation", {})
        if not isinstance(validation, dict):
            return []
        values = validation.get(key, [])
        return values if isinstance(values, list) else []

    tangible_gear_ids: set[str] = set()
    gear_registry_path = ROOT / "config/ascendant_index/gear_registry.json"
    if gear_registry_path.exists():
        try:
            gear_registry = read_json(gear_registry_path)
            if isinstance(gear_registry, dict):
                for collection_name in ASCENDANT_UI_TANGIBLE_GEAR_COLLECTIONS:
                    for entry in gear_registry.get(collection_name, []):
                        if isinstance(entry, dict) and entry.get("id"):
                            tangible_gear_ids.add(str(entry.get("id")))
        except Exception as exc:
            warnings.append(f"Could not validate Ascendant UI policy freshness against gear_registry.json: {exc}")

    tooltip_policy = reports.get("config/ascendant_ui/tooltip_policy.json")
    if isinstance(tooltip_policy, dict):
        if tooltip_policy.get("status") != "audit_control_scaffold_only_no_live_ui_rewrite":
            warnings.append("Ascendant tooltip policy is not marked audit/control-only.")
        missing_rarity_refs = validation_values(tooltip_policy, "tooltip_policy_references_missing_rarity")
        if missing_rarity_refs:
            warnings.append(
                "Ascendant tooltip policy references missing rarity ids: "
                f"{len(missing_rarity_refs)} ({ascendant_loot_preview(missing_rarity_refs)})"
            )
        duplicate_lines = validation_values(tooltip_policy, "duplicate_or_confusing_tooltip_lines")
        if duplicate_lines:
            warnings.append(
                "Ascendant tooltip policy found duplicate/confusing tooltip lines: "
                f"{len(duplicate_lines)} ({ascendant_loot_preview(duplicate_lines)})"
            )
        missing_tooltips = validation_values(tooltip_policy, "tooltip_item_ids_missing_for_tangible_items")
        if missing_tooltips:
            warnings.append(
                "Ascendant rarity tooltip script is missing tangible gear item IDs: "
                f"{len(missing_tooltips)} ({ascendant_loot_preview(missing_tooltips)})"
            )
        jei_conflicts = validation_values(tooltip_policy, "jei_material_unification_conflicts")
        if jei_conflicts:
            warnings.append(
                "Ascendant JEI tooltip policy conflicts with material unification: "
                f"{len(jei_conflicts)} ({ascendant_loot_preview(jei_conflicts)})"
            )
        script_status = tooltip_policy.get("rarity_tooltip_script", {})
        if isinstance(script_status, dict) and tangible_gear_ids:
            policy_count = int(script_status.get("tangible_item_count", 0) or 0)
            if policy_count != len(tangible_gear_ids):
                warnings.append(
                    "Ascendant tooltip policy may be stale against gear_registry.json: "
                    f"policy tangible count {policy_count}, registry tangible count {len(tangible_gear_ids)}."
                )

    rarity_policy = reports.get("config/ascendant_ui/rarity_visual_policy.json")
    if isinstance(rarity_policy, dict):
        if rarity_policy.get("status") != "audit_control_scaffold_only_no_visual_rewrite":
            warnings.append("Ascendant rarity visual policy is not marked audit/control-only.")
        border_misses = validation_values(rarity_policy, "rarity_ids_missing_item_border_for_tangible_items")
        if border_misses:
            warnings.append(
                "Ascendant Item Borders are missing tangible gear IDs: "
                f"{len(border_misses)} ({ascendant_loot_preview(border_misses)})"
            )
        border_mismatches = validation_values(rarity_policy, "item_border_color_mismatches")
        if border_mismatches:
            warnings.append(
                "Ascendant Item Borders have rarity color mismatches: "
                f"{len(border_mismatches)} ({ascendant_loot_preview(border_mismatches)})"
            )
        missing_palette_colors = validation_values(rarity_policy, "rarity_palette_missing_item_border_colors")
        if missing_palette_colors:
            warnings.append(
                "Ascendant rarity palette colors are not present in Item Borders manual colors: "
                f"{len(missing_palette_colors)} ({ascendant_loot_preview(missing_palette_colors)})"
            )
        duplicate_borders = validation_values(rarity_policy, "duplicate_item_border_entries")
        if duplicate_borders:
            warnings.append(
                "Ascendant Item Borders has duplicate manual border item entries: "
                f"{len(duplicate_borders)} ({ascendant_loot_preview(duplicate_borders)})"
            )
        loot_beam_conflicts = validation_values(rarity_policy, "loot_beam_color_policy_conflicts")
        if loot_beam_conflicts:
            warnings.append(
                "Loot Beams no longer matches Ascendant rarity color policy: "
                f"{len(loot_beam_conflicts)} ({ascendant_loot_preview(loot_beam_conflicts)})"
            )
        item_borders = rarity_policy.get("item_borders", {})
        if isinstance(item_borders, dict) and tangible_gear_ids:
            policy_count = int(item_borders.get("tangible_item_count", 0) or 0)
            if policy_count != len(tangible_gear_ids):
                warnings.append(
                    "Ascendant rarity visual policy may be stale against gear_registry.json: "
                    f"policy tangible count {policy_count}, registry tangible count {len(tangible_gear_ids)}."
                )

    danger_policy = reports.get("config/ascendant_ui/mob_danger_display_policy.json")
    if isinstance(danger_policy, dict):
        if danger_policy.get("status") != "audit_control_scaffold_only_no_new_overlay":
            warnings.append("Ascendant mob danger display policy is not marked audit/control-only.")
        missing_settings = validation_values(danger_policy, "health_bar_plus_missing_required_settings")
        if missing_settings:
            warnings.append(
                "Health Bar Plus does not satisfy Ascendant danger display policy: "
                f"{len(missing_settings)} ({ascendant_loot_preview(missing_settings)})"
            )
        boss_blacklist_missing = validation_values(danger_policy, "boss_blacklist_missing")
        if boss_blacklist_missing:
            warnings.append(
                "Health Bar Plus boss blacklist is missing entries: "
                f"{len(boss_blacklist_missing)} ({ascendant_loot_preview(boss_blacklist_missing)})"
            )

    region_policy = reports.get("config/ascendant_ui/region_title_policy.json")
    if isinstance(region_policy, dict):
        if region_policy.get("status") != "audit_control_scaffold_only_no_region_title_runtime_hook":
            warnings.append("Ascendant region title UI policy is not marked audit/control-only.")
        missing_regions = validation_values(region_policy, "region_title_policy_missing_regions")
        if missing_regions:
            warnings.append(
                "Ascendant region title policy is missing Atlas regions: "
                f"{len(missing_regions)} ({ascendant_loot_preview(missing_regions)})"
            )
        missing_packs = validation_values(region_policy, "resource_pack_order_missing_required_visual_packs")
        if missing_packs:
            warnings.append(
                "Required Ascendant UI/title resource packs are missing from the policy snapshot: "
                f"{len(missing_packs)} ({ascendant_loot_preview(missing_packs)})"
            )
        order_conflicts = validation_values(region_policy, "resource_pack_order_conflicts")
        if order_conflicts:
            warnings.append(
                "Ascendant UI/title resource pack order has conflicts: "
                f"{len(order_conflicts)} ({ascendant_loot_preview(order_conflicts)})"
            )
        sync_gaps = validation_values(region_policy, "sync_coverage_missing")
        if sync_gaps:
            warnings.append(
                "Ascendant UI config files are missing from active-client sync coverage: "
                f"{len(sync_gaps)} ({ascendant_loot_preview(sync_gaps)})"
            )

    death_policy = reports.get("config/ascendant_ui/death_waypoint_policy.json")
    if isinstance(death_policy, dict):
        if death_policy.get("status") != "active_client_death_waypoint_clutter_control":
            warnings.append("Ascendant death waypoint policy is not marked as the active clutter-control policy.")
        if death_policy.get("owner") != "xaeros_minimap":
            warnings.append("Ascendant death waypoint policy does not declare Xaero's Minimap as owner.")

        implemented_behavior = death_policy.get("implemented_behavior", {})
        if not isinstance(implemented_behavior, dict):
            errors.append("Ascendant death waypoint policy must include implemented_behavior.")
            implemented_behavior = {}
        if implemented_behavior.get("current_deathpoint_visible") is not True:
            errors.append("Ascendant death waypoint policy must keep the current deathpoint visible.")
        if implemented_behavior.get("old_deathpoints_rendering_enabled") is not False:
            errors.append("Ascendant death waypoint policy must disable old deathpoint world rendering.")
        if implemented_behavior.get("exact_old_death_only_distance_supported_by_current_xaero_profile") is not False:
            warnings.append("Ascendant death waypoint policy should document that Xaero lacks an old-death-only distance setting.")

        xaero_settings = death_policy.get("xaero_profile_settings", {})
        if isinstance(xaero_settings, dict):
            if xaero_settings.get("deathpoints") is not True:
                errors.append("Ascendant death waypoint policy must set Xaero deathpoints to true.")
            if xaero_settings.get("old_deathpoints") is not False:
                errors.append("Ascendant death waypoint policy must set Xaero old_deathpoints to false.")
        else:
            errors.append("Ascendant death waypoint policy must include xaero_profile_settings.")

        sync_script = ROOT / "scripts/sync-active-client-files.ps1"
        if sync_script.exists():
            sync_text = read_text(sync_script)
            for expected_text in ["Apply-DeathWaypointPolicy", "death_waypoint_policy.json", "Applied Ascendant death waypoint policy"]:
                if expected_text not in sync_text:
                    errors.append(f"scripts/sync-active-client-files.ps1 is missing death waypoint policy sync marker: {expected_text}")

        active_xaero_profile = ACTIVE_CURSEFORGE_INSTANCE / "config/xaero/minimap/profiles/default.cfg"
        if active_xaero_profile.exists():
            active_xaero_text = read_text(active_xaero_profile)
            if not re.search(r"(?m)^deathpoints\s*=\s*true\s*$", active_xaero_text):
                warnings.append("Active Xaero minimap profile does not have deathpoints = true.")
            if not re.search(r"(?m)^old_deathpoints\s*=\s*false\s*$", active_xaero_text):
                warnings.append(
                    "Active Xaero minimap profile still has old deathpoints enabled. "
                    "Run scripts/sync-active-client-files.ps1 while Minecraft is closed."
                )

        active_xaero_waypoint_root = ACTIVE_CURSEFORGE_INSTANCE / "xaero/minimap"
        if active_xaero_waypoint_root.exists():
            enabled_old_deathpoints: list[str] = []
            for waypoint_file in active_xaero_waypoint_root.rglob("waypoints.txt"):
                try:
                    for line in read_text(waypoint_file).splitlines():
                        if line.startswith("waypoint:gui.xaero_deathpoint_old:"):
                            parts = line.split(":")
                            if len(parts) > 7 and parts[7] != "true":
                                enabled_old_deathpoints.append(str(waypoint_file.relative_to(ACTIVE_CURSEFORGE_INSTANCE)))
                                break
                except OSError as exc:
                    warnings.append(f"Could not inspect active Xaero waypoint file {waypoint_file}: {exc}")
            if enabled_old_deathpoints:
                warnings.append(
                    "Active Xaero waypoint files still have enabled old deathpoint markers: "
                    f"{len(enabled_old_deathpoints)} file(s) ({ascendant_loot_preview(enabled_old_deathpoints, limit=5)}). "
                    "Run scripts/sync-active-client-files.ps1 while Minecraft is closed."
                )

    options_path = ROOT / "options.txt"
    if options_path.exists():
        options_text = read_text(options_path)
        match = re.search(r"(?m)^resourcePacks:(\[.*\])$", options_text)
        if match:
            try:
                resource_packs = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                warnings.append(f"Could not parse options.txt for Ascendant UI resource-pack validation: {exc}")
                resource_packs = []
            if isinstance(resource_packs, list):
                missing_required_packs = [
                    pack
                    for pack in ASCENDANT_UI_REQUIRED_RESOURCE_PACKS
                    if pack not in resource_packs
                ]
                if missing_required_packs:
                    warnings.append(
                        "options.txt excludes required Ascendant UI/visual resource packs: "
                        f"{len(missing_required_packs)} ({ascendant_loot_preview(missing_required_packs)})"
                    )

    sync_script_path = ROOT / "scripts/sync-active-client-files.ps1"
    if sync_script_path.exists():
        sync_text = read_text(sync_script_path)
        missing_sync_tokens = [
            token
            for token in ASCENDANT_UI_SYNC_REQUIRED_TOKENS
            if token not in sync_text
        ]
        if missing_sync_tokens:
            warnings.append(
                "scripts/sync-active-client-files.ps1 is missing Ascendant UI sync coverage: "
                f"{len(missing_sync_tokens)} ({ascendant_loot_preview(missing_sync_tokens)})"
            )


def validate_ascendant_npc_visual_identity(
    errors: list[str],
    warnings: list[str],
    gear_items_by_id: dict[str, dict],
) -> None:
    reports: dict[str, object] = {}
    for report_name in ASCENDANT_NPC_VISUAL_JSON_FILES:
        report_path = ROOT / report_name
        if not report_path.exists():
            continue
        try:
            report = read_json(report_path)
            if not isinstance(report, dict):
                errors.append(f"Ascendant NPC visual JSON must be an object: {report_name}")
                continue
            reports[report_name] = report
        except Exception as exc:
            errors.append(f"Ascendant NPC visual JSON is invalid: {report_name}: {exc}")

    if reports:
        for doc_name in ASCENDANT_NPC_VISUAL_REQUIRED_DOCS:
            if not (ROOT / doc_name).exists():
                warnings.append(f"Ascendant NPC visual policy exists but is not documented: {doc_name}")

    def validation_values(report: object, key: str) -> list[object]:
        if not isinstance(report, dict):
            return []
        validation = report.get("validation", {})
        if not isinstance(validation, dict):
            return []
        values = validation.get(key, [])
        return values if isinstance(values, list) else []

    def profile_ids_from_loadouts() -> set[str]:
        loadouts_path = ROOT / "config/ascendant_guild/npc_loadouts.json"
        if not loadouts_path.exists():
            return set()
        try:
            loadouts = read_json(loadouts_path)
        except Exception as exc:
            errors.append(f"npc_loadouts.json is invalid for NPC visual validation: {exc}")
            return set()
        if not isinstance(loadouts, dict):
            return set()
        return {
            str(profile_id)
            for group_name in ("archetypes", "npc_profiles")
            for profile_id, profile in (loadouts.get(group_name, {}) or {}).items()
            if isinstance(profile, dict)
        }

    def profile_ids_from_nameplates() -> set[str]:
        nameplates_path = ROOT / "config/ascendant_guild/nameplates.json"
        if not nameplates_path.exists():
            return set()
        try:
            nameplates = read_json(nameplates_path)
        except Exception as exc:
            errors.append(f"nameplates.json is invalid for NPC visual validation: {exc}")
            return set()
        if not isinstance(nameplates, dict):
            return set()
        profiles = nameplates.get("profiles", {})
        return {str(profile_id) for profile_id in profiles} if isinstance(profiles, dict) else set()

    known_loadouts = profile_ids_from_loadouts()
    known_nameplates = profile_ids_from_nameplates()

    policy = reports.get("config/ascendant_guild/npc_visual_policy.json")
    if isinstance(policy, dict):
        if policy.get("status") != "audit_control_scaffold_only_no_npc_placement":
            warnings.append("Ascendant NPC visual policy is not marked audit/control-only.")
        scope = policy.get("scope", {})
        if isinstance(scope, dict):
            live_flags = [
                key
                for key in ("places_npcs", "injects_villages", "adds_npc_mods", "changes_spawn_rules", "changes_structure_generation")
                if scope.get(key)
            ]
            if live_flags:
                errors.append(
                    "Ascendant NPC visual policy claims live NPC/world changes are enabled without approval: "
                    f"{', '.join(live_flags)}"
                )
        missing_mca = validation_values(policy, "mca_medieval_pack_missing_or_inactive")
        if missing_mca:
            warnings.append(
                "MCA medieval visual layer is missing or inactive: "
                f"{len(missing_mca)} ({ascendant_loot_preview(missing_mca)})"
            )
        validation = policy.get("validation", {})
        if isinstance(validation, dict) and validation.get("mca_medieval_pack_active") is False:
            warnings.append("MCA Reborn is present but the MCA Default Medieval visual pack is not active.")
        modern_flags = validation_values(policy, "modern_or_unknown_skin_review_flags")
        if modern_flags:
            warnings.append(
                "MCA medieval skin audit found modern or unknown tone-review flags: "
                f"{len(modern_flags)} ({ascendant_loot_preview(modern_flags)})"
            )
        missing_bridge_skins = validation_values(policy, "generated_bridge_skins_missing")
        if missing_bridge_skins:
            warnings.append(
                "Generated CustomNPC MCA-style bridge skins are missing: "
                f"{len(missing_bridge_skins)} ({ascendant_loot_preview(missing_bridge_skins)})"
            )
        loadout_misses = validation_values(policy, "loadout_missing_gear_item_ids")
        if loadout_misses:
            warnings.append(
                "NPC visual/loadout policy references gear missing from gear_registry.json: "
                f"{len(loadout_misses)}"
            )
        visual_note_misses = validation_values(policy, "visual_only_skin_without_equivalent_item_note")
        if visual_note_misses:
            warnings.append(
                "NPC visual-only skins are missing equivalent gear/clothing notes: "
                f"{len(visual_note_misses)} ({ascendant_loot_preview(visual_note_misses)})"
            )

    silhouettes_report = reports.get("config/ascendant_guild/npc_profession_silhouettes.json")
    if isinstance(silhouettes_report, dict):
        if silhouettes_report.get("status") != "visual_identity_policy_only_no_world_placement":
            warnings.append("Ascendant NPC profession silhouettes are not marked visual-policy-only.")
        silhouettes = silhouettes_report.get("silhouettes", [])
        if not isinstance(silhouettes, list) or not silhouettes:
            errors.append("config/ascendant_guild/npc_profession_silhouettes.json must contain silhouettes.")
            silhouettes = []
        object_silhouettes = [entry for entry in silhouettes if isinstance(entry, dict)]
        if len(object_silhouettes) != len(silhouettes):
            errors.append("NPC profession silhouettes contain non-object entries.")
        silhouette_ids = {
            str(entry.get("profession_id"))
            for entry in object_silhouettes
            if entry.get("profession_id")
        }
        missing_silhouettes = sorted(ASCENDANT_IMPORTANT_NPC_PROFESSIONS - silhouette_ids)
        if missing_silhouettes:
            warnings.append(
                "Important NPC professions lack silhouette policy: "
                f"{len(missing_silhouettes)} ({ascendant_loot_preview(missing_silhouettes)})"
            )
        for entry in object_silhouettes:
            profession_id = str(entry.get("profession_id") or "<unknown>")
            if entry.get("uses_visual_only_skin") and not str(entry.get("visual_only_skin_equivalent_item_note", "")).strip():
                warnings.append(f"NPC profession {profession_id} uses visual_only_skin without an equivalent item note.")
            loadout_profile_id = entry.get("loadout_profile_id")
            if loadout_profile_id and str(loadout_profile_id) not in known_loadouts:
                warnings.append(f"NPC profession {profession_id} references missing loadout profile {loadout_profile_id}.")
            nameplate_profile_id = entry.get("nameplate_profile_id")
            if nameplate_profile_id and str(nameplate_profile_id) not in known_nameplates:
                warnings.append(f"NPC profession {profession_id} references missing nameplate profile {nameplate_profile_id}.")
            for item_id in entry.get("gear_item_ids", []):
                item_id = str(item_id)
                if item_id and item_id not in gear_items_by_id:
                    warnings.append(f"NPC profession {profession_id} references missing gear item {item_id}.")

    roster_report = reports.get("config/ascendant_guild/rival_hunter_roster.json")
    if isinstance(roster_report, dict):
        if roster_report.get("status") != "visual_roster_only_no_spawn_or_village_injection":
            warnings.append("Ascendant rival hunter roster is not marked visual-roster-only.")
        rivals = roster_report.get("rivals", [])
        if not isinstance(rivals, list) or not rivals:
            errors.append("config/ascendant_guild/rival_hunter_roster.json must contain rivals.")
            rivals = []
        object_rivals = [entry for entry in rivals if isinstance(entry, dict)]
        if len(object_rivals) != len(rivals):
            errors.append("Rival hunter roster contains non-object entries.")
        roster_ids = {
            str(entry.get("rival_id"))
            for entry in object_rivals
            if entry.get("rival_id")
        }
        missing_rivals = sorted(RIVAL_PROFILE_IDS - roster_ids)
        if missing_rivals:
            warnings.append(
                "Rival hunter roster is missing expected rivals: "
                f"{len(missing_rivals)} ({ascendant_loot_preview(missing_rivals)})"
            )
        for entry in object_rivals:
            rival_id = str(entry.get("rival_id") or "<unknown>")
            for key in ("rank", "style", "gear_tier", "nameplate_profile_id", "loadout_profile_id", "drop_policy"):
                if not str(entry.get(key, "")).strip():
                    warnings.append(f"Rival hunter {rival_id} is missing {key}.")
            loadout_profile_id = entry.get("loadout_profile_id")
            if loadout_profile_id and str(loadout_profile_id) not in known_loadouts:
                warnings.append(f"Rival hunter {rival_id} references missing loadout profile {loadout_profile_id}.")
            nameplate_profile_id = entry.get("nameplate_profile_id")
            if nameplate_profile_id and str(nameplate_profile_id) not in known_nameplates:
                warnings.append(f"Rival hunter {rival_id} references missing nameplate profile {nameplate_profile_id}.")
            if entry.get("uses_visual_only_skin") and not str(entry.get("visual_only_skin_equivalent_item_note", "")).strip():
                warnings.append(f"Rival hunter {rival_id} uses visual_only_skin without an equivalent item note.")
            for item_id in entry.get("gear_item_ids", []):
                item_id = str(item_id)
                if item_id and item_id not in gear_items_by_id:
                    warnings.append(f"Rival hunter {rival_id} references missing gear item {item_id}.")


def iter_loadout_profiles(loadouts: dict):
    for group_name in ("archetypes", "npc_profiles"):
        for profile_id, profile in loadouts.get(group_name, {}).items():
            if isinstance(profile, dict):
                yield group_name, profile_id, profile


def iter_equipment_slots(profile: dict):
    equipment = profile.get("equipment", {})
    if not isinstance(equipment, dict):
        return
    for slot_name, slot_data in equipment.items():
        if slot_name not in NPC_LOADOUT_SLOT_KEYS:
            continue
        if isinstance(slot_data, dict):
            yield slot_name, slot_data
        elif isinstance(slot_data, list):
            for entry in slot_data:
                if isinstance(entry, dict):
                    yield slot_name, entry


def rank_allowed_rarities(loadouts: dict, rank: str) -> set[str]:
    rank_rules = loadouts.get("rank_rules", {})
    rule = rank_rules.get(rank, {}) if isinstance(rank_rules, dict) else {}
    allowed = rule.get("allowed_rarities", [])
    if isinstance(allowed, list):
        return {str(rarity) for rarity in allowed}
    return set()


def parse_options_keybinds(path: pathlib.Path) -> dict[str, str]:
    keybinds: dict[str, str] = {}
    if not path.exists():
        return keybinds
    for line in read_text(path).splitlines():
        if not line.startswith("key_") or ":" not in line:
            continue
        key_name, key_value = line.split(":", 1)
        keybinds[key_name] = key_value
    return keybinds


def validate_ascendant_keybind_policy(errors: list[str], warnings: list[str]) -> None:
    policy_path = ROOT / "config/ascendant_ui/keybind_policy.json"
    if not policy_path.exists():
        return

    try:
        policy = read_json(policy_path)
    except Exception as exc:
        errors.append(f"config/ascendant_ui/keybind_policy.json is invalid JSON: {exc}")
        return

    if not isinstance(policy, dict):
        errors.append("config/ascendant_ui/keybind_policy.json must be a JSON object.")
        return

    if policy.get("version") != 1:
        errors.append("config/ascendant_ui/keybind_policy.json must use version 1.")

    bindings = policy.get("bindings")
    if not isinstance(bindings, dict) or not bindings:
        errors.append("config/ascendant_ui/keybind_policy.json must contain a non-empty bindings object.")
        return

    required_bindings = {
        "key_key.puffish_skills.open": "key.keyboard.k",
        "key_Quest Log": "key.keyboard.l",
        "key_key.irons_spellbooks.spell_wheel": "key.keyboard.r",
        "key_key.irons_spellbooks.spellbook_cast": "key.keyboard.v",
        "key_key.irons_spellbooks.spell_bar_modifier": "key.keyboard.left.alt",
        "key_keybinds.combatroll.roll": "key.keyboard.z",
        "key_key.sophisticatedbackpacks.open_backpack": "key.keyboard.b",
        "key_key.curios.open.desc": "key.keyboard.g",
        "key_gui.xaero_waypoints_key": "key.keyboard.u",
        "key_gui.xaero_minimap_settings": "key.keyboard.y",
    }
    for key_name, expected_key in required_bindings.items():
        if bindings.get(key_name) != expected_key:
            errors.append(
                "Ascendant keybind policy must keep "
                f"{key_name} on {expected_key}; found {bindings.get(key_name)!r}."
            )

    intentionally_unbound = [
        "key_iris.keybind.reload",
        "key_iris.keybind.toggleShaders",
        "key_iris.keybind.shaderPackSelection",
        "key_Scene1 start/pause",
        "key_Scene2 start/pause",
        "key_Scene3 start/pause",
        "key_Scene reset",
        "key_key.titles.openTitleSelection",
        "key_key.presencefootsteps.settings",
        "key_key.mca.skin_library",
        "key_key.saveToolbarActivator",
        "key_key.loadToolbarActivator",
        "key_key.advancements",
    ]
    for key_name in intentionally_unbound:
        if bindings.get(key_name) != "key.keyboard.unknown":
            errors.append(f"Ascendant keybind policy must leave {key_name} unbound.")

    used: dict[str, list[str]] = {}
    for key_name, key_value in bindings.items():
        if not isinstance(key_value, str):
            errors.append(f"Ascendant keybind policy binding {key_name} must be a string.")
            continue
        if key_value == "key.keyboard.unknown":
            continue
        used.setdefault(key_value, []).append(str(key_name))
    duplicate_policy_binds = {
        key_value: sorted(names)
        for key_value, names in used.items()
        if len(names) > 1
    }
    if duplicate_policy_binds:
        errors.append(
            "Ascendant keybind policy contains duplicate bound keys: "
            f"{ascendant_loot_preview([f'{key}: {names}' for key, names in duplicate_policy_binds.items()], limit=5)}"
        )

    sync_script = ROOT / "scripts/sync-active-client-files.ps1"
    if sync_script.exists():
        sync_text = read_text(sync_script)
        for expected_text in ["Apply-KeybindPolicy", "keybind_policy.json", "Applied Ascendant keybind policy"]:
            if expected_text not in sync_text:
                errors.append(f"scripts/sync-active-client-files.ps1 is missing keybind policy sync marker: {expected_text}")

    for doc_name, expected_terms in {
        "docs/KEYBIND_REEVALUATION.md": ["Iron's Spells spell wheel", "shader reload", "Combat Roll", "Ascendant Web"],
        "docs/MAGIC_UI_SKILL_HANDOFF.md": ["Iron's Spells", "Puffish Skills", "Ascendant Web", "audit-only", "keybind_policy.json"],
    }.items():
        doc_path = ROOT / doc_name
        if not doc_path.exists():
            continue
        doc_text = read_text(doc_path)
        for expected_term in expected_terms:
            if expected_term not in doc_text:
                warnings.append(f"{doc_name} may be missing key handoff term: {expected_term}")

    active_options = ACTIVE_CURSEFORGE_INSTANCE / "options.txt"
    if active_options.exists():
        active_keybinds = parse_options_keybinds(active_options)
        drift = []
        for key_name, expected_key in bindings.items():
            actual_key = active_keybinds.get(str(key_name))
            if actual_key is not None and actual_key != expected_key:
                drift.append(f"{key_name} expected {expected_key} got {actual_key}")
        if drift:
            warnings.append(
                "Active CurseForge options.txt differs from config/ascendant_ui/keybind_policy.json: "
                f"{ascendant_loot_preview(drift, limit=8)}. Run scripts/sync-active-client-files.ps1 while Minecraft is closed."
            )


def is_valid_hex_color(value: str) -> bool:
    return bool(re.fullmatch(r"#[0-9A-Fa-f]{6}", value or ""))


def has_utf8_bom(path: pathlib.Path) -> bool:
    try:
        return path.read_bytes().startswith(b"\xef\xbb\xbf")
    except OSError:
        return False


def probe_media_streams(path: pathlib.Path) -> tuple[list[dict[str, object]], str | None]:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-print_format",
                "json",
                "-show_streams",
                str(path),
            ],
            capture_output=True,
            check=False,
            text=True,
        )
    except FileNotFoundError:
        return [], "ffprobe is not available; FancyMenu MP4 codec checks were skipped."

    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        return [], f"ffprobe could not inspect {path.name}: {detail or 'unknown error'}"

    try:
        data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError as exc:
        return [], f"ffprobe returned invalid JSON for {path.name}: {exc}"

    streams = data.get("streams", [])
    if not isinstance(streams, list):
        return [], f"ffprobe returned an unexpected stream list for {path.name}."
    return [stream for stream in streams if isinstance(stream, dict)], None


def pack_forge_version(pack_text: str) -> tuple[int, ...] | None:
    match = re.search(r'(?m)^forge\s*=\s*"([^"]+)"', pack_text)
    if not match:
        return None
    return version_tuple(match.group(1))


def version_tuple(value: str) -> tuple[int, ...]:
    parts = re.findall(r"\d+", value)
    return tuple(int(part) for part in parts)


def toml_int_setting(text: str, setting: str) -> int | None:
    match = re.search(rf"(?m)^\s*{re.escape(setting)}\s*=\s*(-?\d+)\s*$", text)
    return int(match.group(1)) if match else None


def spawn_balance_default_weights(text: str) -> dict[str, int]:
    weights: dict[str, int] = {}
    for match in re.finditer(r'(?m)^\s*defaultSpawnWeightList\s*=\s*"([^"]*)"', text):
        for entry in match.group(1).split(";"):
            if not entry.strip() or "," not in entry:
                continue
            entity_id, raw_weight = entry.split(",", 1)
            try:
                weights[entity_id.strip()] = int(raw_weight.strip())
            except ValueError:
                continue
    return weights


def find_nested_dict(data: object, key: str) -> dict | None:
    if isinstance(data, dict):
        value = data.get(key)
        if isinstance(value, dict):
            return value
        for nested in data.values():
            found = find_nested_dict(nested, key)
            if found is not None:
                return found
    elif isinstance(data, list):
        for nested in data:
            found = find_nested_dict(nested, key)
            if found is not None:
                return found
    return None


def string_values(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if isinstance(item, str)]
    return []


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    print("Ascendant Realms planning check")
    print(f"Repo: {ROOT}")
    print()

    atlas_worldgen_override_policy: dict = {}
    atlas_worldgen_override_enabled = True
    atlas_worldgen_override_policy_path = ROOT / "config/ascendant_atlas/worldgen_override_policy.json"
    if atlas_worldgen_override_policy_path.exists():
        try:
            loaded_policy = read_json(atlas_worldgen_override_policy_path)
            if isinstance(loaded_policy, dict):
                atlas_worldgen_override_policy = loaded_policy
                atlas_worldgen_override_enabled = atlas_worldgen_override_policy.get("worldgen_override_enabled") is not False
            else:
                errors.append("config/ascendant_atlas/worldgen_override_policy.json must be a JSON object.")
        except Exception as exc:
            errors.append(f"config/ascendant_atlas/worldgen_override_policy.json is invalid JSON: {exc}")

    for name in REQUIRED_FILES:
        if not (ROOT / name).exists():
            errors.append(f"Missing required file: {name}")

    pack_text = read_text(ROOT / "pack.toml") if (ROOT / "pack.toml").exists() else ""
    index_text = read_text(ROOT / "index.toml") if (ROOT / "index.toml").exists() else ""
    if pack_text:
        if 'name = "Ascendant Realms"' not in pack_text:
            errors.append("pack.toml does not name the pack Ascendant Realms.")
        if 'version = "0.1.0-alpha"' not in pack_text:
            errors.append("pack.toml does not use version 0.1.0-alpha.")
        if 'minecraft = "1.20.1"' not in pack_text:
            errors.append("pack.toml does not target Minecraft 1.20.1.")
        if 'forge =' not in pack_text:
            errors.append("pack.toml does not target Forge.")

    if index_text and re.search(r'(?m)^file\s*=\s*"dist/', index_text):
        errors.append("index.toml contains dist/ export artifacts. Clean dist/ and run packwiz refresh.")

    forge_version = pack_forge_version(pack_text)
    if forge_version and forge_version < (47, 4, 20):
        warnings.append("Forge is below the current Ascendant Realms Batch A target 47.4.20.")

    options_path = ROOT / "options.txt"
    if options_path.exists():
        if has_utf8_bom(options_path):
            errors.append("options.txt has a UTF-8 BOM; write it as UTF-8 without BOM so Minecraft can reliably parse it.")
        options_text = read_text(options_path)
        if not re.search(r"(?m)^version:3465$", options_text):
            errors.append("options.txt must include version:3465 to prevent Minecraft from running old keybind migration on modern key names.")
        match = re.search(r"(?m)^resourcePacks:(\[.*\])$", options_text)
        if not match:
            errors.append("options.txt is missing a resourcePacks list.")
        else:
            try:
                resource_packs = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                errors.append(f"options.txt resourcePacks is not valid JSON-style syntax: {exc}")
                resource_packs = []

            cubic_pack = "file/cubic-sun-moon-v1.8.5.zip"
            vanilla_plus_pack = "file/Vanilla Experience Plus.zip"
            mca_medieval_pack = "file/MCAR_VanillaMedieval_Universal_1.20.x_Only_Clothes_byDE4THR4SH_v4.zip"
            medieval_music_pack = "file/MedievalMusic.zip"
            visual_titles_pack = "file/Visual Titles 1.3.zip"
            visual_titles_biomes_pack = "file/Visual Travelers Titles Biomes Addon.zip"
            ascendant_titles_pack = "file/ascendant-realms-travelers-titles"
            if cubic_pack not in resource_packs:
                errors.append("options.txt does not enable Cubic Sun & Moon.")
            if vanilla_plus_pack not in resource_packs:
                errors.append("options.txt does not enable Vanilla Experience+.")
            for title_pack in [visual_titles_pack, visual_titles_biomes_pack, ascendant_titles_pack]:
                if title_pack not in resource_packs:
                    errors.append(f"options.txt does not enable Traveler's Titles visual pack: {title_pack}")
            if medieval_music_pack not in resource_packs:
                errors.append("options.txt does not enable Medieval Music.")
            if (ROOT / "mods/minecraft-comes-alive-reborn.pw.toml").exists() and mca_medieval_pack not in resource_packs:
                errors.append("options.txt does not enable MCA - Default Medieval while MCA Reborn is active.")
            if cubic_pack in resource_packs and vanilla_plus_pack in resource_packs:
                if resource_packs.index(cubic_pack) <= resource_packs.index(vanilla_plus_pack):
                    errors.append(
                        "Cubic Sun & Moon must appear after Vanilla Experience+ in options.txt so its sky textures win."
                    )
            if vanilla_plus_pack in resource_packs:
                for title_pack in [visual_titles_pack, visual_titles_biomes_pack, ascendant_titles_pack]:
                    if title_pack in resource_packs and resource_packs.index(title_pack) <= resource_packs.index(vanilla_plus_pack):
                        errors.append(
                            "Traveler's Titles visual packs must appear after Vanilla Experience+ in options.txt "
                            f"so styled title fonts win: {title_pack}"
                        )

            overrides_path = ROOT / "config/resourcepackoverrides.json"
            if not overrides_path.exists():
                errors.append("config/resourcepackoverrides.json is missing; Resource Pack Overrides cannot force the pack order.")
            else:
                try:
                    overrides = read_json(overrides_path)
                    if overrides.get("schema_version") != 2:
                        errors.append("config/resourcepackoverrides.json must use schema_version 2.")
                    if int(overrides.get("failed_reloads_per_session", 99)) > 2:
                        errors.append("Resource Pack Overrides failed_reloads_per_session should stay at 2 or lower to avoid slow failed-reload loops.")
                    if overrides.get("default_packs") != resource_packs:
                        errors.append("Resource Pack Overrides default_packs must match options.txt resourcePacks exactly.")
                    pack_overrides = overrides.get("pack_overrides", {})
                    for pack in [
                        cubic_pack,
                        vanilla_plus_pack,
                        mca_medieval_pack,
                        medieval_music_pack,
                        visual_titles_pack,
                        visual_titles_biomes_pack,
                        ascendant_titles_pack,
                        "file/ascendant-realms-compat-fixes",
                    ]:
                        override = pack_overrides.get(pack)
                        if not isinstance(override, dict) or not override.get("required") or not override.get("force_compatible"):
                            errors.append(f"Resource Pack Overrides must require and force-compatible: {pack}")
                except Exception as exc:
                    errors.append(f"config/resourcepackoverrides.json is invalid: {exc}")

    resource_pack_overrides_meta = ROOT / "mods/resource-pack-overrides.pw.toml"
    if not resource_pack_overrides_meta.exists():
        errors.append("Resource Pack Overrides must stay installed so required resource packs survive restarts/reimports.")
    elif 'side = "client"' not in read_text(resource_pack_overrides_meta):
        errors.append("Resource Pack Overrides must stay client-only.")

    vanilla_exp_meta = ROOT / "resourcepacks/vanilla-exp.pw.toml"
    if vanilla_exp_meta.exists():
        vanilla_exp_text = read_text(vanilla_exp_meta)
        if 'filename = "Vanilla Experience Plus.zip"' not in vanilla_exp_text:
            errors.append("Vanilla Experience+ resource-pack filename must stay ASCII: Vanilla Experience Plus.zip.")
        if "§" in vanilla_exp_text or "Â§" in vanilla_exp_text:
            errors.append("Vanilla Experience+ Packwiz metadata must not use section-sign color codes in filename.")

    jar_files = [p for p in ROOT.rglob("*.jar") if ".git" not in p.parts and "dist" not in p.parts]
    for path in jar_files:
        relative_jar = rel(path)
        if relative_jar not in ALLOWED_LOCAL_JARS:
            errors.append(f"Jar file present in repo; do not commit downloaded mod jars: {relative_jar}")

    mods_dir = ROOT / "mods"
    metadata_files = []
    for folder in ["mods", "resourcepacks", "shaderpacks"]:
        base = ROOT / folder
        if base.exists():
            metadata_files.extend(base.glob("*.pw.toml"))

    print(f"Packwiz metadata files: {len(metadata_files)}")
    active_relatives = {rel(path) for path in metadata_files}
    active_text_by_relative = {rel(path): read_text(path) for path in metadata_files}

    validate_ascendant_keybind_policy(errors, warnings)

    if any(relative in active_relatives for relative in {"mods/pick-up-notifier.pw.toml", "mods/pickup-notifier.pw.toml"}):
        errors.append("Pick Up Notifier metadata is active even though Loot Journal was selected for Batch E2.")

    if "resourcepacks/biome-edition-visual-travelers-titles.pw.toml" in active_relatives:
        errors.append("Biome Edition Visual Traveler's Titles is active, but verified files target Minecraft 1.21.1.")

    missing_batch_b = sorted(BATCH_B_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_b:
        errors.append(f"Batch B metadata is missing: {relative}")

    missing_batch_c = sorted(BATCH_C_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_c:
        errors.append(f"Batch C metadata is missing: {relative}")

    missing_batch_d = sorted(BATCH_D_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_d:
        errors.append(f"Batch D metadata is missing: {relative}")

    if "mods/default-skill-trees.pw.toml" in active_relatives:
        errors.append("Default Skill Trees is active, but Ascendant Realms now uses the custom skill-tree datapack instead.")

    for relative in sorted(CUSTOM_SKILL_TREE_REQUIRED_FILES):
        if not (ROOT / relative).exists():
            errors.append(f"Custom skill-tree file is missing: {relative}")

    skill_roots = {
        "config auto-load": ROOT / "config/puffish_skills",
        "datapack source": ROOT / "datapacks/ascendant_realms_skills/data/ascendant_realms/puffish_skills",
        "Open Loader legacy/source datapack": ROOT
        / "openloader/data/ascendant_realms_skills/data/ascendant_realms/puffish_skills",
    }
    for skill_root_label, skill_root in skill_roots.items():
        if not skill_root.exists():
            errors.append(f"Custom skill-tree {skill_root_label} root is missing: {rel(skill_root)}")
            continue
        try:
            skill_config = read_json(skill_root / "config.json")
            categories = set(skill_config.get("categories", []))
            missing_categories = sorted(CUSTOM_SKILL_TREE_CATEGORIES - categories)
            if missing_categories:
                errors.append(
                    f"Custom skill-tree {skill_root_label} config is missing categories: {', '.join(missing_categories)}"
                )
        except Exception as exc:
            errors.append(f"Custom skill-tree {skill_root_label} config JSON is invalid: {exc}")

        for category in sorted(CUSTOM_SKILL_TREE_CATEGORIES):
            category_root = skill_root / "categories" / category
            for filename in ["category.json", "definitions.json", "skills.json", "connections.json", "experience.json"]:
                path = category_root / filename
                if not path.exists():
                    errors.append(f"Custom skill-tree {skill_root_label} category file is missing: {rel(path)}")
                    continue
                try:
                    data = read_json(path)
                except Exception as exc:
                    errors.append(f"Custom skill-tree {skill_root_label} JSON is invalid in {rel(path)}: {exc}")
                    continue
                if filename == "definitions.json":
                    for definition_id, definition in data.items():
                        description_text = json.dumps(definition.get("description", ""), ensure_ascii=False)
                        extra_description_text = json.dumps(
                            definition.get("extra_description", ""), ensure_ascii=False
                        )
                        if "Effect:" not in description_text:
                            errors.append(
                                "Custom skill-tree "
                                f"{skill_root_label} definition {category}/{definition_id} is missing an Effect line."
                            )
                        if "Cost:" not in extra_description_text:
                            errors.append(
                                "Custom skill-tree "
                                f"{skill_root_label} definition {category}/{definition_id} is missing cost metadata."
                            )
                        if isinstance(definition.get("extra_description"), dict):
                            if definition["extra_description"].get("extra") == []:
                                errors.append(
                                    "Custom skill-tree "
                                    f"{skill_root_label} definition {category}/{definition_id} has an empty "
                                    "extra_description.extra array; Puffish Skills rejects this."
                                )
                    if category == "ascendant" and len(data) < CUSTOM_SKILL_TREE_MIN_DEFINITIONS:
                        errors.append(
                            "Custom skill-tree "
                            f"{skill_root_label} Ascendant Web has only {len(data)} definitions; "
                            f"expected at least {CUSTOM_SKILL_TREE_MIN_DEFINITIONS}."
                        )
                if filename == "category.json":
                    if category == "ascendant" and data.get("title") != "Ascendant Web":
                        errors.append(
                            f"Custom skill-tree {skill_root_label} category {category} must be titled Ascendant Web."
                        )
                if filename == "skills.json":
                    if category == "ascendant" and len(data) < CUSTOM_SKILL_TREE_MIN_DEFINITIONS:
                        errors.append(
                            "Custom skill-tree "
                            f"{skill_root_label} Ascendant Web has only {len(data)} skill positions; "
                            f"expected at least {CUSTOM_SKILL_TREE_MIN_DEFINITIONS}."
                        )
                if filename == "connections.json":
                    connections = data.get("normal", {}).get("bidirectional", [])
                    if category == "ascendant" and len(connections) > CUSTOM_SKILL_TREE_MAX_CONNECTIONS:
                        errors.append(
                            "Custom skill-tree "
                            f"{skill_root_label} Ascendant Web has {len(connections)} connections; "
                            f"expected at most {CUSTOM_SKILL_TREE_MAX_CONNECTIONS} after the readability pass."
                        )

    identity_load = ROOT / "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/load.mcfunction"
    identity_tick = ROOT / "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/tick.mcfunction"
    identity_level_up = (
        ROOT / "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/level_up.mcfunction"
    )
    identity_kit = ROOT / "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/npc_test/kit.mcfunction"
    identity_fix_rank_examiner = (
        ROOT / "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/npc_test/fix_rank_examiner.mcfunction"
    )
    identity_rank_examiner_evaluate = (
        ROOT / "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank_examiner/evaluate.mcfunction"
    )
    identity_rank_examiner_sync = (
        ROOT / "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank_examiner/sync_nameplate.mcfunction"
    )
    identity_rank_examiner_debug = (
        ROOT / "config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank_examiner/debug_scores.mcfunction"
    )
    identity_kit_mirror = ROOT / "openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/npc_test/kit.mcfunction"
    identity_rank_examiner_evaluate_mirror = (
        ROOT / "openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank_examiner/evaluate.mcfunction"
    )
    identity_rank_examiner_sync_mirror = (
        ROOT / "openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank_examiner/sync_nameplate.mcfunction"
    )
    identity_rank_examiner_debug_mirror = (
        ROOT / "openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank_examiner/debug_scores.mcfunction"
    )
    rank_nameplate_policy = ROOT / "config/ascendant_guild/rank_nameplate_policy.json"
    rank_examiner_policy = ROOT / "config/ascendant_guild/rank_examiner_policy.json"
    npc_relationship_policy = ROOT / "config/ascendant_guild/npc_relationship_policy.json"
    customnpcs_config = ROOT / "config/CustomNpcs.cfg"
    customnpcs_identity_script = ROOT / "customnpcs/scripts/ecmascript/ascendant_npc_identity.js"
    if identity_load.exists():
        identity_load_text = read_text(identity_load)
        for expected in [
            "scoreboard objectives add ar_skill_level dummy",
            "scoreboard objectives add ar_skill_xp dummy",
            "scoreboard objectives add ar_skill_xp_req dummy",
            "scoreboard objectives add ar_skill_sp dummy",
            "scoreboard objectives setdisplay belowName ar_skill_level",
            "team modify ar_ascendant prefix",
        ]:
            if expected not in identity_load_text:
                errors.append(f"Ascendant identity load function is missing: {expected}")
        if "scoreboard objectives setdisplay belowName ar_level" in identity_load_text:
            errors.append(
                "Ascendant identity load function must display ar_skill_level below names, "
                "not the vanilla XP ar_level fallback."
            )
        if "below_name" in identity_load_text:
            errors.append(
                "Ascendant identity load function uses below_name, but Minecraft 1.20.1 rejects that display slot. "
                "Use belowName so the rank/level fallback loads."
            )
    if identity_tick.exists():
        identity_tick_text = read_text(identity_tick)
        for expected in [
            "team join ar_ascendant @a[team=]",
            "KubeJS mirrors Puffish Skills Ascendant Web level data into ar_skill_level",
        ]:
            if expected not in identity_tick_text:
                errors.append(f"Ascendant identity tick function is missing: {expected}")
        for old_fallback in [
            "if score @s ar_level > @s ar_level_last",
            "scoreboard players operation @s ar_level_last = @s ar_level",
        ]:
            if old_fallback in identity_tick_text:
                errors.append(
                    "Ascendant identity tick function must not drive level-up popups from vanilla XP anymore: "
                    f"{old_fallback}"
                )
    if identity_level_up.exists():
        identity_level_up_text = read_text(identity_level_up)
        if "Level Up!" not in identity_level_up_text:
            errors.append("Ascendant identity level-up function must show a Level Up! title.")
        if "ar_skill_level" not in identity_level_up_text:
            errors.append("Ascendant identity level-up function must read ar_skill_level.")
    if not identity_kit.exists():
        errors.append("Ascendant identity NPC test kit function is missing.")
    else:
        identity_kit_text = read_text(identity_kit)
        if "irons_spellbooks:truthseeker" in identity_kit_text:
            errors.append(
                "Ascendant identity NPC test kit must not give irons_spellbooks:truthseeker. "
                "The live 1.20.1 client rejects that id in command parsing, which makes the whole "
                "ascendant_identity:npc_test/kit function disappear."
            )
        for expected in [
            "customnpcs:npcwand",
            "customnpcs:npcmobcloner",
            "minecraft:name_tag",
            "mira_ash",
            "minecraft:iron_sword",
        ]:
            if expected not in identity_kit_text:
                errors.append(f"Ascendant identity NPC test kit is missing command-safe item: {expected}")
        nameplates_for_kit = ROOT / "config/ascendant_guild/nameplates.json"
        if nameplates_for_kit.exists():
            try:
                kit_nameplates = read_json(nameplates_for_kit)
                for profile_id in sorted((kit_nameplates.get("profiles") or {}).keys()):
                    expected_profile_key = f"ar:{profile_id}"
                    if expected_profile_key not in identity_kit_text:
                        errors.append(
                            f"Ascendant identity NPC test kit is missing profile name tag: {expected_profile_key}"
                        )
            except Exception as exc:
                errors.append(f"Could not validate NPC test kit profile tags against nameplates.json: {exc}")
    if not identity_kit_mirror.exists():
        errors.append(
            "Ascendant identity NPC test kit mirror is missing under openloader/data. "
            "Keep the config/openloader and root openloader copies aligned."
        )
    elif identity_kit.exists() and read_text(identity_kit_mirror) != read_text(identity_kit):
        errors.append(
            "Ascendant identity NPC test kit mirror differs from config/openloader copy. "
            "Keep both copies aligned so client and export staging behave the same."
        )
    if not identity_fix_rank_examiner.exists():
        errors.append("Ascendant Rank Examiner repair function is missing.")
    else:
        identity_fix_text = read_text(identity_fix_rank_examiner)
        for expected in [
            "customnpcs:customnpc",
            "data merge entity",
            "Rank Examiner",
            "B-Rank",
            "ar_rank:\"B-Rank\"",
        ]:
            if expected not in identity_fix_text:
                errors.append(f"Ascendant Rank Examiner repair function is missing: {expected}")
    for label, path, mirror_path in [
        ("evaluate", identity_rank_examiner_evaluate, identity_rank_examiner_evaluate_mirror),
        ("sync_nameplate", identity_rank_examiner_sync, identity_rank_examiner_sync_mirror),
        ("debug_scores", identity_rank_examiner_debug, identity_rank_examiner_debug_mirror),
    ]:
        if not path.exists():
            errors.append(f"Ascendant Rank Examiner {label} function is missing.")
            continue
        if not mirror_path.exists():
            errors.append(f"Ascendant Rank Examiner {label} mirror is missing under openloader/data.")
        elif read_text(mirror_path) != read_text(path):
            errors.append(
                f"Ascendant Rank Examiner {label} mirror differs from config/openloader copy. "
                "Keep both copies aligned."
            )
    if identity_rank_examiner_evaluate.exists():
        rank_examiner_text = read_text(identity_rank_examiner_evaluate)
        for expected in [
            "function ascendant_identity:rank_examiner/debug_scores",
            "function ascendant_identity:rank_examiner/sync_nameplate",
            "function ascendant_identity:rank/e_rank",
            "function ascendant_identity:rank/d_rank",
            "function ascendant_identity:rank/c_rank",
            "function ascendant_identity:rank/b_rank",
            "function ascendant_identity:rank/a_rank",
            "function ascendant_identity:rank/s_rank",
            "ar_guild_rep matches 10..",
            "ar_hunt_kills matches 10..",
            "ar_bosses_done matches 8..",
            "ar_dragons_done matches 2..",
        ]:
            if expected not in rank_examiner_text:
                errors.append(f"Ascendant Rank Examiner evaluate function is missing: {expected}")
    if identity_rank_examiner_sync.exists():
        sync_text = read_text(identity_rank_examiner_sync)
        for expected in [
            "team join ar_rank_unranked",
            "team join ar_rank_e",
            "team join ar_rank_d",
            "team join ar_rank_c",
            "team join ar_rank_b",
            "team join ar_rank_a",
            "team join ar_rank_s",
        ]:
            if expected not in sync_text:
                errors.append(f"Ascendant Rank Examiner sync function is missing: {expected}")
    if not rank_nameplate_policy.exists():
        errors.append("config/ascendant_guild/rank_nameplate_policy.json is missing.")
    else:
        try:
            nameplate_policy = read_json(rank_nameplate_policy)
            if nameplate_policy.get("status") not in {"live_forge_safe_fallback", "live_internal_forge_renderer"}:
                errors.append("rank_nameplate_policy.json must mark the active status as live_internal_forge_renderer or live_forge_safe_fallback.")
            requested_reference_mod = nameplate_policy.get("requested_reference_mod", {})
            if requested_reference_mod.get("decision") not in {
                "do_not_install",
                "do_not_install_fabric_jar_recreated_inside_helper",
                "do_not_install_fabric_jar_recreated_inside_ascendant_nametags",
            }:
                errors.append("rank_nameplate_policy.json must reject direct CustomNameTags install for this Forge pack.")
            active_renderer = nameplate_policy.get("active_renderer", {})
            player_renderer = str(active_renderer.get("players", ""))
            if "ascendant_nametags" not in player_renderer and player_renderer != "minecraft_scoreboard_teams":
                errors.append("rank_nameplate_policy.json must keep players on Ascendant Nametags or minecraft_scoreboard_teams fallback.")
            ai_hunter_renderer = str(active_renderer.get("ai_hunters", ""))
            if nameplate_policy.get("status") == "live_internal_forge_renderer" and "ascendant_nametags" not in ai_hunter_renderer:
                errors.append("rank_nameplate_policy.json must document Ascendant Nametags for AI hunter nameplates.")
            npc_renderer = str(active_renderer.get("authored_npcs", ""))
            if "customnpcs_scripted_display_name" not in npc_renderer:
                errors.append("rank_nameplate_policy.json must keep authored NPCs on customnpcs_scripted_display_name.")
            for rank_id in ["unranked", "e_rank", "d_rank", "c_rank", "b_rank", "a_rank", "s_rank"]:
                if rank_id not in nameplate_policy.get("palette", {}):
                    errors.append(f"rank_nameplate_policy.json palette is missing {rank_id}.")
        except Exception as exc:
            errors.append(f"rank_nameplate_policy.json is invalid: {exc}")
    if not rank_examiner_policy.exists():
        errors.append("config/ascendant_guild/rank_examiner_policy.json is missing.")
    else:
        try:
            examiner_policy = read_json(rank_examiner_policy)
            if examiner_policy.get("evaluation_function") != "ascendant_identity:rank_examiner/evaluate":
                errors.append("rank_examiner_policy.json must reference ascendant_identity:rank_examiner/evaluate.")
            trial_ranks = {str(entry.get("rank", "")) for entry in examiner_policy.get("rank_trials", []) if isinstance(entry, dict)}
            for rank_id in ["e_rank", "d_rank", "c_rank", "b_rank", "a_rank", "s_rank"]:
                if rank_id not in trial_ranks:
                    errors.append(f"rank_examiner_policy.json rank_trials is missing {rank_id}.")
        except Exception as exc:
            errors.append(f"rank_examiner_policy.json is invalid: {exc}")
    if not npc_relationship_policy.exists():
        errors.append("config/ascendant_guild/npc_relationship_policy.json is missing.")
    else:
        try:
            relationship_policy = read_json(npc_relationship_policy)
            if relationship_policy.get("status") != "live_script_policy_v1":
                errors.append("npc_relationship_policy.json must mark status live_script_policy_v1.")
            tiers = relationship_policy.get("relationship_tiers", {})
            for tier in ["stranger", "familiar", "trusted"]:
                if tier not in tiers:
                    errors.append(f"npc_relationship_policy.json is missing relationship tier {tier}.")
            profile_policies = relationship_policy.get("profile_policies", {})
            for profile_id in [
                "guild_clerk",
                "bounty_master",
                "rank_examiner",
                "guild_arcanist",
                "hunter_quartermaster",
                "guard_captain",
                "tavern_keeper",
                "village_elder",
                "wounded_hunter",
                "mira_ash",
                "darius_crowe",
                "seren_valehart",
                "kael_vorn",
                "black_hound",
            ]:
                policy = profile_policies.get(profile_id)
                if not isinstance(policy, dict):
                    errors.append(f"npc_relationship_policy.json profile_policies is missing {profile_id}.")
                    continue
                for expected_key in ["relationship_gate", "command_policy", "service_min_relation", "can_follow", "can_take_orders"]:
                    if expected_key not in policy:
                        errors.append(f"npc_relationship_policy.json profile {profile_id} is missing {expected_key}.")
                if policy.get("can_follow") is not False:
                    errors.append(f"npc_relationship_policy.json profile {profile_id} must not allow instant follow behavior.")
                if policy.get("can_take_orders") is not False:
                    errors.append(f"npc_relationship_policy.json profile {profile_id} must not allow instant player orders.")
            examiner = profile_policies.get("rank_examiner", {})
            if examiner.get("command_policy") != "rank_evaluation_only":
                errors.append("Rank Examiner relationship policy must be rank_evaluation_only.")
        except Exception as exc:
            errors.append(f"npc_relationship_policy.json is invalid: {exc}")
    if not customnpcs_config.exists():
        errors.append("config/CustomNpcs.cfg is missing; source must own CustomNPCs command safety.")
    else:
        customnpcs_config_text = read_text(customnpcs_config)
        for expected in [
            "EnableScripting=true",
            "NpcUseOpCommands=false",
            "NoppesCommandOpOnly=true",
            "OpsOnly=true",
            "DefaultInteractLine=",
            "SoulStoneNPCs=false",
        ]:
            if expected not in customnpcs_config_text:
                errors.append(f"config/CustomNpcs.cfg is missing safety setting: {expected}")
        if re.search(r"^DefaultInteractLine=.+", customnpcs_config_text, re.MULTILINE):
            errors.append("config/CustomNpcs.cfg DefaultInteractLine must stay empty so scripted NPCs own dialogue.")
    custom_name_tags_hits = []
    mods_dir = ROOT / "mods"
    if mods_dir.exists():
        custom_name_tags_hits = [
            str(path.relative_to(ROOT))
            for path in mods_dir.iterdir()
            if "customnametag" in path.name.lower() or "custom_name_tag" in path.name.lower()
        ]
    if custom_name_tags_hits:
        errors.append(
            "CustomNameTags appears to be installed in mods/, but the requested visible mod is Fabric/server-side "
            f"and must not be installed directly in this Forge pack: {custom_name_tags_hits}"
        )
    if not customnpcs_identity_script.exists():
        errors.append("Ascendant CustomNPCs dynamic identity script is missing.")
    else:
        script_text = read_text(customnpcs_identity_script)
        for expected in [
            "function init(event)",
            "function tick(event)",
            "arApplyIdentity",
            "mira_ash",
            "Guild Clerk",
            "Rank Examiner",
            "B-Rank",
            "setName",
            "setTitle",
            "setShowName",
            "updateClient",
            "arIsPublicRank",
            "arShouldUseProfileRank",
            "arNormalizeLevel",
            "arTryRankExaminerEvaluation",
            "arHandleInteraction",
            "arRecordInteraction",
            "arRelationTier",
            "I do not take orders from strangers",
            "not a follower",
            "Companion orders are still locked",
            "function ascendant_identity:rank_examiner/evaluate",
            "execute as ",
            "run function ascendant_identity:rank_examiner/evaluate",
            "event.npc.executeCommand",
            "event.API.executeCommand",
            "sayTo",
        ]:
            if expected not in script_text:
                errors.append(f"Ascendant CustomNPCs dynamic identity script is missing: {expected}")
        for forbidden in [
            "Use \\u00a7e/",
            "Use §e/",
            "player.executeCommand",
            "player.runCommand",
            "player.runCommandSilent",
        ]:
            if forbidden in script_text:
                errors.append(
                    "Ascendant Rank Examiner must be an NPC interaction, not a player-facing command fallback. "
                    f"Remove script text/method: {forbidden}"
                )
        if "guild_staff\" ||" in script_text or "rank === \"guild_staff\"" in script_text:
            errors.append(
                "Ascendant CustomNPCs dynamic identity script must not treat guild_staff as a public rank. "
                "guild_staff is a visual style id only."
            )
        if '"Guild", "Examiner"' in script_text or 'rank = "Guild"' in script_text:
            errors.append(
                "Ascendant CustomNPCs dynamic identity script must not render Rank Examiner as [Guild]; "
                "use the B-Rank profile from nameplates.json."
            )
        if re.search(r"function\s+tick\s*\([^)]*\)\s*\{[^}]*arApplyIdentity", script_text, re.DOTALL):
            errors.append(
                "Ascendant CustomNPCs dynamic identity script must not rewrite display data every tick. "
                "Init/interact refresh is enough and avoids repeated CustomNPCs script errors."
            )
        if "CustomNPCs only renders display titles inside close range" not in script_text:
            errors.append(
                "Ascendant CustomNPCs dynamic identity script must document the close-range title-slot fallback."
            )
    customnpcs_identity_test = ROOT / "scripts/test-customnpcs-identity.js"
    if customnpcs_identity_test.exists():
        identity_test_text = read_text(customnpcs_identity_test)
        for expected in [
            "fresh profile key",
            "stale guild style id",
            "stale unranked display",
            "stale unranked stored rank",
            "CustomNPCs identity script tests passed",
            "non-examiner NPCs must not execute commands",
            "I do not take orders from strangers",
            "not a follower",
        ]:
            if expected not in identity_test_text:
                errors.append(f"CustomNPCs identity test is missing case: {expected}")
    customnpcs_identity_audit = ROOT / "scripts/customnpcs-identity-audit.py"
    if customnpcs_identity_audit.exists():
        audit_text = read_text(customnpcs_identity_audit)
        for expected in [
            "embedded script is stale",
            "Minecraft is running",
            "CNPCStoredData",
            "customnpcs:customnpc",
            "Backups written under",
        ]:
            if expected not in audit_text:
                errors.append(f"CustomNPCs identity audit/repair script is missing: {expected}")

    guild_root = ROOT / "config/ascendant_guild"
    guild_count_expectations = {
        "ranks.json": ("ranks", 7),
        "rival_hunters.json": ("rivals", 5),
        "bounty_categories.json": ("categories", 6),
        "hunter_boards.json": ("boards", 3),
        "npc_roster.json": ("npcs", 10),
    }
    for filename, (key, minimum_count) in guild_count_expectations.items():
        path = guild_root / filename
        if not path.exists():
            continue
        try:
            data = read_json(path)
            values = data.get(key, [])
            if len(values) < minimum_count:
                errors.append(
                    f"Ascendant Guild {filename} has {len(values)} {key}; expected at least {minimum_count}."
                )
        except Exception as exc:
            errors.append(f"Ascendant Guild {filename} JSON is invalid: {exc}")

    generated_registry_expectations = [
        (ROOT / "config/ascendant_index/mob_registry.json", "mobs", 100),
        (ROOT / "config/ascendant_index/structure_registry.json", "structures", 100),
        (ROOT / "config/ascendant_guild/generated_bounty_targets.json", "bounty_targets", 50),
        (ROOT / "config/ascendant_index/spawn_tuning_worklist.json", "spawn_groups", 5),
        (ROOT / "config/ascendant_guild/bounty_pool_worklist.json", "pool_groups", 3),
    ]
    for path, key, minimum_count in generated_registry_expectations:
        if not path.exists():
            continue
        try:
            data = read_json(path)
            values = data.get(key, [])
            if len(values) < minimum_count:
                errors.append(
                    f"Generated Ascendant registry {path.name} has {len(values)} {key}; expected at least {minimum_count}."
                )
        except Exception as exc:
            errors.append(f"Generated Ascendant registry {path.name} JSON is invalid: {exc}")

    generated_npc_profiles = ROOT / "config/ascendant_guild/generated_npc_profiles.json"
    if generated_npc_profiles.exists():
        try:
            profile_data = read_json(generated_npc_profiles)
            profiles = profile_data.get("profiles", [])
            if len(profiles) < 10:
                errors.append("Generated NPC profile set must include at least 10 Guild/rival profiles.")
            for profile in profiles:
                for expected in [
                    "id",
                    "rank",
                    "level",
                    "role",
                    "generated_name",
                    "entity_type",
                    "skin_texture",
                    "equipment",
                    "relationship_gate",
                    "command_policy",
                    "service_min_relation",
                    "can_follow",
                    "can_take_orders",
                    "obedience_note",
                ]:
                    if expected not in profile:
                        errors.append(f"Generated NPC profile {profile.get('id', '<unknown>')} is missing {expected}.")
                if profile.get("entity_type") != "customnpcs:customnpc":
                    errors.append(f"Generated NPC profile {profile.get('id', '<unknown>')} must use customnpcs:customnpc.")
                profile_id = str(profile.get("id", ""))
                skin_texture = str(profile.get("skin_texture", ""))
                expected_skin = f"customnpcs:textures/entity/ascendant_mca/{profile_id}.png"
                if skin_texture != expected_skin:
                    errors.append(
                        f"Generated NPC profile {profile.get('id', '<unknown>')} should use bridged MCA-style "
                        f"skin {expected_skin}, got {skin_texture or '<missing>'}."
                    )
                equipment = profile.get("equipment", {})
                if not isinstance(equipment, dict) or not (set(equipment) & IMPORTANT_NPC_VISIBLE_SLOT_KEYS):
                    errors.append(f"Generated NPC profile {profile.get('id', '<unknown>')} has no visible generated gear.")
                if profile.get("manual_build_required") is not False:
                    errors.append(f"Generated NPC profile {profile.get('id', '<unknown>')} must not require hand building.")
                if profile.get("can_follow") is not False:
                    errors.append(f"Generated NPC profile {profile.get('id', '<unknown>')} must not allow instant follow behavior.")
                if profile.get("can_take_orders") is not False:
                    errors.append(f"Generated NPC profile {profile.get('id', '<unknown>')} must not allow instant player orders.")
        except Exception as exc:
            errors.append(f"Generated NPC profile JSON is invalid: {exc}")

    for skin_id in sorted(ASCENDANT_GUILD_REQUIRED_SKINS):
        skin_paths = [
            (
                ROOT
                / "resourcepacks/ascendant-realms-compat-fixes/assets/customnpcs/textures/entity/ascendant_mca"
                / f"{skin_id}.png"
            ),
            (
                ROOT
                / "customnpcs/assets/customnpcs/textures/entity/ascendant_mca"
                / f"{skin_id}.png"
            ),
        ]
        for skin_path in skin_paths:
            if not skin_path.exists():
                errors.append(f"Generated NPC bridged MCA-style skin is missing: {rel(skin_path)}")

    generated_npc_spawn_sets = ROOT / "config/ascendant_guild/generated_npc_spawn_sets.json"
    if generated_npc_spawn_sets.exists():
        try:
            spawn_data = read_json(generated_npc_spawn_sets)
            spawn_set_ids = {entry.get("id") for entry in spawn_data.get("spawn_sets", []) if isinstance(entry, dict)}
            for expected in ["starter_guild_staff", "roadside_rumor_camp", "frontier_guild_outpost"]:
                if expected not in spawn_set_ids:
                    errors.append(f"Generated NPC spawn sets are missing {expected}.")
        except Exception as exc:
            errors.append(f"Generated NPC spawn-set JSON is invalid: {exc}")

    guild_pack_roots = [
        ROOT / "config/openloader/data/ascendant_realms_guild",
        ROOT / "openloader/data/ascendant_realms_guild",
    ]
    for guild_pack_root in guild_pack_roots:
        if not guild_pack_root.exists():
            continue
        for structure_id in sorted(ASCENDANT_GUILD_STRUCTURE_IDS):
            structure_json = guild_pack_root / f"data/ascendant_guild/worldgen/structure/{structure_id}.json"
            structure_set_json = guild_pack_root / f"data/ascendant_guild/worldgen/structure_set/{structure_id}.json"
            template_pool_json = guild_pack_root / f"data/ascendant_guild/worldgen/template_pool/guild/{structure_id}.json"
            biome_tag_json = guild_pack_root / f"data/ascendant_guild/tags/worldgen/biome/has_structure/{structure_id}.json"
            structure_nbt = guild_pack_root / f"data/ascendant_guild/structures/guild/{structure_id}.nbt"
            try:
                structure_data = read_json(structure_json)
                if structure_data.get("type") != "minecraft:jigsaw":
                    errors.append(f"{rel(structure_json)} must be a minecraft:jigsaw structure.")
                if structure_data.get("start_pool") != f"ascendant_guild:guild/{structure_id}":
                    errors.append(f"{rel(structure_json)} has the wrong start_pool.")
                if structure_data.get("biomes") != f"#ascendant_guild:has_structure/{structure_id}":
                    errors.append(f"{rel(structure_json)} has the wrong biome tag.")
            except Exception as exc:
                errors.append(f"{rel(structure_json)} JSON is invalid: {exc}")
            try:
                set_data = read_json(structure_set_json)
                placement = set_data.get("placement", {})
                if placement.get("type") != "minecraft:random_spread":
                    errors.append(f"{rel(structure_set_json)} must use random_spread placement.")
                if int(placement.get("spacing", 0) or 0) <= int(placement.get("separation", 0) or 0):
                    errors.append(f"{rel(structure_set_json)} spacing must be greater than separation.")
                minimum_spacing = ASCENDANT_GUILD_MIN_SPACING.get(structure_id, 0)
                if int(placement.get("spacing", 0) or 0) < minimum_spacing:
                    errors.append(
                        f"{rel(structure_set_json)} spacing is {placement.get('spacing')}; "
                        f"expected at least {minimum_spacing} after density tuning."
                    )
            except Exception as exc:
                errors.append(f"{rel(structure_set_json)} JSON is invalid: {exc}")
            try:
                pool_data = read_json(template_pool_json)
                locations = [
                    element.get("element", {}).get("location")
                    for element in pool_data.get("elements", [])
                    if isinstance(element, dict)
                ]
                if f"ascendant_guild:guild/{structure_id}" not in locations:
                    errors.append(f"{rel(template_pool_json)} does not reference its matching structure NBT.")
            except Exception as exc:
                errors.append(f"{rel(template_pool_json)} JSON is invalid: {exc}")
            try:
                biome_data = read_json(biome_tag_json)
                if len(biome_data.get("values", [])) < 6:
                    errors.append(f"{rel(biome_tag_json)} should include at least 6 biome values.")
            except Exception as exc:
                errors.append(f"{rel(biome_tag_json)} JSON is invalid: {exc}")
            try:
                import nbtlib  # type: ignore

                structure_file = nbtlib.load(structure_nbt, gzipped=True)
                palette = structure_file.get("palette", [])
                blocks = structure_file.get("blocks", [])
                if len(palette) < 3 or len(blocks) < 20:
                    errors.append(f"{rel(structure_nbt)} is too small or has an empty palette.")
                palette_names = []
                for state in palette:
                    try:
                        palette_names.append(str(state.get("Name", "")))
                    except AttributeError:
                        continue
                if "minecraft:fence" in palette_names:
                    errors.append(f"{rel(structure_nbt)} contains invalid generic minecraft:fence block state.")
                notice_count = 0
                loot_container_count = 0
                required_wall_lantern = ASCENDANT_GUILD_REQUIRED_WALL_LANTERNS.get(structure_id)
                required_wall_lantern_count = 0
                for block in blocks:
                    try:
                        block_nbt = block.get("nbt", {})
                    except AttributeError:
                        block_nbt = {}
                    try:
                        state_index = int(block.get("state", -1))
                        block_state = palette[state_index] if 0 <= state_index < len(palette) else {}
                    except Exception:
                        block_state = {}
                    try:
                        block_state_name = str(block_state.get("Name", ""))
                    except AttributeError:
                        block_state_name = ""
                    try:
                        block_state_properties = block_state.get("Properties", {})
                    except AttributeError:
                        block_state_properties = {}
                    if required_wall_lantern and block_state_name == required_wall_lantern:
                        required_wall_lantern_count += 1
                    try:
                        block_entity_id = str(block_nbt.get("id", ""))
                    except AttributeError:
                        block_entity_id = ""
                    if block_entity_id == "supplementaries:notice_board":
                        notice_count += 1
                        if str(block_state_properties.get("facing", "")) == "south":
                            errors.append(f"{rel(structure_nbt)} has a notice board facing back into the wall.")
                        text_holder = block_nbt.get("TextHolder", {})
                        try:
                            messages = text_holder.get("message", [])
                        except AttributeError:
                            messages = []
                        items = block_nbt.get("Items", [])
                        if len(messages) < 2:
                            errors.append(f"{rel(structure_nbt)} has a notice board without enough written lines.")
                        if len(items) < 1:
                            errors.append(f"{rel(structure_nbt)} has a notice board without a displayed book/item.")
                    if block_entity_id in {"minecraft:barrel", "minecraft:chest"}:
                        if str(block_nbt.get("LootTable", "")).startswith("ascendant_guild:chests/"):
                            loot_container_count += 1
                if notice_count < ASCENDANT_GUILD_MIN_NOTICE_BOARDS.get(structure_id, 0):
                    errors.append(
                        f"{rel(structure_nbt)} has {notice_count} notice boards; "
                        f"expected at least {ASCENDANT_GUILD_MIN_NOTICE_BOARDS.get(structure_id, 0)}."
                    )
                if loot_container_count < ASCENDANT_GUILD_MIN_LOOT_CONTAINERS.get(structure_id, 0):
                    errors.append(
                        f"{rel(structure_nbt)} has {loot_container_count} loot containers; "
                        f"expected at least {ASCENDANT_GUILD_MIN_LOOT_CONTAINERS.get(structure_id, 0)}."
                    )
                if required_wall_lantern and required_wall_lantern_count < 1:
                    errors.append(
                        f"{rel(structure_nbt)} should use {required_wall_lantern} for wall-adjacent lantern spots."
                    )
            except Exception as exc:
                errors.append(f"{rel(structure_nbt)} NBT is invalid or unreadable: {exc}")

        for spawn_set in ["starter_guild_staff", "roadside_rumor_camp", "frontier_guild_outpost"]:
            function_path = guild_pack_root / f"data/ascendant_guild/functions/npc/spawn_set/{spawn_set}.mcfunction"
            if function_path.exists():
                text = read_text(function_path)
                if "~+" in text:
                    errors.append(f"{rel(function_path)} contains invalid relative coordinate syntax '~+'.")
                if "customnpcs:customnpc" in text:
                    errors.append(f"{rel(function_path)} should call profile spawn functions instead of duplicating summon NBT.")

        profile_function_root = guild_pack_root / "data/ascendant_guild/functions/npc"
        for profile_function in sorted(profile_function_root.glob("spawn_*.mcfunction")):
            text = read_text(profile_function)
            if "summon customnpcs:customnpc" not in text:
                continue
            for required_token in [
                "Texture:",
                "ScriptEnabled:1b",
                "Scripts:[",
                "ascendant_npc_identity.js",
                "arTryRankExaminerEvaluation",
                "NpcInv:[]",
                "Weapons:[",
                "Armor:[",
                "HandItems:",
                "ArmorItems:",
                "HandDropChances:",
                "ArmorDropChances:",
                "MovingState:",
                "WalkingRange:",
                "ActiveRange:",
                "ar_relationship_gate:",
                "ar_command_policy:",
                "ar_service_min_relation:",
                "ar_can_follow:\"false\"",
                "ar_can_take_orders:\"false\"",
            ]:
                if required_token not in text:
                    errors.append(f"{rel(profile_function)} is missing generated NPC visual/equipment token {required_token}.")
            if 'Texture:"customnpcs:textures/entity/ascendant_mca/' not in text:
                errors.append(f"{rel(profile_function)} should use bridged MCA-style CustomNPC textures.")
            if "NpcInv:{" in text:
                errors.append(f"{rel(profile_function)} nests visible gear in NpcInv; CustomNPCs renders from top-level Weapons/Armor.")
            if "ScriptEnabled:0b" in text:
                errors.append(f"{rel(profile_function)} spawns a visual-only CustomNPC without enabling the Ascendant identity script.")
            if re.search(r'(?<!\\)\\[nrtu]', text):
                errors.append(f"{rel(profile_function)} contains a single-backslash script escape that Minecraft function parsing can reject.")
            if re.search(r"Weapons:\[[^\]]*Slot:1", text):
                errors.append(f"{rel(profile_function)} uses CustomNPCs weapon Slot 1; offhand visuals must use Slot 2.")
            if re.search(r"Texture:\"customnpcs:textures/entity/human(?:male|female)/", text):
                errors.append(f"{rel(profile_function)} is still using a bundled CustomNPCs human texture instead of the MCA-style bridge.")

        for board_id, (pool_name, minimum_count) in ASCENDANT_GUILD_BOUNTY_BOARDS.items():
            decree_path = guild_pack_root / f"data/bountiful/bounty_decrees/ascendant_guild/{board_id}.json"
            pool_path = guild_pack_root / f"data/bountiful/bounty_pools/ascendant_guild/{pool_name}.json"
            try:
                decree_data = read_json(decree_path)
                if pool_name not in decree_data.get("objectives", []):
                    errors.append(f"{rel(decree_path)} does not reference {pool_name}.")
            except Exception as exc:
                errors.append(f"{rel(decree_path)} JSON is invalid: {exc}")
            try:
                pool_data = read_json(pool_path)
                content = pool_data.get("content", {})
                if len(content) < minimum_count:
                    errors.append(f"{rel(pool_path)} has {len(content)} targets; expected at least {minimum_count}.")
                for key, entry in content.items():
                    target = str(entry.get("content", "")).lower()
                    if any(token in target for token in ASCENDANT_GUILD_BAD_BOUNTY_TOKENS):
                        errors.append(f"{rel(pool_path)} has unsuitable bounty target {key}: {target}")
            except Exception as exc:
                errors.append(f"{rel(pool_path)} JSON is invalid: {exc}")

    live_bountiful_pools = ROOT / "config/ascendant_guild/live_bountiful_pools.json"
    if live_bountiful_pools.exists():
        try:
            live_data = read_json(live_bountiful_pools)
            selected_counts = live_data.get("selected_counts", {})
            for board_id, (_, minimum_count) in ASCENDANT_GUILD_BOUNTY_BOARDS.items():
                if int(selected_counts.get(board_id, 0) or 0) < minimum_count:
                    errors.append(f"Live Bountiful pool summary for {board_id} has too few selected targets.")
        except Exception as exc:
            errors.append(f"Live Bountiful pool summary JSON is invalid: {exc}")

    skill_hook_registry = ROOT / "config/ascendant_index/skill_hook_registry.json"
    if skill_hook_registry.exists():
        try:
            data = read_json(skill_hook_registry)
            branches = data.get("branches", {})
            for branch in ["warrior", "rogue", "ranger", "arcanist", "engineer", "survivalist", "dragonbound"]:
                if branch not in branches:
                    errors.append(f"Skill hook registry is missing branch: {branch}")
        except Exception as exc:
            errors.append(f"Skill hook registry JSON is invalid: {exc}")

    integration_matrix = ROOT / "config/ascendant_index/integration_matrix.json"
    if integration_matrix.exists():
        try:
            data = read_json(integration_matrix)
            candidates = data.get("custom_mod_candidates", [])
            for expected in ["ascendant_core", "ascendant_nameplates", "ascendant_progression_hud"]:
                if not any(candidate.get("id") == expected for candidate in candidates if isinstance(candidate, dict)):
                    errors.append(f"Integration matrix is missing custom mod candidate: {expected}")
        except Exception as exc:
            errors.append(f"Integration matrix JSON is invalid: {exc}")

    ascendant_core_root = ROOT / "config/ascendant_core"
    ascendant_core_manifest = ascendant_core_root / "core_manifest.json"
    if ascendant_core_manifest.exists():
        try:
            manifest = read_json(ascendant_core_manifest)
            if not manifest.get("enabled", False):
                errors.append("config/ascendant_core/core_manifest.json must keep enabled=true.")

            sources = manifest.get("source_registries", {})
            if not isinstance(sources, dict) or len(sources) < 10:
                errors.append("Ascendant Core manifest must list the source registries it unifies.")
                sources = {}
            for key, relative_path in sources.items():
                source_path = ROOT / str(relative_path)
                if not source_path.exists():
                    errors.append(f"Ascendant Core manifest source {key} is missing: {relative_path}")

            domains = manifest.get("domain_files", {})
            core_domains = set(manifest.get("core_domains", []))
            if not isinstance(domains, dict) or len(domains) < 8:
                errors.append("Ascendant Core manifest must list all domain files.")
                domains = {}
            for domain in core_domains:
                if domain not in domains:
                    errors.append(f"Ascendant Core manifest is missing domain file mapping for {domain}.")
            for key, relative_path in domains.items():
                domain_path = ROOT / str(relative_path)
                if not domain_path.exists():
                    errors.append(f"Ascendant Core domain {key} is missing: {relative_path}")
                else:
                    try:
                        read_json(domain_path)
                    except Exception as exc:
                        errors.append(f"Ascendant Core domain {key} JSON is invalid: {exc}")

            scoreboards = {
                str(entry.get("id", ""))
                for entry in manifest.get("runtime_scoreboards", [])
                if isinstance(entry, dict)
            }
            for expected_objective in [
                "ar_guild_rep",
                "ar_guild_rank",
                "ar_bounties_done",
                "ar_structures_done",
                "ar_bosses_done",
                "ar_dragons_done",
                "ar_region_tier",
                "ar_threat_tier",
                "ar_hunt_kills",
                "ar_elite_kills",
                "ar_core_state",
            ]:
                if expected_objective not in scoreboards:
                    errors.append(f"Ascendant Core manifest is missing runtime scoreboard {expected_objective}.")

            core_count_expectations = [
                (ascendant_core_root / "world_regions.json", "regions", 7),
                (ascendant_core_root / "mob_ecology.json", "groups", 7),
                (ascendant_core_root / "structure_ecology.json", "groups", 6),
                (ascendant_core_root / "loot_rarity_rules.json", "tiers", 7),
                (ascendant_core_root / "npc_role_contracts.json", "roles", 7),
                (ascendant_core_root / "material_unification.json", "material_groups", 4),
                (ascendant_core_root / "progression_hooks.json", "hooks", 8),
                (ascendant_core_root / "custom_module_plan.json", "modules", 5),
            ]
            for path, key, minimum_count in core_count_expectations:
                data = read_json(path)
                values = data.get(key, [])
                if not isinstance(values, list) or len(values) < minimum_count:
                    errors.append(
                        f"Ascendant Core {path.name} has {len(values) if isinstance(values, list) else 0} "
                        f"{key}; expected at least {minimum_count}."
                    )

            rank_data = read_json(ascendant_core_root / "rank_progression.json")
            rank_ladder = rank_data.get("rank_ladder", [])
            rank_ids = [entry.get("id") for entry in rank_ladder if isinstance(entry, dict)]
            if rank_ids != ["unranked", "e_rank", "d_rank", "c_rank", "b_rank", "a_rank", "s_rank"]:
                errors.append("Ascendant Core rank_progression.json must keep the canonical Guild rank order.")

            loot_rules = read_json(ascendant_core_root / "loot_rarity_rules.json")
            active_presenters = loot_rules.get("active_presenters", {})
            for presenter in ["item_borders", "tooltips", "loot_beams", "legendary_tooltips"]:
                if presenter not in active_presenters:
                    errors.append(f"Ascendant Core loot_rarity_rules.json is missing active presenter {presenter}.")

            runtime_rules = read_json(ascendant_core_root / "runtime_rules.json")
            if not runtime_rules.get("enabled", False):
                errors.append("config/ascendant_core/runtime_rules.json must keep enabled=true.")
            for key in ["rank_promotions", "region_tiers"]:
                values = runtime_rules.get(key, [])
                if not isinstance(values, list) or len(values) < 6:
                    errors.append(f"Ascendant Core runtime_rules.json must define at least 6 {key}.")
            for key in ["kill_rewards", "namespace_roles", "entity_overrides"]:
                values = runtime_rules.get(key, {})
                if not isinstance(values, dict) or not values:
                    errors.append(f"Ascendant Core runtime_rules.json must define {key}.")
            runtime_boards = runtime_rules.get("scoreboards", {})
            for key in ["hunt_kills", "elite_kills", "region_tier", "threat_tier"]:
                if key not in runtime_boards:
                    errors.append(f"Ascendant Core runtime_rules.json is missing scoreboard mapping {key}.")

            module_plan = read_json(ascendant_core_root / "custom_module_plan.json")
            modules = {
                str(module.get("id", ""))
                for module in module_plan.get("modules", [])
                if isinstance(module, dict)
            }
            for expected_module in [
                "ascendant_core",
                "ascendant_nameplates",
                "ascendant_npc_runtime",
                "ascendant_settlement_engine",
                "ascendant_atlas",
                "ascendant_encounter_director",
            ]:
                if expected_module not in modules:
                    errors.append(f"Ascendant Core custom module plan is missing {expected_module}.")
        except Exception as exc:
            errors.append(f"Ascendant Core manifest validation failed: {exc}")

    ascendant_core_script = ROOT / "kubejs/server_scripts/ascendant_core_integration.js"
    if ascendant_core_script.exists():
        core_script_text = read_text(ascendant_core_script)
        for expected in [
            "ASCENDANT_CORE_MANIFEST_PATH",
            "config/ascendant_core/core_manifest.json",
            "JsonIO",
            "AscendantCoreJsonIO.read",
            "ServerEvents.loaded",
            "PlayerEvents.loggedIn",
            "PlayerEvents.tick",
            "EntityEvents.death",
            "runtime_scoreboards",
            "ASCENDANT_CORE_RUNTIME_RULES_PATH",
            "scoreboard objectives add",
            "scoreboard players set #manifest ar_core_state",
            "ascendantCorePlayerId",
            "ascendantCoreEnsurePlayerScores",
            "It does not rewrite worldgen, mob spawns",
        ]:
            if expected not in core_script_text:
                errors.append(f"kubejs/server_scripts/ascendant_core_integration.js is missing {expected}.")
        for forbidden in [
            "java.nio.file.Files",
            "java.nio.file.Paths",
            "java.io.File",
            'Java.loadClass("java.io.File")',
            ".getFileSystem().getPath(",
            ".resolve(",
            "AscendantCoreFiles",
            "AscendantCoreFile",
            "const candidate = candidates[i]",
            "const killerPlayer = ascendantCoreFindKiller",
            "for (let i = 0; i < tiers.length; i++)",
            "promotions.forEach((promotion)",
        ]:
            if forbidden in core_script_text:
                errors.append(
                    "kubejs/server_scripts/ascendant_core_integration.js contains a blocked pattern "
                    f"that has failed under KubeJS/Rhino: {forbidden}"
                )

    sync_active_client = ROOT / "scripts/sync-active-client-files.ps1"
    if sync_active_client.exists():
        sync_active_client_text = read_text(sync_active_client)
        if "config\\ascendant_core" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must sync config\\ascendant_core.")
        for required_sync_file in [
            "guardvillagers-common.toml",
            "spawnbalanceutility-common.toml",
            "majruszsdifficulty.json",
            "healthbarplus-client.toml",
            "lootbeams-client.toml",
            "integrated_villages-forge-1_20.toml",
            "create_structures_arise-server.toml",
        ]:
            if required_sync_file not in sync_active_client_text:
                errors.append(
                    "scripts/sync-active-client-files.ps1 must sync tuned gameplay/config file "
                    f"{required_sync_file}."
                )

    progression_config = ROOT / "config/ascendant_progression/progression.json"
    if progression_config.exists():
        try:
            data = read_json(progression_config)
            if not data.get("enabled", False):
                errors.append("config/ascendant_progression/progression.json must keep enabled=true.")
            category_ids = data.get("category_ids", [])
            if not isinstance(category_ids, list) or not any(str(value).endswith(":ascendant") or str(value) == "ascendant" for value in category_ids):
                errors.append("Ascendant progression config must include an Ascendant Web Puffish category id.")
            scoreboard = data.get("scoreboard", {})
            for key, expected in {
                "level_objective": "ar_skill_level",
                "xp_objective": "ar_skill_xp",
                "xp_required_objective": "ar_skill_xp_req",
                "points_left_objective": "ar_skill_sp",
                "points_spent_objective": "ar_skill_spent",
                "points_total_objective": "ar_skill_total",
            }.items():
                if scoreboard.get(key) != expected:
                    errors.append(f"Ascendant progression scoreboard {key} must be {expected}.")
            hud = data.get("hud", {})
            if hud.get("style") != "vanilla_blue_segments":
                errors.append("Ascendant progression HUD must use the vanilla_blue_segments style instead of the failed custom texture fill.")
            if hud.get("draw_mode") != "ingame":
                errors.append("Ascendant progression HUD must use draw_mode=ingame so it does not render over menus/resource-pack screens.")
            if hud.get("hide_in_creative") is not True or hud.get("hide_in_spectator") is not True:
                errors.append("Ascendant progression HUD must hide in creative and spectator while the KubeJS overlay fallback is active.")
            if hud.get("y") != "$screenH - 55":
                errors.append("Ascendant progression HUD y should keep the blue skill XP strip above the vanilla heart/armor rows until a custom HUD helper can shift them.")
            if hud.get("level_text_y") != "$screenH - 66":
                errors.append("Ascendant progression level text should stay compact above the non-overlapping XP strip.")
            if hud.get("track_y") != hud.get("y") or hud.get("fill_y") != hud.get("y"):
                errors.append("Ascendant progression track/fill y positions must match the frame to avoid split double bars.")
            if int(hud.get("height", 0) or 0) > 4:
                errors.append("Ascendant progression HUD height should stay vanilla XP-bar thin.")
            if int(hud.get("fill_height", 0) or 0) != int(hud.get("height", 0) or 0):
                errors.append("Ascendant progression HUD fill_height should match height so the segmented fill sits inside one bar.")
            if int(hud.get("segment_count", 0) or 0) != 20:
                errors.append("Ascendant progression HUD should use 20 segments to mimic the vanilla XP bar.")
            for expected_key in ["track_color", "track_border_color", "segment_track_color", "track_x", "track_y", "fill_x", "fill_y", "xp_text_y"]:
                if expected_key not in hud:
                    errors.append(f"Ascendant progression HUD config is missing {expected_key}.")
            if int(data.get("sync_interval_ticks", 0) or 0) <= 0:
                errors.append("Ascendant progression sync_interval_ticks must be positive.")
            milestones = (data.get("managed_bonus_points") or {}).get("milestones", [])
            if not isinstance(milestones, list) or len(milestones) < 5:
                errors.append("Ascendant progression managed bonus points should define at least five long-term milestones.")
        except Exception as exc:
            errors.append(f"Ascendant progression config JSON is invalid: {exc}")

    progression_script = ROOT / "kubejs/server_scripts/ascendant_progression.js"
    if progression_script.exists():
        progression_script_text = read_text(progression_script)
        for expected in [
            "AscendantSkillsAPI",
            "JsonIO",
            "AscendantProgressionJsonIO.read",
            "getExperience()",
            "getPointsLeft",
            "getSpentPoints",
            "getPointsTotal",
            "setExtraPoints",
            "managed_bonus_points",
            "player.paint",
            "ar_xp_track",
            "ar_xp_segment_fill_",
            "vanilla_blue_segments",
            "shouldHideAscendantProgressionHud",
            "clearAscendantProgressionHud",
            "scoreboard objectives setdisplay belowName",
            "ar_skill_level",
            "getAscendantPlayerId",
            "Level Up!",
        ]:
            if expected not in progression_script_text:
                errors.append(f"kubejs/server_scripts/ascendant_progression.js is missing {expected}.")
        for forbidden in [
            "kjs$getXpLevel",
            "getXpLevel",
            "scoreboard objectives setdisplay belowName ar_level",
            "scoreboard objectives add ar_level level",
            "const id = String(player.getUUID())",
        ]:
            if forbidden in progression_script_text:
                errors.append(
                    "Ascendant progression script must read Puffish Skills, not vanilla XP or old fallback: "
                    f"{forbidden}"
                )
        for forbidden in [
            "java.nio.file.Files",
            "java.nio.file.Paths",
            "java.io.File",
            'Java.loadClass("java.io.File")',
            ".getFileSystem().getPath(",
            ".resolve(",
            "AscendantFiles",
            "AscendantProgressionFile",
            "Java.from",
            "const optional =",
            "for (let i = 0; i < milestones.length; i++)",
            "const level = Number(milestones[i].level",
            "const progress = collectAscendantProgression(player)",
            "texture: hud.texture",
            "u1: progress.progress",
        ]:
            if forbidden in progression_script_text:
                errors.append(
                    "kubejs/server_scripts/ascendant_progression.js contains a blocked pattern "
                    f"that has failed under KubeJS/Rhino: {forbidden}"
                )

    sync_active_client = ROOT / "scripts/sync-active-client-files.ps1"
    if sync_active_client.exists():
        sync_active_client_text = read_text(sync_active_client)
        if "config\\ascendant_progression" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must sync config\\ascendant_progression.")
        if "config\\ascendant_atlas" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must sync config\\ascendant_atlas.")
        if "ascendant-atlas-regions-0.1.0.jar" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must directly sync the local Ascendant Atlas helper jar.")
        if "ascendant-nametags-0.1.0.jar" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must directly sync the local Ascendant Nametags helper jar.")
        if "travelerstitles-forge-1_20.toml" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must sync Traveler's Titles config.")
        if "irons_spellbooks-client.toml" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must sync Iron's Spells client HUD config.")
        if "overflowingbars-client.toml" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must sync Overflowing Bars client HUD config.")
        if "resourcepackoverrides.json" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must sync Resource Pack Overrides config.")
        if "oculus.properties" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must sync Oculus shader selection config.")
        if "Install-PackwizClientJar" not in sync_active_client_text or "mods\\resource-pack-overrides.pw.toml" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must install Resource Pack Overrides into the active client when syncing.")
        if "Write-Utf8NoBomLines" not in sync_active_client_text or "UTF8Encoding]::new($false)" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must write options.txt as UTF-8 without BOM.")
        if "Ensure-ModernOptionsVersion" not in sync_active_client_text or "version:3465" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must keep options.txt at Minecraft 1.20.1 options version 3465.")
        if "Copy-ResourcePacks" not in sync_active_client_text or "*.pw.toml" not in sync_active_client_text:
            errors.append("scripts/sync-active-client-files.ps1 must exclude Packwiz .pw.toml metadata from the live resourcepacks folder.")
        if "shaderpacks" not in sync_active_client_text or "ComplementaryReimagined" not in read_text(ROOT / "shaderpacks/complementary-reimagined.pw.toml"):
            errors.append(
                "scripts/sync-active-client-files.ps1 must install Packwiz shaderpacks into the active client; "
                "Complementary Reimagined should not disappear from Ascendant Realms (2)."
            )

    oculus_config = ROOT / "config/oculus.properties"
    if "mods/oculus.pw.toml" in active_relatives and oculus_config.exists():
        oculus_text = read_text(oculus_config)
        if "shaderPack=ComplementaryReimagined_r5.8.1.zip" not in oculus_text:
            errors.append("config/oculus.properties must select ComplementaryReimagined_r5.8.1.zip.")
        if "enableShaders=true" not in oculus_text:
            errors.append("config/oculus.properties must keep shaders enabled for the current visual baseline.")

    irons_client_config = ROOT / "config/irons_spellbooks-client.toml"
    if irons_client_config.exists():
        irons_client_text = read_text(irons_client_config)
        if 'manaBarAnchor = "Hunger"' not in irons_client_text:
            errors.append("Iron's Spells mana bar should stay anchored to Hunger for the current HUD stack.")
        if "manaBarYOffset = 11" not in irons_client_text:
            errors.append("Iron's Spells mana bar should be shifted up by one row for the Ascendant HUD stack.")

    overflowingbars_config = ROOT / "config/overflowingbars-client.toml"
    if overflowingbars_config.exists():
        overflowingbars_text = read_text(overflowingbars_config)
        if "move_chat_above_armor = true" not in overflowingbars_text:
            errors.append("Overflowing Bars should keep chat moved above armor/status rows.")
        if "move_experience_above_bar = true" not in overflowingbars_text:
            errors.append("Overflowing Bars should keep experience level above the vanilla XP bar.")

    custom_npc_profiles = guild_root / "custom_npc_test_profiles.json"
    if custom_npc_profiles.exists():
        try:
            profile_data = read_json(custom_npc_profiles)
            for profile in profile_data.get("test_profiles", []):
                if "display_name" in profile:
                    errors.append(
                        "Custom NPC test profiles should use profile_key/generated_name/generated_title, "
                        f"not hardcoded display_name: {profile.get('id')}"
                    )
                for expected in ["profile_key", "generated_name", "generated_title"]:
                    if expected not in profile:
                        errors.append(
                            f"Custom NPC test profile {profile.get('id', '<unknown>')} is missing {expected}."
                        )
        except Exception as exc:
            errors.append(f"Ascendant Guild custom_npc_test_profiles.json is invalid: {exc}")

    guild_tool_audit = guild_root / "tool_audit.json"
    if guild_tool_audit.exists():
        try:
            audit_data = read_json(guild_tool_audit)
            installed = set(audit_data.get("installed", []))
            delayed = {entry.get("name") for entry in audit_data.get("delayed", [])}
            for name in [
                "Patchouli",
                "FTB Quests",
                "FTB Ranks",
                "Easy NPC",
                "CustomNPCs-Unofficial",
                "Human Companions",
                "MCA Reborn",
            ]:
                if name not in installed:
                    errors.append(f"Ascendant Guild tool audit must list installed tool: {name}")
        except Exception as exc:
            errors.append(f"Ascendant Guild tool_audit.json is invalid: {exc}")

    guild_items_script = ROOT / "kubejs/startup_scripts/ascendant_guild_items.js"
    if guild_items_script.exists():
        guild_items_text = read_text(guild_items_script)
        for item_id in ["guild_mark", "hunter_seal", "ascendant_sigil"]:
            if item_id not in guild_items_text:
                errors.append(f"Ascendant Guild KubeJS item script is missing {item_id}.")

    rarity_schema = ROOT / "config/ascendant_index/rarity_schema.json"
    if rarity_schema.exists():
        try:
            schema = read_json(rarity_schema)
            tier_ids = {tier.get("id") for tier in schema.get("tiers", [])}
            if schema.get("version") != 1:
                errors.append("Ascendant rarity schema must use version 1.")
            for required_tier in ["common", "rare", "epic", "legendary", "mythic", "ascendant"]:
                if required_tier not in tier_ids:
                    errors.append(f"Ascendant rarity schema is missing tier: {required_tier}")
            if len(schema.get("entries_needing_rarity", [])) < 25:
                errors.append("Ascendant rarity schema has too few entries needing rarity/integration.")
        except Exception as exc:
            errors.append(f"Ascendant rarity schema JSON is invalid: {exc}")

    missing_batch_e1 = sorted(BATCH_E1_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_e1:
        errors.append(f"Batch E1 metadata is missing: {relative}")

    missing_batch_e2 = sorted(BATCH_E2_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_e2:
        errors.append(f"Batch E2 metadata is missing: {relative}")

    missing_batch_f = sorted(BATCH_F_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_f:
        errors.append(f"Batch F metadata is missing: {relative}")

    missing_batch_g = sorted(BATCH_G_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_g:
        errors.append(f"Batch G metadata is missing: {relative}")

    missing_batch_h = sorted(BATCH_H_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_h:
        errors.append(f"Batch H metadata is missing: {relative}")

    missing_batch_j = sorted(BATCH_J_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_j:
        errors.append(f"Batch J candidate-pass metadata is missing: {relative}")

    missing_batch_k = sorted(BATCH_K_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_k:
        errors.append(f"Batch K metadata is missing: {relative}")

    missing_batch_l = sorted(BATCH_L_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_l:
        errors.append(f"Batch L metadata is missing: {relative}")

    missing_batch_n = sorted(BATCH_N_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_n:
        errors.append(f"Batch N metadata is missing: {relative}")

    missing_batch_m = sorted(BATCH_M_REQUIRED_METADATA - active_relatives)
    for relative in missing_batch_m:
        errors.append(f"Batch M metadata is missing: {relative}")

    missing_world_ui_polish = sorted(WORLD_UI_POLISH_REQUIRED_METADATA - active_relatives)
    for relative in missing_world_ui_polish:
        errors.append(f"World integration/menu polish metadata is missing: {relative}")

    missing_ui_customization_tooling = sorted(UI_CUSTOMIZATION_TOOLING_REQUIRED_METADATA - active_relatives)
    for relative in missing_ui_customization_tooling:
        errors.append(f"UI customization tooling metadata is missing: {relative}")

    missing_guild_hunter = sorted(GUILD_HUNTER_REQUIRED_METADATA - active_relatives)
    for relative in missing_guild_hunter:
        errors.append(f"Guild/Hunter tooling metadata is missing: {relative}")

    original_ice_and_fire_candidates = {
        "mods/ice-and-fire-dragons.pw.toml",
        "mods/ice-and-fire.pw.toml",
    }
    if "mods/iceandfire-ce.pw.toml" in active_relatives and active_relatives.intersection(original_ice_and_fire_candidates):
        errors.append("Both IceAndFire Community Edition and original Ice and Fire metadata are active; Batch G must use exactly one.")

    if "mods/subtle-effects.pw.toml" in active_relatives:
        if forge_version and forge_version < (47, 4, 14):
            errors.append("Subtle Effects is installed but Forge is below 47.4.14.")

    if "mods/fzzy-config.pw.toml" in active_relatives:
        if "mods/kotlin-for-forge.pw.toml" not in active_relatives:
            errors.append("Fzzy Config is installed but Kotlin for Forge is missing.")
        else:
            kotlin_text = active_text_by_relative["mods/kotlin-for-forge.pw.toml"]
            kotlin_filename = metadata_filename(kotlin_text)
            kotlin_version = version_tuple(kotlin_filename)
            if not kotlin_version:
                warnings.append("Could not detect Kotlin for Forge version from filename.")
            elif not ((4, 11, 0) <= kotlin_version <= (4, 99, 0)):
                errors.append(
                    f"Kotlin for Forge version in {kotlin_filename} is outside fzzy_config's required 4.11.0-4.99.0 range."
                )

    if "mods/loot-integrations.pw.toml" in active_relatives and "mods/cupboard.pw.toml" not in active_relatives:
        errors.append("Loot Integrations is installed but Cupboard is missing.")

    if "mods/artifacts.pw.toml" in active_relatives and "mods/curios.pw.toml" not in active_relatives:
        errors.append("Artifacts is installed but Curios API is missing.")

    if "mods/irons-spells-n-spellbooks.pw.toml" in active_relatives and "mods/irons-lib.pw.toml" not in active_relatives:
        errors.append("Iron's Spells is installed but Iron's Lib is missing.")

    if "mods/aquamirae.pw.toml" in active_relatives and "mods/obscure-api.pw.toml" not in active_relatives:
        errors.append("Aquamirae is installed but Obscure API is missing.")

    if "mods/iceandfire-ce.pw.toml" in active_relatives:
        for relative in ["mods/jupiter.pw.toml", "mods/uranus.pw.toml"]:
            if relative not in active_relatives:
                errors.append(f"IceAndFire Community Edition is installed but {relative} is missing.")

    if "mods/l_enders-cataclysm.pw.toml" in active_relatives:
        for relative in ["mods/lionfish-api.pw.toml", "mods/curios.pw.toml"]:
            if relative not in active_relatives:
                errors.append(f"L_Ender's Cataclysm is installed but {relative} is missing.")

    if "mods/mariums-soulslike-weaponry.pw.toml" in active_relatives:
        for relative in ["mods/attributefix.pw.toml", "mods/projectile-damage-attribute.pw.toml", "mods/geckolib.pw.toml"]:
            if relative not in active_relatives:
                errors.append(f"Marium's Soulslike Weaponry is installed but {relative} is missing.")
        projectile_text = active_text_by_relative.get("mods/projectile-damage-attribute.pw.toml", "")
        projectile_filename = metadata_filename(projectile_text)
        if projectile_filename != "projectile_damage-forge-3.2.2+1.20.1.jar":
            errors.append(
                "Marium's Soulslike Weaponry requires the Projectile Damage Attribute startup-fix pin "
                "`projectile_damage-forge-3.2.2+1.20.1.jar`; "
                f"found {projectile_filename or 'missing filename'}."
            )

    if "mods/create-big-cannons.pw.toml" in active_relatives:
        for relative in ["mods/create.pw.toml", "mods/rpl.pw.toml"]:
            if relative not in active_relatives:
                errors.append(f"Create Big Cannons is installed but {relative} is missing.")

    if "mods/create-structures-arise.pw.toml" in active_relatives and "mods/create.pw.toml" not in active_relatives:
        errors.append("Create: Structures Arise is installed but Create is missing.")

    if "mods/kubejs.pw.toml" in active_relatives and "mods/rhino.pw.toml" not in active_relatives:
        errors.append("KubeJS is installed but Rhino is missing.")

    if "mods/ftb-quests-forge.pw.toml" in active_relatives:
        for relative in ["mods/ftb-library-forge.pw.toml", "mods/ftb-teams-forge.pw.toml", "mods/architectury-api.pw.toml"]:
            if relative not in active_relatives:
                errors.append(f"FTB Quests is installed but {relative} is missing.")

    if "mods/ftb-ranks-forge.pw.toml" in active_relatives and "mods/ftb-library-forge.pw.toml" not in active_relatives:
        errors.append("FTB Ranks is installed but FTB Library is missing.")

    if "mods/easy-npc-core.pw.toml" in active_relatives or "mods/easy-npc-config-ui.pw.toml" in active_relatives:
        for relative in ["mods/easy-npc-core.pw.toml", "mods/easy-npc-config-ui.pw.toml"]:
            if relative not in active_relatives:
                errors.append(f"Easy NPC Prism-managed split is installed but {relative} is missing.")

    if "mods/patchouli.pw.toml" in active_relatives:
        codex_book = ROOT / "config/openloader/data/ascendant_realms_codex/data/ascendant_realms/patchouli_books/ascendant_codex/book.json"
        if not codex_book.exists():
            errors.append("Patchouli is installed but the active Ascendant Codex book.json is missing.")
        else:
            try:
                codex_data = read_json(codex_book)
                if codex_data.get("name") != "Ascendant Codex":
                    errors.append("Ascendant Codex book.json must have name = Ascendant Codex.")
            except Exception as exc:
                errors.append(f"Ascendant Codex book.json is invalid: {exc}")

    if "mods/almost-unify-everything.pw.toml" in active_relatives and "mods/almostunified.pw.toml" not in active_relatives:
        errors.append("Almost Unify Everything is installed but Almost Unified is missing.")

    if "mods/every-compat.pw.toml" in active_relatives and "mods/moonlight.pw.toml" not in active_relatives:
        errors.append("Every Compat is installed but Moonlight Lib is missing.")

    if "mods/supplementaries.pw.toml" in active_relatives and "mods/moonlight.pw.toml" not in active_relatives:
        errors.append("Supplementaries is installed but Moonlight Lib is missing.")

    if "mods/supplementaries.pw.toml" in active_relatives and "mods/amendments.pw.toml" not in active_relatives:
        errors.append(
            "Supplementaries is installed but Amendments is missing. Supplementaries 2.8.0+ moved wall lanterns, "
            "skull candles, ceiling pots, ceiling banners, and skull piles into Amendments."
        )

    if "mods/sodium-dynamic-lights.pw.toml" in active_relatives:
        if "mods/sodium-options-api.pw.toml" not in active_relatives:
            errors.append("Sodium Dynamic Lights is installed but Sodium Options API is missing.")
        dynamic_light_conflicts = [
            "mods/ryoamiclights.pw.toml",
            "mods/ryoamic-lights.pw.toml",
            "mods/lambdynamiclights.pw.toml",
            "mods/lamb-dynamic-lights.pw.toml",
        ]
        for relative in dynamic_light_conflicts:
            if relative in active_relatives:
                errors.append(
                    "Do not stack multiple dynamic-light engines. Sodium Dynamic Lights is active, "
                    f"but {relative} is also active."
                )

    if "mods/quark.pw.toml" in active_relatives and "mods/zeta.pw.toml" not in active_relatives:
        errors.append("Quark is installed but Zeta is missing.")

    if "mods/slice-and-dice.pw.toml" in active_relatives:
        for relative in ["mods/create.pw.toml", "mods/farmers-delight.pw.toml"]:
            if relative not in active_relatives:
                errors.append(f"Create Slice & Dice is installed but {relative} is missing.")

    if "mods/alexs-delight.pw.toml" in active_relatives:
        for relative in ["mods/alexs-mobs.pw.toml", "mods/farmers-delight.pw.toml"]:
            if relative not in active_relatives:
                errors.append(f"Alex's Delight is installed but {relative} is missing.")

    if "mods/integrated-villages.pw.toml" in active_relatives and "mods/integrated-api.pw.toml" not in active_relatives:
        warnings.append("Integrated Villages is active; keep Integrated API installed for the Integrated worldgen stack.")

    if "mods/integrated-villages.pw.toml" in active_relatives:
        world_integration_root = ROOT / "config/openloader/data/ascendant_realms_world_integration"
        workstation_repaired_villages = [
            "airship_village",
            "cabin_village",
            "clockwork_village",
            "kutcha_village",
            "marketstead_village",
            "mediterranean_village",
            "minka_village",
            "mossy_mounds",
            "oasis_village",
            "pirate_village_dock",
            "pirate_village",
            "swamp_village",
            "tavern_village",
        ]
        processor_root = world_integration_root / "data/integrated_villages/worldgen/processor_list"
        if not processor_root.exists():
            errors.append(
                "Integrated Villages is active, but the OpenLoader processor-list repair folder is missing. "
                "This repair bypasses integrated_api:workstation_processor, the shared POI-cast crash path."
            )
        else:
            for processor_name in workstation_repaired_villages:
                processor_file = processor_root / f"{processor_name}_processor.json"
                if not processor_file.exists():
                    errors.append(f"Integrated Villages workstation repair is missing {processor_file.relative_to(ROOT)}.")
                    continue
                try:
                    processor_text = read_text(processor_file)
                    if "integrated_api:workstation_processor" in processor_text:
                        errors.append(
                            f"{processor_file.relative_to(ROOT)} must not use integrated_api:workstation_processor; "
                            "use static minecraft:rule replacements for workstation placeholders."
                        )
                    if "minecraft:rule" not in processor_text:
                        errors.append(
                            f"{processor_file.relative_to(ROOT)} is missing the static minecraft:rule workstation replacement."
                        )
                except Exception as exc:
                    errors.append(f"Integrated Villages workstation repair could not be read: {exc}")

        for repaired_biome_tag in [
            "airship_village_biomes",
            "mossy_mounds_biomes",
            "marketstead_village_biomes",
        ]:
            biome_tag = (
                world_integration_root
                / f"data/integrated_villages/tags/worldgen/biome/has_structure/{repaired_biome_tag}.json"
            )
            if not biome_tag.exists():
                errors.append(f"Integrated Villages repaired biome tag is missing: {biome_tag.relative_to(ROOT)}")
                continue
            try:
                biome_data = read_json(biome_tag)
                if biome_data.get("values") == []:
                    errors.append(
                        f"{biome_tag.relative_to(ROOT)} still disables the repaired structure. "
                        "The workstation processor repair should keep this structure enabled for retest."
                    )
            except Exception as exc:
                errors.append(f"Integrated Villages repaired biome tag JSON is invalid: {exc}")

        active_village_tag = world_integration_root / "data/minecraft/tags/worldgen/structure/village.json"
        if not active_village_tag.exists():
            errors.append(
                "Integrated Villages is active, but the active OpenLoader minecraft:village repair tag is missing."
            )
        else:
            try:
                village_data = read_json(active_village_tag)
                village_values = village_data.get("values", [])
                if village_data.get("replace") is not True:
                    errors.append("OpenLoader minecraft:village repair tag must use replace=true.")
                for forbidden_structure in [
                    "integrated_villages:swamp_village",
                ]:
                    if forbidden_structure in village_values:
                        errors.append(
                            "OpenLoader minecraft:village repair tag must not include "
                            f"{forbidden_structure}; the upstream tag references it but no active structure file exists."
                        )
                for required_structure in [
                    "minecraft:village_plains",
                    "minecraft:village_desert",
                    "integrated_villages:airship_village",
                    "integrated_villages:mossy_mounds",
                    "integrated_villages:marketstead_village",
                    "integrated_villages:clockwork_village",
                    "integrated_villages:sunken_village",
                ]:
                    if required_structure not in village_values:
                        errors.append(f"OpenLoader minecraft:village repair tag is missing {required_structure}.")
            except Exception as exc:
                errors.append(f"OpenLoader minecraft:village repair tag JSON is invalid: {exc}")

        active_integrated_village_tag = (
            world_integration_root / "data/integrated_villages/tags/worldgen/structure/villages.json"
        )
        active_integrated_village_set = (
            world_integration_root / "data/integrated_villages/worldgen/structure_set/regular_villages.json"
        )
        for active_structure_file in [active_integrated_village_tag, active_integrated_village_set]:
            if not active_structure_file.exists():
                errors.append(f"Integrated Villages repair file is missing: {active_structure_file.relative_to(ROOT)}")
                continue
            try:
                active_structure_text = read_text(active_structure_file)
                if "integrated_villages:swamp_village" in active_structure_text:
                    errors.append(
                        f"{active_structure_file.relative_to(ROOT)} must not include integrated_villages:swamp_village; "
                        "the upstream tag references it but no active structure file exists."
                    )
                for repaired_structure in [
                    "integrated_villages:mossy_mounds",
                    "integrated_villages:marketstead_village",
                ]:
                    if repaired_structure not in active_structure_text:
                        errors.append(
                            f"{active_structure_file.relative_to(ROOT)} should include repaired structure {repaired_structure}."
                        )
            except Exception as exc:
                errors.append(f"Integrated Villages repair file could not be read: {exc}")

        aquamirae_surface_set = world_integration_root / "data/aquamirae/worldgen/structure_set/surface.json"
        if not aquamirae_surface_set.exists():
            errors.append(f"{rel(aquamirae_surface_set)} is required to reduce Aquamirae surface-structure density.")
        else:
            try:
                surface_set = read_json(aquamirae_surface_set)
                placement = surface_set.get("placement", {})
                spacing = int(placement.get("spacing", 0) or 0)
                separation = int(placement.get("separation", -1) or -1)
                if placement.get("type") != "minecraft:random_spread":
                    errors.append(f"{rel(aquamirae_surface_set)} must keep random_spread placement.")
                if spacing < 20:
                    errors.append(f"{rel(aquamirae_surface_set)} spacing must be at least 20.")
                if separation < 8:
                    errors.append(f"{rel(aquamirae_surface_set)} separation must be at least 8.")
                if spacing <= separation:
                    errors.append(f"{rel(aquamirae_surface_set)} spacing must be greater than separation.")
                structures = {
                    entry.get("structure")
                    for entry in surface_set.get("structures", [])
                    if isinstance(entry, dict)
                }
                for expected_structure in ["aquamirae:surface/arch", "aquamirae:surface/spiral"]:
                    if expected_structure not in structures:
                        errors.append(f"{rel(aquamirae_surface_set)} must keep {expected_structure}.")
            except Exception as exc:
                errors.append(f"{rel(aquamirae_surface_set)} JSON is invalid: {exc}")

        world_shim_expectations = {
            "data/humancompanions/tags/worldgen/biome/has_structure/oak_house.json": "windswept_gravelly_hills",
            "data/humancompanions/tags/worldgen/biome/has_structure/spruce_house.json": "windswept_gravelly_hills",
            "data/c/tags/entity_types/bosses.json": "minecraft:warden",
            "data/idas/integrated_structure_spawners/archmages_tower.json": "irons_spellbooks:archevoker",
            "data/idas/loot_tables/chests/enchantingtower/enchantingtower_basic_ars.json": "irons_spellbooks:scroll",
            "data/idas/loot_tables/chests/enchantingtower/enchantingtower_top_ars.json": "irons_spellbooks:diamond_spell_book",
            "data/idas/loot_tables/chests/archmages_tower/archmages_tower.json": "irons_spellbooks:arcane_essence",
            "data/idas/loot_tables/chests/archmages_tower/archmages_tower_library.json": "irons_spellbooks:eldritch_manuscript",
            "data/idas/loot_tables/chests/archmages_tower/archmages_tower_treasure.json": "irons_spellbooks:legendary_spell_book",
            "data/irons_spellbooks/loot_tables/chests/catacombs/crypt_loot.json": "irons_spellbooks:ancient_knowledge_fragment",
            "data/irons_spellbooks/loot_tables/chests/citadel/citadel_tomes.json": "Citadel Field Notes",
        }
        for relative, expected_text in world_shim_expectations.items():
            shim_path = world_integration_root / relative
            if not shim_path.exists():
                errors.append(f"World integration compatibility shim is missing: {shim_path.relative_to(ROOT)}")
                continue
            try:
                shim_text = read_text(shim_path)
                if expected_text not in shim_text:
                    errors.append(
                        f"World integration compatibility shim {shim_path.relative_to(ROOT)} is missing "
                        f"expected marker {expected_text}."
                    )
                if "windswept_gravelley_hills" in shim_text or "ars_nouveau:wilden_hunter" in shim_text:
                    errors.append(
                        f"World integration compatibility shim {shim_path.relative_to(ROOT)} still contains "
                        "a known broken optional reference."
                    )
            except Exception as exc:
                errors.append(f"World integration compatibility shim could not be read: {exc}")

        disabled_optional_recipe_shims = [
            "data/everycomp/recipes/fd/born_in_chaos_v1/salvaging/scorched_furniture.json",
            "data/everycomp/recipes/fd/born_in_chaos_v1/salvaging/scorched_chest_boat.json",
            "data/everycomp/recipes/fd/cataclysm/cutting/chorus_log.json",
            "data/everycomp/recipes/fd/cataclysm/salvaging/chorus_furniture.json",
            "data/everycomp/recipes/fd/cataclysm/salvaging/chorus_chest_boat.json",
            "data/everycomp/recipes/fd/iceandfire/cutting/dreadwood_log.json",
            "data/everycomp/recipes/fd/iceandfire/salvaging/dreadwood_furniture.json",
            "data/everycomp/recipes/fd/iceandfire/salvaging/dreadwood_chest_boat.json",
            "data/alexsdelight/recipes/barbecue_on_a_stick.json",
        ]
        for relative in disabled_optional_recipe_shims:
            shim_path = world_integration_root / relative
            if not shim_path.exists():
                errors.append(f"Disabled optional compat recipe shim is missing: {shim_path.relative_to(ROOT)}")
                continue
            try:
                shim_data = read_json(shim_path)
                conditions = shim_data.get("conditions", [])
                if not any(
                    condition.get("type") == "forge:false"
                    for condition in conditions
                    if isinstance(condition, dict)
                ):
                    errors.append(
                        f"Optional compat recipe shim must stay disabled with forge:false: {shim_path.relative_to(ROOT)}"
                    )
            except Exception as exc:
                errors.append(f"Disabled optional compat recipe shim JSON is invalid: {exc}")

    if "mods/idas.pw.toml" in active_relatives:
        for relative in ["mods/integrated-api.pw.toml", "mods/supplementaries.pw.toml", "mods/quark.pw.toml", "mods/zeta.pw.toml"]:
            if relative not in active_relatives:
                errors.append(f"IDAS is installed but {relative} is missing.")

    if "mods/fancymenu.pw.toml" in active_relatives:
        for relative in [
            "mods/konkrete.pw.toml",
            "mods/melody.pw.toml",
            "mods/watermedia.pw.toml",
            "mods/watermedia-binaries.pw.toml",
        ]:
            if relative not in active_relatives:
                errors.append(f"FancyMenu is installed but {relative} is missing.")
        fancymenu_assets = ROOT / "config/fancymenu/assets"
        for filename in [
            "ascendant_realms_title.png",
            "minecraft_title.png",
            "ascendant_realms_background.mp4",
            "ascendant_level_bar_spritesheet.png",
            "ascendant_menu_status.txt",
            "ascendant_pack_meta.json",
        ]:
            if not (fancymenu_assets / filename).exists():
                errors.append(f"FancyMenu is installed but config/fancymenu/assets/{filename} is missing.")
        level_bar_texture = ROOT / "kubejs/assets/kubejs/textures/gui/ascendant_level_bar_spritesheet.png"
        if not level_bar_texture.exists():
            errors.append("Ascendant HUD level bar texture is missing from kubejs/assets/kubejs/textures/gui/.")
        background_mp4 = fancymenu_assets / "ascendant_realms_background.mp4"
        if background_mp4.exists():
            streams, probe_warning = probe_media_streams(background_mp4)
            if probe_warning:
                warnings.append(probe_warning)
            else:
                audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
                video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
                if audio_streams:
                    errors.append("FancyMenu MP4 background must stay video-only; WaterMedia failed on the old audio-first MP4.")
                if not video_streams:
                    errors.append("FancyMenu MP4 background has no video stream.")
                else:
                    first_stream = streams[0] if streams else {}
                    video = video_streams[0]
                    profile = str(video.get("profile", ""))
                    codec = str(video.get("codec_name", ""))
                    width = int(video.get("width") or 0)
                    height = int(video.get("height") or 0)
                    if first_stream.get("codec_type") != "video":
                        errors.append("FancyMenu MP4 background must have the video stream first.")
                    if codec != "h264":
                        errors.append(f"FancyMenu MP4 background should use H.264 video, found {codec or 'unknown'}.")
                    if "Baseline" not in profile:
                        errors.append(f"FancyMenu MP4 background should use an H.264 Baseline profile, found {profile or 'unknown'}.")
                    if (width, height) != (1920, 1080):
                        warnings.append(f"FancyMenu MP4 background is {width}x{height}; expected 1920x1080 for the packaged menu layout.")
        status_asset = fancymenu_assets / "ascendant_menu_status.txt"
        if status_asset.exists():
            status_text = read_text(status_asset)
            if '"placeholder":"loadedmods"' not in status_text:
                errors.append("FancyMenu status text must use the live loadedmods placeholder instead of a hardcoded mod count.")
            if '"placeholder":"json"' not in status_text or "ascendant_pack_meta.json" not in status_text:
                errors.append("FancyMenu status text must read the Ascendant version from ascendant_pack_meta.json.")
            if re.search(r"\b\d+\s+Mods\b", status_text):
                errors.append("FancyMenu status text contains a hardcoded mod count.")
        meta_asset = fancymenu_assets / "ascendant_pack_meta.json"
        if meta_asset.exists():
            try:
                meta = read_json(meta_asset)
                pack_text = read_text(ROOT / "pack.toml")
                version_match = re.search(r'(?m)^version\s*=\s*"([^"]+)"', pack_text)
                if version_match and meta.get("version") != version_match.group(1):
                    errors.append("FancyMenu Ascendant version metadata does not match pack.toml.")
            except Exception as exc:
                errors.append(f"FancyMenu Ascendant version metadata JSON is invalid: {exc}")
        layout_file = ROOT / "config/fancymenu/customization/custom_title_screen_layout.txt"
        if layout_file.exists():
            layout_text = read_text(layout_file)
            if "identifier = title_screen" not in layout_text:
                errors.append("FancyMenu custom title-screen layout is not bound to the title_screen menu.")
            if "is_enabled = true" not in layout_text:
                errors.append("FancyMenu custom title-screen layout must stay enabled so it loads after reimport.")
            if "layout_index = 0" not in layout_text:
                errors.append("FancyMenu custom title-screen layout must stay at layout_index 0 for default loading.")
            if (
                "[source:local]/config/fancymenu/assets/minecraft_title.png" not in layout_text
                and "[source:local]/config/fancymenu/assets/ascendant_realms_title.png" not in layout_text
            ):
                errors.append("FancyMenu custom title-screen layout does not reference the Ascendant Realms title image.")
            if "ascendant_realms_background.mp4" not in layout_text and "ascendant_realms_menu_anim.mp4" not in layout_text:
                errors.append("FancyMenu custom title-screen layout does not reference a staged Ascendant MP4 background asset.")
            if '"placeholder":"loadedmods"' not in layout_text:
                errors.append("FancyMenu custom title-screen layout must use the live loadedmods placeholder.")
            if "ascendant_pack_meta.json" not in layout_text:
                errors.append("FancyMenu custom title-screen layout must use generated Ascendant version metadata.")
            if "element_type = text_v2" not in layout_text:
                errors.append("FancyMenu custom title-screen layout is missing the dynamic status text element.")
            if re.search(r"\b\d+\s+Mods\b", layout_text):
                errors.append("FancyMenu custom title-screen layout contains a hardcoded mod count.")
            video_block_match = re.search(
                r"background_type\s*=\s*video(?P<body>.*?)(?:\n}\s*\n|$)",
                layout_text,
                re.S,
            )
            if video_block_match and "show_background = false" in video_block_match.group("body"):
                warnings.append("FancyMenu title layout references the MP4 background, but the saved video background block is currently disabled.")
        drippy_options = ROOT / "config/drippyloadingscreen/options.txt"
        if drippy_options.exists():
            drippy_text = read_text(drippy_options)
            if "##[early_loading]" not in drippy_text:
                errors.append("Drippy Loading Screen options are missing the early_loading section.")

    for relative in ["mods/spiffyhud.pw.toml", "mods/drippy-loading-screen.pw.toml"]:
        if relative in active_relatives:
            for dependency in ["mods/fancymenu.pw.toml", "mods/konkrete.pw.toml", "mods/melody.pw.toml"]:
                if dependency not in active_relatives:
                    errors.append(f"{relative} is installed but {dependency} is missing.")

    if "mods/item-borders.pw.toml" in active_relatives:
        for relative in ["mods/iceberg.pw.toml", "mods/prism-lib.pw.toml"]:
            if relative not in active_relatives:
                errors.append(f"Item Borders is installed but {relative} is missing.")

    for relative in ["mods/stylish-effects.pw.toml", "mods/overflowing-bars.pw.toml"]:
        if relative in active_relatives and "mods/puzzles-lib.pw.toml" not in active_relatives:
            errors.append(f"{relative} is installed but Puzzles Lib is missing.")

    if "mods/perception.pw.toml" in active_relatives and "mods/shatterbyte-lib.pw.toml" not in active_relatives:
        errors.append("Perception is installed but OctoLib/ShatterLib is missing.")

    if "mods/scaling-health.pw.toml" in active_relatives and "mods/silent-lib.pw.toml" not in active_relatives:
        errors.append("Scaling Health is installed but Silent Lib is missing.")

    if "mods/weather-storms-tornadoes.pw.toml" in active_relatives and "mods/coroutil.pw.toml" not in active_relatives:
        errors.append("Weather, Storms & Tornadoes is installed but CoroUtil is missing.")

    if "mods/majruszs-progressive-difficulty.pw.toml" in active_relatives and "mods/majrusz-library.pw.toml" not in active_relatives:
        errors.append("Majrusz's Progressive Difficulty is installed but Majrusz Library is missing.")

    if "mods/improved-mobs.pw.toml" in active_relatives and "mods/tenshilib.pw.toml" not in active_relatives:
        errors.append("Improved Mobs is installed but TenshiLib is missing.")

    if "mods/ambientsounds.pw.toml" in active_relatives:
        ambient_filename = metadata_filename(active_text_by_relative["mods/ambientsounds.pw.toml"])
        if "mods/creativecore.pw.toml" not in active_relatives:
            errors.append("AmbientSounds 6 is installed but CreativeCore is missing.")
        if ambient_filename == "AmbientSounds_FORGE_v6.1.0_mc1.20.1.jar":
            errors.append(
                "AmbientSounds 6.1.0 is rejected for this pack because it crashes on startup with "
                "CreativeCore 2.12.38; use AmbientSounds_FORGE_v6.3.8_mc1.20.1.jar instead."
            )
        elif ambient_filename != "AmbientSounds_FORGE_v6.3.8_mc1.20.1.jar":
            warnings.append(
                "AmbientSounds filename differs from the validated crash-fix pin: "
                f"{ambient_filename or 'missing filename'}."
            )

    if "mods/project-atmosphere.pw.toml" in active_relatives and "mods/weather-storms-tornadoes.pw.toml" in active_relatives:
        errors.append("Do not stack Project Atmosphere with Weather, Storms & Tornadoes in Batch K/L.")

    if "mods/simple-clouds.pw.toml" in active_relatives and "mods/weather-storms-tornadoes.pw.toml" in active_relatives:
        errors.append("Do not stack Simple Clouds with Weather, Storms & Tornadoes in Batch K/L.")

    if "mods/to-tweaks-irons-spells.pw.toml" in active_relatives:
        for relative in [
            "mods/irons-spells-n-spellbooks.pw.toml",
            "mods/irons-lib.pw.toml",
            "mods/alexs-caves.pw.toml",
            "mods/apothic-attributes.pw.toml",
            "mods/placebo.pw.toml",
        ]:
            if relative not in active_relatives:
                errors.append(f"T.O Magic 'n Extras is installed but {relative} is missing.")

    if "mods/alexs-caves.pw.toml" in active_relatives and "mods/citadel.pw.toml" not in active_relatives:
        errors.append("Alex's Caves is installed but Citadel is missing.")

    if "mods/apothic-attributes.pw.toml" in active_relatives and "mods/placebo.pw.toml" not in active_relatives:
        errors.append("Apothic Attributes is installed but Placebo is missing.")

    if "mods/malfu-combat-animation.pw.toml" in active_relatives and "mods/better-combat.pw.toml" not in active_relatives:
        errors.append("Malfu Combat Animation is installed but Better Combat is missing.")

    if (
        "resourcepacks/embellished-stone-advancements-plaques.pw.toml" in active_relatives
        and "mods/advancement-plaques.pw.toml" not in active_relatives
    ):
        errors.append("Embellished Stone is installed but Advancement Plaques is missing.")

    if (
        "resourcepacks/icon-xaeros-x-freshanimations.pw.toml" in active_relatives
        and "resourcepacks/icon-xaeros.pw.toml" not in active_relatives
    ):
        errors.append("Icon Xaero's X FreshAnimations is installed but Icon Xaero's is missing.")

    if (
        "resourcepacks/icon-xaeros-x-freshanimations.pw.toml" in active_relatives
        and "resourcepacks/fresh-animations.pw.toml" not in active_relatives
    ):
        errors.append("Icon Xaero's X FreshAnimations is installed but Fresh Animations is missing.")

    if (
        "resourcepacks/simply-swords-reforged.pw.toml" in active_relatives
        and "mods/simply-swords.pw.toml" not in active_relatives
    ):
        errors.append("Simply Swords Reforged is installed but Simply Swords is missing.")

    if "mods/lendercataclysm.pw.toml" in active_relatives:
        errors.append("Duplicate Cataclysm metadata is active as mods/lendercataclysm.pw.toml.")

    if "mods/travelerscrossroads.pw.toml" in active_relatives:
        errors.append("TravelersCrossroads is active, but current project metadata only shows 1.21.x NeoForge.")

    delayed_t_magic_chain = {
        "mods/to-tweaks-irons-spells.pw.toml": "T.O Magic is delayed because traveloptics 6.3.0 crashes against Cataclysm 3.30 with missing DungeonEyeItem.",
        "mods/alexs-caves.pw.toml": "Alex's Caves was only added by the delayed T.O Magic chain.",
        "mods/apothic-attributes.pw.toml": "Apothic Attributes was only added by the delayed T.O Magic chain.",
        "mods/placebo.pw.toml": "Placebo was only added by the delayed T.O Magic/Apothic chain.",
    }
    for relative, reason in delayed_t_magic_chain.items():
        if relative in active_relatives:
            errors.append(f"{relative} is active but delayed: {reason}")

    delayed_ctov_chain = {
        "mods/ct-overhaul-village.pw.toml": "CTOV is delayed after an in-world crash while placing ctov:medium/village_swamp.",
        "mods/lithostitched.pw.toml": "Lithostitched was only required by the delayed CTOV install.",
    }
    for relative, reason in delayed_ctov_chain.items():
        if relative in active_relatives:
            errors.append(f"{relative} is active but delayed: {reason}")

    delayed_batch_l_feedback = {
        "mods/first-person-model.pw.toml": "First-person Model is removed because Jayden did not like seeing the body in first person.",
    }
    for relative, reason in delayed_batch_l_feedback.items():
        if relative in active_relatives:
            errors.append(f"{relative} is active but delayed: {reason}")

    delayed_batch_m_feedback = {
        "mods/immersive-lanterns.pw.toml": "Toni's Immersive Lanterns is delayed because Packwiz resolved Accessories to a NeoForge-named 1.20.1 dependency file.",
        "mods/accessories.pw.toml": "Accessories is delayed because the selected file was accessories-neoforge-1.0.0-beta.48+1.20.1.jar in this Forge pack.",
        "mods/txnilib.pw.toml": "TxniLib was only required by the delayed Toni's Immersive Lanterns chain.",
    }
    for relative, reason in delayed_batch_m_feedback.items():
        if relative in active_relatives:
            errors.append(f"{relative} is active but delayed: {reason}")

    if (
        "mods/variants-and-ventures.pw.toml" in active_relatives
        and "mods/entity-model-features.pw.toml" in active_relatives
    ):
        errors.append(
            "Variants & Ventures 1.20.1 Forge is delayed because it crashes with Entity Model Features during "
            "murk_skull model registration on client startup."
        )

    lootbeams_config = ROOT / "config/lootbeams-client.toml"
    if "mods/loot-beams.pw.toml" in active_relatives:
        if not lootbeams_config.exists():
            errors.append("Loot Beams is installed but config/lootbeams-client.toml is missing.")
        else:
            lootbeams_text = read_text(lootbeams_config).lower()
            expected_lootbeam_settings = {
                "render_name_color": "false",
                "render_rarity_color": "true",
                "render_distance": "24.0",
                "all_items": "false",
                "only_rare": "true",
                "render_nametags": "true",
                "render_nametags_onlook": "true",
                "dmcloot_compat_rarity": "false",
                "combine_name_and_rarity": "true",
            }
            for key, expected in expected_lootbeam_settings.items():
                if not re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*{re.escape(expected)}\s*$", lootbeams_text):
                    errors.append(f"config/lootbeams-client.toml must set {key} = {expected}.")

    loot_journal_config = ROOT / "config/obscuria/loot_journal-client.toml"
    if "mods/loot-journal.pw.toml" in active_relatives:
        if not loot_journal_config.exists():
            errors.append("Loot Journal is installed but config/obscuria/loot_journal-client.toml is missing.")
        else:
            loot_journal_text = read_text(loot_journal_config).lower()
            expected_loot_journal_settings = {
                "enableLootJournal": "true",
                "showItemPickups": "true",
                "showOverflowPickups": "true",
                "trackItemPickups": "false",
                "enableRayGlow": "true",
            }
            for key, expected in expected_loot_journal_settings.items():
                if not re.search(rf"(?m)^\s*{re.escape(key).lower()}\s*=\s*{re.escape(expected)}\s*$", loot_journal_text):
                    errors.append(f"config/obscuria/loot_journal-client.toml must set {key} = {expected}.")

    healthbarplus_config = ROOT / "config/healthbarplus-client.toml"
    if "mods/health-bar-plus.pw.toml" in active_relatives:
        if not healthbarplus_config.exists():
            errors.append("Health Bar Plus is installed but config/healthbarplus-client.toml is missing.")
        else:
            healthbarplus_text = read_text(healthbarplus_config).lower()
            for key in ["samo_passive", "samo_neutral", "samo_hostile"]:
                if not re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*1\s*$", healthbarplus_text):
                    errors.append(f"config/healthbarplus-client.toml must set {key} = 1.")
            blacklist_match = re.search(r'(?m)^\s*blacklist\s*=\s*"([^"]*)"', healthbarplus_text)
            blacklist = blacklist_match.group(1) if blacklist_match else ""
            for boss_name in ["ender dragon", "wither"]:
                if boss_name not in blacklist:
                    errors.append(f"config/healthbarplus-client.toml blacklist must include {boss_name}.")

    travelers_titles_lang = ROOT / "resourcepacks/ascendant-realms-travelers-titles/assets/travelerstitles/lang/en_us.json"
    if travelers_titles_lang.exists():
        try:
            travelers_title_entries = read_json(travelers_titles_lang)
            for key in sorted(TRAVELERS_TITLES_REQUIRED_KEYS):
                if key not in travelers_title_entries:
                    errors.append(f"Ascendant Realms Traveler's Titles fallback is missing key: {key}")
                if f"{key}.color" not in travelers_title_entries:
                    errors.append(f"Ascendant Realms Traveler's Titles fallback is missing color key: {key}.color")
        except Exception as exc:
            errors.append(f"Ascendant Realms Traveler's Titles fallback JSON is invalid: {exc}")

    travelers_titles_config = ROOT / "config/travelerstitles-forge-1_20.toml"
    if travelers_titles_config.exists():
        travelers_titles_config_text = read_text(travelers_titles_config)
        for expected in [
            '"Enable Biome Titles" = true',
            '"Enable Dimension Titles" = true',
            '"Default Text Color" = "58b7d1"',
            '"Default Text Color" = "4fdfff"',
        ]:
            if expected not in travelers_titles_config_text:
                errors.append(f"config/travelerstitles-forge-1_20.toml is missing expected setting: {expected}")

    weather2_snow_config = ROOT / "config/Weather2/Snow.toml"
    if weather2_snow_config.exists():
        weather2_snow_text = read_text(weather2_snow_config)
        if "Snowstorm_Snow_Buildup_AllowOutsideColdBiomes = false" not in weather2_snow_text:
            errors.append(
                "config/Weather2/Snow.toml must disable snowstorm buildup outside cold biomes "
                "so warm Atlas regions do not get painted with snow."
            )

    snowrealmagic_config = ROOT / "config/snowrealmagic-common.yaml"
    if snowrealmagic_config.exists():
        snowrealmagic_text = read_text(snowrealmagic_config)
        for expected in [
            "snowAndIceMeltInWarmBiomes: true",
            "accumulationWinterOnly: true",
        ]:
            if expected not in snowrealmagic_text:
                errors.append(f"config/snowrealmagic-common.yaml is missing expected Atlas climate guard: {expected}")

    sereneseasons_config = ROOT / "config/sereneseasons/seasons.toml"
    if sereneseasons_config.exists():
        sereneseasons_text = read_text(sereneseasons_config)
        if "generate_snow_ice = false" not in sereneseasons_text:
            errors.append(
                "config/sereneseasons/seasons.toml must set generate_snow_ice = false; "
                "Atlas regional snow should come from cold biomes, not global winter conversion."
            )

    gear_items_by_id: dict[str, dict] = {}
    gear_registry_path = ROOT / "config/ascendant_index/gear_registry.json"
    if gear_registry_path.exists():
        try:
            gear_registry = read_json(gear_registry_path)
            counts = gear_registry.get("counts", {})
            for key, minimum in GEAR_INDEX_MIN_COUNTS.items():
                actual = int(counts.get(key, 0) or 0)
                if actual < minimum:
                    errors.append(
                        f"Gear registry count for {key} is {actual}; expected at least {minimum}."
                    )

            missing_rarity = []
            bad_ids = []
            missing_damage_status = []
            for collection_name in GEAR_INDEX_COLLECTIONS:
                for entry in gear_registry.get(collection_name, []):
                    item_id = str(entry.get("id", ""))
                    if item_id and item_id not in gear_items_by_id:
                        gear_items_by_id[item_id] = entry
                    if not entry.get("rarity") or not entry.get("rarity_color"):
                        missing_rarity.append(item_id or f"<missing id in {collection_name}>")
                    if GEAR_INDEX_BAD_ID_PATTERN.search(item_id):
                        bad_ids.append(item_id)
                    if collection_name == "weapons" and not entry.get("damage_status"):
                        missing_damage_status.append(item_id)

            if missing_rarity:
                sample = ", ".join(missing_rarity[:10])
                errors.append(f"Gear registry entries are missing rarity/color: {sample}")
            if bad_ids:
                sample = ", ".join(bad_ids[:10])
                errors.append(f"Gear registry contains non-player/item-model IDs: {sample}")
            if missing_damage_status:
                sample = ", ".join(missing_damage_status[:10])
                errors.append(f"Weapon registry entries are missing damage status: {sample}")
        except Exception as exc:
            errors.append(f"Gear registry JSON is invalid: {exc}")

    validate_ascendant_loot_economy(errors, warnings, gear_items_by_id)
    validate_ascendant_recipe_progression(errors, warnings, gear_items_by_id)
    validate_ascendant_magic_progression(errors, warnings, gear_items_by_id)
    validate_ascendant_balance(errors, warnings, gear_items_by_id)
    validate_ascendant_player_progression(errors, warnings)
    validate_ascendant_ranked_dungeons(errors, warnings)
    validate_ascendant_structure_tiering(errors, warnings)
    validate_ascendant_atmosphere(errors, warnings)
    validate_ascendant_travel_network(errors, warnings)
    validate_ascendant_npc_visual_identity(errors, warnings, gear_items_by_id)
    validate_ascendant_ui_clarity(errors, warnings)

    npc_loadouts_path = ROOT / "config/ascendant_guild/npc_loadouts.json"
    nameplates_path = ROOT / "config/ascendant_guild/nameplates.json"
    if npc_loadouts_path.exists():
        try:
            npc_loadouts = read_json(npc_loadouts_path)
            profile_ranks: dict[str, str] = {}
            for group_name, profile_id, profile in iter_loadout_profiles(npc_loadouts):
                rank = str(profile.get("rank", ""))
                profile_ranks[profile_id] = rank
                if not rank:
                    errors.append(f"{profile_id} in npc_loadouts.json is missing rank.")
                allowed_rarities = rank_allowed_rarities(npc_loadouts, rank)
                if not allowed_rarities:
                    errors.append(f"{profile_id} in npc_loadouts.json uses unknown rank {rank!r}.")

                visible_slots = {slot_name for slot_name, _ in iter_equipment_slots(profile)}
                if not (visible_slots & IMPORTANT_NPC_VISIBLE_SLOT_KEYS):
                    warnings.append(
                        f"{profile_id} in npc_loadouts.json has no visible mainhand/head/chest identity slot."
                    )

                for slot_name, slot_data in iter_equipment_slots(profile):
                    item_id = str(slot_data.get("item", ""))
                    if not item_id:
                        errors.append(f"{profile_id} {slot_name} in npc_loadouts.json is missing item.")
                        continue
                    gear_entry = gear_items_by_id.get(item_id)
                    if not gear_entry:
                        errors.append(f"{profile_id} {slot_name} item {item_id} is missing from gear_registry.json.")
                        continue
                    expected_rarity = str(gear_entry.get("rarity", ""))
                    declared_rarity = str(slot_data.get("rarity", ""))
                    if declared_rarity and declared_rarity != expected_rarity:
                        errors.append(
                            f"{profile_id} {slot_name} declares rarity {declared_rarity} "
                            f"but gear_registry.json has {expected_rarity} for {item_id}."
                        )
                    if (
                        allowed_rarities
                        and expected_rarity not in allowed_rarities
                        and not str(slot_data.get("override_reason", "")).strip()
                    ):
                        errors.append(
                            f"{profile_id} {slot_name} uses {expected_rarity} item {item_id}, "
                            f"outside allowed rank rarities {sorted(allowed_rarities)} without override_reason."
                        )

                if profile_id in RIVAL_PROFILE_IDS and not str(profile.get("drop_policy", "")).strip():
                    errors.append(f"Rival profile {profile_id} in npc_loadouts.json is missing drop_policy.")

            if nameplates_path.exists():
                nameplates = read_json(nameplates_path)
                palette = nameplates.get("palette", {})
                if isinstance(palette, dict):
                    for style_id, style in palette.items():
                        color = str(style.get("color", "")) if isinstance(style, dict) else ""
                        if not is_valid_hex_color(color):
                            errors.append(f"nameplates.json palette style {style_id} has invalid color {color!r}.")
                profiles = nameplates.get("profiles", {})
                if not isinstance(profiles, dict):
                    errors.append("nameplates.json profiles must be an object.")
                    profiles = {}
                for profile_id, rank in profile_ranks.items():
                    if profile_id not in profiles:
                        errors.append(f"Nameplate profile missing for NPC/loadout profile: {profile_id}.")
                        continue
                    plate_rank = str(profiles[profile_id].get("rank", ""))
                    if plate_rank != rank:
                        errors.append(
                            f"Nameplate rank mismatch for {profile_id}: {plate_rank!r} != loadout rank {rank!r}."
                        )
                for rival_id in RIVAL_PROFILE_IDS:
                    profile = profiles.get(rival_id, {})
                    for key in ("rank", "level", "profession", "style"):
                        if key not in profile or profile.get(key) in ("", None):
                            errors.append(f"Rival nameplate {rival_id} is missing {key}.")
            else:
                errors.append("npc_loadouts.json exists but config/ascendant_guild/nameplates.json is missing.")
        except Exception as exc:
            errors.append(f"NPC loadout/nameplate JSON validation failed: {exc}")

    settlements_path = ROOT / "config/ascendant_settlements/settlement_unification.json"
    if settlements_path.exists():
        try:
            settlements = read_json(settlements_path)
            active_changes = settlements.get("active_worldgen_changes", [])
            active_ids = {
                str(entry.get("id", ""))
                for entry in active_changes
                if isinstance(entry, dict)
            }
            unexpected_active_ids = active_ids - ASCENDANT_GUILD_STRUCTURE_IDS
            if unexpected_active_ids:
                errors.append(
                    "config/ascendant_settlements/settlement_unification.json enables unapproved live worldgen "
                    f"changes: {sorted(unexpected_active_ids)}"
                )
            if active_ids != ASCENDANT_GUILD_STRUCTURE_IDS:
                errors.append(
                    "config/ascendant_settlements/settlement_unification.json must list exactly the approved "
                    f"standalone Guild structures: {sorted(ASCENDANT_GUILD_STRUCTURE_IDS)}"
                )
            for entry in active_changes:
                if isinstance(entry, dict) and entry.get("type") != "standalone_jigsaw_structure":
                    errors.append(
                        "config/ascendant_settlements/settlement_unification.json may only enable standalone_jigsaw_structure "
                        f"pilot entries right now: {entry.get('id')}"
                    )
            ownership = settlements.get("ownership", [])
            if not isinstance(ownership, list) or len(ownership) < 8:
                errors.append("settlement_unification.json should list the major village/worldgen ownership layers.")
            threshold = settlements.get("custom_mod_threshold", {})
            if not isinstance(threshold, dict) or "decision" not in threshold:
                errors.append("settlement_unification.json must record the custom mod threshold decision.")
        except Exception as exc:
            errors.append(f"Ascendant Settlements JSON is invalid: {exc}")

    for filename in ASCENDANT_CORE_POLICY_FILES:
        policy_path = ROOT / "config/ascendant_core" / filename
        if not policy_path.exists():
            errors.append(f"Ascendant Core policy file is missing: {policy_path.relative_to(ROOT)}")
            continue
        try:
            policy = read_json(policy_path)
            if not isinstance(policy, dict) or policy.get("version") != 1:
                errors.append(f"{policy_path.relative_to(ROOT)} must be a version 1 JSON object.")
        except Exception as exc:
            errors.append(f"{policy_path.relative_to(ROOT)} is invalid JSON: {exc}")

    for filename in ASCENDANT_ATLAS_POLICY_FILES:
        policy_path = ROOT / "config/ascendant_atlas" / filename
        if not policy_path.exists():
            errors.append(f"Ascendant Atlas policy file is missing: {policy_path.relative_to(ROOT)}")
            continue
        try:
            policy = read_json(policy_path)
            if not isinstance(policy, dict) or policy.get("version") != 1:
                errors.append(f"{policy_path.relative_to(ROOT)} must be a version 1 JSON object.")
        except Exception as exc:
            errors.append(f"{policy_path.relative_to(ROOT)} is invalid JSON: {exc}")

    atlas_manifest_path = ROOT / "config/ascendant_atlas/atlas_manifest.json"
    if atlas_manifest_path.exists():
        try:
            manifest = read_json(atlas_manifest_path)
            live_ids = set(str(value) for value in manifest.get("live_structure_ids", []))
            debug_ids = set(str(value) for value in manifest.get("debug_structure_ids", []))
            if live_ids:
                errors.append(
                    "config/ascendant_atlas/atlas_manifest.json live_structure_ids must be empty; "
                    "Atlas waymarks are debug-only and should not generate naturally."
                )
            if debug_ids != ASCENDANT_ATLAS_DEBUG_STRUCTURE_IDS:
                errors.append(
                    "config/ascendant_atlas/atlas_manifest.json debug_structure_ids must exactly match "
                    f"{sorted(ASCENDANT_ATLAS_DEBUG_STRUCTURE_IDS)}."
                )
            if int(manifest.get("biomes_indexed", 0)) <= 0:
                errors.append("config/ascendant_atlas/atlas_manifest.json must record indexed biomes.")
            if int(manifest.get("structures_indexed", 0)) <= 0:
                errors.append("config/ascendant_atlas/atlas_manifest.json must record indexed structures.")
            runtime_features = manifest.get("live_runtime_features", [])
            if not isinstance(runtime_features, list) or "60000 block world border centered at 0,0" not in runtime_features:
                errors.append("Atlas manifest must record the live finite-world runtime features.")
            future_note = str(manifest.get("future_custom_module", "")).lower()
            if "helper module" not in future_note or "road/bridge" not in future_note:
                errors.append("Atlas manifest must record the helper-module boundary for road/bridge and hard biome-source control.")
            if atlas_worldgen_override_enabled:
                if manifest.get("helper_mod") != "ascendant_atlas_regions":
                    errors.append("Atlas manifest must record helper_mod ascendant_atlas_regions.")
                if manifest.get("biome_source_type") != "ascendant_atlas_regions:regional_multi_noise":
                    errors.append("Atlas manifest must record the active regional_multi_noise biome source.")
                if manifest.get("worldgen_region_manifest") != "config/ascendant_atlas/worldgen_regions.json":
                    errors.append("Atlas manifest must point at config/ascendant_atlas/worldgen_regions.json.")
            else:
                if manifest.get("worldgen_override_enabled") is not False:
                    errors.append(
                        "Atlas manifest must record worldgen_override_enabled=false while random generation is restored."
                    )
                if "random" not in str(manifest.get("status", "")).lower() and "disabled" not in str(manifest.get("status", "")).lower():
                    warnings.append(
                        "Atlas manifest should clearly say the coordinate-aware worldgen override is disabled."
                    )
        except Exception as exc:
            errors.append(f"Ascendant Atlas manifest is invalid: {exc}")

    atlas_climate_sectors_path = ROOT / "config/ascendant_atlas/climate_sectors.json"
    if atlas_climate_sectors_path.exists():
        try:
            climate_sectors = read_json(atlas_climate_sectors_path)
            for sector in climate_sectors.get("sectors", []):
                if isinstance(sector, dict) and sector.get("id") == "center":
                    center_keywords = {str(keyword) for keyword in sector.get("biome_keywords", [])}
                    if "river" in center_keywords:
                        errors.append("Atlas center climate-sector keywords must not include river after the Hearthlands seam fix.")
        except Exception as exc:
            errors.append(f"Ascendant Atlas climate sectors JSON is invalid: {exc}")

    atlas_worldgen_manifest_path = ROOT / "config/ascendant_atlas/worldgen_regions.json"
    if atlas_worldgen_manifest_path.exists():
        try:
            worldgen_manifest = read_json(atlas_worldgen_manifest_path)
            if worldgen_manifest.get("helper_mod_id") != "ascendant_atlas_regions":
                errors.append("config/ascendant_atlas/worldgen_regions.json must record ascendant_atlas_regions.")
            if worldgen_manifest.get("biome_source_type") != "ascendant_atlas_regions:regional_multi_noise":
                errors.append("config/ascendant_atlas/worldgen_regions.json must record regional_multi_noise.")
            if worldgen_manifest.get("terrain_settings") != "minecraft:overworld":
                errors.append("Atlas worldgen must keep terrain_settings as minecraft:overworld so Tectonic terrain survives.")
            if int(worldgen_manifest.get("world_radius_blocks", 0)) != 12000:
                errors.append("Atlas worldgen manifest must use a 12000 block climate-gradient radius to prevent near-spawn climate snapping.")
            if int(worldgen_manifest.get("outer_radius_blocks", 0)) != 50000:
                errors.append("Atlas worldgen manifest must delay the shared outer biome table until 50000 blocks for the square-border visual buffer.")
            if int(worldgen_manifest.get("center_radius_blocks", 0)) != 500:
                errors.append("Atlas worldgen manifest must keep the 500 block Hearthlands center radius so the north gradient starts before it visibly snaps.")
            regions = worldgen_manifest.get("regions", {})
            expected_region_counts = {
                "center": 80,
                "north": 80,
                "south": 80,
                "east": 60,
                "west": 60,
                "north_east": 120,
                "north_west": 120,
                "south_east": 120,
                "south_west": 120,
                "outer": 160,
            }
            for region_name, minimum in expected_region_counts.items():
                region = regions.get(region_name)
                if not isinstance(region, dict):
                    errors.append(f"Atlas worldgen manifest is missing region {region_name}.")
                    continue
                if int(region.get("entry_count", 0)) < minimum:
                    errors.append(
                        f"Atlas worldgen region {region_name} has too few climate entries: "
                        f"{region.get('entry_count')}"
                    )
                if int(region.get("unique_biome_count", 0)) < 10:
                    errors.append(f"Atlas worldgen region {region_name} has too few unique biomes.")
            center_biomes = regions.get("center", {}).get("biomes", [])
            for forbidden_center_biome in ["terralith:alpha_islands", "minecraft:grove", "minecraft:river"]:
                if forbidden_center_biome in center_biomes:
                    errors.append(f"Atlas center biome table must not include {forbidden_center_biome}.")
            watery_or_cold_center_biomes = [
                biome
                for biome in center_biomes
                if any(token in str(biome) for token in ["ocean", "river", "island", "beach", "swamp", "snow", "frozen", "ice_", "cold"])
            ]
            if watery_or_cold_center_biomes:
                errors.append(
                    "Atlas center biome table must stay mild and mostly dry, found: "
                    f"{watery_or_cold_center_biomes}"
                )
            if "minecraft:snowy_plains" not in regions.get("north", {}).get("biomes", []):
                errors.append("Atlas north biome table must include snowy plains.")
            if "minecraft:frozen_ocean" not in regions.get("north", {}).get("biomes", []):
                errors.append("Atlas north biome table must include frozen ocean for the cold-to-frozen gradient.")
            for deep_north_ocean in ["minecraft:deep_cold_ocean", "minecraft:deep_frozen_ocean"]:
                if deep_north_ocean in regions.get("north", {}).get("biomes", []):
                    errors.append(f"Atlas north biome table must not include {deep_north_ocean}; it creates long deep-ocean runs.")
            for direct_north_water_or_peak in [
                "minecraft:cold_ocean",
                "minecraft:snowy_beach",
                "minecraft:frozen_peaks",
                "minecraft:grove",
                "minecraft:snowy_slopes",
                "terralith:frozen_cliffs",
                "terralith:ice_marsh",
            ]:
                if direct_north_water_or_peak in regions.get("north", {}).get("biomes", []):
                    errors.append(
                        f"Atlas north biome table must not include {direct_north_water_or_peak}; "
                        "direct north should be land-first tundra/taiga/ice fields, not ocean/steep alpine first."
                    )
            if "minecraft:desert" not in regions.get("south", {}).get("biomes", []):
                errors.append("Atlas south biome table must include desert.")
            if "minecraft:warm_ocean" not in regions.get("south", {}).get("biomes", []):
                errors.append("Atlas south biome table must include warm ocean for the warm-coast-to-desert gradient.")
            if "minecraft:deep_lukewarm_ocean" in regions.get("south", {}).get("biomes", []):
                errors.append("Atlas south biome table must not include deep lukewarm ocean; it creates long deep-ocean runs.")
            for inner_south_seam_biome in ["minecraft:lukewarm_ocean", "terralith:gravel_desert"]:
                if inner_south_seam_biome in regions.get("south", {}).get("biomes", []):
                    errors.append(
                        f"Atlas south biome table must not include {inner_south_seam_biome}; "
                        "it makes the inner south boundary fragment into ocean/gravel seams."
                    )
            if "minecraft:jungle" not in regions.get("east", {}).get("biomes", []):
                errors.append("Atlas east biome table must include jungle.")
            if "terralith:gravel_beach" in regions.get("east", {}).get("biomes", []):
                errors.append("Atlas east biome table must not include terralith:gravel_beach; it fragments the Hearthlands seam.")
            forbidden_south_east_oceans = {
                "minecraft:ocean",
                "minecraft:deep_ocean",
                "minecraft:warm_ocean",
                "minecraft:lukewarm_ocean",
                "minecraft:deep_lukewarm_ocean",
            }
            leaked_south_east_oceans = sorted(set(regions.get("south_east", {}).get("biomes", [])) & forbidden_south_east_oceans)
            if leaked_south_east_oceans:
                errors.append(
                    "Atlas south_east biome table must stay land-first and must not include ocean biome IDs after "
                    f"the southeast transition hotfix: {leaked_south_east_oceans}"
                )
            if "minecraft:stony_peaks" not in regions.get("west", {}).get("biomes", []):
                errors.append("Atlas west biome table must include non-snow highland peaks.")
            snow_blocked_outside_cold = [
                "minecraft:jagged_peaks",
                "terralith:alpine_grove",
                "terralith:emerald_peaks",
                "terralith:scarlet_mountains",
            ]
            for region_name in ["west", "south_west"]:
                present_snow_biomes = [
                    biome
                    for biome in regions.get(region_name, {}).get("biomes", [])
                    if biome in snow_blocked_outside_cold
                ]
                if present_snow_biomes:
                    errors.append(
                        f"Atlas {region_name} biome table must block snow-allowed highlands outside intended cold regions, "
                        f"found: {present_snow_biomes}"
                    )
            for region_name in ["south", "south_west"]:
                cold_biomes = [
                    biome
                    for biome in regions.get(region_name, {}).get("biomes", [])
                    if any(token in str(biome) for token in ["snow", "frozen", "ice_", "cold"])
                ]
                if cold_biomes:
                    errors.append(f"Atlas {region_name} biome table must stay warm/arid, found cold biomes: {cold_biomes}")
        except Exception as exc:
            errors.append(f"Ascendant Atlas worldgen region manifest is invalid: {exc}")

    atlas_content_audit_path = ROOT / "docs/generated/worldgen_content_audit.json"
    if atlas_content_audit_path.exists():
        try:
            content_audit = read_json(atlas_content_audit_path)
            counts = content_audit.get("counts", {})
            if int(counts.get("biomes", 0) or 0) < 500:
                errors.append("Worldgen content audit must index active biome JSON from installed jars/datapacks.")
            if int(counts.get("structures", 0) or 0) < 400:
                errors.append("Worldgen content audit must index active structure JSON from installed jars/datapacks.")
            if int(counts.get("templates", 0) or 0) < 1000:
                errors.append("Worldgen content audit must index structure template NBT palettes.")
            north_review = content_audit.get("region_review", {}).get("north", {})
            if float(north_review.get("water_noise_entry_share", 1.0) or 1.0) > 0.02:
                errors.append(
                    "Worldgen content audit says Atlas north has too much water/sea noise; "
                    f"share={north_review.get('water_noise_entry_share')}"
                )
            north_flags = north_review.get("flagged_biomes", {})
            allowed_north_flags = {"minecraft:frozen_ocean"}
            unexpected_flags = sorted(set(north_flags) - allowed_north_flags)
            if unexpected_flags:
                errors.append(
                    "Worldgen content audit found unexpected direct-north biome flags: "
                    f"{unexpected_flags}"
                )
        except Exception as exc:
            errors.append(f"Worldgen content audit JSON is invalid: {exc}")

    atlas_dimension_override_paths = [
        ROOT / "config/openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json",
        ROOT / "openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json",
    ]
    atlas_continents_override_paths = [
        ROOT / "config/openloader/data/ascendant_realms_atlas/data/minecraft/worldgen/density_function/overworld/continents.json",
        ROOT / "openloader/data/ascendant_realms_atlas/data/minecraft/worldgen/density_function/overworld/continents.json",
    ]
    if not atlas_worldgen_override_enabled:
        for atlas_influence_path in atlas_dimension_override_paths + atlas_continents_override_paths:
            if atlas_influence_path.exists():
                errors.append(
                    f"{atlas_influence_path.relative_to(ROOT)} must be absent while "
                    "config/ascendant_atlas/worldgen_override_policy.json disables Atlas worldgen influence."
                )

    for atlas_dimension_path in atlas_dimension_override_paths:
        if atlas_dimension_path.exists():
            try:
                dimension = read_json(atlas_dimension_path)
                generator = dimension.get("generator", {})
                biome_source = generator.get("biome_source", {})
                if generator.get("type") != "minecraft:noise":
                    errors.append(f"{atlas_dimension_path.relative_to(ROOT)} must keep minecraft:noise generator.")
                if generator.get("settings") != "minecraft:overworld":
                    errors.append(f"{atlas_dimension_path.relative_to(ROOT)} must keep settings minecraft:overworld.")
                if biome_source.get("type") != "ascendant_atlas_regions:regional_multi_noise":
                    errors.append(f"{atlas_dimension_path.relative_to(ROOT)} must use regional_multi_noise biome source.")
                if int(biome_source.get("world_radius_blocks", 0)) != 12000:
                    errors.append(f"{atlas_dimension_path.relative_to(ROOT)} must use world_radius_blocks 12000 for smoother climate gradients.")
                if int(biome_source.get("outer_radius_blocks", 0)) != 50000:
                    errors.append(f"{atlas_dimension_path.relative_to(ROOT)} must keep outer_radius_blocks 50000 for the square-border visual buffer.")
                if int(biome_source.get("center_radius_blocks", 0)) != 500:
                    errors.append(f"{atlas_dimension_path.relative_to(ROOT)} must keep center_radius_blocks 500.")
                north_biomes = {entry.get("biome") for entry in biome_source.get("north", []) if isinstance(entry, dict)}
                south_biomes = {entry.get("biome") for entry in biome_source.get("south", []) if isinstance(entry, dict)}
                east_biomes = {entry.get("biome") for entry in biome_source.get("east", []) if isinstance(entry, dict)}
                south_east_biomes = {entry.get("biome") for entry in biome_source.get("south_east", []) if isinstance(entry, dict)}
                forbidden_south_east_oceans = {
                    "minecraft:ocean",
                    "minecraft:deep_ocean",
                    "minecraft:warm_ocean",
                    "minecraft:lukewarm_ocean",
                    "minecraft:deep_lukewarm_ocean",
                }
                leaked_south_east_oceans = sorted(south_east_biomes & forbidden_south_east_oceans)
                if leaked_south_east_oceans:
                    errors.append(
                        f"{atlas_dimension_path.relative_to(ROOT)} south_east pool must stay land-first and must not "
                        f"include ocean biome IDs: {leaked_south_east_oceans}"
                    )
                if "minecraft:frozen_ocean" not in north_biomes:
                    errors.append(f"{atlas_dimension_path.relative_to(ROOT)} north region must include frozen ocean.")
                for deep_north_ocean in ["minecraft:deep_cold_ocean", "minecraft:deep_frozen_ocean"]:
                    if deep_north_ocean in north_biomes:
                        errors.append(
                            f"{atlas_dimension_path.relative_to(ROOT)} north region must not include "
                            f"{deep_north_ocean}; it creates long deep-ocean runs."
                        )
                for direct_north_water_or_peak in [
                    "minecraft:cold_ocean",
                    "minecraft:snowy_beach",
                    "minecraft:frozen_peaks",
                    "minecraft:grove",
                    "minecraft:snowy_slopes",
                    "terralith:frozen_cliffs",
                    "terralith:ice_marsh",
                ]:
                    if direct_north_water_or_peak in north_biomes:
                        errors.append(
                            f"{atlas_dimension_path.relative_to(ROOT)} north region must not include "
                            f"{direct_north_water_or_peak}; direct north should be land-first tundra/taiga/ice fields."
                        )
                if "minecraft:warm_ocean" not in south_biomes:
                    errors.append(f"{atlas_dimension_path.relative_to(ROOT)} south region must include warm ocean.")
                if "minecraft:deep_lukewarm_ocean" in south_biomes:
                    errors.append(
                        f"{atlas_dimension_path.relative_to(ROOT)} south region must not include deep lukewarm ocean; "
                        "it creates long deep-ocean runs."
                    )
                for inner_south_seam_biome in ["minecraft:lukewarm_ocean", "terralith:gravel_desert"]:
                    if inner_south_seam_biome in south_biomes:
                        errors.append(
                            f"{atlas_dimension_path.relative_to(ROOT)} south region must not include "
                            f"{inner_south_seam_biome}; it fragments the inner south boundary."
                        )
                if "terralith:gravel_beach" in east_biomes:
                    errors.append(
                        f"{atlas_dimension_path.relative_to(ROOT)} east region must not include terralith:gravel_beach; "
                        "it fragments the Hearthlands seam."
                    )
                snow_blocked_outside_cold = {
                    "minecraft:jagged_peaks",
                    "terralith:alpine_grove",
                    "terralith:emerald_peaks",
                    "terralith:scarlet_mountains",
                }
                west_biomes = {entry.get("biome") for entry in biome_source.get("west", []) if isinstance(entry, dict)}
                south_west_biomes = {entry.get("biome") for entry in biome_source.get("south_west", []) if isinstance(entry, dict)}
                for region_name, region_biomes in {"west": west_biomes, "south_west": south_west_biomes}.items():
                    present_snow_biomes = sorted(region_biomes & snow_blocked_outside_cold)
                    if present_snow_biomes:
                        errors.append(
                            f"{atlas_dimension_path.relative_to(ROOT)} region {region_name} must block "
                            f"snow-allowed highlands outside intended cold regions: {present_snow_biomes}"
                        )
                center_biomes = {entry.get("biome") for entry in biome_source.get("center", []) if isinstance(entry, dict)}
                for forbidden_center_biome in ["terralith:alpha_islands", "minecraft:grove", "minecraft:river"]:
                    if forbidden_center_biome in center_biomes:
                        errors.append(
                            f"{atlas_dimension_path.relative_to(ROOT)} center region must not include "
                            f"{forbidden_center_biome}."
                        )
                watery_or_cold_center_biomes = [
                    biome
                    for biome in center_biomes
                    if any(token in str(biome) for token in ["ocean", "river", "island", "beach", "swamp", "snow", "frozen", "ice_", "cold"])
                ]
                if watery_or_cold_center_biomes:
                    errors.append(
                        f"{atlas_dimension_path.relative_to(ROOT)} center region must stay mild and mostly dry, "
                        f"found {sorted(watery_or_cold_center_biomes)}."
                    )
                for region_name, minimum in {
                    "center": 80,
                    "north": 80,
                    "south": 80,
                    "east": 60,
                    "west": 60,
                    "north_east": 120,
                    "north_west": 120,
                    "south_east": 120,
                    "south_west": 120,
                    "outer": 160,
                }.items():
                    entries = biome_source.get(region_name)
                    if not isinstance(entries, list) or len(entries) < minimum:
                        errors.append(
                            f"{atlas_dimension_path.relative_to(ROOT)} region {region_name} "
                            f"has too few biome entries."
                        )
                    if region_name in ["south", "south_west"] and isinstance(entries, list):
                        cold_entries = [
                            entry.get("biome")
                            for entry in entries
                            if any(token in str(entry.get("biome")) for token in ["snow", "frozen", "ice_", "cold"])
                        ]
                        if cold_entries:
                            errors.append(
                                f"{atlas_dimension_path.relative_to(ROOT)} region {region_name} "
                                f"must stay warm/arid, found cold entries: {sorted(set(cold_entries))}"
                            )
            except Exception as exc:
                errors.append(f"{atlas_dimension_path.relative_to(ROOT)} is invalid JSON: {exc}")

    for atlas_continents_path in atlas_continents_override_paths:
        if atlas_continents_path.exists():
            try:
                continents = read_json(atlas_continents_path)
                if continents.get("type") != "minecraft:add":
                    errors.append(f"{atlas_continents_path.relative_to(ROOT)} must add Atlas land bias to vanilla continentalness.")
                argument2 = continents.get("argument2", {})
                if not isinstance(argument2, dict) or argument2.get("type") != "ascendant_atlas_regions:atlas_land_bias":
                    errors.append(f"{atlas_continents_path.relative_to(ROOT)} must use ascendant_atlas_regions:atlas_land_bias.")
                if int(argument2.get("center_radius_blocks", 0) or 0) != 500:
                    errors.append(f"{atlas_continents_path.relative_to(ROOT)} must use center_radius_blocks 500.")
                if int(argument2.get("outer_radius_blocks", 0) or 0) != 50000:
                    errors.append(f"{atlas_continents_path.relative_to(ROOT)} must use outer_radius_blocks 50000.")
                if float(argument2.get("south_outer_bias", 0.0) or 0.0) <= 0.0 or float(argument2.get("west_outer_bias", 0.0) or 0.0) <= 0.0:
                    errors.append(f"{atlas_continents_path.relative_to(ROOT)} must bias south and west continentalness above 0.")
            except Exception as exc:
                errors.append(f"{atlas_continents_path.relative_to(ROOT)} is invalid JSON: {exc}")
        elif atlas_worldgen_override_enabled:
            errors.append(f"{atlas_continents_path.relative_to(ROOT)} is required for natural Atlas land-water coherence.")

    atlas_hydrology_paths = [
        "config/ascendant_atlas/biome_hydrology_registry.json",
        "config/ascendant_atlas/hydrology_policy.json",
        "config/ascendant_atlas/coastal_policy.json",
        "config/ascendant_atlas/region_gradient_policy.json",
        "config/ascendant_atlas/transition_adjacency.json",
        "config/ascendant_atlas/domain_warp_policy.json",
        "config/ascendant_atlas/reports/hydrology_grid_latest.json",
        "config/ascendant_atlas/reports/region_gradient_grid_latest.json",
        "config/ascendant_atlas/reports/transition_transects_latest.json",
        "config/ascendant_atlas/reports/invalid_ocean_selections_latest.json",
    ]
    for relative_path in atlas_hydrology_paths:
        path = ROOT / relative_path
        if not path.exists():
            warnings.append(f"{relative_path} is missing; Atlas hydrology/gradient validation is incomplete.")
            continue
        try:
            data = read_json(path)
            if relative_path.endswith("biome_hydrology_registry.json"):
                if data.get("classification_rule") and "name" in str(data.get("classification_rule")).lower() and "not accepted" not in str(data.get("classification_rule")).lower():
                    warnings.append("biome_hydrology_registry classification rule may allow name-based classification.")
                for row in data.get("biomes", []):
                    if isinstance(row, dict) and row.get("classification_method") == "name_token":
                        warnings.append(f"Hydrology registry uses name-token classification for {row.get('biome_id')}.")
            if relative_path.endswith("region_gradient_policy.json") and data.get("hard_axis_boundaries") is not False:
                warnings.append("region_gradient_policy.json must explicitly disable hard axis boundaries.")
            if relative_path.endswith("invalid_ocean_selections_latest.json") and isinstance(data, dict):
                invalid = int(data.get("invalid_ocean_selections", 0) or 0)
                if invalid > 0:
                    warnings.append(f"Atlas invalid ocean selection report currently has {invalid} invalid ocean selections.")
        except Exception as exc:
            errors.append(f"{relative_path} is malformed JSON: {exc}")

    helper_source = ROOT / "local-mods/ascendant-atlas-regions/src/main/java/com/robbinstech/ascendant_atlas_regions/RegionalMultiNoiseBiomeSource.java"
    helper_entrypoint = ROOT / "local-mods/ascendant-atlas-regions/src/main/java/com/robbinstech/ascendant_atlas_regions/AscendantAtlasRegions.java"
    helper_land_bias = ROOT / "local-mods/ascendant-atlas-regions/src/main/java/com/robbinstech/ascendant_atlas_regions/AtlasLandBiasDensityFunction.java"
    helper_build = ROOT / "scripts/build-ascendant-atlas-regions.ps1"
    helper_jar = ROOT / "mods/ascendant-atlas-regions-0.1.0.jar"
    if helper_source.exists():
        helper_source_text = read_text(helper_source)
        for expected in [
            "RegionalMultiNoiseBiomeSource",
            "worldRadiusBlocks",
            "outerRadiusBlocks",
            "centerRadiusBlocks",
            "axisDominanceRatio",
            "northEast",
            "southWest",
            "selectRegion",
            "adjustTargetForAtlasGradient",
            "biasNorth",
            "biasSouth",
            "biasCenterNorthTransition",
            "m_203407_",
            "describeBlock",
            "atlasPoolBiomeIds",
            "explainBiomeDecision",
            "classifyHydrology",
            "regionWeightsForBlock",
            "invalidOceanSelection",
        ]:
            if expected not in helper_source_text:
                errors.append(f"Atlas helper source is missing {expected}.")
        if "absZ > absX *" in helper_source_text or "absX > absZ *" in helper_source_text:
            warnings.append("Atlas biome-source helper still contains hard axis dominance comparisons; region transitions should use continuous weights.")
        if "contains(\"ocean\")" in helper_source_text or "contains(\"river\")" in helper_source_text:
            warnings.append("Atlas biome-source helper appears to classify water by name tokens; use exact IDs and climate/hydrology data instead.")
    if helper_land_bias.exists():
        helper_land_bias_text = read_text(helper_land_bias)
        for expected in [
            "AtlasLandBiasDensityFunction",
            "DensityFunction",
            "atlas_land_bias",
            "southOuterBias",
            "westOuterBias",
            "southWestOuterBias",
            "directionWeights",
            "warpedCoordinates",
        ]:
            if expected not in helper_land_bias_text:
                errors.append(f"Atlas land-bias density function source is missing {expected}.")
        if "absZ > absX *" in helper_land_bias_text or "absX > absZ *" in helper_land_bias_text:
            warnings.append("Atlas land-bias density function still contains hard axis dominance comparisons; terrain bias should use continuous weights.")
        if "chunk.m_6978_" in helper_land_bias_text or "BlockState" in helper_land_bias_text:
            errors.append("Atlas land-bias density function must not mutate blocks; it should only return a density bias.")
    else:
        errors.append("Atlas helper is missing AtlasLandBiasDensityFunction.java.")
    if helper_entrypoint.exists():
        helper_entrypoint_text = read_text(helper_entrypoint)
        for expected in [
            "DeferredRegister",
            "FMLJavaModLoadingContext",
            'new ResourceLocation("minecraft", "worldgen/biome_source")',
            "BIOME_SOURCES.register",
            "DENSITY_FUNCTIONS.register",
            "atlas_land_bias",
            "MinecraftForge.EVENT_BUS.register",
            "AtlasCommands.class",
            "regional_multi_noise",
        ]:
            if expected not in helper_entrypoint_text:
                errors.append(f"Atlas helper entrypoint must use deferred biome-source registration: missing {expected}.")
    helper_commands = ROOT / "local-mods/ascendant-atlas-regions/src/main/java/com/robbinstech/ascendant_atlas_regions/AtlasCommands.java"
    if helper_commands.exists():
        helper_commands_text = read_text(helper_commands)
        for expected in [
            '"ascatlas"',
            '"here"',
            '"region"',
            '"sample_grid"',
            '"sample_surface_grid"',
            '"terrain_probe"',
            '"terrain_probe_here"',
            '"sample_land_water"',
            '"dump_land_water_policy"',
            '"dump_terrain_noise_policy"',
            '"dump_gradient_policy"',
            '"dump_hydrology_registry"',
            '"hydrology_here"',
            '"biome_decision_here"',
            '"region_weights_here"',
            '"sample_transect"',
            '"dump_biome_pools"',
            "sample_grid_source_latest.json",
            "sample_grid_surface_latest.json",
            "terrain_noise_probe_latest.json",
            "land_water_coherence_latest.json",
            "terrain_wrapper_test_latest.json",
            "hydrology_grid_latest.json",
            "region_gradient_grid_latest.json",
            "transition_transects_latest.json",
            "invalid_ocean_selections_latest.json",
            "biome_pools_resolved.json",
        ]:
            if expected not in helper_commands_text:
                errors.append(f"Atlas helper commands source is missing {expected}.")
        if "contains(\"ocean\")" in helper_commands_text or "contains(\"beach\")" in helper_commands_text:
            warnings.append("Atlas command validation still contains name-token ocean/coast checks; prefer hydrology class evidence.")
    else:
        errors.append("Atlas helper commands source is missing AtlasCommands.java.")
        for forbidden in ["BuiltInRegistries.f_256737_", "Registry.m_122965_"]:
            if forbidden in helper_entrypoint_text:
                errors.append(
                    "Atlas helper entrypoint must not directly mutate the built-in biome-source registry; "
                    f"found {forbidden}."
                )
    if helper_build.exists():
        helper_build_text = read_text(helper_build)
        for expected in ["javac", "mods\\ascendant-atlas-regions-0.1.0.jar", "Test-ZipJar"]:
            if expected not in helper_build_text:
                errors.append(f"Atlas helper build script is missing {expected}.")
    if helper_jar.exists():
        try:
            with zipfile.ZipFile(helper_jar) as jar:
                names = set(jar.namelist())
            for expected in [
                "META-INF/mods.toml",
                "com/robbinstech/ascendant_atlas_regions/AscendantAtlasRegions.class",
                "com/robbinstech/ascendant_atlas_regions/RegionalMultiNoiseBiomeSource.class",
                "com/robbinstech/ascendant_atlas_regions/AtlasCommands.class",
                "com/robbinstech/ascendant_atlas_regions/AtlasTerrainCorrection.class",
            ]:
                if expected not in names:
                    errors.append(f"Atlas helper jar is missing {expected}.")
        except Exception as exc:
            errors.append(f"Atlas helper jar could not be read: {exc}")
        active_helper_jar = ACTIVE_CURSEFORGE_INSTANCE / "mods" / "ascendant-atlas-regions-0.1.0.jar"
        if active_helper_jar.exists():
            try:
                repo_hash = file_sha256(helper_jar)
                active_hash = file_sha256(active_helper_jar)
                if repo_hash != active_hash:
                    warnings.append(
                        "Atlas helper jar differs between repo mods/ and active Ascendant Realms (2) instance; "
                        "Minecraft must be closed and the rebuilt helper jar synced before in-game validation."
                    )
            except Exception as exc:
                warnings.append(f"Could not compare active Atlas helper jar hash: {exc}")
        else:
            warnings.append(
                "Active Ascendant Realms (2) instance is missing ascendant-atlas-regions-0.1.0.jar; "
                "sync before Atlas in-game validation."
            )

    nametags_build = ROOT / "scripts/build-ascendant-nametags.ps1"
    nametags_jar = ROOT / "mods/ascendant-nametags-0.1.0.jar"
    if nametags_build.exists():
        nametags_build_text = read_text(nametags_build)
        for expected in ["javac", "mods\\ascendant-nametags-0.1.0.jar", "Test-ZipJar"]:
            if expected not in nametags_build_text:
                errors.append(f"Ascendant Nametags build script is missing {expected}.")
    if nametags_jar.exists():
        try:
            with zipfile.ZipFile(nametags_jar) as jar:
                names = set(jar.namelist())
            for expected in [
                "META-INF/mods.toml",
                "com/robbinstech/ascendant_nametags/AscendantNametags.class",
                "com/robbinstech/ascendant_nametags/AscendantNametagsClient.class",
            ]:
                if expected not in names:
                    errors.append(f"Ascendant Nametags jar is missing {expected}.")
        except Exception as exc:
            errors.append(f"Ascendant Nametags jar could not be read: {exc}")
        active_nametags_jar = ACTIVE_CURSEFORGE_INSTANCE / "mods" / "ascendant-nametags-0.1.0.jar"
        if active_nametags_jar.exists():
            try:
                repo_hash = file_sha256(nametags_jar)
                active_hash = file_sha256(active_nametags_jar)
                if repo_hash != active_hash:
                    warnings.append(
                        "Ascendant Nametags jar differs between repo mods/ and active Ascendant Realms (2) instance; "
                        "Minecraft must be closed and the rebuilt nametag jar synced before in-game validation."
                    )
            except Exception as exc:
                warnings.append(f"Could not compare active Ascendant Nametags jar hash: {exc}")
        else:
            warnings.append(
                "Active Ascendant Realms (2) instance is missing ascendant-nametags-0.1.0.jar; "
                "sync before nameplate in-game validation."
            )

    packwizignore_path = ROOT / ".packwizignore"
    if packwizignore_path.exists():
        packwizignore_text = read_text(packwizignore_path)
        if "!mods/ascendant-atlas-regions-0.1.0.jar" not in packwizignore_text:
            errors.append(".packwizignore must allow the local Atlas helper jar into client exports.")
        if "!mods/ascendant-nametags-0.1.0.jar" not in packwizignore_text:
            errors.append(".packwizignore must allow the local Ascendant Nametags helper jar into client exports.")
        if "local-mods/" not in packwizignore_text:
            errors.append(".packwizignore must keep local-mods source out of client exports.")

    atlas_reports: dict[str, object] = {}
    for report_name in ASCENDANT_ATLAS_REPORT_JSON_FILES:
        report_path = ROOT / report_name
        if not report_path.exists():
            continue
        try:
            report = read_json(report_path)
            if not isinstance(report, dict):
                errors.append(f"Ascendant Atlas report JSON must be an object: {report_name}")
                continue
            atlas_reports[report_name] = report
        except Exception as exc:
            errors.append(f"Ascendant Atlas report JSON is invalid: {report_name}: {exc}")

    source_sample_grid = atlas_reports.get("config/ascendant_atlas/reports/sample_grid_source_latest.json")
    if source_sample_grid is None:
        source_sample_grid = atlas_reports.get("config/ascendant_atlas/reports/sample_grid_latest.json")
    surface_sample_grid = atlas_reports.get("config/ascendant_atlas/reports/sample_grid_surface_latest.json")
    biome_pool_report = atlas_reports.get("config/ascendant_atlas/reports/biome_pools_resolved.json")
    water_review_report = atlas_reports.get("config/ascendant_atlas/reports/water_surface_samples_latest.json")
    water_body_report = atlas_reports.get("config/ascendant_atlas/reports/water_body_classification_latest.json")
    terrain_probe_report = atlas_reports.get("config/ascendant_atlas/reports/terrain_noise_probe_latest.json")
    land_water_coherence_report = atlas_reports.get("config/ascendant_atlas/reports/land_water_coherence_latest.json")
    terrain_wrapper_report = atlas_reports.get("config/ascendant_atlas/reports/terrain_wrapper_test_latest.json")
    if surface_sample_grid is None:
        warnings.append(
            "HARD WARNING: Atlas surface validation report is missing: "
            "config/ascendant_atlas/reports/sample_grid_surface_latest.json"
        )
    if water_body_report is None:
        warnings.append(
            "HARD WARNING: Atlas water-body classification report is missing: "
            "config/ascendant_atlas/reports/water_body_classification_latest.json"
        )
    if terrain_probe_report is None:
        warnings.append(
            "HARD WARNING: Atlas terrain/noise probe report is missing: "
            "config/ascendant_atlas/reports/terrain_noise_probe_latest.json"
        )
    if land_water_coherence_report is None:
        warnings.append(
            "HARD WARNING: Atlas land/water coherence report is missing: "
            "config/ascendant_atlas/reports/land_water_coherence_latest.json"
        )
    if terrain_wrapper_report is None:
        warnings.append(
            "HARD WARNING: Atlas terrain wrapper/correction prototype report is missing: "
            "config/ascendant_atlas/reports/terrain_wrapper_test_latest.json"
        )

    land_water_policy_path = ROOT / "config/ascendant_atlas/land_water_region_policy.json"
    land_water_policy_enabled = False
    if not land_water_policy_path.exists():
        warnings.append("Atlas land/water region policy is missing: config/ascendant_atlas/land_water_region_policy.json")
    else:
        try:
            land_water_policy = read_json(land_water_policy_path)
            if not isinstance(land_water_policy, dict):
                errors.append("config/ascendant_atlas/land_water_region_policy.json must be a JSON object.")
            else:
                land_water_policy_enabled = bool(land_water_policy.get("enabled"))
                land_first_regions = land_water_policy.get("land_first_regions", [])
                if land_water_policy_enabled and not isinstance(land_first_regions, list):
                    errors.append("config/ascendant_atlas/land_water_region_policy.json land_first_regions must be a list.")
                for required_region in ["sunreach", "stoneback", "south", "west", "south_west"]:
                    if land_water_policy_enabled and required_region not in {str(value) for value in land_first_regions if isinstance(value, str)}:
                        warnings.append(
                            "Atlas land/water region policy enabled but missing land-first region "
                            f"{required_region}."
                        )
        except Exception as exc:
            errors.append(f"config/ascendant_atlas/land_water_region_policy.json is invalid JSON: {exc}")

    if land_water_policy_enabled:
        if not isinstance(terrain_probe_report, dict):
            warnings.append(
                "HARD WARNING: Atlas land/water prototype policy is enabled but no terrain probe report exists yet; "
                "run /ascatlas sample_land_water 30000 5000 in a fresh validation world."
            )
        elif terrain_probe_report.get("source") != "in_game_ascatlas_sample_land_water_command" and terrain_probe_report.get("source") != "in_game_ascatlas_terrain_probe_command":
            warnings.append(
                "HARD WARNING: Atlas terrain probe report was not produced by the in-game land/water probe commands."
            )

    terrain_noise_policy_path = ROOT / "config/ascendant_atlas/terrain_noise_policy.json"
    if terrain_noise_policy_path.exists():
        try:
            terrain_noise_policy = read_json(terrain_noise_policy_path)
            if not isinstance(terrain_noise_policy, dict):
                errors.append("config/ascendant_atlas/terrain_noise_policy.json must be a JSON object.")
            else:
                correction = terrain_noise_policy.get("terrain_correction") or terrain_noise_policy.get("correction") or {}
                if terrain_noise_policy.get("enabled") is True and not isinstance(correction, dict):
                    errors.append("config/ascendant_atlas/terrain_noise_policy.json terrain_correction must be an object.")
                if isinstance(correction, dict) and correction.get("enabled") is True and terrain_wrapper_report is None:
                    warnings.append(
                        "HARD WARNING: Atlas terrain correction is enabled but no terrain wrapper test report exists yet; "
                        "run /ascatlas dump_terrain_noise_policy and fresh-world terrain validation."
                    )
                if isinstance(correction, dict) and correction.get("enabled") is True:
                    max_lift = correction.get("maximum_lift_above_water")
                    min_lift = correction.get("minimum_lift_above_water", 4)
                    water_ratio = correction.get("min_chunk_water_ratio_for_correction")
                    variation = correction.get("target_surface_variation")
                    if not isinstance(max_lift, (int, float)):
                        warnings.append(
                            "HARD WARNING: Atlas terrain correction is enabled but maximum_lift_above_water is missing; "
                            "set a cap so basin fixes cannot create artificial stone/terracotta shelves."
                        )
                    else:
                        if isinstance(min_lift, (int, float)) and max_lift < min_lift:
                            warnings.append(
                                "HARD WARNING: Atlas terrain correction maximum_lift_above_water is below "
                                "minimum_lift_above_water; corrected basin height bounds are inconsistent."
                            )
                        if max_lift > 16:
                            warnings.append(
                                "HARD WARNING: Atlas terrain correction maximum_lift_above_water is above 16; "
                                "this can recreate the artificial shelf/shear-wall terrain seen near Stoneback/Sunreach."
                            )
                    if isinstance(water_ratio, (int, float)) and water_ratio < 0.5:
                        warnings.append(
                            "HARD WARNING: Atlas terrain correction min_chunk_water_ratio_for_correction is below 0.5; "
                            "this may overcorrect ordinary lakes or coastal edges into artificial shelves."
                        )
                    if isinstance(variation, (int, float)) and variation > 3:
                        warnings.append(
                            "HARD WARNING: Atlas terrain correction target_surface_variation is above 3; "
                            "this can make corrected basin fill look noisy and unnatural."
                        )
        except Exception as exc:
            errors.append(f"config/ascendant_atlas/terrain_noise_policy.json is invalid JSON: {exc}")

    pool_biomes: dict[str, set[str]] = {}
    if isinstance(biome_pool_report, dict) and isinstance(biome_pool_report.get("pools"), dict):
        for pool_key, pool in biome_pool_report["pools"].items():
            if isinstance(pool, dict):
                biomes = pool.get("biomes", [])
                if isinstance(biomes, list):
                    pool_biomes[str(pool_key)] = {
                        str(biome.get("id"))
                        for biome in biomes
                        if isinstance(biome, dict) and biome.get("id")
                    }
            elif isinstance(pool, list):
                pool_biomes[str(pool_key)] = {str(biome) for biome in pool if biome}

    atlas_pool_cave_biomes = [
        f"{pool}:{biome}"
        for pool, biomes in sorted(pool_biomes.items())
        for biome in sorted(biomes)
        if atlas_is_cave_only_biome(biome)
    ]
    if atlas_pool_cave_biomes:
        errors.append(
            "Atlas biome pools must not include cave-only biomes in surface region tables: "
            + ", ".join(atlas_pool_cave_biomes[:20])
            + ("..." if len(atlas_pool_cave_biomes) > 20 else "")
        )

    if isinstance(source_sample_grid, dict):
        raw_samples = source_sample_grid.get("samples", [])
        if not isinstance(raw_samples, list):
            errors.append("config/ascendant_atlas/reports/sample_grid_source_latest.json samples must be a list.")
            raw_samples = []
        samples = [sample for sample in raw_samples if isinstance(sample, dict)]
        if len(samples) != len(raw_samples):
            errors.append("config/ascendant_atlas/reports/sample_grid_source_latest.json contains non-object sample entries.")
        source_pool_mismatches = []
        for sample in samples:
            actual_biome = str(sample.get("actual_biome_id") or "")
            expected_pool = str(sample.get("expected_biome_pool") or "")
            in_expected_pool = sample.get("actual_biome_in_expected_pool")
            if in_expected_pool is False:
                source_pool_mismatches.append(sample)
            elif (
                in_expected_pool is None
                and actual_biome
                and expected_pool in pool_biomes
                and actual_biome not in pool_biomes[expected_pool]
            ):
                source_pool_mismatches.append(sample)
        if source_pool_mismatches:
            warnings.append(
                "Atlas source sample grid has actual biomes outside the expected region pool: "
                f"{len(source_pool_mismatches)} ({atlas_sample_preview(source_pool_mismatches)})"
            )

        source_snow_outside_cold = [
            sample
            for sample in samples
            if sample.get("snow_allowed") is True
            and str(sample.get("expected_biome_pool") or sample.get("climate_sector") or "") not in ASCENDANT_ATLAS_SNOW_ALLOWED_POOLS
            and str(sample.get("climate_sector") or "") not in ASCENDANT_ATLAS_SNOW_ALLOWED_POOLS
        ]
        if source_snow_outside_cold:
            warnings.append(
                "Atlas source sample grid allows snow outside cold/Frostmarch pools: "
                f"{len(source_snow_outside_cold)} ({atlas_sample_preview(source_snow_outside_cold)})"
            )

    if isinstance(surface_sample_grid, dict):
        raw_surface_samples = surface_sample_grid.get("samples", [])
        if not isinstance(raw_surface_samples, list):
            errors.append("config/ascendant_atlas/reports/sample_grid_surface_latest.json samples must be a list.")
            raw_surface_samples = []
        surface_samples = [sample for sample in raw_surface_samples if isinstance(sample, dict)]
        if len(surface_samples) != len(raw_surface_samples):
            errors.append("config/ascendant_atlas/reports/sample_grid_surface_latest.json contains non-object sample entries.")

        normal_surface_samples = [sample for sample in surface_samples if atlas_is_normal_surface_sample(sample)]
        if not normal_surface_samples:
            warnings.append(
                "HARD WARNING: Atlas surface validation has 0 normal surface samples in "
                "config/ascendant_atlas/reports/sample_grid_surface_latest.json"
            )

        underground_surface_samples = [
            sample
            for sample in normal_surface_samples
            if (atlas_numeric(sample.get("surface_y")) or 0) <= -60
        ]
        if underground_surface_samples:
            warnings.append(
                "Atlas surface sample grid has samples at or below y=-60: "
                f"{len(underground_surface_samples)} ({atlas_sample_preview(underground_surface_samples)})"
            )

        cave_surface_samples = [
            sample
            for sample in normal_surface_samples
            if sample.get("cave_like_biome_at_surface") is True or atlas_is_cave_only_biome(sample.get("actual_biome_id"))
        ]
        if cave_surface_samples:
            warnings.append(
                "Atlas surface sample grid has cave-like biomes at surface: "
                f"{len(cave_surface_samples)} ({atlas_sample_preview(cave_surface_samples)})"
            )

        surface_pool_mismatches = []
        accepted_transition_edges = []
        invalid_declared_transition_edges = []
        for sample in normal_surface_samples:
            actual_biome = str(sample.get("actual_biome_id") or "")
            expected_pool = str(sample.get("expected_biome_pool") or "")
            in_expected_pool = sample.get("actual_biome_in_expected_pool")
            accepted_transition = atlas_accepted_transition_edge_case(sample)
            declared_transition = sample.get("accepted_transition_edge_case")
            if accepted_transition:
                accepted_transition_edges.append(sample)
            if declared_transition and declared_transition != accepted_transition:
                invalid_declared_transition_edges.append(sample)
            if in_expected_pool is False:
                if not accepted_transition:
                    surface_pool_mismatches.append(sample)
            elif (
                in_expected_pool is None
                and actual_biome
                and expected_pool in pool_biomes
                and actual_biome not in pool_biomes[expected_pool]
                and not accepted_transition
            ):
                surface_pool_mismatches.append(sample)
        if invalid_declared_transition_edges:
            warnings.append(
                "Atlas surface sample grid has malformed accepted transition edge cases: "
                f"{len(invalid_declared_transition_edges)} ({atlas_sample_preview(invalid_declared_transition_edges)})"
            )
        if surface_pool_mismatches:
            warnings.append(
                "Atlas surface sample grid has actual surface biomes outside the expected region pool: "
                f"{len(surface_pool_mismatches)} ({atlas_sample_preview(surface_pool_mismatches)})"
            )

        surface_snow_outside_cold = [
            sample
            for sample in normal_surface_samples
            if atlas_has_snow_rule_violation(sample)
        ]
        if surface_snow_outside_cold:
            warnings.append(
                "Atlas surface sample grid allows snow outside cold/Frostmarch pools: "
                f"{len(surface_snow_outside_cold)} ({atlas_sample_preview(surface_snow_outside_cold)})"
            )

        surface_water_review = [
            sample
            for sample in normal_surface_samples
            if sample.get("surface_block_id") == "minecraft:water"
            and str(sample.get("expected_biome_pool") or sample.get("climate_sector") or "") in ASCENDANT_ATLAS_WATER_REVIEW_POOLS
        ]
        if surface_water_review and atlas_worldgen_override_enabled:
            warnings.append(
                "Atlas surface sample grid has water surface blocks in south/west review pools: "
                f"{len(surface_water_review)} ({atlas_sample_preview(surface_water_review)})"
            )

    if isinstance(water_review_report, dict):
        raw_water_samples = water_review_report.get("samples", [])
        if isinstance(raw_water_samples, list):
            water_samples = [sample for sample in raw_water_samples if isinstance(sample, dict)]
            ocean_leak_samples = [
                sample
                for sample in water_samples
                if sample.get("is_south_west_water_target_region")
                and sample.get("classification") == "ocean_leak"
            ]
            if ocean_leak_samples and atlas_worldgen_override_enabled:
                warnings.append(
                    "Atlas water review has visually confirmed south/west ocean leaks: "
                    f"{len(ocean_leak_samples)} ({atlas_sample_preview(ocean_leak_samples)})"
                )
        else:
            errors.append("config/ascendant_atlas/reports/water_surface_samples_latest.json samples must be a list.")

    if isinstance(water_body_report, dict):
        if water_body_report.get("source") != "in_game_ascatlas_classify_water_bodies_command":
            warnings.append(
                "HARD WARNING: Atlas water-body classification has not been produced by the in-game neighborhood sampler yet."
            )
        elif water_body_report.get("status") != "complete":
            warnings.append(
                "HARD WARNING: Atlas water-body classification report is not complete: "
                f"{water_body_report.get('status')}"
            )
        raw_water_body_samples = water_body_report.get("samples", [])
        if isinstance(raw_water_body_samples, list):
            water_body_samples = [sample for sample in raw_water_body_samples if isinstance(sample, dict)]
            if len(water_body_samples) != len(raw_water_body_samples):
                errors.append("config/ascendant_atlas/reports/water_body_classification_latest.json contains non-object sample entries.")
            if (
                water_body_report.get("source") == "in_game_ascatlas_classify_water_bodies_command"
                and water_body_samples
                and not any("skipped_unloaded_chunk_counts_by_radius_blocks" in sample for sample in water_body_samples)
            ):
                warnings.append(
                    "HARD WARNING: Atlas water-body classification report was generated by the old forcing scanner; "
                    "rerun with the bounded local helper jar before terrain-water signoff."
                )
            insufficient_coverage_samples = [
                sample for sample in water_body_samples
                if sample.get("estimated_water_body_size") == "insufficient_loaded_chunk_coverage"
            ]
            if insufficient_coverage_samples:
                warnings.append(
                    "HARD WARNING: Atlas water-body classification has insufficient local coverage samples: "
                    f"{len(insufficient_coverage_samples)} ({atlas_sample_preview(insufficient_coverage_samples)})"
                )
            water_body_ocean_leaks = [
                sample for sample in water_body_samples if sample.get("classification") == "ocean_leak"
            ]
            water_body_basin_leaks = [
                sample for sample in water_body_samples if sample.get("classification") == "basin_leak"
            ]
            if water_body_ocean_leaks and atlas_worldgen_override_enabled:
                warnings.append(
                    "Atlas water-body classification reports ocean leaks: "
                    f"{len(water_body_ocean_leaks)} ({atlas_sample_preview(water_body_ocean_leaks)})"
                )
            if water_body_basin_leaks and atlas_worldgen_override_enabled:
                warnings.append(
                    "Atlas water-body classification reports basin leaks: "
                    f"{len(water_body_basin_leaks)} ({atlas_sample_preview(water_body_basin_leaks)})"
                )
        else:
            errors.append("config/ascendant_atlas/reports/water_body_classification_latest.json samples must be a list.")

    if isinstance(terrain_probe_report, dict):
        raw_probe_samples = terrain_probe_report.get("samples", [])
        if isinstance(raw_probe_samples, list):
            probe_samples = [sample for sample in raw_probe_samples if isinstance(sample, dict)]
            if len(probe_samples) != len(raw_probe_samples):
                errors.append("config/ascendant_atlas/reports/terrain_noise_probe_latest.json contains non-object sample entries.")
            land_first_leaks = [
                sample for sample in probe_samples
                if sample.get("land_first_rule_applied") is True
                and sample.get("classification") in {"ocean_leak", "basin_leak"}
            ]
            ocean_leaks = [sample for sample in land_first_leaks if sample.get("classification") == "ocean_leak"]
            basin_leaks = [sample for sample in land_first_leaks if sample.get("classification") == "basin_leak"]
            if ocean_leaks and atlas_worldgen_override_enabled:
                warnings.append(
                    "Atlas terrain probe still reports land-first ocean leaks: "
                    f"{len(ocean_leaks)} ({atlas_sample_preview(ocean_leaks)})"
                )
            if basin_leaks and atlas_worldgen_override_enabled:
                warnings.append(
                    "Atlas terrain probe still reports land-first basin leaks: "
                    f"{len(basin_leaks)} ({atlas_sample_preview(basin_leaks)})"
                )
            overcorrected = [
                sample for sample in probe_samples
                if sample.get("valid_water_feature_overcorrected") is True
                or str(sample.get("classification") or "").startswith("overcorrected_")
            ]
            if overcorrected:
                warnings.append(
                    "Atlas terrain probe says valid rivers/oases/mountain lakes were overcorrected: "
                    f"{len(overcorrected)} ({atlas_sample_preview(overcorrected)})"
                )
            summary = terrain_probe_report.get("summary", {})
            if isinstance(summary, dict) and terrain_probe_report.get("status") == "complete":
                if int(summary.get("water_surface_samples", 0) or 0) > 0 and int(summary.get("preserved_water_feature_samples", 0) or 0) == 0:
                    warnings.append(
                        "Atlas terrain probe found water samples but no preserved river/oasis/lake/coastline classifications; "
                        "review for overcorrection before terrain signoff."
                    )
        else:
            errors.append("config/ascendant_atlas/reports/terrain_noise_probe_latest.json samples must be a list.")

    terrain_doc_text = ""
    for doc_name in [
        "docs/CURRENT_STATUS.md",
        "docs/ATLAS_TERRAIN_VALIDATION_REPORT.md",
        "docs/ATLAS_LAND_WATER_COHERENCE.md",
        "docs/ATLAS_TERRAIN_NOISE_CONTROL_PLAN.md",
    ]:
        doc_path = ROOT / doc_name
        if doc_path.exists():
            terrain_doc_text += "\n" + read_text(doc_path)
    if re.search(r"(?i)\bterrain(?:/noise)?\s+(?:is\s+)?signed off\b|\bfull terrain signoff complete\b", terrain_doc_text):
        terrain_probe_clean = (
            isinstance(terrain_probe_report, dict)
            and terrain_probe_report.get("status") == "complete"
            and isinstance(terrain_probe_report.get("summary"), dict)
            and int(terrain_probe_report["summary"].get("land_first_ocean_leaks", 1) or 1) == 0
            and int(terrain_probe_report["summary"].get("land_first_basin_leaks", 1) or 1) == 0
        )
        if not terrain_probe_clean:
            warnings.append(
                "Terrain/noise docs appear to claim signoff without a complete clean fresh-world land/water probe report."
            )

    atlas_runtime_path = ROOT / "config/ascendant_atlas/runtime.json"
    if atlas_runtime_path.exists():
        try:
            runtime = read_json(atlas_runtime_path)
            border = runtime.get("worldborder", {})
            runtime_radius = int(runtime.get("world_radius_blocks", 0))
            if runtime_radius != 30000:
                errors.append("config/ascendant_atlas/runtime.json must use the 30000 block Atlas validation radius.")
            if int(border.get("diameter_blocks", 0)) != 60000:
                errors.append("config/ascendant_atlas/runtime.json must set a 60000 block worldborder diameter.")
            scoreboards = runtime.get("scoreboards", {})
            for objective in ["ar_atlas_region", "ar_atlas_ring", "ar_atlas_sector", "ar_atlas_distance"]:
                if objective not in scoreboards.values():
                    errors.append(f"Atlas runtime scoreboards must include {objective}.")
            atlas_dimension_path = ROOT / "config/openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json"
            if atlas_dimension_path.exists():
                dimension = read_json(atlas_dimension_path)
                biome_source = dimension.get("generator", {}).get("biome_source", {})
                outer_radius = int(biome_source.get("outer_radius_blocks", 0) or 0)
                if outer_radius <= runtime_radius:
                    errors.append(
                        "Atlas biome-source outer_radius_blocks must extend beyond the 30000 block world border "
                        "so visible terrain past the barrier does not snap to the shared outer pool."
                    )
                if outer_radius < runtime_radius + 2048:
                    warnings.append(
                        "Atlas biome-source outer_radius_blocks has less than 2048 blocks of visual buffer beyond "
                        "the world border."
                    )
        except Exception as exc:
            errors.append(f"Ascendant Atlas runtime is invalid: {exc}")

    atlas_runtime_script = ROOT / "kubejs/server_scripts/ascendant_atlas_runtime.js"
    if atlas_runtime_script.exists():
        atlas_runtime_script_text = read_text(atlas_runtime_script)
        for expected in [
            "AscendantAtlasJsonIO.read",
            "JsonIO",
            "ServerEvents.loaded",
            "PlayerEvents.tick",
            "worldborder set",
            "ascendant_atlas/runtime.json",
        ]:
            if expected not in atlas_runtime_script_text:
                errors.append(f"kubejs/server_scripts/ascendant_atlas_runtime.js is missing {expected}.")
        for forbidden in [
            ".getFileSystem().getPath(",
            ".resolve(",
            "java.nio.file.Files",
            "java.nio.file.Paths",
            "java.io.File",
            'Java.loadClass("java.io.File")',
        ]:
            if forbidden in atlas_runtime_script_text:
                errors.append(
                    "kubejs/server_scripts/ascendant_atlas_runtime.js contains a blocked pattern "
                    f"that has failed under KubeJS/Rhino: {forbidden}"
                )

    atlas_areas_path = ROOT / "config/incontrol/areas.json"
    if atlas_areas_path.exists():
        try:
            areas = read_json(atlas_areas_path)
            area_names = {str(entry.get("name")) for entry in areas if isinstance(entry, dict)}
            missing_areas = ASCENDANT_ATLAS_AREA_NAMES - area_names
            if missing_areas:
                errors.append(f"config/incontrol/areas.json is missing Atlas areas: {sorted(missing_areas)}")
            for entry in areas:
                if not isinstance(entry, dict) or str(entry.get("name")) not in ASCENDANT_ATLAS_AREA_NAMES:
                    continue
                if entry.get("type") != "box":
                    errors.append(
                        f"config/incontrol/areas.json area {entry.get('name')} must set type to box for In Control 1.20."
                    )
                if entry.get("dimension") != "minecraft:overworld":
                    errors.append(
                        f"config/incontrol/areas.json area {entry.get('name')} must target minecraft:overworld."
                    )
        except Exception as exc:
            errors.append(f"In Control Atlas areas are invalid: {exc}")

    incontrol_spawn_path = ROOT / "config/incontrol/spawn.json"
    if incontrol_spawn_path.exists():
        try:
            spawn_text = read_text(incontrol_spawn_path)
            for required_area in ["ar_hearthlands", "ar_frostmarch", "ar_sunreach", "ar_stoneback_highlands"]:
                if required_area not in spawn_text:
                    errors.append(f"config/incontrol/spawn.json must reference Atlas area {required_area}.")
            for required_mod in ["cataclysm", "iceandfire", "aquamirae", "soulsweapons"]:
                if required_mod not in spawn_text:
                    errors.append(f"config/incontrol/spawn.json must keep regional guardrail coverage for {required_mod}.")
        except Exception as exc:
            errors.append(f"In Control spawn rules could not be read: {exc}")

    spawn_density_policy_path = ROOT / "config/ascendant_core/spawn_density_policy.json"
    if spawn_density_policy_path.exists():
        try:
            spawn_density_policy = read_json(spawn_density_policy_path)
            if not isinstance(spawn_density_policy, dict):
                errors.append("config/ascendant_core/spawn_density_policy.json must be a JSON object.")
            else:
                accepted_spawn_density_statuses = {
                    "active_high_density_spawn_pass",
                    "active_flat_strong_modded_daytime_spawn_pass",
                    "active_region_based_spawn_difficulty_pass",
                }
                if spawn_density_policy.get("status") not in accepted_spawn_density_statuses:
                    warnings.append(
                        "Ascendant spawn density policy is not marked as an accepted active spawn-density pass."
                    )
                changes = spawn_density_policy.get("changes", {})
                changes = changes if isinstance(changes, dict) else {}

                sbu_expected = changes.get("spawn_balance_utility", {})
                sbu_expected = sbu_expected if isinstance(sbu_expected, dict) else {}
                sbu_path = ROOT / "config/spawnbalanceutility-common.toml"
                if sbu_path.exists():
                    sbu_text = read_text(sbu_path)
                    for setting in ["minSpawnWeight", "maxSpawnWeight"]:
                        expected = sbu_expected.get(setting)
                        actual = toml_int_setting(sbu_text, setting)
                        if isinstance(expected, int) and actual is not None and actual < expected:
                            warnings.append(
                                f"Spawn Balance Utility {setting} is {actual}, below density policy floor {expected}."
                            )
                    expected_weights = sbu_expected.get("defaultSpawnWeightList", {})
                    if isinstance(expected_weights, dict):
                        actual_weights = spawn_balance_default_weights(sbu_text)
                        for entity_id, expected_weight in expected_weights.items():
                            actual_weight = actual_weights.get(str(entity_id))
                            if isinstance(expected_weight, int) and (actual_weight is None or actual_weight < expected_weight):
                                warnings.append(
                                    "Spawn Balance Utility defaultSpawnWeightList is below density policy for "
                                    f"{entity_id}: {actual_weight!r} < {expected_weight}."
                                )

                majrusz_expected = changes.get("majruszsdifficulty", {})
                majrusz_expected = majrusz_expected if isinstance(majrusz_expected, dict) else {}
                majrusz_path = ROOT / "config/majruszsdifficulty.json"
                if majrusz_path.exists():
                    try:
                        majrusz_config = read_json(majrusz_path)
                        spawn_rate_increaser = find_nested_dict(majrusz_config, "spawn_rate_increaser")
                        expected_multipliers = majrusz_expected.get("spawn_rate_increaser", {})
                        actual_multipliers = (
                            spawn_rate_increaser.get("multiplier", {}) if isinstance(spawn_rate_increaser, dict) else {}
                        )
                        if isinstance(expected_multipliers, dict) and isinstance(actual_multipliers, dict):
                            for stage, expected_multiplier in expected_multipliers.items():
                                actual_multiplier = actual_multipliers.get(str(stage))
                                if isinstance(expected_multiplier, (int, float)) and (
                                    not isinstance(actual_multiplier, (int, float))
                                    or float(actual_multiplier) < float(expected_multiplier)
                                ):
                                    warnings.append(
                                        "Majrusz spawn_rate_increaser multiplier is below density policy for "
                                        f"{stage}: {actual_multiplier!r} < {expected_multiplier}."
                                    )
                        mob_groups = find_nested_dict(majrusz_config, "mob_groups")
                        expected_groups = majrusz_expected.get("mob_groups", {})
                        if isinstance(expected_groups, dict) and isinstance(mob_groups, dict):
                            for group_id, expected_group in expected_groups.items():
                                if not isinstance(expected_group, dict):
                                    continue
                                actual_group = mob_groups.get(str(group_id), {})
                                actual_group = actual_group if isinstance(actual_group, dict) else {}
                                actual_chance = actual_group.get("chance")
                                expected_chance = expected_group.get("chance")
                                if isinstance(expected_chance, (int, float)) and (
                                    not isinstance(actual_chance, (int, float)) or float(actual_chance) < float(expected_chance)
                                ):
                                    warnings.append(
                                        f"Majrusz mob group {group_id} chance is below density policy: "
                                        f"{actual_chance!r} < {expected_chance}."
                                    )
                                actual_sidekicks = actual_group.get("sidekicks_count", {})
                                actual_sidekicks = actual_sidekicks if isinstance(actual_sidekicks, dict) else {}
                                for sidekick_key, actual_key in [("sidekicks_min", "min"), ("sidekicks_max", "max")]:
                                    expected_count = expected_group.get(sidekick_key)
                                    actual_count = actual_sidekicks.get(actual_key)
                                    if isinstance(expected_count, int) and (
                                        not isinstance(actual_count, int) or actual_count < expected_count
                                    ):
                                        warnings.append(
                                            f"Majrusz mob group {group_id} {sidekick_key} is below density policy: "
                                            f"{actual_count!r} < {expected_count}."
                                        )
                    except Exception as exc:
                        errors.append(f"config/majruszsdifficulty.json is invalid for spawn-density validation: {exc}")

                expected_caps = changes.get("incontrol_caps", {})
                if isinstance(expected_caps, dict) and incontrol_spawn_path.exists():
                    try:
                        spawn_rules = read_json(incontrol_spawn_path)
                        if isinstance(spawn_rules, list):
                            actual_caps: dict[str, int] = {}
                            for rule in spawn_rules:
                                if not isinstance(rule, dict) or rule.get("result") != "deny":
                                    continue
                                mod_id = rule.get("mod")
                                mincount = rule.get("mincount", {})
                                amount = mincount.get("amount") if isinstance(mincount, dict) else None
                                if isinstance(mod_id, str) and isinstance(amount, int):
                                    actual_caps[mod_id] = max(actual_caps.get(mod_id, 0), amount)
                            for mod_id, expected_cap in expected_caps.items():
                                actual_cap = actual_caps.get(str(mod_id))
                                if isinstance(expected_cap, int) and (actual_cap is None or actual_cap < expected_cap):
                                    warnings.append(
                                        f"In Control cap for {mod_id} is below density policy: {actual_cap!r} < {expected_cap}."
                                    )
                    except Exception as exc:
                        errors.append(f"config/incontrol/spawn.json is invalid for spawn-density validation: {exc}")
                spawner_expected = changes.get("incontrol_hostile_spawner", {})
                if isinstance(spawner_expected, dict):
                    accepted_spawner_statuses = {
                        "active_daytime_hostile_injection",
                        "active_modded_daytime_and_cave_hostile_injection",
                    }
                    if spawner_expected.get("status") not in accepted_spawner_statuses:
                        warnings.append("Ascendant hostile spawner policy is not marked as an accepted active injection pass.")
                    spawner_path = ROOT / str(spawner_expected.get("file") or "config/incontrol/spawner.json")
                else:
                    spawner_path = ROOT / "config/incontrol/spawner.json"

                if spawner_path.exists():
                    try:
                        spawner_rules = read_json(spawner_path)
                        if not isinstance(spawner_rules, list) or len(spawner_rules) < 6:
                            errors.append("config/incontrol/spawner.json must contain at least six hostile density rules.")
                        else:
                            explicit_mobs: list[str] = []
                            biome_native_surface = False
                            cave_rule = False
                            daylight_bypass_rules = 0
                            missing_caps = 0
                            for rule in spawner_rules:
                                if not isinstance(rule, dict):
                                    errors.append("config/incontrol/spawner.json rules must be JSON objects.")
                                    continue
                                explicit_mobs.extend(string_values(rule.get("mob")))
                                conditions = rule.get("conditions", {})
                                conditions = conditions if isinstance(conditions, dict) else {}
                                if conditions.get("dimension") != "minecraft:overworld":
                                    errors.append("config/incontrol/spawner.json hostile rules must target minecraft:overworld.")
                                if conditions.get("norestrictions") is True:
                                    daylight_bypass_rules += 1
                                if any(cap not in conditions for cap in ["maxhostile", "maxlocal", "maxthis"]):
                                    missing_caps += 1
                                nested_and = conditions.get("and", {})
                                nested_and = nested_and if isinstance(nested_and, dict) else {}
                                if rule.get("mobsfrombiome") == "monster" and conditions.get("norestrictions") is True and nested_and.get("seesky") is True:
                                    biome_native_surface = True
                                if rule.get("mobsfrombiome") == "monster" and nested_and.get("cave") is True:
                                    cave_rule = True
                            if biome_native_surface:
                                errors.append(
                                    "config/incontrol/spawner.json must not include open-sky biome-native monster injection; "
                                    "it can reintroduce burning undead during daytime."
                                )
                            if not cave_rule:
                                warnings.append("config/incontrol/spawner.json has no biome-native cave reinforcement rule.")
                            if daylight_bypass_rules < 5:
                                warnings.append("config/incontrol/spawner.json has too few norestrictions daylight hostile rules.")
                            if missing_caps:
                                warnings.append(
                                    f"config/incontrol/spawner.json has {missing_caps} rules missing maxhostile/maxlocal/maxthis caps."
                                )
                            forbidden_boss_mobs = {
                                "minecraft:wither",
                                "minecraft:ender_dragon",
                                "iceandfire:fire_dragon",
                                "iceandfire:ice_dragon",
                                "iceandfire:lightning_dragon",
                                "aquamirae:ghost_of_captain_cornelia",
                                "bossesrise:gauntlet",
                                "cataclysm:ender_guardian",
                                "cataclysm:ignis",
                                "cataclysm:netherite_monstrosity",
                                "cataclysm:the_harbinger",
                                "cataclysm:the_leviathan",
                                "cataclysm:ancient_remnant",
                                "mowziesmobs:frostmaw",
                                "mowziesmobs:ferrous_wroughtnaut",
                                "mowziesmobs:umvuthi",
                            }
                            forbidden_mobs = [
                                mob_id for mob_id in explicit_mobs
                                if mob_id in forbidden_boss_mobs
                            ]
                            if forbidden_mobs:
                                errors.append(
                                    "config/incontrol/spawner.json explicitly injects boss/dragon-tier mobs: "
                                    f"{ascendant_loot_preview(forbidden_mobs)}"
                                )
                    except Exception as exc:
                        errors.append(f"config/incontrol/spawner.json is invalid for hostile spawn validation: {exc}")
                else:
                    errors.append("config/incontrol/spawner.json is missing while hostile daytime spawn policy is active.")

                regional_expected = changes.get("regional_difficulty", {})
                regional_expected = regional_expected if isinstance(regional_expected, dict) else {}
                regional_required = spawn_density_policy.get("status") == "active_region_based_spawn_difficulty_pass" or bool(regional_expected)
                regional_path = ROOT / str(regional_expected.get("file") or "config/ascendant_core/regional_difficulty_policy.json")
                regional_script = ROOT / str(regional_expected.get("script") or "kubejs/server_scripts/ascendant_regional_difficulty.js")
                if regional_required:
                    if not regional_path.exists():
                        errors.append("config/ascendant_core/regional_difficulty_policy.json is missing for region-based difficulty.")
                    else:
                        try:
                            regional_policy = read_json(regional_path)
                            if not isinstance(regional_policy, dict):
                                errors.append("config/ascendant_core/regional_difficulty_policy.json must be a JSON object.")
                            else:
                                if regional_policy.get("status") != "active_region_based_difficulty_multiplier":
                                    warnings.append("Regional difficulty policy is not marked active_region_based_difficulty_multiplier.")
                                implementation = regional_policy.get("implementation", {})
                                implementation = implementation if isinstance(implementation, dict) else {}
                                for disabled_key in ["uses_day_count", "uses_time_of_day", "uses_crd"]:
                                    if implementation.get(disabled_key) is not False:
                                        errors.append(
                                            f"Regional difficulty policy must set implementation.{disabled_key}=false."
                                        )
                                profiles = regional_policy.get("region_profiles", {})
                                profiles = profiles if isinstance(profiles, dict) else {}
                                required_profiles = {
                                    "hearthlands": 0,
                                    "frostmarch": 1,
                                    "sunreach": 2,
                                    "verdant_coast": 3,
                                    "stoneback_highlands": 4,
                                    "north_east_marches": 5,
                                    "north_west_marches": 6,
                                    "south_east_wilds": 7,
                                    "south_west_wilds": 8,
                                    "outer_rim": 9,
                                }
                                for profile_id, region_id in required_profiles.items():
                                    profile = profiles.get(profile_id)
                                    if not isinstance(profile, dict):
                                        errors.append(f"Regional difficulty policy is missing profile {profile_id}.")
                                        continue
                                    if profile.get("atlas_region_id") != region_id:
                                        errors.append(
                                            f"Regional difficulty profile {profile_id} must use atlas_region_id {region_id}."
                                        )
                        except Exception as exc:
                            errors.append(f"config/ascendant_core/regional_difficulty_policy.json is invalid: {exc}")
                    if not regional_script.exists():
                        errors.append("kubejs/server_scripts/ascendant_regional_difficulty.js is missing for region-based difficulty.")

                coverage_report_path = ROOT / "config/ascendant_core/reports/overworld_mob_spawn_coverage_latest.json"
                if not coverage_report_path.exists():
                    warnings.append(
                        "Overworld mob spawn coverage report is missing; run scripts/audit-overworld-mob-spawn-coverage.py."
                    )
                else:
                    try:
                        coverage_report = read_json(coverage_report_path)
                        summary = coverage_report.get("summary", {}) if isinstance(coverage_report, dict) else {}
                        counts = summary.get("coverage_status_counts", {}) if isinstance(summary, dict) else {}
                        if not isinstance(counts, dict):
                            warnings.append("Overworld mob spawn coverage report is missing summary.coverage_status_counts.")
                        else:
                            missing_count = int(counts.get("missing_expected_overworld_evidence", 0) or 0)
                            review_count = int(counts.get("needs_manual_classification", 0) or 0)
                            if missing_count:
                                missing_entries = coverage_report.get("missing_expected_overworld_evidence", [])
                                missing_ids = [
                                    str(entry.get("entity_id"))
                                    for entry in missing_entries
                                    if isinstance(entry, dict) and entry.get("entity_id")
                                ]
                                warnings.append(
                                    "Overworld mob spawn coverage still has "
                                    f"{missing_count} expected entries without spawn evidence: "
                                    f"{ascendant_loot_preview(missing_ids)}"
                                )
                            if review_count:
                                warnings.append(
                                    "Overworld mob spawn coverage still has "
                                    f"{review_count} entries needing manual classification."
                                )
                    except Exception as exc:
                        warnings.append(f"Overworld mob spawn coverage report is invalid JSON: {exc}")
        except Exception as exc:
            errors.append(f"config/ascendant_core/spawn_density_policy.json is invalid JSON: {exc}")

    biome_assignments_path = ROOT / "config/ascendant_atlas/biome_assignments.json"
    if biome_assignments_path.exists():
        try:
            biome_assignments = read_json(biome_assignments_path)
            assignments = biome_assignments.get("assignments", [])
            if not isinstance(assignments, list) or len(assignments) < 50:
                errors.append("Atlas biome_assignments must contain the scanned vanilla/modded biome surface.")
            for entry in assignments[:100]:
                if not isinstance(entry, dict):
                    errors.append("Atlas biome_assignments entries must be objects.")
                    break
                for key in ("biome", "region", "sector", "danger_tier"):
                    if key not in entry:
                        errors.append(f"Atlas biome assignment is missing {key}: {entry}")
                        break
        except Exception as exc:
            errors.append(f"Atlas biome assignments are invalid: {exc}")

    structure_distribution_path = ROOT / "config/ascendant_atlas/structure_distribution.json"
    if structure_distribution_path.exists():
        try:
            structure_distribution = read_json(structure_distribution_path)
            assignments = structure_distribution.get("assignments", [])
            if not isinstance(assignments, list) or not assignments:
                errors.append("Atlas structure_distribution must include scanned structure assignments.")
            for entry in assignments:
                if not isinstance(entry, dict):
                    continue
                tier = int(entry.get("atlas_tier", 0))
                if tier >= 4 and entry.get("allowed_near_spawn") is True:
                    errors.append(
                        "Atlas structure_distribution allows high-tier structure near spawn: "
                        f"{entry.get('structure_id')}"
                    )
        except Exception as exc:
            errors.append(f"Atlas structure distribution is invalid: {exc}")

    for atlas_pack_root in [
        ROOT / "config/openloader/data/ascendant_realms_atlas",
        ROOT / "openloader/data/ascendant_realms_atlas",
    ]:
        if not atlas_pack_root.exists():
            errors.append(f"Ascendant Atlas OpenLoader pack is missing: {atlas_pack_root.relative_to(ROOT)}")
            continue
        pack_meta = atlas_pack_root / "pack.mcmeta"
        if not pack_meta.exists():
            errors.append(f"Ascendant Atlas pack.mcmeta is missing: {pack_meta.relative_to(ROOT)}")
        for structure_id in ASCENDANT_ATLAS_DEBUG_STRUCTURE_IDS:
            structure_name = structure_id.split(":", 1)[1]
            file_bundle = {
                "structure nbt": atlas_pack_root / f"data/ascendant_atlas/structures/atlas/{structure_name}.nbt",
                "structure json": atlas_pack_root / f"data/ascendant_atlas/worldgen/structure/{structure_name}.json",
                "template pool": atlas_pack_root / f"data/ascendant_atlas/worldgen/template_pool/atlas/{structure_name}.json",
                "biome tag": atlas_pack_root / f"data/ascendant_atlas/tags/worldgen/biome/has_structure/{structure_name}.json",
                "loot table": atlas_pack_root / f"data/ascendant_atlas/loot_tables/chests/{structure_name}.json",
            }
            for label, path in file_bundle.items():
                if not path.exists():
                    errors.append(f"Ascendant Atlas {label} is missing: {path.relative_to(ROOT)}")
            structure_nbt = file_bundle["structure nbt"]
            if structure_nbt.exists() and structure_nbt.stat().st_size < 100:
                errors.append(f"Ascendant Atlas structure NBT looks empty: {structure_nbt.relative_to(ROOT)}")
            structure_json_path = file_bundle["structure json"]
            if structure_json_path.exists():
                try:
                    structure_json = read_json(structure_json_path)
                    if structure_json.get("type") != "minecraft:jigsaw":
                        errors.append(f"{structure_json_path.relative_to(ROOT)} must be a minecraft:jigsaw structure.")
                    if structure_json.get("start_pool") != f"ascendant_atlas:atlas/{structure_name}":
                        errors.append(f"{structure_json_path.relative_to(ROOT)} has the wrong start_pool.")
                    if structure_json.get("biomes") != f"#ascendant_atlas:has_structure/{structure_name}":
                        errors.append(f"{structure_json_path.relative_to(ROOT)} has the wrong biome tag.")
                except Exception as exc:
                    errors.append(f"{structure_json_path.relative_to(ROOT)} is invalid JSON: {exc}")
            structure_set_path = atlas_pack_root / f"data/ascendant_atlas/worldgen/structure_set/{structure_name}.json"
            if structure_set_path.exists():
                errors.append(
                    f"Ascendant Atlas waymark structure set should not exist while waymarks are debug-only: "
                    f"{structure_set_path.relative_to(ROOT)}"
                )
            biome_tag_path = file_bundle["biome tag"]
            if biome_tag_path.exists():
                try:
                    biome_tag = read_json(biome_tag_path)
                    values = biome_tag.get("values", [])
                    if not isinstance(values, list) or not values:
                        errors.append(f"{biome_tag_path.relative_to(ROOT)} must include at least one biome.")
                except Exception as exc:
                    errors.append(f"{biome_tag_path.relative_to(ROOT)} is invalid JSON: {exc}")

    item_borders_config = ROOT / "config/itemborders-common.toml"
    if "mods/item-borders.pw.toml" in active_relatives:
        if not item_borders_config.exists():
            errors.append("Item Borders is installed but config/itemborders-common.toml is missing.")
        else:
            if has_utf8_bom(item_borders_config):
                errors.append(
                    "config/itemborders-common.toml has a UTF-8 BOM; Forge/NightConfig reads it as ï»¿# and crashes."
                )
            item_borders_text = read_text(item_borders_config)
            expected_item_border_settings = {
                "auto_borders": "false",
                "legendary_tooltips_sync": "false",
                "show_for_common": "false",
            }
            for key, expected in expected_item_border_settings.items():
                if not re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*{expected}\s*$", item_borders_text):
                    errors.append(f"config/itemborders-common.toml must set {key} = {expected}.")
            if "manual_borders = {" not in item_borders_text:
                errors.append("config/itemborders-common.toml must define manual_borders.")
            for color in ["#55FF55", "#55AAFF", "#D966FF", "#FFE66D", "#FF3B00", "#E6FBFF"]:
                if color not in item_borders_text:
                    warnings.append(f"Item Borders manual rarity color {color} is not present.")

    amendments_client_config = ROOT / "config/amendments-client.toml"
    if "mods/amendments.pw.toml" in active_relatives:
        if not amendments_client_config.exists():
            errors.append("Amendments is installed but config/amendments-client.toml is missing.")
        else:
            if has_utf8_bom(amendments_client_config):
                errors.append("config/amendments-client.toml has a UTF-8 BOM.")
            amendments_client_text = read_text(amendments_client_config)
            expected_amendments_client_settings = {
                "new_model": "false",
                "disc_spin": "false",
            }
            for key, expected in expected_amendments_client_settings.items():
                if not re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*{expected}\s*$", amendments_client_text):
                    errors.append(
                        f"config/amendments-client.toml must set {key} = {expected} to avoid Cataclysm animated disc mask resource errors."
                    )

    gear_rarity_script = ROOT / "kubejs/startup_scripts/ascendant_gear_rarity.js"
    if "mods/kubejs.pw.toml" in active_relatives and gear_rarity_script.exists():
        gear_rarity_text = read_text(gear_rarity_script)
        for expected_text in [
            "generated gear rarity metadata",
            "intentionally no-op",
            "manual_borders",
            "Do not set item.rarity",
        ]:
            if expected_text not in gear_rarity_text:
                errors.append(f"kubejs/startup_scripts/ascendant_gear_rarity.js is missing {expected_text}.")
        for forbidden_text in ["ItemEvents.modification", "event.modify(", "item.rarity ="]:
            if forbidden_text in gear_rarity_text:
                errors.append(
                    "kubejs/startup_scripts/ascendant_gear_rarity.js must not mutate item rarity "
                    f"with {forbidden_text}; custom mod item classes can crash KubeJS startup."
                )

    gear_tooltip_script = ROOT / "kubejs/client_scripts/ascendant_rarity_tooltips.js"
    if "mods/kubejs.pw.toml" in active_relatives and gear_tooltip_script.exists():
        gear_tooltip_text = read_text(gear_tooltip_script)
        for expected_text in [
            "ASCENDANT_RARITY_TOOLTIPS",
            "ItemEvents.tooltip",
            "event.addAdvanced",
            "buildAscendantRarityLines",
            "insertAscendantRarityLine",
            '"label"',
            '"MYTHIC"',
            '"ASCENDANT"',
            "Legendary Tooltips styles the tooltip frame",
        ]:
            if expected_text not in gear_tooltip_text:
                errors.append(f"kubejs/client_scripts/ascendant_rarity_tooltips.js is missing {expected_text}.")
        for forbidden_text in [
            "ItemEvents.modification",
            "event.modify(",
            "item.rarity =",
            "Object.entries(ASCENDANT_RARITY_TOOLTIPS)",
            "data.aura",
            "data.effect",
            "data.index",
            "data.reason",
            "Effect:",
            "Index:",
            "Why:",
            "MYTHIC FLAME",
            "ASCENDANT PULSE",
            "§k",
            "\\u003c",
            "<>",
            "Gilded late-game reward",
        ]:
            if forbidden_text in gear_tooltip_text:
                errors.append(
                    "kubejs/client_scripts/ascendant_rarity_tooltips.js must only add tooltip text "
                    f"and must not contain {forbidden_text}."
                )

    jei_alias_script = ROOT / "kubejs/client_scripts/ascendant_jei_aliases.js"
    if "mods/kubejs.pw.toml" in active_relatives and jei_alias_script.exists():
        jei_alias_text = read_text(jei_alias_script)
        for expected_text in [
            "ASCENDANT_RUNIC_GRIMOIRE",
            "patchouli:guide_book",
            "simplyswords:runic_grimoire",
            "JEIEvents.addItems",
            "ItemEvents.tooltip",
        ]:
            if expected_text not in jei_alias_text:
                errors.append(f"kubejs/client_scripts/ascendant_jei_aliases.js is missing {expected_text}.")
        if "useNBTKey" in jei_alias_text or "JEIEvents.subtypes" in jei_alias_text:
            errors.append(
                "kubejs/client_scripts/ascendant_jei_aliases.js must not register a Patchouli guide_book subtype; "
                "Patchouli/JEI already owns that interpreter and duplicate registration errors on startup."
            )
        if "JEIEvents.information" in jei_alias_text:
            errors.append(
                "kubejs/client_scripts/ascendant_jei_aliases.js must not use JEIEvents.information for the "
                "NBT-backed Runic Grimoire alias; JEI reports an empty ingredient for that info page."
            )
        for forbidden_text in ["Effect:", "Index:", "Why:", "MYTHIC FLAME", "ASCENDANT PULSE", "§k", "\\u003c", "<>"]:
            if forbidden_text in jei_alias_text:
                errors.append(
                    "kubejs/client_scripts/ascendant_jei_aliases.js should keep guide item tooltips player-facing "
                    f"and must not contain {forbidden_text}."
                )

    major_bountiful_objectives = (
        ROOT
        / "config/openloader/data/ascendant_realms_guild/data/bountiful/bounty_pools/ascendant_guild/ar_major_guild_objs.json"
    )
    if major_bountiful_objectives.exists():
        major_bountiful_text = read_text(major_bountiful_objectives)
        for forbidden_text in ["major_contract_08_black_frost", "iceandfire:black_frost_dragon"]:
            if forbidden_text in major_bountiful_text:
                errors.append(
                    "Ascendant Guild major Bountiful objectives must not use the runtime-invalid "
                    f"Black Frost objective entry: {forbidden_text}"
                )

    for path in sorted(metadata_files):
        relative = rel(path)
        text_raw = read_text(path)
        text = text_raw.lower()
        if relative not in ALLOWED_PACKWIZ_METADATA:
            errors.append(
                "Non-approved Batch A/B/C/D/E1/E2/F/G/H/J/K/L/M/N, Guild/Hunter, or world/menu polish metadata "
                f"is active: {relative}"
            )
        expected_side = EXPECTED_SIDE.get(relative)
        actual_side = metadata_side(text_raw)
        if expected_side and actual_side != expected_side:
            errors.append(f"{relative} has side={actual_side!r}; expected {expected_side!r}.")
        for slug in FORBIDDEN_ACTIVE_SLUGS:
            slug_pattern = slug.replace("-", "[-_ ]?")
            if re.search(slug_pattern, text) or re.search(slug_pattern, path.name.lower()):
                errors.append(f"Forbidden current-phase mod metadata detected: {relative}")

    if mods_dir.exists():
        for path in mods_dir.glob("*.pw.toml"):
            text = read_text(path).lower()
            for slug in FORBIDDEN_ACTIVE_SLUGS:
                if slug in text or slug in path.name.lower():
                    errors.append(f"Forbidden active mod metadata detected: {rel(path)}")

    dist_dir = ROOT / "dist"
    if dist_dir.exists():
        exported = list(dist_dir.rglob("*.zip")) + list(dist_dir.rglob("*.mrpack"))
        if exported:
            warnings.append("dist/ contains exported pack files. Remove them after validation unless intentionally keeping them.")

    for doc, pattern in EXPECTED_DOC_PATTERNS:
        path = ROOT / doc
        if path.exists() and not re.search(pattern, read_text(path), re.IGNORECASE):
            warnings.append(f"{doc} does not mention expected pattern: {pattern}")

    for doc, pattern, message in FORBIDDEN_DOC_PATTERNS:
        path = ROOT / doc
        if path.exists() and re.search(pattern, read_text(path), re.IGNORECASE):
            errors.append(f"{doc} has stale wording: {message}")

    readme_path = ROOT / "README.md"
    if readme_path.exists():
        readme_text = read_text(readme_path)
        if len(readme_text) > README_MAX_CHARS:
            warnings.append(
                f"README.md is {len(readme_text)} characters; keep it short and move running history to docs/archive/BATCH_HISTORY.md."
            )
        for pattern in README_HANDOFF_SPAM_PATTERNS:
            if re.search(pattern, readme_text):
                warnings.append(
                    "README.md appears to contain old running batch/handoff narrative. "
                    "Keep README short and archive history in docs/archive/BATCH_HISTORY.md."
                )
                break

    testing_checklist_path = ROOT / "docs/TESTING_CHECKLIST.md"
    if testing_checklist_path.exists():
        headings: dict[str, int] = {}
        for match in re.finditer(r"(?m)^##\s+(.+?)\s*$", read_text(testing_checklist_path)):
            heading = match.group(1).strip().lower()
            headings[heading] = headings.get(heading, 0) + 1
        duplicate_headings = sorted(heading for heading, count in headings.items() if count > 1)
        if duplicate_headings:
            warnings.append(
                "docs/TESTING_CHECKLIST.md contains duplicate section headings: "
                f"{ascendant_loot_preview(duplicate_headings)}"
            )

    current_status_path = ROOT / "docs/CURRENT_STATUS.md"
    if current_status_path.exists():
        current_status_text = read_text(current_status_path)
        for pattern in CURRENT_STATUS_BLOCKER_PATTERNS:
            if not re.search(pattern, current_status_text, re.IGNORECASE):
                warnings.append(
                    "docs/CURRENT_STATUS.md may be missing the current terrain blocker context: "
                    f"{pattern}"
                )

    docs_to_lint = [
        *ROOT.glob("*.md"),
        *ROOT.glob("docs/**/*.md"),
        *ROOT.glob("config/**/*.md"),
        *ROOT.glob("openloader/**/*.md"),
        *ROOT.glob("local-mods/**/*.md"),
        *ROOT.glob("kubejs/**/*.md"),
    ]
    for path in docs_to_lint:
        try:
            relative = rel(path)
        except ValueError:
            continue
        if relative.startswith("dist/") or relative.startswith("docs/archive/"):
            continue
        text = read_text(path)
        for stale_re, message in STALE_CURRENT_HELPER_PATTERNS:
            if stale_re.search(text):
                warnings.append(f"{relative} has potentially stale documentation wording: {message}")
                break
        for line_number, line in enumerate(text.splitlines(), start=1):
            if "dist/" not in line:
                continue
            if DOC_DIST_SOURCE_RE.search(line) and not DOC_DIST_NEGATION_RE.search(line):
                warnings.append(
                    f"{relative}:{line_number} may reference dist/ as source. "
                    "Docs under dist/ are generated exports, not authoritative source."
                )
                break

    print()
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
        print()

    if errors:
        print("Blocking issues:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

