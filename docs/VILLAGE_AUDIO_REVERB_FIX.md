# Village Audio Reverb Fix

Status: source and active `Ascendant Realms (2)` synced.
Date: 2026-06-22.

## Issue

Village audio was reported as sounding extremely echoing, like a cave.

The likely cause is Sound Physics Remastered treating clustered village blocks, nearby cliffs, and partially enclosed outdoor spaces as highly reflective environments. The previous config had strong reverb, high default reflectivity, multiple reflection bounces, and non-occluded sound redirection enabled.

## Source Change

File: `config/sound_physics_remastered/soundphysics.properties`

Changed values:

- `reverb_gain`: `0.8` -> `0.35`
- `reverb_brightness`: `1.0` -> `0.75`
- `default_block_reflectivity`: `0.45` -> `0.22`
- `sound_distance_allowance`: `4.0` -> `2.5`
- `environment_evaluation_ray_count`: `24` -> `16`
- `environment_evaluation_ray_bounces`: `3` -> `1`
- `sound_direction_evaluation`: `true` -> `false`
- `redirect_non_occluded_sounds`: `true` -> `false`

## Intent

Keep Sound Physics active for muffling, occlusion, and environmental feel, but stop ordinary villages from sounding like stone caverns.

This is intentionally not a full audio-mod removal and does not touch terrain, mobs, structures, dungeons, NPCs, rank systems, resource packs, or shaders.

## Active Instance

The fix was synced into active `Ascendant Realms (2)` on 2026-06-22 after Jayden confirmed the running Minecraft process was a different instance.

After syncing, relaunch and test:

- one village in the open
- one village near cliffs or stone buildings
- one cave or dungeon

Expected result: villages should sound open-air with only light space, while caves and enclosed structures can still have stronger reverb.

## If Still Too Echoing

Next safe tuning step:

- lower `reverb_gain` to `0.2`
- lower `default_block_reflectivity` to `0.15`

Last-resort tuning:

- set `reverb_gain=0.0` to keep occlusion without audible reverb.
