# Batch Install Plan

Do not install all candidates. Each batch needs a client boot test, creative/system functionality test, dedicated server boot/join test, 10-minute stability check, and rollback plan. Disposable survival tests are no longer required after every batch; full survival tuning happens after the main feature stack is installed.

## Guild/Hunter RPG Spine

Status: installed and scaffolded, not yet validated.

This pass implements the first playable social/RPG spine from `docs/GUILD_HUNTER_SYSTEM_RUNDOWN.md` without adding another combat, boss, dragon, or worldgen batch.

Installed mods:

- Patchouli
- FTB Quests
- FTB Library
- FTB Teams
- FTB Ranks
- Easy NPC
- Easy NPC Core
- Easy NPC Config UI
- CustomNPCs-Unofficial
- Human Companions
- MCA Reborn
- MCA - Default Medieval resource pack

Generated scaffolds:

- `config/ascendant_guild/` rank, rival, bounty, board, NPC, and tool-audit data.
- `config/openloader/data/ascendant_realms_codex/` starter Patchouli Ascendant Codex.
- `config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank/` starter rank functions.
- `kubejs/startup_scripts/ascendant_guild_items.js` starter Guild currency items.

Side metadata:

- Both-side: all installed Guild/Hunter gameplay mods for first validation, including MCA Reborn. MCA - Default Medieval is client-only because it is a resource pack.

Delayed:

- FTB quest chapter authoring.
- FTB Ranks config authoring.
- Actual Guild NPC placement.
- Hunter Board structure templates.
- Guild currency textures/models.

Test gate:

- Client boot and creative/system test must pass.
- Dedicated server boot/join and 10-minute stability must pass.
- Do not use this as real server progression until FTB Quests/Ranks, NPC placement, Codex content, and board structures are authored.

## Server Utility And Safety

Status: installed and staged; restart validation pending.

This pass adds Jayden-requested maintenance tooling before heavier Chunky pregeneration and live multiplayer tuning.

Installed mods:

- Spark
- FTB Backups 2
- PolyLib

Side metadata:

- Both-side/server-required for local validation: Spark, FTB Backups 2, and PolyLib.

Test gate:

- Restart the dedicated server and confirm the three jars load.
- Run a Spark command during Chunky pregeneration or a heavy fight before guessing at lag sources.
- Confirm FTB Backups creates its backup folder/config on first server boot, then review retention before long pregeneration.

## Batch A: Core Performance / QoL / Client Visual Foundation

Status: installed and validated.

Validation passed: client boot, Complementary Reimagined, Fresh Animations/resource visuals, dedicated local Forge server boot, localhost join, Visual Workbench, Sophisticated Backpack use, disconnect/rejoin, and 10-minute multiplayer stability with shaders enabled.

Startup fix retained: Forge is now 47.4.20 because Subtle Effects 1.20.1-1.14.3 requires Forge 47.4.14 or newer. Kotlin for Forge 4.12.0 is installed for Fzzy Config and remains inside Fzzy Config's required >=4.11.0 and <=4.99.0 range.

Traveler's Titles visual pass: Visual Traveler's Titles and Visual Traveler's Title Biomes Addon are installed as client-only resource packs. A local Ascendant Realms Traveler's Titles fallback pack covers current Terralith, IceAndFire CE, and Iron's Spells biome/dimension gaps. Biome Edition Visual Traveler's Titles is delayed because verified files target Minecraft 1.21.1.

Candidate mods:

- Embeddium
- Oculus
- ModernFix
- FerriteCore
- Entity Culling
- EMF
- ETF
- Fresh Animations resource pack
- Visual Traveler's Titles resource pack
- Visual Traveler's Title Biomes Addon resource pack
- Ascendant Realms Traveler's Titles fallback resource pack
- 3D Skin Layers
- Visual Workbench
- Legendary Tooltips
- Enchantment Descriptions
- Traveler's Titles
- Particular Reforged
- Falling Leaves
- JEI
- Sophisticated Backpacks
- Sophisticated Core as dependency
- Complementary Reimagined shaderpack

Installed dependencies:

- Bookshelf
- Fzzy Config
- Iceberg
- Kotlin for Forge
- Prism
- Puzzles Lib
- YUNG's API

Expected side metadata:

- Client: Oculus, Embeddium, Entity Culling, EMF, ETF, Fresh Animations, Visual Traveler's Titles, Visual Traveler's Title Biomes Addon, Ascendant Realms Traveler's Titles fallback, 3D Skin Layers, Legendary Tooltips, Enchantment Descriptions, Traveler's Titles, Falling Leaves, JEI, Bookshelf, Iceberg, Prism.
- Both: ModernFix, FerriteCore, Visual Workbench, Puzzles Lib, Sophisticated Backpacks, Sophisticated Core, Particular Reforged, Subtle Effects, Fzzy Config, Kotlin for Forge.

Multiplayer finding: Particular Reforged was required by the Forge multiplayer handshake, and Subtle Effects crashed when kept client-only on a dedicated server with `Registry Object not present: subtle_effects:waterfall_droplet`. Subtle Effects, Fzzy Config, and Kotlin for Forge stay both-side while Subtle Effects remains active.

Test:

- Client boots.
- Local server boots if any both-side mods added.
- Shader loads with Complementary Reimagined.
- Fresh Animations works.
- Traveler's Titles visual resource packs are visible in the resource pack list and can be enabled in the documented load order.
- `/dimensiontitle minecraft:the_nether`, `/dimensiontitle iceandfire:dread_land`, and `/dimensiontitle irons_spellbooks:pocket_dimension` preview readable titles if commands are available.
- `/biometitle minecraft:plains`, `/biometitle terralith:red_oasis`, and `/biometitle iceandfire:dread_forest` preview readable titles if commands are available.
- No missing dependency errors.
- JEI opens.
- Server export excludes client-only mods/resource packs/shaderpacks.

Rollback:

- Remove visual mods in reverse dependency order.

## Batch B: Worldgen And Structures

Status: installed and validated.

Validation passed: updated client export included Sparse Structures and the intended YUNG structure jars. The materializer copied the full Batch A/B server jar set from the then-active CurseForge instance using `-Clean`. The current active instance path for the latest ecosystem pass is `C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (1)\mods`. A fresh local dedicated Forge server world passed client join, terrain generation, structure generation, disconnect/rejoin, and 10-minute stability.

Candidate mods:

- Terralith
- Tectonic
- Serene Seasons
- Towns and Towers
- Structory
- YUNG's API
- YUNG's Better Dungeons
- YUNG's Better Mineshafts
- YUNG's Better Strongholds
- YUNG's Bridges
- Sparse Structures

Installed dependencies:

- Cristel Lib for Towns and Towers
- GlitchCore for Serene Seasons

Not installed in Batch B:

- Biomes O' Plenty
- Dynamic Trees
- CTOV
- Integrated Villages
- Moog structures
- YUNG's Better Caves
- YUNG's Extras
- Combat, RPG, magic, mobs, bosses, Ice and Fire, or RPG Series modules

Test:

- Passed on a fresh dedicated-server world.
- Client joined localhost.
- Terrain generated.
- Structures generated.
- Disconnect/rejoin worked.
- Server remained stable for 10 minutes.

