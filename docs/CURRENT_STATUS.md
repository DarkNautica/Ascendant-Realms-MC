# Current Status

Last updated: 2026-06-18.

This is the short handoff for the next Ascendant Realms work session. Use it before diving into the deeper batch docs.

## Active Target

- Minecraft: 1.20.1.
- Loader: Forge 47.4.20.
- Pack version: 0.1.0-alpha.
- Latest active CurseForge instance: `C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)`.
- Current pack shape: vanilla+++ medieval fantasy RPG exploration for two-player multiplayer.
- Current terrain direction: random Tectonic/Terralith Overworld generation restored. Atlas north/south/east/west terrain and biome steering is disabled.
- Sync status for this pass: source has removed the Atlas Overworld dimension override and Atlas `minecraft:overworld/continents` land-bias override. Active `Ascendant Realms (2)` has also received the current client keybind policy.
- Login stability fix synced: `config/alexsmobs.toml` now has `giveBookOnStartup=false` in source and the active instance, preventing the Alex's Mobs first-login book grant from triggering the observed invalid-player-data bounce.
- Client keybind pass synced: `config/ascendant_ui/keybind_policy.json` is active in `Ascendant Realms (2)`. The latest active options scan found 202 keybind entries, 89 bound entries, and 0 duplicate bound-key groups. Core controls are `K` Ascendant Web, `L` Quest Log, `R` Iron's spell wheel, `V` spell cast, `Left Alt` spell modifier, `Z` Combat Roll, `B` backpack, `G` Curios, `U` waypoints, and `Y` minimap settings. Shader reload/toggle/selection and other non-gameplay menu/debug controls are intentionally unbound.
- Death waypoint clutter cleanup synced: Xaero's current deathpoint remains enabled, but old deathpoints are disabled/hidden by `config/ascendant_ui/death_waypoint_policy.json` and `scripts/sync-active-client-files.ps1`. This solves repeated-death screen clutter without using a global 100m waypoint cap that would also hide the recent death marker.
- Village audio reverb fix synced: `config/sound_physics_remastered/soundphysics.properties` now keeps Sound Physics enabled but reduces reverb gain, default reflectivity, reflection bounces, sound-distance allowance, and disables sound redirection that made villages sound cave-like. Source and active `Ascendant Realms (2)` both have the tuned values. See `docs/VILLAGE_AUDIO_REVERB_FIX.md`.
- Main menu edits preserved: Jayden's active FancyMenu/Drippy menu changes, including the current background/menu assets, were copied back from `Ascendant Realms (2)` into source before the latest sync. Source and active `config/fancymenu` now match with 0 file-hash mismatches, so future syncs should keep this menu work.
- Resource Pack Overrides mismatch fixed and synced: `file/ascendant-realms-buttons` is now included in `config/resourcepackoverrides.json`, matching `options.txt`.
- Pre-coop blockers fixed and synced: `kubejs/client_scripts/ascendant_jei_aliases.js` no longer has the extra closing `})`, the missing `projectvibrantjourneys:baobab_fields` entry is filtered from generated Structure Director Live biome tags, and source/active Structure Director Live v1 datapack hashes match at `540DD32065EE85CF861812B268BE567E51CB088112F1A844CD00569D570ABDDD`.
- Mob density and regional difficulty pass active in source: `docs/MOB_SPAWN_DENSITY_PASS.md`, `docs/HOSTILE_DAY_SPAWN_PASS.md`, `docs/REGIONAL_SPAWN_DIFFICULTY_PASS.md`, and `config/ascendant_core/spawn_density_policy.json` record the direction that ordinary exploration should show multiple mobs nearby. Spawn Balance Utility, Majrusz flat spawn-rate/group pressure, In Control cap ceilings, and `config/incontrol/spawner.json` hostile daytime/cave injection are active. CRD/day-count difficulty scaling remains disabled; regional pressure now comes from `config/ascendant_core/regional_difficulty_policy.json` plus `kubejs/server_scripts/ascendant_regional_difficulty.js`, which tags/buffs eligible hostiles by nearest-player Atlas region/ring. Boss/dragon-tier mobs remain controlled; no new mob mods were added.
- Overworld mob spawn coverage is now audited but not fully signed off. `docs/OVERWORLD_MOB_SPAWN_COVERAGE.md` and `config/ascendant_core/reports/overworld_mob_spawn_coverage_latest.json` prove the current state: 47 explicit In Control injected mobs, 92 natural/mod-config-evidence entries, and 42 tracked vanilla natural overworld defaults. The report still has 11 expected entries without spawn evidence and 8 entries needing manual classification, so do not claim every intended modded overworld mob is guaranteed naturally spawning yet.
- Ranked Dungeon rank-slot random world rifts are active in source and synced to `Ascendant Realms (2)`: Immersive Portals is Packwiz-managed and now used through circular teleportable helper-created portal surfaces, Elite Holograms is installed but helper auto-creation is suppressed, and `config/ascendant_dungeons/` owns rank/spawn/portal/hologram/template/dimension policy. The helper adds `/ascdungeon status`, `/ascdungeon roll <rank>`, `/ascdungeon preview_here <rank>`, `/ascdungeon spawn_test_here <rank>`, `/ascdungeon spawn_visual_here <rank>`, `/ascdungeon spawn_test_all_ranks <spacing>`, `/ascdungeon open_test_rift <rank>`, `/ascdungeon spawn_random_now`, `/ascdungeon enter_latest`, `/ascdungeon return_latest`, `/ascdungeon cleanup_instance`, `/ascdungeon cleanup_rank <rank>`, `/ascdungeon cleanup_test`, and `/ascdungeon dump_policy`. `spawn_test_here`, `open_test_rift`, and `spawn_random_now` create real generated dungeon instances whose intended travel path is the circular Immersive Portals entity; helper enter/return commands are fallback/admin tools only. `spawn_visual_here` and `spawn_test_all_ranks` are visual-only gate-art checks and do not teleport. Real dungeon rifts force-load and command-build a generated room-chain dungeon in `ascendant_dungeons:ranked_dungeon`, create a safe no-mob entry room, connected modded-decor combat rooms, rank-scaled modded enemy pools, rank-bounded chest/entity loot tables, mandatory boss room, boss-locked return gate, fallback enter/return commands, and cleanup. Natural world rifts now run as one active rift per rank: one D, one C, one B, one A, and one S can exist at the same time, for five active rifts total.
- Latest local helper sync: source and active `Ascendant Realms (2)` Atlas helper jar hash `EBF4B97EDA4DD6E067B2BDBCDF9C7E41C2DF1FEEA50BE942E131AE0DF7174D42`; source and active Ascendant Nametags jar hash `09FDA8EE3F7A7829AF22AD5BB285395315D9D67AF503F554C0E83562E5DEB9A3`.
- Latest ranked-dungeon source pass: helper code now creates circular Immersive Portals `specialShape` surfaces, marks them teleportable, disables helper walk-in travel when the Immersive Portal surface exists, uses transparent-center gate item textures, keeps the art fixed-facing, keeps the entrance open for 5 seconds after first entry, then shrinks the visible gate before removing it. The entrance cleanup now kills both front/back Immersive Portal surfaces plus a nearby safety sweep so invisible portal surfaces do not linger after the visible gate closes. Portal size ranges were bumped again by rank: D `3.8-4.7`, C `4.2-5.3`, B `4.9-6.4`, A `5.8-7.5`, and S `6.8-9.0`. Jayden visually signed off rifts for v1 on 2026-06-18; next dungeon work should focus on dungeon-side encounter/template polish, not portal visuals. Rank Examiner interaction has a Forge-side right-click bridge keyed off the spawned `ar_profile_rank_examiner` CustomNPC tag.
- Rank nameplate and Rank Examiner bridge added in source and synced. The attached CustomNameTags jar was inspected and is Fabric/server-side, so it was not installed into the Forge pack. The needed player/AI-hunter behavior now lives in the modular local Forge helper `ascendant-nametags-0.1.0.jar`: it renders player rank/name/level from `ar_guild_rank` and `ar_skill_level`, renders AI hunter rank/profile labels from synced tags or CustomNPC display/custom-name fallback, adds animated per-character rank gradients/glow effects, and adds `/ascnametag preview_self` so Jayden can see his own styled plate above his actual third-person model. AI hunters now use a level-stage world overlay fallback because CustomNPCs can bypass Forge's normal name-tag event. Health Bar Plus owns routine mob health bars while Ascendant Nametags owns styled rank/name identity over hunters. Vanilla scoreboard teams and `ar_skill_level` below-name remain as fallback/context; CustomNPCs scripted rank/name/level/role lines remain for authored NPCs. The `/function ascendant_identity:rank_examiner/evaluate` path is an admin/test hook only, not player-facing gameplay. See `docs/RANK_NAMEPLATE_AND_EXAMINER_SYSTEM.md`.
- AI Hunter Director v1 added in source helper. It adds `/aschunter status`, `/aschunter spawn_near <rank>`, `/aschunter spawn_random_now`, `/aschunter grow_near`, and `/aschunter cleanup_near`, plus a low-frequency overworld scheduler for ranked hunter encounters when no hunter is already nearby. The latest helper pass routes hunter spawning through known-good CustomNPC spawn functions, then applies hunter rank/profile tags and stats, so the earlier command parser failure should be fixed. A helper-side combat bridge now pulses near players, force-targeting AI hunters and nearby hostile mobs against each other so hunter field tests visibly fight. It writes `config/ascendant_guild/reports/ai_hunter_latest.json` and is documented in `docs/AI_HUNTER_DIRECTOR.md` and `config/ascendant_guild/ai_hunter_policy.json`. This creates ranked hunter encounters only; it does not place Hunter Boards, Guild Halls, roads, villages, or settlement content.
- Player nameplate self-preview commands added in `Ascendant Nametags`: `/ascnametag status`, `/ascnametag preview_self`, and `/ascnametag hide_preview`. Older `/ascidentity preview_nameplate` remains an admin/debug marker path, but the supported self-check is the new third-person in-world preview.
- Generated CustomNPC spawn functions now embed and enable the Ascendant identity script. This fixes the visual-only Rank Examiner failure where a spawned examiner only said the default `hello <player>` greeting instead of running Guild rank evaluation.
- NPC relationship/behavior v1 added in source and ready for active-client sync: generated Guild/Hunter CustomNPCs now track simple per-player familiarity, use role-specific dialogue, and refuse instant follow/order behavior. `config/CustomNpcs.cfg` is source-controlled with the generic `Hello @p` fallback disabled and normal CustomNPC edit/command tooling locked behind ops. Rank Examiner remains the one public-service interaction bridge. See `docs/NPC_RELATIONSHIP_AND_BEHAVIOR.md`.

