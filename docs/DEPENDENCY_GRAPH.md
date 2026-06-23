# Dependency Graph

This is a planning graph plus the installed Batch A/B/C/D/E1/E2/F/G/H/J and custom skill-tree dependency record. Exact dependencies for later batches must still be confirmed by Packwiz/provider metadata before installation.

## Ascendant Core Integration Dependency Record

Status: implemented as a data-first core layer.

Active roots:

- `config/ascendant_core/core_manifest.json`
- `config/ascendant_core/rank_progression.json`
- `config/ascendant_core/world_regions.json`
- `config/ascendant_core/mob_ecology.json`
- `config/ascendant_core/structure_ecology.json`
- `config/ascendant_core/loot_rarity_rules.json`
- `config/ascendant_core/npc_role_contracts.json`
- `config/ascendant_core/material_unification.json`
- `config/ascendant_core/progression_hooks.json`
- `config/ascendant_core/custom_module_plan.json`
- `kubejs/server_scripts/ascendant_core_integration.js`

Source dependencies:

- Ascendant generated indexes under `config/ascendant_index/`.
- Guild/Hunter registries under `config/ascendant_guild/`.
- Settlement ownership under `config/ascendant_settlements/`.
- Progression HUD and skill-point pacing under `config/ascendant_progression/`.

Runtime dependencies:

- KubeJS and Rhino must be present because the current live bridge is a KubeJS server script.
- Open Loader identity functions create the same core objectives as a datapack fallback.
- No new mod jar was added for this pass.

Side/deployment decision:

- The core JSON and KubeJS loader are both-side pack data for local multiplayer consistency.
- The core layer does not belong in the materialized server `mods/` folder because it is not a jar. It must be present in exported/synced `config/` and `kubejs/` folders.
- Final dynamic nameplates, NPC runtime behavior, coordinate-aware regions, and encounter direction are still custom-helper-mod candidates, not active jar dependencies yet.

## Gear Rarity Index Dependency Record

Status: generated; client visual retest pending after reimport.

Generated roots:

- `scripts/generate-gear-rarity-index.ps1`
- `config/ascendant_index/gear_registry.json`
- `config/itemborders-common.toml`
- `kubejs/startup_scripts/ascendant_gear_rarity.js`
- `kubejs/client_scripts/ascendant_rarity_tooltips.js`
- `kubejs/client_scripts/ascendant_jei_aliases.js`
- `docs/WEAPON_INDEX.md`
- `docs/ARMOR_INDEX.md`
- `docs/SHIELD_INDEX.md`
- `docs/MAGIC_INDEX.md`
- `docs/ACCESSORY_RELIC_INDEX.md`

Tooling dependencies:

- Item Borders reads `config/itemborders-common.toml` client-side.
- KubeJS reads `kubejs/startup_scripts/ascendant_gear_rarity.js` during startup, but the generated file is intentionally no-op metadata.
- KubeJS reads `kubejs/client_scripts/ascendant_rarity_tooltips.js` client-side to add the player-facing rarity label line.
- KubeJS reads `kubejs/client_scripts/ascendant_jei_aliases.js` client-side to register NBT-backed guide item aliases such as the Simply Swords Runic Grimoire.
- The generator reads Packwiz `mods/*.pw.toml` metadata to decide which active CurseForge jars are valid scan sources.

Side metadata decisions:

- Item Borders remains client-only.
- The generated KubeJS startup script is packaged with the pack because KubeJS is both-side, but it must not modify item rarity fields. Item Borders handles the visible rarity colors client-side.
- The generated KubeJS tooltip script is client-side only and only adds tooltip text.
- The JEI alias script is client-side only and only adds JEI/search/tooltip readability for NBT-backed guide items.
- The generated registry/docs are repo planning/config outputs and do not require server jar materialization.

## Guild/Hunter RPG Spine Dependency Record

Status: installed and scaffolded; client/server validation pending.

Installed roots:

- Patchouli
- FTB Quests
- FTB Ranks
- Easy NPC
- CustomNPCs-Unofficial
- Human Companions

Packwiz-resolved dependencies:

- FTB Quests -> FTB Library, FTB Teams, Architectury API.
- FTB Ranks -> FTB Library.
- Easy NPC -> Easy NPC Core, Easy NPC Config UI.
- Patchouli -> no extra dependency metadata was added by Packwiz.
- CustomNPCs-Unofficial -> no extra dependency metadata was added by Packwiz.
- Human Companions -> no extra dependency metadata was added by Packwiz.

Side metadata decisions:

- Both-side: Patchouli, FTB Quests, FTB Library, FTB Teams, FTB Ranks, Easy NPC, Easy NPC Core, Easy NPC Config UI, CustomNPCs-Unofficial, Human Companions.

Generated integration data:

- `config/ascendant_guild/` holds ranks, rivals, bounty categories, Hunter Board templates, NPC role roster, and the tool audit.
- `config/openloader/data/ascendant_realms_codex/` holds the active Patchouli Ascendant Codex data pack.
- `kubejs/startup_scripts/ascendant_guild_items.js` registers Guild Mark, Hunter Seal, and Ascendant Sigil starter items.

Delayed dependency decisions:

- MCA Reborn is installed as both-side. MCA - Default Medieval is installed, default-enabled as a client-only resource pack, and required for medieval/fantasy-safe MCA clothing.
- FTB quest chapter files and FTB Ranks config are intentionally not generated until the current in-game/editor formats are confirmed.

## Batch A Installed Dependency Record

Installed root mods/assets:

- ModernFix
- FerriteCore
- Embeddium
- Entity Culling
- Oculus
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
- Fresh Animations
- Visual Traveler's Titles
- Visual Traveler's Title Biomes Addon
- Ascendant Realms Traveler's Titles fallback
- Complementary Reimagined
- JEI
- Sophisticated Backpacks

Packwiz-resolved dependencies:

- Visual Workbench -> Puzzles Lib.
- Legendary Tooltips -> Iceberg, Prism.
- Enchantment Descriptions -> Bookshelf.
- Subtle Effects -> Fzzy Config.
- Fzzy Config -> Kotlin for Forge 4.12.0.
- No TRender or TRansition metadata is currently installed. The server materializer treats them as optional Subtle Effects follow-up dependencies if they appear later.
- Traveler's Titles -> YUNG's API.
- Visual Traveler's Titles -> Traveler's Titles.
- Visual Traveler's Title Biomes Addon -> Traveler's Titles.
- Ascendant Realms Traveler's Titles fallback -> Traveler's Titles; covers current Terralith, IceAndFire CE, and Iron's Spells gaps.
- Sophisticated Backpacks -> Sophisticated Core.
- Entity Model Features -> Entity Texture Features.
- Oculus -> Embeddium already installed.

Side metadata decisions:

- Client-only: Embeddium, Entity Culling, Oculus, EMF, ETF, 3D Skin Layers, Legendary Tooltips, Enchantment Descriptions, Traveler's Titles, Falling Leaves, Fresh Animations, Visual Traveler's Titles, Visual Traveler's Title Biomes Addon, Ascendant Realms Traveler's Titles fallback, Complementary Reimagined, JEI, Bookshelf, Iceberg, Prism.
- Both-side: ModernFix, FerriteCore, Visual Workbench, Puzzles Lib, Sophisticated Backpacks, Sophisticated Core, Particular Reforged, Subtle Effects, Fzzy Config, Kotlin for Forge, YUNG's API.

Multiplayer validation changed the side split: Subtle Effects crashed on a dedicated server when kept client-only with `Registry Object not present: subtle_effects:waterfall_droplet`, so Subtle Effects, Fzzy Config, and Kotlin for Forge are both-side. Particular Reforged was also required by the Forge multiplayer handshake and is both-side for now.

Forge target note: Subtle Effects 1.20.1-1.14.3 requires Forge 47.4.14 or newer, so the pack target is Forge 47.4.20 instead of 47.4.10.

## Visual Foundation

- Fresh Animations -> EMF + ETF for entity model/texture features.
- Traveler's Titles visual resource packs -> Traveler's Titles.
- Ascendant Realms Traveler's Titles fallback -> Terralith biome lang entries, IceAndFire CE Dreadlands entries, Iron's Spells pocket dimension entry.
- Oculus -> Embeddium on Forge/NeoForge shader path.
- Legendary Tooltips -> likely Iceberg depending selected file.
- Enchantment Descriptions -> may require Bookshelf/Iceberg family depending selected file.
- Visual Workbench -> Puzzles Lib.
- Loot Journal -> Fragmentum. Pick Up Notifier is not installed.
- Particular Reforged and Subtle Effects -> visual polish that must stay both-side in this pack unless later testing proves otherwise.
- Falling Leaves, Auroras -> client-only polish stack.

## Batch B Installed Dependency Record

Installed root worldgen/structure/control mods:

- Terralith
- Tectonic
- Serene Seasons
- Towns and Towers
- Structory
- YUNG's Better Mineshafts
- YUNG's Better Strongholds
- YUNG's Better Dungeons
- YUNG's Bridges
- Sparse Structures

Packwiz-resolved dependencies:

- Serene Seasons -> GlitchCore.
- Towns and Towers -> Cristel Lib.
- YUNG's Better Mineshafts -> YUNG's API.
- YUNG's Better Strongholds -> YUNG's API.
- YUNG's Better Dungeons -> YUNG's API.
- YUNG's Bridges -> YUNG's API.

Batch B side metadata decisions:

- Both-side: Terralith, Tectonic, Serene Seasons, GlitchCore, Towns and Towers, Cristel Lib, Structory, YUNG's API, Sparse Structures, YUNG's Better Mineshafts, YUNG's Better Strongholds, YUNG's Better Dungeons, YUNG's Bridges.
- Server-only: none in Batch B for the current private/local workflow.

Sparse Structures and the four intended YUNG structure mods were originally server-only, which excluded them from the active CurseForge client instance and caused the materializer to miss them. They are now both-side so the client export/import carries the jars into the active instance for server materialization.

Validation passed: the updated client export included Sparse Structures, YUNG's Better Mineshafts, YUNG's Better Strongholds, YUNG's Better Dungeons, and YUNG's Bridges. The materializer copied the full Batch A/B server jar set from the active CurseForge instance with `-Clean`. A fresh dedicated-server world passed localhost join, terrain generation, structure generation, disconnect/rejoin, and 10-minute stability.

