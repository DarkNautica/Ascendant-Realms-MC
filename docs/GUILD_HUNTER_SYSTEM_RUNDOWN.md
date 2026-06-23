# Guild Hunter System Rundown

Status: first Guild/Hunter tool pass installed and scaffolded. The master design is now backed by Patchouli, FTB Quests, FTB Ranks, Easy NPC, CustomNPCs-Unofficial, Human Companions, generated Guild data, starter rank functions, starter Guild currency items, and a starter Ascendant Codex. This is not yet validated in-game and still needs client/server boot testing plus in-world authoring.

Ascendant Realms already has the core world: terrain, structures, combat, spells, mobs, bosses, loot, visual identity, survival pressure, and a custom skill tree. The missing spine is social meaning. Players need to feel like they are rising inside a dangerous hunter society instead of only wandering through a beautiful modded world.

The goal is a medieval fantasy survival RPG where players become recognized hunters by protecting settlements, clearing structures, mastering weapons and magic, competing with rivals, and surviving threats that villages cannot handle alone.

## Core Identity

Ascendant Realms should feel like this:

The world is dangerous, beautiful, and already inhabited. Villages need protection. Guilds organize hunters. Ranks define public power. Rivals are competing. Bounties point players toward danger. Towns feel like real hubs. The Codex gives direction. The player rises through the world by surviving, protecting, discovering, and becoming recognized.

This should not become a town-building pack. Settlement interaction matters, but the player is a hunter/adventurer, not a colony manager.

## Guild Rank System

Ranks are the public social layer. They are separate from normal XP level and separate from the custom Ascendant Web skill progression.

Recommended rank ladder:

- Unranked: not formally recognized by the Guild.
- E-Rank: unknown survivor, barely registered hunter.
- D-Rank: field adventurer and village-level helper.
- C-Rank: licensed monster hunter.
- B-Rank: elite hunter and dungeon clearer.
- A-Rank: realm-class fighter.
- S-Rank: ascendant-class anomaly and myth-tier hunter.

Rank should feel like an institution judging the player's record, not a fake checklist. The player should return to a Rank Examiner NPC at a Guild Hall, Hunter Board station, or major town and request evaluation.

Evaluation should consider:

- Bounties completed.
- Bosses defeated.
- Dangerous mobs killed.
- Structures cleared.
- Dimensions discovered.
- Village defense or rescue outcomes.
- Rare gear obtained.
- Magic and weapon milestones.
- Rival hunter comparisons.
- Death count only if it improves the design rather than punishing experimentation.

Likely implementation stack:

- FTB Quests for hidden milestone tracking and structured rank objectives.
- FTB Ranks or a similar rank/title system for public rank display if compatible.
- Titles and the existing vanilla scoreboard fallback for visible identity until a better rank display is proven.
- KubeJS for glue logic, reward triggers, and pack-specific integration.
- Easy NPC or CustomNPCs for Rank Examiner interactions.
- Patchouli for in-game explanation through the Ascendant Codex.

Current active tools that already support the direction:

- Titles is installed and validated.
- KubeJS is installed and validated. Recipe/tag/loot files remain cautious scaffolds, while the progression HUD and Ascendant Core loader are active bridges.
- Open Loader is installed and validated.
- Patchouli is installed for the Ascendant Codex.
- FTB Quests is installed for rank milestones and structured Guild quests.
- FTB Ranks is installed for rank display/permission experiments.
- Easy NPC is installed for Guild clerks, rank examiners, and controlled social NPCs.
- CustomNPCs-Unofficial is installed for named rival-hunter prototypes and combat-capable special NPCs.
- Human Companions is installed for generic hunter/companion testing.
- The OpenLoader/KubeJS progression bridge currently displays Ascendant Web level below player names, renders the custom skill-XP bar, and keeps a static `[Ascendant]` prefix fallback.

Missing or not-yet-authored pieces:

- FTB quest chapter files still need in-game editor/export work or a confirmed SNBT generation format.
- FTB Ranks config should be authored after the first boot confirms the generated config layout.
- Actual NPCs still need to be created and placed in a creative copy.
- Hunter Board structures still need to be built and exported.
- Guild currency textures/models are placeholder-only.
- MCA Reborn is installed with MCA - Default Medieval default-enabled, but remains unverified until medieval/fantasy skin control and server behavior are proven.

