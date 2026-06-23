# Atlas Region Gradients

Last updated: 2026-06-17.

## Current Rule

Atlas region influence is now continuous and domain-warped. Region boundaries should read as broad travel gradients, not straight invisible cuts.

The helper still reports a primary pool for validation, but biome candidates may come from secondary weighted regions when they are close enough and hydrology-compatible.

## What Changed

- Hard dominance slice logic was removed from the biome-source decision path.
- The land-bias density function now blends south, southeast, west, and southwest influence through continuous weights.
- Deterministic low-frequency domain warp breaks straight sector lines.
- Region weights are written by `/ascatlas region_weights_here` and `/ascatlas dump_gradient_policy`.

## Required Transects

Southeast Wilds to Sunreach:

- Use 250 to 500 block steps across the visible cutoff zone.

Northward gradient:

- `/ascatlas sample_transect 0 0 0 -15000 500`
- `/ascatlas sample_transect 500 0 500 -15000 500`
- `/ascatlas sample_transect -500 0 -500 -15000 500`

Acceptance needs visual confirmation that snow/cold influence grows northward without random green/snow/green flips unless elevation or terrain context explains it.
