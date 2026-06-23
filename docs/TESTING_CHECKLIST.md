# Testing Checklist

Use `docs/CURRENT_STATUS.md` for the newest live blocker list before running this broad checklist. Older batch sections below are historical validation evidence unless the current status or docs index points at them for a fresh retest.

## Phase 1.5 Packwiz State

- Compatibility matrix updated.
- Version/loader decision approved: Minecraft 1.20.1 Forge 47.4.20.
- Batch A installed and validated.
- Batch B installed and validated.
- Batch C installed and validated.
- Batch D installed and validated in solo and dedicated server tests.
- Batch E1 world pressure and density installed and validated.
- Batch E2 loot, rewards, and contracts installed and validated.
- Batch F Arcane Nightfall Expansion installed and validated.
- Batch G Dragonforge Cataclysm installed and validated.
- Batch H Civilization and Atmosphere installed and validated.
- Custom Ascendant Realms skill tree implemented in `config/puffish_skills/`; playtest passed and long-form tuning is active.
- Batch J visual/add-on candidate pass installed and validated.
- Batch K Identity, Threat UI, and Atmosphere installed and validated.
- Batch L Living World, Body Presence, Music, and Atmosphere installed and validated.
- Batch M Lighting, Fire, Lanterns, and Micro-Polish installed and validated.
- Batch N Cohesion Layer installed and validated.
- World Integration and Main Menu polish pass installed and validated.
- Latest Integrated Villages fix staged: the shared `integrated_api:workstation_processor` POI-cast crash path is bypassed through OpenLoader static `minecraft:rule` workstation replacements. `airship_village`, `mossy_mounds`, and `marketstead_village` are restored for retest; only nonexistent `integrated_villages:swamp_village` remains removed from the repaired vanilla village tag.
- Latest multiplayer playtest finished and the server was shut down afterward.
- Post-playtest issue found: player titles/levels did not show above names and enemy numeric levels did not show above mobs.
- Player identity fallback is staged through `config/openloader/data/ascendant_realms_identity/`; retest on the next server boot.
- Root-cause compatibility policy is active; validate fixes before removing content.
- Latest compatibility-shim pass staged: Human Companions biome typo tags, IceAndFire CE `c:bosses`, IDAS optional Ars/BOP/BYG hooks, Iron's Spells loot-table fallback, and optional compat recipe/advancement placeholders.
- Universal mod/rarity index generated for the active Packwiz list.
- First unification implementation pass staged: expanded live Bountiful contract pools and cap-only In Control settlement-safety rules.
- Gear rarity indexes generated for weapons, armor, shields, magic/spells, and accessories/relics.
- FancyMenu, Konkrete, Melody, and Immersive UI are installed as client-only UI mods.
- No `.jar` files in repo.
- `pack.toml` and `index.toml` exist.
- Kotlin for Forge 4.12.0 is installed for Fzzy Config and stays within the required >=4.11.0 and <=4.99.0 range.
- Subtle Effects is paired with Forge 47.4.20 because it requires Forge 47.4.14 or newer.
- `python scripts\check-pack.py` passes.
- `packwiz refresh` passes.

## Gear Rarity And Item Borders Test

Status: generated; needs in-game client retest after reimport.

- Confirm `docs/WEAPON_INDEX.md`, `docs/ARMOR_INDEX.md`, `docs/SHIELD_INDEX.md`, `docs/MAGIC_INDEX.md`, and `docs/ACCESSORY_RELIC_INDEX.md` exist.
- Confirm `config/ascendant_index/gear_registry.json` includes weapons, armor, shields, magic items, spells, and accessories/relics.
- Confirm `config/itemborders-common.toml` has `auto_borders = false` and populated `manual_borders`.
- Confirm the client no longer crashes on an Item Borders `ï»¿#` TOML parse error.
- Confirm resource reload no longer reports the Amendments/Cataclysm `music_disc_maledictus` animated disc mask error.
- Confirm weapons from Simply Swords, Marium's Soulslike Weaponry, Cataclysm, IceAndFire CE, Born in Chaos, Bosses'Rise, Aquamirae, and vanilla have rarity frames.
- Confirm frame colors match the rarity color in the relevant index, not the item display-name color.
- Confirm Farmer's Delight/Alex's Delight/Slice & Dice cooking knives are excluded from combat weapon rarity expectations.
- Confirm no KubeJS startup errors from `ascendant_gear_rarity.js`.
- Confirm `ascendant_gear_rarity.js` remains a no-op metadata file and does not call `ItemEvents.modification` or assign `item.rarity`.
- Confirm hover tooltips show only the generated rarity tier label from `kubejs/client_scripts/ascendant_rarity_tooltips.js`.
- Confirm weapon tooltip order is native damage/speed/stat lines first, then the generated rarity label, then green attack range/combat behavior/chance lines.
- Confirm the tooltip no longer shows a `Rarity:` prefix.
- Confirm item rarity tooltips do not show generated `Effect:`, `Index:`, or `Why:` backend lines.
- Confirm only Legendary, Mythic, and Ascendant rarity labels are bold.
- Confirm Mythic and Ascendant items show clean `MYTHIC` and `ASCENDANT` labels without `Flame`, `Pulse`, side symbols, or obfuscated side characters.
- Confirm tooltip text remains readable inside Legendary Tooltips/STONEBORN frames and does not duplicate lines.
- Confirm Loot Beams/Legendary Tooltips still read cleanly while Item Borders manual colors provide the rarity frame.
- Confirm searching JEI for `Runic Grimoire` shows the NBT-backed Patchouli guide book registered by `kubejs/client_scripts/ascendant_jei_aliases.js`.
- Confirm the Runic Grimoire tooltip shows clean `ASCENDANT CODEX` / `Runic Grimoire` identity text without generated backend lines.

## Custom NPC Test

Status: automated audit/repair tooling added; active save currently requires offline repair while Minecraft is closed if the audit reports stale NPC entity data.

- Run `powershell -ExecutionPolicy Bypass -File scripts\check-custom-hero-system.ps1 -SyncClient` and confirm the CustomNPCs identity script unit tests pass.
- Confirm the saved-world audit reports no stale embedded scripts or broken visible name data.
- If the audit reports issues, close Minecraft and run `powershell -ExecutionPolicy Bypass -File scripts\check-custom-hero-system.ps1 -SyncClient -Apply`, then reopen the world.
- Run `powershell -ExecutionPolicy Bypass -File scripts\check-custom-hero-system.ps1` for the combined automated check after the world is repaired.

