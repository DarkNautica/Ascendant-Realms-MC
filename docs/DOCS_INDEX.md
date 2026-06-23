# Docs Index

Use this index to avoid treating every Markdown file as equally current.

Read source docs from the repo root. Ignore duplicate Markdown files under `dist/server-pack-staging/`; those are generated export copies and can lag until the next server-pack export.

## Start Here

- `docs/CURRENT_STATUS.md` - current handoff, latest fixes, and retest checklist.
- `docs/ATLAS_RANDOM_WORLDGEN_RESTORE.md` - current rollback from Atlas-directed terrain to random Tectonic/Terralith generation.
- `docs/ATLAS_TERRAIN_VALIDATION_REPORT.md` - historical terrain-first Atlas source checks and why Atlas terrain steering is no longer the active signoff path.
- `docs/ATLAS_BIOME_POOL_REPORT.md` - resolved active Atlas biome pools with audit-backed temperature, precipitation, terrain, and snow-risk data.
- `docs/ATLAS_WORLDGEN_FAILURES.md` - historical terrain-foundation blockers and the reason random generation was restored.
- `docs/ATLAS_WATER_REVIEW.md` - manual water sample review, accepted rivers/lakes, and confirmed south/west ocean-leak evidence.
- `docs/ATLAS_LAND_WATER_COHERENCE.md` - current land/water stack diagnosis, natural density-bias prototype, probe command path, and fresh-world validation gate.
- `docs/ATLAS_HYDROLOGY_MODEL.md` - historical hydrology-first biome selection model from the rejected Atlas helper path.
- `docs/ATLAS_BIOME_SELECTION_PIPELINE.md` - historical helper selection order and diagnostics from the rejected Atlas helper path.
- `docs/ATLAS_REGION_GRADIENTS.md` - historical continuous region weights and transect validation rules.
- `docs/ATLAS_HYDROLOGY_VALIDATION.md` - historical hydrology reports and invalid-ocean checks.
- `docs/ATLAS_GRADIENT_TRANSITION_VALIDATION.md` - historical transition transects from the rejected gradient path.
- `docs/ATLAS_TERRAIN_NOISE_CONTROL_PLAN.md` - historical terrain/noise fix plan; no longer active while random generation is restored.
- `docs/ATLAS_TERRAIN_NOISE_WRAPPER_PROTOTYPE.md` - failed Option C terrain correction prototype, rollback, commands, and why post-generation block filling is rejected.
- `docs/ATLAS_TERRAIN_NOISE_RESEARCH.md` - active Overworld, helper, Tectonic/Terratonic, density hook, noise-settings, and basin-root-cause research.
- `docs/ATLAS_TECTONIC_INTEGRATION_RISK.md` - risk matrix, rollback plan, and Tectonic-preservation guardrails for terrain/noise prototypes.
- `README.md` - short project overview, hard rules, validation commands, and current doc entry points.
- `AGENTS.md` - standing rules for future Codex sessions.
- `docs/TESTING_CHECKLIST.md` - in-game and server validation checklist.
- `docs/SYSTEM_ECOSYSTEM_OVERVIEW.md` - current layer-by-layer ecosystem map.
- `docs/AI_MODPACK_HANDOFF.md` - full mod list, interaction hotspots, category breakdown, and AI handoff map.
- `docs/MORNING_HANDOFF.md` - overnight summary for Jayden, now with a short post-morning Atlas update for the latest five-command terrain run.
- `docs/DOCUMENTATION_CLEANUP_REPORT.md` - latest documentation cleanup findings and navigation rules.
- `docs/KEYBIND_REEVALUATION.md` - current keybind cleanup, conflict decisions, active controls, and test checklist.
- `docs/MAGIC_UI_SKILL_HANDOFF.md` - compact AI handoff for Iron's Spells, Puffish Skills, rarity/UI surfaces, keybinds, and live-versus-audit boundaries.
- `docs/DEATH_WAYPOINT_UI_POLICY.md` - active Xaero deathpoint clutter cleanup; current death stays visible while old deathpoints are hidden from world UI.
- `docs/VILLAGE_AUDIO_REVERB_FIX.md` - staged Sound Physics tuning to stop villages from sounding like caves; sync pending while Minecraft is running.
- `docs/MOB_SPAWN_DENSITY_PASS.md` - current live spawn-density pass and testing checklist.
- `docs/HOSTILE_DAY_SPAWN_PASS.md` - active In Control daytime/cave hostile injection pass.
- `docs/REGIONAL_SPAWN_DIFFICULTY_PASS.md` - active Atlas region/ring difficulty multiplier pass; CRD/day-count scaling remains disabled.
- `docs/OVERWORLD_MOB_SPAWN_COVERAGE.md` - current evidence-based answer for vanilla/modded overworld spawn coverage; not every intended mob is signed off yet.
- `docs/RANK_NAMEPLATE_AND_EXAMINER_SYSTEM.md` - live Ascendant Nametags player/AI-hunter rank renderer, self-preview command, CustomNPC fallback, and Rank Examiner evaluation bridge.
- `docs/AI_HUNTER_DIRECTOR.md` - live helper v1 for ranked AI hunter encounter spawning, nameplate preview testing, and current limitations.
- `docs/NPC_RELATIONSHIP_AND_BEHAVIOR.md` - live CustomNPC relationship/command-boundary policy; NPCs do not instantly follow or obey players.
- `docs/ASCENDANT_RANKED_DUNGEONS.md` - current ranked dungeon foundation, rank model, command surface, and why random rifts are not autonomous yet.
- `docs/DUNGEON_PORTAL_SYSTEM.md` - Immersive Portals ownership, item-display gate visuals, portal safety rules, and controlled-rift acceptance path.
- `docs/ASCENDANT_DUNGEON_HOLOGRAMS.md` - Elite Holograms ownership for styled world-space dungeon rank text.
- `docs/ASCENDANT_DUNGEON_SPAWN_TESTING.md` - current manual spawn-test commands for visible ranked dungeon entrances, animated gates, holograms, reports, and cleanup.
- `docs/ASCENDANT_DUNGEON_DIMENSIONS.md` - current generated dungeon dimension, `/ascdungeon open_test_rift`, safe entry room, modded enemy pools, rank-bounded loot tables, boss-room, return-gate, and cleanup test route.