Rollback:

- Start a new world after removing worldgen mods.

## Batch C: Combat Movement And Weapons

Status: installed and validated.

Validation passed: Batch C client test and dedicated server test passed. Better Combat, Combat Roll, Simply Swords, playerAnimator, Cloth Config API, and Architectury API are stable enough for the next batch.

Installed mods:

- Better Combat
- Combat Roll
- Simply Swords

Installed dependencies:

- playerAnimator
- Cloth Config API
- Architectury API

Scope limits:

- Combat foundation only.
- No RPG skills.
- No classes.
- No magic.
- No mobs.
- No bosses.
- No Ice and Fire.
- No RPG Series modules.
- No Bountiful.
- No Artifacts.
- No Alex's Mobs.
- No Mowzie's Mobs.

Test:

- Passed client launch and fresh creative test world.
- Passed Better Combat attack animation test.
- Passed Combat Roll keybind and roll test.
- Passed Simply Swords JEI visibility and weapon test.
- Passed vanilla mob combat test.
- Passed shader-on and save/reload checks.
- Passed dedicated Forge 1.20.1-47.4.20 server boot and localhost join.
- Passed no-mod-mismatch multiplayer join.
- Passed disconnect/rejoin.
- Passed 10-minute server stability test.

Rollback:

- Remove movement/combat mods before adding RPG skills.

## Batch D: Skills / Classes / Attributes

Status: installed and validated.

Validation passed: Batch D solo and dedicated server tests passed.

Installed mods:

- Pufferfish's Attributes
- Pufferfish's Skills

Installed dependencies:

- No additional dependency mods were added by Packwiz.

Default Skill Trees was originally installed to validate the framework, then removed after the custom Ascendant Realms skill tree was approved. Pufferfish's Attributes and Pufferfish's Skills remain the active Batch D foundation.

Do not install in Batch D:

- Magic
- Mobs
- Bosses
- Loot systems
- Ice and Fire
- RPG Series modules
- Alex's Mobs
- Mowzie's Mobs
- Guard Villagers
- Create
- ParCool
- Additional worldgen
- Bountiful
- Artifacts

Test:

- Launch client.
- Confirm main menu loads.
- Create or load a creative test world.
- Check keybinds for skills/skill tree UI.
- Open the skill UI if available.
- Confirm skill tree loads without missing textures or broken screens.
- Confirm attributes appear where visible.
- Fight vanilla mobs with Better Combat and Simply Swords.
- Confirm no crash when gaining XP, levels, or skill points.
- Save/reload.
- Export server staging.
- Materialize from active CurseForge instance with `-Clean`.
- Boot Forge 1.20.1-47.4.20 dedicated server.
- Join localhost.
- Confirm no mod mismatch.
- Open skill UI if available.
- Fight vanilla mobs.
- Confirm progression/attributes do not crash.
- Disconnect/rejoin.
- Let server run 10 minutes.

Do not invent commands for giving skill points unless the mod documentation/config clearly exposes them. If commands exist, document them after verification. If not, test through normal XP/combat progression.

Real survival tuning is now active. The pack is validated enough for long-form tuning, but not final-balanced.

Rollback:

- Remove skill/attribute mods and reset test world/player data.

## Batch E1: World Pressure And Density

Status: installed and validated.

Reason: short survival feedback says the world is beautiful but too empty, not dangerous enough, and light on scary mobs and structures.

Installed mods:

- In Control!
- Mowzie's Mobs
- Alex's Mobs
- Guard Villagers
- MVS - Moog's Voyager Structures
- YUNG's Extras
- Enhanced Boss Bars

Installed dependencies:

- GeckoLib for Mowzie's Mobs
- Citadel for Alex's Mobs
- Moog's Structure Lib for MVS

Side metadata:

- Both/server-required for local testing: In Control!, Mowzie's Mobs, Alex's Mobs, Guard Villagers, MVS, Moog's Structure Lib, YUNG's Extras, GeckoLib, Citadel.
- Client-only: Enhanced Boss Bars.

Sparse Structures decision:

- Keep Sparse Structures enabled.
- No local Sparse Structures config exists yet, so do not guess config keys.
- E1 increases density through MVS and YUNG's Extras first.
- See `docs/STRUCTURE_DENSITY_TUNING.md`.

In Control decision:

- Add conservative starter caps in `config/incontrol/spawn.json`.
- Do not add custom spawns, distance scaling, health changes, damage changes, loot changes, or fake skill-point commands.
- See `docs/DANGER_SPAWN_TUNING.md`.

Not installed in Batch E1:

- Magic
- Loot systems
- Ice and Fire
- Born in Chaos
- Bosses'Rise
- Aquamirae
- Enhanced Celestials
- Marium's Soulslike Weaponry
- Bountiful
- Artifacts
- Iron's Spells
- RPG Series modules
- Create
- ParCool
- Additional worldgen beyond the approved E1 structure additions

Validation passed:

- Client boot passed.
- Creative/system functionality test passed.
- Dedicated server boot/join passed.
- 10-minute stability check passed.

Client/creative test:

- Launch client.
- Create fresh creative world.
- Confirm no crash.
- Confirm Mowzie's Mobs appears in JEI.
- Confirm Alex's Mobs appears in JEI.
- Confirm Guard Villagers appears/works.
- Confirm MVS structures can generate or be located if possible.
- Confirm YUNG's Extras generates if locatable.
- Fly 3000-5000 blocks.
- Check whether structure density feels better.
- Spawn hostile mobs from Mowzie/Alex's manually and test combat.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from active CurseForge instance with `-Clean`.
- Boot Forge 1.20.1-47.4.20 dedicated server.
- Use a fresh world name.
- Join localhost.
- Confirm no mod mismatch.
- Fly 3000-5000 blocks.
- Check server TPS.
- Check villages have guards.
- Fight Mowzie/Alex mobs.
- Disconnect/rejoin.
- Let server run 10 minutes.

Rollback:

- Remove E1 mob and structure mods before adding later danger systems.
- Use a fresh world after removing structure mods.

## Batch E2: Loot, Rewards, And Contracts

Status: installed and validated.

Goal: add exploration rewards, rare loot, bounty/contract systems, and loot visibility so dangerous structures and mobs feel worth engaging.

Installed mods:

- Artifacts
- Bountiful
- Loot Beams: Relooted
- Villager Names
- Loot Journal: Pickup Notifier
- Loot Integrations

Installed dependencies:

- Kambrik for Bountiful
- Collective for Villager Names
- Fragmentum for Loot Journal
- Curios API for Artifacts
- Cupboard for Loot Integrations

Startup dependency fix:

- First E2 client load showed `lootintegrations` requires Cupboard `1.20.1-1.5.7` or above, so Cupboard `1.20.1-3.7` was added.
- First E2 client load showed Artifacts requires Curios `5.8.1+1.20.1` or above, so Curios API `5.14.1+1.20.1` was added.

Notifier decision:

