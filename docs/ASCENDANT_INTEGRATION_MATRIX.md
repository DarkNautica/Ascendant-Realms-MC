# Ascendant Integration Matrix

Generated: 2026-06-14T15:41:03.2735019-04:00

Current integration update: `config/ascendant_core/` is now the active pack-owned contract layer. The generated matrix remains the scan-derived coverage view, while Ascendant Core turns it into ranked gameplay domains and runtime scoreboard ownership.

This matrix turns the master integration plan into implementation layers that can be tested without manual play-feel checks.

## Coverage

| Area | Count |
| --- | ---: |
| Mobs indexed | 757 |
| Structures indexed | 617 |
| Mobs requiring spawn review | 476 |
| Structures requiring density review | 496 |

## Implementation Layers

| Layer | Use |
| --- | --- |
| Config | Mod-exposed spawn, UI, density, health, audio, and visual settings. |
| Open Loader datapacks | Tags, loot tables, structure tags, recipes, advancements, and function fallbacks. |
| KubeJS | Tooltips, item registration, JEI aliases, tags, recipe glue, and light event glue. |
| Custom Forge helper mods | Dynamic nameplates, skill HUD, runtime NPC profiles, encounter director, and synced rarity/progression data. |

## Active Ascendant Core Domains

| Domain | File | Runtime state |
| --- | --- | --- |
| Ranks | `config/ascendant_core/rank_progression.json` | contract active |
| Regions | `config/ascendant_core/world_regions.json` | contract active |
| Mob ecology | `config/ascendant_core/mob_ecology.json` | contract active |
| Structure ecology | `config/ascendant_core/structure_ecology.json` | contract active |
| Loot and rarity | `config/ascendant_core/loot_rarity_rules.json` | live UI, reward contracts active |
| NPC roles | `config/ascendant_core/npc_role_contracts.json` | contract active |
| Materials | `config/ascendant_core/material_unification.json` | live tooling, recipe contracts active |
| Progression hooks | `config/ascendant_core/progression_hooks.json` | live HUD, milestone contracts active |
| Custom modules | `config/ascendant_core/custom_module_plan.json` | planned custom mod thresholds |

## Current Live Unification Outputs

| Output | File | Status |
| --- | --- | --- |
| Expanded Guild contracts | `config/openloader/data/ascendant_realms_guild/data/bountiful/` | live through Open Loader |
| Bountiful summary | `config/ascendant_guild/live_bountiful_pools.json` | live, generated |
| Settlement-safety spawn caps | `config/incontrol/spawn.json` | live, cap-only |
| Spawn policy record | `config/ascendant_core/live_spawn_policy.json` | active documentation/config contract |
| Implementation notes | `docs/ASCENDANT_UNIFICATION_IMPLEMENTATION_PASS.md` | active pass record |

## Custom Mod Candidates

| Candidate | Priority | Why |
| --- | --- | --- |
| `ascendant_core` | high | Shared registry loader, client/server sync, commands, and integration APIs. |
| `ascendant_nameplates` | very_high | Styled dynamic player, NPC, rival, and enemy labels beyond vanilla scoreboard limits. |
| `ascendant_progression_hud` | very_high | Second skill XP bar, level-up popups, and rank milestone presentation. |
| `ascendant_npc_runtime` | high | Profile-driven NPC setup, equipment, rank/level identity, and repair without embedded script drift. |
| `ascendant_settlement_engine` | medium_high | Safe Hunter Board/Guild structure placement and NPC population once standalone structures are proven. |
| `ascendant_encounter_director` | medium | Player/rank-aware spawn pressure if config and In Control rules are not enough. |

## Automated Next Steps

- Use config/ascendant_index/mob_registry.json to drive the next In Control and bounty tuning pass. First pass is now active for Bountiful pools and cap-only In Control rules.
- Use config/ascendant_index/structure_registry.json to drive settlement, loot, and density tuning. Structure loot and settlement injection are next, not yet broad-live.
- Use config/ascendant_index/integration_matrix.json as the machine-readable custom-mod threshold list.
- Use config/ascendant_core/core_manifest.json as the current source of truth for runtime scoreboards and domain ownership.
- Keep runtime overlays and entity behavior out of datapacks if the data cannot be read or synced safely.
