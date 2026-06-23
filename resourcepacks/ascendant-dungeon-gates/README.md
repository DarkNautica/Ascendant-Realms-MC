# Ascendant Dungeon Gates

Ranked gate textures imported from `gate-art`.

These assets are tracked and bound to item-display models for the manual ranked dungeon test loop. The helper summons `minecraft:item_display` entities using `minecraft:paper` with CustomModelData values 9101-9105 so the D/C/B/A/S gates can show animated textures without adding a new block or mod registry entry.

The original imports live under `textures/gate/` as source/reference copies. The runtime item-display models intentionally reference `textures/item/` copies because Minecraft reliably stitches item-model sprites from the item texture atlas path. If the models point at `ascendant_dungeons:gate/...`, the portal renders as the magenta/black missing texture checkerboard.

Model map:
- 9101: `ascendant_dungeons:item/gate_blue`
- 9102: `ascendant_dungeons:item/gate_green`
- 9103: `ascendant_dungeons:item/gate_purple`
- 9104: `ascendant_dungeons:item/gate_gold`
- 9105: `ascendant_dungeons:item/gate_red`
