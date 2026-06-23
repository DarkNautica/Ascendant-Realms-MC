# Ascendant Core Integration

Status: active data-first integration layer.

Ascendant Core is now the pack-owned control layer for cohesion. It does not replace Packwiz, KubeJS, Open Loader, Puffish Skills, Bountiful, In Control, or the generated indexes. It tells those systems what Ascendant Realms means.

## What Was Added

- `config/ascendant_core/core_manifest.json` is the top-level manifest.
- `config/ascendant_core/rank_progression.json` defines rank order, level bands, contract access, and scoreboard ownership.
- `config/ascendant_core/world_regions.json` defines Hearthlands, Green Frontier, Frozen Reaches, Scorched South, Deep Wilds, Dragon Scars, Nether Front, and End Expanse as authored progression zones.
- `config/ascendant_core/mob_ecology.json` defines mob roles from passive wildlife through dragon-tier threats.
- `config/ascendant_core/structure_ecology.json` defines villages, Guild anchors, landmarks, minor dungeons, major dungeons, and boss/dragon sites.
- `config/ascendant_core/loot_rarity_rules.json` keeps rarity display and reward rules tied to the generated gear registry.
- `config/ascendant_core/npc_role_contracts.json` defines the NPC profile/equipment/nameplate contract.
- `config/ascendant_core/material_unification.json` defines the Almost Unified, Polymorph, Every Compat, KubeJS recipe, and KubeJS tag boundaries.
- `config/ascendant_core/progression_hooks.json` links the Ascendant Web, Guild ranks, bounties, bosses, dragons, Create, food, magic, and survival hooks.
- `config/ascendant_core/runtime_rules.json` defines the first live runtime rules for region tier mirroring, Guild reputation rewards, proof counters, and automatic rank promotion thresholds.
- `config/ascendant_core/live_spawn_policy.json` records the first active cap-only In Control settlement-safety pass.
- `config/ascendant_core/custom_module_plan.json` records when a custom Forge helper mod becomes justified.
- The exact Ascendant Core policy files from the unification brief now exist: `materials.json`, `ore_generation.json`, `recipe_policy.json`, `loot_policy.json`, `mob_policy.json`, `progression_tiers.json`, `dimension_policy.json`, `structure_rewards.json`, `vendor_policy.json`, and `unification_policy.json`.
- `config/ascendant_atlas/` now owns the broader Atlas contracts for regions, difficulty rings, climate sectors, biome assignments, settlement rules, structure distribution, mob distribution, loot distribution, ore distribution, and naming pools.
- `config/openloader/data/ascendant_realms_atlas/` keeps debug Atlas waymark assets, adds `/function ascendant_atlas:status`, and overrides the Overworld biome source through the local `ascendant_atlas_regions` helper mod.
- `kubejs/server_scripts/ascendant_core_integration.js` safely loads the manifest/runtime rules, creates shared scoreboard objectives, mirrors region tier, promotes rank from proof counters, and awards conservative reputation/proof counters from player kills.
- `config/openloader/data/ascendant_realms_core/` adds `/function ascendant_core:status` plus debug proof helpers for in-game validation.

Hotfix note: the KubeJS runtime blocks direct `java.nio.file.Files`, `java.nio.file.Paths`, and `java.io.File` access, and Rhino treated direct `Path.resolve(String)` as ambiguous. The core and progression bridges must use KubeJS `JsonIO` plus the allowed `KubeJSPaths.CONFIG` handle for config reads or they will fail before any scoreboards/HUD data can load.

## Runtime State

Live now:

- Core manifest loader.
- Linked-file existence checks.
- Shared scoreboard objectives:
  - `ar_guild_rep`
  - `ar_guild_rank`
  - `ar_bounties_done`
  - `ar_structures_done`
  - `ar_bosses_done`
  - `ar_dragons_done`
  - `ar_region_tier`
  - `ar_threat_tier`
  - `ar_hunt_kills`
  - `ar_elite_kills`
  - `ar_core_state`
