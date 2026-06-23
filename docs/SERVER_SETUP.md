# Server Setup

Packwiz is initialized for Ascendant Realms. Batch A, Batch B, Batch C, Batch D, Batch E1, Batch E2, Batch F, Batch G, Batch H, Batch J, Batch K, Batch L, Batch M, and Batch N passed client/local dedicated server validation. The custom Ascendant Web skill tree, World Integration pass, and Main Menu polish pass have also passed playtest validation. Real survival tuning is now active; the pack is validated enough to tune, but not final-balanced.

Latest active CurseForge mods path:

```text
C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)\mods
```

CurseForge can create duplicate instance folders such as `Ascendant Realms (1)` or `Ascendant Realms (2)`. Always point server materialization at the active instance that contains the current batch jars. After importing the latest client ZIP, use the newest imported Ascendant Realms instance that contains Batch G jars such as `IceAndFireCE`, `L_Enders_Cataclysm`, `create-1.20.1-6.0.8`, and `createbigcannons`, Batch H jars such as `villagesandpillages`, `MoogsSoaringStructures`, `MoogsEndStructures`, `medievalend`, and `medieval_buildings_nether_edition`, Batch J jars such as `fantasy_armor` and `malfu-combat-animation`, Batch K jars such as `weather2`, `coroutil`, and `scalinghealth`, Batch L jars such as `spawnbalanceutility`, `majruszs-difficulty`, `majrusz-library`, `improvedmobs`, and `tenshilib`, Batch M jars such as `amendments`, `mcw-lights`, and `decorative_blocks`, and Batch N jars such as `kubejs`, `openloader`, `integrated_villages`, `idas`, `supplementaries`, `quark`, and `zeta`. If `ctov`, `lithostitched`, `traveloptics`, `alexscaves`, `ApothicAttributes`, or `Placebo` are present, the instance still has stale delayed jars and should be cleaned or reimported.

## Target Server Style

- Minecraft: 1.20.1
- Loader: Forge 47.4.20
- Java: 17
- Private two-player multiplayer
- 4 player cap
- 8-10 GB RAM target after worldgen and mobs are selected
- Whitelist enabled
- Online mode true

## Server-Side Mods

Server export should include only non-client metadata. For the current Batch A/B/C/D/E1/E2/F/G/H/J/K/L/M/N pack, that means:

- ModernFix
- FerriteCore
- Visual Workbench
- Puzzles Lib
- Sophisticated Backpacks
- Sophisticated Core
- Particular Reforged
- Subtle Effects
- Fzzy Config
- Kotlin for Forge
- Terralith
- Tectonic
- Serene Seasons
- GlitchCore
- Towns and Towers
- Cristel Lib
- Structory
- Sparse Structures
- YUNG's API
- YUNG's Better Mineshafts
- YUNG's Better Strongholds
- YUNG's Better Dungeons
- YUNG's Bridges
- Better Combat
- Combat Roll
- Simply Swords
- playerAnimator
- Cloth Config API
- Architectury API
- Pufferfish's Attributes
- Pufferfish's Skills
- In Control!
- Mowzie's Mobs
- GeckoLib
- Alex's Mobs
- Citadel
- Guard Villagers
- MVS - Moog's Voyager Structures
- Moog's Structure Lib
- YUNG's Extras
- Artifacts
- Curios API
- Bountiful
- Kambrik
- Villager Names
- Collective
- Loot Integrations
- Cupboard
- Fragmentum
- Iron's Spells 'n Spellbooks
- Iron's Lib
- Born in Chaos
- Aquamirae
- Obscure API
- Enhanced Celestials
- CorgiLib
- Data Anchor
- Bosses'Rise
- Immersive Armors
- Spartan Shields
- Small Ships
- Snow! Real Magic
- Kiwi
- Handcrafted
- Resourceful Lib
- Macaw's Bridges
- Macaw's Fences and Walls
- IceAndFire Community Edition
- Jupiter
- Uranus
- L_Ender's Cataclysm
- Lionfish API
- Marium's Soulslike Weaponry
- AttributeFix
- Projectile Damage Attribute
- Create
- Create Big Cannons
- Ritchie's Projectile Library
- Farmer's Delight
- Create: Structures Arise
- Villages&Pillages
- MSS - Moog's Soaring Structures
- MES - Moog's End Structures
- Medieval Buildings [End Edition]
- Medieval Buildings [Nether Edition]
- Fantasy Armor (Medieval Series)
- Malfu Combat Animation
- Titles
- Scaling Health
- Silent Lib
- Weather, Storms & Tornadoes
- CoroUtil
- Spawn Balance Utility
- Majrusz's Progressive Difficulty
- Majrusz Library
- Improved Mobs
- TenshiLib
- KubeJS
- Rhino
- Open Loader
- Almost Unified
- Almost Unify Everything
- Polymorph
- Every Compat
- Moonlight Lib
- Create Slice & Dice
- Alex's Delight
- Integrated Villages
- IDAS
- Integrated API
- Supplementaries
- Quark
- Zeta
- Amendments
- Macaw's Lights and Lamps
- Decorative Blocks

