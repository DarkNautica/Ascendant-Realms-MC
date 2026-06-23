# Ascendant Atlas Worldgen

Status: finite-world coordinate runtime remains, but coordinate-aware Overworld biome/terrain steering is disabled; Atlas waymarks are debug-only assets.

Ascendant Atlas is no longer the active Overworld terrain-shaping layer. Jayden rejected the coordinate-directed north/south/east/west worldgen approach after hard biome and terrain cuts remained visible. The pack is returning to random Tectonic/Terralith Overworld generation, with structures and roads tuned against that baseline.

The previous biome-source layer was implemented by the local Forge helper mod `ascendant_atlas_regions`, and the previous land-bias prototype used `ascendant_atlas_regions:atlas_land_bias` through `minecraft:overworld/continents`. Both active datapack references are now intentionally removed. See `docs/ATLAS_RANDOM_WORLDGEN_RESTORE.md` and `config/ascendant_atlas/worldgen_override_policy.json`.

## Live Runtime

- Runtime config: `config/ascendant_atlas/runtime.json`
- Worldgen override policy: `config/ascendant_atlas/worldgen_override_policy.json`
- Worldgen region manifest: `config/ascendant_atlas/worldgen_regions.json` (historical/generated table while random mode is active)
- KubeJS bridge: `kubejs/server_scripts/ascendant_atlas_runtime.js`
- In Control areas: `config/incontrol/areas.json`
- Spawn guardrails: `config/incontrol/spawn.json`
- Road/bridge policy: `config/ascendant_atlas/road_bridge_policy.json`
- Debug/status function: `/function ascendant_atlas:status`
- Terrain diagnostic commands: `/ascatlas here`, `/ascatlas region <x> <z>`, `/ascatlas sample_grid <radius> <step>`, `/ascatlas sample_surface_grid <radius> <step>`, `/ascatlas dump_biome_pools`
- Terrain validation reports: `docs/ATLAS_TERRAIN_VALIDATION_REPORT.md`, `docs/ATLAS_BIOME_POOL_REPORT.md`, `docs/ATLAS_WORLDGEN_FAILURES.md`
- Machine reports: `config/ascendant_atlas/reports/sample_grid_source_latest.json`, `config/ascendant_atlas/reports/sample_grid_surface_latest.json`, `config/ascendant_atlas/reports/biome_pools_resolved.json`, `config/ascendant_atlas/reports/missing_biomes.json`
- Helper source: `local-mods/ascendant-atlas-regions/`
- Helper build script: `scripts/build-ascendant-atlas-regions.ps1`
- Helper jar: `mods/ascendant-atlas-regions-0.1.0.jar` (may remain installed, but not referenced by Overworld worldgen while random mode is active)
- Removed Overworld override: `config/openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json`
- Removed continentalness override: `config/openloader/data/ascendant_realms_atlas/data/minecraft/worldgen/density_function/overworld/continents.json`
- Biome-source generator: `scripts/generate-ascendant-atlas-worldgen.py` (must not regenerate overrides while policy is disabled)

Live scoreboards:

| Objective | Meaning |
|---|---|
| `ar_atlas_region` | Numeric region ID |
| `ar_atlas_ring` | Distance/progression ring |
| `ar_atlas_sector` | Direction sector |
| `ar_atlas_distance` | Distance from origin |
| `ar_atlas_x` | X offset from origin |
| `ar_atlas_z` | Z offset from origin |

Region IDs:

| ID | Region |
|---:|---|
| 0 | Hearthlands |
| 1 | Frostmarch |
| 2 | Sunreach |
| 3 | Verdant Coast |
| 4 | Stoneback Highlands |
| 5 | North East Marches |
| 6 | North West Marches |
| 7 | South East Wilds |
| 8 | South West Wilds |
| 9 | Outer Rim |
| 10 | Nether Front |
| 11 | End Expanse |

## Existing Density Context

The current terrain-first pass does not add Hunter Boards, Guild structures, decorative Atlas structures, village injection, or road tuning. Existing density files remain in the pack, but terrain validation must pass before moving back to settlements, Guild/Hunter placement, NPCs, roads, or bridges.