## Current Reality

- Jayden rejected the Atlas coordinate-directed terrain approach after hard biome/terrain cuts remained visible. The pack is now reverting to random generation instead of continuing the compass-gradient system.
- `config/ascendant_atlas/worldgen_override_policy.json` is the authority switch. It currently sets `worldgen_override_enabled=false`, so the Atlas worldgen override is disabled.
- The removed source influence files are `config/openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json` and `config/openloader/data/ascendant_realms_atlas/data/minecraft/worldgen/density_function/overworld/continents.json`, plus the mirrored `openloader/data/...` copies.
- The `ascendant_atlas_regions` helper jar may remain installed for diagnostics/history, but it must not be referenced by active Overworld dimension or density-function JSON while random mode is selected.
- A fresh world is required to judge the rollback. Old chunks can preserve old Atlas-shaped terrain, old biome decisions, and old structure placement.
- Structure and road tuning can proceed against the random terrain baseline after the active instance is synced and a fresh world confirms the hard-cut issue is gone.
- Packwiz and the project checker must be rerun after this rollback and active sync.
- Structure Director Live v1 source files are now generated: `config/openloader/data/ascendant_structure_director_live/`, `config/ascendant_structures/live_structure_policy.json`, `config/ascendant_structures/live_structure_manifest.json`, and rollback snapshots under `config/ascendant_structures/rollback/pre_structure_director_v1/`.
- Structure Director Live v1 is active in newly generated worlds. Source and active live datapack hash: `7C6A5C40F73BA29EEEE58DDB480B2B273B98F27DB393AF04FB21663AEAFE9EE3`.
- Structure Director Live v1 changes newly generated chunks through 23 live datapack changes: dragon roost/cave/siren spacing, IDAS vineyard split, IDAS/YUNG/Cataclysm/Bosses density reductions, Aquamirae surface spacing, Towns and Towers settlement/outpost spacing, and evidence-resolved land/ocean biome tags.
- New helper commands are synced in active helper `242E889D`: `/ascatlas hydrology_here`, `/ascatlas biome_decision_here`, `/ascatlas region_weights_here`, `/ascatlas sample_transect <x1> <z1> <x2> <z2> <step>`, `/ascatlas dump_gradient_policy`, `/ascatlas dump_hydrology_registry`, plus the existing `/ascstructure status`, `/ascstructure rule <structure_id>`, `/ascstructure here`, `/ascstructure test_context <structure_id>`, `/ascstructure dump_live_manifest`, and `/ascstructure explain_last_denial`.
- Structure Director honesty boundary: Forge does not expose a safe structure placement veto event to the helper. Live v1 is real datapack/worldgen control plus helper diagnostics; a true before-placement land/water context veto remains a future mixin or generator-wrapper task.
- Historical Atlas water/visual review is superseded by the random-worldgen rollback. Keep the reports as evidence, but do not keep tuning Atlas terrain unless Jayden explicitly reopens it.
- Ascendant Atlas is active as a finite coordinate/runtime layer: world border, region/ring/sector scoreboards, `/function ascendant_atlas:status`, and In Control area guardrails.
- Ascendant Atlas previously shipped a local helper mod, `ascendant_atlas_regions`, plus an OpenLoader Overworld dimension override. The helper and reports remain in source, but the Overworld override is now disabled/removed so normal random generation is active after sync.
- Guild/Hunter systems are scaffolded: Bountiful pools, generated NPC profiles, generated Guild structures, Patchouli Codex entries, and CustomNPC spawn functions.
- Structure volume is now high enough. The current work is tuning, validation, and targeted helper modules, not adding more structure packs.
- Random ranked dungeon work has moved from report-only to manual in-world spawn testing. It still does not add structure packs, rewrite loot, inject villages, or hard-gate ranks. See `docs/ASCENDANT_RANKED_DUNGEONS.md`, `docs/DUNGEON_PORTAL_SYSTEM.md`, `docs/ASCENDANT_DUNGEON_HOLOGRAMS.md`, and `docs/ASCENDANT_DUNGEON_SPAWN_TESTING.md`.
- Rank identity now has a live Forge-safe layer: `Ascendant Nametags` renders players and AI hunters with animated rank gradients/glow effects, authored NPCs use the CustomNPCs identity script, vanilla teams remain fallback/context, and Rank Examiner NPCs run the evaluation as the interacting player. This is not the final FTB Quest trial system and does not hard-lock content.
- Keybind policy is now source-controlled and applied by `scripts/sync-active-client-files.ps1` without replacing unrelated options. See `docs/KEYBIND_REEVALUATION.md`.
- Death waypoint UI policy is source-controlled and applied by `scripts/sync-active-client-files.ps1`; see `docs/DEATH_WAYPOINT_UI_POLICY.md`.
- The compact handoff for magic, UI, rarity, keybinds, skill tree, and audit-only versus live-enforced boundaries is `docs/MAGIC_UI_SKILL_HANDOFF.md`.
- The current spawn-density target is no longer conservative. See `docs/MOB_SPAWN_DENSITY_PASS.md`, `docs/HOSTILE_DAY_SPAWN_PASS.md`, and `docs/REGIONAL_SPAWN_DIFFICULTY_PASS.md`; if the world still feels sparse after testing, the next pass should tune the active `config/incontrol/spawner.json` rates or add reviewed modded common-hostile entries, not boss spam. If enemy amount feels good but the wrong places feel too hard or too easy, tune `config/ascendant_core/regional_difficulty_policy.json` rather than re-enabling time-based scaling.
- `docs/OVERWORLD_MOB_SPAWN_COVERAGE.md` is the current answer to whether all intended overworld mobs are naturally spawning. It says no full guarantee yet; unresolved candidates must be reviewed before adding broad spawn rules.

