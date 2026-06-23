# Rejected Or Delayed Mods

## Rejected For Main 1.20.1 Forge Path

- Toast Control: current visible Modrinth result is Fabric-focused and no 1.20.1 Forge signal was found.
- LambDynamicLights: main mod is Fabric; use a Forge-compatible dynamic lights/shader alternative instead.
- Faster Random: user noted archived; metadata did not show a clean 1.20.1 Forge path. Reject unless there is a specific proven need.
- OptiFine: hard banned by project rules.
- Sinytra Connector: hard banned by project rules for the main path.

## Delayed For Loader/Version Tension

These are promising but mostly point toward 1.21.1 NeoForge/Fabric or 1.20.1 Fabric, not 1.20.1 Forge:

- Spell Engine
- Skill Tree RPG Series
- Paladins & Priests RPG Series
- Arsenal RPG Series
- Wizards RPG Series
- Armory RPG Series
- Relics RPG Series
- Rogues & Warriors RPG Series
- Archers RPG Series
- Jewelry RPG Series
- Dungeon Difficulty
- Spell Power Attributes
- Ranged Weapon API
- Runes
- Critical Strike
- Village Taverns RPG Series

## Delayed For Balance Or Cohesion

- Biomes O' Plenty: delay until Terralith/Tectonic direction is tested.
- Dynamic Trees: high compatibility cost.
- Original Ice and Fire: delayed because IceAndFire Community Edition was selected as the single active Batch G dragon variant.
- Ice and Fire addons: delayed until the selected IceAndFire Community Edition path passes validation and addon compatibility is explicit.
- Marium addons: delayed until base Marium's Soulslike Weaponry passes validation.
- Theurgy: deep system that may compete with Iron's Spells.
- Ars Nouveau: not part of the approved Forge proof path while Iron's Spells is being validated.
- Cataclysm addons: delayed until base L_Ender's Cataclysm passes validation.
- Create addon flood: delayed; Batch G installs only Create Big Cannons and one Create structure addon.
- Multiple village overhauls: choose one primary village stack first.

## Batch F Candidate Result

- No approved Batch F candidate was rejected or delayed.
- Bosses'Rise had a clean Minecraft 1.20.1 Forge file and was installed.
- Born in Chaos, Aquamirae, Enhanced Celestials, Iron's Spells, Immersive Armors, Spartan Shields, Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences and Walls were installed through Packwiz.
- Variants & Ventures was originally installed in Batch F, then delayed/removed after the Batch J client startup crash. Its 1.20.1 Forge file crashes with Entity Model Features during `variantsandventures:murk_skull` model registration; a 1.20.2 changelog notes skull model crash fixes, but that file is not safe for the current 1.20.1 Forge target.

## Batch G Candidate Result

- IceAndFire Community Edition was selected over original Ice and Fire because it has a current clean Minecraft 1.20.1 Forge/NeoForge target. It is a community fork and not a direct replacement path for existing original Ice and Fire saves.
- Original Ice and Fire was delayed because exactly one Ice and Fire variant may be active.
- L_Ender's Cataclysm, Marium's Soulslike Weaponry, Create, Create Big Cannons, Farmer's Delight, and Create: Structures Arise were installed through Packwiz.
- Create: Structures was not installed because Batch G allows at most one Create structure addon and Create: Structures Arise was selected.
- Cataclysm addons, Ice and Fire addons, Marium addons, extra Create addons, Ars Nouveau, Theurgy, RPG Series modules, Dynamic Trees, Biomes O' Plenty, extra village overhauls beyond Batch H, Sinytra Connector, and Fabric-only mods remain delayed or rejected by standing rules.

## Batch H Candidate Result