## Villages Must Matter

Villages should be more than scenery. A village should imply local needs, danger, protection, and a reason to return.

Every significant village should ideally have:

- A Hunter Board or village bounty board.
- A local Guild Clerk or village representative.
- Guards or defenders.
- A notice board with local problems and rumors.
- Small bounties or requests.
- Nearby threats the player can clear.
- Rewards that make returning worthwhile.

Village problems should include:

- Clear the nearby crypt.
- Rescue a missing scout.
- Kill the beast attacking livestock.
- Defend against raiders.
- Recover stolen supplies.
- Escort or rescue a wounded hunter.
- Bring medicine or food to a local helper.
- Investigate a monster sighting.
- Repair or reinforce defenses.

Villages should react to rank:

- E-Rank: skepticism.
- D-Rank: cautious hope.
- C-Rank: respect.
- B-Rank: trust.
- A-Rank: urgency and awe.
- S-Rank: legendary treatment.

Current active tools that already support village meaning:

- Guard Villagers.
- Villager Names.
- Bountiful.
- Supplementaries.
- Integrated Villages.
- Towns and Towers.
- Villages and Pillages.
- MVS, MSS, MES, Structory, YUNG structures, Medieval Buildings.
- Patchouli, FTB Quests, FTB Ranks, Easy NPC, CustomNPCs-Unofficial, and Human Companions are now installed for the first Guild/Hunter implementation pass.

Missing or not-yet-authored pieces:

- Built Hunter Board structures.
- Placed local clerks, representatives, and Rank Examiner NPCs.
- FTB quest chains that point to specific village problems.
- Final Patchouli entries that reference actual in-world boards and NPCs.

## Major Towns And Guild Settlements

Normal generated villages are not enough for the intended fantasy. The pack needs rare, meaningful hubs that feel like Guild settlements rather than random vanilla village variants.

Recommended settlement types:

- Small Guild Outpost.
- Frontier Town.
- Walled Hunter Town.
- Capital Guild Hall or major Guild city.
- Ruined Guildhall.
- Fortress Sanctuary.

Major towns should include:

- Guild Hall.
- Hunter Board.
- Rank Examiner.
- Bounty Master.
- Guild Clerk.
- Tavern.
- Blacksmith or weapon appraiser.
- Arcanist or spell scholar.
- Inn or respawn area.
- Training yard.
- Guard barracks.
- Market stalls.
- Notice board.
- Rival hunter NPCs.
- Waystone or travel point only if a compatible travel system is deliberately added.

Preferred generation route:

- Build curated structures in creative.
- Save them as structure templates.
- Add them through datapack structures, jigsaw/template pools, or a compatible structure tool.
- Use biome variants for material swaps.
- Do not rely on vanilla village randomness to create logical Guild towns.

## Hunter Board System

The Hunter Board should be the central world object that ties villages, towns, ranks, bounties, rumors, and rival activity together.

It needs to be consistent enough for players to recognize instantly, but varied enough to avoid copy-paste boredom.

Recommended scale variants:

- Village Hunter Board: small 5x4 or 7x5 roadside or village-center station.
- Town Hunter Board: medium 9x6 board with separate contract, notice, and rank areas.
- Major Guild Registry: large interior wall in Guild Halls or major towns.

Standard functional layout:

- Center: Bountiful Bounty Board.
- Left: Supplementaries Notice Board for local warnings, missing people, and rumors.
- Right: rank plaques, evaluation sign, or Guild status board.
- Top: Guild banner or crest.
- Bottom: crates, candles, monster trophies, broken weapons, maps, barrels.
- Nearby: Guild Clerk, Bounty Master, or Rank Examiner NPC.

Board content categories:

- Active Contracts.
- Local Threats.
- Village Requests.
- Rank Evaluation.
- Hunter Sightings.
- Realm Warnings.

Visual palette:

- Wood: dark oak and spruce.
- Stone: deepslate, stone brick, cracked stone.
- Metal: iron bars, chains, anvils.
- Light: lanterns, candles, soul lanterns for dangerous towns.
- Cloth: Guild banners.
- Accent: gold trim only for high-rank boards.

Avoid:

- Modern-looking skins or signage.
- Bright clashing colors everywhere.
- Too many signs.
- Random modded blocks with mismatched texture language.
- Huge unreadable wall text.

First prototype to build:

- 7 blocks wide.
- 5 blocks tall.
- 2 blocks deep.
- Dark oak frame.
- Deepslate base.
- Bountiful board in center.
- Supplementaries Notice Board on the left.
- Rank sign or plaque on the right.
- Two lanterns.
- One Guild banner.
- One barrel or crate.
- One monster trophy.
- One Guild Clerk NPC nearby once an NPC tool is installed.

This should become the "Hunter Board - Village Standard" template. After it looks good, build richer town and Guild Hall variants from the same visual bones.

## Rival Hunters

The world should feel like other hunters exist, compete, help, fail, and sometimes beat the player to contracts. Do not simulate dozens of real AI hunters across unloaded chunks. Use a hybrid illusion:

- Real NPCs when players are nearby.
- Simulated rival progress when players are far away.
- Evidence, rumors, camps, board updates, and dialogue to make them feel active.

Initial named rivals:

- Mira Ash: C-Rank scout. Finds structures, sells maps, can be rescued.
- Darius Crowe: B-Rank duelist. Arrogant, competitive, may challenge the player.
- Seren Valehart: B-Rank arcanist. Tied to magic and corruption knowledge.
- Kael Vorn: A-Rank monster hunter. Rarely appears and may clear threats first.
- The Black Hound: S-Rank unknown. Mostly rumors and evidence, extremely rare physical appearance.

Rival hunter behavior should include:

- Appearing in taverns and Guild Halls.
- Taking contracts from boards.
- Leaving camp evidence near dungeons.
- Being found wounded or dead.
- Fighting mobs when the player approaches.
- Claiming bounties if the player waits too long.
- Challenging or helping the player based on relationship.
- Being mentioned by NPCs and notice boards.
- Affecting rank evaluation context.

Rival Hunter Director concept:

Keep a hidden ledger of named hunters. Each rival needs:

- Name.
- Rank.
- Class.
- Home town.
- Personality.
- Preferred biome or region.
- Current status.
- Kill count.
- Boss clear count.
- Relationship with player.
- Active, inactive, wounded, missing, or dead status.

Every few in-game days, a lightweight director can roll events:

- A rival accepts a bounty.
- A rival clears a crypt before the player.
- A rival is wounded.
- A rival camp appears near a structure.
- A hunter sighting is posted on the board.
- A rival challenges the player after repeated competition.
- The Black Hound leaves evidence near a cleared danger zone.

Good example loops:

- Rival beats player: the board lists a B-Rank contract, Darius Crowe is marked interested, the player waits too long, Darius claims it, the board updates, and Darius appears in the tavern bragging.
- Rival needs help: Mira Ash scouts a dungeon, the player finds her wrecked camp, a trail leads inside, and the player can rescue or abandon her.
- S-Rank mystery: the board says The Black Hound was sighted, the player finds dead monsters and broken weapons, but no hunter. Later the Black Hound appears briefly in a Guild Hall.

Likely implementation stack:

- CustomNPCs Unofficial for named combat-capable rivals if verified clean for the pack.
- Easy NPC for social/town versions of rivals.
- Human Companions for generic wild hunters if compatible and visually acceptable.
- In Control for rare generic hunter patrols and spawn rules.
- KubeJS for director logic and event glue.
- FTB Quests for tracked rival events and rank evaluation milestones.
- Bountiful and Hunter Boards for public contract context.

## NPCs And Skins

NPCs must match the medieval fantasy tone. Avoid modern outfits, modern civilian skins, and random visual noise.

Required NPC archetypes:

- Guild Registrar.
- Rank Examiner.
- Bounty Master.
- Guild Clerk.
- Hunter Quartermaster.
- Weapon Appraiser.
- Arcanist.
- Tavern Keeper.
- Town Steward.
- Guard Captain.
- Wounded Hunter.
- Rival Hunter.
- Village Elder or local representative.

Potential tools:

- Easy NPC for town NPCs, dialogue, clerks, merchants, and rank examiners.
- CustomNPCs Unofficial for combat-capable named rivals if verified.
- Guard Villagers for village defense, already installed.
- Human Companions for generic hunter presence if verified and visually acceptable.
- MCA Reborn only stays if MCA - Default Medieval keeps villagers medieval/fantasy-safe in normal play. If skins cannot be controlled cleanly, remove or delay it again.

