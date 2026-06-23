# Custom Integration Plan

For the full feature-unification roadmap, use `docs/ASCENDANT_REALMS_SEAMLESS_INTEGRATION_MASTER_PLAN.md`. For the new active source-of-truth layer, use `docs/ASCENDANT_CORE_INTEGRATION.md` and `config/ascendant_core/`. This file remains the tactical integration plan for current KubeJS, Open Loader, Puffish Skills, and Guild/Hunter glue.

The first custom integration file set is now active as the unified Ascendant Web skill-tree config:

```text
config/puffish_skills/
```

It uses Pufferfish's Skills and Pufferfish's Attributes as the framework and replaces Default Skill Trees as the intended progression layer. Matching fallback/source copies remain in `datapacks/ascendant_realms_skills/` and `openloader/data/ascendant_realms_skills/`; the active load path remains `config/puffish_skills/`.

## Active Batch N Tools

- KubeJS: installed for recipes, tags, and pack glue. Recipe/tag/loot scripts remain cautious scaffolds; the Ascendant progression HUD bridge and Ascendant Core manifest loader are active.
- Open Loader: installed for global datapack/resource-pack loading, starting with the Ascendant Realms skill datapack copy.
- Open Loader also carries `ascendant_realms_world_integration`, which repairs Integrated Villages' shared workstation/POI processor path and extends a small number of Mowzie's Mobs biome tags.
- Almost Unified, Almost Unify Everything, and Polymorph: installed for recipe/material cleanup and conflict fallback.
- Every Compat, Create Slice & Dice, Alex's Delight, Integrated Villages, and IDAS: installed as Batch N cohesion bridges.
- CraftTweaker: delayed unless KubeJS is not suitable.
- Datapacks: preferred for loot tables, tags, worldgen spacing, and vanilla-compatible rules.
- Loot Integrations: useful if RPG loot needs to appear inside dungeon/structure loot.
- In Control: useful for spawn rules and difficulty gating.
- Ascendant Core: active data-first contract layer under `config/ascendant_core/`, with a KubeJS loader that verifies linked registries and creates shared scoreboards.

## Integration Goals

- Dungeon loot includes appropriate RPG weapons, spellbooks, artifacts, coins, and rare materials.
- Structures do not spam.
- Boss loot is meaningful but not overpowered.
- Mobs scale by biome, distance, dimension, or progression where possible.
- Seasons, biomes, structures, and mobs feel coherent.
- Visual resource packs are properly ordered.
- Duplicate systems do not fight each other.

## Current Full-Stack Audit

`scripts/audit-world-integration.ps1` generated `docs/WORLD_INTEGRATION_AUDIT.md` from the active CurseForge instance.

The audit confirms the current stack already has broad integration surface:

- Structures and structure sets for villages, towers, dungeons, boss locations, and landmarks.
- Biome tags and biome modifiers for mob/worldgen placement.
- Loot tables for dungeon, boss, artifact, spell, and structure rewards.
- Recipes and item/entity tags for later KubeJS/Almost Unified cleanup.

Use this audit before adding more mods. If something feels missing in-game, first check whether it is installed but not spawning, installed but too rare, or present only in a dimension/biome that has not been tested yet.

## Initial Custom Rules To Plan

- `config/ascendant_core/mob_ecology.json` should drive the first reviewed In Control draft.
- `config/ascendant_core/structure_ecology.json` should drive structure density and loot-tier review.
- `config/ascendant_core/loot_rarity_rules.json` should drive Bountiful reward and loot-table generation.
- `config/ascendant_core/progression_hooks.json` should drive FTB Quest rank trials and branch milestone hooks.
- Restrict top-tier Simply Swords and spellbooks from early chests.
- Gate dragon spawns away from spawn/villages if Ice and Fire is added.
- Tune Enhanced Celestials events so blood moons are dangerous but not server-wiping.
- Make Bountiful rewards match progression tiers.
- Tune structure spacing if Towns and Towers, YUNG, Structory, and Moog's structures are combined.

## Active Skill Tree Hooks

The current skill tree implements one category, generated node positions, connection web, cost pacing, experience, and direct attribute reward data. It does not yet implement deeper cross-mod hooks.

Future hook candidates:

- Bountiful contracts rewarding skill XP or points.
- Boss kills granting progression.
- Dragon kills unlocking Dragonbound nodes.
- Create milestones unlocking Engineer nodes.
- Iron's Spells milestones supporting Arcanist nodes.
- Cataclysm/Marium boss achievements unlocking endgame nodes.
- Farmer's Delight cooking supporting Survivalist.
- Loot Integrations adding skill-relevant rewards.

Use `docs/SKILL_TREE_INTEGRATION_HOOKS.md` as the detailed backlog.

## Universal Index Pass

`scripts/generate-universal-mod-index.js` now generates:

- `docs/UNIVERSAL_MOD_INDEX.md`
- `docs/UNIVERSAL_RARITY_AND_INTEGRATION.md`
- `config/ascendant_index/rarity_schema.json`
- `config/ascendant_core/`

Use those files as the shared map for the next integration work:

- Which mods need rarity tiers.
- Which mobs need spawn/ecology tiers.
- Which structures need density, biome, loot, or bounty hooks.
- Which items need tooltip/loot rarity alignment.
- Which skills should connect to actual combat, magic, Create, food, bounty, dragon, or boss milestones.

## Guild/Hunter Spine

Use `docs/GUILD_HUNTER_SYSTEM_RUNDOWN.md` as the master social/RPG integration direction. It defines the Guild rank ladder, Hunter Board visual/function standard, rival hunter illusion system, village/town social roles, Codex needs, missing tool candidates, assets, and clean next steps.

Installed first-pass tools:

- Patchouli for the Ascendant Codex.
- FTB Quests for future rank milestones and Guild quest chapters.
- FTB Ranks for future public rank/display experiments.
- Easy NPC for clerks, examiners, merchants, and social NPCs.
- CustomNPCs-Unofficial for named rivals and special NPC prototypes.
- Human Companions for generic hunter/companion tests.

Generated scaffolds:

- `config/ascendant_guild/` keeps the current Guild design data.
- `config/openloader/data/ascendant_realms_codex/` keeps the active starter Codex.
- `kubejs/startup_scripts/ascendant_guild_items.js` creates starter Guild currency concept items.

Installed but still validation-gated:

- MCA Reborn with MCA - Default Medieval.

Still delayed:

- Real FTB quest chapters and rank configs.
- Placed NPCs, dialogue, Hunter Board structure templates, and final Codex content.

Do not treat this as validated until the Guild/Hunter tests pass in `docs/GUILD_HUNTER_IMPLEMENTATION_STATUS.md`.