- Loot Journal: Pickup Notifier is installed.
- Pick Up Notifier is not installed.
- Rationale: Loot Journal has a current Minecraft 1.20.1 Forge file, explicit client-side metadata, and a richer pickup visibility feature set. Installing both would duplicate the same UX layer.

Optional integration decision:

- Loot Integrations is installed because the selected CurseForge file is `lootintegrations-1.20.1-4.7.jar` for Forge.
- YUNG Structures Addon for Loot Integrations is delayed because the visible 1.20.1-specific recent file was Fabric, not a clean Forge 1.20.1 target.

Side metadata:

- Both/server-required for local testing: Artifacts, Curios API, Bountiful, Kambrik, Villager Names, Collective, Loot Integrations, Cupboard, Fragmentum.
- Client-only: Loot Beams: Relooted, Loot Journal: Pickup Notifier.

Validation passed:

- Client creative/system test passed.
- Dedicated server boot/join test passed.
- 10-minute stability check passed.
- Artifacts, Bountiful, Villager Names, Loot Integrations, Kambrik, Collective, and Fragmentum are stable enough for the next batch.
- Loot Beams: Relooted and Loot Journal: Pickup Notifier remained client-only.
- No disposable survival test is required for Batch E2 validation.
- The previous loot-beam/UI concern is resolved and is not a Batch E2 blocker.
- Full balance and UI tuning happens later after the major stack is installed.

Do not install in Batch E2:

- Magic
- Born in Chaos
- Ice and Fire
- Aquamirae
- Bosses'Rise
- Enhanced Celestials
- Marium's Soulslike Weaponry
- RPG Series modules
- Create
- Iron's Spells
- Additional worldgen
- Additional pickup notifier mods

Client creative/system test:

- Passed client launch.
- Passed creative/system test world.
- Confirmed Artifacts items appeared in JEI.
- Confirmed Bountiful bounty board/items appeared in JEI.
- Confirmed Villager Names worked where visible.
- Confirmed Loot Beams worked on dropped rare items.
- Confirmed Loot Journal pickup notifications worked.
- Spawned/opened village context as needed to inspect Bountiful boards.
- Save/reload passed.

Dedicated server test:

- Server staging exported.
- Server mods materialized from the active CurseForge instance with `-Clean`.
- Server configs copied as needed.
- Forge 1.20.1-47.4.20 dedicated server booted.
- Client joined localhost.
- No mod mismatch blocked join.
- Bountiful worked server-side.
- Artifacts items existed/functioned.
- Villager names appeared where applicable.
- Disconnect/rejoin passed.
- Server remained stable for 10 minutes.

Rollback:

- Remove E2 loot/reward mods and use a fresh test world if loot tables or structures were generated during validation.

## Batch F: Arcane Nightfall Expansion

Status: installed and validated.

Batch F is intentionally larger than prior batches. Goal: add magic, stronger enemy pressure, dangerous events, ocean/ice danger, expanded hostile variety, better armor/shields, travel/exploration tools, and medieval build polish.

Installed mods:

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

Installed dependencies:

- CorgiLib for Enhanced Celestials
- Data Anchor for Enhanced Celestials
- Iron's Lib for Iron's Spells 'n Spellbooks
- Obscure API for Aquamirae
- Kiwi for Snow! Real Magic
- Resourceful Lib for Handcrafted
- Curios API, GeckoLib, and Citadel were already installed in earlier batches.

Side metadata:

- Both/server-required for local testing: all Batch F root mods and dependencies.
- Client-only visual mods from earlier batches remain client-only.

Not installed in Batch F:

- Ice and Fire
- Marium's Soulslike Weaponry
- Cataclysm
- RPG Series modules
- Ars Nouveau
- Theurgy
- Create
- Additional worldgen/village overhauls
- Sinytra Connector
- Fabric-only mods

Bosses'Rise decision:

- Bosses'Rise had a clean Minecraft 1.20.1 Forge target and was installed.

In Control / danger config:

- Do not create reckless spawn rules before testing.
- Born in Chaos, Aquamirae, Enhanced Celestials, and Bosses'Rise are installed with their default behavior for first validation.
- If defaults create too much pressure, tune after the client and server tests identify the actual problem.

Client creative/system test:

- Client creative/system test passed.
- JEI opened.
- Iron's Spells items/spellbooks appeared and basic spell testing passed.
- Born in Chaos and Aquamirae content appeared.
- Enhanced Celestials loaded.
- Immersive Armors and Spartan Shields items appeared.
- Small Ships, Handcrafted, Macaw's Bridges, and Macaw's Fences/Walls items appeared/placed where applicable.
- Selected mobs were spawned manually and fought with Better Combat / Simply Swords / spells.
- Shader-on pass succeeded.
- Save/reload passed.

Dedicated server test:

- Server staging exported.
- Server mods materialized from the active CurseForge instance with `-Clean`.
- Forge 1.20.1-47.4.20 server booted.
- Client joined localhost.
- No mod mismatch blocked join.
- Iron's Spells worked.
- Born in Chaos/Aquamirae content existed.
- Enhanced Celestials did not crash.
- Gear/building/travel items existed.
- Manually spawned mob fight test passed.
- Disconnect/rejoin passed.
- Server remained stable for 10 minutes.

Passed evidence:

- Batch F client creative/system test passed.
- Batch F dedicated server boot/join test passed.
- Iron's Spells, Born in Chaos, Aquamirae, Enhanced Celestials, Bosses'Rise, Immersive Armors, Spartan Shields, Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences/Walls are stable enough for the next batch.
- Variants & Ventures was removed after the Batch J startup crash because its 1.20.1 Forge file crashes with Entity Model Features during `variantsandventures:murk_skull` model registration.
- No disposable survival test is required for batch validation.
- Full balance tuning happens later.

Rollback:

- Remove Batch F mods and dependencies in reverse dependency order.
- Use a fresh test world after removing content, mob, event, or structure-affecting mods.
- Ice and Fire remains reserved for a later dragon-tier batch.

## Batch G: Dragonforge Cataclysm

Status: installed and verified.

Batch G is intentionally large. Goal: add dragon-tier fantasy escalation, endgame boss pressure, legendary weapon progression, Create engineering, siege/artillery options, and survival/food depth.

Installed mods:

- IceAndFire Community Edition
- L_Ender's Cataclysm
- Marium's Soulslike Weaponry
- Create
- Create Big Cannons
- Farmer's Delight
- Create: Structures Arise

Installed dependencies:

- Jupiter for IceAndFire Community Edition
- Uranus for IceAndFire Community Edition
- Lionfish API for L_Ender's Cataclysm
- AttributeFix for Marium's Soulslike Weaponry
- Projectile Damage Attribute for Marium's Soulslike Weaponry
- Ritchie's Projectile Library for Create Big Cannons
- Curios API and GeckoLib were already installed and remain both-side.

Ice and Fire decision:

- Selected IceAndFire Community Edition.
- Original Ice and Fire is delayed because exactly one Ice and Fire variant may be active.
- IceAndFire Community Edition has a current Minecraft 1.20.1 Forge/NeoForge file and clear dependency metadata.
- It is a community fork and is not a direct replacement path for existing original Ice and Fire saves. Ascendant Realms has no committed real survival world yet, so there is no current save-migration risk.

