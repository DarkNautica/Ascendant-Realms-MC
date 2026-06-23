# Ascendant Realms Compatibility Resource Fixes

This local resource pack contains tiny compatibility assets that preserve active mod functionality while preventing missing-resource warnings.

Current fixes:

- `assets/minecraft/textures/models/armor/wizard_layer_1.png`
- `assets/minecraft/textures/models/armor/wizard_layer_1_overlay.png`
- `assets/minecraft/textures/models/armor/cultist_layer_1.png`
- `assets/minecraft/textures/models/armor/geomancer_armor_layer_1.png`
- `assets/minecraft/textures/models/armor/netherite_layer_1_overlay.png`
- `assets/minecraft/textures/models/armor/netherite_layer_2_overlay.png`
- `assets/minecraft/textures/models/armor/wandering_magician_layer_2.png`

These are visual-only fallback armor textures for renderer paths that ask for vanilla-namespace armor textures that the owning mod stores under its own namespace or does not expose as a split layer. The Iron's Spells fallbacks are mirrored from the active Iron's Spells jar, and the Geomancer fallback is mirrored from the active Mowzie's Mobs item texture. They do not change item IDs, recipes, loot, structures, gameplay, or server behavior.