Real survival tuning is now active. The pack is validated enough for long-form tuning, but not final-balanced.

## Worldgen Foundation

- Terralith -> installed terrain/datapack-style worldgen.
- Tectonic -> installed terrain shaping.
- Serene Seasons -> installed both-side season logic with GlitchCore.
- Towns and Towers -> installed with Cristel Lib.
- YUNG's Better Dungeons/Mineshafts/Strongholds/Bridges -> installed with YUNG's API.
- Sparse Structures -> installed first density-control path.
- Structurify / Structure Control -> deferred alternatives.
- Dynamic Trees -> compatibility addons for biome mods if used; high integration cost.

## Batch C Installed Dependency Record

Installed combat foundation:

- Better Combat
- Combat Roll
- Simply Swords

Packwiz-resolved dependencies:

- Better Combat -> playerAnimator, Cloth Config API.
- Combat Roll -> playerAnimator already installed.
- Simply Swords -> Architectury API.

Batch C side metadata decisions:

- Both-side: Better Combat, Combat Roll, Simply Swords, playerAnimator, Cloth Config API, Architectury API.

Batch C passed client and dedicated server validation. Better Combat, Combat Roll, Simply Swords, playerAnimator, Cloth Config API, and Architectury API are stable enough for the next batch.

## Batch D Installed Dependency Record

Installed skills/classes/stat foundation:

- Pufferfish's Attributes
- Pufferfish's Skills

Packwiz-resolved dependencies:

- Pufferfish's Attributes -> no extra dependency metadata was added by Packwiz.
- Pufferfish's Skills -> no extra dependency metadata was added by Packwiz.

Batch D side metadata decisions:

- Both-side: Pufferfish's Attributes, Pufferfish's Skills.

Default Skill Trees was originally used as the generic validation content for Batch D, then removed from active Packwiz metadata when the custom Ascendant Realms skill tree was approved. It is now reference-only.

Batch D passed solo and dedicated server validation.

## Batch E1 Installed Dependency Record

Installed world pressure and density roots:

- In Control!
- Mowzie's Mobs
- Alex's Mobs
- Guard Villagers
- MVS - Moog's Voyager Structures
- YUNG's Extras
- Enhanced Boss Bars

Packwiz-resolved dependencies:

- Mowzie's Mobs -> GeckoLib.
- Alex's Mobs -> Citadel.
- MVS - Moog's Voyager Structures -> Moog's Structure Lib.
- YUNG's Extras -> YUNG's API already installed.
- Enhanced Boss Bars -> no extra dependency metadata was added by Packwiz.
- In Control! -> no extra dependency metadata was added by Packwiz.
- Guard Villagers -> no extra dependency metadata was added by Packwiz.

Batch E1 side metadata decisions:

- Both/server-required for local testing: In Control!, Mowzie's Mobs, GeckoLib, Alex's Mobs, Citadel, Guard Villagers, MVS, Moog's Structure Lib, YUNG's Extras.
- Client-only: Enhanced Boss Bars.

Server export note: MVS, Moog's Structure Lib, YUNG's Extras, and In Control were moved to both-side for the private/local testing workflow so the active CurseForge client instance carries their jars for materialization.

Batch E1 passed client, creative/system, dedicated server boot/join, and 10-minute stability validation.

## Batch E2 Installed Dependency Record

Installed loot, rewards, and contract roots:

- Artifacts
- Bountiful
- Loot Beams: Relooted
- Villager Names
- Loot Journal: Pickup Notifier
- Loot Integrations

Packwiz-resolved dependencies:

- Bountiful -> Kambrik.
- Bountiful -> Kotlin for Forge already installed.
- Villager Names -> Collective.
- Loot Journal -> Fragmentum.
- Artifacts -> Curios API. This was confirmed by the client missing-dependency screen after the first E2 export.
- Loot Beams: Relooted -> no extra dependency metadata was added by Packwiz.
- Loot Integrations -> Cupboard. This was confirmed by the client missing-dependency screen after the first E2 export.

Batch E2 side metadata decisions:

- Both/server-required for local testing: Artifacts, Curios API, Bountiful, Kambrik, Villager Names, Collective, Loot Integrations, Cupboard, Fragmentum.
- Client-only: Loot Beams: Relooted, Loot Journal: Pickup Notifier.

Loot Journal was selected over Pick Up Notifier. Pick Up Notifier is not installed.

Loot Integrations is installed as a server-side loot bridge. YUNG Structures Addon for Loot Integrations is delayed because the visible 1.20.1-specific recent file was Fabric, not a clean Forge 1.20.1 target.

Batch E2 validation passed:

- Client creative/system test passed.
- Dedicated server boot/join test passed.
- 10-minute stability check passed.
- Artifacts, Bountiful, Villager Names, Loot Integrations, Kambrik, Collective, and Fragmentum are stable enough for the next batch.
- Loot Beams: Relooted and Loot Journal: Pickup Notifier remained client-only.
- No disposable survival test is required for batch validation.
- The previous loot-beam/UI concern is resolved and is not a Batch E2 blocker.

Real survival tuning is now active; final balance still needs long-form play.

## Batch F Verified Dependency Record

Status: installed and validated.

Installed Arcane Nightfall roots:

- Iron's Spells 'n Spellbooks
- Born in Chaos
- Aquamirae
- Enhanced Celestials
- Bosses'Rise
- Immersive Armors
- Spartan Shields
- Small Ships
- Snow! Real Magic
- Handcrafted
- Macaw's Bridges
- Macaw's Fences and Walls

Packwiz-resolved dependencies:

- Enhanced Celestials -> CorgiLib, Data Anchor.
- Iron's Spells 'n Spellbooks -> Iron's Lib.
- Aquamirae -> Obscure API.
- Snow! Real Magic -> Kiwi.
- Handcrafted -> Resourceful Lib.
- Born in Chaos dependencies were already present.
- Bosses'Rise dependencies were already present.
- Curios API, GeckoLib, and Citadel were already installed from earlier batches.

Batch F side metadata decisions:

- Both/server-required for local testing: all Batch F root mods and dependencies.
- Client-only visual mods from earlier batches remain client-only.

Batch F is intentionally larger than prior batches. It adds magic, stronger enemy pressure, dangerous events, ocean/ice danger, hostile variety, gear, travel/exploration tools, and medieval building polish.

Batch F validation passed:

- Client creative/system test passed.
- Dedicated server boot/join test passed.
- 10-minute stability check passed.
- Iron's Spells, Born in Chaos, Aquamirae, Enhanced Celestials, Bosses'Rise, Immersive Armors, Spartan Shields, Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences/Walls are stable enough for the next batch.
- Variants & Ventures has no active dependency graph entry now because it was removed after the Batch J startup crash with Entity Model Features and `variantsandventures:murk_skull`.
- No disposable survival test is required for batch validation.

Batch G passed validation. Batch H, Batch J, Batch K, Batch L, Batch M, and Batch N are now validated. Do not add any new boss packs, dragon addons, RPG Series modules, Biomes O' Plenty, Dynamic Trees, Ars Nouveau, Theurgy, extra Create addons, Sinytra Connector, Fabric-only mods, or post-N batch content until Jayden approves the next install.

## Batch G Installed Dependency Record

Status: installed and verified.

Installed Dragonforge Cataclysm roots:

- IceAndFire Community Edition
- L_Ender's Cataclysm
- Marium's Soulslike Weaponry
- Create
- Create Big Cannons
- Farmer's Delight
- Create: Structures Arise

Packwiz-resolved dependencies:

- IceAndFire Community Edition -> Jupiter, Uranus.
- L_Ender's Cataclysm -> Lionfish API, Curios API.
- Marium's Soulslike Weaponry -> AttributeFix, Projectile Damage Attribute, GeckoLib.
- Projectile Damage Attribute is pinned to `projectile_damage-forge-3.2.2+1.20.1.jar`. The first Batch G client load rejected `3.2.3+1.20.1`, so do not let Packwiz pull `3.2.3` again unless a later test proves it safe.
- Create Big Cannons -> Create, Ritchie's Projectile Library.
- Farmer's Delight -> no additional dependency metadata added by Packwiz.
- Create: Structures Arise -> no additional dependency metadata added by Packwiz.
- Curios API and GeckoLib were already part of earlier batches and remain both-side.

Ice and Fire variant decision:

- Selected IceAndFire Community Edition.
- Original Ice and Fire remains delayed so exactly one variant is active.
- IceAndFire Community Edition is a community fork, not a direct replacement path for existing original Ice and Fire saves. No committed real survival world exists yet, so this warning is documented but not currently blocking.

Batch G side metadata decisions:

- Both/server-required for local testing: all Batch G root mods and dependencies.
- Client-only visual mods from earlier batches remain client-only.

Batch G client creative/system and dedicated server validation passed. The custom skill tree gate plus Batch K, Batch L, Batch M, and Batch N validation have now passed, so survival tuning is active.

## Batch H Installed Dependency Record

Status: installed and verified.

Installed Civilization and Atmosphere roots:

- Villages&Pillages
- MSS - Moog's Soaring Structures
- MES - Moog's End Structures
- Auroras
- Beautiful Enchanted Books [MOD EDITION]
- Perception
- Medieval Buildings [End Edition]
- Medieval Buildings [Nether Edition]

Packwiz-resolved dependencies:

- Perception -> OctoLib/ShatterLib.
- Villages&Pillages -> no additional dependency metadata added by Packwiz.
- MSS - Moog's Soaring Structures -> no additional dependency metadata added by Packwiz.
- MES - Moog's End Structures -> no additional dependency metadata added by Packwiz.
- Medieval Buildings [End Edition] -> no additional dependency metadata added by Packwiz.
- Medieval Buildings [Nether Edition] -> no additional dependency metadata added by Packwiz.
- Auroras -> no additional dependency metadata added by Packwiz.
- Beautiful Enchanted Books -> no additional dependency metadata added by Packwiz.

Batch H side metadata decisions:

- Both-side for local multiplayer validation: Villages&Pillages, MSS, MES, Medieval Buildings [End Edition], and Medieval Buildings [Nether Edition].
- Client-only: Auroras, Beautiful Enchanted Books, Perception, and OctoLib/ShatterLib.

Delayed or not installed:

- Biome Music was delayed from Batch H, then installed in Batch L after clean Packwiz resolution.
- Medieval Music was delayed from Batch H, then installed in Batch L after clean Packwiz resolution.
- Neko's Enchanted Books was not installed because Beautiful Enchanted Books had the cleaner exact Forge 1.20.1 file.
- ChoiceTheorem's Overhauled Village is delayed after an in-world crash during `ctov:medium/village_swamp` feature placement.
- Lithostitched is removed because it was only required by CTOV.

Batch H client creative/system and dedicated server tests passed. The custom skill tree remains its own validation/tuning gate.

## Custom Skill Tree Data Pack Record

Status: implemented as `config/puffish_skills/` auto-load source; playtest passed and tuning is active.

Active source:

- `config/puffish_skills/`

Fallback/source datapack:

- `datapacks/ascendant_realms_skills/`

Framework dependencies:

- Pufferfish's Skills -> loads the custom categories, skills, definitions, connections, experience sources, points, and rewards.
- Pufferfish's Attributes -> provides most non-vanilla stat rewards.
- Projectile Damage Attribute -> provides `projectile_damage:generic` for Ranger/Engineer projectile rewards, pending in-game validation.

Data pack structure:

- `pack.mcmeta`
- `data/ascendant_realms/puffish_skills/config.json`
- `data/ascendant_realms/puffish_skills/categories/warrior/`
- `data/ascendant_realms/puffish_skills/categories/rogue/`
- `data/ascendant_realms/puffish_skills/categories/ranger/`
- `data/ascendant_realms/puffish_skills/categories/arcanist/`
- `data/ascendant_realms/puffish_skills/categories/engineer/`
- `data/ascendant_realms/puffish_skills/categories/survivalist/`
- `data/ascendant_realms/puffish_skills/categories/dragonbound/`

Each category includes `category.json`, `definitions.json`, `skills.json`, `connections.json`, and `experience.json`.

Side/deployment decision:

- Mods remain both-side: Pufferfish's Attributes, Pufferfish's Skills, and attribute-related dependencies.
- Config tree must be present in the active client/server `config/puffish_skills/` folder.
- Datapack fallback can be installed into a world if the config path fails.
- No custom resource pack is required for this pass because existing item icons are used.

## Batch J Installed Dependency Record

Status: installed and verified.

Installed visual/add-on roots:

- Fantasy Armor (Medieval Series)
- Wavey Capes
- Xaero's Minimap
- Advancement Plaques
- Malfu Combat Animation
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

Packwiz-resolved dependencies and forced metadata changes:

- T.O Magic 'n Extras had resolved to Alex's Caves, Apothic Attributes, and Placebo, but all four are now delayed after `traveloptics-6.3.0-1.20.1.jar` crashed against Cataclysm `3.30` with missing `DungeonEyeItem`.
- T.O Magic 'n Extras updated Iron's Spells to `irons_spellbooks-1.20.1-3.16.1.jar`.
- T.O Magic 'n Extras updated Iron's Lib to `irons_lib-1.20.1-1.1.0.jar`.
- Iron's Spells `3.16.1` and Iron's Lib `1.1.0` were carried through the Batch J validation pass.
- Embellished Stone -> Advancement Plaques.
- Icon Xaero's X FreshAnimations -> Icon Xaero's and Fresh Animations.
- Simply Swords Reforged -> Simply Swords.
- Malfu Combat Animation -> Better Combat.

Batch J side metadata decisions:

- Both-side for local multiplayer validation: Fantasy Armor and Malfu Combat Animation.
- Client-only: Wavey Capes, Xaero's Minimap, Advancement Plaques, Icon Xaero's, Icon Xaero's X FreshAnimations, The Rename Compat Project, Cubic Leaves, Simply Swords Reforged, Cubic Sun & Moon, Embellished Stone, STONEBORN, Excalibur, Vanilla Experience+.

Delayed:

- T.O Magic 'n Extras, Alex's Caves, Apothic Attributes, and Placebo are delayed and must not be active in the current client/server test set.
- TravelersCrossroads is not installed because Packwiz rejected it for the configured Minecraft 1.20.1 Forge target and the visible current project files target 1.21.x NeoForge.

Validation note:

- Batch J client creative/system and dedicated server validation passed. If a future client/server test fails, first confirm the delayed T.O Magic chain is gone from the active instance, then inspect Malfu Combat Animation, Fantasy Armor, and the Iron's Spells/Iron's Lib updates before spending time on cosmetic resource packs.

## Batch K Installed Dependency Record

Status: installed and validated.

Installed Batch K roots:

- Titles: `Titles-1.20.1-3.8.3.jar`
- YDM's MobHealthBar: `mobhealthbar-forge-1.20.x-2.3.0.jar`
- Scaling Health: `ScalingHealth-1.20.1-8.0.2+9.jar`
- Sound Physics Remastered: `sound-physics-remastered-forge-1.20.1-1.3.1.jar`
- Weather, Storms & Tornadoes: `weather2-1.20.1-2.8.3.jar`

Packwiz-resolved dependencies:

- Scaling Health -> Silent Lib `silent-lib-1.20.1-8.0.0.jar`.
- Weather, Storms & Tornadoes -> CoroUtil `coroutil-forge-1.20.1-1.3.7.jar`.
- Sound Physics Remastered has optional integration paths such as Cloth Config and Simple Voice Chat; no new required server dependency is added for the current client-only install.