Side metadata:

- Both/server-required for local testing: all Batch G root mods and dependencies.
- Client-only visual mods from earlier batches remain client-only.

Not installed in Batch G:

- Original Ice and Fire
- Cataclysm addons
- Ice and Fire addons
- Marium addons
- Create addon flood
- Ars Nouveau
- Theurgy
- RPG Series modules
- Dynamic Trees
- Biomes O' Plenty
- Extra village overhauls
- Sinytra Connector
- Fabric-only mods

Client creative/system test:

- Launch client.
- Load creative test world.
- Confirm JEI opens.
- Confirm IceAndFire Community Edition appears in JEI.
- Confirm dragon items, dragon eggs, dragon gear, or bestiary content appears.
- Confirm Cataclysm items/entities/structures appear.
- Confirm Marium's Soulslike Weaponry items appear.
- Confirm Create items appear and Ponder works if available.
- Confirm Create Big Cannons appears.
- Confirm Farmer's Delight items appear.
- Confirm Create: Structures Arise appears.
- Spawn one low-tier dragon or Ice and Fire creature manually in an isolated area.
- Spawn one Cataclysm enemy manually, not a full boss rush.
- Spawn/test one Marium weapon.
- Build a tiny Create kinetic setup.
- Test Farmer's Delight basic block/item placement.
- Test shader-on pass.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from active CurseForge instance with `-Clean`.
- Copy server configs if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm IceAndFire Community Edition content exists.
- Confirm Cataclysm content exists.
- Confirm Marium content exists.
- Confirm Create content exists.
- Confirm Farmer's Delight content exists.
- Place/test a tiny Create kinetic setup.
- Place/test Farmer's Delight blocks.
- Spawn one controlled dragon/creature in an isolated area.
- Spawn one controlled Cataclysm enemy.
- Test one Marium weapon.
- Disconnect/rejoin.
- Let server run 10 minutes.

Safety rule:

- Do not spawn multiple dragons, multiple Cataclysm bosses, or multiple Marium bosses at once during validation.
- The goal is stability, not turning the test world into a casualty report.

Rollback:

- Remove Batch G mods and dependencies in reverse dependency order.
- Use a fresh test world after removing dragon, boss, structure, Create, artillery, or food mods.
- Do not swap between original Ice and Fire and IceAndFire Community Edition after a real world starts without a separate migration plan.

Validation result:

- Batch G client creative/system test passed.
- Batch G dedicated server boot/join test passed.
- 10-minute stability check passed.
- No disposable survival test is required for batch validation.

Real survival tuning is now active after the custom skill tree gate and Batch K/L/M/N validation passed.

## Batch H: Civilization and Atmosphere

Status: installed and validated.

Goal: add living-world depth, better villages, more landmarks, atmosphere, and fantasy presentation without massively increasing combat complexity.

Installed mods:

- Villages&Pillages
- MSS - Moog's Soaring Structures
- MES - Moog's End Structures
- Auroras
- Beautiful Enchanted Books [MOD EDITION]
- Perception
- Medieval Buildings [End Edition]
- Medieval Buildings [Nether Edition]

Installed dependencies:

- OctoLib/ShatterLib for Perception

Side metadata:

- Both-side for local multiplayer validation: Villages&Pillages, MSS, MES, Medieval Buildings [End Edition], and Medieval Buildings [Nether Edition].
- Client-only: Auroras, Beautiful Enchanted Books, Perception, and OctoLib/ShatterLib.

Delayed or not installed in Batch H:

- Biome Music was delayed from Batch H, then installed in Batch L after clean Packwiz resolution.
- Medieval Music was delayed from Batch H, then installed in Batch L after clean Packwiz resolution.
- Neko's Enchanted Books was not installed because Beautiful Enchanted Books had the cleaner exact Forge 1.20.1 file.
- ChoiceTheorem's Overhauled Village is delayed after an in-world crash during `ctov:medium/village_swamp` feature placement.
- Lithostitched is removed because it was only required by CTOV.
- Biomes O' Plenty, Dynamic Trees, extra Cataclysm addons, Ice and Fire addons, extra Create addons, RPG Series modules, Ars Nouveau, Theurgy, Sinytra Connector, Fabric-only mods, and village/structure packs beyond the Batch N Integrated Villages/IDAS install remain blocked.

Client creative/system test:

- Launch client.
- Create or load a creative test world.
- Confirm main menu and JEI load.
- Confirm Villages&Pillages content appears in JEI or can be found/spawned safely.
- Confirm MSS and MES structure content appears in `/locate` suggestions if commands expose it.
- Confirm Medieval Buildings End/Nether content appears in `/locate` suggestions if commands expose it.
- Confirm Auroras renders during an appropriate night/weather pass if visible.
- Confirm Beautiful Enchanted Books changes enchanted-book visuals without breaking JEI or enchanting screens.
- Confirm Perception loads with no client crash or visual settings conflict.
- Test shader-on pass.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Copy server configs if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm Villages&Pillages, MSS, MES, and the Medieval Buildings editions are present server-side.
- Confirm client-only H mods are not required by the dedicated server.
- Generate or locate a few H structures in a fresh test world without stress-loading huge distances.
- Disconnect/rejoin.
- Let server run 10 minutes.

Rollback:

- Remove Batch H mods and dependencies in reverse dependency order.
- Use a fresh test world after removing village, structure, or dimension structure mods.
- Do not start a committed survival world until the custom skill tree gate plus Batch K, Batch L, Batch M, and Batch N validation pass.

## Batch I: Custom Skill Tree Integration

Status: implemented as the unified Ascendant Web through `config/puffish_skills/`, validation/tuning gate remains tracked separately. Matching source/fallback copies remain under `datapacks/ascendant_realms_skills/` and `openloader/data/ascendant_realms_skills/`.

Goal: replace generic/default skill-tree behavior with a custom Ascendant Realms progression identity that ties combat, magic, exploration, engineering, survival, loot, dragons, and bosses into one framework.

Active framework:

- Pufferfish's Attributes
- Pufferfish's Skills
- Custom config tree: `config/puffish_skills/`
- Fallback/source datapack: `datapacks/ascendant_realms_skills/`
- Open Loader legacy/source mirror: `openloader/data/ascendant_realms_skills/`
- Generator: `scripts/generate-ascendant-skill-web.js`

Removed from active Packwiz metadata:

- Default Skill Trees

Designed web:

- One Puffish Skills category: `Ascendant Web`
- 113 nodes
- 196 bidirectional connections after the readability pass
- Seven cleaner branch lanes: Warrior, Rogue / Duelist, Ranger / Hunter, Arcanist, Engineer / Artificer, Survivalist / Explorer, Dragonbound / Endgame

Current implementation:

- One large category mirrored into config, datapack source, and Open Loader.
- Two starting points.
- Default Puffish 1 skill point per web level pacing.
- Higher-tier node costs for slow but meaningful progression.
- Attribute rewards using vanilla attributes, Pufferfish's Attributes, Iron's Spells, and Projectile Damage Attribute where detected.
- Unique-identity pass implemented: Arcanist uses Iron's Spells mana/cooldown/spell-school attributes; other branches use specialized stealth, tamed, fortune, shred, reflection, fall-reduction, projectile-speed, travel, crafting, food, and sustain attributes.
- Shared kill-based experience source uses dropped XP plus killed mob max health, so Scaling Health stronger mobs naturally feed more skill XP.
- Anti-farming limits retained.

