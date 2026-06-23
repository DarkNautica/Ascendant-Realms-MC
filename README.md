# Ascendant Realms

Ascendant Realms is a vanilla+++ medieval fantasy RPG exploration modpack for two-player multiplayer. The goal is a beautiful, dangerous, progression-rich world with coherent regions, readable loot, satisfying combat, magic, ambience, seasons/weather, and visual polish.

This is not a MineColonies pack. Do not add MineColonies unless Jayden explicitly asks later.

## Start Here

Use these docs in order when continuing the project:

1. `docs/CURRENT_STATUS.md` - newest live state, blockers, and next test checklist.
2. `docs/DOCS_INDEX.md` - authority map for current, generated, and historical docs.
3. `docs/AI_MODPACK_HANDOFF.md` - full mod list and interaction map for another AI.
4. `docs/ATLAS_RANDOM_WORLDGEN_RESTORE.md` - current rollback from Atlas-directed terrain to random Tectonic/Terralith generation.
5. `docs/ATLAS_WORLDGEN_FAILURES.md` - historical Atlas terrain blockers and why the rollback happened.
6. `docs/TESTING_CHECKLIST.md` - broad client/server validation checklist.
7. `AGENTS.md` - standing rules for future Codex sessions.

Ignore duplicate Markdown under `dist/`; export copies can lag behind source.

## Current Reality

- Minecraft `1.20.1`, Forge `47.4.20`, pack version `0.1.0-alpha`.
- Packwiz is the source package manager. Use `packwiz refresh` after source file changes.
- Ascendant Atlas terrain influence is disabled. The pack is back to random Tectonic/Terralith Overworld generation.
- The local Forge helper jar `ascendant-atlas-regions-0.1.0.jar` may remain installed for diagnostics/history, but it must not be referenced by the active Overworld dimension or continentalness override while random mode is selected.
- Tectonic and Terralith should provide the normal random terrain/biome baseline.
- Structure and road tuning should proceed against that random baseline, not against compass-directed north/south/east/west terrain.

## Hard Boundaries

- Do not re-enable Atlas north/south/east/west terrain or biome steering unless Jayden explicitly asks to reopen that system.
- Do not judge the rollback in old generated chunks. Use a fresh world or fully ungenerated chunks after syncing the active instance.
- Do not add new mods unless Jayden explicitly asks for that task.
- Do not rewrite generated indexes by hand. Regenerate or document findings instead.
- Do not treat audit/control scaffolds as live-enforced systems unless the docs say they are actually enabled and validated.

## Validation Commands

Run these from the repo root after documentation or config changes:

```powershell
packwiz refresh
python scripts\check-pack.py
```

Worldgen changes also need fresh-world or ungenerated-chunk testing. Old worlds are not valid evidence for terrain changes.

## Historical Batch Log

The previous long README batch narrative was archived intact at:

- `docs/archive/BATCH_HISTORY.md`

Use it for archaeology only. Current direction lives in `docs/CURRENT_STATUS.md` and `docs/DOCS_INDEX.md`.
