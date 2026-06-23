# Ascendant Realms Seamless Integration Master Plan

Status: planning blueprint active.

This document is the long-term cohesion plan for turning Ascendant Realms from a large modpack into a world that feels like one authored RPG. The goal is not only "all mods installed." The goal is that villages, mobs, loot, skills, magic, bosses, structures, UI, names, ranks, recipes, and progression all speak the same language.

## North Star

Ascendant Realms should feel like a single giant medieval fantasy RPG mod built around these truths:

- The world is beautiful, full, dangerous, and worth exploring.
- Villages and towns feel inhabited, protected, useful, and threatened.
- NPCs look like they belong to the world and wear gear the player can also find.
- Every major enemy, boss, structure, item, spell, relic, and contract has a place in one shared progression ladder.
- Rarity is not cosmetic only. Rarity should drive loot beams, item borders, tooltips, bounties, boss rewards, skill milestones, and late-game goals.
- Skill growth should be slow but meaningful. Early game should be hard; progression should feel earned; late game should make the player stronger without making the world harmless.
- UI should look like Ascendant Realms, not like five unrelated UI mods stacked together.
- Fixes should preserve content. Remove a mod or feature only after root-cause repair fails or the feature proves unstable.

## Current Foundation

The pack already has the right backbone:

- Packwiz: source of truth for installed mods and exported packs.
- Forge 1.20.1 47.4.20: proof target.
- Open Loader: global datapack and resource-pack delivery.
- KubeJS: recipe, tag, item, tooltip, and light logic glue.
- Almost Unified / Almost Unify Everything / Polymorph: recipe and duplicate material cleanup.
- Item Borders / Legendary Tooltips / KubeJS tooltip script: current rarity presentation layer.
- Puffish Skills and Pufferfish's Attributes: current skill/progression framework.
- Bountiful / FTB Quests / FTB Ranks / Patchouli: contract, quest, rank, and codex tooling.
- CustomNPCs / Easy NPC / Human Companions / MCA Reborn / Guard Villagers: current NPC and settlement tooling.
- In Control / Spawn Balance Utility / Scaling Health / Majrusz's Progressive Difficulty / Improved Mobs: current enemy pressure tooling.
- Integrated Villages / IDAS / Towns and Towers / Structory / Moog structures / YUNG structures / Medieval Buildings / Villages & Pillages: current structure layer.
- Loot Integrations / Artifacts / Cataclysm / IceAndFire CE / Marium / Iron's Spells / Simply Swords: current reward and chase-loot layer.

The missing piece is not "more mods" first. The missing piece is an Ascendant control layer that tells these mods what the pack means.

## Current Custom Worldgen Reality

The pack now has two pack-owned worldgen layers:

- Ascendant Guild: three standalone Guild/Hunter structures for bounty boards, camps, outposts, notice boards, NPC spawn-set testing, and Guild loot.
- Ascendant Atlas: finite-world coordinate runtime, In Control area guardrails, road/bridge policy, debug-only waymark assets, and broader region/climate/settlement/structure/mob/loot/ore/naming contracts.

This is real custom worldgen, but it is intentionally the safe first version. It adds locate-able Open Loader structures and control contracts without pretending datapacks can replace Terralith/Tectonic's biome source. True coordinate-locked radial rings, directional climate sectors, and hard biome/ore placement by map direction require a future Ascendant Atlas Forge helper module or a curated map.

## The Ascendant Control Layer

Everything should be organized around one pack-owned data model. The current files already point in that direction:

- `config/ascendant_index/rarity_schema.json`
- `config/ascendant_index/gear_registry.json`
- `config/ascendant_guild/ranks.json`
- `config/ascendant_guild/rival_hunters.json`
- `config/ascendant_guild/bounty_categories.json`
- `config/ascendant_guild/hunter_boards.json`
- `config/ascendant_guild/npc_roster.json`
- `config/ascendant_guild/npc_loadouts.json`
- `config/ascendant_guild/nameplates.json`
- `config/ascendant_settlements/settlement_unification.json`
- `config/puffish_skills/`
- `config/openloader/data/ascendant_realms_world_integration/`
- `kubejs/client_scripts/ascendant_rarity_tooltips.js`
- `config/itemborders-common.toml`

These should become the canonical Ascendant design database. Mods can still own their own content, but Ascendant Realms owns the interpretation.

## Integration Method Ladder

Use the lightest tool that gives stable control:

1. Config files:
   - Use when a mod already exposes the exact behavior.
   - Examples: spawn weights, health bar visibility, structure spacing, visual options.

2. Datapacks through Open Loader:
   - Use for tags, loot tables, recipes, structure tags, biome tags, advancement triggers, function-based scoreboard fallbacks, and worldgen data overrides.
   - Best for stable vanilla/data-driven logic.

3. KubeJS:
   - Use for recipes, tags, tooltip presentation, item registration, JEI aliases, lightweight events, and pack glue.
   - Best for iteration.
   - Avoid deep runtime systems if the scripting API is fragile or cannot read the needed mod internals.

4. Existing mod APIs:
   - Use FTB Quests, Bountiful, Puffish Skills, CustomNPCs, Easy NPC, In Control, Loot Integrations, and Almost Unified before writing Java.
   - Best when the mod already has a clean external data format.

5. Custom Forge helper mods:
   - Use when the pack needs real runtime control, client overlays, entity labels, custom NPC behavior, progression events, or structure placement hooks that datapacks/KubeJS cannot safely provide.
   - This is likely needed for the final nameplate/HUD/progression integration and possibly advanced settlement injection.

## Custom Mods We Will Probably Need

### 1. Ascendant Core

Purpose: shared Java foundation for any custom systems.

Why we may need it:

- KubeJS is good for glue, but some things need typed runtime access.
- Multiple future modules should not each reinvent registry loading, config parsing, packet sync, or rarity lookup.
- The pack needs one central place to load the Ascendant index and expose it to client/server systems.

Likely responsibilities:

- Load Ascendant registries from JSON:
  - rarity schema
  - gear index
  - spell index
  - armor index
  - shield index
  - accessory/relic index
  - NPC profiles
  - settlement profiles
  - boss/elite definitions
- Sync server-owned data to clients.
- Provide commands for debugging:
  - `/ascendant profile npc`
  - `/ascendant rarity get <item>`
  - `/ascendant rank set <player>`
  - `/ascendant npc apply <profile>`
  - `/ascendant audit nearby`
- Provide safe logging around pack integration errors.

Datapack/KubeJS alternative:

- We can keep using JSON and KubeJS for some of this, but once UI, entity nameplates, level displays, and event-driven progression need to share the same data, a real mod becomes cleaner.

Priority: high.

### 2. Ascendant Nameplates

Purpose: styled, readable, dynamic nameplates for players, NPCs, rival hunters, elite mobs, and bosses.

Why we need it:

- Vanilla scoreboard names are limited.
- CustomNPCs titles are close-range and awkward.
- The current fallback can display text, but it cannot deliver the polished RPG nameplate the pack needs.
- We need names, ranks, levels, roles, guild titles, faction colors, and threat readability to look like one custom UI.

Features:

- Player nameplates:
  - player name
  - Guild rank
  - level
  - optional title from Titles/FTB Ranks
  - party/friendly styling later

- NPC nameplates:
  - `[B-Rank] Rank Examiner`
  - `Lv.52 Examiner`
  - profession icon or color
  - faction styling

- Rival hunter nameplates:
  - name
  - rank
  - level
  - archetype
  - hostile/neutral state

- Enemy nameplates:
  - hidden for passive mobs by default
  - visible when targeted, recently damaged, aggressive, elite, or boss
  - level/threat indicator
  - boss bars remain for true bosses

- Visual style:
  - rank-colored frame accents
  - clean font color hierarchy
  - no giant clutter wall over passive entities
  - config to hide/show layers

Integration points:

- Scaling Health / Majrusz / Improved Mobs for enemy danger.
- FTB Ranks / scoreboard for player rank.
- Ascendant Core data for rank colors and level formatting.
- CustomNPCs/Easy NPC/MCA for authored NPC profiles.

Priority: very high.

### 3. Ascendant Progression HUD

Purpose: custom HUD elements for skill XP, level-up popups, rank progression, and milestone feedback.

Why we need it:

- The user specifically wants a second XP bar tied to the custom skill tree.
- Existing HUD mods may style the HUD, but they likely cannot read Puffish Skills internals cleanly.
- Level-up feedback should feel like Ascendant Realms, not a vanilla toast.

Features:

- Skill XP bar:
  - separate from vanilla XP
  - visible when XP changes or when the player holds a hotkey
  - shows current Ascendant level and progress
  - styled to match the main menu/title/tooltip language