## Documentation Cleanup Status

- Status: documentation-only cleanup completed; no gameplay configs, worldgen configs, mobs, ores, structures, roads, villages, Hunter Boards, Guild Halls, NPC placement, loot tables, recipes, or menu behavior were changed.
- `README.md` is now a short current orientation page. The former long README batch/session narrative was preserved intact at `docs/archive/BATCH_HISTORY.md`.
- `docs/DOCS_INDEX.md` is the authority map for current, generated, and historical docs.
- `docs/DOCUMENTATION_CLEANUP_REPORT.md` records the cleanup findings, what moved, what stayed put, and the validation rules added.
- `docs/TESTING_CHECKLIST.md` remains the broad checklist, but now warns that old batch sections are historical unless `CURRENT_STATUS.md` points to them for retest.
- `AGENTS.md` now points future sessions at the current terrain gate instead of old Batch A-era instructions.
- Current docs still intentionally do not move generated indexes under `docs/generated/`; that needs a separate reference-rewrite pass.

## Morning Handoff Summary

- `docs/MORNING_HANDOFF.md` is the newest human-readable overnight handoff for Jayden.
- Final validation command status: `packwiz refresh` passed and `python scripts/check-pack.py` passed from source.
- Client export and server staging were rebuilt during the final handoff pass; `dist/` remains generated output, not source.
- Terrain status is not signed off. Jayden visually confirmed the border snap is fixed, but the post-generation block-fill terrain correction created artificial Stoneback/Sunreach shelves. Source now uses a natural `minecraft:overworld/continents` density-function bias for Atlas land-first south/west/southwest/south-east sectors.
- The experimental Option C fresh-chunk block-fill correction is classified as a failed prototype and remains disabled in source. It proved the issue is below biome selection, but it is not an acceptable fix because it replaces water with helper-chosen blocks instead of generating natural Tectonic/Terralith land. The active source prototype is now `ascendant_atlas_regions:atlas_land_bias`, which nudges continentalness before Tectonic evaluates terrain. V3 stretches climate saturation from 3000 to 12000 blocks, removes ocean biome IDs from `south_east`, and softens straight sector boundaries. See `docs/ATLAS_TERRAIN_NOISE_WRAPPER_PROTOTYPE.md`, `docs/ATLAS_TERRAIN_NOISE_CONTROL_PLAN.md`, `docs/ATLAS_TERRAIN_NOISE_RESEARCH.md`, `docs/ATLAS_TECTONIC_INTEGRATION_RISK.md`, `config/ascendant_atlas/terrain_noise_policy.json`, and `config/ascendant_atlas/land_water_region_policy.json`.
- Latest five-command in-game run was copied back into source reports. It produced 181/181 source samples, 181/181 surface samples, and 181/181 land/water samples.
- Do not rerun the lag-heavy `/ascatlas classify_water_bodies 30000 5000` command for this pass. Use `/ascatlas sample_land_water 30000 5000`; it is the current terrain proof path.

## Latest Atlas Test Result - 2026-06-17

- Active helper during the latest completed in-game report: `E9597A745`.
- Current source and active helper after the southeast transition hotfix: `E06BE804`.
- Latest completed reports from active `Ascendant Realms (2)` have been copied back into source.
- `/ascatlas dump_biome_pools`: complete; active biome pools resolved.
- `/ascatlas sample_grid 12000 2000`: complete, 181/181 source samples, 0 biome-pool mismatches, 0 snow outside intended cold pools.
- `/ascatlas sample_surface_grid 12000 2000`: complete, 181/181 surface samples, 0 sample errors, 0 cave-like surface biomes, 0 low-surface samples, 0 snow outside intended cold pools, and 0 surface mismatches.
- Previous surface mismatch resolved: `/tp @s 10000 147 8000` now resolves as `south_east`, `terralith:red_oasis`, and Jayden visually confirmed it looks pretty good.
- `/ascatlas sample_land_water 30000 5000`: complete, 181/181 samples, 28 water surface samples, 1 land-first `ocean_leak`, 0 land-first `basin_leak`, 0 `needs_manual_review`, and 27 preserved water-feature samples.
- Latest visual result: Jayden has not visually reviewed the v2 points yet, but the reports confirm the rejected block-fill path is disabled and changed 0 blocks.
- Remaining v2 ocean leak: `/tp @s -2000 71 0` in inner Stoneback/highlands, `minecraft:windswept_forest`, local water 96%, nearby land 4%, `ocean_like_local_basin`.
- Source now has v3 density/biome tuning: south outer bias `0.86`, south-east outer bias `0.58`, west outer bias `0.82`, and south-west outer bias `0.96`; the `south_east` pool has 0 ocean biome IDs; `world_radius_blocks` is now `12000`. This is still natural terrain/noise bias, not block filling.
- Failed Option C correction report: 5634 chunks scanned, 80 chunks corrected, 19909 columns corrected, and 990278 blocks changed; `last_error` is null. Those numbers are kept as evidence only and should not be repeated.
- The validation run caused severe integrated-server lag while far chunks generated. Treat the commands as heavy validation only, not normal gameplay.
- Conclusion: the biome-source layer, surface sampling, snow guard, and border buffer are working, and the fake-fill shelf artifact is gone. Terrain is still not accepted because v2 left 1 inner-west automated ocean leak at `/tp @s -2000 71 0`. If that point visually reads as a bad inland sea, tune inner-west land bias next; if it reads as a legitimate mountain lake, document a narrow accepted edge case.