Future integration work:

- Bountiful contract skill XP or points.
- Boss-kill progression.
- Dragon-kill Dragonbound gates.
- Create milestones for Engineer.
- Spell-cast event XP and school-specific Arcanist progression.
- Combat Roll cooldown/stamina-specific rewards.
- Custom icons/resource pack.
- KubeJS only if datapack/config/advancement hooks cannot cover the desired behavior.

Client test:

- Confirm the imported client instance has `config/puffish_skills/config.json`.
- Launch client.
- Create a fresh test world.
- Open the Pufferfish's Skills UI.
- Confirm one `Ascendant Web` category appears.
- Confirm the old seven custom categories do not appear.
- Confirm Default Skill Trees generic combat/mining tabs do not appear.
- Confirm icons display.
- Hover several nodes and confirm flavor text plus exact `Effect:` lines.
- Unlock root and mid nodes; test capstones only if enough points are available.
- Confirm attributes apply.
- Test Better Combat, Simply Swords, Iron's Spells, projectile behavior, skill XP gain from stronger mobs, and save/reload.

Dedicated server test:

- Export server staging.
- Materialize from active CurseForge instance with `-Clean`.
- Copy server configs from staging so `config/puffish_skills/` exists on the server.
- Boot Forge 1.20.1-47.4.20 dedicated server.
- Join localhost.
- Confirm the unified Ascendant Web appears.
- Unlock nodes and confirm attributes apply server-side.
- Fight vanilla and modded mobs and confirm skill XP/progression does not crash.
- Disconnect/rejoin and confirm persistence.
- Let server run 10 minutes.

Rollback:

- Remove `config/puffish_skills/` from the test instance/server to disable the custom tree.
- Re-run `packwiz refresh` if skill tree files are removed from the pack source.
- Do not re-add Default Skill Trees unless explicitly rolling back to generic progression.

## Batch J: Visual And Add-On Candidate Pass

Status: installed and validated.

Goal: test Jayden's requested visual polish, UI/resource-pack layers, minimap support, fantasy armor, and Better Combat animation polish without starting the next major balance batch.

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

Installed dependencies and forced metadata changes:

- T.O Magic pulled Alex's Caves, Apothic Attributes, and Placebo, but all four were removed after the Cataclysm `DungeonEyeItem` startup crash.
- T.O Magic updated Iron's Spells to `irons_spellbooks-1.20.1-3.16.1.jar`.
- T.O Magic updated Iron's Lib to `irons_lib-1.20.1-1.1.0.jar`.
- Iron's Spells `3.16.1` and Iron's Lib `1.1.0` were carried through the Batch J validation pass.
- Embellished Stone uses Advancement Plaques.
- Icon Xaero's X FreshAnimations is layered with Icon Xaero's and Fresh Animations.
- Simply Swords Reforged is layered with Simply Swords.

Delayed:

- T.O Magic 'n Extras is delayed because `traveloptics-6.3.0-1.20.1.jar` crashes on startup with Cataclysm `3.30` due to missing `com/github/L_Ender/Cataclysm/items/Dungeon_Eye/DungeonEyeItem`.
- Alex's Caves, Apothic Attributes, and Placebo are delayed with T.O Magic because they were only added by that dependency chain.
- TravelersCrossroads is delayed. Packwiz refused it for the configured Minecraft 1.20.1 Forge target, and the visible current project files target 1.21.x NeoForge.

Side metadata:

- Both-side for local multiplayer validation: Fantasy Armor and Malfu Combat Animation.
- Client-only: Wavey Capes, Xaero's Minimap, Advancement Plaques, Icon Xaero's, Icon Xaero's X FreshAnimations, The Rename Compat Project, Cubic Leaves, Simply Swords Reforged, Cubic Sun & Moon, Embellished Stone, STONEBORN, Excalibur, and Vanilla Experience+.

Client creative/system test:

- Launch client.
- Confirm main menu loads with no missing dependency screen.
- Confirm resource packs can be enabled in a sane order with STONEBORN and Vanilla Experience+ reviewed for UI conflicts.
- Create or load a creative test world.
- Confirm Xaero's Minimap appears and can be configured.
- Confirm Wavey Capes works on the player model.
- Confirm Advancement Plaques and Embellished Stone render advancement popups cleanly.
- Confirm Fantasy Armor items appear in JEI and can be equipped.
- Confirm Iron's Spells still works after the version bump.
- Confirm Malfu Combat Animation works with Better Combat and does not break Simply Swords attacks.
- Confirm the requested resource packs do not break item names, icons, or UI readability.
- Test shader-on pass.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Copy server configs if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm Fantasy Armor and Malfu Combat Animation are present server-side.
- Confirm Wavey Capes, Xaero's Minimap, Advancement Plaques, and resource packs are not required server-side.
- Test Better Combat/Simply Swords attacks with Malfu animation.
- Test one basic Iron's Spells spell.
- Disconnect/rejoin.
- Let server run 10 minutes.

Rollback:

- If client load fails, inspect Malfu Combat Animation, Fantasy Armor, Iron's Spells, and Iron's Lib before touching cosmetic resource packs.
- If server boot fails, confirm the delayed T.O Magic chain is not still present in the active CurseForge instance or materialized server.
- If UI is ugly but stable, keep the pack technically valid and move visual tuning to the later polish pass.

## Batch K: Identity, Threat UI, And Atmosphere

Status: installed and validated.

Goal: add earned player identity, enemy threat readability, conservative enemy scaling, and one immersive weather/audio layer.

Installed mods:

- Titles: `Titles-1.20.1-3.8.3.jar`
- YDM's MobHealthBar: `mobhealthbar-forge-1.20.x-2.3.0.jar`
- Scaling Health: `ScalingHealth-1.20.1-8.0.2+9.jar`
- Sound Physics Remastered: `sound-physics-remastered-forge-1.20.1-1.3.1.jar`
- Weather, Storms & Tornadoes: `weather2-1.20.1-2.8.3.jar`

Installed dependencies:

- Silent Lib: `silent-lib-1.20.1-8.0.0.jar`
- CoroUtil: `coroutil-forge-1.20.1-1.3.7.jar`

Optional/delayed:

- IntegratedPlaytime: optional secondary playtime tracker only. Do not base the main rank on playtime.
- Simple Clouds / Project Atmosphere: delayed alternate weather path. Simple Clouds is open beta; Project Atmosphere's current 1.20.1 Forge path depends on Simple Clouds/Gabou's Libs and has a recent public crash report when paired with Simple Clouds.
- CustomNameTags: rejected/delayed because the visible project is Fabric/server-side.
- Champions: rejected/delayed because the current visible project is Fabric-oriented and the pack already has major threat escalation.
- Health Indicators: rejected/delayed because the visible 1.20.1 project lists Fabric/NeoForge/Quilt rather than Forge.
- Immersive Storms: rejected/delayed because the current visible project is Fabric/Quilt and newer-version focused.
- Better Clouds: rejected because the current 1.20.1 file is Fabric.

