# Atlas Random Worldgen Restore

Last updated: 2026-06-18.

Status: active rollback. Ascendant Atlas no longer steers Overworld terrain or biome generation by north/south/east/west coordinates.

## Decision

Jayden rejected the coordinate-directed Atlas worldgen pass after repeated visible failures:

- hard biome/terrain cuts that ran in long straight lines
- terrain that still changed too abruptly across Atlas sectors
- earlier ocean/basin fixes that either failed below biome selection or produced artificial filled shelves
- north/south gradient behavior that was too fragile for the pack's visual goals

The pack should return to random Tectonic/Terralith generation. Structures and roads should be tuned against that random baseline.

## Disabled Influence Points

These files are intentionally absent:

- `config/openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json`
- `config/openloader/data/ascendant_realms_atlas/data/minecraft/worldgen/density_function/overworld/continents.json`
- `openloader/data/ascendant_realms_atlas/data/minecraft/dimension/overworld.json`
- `openloader/data/ascendant_realms_atlas/data/minecraft/worldgen/density_function/overworld/continents.json`

`scripts/check-pack.py` now fails if those files exist while `config/ascendant_atlas/worldgen_override_policy.json` says `worldgen_override_enabled=false`.

## What Remains

The Atlas datapack can still keep debug/status assets, old reports, planning configs, and historical validation data. The helper jar may remain installed for diagnostics/history.

Those pieces must not be treated as active terrain steering while random mode is selected.

## Validation

After syncing the active CurseForge instance, use a fresh world or fully ungenerated chunks. Existing generated chunks can preserve old Atlas-shaped terrain and old structure placement.

Expected result:

- no Atlas Overworld dimension override
- no Atlas `minecraft:overworld/continents` density-function override
- normal random Tectonic/Terralith biome and terrain distribution
- structure testing can continue against the random baseline

Do not rerun Atlas terrain validation commands as signoff for this mode. They were built for the disabled coordinate-aware biome source and can be misleading after the rollback.