## Terrain/Noise Control Investigation - 2026-06-17

- Active Overworld override confirmed: `minecraft:noise` generator, `minecraft:overworld` settings, `ascendant_atlas_regions:regional_multi_noise` biome source.
- Active Tectonic/Terratonic role confirmed: terrain/noise shape is still owned below Atlas through injected `minecraft:overworld` worldgen resources.
- Active Tectonic config reviewed: `config/tectonic.json` exposes `legacy_mode` only; no safe config-only control was found for ocean basin frequency, continentalness, sea level, aquifers, or terrain height.
- The helper owns biome selection and now also has a feature-flagged fresh-chunk terrain correction pass. It still does not replace the chunk generator, lower sea level, or replace Tectonic/noise settings.
- New helper command surface: `/ascatlas terrain_probe <x> <z>`, `/ascatlas terrain_probe_here`, `/ascatlas sample_land_water <radius> <step>`, `/ascatlas cancel_land_water_sample`, `/ascatlas dump_land_water_policy`, and `/ascatlas dump_terrain_noise_policy`.
- New natural terrain prototype: helper registers `ascendant_atlas_regions:atlas_land_bias`; OpenLoader overrides `data/minecraft/worldgen/density_function/overworld/continents.json` to add a south/west/southwest/south-east land-first continentalness bias before Tectonic's terrain splines run. V3 also removes ocean biome IDs from the `south_east` pool and softens sector boundaries. This should generate natural land instead of filling water after the fact.
- New reports: `config/ascendant_atlas/reports/terrain_noise_probe_latest.json`, `config/ascendant_atlas/reports/land_water_coherence_latest.json`, and `config/ascendant_atlas/reports/terrain_wrapper_test_latest.json`.
- Prototype behavior: the experimental fresh-chunk-only block-fill correction is a failed prototype and is disabled in source. The active prototype is a density-function override, not a block mutation pass and not terrain signoff.
- Preferred next code path if this fails: keep Atlas biome-source control, then prototype a deeper delegate-based Atlas terrain/noise wrapper. Do not return to post-generation block filling.
- Latest land/water probe result: complete, 181/181 samples, 28 water surfaces, 1 ocean leak, 0 basin leaks, 0 manual-review samples, and 27 preserved water-feature samples. Logs showed integrated-server lag during far-chunk generation, but the sampler completed.

## Fixes Applied In Source/Exports This Pass

