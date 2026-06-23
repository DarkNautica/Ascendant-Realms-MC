# UI Clarity And Feedback Audit

Generated: 2026-06-17T05:01:19Z

Status: audit/control scaffold only. No menu redesign, no new UI mods, no live progression locks, and no gameplay tuning were enabled.

## Summary Counts

- Tangible registry item IDs checked: 1460
- Tangible item borders missing: 0
- Item border color mismatches: 0
- Tangible rarity tooltip gaps: 0
- Non-inventory spell IDs without item tooltips, expected: 113
- Required title/visual resource packs missing from options: 0
- UI sync coverage gaps: 0
- Death waypoint clutter policy: active; current death marker stays visible, old Xaero death markers are hidden from world UI

## Surface Audit

| Surface | Status | Evidence |
| --- | --- | --- |
| Item Borders | clean | 1460 tangible item IDs covered; 0 color mismatches |
| Rarity Tooltips | clean | 0 tangible item tooltip gaps; 113 spell IDs are not inventory items |
| Legendary Tooltips | compatible | frame styling only; Item Borders owns rarity color |
| JEI | compatible | Runic Grimoire alias only; no material hiding found |
| Loot Beams | aligned | rarity color on, item-name color off, rare+ style filter |
| Loot Journal | aligned | pickup UI on; long-term item-history tracking off |
| MobHealthBar | policy-ready | health bar available; name text is disabled so Ascendant Nametags owns styled rank/name identity |
| Traveler's Titles | partly live | biome/dimension titles live; Atlas coordinate-region titles policy-only |
| Immersive UI / SpiffyHUD | manual review | installed, but no source-side tuning file found in this pass |
| FancyMenu | unchanged | no menu redesign in this audit |
| Xaero Death Waypoints | active cleanup | current deathpoint remains on; old deathpoints are disabled during sync to prevent repeated-death world/HUD clutter |

## Current Interpretation

The current player-facing item identity stack is mostly coherent. Item Borders uses manual registry colors, KubeJS adds the readable rarity line, Legendary Tooltips provides frame styling, and Loot Beams is set to use rarity color rather than item-name color.

The two intentional boundaries are threat tiers and Atlas region titles. MobHealthBar can show health on hover, damage, or aggro, but its plain name line is disabled because it duplicated AI hunter rank text in white and fought the Ascendant Nametags renderer. Traveler's Titles can show biome and dimension titles, but Atlas coordinate-region titles remain policy-only until a runtime title hook exists.

Xaero death waypoint clutter is now handled as a client UI policy rather than a gameplay/death-system change. The exact ideal behavior is old deathpoints visible only within 100m, but Xaero's exposed profile has only a global waypoint distance cap. The safe active behavior is current death visible and old deathpoints hidden/disabled, documented in `docs/DEATH_WAYPOINT_UI_POLICY.md`.

## Review Notes

- Keep `config/ascendant_index/gear_registry.json` as the canonical item rarity/color source.
- Treat `config/ascendant_index/rarity_schema.json` and `config/ascendant_core/loot_rarity_rules.json` color differences as legacy policy drift until they are regenerated against the current palette.
- Do not use item rarity color as player rank color. Rank/nameplate color can rhyme with rarity, but the surfaces mean different things.
- Do not make JEI hide duplicate materials from this UI pass. Material unification belongs to Almost Unified and the materials/recipe policies.
- Do not use `waypoint_max_distance=100` as the deathpoint fix, because it would also hide the current death marker.
