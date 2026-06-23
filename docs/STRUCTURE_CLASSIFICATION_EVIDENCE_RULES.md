# Structure Classification Evidence Rules

Generated: 2026-06-18T01:57:55+00:00

This is the evidence contract for the Ascendant Structure Director. It fixes the previous bad inference where English words in mod labels or structure IDs were treated as placement truth.

## Evidence Strength

- Strong: manual/live locate evidence, resolved biome tags or biome IDs, structure-set rules, structure JSON placement fields, template pool/NBT evidence, and sampled block palettes.
- Medium: registry class, registry integration hooks, loot/policy linkage, and worldgen type/step.
- Weak: structure ID words, namespace/path words, template-pool words, mod display names, and English labels such as ice, ocean, ship, water, desert, cave, village, dragon, sky, or boss.

## Hard Rules

- Weak hints are recorded in `name_hints_weak_only` and must never be the only evidence for a final sensitive classification.
- Water, frozen-ocean, ocean, sky, sea-floor, village/town, boss, and dungeon classifications must carry non-name evidence and a confidence score.
- If evidence is weak or conflicting, the row must set `manual_review_required=true`.
- IDAS replacement cases are classified from the active generated structure, not only the requested Ice and Fire locate name.
- Candidate overrides stay disabled until Jayden approves a specific live change after in-game review.
