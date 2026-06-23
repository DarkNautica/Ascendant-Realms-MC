# Ascendant Realms

Archived from the former long `README.md` during the 2026-06-17 documentation cleanup pass.

This file preserves historical batch/session narrative for archaeology. It is not the live handoff. For current direction, read `docs/CURRENT_STATUS.md` and `docs/DOCS_INDEX.md` first.

---

Ascendant Realms is a vanilla+++ medieval fantasy RPG exploration modpack for two-player multiplayer. The goal is a beautiful, seamless, dangerous, progression-rich world with strong exploration, combat, loot, classes/skills, magic or abilities, bosses/minibosses, ambience, seasons/weather, and visual polish.

This is not a MineColonies pack. Do not add MineColonies unless Jayden explicitly asks later.

## Start Here

- `docs/CURRENT_STATUS.md` - current handoff, latest runtime fixes, and the next retest checklist.
- `docs/DOCS_INDEX.md` - map of current docs, generated registries, and consolidation direction.
- `docs/ATLAS_TERRAIN_VALIDATION_REPORT.md` - current terrain-first Atlas validation gate and required sample grid.
- `docs/ATLAS_BIOME_POOL_REPORT.md` - active biome pools resolved with audit-backed climate/snow data.
- `docs/ATLAS_WORLDGEN_FAILURES.md` - terrain blockers to clear before roads, villages, Hunter Boards, Guild Halls, or NPC placement.
- `docs/TESTING_CHECKLIST.md` - active in-game and server validation checklist.
- `AGENTS.md` - standing rules for future Codex sessions.

## Current Status