- Run `/reload`, then run `/function ascendant_identity:npc_test/kit`.
- Confirm the function gives the CustomNPCs NPC Wand, Mob Cloner, Mounter, Moving Path, Teleporter, Scripter, NBT Book, and Soulstone.
- Confirm the kit command appears and does not return `Unknown function`.
- With the NPC Wand selected, right-click a block to create the first NPC.
- If right-clicking air opens a blank remote editor list, that is expected before NPCs exist; close it and use the Wand on a block.
- Create Guild Clerk, Rank Examiner, Guard Captain, and Mira Ash prototypes using the supplied `ar:*` profile-key name tags.
- Paste the contents of `customnpcs/scripts/ecmascript/ascendant_npc_identity.js` into the NPC Scripter black code box.
- Confirm the script converts profile keys into one styled always-visible rank/name/level/role line.
- Confirm Rank Examiner renders as `[B-Rank] Rank Examiner | Lv.52 Examiner`, not `[Guild] Rank Examiner`.
- If an old prototype still shows `[Guild]` or `[Unranked]` Rank Examiner after script updates, the placed NPC has stale embedded entity data. Close Minecraft and run `powershell -ExecutionPolicy Bypass -File scripts\check-custom-hero-system.ps1 -SyncClient -Apply`.
- The in-game `/function ascendant_identity:npc_test/fix_rank_examiner` is only a quick profile-key reset; it cannot replace the embedded script copy stored inside the NPC entity.
- Confirm no new `EntityCustomNpc ... script errored` line appears after interacting with the test NPC.
- Confirm the visible level comes from the script profile baseline rather than manually typed final name text.
- Equip the command-safe placeholder gear supplied by the test kit first.
- Equip richer modded showcase gear manually from JEI after confirming exact live item ids in the NPC editor.
- Confirm friendly NPCs do not attack players.
- Confirm a combat NPC can fight a vanilla zombie in a controlled creative test.
- Save a finished prototype with the Mob Cloner.
- Save/reload and disconnect/rejoin without losing the test NPCs.

## Root-Cause Compatibility Retest

Status: staged; needs fresh client/server retest after import.

- Confirm startup no longer reports `Unknown display slot 'below_name'` and player levels display below names.
- Confirm startup no longer reports missing `c:bosses` for `iceandfire:immune_to_gorgon_stone`.
- Confirm startup no longer reports Human Companions `windswept_gravelley_hills` biome tag errors.
- Confirm startup no longer reports IDAS missing optional BOP/BYG biome references.
- Confirm IDAS Archmage Tower spawner parsing no longer references `ars_nouveau:wilden_hunter`.
- Confirm IDAS Ars-themed Archmage/Enchanting Tower loot tables load with Iron's Spells replacements.
- Confirm Iron's Spells `crypt_loot` and `citadel_tomes` no longer throw loot-table parse errors.
- Confirm Every Compat / Alex's Delight / Spartan Shields optional compat warnings are reduced without losing their installed core content.
- Confirm KubeJS Guild Mark, Hunter Seal, and Ascendant Sigil items have icons.
- Confirm fallback armor texture warnings are gone when the compatibility resource pack is enabled, especially `wizard_layer_1`, `wizard_layer_1_overlay`, `cultist_layer_1`, `wandering_magician_layer_2`, `netherite_layer_1_overlay`, `netherite_layer_2_overlay`, `geomancer_armor_layer_1`, and `plagued_layer_1`.

## MCA Reborn Medieval Import Test

Status: installed; needs fresh client/server validation.

- Confirm MCA Reborn and MCA - Default Medieval are present after client import.
- Confirm the MCA - Default Medieval resource pack is enabled above vanilla/UI packs as needed.
- Create/load a fresh creative test world and inspect naturally spawned MCA villagers.
- Confirm MCA villagers use medieval/fantasy-safe clothing across normal, burnt, and zombie variants.
- Confirm no common modern hoodie/shirt/off-tone skins appear in normal village testing.
- Confirm MCA interaction screens open without crash.
- Confirm JEI/search remains responsive after MCA is installed.
- Dedicated server: materialize with `-Clean`, boot Forge 1.20.1-47.4.20, join localhost, visit a village, interact with MCA villagers, disconnect/rejoin, and run a 10-minute stability check near villagers.

## Batch Validation Policy

- Client boot test.
- Creative/system functionality test.
- Dedicated server boot/join test.
- 10-minute stability check.
- Disposable survival throwaway tests are no longer required after every batch.
- Full survival tuning happens later after the main feature stack is installed.

## Ascendant Unification Pass Test

Status: staged; needs next client/server retest after import or sync.

- Confirm startup has no In Control rule parse errors.
- Confirm startup has no Bountiful pool/decree parse errors.
- Confirm Open Loader injects `ascendant_realms_guild`, `ascendant_realms_core`, `ascendant_realms_identity`, `ascendant_realms_world_integration`, and `ascendant_realms_codex`.
- Open a Village Hunter Board and confirm it has a wider mix of modded mob contracts.
- Open or locate a Town Guild/Major Guild board and confirm higher-tier targets appear.
- Confirm no Bountiful board asks for CustomNPCs, MCA, Easy NPC, Human Companions, or GeckoLib helper entities.
- Load or visit a village at night and watch whether guards/MCA villagers survive longer than the last log where Born in Chaos-style pressure wiped several villagers quickly.
- Fight several contract mobs and confirm Ascendant Core still awards reputation/proof counters through `/function ascendant_core:status`.
- Dedicated server: export staging, materialize with `-Clean`, join, open a Bountiful board, visit a village, disconnect/rejoin, and run a 10-minute stability check.

## Batch A Validation Passed

- Client boot passed on Minecraft 1.20.1 Forge 47.4.20.
- Complementary Reimagined shader worked.
- Fresh Animations/resource visuals worked.
- Local dedicated Forge server booted.
- Client joined localhost.
- Visual Workbench placed and worked.
- Sophisticated Backpack item worked and opened.
- Disconnect/rejoin worked.
- World remained stable for 10 minutes.
- Shaders stayed enabled during the successful multiplayer test.

## Client Boot

