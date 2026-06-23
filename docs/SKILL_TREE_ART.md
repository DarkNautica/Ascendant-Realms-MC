# Ascendant Web - Skill Tree Art (Arcane Void)

Custom visual overhaul of the Puffish Skills `ascendant` category. Theme: **Arcane Void**
(deep indigo nebula, glowing rune-ring nodes), with the **7 branch lanes color-coded** and
**custom per-node glyph icons**.

## What changed

- `category.json` `background` -> custom `ascendant:textures/skilltree/background.png`
  (1024x1024 nebula, `position: fill`). Category icon -> the root glyph.
- Every definition's `frame` -> `type: texture`, pointing at lane/tier frames
  (`<lane>_<tier>_{available,unlocked}.png`). Locked/excluded auto-darken (Puffish).
- Every definition's `icon` -> `type: texture`, a custom 16x16 lane-colored glyph
  (`icons/<node>.png`). Glyph is chosen from the node id/title keywords.

Tiers map from the old advancement frames: `task -> normal`, `goal -> notable`,
`challenge -> major` (more ornate ring per tier).

Lane colors: warrior red, rogue violet, ranger green, arcanist blue, engineer gold,
survivalist teal, dragonbound orange, root (ascendant) white-cyan.

## Where the files live

- Textures: `kubejs/assets/ascendant/textures/skilltree/` (background, `frames/`, `icons/`).
  Served by the always-on KubeJS resource pack, so no resource-pack toggling is needed.
- Config: `config/puffish_skills/categories/ascendant/` (authoritative; what the instance
  loads). The `datapacks/` and `openloader/data/ascendant_realms_skills/` mirrors were
  updated to match.

## Regenerating

From the repo root:

```
python scripts/generate-ascendant-skilltree-art.py     # builds bg, 48 frames, 113 icons
python scripts/apply-skilltree-art.py config/puffish_skills/categories/ascendant [mirrors...]
python scripts/generate-ascendant-skilltree-layout.py config/puffish_skills/categories/ascendant [mirrors...]
```

## Web layout

`generate-ascendant-skilltree-layout.py` rewrites `skills.json` (positions),
`connections.json`, and the category connection colors:

- Root at center; each lane grows its **own organic branch** (seeded per lane, so no two
  branches share a shape), tasks inner -> goals mid -> challenge capstones outer, with
  wide spacing + collision avoidance so nodes don't overlap.
- Connections are **unidirectional** `[prerequisite, dependent]` = the real unlock order.
  Every node has exactly one prerequisite chain back to the root (verified reachable
  before writing), so the lines show what you must unlock first.
- `category.json` -> `colors.connections.unlocked` is set to a luminous cyan-white, so
  connections **between two unlocked nodes glow** (your traveled path) while everything
  beyond keeps Puffish's default neutral look. Note: Puffish connection colors are
  per-state **category-wide**, not per-lane, so the glow is one color (the nodes carry
  the lane color via their frames/icons).

Spacing, radii bands, branch spread, child cap, and the glow color are constants at the
top of the script.

Palette, lane colors, the glyph library, and the keyword->glyph map are constants at the
top of `generate-ascendant-skilltree-art.py`. To change a single node's icon, adjust the
keyword map (or add a per-node override) and rerun both scripts.

## Applying in-game

Puffish reads the category config at startup, so a **relaunch** is needed (textures alone
reload with F3+T, but the frame/icon definition swap needs the config reload). Open with `K`.