- Current handoff: see `docs/CURRENT_STATUS.md` before reading the historical batch log below.
- Phase 0 scaffold: complete.
- Version target approved: Minecraft 1.20.1 Forge 47.4.20.
- Phase 1.5 Packwiz initialization: complete.
- Verified batches: Batch A, Batch B, Batch C, Batch D, Batch E1, Batch E2, Batch F, Batch G, Batch H, Batch J, Batch K, Batch L, Batch M, and Batch N.
- Batch A install: complete.
- Batch A validation: passed for client boot, shaders, resource visuals, dedicated local server boot, localhost join, Visual Workbench, Sophisticated Backpacks, disconnect/rejoin, and 10-minute multiplayer stability.
- Batch B worldgen foundation: installed and validated.
- Custom worldgen correction: Ascendant Atlas is now the pack-owned finite-world control layer. It adds `config/ascendant_atlas/runtime.json`, `config/incontrol/areas.json`, `kubejs/server_scripts/ascendant_atlas_runtime.js`, `/function ascendant_atlas:status`, exact Ascendant Core policy files, generated docs, and validator coverage.
- Full Atlas worldgen v1: `ascendant_atlas_regions` is now a local Forge helper mod that supplies `ascendant_atlas_regions:regional_multi_noise`; the Atlas OpenLoader pack overrides the Overworld biome source so north/south/east/west/diagonal regions use real Terralith biome tables while Tectonic keeps the `minecraft:overworld` terrain settings.
- Live Ascendant Atlas runtime: the terrain validation envelope is centered at `0,0`, uses a 30000-block radius / 60000-block world border, mirrors player region/ring/sector into scoreboards, and gives region-change actionbar feedback for Hearthlands, Frostmarch, Sunreach, Verdant Coast, Stoneback Highlands, diagonals, Nether, and End.
- Atlas boundary: the previous Atlas waymarks are now debug-only structure assets and no longer generate naturally. Hard biome-source shaping is active through the local helper; terrain-aware road-to-bridge substitution remains future helper-module work.
- Pack name: Ascendant Realms.
- Pack version: 0.1.0-alpha.
- Java target: Java 17.
- Startup fix staged: Kotlin for Forge 4.12.0 was added for Fzzy Config, and Forge was raised from 47.4.10 to 47.4.20 because Subtle Effects requires Forge 47.4.14 or newer.
- Multiplayer side correction: Subtle Effects, Fzzy Config, Kotlin for Forge, and Particular Reforged are treated as both-side for this pack unless later testing proves a narrower split.
- Batch B validation: passed. Updated client export included Sparse Structures and the intended YUNG structure jars, the materializer copied the full Batch A/B server jar set from the active CurseForge instance with `-Clean`, and the fresh dedicated-server world passed join, terrain generation, structure generation, disconnect/rejoin, and 10-minute stability.
- Active CurseForge client mods path for the latest sync/export pass: `C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)\mods`.
- Batch C combat foundation: installed and validated.
- Batch C validation: passed. Client combat test and dedicated local server test passed with Better Combat, Combat Roll, Simply Swords, playerAnimator, Cloth Config API, and Architectury API.
- Batch D skills/attributes foundation: installed and validated in solo and dedicated server tests.
- Batch E1 world pressure and density: installed and validated.
- Batch E1 install: In Control!, Mowzie's Mobs, Alex's Mobs, Guard Villagers, MVS - Moog's Voyager Structures, YUNG's Extras, and Enhanced Boss Bars.
- Batch E1 dependencies: GeckoLib, Citadel, and Moog's Structure Lib.
- Batch E2 loot, rewards, and contracts: installed and validated.
- Batch E2 install: Artifacts, Bountiful, Loot Beams: Relooted, Villager Names, Loot Journal: Pickup Notifier, and Loot Integrations.
- Batch E2 dependencies: Kambrik, Collective, Fragmentum, Curios API, and Cupboard.
- Batch E2 visual tuning: `config/lootbeams-client.toml` keeps the Loot Beams dropped-item look tooltip enabled, combines item name and rarity into one box, uses rarity-color beams, maxes native beam distance, and limits beams to non-common rarity as the closest built-in filter to Epic+.
- Batch E2 pickup UI tuning: `config/obscuria/loot_journal-client.toml` keeps Loot Journal pickup notifications enabled.
- Batch E2 validation: passed client creative/system test and dedicated server boot/join plus 10-minute stability check. Artifacts, Bountiful, Villager Names, Loot Integrations, Kambrik, Collective, and Fragmentum are stable enough for the next batch.
- Loot Beams: Relooted and Loot Journal: Pickup Notifier remain client-only.
- Batch E2 delayed integration: YUNG Structures Addon for Loot Integrations is not installed because the visible 1.20.1-specific recent file was Fabric, not a clean Forge 1.20.1 target.
- Batch F Arcane Nightfall Expansion: installed and validated.
- Batch F is intentionally larger than prior batches and adds magic, enemy escalation, dangerous events, ocean/ice danger, gear, travel/exploration tools, and medieval build polish.
- Batch F dependencies added by Packwiz: Iron's Lib, Obscure API, CorgiLib, Data Anchor, Kiwi, and Resourceful Lib. Curios API, GeckoLib, and Citadel were already present.
- Batch F delayed/rejected candidates: none from the approved install list; Bosses'Rise had a clean Minecraft 1.20.1 Forge target and was installed.
- Batch F validation: passed client creative/system test and dedicated server boot/join plus 10-minute stability check. Iron's Spells, Born in Chaos, Aquamirae, Enhanced Celestials, Bosses'Rise, Immersive Armors, Spartan Shields, Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences/Walls are stable enough for the next batch.
- Startup crash fix after Batch J: Variants & Ventures was removed from the active pack because its 1.20.1 Forge file crashes on client startup with Entity Model Features during `variantsandventures:murk_skull` model registration. A newer 1.20.2 Variants & Ventures changelog notes skull model crash fixes, but it is not safe to force that file into the 1.20.1 Forge pack.
- Short survival feedback: the world is beautiful but too empty, not dangerous enough, and light on scary mobs and structures.
- Playability status: validated enough to begin long-form survival tuning; balance is not final.
- Batch validation policy: use client boot, creative/system functionality, dedicated server boot/join, and a 10-minute stability check. Disposable survival tests are no longer required after every batch.
- Previous loot beam/UI concern: resolved and not a Batch E2 blocker. Full balance and UI tuning happens later after the major stack is installed.
- Batch G Dragonforge Cataclysm: installed and validated.
- Batch G is intentionally large and adds dragon-tier threats, endgame boss structures, legendary weapon progression, Create engineering, artillery, survival/food depth, and one Create structure addon.
- Batch G install: IceAndFire Community Edition, L_Ender's Cataclysm, Marium's Soulslike Weaponry, Create, Create Big Cannons, Farmer's Delight, and Create: Structures Arise.
- Batch G dependencies added by Packwiz: Jupiter, Uranus, Lionfish API, AttributeFix, Projectile Damage Attribute, and Ritchie's Projectile Library. Curios API and GeckoLib remain both-side and were already part of the pack.
- Batch G validation: passed client creative/system test and dedicated server boot/join plus 10-minute stability check.
- Ice and Fire decision: IceAndFire Community Edition was selected over original Ice and Fire for the 1.20.1 Forge path because it has a current clean Forge/NeoForge 1.20.1 file. It is a community fork and must not be treated as a safe drop-in replacement for existing original Ice and Fire saves.
- Batch H Civilization and Atmosphere: installed and validated.
- Batch H install: Villages&Pillages, MSS - Moog's Soaring Structures, MES - Moog's End Structures, Auroras, Beautiful Enchanted Books, Perception, Medieval Buildings [End Edition], and Medieval Buildings [Nether Edition].
- Batch H dependencies added by Packwiz: OctoLib/ShatterLib for Perception.
- Batch H delayed/rejected candidates: CTOV and Lithostitched are delayed after CTOV crashed during `ctov:medium/village_swamp` feature placement; Biome Music and Medieval Music were delayed from Batch H, then installed in Batch L after clean Packwiz resolution; Neko's Enchanted Books was not installed because Beautiful Enchanted Books had the cleaner exact Forge 1.20.1 file.
- Batch H side split: Villages&Pillages, MSS, MES, and the Medieval Buildings editions are both-side for local multiplayer validation; Auroras, Beautiful Enchanted Books, Perception, and OctoLib/ShatterLib are client-only.
- Custom skill tree integration: upgraded from seven separate tabs into one unified `Ascendant Web` loaded from `config/puffish_skills/`, mirrored into `datapacks/ascendant_realms_skills/`, and mirrored again through Open Loader. The web has 113 nodes, 196 cleaner connections, and seven branch lanes inside one shared progression surface.
- Custom skill tree tooltip/visual pass: implemented. Each node has a fantasy line, an exact visible `Effect:` line, cost metadata, branch metadata, loaded-mod requirements, and pack-system links. The visual layout now acts like a single large upgrade web where players can mix Warrior, Rogue, Ranger, Arcanist, Engineer, Survivalist, and Dragonbound paths without the previous heavy cross-branch line clutter.
- Custom skill tree progression pass: the unified web starts with 2 points, uses one shared Puffish level track, and keeps the default Puffish 1 skill point per level behavior with higher-tier nodes costing more. XP is kill-based, now uses a slower long-term curve, and still scales from killed mob max health so Scaling Health/Improved Mobs naturally make stronger enemies feed stronger progression without inventing commands.
- Traveler's Titles visual pass: installed Visual Traveler's Titles and Visual Traveler's Title Biomes Addon as client-only resource packs, and added a local Ascendant Realms fallback title pack for current Terralith, IceAndFire CE, and Iron's Spells biome/dimension gaps. Biome Edition Visual Traveler's Titles remains delayed because its verified files target Minecraft 1.21.1, not 1.20.1.
- Batch J visual/add-on candidate pass: installed and validated.
- Batch J install: Fantasy Armor, Wavey Capes, Xaero's Minimap, Advancement Plaques, Malfu Combat Animation, Icon Xaero's, Icon Xaero's X FreshAnimations, The Rename Compat Project, Cubic Leaves, Simply Swords Reforged, Cubic Sun & Moon, Embellished Stone, STONEBORN, Excalibur, and Vanilla Experience+.
- Batch J delayed removals: T.O Magic 'n Extras was removed after `traveloptics-6.3.0-1.20.1.jar` crashed against Cataclysm `3.30` with missing `DungeonEyeItem`; Alex's Caves, Apothic Attributes, and Placebo were removed with it because they were only added by that dependency chain.
- Batch J metadata note: T.O Magic had updated Iron's Spells to `3.16.1` and Iron's Lib to `1.1.0`; those versions were carried through the Batch J validation pass.
- Batch J delayed candidate: TravelersCrossroads is not installed because Packwiz rejected it for the configured Minecraft 1.20.1 Forge target, and the visible provider page shows current 1.21.x NeoForge files.
- Batch J risk note: the first startup blockers were Variants & Ventures with Entity Model Features and T.O Magic with Cataclysm. Both are delayed; the remaining Batch J set passed validation.
- Resource-pack persistence fix: Resource Pack Overrides is now installed client-only, `config/resourcepackoverrides.json` mirrors the root `options.txt` order, and Medieval Music is included in the default enabled stack. This should stop Minecraft/CurseForge from making Jayden manually re-enable visual/music packs after closing, reopening, or reimporting the client.
- Resource-pack root-cause fix: the active `Ascendant Realms (1)` log showed `Failed to load options` through `OptionsKeyLwjgl3Fix` on `key.keyboard.left.alt`, which made Minecraft reload only the default/dynamic packs. Root `options.txt` now includes `version:3465`, `scripts/sync-active-client-files.ps1` writes options as UTF-8 without BOM, installs the Resource Pack Overrides jar into the active client, and strips Packwiz `.pw.toml` metadata from the live resourcepacks folder.
- Batch K Identity, Threat UI, and Atmosphere: installed and validated. Weather, Storms & Tornadoes with CoroUtil remains the single major weather path; Simple Clouds/Project Atmosphere remains delayed because of beta/dependency/crash risk.
- Batch L Living World, Body Presence, Music, and Atmosphere: installed and validated. It adds Spawn Balance Utility, Majrusz's Progressive Difficulty, Improved Mobs, Not Enough Animations, AmbientSounds 6, Presence Footsteps, Biome Music, and Medieval Music without adding new boss packs, dragon addons, RPG Series modules, Biomes O' Plenty, Dynamic Trees, Sinytra Connector, or Fabric-only mods.
- Batch L dependencies added by Packwiz: Majrusz Library, TenshiLib, and CreativeCore.
- Batch K/L hotfix: `config/mobhealthbar-client.toml` now prevents proximity-only health bars by requiring hovered, damaged, or aggressive mobs, and AmbientSounds 6 is pinned to `AmbientSounds_FORGE_v6.3.8_mc1.20.1.jar` after `v6.1.0` crashed on startup with CreativeCore `2.12.38`.
- Batch K/L audio route note: Sound Physics Remastered is restored after the zero-audio report was traced to the headphone/output route, not the mod stack.
- Batch L delayed candidates: First-person Model is removed because Jayden disliked the first-person body view; Better Animations Collection remains delayed because it overlaps with Fresh Animations, EMF, ETF, and the existing visual stack.
- Batch L side split: Spawn Balance Utility, Majrusz's Progressive Difficulty, Majrusz Library, Improved Mobs, and TenshiLib are both-side/server-required for local multiplayer validation. Not Enough Animations, AmbientSounds 6, CreativeCore, Presence Footsteps, Biome Music, Medieval Music, Sound Physics Remastered, and YDM's MobHealthBar are client-only.
- Batch N Cohesion Layer: installed and validated. It adds KubeJS, Open Loader, Almost Unified, Almost Unify Everything, Polymorph, Every Compat, Create Slice & Dice, Alex's Delight, Integrated Villages, and IDAS.
- Batch N dependencies added by Packwiz: Rhino, Moonlight Lib, Integrated API, Supplementaries, Quark, and Zeta. Zeta was added explicitly because Quark normally requires it and Packwiz did not pull it automatically with IDAS.
- Batch N integration scaffolds: KubeJS recipe/tag/loot scripts remain cautious scaffolds, while the Ascendant progression bridge and Ascendant Core manifest loader are active. The active skill tree still loads from `config/puffish_skills/`; repo-level `openloader/data/ascendant_realms_skills/` is retained as a legacy/source mirror, not the live OpenLoader injection path.
- Batch N delayed candidates: CraftTweaker, LootJS, Paxi, Item Obliterator, and Integrated Dungeons Arise remain delayed until focused later passes.
- Batch M Lighting, Fire, Lanterns, and Micro-Polish: installed and validated. Active installs are Sodium Dynamic Lights, Sodium Options API, Amendments, Macaw's Lights and Lamps, and Decorative Blocks.
- Batch M startup-warning fix: Amendments is now installed because Supplementaries 2.8.0+ moved wall lanterns, skull candles, ceiling pots, ceiling banners, and skull piles into Amendments.
- Batch M delayed candidates: Toni's Immersive Lanterns is delayed because Packwiz resolved its Accessories dependency to `accessories-neoforge-1.0.0-beta.48+1.20.1.jar` in this Forge pack. TxniLib was removed with that delayed chain. RyoamicLights, Hardcore Torches, and Lanterns Belong on Walls are not installed.
- Batch M side split: Amendments, Macaw's Lights and Lamps, and Decorative Blocks are both-side/server-required. Sodium Dynamic Lights and Sodium Options API are client-only and must not be copied to the dedicated server.
- World Integration and Main Menu polish pass: installed and validated. FancyMenu, Konkrete, Melody, WATERMeDIA, WATERMeDIA Binaries, and Immersive UI are client-only UI/video mods; the supplied title image is staged at `config/fancymenu/assets/ascendant_realms_title.png` with `minecraft_title.png` kept as a compatibility alias, the supplied cloud/fog background video is staged at `config/fancymenu/assets/ascendant_realms_background.mp4`, generated config surfaces were imported from the active client instance, and `docs/WORLD_INTEGRATION_AUDIT.md` inventories the current world/data surface.
- Crash fix pass: Integrated Villages has now produced the same `Holder$Reference` to `PoiType` worldgen crash from `integrated_villages:airship_village`, `integrated_villages:mossy_mounds`, and `integrated_villages:marketstead_village`. The shared root path is the Integrated API `integrated_api:workstation_processor`, not three unrelated bad structures. The active OpenLoader fix lives in `config/openloader/data/ascendant_realms_world_integration`, replaces that processor with static `minecraft:rule` workstation placeholder replacements, restores those village structures for retest, and keeps only the nonexistent `integrated_villages:swamp_village` tag repair.
- World integration audit summary: 172 jars scanned, 64 jars with world/data integration surfaces, 623 structures, 333 structure sets, 1,586 template pools, 696 placed features, 631 configured features, 98 biome modifiers, 614 biome tags, 4,324 loot tables, 10,551 recipes, 1,065 item tags, and 145 entity type tags.
- Main menu status: FancyMenu/Immersive UI and the packaged title asset passed the latest playtest. Jayden's saved FancyMenu title-screen layout is now packaged at `config/fancymenu/customization/custom_title_screen_layout.txt`, enabled for `title_screen`, guarded by `scripts/check-pack.py`, and now has its MP4 background block enabled by default because WATERMeDIA and WATERMeDIA Binaries are installed. Drippy Loading Screen options are also packaged under `config/drippyloadingscreen/`.
- Main menu video hotfix: the supplied background MP4 was found by FancyMenu/WaterMedia but failed native playback, then FancyMenu auto-cleared it after the watchdog timeout. The packaged `config/fancymenu/assets/ascendant_realms_background.mp4` is now re-encoded as video-only H.264 Baseline 1920x1080/30fps, with the original preserved as `ascendant_realms_background_original.mp4`.
- Weather path: Weather, Storms & Tornadoes remains the single major weather system. Simple Clouds and Project Atmosphere remain delayed and must not be stacked with Weather2.
- Real survival tuning: active. The first tuning pass makes the start harder, keeps long-term skill growth slower, increases village/structure density, and adds more visible NPC defense without installing another worldgen pack.
- Current structure density tuning: Sparse Structures global spread is now `1.25`, vanilla villages are back to factor `1.0`, pillager outposts are slightly rarer at `1.1`, Towns and Towers towns/towers/other structures are widened, Integrated Villages regular villages are widened to `64/32` with a larger exclusion zone, and standalone Guild structures are widened to reduce duplicate boards near villages.
- Current village/NPC tuning: Guard Villagers now uses `10` guards per village, regular guard patrols, `24` guard health, and `28` guard follow range.
- Current difficulty tuning: Majrusz group pressure and spawn scaling are raised conservatively, Spawn Balance Utility weight bounds are widened to `12-110`, and the Ascendant Web XP curve is slowed to `min(55 + level ^ 1.82 * 11, 2400)` with kill XP `dropped_xp * 0.75 + max_health / 24`.
- Latest multiplayer playtest: server was shut down after the session. Player titles/levels were not visible above names and enemy numeric levels were not visible; the player level gap is now addressed by the Ascendant progression bridge, while enemy numeric levels remain a later overlay task.
- Player identity/progression bridge staged: `config/openloader/data/ascendant_realms_identity/` now displays `ar_skill_level` below player names, assigns a static `[Ascendant]` prefix to unteamed players, and lets KubeJS mirror real Puffish Skills Ascendant Web levels into the scoreboard.
- Skill tree readability pass: the Ascendant Web still has 113 nodes, but the layout was regenerated as cleaner branch lanes with 196 connections instead of the older dense 343-connection web.
- Custom XP/HUD implementation: `kubejs/server_scripts/ascendant_progression.js` now reads the Puffish Skills Ascendant Web API, draws a blue vanilla-style segmented skill-XP bar through KubeJS Painter, shows current/required Ascendant XP, mirrors unspent skill points, fires a `Level Up! <level>` popup/sound/banner, and updates `ar_skill_level` for multiplayer nameplates.
- Custom XP/HUD startup hotfix: the first live bridge reached the active client but failed to load because KubeJS blocked direct `java.nio.file.Files` access, then the next live log showed Rhino/KubeJS rejecting repeated block-scoped loop variables and `Java.from`. `ascendant_progression.js` and `ascendant_core_integration.js` now use KubeJS `JsonIO`, safer runtime loop variables, one-time HUD bridge logging, and a guarded paint call. `scripts/check-pack.py` blocks the failed patterns, and the fixed files were synced to `C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (1)`.
- Custom XP/HUD JSON-read hotfix: the latest live log showed KubeJS blocking `java.io.File` after the earlier `Path.resolve(String)` ambiguity fix. The KubeJS bridges now build config paths from the allowed `KubeJSPaths.CONFIG` handle and pass those paths to `JsonIO`, so they can read `config/ascendant_progression/progression.json` and `config/ascendant_core/*.json` without loading blocked Java file/path classes.
- Custom level bar asset: Jayden's 182x10 level bar remains staged for FancyMenu/SpiffyHUD browsing at `config/fancymenu/assets/ascendant_level_bar_spritesheet.png`, but the live HUD no longer uses that texture because the in-game crop/tint path produced a dirty gray overlay.
- Custom XP/HUD visual layout hotfix: the live HUD data bridge is confirmed working in-game because level, SP, and skill XP matched the Ascendant Web. The failed visual pass used a custom PNG fill, drew too high, and left a gray slab over the bar. The HUD now draws a compact 20-segment blue strip that mimics the vanilla XP bar rhythm: smaller `Lv`/SP labels, tiny XP text, no custom texture crop, no gray slab, `draw_mode=ingame` so resource-pack/menu screens do not show it, and explicit creative/spectator hiding. Iron's Spells mana is shifted up by one row through `config/irons_spellbooks-client.toml`, and Overflowing Bars client config is tracked for the current hotbar/status stack.
- Traveler's Titles styling hotfix: `config/travelerstitles-forge-1_20.toml` is now tracked and synced, and `options.txt` loads Visual Traveler's Titles, the biome addon, and the Ascendant fallback after Vanilla Experience+ so biome/dimension popup fonts and colors are not flattened to plain white.
- Custom skill-point pacing: `config/ascendant_progression/progression.json` adds configurable managed bonus points at levels 10, 20, 35, 50, 70, 90, and 110 while preserving any manual/admin extra points.
- Enemy level gap: Scaling Health is active for threat scaling, but the inspected configs do not expose a numeric enemy-level nameplate. Keep YDM's MobHealthBar for health readability while a proper enemy-level overlay is researched or built.
- Universal integration index: `docs/UNIVERSAL_MOD_INDEX.md`, `docs/UNIVERSAL_RARITY_AND_INTEGRATION.md`, and `config/ascendant_index/rarity_schema.json` now inventory the active mod/resource/shader list and mark which systems need rarity, loot, spawn, skill, structure, or UI integration.
- UI customization tooling pass: installed SpiffyHUD, Drippy Loading Screen, Item Borders, Stylish Effects, Overflowing Bars, and AppleSkin. SpiffyHUD/Drippy/Item Borders/Stylish Effects/Overflowing Bars are client-only; AppleSkin is both-side for accurate multiplayer food/saturation data.
- UI test status: Packwiz refresh, check-pack, client export, and server staging export passed. In-game visual testing still needs to confirm SpiffyHUD can support the custom HUD direction, Drippy can style the loading screen, Item Borders match rarity, Stylish Effects stays readable, Overflowing Bars handles scaled stats, and AppleSkin reads food clearly.
- Gear rarity index pass: generated separate indexes for weapons, armor, shields, magic/spells, and accessories/relics. Current generated registry covers 499 weapons, 601 armor entries, 77 shields, 273 magic items, 113 spells, and 160 accessories/relics from the active Packwiz jar set.
- Item Borders rarity pass: `config/itemborders-common.toml` is generated from `config/ascendant_index/gear_registry.json` with exact item-ID manual borders, so the inventory frame follows the assigned Ascendant rarity color instead of the item display-name color.
- Gear rarity script: `scripts/generate-gear-rarity-index.ps1` scans only Packwiz-selected jars in the active CurseForge instance, excludes stale instance leftovers, spawn eggs, render-only item model variants, and utility cooking knives, writes a no-op KubeJS metadata file at `kubejs/startup_scripts/ascendant_gear_rarity.js`, and writes client tooltip lines at `kubejs/client_scripts/ascendant_rarity_tooltips.js`.
- Gear tooltip pass: every indexed non-utility gear item now gets one generated KubeJS tooltip line: the rarity tier label. The label is inserted under native damage/speed/stat lines and before green combat behavior lines such as attack range. The `Rarity:` prefix, backend `Effect:`, `Index:`, and `Why:` lines are intentionally hidden from player-facing item tooltips. Legendary, Mythic, and Ascendant labels are bold; Mythic and Ascendant use clean tier text only, without side symbols or extra `Flame`/`Pulse` wording.
- Runic Grimoire JEI pass: `kubejs/client_scripts/ascendant_jei_aliases.js` registers the NBT-backed Patchouli stack `patchouli:guide_book` with `patchouli:book=simplyswords:runic_grimoire`, so JEI can surface the Simply Swords Runic Grimoire even though it is not a standalone item ID. The JEI add-item hook now passes the stack directly instead of wrapping it in an array, avoiding the old `ingredients must not be empty` JEI plugin warning.
- Latest startup/resource hotfix: `config/itemborders-common.toml` is now written without a UTF-8 BOM after Forge/NightConfig crashed on `ï»¿#`, `config/amendments-client.toml` disables Amendments' custom jukebox disc model/spin to avoid the Cataclysm animated `music_disc_maledictus` mask resource error, and the KubeJS rarity bridge no longer mutates `item.rarity` after Iron's Spells `InkItem` rejected that field during startup.
- Guild/Hunter RPG spine: first implementation pass installed and scaffolded. Patchouli, FTB Quests, FTB Ranks, Easy NPC, CustomNPCs-Unofficial, Human Companions, and MCA Reborn are now active Packwiz tooling for the Guild/Hunter layer.
- Guild/Hunter generated data: `config/ascendant_guild/` now defines the rank ladder, rival hunter roster, bounty categories, Hunter Board templates, NPC role roster, formal NPC equipment loadouts, nameplate profiles, generated NPC spawn sets, and active Bountiful contract pools. `config/ascendant_settlements/` now owns the standalone Guild/Hunter worldgen pilot contract. `config/openloader/data/ascendant_realms_codex/` adds the starter Patchouli Ascendant Codex, and `kubejs/startup_scripts/ascendant_guild_items.js` adds Guild Mark, Hunter Seal, and Ascendant Sigil starter currency items.
- Guild/Hunter validation status: installed/scaffolded but not yet passed. Client boot, creative/system checks, dedicated server boot/join, MCA Reborn village checks, NPC tool checks, FTB Quests/Ranks checks, and 10-minute stability still need a fresh client import and test.
- MCA medieval pass: installed MCA Reborn `minecraft-comes-alive-7.6.16+1.20.1-universal.jar` and MCA - Default Medieval clothes-only `MCAR_VanillaMedieval_Universal_1.20.x_Only_Clothes_byDE4THR4SH_v4.zip`. Local inspection found 974 MCA clothing PNGs across normal/burnt/zombie states, male/female/neutral variants, and 23 profession/life-stage buckets. Visual skin control still needs in-game validation.
- Guild/Hunter delayed pieces: FTB quest chapters, FTB rank config, actual NPC placement, Hunter Board structures/templates, custom animated nameplate overlay, Guild currency textures, and final Codex copy still require in-game authoring.
- Root-cause fix policy: active. Future issues should be traced to the smallest broken config/data/resource/script/mod boundary and repaired through a documented compatibility shim before removing content. See `docs/ROOT_CAUSE_FIX_POLICY.md`.
- Current compatibility-shim pass: staged. `config/openloader/data/ascendant_realms_world_integration/` now also repairs Human Companions biome typo tags, IceAndFire CE `c:bosses`, IDAS optional Ars/BOP/BYG hooks, malformed Iron's Spells loot tables, and broken optional Every Compat/Alex's Delight/Spartan Shields compat data. See `docs/FULL_SYSTEM_GAP_REVIEW.md`.
- Identity fallback command fix: staged. `ascendant_identity:load` now uses `belowName` instead of the rejected `below_name` display slot, so player level/name visibility can be retested without removing the identity layer.
- Functionality impact from the latest fixes: intended to be preservative. Integrated Villages content remains active; only the crash-prone POI processor is replaced. Rarity tooltips remain client-only and do not mutate item stats. JEI/Patchouli grimoire handling removes only the duplicate subtype hook. Resource fallbacks add missing visuals without changing gameplay.
- Custom Hero automation pass: active. `scripts/test-customnpcs-identity.js` now catches stale `[Guild]`, stale `[Unranked]` display, and stale stored `Unranked` ranks; `scripts/customnpcs-identity-audit.py` audits and repairs saved CustomNPC entities, including embedded script copies; and `scripts/sync-active-client-files.ps1` syncs current config/script data into the active CurseForge instance.
- CustomNPCs root-cause note: placed NPCs embed their own script copy. Source-file updates do not automatically update already placed NPCs, so saved-world repair is required for old prototypes. The active Rank Examiner issue is a stale saved entity, not a missing profile definition.
- CustomNPCs saved-world repair: applied to `C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms\saves\New World`. The old Rank Examiner prototype was repaired from `[Unranked]` to `[B-Rank] Rank Examiner | Lv.52 Examiner`, the stale title was cleared, and the embedded script copy was replaced. A clean audit now reports `0` stale CustomNPC identity records.
- Generated Guild worldgen feedback pass: staged. Generated CustomNPC spawn functions now use bridged MCA-medieval-style skins from `resourcepacks/ascendant-realms-compat-fixes/assets/customnpcs/textures/entity/ascendant_mca/`, and those same skins are mirrored into `customnpcs/assets/customnpcs/textures/entity/ascendant_mca/` so CustomNPCs can resolve them through its own resource surface instead of showing magenta missing textures. NPCs also use visible role gear from `config/ascendant_guild/npc_loadouts.json`, CustomNPCs top-level `Weapons`/`Armor` render data, and empty `NpcInv` drop-table data so gear renders without becoming free loot. Standalone Guild structure spacing is now `192/80`, `224/96`, and `288/128` after the first village produced too many board structures.
- Generated Guild structure repair pass: staged. Hunter boards, roadside camps, and frontier outposts now use multiple written Supplementaries notice boards, their containers use `ascendant_guild:chests/*` loot tables, notice boards face outward, and wall-adjacent Hunter/Frontier lanterns use Macaw wall lantern blocks instead of freestanding lanterns against walls.
- Full ecosystem overview pass: tooling validation passed after refreshing the newest CurseForge import path. Client sync now targets the newest `Ascendant Realms*` instance, preserves user options by merging only resource-pack lines into `options.txt`, requires MCA - Default Medieval when MCA Reborn is active, enables the FancyMenu MP4 background by default, adds visual-only armor texture aliases for missing Iron's Spells/IceAndFire armor paths, and records the current layer-by-layer health in `docs/SYSTEM_ECOSYSTEM_OVERVIEW.md`.
- Ascendant Core integration layer: implemented and now lightly active. `config/ascendant_core/` owns the pack-level contracts for ranks, regions, mob ecology, structure ecology, loot/rarity, NPC roles, material unification, progression hooks, runtime rules, and future custom modules. `kubejs/server_scripts/ascendant_core_integration.js` loads the core manifest/runtime rules, verifies linked registries, creates shared scoreboards, mirrors region tier, promotes Guild rank from proof counters, and awards conservative Guild reputation/proof counters from known player-killed threats. It still does not rewrite spawns, loot tables, mob stats, or worldgen.
- Ascendant Atlas worldgen/control pass: implemented. `scripts/generate-ascendant-atlas.py` writes the requested `materials.json`, `ore_generation.json`, `recipe_policy.json`, `loot_policy.json`, `mob_policy.json`, `progression_tiers.json`, `dimension_policy.json`, `structure_rewards.json`, `vendor_policy.json`, and `unification_policy.json`, plus the `config/ascendant_atlas/` region, climate, biome, settlement, structure, mob, loot, ore, naming, runtime, and road/bridge contracts. Natural Atlas waymark generation is disabled; the live layer is now the finite coordinate runtime, In Control areas, and density tuning.
- Stability/performance cleanup pass: staged. Vanilla Experience+ now downloads as ASCII `Vanilla Experience Plus.zip`, Resource Pack Overrides retries failed reloads only twice, active-client sync installs URL-backed Packwiz resource packs and removes stale color-code filenames, tracked performance configs now cover ModernFix/Embeddium/EntityCulling/Sodium Dynamic Lights/Sound Physics, missing armor texture fallbacks were expanded from active mod assets, and In Control caps were tightened to reduce village wipeouts without removing any mob mods.
- Ascendant Core test helpers: `config/openloader/data/ascendant_realms_core/` adds `/function ascendant_core:status` plus debug proof helpers for structure, boss, and dragon proof validation.
- Bountiful contract hotfix: the generated major Guild objective for `iceandfire:black_frost_dragon` was runtime-invalid in Bountiful despite appearing in the IceAndFire language data. Only that one contract was replaced with the confirmed `iceandfire:ice_dragon` objective so dragon contracts remain active.
- Ascendant unification implementation pass: active. `scripts/generate-ascendant-guild-worldgen.py` now writes expanded registry-backed Bountiful pools with 79 village, 23 town, and 51 major targets while filtering friendly NPC/tooling namespaces and the known-invalid Black Frost objective. `config/incontrol/spawn.json` now adds cap-only settlement-safety pressure tuning for the major mob/boss namespaces instead of removing content. Details live in `docs/ASCENDANT_UNIFICATION_IMPLEMENTATION_PASS.md` and `config/ascendant_core/live_spawn_policy.json`.

