# Structure Director Live v1

Generated: 2026-06-22T20:45:24+00:00

Structure Director Live v1 is the first reversible live structure-control pass. It changes newly generated worlds through OpenLoader datapack overrides and helper diagnostics. It does not add mods, place NPCs, inject Hunter Boards, add Guild Halls, rewrite loot, rewrite recipes, or change roads/bridges.

## Active Live Controls

- Live datapack: `config/openloader/data/ascendant_structure_director_live/`.
- Enabled policy: `config/ascendant_structures/live_structure_policy.json`.
- Rollback manifest: `config/ascendant_structures/rollback/pre_structure_director_v1/rollback_manifest.json`.
- Structure-set overrides active: 17.
- Biome-tag overrides active: 5.
- Land/water policy rules recorded: 4.
- Settlement overlap reductions active: 2.

## Important Honesty Boundary

Forge 47.4.20 does not expose a safe pack-owned structure placement veto event to this helper. Live v1 therefore uses real datapack controls now: spacing/separation, evidence-resolved biome tags, a dedicated vineyard structure set, and larger Integrated API terrain/biome context checks. The helper commands expose policy/context diagnostics. A true before-placement land/water veto remains a future mixin or generator-wrapper job.

## Known Manual Fixes

- Dragon roosts are rarer, keep land-biome tags, and exclude ocean/river/cave/wet biome IDs from their evidence-resolved tags.
- Dragon caves are rarer and remain underground content.
- `idas:abandoned_vineyard` is split out of broad `idas:idas_common` into `idas:abandoned_vineyard_director`, made rarer, and gets larger Integrated API context checks.
- `iceandfire:siren_island` remains ocean/deep-ocean content.
- IDAS replacement cases stay documented: gorgon temple can resolve to `idas:labyrinth`; graveyard can resolve to `idas:haunted_manor`.
