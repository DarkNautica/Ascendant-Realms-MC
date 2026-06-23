# Ascendant Player HUD (Unified, native-style)

Drawn with the KubeJS Painter API from `kubejs/server_scripts/ascendant_progression.js`.

## Look
- **XP bar** — a continuous vanilla-style bar in **blue** at the vanilla XP-bar spot,
  drawn as rectangles (dark border + groove + 3-row beveled fill) so it reads like the
  real bar. A faceted **level-badge shield** sits at its left with the level number on it.
- **Mana bar** — same vanilla-style bar in **cyan**, stacked just above, from Iron's
  Spells `MagicData`. Iron's own mana bar is off (`manaBarDisplay = "Never"`).
- **Skill points** — a 9x9 faceted gem (Minecraft HUD pixel ratio) + native count, right side.
- All text is the **native Minecraft font at scale 1**. No panel/frame.

## Why bars are drawn, not textured
The KubeJS Painter dynamic **texture-fill** path is unreliable in this pack (an earlier
in-game test fell back from it). So the bar fills are plain rectangles (reliable), while
the **static** icons (level badge, skill gem) are PNG textures.

## Assets / data
- Icons: `kubejs/assets/ascendant/textures/gui/hud/` — `level_badge.png` (shield),
  `sp_gem.png`. Regenerate with `python scripts/generate-ascendant-hud-art.py [1.20.1.jar]`
  (the unused `xp_*`/`mana_*` track/fill PNGs are kept for reference; the bars are drawn).
- The script also mirrors level/XP/SP to `ar_skill_*` scoreboards.

## Tuning
`config/ascendant_progression/progression.json` -> `hud`: `enabled`, `mana_enabled`,
`show_values`, and text colors. Bar/badge/gem positions + bar colors are constants in
`paintAscendantProgressionHud`.

## Notes
- Health / armor / air stay on OverflowingBars (unchanged).
- Mana read is defensive: if the Iron's API can't be reached, the mana bar hides and logs
  one warning; XP/level keep working.
- The badge + gem are static textures; if they ever fail to render that's the Painter
  texture bug, and they'd need a drawn-rect fallback.
- Painter/KubeJS load at startup -> relaunch to see HUD changes.


## HUD position (bottom-left)
The custom progression cluster (level badge + blue XP bar + cyan mana bar + skill-point gem)
is drawn in the **bottom-left corner**, not bottom-center, to avoid crowding vanilla health/
hunger/armor and the hotbar. Bars are 90px wide so the cluster clears the hotbar at every GUI
scale (verified to GUI scale 4). Positions live in `paintAscendantProgressionHud` in
`kubejs/server_scripts/ascendant_progression.js`.