Weather recommendation:

- Choose Weather, Storms & Tornadoes for the first Batch K install.
- Use conservative configs: reduce storm/tornado frequency, reduce or disable destructive effects if exposed by config, and watch TPS.
- Do not stack Weather, Storms & Tornadoes with Simple Clouds or Project Atmosphere.

Side metadata plan:

- Both-side/server-required for local multiplayer validation: Titles, Scaling Health, Silent Lib, Weather, Storms & Tornadoes, CoroUtil.
- Client-only: YDM's MobHealthBar and Sound Physics Remastered.
- Optional/server-only if ever used: IntegratedPlaytime.

Client creative/system test:

- Confirm client boots with no missing dependency screen.
- Confirm Titles renders earned titles or exposes title UI/commands.
- Confirm scoreboard below-name level display or static team-prefix fallback works.
- Confirm YDM's MobHealthBar renders and passive mobs are hidden or minimally noisy.
- Confirm normal hostiles do not show bars from proximity alone.
- Confirm bars appear only when looking directly at a mob, after damaging it, or while it is actively aggressive.
- Confirm Scaling Health does not crash on vanilla or modded mobs.
- Review generated Scaling Health config before tuning difficulty/blights.
- Confirm Weather, Storms & Tornadoes visuals work with Complementary Reimagined.
- Review generated Weather2 config before allowing destructive/frequent storms in a committed world.
- Confirm vanilla audio works first, then confirm Sound Physics Remastered has no severe muffling, echo, cutoff, or zero-audio symptoms.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Copy server configs if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm Titles, Scaling Health, Silent Lib, Weather, Storms & Tornadoes, and CoroUtil are present server-side.
- Confirm YDM's MobHealthBar is not required server-side unless testing proves otherwise.
- Confirm titles and scoreboard/rank data persist after reconnect.
- Fight vanilla and modded mobs.
- Watch weather logs/TPS during a weather pass if practical.
- Disconnect/rejoin.
- Let server run 10 minutes.

## Batch L: Living World, Body Presence, Music, And Atmosphere

Status: installed and validated.

Goal: increase living-world density and long-term enemy pressure while adding better player animation coverage, richer ambience, footsteps, and fantasy music. This batch does not add boss packs, dragon addons, RPG Series modules, Biomes O' Plenty, Dynamic Trees, Sinytra Connector, or Fabric-only mods.

Installed server/both-side systems:

- Spawn Balance Utility: `spawnbalanceutility-1.20-46.13.7.jar`
- Majrusz's Progressive Difficulty: `majruszs-difficulty-forge-1.20.1-1.9.10.jar`
- Improved Mobs: `improvedmobs-1.20.1-1.13.6-forge.jar`

Installed client-side systems:

- Not Enough Animations: `notenoughanimations-forge-1.12.3-mc1.20.1.jar`
- AmbientSounds 6: `AmbientSounds_FORGE_v6.3.8_mc1.20.1.jar`
- Presence Footsteps: `PresenceFootsteps-1.20.1-1.9.1-beta.1.jar`
- Biome Music: `biomemusic-1.20.1-3.5.jar`
- Medieval Music: `MedievalMusic.zip`
- Sound Physics Remastered: `sound-physics-remastered-forge-1.20.1-1.3.1.jar`

Installed dependencies:

- Majrusz Library: required by Majrusz's Progressive Difficulty.
- TenshiLib: required by Improved Mobs.
- CreativeCore: required by AmbientSounds 6.
- AmbientSounds `v6.1.0` is rejected with CreativeCore `2.12.38` because it caused a startup `NoSuchMethodError`; keep the `v6.3.8` pin unless retested.

Delayed:

- Better Animations Collection: delayed because it overlaps with Fresh Animations, EMF, ETF, and the current visual stack. Revisit only after Batch L passes.
- First-person Model: removed because Jayden disliked the first-person body view.
- Simple Clouds / Project Atmosphere: still delayed because Weather, Storms & Tornadoes is already the selected major weather path.

Side metadata plan:

- Both-side/server-required for local multiplayer validation: Spawn Balance Utility, Majrusz's Progressive Difficulty, Majrusz Library, Improved Mobs, and TenshiLib.
- Client-only: Not Enough Animations, AmbientSounds 6, CreativeCore, Presence Footsteps, Biome Music, Medieval Music, and Sound Physics Remastered.

Client creative/system test:

- Import the latest client ZIP.
- Launch client.
- Confirm no missing dependency screen.
- Create or load a creative test world.
- Confirm Not Enough Animations does not break Better Combat, Combat Roll, Simply Swords, shields, or Iron's Spells.
- Confirm vanilla sound, AmbientSounds, Presence Footsteps, Biome Music, Medieval Music, and Sound Physics Remastered work without zero-audio symptoms.
- If audio is silent, check the Minecraft output device and Windows/Sonar route first because the prior zero-audio report was traced to headphone/output routing.
- Confirm Weather, Storms & Tornadoes remains the only major weather system.
- Fight vanilla and modded mobs to confirm Majrusz/Improved Mobs/Scaling Health overlap does not crash.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Copy server configs if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm Spawn Balance Utility, Majrusz's Progressive Difficulty, Majrusz Library, Improved Mobs, and TenshiLib are present server-side.
- Confirm Not Enough Animations, AmbientSounds, CreativeCore, Presence Footsteps, Biome Music, and Medieval Music are not required server-side.
- Fight vanilla and modded mobs.
- Disconnect/rejoin.
- Let server run 10 minutes.

## Batch N: Cohesion And Integration Layer

Status: installed and validated.

Goal: connect the existing pack systems with scripting, global datapack loading, recipe/material cleanup, recipe conflict fallback, wood/block compatibility, food/Create integration, and stronger village/dungeon integration.

Installed core integration mods:

- KubeJS: `kubejs-forge-2001.6.5-build.26.jar`
- Rhino: `rhino-forge-2001.2.3-build.10.jar`
- Open Loader: `OpenLoader-Forge-1.20.1-19.0.5.jar`
- Almost Unified: `almostunified-forge-1.20.1-0.11.0.jar`
- Almost Unify Everything: `unifyeverything-1.20.1-1.0.2.9.jar`
- Polymorph: `polymorph-forge-0.49.10+1.20.1.jar`
- Every Compat (Wood Good): `everycomp-1.20-2.9.23-forge.jar`
- Moonlight Lib: `moonlight-1.20-2.16.33-forge.jar`
- Create Slice & Dice: `sliceanddice-forge-3.6.0.jar`
- Alex's Delight: `alexsdelight-1.5.jar`

Installed village/dungeon integration mods:

- Integrated Villages: `integrated_villages-1.3.2+1.20.1-forge.jar`
- IDAS: `idas_forge-1.13.0+1.20.1.jar`
- Integrated API: `integrated_api-1.7.2+1.20.1-forge.jar`
- Supplementaries: `supplementaries-1.20-3.1.43-forge.jar`
- Quark: `Quark-4.0-462.jar`
- Zeta: `Zeta-1.0-31.jar`