Client-only visual, shader, resource-pack, UI, and renderer mods should not be uploaded to the server.

`scripts/export-server-pack.ps1` now also removes known client-only config files from `dist\server-pack-staging` after copying shared config. If a file such as FancyMenu, Embeddium, EntityCulling, Sound Physics Remastered, Resource Pack Overrides, Sodium Dynamic Lights, Health Bar Plus, or Overflowing Bars is absent from server staging, that is intentional cleanup, not a missing gameplay system.

Enhanced Boss Bars is client-only unless a later multiplayer handshake test proves otherwise.

Loot Beams: Relooted and Loot Journal: Pickup Notifier are client-only for Batch E2 and should not be copied to the server unless multiplayer testing proves a handshake requirement.

Auroras, Beautiful Enchanted Books, Perception, and OctoLib/ShatterLib are client-only for Batch H and should not be copied to the server unless multiplayer testing proves a handshake requirement.

Wavey Capes, Xaero's Minimap, Advancement Plaques, and all Batch J resource packs are client-only and should not be copied to the server unless multiplayer testing proves a handshake requirement.

Health Bar Plus, Sound Physics Remastered, Not Enough Animations, AmbientSounds, CreativeCore, Presence Footsteps, Biome Music, Medieval Music, Sodium Dynamic Lights, Sodium Options API, FancyMenu, Konkrete, Melody, WATERMeDIA, WATERMeDIA Binaries, and Immersive UI are client-only and should not be copied to the server unless a future handshake test proves otherwise.

Subtle Effects, Fzzy Config, Kotlin for Forge, and Particular Reforged are intentionally server-side for this pack because multiplayer validation required them.

Default Skill Trees is not active anymore. The server must use the custom `config/puffish_skills/` tree plus `config/ascendant_progression/` and `kubejs/server_scripts/ascendant_progression.js` for the live Ascendant level/HUD bridge.

## Server Materialization

`dist/server-pack-staging` is a Packwiz metadata staging folder. It is useful for review, but it is not a runnable Forge server `mods` folder by itself because it contains `.pw.toml` metadata instead of downloaded `.jar` files.

Use the materializer after the client instance has downloaded the pack:

```powershell
.\scripts\materialize-server-mods-from-client.ps1 `
  -ClientModsPath "C:\Path\To\Client\mods" `
  -ServerFolder "C:\Path\To\ForgeServer" `
  -Clean
