# Ascendant Structure Director

Generated: 2026-06-18T01:57:55+00:00

This is the v1 Structure Director control pass. It does not add mods, does not place NPCs, does not inject villages, does not add Hunter Boards or Guild Halls, and does not rewrite loot or recipes. It turns the existing worldgen audit into a pack-owned map for region fit, vertical layer, water/sky placement, density risk, danger tier, loot tier, and review priority. Structure Director Live v1 is now active as a reversible OpenLoader datapack plus helper diagnostics; see `docs/STRUCTURE_DIRECTOR_LIVE_V1.md`.

## Status

- Mode: live v1 active for newly generated chunks, with evidence/candidate files retained for audit.
- Structures classified: 579.
- Structure sets classified: 330.
- Water structures: 22.
- Sky structures: 14.
- Sea-floor structures: 4.
- Ship/ocean-surface structures: 13.
- Dungeons: 111.
- Boss/dragon structures: 38.
- Village/town/settlement structures: 109.
- Review-only density candidates retained: 70.
- Live v1 changes active: 23.
- Live v1 structure-set/structure JSON overrides: 17.
- Live v1 biome-tag overrides: 5.
- Live v1 land/water context policy rules: 4.
- Live v1 settlement overlap reductions: 2.
- Classification confidence: {'medium': 33, 'strong': 543, 'weak': 3}.
- Manual-review rows: 13.
- Name-only final classifications: 0.

## Authority Files

- `config/ascendant_structures/structure_registry.json`
- `config/ascendant_structures/structure_evidence_registry.json`
- `config/ascendant_structures/structure_classification_confidence.json`
- `config/ascendant_structures/manual_structure_observations.json`
- `config/ascendant_structures/structure_region_rules.json`
- `config/ascendant_structures/structure_vertical_layer_rules.json`
- `config/ascendant_structures/structure_density_policy.json`
- `config/ascendant_structures/structure_set_overrides.json`
- `config/ascendant_structures/water_structure_policy.json`
- `config/ascendant_structures/sky_structure_policy.json`
- `config/ascendant_structures/sea_floor_structure_policy.json`
- `config/ascendant_structures/ship_structure_policy.json`
- `config/ascendant_structures/dungeon_structure_policy.json`
- `config/ascendant_structures/boss_structure_policy.json`
- `config/ascendant_structures/village_structure_policy.json`
- `config/ascendant_structures/structure_test_points.json`

## Director Rules

- Names, namespace/path words, template-pool words, and mod labels are weak hints only. They must never be the only evidence for water, frozen-ocean, sky, sea-floor, village/town, boss, or dungeon classifications.
- Crownlands/Hearthlands stay beginner-friendly. Bosses, dragons, and high-danger dungeons must not become common starter landmarks.
- Sunreach and Stoneback are land-first. Ocean/ship/sea-floor structures need explicit coastline, ocean, frozen-ocean, or wetland context.
- Verdant Coast owns most lush/coastal/oceanic structure identity. Frostmarch owns frozen-ocean and ice-themed water content.
- Sky structures must be rare and manually reviewed for visual noise before any density increase.
- Village/town structures are not injected into new village pools in this pass. Existing generation is only audited for overlap, density, and region fit.
- Structure loot and danger tier are policy-only here. No loot rewrites or rank gates are enabled.

## Current Blockers

- Dense structure families still need manual review before any live spacing changes.
- Some IDAS, Moog, Integrated Villages, and Towns and Towers structures have broad biome selectors and need in-game spot checks.
- A true pre-generation land/water placement veto still requires a later mixin or generator-wrapper implementation. Live v1 uses what is safely available now: structure-set spacing/separation, evidence-resolved biome tags, a dedicated vineyard set, larger Integrated API context checks for the vineyard, rollback snapshots, and `/ascstructure` diagnostics.