## Current Authoritative Plans

- `docs/ASCENDANT_ATLAS_WORLDGEN.md` - Atlas runtime and disabled coordinate-aware worldgen boundary.
- `docs/ATLAS_RANDOM_WORLDGEN_RESTORE.md` - authoritative current terrain direction: random Tectonic/Terralith generation, with Atlas worldgen influence disabled.
- `docs/ASCENDANT_CORE_INTEGRATION.md` - data-first core bridge, scoreboards, rank/proof ownership, custom-module threshold.
- `docs/GUILD_HUNTER_SYSTEM_RUNDOWN.md` - Guild ranks, Hunter Boards, rival hunters, NPCs, Codex, and settlement goals.
- `docs/VILLAGE_AND_CITY_INTEGRATION.md` - village/city stack, Integrated Villages risk notes, Guild structure pilot.
- `docs/STRUCTURE_DENSITY_TUNING.md` - Sparse Structures, Towns and Towers, Integrated Villages, and Guild spacing.
- `docs/KNOWN_RISKS.md` - larger risk register.
- `docs/MOB_SPAWN_DENSITY_PASS.md` - active high-density spawn tuning for Spawn Balance Utility, Majrusz, In Control caps, hostile spawner rules, and regional difficulty.
- `docs/HOSTILE_DAY_SPAWN_PASS.md` - active hostile daytime/cave spawner rules using daylight-safe modded surface pools and cave-native monster reinforcement.
- `docs/REGIONAL_SPAWN_DIFFICULTY_PASS.md` - active Atlas region/ring hostile pressure bridge; no time/day-count difficulty ramp.
- `docs/OVERWORLD_MOB_SPAWN_COVERAGE.md` - generated coverage audit separating verified natural/injected spawns from structure/event, non-natural helper entities, and unresolved spawn candidates.