- KubeJS JSON readers now resolve config files with string paths instead of ambiguous Java `Path` objects.
- Ascendant Core death-hook locals were renamed to avoid the Rhino redeclaration warning seen in the latest in-game log.
- Active-client sync now copies tuned top-level gameplay/config files, including Guard Villagers, Spawn Balance Utility, Majrusz difficulty, mob health bar, loot beams, Integrated Villages, and Create Structures Arise.
- Compatibility resource-pack aliases were added for the latest missing armor texture warnings: `dev_layer_1`, `plagued_layer_2`, and bronze sea-serpent layers.
- The duplicate Guild worldgen/NPC test section was removed from `docs/TESTING_CHECKLIST.md`.
- Historical Atlas worldgen v1 was implemented: `mods/ascendant-atlas-regions-0.1.0.jar`, source under `local-mods/ascendant-atlas-regions/`, generated region tables in `config/ascendant_atlas/worldgen_regions.json`, and an OpenLoader Overworld override. That override is now removed while random generation is restored.
- Startup crash fix after the first helper launch: `ascendant_atlas_regions` now registers `regional_multi_noise` through Forge `DeferredRegister` instead of directly mutating the frozen built-in biome-source registry.
- Live world-load check found KubeJS config reads still using ambiguous Java `Path.resolve(...)`; Atlas, Core, and Progression now read config through direct `JsonIO.read("config/...")` string paths instead.
- North/south field-test fix: the helper now applies a distance-based climate gradient and delays the shared outer table until 50000 blocks. The playable world border remains 30000 blocks; the larger radial buffer covers the square border edges and corners so terrain beyond the barrier keeps directional identity. North should progress from cold/cold-ocean possibilities toward tundra, ice, and frozen biomes; south should progress from warm/lukewarm coast toward dry stone/sand, desert, and badlands instead of snapping to the shared outer table at the barrier.
- Center field-test fix: the Hearthlands center table now excludes `terralith:alpha_islands`, `minecraft:grove`, and `minecraft:river`, and the checker rejects ocean/river/island/snowy center biomes.
- Cardinal ocean field-test fix: a live sample at about `x=339, z=-1937` showed uniform `minecraft:deep_frozen_ocean`; the north table now excludes deep cold/deep frozen ocean, cold ocean, snowy beach, ice marsh, and steep alpine-first picks, while frozen ocean is kept only as a sparse far-north sea pocket when the underlying climate noise is strongly oceanic. The south table excludes lukewarm and deep lukewarm ocean, keeping warm ocean only as a sparse warm-sea candidate.
- Center/south-east seam fix: a live sample around `x=359, z=619` showed river, lukewarm ocean, gravel desert, and gravel beach mixing at the Hearthlands boundary. The center table rejects river, the direct south table rejects `minecraft:lukewarm_ocean` and `terralith:gravel_desert`, the east table rejects `terralith:gravel_beach`, and the south helper bias starts land-first before allowing sparse warm-sea pockets farther out.
- Warm-region snow fix: the same live sample showed saved `minecraft:snow`, `snowrealmagic:snow`, and `minecraft:ice` on `terralith:gravel_desert`. The audit found `terralith:gravel_desert` has biome temperature `0.14` despite the name, and the active Weather2/Snow Real Magic/Serene Seasons defaults allowed snow outside cold biomes and preserved it in warm biomes. Source configs now block snowstorm buildup outside cold biomes, make Snow Real Magic melt snow/ice in warm biomes, and disable global seasonal snow/ice generation.
- Aquamirae density fix: a wider chunk scan around the same north test route found dense `aquamirae:surface/arch` and `aquamirae:surface/spiral` starts from the jar's `spacing: 4, separation: 0`; the world-integration datapack now overrides that set to `spacing: 20, separation: 8`.
- Evidence-audit pass: `scripts/audit-worldgen-content.py` now generates `docs/WORLDGEN_CONTENT_AUDIT.md` and `docs/generated/worldgen_content_audit.json` from active biome JSON, Terralith climate entries, structure sets/templates, block palettes, biome spawns, and structure spawn overrides.
- Terrain-validation pass: `ascendant_atlas_regions` now adds `/ascatlas here`, `/ascatlas region <x> <z>`, `/ascatlas sample_grid <radius> <step>`, `/ascatlas sample_surface_grid <radius> <step>`, `/ascatlas classify_water_bodies <radius> <step>`, `/ascatlas cancel_water_body_classification`, `/ascatlas terrain_probe <x> <z>`, `/ascatlas terrain_probe_here`, `/ascatlas sample_land_water <radius> <step>`, `/ascatlas cancel_land_water_sample`, `/ascatlas dump_land_water_policy`, `/ascatlas dump_terrain_noise_policy`, and `/ascatlas dump_biome_pools`. Source and active helper `E06BE804` have the v3 southeast transition fix.
- Latest focused Atlas command evidence: `/ascatlas dump_terrain_noise_policy`, `/ascatlas dump_biome_pools`, `/ascatlas sample_grid 12000 2000`, `/ascatlas sample_surface_grid 12000 2000`, and `/ascatlas sample_land_water 30000 5000` completed in-game on 2026-06-17 with helper `E9597A745`. Source validation has 0 mismatches. Surface validation has 0 mismatches. Land/water validation has 1 remaining land-first ocean leak and 0 basin leaks.
- Atlas terrain status: not accepted. V3 is synced and must be retested in a fresh world at the screenshot coordinates plus `/tp @s -2000 71 0`.
- Water review pass: `docs/ATLAS_WATER_REVIEW.md` remains the manual/historical water-review register. Current terrain proof should come from `config/ascendant_atlas/reports/land_water_coherence_latest.json` and `docs/ATLAS_LAND_WATER_COHERENCE.md`.
- Land/water coherence pass: `docs/ATLAS_LAND_WATER_COHERENCE.md`, `config/ascendant_atlas/reports/terrain_noise_probe_latest.json`, and `config/ascendant_atlas/reports/land_water_coherence_latest.json` still hold the latest completed v2 in-game result: no artificial fills, 1 land-first ocean leak, 0 basin leaks, and 27 preserved water features. Source v3 must be retested before those reports are considered current. Do not solve remaining issues by deleting all water or lowering sea level.
- Invalid-player-data fix: `config/alexsmobs.toml` now disables the Alex's Mobs first-login Animal Dictionary grant, and `scripts/sync-active-client-files.ps1` now syncs that config into the active instance.
- Historical cave-pool correction result: `scripts/generate-ascendant-atlas-worldgen.py` excludes cave-only biome IDs from Atlas surface region tables. This remains report/history data only while the active Overworld override is removed.
- Runtime scale correction: `config/ascendant_atlas/runtime.json` and `kubejs/server_scripts/ascendant_atlas_runtime.js` use a 30000-block playable validation radius and a 60000-block world border. The helper biome-source `world_radius_blocks` is now `12000` so north/south climate saturation is a long gradient instead of a near-spawn snap.
- Data-driven biome correction: audit-backed reports found snow-allowed mountain biomes in west/south-west. `scripts/generate-ascendant-atlas-worldgen.py` now removes `minecraft:jagged_peaks`, `terralith:alpine_grove`, `terralith:emerald_peaks`, and `terralith:scarlet_mountains` from west so west/south-west no longer allow snow outside intended cold regions.
- New required terrain reports: `docs/ATLAS_TERRAIN_VALIDATION_REPORT.md`, `docs/ATLAS_BIOME_POOL_REPORT.md`, `docs/ATLAS_WORLDGEN_FAILURES.md`, `docs/ATLAS_WATER_REVIEW.md`, `docs/ATLAS_LAND_WATER_COHERENCE.md`, `docs/ATLAS_TERRAIN_NOISE_CONTROL_PLAN.md`, `docs/ATLAS_TERRAIN_NOISE_RESEARCH.md`, `docs/ATLAS_TECTONIC_INTEGRATION_RISK.md`, `config/ascendant_atlas/terrain_noise_policy.json`, `config/ascendant_atlas/land_water_region_policy.json`, `config/ascendant_atlas/reports/sample_grid_source_latest.json`, `config/ascendant_atlas/reports/sample_grid_surface_latest.json`, `config/ascendant_atlas/reports/water_surface_samples_latest.json`, `config/ascendant_atlas/reports/water_body_classification_latest.json`, `config/ascendant_atlas/reports/terrain_noise_probe_latest.json`, `config/ascendant_atlas/reports/land_water_coherence_latest.json`, `config/ascendant_atlas/reports/biome_pools_resolved.json`, and `config/ascendant_atlas/reports/missing_biomes.json`.

## Must Retest

1. Relaunch `Ascendant Realms (2)` and create a fresh creative validation world.
2. Check `logs/kubejs/server.log` for absence of:
   - `Could not read config/ascendant_atlas/runtime.json`
   - `Could not load config/ascendant_core/runtime_rules.json`
   - `Manifest disabled or unavailable; core bridge is idle`
   - `Could not read config/ascendant_progression/progression.json`
   - `redeclaration of var killerPlayer`
   - `The choice of Java method sun.nio.fs.WindowsPath.resolve`
3. Check `logs/latest.log` for absence of:
   - `Registry is already frozen`
   - `ascendant_atlas_regions) has failed to load correctly`
4. Confirm the new world no longer bounces to the menu with an invalid-player-data message on first join.
5. Keep the `minecraft:frozen_river` transition rule available only for northwest Stoneback/Frostmarch edge cases; do not add `minecraft:frozen_river` to all west/Stoneback pools.
6. Synced helper `E06BE804` plus v3 southeast transition tuning is now active. Latest automated report is still v2; fresh-world v3 validation is now the blocker.
   - `/ascatlas dump_terrain_noise_policy`
   - `/ascatlas dump_biome_pools`
   - `/ascatlas sample_grid 12000 2000`
   - `/ascatlas sample_surface_grid 12000 2000`
   - `/ascatlas sample_land_water 30000 5000`
