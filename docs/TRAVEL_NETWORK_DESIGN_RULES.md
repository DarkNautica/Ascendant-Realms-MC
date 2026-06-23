
# Travel Network Design Rules

Generated: 2026-06-17T02:37:09+00:00

Status: design scaffold only. These rules are not active generation logic.

## Core Rules

- Roads should connect settlements, waystations, bridges, passes, ports, and future Guild outposts.
- Roads should not generate randomly without a visible purpose.
- Roads should not cross large cliffs without switchbacks, stairs, tunnels, supports, or bridges.
- River roads should prefer bridges, fords, docks, or intentional crossings rather than flat path pieces through water.
- Crownlands/Hearthlands should have the safest and clearest starter road network.
- Dangerous or broken roads are allowed only when the region identity supports it and the player can read the intent.

## Regional Rules

### Hearthlands

- safe low-grade roads; short timber or stone bridges over small rivers; avoid dangerous cliffs near spawn
### Sunreach

- caravan roads, dry washes, rare oases, and small river bridges; avoid ocean-like basins as road anchors
### Frostmarch

- snow roads, frozen crossings, mountain passes, and sturdy cold-weather bridges
### Stoneback Highlands

- passes, switchbacks, tunnels, mountain bridges, and supported roads instead of straight cliff paths
### Verdant Coast

- river bridges, docks, swamp boardwalks, port roads, and coastal crossings
### Outer Rim

- dangerous, sparse routes; ruins, broken bridges, and difficult crossings are acceptable when intentional

## Source Ownership

- YUNG's Bridges: keep as natural bridge landmarks until field review proves route value.
- Macaw's Bridges: keep as a build palette for future authored or helper-placed bridge pieces.
- Integrated Villages: treat roads, docks, and mossy_mounds bridge pieces as local settlement content.
- Towns and Towers: treat streets as local settlement content until bridge gaps, slopes, and overlap are reviewed.
- Moog/IDAS/Structory/Human Companions: treat path blocks as local template dressing, not as the Atlas road network.

## Future Helper Boundary

A real route layer needs terrain awareness after chunks, roads, water, ravines, and cliffs exist. Datapack rules can define palettes and structures, but a helper module is the right tool for detecting bad crossings and replacing a road segment with a bridge, stair, tunnel, or support piece.

## Candidate Status

All travel candidates in `config/ascendant_travel/travel_network_candidates.json` are disabled review items. Do not enable them until terrain signoff and explicit approval.