## Generated Or Registry-Like Docs

- [RECIPE_PROGRESSION_AUDIT.md](RECIPE_PROGRESSION_AUDIT.md) - Generated recipe progression audit summary.
- [CRAFTING_GATE_PLAN.md](CRAFTING_GATE_PLAN.md) - Authoritative candidate crafting gate plan.
- [BROKEN_OR_EASY_RECIPE_REPORT.md](BROKEN_OR_EASY_RECIPE_REPORT.md) - Generated high-risk recipe report.
- [ASCENDANT_STRUCTURE_TIERING.md](ASCENDANT_STRUCTURE_TIERING.md) - Authoritative structure region, tier, danger, rank, loot, and density policy scaffold.
- [STRUCTURE_DENSITY_AND_REGION_AUDIT.md](STRUCTURE_DENSITY_AND_REGION_AUDIT.md) - Generated structure spacing, density, and region-fit audit.
- [STRUCTURE_CONFLICTS_AND_OVERLAPS.md](STRUCTURE_CONFLICTS_AND_OVERLAPS.md) - Generated overlap and conflict-risk register.
- [ASCENDANT_STRUCTURE_DIRECTOR.md](ASCENDANT_STRUCTURE_DIRECTOR.md) - Authoritative v1 structure director across region, vertical layer, water/sky, danger, loot, density, and review-only candidates.
- [STRUCTURE_REGION_AND_LAYER_INDEX.md](STRUCTURE_REGION_AND_LAYER_INDEX.md) - Generated Atlas region and vertical-layer index for every classified structure.
- [STRUCTURE_DENSITY_IMPLEMENTATION_REPORT.md](STRUCTURE_DENSITY_IMPLEMENTATION_REPORT.md) - Review-only density implementation candidate report; no live structure-set overrides enabled.
- [WATER_AND_SKY_STRUCTURES.md](WATER_AND_SKY_STRUCTURES.md) - Water, sea-floor, ship/ocean-surface, wetland, coastline, and sky structure policy report.
- [STRUCTURE_LOOT_AND_DANGER_TIERS.md](STRUCTURE_LOOT_AND_DANGER_TIERS.md) - Structure danger, Guild rank, loot tier, and rarity ceiling policy report.
- [STRUCTURE_TESTING_CHECKLIST.md](STRUCTURE_TESTING_CHECKLIST.md) - Fresh-world structure validation checklist and manual review workflow.
- [STRUCTURE_VISUAL_REVIEW_ROUTE.md](STRUCTURE_VISUAL_REVIEW_ROUTE.md) - First in-game Structure Director review route with sections, priority queues, and manual visual questions.
- [STRUCTURE_DIRECTOR_REVIEW_RESULTS_TEMPLATE.md](STRUCTURE_DIRECTOR_REVIEW_RESULTS_TEMPLATE.md) - Manual result template for each located structure.
- [STRUCTURE_VISUAL_REVIEW_FINDINGS.md](STRUCTURE_VISUAL_REVIEW_FINDINGS.md) - Jayden's first Structure Director field-review findings and source-only classification correction.
- [STRUCTURE_CLASSIFICATION_EVIDENCE_RULES.md](STRUCTURE_CLASSIFICATION_EVIDENCE_RULES.md) - Evidence contract: names/path/mod labels are weak hints only, and sensitive structure classifications need non-name evidence.
- [STRUCTURE_CLASSIFICATION_AUDIT_REPORT.md](STRUCTURE_CLASSIFICATION_AUDIT_REPORT.md) - Generated evidence/confidence audit, Ice and Fire correction, IDAS override handling, and manual review queue.
- [STRUCTURE_DIRECTOR_LIVE_V1.md](STRUCTURE_DIRECTOR_LIVE_V1.md) - Current live Structure Director implementation: OpenLoader datapack overrides, live policy, limits, and known manual fixes.
- [STRUCTURE_DIRECTOR_LIVE_CHANGELOG.md](STRUCTURE_DIRECTOR_LIVE_CHANGELOG.md) - Live v1 change summary.
- [STRUCTURE_DIRECTOR_ROLLBACK.md](STRUCTURE_DIRECTOR_ROLLBACK.md) - Enable/disable/rollback instructions for Structure Director Live v1.
- [STRUCTURE_DIRECTOR_LIVE_V1_TESTING.md](STRUCTURE_DIRECTOR_LIVE_V1_TESTING.md) - Fresh-world test route for live structure changes.
- [ASCENDANT_TRAVEL_NETWORK_AUDIT.md](ASCENDANT_TRAVEL_NETWORK_AUDIT.md) - Authoritative road, bridge, river, and terrain-seam reconnaissance scaffold.
- [ROAD_BRIDGE_RIVER_FAILURES.md](ROAD_BRIDGE_RIVER_FAILURES.md) - Generated travel failure and field-evidence register.
- [TRAVEL_NETWORK_DESIGN_RULES.md](TRAVEL_NETWORK_DESIGN_RULES.md) - Future regional travel-network design rules.
- [ASCENDANT_REGIONAL_ATMOSPHERE.md](ASCENDANT_REGIONAL_ATMOSPHERE.md) - Authoritative regional weather, music, ambience, title, and visual-feedback scaffold.
- [WEATHER_AND_SEASON_REGION_POLICY.md](WEATHER_AND_SEASON_REGION_POLICY.md) - Weather, season, snow, and ice guardrail policy.
- [BIOME_TITLE_AND_AUDIO_POLICY.md](BIOME_TITLE_AND_AUDIO_POLICY.md) - Biome/title/audio policy and current implementation boundary.
- [ASCENDANT_MAGIC_PROGRESSION.md](ASCENDANT_MAGIC_PROGRESSION.md) - Authoritative magic progression, school/region, Guild rank, rarity, loot, and recipe policy scaffold.
- [SPELL_REGION_AND_RANK_INDEX.md](SPELL_REGION_AND_RANK_INDEX.md) - Generated spell-to-region and rank index.
- [MAGIC_LOOT_AND_RECIPE_AUDIT.md](MAGIC_LOOT_AND_RECIPE_AUDIT.md) - Generated magic loot and recipe risk audit.
- [GEAR_BALANCE_OUTLIER_REPORT.md](GEAR_BALANCE_OUTLIER_REPORT.md) - Authoritative gear balance outlier scaffold; audit-only, no stat or rarity changes.
- [RARITY_CONSISTENCY_AUDIT.md](RARITY_CONSISTENCY_AUDIT.md) - Generated rarity consistency audit across exposed stats and progression context.
- [GEAR_PROGRESSion_RISK_REGISTER.md](GEAR_PROGRESSion_RISK_REGISTER.md) - Generated progression-placement risk register for rank, loot, recipe, and boss-review candidates.
- [ASCENDANT_PLAYER_PROGRESSION.md](ASCENDANT_PLAYER_PROGRESSION.md) - Authoritative player progression bridge scaffold across Guild rank, Puffish Skills, Atlas regions, loot, gear, magic, bounties, and bosses.
- [GUILD_RANK_REQUIREMENT_MATRIX.md](GUILD_RANK_REQUIREMENT_MATRIX.md) - Generated public Guild rank requirement matrix; guidance only, no hard gates.
- [SKILL_TREE_INTEGRATION_PLAN.md](SKILL_TREE_INTEGRATION_PLAN.md) - Generated Puffish Skills to Guild rank integration plan.
- [RANK_NAMEPLATE_AND_EXAMINER_SYSTEM.md](RANK_NAMEPLATE_AND_EXAMINER_SYSTEM.md) - Live Ascendant Nametags renderer, self-preview command, rank team sync, NPC/rival hunter display path, and Rank Examiner evaluation command.
- [AI_HUNTER_DIRECTOR.md](AI_HUNTER_DIRECTOR.md) - Live helper v1 ranked AI hunter encounter director, commands, growth pulse, and nameplate preview notes.
- [NPC_VISUAL_VALIDATION_REPORT.md](NPC_VISUAL_VALIDATION_REPORT.md) - Authoritative NPC visual identity validation scaffold; audit-only, no NPC placement.
- [MCA_MEDIEVAL_SKIN_AUDIT.md](MCA_MEDIEVAL_SKIN_AUDIT.md) - MCA Default Medieval resource-pack evidence and medieval clothing asset count.
- [RIVAL_HUNTER_VISUAL_ROSTER.md](RIVAL_HUNTER_VISUAL_ROSTER.md) - Rival hunter rank, class, gear, nameplate, and drop-policy visual roster.
- [UI_CLARITY_AND_FEEDBACK_AUDIT.md](UI_CLARITY_AND_FEEDBACK_AUDIT.md) - Authoritative player-facing UI clarity scaffold for rarity, rank, level, region, loot value, mob danger, and progression feedback.
- [RARITY_TOOLTIP_VISUAL_POLICY.md](RARITY_TOOLTIP_VISUAL_POLICY.md) - Item Borders, KubeJS rarity tooltip, Legendary Tooltips, and Loot Beams visual policy.
- [MOB_DANGER_UI_POLICY.md](MOB_DANGER_UI_POLICY.md) - MobHealthBar, boss-bar, nameplate, and future threat-tier display policy.
- [REGION_TITLE_UI_POLICY.md](REGION_TITLE_UI_POLICY.md) - Traveler's Titles, title resource packs, and Atlas coordinate-region title boundary.
- [KEYBIND_REEVALUATION.md](KEYBIND_REEVALUATION.md) - Active keybind policy and collision cleanup.
- [MAGIC_UI_SKILL_HANDOFF.md](MAGIC_UI_SKILL_HANDOFF.md) - Magic/UI/skill handoff for future AI sessions.
- [DEATH_WAYPOINT_UI_POLICY.md](DEATH_WAYPOINT_UI_POLICY.md) - Xaero current-vs-old deathpoint visibility policy and active sync behavior.
- [ASCENDANT_RANKED_DUNGEONS.md](ASCENDANT_RANKED_DUNGEONS.md) - Ranked dungeon foundation using Immersive Portals, with `/ascdungeon` validation commands and random spawning still gated.
- [DUNGEON_PORTAL_SYSTEM.md](DUNGEON_PORTAL_SYSTEM.md) - Portal design, dependency status, animated gate visuals, and test-rift acceptance criteria.
- [ASCENDANT_DUNGEON_HOLOGRAMS.md](ASCENDANT_DUNGEON_HOLOGRAMS.md) - Elite Holograms policy for floating rank/name/danger/loot labels above dungeon rifts.
- [ASCENDANT_DUNGEON_SPAWN_TESTING.md](ASCENDANT_DUNGEON_SPAWN_TESTING.md) - Manual in-world ranked entrance spawn-test commands, animated gate visuals, and visual review rules.
- [ASCENDANT_DUNGEON_DIMENSIONS.md](ASCENDANT_DUNGEON_DIMENSIONS.md) - Generated dungeon dimension and playable `/ascdungeon open_test_rift` test loop with force-loaded build safety, safe entry room, modded enemies, and rank-bounded loot.