7. For Ranked Dungeon generated-instance testing after the next sync/relaunch, use a safe creative world and run:
   - `/ascdungeon cleanup_instance`
   - `/ascdungeon status`
   - `/ascdungeon spawn_random_now`
   - confirm the animated gate texture appears with no visible frame blocks and no yellow Elite Holograms edit text, then walk into the gate or run `/ascdungeon enter_latest`
   - confirm the gate art stays fixed in world space instead of turning to face the player
   - confirm the entrance stays open for about 5 seconds after first entry, then shrinks out instead of vanishing instantly
   - stand near the gate for a few seconds and confirm the subtle portal ambience and rank-colored particles are present
   - confirm you land on a solid generated room floor, not falling from the sky/void
   - confirm there is no return gate before boss defeat
   - clear the boss room and confirm the return gate appears
   - use the return gate, or run `/ascdungeon return_latest` after boss defeat
   - `/ascdungeon cleanup_instance`
   - optional manual rank test: `/ascdungeon open_test_rift d_rank`
   - optional visual-only row: `/ascdungeon spawn_test_all_ranks 12`
   - optional visual cleanup: `/ascdungeon cleanup_test`
   - `/ascdungeon dump_policy`
   - check `config/ascendant_dungeons/reports/dungeon_instance_latest.json` for `immersive_portal_bridge.status`
   - check the same report for `portal_shape=circular_special_shape`, `immersive_portal_teleportable=true`, and `entrance_travel_owned_by_immersive_portals=true`
   - check the same report for `entrance_close_at_millis` and `entrance_shrink_started_at_millis` after first entry
   - `/eh` only if you want to manually confirm the Elite Holograms command root exists.
8. If the probe is running, let it finish; the job progresses on server ticks and will stall while the game is paused.
9. Do not rerun `/ascatlas classify_water_bodies 30000 5000` for this pass; it is older, lag-heavy evidence.
10. Manual follow-up points after the latest commands:
   - `/tp @s -2000 71 0` - only remaining v2 automated ocean leak; inspect whether this is an unacceptable inland sea or an acceptable Stoneback mountain lake.
   - `/tp @s -29989 120 3` - confirm the Stoneback shelf/shear-wall artifact no longer appears and that west terrain reads as natural highland, not an ocean basin or filled shelf.
   - `/tp @s 703 141 1129` - confirm the Sunreach terracotta shelf artifact no longer appears and that south terrain reads as natural arid land, canyon, oasis, river, or beach where appropriate.
   - `/tp @s -310 153 -509` - inspect the near-north Hearthlands/Frostmarch transition from the screenshot; it should no longer read as random snow patch then grass again farther north.
   - Border snap is visually fixed; only recheck border edges/corners if a new world shows a fresh snap.
11. Confirm actual generated biomes match Atlas direction: Hearthlands mild and mostly dry near spawn, Frostmarch progressively colder north, Sunreach progressively arid/hot south, Verdant Coast wet/coastal/jungle/oceanic east, and Stoneback mountain/highland west.
12. Fly the required grid in `docs/ATLAS_TERRAIN_VALIDATION_REPORT.md`, including 5000, 9000, 12000, and the water-review teleport points. Record whether terrain visually matches and whether transitions are too sharp.
13. Confirm legitimate water still exists where it should: rivers, oases, mountain lakes, Verdant Coast water, coastlines, and Frostmarch frozen water.
14. Confirm the HUD bridge still shows Ascendant Web level, XP, and skill points.
15. Confirm Guard Villagers active config uses the source tuning: 10 guards, patrols enabled, 24 health, 28 follow range.
16. Do not tune roads yet; only note road/river/cliff issues and bridge opportunities after the terrain grid is validated.
17. In frozen-ocean test areas, Aquamirae surface arches/spirals should be occasional landmarks, not a repeated structure field.
18. Do not move to villages, settlements, Hunter Boards, Guild Halls, or NPC placement until the terrain report passes.

## Known Design Boundary

Hard regional biome identity now uses the local `ascendant_atlas_regions` helper. The remaining hard boundary is terrain-aware road/bridge substitution and deeper structure-pool conflict resolution; datapacks can still define structures/tags/loot, but they cannot inspect final terrain and replace bad road crossings after worldgen.

## Do Not Do Yet

- Do not add more external worldgen or village overhaul packs.
- Do not add Biomes O' Plenty, Dynamic Trees, Sinytra Connector, OptiFine, original Ice and Fire alongside IceAndFire CE, or another boss-campaign stack.
- Do not add more helper modules until the regional biome-source helper relaunches cleanly and fresh-world biome checks pass.

## Loot Economy Control Scaffold

- Status: generated audit/control scaffold only; no broad loot rewrites are enabled.
- Audited loot tables: 4354.
- High-rarity low-tier warnings: 30.
- High-rarity village/basic warnings: 38.
- Authoritative docs/configs: `docs/ASCENDANT_LOOT_ECONOMY.md`, `docs/LOOT_TABLE_AUDIT.md`, `docs/STRUCTURE_REWARD_TIER_INDEX.md`, and `config/ascendant_loot/*.json`.
- Next step after terrain signoff: manually review flagged loot sources, then approve narrow KubeJS/datapack rewrites source by source.

## Recipe Progression Control Scaffold

- Status: generated audit/candidate scaffold only; no hard crafting gates or broad recipe rewrites are enabled.
- Recipe outputs audited: 8075.
- High-risk recipes: 109.
- Malformed recipe JSON: 0.
- Authoritative docs/configs: `docs/RECIPE_PROGRESSION_AUDIT.md`, `docs/CRAFTING_GATE_PLAN.md`, `docs/BROKEN_OR_EASY_RECIPE_REPORT.md`, and `config/ascendant_recipes/*.json`.
- Candidate rewrites live only in disabled review paths until explicitly approved.

## Structure Tiering Control Scaffold

