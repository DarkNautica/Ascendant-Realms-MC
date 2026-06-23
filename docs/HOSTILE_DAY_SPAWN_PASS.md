# Hostile Day Spawn Pass

Status: active as of 2026-06-18.

Jayden's test showed the first density pass helped animals and wildlife but still left too few enemies. The reason is simple: boosted natural spawn weights do not overcome daylight restrictions for most hostile surface spawns.

This pass adds active hostile injection through `config/incontrol/spawner.json`.

## Live Files

- `config/incontrol/spawner.json`
- `config/incontrol/spawn.json`
- `config/spawnbalanceutility-common.toml`
- `config/majruszsdifficulty.json`
- `config/ascendant_core/spawn_density_policy.json`
- `config/ascendant_core/live_spawn_policy.json`

## What Changed

`config/incontrol/spawner.json` now adds six controlled hostile spawn rules:

1. Daylight-safe modded wilderness predators, raiders, casters, and elites.
2. Hot/arid daylight-safe modded hostile pool.
3. Cold/highland daylight-safe modded hostile pool.
4. Forest/jungle/swamp daylight-safe modded hostile pool.
5. Mage/raider daylight-safe modded pressure pool.
6. Biome-native cave monster reinforcement.

The surface rules use `norestrictions` so they can spawn during the day. They also use positive land biome tags, village-structure avoidance, and `maxhostile` / `maxlocal` / `maxthis` caps. Open-sky biome-native monster injection was removed because it can pull in burning undead during the day.

Regional difficulty now comes from `config/ascendant_core/regional_difficulty_policy.json` and `kubejs/server_scripts/ascendant_regional_difficulty.js`, which tag/buff eligible hostile mobs according to the nearest player's Atlas region/ring.

## What Did Not Change

- No new mods were added.
- Boss/dragon-tier mobs were not explicitly injected.
- CRD/day-count difficulty ramping was not re-enabled.
- Loot, structures, villages, roads, recipes, magic gates, and rank gates were not changed.
- Existing In Control regional boss/elite guardrails remain in `spawn.json`.

## Test Checklist

Use the existing test world after restarting Minecraft.

1. Set difficulty to Normal or Hard.
2. Test daytime first, not only night.
3. Walk 500-1000 blocks through plains, forest, hills, hot/arid terrain, cold terrain, and caves.
4. Expect multiple enemies to appear in sight during daytime in normal wilderness.
5. Check villages for excessive pressure against villagers and guards.
6. Watch TPS/frame feel for 5-10 minutes.

If the world still feels too empty, raise `persecond` on the six spawner rules before adding boss or elite mobs. If the amount feels good but a specific region feels wrong, tune `regional_difficulty_policy.json` before changing the global baseline.
