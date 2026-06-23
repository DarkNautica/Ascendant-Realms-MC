# Dungeon And Loot Integration

Status: Batch N installed and validated.

Installed:

- IDAS: Integrated Dungeons and Structures
- Integrated API
- Supplementaries
- Quark
- Zeta

Existing dungeon/loot stack:

- YUNG's Better Dungeons
- YUNG's Better Mineshafts
- YUNG's Better Strongholds
- YUNG's Bridges
- YUNG's Extras
- MVS
- MSS
- MES
- Cataclysm
- Marium's Soulslike Weaponry
- IceAndFire CE
- Artifacts
- Loot Integrations
- Bountiful
- Iron's Spells
- Immersive Portals for (Neo)Forge is now added as the planned ranked-dungeon rift layer. See `docs/ASCENDANT_RANKED_DUNGEONS.md` and `docs/DUNGEON_PORTAL_SYSTEM.md`.

Current audit result:

- `docs/WORLD_INTEGRATION_AUDIT.md` found 623 structures, 333 structure sets, 1,586 template pools, and 4,324 loot tables across the active jar set.
- This is enough content for a full world; the next work is targeted tuning and validation, not adding more structure packs.

Design intent:

- Dungeon chests should eventually contain useful spell scrolls and spell materials.
- Rare structures should contain Artifacts and high-rarity materials.
- Boss drops should feed crafting, skill-tree milestones, and Bountiful contracts.
- Loot Integrations remains the first passive loot bridge; KubeJS/LootJS work comes later only if needed.
- Ranked dungeon rifts should use the same loot economy and Guild rank guidance, but no broad loot rewrites are enabled by the first portal foundation pass.

Risk notes:

- IDAS overlaps with YUNG, Moog structures, Cataclysm structures, and existing density tuning.
- Structure density may become too high before balance tuning.
- Loot may become too generous if Artifacts, Iron's Spells, Cataclysm, Marium, and IceAndFire rewards stack unchecked.

Validation notes:

- Generate a fresh creative test world.
- Locate several dungeons/large structures.
- Confirm no placement crash.
- Confirm chest loot opens without missing item crashes.
- Confirm IDAS, YUNG structures, Moog structures, Cataclysm, Marium, Iron's Spells, Artifacts, and Loot Integrations can coexist without immediate loot or placement failures.
- Keep full loot/balance tuning for a later pass.
