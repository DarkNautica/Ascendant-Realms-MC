# Custom Hotbar (Minecraft 1.20.1)

## Where the hotbar asset lives
The hotbar is part of the GUI atlas, not a standalone file:
`assets/minecraft/textures/gui/widgets.png`  (256x256)
inside the version jar: `curseforge/minecraft/Install/versions/1.20.1/1.20.1.jar`.

`widgets.png` here was extracted straight from your 1.20.1 jar — open it in Aseprite.

## Regions inside widgets.png (see widgets_REFERENCE.png)
- HOTBAR ............ 182 x 22 at (0,0)   <- the 9-slot bar (each slot 20px wide, 1px border)
- selected selector . 24 x 24 at (0,22)   <- the white box on the selected slot
- offhand slot ...... 24 x 24 at (0,46)
- (the gray bars + lock icons below are vanilla buttons / recipe-book toggles)

## Editing tips (Aseprite)
- Edit the FULL widgets.png; keep it 256x256, RGBA (transparent background), don't resize the canvas.
- Only repaint the hotbar/selector pixels; leave the other regions intact so buttons etc. still work.
- You CAN make it higher-res (e.g. 512x512 = 2x, or 1024x1024 = 4x) as long as the layout stays
  proportional — Minecraft scales it. Keep the same relative positions/sizes.
- Turn on a 1px grid (or 20px for slots) to line up the slots.

## How to use your custom hotbar
Put your edited file in a resource pack at:
`<pack>/assets/minecraft/textures/gui/widgets.png`
then enable that pack at the TOP of the resource-pack list (highest priority).
Press F3+T in-game to hot-reload while iterating.

Note: 1.20.1 uses this single widgets.png atlas. (1.20.2+ split the GUI into
gui/sprites/hud/*.png — not relevant here.)
