
# Road, Bridge, And River Failures

Generated: 2026-06-17T02:37:09+00:00

Status: reconnaissance only. No road or bridge behavior was changed.

## Summary

- Confirmed terrain-water issue affecting road design: south/west ocean-like basins.
- Confirmed connected-road issue: no pack-owned connected road network exists yet.
- Confirmed bridge issue: bridge content exists, but route linkage is not established.
- Confirmed no-change rule: all candidates remain disabled.

## Failure Register

| Failure | Severity | Evidence | Recommendation |
| --- | --- | --- | --- |
| `atlas_south_west_ocean_leak_blocks_travel_signoff` | terrain_blocker | 15 confirmed ocean-leak water samples remain in south/west target regions. | Resolve Atlas land/water coherence before designing permanent roads through Sunreach or Stoneback. |
| `template_paths_not_terrain_aware` | manual_review | Vanilla villages, Integrated Villages, and Towns and Towers provide local paths/streets, but no Atlas-aware slope or cliff correction. | Field-test path crossings after terrain signoff; future helper should substitute bridges/supports. |
| `yungs_bridges_are_standalone` | manual_review | YUNG's Bridges is active, but jar inspection found no JSON route linkage to road networks. | Keep as scenic landmarks until route anchor behavior is manually reviewed. |
| `macaws_bridges_are_palette_only` | not_a_failure | Macaw's Bridges has no worldgen files in jar inspection. | Use as future authored/helper bridge blocks, not as an automatic fix. |
| `towns_and_towers_bridge_gap_risk` | manual_review | Towns and Towers has road/crossroad template evidence but no direct bridge template evidence from jar scan. | Inspect villages near rivers and cliffs before enabling any settlement expansion. |
| `mvs_paths_route_purpose_unknown` | manual_review | `mvs:paths` is a generated path structure with spacing 35 / separation 12. | Check whether it reads like useful trail detail or roads to nowhere. |

## Field Evidence Needed Later

- Coordinates where village paths cross rivers without bridges.
- Coordinates where paths float, cut cliffs, or shear through steep terrain.
- Coordinates where YUNG's Bridges generate naturally and whether they align with nearby roads or settlements.
- Coordinates where Towns and Towers streets meet rivers, ravines, ocean-leak basins, or cliff edges.
- Coordinates where Integrated Villages docks or local bridges create useful crossings versus awkward water edges.

## Current Do-Not-Fix-Yet Boundary

Do not disable road, village, bridge, or structure sources only because they are listed here. The current pass is evidence-gathering. The only terrain blocker still confirmed is Atlas land/water coherence in south/west regions.
