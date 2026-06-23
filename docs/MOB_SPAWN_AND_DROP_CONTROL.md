# Mob Spawn And Drop Control

Status: high-density spawn pass active; broader region-aware spawn/drop policy still pending.

`config/incontrol/spawn.json` now uses higher cap ceilings so installed mob families are not suppressed by the older quiet-world pass. `config/spawnbalanceutility-common.toml` and `config/majruszsdifficulty.json` raise natural density. `config/incontrol/spawner.json` is now active and adds daytime/cave common-hostile pressure using biome-native monster tables plus biome-tagged fallback groups.

See `docs/MOB_SPAWN_DENSITY_PASS.md`, `docs/HOSTILE_DAY_SPAWN_PASS.md`, and `config/ascendant_core/spawn_density_policy.json`.
