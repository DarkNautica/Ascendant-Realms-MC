# Ascendant Effects

A small KubeJS module for custom ambient effects in Ascendant Realms.

## v1 — Heat Haze (hot biomes)
`kubejs/server_scripts/ascendant_effects.js` + `config/ascendant_effects/effects.json`.

In hot biomes (base temperature >= threshold, e.g. desert / savanna / badlands / Nether) the
player sees a subtle warm **heat shimmer**: faint amber bands that ripple over the lower view,
stronger near the ground, plus sparse rising heat particles.

It's drawn on the 2D HUD layer via the KubeJS Painter, so it renders **over shaderpacks**
(Complementary/Oculus) — unlike a true post-process distortion shader, which Oculus hides.

### Tuning (config/ascendant_effects/effects.json)
- `enabled` — master toggle.
- `temperature_threshold` — biome base temp counted as hot (1.5 default; lower = more biomes).
- `intensity` / `max_alpha` — strength of the shimmer (keep low for subtlety).
- `band_count`, `region_top`, `region_bottom` — shimmer density and screen area.
- `repaint_interval_ticks` — 2 = smoother, higher = lighter on multiplayer.
- `particles_enabled`, `particle`, `particle_chance` — the rising heat particles.

### Applying changes
Server script + config: run `/reload` in-game (no relaunch needed) to apply edits.

## Adding more effects
Add new effect blocks to the config and new functions in `ascendant_effects.js`, gated by
their own conditions, painting via `player.paint({...})` (overlay) or `/particle` (in-world).
