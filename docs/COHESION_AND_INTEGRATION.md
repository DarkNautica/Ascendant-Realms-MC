# Cohesion And Integration

Status: Batch N installed and validated.

Batch N is the cohesion layer. It does not add a new combat tier; it connects the existing systems so villages, dungeons, loot, food, Create, Farmer's Delight, Alex's Mobs, IceAndFire CE, Cataclysm, Marium, Bountiful, Artifacts, Iron's Spells, and the custom skill tree can feel like one designed pack.

The top-level long-term blueprint now lives in `docs/ASCENDANT_REALMS_SEAMLESS_INTEGRATION_MASTER_PLAN.md`. Use this file for Batch N status and installed-tool notes; use the master plan for how every system should ultimately connect.

Installed core systems:

- KubeJS: primary script layer for future recipes, tags, and pack glue.
- Rhino: KubeJS dependency.
- Open Loader: global datapack/resource-pack loader.
- Almost Unified: material and recipe unification.
- Almost Unify Everything: server-side add-on for broader unification coverage.
- Polymorph: recipe conflict fallback UI.
- Every Compat (Wood Good): wood/block compatibility generator.
- Moonlight Lib: Every Compat and Supplementaries dependency.
- Create Slice & Dice: Create automation for Farmer's Delight processing.
- Alex's Delight: Alex's Mobs plus Farmer's Delight food bridge.

Installed world integration systems:

- Integrated Villages: active because villages still felt bland after CTOV was removed.
- IDAS: Integrated Dungeons and Structures.
- Integrated API: dependency for the Integrated structure stack.
- Supplementaries: dependency pulled by IDAS.
- Quark and Zeta: dependencies pulled by IDAS, with Zeta added explicitly because Packwiz did not add it automatically.

Delayed:

- CraftTweaker: delayed because KubeJS is the chosen script layer.
- LootJS: delayed until a loot scripting pass approves exact support and syntax.
- Paxi: delayed because Open Loader is enough for the current global datapack goal.
- Item Obliterator: delayed until a later item-cleanup review.
- Integrated Dungeons Arise: delayed until When Dungeons Arise is installed.

Batch N validation passed through client creative/system and dedicated server boot/join testing.

## World Integration Audit Pass

Status: staged and validated.

The current pass scanned the active client instance jars and generated `docs/WORLD_INTEGRATION_AUDIT.md`.

Key inventory:

- 64 jars with world/data integration surfaces.
- 623 structures and 333 structure sets.
- 1,586 template pools.
- 696 placed features and 631 configured features.
- 98 biome modifiers and 614 biome tags.
- 4,324 loot tables and 10,551 recipes.
- 1,065 item tags and 145 entity type tags.

Immediate integration actions:

- Repaired the shared Integrated Villages `integrated_api:workstation_processor` POI-cast crash path with static `minecraft:rule` workstation replacements under the active OpenLoader path.
- Repaired Integrated Villages' broken `minecraft:village` structure tag by removing only nonexistent `integrated_villages:swamp_village`.
- Staged generated configs from the active client for structure, spawn, mob, loot, and block integration systems.
- Kept KubeJS recipe/tag/loot scripts non-invasive; no broad recipe/loot rewrites are made until validation proves the current stack is stable. The progression HUD and Ascendant Core loader are active KubeJS bridges.

Current stance:

- Do not add more worldgen/village/dungeon packs yet. The pack has enough content volume; the next work is targeted tuning, stable generation, loot balance, and cross-mod recipes.
