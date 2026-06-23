# Atlas Hydrology Validation

Last updated: 2026-06-17.

## Reports

Runtime reports:

- `config/ascendant_atlas/reports/hydrology_grid_latest.json`
- `config/ascendant_atlas/reports/invalid_ocean_selections_latest.json`

Source registry and policy:

- `config/ascendant_atlas/biome_hydrology_registry.json`
- `config/ascendant_atlas/hydrology_policy.json`
- `config/ascendant_atlas/coastal_policy.json`

## Fresh-World Test

In a fresh validation world, run:

```mcfunction
/tp @s 2375 170 1895
/ascatlas hydrology_here
/ascatlas biome_decision_here
/ascatlas region_weights_here
/ascstructure here
```

Then run:

```mcfunction
/ascatlas dump_hydrology_registry
/ascatlas sample_transect 250 500 3000 3000 250
```

## Pass Conditions

- High dry land does not select `minecraft:ocean`.
- Ocean biome selection is allowed only in ocean/coast hydrology.
- Land biome selection in deep ocean is flagged unless it is an allowed island/coastline case.
- Structure context reports hydrology for land/water rules.
- `invalid_ocean_selections_latest.json` reports 0 invalid ocean selections on the tested transects.

## Still Manual

Jayden must visually confirm that the resulting terrain still looks natural and that water structures remain on real water.