| Layer | Current tuning |
|---|---|
| Sparse Structures | Global spread `1.25`; vanilla village factor `1.0`; pillager outpost factor `1.1` |
| Integrated Villages | Regular villages `64/32`, exclusion zone `12` chunks |
| Towns and Towers | Towns `52/24`, towers `48/22`, other structures `36/14` |

These numbers are historical context only for this pass. The target right now is terrain identity, biome fit, and smooth transitions.

## Debug Atlas Structures

The previous waymark structures remain in the datapack as debug/source assets:

- `ascendant_atlas:crownlands_waymark`
- `ascendant_atlas:frostmarch_waymark`
- `ascendant_atlas:sunreach_waymark`
- `ascendant_atlas:verdant_crossing`
- `ascendant_atlas:stoneback_waystation`

They are no longer registered in structure sets, so they should not generate naturally in fresh worlds. This prevents placeholder waymarks from distracting from the actual worldgen test.

## Road/Bridge Boundary

The pack currently has two bridge layers:

- YUNG's Bridges generates standalone bridge landmarks.
- Macaw's Bridges and Macaw's Lights provide bridge and wall-lantern blocks for authored structures.

What is live now:

- Custom Guild structures can use Macaw wall lanterns and authored bridge materials.
- The road/bridge policy records how roads should behave by region.
- The Overworld biome source is no longer coordinate-aware through Atlas while random mode is active.
- Fresh-world tests should record coordinates where roads cross rivers, ravines, or steep cliffs without a bridge.

What needs a helper module:

- Detecting a road after terrain and village pieces generate.
- Inspecting nearby water, cliffs, or ravines.
- Replacing that road segment with a Macaw/YUNG-style bridge or support piece.

The first helper module previously handled hard north/south/east/west biome-source placement, but that influence is now disabled. Future work should focus on structure placement, route/bridge substitution, and structure-pool conflict resolution against the random terrain baseline.

Startup note: the helper must register `regional_multi_noise` through Forge `DeferredRegister`. Direct calls into `BuiltInRegistries.f_256737_` or `Registry.m_122965_` happen too late on Forge 47.4.20 and crash during mod loading with `Registry is already frozen`.

KubeJS runtime note: Atlas config reads must use direct `JsonIO.read("config/ascendant_atlas/runtime.json")` style string paths. Calling `KubeJSPaths.CONFIG.resolve("...")` is ambiguous under Rhino on Windows and prevents the runtime from reading its config.

North/south field-test note: the first live world proved the status runtime worked but exposed two Atlas worldgen issues: the north could collapse into one long ocean stretch, and the shared `outer` table took over immediately past the old 3000-block proof radius, allowing southern terrain to become snowy. The helper now delays the shared outer table until 50000 blocks and applies a climate gradient before selecting biomes. The 30000-block square world border remains the playable limit; the 50000-block radial outer cutoff is a visual buffer that covers the border edges and corners so the player does not see a hard climate snap beyond the barrier. North intentionally allows cold/frozen oceans as seas rather than endless oceans and should move toward tundra, ice, and frozen biomes with distance; south intentionally allows warm ocean near the first transition but should move toward dry stone, sand, desert, and badlands with distance.

Center field-test note: a later live pass found ocean/island terrain inside the Hearthlands radius. The center table now rejects `terralith:alpha_islands`, `minecraft:grove`, and `minecraft:river`; Hearthlands should stay mild and mostly dry.

Cardinal ocean field-test note: a live pass at about `x=339, z=-1937` generated a uniform `minecraft:deep_frozen_ocean` field. The north table now rejects deep cold/deep frozen ocean, cold ocean, snowy beach, ice marsh, and steep alpine-first picks; it keeps frozen ocean only as a sparse far-north sea pocket when the underlying climate noise is strongly oceanic. The south table keeps regular warm ocean only for sparse warm-sea pockets and rejects lukewarm/deep lukewarm ocean.