These are useful, but should be regenerated or audited before making major balance decisions from them.

- `docs/UNIVERSAL_MOD_INDEX.md`
- `docs/STRUCTURE_INDEX.md`
- `docs/MOB_THREAT_INDEX.md`
- `docs/BOUNTY_TARGET_INDEX.md`
- `docs/ARMOR_INDEX.md`
- `docs/WEAPON_INDEX.md`
- `docs/MAGIC_INDEX.md`
- `docs/ACCESSORY_RELIC_INDEX.md`
- `docs/DEPENDENCY_GRAPH.md`
- `docs/WORLD_INTEGRATION_AUDIT.md`

## Consolidation Direction

- Keep `README.md` short enough to orient a new session quickly.
- Old batch-by-batch README narrative now lives in `docs/archive/BATCH_HISTORY.md`.
- Keep one active testing checklist instead of duplicate per-session fragments.
- Keep generated indexes grouped conceptually; move them under `docs/generated/` only in a dedicated reference-rewrite pass.
- Prefer `docs/CURRENT_STATUS.md` for handoff notes instead of adding more running status bullets to the README.
- Treat `docs/CURRENT_STATUS.md`, this index, and `docs/ASCENDANT_ATLAS_WORLDGEN.md` as the first read for worldgen work; older batch notes are historical unless one of these files points to them.

