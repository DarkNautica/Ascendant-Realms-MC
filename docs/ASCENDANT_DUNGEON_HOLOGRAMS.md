# Ascendant Dungeon Holograms

Status: Elite Holograms dependency installed; helper auto-creation is currently suppressed.

Ascendant Ranked Dungeons will use Elite Holograms for world-space styled text above dungeon rifts. The target visual is a clean floating label like:

```text
D-RANK DUNGEON
Ruined Cellar Breach
Danger 2 | Loot uncommon_to_rare
```

The intended style is MiniMessage-based and lives in `config/ascendant_dungeons/dungeon_hologram_policy.json`.

## Why Elite Holograms

- It gives us persistent world-space hologram text without writing a custom renderer.
- It supports colored and gradient text styling.
- It fits the dungeon-rift use case better than HUD text because the label belongs in the world above the portal.

## Current Boundary

Elite Holograms is installed for future world-space rank text, but the helper no longer auto-creates holograms during this portal visual pass. Jayden observed that generated holograms displayed a yellow editor-instruction helper line above the intended dungeon title, so the current in-game gate presentation uses frameless item-display gate art, rank-colored particles, invisible light, and ambient sound instead.

## Planned Dungeon Label Rules

- One hologram per manual test entrance or future live dungeon rift.
- Hologram is anchored above the rift, not globally visible across the world.
- Hologram is cleaned up when the rift expires.
- Rank color must match the dungeon rank policy.
- Text should show rank, dungeon display name, danger tier, and loot tier.
- Holograms must not be used as decoration spam.

## First Test

After the next sync, launch a safe creative world and run:

```mcfunction
/ascdungeon spawn_test_here d_rank
/ascdungeon spawn_test_all_ranks 12
/ascdungeon cleanup_test
```

The helper does not currently use Elite Holograms' command bridge:

```mcfunction
/eh createat <id> <x> <y> <z> <world> <text>
/eh addline <id> <text>
/eh delete <id>
```

Expected result for this pass: no yellow Elite Holograms edit-instruction text appears. The report records that Elite Holograms is loaded but not created by the helper.
