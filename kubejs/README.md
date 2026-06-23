# Ascendant Realms KubeJS

Status: Batch N scaffold only.

KubeJS is installed as the pack's primary scripting layer. CraftTweaker stays delayed unless KubeJS proves insufficient.

Most server scripts are intentionally conservative comment scaffolds. They should load without changing gameplay until a focused recipe/tag pass is approved and tested.

Active client-side script:

- `client_scripts/ascendant_rarity_tooltips.js` inserts one generated rarity label into indexed gear tooltips. It places the label under native damage/speed/stat lines and before mod behavior lines such as attack range. It does not show backend effect/index/reason text, mutate item classes, or change vanilla rarity fields.

Active startup scripts:

- `startup_scripts/ascendant_gear_rarity.js` is no-op metadata for the generated rarity registry.
- `assets/kubejs/models/item/` and `assets/kubejs/textures/item/` provide starter visuals for Guild Mark, Hunter Seal, and Ascendant Sigil so the registered Guild/Hunter currency items do not render as missing-texture cubes.
- `startup_scripts/ascendant_guild_items.js` creates starter Guild currency concept items.

Planned responsibilities:

- unify duplicate recipes after Almost Unified reports the real conflicts
- add cross-mod recipes for Farmer's Delight, Create, Slice & Dice, Alex's Mobs, Iron's Spells, IceAndFire CE, Cataclysm, and Marium where needed
- define shared tags for monster parts, dragon materials, boss trophies, spell materials, cooked foods, and engineering parts
- support future Bountiful contract hooks and skill-tree milestone hooks

Do not add aggressive item deletion here. Use Item Obliterator later only after a separate balance review.