## Documentation Hygiene

- [MORNING_HANDOFF.md](MORNING_HANDOFF.md) - newest overnight handoff for Jayden; use before resuming gameplay validation.
- [DOCUMENTATION_CLEANUP_REPORT.md](DOCUMENTATION_CLEANUP_REPORT.md) - Documentation cleanup findings, stale-doc risks, and validation rules.
- [archive/BATCH_HISTORY.md](archive/BATCH_HISTORY.md) - Archived former README batch/session narrative. Use for historical archaeology only.


## Loot Economy Docs

- [ASCENDANT_LOOT_ECONOMY.md](ASCENDANT_LOOT_ECONOMY.md) - Authoritative loot/reward economy policy scaffold.
- [LOOT_TABLE_AUDIT.md](LOOT_TABLE_AUDIT.md) - Generated loot table audit summary.
- [STRUCTURE_REWARD_TIER_INDEX.md](STRUCTURE_REWARD_TIER_INDEX.md) - Generated structure reward tier index.

## Ranked Dungeon Docs

- [ASCENDANT_RANKED_DUNGEONS.md](ASCENDANT_RANKED_DUNGEONS.md) - Active foundation for random ranked dungeon rifts. Controlled random world rift testing is enabled with one active rift per rank, fixed-facing rank-scaled gate art, timed entrances, and boss-locked return gates.
- [DUNGEON_PORTAL_SYSTEM.md](DUNGEON_PORTAL_SYSTEM.md) - Immersive Portals integration plan, current dependency status, item-display gate visuals, safety rules, manual entrance test, and next return-safe portal step.
- [ASCENDANT_DUNGEON_HOLOGRAMS.md](ASCENDANT_DUNGEON_HOLOGRAMS.md) - Elite Holograms integration for world-space ranked dungeon text. Manual test creation is active; autonomous permanent holograms remain gated.
- [ASCENDANT_DUNGEON_SPAWN_TESTING.md](ASCENDANT_DUNGEON_SPAWN_TESTING.md) - Exact manual spawn-test commands, cleanup command, animated gate visual check, and what Jayden should inspect.
- [ASCENDANT_DUNGEON_DIMENSIONS.md](ASCENDANT_DUNGEON_DIMENSIONS.md) - Current generated dungeon instance command, forced random rift test path, dimension, force-loaded build safety, safe entry room, rank scaling, modded mobs, bounded loot, boss-room rule, boss-locked return gate, and cleanup path.

