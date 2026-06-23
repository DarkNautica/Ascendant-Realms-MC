# Mob Spawn Density Pass

Last updated: 2026-06-18.

## Status

Active gameplay tuning pass. This is no longer the old conservative settlement-safety posture.

Jayden's current target is clear: ordinary exploration should feel alive and dangerous, and the player should almost never be able to walk through the world without seeing multiple mobs nearby.

Latest clarification: difficulty multipliers are allowed, but they must come from Atlas region/ring identity instead of time, day count, or chunk-residence duration.

## Live Files Changed

- `config/spawnbalanceutility-common.toml`
- `config/majruszsdifficulty.json`
- `config/incontrol/spawner.json`
- `config/incontrol/spawn.json`
- `config/ascendant_core/regional_difficulty_policy.json`
- `kubejs/server_scripts/ascendant_regional_difficulty.js`
- `config/ascendant_core/live_spawn_policy.json`
- `config/ascendant_core/spawn_density_policy.json`

## What Changed

Spawn Balance Utility:

- Minimum spawn weight: `12` -> `20`.
- Maximum spawn weight: `110` -> `180`.
- Vanilla default weight overrides now include zombies, skeletons, spiders, creepers, endermen, and witches.

Majrusz's Progressive Difficulty:

- Spawn-rate multiplier is a flat immediate baseline: `2.1` for default, expert, and master.
- CRD/time scaling is disabled: all `is_scaled_by_crd` flags are false, and all `crd_penalty` values are `0.0`.
- Skeleton, undead, zombie-miner, and piglin mob-group chances and sidekick counts were raised so hostile mobs more often appear as visible groups instead of lonely singles.

In Control:

- Broad per-mod caps were raised so installed mob families are less likely to be suppressed by the older settlement-safety pass.
- `config/incontrol/spawner.json` now injects common hostile pressure during daytime and in caves.
- Surface rules use reviewed daylight-safe modded hostile pools instead of open-sky biome-native monsters, because biome-native daytime injection can create burning undead filler.
- Cave rules still pull biome-native monster entries because sunlight burn is not a cave problem.
- Hearthlands still blocks routine boss/dragon-tier namespaces.
- Born in Chaos and Mowzie pressure are allowed more often in Hearthlands, but not completely unrestricted.
- Aquamirae remains denied in Sunreach so water/ocean mobs do not become desert filler.

Regional Difficulty Bridge:

- `kubejs/server_scripts/ascendant_regional_difficulty.js` listens for hostile mob spawns.
- It reads the nearest player's Atlas region/ring scoreboards.
- It tags eligible hostiles and applies hidden regional pressure effects.
- Hearthlands has no extra regional buff, while diagonal frontier and outer regions are harsher.

## What Did Not Change

- No new mob mods were added.
- No dragons or bosses were made common.
- No loot, recipes, rank gates, magic gates, roads, villages, structures, or NPC placement changed.
- Alex's Mobs individual spawn weights were not blanket-edited.
- No elite/boss/dragon custom spawner entries were added.
- No time/day-count difficulty increase was enabled.

## Test Plan

Use a fresh or existing test world. New chunks are best for biome wildlife checks, but the config changes apply to spawning behavior without needing brand-new terrain.

1. Set difficulty to Normal or Hard.
2. Test daytime first in an open land area and wait one to two minutes.
3. Walk for 500-1000 blocks through plains/forest/hills and check whether multiple hostile mobs stay in sight.
4. Test hot/arid, cold/highland, and forest/jungle terrain during the day.
5. Compare Hearthlands against at least one diagonal/wilds region; the wilds should feel noticeably harsher without waiting for time to pass.
6. Enter a cave and check whether it feels populated without relying on dungeon spawners.
7. Visit a village at day and night and watch whether guards can keep the area usable.
8. Check Sunreach/desert terrain and confirm it is not filled with Aquamirae.
9. Watch TPS/frame feel for 5-10 minutes. If the game hitches hard, lower `spawner.json` `persecond` values first, then regional effects, then Majrusz spawn-rate.

## Expected Result

The world should now read as heavily populated in daylight and night. It should also feel more dangerous by region/ring, not by elapsed time. If Jayden still sees long empty walks, the next correct step is not to add more mob mods; it is to raise the reviewed `spawner.json` hostile rule rates or add carefully selected modded common-hostile entries.