- Launcher profile uses chosen Minecraft version.
- Loader version matches `pack.toml` once initialized.
- Java version matches Minecraft target.
- Client boots to menu.
- No Fzzy Config / Kotlin for Forge missing dependency screen.
- No Subtle Effects Forge-version dependency screen.
- Resource packs load in intended order.
- Shaderpack loads.
- Complementary Reimagined appears in shader menu.
- Fresh Animations appears in resource pack list.
- Visual Traveler's Titles, Visual Traveler's Title Biomes Addon, and Ascendant Realms Traveler's Titles fallback appear in the resource pack list.
- Batch J resource packs appear in the resource pack list: Icon Xaero's, Icon Xaero's X FreshAnimations, The Rename Compat Project, Cubic Leaves, Simply Swords Reforged, Cubic Sun & Moon, Embellished Stone, STONEBORN, Excalibur, and Vanilla Experience+.
- FancyMenu and Immersive UI load without a missing dependency screen.
- The supplied title asset exists at `config/fancymenu/assets/ascendant_realms_title.png`.
- Main menu layout is readable and clickable after saving a FancyMenu title-screen layout.
- Resource-pack order keeps Vanilla Experience+ below Cubic Sun & Moon so the dedicated 3D sun/moon textures render.
- Confirm the active resourcepacks folder uses `Vanilla Experience Plus.zip`, not the old section-sign color-code filename.
- Close and reopen the client once; confirm Resource Pack Overrides keeps the visual/music packs enabled without manually toggling them back on.
- After the restart, check `logs/latest.log` and confirm there is no `Failed to load options` / `OptionsKeyLwjgl3Fix` error and no `key.keyboard.left.alt` parse error.
- Confirm the active instance `mods` folder contains `ResourcePackOverrides-v8.0.3-1.20.1-Forge.jar`.
- Confirm the active instance `resourcepacks` folder does not contain copied Packwiz `.pw.toml` metadata files.
- If packs still disable after restart, confirm the imported client has `ResourcePackOverrides-v8.0.3-1.20.1-Forge.jar`; the config/order files alone cannot enforce the selected stack without that client-only jar.
- Traveler's Titles resource packs are enabled in this top-to-bottom order: Ascendant Realms fallback, Visual Traveler's Title Biomes Addon, Visual Traveler's Titles, Fresh Animations.
- If commands are available, preview `/dimensiontitle minecraft:the_nether`, `/dimensiontitle iceandfire:dread_land`, and `/dimensiontitle irons_spellbooks:pocket_dimension`.
- If commands are available, preview `/biometitle minecraft:plains`, `/biometitle terralith:red_oasis`, and `/biometitle iceandfire:dread_forest`.
- JEI opens in inventory/recipe view.
- Sophisticated Backpacks items appear in JEI.
- No missing dependency screen.
- No AmbientSounds startup crash with CreativeCore; active client import should use `AmbientSounds_FORGE_v6.3.8_mc1.20.1.jar`, not `AmbientSounds_FORGE_v6.1.0_mc1.20.1.jar`.
- No major visual corruption.

## Local Server Boot

- Server uses chosen Minecraft version and loader.
- Server boots with approved server/both-side mods.
- Server includes Subtle Effects, Fzzy Config, Kotlin for Forge, and Particular Reforged while the current Batch A visual stack remains active.
- Server staging excludes client-only visual/render/UI mods.
- Player joins.
- New world generates.
- No immediate crash.
- No severe log spam.
- Client-only visual mods are not required on the server.

## New Worldgen Test

- Batch B validation passed.
- Ascendant Guild custom structures are active through Open Loader.
- Ascendant Atlas finite-world coordinate runtime is active through KubeJS, In Control areas, and `/function ascendant_atlas:status`.
- Ascendant Atlas full worldgen v1 is active through the local `ascendant_atlas_regions` helper and the OpenLoader Overworld dimension override.
- Ascendant Atlas waymark structures are debug-only assets and should not generate naturally.
- Batch B single-player appeared to work in the updated client instance.
- Updated client export included Sparse Structures, YUNG's Better Mineshafts, YUNG's Better Strongholds, YUNG's Better Dungeons, and YUNG's Bridges.
- Materializer copied the full Batch A/B server jar set from the active CurseForge instance path using `-Clean`.
- Batch B dedicated server join worked on a fresh world.
- Current active CurseForge mods path for the latest sync/export pass: `C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)\mods`.
- Client joined localhost.
- Terrain generated.
- Structures generated.
- Disconnect/rejoin worked.
- Server remained stable for 10 minutes.
- Real survival tuning is active; the pack is not final-balanced yet.

Atlas runtime checks:

- `/function ascendant_atlas:status` at spawn should report region `0`, ring `0`.
- `/tp @s 0 100 -1600`, then status should report Frostmarch / region `1`.
- `/tp @s 0 100 1600`, then status should report Sunreach / region `2`.
- `/tp @s 1600 100 0`, then status should report Verdant Coast / region `3`.
- `/tp @s -1600 100 0`, then status should report Stoneback Highlands / region `4`.
- `/tp @s 2600 100 0`, then status should show outer-ring distance and worldborder warning should appear as the player approaches 3000 blocks.

Atlas validation:

- Confirm scoreboards `ar_atlas_region`, `ar_atlas_ring`, `ar_atlas_sector`, `ar_atlas_distance`, `ar_atlas_x`, and `ar_atlas_z` update.
- Confirm actual generated biome identity follows Atlas regions in a fresh world: mild Hearthlands near spawn, snowy/cold Frostmarch north, arid Sunreach south, wet/jungle/ocean Verdant Coast east, and mountain/cliff Stoneback Highlands west.
- Confirm diagonal regions blend neighboring biome tables instead of snapping to unrelated vanilla/Terralith climates.
- Confirm Tectonic-style terrain still appears; the helper should change biome source only, not flatten or replace terrain settings.
- Confirm high-tier boss/dragon/ocean mobs do not flood the Hearthlands near spawn.
- Fly villages and roads for 10-15 minutes.
- Record overlapping villages, structures inside structures, road cliffs, floating roads, and river crossings with no bridge.
- Confirm YUNG's Bridges still generates bridge landmarks and Macaw wall lantern blocks still appear in custom Guild structures.
- Save/reload, then repeat on a dedicated server.

## Batch C Combat Foundation Test

Status: validation passed.

Passed evidence:

- Batch C client test passed.
- Batch C dedicated server test passed.
- Better Combat, Combat Roll, Simply Swords, playerAnimator, Cloth Config API, and Architectury API are stable enough for the next batch.

Client test:

- Client launched.
- Fresh creative test world loaded.
- Better Combat attack animations worked.
- Combat Roll keybind existed and roll worked.
- Simply Swords weapons appeared in JEI.
- Vanilla zombies/skeletons were used for melee combat testing.
- Shield behavior was checked where relevant.
- Shader-on test passed.
- Save/reload passed.

Dedicated server test:

- Server staging exported.
- Server mods materialized from the active CurseForge instance using `-Clean`.
- Forge 1.20.1-47.4.20 server booted.
- Client joined localhost.
- No mod mismatch blocked join.
- Better Combat attack animations worked.
- Combat Roll worked.
- Simply Swords weapons worked.
- Vanilla mob fight test passed.
- Disconnect/rejoin worked.
- Server remained stable for 10 minutes.

## Batch D Skills/Classes Test Plan

Status: validation passed in solo and dedicated server tests.

Installed:

- Pufferfish's Attributes
- Pufferfish's Skills

Default Skill Trees was used for earlier framework validation, then removed from active Packwiz metadata after the custom Ascendant Realms skill tree was approved.

Client test:

- Launch client.
- Confirm main menu loads.
- Create or load a creative test world.
- Check keybinds for skills/skill tree UI.
- Confirm skills UI opens.
- Confirm skill tree loads without missing textures or broken screens.
- Confirm attributes appear where visible.
- Fight vanilla mobs with Better Combat and Simply Swords.
- Confirm no crash when gaining XP, levels, or skill points.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize server mods from the active CurseForge instance using `-Clean`.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Open skill UI if available.
- Fight vanilla mobs.
- Confirm progression/attributes do not crash.
- Disconnect/rejoin.
- Let server run 10 minutes.

Do not invent commands for giving skill points unless the mod documentation/config clearly exposes them. If commands exist, document them after verification. If not, test through normal XP/combat progression.