Delayed/optional dependency paths:

- Project Atmosphere -> Simple Clouds and Gabou's Libs in current Forge 0.7 metadata; Serene Seasons integration is appealing but delayed.
- IntegratedPlaytime has no current main dependency role and should stay optional/server-only if ever installed.

Batch K side metadata decisions:

- Both-side/server-required for local multiplayer validation: Titles, Scaling Health, Silent Lib, Weather, Storms & Tornadoes, CoroUtil.
- Client-only: YDM's MobHealthBar and Sound Physics Remastered.

Materializer status:

- Batch K server patterns are required for Titles, Scaling Health, Silent Lib, Weather, Storms & Tornadoes, and CoroUtil.
- IntegratedPlaytime remains optional/delayed and is not installed.
- Client-only Batch K candidates are flagged as server-review warnings if they appear in the server mods folder.

## Batch L Installed Dependency Record

Status: installed and validated.

Installed Batch L roots:

- Spawn Balance Utility: `spawnbalanceutility-1.20-46.13.7.jar`
- Majrusz's Progressive Difficulty: `majruszs-difficulty-forge-1.20.1-1.9.10.jar`
- Improved Mobs: `improvedmobs-1.20.1-1.13.6-forge.jar`
- Not Enough Animations: `notenoughanimations-forge-1.12.3-mc1.20.1.jar`
- AmbientSounds 6: `AmbientSounds_FORGE_v6.3.8_mc1.20.1.jar`
- Presence Footsteps: `PresenceFootsteps-1.20.1-1.9.1-beta.1.jar`
- Biome Music: `biomemusic-1.20.1-3.5.jar`
- Medieval Music: `MedievalMusic.zip`
- Sound Physics Remastered remains installed from Batch K: `sound-physics-remastered-forge-1.20.1-1.3.1.jar`

Packwiz-resolved dependencies:

- Majrusz's Progressive Difficulty -> Majrusz Library `majrusz-library-forge-1.20.1-7.0.8.jar`.
- Improved Mobs -> TenshiLib `tenshilib-1.20.1-1.7.6-forge.jar`.
- AmbientSounds 6 -> CreativeCore `CreativeCore_FORGE_v2.12.38_mc1.20.1.jar`.
- AmbientSounds `v6.1.0` is rejected with this CreativeCore version because it caused a startup `NoSuchMethodError`; `v6.3.8` is the current crash-fix pin.
- First-person Model is removed because Jayden disliked the first-person body view.
- The zero-audio report was traced to headphone/output routing, so Sound Physics Remastered is restored as a client-only audio mod.

Batch L side metadata decisions:

- Both-side/server-required for local multiplayer validation: Spawn Balance Utility, Majrusz's Progressive Difficulty, Majrusz Library, Improved Mobs, and TenshiLib.
- Client-only: Not Enough Animations, AmbientSounds 6, CreativeCore, Presence Footsteps, Biome Music, Medieval Music, and Sound Physics Remastered.

Materializer status:

- Batch L server patterns are required for Spawn Balance Utility, Majrusz's Progressive Difficulty, Majrusz Library, Improved Mobs, and TenshiLib.
- Batch L client-only body/audio/music mods are flagged as server-review warnings if they appear in the server mods folder.

Delayed:

- Better Animations Collection is delayed because it overlaps with Fresh Animations, EMF, ETF, and the current resource-pack animation stack.
- Simple Clouds / Project Atmosphere remains delayed because Weather, Storms & Tornadoes is the selected major weather path.

## Batch N Installed Dependency Record

Status: installed and validated.

Installed Batch N roots:

- KubeJS: `kubejs-forge-2001.6.5-build.26.jar`
- Open Loader: `OpenLoader-Forge-1.20.1-19.0.5.jar`
- Almost Unified: `almostunified-forge-1.20.1-0.11.0.jar`
- Almost Unify Everything: `unifyeverything-1.20.1-1.0.2.9.jar`
- Polymorph: `polymorph-forge-0.49.10+1.20.1.jar`
- Every Compat (Wood Good): `everycomp-1.20-2.9.23-forge.jar`
- Create Slice & Dice: `sliceanddice-forge-3.6.0.jar`
- Alex's Delight: `alexsdelight-1.5.jar`
- Integrated Villages: `integrated_villages-1.3.2+1.20.1-forge.jar`
- IDAS: `idas_forge-1.13.0+1.20.1.jar`

Packwiz-resolved dependencies and dependency corrections:

- KubeJS -> Rhino `rhino-forge-2001.2.3-build.10.jar`.
- Every Compat -> Moonlight Lib `moonlight-1.20-2.16.33-forge.jar`.
- Create Slice & Dice -> Create and Farmer's Delight, both already installed.
- Alex's Delight -> Alex's Mobs and Farmer's Delight, both already installed.
- IDAS -> Integrated API `integrated_api-1.7.2+1.20.1-forge.jar`.
- IDAS -> Supplementaries `supplementaries-1.20-3.1.43-forge.jar`.
- IDAS -> Quark `Quark-4.0-462.jar`.
- Quark -> Zeta `Zeta-1.0-31.jar`; Zeta was added explicitly because Packwiz did not add it automatically.
- Supplementaries -> Moonlight Lib.