## Structure Control Docs

- [ASCENDANT_STRUCTURE_DIRECTOR.md](ASCENDANT_STRUCTURE_DIRECTOR.md) - V1 structure director; start here for structure region, layer, water/sky, density, danger, and review candidate decisions.
- [STRUCTURE_REGION_AND_LAYER_INDEX.md](STRUCTURE_REGION_AND_LAYER_INDEX.md) - Region and vertical-layer map for structures.
- [STRUCTURE_DENSITY_IMPLEMENTATION_REPORT.md](STRUCTURE_DENSITY_IMPLEMENTATION_REPORT.md) - Disabled density/spacings candidate report.
- [WATER_AND_SKY_STRUCTURES.md](WATER_AND_SKY_STRUCTURES.md) - Water, sea-floor, ship, coastline, wetland, and sky structure policy.
- [STRUCTURE_LOOT_AND_DANGER_TIERS.md](STRUCTURE_LOOT_AND_DANGER_TIERS.md) - Danger and reward tier policy for dungeons, bosses, and major structures.
- [STRUCTURE_TESTING_CHECKLIST.md](STRUCTURE_TESTING_CHECKLIST.md) - Fresh-world manual structure testing workflow.
- [STRUCTURE_VISUAL_REVIEW_ROUTE.md](STRUCTURE_VISUAL_REVIEW_ROUTE.md) - First route to validate structure placement in game; review-only, no live overrides.
- [STRUCTURE_DIRECTOR_REVIEW_RESULTS_TEMPLATE.md](STRUCTURE_DIRECTOR_REVIEW_RESULTS_TEMPLATE.md) - Copyable manual review template for structure screenshots and pass/fail notes.
- [STRUCTURE_VISUAL_REVIEW_FINDINGS.md](STRUCTURE_VISUAL_REVIEW_FINDINGS.md) - Latest manual field evidence: dragon roost/vineyard island placement issues, acceptable IDAS labyrinth override, and corrected Ice and Fire water classification.
- [STRUCTURE_CLASSIFICATION_EVIDENCE_RULES.md](STRUCTURE_CLASSIFICATION_EVIDENCE_RULES.md) - Required Structure Director evidence rules; name/path/mod-label hints are never authoritative.
- [STRUCTURE_CLASSIFICATION_AUDIT_REPORT.md](STRUCTURE_CLASSIFICATION_AUDIT_REPORT.md) - Evidence-backed classification audit and confidence summary.
- [ASCENDANT_STRUCTURE_TIERING.md](ASCENDANT_STRUCTURE_TIERING.md) - Structure tier, Atlas region, danger, Guild rank, loot, and density policy scaffold.
- [STRUCTURE_DENSITY_AND_REGION_AUDIT.md](STRUCTURE_DENSITY_AND_REGION_AUDIT.md) - Structure set spacing and density-risk review.
- [STRUCTURE_CONFLICTS_AND_OVERLAPS.md](STRUCTURE_CONFLICTS_AND_OVERLAPS.md) - Conflict and overlap review list.

