# AGENTS.md

This repo is for Ascendant Realms, a vanilla+++ medieval fantasy RPG exploration modpack. It is a separate project from `crownfall-colonies`.

## First Read

Future Codex sessions should read these before acting:

1. `docs/CURRENT_STATUS.md`
2. `docs/DOCS_INDEX.md`
3. `docs/AI_MODPACK_HANDOFF.md`
4. `docs/ATLAS_TERRAIN_VALIDATION_REPORT.md`
5. `docs/ATLAS_WORLDGEN_FAILURES.md`

Use `docs/archive/BATCH_HISTORY.md` only for historical archaeology.

## Current Project Rules

- Do not modify `crownfall-colonies` while working on this repo.
- Do not add MineColonies unless Jayden explicitly requests it later.
- Do not add new mods unless the current task asks for mod installation.
- Do not use Sinytra Connector, OptiFine, or Fabric-only mods in this Forge pack unless Jayden explicitly creates an experimental branch.
- Packwiz is initialized for Minecraft `1.20.1` Forge `47.4.20`, pack version `0.1.0-alpha`.
- Keep docs updated whenever a system moves from candidate, audit-only, or scaffolded into live/enforced behavior.
- Do not rewrite generated indexes by hand. Regenerate them or document findings.

## Terrain Gate

Ascendant Atlas is active through the local `ascendant_atlas_regions` helper and the OpenLoader Overworld override, but terrain is not signed off while south/west water review and visual terrain review remain open.

Do not move to roads, bridges, villages, settlements, Hunter Boards, Guild Halls, NPC placement, or civilization generation until `docs/ATLAS_TERRAIN_VALIDATION_REPORT.md` and `docs/ATLAS_WORLDGEN_FAILURES.md` say the terrain/water blockers are resolved.

## Validation

After source changes, run:

```powershell
packwiz refresh
python scripts\check-pack.py
```

Worldgen changes require fresh-world or ungenerated-chunk evidence. Old worlds are not valid terrain proof.

## Design Goal

The pack should feel unified: beautiful terrain, coherent medieval structures, dangerous mobs, readable loot progression, satisfying movement/combat, and polished visuals. Avoid random kitchen-sink additions and avoid a single forced boss-campaign endgame.
