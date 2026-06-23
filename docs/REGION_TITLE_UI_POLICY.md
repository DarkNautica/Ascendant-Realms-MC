# Region Title UI Policy

Generated: 2026-06-17T05:01:19Z

Status: policy scaffold only. Traveler's Titles biome/dimension titles are live; Atlas coordinate-region titles are not live-triggered yet.

## Current Stack

- `config/travelerstitles-forge-1_20.toml` enables biome and dimension titles.
- `resourcepacks/ascendant-realms-travelers-titles` supplies fallback title keys and colors.
- `config/ascendant_atmosphere/title_policy.json` defines the Atlas region title language.
- `config/resourcepackoverrides.json` and `options.txt` keep visual title packs active and ordered.

## Region Rules

| Region | Display | Status |
| --- | --- | --- |
| hearthlands | The Crownlands | policy_only_not_live_region_trigger |
| frostmarch | The Frostmarch | policy_only_not_live_region_trigger |
| sunreach | Sunreach | policy_only_not_live_region_trigger |
| verdant_coast | The Verdant Coast | policy_only_not_live_region_trigger |
| stoneback_highlands | The Stoneback Highlands | policy_only_not_live_region_trigger |
| north_east_marches | The North-East Marches | policy_only_not_live_region_trigger |
| north_west_marches | The North-West Marches | policy_only_not_live_region_trigger |
| south_east_wilds | The South-East Wilds | policy_only_not_live_region_trigger |
| south_west_wilds | The South-West Wilds | policy_only_not_live_region_trigger |
| outer_rim | The Outer Rim | policy_only_not_live_region_trigger |
| nether_front | The Nether Front | policy_only_not_live_region_trigger |
| end_expanse | The End Expanse | policy_only_not_live_region_trigger |

## Validation Snapshot

- Missing region title policy rows: 0
- Required title/visual packs missing: 0
- Resource pack order conflicts: 0
- Atlas region title runtime hook live: no

## Boundary

Do not treat biome-title fallback keys as proof that coordinate-region titles are live. A future runtime hook must connect Atlas region scoreboards to title events before this becomes an implemented region feedback system.