Center/south-east seam field-test note: a live pass around `x=359, z=619` exposed an ugly Hearthlands boundary mix of river, lukewarm ocean, gravel desert, and gravel beach noise. The center table now rejects river, the direct south table rejects `minecraft:lukewarm_ocean` and `terralith:gravel_desert`, the east table rejects `terralith:gravel_beach`, and the south helper bias starts land-first with sparse warm-sea pockets only farther from spawn.

Warm-region snow field-test note: the same live pass found real `minecraft:snow`, `snowrealmagic:snow`, and `minecraft:ice` blocks saved on `terralith:gravel_desert`, with nearby surface examples around `x=400-421, z=557-579, y=208-211`. The audit explains why: `terralith:gravel_desert` has biome temperature `0.14` and negative Terralith climate temperature despite the desert name, so it is a snow-risk biome. Atlas removes it from the direct south seam, and source configs now prevent Weather2 snowstorms from building outside cold biomes, make Snow Real Magic melt snow/ice in warm biomes, and disable global Serene Seasons winter snow/ice conversion.

West/south-west snow audit note: the terrain validation report found that `terralith:scarlet_mountains`, `minecraft:jagged_peaks`, `terralith:alpine_grove`, and `terralith:emerald_peaks` allow snow by biome data. They are removed from the west pool so Stoneback Highlands and South West Wilds do not create snow outside intended cold regions.

Direct-north biome note: `minecraft:grove` is a snowy alpine forest by its actual biome data and should not appear in the Hearthlands center or direct Frostmarch north opener. If it returns, it belongs to later alpine/highland tuning, not the first north gradient band.

Content audit note: biome, structure, and mob placement decisions should be checked against `docs/WORLDGEN_CONTENT_AUDIT.md` and `docs/generated/worldgen_content_audit.json`. The audit reads active jar/datapack JSON, Terralith climate entries, structure sets, direct jigsaw templates, structure block palettes, biome spawners, and structure spawn overrides.

## Fresh World Test

1. Launch a fresh creative test world.
2. Run `/ascatlas here` at spawn; expected Hearthlands center and a mild/dry biome from the center pool.
3. Run `/ascatlas dump_biome_pools`; confirm it writes `config/ascendant_atlas/reports/biome_pools_resolved.json`.
4. Run `/ascatlas sample_grid 12000 2000`; confirm it writes `config/ascendant_atlas/reports/sample_grid_source_latest.json` with source-level biome IDs.
5. Run `/ascatlas sample_surface_grid 12000 2000`; confirm it writes `config/ascendant_atlas/reports/sample_grid_surface_latest.json` with generated surface height, surface block, and surface biome data.
6. Rerun `python scripts/generate-atlas-terrain-validation.py` outside the game to enrich actual biome IDs with audit climate data and refresh the docs.
7. Visit the required points in `docs/ATLAS_TERRAIN_VALIDATION_REPORT.md`: 0, 2000, 5000, 9000, 12000 along each axis plus the 5000-block diagonals.
8. Confirm actual generated biomes match the region identity: mild and mostly dry Hearthlands, progressively colder Frostmarch, progressively arid/hot Sunreach, wet/coastal/jungle/oceanic Verdant Coast, and mountain/highland Stoneback Highlands.
9. Record whether transitions are too sharp or acceptable. Diagonals should blend instead of hard snapping.
10. Confirm high-tier boss/dragon/ocean mobs do not flood the Hearthlands near spawn.
11. Only document road/river/cliff issues during this pass. Do not tune roads, villages, Hunter Boards, Guild Halls, or NPC placement until the terrain report passes.
11. Save/reload, then repeat the same status, biome, and density checks on a dedicated server.

## Next Helper-Mod Work

The first helper module is active. Next targets:

- `ascendant_route_bridge`: terrain-aware road and bridge substitution.
- `ascendant_settlement_director`: village/structure spacing and pool conflict resolution when static spacing is not enough.
- `ascendant_encounter_director`: rank, region, and distance-aware mob pressure beyond what In Control can safely express.
