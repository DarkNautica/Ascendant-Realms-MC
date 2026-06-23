# Dungeon Portal System

Status: rank-slot random dungeon rifts active; frameless fixed-facing gate visuals and circular teleportable Immersive Portals surfaces are enabled. Helper enter/return commands remain fallback/admin plumbing only.

Ascendant Ranked Dungeons will use Immersive Portals as the main portal layer. The design goal is for dungeon entrances to feel like actual breaches into ranked content instead of ordinary overworld structure spam.

## Portal Owner

- Primary portal mod: Immersive Portals for (Neo)Forge.
- Packwiz metadata: `mods/immersive-portals-neoforge.pw.toml`.
- Expected jar after export/sync: `immersive-portals-3.0.7-all.jar`.
- Required dependency already present: Cloth Config.

## Current Behavior

The helper validates rolls, opens one controlled generated dungeon instance per rank with `/ascdungeon spawn_test_here <rank>` or `/ascdungeon open_test_rift <rank>`, and can force a timed random world rift with `/ascdungeon spawn_random_now`. Current gates are intentionally frameless: they use Jayden's animated rank gate texture, invisible light blocks, rank-colored particles, nearby portal ambience, report files, and cleanup commands. Current rank size ranges are D `3.8-4.7`, C `4.2-5.3`, B `4.9-6.4`, A `5.8-7.5`, and S `6.8-9.0`.

The intended playable travel path is now the Immersive Portals entity itself. The helper creates a circular `GeometryPortalShape`, marks the portal teleportable, and uses a transparent-center gate texture so the see-through dungeon view lives inside the circular art instead of behind a square. Helper enter/return commands remain available only as fallback/admin tools if a test surface fails.

After the first player enters, the overworld entrance stays open for 5 seconds so another player can follow through. It then starts a short shrink-out animation on the visible gate art and removes the entrance surface/light after the shrink completes.

Elite Holograms remains installed, but helper auto-creation is disabled because the mod currently adds a yellow editor-instruction helper line above spawned holograms. See `docs/ASCENDANT_DUNGEON_HOLOGRAMS.md` and `docs/ASCENDANT_DUNGEON_SPAWN_TESTING.md`.

## Planned Portal Rules

- Every dungeon rift must have a return path after the boss is defeated.
- The overworld entrance must remain open for a short party grace window after first entry, then shrink out instead of vanishing instantly.
- Every live rift must write a cleanup record.
- Random rifts use one active slot per rank: at most one D, one C, one B, one A, and one S rift can exist at once.
- Rifts must avoid villages, major structures, and immediate spawn.
- D and C rifts can be smaller and more common.
- A and S rifts must be rare and manual-reviewed before expanding beyond controlled testing.

## Direct API vs Command Bridge

The helper now compiles against Immersive Portals and creates direct circular API portal surfaces from `/ascdungeon open_test_rift <rank>`, `/ascdungeon spawn_test_here <rank>`, and `/ascdungeon spawn_random_now`. The command bridge is not used for this pass.

## Current Test Acceptance

- Game launches with the portal jar in the active instance.
- `/ascdungeon status` reports Immersive Portals loaded.
- `/ascdungeon spawn_random_now` creates one timed random ranked rift in an open rank slot.
- The gate texture is fixed-facing and does not billboard toward the player.
- `/ascdungeon spawn_visual_here <rank>` creates one visual-only gate-art check.
- `/ascdungeon spawn_test_all_ranks 12` creates a D/C/B/A/S visual-only test row.
- `/ascdungeon cleanup_test` removes temporary gate displays, invisible light blocks, particles, old fallback nameplates, and any old holograms.
- No return gate exists before the boss is defeated.
- Defeating the tagged boss opens the return gate.
- The player lands on a solid generated room floor in the dungeon dimension, not in the sky/void.
- The report `config/ascendant_dungeons/reports/dungeon_instance_latest.json` shows whether Immersive Portal visual surfaces were created.
- Per-rank reports such as `config/ascendant_dungeons/reports/dungeon_instance_d_rank_latest.json` show the active state for each rank slot.
- The report should show `portal_shape=circular_special_shape`, `immersive_portal_teleportable=true`, and `entrance_travel_owned_by_immersive_portals=true` when the circular portal surface is active.
- After first entry, the report should show `entrance_close_at_millis`, `entrance_shrink_started_at_millis`, and `entrance_remove_at_millis`.