- Level-up popup:
  - "Level Up! 45"
  - rank color accents
  - short reward summary if known

- Rank milestone popup:
  - "C-Rank Trial Available"
  - "B-Rank Contract Board Unlocked"

- Skill point popup:
  - "+1 Skill Point"
  - possible rare bonus points at milestone levels

Integration points:

- Puffish Skills level/XP/points if accessible.
- FTB Quests for milestone unlocks.
- Bountiful for contract tier unlocks.
- Ascendant Core as the data bridge.

Priority: very high if existing HUD tools cannot read Puffish Skills.

### 4. Ascendant NPC Runtime

Purpose: make important NPCs, rival hunters, clerks, examiners, guards, and guild staff feel authored and alive.

Why we need it:

- CustomNPCs is powerful but stores script copies per entity, which makes source updates awkward.
- Easy NPC is useful but may not handle every dynamic profile/gear/nameplate requirement.
- MCA Reborn handles villagers, but special Guild NPCs need custom control.

Features:

- Apply profiles to NPCs from JSON:
  - name
  - rank
  - level
  - role
  - equipment
  - dialogue group
  - faction
  - behavior

- Equipment rules:
  - all important NPC equipment must be real player-obtainable gear.
  - loadouts scale by role and rank.
  - rivals use real world weapons, shields, armor, relics, or spellbooks.
  - guild clerks and examiners use clothing/armor that visually fits but does not look combat-heavy unless intended.

- Interaction hooks:
  - Rank Examiner opens rank trial info.
  - Guild Clerk explains contracts and codex.
  - Bounty Master points to Bountiful/FTB quest paths.
  - Quartermaster points to food, tools, backpacks, and early supplies.
  - Guard Captain gives settlement threat context.

- Maintenance:
  - no embedded stale scripts.
  - profile updates should apply through commands or data reload.
  - existing NPCs can be audited and repaired.

Priority: high.

### 5. Ascendant Settlement Engine

Purpose: make villages, towns, guild halls, boards, guards, MCA families, and integrated structures feel like one civilization layer.

Why we may need it:

- Datapack pool injection can add structures, but controlling many third-party village pools safely is delicate.
- The pack already had village crashes from processor/POI paths.
- We need Hunter Boards, Guild Outposts, Rank Halls, training yards, kitchens, markets, guard posts, and notice boards to appear naturally.

Initial approach:

- Start with standalone structures:
  - Hunter Board - Village Standard
  - Town Guild Board
  - Guild Outpost
  - Rank Hall
  - roadside Hunter Camp
  - rival campsite

- Prove each structure with `/locate`.
- Use vanilla template pools only after standalone structures are stable.
- Inject into villages only after testing specific target pools.

Potential custom mod responsibilities:

- Choose settlement additions based on village type, biome, and existing nearby structures.
- Avoid placing boards in broken locations.
- Spawn one correct NPC set per generated board.
- Mark claimed settlement data to prevent duplicate boards.
- Add safe POI/job-site handling instead of relying on fragile third-party processors.

Priority: medium-high.

### 6. Ascendant Loot And Rarity Engine

Purpose: make every weapon, armor piece, shield, spell, relic, artifact, boss drop, bounty reward, and rare material use one consistent rarity system.

Why we may need it:

- Item Borders can color frames.
- KubeJS can add tooltip labels.
- But deeper consistency needs loot, shops, bounties, boss rewards, and skill unlocks to all read the same registry.

Features:

- One registry for:
  - weapons
  - armor
  - shields
  - spells
  - accessories/relics
  - boss drops
  - dragon materials
  - rare crafting materials

- Rarity drives:
  - Item Borders color
  - tooltip label
  - Loot Beams visibility
  - Bountiful reward tier
  - dungeon chest tier
  - boss drop expectation
  - NPC equipment rank
  - skill tree milestone requirements
  - Patchouli codex entries

- Rules:
  - Legendary and higher can be bold.
  - Mythic and Ascendant need stronger visual identity.
  - Rarity label must appear under native item stats and before behavior text.
  - Backend reason/index text stays hidden from players.

Datapack/KubeJS path:

- Current approach is acceptable for tooltip/frame generation.
- Loot table integration can start through Open Loader and Loot Integrations.

Custom mod threshold:

- If live item rarity needs to affect runtime behavior, player drops, random rolls, or UI animations beyond KubeJS limits, move to Ascendant Core.

Priority: high.

### 7. Ascendant Encounter Director