- Villages&Pillages, MSS - Moog's Soaring Structures, MES - Moog's End Structures, Auroras, Beautiful Enchanted Books, Perception, Medieval Buildings [End Edition], and Medieval Buildings [Nether Edition] were installed through Packwiz.
- ChoiceTheorem's Overhauled Village is delayed after an in-world crash during `ctov:medium/village_swamp` feature placement.
- Lithostitched was removed because it was only required by CTOV.
- OctoLib/ShatterLib was added by Packwiz for Perception.
- Biome Music was delayed from Batch H, then installed in Batch L after clean Packwiz resolution.
- Medieval Music was delayed from Batch H, then installed in Batch L after clean Packwiz resolution.
- Neko's Enchanted Books was delayed because Beautiful Enchanted Books had the cleaner exact Forge 1.20.1 file and only one enchanted-book visual mod should be active.
- Biome Edition Visual Traveler's Titles was delayed because its verified Modrinth and CurseForge files target Minecraft 1.21.1, not the current Minecraft 1.20.1 Forge proof pack. The pack now uses Visual Traveler's Title Biomes Addon plus a local Ascendant Realms fallback for current modded biome/dimension gaps.
- Biomes O' Plenty, Dynamic Trees, extra Cataclysm addons, Ice and Fire addons, extra Create addons, RPG Series modules, Ars Nouveau, Theurgy, Sinytra Connector, Fabric-only mods, and village/structure packs beyond the Batch N Integrated Villages/IDAS install remain delayed or rejected by standing rules.

## Batch J Candidate Result

- Fantasy Armor, Wavey Capes, Xaero's Minimap, Icon Xaero's, The Rename Compat Project, Icon Xaero's X FreshAnimations, Cubic Leaves, Simply Swords Reforged, Cubic Sun & Moon, Embellished Stone, STONEBORN, Malfu Combat Animation, Excalibur, and Vanilla Experience+ were installed through Packwiz.
- Advancement Plaques was installed because Embellished Stone is an Advancement Plaques resource-pack layer.
- T.O Magic 'n Extras is delayed because `traveloptics-6.3.0-1.20.1.jar` crashed against Cataclysm `3.30` with missing `com/github/L_Ender/Cataclysm/items/Dungeon_Eye/DungeonEyeItem`.
- Alex's Caves, Apothic Attributes, and Placebo are delayed with T.O Magic because they were only added by that dependency chain.
- The attempted T.O Magic install updated Iron's Spells/Iron's Lib metadata; those versions were carried through the Batch J validation pass.
- TravelersCrossroads is delayed because Packwiz rejected it for the configured Minecraft 1.20.1 Forge target. The visible current CurseForge project files target 1.21.x NeoForge rather than the current 1.20.1 Forge proof pack.

## Batch K Candidate Result

Installed and validated.

Installed through Packwiz:

- Titles
- YDM's MobHealthBar
- Scaling Health
- Silent Lib
- Sound Physics Remastered
- Weather, Storms & Tornadoes
- CoroUtil

Delayed or rejected:

- IntegratedPlaytime: optional only as a secondary playtime tracker. Do not use playtime as the main Ascendant rank.
- Simple Clouds: delayed because it is open beta and explicitly warns about bugs, crashes, and instability.
- Project Atmosphere: delayed because the current 1.20.1 Forge path depends on Simple Clouds and Gabou's Libs, and a recent public crash report shows Simple Clouds plus Project Atmosphere crashing together.
- CustomNameTags: rejected/delayed because the visible project is Fabric/server-side, not a clean Forge 1.20.1 target.
- Champions: rejected/delayed because the current visible project is Fabric-oriented and the pack already has several threat escalation systems.
- Health Indicators: rejected/delayed because the visible 1.20.1 project lists Fabric/NeoForge/Quilt, not Forge.
- Immersive Storms: rejected/delayed because the current visible project is Fabric/Quilt and newer-version focused.
- Better Clouds: rejected because the current 1.20.1 file is Fabric and requires Fabric API.

## Batch L Candidate Result

Installed and validated.

Installed through Packwiz:

- Spawn Balance Utility
- Majrusz's Progressive Difficulty
- Improved Mobs
- Not Enough Animations
- AmbientSounds 6
- Presence Footsteps
- Biome Music
- Medieval Music

