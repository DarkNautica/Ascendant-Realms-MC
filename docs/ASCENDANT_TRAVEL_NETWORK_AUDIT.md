
# Ascendant Travel Network Audit

Generated: 2026-06-17T02:37:09+00:00

Status: reconnaissance only. No roads, bridges, village pools, structure sets, or active generation configs were changed.

## Summary

- Road/path sources covered: 6
- Bridge sources covered: 4
- Path or travel-like structures detected in the generated worldgen audit: 68
- Confirmed south/west ocean-leak water samples still blocking travel signoff: 15
- Live generation changes enabled by this pass: 0

The current pack does not have one intentional connected travel network yet. It has village-local paths, template-local grounds, standalone bridge landmarks, way signs, and a bridge block palette. That is enough raw material, but not enough authorship. Future roads should wait until Atlas terrain-water coherence is signed off.

## Road And Path Sources

| Source | Mod/source | Config path | Spacing/density | Slope behavior | Bridge behavior | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| `minecraft:village_paths` | Minecraft vanilla villages | none | minecraft:villages spacing 34 / separation 8 from generated audit | template and jigsaw terrain adaptation; not Atlas-aware | not a reliable road bridge layer | keep_manual_review |
| `integrated_villages:path_networks` | Integrated Villages | config/integrated_villages-forge-1_20.toml | regular_villages spacing 64 / separation 32 from OpenLoader override | template-local paths; final slope handling needs in-game field review | mossy_mounds has bridge templates; pirate_village has docks; not a general road network | keep_but_review_paths_docks_and_local_bridges |
| `towns_and_towers:streets` | Towns and Towers | config/towns_and_towers/structure_rarity_new.json5 | towns 52/24, towers 48/22, other 36/14 from active config | village street templates; no terrain-aware Atlas road correction | no direct bridge/dock template evidence found in jar scan | keep_but_manual_review_before_settlement_work |
| `mvs:paths` | Moog's Voyager Structures | none | spacing 35 / separation 12 from generated audit | small path landmark; terrain purpose unknown | not a river crossing system | manual_review_for_roads_to_nowhere |
| `supplementaries:way_sign` | Supplementaries | none | spacing 19 / separation 10 from structure density audit | not a road, but a travel marker that should not imply missing routes | none | keep_observe_only |
| `template_local_paths:idas_structory_humancompanions_moog` | IDAS, Structory, Human Companions, Moog structures | none | varies by structure set; see template_local_path_risks | template-local paths/grounds only | not a connected bridge system | keep_observe_only |

## Bridge Sources

| Source | Mod/source | Config path | Spacing/density | Bridge behavior | Recommendation |
| --- | --- | --- | --- | --- | --- |
| `yungsbridges:bridges` | YUNG's Bridges | mods/yungs-bridges.pw.toml | code-driven or non-json; no structure_set JSON visible in jar scan | standalone world bridge landmarks, not linked to Atlas road routing | keep_manual_review |
| `macaws_bridges:palette` | Macaw's Bridges | mods/macaws-bridges.pw.toml | no worldgen files detected; palette only | build palette for future authored/helper bridge pieces | keep_palette_only |
| `integrated_villages:mossy_mounds_bridge` | Integrated Villages | config/integrated_villages-forge-1_20.toml | inherits integrated_villages:regular_villages 64/32 | local village bridge, not global road crossing | keep_manual_review |
| `integrated_villages:pirate_village_docks` | Integrated Villages | config/integrated_villages-forge-1_20.toml | inherits integrated village spacing | dock behavior only | keep_manual_review |

## Template-Local Path Risks

These are the highest path-like structures from `docs/generated/worldgen_content_audit.json`. A path count does not prove a broken road; it marks field-review priority.