Purpose: connect enemy spawns, danger zones, structures, moons/weather, bosses, and progression into one difficulty ecology.

Why we may need it:

- In Control, Spawn Balance Utility, Scaling Health, Majrusz, and Improved Mobs are strong, but cross-system conditions can get complex.
- We need early game hard, midgame rewarding, late game still dangerous.
- We need mobs from all packs to appear where they make sense.

Features:

- Mob category registry:
  - passive ambient
  - livestock/wildlife
  - common hostile
  - dangerous hostile
  - elite
  - miniboss
  - boss
  - dragon-tier
  - event-only
  - structure-only

- Spawn rules by:
  - biome
  - structure proximity
  - dimension
  - moon/event state
  - distance from spawn
  - player level/rank later
  - local settlement safety

- Integration examples:
  - Born in Chaos mobs increase around ruins, graveyards, and night pressure.
  - Aquamirae threats stay ice/ocean/deep cold themed.
  - Mowzie's Mobs keep rare encounter identity.
  - Alex's Mobs enrich biomes but do not drown out hostile progression.
  - IceAndFire dragon-tier content is rare, dangerous, and not spawn-camp adjacent.
  - Cataclysm/Marium boss-tier content supports late-game bounties and skill unlocks.

Implementation path:

- Start with config and In Control rules.
- Use datapack biome/entity tags.
- Add KubeJS/commands only for milestone events if stable.
- Build custom director only if we need player-rank-aware dynamic spawns.

Priority: high.

## Feature Integration Map

### Villages And Towns

Goal:

Villages should feel like small living settlements in a dangerous RPG world, not decorative structures.

Systems involved:

- Integrated Villages
- Towns and Towers
- Villages & Pillages
- Guard Villagers
- Villager Names
- MCA Reborn
- Bountiful
- FTB Quests
- Patchouli
- Farmer's Delight
- Create
- Supplementaries
- Every Compat
- Macaw's blocks
- Handcrafted
- Decorative Blocks
- CustomNPCs / Easy NPC

Target experience:

- The player finds villages more often.
- Villages have named villagers and guards.
- Some villages have Hunter Boards.
- Bigger towns have Guild staff.
- Food, kitchens, workshops, and guard posts use the pack's actual block palette.
- Villages can ask for modded mob parts, food, materials, boss trophies, and rare items.
- Structures should imply the world understands its own mods.

Concrete integration work:

- Create a settlement role table:
  - farm village
  - trade town
  - frontier camp
  - guild outpost
  - coastal harbor
  - mountain hold
  - magic enclave
  - dragon-scarred ruin

- Build structure templates:
  - Hunter Board kiosk
  - Guild clerk desk
  - Rank Examiner platform
  - training yard
  - guard barracks
  - bounty hall
  - tavern rumor corner
  - small Create workshop
  - Farmer's Delight kitchen
  - apothecary/arcanist desk

- Tie settlement types to contracts:
  - frontier villages: hostile mob contracts
  - towns: delivery, artifact recovery, miniboss rumors
  - coastal settlements: Aquamirae/ship contracts
  - cold settlements: ice/ocean danger
  - dragon-scarred regions: dragon warnings and late-game bounties

- Use real gear on NPCs:
  - guards use obtainable shields/armor
  - rank examiners use formal high-rank gear
  - hunters use rank-matched weapons
  - arcanists use Iron's Spells themed gear

Risk:

- Too much village-pool injection can reintroduce generation crashes.

Plan:

- Build standalone structures first.
- Audit templates and processors.
- Inject into village pools later with exact target pools and rollback files.

### NPCs And Heroes

Goal:

Important NPCs should be memorable, ranked, styled, and mechanically connected.

Systems involved:

- CustomNPCs
- Easy NPC
- Human Companions
- MCA Reborn
- FTB Quests
- FTB Ranks
- Patchouli
- Ascendant Nameplates
- Ascendant NPC Runtime

NPC classes:

- Guild Clerk:
  - teaches basics
  - points to Codex
  - explains ranks/contracts

- Rank Examiner:
  - gives rank trial info
  - displays B-Rank or higher authority
  - should not be `[Unranked]`

- Bounty Master:
  - points to Bountiful boards and FTB quest chapters

- Quartermaster:
  - sells or explains supplies later

- Guard Captain:
  - explains local threats
  - protects town

- Rival Hunters:
  - appear as named competitors
  - use real gear
  - can be neutral, hostile, or quest-related