- `ar_region_tier` updates from dimension and rough distance bands.
- Player kills now add small Guild reputation/proof counters when the killed entity maps to a known hostile/modded threat group.
- Boss and dragon-tier kills add boss/dragon proof counters and trigger a small proof popup.
- Guild rank now auto-promotes from the runtime rules when the player meets the required reputation/proof scoreboards.
- `/function ascendant_core:status` displays the current core counters for the player.
- The existing custom XP HUD still reads Puffish Skills directly and mirrors level data to `ar_skill_level`.
- The rarity display layer still uses Item Borders, Legendary Tooltips, and KubeJS tooltips.
- Bountiful Guild boards now use expanded generated pools from the mob registry: 79 village targets, 23 town targets, and 51 major targets after friendly/tooling namespace filtering and the known-invalid Black Frost objective filter.
- `config/incontrol/spawn.json` now has active cap-only pressure tuning for the major mob/boss namespaces that were overwhelming villages in the latest live log.

Contract active, not yet fully enforced:

- Biome-aware and structure-aware region rules.
- Full In Control mob ecology generation.
- Full structure loot-table rewrite.
- Automatic NPC settlement population.
- Polished animated nameplates.

This distinction matters. We now have a real source of truth, but we are not forcing unstable worldgen or entity rewrites until the specific bridge is ready.

## Ownership Map

| Area | Current owner | Core file |
| --- | --- | --- |
| Rank/reputation | KubeJS runtime bridge now, future FTB Quests for formal trials | `rank_progression.json`, `runtime_rules.json` |
| Skill XP/HUD | Puffish Skills + KubeJS Painter | `progression_hooks.json` |
| Rarity UI | Item Borders + Legendary Tooltips + KubeJS | `loot_rarity_rules.json` |
| Mob threat roles | generated mob index, future In Control | `mob_ecology.json` |
| Structures/density | generated structure index, Open Loader, configs | `structure_ecology.json` |
| NPC profiles | CustomNPCs/Easy NPC + generated registries | `npc_role_contracts.json` |
| Materials/recipes | Almost Unified, Polymorph, KubeJS | `material_unification.json` |
| Regions | KubeJS distance/dimension mirror, Ascendant Atlas finite coordinate runtime, and the `ascendant_atlas_regions:regional_multi_noise` biome source | `world_regions.json`, `runtime_rules.json`, `config/ascendant_atlas/*.json`, `config/incontrol/areas.json`, `config/ascendant_atlas/worldgen_regions.json` |

## Custom Mod Threshold

Build a custom Forge helper only when the data layer cannot solve the problem cleanly:

- `Ascendant Core`: registry sync, debug commands, shared APIs.
- `Ascendant Nameplates`: final player/NPC/enemy rank and level overlay.
- `Ascendant NPC Runtime`: generated NPC behavior, equipment repair, and settlement defense roles.
- `Ascendant Settlement Engine`: safe one-board-per-settlement placement and village integration.
- `Ascendant Atlas`: first helper is active for coordinate-aware biome-source control. Future Atlas helper work is limited to terrain-aware road/bridge substitution and structure-pool conflict resolution.
- `Ascendant Encounter Director`: rank-aware or region-aware dynamic spawn pressure.

## Next Implementation Steps

1. Retest the expanded Bountiful boards and cap-only spawn safety in a fresh client/server pass.
2. Generate a copied-world `spawner.json` draft only for missing biome/region ambience after entity IDs and biome targets are narrowed.
3. Use `structure_ecology.json` to add specific safe loot links into selected structure loot tables without blanket overriding all dungeons.
4. Use `rank_progression.json`, `progression_hooks.json`, and `runtime_rules.json` to build formal FTB Quest rank trials on top of the live counters.
5. Start the first custom helper mod only for nameplates/NPC runtime if the current fallbacks remain visually or behaviorally limited.