## Travel Network Docs

- [ASCENDANT_TRAVEL_NETWORK_AUDIT.md](ASCENDANT_TRAVEL_NETWORK_AUDIT.md) - Road/path, bridge, water crossing, and terrain-seam audit.
- [ROAD_BRIDGE_RIVER_FAILURES.md](ROAD_BRIDGE_RIVER_FAILURES.md) - Failure register for road, bridge, river, cliff, and route-purpose issues.
- [TRAVEL_NETWORK_DESIGN_RULES.md](TRAVEL_NETWORK_DESIGN_RULES.md) - Regional travel-network rules for later implementation.

## Regional Atmosphere Docs

- [ASCENDANT_REGIONAL_ATMOSPHERE.md](ASCENDANT_REGIONAL_ATMOSPHERE.md) - Atlas-region atmosphere matrix for weather, music, ambience, titles, seasons, and danger mood.
- [WEATHER_AND_SEASON_REGION_POLICY.md](WEATHER_AND_SEASON_REGION_POLICY.md) - Weather2, Serene Seasons, Snow Real Magic, snow/ice, and seasonal guardrails.
- [BIOME_TITLE_AND_AUDIO_POLICY.md](BIOME_TITLE_AND_AUDIO_POLICY.md) - Traveler's Titles, Titles, audio layers, and coordinate-region title boundary.
- [VILLAGE_AUDIO_REVERB_FIX.md](VILLAGE_AUDIO_REVERB_FIX.md) - Sound Physics Remastered tuning for village echo/reverb; source staged, active sync pending until Minecraft is closed.

## Magic Progression Docs

- [ASCENDANT_MAGIC_PROGRESSION.md](ASCENDANT_MAGIC_PROGRESSION.md) - Magic-school, Atlas-region, Guild-rank, rarity, loot, and recipe policy scaffold.
- [SPELL_REGION_AND_RANK_INDEX.md](SPELL_REGION_AND_RANK_INDEX.md) - Every indexed spell mapped to school, region affinity, rank, and acquisition route.
- [MAGIC_LOOT_AND_RECIPE_AUDIT.md](MAGIC_LOOT_AND_RECIPE_AUDIT.md) - Magic loot and recipe warnings, including disabled review-only candidate notes.

## Gear Balance Docs