## Batch A Installed

Performance:

- ModernFix
- FerriteCore
- Embeddium
- Entity Culling

Shader base:

- Oculus
- Complementary Reimagined shaderpack

Core visual polish:

- Entity Model Features
- Entity Texture Features
- 3D Skin Layers
- Visual Workbench
- Legendary Tooltips
- Enchantment Descriptions
- Particular Reforged
- Subtle Effects
- Traveler's Titles
- Falling Leaves
- Fresh Animations resource pack

QoL:

- JEI
- Sophisticated Backpacks
- Sophisticated Core

Resolved dependencies:

- Bookshelf
- Fzzy Config
- Iceberg
- Kotlin for Forge
- Prism
- Puzzles Lib
- YUNG's API

JEI was chosen over EMI for this first Forge proof because JEI has the broadest expected Forge ecosystem compatibility and many mods list optional JEI support.

## Batch B Installed

Terrain/world:

- Terralith
- Tectonic
- Serene Seasons

Structures:

- Towns and Towers
- Structory
- YUNG's Better Mineshafts
- YUNG's Better Strongholds
- YUNG's Better Dungeons
- YUNG's Bridges

Control:

- Sparse Structures

Resolved dependencies:

- Cristel Lib
- GlitchCore

## Current Direction

Approved proof target: Minecraft 1.20.1 Forge 47.4.20.