- Village Elder:
  - local context and rumors

Needed custom behavior:

- Profile-based NPC setup.
- Dynamic rank/level/nameplate.
- Equipment from the gear registry.
- Faction and hostility rules.
- Audit and repair commands.

Short-term:

- Continue using CustomNPCs/Easy NPC with the audit tools.

Long-term:

- Move important profile handling into Ascendant NPC Runtime so scripted entity copies stop being a maintenance trap.

### Skills And Progression

Goal:

The Ascendant Web should make players feel increasingly capable while preserving danger.

Systems involved:

- Puffish Skills
- Pufferfish's Attributes
- Better Combat
- Combat Roll
- Simply Swords
- Iron's Spells
- Create
- Farmer's Delight
- Bountiful
- Cataclysm
- Marium
- IceAndFire CE
- Scaling Health
- Majrusz

Branch identity:

- Warrior:
  - melee control
  - shields
  - armor
  - stagger/knockback resistance
  - boss survival

- Rogue:
  - mobility
  - crit windows
  - roll cooldown
  - light weapons
  - bounty mobility

- Ranger:
  - tracking
  - hostile awareness
  - projectile utility
  - monster part rewards
  - wildlife/biome knowledge

- Arcanist:
  - Iron's Spells milestones
  - mana or spell cooldown support if accessible
  - scroll/spellbook progression
  - rare spell discovery

- Engineer:
  - Create milestones
  - Slice & Dice/Farmer's Delight support
  - artillery/automation identity later

- Survivalist:
  - food, seasons, snow, travel, weather
  - backpack/supply utility
  - village survival support

- Dragonbound:
  - dragon materials
  - Cataclysm/Marium/IceAndFire milestones
  - late-game resistance and trophies

Needed improvements:

- More unique nodes per branch.
- Fewer generic heart/damage nodes.
- Milestone locks tied to actual pack actions.
- Skill XP bar and level-up popups.
- Cleaner visual web and better icons.

Implementation:

- Keep Puffish Skills config as the source for now.
- Generate better positions/icons/text from script.
- Use FTB Quests or advancements for milestone proof.
- Build Ascendant Progression HUD if HUD mods cannot read the skill track.

### Loot, Rarity, And Rewards

Goal:

Every important reward should tell the player where it sits in the world.

Systems involved:

- Item Borders
- Legendary Tooltips
- Loot Beams
- KubeJS tooltip script
- Loot Integrations
- Bountiful
- Artifacts
- Curios
- Simply Swords
- Iron's Spells
- Cataclysm
- Marium
- IceAndFire CE
- Farmer's Delight
- Create

Rules:

- Common to Epic: readable, not too loud.
- Legendary: bold, gold, boss-signature.
- Mythic: bold, high-energy, very rare.
- Ascendant: bold, glowing/capstone direction, pack-defining.
- Loot beams should highlight high-value drops only.
- Item borders should match assigned rarity, not item display-name color.
- Tooltip rarity should be directly under native stats.
- Backend notes stay hidden.

Integration:

- Dungeon chest loot should include:
  - early useful gear
  - rare spell scrolls
  - artifacts
  - bounty materials
  - food/supplies
  - structure-appropriate trophies

- Boss loot should include:
  - unique gear
  - materials for capstone crafting
  - skill milestone proof
  - bounty/rank progression proof

- Village rewards should include:
  - food
  - supplies
  - moderate gear
  - local contracts
  - not endgame loot

Needed custom work:

- Generate loot tables from the rarity registry.
- Generate Bountiful reward pools from the same registry.
- Generate Patchouli/JEI documentation from the same registry.

### Mobs, Bosses, And Threat

Goal:

The world should be hard at the start, but the player should feel long-term growth while still respecting elite threats.

Systems involved:

- Alex's Mobs
- Mowzie's Mobs
- Born in Chaos
- Aquamirae
- Bosses'Rise
- Cataclysm
- Marium
- IceAndFire CE
- Enhanced Celestials
- Weather2
- Scaling Health
- Majrusz
- Improved Mobs
- Spawn Balance Utility
- In Control
- YDM's MobHealthBar
- Enhanced Boss Bars

Threat tiers:

- Tier 0: passive/ambient.
- Tier 1: normal hostile.
- Tier 2: dangerous hostile.
- Tier 3: elite/rare hostile.
- Tier 4: miniboss.
- Tier 5: boss.
- Tier 6: dragon-tier/world event.