- Status: expanded into Ascendant Structure Director Live v1. No new structure mods, village-pool injections, Hunter Boards, Guild Halls, NPC placement, loot rewrites, recipe gates, magic gates, or rank gates were enabled.
- Direct generated structures classified: 579.
- Structure sets with density policy rows: 330.
- Structure/tag rows skipped as non-direct generated structures: 149.
- Structure Director split policies now classify water, sea-floor, ship/ocean-surface, sky, dungeon, boss/dragon, village/town, vertical layer, region fit, danger tier, loot tier, and disabled density candidates with evidence/confidence fields.
- Review-only candidate overrides: 70 structure-set spacing/density candidates under `config/ascendant_structures/candidates/`; selected evidence-backed changes are now live through `config/openloader/data/ascendant_structure_director_live/`.
- Live v1 active changes: 23 total, 17 structure/structure-set JSON overrides, 5 biome-tag overrides, 4 land/water policy rules, and 2 settlement-family overlap controls.
- First in-game Structure Director review route generated: `docs/STRUCTURE_VISUAL_REVIEW_ROUTE.md`, `docs/STRUCTURE_DIRECTOR_REVIEW_RESULTS_TEMPLATE.md`, `config/ascendant_structures/structure_visual_review_route.json`, `config/ascendant_structures/structure_locate_commands.md`, and `config/ascendant_structures/structure_review_priority_queue.json`.
- Route coverage after the evidence purge: 7 review sections, 154 unique locate commands, 70 priority queue entries, and 50 unique priority structures. This is review-only and does not change live generation.
- Jayden's first structure field review found that most checked structures looked good; the current visible problem is land structures spawning as islands in ocean/lake terrain, especially dragon roosts and `idas:abandoned_vineyard`.
- Evidence purge applied: names, namespaces, path words, and mod labels are weak hints only. Final sensitive classifications now require non-name evidence from biome tags/IDs, structure JSON, structure sets, template/block palettes, registry hooks, or manual observations. Current evidence summary: 543 strong, 33 medium, 3 weak, 13 manual-review rows, and 0 name-only classifications.
- Ice and Fire correction is now evidence-backed: dragon roosts/caves/gorgon/graveyard/cyclops/hydra no longer classify as water/frozen-ocean from the word `Ice`; `iceandfire:siren_island` remains ocean-backed because its actual biome tag resolves to ocean evidence. IDAS override cases are recorded as active generated results: gorgon temple -> `idas:labyrinth`, graveyard -> `idas:haunted_manor`.
- New review evidence: `docs/STRUCTURE_CLASSIFICATION_EVIDENCE_RULES.md`, `docs/STRUCTURE_CLASSIFICATION_AUDIT_REPORT.md`, `docs/STRUCTURE_VISUAL_REVIEW_FINDINGS.md`, `config/ascendant_structures/structure_evidence_registry.json`, `config/ascendant_structures/structure_classification_confidence.json`, `config/ascendant_structures/manual_structure_observations.json`, and disabled candidate notes in `config/ascendant_structures/candidates/`.
- Current warnings remain partly review work: boss/dungeon beginner-region conflicts, remaining dense entries outside the selected Live v1 pass, village/town overlap-risk sets, water/sky placement risks, and review-only or missing structure loot tiers.
- Authoritative docs/configs: `docs/ASCENDANT_STRUCTURE_DIRECTOR.md`, `docs/STRUCTURE_REGION_AND_LAYER_INDEX.md`, `docs/STRUCTURE_DENSITY_IMPLEMENTATION_REPORT.md`, `docs/WATER_AND_SKY_STRUCTURES.md`, `docs/STRUCTURE_LOOT_AND_DANGER_TIERS.md`, `docs/STRUCTURE_TESTING_CHECKLIST.md`, `docs/ASCENDANT_STRUCTURE_TIERING.md`, `docs/STRUCTURE_DENSITY_AND_REGION_AUDIT.md`, `docs/STRUCTURE_CONFLICTS_AND_OVERLAPS.md`, and `config/ascendant_structures/*.json`.
- Next step: after sync/export, create a fresh structure validation world and run `config/ascendant_structures/live_test_commands.md`, starting with dragon roosts, `idas:abandoned_vineyard`, `iceandfire:siren_island`, and Towns and Towers/vanilla village spacing. Existing generated structures will not move.

## Travel Network Reconnaissance Scaffold

- Status: generated reconnaissance/control scaffold only; no roads, bridges, village injections, route helpers, or live generation changes were enabled.
- Road/path sources covered: 6.
- Bridge sources covered: 4.
- Path or travel-like structures detected in the generated worldgen audit: 68.
- Current travel warnings: 4 road/path sources with cliff/slope or bridge-absence risk, 1 route-purpose risk source, 2 bridge sources not linked to a river/water crossing strategy, and 15 Atlas ocean-leak samples still blocking permanent route design.
- Authoritative docs/configs: `docs/ASCENDANT_TRAVEL_NETWORK_AUDIT.md`, `docs/ROAD_BRIDGE_RIVER_FAILURES.md`, `docs/TRAVEL_NETWORK_DESIGN_RULES.md`, and `config/ascendant_travel/*.json`.
- Next step after Atlas land/water signoff: field-record road, bridge, river, ravine, cliff, dock, and village-street failure coordinates before enabling any route or bridge changes.

## Regional Atmosphere Control Scaffold

- Status: generated audit/control scaffold only; no terrain, mob, ore, structure, weather-config, audio-config, title-resource-pack, or UI behavior changes were enabled.
- Atlas-facing atmosphere regions covered: 12.
- Warm regions allowing snow buildup in policy: 0.
- Current snow guard evidence remains clean: Weather2 outside-cold snow buildup is blocked, Serene Seasons blanket snow/ice conversion is disabled, and Snow Real Magic warm-biome melting is enabled.
- Current title status: Traveler's Titles biome/dimension titles are live, but Atlas coordinate-region titles are policy-only and not live-enforced yet.
- Authoritative docs/configs: `docs/ASCENDANT_REGIONAL_ATMOSPHERE.md`, `docs/WEATHER_AND_SEASON_REGION_POLICY.md`, `docs/BIOME_TITLE_AND_AUDIO_POLICY.md`, and `config/ascendant_atmosphere/*.json`.
- Next step after terrain/water acceptance: decide whether Atlas region scoreboards should drive custom region title/audio hooks; do not treat biome-title fallback keys as coordinate-region titles.

## Magic Progression Control Scaffold

- Status: generated audit/control scaffold only; no new magic mods, spell rewrites, loot rewrites, recipe rewrites, or hard rank gates were enabled.
- Indexed spell policy rows: 113.
- Indexed magic-item policy rows: 273.
- Magic loot sources linked to current loot economy: 154.
- Magic recipe entries linked to current recipe audit: 206.
- Current magic warnings: 23 high-tier magic entries exposed through low-tier or under-ceiling loot sources, 16 high-tier/risky magic recipes needing review, and 55 unreviewed magic recipe candidates that must remain disabled.
- Authoritative docs/configs: `docs/ASCENDANT_MAGIC_PROGRESSION.md`, `docs/SPELL_REGION_AND_RANK_INDEX.md`, `docs/MAGIC_LOOT_AND_RECIPE_AUDIT.md`, and `config/ascendant_magic/*.json`.
- Candidate notes are disabled under `kubejs/server_scripts_disabled/review/ascendant_magic/`; do not move them into live KubeJS without explicit approval.
- Next step after terrain/water acceptance: review Iron's Spells ancient knowledge fragments, legendary ink, legendary spellbooks, Dead King rewards, and high-tier spellbook recipes against Atlas region/danger/rank policy.

## Gear Balance Outlier Scaffold

- Status: generated audit/control scaffold only; no item stats, rarity labels, loot tables, recipes, or rank gates were changed.
- Unique gear IDs covered by balance policy: 1573, from 1723 indexed gear-registry collection rows.
- Outlier report rows: 1278. Most are evidence gaps or progression-placement review items, not nerf instructions.
- Rarity review queue rows: 473.
- Current balance warnings: 9 high-stat low-rarity or low-placement items, 0 low-stat high-rarity items without a special ability note, 0 gear IDs missing progression tier, and 0 gear-registry IDs missing balance policy.
- The 9 immediate stat/placement review items are `fantasy_armor:flesh_of_the_feaster_chestplate`, `simplymore:mimicry_chakram`, `simplymore:template_great_spear`, `simplyswords:magic_estoc`, `simplyswords:tempest`, `spartanshields:enderium_tower_shield`, `spartanshields:platinum_tower_shield`, `spartanshields:signalum_tower_shield`, and `spartanshields:terrasteel_tower_shield`.
- Authoritative docs/configs: `docs/GEAR_BALANCE_OUTLIER_REPORT.md`, `docs/RARITY_CONSISTENCY_AUDIT.md`, `docs/GEAR_PROGRESSion_RISK_REGISTER.md`, and `config/ascendant_balance/*.json`.
- Next step after terrain/water acceptance: manually review the 9 stat/placement outliers first, then boss-reward and rank-gate candidates. Prefer loot/rank/recipe placement before stat edits.