Do not add magic, mobs, bosses, loot systems, Ice and Fire, RPG Series modules, Alex's Mobs, Mowzie's Mobs, Guard Villagers, Create, ParCool, Bountiful, Artifacts, or additional worldgen in Batch D.

## Batch E1 World Pressure And Density Test

Status: validation passed.

Installed:

- In Control!
- Mowzie's Mobs
- Alex's Mobs
- Guard Villagers
- MVS - Moog's Voyager Structures
- YUNG's Extras
- Enhanced Boss Bars

Dependencies:

- GeckoLib
- Citadel
- Moog's Structure Lib

Client creative/system test:

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
- Use fresh world name.
- Join localhost.
- Confirm no mod mismatch.
- Fly 3000-5000 blocks.
- Check server TPS.
- Check villages have guards.
- Fight Mowzie/Alex mobs.
- Disconnect/rejoin.
- Let server run 10 minutes.

Blocked during E1:

- Magic
- Loot systems
- Ice and Fire
- Born in Chaos
- Bosses'Rise
- Aquamirae
- Enhanced Celestials
- Marium's Soulslike Weaponry
- Iron's Spells
- RPG Series modules

## Batch E2 Loot, Rewards, And Contracts Test

Status: validation passed.

Installed:

- Artifacts
- Bountiful
- Loot Beams: Relooted
- Villager Names
- Loot Journal: Pickup Notifier
- Loot Integrations

Dependencies:

- Kambrik
- Collective
- Fragmentum
- Curios API
- Cupboard

Startup dependency fix:

- The first E2 client load failed because Loot Integrations required Cupboard `1.20.1-1.5.7` or above and Artifacts required Curios `5.8.1+1.20.1` or above.
- Cupboard `1.20.1-3.7` and Curios API `5.14.1+1.20.1` are now installed and must be present in the next client import/server materialization.

Passed evidence:

- Batch E2 client creative/system test passed.
- Batch E2 dedicated server boot/join test passed.
- 10-minute stability check passed.
- Artifacts, Bountiful, Villager Names, Loot Integrations, Kambrik, Collective, and Fragmentum are stable enough for the next batch.
- Loot Beams: Relooted and Loot Journal: Pickup Notifier remained client-only.
- No disposable survival test is required for batch validation.
- The previous loot-beam/UI concern is resolved and is not a Batch E2 blocker.
- Full balance/UI tuning happens later after the major stack is installed.

Client creative/system test:

- Client launched.
- Creative/system test world loaded.
- Artifacts items appeared in JEI.
- Bountiful bounty board/items appeared in JEI.
- Villager Names worked where visible.
- Loot Beams worked on dropped rare items.
- Dropped rare items showed one combined Loot Beams tooltip when looked at, not separate name and rarity boxes.
- Loot Beams tooltip position was acceptable.
- Epic items used rarity-colored purple beams instead of display-name-colored beams.
- Ordinary/common drops did not get beams.
- Beam distance was acceptable within Loot Beams' native item-render cap.
- Loot Journal pickup notifications worked when items were collected.
- Village/Bountiful board inspection passed where applicable.
- Save/reload passed.

Dedicated server test:

- Server staging exported.
- Server mods materialized from the active CurseForge instance with `-Clean`.
- Server configs copied as needed.
- Forge 1.20.1-47.4.20 server booted.
- Client joined localhost.
- No mod mismatch blocked join.
- Bountiful worked server-side.
- Artifacts items existed/functioned.
- Villager names appeared where applicable.
- Disconnect/rejoin passed.
- Server remained stable for 10 minutes.

Blocked during E2:

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

## Batch F Arcane Nightfall Expansion Test

Status: validation passed.

Installed:

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

Dependencies:

- CorgiLib
- Data Anchor
- Iron's Lib
- Obscure API
- Kiwi
- Resourceful Lib
- Curios API, GeckoLib, and Citadel were already present.

Client creative/system test:

- Client creative/system test passed.
- JEI opened.
- Iron's Spells items/spellbooks appeared and basic spell testing passed.
- Born in Chaos and Aquamirae content appeared.
- Enhanced Celestials loaded.
- Immersive Armors and Spartan Shields items appeared.
- Small Ships items appeared/placed where applicable.
- Handcrafted furniture appeared/placed.
- Macaw's Bridges/Fences/Walls appeared/placed.
- Selected mobs were spawned manually and fought with Better Combat / Simply Swords / spells.
- Shader-on pass succeeded.
- Save/reload passed.

Dedicated server test:

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

Passed evidence:

- Batch F client creative/system test passed.
- Batch F dedicated server boot/join test passed.
- Iron's Spells, Born in Chaos, Aquamirae, Enhanced Celestials, Bosses'Rise, Immersive Armors, Spartan Shields, Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences/Walls are stable enough for the next batch.
- Variants & Ventures was removed after the Batch J startup crash because its 1.20.1 Forge file crashes with Entity Model Features during `variantsandventures:murk_skull` model registration.
- IceAndFire Community Edition was later selected for Batch G; original Ice and Fire remains delayed so only one variant is active.
- No disposable survival test is required for batch validation.
- Full balance tuning happens later.

Blocked during Batch F:

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

## Batch G Dragonforge Cataclysm Test

Status: installed and verified.

Installed:

- IceAndFire Community Edition
- L_Ender's Cataclysm
- Marium's Soulslike Weaponry
- Create
- Create Big Cannons
- Farmer's Delight
- Create: Structures Arise

Dependencies:

- Jupiter
- Uranus
- Lionfish API
- AttributeFix
- Projectile Damage Attribute `projectile_damage-forge-3.2.2+1.20.1.jar`
- Ritchie's Projectile Library
- Curios API and GeckoLib were already present.

Startup dependency fix:

- The first Batch G client load failed because Marium's Soulslike Weaponry rejected Projectile Damage Attribute `3.2.3+1.20.1`.
- Projectile Damage Attribute is now pinned to `3.2.2+1.20.1` from Modrinth.

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
- The goal is stability, not balance.

Validation result:

- Batch G client creative/system test passed.
- Batch G dedicated server boot/join test passed.
- 10-minute stability check passed.
- No disposable survival test is required for batch validation.

Blocked during Batch G:

- Original Ice and Fire alongside IceAndFire Community Edition
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

## Batch H Civilization And Atmosphere Test

Status: validation passed.

Installed:

- Villages&Pillages
- MSS - Moog's Soaring Structures
- MES - Moog's End Structures
- Auroras
- Beautiful Enchanted Books [MOD EDITION]
- Perception
- Medieval Buildings [End Edition]
- Medieval Buildings [Nether Edition]

Dependencies:

- OctoLib/ShatterLib

Client creative/system test:

- Launch client.
- Create or load a creative test world.
- Confirm main menu and JEI load.
- Confirm Villages&Pillages content appears in JEI or can be found/spawned safely.
- Confirm MSS and MES structure content appears in `/locate` suggestions if commands expose it.
- Confirm Medieval Buildings End/Nether content appears in `/locate` suggestions if commands expose it.
- Confirm Auroras renders during a night/weather pass if visible.
- Confirm Beautiful Enchanted Books changes enchanted-book visuals without breaking JEI or enchanting screens.
- Confirm Perception loads with no client crash or visual settings conflict.
- Test shader-on pass.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from active CurseForge instance with `-Clean`.
- Copy server configs if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm Villages&Pillages, MSS, MES, and Medieval Buildings editions are present server-side.
- Confirm Auroras, Beautiful Enchanted Books, Perception, and OctoLib/ShatterLib are not required on the dedicated server.
- Generate or locate a few H structures in a fresh test world without stress-loading huge distances.
- Disconnect/rejoin.
- Let server run 10 minutes.

Blocked during Batch H:

- Integrated Villages
- Biomes O' Plenty
- Dynamic Trees
- Extra Cataclysm addons
- Ice and Fire addons
- Extra Create addons
- RPG Series modules
- Ars Nouveau
- Theurgy
- Sinytra Connector
- Fabric-only mods
- Broad integration/tuning beyond the approved custom skill tree

Passed evidence:

- Batch H client creative/system test passed.
- Batch H dedicated server boot/join test passed.
- Batch H 10-minute stability check passed.
- CTOV and Lithostitched remain delayed/removed after the earlier CTOV feature-placement crash.

## Batch I Custom Skill Tree Integration Test

Status: upgraded to the unified Ascendant Web through `config/puffish_skills/`, mirrored into the source datapack and a legacy/source OpenLoader copy, playtest passed.

Primary auto-load path:

- `config/puffish_skills/`

Fallback/source datapack:

- `datapacks/ascendant_realms_skills/`

Designed web:

- One Puffish category: `Ascendant Web`.
- 113 total nodes.
- 196 connections.
- Seven cleaner branch lanes: Warrior, Rogue / Duelist, Ranger / Hunter, Arcanist, Engineer / Artificer, Survivalist / Explorer, Dragonbound / Endgame.
- Two starting points.
- Default Puffish pacing: 1 skill point per Ascendant Web level.
- Higher-tier nodes cost 2-3 points so progression stays slow but meaningful.
- XP source is killed mob dropped XP plus killed mob max health, so Scaling Health/Improved Mobs stronger enemies naturally feed more progression.

Client creative/system test:

- Import the latest client ZIP.
- Create or choose a fresh test world.
- Confirm the imported client instance has `config/puffish_skills/config.json`.
- Launch the client.
- Open the Pufferfish's Skills UI.
- Confirm one `Ascendant Web` category appears.
- Confirm the old seven separate category tabs do not appear.
- Confirm Default Skill Trees generic combat/mining tabs do not appear.
- Confirm icons display.
- Hover several nodes and confirm each tooltip shows a fantasy sentence plus a visible `Effect:` line with the exact stat change.
- Confirm `Luckbearer` shows `Who says there is no luck?` and `Effect: Increases Luck by +1 and Stealth by +3%.`
- Hold Shift on several nodes and confirm cost, branch, and requirement metadata appears.
- Confirm the unified web starts with 2 points.
- Confirm the web uses cleaner branch lanes and does not have confusing cross-branch line clutter.
- Unlock one root node.
- Use controlled commands only if available and documented by the mod; otherwise test through normal mob XP.
- Unlock a mid node and, if enough points are available, a capstone.
- Confirm attributes apply.
- Test Better Combat melee, Simply Swords, Iron's Spells mana/cooldown/spell-power attributes, and projectile behavior after relevant unlocks.
- Check at least one specialized non-damage stat: Stealth, Tamed Damage/Resistance, Fortune, Damage Reflection, Fall Damage Reduction, or Mount Speed.
- Kill a few scaled/stronger mobs and confirm Ascendant Web XP advances without crash.
- Save/reload.
- Reopen the skill UI and confirm unlocks persist.

Dedicated server test:

- Export server staging.
- Materialize server mods from the active CurseForge instance with `-Clean`.
- Copy server configs from staging so `config/puffish_skills/` exists on the server.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Open the skill UI.
- Confirm the unified Ascendant Web appears.
- Confirm the cleaner branch-lane layout appears on the dedicated server too.
- Hover several nodes and confirm the visible `Effect:` line and Shift metadata appear on the dedicated server too.
- Unlock root and mid nodes.
- Confirm attributes apply server-side.
- Fight vanilla and modded mobs and confirm skill XP/progression does not crash.
- Disconnect/rejoin.
- Confirm unlocks and attributes persist.
- Let server run 10 minutes.

## Post-Playtest Identity And HUD Retest

Status: KubeJS/Puffish progression bridge hotfixed after the active client log showed blocked Java file access. Visual pass still needed.

Active system:

- `config/openloader/data/ascendant_realms_identity/`
- `openloader/data/ascendant_realms_identity/` source mirror
- `config/ascendant_progression/progression.json`
- `kubejs/server_scripts/ascendant_progression.js`
- `kubejs/assets/kubejs/textures/gui/ascendant_level_bar_spritesheet.png`

Client/server retest:

- Boot the dedicated server after importing the refreshed pack.
- Join with both players.
- Confirm `[Ascendant]` appears before player names if no custom team is assigned.
- Confirm Ascendant Web level appears below player names from the other player's view through `ar_skill_level`.
- Confirm the custom Ascendant XP bar appears as a compact blue segmented strip and does not cover the hotbar, hearts, armor, hunger, or mana rows.
- Confirm `Lv <number>` appears above the custom bar.
- Confirm current XP / required XP appears inside the bar.
- Confirm the unspent skill-point count appears beside the level text.
- Confirm the custom HUD is compact: a blue vanilla-style segmented XP strip, no gray slab, no duplicate empty/full bars, smaller `Lv`/SP labels, and no overlap with the hotbar.
- Confirm health, hunger, armor, and mana/status rows remain readable.
- Open inventory/resource-pack/FancyMenu screens and confirm the custom HUD hides instead of drawing over menus.
- Switch to creative mode and confirm the custom HUD clears until survival/adventure mode is active again.
- Kill mobs and confirm the bar fill updates from real Ascendant/Puffish skill XP.
- Gain an Ascendant Web level and confirm the `Level Up! <level>` title, subtitle, sound, HUD banner, and brief bar pulse.
- Open the Ascendant Web and confirm unspent points match the HUD.
- Disconnect/rejoin and confirm the prefix/level objective remains.
- Confirm the Ascendant Web still opens and uses the cleaner 196-connection layout.
- If the HUD is absent, check the latest log for `KubeJS errors found`; there should be no error mentioning `java.nio.file.Files`, `java.io.File`, `Path.resolve`, `Java.from`, `redeclaration`, `ascendant_progression.js`, or `ascendant_core_integration.js`.
- There should also be no `Path.resolve` ambiguity warnings from `ascendant_progression.js` or `ascendant_core_integration.js`.
- If the latest log shows `[Ascendant Progression] HUD bridge active` but the bar is invisible, treat the remaining issue as visual placement/layering instead of Puffish Skills data binding.
- Change dimensions or biomes and confirm Traveler's Titles popups use the visual title styling/colors instead of plain white Minecraft text.