Integration file graph:

- `kubejs/server_scripts/ascendant_recipes.js` -> future recipe bridge; currently comment-only.
- `kubejs/server_scripts/ascendant_tags.js` -> future shared tag bridge; currently comment-only.
- `kubejs/server_scripts/ascendant_loot_notes.js` -> future loot hook notes; currently comment-only.
- `openloader/data/ascendant_realms_skills/` -> legacy/source copy of `datapacks/ascendant_realms_skills/`; active skills load from `config/puffish_skills/`.

Batch N side metadata decisions:

- Both-side/server-required for local multiplayer validation: KubeJS, Rhino, Open Loader, Almost Unified, Almost Unify Everything, Polymorph, Every Compat, Moonlight Lib, Slice & Dice, Alex's Delight, Integrated Villages, IDAS, Integrated API, Supplementaries, Quark, and Zeta.
- Almost Unify Everything and Integrated Villages were changed to both-side for this private workflow so client singleplayer and dedicated server tests see the same behavior.

Delayed dependency paths:

- CraftTweaker is delayed because KubeJS is the chosen scripting layer.
- LootJS is delayed until a focused loot scripting pass verifies exact Forge 1.20.1 support and syntax.
- Paxi is delayed because Open Loader handles the current global datapack need.
- Item Obliterator is delayed until duplicate/trash items are reviewed.
- Integrated Dungeons Arise is delayed until When Dungeons Arise is installed.

## Batch M Installed Dependency Record

Installed Batch M roots:

- Sodium Dynamic Lights: `sodiumdynamiclights-forge-1.0.10-1.20.1.jar`
- Amendments: `amendments-1.20-2.2.5.jar`
- Macaw's Lights and Lamps: `mcw-lights-1.1.5-mc1.20.1forge.jar`
- Decorative Blocks: `decorative_blocks-forge-1.20.1-4.1.3.jar`

Installed Batch M dependency:

- Sodium Dynamic Lights -> Sodium Options API `sodiumoptionsapi-forge-1.0.10-1.20.1.jar`.
- Amendments uses the existing Moonlight Lib path already present from Supplementaries/Every Compat.

Batch M side metadata decisions:

- Client-only: Sodium Dynamic Lights and Sodium Options API.
- Both-side/server-required: Amendments, Macaw's Lights and Lamps, Decorative Blocks.

Delayed Batch M dependency paths:

- Toni's Immersive Lanterns -> Accessories -> TxniLib was removed from the active pack.
- Reason: Toni's Immersive Lanterns resolved as a Forge file, and TxniLib resolved as Forge, but Accessories resolved to `accessories-neoforge-1.0.0-beta.48+1.20.1.jar`. That is not a clean Forge 1.20.1 dependency chain.
- RyoamicLights is delayed/rejected while Sodium Dynamic Lights is selected.
- Hardcore Torches requires explicit approval because it changes survival friction.
- Lanterns Belong on Walls is delayed because the visible 1.20.1 file is Fabric/Quilt; Amendments provides wall lantern coverage cleanly.

## World Integration And Main Menu Polish Dependency Record

Status: installed and validated.

Installed client-only UI roots:

- FancyMenu: `fancymenu_forge_3.9.3_MC_1.20.1.jar`
- WATERMeDIA: Multimedia API: `watermedia-3.0.0.17.jar`
- WATERMeDIA: Binaries: `wm_binaries-3.0.0-rc.1.jar`
- Immersive UI: `ImmersiveUI-FORGE-0.3.0.jar`

Packwiz-resolved dependencies:

- FancyMenu -> Konkrete `konkrete_forge_1.8.0_MC_1.20-1.20.1.jar`.
- FancyMenu -> Melody `melody_forge_1.0.3_MC_1.20.1-1.20.4.jar`.
- FancyMenu video background -> WATERMeDIA: Multimedia API `watermedia-3.0.0.17.jar`.
- WATERMeDIA: Multimedia API -> WATERMeDIA: Binaries `wm_binaries-3.0.0-rc.1.jar`.
- Immersive UI -> no additional Packwiz dependency metadata was added.

Side metadata decisions:

- Client-only: FancyMenu, Konkrete, Melody, WATERMeDIA: Multimedia API, WATERMeDIA: Binaries, Immersive UI.
- Server export/materializer should not include these jars.

World-integration override graph:

- Open Loader -> `config/openloader/data/ascendant_realms_world_integration/`.
- `ascendant_realms_world_integration` -> repairs Integrated Villages' shared `integrated_api:workstation_processor` crash path with static `minecraft:rule` workstation placeholder replacements.
- `ascendant_realms_world_integration` -> repairs Integrated Villages' broken `minecraft:village` structure tag by removing only nonexistent `integrated_villages:swamp_village` while keeping repaired Integrated Villages structures enabled.
- `ascendant_realms_world_integration` -> conservative Mowzie's Mobs biome tag additions for current modded biome coverage.

Audit record:

- `scripts/audit-world-integration.ps1` scanned the active CurseForge instance and generated `docs/WORLD_INTEGRATION_AUDIT.md`.
- The audit inventory covers structures, structure sets, template pools, placed/configured features, biome modifiers, biome tags, loot tables, recipes, item tags, and entity type tags.