Integration:

- Each mob should have:
  - spawn biome/dimension logic
  - rarity/threat tier
  - bounty eligibility
  - loot relevance
  - skill branch relevance
  - structure/event relevance if any

Examples:

- Born in Chaos:
  - night, ruins, graveyard, blood moon pressure.
  - bounty material source.

- Aquamirae:
  - cold/ocean danger.
  - coastal contracts.

- Mowzie's:
  - rare biome encounters.
  - elite contracts.

- Cataclysm:
  - boss structures and late-game progression.
  - Mythic/Ascendant rewards.

- IceAndFire CE:
  - dragon-tier danger.
  - Dragonbound milestones.

Needed custom work:

- Possibly Ascendant Encounter Director if config-only rules cannot handle rank-aware progression.

### Magic

Goal:

Magic should not be a separate toy box. It should be part of progression, loot, bosses, NPCs, skills, and world identity.

Systems involved:

- Iron's Spells
- Iron's Lib
- Obscure API where needed
- Cataclysm/Marium/IceAndFire reward ladders
- Arcanist skill branch
- Guild Arcanist NPC
- Patchouli Codex
- JEI aliases

Integration:

- Spell scrolls and spellbooks appear in:
  - magic structures
  - dungeon loot
  - arcanist shops/quests later
  - boss drops where thematic

- Arcanist branch should support:
  - spell discovery
  - spell cooldown or mana if accessible
  - spellbook progression
  - magic resistance
  - rare scroll identification

- Guild Arcanist should:
  - explain scroll vs spellbook behavior
  - point players to magic loot sources
  - teach why some spells cannot be cast from scrolls

Needed custom work:

- If Iron's Spells internals are not accessible through datapack/KubeJS, Ascendant Core can listen for spell-related events only if the mod exposes safe hooks.

### Create, Food, And Craft Economy

Goal:

Engineering, food, villages, and survival should support the RPG loop.

Systems involved:

- Create
- Create Slice & Dice
- Create Big Cannons
- Farmer's Delight
- Alex's Delight
- Supplementaries
- Every Compat
- Almost Unified
- Polymorph
- Macaw's / Handcrafted / Decorative Blocks

Integration:

- Villages should visibly use:
  - kitchens
  - storage
  - workshops
  - Create shafts/cogs where appropriate
  - Farmer's Delight food blocks

- Engineer branch should reward:
  - automation milestones
  - kitchen automation
  - safer travel/logistics
  - artillery knowledge later

- Food should matter:
  - early survival support
  - bounty rewards
  - travel prep
  - village identity

Needed custom work:

- KubeJS recipe/tag pass first.
- Almost Unified material cleanup.
- Custom mod not needed unless progression needs runtime machine detection.

### UI And Presentation

Goal:

The interface should feel branded and fantasy-RPG polished.

Systems involved:

- FancyMenu
- Immersive UI
- Legendary Tooltips
- Item Borders
- Stylish Effects
- SpiffyHUD
- Drippy Loading Screen
- Overflowing Bars
- AppleSkin
- YDM's MobHealthBar
- Enhanced Boss Bars
- Traveler's Titles

Current state:

- Main menu title asset is staged.
- Item rarity frames and tooltip labels exist.
- Health bars need strict visibility control.
- Enemy numeric levels are not solved yet.
- Skill XP HUD is not solved yet.
- Player/NPC nameplates need a proper overlay.

Needed custom work:

- Ascendant Nameplates.
- Ascendant Progression HUD.
- Possibly an Ascendant UI resource pack for consistent frame assets.

Style rules:

- Rarity and rank colors must be consistent.
- Do not expose backend index/debug text to players.
- Tooltips need flavor plus exact math where custom content is authored.
- UI should be readable before it is flashy.

### Worldgen And Structures

Goal:

The world should be full, but not messy.

Systems involved:

- Terralith
- Tectonic
- Serene Seasons
- Towns and Towers
- Structory
- YUNG structures
- Moog structures
- Integrated Villages
- IDAS
- Medieval Buildings
- Create: Structures Arise
- IceAndFire CE / Cataclysm structure content

Integration:

- Structure density should support exploration every session.
- Villages/towns should feel common enough for multiplayer survival.
- Boss structures should remain special.
- Dragon-tier content should not destroy early progression.
- Loot must match structure danger.
- Hunter Boards/Guild Outposts must become recurring anchors.

