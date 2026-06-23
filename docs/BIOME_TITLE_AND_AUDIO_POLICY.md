
# Biome Title And Audio Policy

Generated: 2026-06-17T04:08:00+00:00

Status: audit/control scaffold only. No title resource pack, audio config, or UI config was changed by this pass.

## Audio Layer Audit

| Layer | Role | Present | Policy |
| --- | --- | --- | --- |
| AmbientSounds | biome/weather ambient texture | True | Use volume tuning before removal if regions sound too busy. |
| Biome Music | biome music variation | True | Future region playlists should map Atlas mood to biome pools, not names alone. |
| Presence Footsteps | ground material/body presence | True | Keep material feedback; verify snow/sand/stone footstep contrast in field tests. |
| Sound Physics Remastered | occlusion/reverb/spatial mix | True | Keep debug logging off; check caves/mountains for overpowering echo. |
| Medieval Music | resource-pack music identity | True | Supports broad fantasy tone; region-specific playlists remain future work. |

## Region Title Policy

| Region | Display title | Subtitle flavor | Color | Implementation |
| --- | --- | --- | --- | --- |
| `hearthlands` | The Crownlands | Safe roads, soft weather, and the first promise of the realm. | f0d68a | policy_only_not_live_region_trigger |
| `frostmarch` | The Frostmarch | Cold wind, old ice, and the long white road north. | 9bd8ff | policy_only_not_live_region_trigger |
| `sunreach` | Sunreach | Red dust, bright heat, and caravan tracks under a hard sky. | d99a4e | policy_only_not_live_region_trigger |
| `verdant_coast` | The Verdant Coast | Rain-wet leaves, river mouths, and the sound of distant surf. | 59bd70 | policy_only_not_live_region_trigger |
| `stoneback_highlands` | The Stoneback Highlands | Stone roads, echoing cliffs, and wind over old watchfires. | c7b27a | policy_only_not_live_region_trigger |
| `north_east_marches` | The North-East Marches | Cold rain, frozen river mouths, and dark coastal timber. | 7fcfb8 | policy_only_not_live_region_trigger |
| `north_west_marches` | The North-West Marches | Wind-cut ridges, black pines, and snow in the high passes. | a7c7d9 | policy_only_not_live_region_trigger |
| `south_east_wilds` | The South-East Wilds | Hot rain, red mud, and green growth fighting the desert. | 9fc96c | policy_only_not_live_region_trigger |
| `south_west_wilds` | The South-West Wilds | Broken mesas, dry canyons, and wind grinding stone to dust. | c98d57 | policy_only_not_live_region_trigger |
| `outer_rim` | The Outer Rim | The map thins, the sky bruises, and old powers press close. | 8c78a8 | policy_only_not_live_region_trigger |
| `nether_front` | The Nether Front | Heat, basalt, and warlight beyond the Overworld line. | c85a48 | policy_only_not_live_region_trigger |
| `end_expanse` | The End Expanse | A silent horizon where the world stops answering. | b78cff | policy_only_not_live_region_trigger |

## Current Title Stack Evidence

- Traveler's Titles biome titles enabled: True
- Traveler's Titles dimension titles enabled: True
- Pack-owned Traveler's Titles fallback keys: 207
- Region-specific title keys currently present: 0

## Implementation Boundary

Biome titles are currently live through Traveler's Titles. Atlas coordinate-region titles are not live-enforced yet. A future KubeJS/resource-pack or helper hook should display region names from `config/ascendant_atmosphere/title_policy.json` using Atlas region scoreboards, but that should wait until terrain and water review are accepted.
