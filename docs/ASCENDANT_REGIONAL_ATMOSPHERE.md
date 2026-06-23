
# Ascendant Regional Atmosphere

Generated: 2026-06-17T04:08:00+00:00

Status: audit/control scaffold only. This pass did not change terrain, mobs, ores, structures, weather configs, audio configs, or title resource packs.

## Summary

- Region atmosphere rows: 12
- Warm regions allowing snow buildup: 0
- Weather snow guardrails currently documented: Weather2 outside-cold buildup blocked, Serene Seasons blanket snow/ice disabled, Snow Real Magic warm-biome melt enabled.
- Atlas region titles are policy-only; current Traveler's Titles support is biome/dimension title presentation, not coordinate-region title enforcement.

## Region Atmosphere Matrix

| Region | Title | Music mood | Weather mood | Snow buildup | Danger mood |
| --- | --- | --- | --- | --- | --- |
| `hearthlands` | The Crownlands | warm medieval strings, light flute, calm travel themes | temperate rain and fair skies; storms should feel rare and readable | False | safe but not sterile; danger should be signposted and sparse |
| `frostmarch` | The Frostmarch | low drones, lonely horns, glassy bells, restrained percussion | snow, blizzards, frozen fog, and hard winter visibility where safe | True | survival pressure, cold isolation, frozen-ocean threat |
| `sunreach` | Sunreach | dry percussion, oud-like plucks, sparse desert travel lines | dry, hot, dusty, storm-scarred; rain should be uncommon and snow forbidden | False | exposed, thirsty, bright, predator-visible |
| `verdant_coast` | The Verdant Coast | lush strings, hand drums, rainstick-like texture, coastal motifs | wet, lush, stormy, coastal; lightning and heavy rain fit better than snow | False | dense, alive, hard to see through, ambush-friendly |
| `stoneback_highlands` | The Stoneback Highlands | low drums, hammered strings, mountain horns, sparse stone ambience | windy, mountainous, exposed; rain and fog fit, broad snow does not | False | vertical, exposed, echoing, hard to cross |
| `north_east_marches` | The North-East Marches | frost strings blended with wet coastal ambience | cold coastal storms, sleet-like mood, frozen crossings | True | cold coastal frontier |
| `north_west_marches` | The North-West Marches | frost drones with mountain horns and stone percussion | cold mountain weather; snow allowed where biome data supports it | True | cold, vertical, exposed |
| `south_east_wilds` | The South-East Wilds | humid percussion with desert plucks and low strings | hot coastal storms and monsoon mood; no snow | False | lush but heat-stressed and unstable |
| `south_west_wilds` | The South-West Wilds | desert percussion with stone drones and tense low brass | hot, arid, storm-carved; no snow or cold-season buildup | False | dry, cracked, remote, predator territory |
| `outer_rim` | The Outer Rim | oppressive drones, broken choirs, sparse drums, corrupted ambience | dangerous, oppressive, region-by-biome; do not blanket snow warm samples | conditional_cold_biome_only | oppressive, ancient, high-rank, dangerous |
| `nether_front` | The Nether Front | low infernal drones, basalt percussion, distant ritual tones | dimension atmosphere only; no Overworld storm control | False | hostile, infernal, advanced |
| `end_expanse` | The End Expanse | void pads, distant choir, sparse crystalline pulses | dimension atmosphere only; no Overworld storm control | False | silent, alien, capstone |

## Current Presentation Stack

- Weather: Weather2, Serene Seasons, Snow Real Magic, Auroras, Enhanced Celestials.
- Audio: AmbientSounds, Biome Music, Presence Footsteps, Sound Physics Remastered, Medieval Music resource pack.
- Titles/UI feedback: Traveler's Titles, Titles, Visual Titles, Visual Traveler's Title Biomes Addon, pack-owned `ascendant-realms-travelers-titles`.

## Important Boundary

This is a regional presentation policy. It does not prove terrain signoff and does not replace the Atlas water review. Terrain remains partial until the south/west ocean-leak samples are resolved or accepted through manual review.