## UI Customization Tooling Dependency Record

Status: installed through Packwiz. Packwiz refresh, check-pack, client export, and server staging export passed; in-game visual validation is still pending after client reimport.

Installed UI tooling:

- SpiffyHUD: `spiffyhud_forge_3.1.2_MC_1.20.1.jar`
- Drippy Loading Screen: `drippyloadingscreen_forge_3.1.2_MC_1.20.1.jar`
- Item Borders: `ItemBorders-1.20.1-forge-1.2.2.jar`
- Stylish Effects: `StylishEffects-v8.0.2-1.20.1-Forge.jar`
- Overflowing Bars: `OverflowingBars-v8.0.1-1.20.1-Forge.jar`
- Resource Pack Overrides: `ResourcePackOverrides-v8.0.3-1.20.1-Forge.jar`
- AppleSkin: `appleskin-forge-mc1.20.1-2.5.1.jar`

Packwiz-resolved and already-present dependencies:

- SpiffyHUD -> FancyMenu, Konkrete, Melody.
- Drippy Loading Screen -> FancyMenu, Konkrete, Melody.
- Item Borders -> Iceberg and Prism.
- Stylish Effects -> Puzzles Lib.
- Overflowing Bars -> Puzzles Lib.
- Resource Pack Overrides -> `config/resourcepackoverrides.json` and root `options.txt`.
- AppleSkin -> no extra dependency metadata added by Packwiz.

Side metadata decisions:

- Client-only: SpiffyHUD, Drippy Loading Screen, Item Borders, Stylish Effects, Overflowing Bars, Resource Pack Overrides.
- Both-side/server-required for accurate multiplayer food data: AppleSkin.

Delayed:

- RPG-Hud is delayed as a separate A/B test because it is a full-HUD replacement and may overlap with SpiffyHUD, STONEBORN, Immersive UI, Xaero's Minimap, YDM's MobHealthBar, and the custom skill-tree/HUD direction.

## Combat And RPG Later Planning

- Better Combat -> installed Batch C action-combat foundation.
- Combat Roll -> installed Batch C action movement layer.
- Pufferfish's Attributes -> installed Batch D attribute foundation.
- Pufferfish's Skills -> installed Batch D skills/classes foundation.
- Custom Ascendant Realms skill tree -> implemented as the post-H progression layer; playtest passed and tuning is active.
- Simply Swords -> installed Batch C weapon foundation with Better Combat integration expected.
- Iron's Spells -> installed in Batch F; Iron's Lib is installed and Curios API was already installed.
- Artifacts -> installed in Batch E2 with Curios API.
- Bountiful -> installed in Batch E2 with Kambrik.
- Loot Journal -> installed in Batch E2 with Fragmentum.
- Loot Integrations -> installed in Batch E2 with Cupboard.
- Theurgy -> Modonomicon likely.

Do not add another feature batch until Batch K, Batch L, Batch M, and Batch N validation pass and Jayden approves it. Cataclysm addons, Ice and Fire addons, Marium addons, RPG Series modules, Ars Nouveau, Theurgy, Create addon flood, Dynamic Trees, Biomes O' Plenty, and additional worldgen beyond the Batch N Integrated Villages/IDAS test remain blocked.

Recommended next step: run Batch K client creative/system and dedicated-server validation before adding more civilization, atmosphere, dragon-tier, boss, magic, or RPG systems.

## Mobs And Bosses

- Alex's Mobs -> Citadel. Installed in Batch E1.
- IceAndFire Community Edition -> Jupiter, Uranus. Installed in Batch G.
- Original Ice and Fire -> Citadel; delayed because IceAndFire Community Edition was selected as the single active variant.
- Mowzie's Mobs -> GeckoLib. Installed in Batch E1.
- Born in Chaos -> installed in Batch F.
- Enhanced Celestials -> installed in Batch F with CorgiLib and Data Anchor.
- Guard Villagers -> no extra dependency metadata was added by Packwiz. Installed in Batch E1.
- L_Ender's Cataclysm -> Lionfish API, Curios API. Installed in Batch G.
- Marium's Soulslike Weaponry -> AttributeFix, Projectile Damage Attribute, GeckoLib. Installed in Batch G. Projectile Damage Attribute is pinned to `3.2.2+1.20.1` after the `3.2.3+1.20.1` startup rejection.

## Integration Tools To Research

- KubeJS: likely useful for recipe, tag, loot, and progression glue on Forge 1.20.1.
- In Control: likely useful for spawn weighting, distance/biome/dimension rules, and dragon/boss gating.
- Loot Integrations: installed in E2; useful if YUNG/dungeon loot needs RPG items.
- YUNG Structures Addon for Loot Integrations: delayed until a clean Forge 1.20.1 file is confirmed.
- Datapacks: useful for structure spacing, loot tables, tags, and worldgen datapack overrides.

## Deferred RPG Series Graph

If choosing 1.21.1 NeoForge later:

- Spell Engine -> Spell Power Attributes, Runes, class modules.
- Better Combat -> class weapon animations.
- Archers -> Ranged Weapon API.
- Skill Tree -> RPG class progression.
- Jewelry / Relics / Armory / Arsenal -> loot and gear.

This graph does not currently fit the preliminary 1.20.1 Forge path cleanly.