```

The script creates `ServerFolder\mods`, removes `.pw.toml` files from that folder, optionally removes old server jars with `-Clean`, copies approved server/both-side jars from the working client mods folder, prints copied jars, prints missing categories, prints the final server mods list, and fails loudly when required Batch A/B/C/D/E1/E2/F/G/H/J/K/L/M/N server jars are missing.

The materializer handles mod jars only. Skill-tree data is supplied through server config:

```text
<server folder>\config\puffish_skills\
<server folder>\config\ascendant_progression\
```

World-integration data is supplied through Open Loader and should be present in server staging:

```text
<server folder>\config\\openloader\\data\\ascendant_realms_world_integration\
```

Player identity fallback data is also supplied through Open Loader and should be present in server staging:

```text
<server folder>\config\openloader\data\ascendant_realms_identity\
```

It creates the `ar_skill_level` below-name display target and the static `[Ascendant]` prefix fallback. KubeJS mirrors real Puffish Skills Ascendant Web levels into `ar_skill_level` and drives the `Level Up! <level>` popup/HUD banner.

Batch E2 verified result: Batch E2 passed client creative/system testing and dedicated server boot/join plus 10-minute stability with Artifacts, Curios API, Bountiful, Kambrik, Villager Names, Collective, Loot Integrations, Cupboard, and Fragmentum included server-side.

Latest Batch F test result: Batch F passed client creative/system testing and dedicated server boot/join plus 10-minute stability with Iron's Spells, Iron's Lib, Born in Chaos, Aquamirae, Obscure API, Enhanced Celestials, CorgiLib, Data Anchor, Bosses'Rise, Immersive Armors, Spartan Shields, Small Ships, Snow! Real Magic, Kiwi, Handcrafted, Resourceful Lib, Macaw's Bridges, and Macaw's Fences and Walls included server-side. Variants & Ventures was later removed after the Batch J startup crash with Entity Model Features and `variantsandventures:murk_skull`.

Latest Batch G test result: Batch G passed client creative/system testing and dedicated server boot/join plus 10-minute stability with IceAndFire Community Edition, Jupiter, Uranus, L_Ender's Cataclysm, Lionfish API, Marium's Soulslike Weaponry, AttributeFix, Projectile Damage Attribute, Create, Create Big Cannons, Ritchie's Projectile Library, Farmer's Delight, and Create: Structures Arise included server-side.

Batch J server-side additions Fantasy Armor and Malfu Combat Animation passed validation. T.O Magic, Alex's Caves, Apothic Attributes, and Placebo are delayed after the Cataclysm `DungeonEyeItem` startup crash and must not be present in the active client or materialized server.

## Batch E2 Server Test Passed

Batch E2 is installed and verified.

Installed Batch E2 server/both-side mods:

- Artifacts
- Curios API
- Bountiful
- Kambrik
- Villager Names
- Collective
- Loot Integrations
- Cupboard
- Fragmentum

Client-only E2 mods:

- Loot Beams: Relooted
- Loot Journal: Pickup Notifier

Passed evidence:

- Client creative/system test passed.
- Dedicated server boot/join test passed.
- Disconnect/rejoin and 10-minute stability passed.
- Artifacts, Bountiful, Villager Names, Loot Integrations, Kambrik, Collective, and Fragmentum are stable enough for the next batch.
- No disposable survival test is required for batch validation.
- The previous loot-beam/UI concern is resolved and is not a Batch E2 blocker.

YUNG Structures Addon for Loot Integrations is delayed until a clean Forge 1.20.1 file is confirmed.

Do not add magic, Ice and Fire, Born in Chaos, Bosses'Rise, Aquamirae, Enhanced Celestials, Marium's Soulslike Weaponry, Iron's Spells, RPG Series modules, Create, or additional worldgen in E2.

## Batch F Server Test Passed

Batch F is installed and verified.

Installed Batch F server/both-side mods:

- Iron's Spells 'n Spellbooks
- Iron's Lib
- Born in Chaos
- Aquamirae
- Obscure API
- Enhanced Celestials
- CorgiLib
- Data Anchor
- Bosses'Rise
- Immersive Armors
- Spartan Shields
- Small Ships
- Snow! Real Magic
- Kiwi
- Handcrafted
- Resourceful Lib
- Macaw's Bridges
- Macaw's Fences and Walls

Client-only split:

- Existing client-only visual, shader, resource-pack, UI, and renderer mods remain client-only.

Passed Batch F server evidence:

- Server staging exported.
- Server mods materialized from the active CurseForge instance with `-Clean`.
- Server configs copied as needed.
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
- Iron's Spells, Born in Chaos, Aquamirae, Enhanced Celestials, Bosses'Rise, Immersive Armors, Spartan Shields, Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences/Walls are stable enough for the next batch.

Batch G supersedes the previous dragon-tier hold. Do not add original Ice and Fire alongside IceAndFire Community Edition, Cataclysm addons, Ice and Fire addons, Marium addons, RPG Series modules, Ars Nouveau, Theurgy, Create addon flood, additional worldgen, Sinytra Connector, or Fabric-only mods until Jayden approves a later batch.

## Batch G Server Test Passed

Batch G is installed and verified.

Installed Batch G server/both-side mods:

- IceAndFire Community Edition
- Jupiter
- Uranus
- L_Ender's Cataclysm
- Lionfish API
- Marium's Soulslike Weaponry
- AttributeFix
- Projectile Damage Attribute
- Create
- Create Big Cannons
- Ritchie's Projectile Library
- Farmer's Delight
- Create: Structures Arise

Client-only split:

- Existing client-only visual, shader, resource-pack, UI, and renderer mods remain client-only.

Passed Batch G server evidence:

- Client creative/system test passed.
- Server staging exported.
- Server mods materialized from the active CurseForge instance with `-Clean`.
- Forge 1.20.1-47.4.20 server booted.
- Client joined localhost.
- No mod mismatch blocked join.
- IceAndFire Community Edition, Cataclysm, Marium, Create, Farmer's Delight, and Create: Structures Arise content existed.
- Disconnect/rejoin passed.
- Server remained stable for 10 minutes.

Safety rule: do not spawn multiple dragons, multiple Cataclysm bosses, or multiple Marium bosses at once during validation.

Do not add original Ice and Fire alongside IceAndFire Community Edition, Cataclysm addons, Ice and Fire addons, Marium addons, Create addon flood, RPG Series modules, Ars Nouveau, Theurgy, Dynamic Trees, Biomes O' Plenty, Integrated Villages, Sinytra Connector, or Fabric-only mods until Jayden approves a later batch.

## Batch H Server Test Passed

Batch H is installed and verified.

Installed Batch H server/both-side mods:

- Villages&Pillages
- MSS - Moog's Soaring Structures
- MES - Moog's End Structures
- Medieval Buildings [End Edition]
- Medieval Buildings [Nether Edition]

Client-only H mods:

- Auroras
- Beautiful Enchanted Books [MOD EDITION]
- Perception
- OctoLib/ShatterLib

Passed Batch H server evidence:

- Server staging exported.
- Server mods materialized from the active CurseForge instance with `-Clean`.
- Forge 1.20.1-47.4.20 server booted.
- Client joined localhost.
- No mod mismatch blocked join.
- Villages&Pillages, MSS, MES, and Medieval Buildings editions were present server-side.
- Client-only H mods were not required by the dedicated server.
- Disconnect/rejoin passed.
- Server remained stable for 10 minutes.

Do not add anything beyond Batch K or any extra civilization, atmosphere, boss, dragon, Create, magic, RPG, biome, or tree systems until Jayden approves the next install.

## Custom Skill Tree And Progression HUD Server Test Pending

The custom skill tree is implemented as Puffish config, and the live progression HUD/nameplate bridge is implemented as KubeJS config/script, not a mod jar.

Source path:

```text
C:\Users\Jayden\Documents\Robbins Tech\ascendant-realms\config\puffish_skills\
C:\Users\Jayden\Documents\Robbins Tech\ascendant-realms\config\ascendant_progression\
C:\Users\Jayden\Documents\Robbins Tech\ascendant-realms\kubejs\server_scripts\ascendant_progression.js
```

Example server destination:

```text
C:\Users\Jayden\Documents\Robbins Tech\ascendant-realms-server-test\config\puffish_skills\
C:\Users\Jayden\Documents\Robbins Tech\ascendant-realms-server-test\config\ascendant_progression\
C:\Users\Jayden\Documents\Robbins Tech\ascendant-realms-server-test\kubejs\server_scripts\ascendant_progression.js
```

Required server test:

- Export server staging.
- Materialize server mods from the active CurseForge instance with `-Clean`.
- Copy server configs from `dist\server-pack-staging\config\` so `config\puffish_skills\`, `config\ascendant_progression\`, and `config\openloader\` exist on the server.
- Confirm `kubejs/server_scripts/ascendant_progression.js` exists on the server.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Open the Pufferfish's Skills UI.
- Confirm the unified Ascendant Web appears.
- Confirm generic Default Skill Trees tabs do not appear.
- Confirm the custom Ascendant XP bar appears client-side after joining.
- Confirm `ar_skill_level` appears below player names from another player's view.
- Unlock nodes and confirm attributes apply server-side.
- Kill mobs and confirm the custom bar and skill-point count update.
- Disconnect/rejoin.
- Confirm unlocks persist.
- Let server run 10 minutes.

## Post-Playtest Identity Retest Pending

The last multiplayer session showed that titles and levels did not display above player names. The server is currently shut down and the OpenLoader identity fallback is staged for the next import/server boot.

Required retest:

- Import the refreshed client pack.
- Export server staging.
- Confirm `config\openloader\data\ascendant_realms_identity\` exists in staging/server files.
- Boot Forge 1.20.1-47.4.20 server.
- Join with both players.
- Confirm `[Ascendant]` prefix appears for players without custom teams.
- Confirm `ar_skill_level` / Ascendant Web level appears below player names.
- Kill mobs and confirm the custom Ascendant XP bar updates.
- Gain an Ascendant Web level and confirm the `Level Up! <level>` popup appears.
- Disconnect/rejoin and confirm the visible identity fallback persists.

## Batch J Server Test Passed

Batch J is installed and verified.

Installed Batch J server/both-side mods:

- Fantasy Armor (Medieval Series)
- Malfu Combat Animation

Client-only Batch J mods/assets:

- Wavey Capes
- Xaero's Minimap
- Advancement Plaques
- Icon Xaero's
- Icon Xaero's X FreshAnimations
- The Rename Compat Project
- Cubic Leaves
- Simply Swords Reforged
- Cubic Sun & Moon
- Embellished Stone
- STONEBORN
- Excalibur
- Vanilla Experience+

Passed Batch J server evidence:

- Server staging exported.
- Server mods materialized from the active CurseForge instance with `-Clean`.
- Forge 1.20.1-47.4.20 server booted.
- Client joined localhost.
- No mod mismatch blocked join.
- Batch J server/both-side mods were present.
- Client-only Batch J mods/assets were not required by the dedicated server.
- Better Combat/Simply Swords with Malfu animation was checked.
- A basic Iron's Spells check passed after the Iron's Spells/Iron's Lib update.
- Disconnect/rejoin passed.
- Server remained stable for 10 minutes.

## Batch K Server Test Passed

Batch K is installed and verified.

Installed Batch K server/both-side mods:

- Titles
- Scaling Health
- Silent Lib
- Weather, Storms & Tornadoes
- CoroUtil

Client-only Batch K mods:

- Health Bar Plus
- Sound Physics Remastered

Optional/delayed:

- IntegratedPlaytime is optional only as a secondary playtime tracker.
- Simple Clouds / Project Atmosphere is delayed as the alternate weather path.

Passed Batch K server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Copy server configs if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm Titles, Scaling Health, Silent Lib, Weather, Storms & Tornadoes, and CoroUtil are server-side.
- Confirm Health Bar Plus is not required server-side unless testing proves otherwise.
- Confirm titles and scoreboard/rank data persist after reconnect.
- Fight vanilla and modded mobs.
- Watch logs/TPS during a weather pass if practical.
- Disconnect/rejoin.
- Let server run 10 minutes.

## Batch L Server Test Passed

Batch L is installed and verified.

Installed Batch L server/both-side mods:

- Spawn Balance Utility
- Majrusz's Progressive Difficulty
- Majrusz Library
- Improved Mobs
- TenshiLib

Client-only Batch L mods/assets:

- Not Enough Animations
- AmbientSounds 6
- CreativeCore
- Presence Footsteps
- Biome Music
- Medieval Music
- Sound Physics Remastered

Delayed:

- First-person Model is removed because Jayden disliked the first-person body view.
- Better Animations Collection is delayed because of overlap with Fresh Animations, EMF, ETF, and the current resource-pack animation stack.
- Simple Clouds / Project Atmosphere stays delayed because Weather, Storms & Tornadoes is already the selected major weather path.

Passed Batch L server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Copy server configs if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm Spawn Balance Utility, Majrusz's Progressive Difficulty, Majrusz Library, Improved Mobs, and TenshiLib are server-side.
- Confirm Not Enough Animations, AmbientSounds, CreativeCore, Presence Footsteps, Biome Music, Medieval Music, and Sound Physics Remastered are not required server-side unless testing proves otherwise.
- Confirm the client import uses `AmbientSounds_FORGE_v6.3.8_mc1.20.1.jar`; stale imports with `v6.1.0` can crash before server testing.
- Fight vanilla and modded mobs.
- Disconnect/rejoin.
- Let server run 10 minutes.

## Batch N Server Test Passed

Batch N is installed and verified.

Installed Batch N server/both-side mods:

- KubeJS
- Rhino
- Open Loader
- Almost Unified
- Almost Unify Everything
- Polymorph
- Every Compat
- Moonlight Lib
- Create Slice & Dice
- Alex's Delight
- Integrated Villages
- IDAS
- Integrated API
- Supplementaries
- Quark
- Zeta

Passed Batch N server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Copy server configs if needed.
- Confirm `kubejs` and `openloader` are present in the staged server pack.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm KubeJS reports no script errors.
- Confirm `config/puffish_skills/` exposes the Ascendant Realms skill tree without manually copying a datapack into the world.
- Confirm recipes and food/Create integration work.
- Confirm Integrated Villages and IDAS can generate in a fresh test world without immediate placement crashes.
- Disconnect/rejoin.
- Let server run 10 minutes.

Batch N server-risk notes:

- If startup fails on Quark, confirm `Zeta-1.0-31.jar` is present.
- If startup fails on Supplementaries or Every Compat, confirm `moonlight-1.20-2.16.33-forge.jar` is present.
- If worldgen crashes, isolate Integrated Villages and IDAS before touching KubeJS or Almost Unified.
- Do not upload client-only audio, shader, minimap, UI, or resource-pack files to the server.

## Batch M Server Test Passed

Batch M is installed and verified.

Server/both-side jars expected after materialization:

- Amendments
- Macaw's Lights and Lamps
- Decorative Blocks

Client-only jars that should not be present on the dedicated server:

- Sodium Dynamic Lights
- Sodium Options API

Required Batch M server test:

- Export server staging.
- Import the latest client pack into the active CurseForge instance.
- Materialize server mods from the active instance path with `-Clean`.
- Confirm the copied list includes Amendments, Macaw's Lights and Lamps, and Decorative Blocks.
- Confirm Sodium Dynamic Lights and Sodium Options API are not in the final server jar list.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Place Amendments, Macaw's Lights and Lamps, Decorative Blocks, Supplementaries, and Quark blocks.
- Disconnect/rejoin.
- Let server run 10 minutes.

Batch M server-risk notes:

- If the client still shows the Supplementaries warning, the active client instance is stale or missing Amendments.
- If server join fails with a missing Batch M block mod, reimport the latest client export and rerun materialization from the active instance.
- If server startup complains about Sodium Dynamic Lights or Sodium Options API, remove those client-only jars from the server mods folder and rerun the materializer.

## World Integration And Main Menu Polish Server Retest Pending

The latest client log crash is addressed by the Open Loader world-integration datapack, not by removing Integrated Villages wholesale.

Crash retest:

- Previous crash feature: `integrated_villages:airship_village`.
- Latest seed: `4571938849163387743`.
- Latest structure center chunk: `15,9`.
- Latest approximate block target: `x=240, z=144`.
- Secondary seed: `-8696758597753506463`.
- Secondary approximate block target: `x=224, z=432`.

Client-only jars that should not be present on the dedicated server:

- FancyMenu
- Konkrete
- Melody
- Immersive UI

Required server test:

- Export server staging.
- Import the latest client pack into the active CurseForge instance.
- Materialize server mods from the active instance path with `-Clean`.
- Confirm FancyMenu, Konkrete, Melody, and Immersive UI are not in the final server jar list.
- Confirm `config\openloader\data\ascendant_realms_world_integration\` is present in server staging/server files.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Create a fresh world with seed `4571938849163387743`.
- Approach approximately `x=240, z=144`.
- Confirm the prior airship-village crash does not reproduce.
- Disconnect/rejoin.
- Let server run 10 minutes.

## UI Customization Tooling Server Notes

Status: installed through Packwiz. Server staging export passed; server materialization must be retested after the client pack is reimported.

Server/both-side jar expected:

- AppleSkin

Client-only UI jars that should not be present on the dedicated server:

- SpiffyHUD
- Drippy Loading Screen
- Item Borders
- Stylish Effects
- Overflowing Bars

Required server test:

- Export server staging.
- Import the latest client pack into the active CurseForge instance.
- Materialize server mods from the active instance path with `-Clean`.
- Confirm AppleSkin appears in the copied server jar list.
- Confirm SpiffyHUD, Drippy Loading Screen, Item Borders, Stylish Effects, and Overflowing Bars are not in the final server jar list.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm AppleSkin food, hunger, and saturation information works in multiplayer.
- Disconnect/rejoin.
- Let server run 10 minutes.

## Guild/Hunter RPG Spine Server Notes

Status: installed and scaffolded. Server validation pending after client reimport.

Server/both-side jars expected after materialization:

- Patchouli
- FTB Library
- FTB Teams
- FTB Quests
- FTB Ranks
- Easy NPC Bundle
- Easy NPC Core
- Easy NPC Config UI
- CustomNPCs-Unofficial
- Human Companions

Required server test:

- Export server staging.
- Import the latest client pack into the active CurseForge instance.
- Materialize server mods from the active instance path with `-Clean`.
- Confirm all Guild/Hunter jars appear in the copied server jar list.
- Confirm client-only UI/resource/shader mods are still absent from the server mods folder.
- Boot Forge 1.20.1-47.4.20 server with Java 17.
- Join localhost.
- Confirm no mod mismatch.
- Confirm `config\openloader\data\ascendant_realms_codex\` is present in server staging/server files.
- Confirm `kubejs\startup_scripts\ascendant_guild_items.js` is present and KubeJS reports no startup errors.
- Confirm FTB Quests, FTB Ranks, Easy NPC, CustomNPCs, and Human Companions do not crash during basic creative testing.
- Disconnect/rejoin.
- Let server run 10 minutes.

Guild/Hunter server-risk notes:

- If the materializer fails after this pass, reimport the client pack first. The active CurseForge instance will not contain the new jars until reimported.
- If FTB Quests or Ranks fails, check FTB Library, FTB Teams, and Architectury API before removing the root mod.
- If an NPC tool crashes, isolate Easy NPC, CustomNPCs-Unofficial, and Human Companions separately; do not remove the whole Guild stack blindly.
- MCA Reborn is part of the server set for the next import and should be copied by the materializer as `minecraft-comes-alive-7.6.16+1.20.1-universal.jar`.
- MCA - Default Medieval is a client-only resource pack and should not be copied into the dedicated server `mods` folder.

## Manual Upload Path

1. Run validation:

```powershell
.\scripts\refresh-pack.ps1
python scripts\check-pack.py
```

2. Export server staging metadata:

```powershell
.\scripts\export-server-pack.ps1
```

3. Install the matching Forge 1.20.1 server with Java 17.
4. Accept EULA.
5. Materialize server mods from a working client mods folder.
6. Review the final server mods list.
7. Run the custom skill-tree checks and the Batch K/L/M/N checks.
8. Complete `docs/TESTING_CHECKLIST.md`.

## Future Packwiz Installer Path

After Batch E2 validation:

1. Host or serve `pack.toml`.
2. Use Packwiz installer or installer-bootstrap if the server host supports custom startup commands.
3. Use server-side filtering.
4. Do not upload shaderpacks, resource packs, or client-only visual mods to the server.

Do not fabricate host-specific steps.

## Next-Batch Rule

Do not install another new batch until Batch K, Batch L, Batch M, and Batch N validation pass and Jayden approves the next install.



## Ascendant Guild Worldgen Server Test

After syncing/exporting the latest pack, test the standalone Guild worldgen layer on a fresh server world:

1. Join the server.
2. Run `/locate structure ascendant_guild:hunter_board_village_standard`.
3. Run `/locate structure ascendant_guild:roadside_hunter_camp`.
4. Run `/locate structure ascendant_guild:frontier_guild_outpost`.
5. Teleport to each result and confirm chunks generate cleanly.
6. Run `/function ascendant_guild:npc/spawn_set/starter_guild_staff` near one structure.
7. Run `/function ascendant_guild:npc/spawn_set/roadside_rumor_camp` and `/function ascendant_guild:npc/spawn_set/frontier_guild_outpost` away from the first group.
8. Confirm generated NPCs keep their rank/level/name line, MCA-style medieval skin texture, and visible gear after disconnect/rejoin.
9. Confirm social NPCs stay near their spawn instead of all walking away together.
10. Confirm written notice boards face outward, show readable text, and Guild loot containers work on the server.
11. Confirm wall-adjacent Hunter/Frontier lanterns render as Macaw wall lanterns.
12. Spawn a vanilla zombie near a guard/rival test NPC and log combat behavior.
13. Disconnect/rejoin and let the server run 10 minutes.

## Ascendant Atlas Worldgen Server Test

After syncing/exporting the latest pack, test the broader Atlas finite-world runtime on a fresh server world:

1. Join the server.
2. Run `/function ascendant_atlas:status` at spawn and confirm region `0`, ring `0`.
3. Run `/tp @s 0 100 -1600`, then status; confirm Frostmarch / region `1`.
4. Run `/tp @s 0 100 1600`, then status; confirm Sunreach / region `2`.
5. Run `/tp @s 1600 100 0`, then status; confirm Verdant Coast / region `3`.
6. Run `/tp @s -1600 100 0`, then status; confirm Stoneback Highlands / region `4`.
7. Fly villages, roads, rivers, and cliffs for 10-15 minutes.
8. Confirm villages are not stacking into a tiny space.
9. Confirm roads do not repeatedly cross rivers/cliffs without bridges; record coordinates where they do.
10. Confirm high-tier dragon/boss/ocean mobs do not flood the Hearthlands.
11. Confirm the 3000-block worldborder warning appears near the map edge.
12. Disconnect/rejoin and let the server run 10 minutes.



## Ascendant Guild Worldgen Server Test

After syncing/exporting the latest pack, test the standalone Guild worldgen layer on a fresh server world:

1. Join the server.
2. Run `/locate structure ascendant_guild:hunter_board_village_standard`.
3. Run `/locate structure ascendant_guild:roadside_hunter_camp`.
4. Run `/locate structure ascendant_guild:frontier_guild_outpost`.
5. Teleport to each result and confirm chunks generate cleanly.
6. Run `/function ascendant_guild:npc/spawn_set/starter_guild_staff` near one structure.
7. Disconnect/rejoin and let the server run 10 minutes.

