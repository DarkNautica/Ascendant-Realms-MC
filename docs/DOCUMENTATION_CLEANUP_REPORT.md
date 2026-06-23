# Documentation Cleanup Report

Generated: 2026-06-17.

Status: documentation-only cleanup. No gameplay configs, worldgen configs, loot tables, recipes, structures, mobs, roads, villages, Hunter Boards, Guild Halls, NPC placement, or menu behavior were changed.

## What Changed

- `README.md` was shortened into a current orientation page.
- The former long README batch/session narrative was preserved intact in `docs/archive/BATCH_HISTORY.md`.
- `AGENTS.md` was refreshed so future sessions read the current live handoff and respect the Atlas terrain gate.
- `docs/TESTING_CHECKLIST.md` now opens with a note that older batch sections are historical unless current docs point to them for retest.
- `docs/DOCS_INDEX.md` now treats `docs/archive/BATCH_HISTORY.md` and this report as part of the navigation map.
- `docs/CURRENT_STATUS.md` now records this documentation cleanup pass and the active documentation boundaries.
- `scripts/check-pack.py` now validates documentation hygiene rules.

## Reviewed

- `README.md`
- `AGENTS.md`
- `docs/CURRENT_STATUS.md`
- `docs/DOCS_INDEX.md`
- `docs/AI_MODPACK_HANDOFF.md`
- `docs/TESTING_CHECKLIST.md`
- `docs/ASCENDANT_ATLAS_WORLDGEN.md`
- `docs/ATLAS_TERRAIN_VALIDATION_REPORT.md`
- `docs/ATLAS_WORLDGEN_FAILURES.md`
- Major generated/audit docs listed in `docs/DOCS_INDEX.md`

## Findings

- README was the largest source of navigational drift. It mixed current status with old batch narrative, survival notes, fixes, and installed-mod history.
- `CURRENT_STATUS.md` is still the newest live state and correctly says terrain is not signed off while water/visual review remains open.
- `DOCS_INDEX.md` is the authority map and now points to the archive instead of asking future sessions to eventually create it.
- Atlas docs already separate active system, validation reports, failure reports, and blocked/manual-review items well enough for the current pass.
- The active Atlas helper exists and is documented as live in the current handoff, Atlas docs, and README.
- `TESTING_CHECKLIST.md` remains long but useful. It now carries a warning that current blockers come from `CURRENT_STATUS.md`.
- Generated indexes were not moved under `docs/generated/` in this pass because many docs and checker rules still reference their current paths. Moving them safely needs a separate reference-rewrite pass.

## Current Documentation Truths

- Ascendant Atlas is active through `ascendant_atlas_regions` and the OpenLoader Overworld override.
- Automated Atlas biome-source and surface validation pass.
- Terrain is not signed off.
- Current terrain blockers are south/west ocean-leak water review, incomplete/insufficient water-body classification coverage, and pending visual terrain review.
- Roads, bridges, villages, settlements, Hunter Boards, Guild Halls, NPC placement, and civilization generation must wait until terrain/water acceptance.
- Loot, recipe, structure, travel, atmosphere, magic, balance, player progression, NPC visual, and UI clarity systems are mostly audit/control scaffolds unless their docs explicitly say live behavior is enabled.

## Validation Added

`scripts/check-pack.py` now warns if:

- README grows back into running handoff spam.
- README contains old batch install narrative.
- duplicate `##` headings appear in `docs/TESTING_CHECKLIST.md`.
- docs under `dist/` are referenced as source instead of generated export copies.
- `docs/CURRENT_STATUS.md` stops mentioning the current terrain/water blockers.
- stale helper-mod phrases return in current source docs.

## Not Changed

- No generated index files were manually rewritten.
- No generated docs were moved under `docs/generated/`.
- No gameplay config or data pack behavior was changed.
- No active CurseForge instance sync was performed.

## Follow-Up

- Keep new session handoffs in `docs/CURRENT_STATUS.md`, not README.
- Keep old batch details in `docs/archive/BATCH_HISTORY.md`.
- Move generated indexes under `docs/generated/` only in a dedicated pass that updates all references and checker rules together.