- [GEAR_BALANCE_OUTLIER_REPORT.md](GEAR_BALANCE_OUTLIER_REPORT.md) - Balance outlier report for weapons, armor, shields, magic items, accessories, relics, and spells.
- [RARITY_CONSISTENCY_AUDIT.md](RARITY_CONSISTENCY_AUDIT.md) - Rarity-vs-stat and rarity-vs-context review queue; do not treat it as automatic rarity regeneration.
- [GEAR_PROGRESSion_RISK_REGISTER.md](GEAR_PROGRESSion_RISK_REGISTER.md) - Progression risk register for rank-gate, boss-reward, missing-stat, missing-loot, and missing-recipe review.

## Player Progression Docs

- [ASCENDANT_PLAYER_PROGRESSION.md](ASCENDANT_PLAYER_PROGRESSION.md) - Unified progression spine for Guild rank, skills, regions, mobs, bounty tiers, gear, magic, and boss milestones.
- [GUILD_RANK_REQUIREMENT_MATRIX.md](GUILD_RANK_REQUIREMENT_MATRIX.md) - Rank-by-rank public evaluation matrix from Unranked through S-Rank.
- [SKILL_TREE_INTEGRATION_PLAN.md](SKILL_TREE_INTEGRATION_PLAN.md) - Puffish Skills integration plan that keeps skill growth separate from public Guild rank.
- [RANK_NAMEPLATE_AND_EXAMINER_SYSTEM.md](RANK_NAMEPLATE_AND_EXAMINER_SYSTEM.md) - Live Forge-safe nameplate fallback, rank team sync, NPC/rival hunter display path, and Rank Examiner evaluation command.

## NPC Visual Identity Docs

- [NPC_VISUAL_VALIDATION_REPORT.md](NPC_VISUAL_VALIDATION_REPORT.md) - NPC visual identity validation report covering MCA Reborn, MCA Default Medieval, Easy NPC, CustomNPCs, Human Companions, Guard Villagers, Villager Names, loadouts, nameplates, and gear references.
- [NPC_RELATIONSHIP_AND_BEHAVIOR.md](NPC_RELATIONSHIP_AND_BEHAVIOR.md) - Live v1 relationship behavior for generated CustomNPC Guild/Hunter profiles, including trust tiers, role boundaries, and the no-instant-orders rule.
- [MCA_MEDIEVAL_SKIN_AUDIT.md](MCA_MEDIEVAL_SKIN_AUDIT.md) - MCA medieval resource-pack activation and clothing asset audit; manual in-game villager visual review is still required.
- [RIVAL_HUNTER_VISUAL_ROSTER.md](RIVAL_HUNTER_VISUAL_ROSTER.md) - Named rival hunter visual roster with rank, class, gear tier, loadout, nameplate, and drop policy.

## UI Clarity Docs

- [UI_CLARITY_AND_FEEDBACK_AUDIT.md](UI_CLARITY_AND_FEEDBACK_AUDIT.md) - Player-facing UI clarity audit covering Item Borders, Legendary Tooltips, JEI, Loot Beams, Loot Journal, MobHealthBar, Overflowing Bars, Traveler's Titles, Titles, Immersive UI, SpiffyHUD, FancyMenu, resource-pack order, rarity tooltips, and nameplate integration.
- [RARITY_TOOLTIP_VISUAL_POLICY.md](RARITY_TOOLTIP_VISUAL_POLICY.md) - Canonical rarity palette and tooltip/border/beam policy; audit-only, no broad visual rewrite.
- [MOB_DANGER_UI_POLICY.md](MOB_DANGER_UI_POLICY.md) - Mob danger readability policy; threat-tier overlay remains future/policy-only.
- [REGION_TITLE_UI_POLICY.md](REGION_TITLE_UI_POLICY.md) - Region title presentation policy; biome/dimension titles are live, Atlas coordinate-region titles are not live-triggered yet.
- [KEYBIND_REEVALUATION.md](KEYBIND_REEVALUATION.md) - Current keybind layout, conflict decisions, and test checklist.
- [MAGIC_UI_SKILL_HANDOFF.md](MAGIC_UI_SKILL_HANDOFF.md) - Short AI handoff tying magic, UI, rarity, skill tree, rank/progression, and keybind policy together.
