# Ascendant Realms Open Loader

Status: legacy/source mirror for Batch N datapack material.

OpenLoader Forge 1.20.1 reads active global datapacks from `config/openloader/data/` in the actual client/server instance. This repo-level `openloader/data/` folder is retained as a source mirror for inspection and manual fallback only.

Current global data packs:

- `data/ascendant_realms_skills/` mirrors the unified Ascendant Web Puffish Skills datapack, but the active skill tree currently loads from `config/puffish_skills/`.
- `data/ascendant_realms_world_integration/` mirrors the active crash-fix datapack that now lives under `config/openloader/data/ascendant_realms_world_integration/`.

Source of truth:

- Primary live skill config: `config/puffish_skills/`
- Fallback/source datapack copy: `datapacks/ascendant_realms_skills/`
- Open Loader legacy/source copy: `openloader/data/ascendant_realms_skills/`
- Active OpenLoader data path: `config/openloader/data/`

If Puffish Skills reports duplicate trees or conflicting definitions, keep `config/puffish_skills/` as the primary path and temporarily remove the Open Loader copy before deeper tuning.
