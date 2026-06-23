# Structure Visual Review Findings

Generated: 2026-06-17T20:52:00-04:00

This records Jayden's first in-game Structure Director route feedback. It is review evidence only. It does not enable live structure overrides, move files into OpenLoader, inject Hunter Boards or Guild Halls, place NPCs, alter villages, roads, bridges, loot, recipes, magic gates, or rank gates.

## Summary

- Most reviewed structures looked good.
- The reported failures are placement/context problems, not structure model problems.
- Main recurring issue: some land structures appear as islands in water like oceans or lakes.
- Confirmed log source: `C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)\logs\latest.log`.
- Review evidence JSON: `config/ascendant_structures/structure_visual_review_findings_latest.json`.
- Disabled candidate notes: `config/ascendant_structures/candidates/structure_land_placement_candidates.json`.
- Full evidence audit: `docs/STRUCTURE_CLASSIFICATION_EVIDENCE_RULES.md`, `docs/STRUCTURE_CLASSIFICATION_AUDIT_REPORT.md`, `config/ascendant_structures/structure_evidence_registry.json`, and `config/ascendant_structures/structure_classification_confidence.json`.

## Findings

| Structure | Result | Evidence | Classification | Next Action |
| --- | --- | --- | --- | --- |
| `iceandfire:*_dragon_roost` | Jayden reported dragon roosts spawning as islands in oceans/lakes. | Visual report; exact roost locate lines were not present in `latest.log`. | `land_structure_water_terrain_misplacement` | Candidate land-only biome/region lock; do not enable live until retested. |
| `idas:abandoned_vineyard` | Spawned as an island in water and in the wrong Atlas region. | Located at `[9568, ~, 9264]`; `/ascatlas here` near it reported `south_east_wilds`, `terralith:hot_shrubland`. | `land_structure_water_terrain_misplacement_and_region_fit_mismatch` | Candidate per-structure lock; avoid broad `idas:idas_common` changes. |
| `iceandfire:gorgon_temple` -> `idas:labyrinth` | IDAS override happened, but Jayden said the labyrinth looked good. | IDAS override chat at log line 5500; `idas:labyrinth` located at `[2704, ~, 14816]`; Atlas region `sunreach`. | `acceptable_mod_override` | Document only unless later placement looks bad. |
| `iceandfire:graveyard` -> `idas:haunted_manor` | IDAS override happened. | IDAS override chat at log line 5730. | `mod_override_needs_followup_visual_review` | Continue if haunted manor placement looks wrong. |

## Source Correction Applied

The Structure Director generator had a classification bug: it used the source mod label while inferring biome families. Because the source mod label was `Ice And Fire Community Edition`, the word `Ice` made several non-ocean Ice and Fire structures look like frozen-ocean structures.

Fixed in source:

- Names, namespace/path words, template-pool words, and mod labels are weak hints only and are stored as `name_hints_weak_only`.
- Final sensitive classifications now carry `evidence_source`, `confidence`, `classification_reason`, `manual_review_required`, and `name_only_classification`.
- `source_mod` is no longer authoritative biome-family evidence.
- `frost_cold`, `ocean`, and `frozen_ocean` are separated; broad tags with a few wet/ocean-capable biomes no longer create water roles by themselves.
- Ice and Fire non-siren structures no longer get `water_role=frozen_ocean` or `water_role=ocean` merely because of `Ice`, `fire`, `graveyard`, beach-adjacent tags, or broad climate tags.
- Dragon roosts, dragon caves, gorgon temple, graveyard, cyclops cave, hydra cave, and related Ice and Fire land structures now keep `water_role=none` unless actual non-name evidence proves water placement.
- `iceandfire:siren_island` remains an ocean/sea-surface structure because its actual biome tag resolves to ocean evidence.
- IDAS replacements are documented as active generated structures: `iceandfire:gorgon_temple` -> `idas:labyrinth`, and `iceandfire:graveyard` -> `idas:haunted_manor`.

## Current Boundary

Do not enable a live structure-set override yet. The next safe move is a focused candidate pass for land-only placement rules, starting with dragon roosts and `idas:abandoned_vineyard`. Broad IDAS changes are risky because `idas:idas_common` contains many structures and some of them looked good.