Known gap:

- Enemy numeric levels are not implemented yet; Scaling Health does not expose a clean numeric nameplate through the inspected configs.

## Ascendant Core Integration Retest

Status: data-first core layer implemented; first light runtime bridge active for scoreboards, region tier, kill proofs, and rank promotion. KubeJS config reads now use `JsonIO`.

Automated checks:

- Run `python scripts/check-pack.py`.
- Confirm `config/ascendant_core/core_manifest.json` loads and all linked files exist.
- Confirm `config/ascendant_core/runtime_rules.json` loads and defines rank promotions, region tiers, and kill rewards.
- Confirm `kubejs/server_scripts/ascendant_core_integration.js` passes syntax checks.
- Confirm `scripts/sync-active-client-files.ps1` copies `config/ascendant_core/` into the active CurseForge instance.

Client/server retest:

- Boot the client after reimport.
- Confirm no KubeJS startup error mentions `ascendant_core_integration.js`.
- Confirm no KubeJS startup error mentions blocked Java file access.
- Open a world and run `/scoreboard objectives list`.
- Confirm these objectives exist: `ar_guild_rep`, `ar_guild_rank`, `ar_bounties_done`, `ar_structures_done`, `ar_bosses_done`, `ar_dragons_done`, `ar_region_tier`, `ar_threat_tier`, `ar_hunt_kills`, `ar_elite_kills`, and `ar_core_state`.
- Run `/function ascendant_core:status` and confirm the status readout appears.
- Kill a vanilla zombie and run `/function ascendant_core:status`; `ar_hunt_kills`, `ar_guild_rep`, and `ar_threat_tier` should increase.
- Run `/function ascendant_core:debug/add_structure_clear`, `/function ascendant_core:debug/add_boss_proof`, and `/function ascendant_core:debug/add_dragon_proof` in a test world only; confirm the status readout updates.
- Confirm rank prefixes promote automatically as reputation/proof thresholds are met. This is the first live bridge, not the final formal FTB rank-trial system.
- Join the dedicated server and repeat the objective check.
- Confirm the core layer does not change mob spawns, loot tables, mob stats, or worldgen by itself; it should only provide the shared data contract, scoreboards, counters, and rank/region mirrors for the next integration pass.

## Batch J Visual And Add-On Candidate Test

Status: validation passed.

Installed mods:

- Fantasy Armor
- Wavey Capes
- Xaero's Minimap
- Advancement Plaques
- Malfu Combat Animation

Installed dependencies/forced additions:

- Iron's Spells updated to `3.16.1`
- Iron's Lib updated to `1.1.0`

Delayed after startup crash:

- T.O Magic 'n Extras
- Alex's Caves
- Apothic Attributes
- Placebo

Installed resource packs:

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

Client creative/system test:

- Import the latest client ZIP.
- Launch client.
- Confirm there is no missing dependency screen.
- Confirm Iron's Spells still loads after the `3.16.1` update.
- Confirm resource packs appear and can be enabled without unreadable menus or broken icons.
- Create or load a creative test world.
- Confirm Xaero's Minimap renders and opens its settings/keybind UI.
- Confirm Wavey Capes works on the player model.
- Confirm Advancement Plaques/Embellished Stone displays an advancement popup cleanly.
- Confirm Fantasy Armor items appear in JEI and can be equipped.
- Confirm Malfu Combat Animation works with Better Combat and Simply Swords.
- Test one basic Iron's Spells spell.
- Test shader-on pass.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Copy server configs if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm Fantasy Armor and Malfu Combat Animation are server-side.
- Confirm Wavey Capes, Xaero's Minimap, Advancement Plaques, and all Batch J resource packs are not required server-side.
- Test one Better Combat/Simply Swords fight with Malfu animation active.
- Test one basic Iron's Spells spell.
- Disconnect/rejoin.
- Let server run 10 minutes.

Known Batch J failure triage:

- If startup still mentions T.O Magic, Alex's Caves, Apothic Attributes, or Placebo, the active CurseForge instance still has stale jars and needs to be cleaned/reimported.
- If startup reports other missing dependencies, inspect Malfu Combat Animation, Fantasy Armor, Iron's Spells, and Iron's Lib first.
- If the server materializer reports missing Batch J categories, make sure the active CurseForge instance path points to the newly imported client instance.
- If only UI/resource-pack visuals look wrong, treat it as a later polish tuning item unless the client crashes.

Passed evidence:

- Batch J client boot and creative/system test passed.
- Batch J dedicated server boot/join test passed.
- Batch J 10-minute stability check passed.
- T.O Magic, Alex's Caves, Apothic Attributes, Placebo, and TravelersCrossroads remain delayed/removed.

## Batch K Identity, Threat UI, And Atmosphere Test

Status: installed and validated.

Installed mods:

- Titles
- YDM's MobHealthBar
- Scaling Health
- Silent Lib
- Sound Physics Remastered
- Weather, Storms & Tornadoes
- CoroUtil

Weather path:

- Recommended: Weather, Storms & Tornadoes with CoroUtil.
- Delayed alternate: Simple Clouds / Project Atmosphere.
- Do not stack multiple major weather systems.

Client creative/system test:

- Import the latest client ZIP after Batch K is approved and installed.
- Launch client.
- Confirm no missing dependency screen.
- Confirm Titles renders earned titles or exposes title UI/commands.
- Confirm scoreboard below-name level display works, or static team-prefix fallback works.
- Confirm YDM's MobHealthBar renders over hostile mobs.
- Confirm passive mobs are hidden or minimally noisy.
- Confirm normal hostile mobs do not show bars from proximity alone.
- Confirm health bars appear when looking directly at a mob, when a mob is damaged, or when a mob is actively aggressive after combat.
- Confirm Enhanced Boss Bars still handles true bosses.
- Confirm Scaling Health does not crash with vanilla or modded mobs.
- Confirm blights/scaling are conservative.
- Confirm Weather, Storms & Tornadoes visuals work with Complementary Reimagined.
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
- Confirm titles persist after reconnect.
- Confirm scoreboard/rank display persists after reconnect.
- Fight vanilla and modded mobs.
- Watch weather TPS/log behavior during a storm pass if practical.
- Disconnect/rejoin.
- Let server run 10 minutes.

## Batch L Living World, Body Presence, Music, And Atmosphere Test

Status: installed and validated.

Installed server/both-side mods:

- Spawn Balance Utility
- Majrusz's Progressive Difficulty
- Majrusz Library
- Improved Mobs
- TenshiLib

Installed client-only mods/resource packs:

- Not Enough Animations
- AmbientSounds 6
- CreativeCore
- Presence Footsteps
- Biome Music
- Medieval Music
- Sound Physics Remastered

Client creative/system test:

- Import the latest client ZIP.
- Launch client.
- Confirm no missing dependency screen.
- Create or load a creative test world.
- Confirm Not Enough Animations does not break Better Combat, Combat Roll, Simply Swords, shields, or Iron's Spells.
- Confirm vanilla sound, AmbientSounds, Presence Footsteps, Biome Music, Medieval Music, and Sound Physics Remastered work without zero-audio symptoms.
- If audio is silent, check the Minecraft output device and Windows/Sonar route first because the prior zero-audio report was traced to headphone/output routing.
- Confirm Weather, Storms & Tornadoes remains the only major weather system.
- Fight vanilla and modded mobs.
- Confirm Majrusz's Progressive Difficulty, Improved Mobs, and Scaling Health overlap does not crash.
- Confirm YDM's MobHealthBar remains readable during fights.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Copy server configs if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm Spawn Balance Utility, Majrusz's Progressive Difficulty, Majrusz Library, Improved Mobs, and TenshiLib are present server-side.
- Confirm Not Enough Animations, AmbientSounds, CreativeCore, Presence Footsteps, Biome Music, Medieval Music, and Sound Physics Remastered are not required server-side.
- Fight vanilla and modded mobs.
- Disconnect/rejoin.
- Let server run 10 minutes.

Known Batch L failure triage:

- If the server materializer reports missing Batch L jars, import the latest client ZIP into the active CurseForge instance and rerun materialization from that active instance mods folder.
- If audio is ugly but stable, keep the batch technically valid and move volume/mix tuning to the later polish pass.
- If early nights are too hard but stable, record it for full survival tuning rather than failing the boot/system validation gate.

## Batch N Cohesion And Integration Layer Test

Status: installed and validated.

Installed both-side/server-required mods:

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

Client creative/system test:

- Import the latest client ZIP.
- Launch client.
- Confirm no missing dependency screen.
- Confirm JEI loads.
- Confirm no KubeJS script errors.
- Confirm the Ascendant Realms skill tree/global datapack is available without manually copying a datapack into the world.
- Confirm Polymorph UI works on a duplicate recipe if one is available.
- Confirm Every Compat generated blocks appear without missing textures.
- Confirm Slice & Dice items appear in JEI.
- Confirm Alex's Delight items and recipes appear in JEI.
- Create a fresh creative test world.
- Inspect several villages and dungeons for placement crashes or broken blocks.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Copy configs, `kubejs`, and `openloader` if needed.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm Batch N jars are present server-side.
- Confirm the skill tree/global datapack loads without manual world-copy steps.
- Confirm recipes and food/Create integration work.
- Confirm new villages/dungeons generate without immediate placement crashes.
- Disconnect/rejoin.
- Let server run 10 minutes.

Known Batch N failure triage:

- If startup fails on Quark, confirm Zeta is present.
- If startup fails on Supplementaries or Every Compat, confirm Moonlight Lib is present.
- If worldgen placement crashes, test Integrated Villages and IDAS separately before touching KubeJS, Almost Unified, or Polymorph.
- If recipes conflict but the pack is stable, record the conflict for the next KubeJS recipe pass.

## Batch M Lighting, Fire, Lanterns, And Micro-Polish Test

Status: installed and validated.

Installed client-only mods:

- Sodium Dynamic Lights
- Sodium Options API

Installed both-side/server-required mods:

- Amendments
- Macaw's Lights and Lamps
- Decorative Blocks

Client creative/system test:

- Import the latest client ZIP.
- Launch client.
- Confirm no missing dependency screen.
- Confirm the previous Supplementaries warning about missing Amendments no longer appears.
- Create or load a creative test world.
- Confirm held torch emits dynamic light.
- Confirm dropped torch emits dynamic light.
- Confirm fire, lava, glow items, or other supported light sources behave correctly if supported.
- Confirm lanterns look good with shaders.
- Place and toggle Macaw lights.
- Place Supplementaries and Amendments blocks that cover wall lanterns, skull candles, ceiling pots, ceiling banners, and skull piles.
- Place Decorative Blocks braziers, chandeliers, and bonfires.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Confirm Sodium Dynamic Lights and Sodium Options API are absent from the materialized server mods folder.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Place Amendments, Macaw's Lights and Lamps, Decorative Blocks, Supplementaries, and Quark blocks.
- Disconnect/rejoin.
- Let server run 10 minutes.

Known Batch M failure triage:

- If the Supplementaries warning still appears, confirm `amendments-1.20-2.2.5.jar` is present in the active client instance.
- If server join fails, verify Sodium Dynamic Lights and Sodium Options API were not copied server-side.
- If a lighting crash occurs, test Sodium Dynamic Lights separately before touching decorative/block mods.

## World Integration And Main Menu Polish Retest

Status: installed and validated.

Installed client-only UI mods:

- FancyMenu
- Konkrete
- Melody
- Immersive UI

Crash retest target:

- Latest seed: `4571938849163387743`
- Latest structure center chunk: `15,9`
- Latest approximate block target: `x=240, z=144`
- Secondary seed: `-8696758597753506463`
- Secondary approximate block target: `x=224, z=432`
- Previous crash feature: `integrated_villages:airship_village`

Client creative/system test:

- Import the latest client ZIP.
- Launch the client.
- Confirm no missing dependency screen.
- Confirm FancyMenu and Immersive UI load.
- Confirm the title-screen MP4 background renders outside the editor. If it shows purple/black or falls back to the old background, check the latest log for WaterMedia or FancyMenu watchdog messages.
- Open FancyMenu's title-screen editor from the main menu.
- Save a clean title-screen layout using `config/fancymenu/assets/ascendant_realms_title.png`.
- Confirm the menu buttons remain readable and clickable at 1920x1080 and a smaller window size.
- Create a fresh creative test world using seed `4571938849163387743`.
- Fly toward approximately `x=240, z=144`.
- Confirm the prior Integrated Villages airship crash does not reproduce.
- Inspect several generated villages, dungeons, towers, roads, and landmark structures for missing blocks, broken loot, or extreme density.
- Confirm mobs from Alex's Mobs, Mowzie's Mobs, Born in Chaos, Aquamirae, IceAndFire CE, Cataclysm, and Marium's stack still appear or can be spawned.
- Save/reload.

Dedicated server test:

- Export server staging.
- Materialize from the active CurseForge instance with `-Clean`.
- Confirm FancyMenu, Konkrete, Melody, and Immersive UI are absent from the server mods folder.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Create a fresh server world with seed `4571938849163387743`.
- Approach approximately `x=240, z=144`.
- Confirm the repaired Integrated Villages workstation processor path does not reproduce the prior POI-cast crash server-side.
- Inspect nearby structures and villages.
- Disconnect/rejoin.
- Let server run 10 minutes.

Known failure triage:

- If the same Integrated Villages crash path returns, inspect the failing processor/template path before removing content.
- Disable an exact Integrated Villages structure only as a temporary emergency bypass while a data repair is built.
- If menu visuals are ugly but the game is stable, keep the technical pass active and tune the FancyMenu layout in-game.