Side metadata plan:

- Both-side/server-required for local multiplayer validation: all Batch N mods and dependencies.
- Integrated Villages and Almost Unify Everything were changed from narrower Packwiz side metadata to both-side so client singleplayer tests and dedicated server tests exercise the same integration set.

KubeJS/Open Loader setup:

- `kubejs/server_scripts/` contains cautious scaffolds for recipes, tags, and loot notes. The Ascendant progression HUD bridge and Ascendant Core manifest loader are active, but no broad recipe/item rewrites are made yet.
- `openloader/data/ascendant_realms_skills/` mirrors the existing custom Ascendant Realms skill datapack as source/legacy material. The active skill-tree load path remains `config/puffish_skills/`.

Delayed:

- CraftTweaker: delayed because KubeJS is the chosen script layer.
- LootJS: delayed until a focused loot scripting pass confirms exact support and syntax.
- Paxi: delayed because Open Loader covers the current global datapack need.
- Item Obliterator: delayed until duplicate/trash items are reviewed after Batch N validation.
- Integrated Dungeons Arise: delayed until When Dungeons Arise is installed.

Client creative/system test:

- Import the latest client ZIP.
- Launch client.
- Confirm no missing dependency screen.
- Confirm JEI loads.
- Confirm KubeJS reports no script errors.
- Confirm `config/puffish_skills/` exposes the Ascendant Realms skill tree without manually copying a datapack into the world.
- Confirm Polymorph UI works on a duplicate recipe if one is available.
- Confirm Every Compat generated blocks appear without missing textures.
- Confirm Slice & Dice items appear in JEI.
- Confirm Alex's Delight items and recipes appear in JEI.
- Create a fresh creative test world and inspect villages/dungeons for placement crashes.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Copy configs, `kubejs`, and `openloader` if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm the skill tree/global datapack loads without manual world-copy steps.
- Confirm recipes and food/Create integration work.
- Confirm new villages/dungeons generate without immediate placement crashes.
- Disconnect/rejoin.
- Let server run 10 minutes.

## Batch M: Lighting, Fire, Lanterns, And Micro-Polish

Status: installed and validated.

Goal: improve held/dropped-item lighting, firelight readability, lantern decoration, medieval ambience, and small vanilla+ building polish without adding another major weather system or combat layer.

Installed mods:

- Sodium Dynamic Lights
- Sodium Options API
- Amendments
- Macaw's Lights and Lamps
- Decorative Blocks

Dependency and warning fixes:

- Sodium Options API was added by Packwiz for Sodium Dynamic Lights.
- Amendments is installed because Supplementaries 2.8.0+ moved wall lanterns, skull candles, ceiling pots, ceiling banners, and skull piles into Amendments.
- Moonlight Lib was already present from Batch N and remains the Supplementaries/Every Compat dependency.

Delayed/rejected:

- Toni's Immersive Lanterns is delayed because Packwiz resolved its Accessories dependency to `accessories-neoforge-1.0.0-beta.48+1.20.1.jar` in this Forge 1.20.1 pack.
- Accessories and TxniLib were removed with the delayed Toni's Immersive Lanterns chain.
- RyoamicLights is not installed because Sodium Dynamic Lights is the selected dynamic-light engine.
- Hardcore Torches is not installed because it was not approved.
- Lanterns Belong on Walls is delayed because the visible Minecraft 1.20.1 Modrinth file is Fabric/Quilt, not clean Forge.

Side metadata:

- Client-only: Sodium Dynamic Lights, Sodium Options API.
- Both/server-required: Amendments, Macaw's Lights and Lamps, Decorative Blocks.

Client creative/system test:

- Launch client.
- Confirm no missing dependency or Supplementaries/Amendments warning screen.
- Create or load a creative test world.
- Confirm held torches emit dynamic light.
- Confirm dropped torches emit dynamic light.
- Confirm fire, lava, glow items, or other supported light sources behave correctly.
- Confirm lanterns look good with Complementary Reimagined.
- Confirm Macaw lights place and toggle.
- Confirm Supplementaries and Amendments moved blocks still exist.
- Confirm Decorative Blocks braziers, chandeliers, and bonfires place.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Confirm Sodium Dynamic Lights and Sodium Options API do not appear in the server mods folder.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Place Amendments, Macaw's Lights and Lamps, Decorative Blocks, Supplementaries, and Quark blocks.
- Disconnect/rejoin.
- Let server run 10 minutes.

Rollback:

- Remove Batch M decorative/block mods only with care if a test world already contains their blocks.
- Dynamic-light rollback is client-only and can be done by removing Sodium Dynamic Lights and Sodium Options API.

## World Integration And Main Menu Polish Pass

Status: installed and validated.

Goal: do a broad integration audit across the current mod stack, stage generated configs into the pack source, fix the latest worldgen crash, and install the requested main-menu/UI polish without adding a new gameplay batch.

Installed client-only UI mods:

- FancyMenu
- Konkrete
- Melody
- Immersive UI

Installed/staged assets:

- `config/fancymenu/assets/ascendant_realms_title.png`

Generated integration assets:

- `docs/WORLD_INTEGRATION_AUDIT.md` inventories structures, structure sets, template pools, placed/configured features, biome modifiers, biome tags, loot tables, recipes, item tags, and entity tags from the active client instance jars.
- `config/openloader/data/ascendant_realms_world_integration/` carries global world-integration overrides for client and dedicated server testing.
- `datapacks/ascendant_realms_world_integration/` mirrors the world-integration datapack for inspection/manual fallback.

Crash fix:

- The latest crashes reproduced the same `Holder$Reference` to `PoiType` cast error through Integrated Villages structures including `airship_village`, `mossy_mounds`, and `marketstead_village`.
- The shared root path is the Integrated API `integrated_api:workstation_processor`, which can touch workstation/POI placement during world generation.
- The current fix overrides Integrated Villages processor lists through the active `config/openloader/data` path and replaces the risky processor with static `minecraft:rule` workstation placeholder replacements.
- The same datapack repairs Integrated Villages' broken `minecraft:village` structure tag by removing only nonexistent `integrated_villages:swamp_village`.
- Integrated Villages stays installed because the confirmed problem is a shared processor path, not a reason to remove each village that exposes it.

Imported config surfaces:

- Structure/worldgen: Integrated Villages, IDAS, Sparse Structures, Towns and Towers, Tectonic, Create: Structures Arise.
- Spawn/mob/boss pressure: Spawn Balance Utility, In Control, Alex's Mobs, Mowzie's Mobs, Aquamirae, Cataclysm, Soulslike Weaponry, Majrusz's Progressive Difficulty, Guard Villagers, Enhanced Boss Bars.
- Integration/blocks/loot: Loot Integrations, Bountiful, Every Compat, Supplementaries, Quark.

Side metadata:

- Client-only: FancyMenu, Konkrete, Melody, Immersive UI.
- Both-side/server-required: existing worldgen, structure, mob, loot, and integration mods stay on their documented sides.

Client creative/system test:

- Import the latest client ZIP.
- Launch client and confirm no missing dependency screen.
- Confirm FancyMenu and Immersive UI load.
- Open FancyMenu's title-screen editor and save a clean layout using `config/fancymenu/assets/ascendant_realms_title.png`.
- Confirm the title screen is readable and clickable at 1920x1080 and a smaller window size.
- Create a fresh creative test world with seed `-8696758597753506463`.
- Fly toward the latest crash areas, including seed `3740828705519225665` chunk `-33,-26` and seed `4571938849163387743` around `x=240, z=144`.
- Confirm the repaired Integrated Villages workstation processor path no longer crashes worldgen.
- Inspect several villages, dungeons, towers, and mob-heavy areas for obvious missing blocks, broken loot, or severe structure spam.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Confirm FancyMenu, Konkrete, Melody, and Immersive UI are absent from the server `mods` folder.
- Copy server configs/openloader data if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Generate or approach the former crash seed/chunk area on a fresh server world.
- Inspect villages/dungeons/structures for placement crashes.
- Disconnect/rejoin.
- Let server run 10 minutes.

Rollback:

- For menu/UI trouble, remove FancyMenu/Immersive UI first because they are client-only.
- For another Integrated Villages placement crash, inspect the failing processor/template path before removing content; disable the exact structure only as a temporary emergency bypass.
- For broad Integrated Villages/IDAS crashes, test those two mods separately before touching unrelated integration systems.

## UI Customization Tooling Pass

Status: installed through Packwiz. Packwiz refresh, check-pack, client export, and server staging export passed; in-game client/server validation is pending after client reimport.

Goal: add practical tools for a custom Ascendant Realms HUD/loading/UI direction without blindly replacing the whole interface stack.

Installed client-only UI mods:

- SpiffyHUD
- Drippy Loading Screen
- Item Borders
- Stylish Effects
- Overflowing Bars

Installed both-side UI/survival readability mod:

- AppleSkin

Dependencies:

- SpiffyHUD and Drippy Loading Screen use the existing FancyMenu, Konkrete, and Melody stack.
- Item Borders uses the existing Iceberg and Prism stack.
- Stylish Effects and Overflowing Bars use the existing Puzzles Lib stack.
- AppleSkin added no new Packwiz dependency metadata.

Side metadata:

- Client-only: SpiffyHUD, Drippy Loading Screen, Item Borders, Stylish Effects, Overflowing Bars.
- Both-side/server-required: AppleSkin.

Delayed:

- RPG-Hud remains delayed as a separate A/B test because it may conflict with SpiffyHUD, STONEBORN, Immersive UI, Xaero's Minimap, YDM's MobHealthBar, and the current skill/HUD direction.

Client creative/system test:

- Import the latest client ZIP.
- Launch client and confirm no missing dependency screen.
- Confirm SpiffyHUD and Drippy Loading Screen appear with the FancyMenu ecosystem.
- Confirm Item Borders, Stylish Effects, Overflowing Bars, and AppleSkin render clearly with STONEBORN, Immersive UI, Xaero's Minimap, YDM's MobHealthBar, Legendary Tooltips, and the current shader/resource-pack stack.
- Confirm AppleSkin reads vanilla, Farmer's Delight, and Alex's Delight food clearly.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Confirm AppleSkin is present server-side.
- Confirm SpiffyHUD, Drippy Loading Screen, Item Borders, Stylish Effects, and Overflowing Bars are not present server-side.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Disconnect/rejoin.
- Let server run 10 minutes.

Rollback:

- For startup issues, check FancyMenu/Konkrete/Melody first if the error mentions SpiffyHUD or Drippy.
- For unreadable HUD overlap, disable or retune SpiffyHUD/STONEBORN/Immersive UI layers before removing gameplay mods.
- For server mismatch, remove client-only UI jars from the server and rerun the materializer.

## Guild/Hunter RPG Spine Direction

Status: first tool pass installed and scaffolded; validation pending.

Use `docs/GUILD_HUNTER_SYSTEM_RUNDOWN.md` as the single source of truth for the next social/RPG spine: Guild ranks, Hunter Boards, rival hunters, village meaning, major Guild towns, Ascendant Codex, needed tools, needed assets, and clean next steps.

Installed tools:

- FTB Quests
- FTB Library
- FTB Teams
- FTB Ranks
- Patchouli
- Easy NPC
- Easy NPC Core
- Easy NPC Config UI
- CustomNPCs-Unofficial
- Human Companions

Already installed supporting systems:

- Bountiful
- Guard Villagers
- Villager Names
- Supplementaries
- KubeJS
- Open Loader
- In Control
- Titles
- Integrated Villages
- IDAS
- Loot Integrations
- MCA Reborn
- MCA - Default Medieval resource pack

Delayed:

- FTB quest chapters until the current editor/export format is confirmed.
- FTB Ranks config until first boot creates the expected config shape.
- Hunter Board structures and actual NPC placements until creative authoring.

Do not mark this pass validated until the tests in `docs/GUILD_HUNTER_IMPLEMENTATION_STATUS.md` pass.

## Later: Magic

Candidate mods:

- Theurgy, optional.

Recommendation:

- Iron's Spells is already installed in Batch F and passed validation. Do not expand magic until Jayden approves a later batch.
- Delay Theurgy unless the first magic pass is stable.
- Do not include additional dragons, Marium addons, RPG Series modules, Create addon flood, or additional worldgen in the same future magic batch.

Test:

- Spell casting.
- Loot readability.
- No early overpowered spellbooks.

Rollback:

- Remove magic/loot visuals before adding bosses.

## Later: Normal Mob Expansion

Candidate mods:

- Additional mob packs only after Batch F danger is tuned or Jayden approves the next danger batch.

Test:

- Village survival.
- Spawn density.
- Server tick rate.

Rollback:

- Remove mob mods and regenerate test world if needed.

## Later: Boss / Miniboss Expansion

Candidate mods:

- Additional boss packs only after Batch F danger is tuned or Jayden approves the next boss batch.

Test:

- Boss encounter balance.
- Loot balance.
- Event difficulty.

Rollback:

- Remove boss mods and test with fresh world.

## Later: Dragon And Boss Addons

Candidate mods:

- Cataclysm addons, only if the base Cataclysm pass proves stable.
- Ice and Fire addons, only if they explicitly support IceAndFire Community Edition or a later approved migration target.
- Marium addons, only if the base Marium pass proves stable.

Required before install:

- Batch G client and dedicated server validation passed.
- Dragon spawn distance rules reviewed.
- Village protection plan reviewed.
- Loot/power curve plan reviewed.
- Create Big Cannons server rules reviewed.

Test:

- New world far from spawn.
- Locate dragon areas.
- Confirm villages near spawn are not erased.

Rollback:

- Remove and regenerate world. Extra dragon/boss addon content should not be added to a committed world until proven.

## Later: Final Polish

Candidate mods:

- Pickup notifier polish only if Loot Journal is rejected during E2 validation.
- Continuity if connected textures are needed.
- Additional structure packs only if density is controlled.

Broad integration/tuning is now active after the custom skill-tree gate plus Batch K, Batch L, Batch M, and Batch N validation passed.