Removed or delayed after initial install:

- First-person Model: removed because Jayden disliked the first-person body view.

Installed dependencies:

- Majrusz Library
- TenshiLib
- CreativeCore

Delayed or rejected:

- Better Animations Collection: delayed because it overlaps with Fresh Animations, Entity Model Features, Entity Texture Features, and the existing resource-pack animation stack. Revisit only after Batch L passes.
- Simple Clouds / Project Atmosphere: remains delayed because Weather, Storms & Tornadoes is already the selected major weather path and should not be stacked with another major weather/cloud system.
- Extra dragons, Cataclysm addons, Ice and Fire addons, RPG Series modules, Lycanites, Schism beta, horror meme mobs, Biomes O' Plenty, Dynamic Trees, Sinytra Connector, and Fabric-only mods remain rejected or delayed by standing Batch L rules.

## Batch N Candidate Result

Installed and validated.

Installed through Packwiz:

- KubeJS
- Open Loader
- Almost Unified
- Almost Unify Everything
- Polymorph
- Every Compat / Wood Good
- Create Slice & Dice
- Alex's Delight
- Integrated Villages
- Integrated Dungeons and Structures

Installed dependencies:

- Rhino
- Moonlight Lib
- Integrated API
- Supplementaries
- Quark
- Zeta

Delayed or rejected:

- CraftTweaker: delayed because KubeJS is the chosen script layer.
- LootJS: delayed until a focused loot scripting pass verifies exact Forge 1.20.1 support and syntax.
- Paxi: delayed because Open Loader covers the current global datapack need.
- Item Obliterator: delayed until duplicate/trash items are reviewed after Batch N validation.
- Integrated Dungeons Arise: delayed until When Dungeons Arise is installed.

## Batch M Candidate Result

Installed and validated:

- Sodium Dynamic Lights
- Sodium Options API
- Amendments
- Macaw's Lights and Lamps
- Decorative Blocks

Delayed or rejected:

- Toni's Immersive Lanterns: delayed. The selected root mod was Forge, but Packwiz resolved Accessories to `accessories-neoforge-1.0.0-beta.48+1.20.1.jar`, so the full dependency chain is not clean for the current Forge target.
- Accessories: delayed with Toni's Immersive Lanterns because the selected file was NeoForge-named.
- TxniLib: removed with the delayed Toni's Immersive Lanterns chain; no active Batch M root needs it.
- RyoamicLights: rejected/delayed while Sodium Dynamic Lights is active. Do not stack dynamic-light engines.
- Hardcore Torches: delayed because it changes survival friction and was not explicitly approved.
- Lanterns Belong on Walls: delayed/rejected for now because the visible Minecraft 1.20.1 file is Fabric/Quilt, not clean Forge. Amendments covers the wall-lantern need.

## Needs Exact Project Verification

- Enchantment Descriptions Compat
- Enchant Icons
- Cubic Sun & Moon
- Extra Gore
- YDM's Weapon Master
- Villagers replant correct modded seeds
- Medieval Buildings - New Structures
- YUNG Structures Addon for Loot Integrations
- Dungeon Heroes RPG Series
- Attribute Icons RPG Series
- ANARCHY Minibosses RPG Series Plus

## Guild/Hunter Candidate Result

Installed and awaiting validation:

- Patchouli
- FTB Quests
- FTB Ranks
- Easy NPC
- CustomNPCs-Unofficial
- Human Companions

Installed dependencies:

- FTB Library
- FTB Teams
- Easy NPC Core
- Easy NPC Config UI

Delayed:

- MCA Reborn: previously delayed, now active with MCA - Default Medieval. It remains unverified and should return here if medieval/fantasy skin control or dedicated server behavior fails.
- FTB quest chapter data: delayed until the in-game FTB Quests editor/export format is confirmed.
- FTB Ranks config: delayed until the first boot generates the expected config shape.
- Hunter Board structures and placed NPCs: delayed because these need in-game creative authoring, not blind file generation.