## UI Customization Tooling Test

Status: installed through Packwiz. Packwiz refresh, check-pack, client export, and server staging export passed; in-game validation is pending after client reimport.

Installed client-only UI mods:

- SpiffyHUD
- Drippy Loading Screen
- Item Borders
- Stylish Effects
- Overflowing Bars

Installed both-side UI/survival readability mod:

- AppleSkin

Delayed:

- RPG-Hud remains delayed as a separate A/B test.

Client creative/system test:

- Import the latest client ZIP.
- Launch the client.
- Confirm no missing dependency screen.
- Confirm SpiffyHUD config/editor is available alongside FancyMenu.
- Confirm `ascendant_level_bar_spritesheet.png` is available in FancyMenu/SpiffyHUD assets.
- Place the level bar near the hotbar and place a level-number text element above it for visual testing. Only treat this as final if the text is reading Ascendant/Puffish progression rather than vanilla XP.
- Confirm Drippy Loading Screen loads or exposes its loading-screen customization.
- Confirm Item Borders renders inventory rarity borders without fighting Legendary Tooltips.
- Confirm Stylish Effects makes active potion/status effects readable with STONEBORN, Immersive UI, Xaero's Minimap, and shader UI scale.
- Confirm Overflowing Bars renders health, armor, and toughness cleanly with AttributeFix and Scaling Health.
- Confirm AppleSkin shows hunger, saturation, and food values for vanilla, Farmer's Delight, and Alex's Delight food.
- Confirm normal gameplay HUD, minimap, mob health bars, hotbar, tooltips, and skill UI remain readable.
- Save/reload.

Dedicated server test:

- Export server staging.
- Import the latest client pack into the active CurseForge instance.
- Materialize server mods from the active instance path with `-Clean`.
- Confirm AppleSkin is present in the final server jar list.
- Confirm SpiffyHUD, Drippy Loading Screen, Item Borders, Stylish Effects, and Overflowing Bars are absent from the server mods folder.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm AppleSkin food/saturation information remains accurate in multiplayer.
- Disconnect/rejoin.
- Let server run 10 minutes.

## Guild/Hunter RPG Spine Test

Status: installed and scaffolded. Validation pending after client reimport.

Installed both-side/server-required mods:

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

Client creative/system test:

- Import the latest client ZIP.
- Launch the client.
- Confirm no missing dependency screen.
- Confirm KubeJS creates `guild_mark`, `hunter_seal`, and `ascendant_sigil`.
- Confirm Patchouli loads and the Ascendant Codex appears.
- Confirm FTB Quests opens without errors.
- Confirm FTB Ranks commands or config surfaces are present enough for later rank testing.
- Confirm Easy NPC menus/items work.
- Confirm CustomNPCs tools/items or creative access works.
- Confirm Human Companions can spawn or appear without client errors.
- Create or load a creative test world.
- Run rank functions manually in a copied test world if command permissions allow it.
- Save/reload.

Dedicated server test:

- Export server staging.
- Import the latest client pack into the active CurseForge instance.
- Materialize server mods from the active instance path with `-Clean`.
- Confirm the copied list includes Patchouli, FTB Library, FTB Teams, FTB Quests, FTB Ranks, Easy NPC bundle/core/config UI, CustomNPCs-Unofficial, and Human Companions.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Confirm KubeJS startup has no Guild item errors.
- Confirm the Ascendant Codex datapack exists server-side.
- Confirm FTB Quests and FTB Ranks do not reject the client.
- Confirm Easy NPC, CustomNPCs, and Human Companions do not crash during simple NPC/entity testing.
- Disconnect/rejoin.
- Let server run 10 minutes.

Known Guild/Hunter failure triage:

- If FTB Quests fails, confirm FTB Library, FTB Teams, and Architectury API are present.
- If FTB Ranks fails, confirm FTB Library is present.
- If Easy NPC fails, confirm Easy NPC Core and Easy NPC Config UI are present.
- If CustomNPCs or Human Companions causes startup or entity crashes, isolate that tool before touching Patchouli/FTB.
- If the Codex is missing, check `config/openloader/data/ascendant_realms_codex/` before changing Patchouli.
- If rank display is not visible, keep the existing vanilla scoreboard fallback and treat FTB Ranks config as an authoring task, not a mod failure.
- If NPC equipment authoring fails, compare the template against `config/ascendant_guild/npc_loadouts.json`; every listed item should exist in `config/ascendant_index/gear_registry.json`.
- If nameplates still look too flat, use `config/ascendant_guild/nameplates.json` as the target contract and move to a custom Forge overlay instead of trying to force a Bukkit/Paper plugin into the Forge pack.

## Later Boss/Mob Test

- Bosses are discoverable, not everywhere.
- Villages survive normal nights.
- Dragon-tier mobs do not spawn near first base unless intended.
- Boss loot is meaningful but not build-ending.


## Ascendant Guild Worldgen And Generated NPC Test

Status: pending Jayden in-game validation.

- Create a fresh creative test world.
- Run `/function ascendant_guild:npc/list`.
- Run `/function ascendant_guild:npc/spawn_set/starter_guild_staff`.
- Run `/function ascendant_guild:npc/spawn_set/roadside_rumor_camp` away from the first group.
- Run `/function ascendant_guild:npc/spawn_set/frontier_guild_outpost` away from the first group.
- Confirm generated NPCs show rank, level, name, and role without manual editing.
- Confirm generated NPCs use medieval/MCA-style bridge skins rather than Steve or plain CustomNPCs defaults.
- Confirm generated NPCs have visible role gear from the pack, such as books/staves/crossbows/shields/armor.
- Confirm social NPCs stay near their spawn instead of all marching away together.
- Spawn a vanilla zombie near Guard Captain, Wounded Hunter, or Mira Ash and check whether combat-profile NPC behavior is usable. If they still ignore hostiles, log it as the next faction/script/runtime task rather than removing the NPC system.
- Confirm test-killing a duplicate NPC does not drop the full visible kit.
- Run `/locate structure ascendant_guild:hunter_board_village_standard`.
- Run `/locate structure ascendant_guild:roadside_hunter_camp`.
- Run `/locate structure ascendant_guild:frontier_guild_outpost`.
- Teleport to each structure in fresh chunks.
- Confirm a normal village no longer gets several generated Guild boards stacked too close together.
- Confirm Bountiful bounty boards and multiple Supplementaries notice boards render.
- Confirm notice boards show readable rank, roster, rules, rumor, or frontier text instead of blank pages.
- Confirm notice boards face outward rather than into the wooden wall.
- Confirm roadside camp and frontier/village containers contain loot.
- Confirm roadside camp lanterns are attached to posts or blocks, not floating.
- Confirm wall-adjacent Hunter/Frontier lanterns use Macaw wall lantern blocks.
- Confirm no startup, datapack, or chunk-generation errors.
- On dedicated server, repeat locate/generate/join/rejoin and 10-minute stability checks.