Reason: it gives the best overlap across the candidate list for Forge-only/Forge-strong visual polish, structures, bosses, mobs, Create, Iron's Spells, Ice and Fire, Alex's Mobs, Mowzie's Mobs, and shader support through Oculus.

Important tradeoff: the newer RPG Series stack is strongest on Minecraft 1.21.1 NeoForge/Fabric. Those modules remain delayed unless Jayden decides to pivot later.

## Batch C Installed

Batch C is installed and verified. It adds the core combat movement and weapon foundation only.

Combat foundation:

- Better Combat
- Combat Roll
- Simply Swords

Resolved dependencies:

- playerAnimator
- Cloth Config API
- Architectury API

Do not add RPG skills, classes, magic, mobs, bosses, Ice and Fire, RPG Series modules, Bountiful, Artifacts, Alex's Mobs, or Mowzie's Mobs in Batch C.

## Batch D Installed

Batch D is installed and verified. It adds the lightweight skills/classes/stat progression foundation only.

Skills and attributes:

- Pufferfish's Attributes
- Pufferfish's Skills

Resolved dependencies:

- No additional dependency mods were added by Packwiz.

Default Skill Trees was originally used to validate the Pufferfish/Puffish framework, then removed from active Packwiz metadata when the custom Ascendant Realms skill tree was approved. The active pack now uses the custom config-loaded tree described below.

