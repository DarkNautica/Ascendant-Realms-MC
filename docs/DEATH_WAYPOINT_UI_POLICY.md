# Death Waypoint UI Policy

Last updated: 2026-06-18.

Status: active client clutter-control policy. This changes Xaero minimap deathpoint presentation only. It does not change death recovery, graves, loot, mobs, worldgen, structures, or progression.

## Problem

Xaero keeps one current death marker and turns older death markers into `gui.xaero_deathpoint_old` waypoints. After repeated deaths, every old death marker can remain visible in the world/HUD, which creates extreme screen clutter before the player retrieves belongings.

Jayden's target behavior is:

- Recent/current death stays visible.
- Older deaths stop cluttering the screen at long range.
- The UI should not show every old death from across the world.

## Current Implementation

Xaero's exposed profile config has a global `waypoint_max_distance`, but not an old-deathpoint-only distance cap. A global 100-block cap would also hide the recent death marker, which is not acceptable.

The current safe implementation is therefore:

- Keep `deathpoints = true`.
- Set `old_deathpoints = false`.
- On sync, disable existing `gui.xaero_deathpoint_old` entries in Xaero `waypoints.txt` files.
- Leave the current `gui.xaero_deathpoint` entry enabled.

This is stricter than the ideal 100m behavior, but it solves the actual screen-clutter problem without breaking the current death marker.

## Source Of Truth

- Policy: `config/ascendant_ui/death_waypoint_policy.json`
- Sync: `scripts/sync-active-client-files.ps1`
- Active profile target: `config/xaero/minimap/profiles/default.cfg`
- Active world waypoint targets: `xaero/minimap/**/waypoints.txt`

## Validation

`python scripts/check-pack.py` checks:

- The policy JSON exists and is valid.
- The sync script contains the death waypoint policy hook.
- Active Xaero config drift is warned if old deathpoints are still enabled.
- Active old deathpoint waypoint drift is warned if old deathpoints remain enabled in saved waypoint files.

## Future Exact 100m Version

The exact requested behavior, "old deaths visible within 100m but hidden farther away," likely needs a client-side Xaero integration or custom HUD hook that checks old deathpoint distance at render time while exempting the current deathpoint. That was not added in this pass.