| Structure | Source | Path-like blocks | Water blocks | Recommendation |
| --- | --- | --- | --- | --- |
| `minecraft:village_savanna` | minecraft-1.20.1 | 501 | 30 | keep_manual_review |
| `integrated_villages:mossy_mounds` | integrated_villages-1.3.2+1.20.1-forge.jar | 477 | 0 | keep_but_review_paths_docks_and_local_bridges |
| `minecraft:village_plains` | minecraft-1.20.1 | 396 | 50 | keep_manual_review |
| `minecraft:village_snowy` | minecraft-1.20.1 | 266 | 0 | keep_manual_review |
| `minecraft:village_taiga` | minecraft-1.20.1 | 160 | 38 | keep_manual_review |
| `idas:treetop_tavern` | idas_forge-1.13.0+1.20.1.jar | 157 | 0 | manual_review_high_path_volume |
| `towns_and_towers:village_jungle` | Towns-and-Towers-1.12-Fabric+Forge.jar | 120 | 8 | keep_but_manual_review_before_settlement_work |
| `structory:outcast_villager_grassy` | Structory_1.20.x_v1.3.5.jar | 120 | 0 | manual_review_high_path_volume |
| `structory:ruin_grassy` | Structory_1.20.x_v1.3.5.jar | 117 | 0 | manual_review_high_path_volume |
| `towns_and_towers:village_snowy_taiga` | Towns-and-Towers-1.12-Fabric+Forge.jar | 90 | 0 | keep_but_manual_review_before_settlement_work |
| `idas:winter_wagon` | idas_forge-1.13.0+1.20.1.jar | 76 | 0 | keep_observe_only |
| `structory:dense_forest_ruin` | Structory_1.20.x_v1.3.5.jar | 70 | 0 | keep_observe_only |
| `structory:graveyard` | Structory_1.20.x_v1.3.5.jar | 66 | 0 | keep_observe_only |
| `structory:abandoned_camp` | Structory_1.20.x_v1.3.5.jar | 64 | 10 | manual_review_water_edge_behavior |
| `mvs:big_oak_tree` | MoogsVoyagerStructures-1.20-5.0.6.jar | 60 | 0 | keep_observe_only |
| `mss:white_house` | MoogsSoaringStructures-1.20-2.1.0.jar | 58 | 0 | keep_observe_only |
| `mvs:tree_monument` | MoogsVoyagerStructures-1.20-5.0.6.jar | 49 | 0 | keep_observe_only |
| `humancompanions:oak_house` | humancompanions-1.20.1-1.7.6.jar | 44 | 0 | keep_observe_only |
| `mvs:campsite` | MoogsVoyagerStructures-1.20-5.0.6.jar | 44 | 0 | keep_observe_only |
| `mvs:crystal` | MoogsVoyagerStructures-1.20-5.0.6.jar | 40 | 0 | keep_observe_only |
| `idas:ancient_statue/ancient_statue_plains` | idas_forge-1.13.0+1.20.1.jar | 37 | 0 | keep_observe_only |
| `mvs:mineshaft` | MoogsVoyagerStructures-1.20-5.0.6.jar | 36 | 0 | keep_observe_only |
| `idas:lumber_camp/lumber_camp_acacia` | idas_forge-1.13.0+1.20.1.jar | 28 | 0 | keep_observe_only |
| `idas:pillager_camp` | idas_forge-1.13.0+1.20.1.jar | 23 | 0 | keep_observe_only |
| `idas:lumber_camp/lumber_camp_bygmahogany` | idas_forge-1.13.0+1.20.1.jar | 20 | 0 | keep_observe_only |

## River And Crossing Context

Water review remains relevant to travel design because bad roads can look even worse when placed on the confirmed south/west ocean-leak basins.

| Classification | Count |
| --- | --- |
| `acceptable_coastline` | 10 |
| `acceptable_lake` | 10 |
| `acceptable_mountain_lake` | 11 |
| `acceptable_oasis` | 3 |
| `acceptable_river` | 9 |
| `ocean_leak` | 15 |

Manual water review status from `config/ascendant_atlas/reports/water_surface_samples_latest.json`:

- Total water samples: 58
- South/west target-region water samples: 31
- Manually reviewed target samples: 19
- Visually confirmed ocean leaks: 15

## Design Rule Preview

| Region | Travel strategy |
| --- | --- |
| `hearthlands` | safe low-grade roads; short timber or stone bridges over small rivers; avoid dangerous cliffs near spawn |
| `sunreach` | caravan roads, dry washes, rare oases, and small river bridges; avoid ocean-like basins as road anchors |
| `frostmarch` | snow roads, frozen crossings, mountain passes, and sturdy cold-weather bridges |
| `stoneback_highlands` | passes, switchbacks, tunnels, mountain bridges, and supported roads instead of straight cliff paths |
| `verdant_coast` | river bridges, docks, swamp boardwalks, port roads, and coastal crossings |
| `outer_rim` | dangerous, sparse routes; ruins, broken bridges, and difficult crossings are acceptable when intentional |

## Validation Warnings To Keep

- Road sources with unknown cliff/slope or bridge-absence risk: `minecraft:village_paths`, `integrated_villages:path_networks`, `towns_and_towers:streets`, `template_local_paths:idas_structory_humancompanions_moog`
- Road sources with route-purpose risk: `mvs:paths`
- Bridge sources not yet linked to a crossing strategy: `yungsbridges:bridges`, `integrated_villages:mossy_mounds_bridge`

## No-Change Confirmation

This pass created documentation and `config/ascendant_travel/*.json` policy files only. It did not add roads, add bridges, inject villages, enable candidates, or rewrite live structure density.