## Player Progression Bridge Scaffold

- Status: generated audit/control scaffold only; no new mods, hard content locks, skill locks, region locks, loot rewrites, recipe gates, or rank gates were enabled.
- Public Guild rank matrix now covers Unranked, E, D, C, B, A, and S rank as evaluation bands rather than a checklist grind.
- The bridge links Guild rank to Puffish Skills, Atlas region readiness, mob threat ranges, bounty tiers, gear rarities, magic tiers, boss/structure milestones, and current loot/balance/magic policy.
- Current coverage: 7 rank rows, 113 known Puffish Ascendant skill IDs, 9 Atlas regions, 7 gear rarity policies, and 8 magic tier policies.
- Current validation: 0 missing rank rows, 0 missing Atlas region references, 0 missing Puffish skill ID references, 0 gear rarities without rank policy, 0 observed magic tiers without rank policy, and 0 starter-region threat excess entries.
- Authoritative docs/configs: `docs/ASCENDANT_PLAYER_PROGRESSION.md`, `docs/GUILD_RANK_REQUIREMENT_MATRIX.md`, `docs/SKILL_TREE_INTEGRATION_PLAN.md`, and `config/ascendant_progression/{rank_requirement_matrix,skill_unlock_policy,region_progression_policy,gear_rank_policy,magic_rank_policy}.json`.
- Rank Examiner live bridge: players talk to a Rank Examiner NPC, which runs the hidden evaluation as the player. The evaluation shows proof counters, applies any earned public Guild rank, syncs the visible player rank team, and reports the next threshold. `/function ascendant_identity:rank_examiner/evaluate` is only for admin/testing when no NPC is available.
- Authoritative nameplate/rank bridge docs/configs: `docs/RANK_NAMEPLATE_AND_EXAMINER_SYSTEM.md`, `docs/ASCENDANT_NAMEPLATES.md`, `config/ascendant_guild/rank_nameplate_policy.json`, and `config/ascendant_guild/rank_examiner_policy.json`.
- Next step after dungeon/rank validation: convert this simple proof bridge into authored FTB Quest rank trials and reward language. Do not use it to lock players out of existing content yet.

## NPC Visual Identity Scaffold

- Status: generated audit/control scaffold only; no NPC placement, village injection, new NPC mods, spawn-rule changes, or structure-generation changes were enabled.
- MCA Reborn, Easy NPC, CustomNPCs-Unofficial, Human Companions, Guard Villagers, Villager Names, and the MCA Default Medieval resource pack are present in pack metadata.
- MCA Default Medieval is enabled in `options.txt`; the active `Ascendant Realms (2)` resource-pack zip was inspected and currently contains 974 MCA medieval clothing PNGs with 0 filename-level hoodie/jeans/t-shirt/sneaker/modern/business flags.
- CustomNPC bridge skins are mirrored cleanly: 12 in `resourcepacks/ascendant-realms-compat-fixes/.../ascendant_mca/` and 12 in `customnpcs/assets/customnpcs/.../ascendant_mca/`.
- Important requested silhouettes covered: Guild Clerk, Rank Examiner, Bounty Master, Guild Arcanist, Quartermaster, Guard Captain, Tavern Keeper, Village Elder, and Rival Hunter. Wounded Hunter is also covered because it already exists in the generated test profile set.
- Rival hunter roster coverage: 5/5 rivals have rank, class/style, gear tier, loadout profile, nameplate profile, and drop policy. Loadout item IDs missing from `gear_registry.json`: 0.
- Authoritative docs/configs: `docs/NPC_VISUAL_VALIDATION_REPORT.md`, `docs/MCA_MEDIEVAL_SKIN_AUDIT.md`, `docs/RIVAL_HUNTER_VISUAL_ROSTER.md`, `config/ascendant_guild/npc_visual_policy.json`, `config/ascendant_guild/npc_profession_silhouettes.json`, and `config/ascendant_guild/rival_hunter_roster.json`.
- Next step after terrain/water acceptance: do a manual in-game MCA village visual pass and Easy NPC/CustomNPC template pass. Do not use this scaffold as approval to place NPCs, inject villages, or expand rival spawns.

## UI Clarity And Feedback Scaffold

- Status: generated audit/control scaffold only; no menu redesign, new UI mods, live tooltip rewrite, new mob overlay, or region-title runtime hook was enabled.
- Tangible gear/item UI coverage: 1460 tangible registry item IDs checked, 0 missing Item Borders entries, 0 Item Borders color mismatches, and 0 tangible rarity tooltip gaps.
- Spell boundary: 113 Iron's Spells spell IDs are intentionally treated as non-inventory spell identifiers for item-border/tooltip purposes; physical spellbooks and magic items remain covered through the tangible item registry.
- Rarity source of truth: `config/ascendant_index/gear_registry.json` and `config/itemborders-common.toml` are now documented as the active item-rarity/color authority. Older rarity color drift in `config/ascendant_index/rarity_schema.json` and `config/ascendant_core/loot_rarity_rules.json` is documented for later cleanup, not treated as the active visual surface.
- Current UI stack is aligned: Item Borders follows assigned rarity color, KubeJS adds the player-facing rarity line, Legendary Tooltips stays frame-only, Loot Beams uses rarity color instead of item-name color, Loot Journal handles pickup feedback, and JEI's current Runic Grimoire alias does not hide material variants.
- Current boundaries: Health Bar Plus can support health danger readability, but threat-tier labels are policy-only. Traveler's Titles biome/dimension titles are live, but Atlas coordinate-region titles remain policy-only until a runtime hook exists.
- Active-client sync coverage now includes `config/ascendant_ui` and `config/obscuria`, so the UI policy files and Loot Journal client config are covered with the other synced client files.
- Authoritative docs/configs: `docs/UI_CLARITY_AND_FEEDBACK_AUDIT.md`, `docs/RARITY_TOOLTIP_VISUAL_POLICY.md`, `docs/MOB_DANGER_UI_POLICY.md`, `docs/REGION_TITLE_UI_POLICY.md`, and `config/ascendant_ui/*.json`.
- Next step after terrain/water acceptance: in-game visual pass for dropped high-rarity loot beams, tooltip order, title pack order, and Health Bar Plus readability. Do not redesign the menu or add UI mods from this scaffold.