Do not add magic, mobs, bosses, loot systems, Bountiful, Artifacts, RPG Series modules, Alex's Mobs, Mowzie's Mobs, Guard Villagers, Create, ParCool, or additional worldgen in Batch D.

## Batch E1 Installed

Batch E1 is installed and verified. It adds world pressure, scary mobs, village defense, and more structure density without adding magic or loot systems.

World pressure and density:

- In Control!
- Mowzie's Mobs
- Alex's Mobs
- Guard Villagers
- MVS - Moog's Voyager Structures
- YUNG's Extras
- Enhanced Boss Bars

Resolved dependencies:

- GeckoLib
- Citadel
- Moog's Structure Lib

Side metadata:

- Both/server-required for local testing: In Control!, Mowzie's Mobs, Alex's Mobs, Guard Villagers, MVS, Moog's Structure Lib, YUNG's Extras, GeckoLib, Citadel.
- Client-only: Enhanced Boss Bars.

Sparse Structures remains installed. No Sparse Structures config exists locally yet, so Batch E1 keeps Sparse enabled and documents the first density tuning pass in `docs/STRUCTURE_DENSITY_TUNING.md`.

In Control uses a conservative starter `config/incontrol/spawn.json` with safety caps for Alex's Mobs and Mowzie's Mobs. It does not add custom spawns yet.

During E1, Born in Chaos, Ice and Fire, Bosses'Rise, Aquamirae, Enhanced Celestials, Marium's Soulslike Weaponry, Iron's Spells, Bountiful, Artifacts, and RPG Series modules stayed blocked. Bountiful and Artifacts are now part of the approved E2 loot batch.

## Batch E2 Installed

Batch E2 is installed and verified. It adds exploration rewards, rare loot visibility, bounty/contract systems, and villager immersion without adding magic, boss escalation, dragons, Create, or RPG Series modules.

Loot, rewards, and contracts:

- Artifacts
- Bountiful
- Loot Beams: Relooted
- Villager Names
- Loot Journal: Pickup Notifier
- Loot Integrations

Resolved dependencies:

- Kambrik for Bountiful
- Collective for Villager Names
- Fragmentum for Loot Journal
- Curios API for Artifacts
- Cupboard for Loot Integrations

Notifier decision:

- Loot Journal: Pickup Notifier was selected over Pick Up Notifier.
- Pick Up Notifier is not installed to avoid duplicate pickup notification systems.

Side metadata:

- Both/server-required for local testing: Artifacts, Curios API, Bountiful, Kambrik, Villager Names, Collective, Loot Integrations, Cupboard, Fragmentum.
- Client-only: Loot Beams: Relooted, Loot Journal: Pickup Notifier.

Delayed integration:

- YUNG Structures Addon for Loot Integrations is delayed because the visible 1.20.1-specific recent file was Fabric. Do not force it into the Forge 1.20.1 pack unless a clean Forge 1.20.1 file is confirmed.

Loot Beams tuning:

- `config/lootbeams-client.toml` keeps Loot Beams' dropped-item look tooltip enabled but combines item name and rarity into one box.
- Beam color follows item rarity color instead of display-name color.
- Beam distance is set to the native Loot Beams maximum, `24.0`.
- All-item beams are disabled and non-common rarity filtering is enabled. If lower-than-Epic items still show beams, blacklist exact item IDs after the next creative test.

Loot Journal tuning:

- `config/obscuria/loot_journal-client.toml` keeps item pickup, overflow, XP pickup, ray glow, and sounds enabled.
- Loot Journal is the pickup notification UI. Loot Beams is the look-at-dropped-item world tooltip.

During E2, Ice and Fire, Marium's Soulslike Weaponry, Cataclysm, RPG Series modules, Ars Nouveau, Theurgy, Create, Sinytra Connector, Fabric-only mods, and additional worldgen stayed blocked. Batch G later installed the approved dragon/boss/Create escalation set.

Validation passed:

- Client creative/system test passed.
- Dedicated server boot/join test passed.
- 10-minute stability check passed.
- Artifacts, Bountiful, Villager Names, Loot Integrations, Kambrik, Collective, and Fragmentum are stable enough for the next batch.
- Loot Beams: Relooted and Loot Journal: Pickup Notifier remained client-only.
- No disposable survival test is required for Batch E2 validation.
- The previous loot-beam/UI concern is not a blocker for E2.

## Batch F Installed And Verified

Batch F is installed and verified. It is the Arcane Nightfall Expansion and is intentionally larger than prior batches.

Magic:

- Iron's Spells 'n Spellbooks

Danger, enemies, and events:

- Born in Chaos
- Aquamirae
- Enhanced Celestials
- Bosses'Rise

Gear and combat support:

- Immersive Armors
- Spartan Shields

Exploration, travel, and environment:

- Small Ships
- Snow! Real Magic

Building and world polish:

- Handcrafted
- Macaw's Bridges
- Macaw's Fences and Walls

Resolved dependencies:

- CorgiLib for Enhanced Celestials
- Data Anchor for Enhanced Celestials
- Iron's Lib for Iron's Spells 'n Spellbooks
- Obscure API for Aquamirae
- Kiwi for Snow! Real Magic
- Resourceful Lib for Handcrafted
- Curios API, GeckoLib, and Citadel were already installed from earlier batches.

Side metadata:

- Both/server-required for local testing: all Batch F roots and dependencies.
- Client-only visual mods from earlier batches remain client-only.

Batch F does not add Ice and Fire, Marium's Soulslike Weaponry, Cataclysm, RPG Series modules, Ars Nouveau, Theurgy, Create, Sinytra Connector, Fabric-only mods, or additional worldgen/village overhauls.

Validation passed:

- Client creative/system test passed.
- Dedicated server boot/join test passed.
- 10-minute stability check passed.
- Iron's Spells, Born in Chaos, Aquamirae, Enhanced Celestials, Bosses'Rise, Immersive Armors, Spartan Shields, Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences/Walls are stable enough for the next batch.
- IceAndFire Community Edition was later selected for Batch G; original Ice and Fire remains delayed so only one variant is active.
- No disposable survival test is required for batch validation.

Full balance tuning happens later after the major feature stack is installed.

## Batch G Installed And Verified

Batch G is installed and verified. It is the Dragonforge Cataclysm escalation batch.

Dragon tier:

- IceAndFire Community Edition

Endgame bosses and legendary danger:

- L_Ender's Cataclysm
- Marium's Soulslike Weaponry

Engineering, artillery, and structures:

- Create
- Create Big Cannons
- Create: Structures Arise

Food and survival support:

- Farmer's Delight

Resolved dependencies:

- Jupiter for IceAndFire Community Edition
- Uranus for IceAndFire Community Edition
- Lionfish API for L_Ender's Cataclysm
- AttributeFix for Marium's Soulslike Weaponry
- Projectile Damage Attribute for Marium's Soulslike Weaponry
- Ritchie's Projectile Library for Create Big Cannons
- Curios API and GeckoLib were already installed and remain both-side.

Ice and Fire decision:

- Selected IceAndFire Community Edition.
- Original Ice and Fire remains delayed because Batch G can only use one Ice and Fire variant.
- IceAndFire Community Edition is a community fork, not a direct replacement path for existing original Ice and Fire saves. Ascendant Realms has no committed real survival world yet, so there is no current save-migration risk.

Side metadata:

- Both/server-required for local testing: all Batch G roots and dependencies.
- Client-only visual mods from earlier batches remain client-only.

Validation status:

- Batch G client creative/system test passed.
- Batch G dedicated server boot/join and 10-minute stability check passed.
- No disposable survival test is required for Batch G validation.
- Full balance tuning happens later after the major feature stack is installed.
- Real survival tuning is now active after the custom skill tree and Batch K/L/M/N validation passes.

## Batch H Installed

Batch H is installed and verified. It is the Civilization and Atmosphere batch and adds living-world depth, better village presentation, more landmarks, atmosphere, and fantasy UI polish without adding new boss packs, dragon addons, RPG Series modules, Biomes O' Plenty, Dynamic Trees, Ars Nouveau, Theurgy, or extra Create addons.

Civilization and structures:

- Villages&Pillages
- MSS - Moog's Soaring Structures
- MES - Moog's End Structures
- Medieval Buildings [End Edition]
- Medieval Buildings [Nether Edition]

Atmosphere and presentation:

- Auroras
- Beautiful Enchanted Books [MOD EDITION]
- Perception

Resolved dependencies:

- OctoLib/ShatterLib for Perception

Delayed or not installed:

- ChoiceTheorem's Overhauled Village: delayed after an in-world crash during `ctov:medium/village_swamp` feature placement.
- Lithostitched: removed because it was only required by CTOV.
- Biome Music: delayed from Batch H, then installed in Batch L after clean Packwiz resolution.
- Medieval Music: delayed from Batch H, then installed in Batch L after clean Packwiz resolution.
- Neko's Enchanted Books: not installed because Beautiful Enchanted Books had the cleaner exact Forge 1.20.1 file for this batch.
- Biomes O' Plenty, Dynamic Trees, extra Cataclysm addons, Ice and Fire addons, extra Create addons, RPG Series modules, Ars Nouveau, Theurgy, Sinytra Connector, Fabric-only mods, and village/structure packs beyond the Batch N Integrated Villages/IDAS install remain blocked.

Side metadata:

- Both-side for local multiplayer validation: Villages&Pillages, MSS, MES, Medieval Buildings [End Edition], and Medieval Buildings [Nether Edition].
- Client-only: Auroras, Beautiful Enchanted Books, Perception, and OctoLib/ShatterLib.

Validation status:

- Batch H client creative/system test passed.
- Batch H dedicated server boot/join and 10-minute stability check passed.
- No disposable survival test is required for Batch H validation.
- Full balance tuning happens later after the major feature stack is installed.
- Real survival tuning is now active after the custom skill tree and Batch K/L/M/N validation passes.

## Custom Skill Tree Integration

Status: implemented as a custom Puffish Skills config tree, unique-identity pass complete, playtest passed.

Primary auto-load path:

- `config/puffish_skills/`

Fallback/source datapack:

- `datapacks/ascendant_realms_skills/`

Framework:

- Pufferfish's Skills provides the skill UI, categories, points, experience, connections, and rewards.
- Pufferfish's Attributes provides most stat rewards, including stealth, tamed damage/resistance, fortune, shred, damage reflection, fall reduction, projectile speed, mount speed, and sustain.
- Iron's Spells provides Arcanist-specific max mana, mana regeneration, cooldown reduction, cast time reduction, spell resistance, and school spell-power attributes.
- Projectile Damage Attribute is used where the pack already exposes projectile damage.
- Default Skill Trees is no longer active in Packwiz and remains reference-only.

Designed branches:

- Warrior
- Rogue / Duelist
- Ranger / Hunter
- Arcanist
- Engineer / Artificer
- Survivalist / Explorer
- Dragonbound / Endgame

Designed node count:

- 113 total nodes inside one unified category, with early, mid, late, and capstone nodes across seven branch lanes.

Currently functional if Puffish Skills loads the config cleanly:

- Category tabs, node layouts, existing item icons, starting points, costs, branch-specific attribute rewards, styled clear tooltips, and a shared kill-based experience source.
- Cleaner branch-lane connections with 196 bidirectional links instead of the older dense 343-link layout.
- Visible Ascendant Web level nameplate, custom XP bar, skill-point readout, and `Level Up!` popup through the OpenLoader/KubeJS progression bridge.

Tooltip convention:

- Skill name remains the title.
- Main description starts with a short fantasy sentence.
- Main description includes `Effect:` with the exact stat change, such as `Increases Luck by +1 and Stealth by +3%.`
- Shift text shows cost, branch, loaded-mod requirements, spent-point requirements, and pack-system links where relevant.
- Legendary Tooltips remains the item-tooltip visual mod; Puffish skill nodes use Puffish raw JSON text in `definitions.json`.

Future hooks still require later datapack, advancement, config, or KubeJS work:

- Bountiful contract rewards, boss-kill progression, dragon-kill unlocks, Create milestones, spell-cast event XP/school progression, Combat Roll-specific cooldown/stamina rewards, custom art, and deeper loot/quest integration.

## Batch J Visual And Add-On Candidate Pass

Status: installed and verified.

Installed mods:

- Fantasy Armor (Medieval Series)
- Wavey Capes
- Xaero's Minimap
- Advancement Plaques
- Malfu Combat Animation

Installed resource packs:

- Icon Xaero's
- Icon Xaero's X FreshAnimations
- The Rename Compat Project
- Cubic Leaves
- Simply Swords Reforged
- Cubic Sun & Moon
- Embellished Stone (Advancement Plaques)
- STONEBORN - Dwarven-Fantasy Inspired UI Overhaul
- Excalibur
- Vanilla Experience+

Dependency and metadata notes:

- T.O Magic pulled in Alex's Caves, Apothic Attributes, and Placebo through Packwiz, but all four were removed after the Cataclysm `DungeonEyeItem` startup crash.
- T.O Magic also updated Iron's Spells to `irons_spellbooks-1.20.1-3.16.1.jar` and Iron's Lib to `irons_lib-1.20.1-1.1.0.jar`; those versions were carried through the Batch J validation pass.
- Embellished Stone depends on Advancement Plaques.
- Icon Xaero's X FreshAnimations depends conceptually on Icon Xaero's and Fresh Animations.
- Simply Swords Reforged is a resource-pack layer for Simply Swords.

Side metadata:

- Both-side for local multiplayer validation: Fantasy Armor and Malfu Combat Animation.
- Client-only: Wavey Capes, Xaero's Minimap, Advancement Plaques, and all Batch J resource packs.

Delayed:

- T.O Magic 'n Extras is delayed because `traveloptics-6.3.0-1.20.1.jar` crashes on startup with Cataclysm `3.30` due to missing `com/github/L_Ender/Cataclysm/items/Dungeon_Eye/DungeonEyeItem`.
- Alex's Caves, Apothic Attributes, and Placebo are delayed with T.O Magic because they were only added by that dependency chain.
- TravelersCrossroads is delayed because it did not resolve for the configured Minecraft 1.20.1 Forge pack and the visible current project files target 1.21.x NeoForge.

Validation status:

- Batch J client boot and creative/system testing passed.
- Batch J dedicated server boot/join and 10-minute stability check passed.
- No disposable survival test is required for Batch J validation.
- Watch Malfu Combat Animation, Fantasy Armor, and the Iron's Spells/Iron's Lib update first if future client loads or server boots fail.

