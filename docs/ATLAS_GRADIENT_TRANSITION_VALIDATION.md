# Atlas Gradient Transition Validation

Last updated: 2026-06-17.

## Reports

- `config/ascendant_atlas/reports/region_gradient_grid_latest.json`
- `config/ascendant_atlas/reports/transition_transects_latest.json`

## Test Commands

Run these in a fresh validation world:

```mcfunction
/ascatlas dump_gradient_policy
/ascatlas sample_transect 250 500 3000 3000 250
/ascatlas sample_transect 0 0 0 -15000 500
/ascatlas sample_transect 500 0 500 -15000 500
/ascatlas sample_transect -500 0 -500 -15000 500
```

## Visual Questions

- Does the southeast/Sunreach transition avoid a straight terrain wall?
- Does north trend cold over distance without random warm land returning farther north?
- Do region weights change gradually between adjacent samples?
- Does elevation explain any local cold/snow pocket?
- Does Verdant water/coast identity survive without labelling high dry cliffs as ocean?

## Status

This pass is a source/runtime correction, not final terrain acceptance. Terrain can be marked accepted only after Jayden confirms the fresh-world visuals.
