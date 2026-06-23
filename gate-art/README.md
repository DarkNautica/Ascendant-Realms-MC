# Ascendant Gate — rift visuals (assets only)

Solo Leveling "gate" — a swirling **vortex** portal: a white-hot core with cyan spiral arms
winding outward, fading to deep blue/black at the edges. Animated by rotation in a seamless
loop. Visuals only; no blocks, dimensions, or logic.

## Built for Immersive Portals (see-through)
The texture is **translucent**, not a solid disc, so Immersive Portals' live view of the
destination shows through it:
- Gaps between the arms are very transparent (you see straight through to the other side).
- The arms are a semi-opaque glowing veil; the white-hot core is the most opaque but still
  lets a little through.
- The outer edge feathers to fully transparent, so there's no hard rectangle around the rift.

Brightest pixels cap at ~88% opacity on purpose — keep it that way if you regenerate, or the
portal will start to occlude the destination view.

## Files
- `gate.png` — the vortex sprite. 64x64 per frame, **32-frame vertical strip** (64x2048).
  The swirl rotates a full turn across the strip, so it loops seamlessly in time.
- `gate.png.mcmeta` — Minecraft animation config (`frametime: 1`, `interpolate: true`).
- Rank-color variants (same format, each with its own `.mcmeta`):
  - `gate_purple.png` — Monarch purple
  - `gate_red.png` — high-rank red
  - `gate_gold.png` — gold
  - `gate_green.png` — green
  - blue (`gate.png`) = default, matching the Arcane Void / shadow theme.

## How to use (when you wire it up later)
- It's a single centered sprite (round vortex on a transparent background). Map it onto the
  Immersive Portals portal plane / a display entity / billboard so the mod renders the
  destination behind the translucent swirl. Add a faint bloom in your shader for the SL look.
- 64px per frame (modern-res). Downscale to 16/32px if you want chunkier pixels.

## Previews
- `PREVIEW_gate_hero.png` — large still of the blue vortex over a destination scene.
- `PREVIEW_gate_seethrough.png` — portal over the destination vs. the texture alone, so you
  can see the transparency.
- `PREVIEW_gate_colors.png` — all five colors over the destination scene.
- `PREVIEW_gate_anim.png` — eight frames across the rotation loop.
- `PREVIEW_gate_in_world.png` — frameless rift mockup with bloom.

## Regenerate / tweak
`python scripts/generate-ascendant-gate-art.py` — palette ramps (`RAMPS`), frame count (`N`),
size (`S`), arm count (`ARMS`), spiral tightness (`TWIST`), and the see-through opacity caps
(`A_MAX` / `A_MIN`) are constants at the top. Add ramps to `RAMPS` for more rank colors.


## Moving wisps layer (layer1)
Each rift now renders TWO animated layers via its item model:
- `layer0` = the vortex (`gate*.png`) — spins, white-hot core, defined outer rim.
- `layer1` = wisps (`gate_wisps*.png`) — orbiting energy tendrils + outward-drifting embers,
  color-matched, moving independently from the vortex for a layered, living look.

Both are 64x64 x 32-frame seamless loops. Models live in
`resourcepacks/ascendant-dungeon-gates/.../models/item/gate_<color>.json`
(`layer0` + `layer1`). Regenerate everything with
`python scripts/generate-ascendant-gate-art.py` (vortex constants + `WISP_COL` at the top).