## Batch K Installed: Identity, Threat UI, And Atmosphere

Status: installed and validated.

Installed mods:

- Titles: `Titles-1.20.1-3.8.3.jar`
- YDM's MobHealthBar: `mobhealthbar-forge-1.20.x-2.3.0.jar`
- Scaling Health: `ScalingHealth-1.20.1-8.0.2+9.jar`
- Sound Physics Remastered: `sound-physics-remastered-forge-1.20.1-1.3.1.jar`
- Weather, Storms & Tornadoes: `weather2-1.20.1-2.8.3.jar`

Installed dependencies:

- Silent Lib: `silent-lib-1.20.1-8.0.0.jar`
- CoroUtil: `coroutil-forge-1.20.1-1.3.7.jar`

Weather recommendation:

- Choose Weather, Storms & Tornadoes for Batch K because it has a clean Minecraft 1.20.1 Forge/NeoForge file and a clear CoroUtil dependency.
- Start with conservative storm/tornado settings.
- Delay Simple Clouds and Project Atmosphere for this batch because Simple Clouds is open beta, Project Atmosphere's current 1.20.1 Forge path depends on Simple Clouds/Gabou's Libs, and a recent public report shows Simple Clouds plus Project Atmosphere crashing together.

Optional/delayed:

- IntegratedPlaytime: optional secondary playtime tracker only; do not base the main rank on playtime.
- Simple Clouds / Project Atmosphere: delayed alternate weather path.
- CustomNameTags, Champions, Health Indicators, Immersive Storms, and Better Clouds: rejected or delayed for current 1.20.1 Forge rules.

Side metadata plan:

- Both-side/server-required for local multiplayer validation: Titles, Scaling Health, Silent Lib, Weather, Storms & Tornadoes, CoroUtil.
- Client-only: YDM's MobHealthBar and Sound Physics Remastered.

See `docs/IDENTITY_AND_TITLES.md`, `docs/ENEMY_THREAT_UI.md`, and `docs/WEATHER_AND_ATMOSPHERE.md`.

## Batch L Installed: Living World, Body Presence, Music, And Atmosphere

Status: installed and validated.

Installed server/both-side systems:

- Spawn Balance Utility: `spawnbalanceutility-1.20-46.13.7.jar`
- Majrusz's Progressive Difficulty: `majruszs-difficulty-forge-1.20.1-1.9.10.jar`
- Improved Mobs: `improvedmobs-1.20.1-1.13.6-forge.jar`

Installed client-side presentation systems:

- Not Enough Animations: `notenoughanimations-forge-1.12.3-mc1.20.1.jar`
- AmbientSounds 6: `AmbientSounds_FORGE_v6.3.8_mc1.20.1.jar`
- Presence Footsteps: `PresenceFootsteps-1.20.1-1.9.1-beta.1.jar`
- Biome Music: `biomemusic-1.20.1-3.5.jar`
- Medieval Music: `MedievalMusic.zip`
- Sound Physics Remastered: `sound-physics-remastered-forge-1.20.1-1.3.1.jar`

Installed dependencies:

- Majrusz Library: `majrusz-library-forge-1.20.1-7.0.8.jar`
- TenshiLib: `tenshilib-1.20.1-1.7.6-forge.jar`
- CreativeCore: `CreativeCore_FORGE_v2.12.38_mc1.20.1.jar`

Side metadata:

- Both-side/server-required for local multiplayer validation: Spawn Balance Utility, Majrusz's Progressive Difficulty, Majrusz Library, Improved Mobs, and TenshiLib.
- Client-only: Not Enough Animations, AmbientSounds 6, CreativeCore, Presence Footsteps, Biome Music, Medieval Music, Sound Physics Remastered, YDM's MobHealthBar, and other visual/audio-only mods.

Delayed:

- Better Animations Collection is delayed because it overlaps with Fresh Animations, EMF, ETF, and the current animation/resource-pack stack.
- First-person Model is removed because Jayden disliked the first-person body view.
- Sound Physics Remastered is restored because the zero-audio report was traced to headphone/output routing. If audio goes silent again, check the Minecraft output device and Windows/Sonar route before changing the mod stack.
- Simple Clouds and Project Atmosphere stay delayed because Weather, Storms & Tornadoes is already the selected major weather path.

See `docs/SPAWN_ECOLOGY_PLAN.md`, `docs/PROGRESSIVE_DIFFICULTY_TUNING.md`, `docs/ELITE_MOB_TUNING.md`, `docs/FIRST_PERSON_AND_ANIMATIONS.md`, `docs/SOUND_AND_MUSIC.md`, and `docs/WEATHER_AND_ATMOSPHERE.md`.

## Repository Structure

