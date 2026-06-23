# Regional Spawn Difficulty Pass

Status: active as of 2026-06-22.

Jayden clarified the target: the difficulty multiplier is fine, but it should be based on where the player is in the world, not how much time has passed.

## Live Files

- `config/ascendant_core/regional_difficulty_policy.json`
- `kubejs/server_scripts/ascendant_regional_difficulty.js`
- `config/ascendant_core/spawn_density_policy.json`
- `config/ascendant_core/live_spawn_policy.json`
- `config/majruszsdifficulty.json`
- `config/incontrol/spawner.json`

## What Changed

Majrusz CRD/time ramping remains disabled:

- all `is_scaled_by_crd` flags stay `false`
- all `crd_penalty` values stay `0.0`
- the global spawn-rate baseline stays strong immediately instead of rising over time

The new regional layer uses the Atlas player scoreboards:

- `ar_atlas_region`
- `ar_atlas_ring`

When an eligible hostile mob spawns near a player, `kubejs/server_scripts/ascendant_regional_difficulty.js` tags it by the nearest player's Atlas region and applies a hidden regional pressure profile.

## Region Pressure

| Region | Pressure | Runtime Feel |
| --- | ---: | --- |
| Hearthlands | 1.00 | strong baseline only; no extra regional buff |
| Frostmarch | 1.18 | tougher cold-region hostiles |
| Sunreach | 1.20 | faster, harder-hitting arid hostiles |
| Verdant Coast | 1.16 | faster ambush pressure |
| Stoneback Highlands | 1.20 | sturdier, harder-hitting highland hostiles |
| North-East Marches | 1.28 | faster, tougher frontier hostiles |
| North-West Marches | 1.30 | sturdy cold/highland frontier hostiles |
| South-East Wilds | 1.30 | fast hot/wet frontier hostiles |
| South-West Wilds | 1.34 | harsh arid/highland frontier hostiles |
| Outer Rim | 1.45 | strongest non-boss location pressure |

Far Atlas rings add a small extra edge through hidden effects. This is location-based, not time-based.

## What Did Not Change

- No new mods were added.
- No boss/dragon spawn spam was added.
- No roads, villages, structures, loot, recipes, magic gates, or rank gates were changed.
- Open-sky daytime spawner rules still avoid forced zombies, skeletons, strays, husks, or other burning-undead filler.
- Players do not use commands for this in normal gameplay.

## Test Checklist

Use an existing test world after restarting Minecraft.

1. Set difficulty to Normal or Hard.
2. Daytime test Hearthlands first. It should be dangerous from density, but not as punishing as the frontier.
3. Move into at least two cardinal regions and one diagonal/wilds region.
4. Compare the same broad fight type across regions. Frontier/outer enemies should feel noticeably more dangerous.
5. Confirm daylight hostile pressure is mostly modded mobs and not rows of burning vanilla undead.
6. Check a village edge. It can be dangerous nearby, but the inside should not instantly become unusable.
7. Watch server feel for 5-10 minutes. If it lags, reduce the In Control `persecond` values before lowering regional pressure.

## Tuning Direction

If the world still feels too empty, raise `config/incontrol/spawner.json` rates or add reviewed daylight-safe common modded mobs.

If the world has enough enemies but the wrong places feel too hard, tune `config/ascendant_core/regional_difficulty_policy.json` region effects first.

Do not re-enable time/day-count scaling to solve region difficulty.
