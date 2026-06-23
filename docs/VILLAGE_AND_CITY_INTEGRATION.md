# Village And City Integration

Status: Batch N installed and validated; density tuning active.

Guild/Hunter direction:

`docs/GUILD_HUNTER_SYSTEM_RUNDOWN.md` is the master plan for making villages and towns matter through Hunter Boards, Guild clerks, Rank Examiners, rival sightings, local requests, and major Guild settlements. This document keeps the current village/city integration notes; the Guild rundown defines the next social/RPG spine.

Guild/Hunter implementation update:

- Patchouli, FTB Quests, FTB Ranks, Easy NPC, CustomNPCs-Unofficial, and Human Companions are now installed for the first social/RPG pass.
- `config/ascendant_guild/hunter_boards.json` defines Village Hunter Board, Town Guild Board, and Major Guild Registry templates.
- `config/ascendant_guild/npc_roster.json` defines the starting village/town/Guild NPC roles.
- `config/ascendant_guild/npc_loadouts.json` defines player-obtainable gear loadouts for clerks, examiners, guard captains, and named rivals.
- `config/ascendant_guild/nameplates.json` defines the target rank/level/profession nameplate profiles.
- `config/ascendant_settlements/settlement_unification.json` defines settlement ownership, crash-safe boundaries, and the custom-mod threshold.
- `config/ascendant_core/structure_ecology.json` now defines village/town, Guild anchor, road/camp, dungeon, major dungeon, and boss/dragon structure roles for later density and loot tuning.
- `config/ascendant_core/npc_role_contracts.json` now defines the standard Guild/social/rival NPC contract so generated NPCs remain profile-driven instead of hand-built.
- The next in-game build target is polish/validation of the generated Hunter Board - Village Standard, Roadside Hunter Camp, and Frontier Guild Outpost rather than hand-building more one-off NPCs.
- Actual board structures and NPC placements now have a generated test layer: `ascendant_guild:hunter_board_village_standard`, `ascendant_guild:roadside_hunter_camp`, and `ascendant_guild:frontier_guild_outpost` generate as standalone structures through Open Loader. NPCs are generated from `config/ascendant_guild/generated_npc_profiles.json` and spawn sets under `/function ascendant_guild:npc/spawn_set/*`.
- The first in-game pass showed the idea works but needed tuning: NPCs had titles but no gear/skins, board structures were too dense near villages, roadside camp containers were empty, and notice boards needed multiple written boards. The generator now applies CustomNPCs skin textures, loadout gear, wider spacing, written notice-board rosters, loot tables, and grounded lantern supports. The skin texture repair mirrors the MCA-style bridge PNGs into CustomNPCs' native resource folder as well as the compatibility resource pack so NPCs do not render as magenta missing textures.

Installed:

- Integrated Villages: `integrated_villages-1.3.2+1.20.1-forge.jar`
- Integrated API
- Supplementaries
- Quark
- Zeta
- Every Compat
- Moonlight Lib

Existing village/civilization stack:

- Towns and Towers
- Villages & Pillages
- Guard Villagers
- Villager Names
- Bountiful
- MVS - Moog's Voyager Structures
- Structory
- Medieval Buildings End/Nether editions

Reason for active install:

CTOV was previously delayed after a swamp-village feature-placement crash, and villages still feel too bland. Integrated Villages is now part of Batch N because it may connect villages with the current Create, Farmer's Delight, Supplementaries, and structure ecosystem more naturally.

Risk notes:

- Integrated Villages overlaps with Towns and Towers, Villages & Pillages, MVS, Structory, and other village/landmark generation.
- The latest village crashes share the Integrated API `integrated_api:workstation_processor` POI path, not three unrelated bad village structures. `config/openloader/data/ascendant_realms_world_integration` now replaces that processor with static `minecraft:rule` workstation placeholder replacements, keeps `airship_village`, `mossy_mounds`, and `marketstead_village` enabled for retest, and repairs Integrated Villages' broken `minecraft:village` tag by removing only nonexistent `integrated_villages:swamp_village`.
- Quark and Supplementaries add gameplay/building content, not only structures.
- New worlds are required for a fair structure test.
- If placement crashes return, inspect the failing processor/template path first and add a data repair where possible. Disable an exact structure only as a temporary emergency fallback; move Integrated Villages to a Batch N.1 experimental branch only if crashes are broad or repeated after processor repair.

Current integration pass:

- Generated configs from the active client instance were copied into the pack source for Integrated Villages, IDAS, Every Compat, Supplementaries, Quark, Towns and Towers, and related worldgen/block systems.
- `docs/WORLD_INTEGRATION_AUDIT.md` now inventories the active village/city/structure data surfaces so tuning can target actual content instead of guesses.
- The goal is to let villages use the current block palette and integration stack while avoiding another CTOV-style total village overhaul crash.
- The Ascendant Settlements layer now adds standalone Ascendant Guild structures only: `hunter_board_village_standard`, `roadside_hunter_camp`, and `frontier_guild_outpost`. Prove them with `/locate`, fresh chunk generation, and server stability before deciding whether village-pool injection or a small custom Forge helper mod is needed.
- Current standalone Guild spacing is intentionally conservative after the first test village showed too many board structures: Hunter Board `192/80`, Roadside Camp `224/96`, Frontier Outpost `288/128`.
- Supplementaries notice boards remain part of the Guild presentation. Use several readable written boards per structure instead of one overloaded board.

Current density/NPC tuning:

- Integrated Villages no longer disables vanilla villages, so vanilla villages can coexist with the integrated village stack.
- Integrated Villages regular villages now use `64/32` spacing with a larger `12` chunk village-avoid exclusion zone.
- Sparse Structures is back to a soft anti-spam role: global `1.25`, vanilla village factor `1.0`, pillager outpost factor `1.1`.
- Towns and Towers towns are widened to `52/24`.
- Towns and Towers towers are widened to `48/22`, frequency `0.35`.
- Towns and Towers miscellaneous structures are widened to `36/14`.
- Guard Villagers now spawns `10` guards per village instead of `6`.
- Guards now patrol regularly.
- Guard health increased from `20` to `24`.
- Guard follow range increased from `20` to `28`.

Intent:

- Villages should feel more common and more alive.
- Settlements should have enough guards to survive the harder world, but they should not be perfect safe zones.
- Villages should eventually give the player reasons to care through Hunter Boards, local requests, bounty context, named NPCs, and visible Guild presence.
- If village overlap becomes ugly, tune Towns and Towers/Sparse Structures before removing Integrated Villages.

Validation notes:

- Generate a fresh creative test world.
- Locate multiple village types.
- Confirm bounty boards, named villagers, guards, and new integrated structures can coexist.
- Retest seed `3740828705519225665`, generated chunk `-33,-26`, plus seed `4571938849163387743` around `x=240, z=144` and seed `-8696758597753506463` around `x=224, z=432` to confirm the workstation processor repair prevents the known crash path.
- Watch logs for feature-placement crashes.