- `docs/MOD_CANDIDATES.md` - source candidate list grouped by category.
- `docs/COMPATIBILITY_MATRIX.md` - audit and installed Batch A/B/C/D/E1/E2/F/G/H/J/K/L/M/N plus custom skill tree status.
- `docs/VERSION_AND_LOADER_DECISION.md` - target comparison and approved proof target.
- `docs/BATCH_INSTALL_PLAN.md` - install order and rollback discipline.
- `docs/STRUCTURE_DENSITY_TUNING.md` - Sparse Structures and E1 structure-density notes.
- `docs/DANGER_SPAWN_TUNING.md` - In Control starter rules and danger design notes.
- `docs/DRAGON_AND_BOSS_TUNING.md` - Batch G dragon, boss, artillery, and legendary gear tuning notes.
- `docs/SKILL_TREE_DESIGN.md` - Ascendant Realms custom skill-tree branch and node design.
- `docs/SKILL_TREE_IMPLEMENTATION_PLAN.md` - config/datapack implementation notes and next passes.
- `docs/SKILL_TREE_ATTRIBUTE_MAPPING.md` - confirmed/provisional attribute mapping.
- `docs/SKILL_TREE_BALANCE_NOTES.md` - skill cost and reward tuning notes.
- `docs/SKILL_TREE_TESTING.md` - client and dedicated-server skill-tree validation plan.
- `docs/SKILL_TREE_INTEGRATION_HOOKS.md` - future hooks for contracts, bosses, dragons, Create, magic, and loot.
- `docs/HUD_AND_PROGRESSION_UI.md` - player level/nameplate fallback, level-up popup, and custom HUD-bar requirements.
- `docs/IDENTITY_AND_TITLES.md` - Batch K title, rank, and scoreboard planning.
- `docs/ENEMY_THREAT_UI.md` - Batch K mob health bar and Scaling Health planning.
- `docs/UNIVERSAL_MOD_INDEX.md` - generated active mod/resource/shader index with integration targets.
- `docs/UNIVERSAL_RARITY_AND_INTEGRATION.md` - shared rarity and cross-mod integration contract.
- `docs/MOB_THREAT_INDEX.md` - generated entity/threat registry for spawn tuning, bounties, skill hooks, and future nameplates.
- `docs/STRUCTURE_INDEX.md` - generated structure registry for density, loot, settlement, bounty, and crash-safe integration work.
- `docs/BOUNTY_TARGET_INDEX.md` - generated Guild/Hunter target list for future Bountiful and FTB Quest contract authoring.
- `docs/BOUNTY_POOL_WORKLIST.md` - generated board/tier/reward grouping for future Bountiful pool authoring.
- `docs/SKILL_HOOK_REGISTRY.md` - generated branch hook counts and candidate content for Ascendant Web progression links.
- `docs/SPAWN_TUNING_WORKLIST.md` - generated spawn-review groups for future In Control and mob-ecology tuning.
- `docs/ASCENDANT_INTEGRATION_MATRIX.md` - generated implementation matrix for config, datapack, KubeJS, and custom mod boundaries.
- `docs/WEATHER_AND_ATMOSPHERE.md` - Batch K weather path and audio atmosphere planning.
- `docs/SPAWN_ECOLOGY_PLAN.md` - Batch L spawn ecology and pressure design.
- `docs/PROGRESSIVE_DIFFICULTY_TUNING.md` - Batch L progressive difficulty tuning notes.
- `docs/ELITE_MOB_TUNING.md` - Batch L Improved Mobs tuning notes.
- `docs/FIRST_PERSON_AND_ANIMATIONS.md` - Batch L body-view and animation validation notes.
- `docs/SOUND_AND_MUSIC.md` - Batch L ambience, footsteps, and music validation notes.
- `docs/COHESION_AND_INTEGRATION.md` - Batch N cohesion layer overview.
- `docs/ASCENDANT_REALMS_SEAMLESS_INTEGRATION_MASTER_PLAN.md` - top-level roadmap for making all features feel like one authored RPG, including custom mod thresholds.
- `docs/RECIPE_AND_TAG_UNIFICATION.md` - Batch N KubeJS, Almost Unified, and Polymorph policy.
- `docs/FOOD_AND_HUNTING_INTEGRATION.md` - Batch N Alex's Delight and hunting/food bridge notes.
- `docs/CREATE_AND_FARMERS_DELIGHT_INTEGRATION.md` - Batch N Create Slice & Dice and production hooks.
- `docs/VILLAGE_AND_CITY_INTEGRATION.md` - Batch N Integrated Villages and civilization-risk notes.
- `docs/DUNGEON_AND_LOOT_INTEGRATION.md` - Batch N IDAS and dungeon/loot integration notes.
- `docs/WORLD_INTEGRATION_AUDIT.md` - generated jar-data audit for structures, features, loot, recipes, and tags.
- `docs/SYSTEM_ECOSYSTEM_OVERVIEW.md` - current full-pack layer map, latest fixes, remaining gaps, and next-step checklist.
- `docs/MAIN_MENU_POLISH.md` - FancyMenu, Immersive UI, and supplied title-image setup/test plan.
- `docs/UI_CUSTOMIZATION_TOOLING.md` - SpiffyHUD, Drippy, Item Borders, Stylish Effects, Overflowing Bars, and AppleSkin test plan.
- `docs/GUILD_HUNTER_SYSTEM_RUNDOWN.md` - master rundown for Guild ranks, Hunter Boards, rival hunters, NPCs, Codex, missing tools, assets, and next steps.
- `docs/NPC_EQUIPMENT_AND_VISUAL_IDENTITY.md` - formal NPC equipment/loadout contract tied to player-obtainable gear.
- `docs/ASCENDANT_SETTLEMENTS_UNIFICATION.md` - village, town, Hunter Board, and Guild Outpost ownership plan.
- `docs/ASCENDANT_NAMEPLATES.md` - player/NPC/rival nameplate target and Forge-safe implementation path.
- `docs/ASCENDANT_CORE_INTEGRATION.md` - active data-first core layer, runtime scoreboards, ownership map, and custom-module threshold.
- `scripts/check-pack.py` - validates the current approved Batch A/B/C/D/E1/E2/F/G/H/J/K/L/M/N and custom skill-tree state.
- `scripts/generate-ascendant-skill-web.js` - regenerates the unified Ascendant Web across config, datapack, and Open Loader paths.
- `scripts/generate-universal-mod-index.js` - regenerates the universal mod index and rarity schema from Packwiz metadata.
- `scripts/generate-ascendant-content-registries.ps1` - scans the active client jars and regenerates mob, structure, bounty, skill-hook, and integration-matrix registries.
- `scripts/materialize-server-mods-from-client.ps1` - copies approved server/both-side jars from a working client mods folder into a server folder.
- `config/README.md` - future config landing area.
- `config/README.md` - reviewed config landing area, including the Puffish skill tree auto-load path.
- `config/fancymenu/assets/ascendant_realms_title.png` - supplied main menu title asset.
- `resourcepacks/ascendant-realms-travelers-titles/` - local Traveler's Titles fallback for current Terralith, IceAndFire CE, and Iron's Spells gaps.
- `datapacks/README.md` - datapack fallback/source landing area.
- `openloader/data/ascendant_realms_skills/` - legacy/source mirror of the Ascendant Realms skill datapack; `config/puffish_skills/` remains the active skill-tree load path.
- `config/openloader/data/ascendant_realms_world_integration/` - Open Loader world integration overrides, including the Integrated Villages workstation-processor repair.
- `config/openloader/data/ascendant_realms_identity/` - Open Loader player identity fallback for below-name level, static `[Ascendant]` prefix, and level-up popup.
- `config/ascendant_index/rarity_schema.json` - machine-readable rarity/integration schema generated from the universal index pass.
- `config/ascendant_index/mob_registry.json` - generated entity/threat registry.
- `config/ascendant_index/structure_registry.json` - generated structure/density/loot registry.
- `config/ascendant_index/skill_hook_registry.json` - generated Ascendant Web branch hook candidates.
- `config/ascendant_index/spawn_tuning_worklist.json` - generated spawn-review worklist grouped by mod namespace.
- `config/ascendant_index/integration_matrix.json` - generated implementation and custom-mod threshold matrix.
- `config/ascendant_core/` - pack-owned cohesion contracts for ranks, regions, mobs, structures, loot, NPCs, materials, progression hooks, and custom helper-mod thresholds.
- `config/ascendant_atlas/` - pack-owned region, climate, biome, settlement, structure, mob, loot, ore, and naming contracts for the Atlas layer.
- `config/openloader/data/ascendant_realms_atlas/` - Ascendant Atlas status/debug datapack with debug-only waymark assets.
- `config/ascendant_guild/generated_bounty_targets.json` - generated Guild/Hunter bounty target candidates.
- `config/ascendant_guild/generated_npc_profiles.json` - generated CustomNPC profile set for non-manual Guild NPC placement.
- `config/ascendant_guild/generated_npc_spawn_sets.json` - generated spawn groups for Guild staff, roadside rumor camps, and frontier outposts.
- `config/ascendant_guild/live_bountiful_pools.json` - active Bountiful Guild contract pool summary.
- `docs/GENERATED_NPC_SYSTEM.md` - generated NPC profile/spawn-set test plan.
- `docs/ASCENDANT_GUILD_WORLDGEN.md` - first standalone Ascendant Guild worldgen test plan.
- `docs/ASCENDANT_ATLAS_WORLDGEN.md` - pack-owned Atlas finite-world runtime, active regional biome source, In Control areas, road/bridge policy, debug waymark assets, and remaining helper-module boundary.
- `docs/MATERIAL_UNIFICATION.md`, `docs/ORE_AND_WORLDGEN_CONTROL.md`, `docs/RECIPE_PROGRESSION.md`, `docs/LOOT_TABLE_CONTROL.md`, and `docs/MOB_SPAWN_AND_DROP_CONTROL.md` - Ascendant Core control docs generated from the unification pass.
- `docs/BOUNTIFUL_GUILD_CONTRACTS.md` - active Bountiful Guild contract pool notes.
- `config/ascendant_guild/bounty_pool_worklist.json` - generated future board/tier/reward grouping for bounty pool authoring.
- `config/ascendant_guild/npc_loadouts.json` - generated NPC and rival equipment profiles sourced from the gear registry.
- `config/ascendant_guild/nameplates.json` - generated player/NPC/rival nameplate style profiles.
- `config/ascendant_settlements/settlement_unification.json` - standalone Guild/Hunter worldgen pilot, village/worldgen ownership, and custom-mod threshold contract.
- `kubejs/server_scripts/` - server-side pack glue. Recipe/tag/loot scripts remain cautious scaffolds, while the Ascendant progression bridge and Ascendant Core manifest loader are active.
- `kubejs/client_scripts/ascendant_rarity_tooltips.js` - generated player-facing rarity label text for indexed gear, inserted above mod behavior lines.
- `kubejs/client_scripts/ascendant_jei_aliases.js` - client-side JEI alias and tooltip entry for NBT-backed guide items like the Runic Grimoire.

## Hard Rules

- Do not touch `crownfall-colonies`.
- Do not add another new batch until the current tuning pass is checked in-game and Jayden approves the next install.
- Do not add additional external worldgen or village overhauls beyond approved Batch H, Batch N, standalone Ascendant Guild worldgen, and the Ascendant Atlas runtime yet.
- Do not add more combat beyond the verified Batch C foundation and approved Batch F/G gear support until a later batch is approved.
- Do not add original Ice and Fire alongside IceAndFire Community Edition. Do not add Marium addons, Cataclysm addons, extra Ice and Fire addons, RPG Series modules, Ars Nouveau, Theurgy, Create addon flood, Dynamic Trees, Biomes O' Plenty, extra village/structure overhauls beyond H/N, or ParCool yet.
- Do not add additional loot systems beyond the approved Batch E2 set until Jayden approves the next loot/balance pass.
- Do not re-add Default Skill Trees unless the custom tree is deliberately rolled back.
- Do not add Fabric-only mods to Forge/NeoForge without an explicit experimental connector branch.
- Do not use Sinytra Connector.
- Do not use OptiFine.
- Do not add archived/deprecated mods without a documented reason and successful compatibility evidence.
- Do not let boss mods force one giant endgame campaign.

## Validation Commands

```powershell
cd "C:\Users\Jayden\Documents\Robbins Tech\ascendant-realms"
.\scripts\refresh-pack.ps1
python scripts\check-pack.py
.\scripts\export-client-pack.ps1
.\scripts\export-server-pack.ps1
```

Generated exports live under `dist/`, which is ignored. Remove exported ZIPs after validation unless intentionally keeping one for import. Server staging contains Packwiz metadata, not runnable mod jars; use `scripts\materialize-server-mods-from-client.ps1` with the active CurseForge instance `mods` folder before testing a dedicated server. The current active path for the latest sync/export pass is `C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)\mods`; CurseForge may still create duplicate folders, so check the active instance path carefully after each import.