Risk:

- Processor/template crashes.
- Too many structures close together.
- Overlapping village mods creating ugly settlements.
- Performance spikes during exploration.

Plan:

- Keep auditing actual jar data.
- Keep root-cause data repairs in Open Loader.
- Add structures carefully through standalone tests.
- Use custom settlement placement only when injection needs runtime safety.

## Global Data Contracts

### Rarity Contract

Every meaningful item, spell, relic, boss drop, and special material should have:

- item id
- display name
- source mod
- category
- rarity
- color
- power reason
- acquisition source
- loot tier
- bounty tier
- NPC equipment eligibility
- skill milestone relevance

### Mob Contract

Every meaningful mob should have:

- entity id
- source mod
- threat tier
- biome/dimension spawn role
- bounty eligibility
- drop relevance
- skill branch relevance
- structure/event relation
- early/mid/late progression status

### Structure Contract

Every meaningful structure should have:

- structure id
- source mod
- biome/dimension role
- density target
- danger tier
- loot tier
- bounty relevance
- NPC/settlement relevance
- crash repair notes

### NPC Contract

Every authored NPC should have:

- profile id
- name
- rank
- level
- role/profession
- faction
- equipment loadout
- dialogue role
- quest/contract hook
- nameplate style
- spawn/placement rule

### Skill Contract

Every skill node should have:

- node id
- branch
- tier
- cost
- prerequisite logic
- flavor line
- exact effect line
- linked mods/systems
- milestone requirement if any
- test method

## Master Roadmap

### Phase 1: Stabilize The Existing Authored Systems

Goal: remove the current rough edges without adding big new content.

Tasks:

- Apply the saved CustomNPC repair after Minecraft closes.
- Retest Rank Examiner and at least one new NPC profile.
- Finish the CustomNPC/Easy NPC profile workflow.
- Confirm MCA medieval clothes are loading.
- Confirm the player identity fallback loads without command errors.
- Confirm rarity tooltips and borders still behave after latest changes.
- Confirm Integrated Villages repaired structures do not crash across known seeds.

Exit criteria:

- No startup script errors.
- No stale Rank Examiner.
- No village crash in the known repaired seeds.
- NPC profile creation and repair workflow is documented and repeatable.

### Phase 2: Build The Universal Registries

Goal: every important content type has a pack-owned classification.

Tasks:

- Finish weapon index.
- Finish armor index.
- Finish shield index.
- Finish spell/magic index.
- Finish accessory/relic index.
- Add mob threat index.
- Add structure/dungeon/village index.
- Add NPC role/loadout index.
- Add bounty reward index.
- Add boss/dragon milestone index.

Exit criteria:

- A player-facing item should never look unclassified.
- A developer-facing registry should explain why each important thing has its tier.
- Every new system can read the same labels.

Current automated registry status:

- `scripts/generate-ascendant-content-registries.ps1` scans the active client jars and generates first-pass mob, structure, bounty target, skill-hook, and implementation-matrix registries.
- `config/ascendant_index/mob_registry.json` currently owns generated entity threat tiers.
- `config/ascendant_index/structure_registry.json` currently owns generated structure classes, loot tiers, hooks, and density review flags.
- `config/ascendant_guild/generated_bounty_targets.json` currently owns generated Hunter Board target candidates.
- These generated files are planning and authoring data until their individual entries are validated in-game or wired through Bountiful, FTB Quests, Puffish Skills, In Control, or a custom helper mod.

### Phase 3: Settlement And Guild Prototype

Goal: make villages matter through one handcrafted prototype loop.

Build:

- Hunter Board - Village Standard.
- One Guild Clerk.
- One Rank Examiner.
- One Bounty Master.
- One Guard Captain.
- One rival hunter.
- One Patchouli Codex starter chapter.
- One FTB Quest chapter.
- One Bountiful contract tier.

Test:

- Spawn/locate the structure.
- Interact with NPCs.
- Pick up a contract.
- Kill target mobs.
- Receive reward.
- See rarity UI.
- See skill/progression feedback.

Exit criteria:

- The loop feels like one designed system, even if content volume is still small.

### Phase 4: Custom UI Bridge

Goal: solve nameplates, levels, and skill XP properly.

Build if needed:

- Ascendant Core.
- Ascendant Nameplates.
- Ascendant Progression HUD.

Test:

- Player nameplate shows rank and level.
- NPC nameplate shows rank, name, level, role.
- Hostile mobs show threat only when relevant.
- Skill XP bar appears and progresses.
- Level-up popup looks styled.
- Server/client sync works in multiplayer.

Exit criteria:

- No more hardcoded-looking nameplates.
- No need to rely on vanilla below-name fallback for final presentation.

### Phase 5: Loot And Bounty Integration

Goal: make danger pay off.

Tasks:

- Generate tiered loot pools.
- Connect Bountiful contracts to modded mobs/materials.
- Connect boss drops to rank trials.
- Connect rare structures to spell/artifact loot.
- Connect dragon-tier rewards to Dragonbound.
- Connect village board rewards to food/supplies/early gear.

Exit criteria:

- Dangerous structures and mobs feel worth engaging.
- Rewards do not skip progression tiers.
- Bounties teach players what matters in the world.

### Phase 6: Spawn Ecology And Difficulty Tuning

Goal: hard start, meaningful growth, persistent danger.

Tasks:

- Build mob threat index.
- Tune common hostile density.
- Tune elite rarity.
- Tune dragon/boss distance and biome rules.
- Tune blood moon/event danger.
- Tune settlement safety.
- Tune Scaling Health and skill XP together.

Exit criteria:

- Early game is scary but playable.
- Midgame feels stronger.
- Late game still has enemies that can kill players.
- Villages are not instantly wiped out.

### Phase 7: Settlement Expansion

Goal: the world feels full of civilization.

Tasks:

- Add more Hunter Board variants.
- Add guild outposts.
- Add town halls or rank halls.
- Add rival camps.
- Add arcanist towers or desks.
- Add guarded road/travel points.
- Add settlement-specific bounty themes.

Exit criteria:

- Players regularly find reasons to stop in towns.
- Villages are not bland shells.
- NPCs and boards appear in believable places.

### Phase 8: Final Cohesion Polish

Goal: everything feels authored.

Tasks:

- Finish tooltip language.
- Finish codex pages.
- Finish UI styling.
- Finish main menu/loading screen.
- Finish resource pack order.
- Fix lingering log noise.
- Performance profile long exploration.
- Multiplayer test with fresh server.

Exit criteria:

- A new player can understand the pack by playing.
- The pack feels coherent instead of assembled.

## What Not To Do Yet

- Do not add more major worldgen packs to solve emptiness until current density and settlement authoring are tuned.
- Do not add another skill/class framework unless Puffish Skills cannot support required progression.
- Do not run both KubeJS and CraftTweaker unless KubeJS clearly cannot solve a specific recipe/data problem.
- Do not add another HUD/nameplate mod randomly if a small custom overlay is the cleaner solution.
- Do not remove Integrated Villages, CustomNPCs, or UI systems just because one crash or stale file happens. Root-cause repair first.
- Do not make bounties purely playtime-based. Progression should come from action, danger, exploration, rank trials, and milestones.

## Testing Strategy

Automated tests should cover what can be verified without Jayden:

- Pack metadata validation.
- Packwiz refresh.
- Client export.
- Server staging export.
- Gear index generation.
- Rarity tooltip generation.
- Item border generation.
- CustomNPC script unit tests.
- CustomNPC saved-world audit/repair when Minecraft is closed.
- World integration audit.
- JSON schema checks for registries.
- Datapack syntax checks where practical.

Manual tests should be reserved for what genuinely needs a player:

- Visual nameplate quality.
- HUD readability.
- Structure feel.
- Village life feel.
- Combat difficulty feel.
- Loot reward satisfaction.
- Multiplayer stability.

## Immediate Next Actions

1. Close Minecraft and apply the CustomNPC saved-world repair.
2. Retest the Rank Examiner label.
3. Build the first Hunter Board / Guild Clerk / Rank Examiner prototype loop.
4. Add mob and structure indexes beside the existing gear indexes.
5. Decide whether Ascendant Core and Ascendant Nameplates should start now or after one more CustomNPC/Easy NPC prototype test.
6. Keep all future fixes documented under the root-cause policy.

## Definition Of Seamless

A feature is seamless only when:

- It has a place in the rarity/progression language.
- It appears in the world where it makes sense.
- It rewards or threatens the player at the right tier.
- NPCs, bounties, skills, loot, and UI know how to refer to it.
- It does not require the player to understand which mod added it.
- It can be tested and repaired without ripping out unrelated systems.

That is the standard for Ascendant Realms.