## NPC Equipment And Nameplates

Status: formal data contract implemented; generated CustomNPC spawn sets are active for testing.

The NPC layer now has four source files:

- `config/ascendant_guild/npc_loadouts.json`
- `config/ascendant_guild/nameplates.json`
- `config/ascendant_guild/generated_npc_profiles.json`
- `config/ascendant_guild/generated_npc_spawn_sets.json`

The loadout registry ties important NPCs and rivals to real gear from `config/ascendant_index/gear_registry.json`. This means a Guild Clerk, Rank Examiner, rival scout, arcanist, or monster hunter should visibly wear or carry gear the player can actually find in the world. Social NPCs use no-drop identity gear; rivals use story-safe drop policies so named characters do not become farmable gear vending machines.

The nameplate registry defines the target visual identity:

```text
[ C-Rank ] Mira Ash
Lv. 34 Scout
```

Current fallback:

- Players: vanilla teams/scoreboard plus FTB Ranks/Titles experiments.
- NPCs: Easy NPC and CustomNPCs display names.

Do not install Bukkit/Paper nameplate plugins directly into this Forge pack. Use that style as visual reference only. If the fallback remains too flat after the NPC templates exist, build the small internal `Ascendant Nameplates` Forge overlay so the pack can render styled two-line plates cleanly.

Validation is handled by `scripts/check-pack.py`: loadout item IDs must exist in the generated gear registry, rank rarity ceilings must match or have an override reason, rivals need drop policies, and every loadout profile needs a matching nameplate profile.

## Ascendant Settlements Layer

Status: standalone generated Guild/Hunter worldgen pilot active.

The settlement ownership contract lives at `config/ascendant_settlements/settlement_unification.json`.

This now adds only standalone Ascendant Guild structures. It does not inject into vanilla, Integrated Villages, Towns and Towers, IDAS, or other third-party village pools yet. The current rule is standalone first:

1. Generate and test `ascendant_guild:hunter_board_village_standard`.
2. Generate and test `ascendant_guild:roadside_hunter_camp`.
3. Generate and test `ascendant_guild:frontier_guild_outpost`.
4. Prove `/locate`, natural generation, client load, dedicated server load, and stability.
5. Only then consider injecting rare board pieces into vanilla or modded village pools.

A custom `Ascendant Settlements` Forge helper mod is approved only when data-driven control is not enough: automatic NPC equipment hooks, animated nameplates, runtime village role assignment, or deep jigsaw conflict handling.

## Ascendant Codex

The player needs an in-game guidebook that gives direction without spoiling the whole pack.

Active tool:

- Patchouli. The starter Ascendant Codex exists in `config/openloader/data/ascendant_realms_codex/`, mirrored to repo-level OpenLoader/datapack folders for source/reference.

Suggested Codex chapters:

- Welcome to Ascendant Realms.
- The Guild.
- Hunter Ranks.
- Evaluation.
- Hunter Boards.
- Bounties and Guild Marks.
- Villages and Protection.
- Rival Hunters.
- Weapons and Combat Paths.
- Magic and Spell Paths.
- Dangerous Structures.
- Known Realm Threats.
- Major Towns.
- Early Survival Goals.

The Codex should explain what to pursue and why, not list every mod or every secret.

## Currency And Rewards

The Guild needs a reward currency so contracts matter beyond random loot.

Candidate currency names:

- Guild Marks.
- Hunter Seals.
- Ascendant Tokens.
- Realm Sigils.

Contract and quest rewards can feed:

- Spell scrolls.
- Weapon upgrade materials.
- Rare food and potions.
- Maps to structures.
- Rank cosmetics.
- Rank-appropriate gear.
- Mount or travel items if compatible.
- Special materials for Create, magic, boss, dragon, and skill-tree systems.

Rank should unlock better contracts and vendors, but not hard-lock all exploration.

## Structure And World Integration

Existing exploration content should become bounty targets and world threats.

Contract tiers should guide players into the current modded content:

- E/D-Rank: small undead camps, village requests, common monster parts, rescue tasks.
- C-Rank: crypts, towers, named minibosses, dangerous structure scouting.
- B-Rank: larger dungeons, beast hunts, village raid defense, elite monster contracts.
- A-Rank: major bosses, rare relic recovery, dangerous dimensions.
- S-Rank: realm-level threats, legendary bosses, corrupted ancient sites.

Structures should not just be loot containers. Hunter Boards should point players toward them, rivals should appear around them, and the Codex should teach why they matter.

## Tools To Evaluate Or Add

Already installed and useful:

- Bountiful.
- Guard Villagers.
- Villager Names.
- Supplementaries.
- KubeJS.
- Open Loader.
- In Control.
- Titles.
- Integrated Villages.
- IDAS.
- Loot Integrations.
- Almost Unified and Polymorph.
- Patchouli.
- FTB Quests.
- FTB Ranks.
- Easy NPC.
- CustomNPCs-Unofficial.
- Human Companions.

Installed but still needs authoring/testing:

- FTB Quests for hidden progression, rank milestones, and structured questing.
- FTB Ranks or a clean rank/title replacement for public rank display.
- Patchouli for the Ascendant Codex.
- Easy NPC for clerks, examiners, merchants, dialogue, and controlled town NPCs.
- CustomNPCs-Unofficial for named rival hunters.
- Human Companions for generic hunters if visually acceptable.

Still delayed:

- MCA Reborn plus MCA - Default Medieval requires a separate village client/server test before it becomes part of the stable Guild layer.
- A structure template/datapack/jigsaw workflow for Guild Outposts, Hunter Boards, and major towns.

Do not treat this pass as validated until the client and dedicated server tests in `docs/GUILD_HUNTER_IMPLEMENTATION_STATUS.md` pass.

## Assets Needed

- Guild banner or crest.
- Small, medium, and large Hunter Board structure designs.
- Rank plaque block designs or textures.
- Medieval/fantasy NPC skins.
- Rival hunter skins.
- Guild currency item texture.
- Patchouli Codex book icon or texture.
- Bounty paper or contract visual assets if needed.
- Town and Guild signage.
- Monster trophy decorations.
- Structure templates for outposts, towns, and Guild Halls.

## Design Data Needed

- Final rank names and descriptions.
- Evaluation requirements per rank.
- List of tracked bosses, mobs, and structures.
- Bounty categories.
- Guild currency name and reward economy.
- NPC roster and dialogue.
- Rival hunter roster and personalities.
- Hunter Board layout standards.
- Village board biome variants.
- Major town structure list.
- Codex entries.
- Relationship and reputation rules for rivals and villages.

## Clean Next Steps

Do these as a connected implementation rundown, not separate phases:

1. Reimport the latest client ZIP and complete the Guild/Hunter client boot test.
2. Materialize the dedicated server from the reimported active client instance and complete the server boot/join test.
3. Build the "Hunter Board - Village Standard" in a creative test world with Bountiful, Supplementaries, banners, lanterns, crates, rank signage, and trophy dressing.
4. Build the upgraded Town Hunter Board and a first Guild Outpost using the same visual language.
5. Use the in-game FTB Quests editor to create the first rank-evaluation chapter, then export/commit the generated files.
6. Author FTB Ranks config after the first boot shows the exact generated config layout.
7. Place prototype NPCs: Guild Clerk, Rank Examiner, Bounty Master, and one rival hunter.
8. Polish the starter Ascendant Codex outline so it references actual boards, ranks, NPCs, and first objectives.
9. Texture the Guild Mark, Hunter Seal, and Ascendant Sigil items.
10. Connect early existing structures to board contracts so players are guided into current modded content instead of wandering blindly.
11. Validate MCA Reborn plus MCA - Default Medieval in a separate test. Keep it installed only if medieval/fantasy skin control and server behavior are clean.

## Core Rules

- Do not turn Ascendant Realms into a town-building pack.
- Do not make rank feel like a fake checklist.
- Do not allow modern-looking NPCs.
- Do not simulate rival hunters across the whole world all the time.
- Do not make every village board identical.
- Do not make players read walls of text before playing.
- Do not add unverified NPC or quest mods directly into the live pack.
- Do not mark the Guild/Hunter pass validated until both client and dedicated server tests pass.
