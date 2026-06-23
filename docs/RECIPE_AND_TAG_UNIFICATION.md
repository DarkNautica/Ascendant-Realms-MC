# Recipe And Tag Unification

Status: Batch N installed and validated.

Installed:

- KubeJS
- Rhino
- Almost Unified
- Almost Unify Everything
- Polymorph

KubeJS scaffold:

- `kubejs/server_scripts/ascendant_recipes.js`
- `kubejs/server_scripts/ascendant_tags.js`
- `kubejs/server_scripts/ascendant_loot_notes.js`
- `kubejs/README.md`

The current KubeJS recipe/tag/loot files are intentionally safe scaffolds. They should not alter recipes, tags, loot, or items until a focused integration pass confirms exact item ids and recipes in JEI. Other KubeJS bridges are active for the progression HUD, JEI aliasing, rarity tooltip labels, Guild starter items, and Ascendant Core manifest loading.

Current audit inventory:

- `docs/WORLD_INTEGRATION_AUDIT.md` found 10,551 recipes, 1,065 item tags, and 145 entity type tags in the active jar set.
- Use the audit as the first map for duplicate materials, food/knife/cooking bridges, Create/Farmer's Delight/Slice & Dice overlap, and mob-drop tags.
- Do not activate KubeJS rewrites until the current world-integration retest passes.

Unification policy:

- Use Almost Unified for obvious duplicate commodities.
- Use Polymorph as a user-facing fallback when more than one recipe still exists.
- Use KubeJS for known, tested recipe corrections.
- Do not use Item Obliterator yet.

Safe unification targets:

- common ingots
- common nuggets
- common dusts
- common plates/gears if duplicated
- common raw ore and storage blocks if duplicated

Protected materials:

- dragon materials
- Cataclysm boss drops
- Marium legendary materials
- Iron's Spells spell materials
- Artifacts
- Create unique mechanisms
- Bountiful-specific items
- custom skill-tree milestone items

Validation notes:

- Confirm JEI loads.
- Confirm Polymorph UI appears on a known duplicate recipe if one exists.
- Confirm Almost Unified does not merge unique boss, spell, dragon, or artifact items.
- Confirm no KubeJS script errors appear during startup.
- Confirm common duplicates are visible before writing removal/unification scripts; do not guess item IDs.
