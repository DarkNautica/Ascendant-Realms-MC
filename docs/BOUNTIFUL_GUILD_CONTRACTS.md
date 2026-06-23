# Bountiful Guild Contracts

Status: first live Ascendant Guild Bountiful pools are generated through Open Loader.

The source candidate list is `config/ascendant_guild/generated_bounty_targets.json`. This pass selects a controlled subset and writes Bountiful pools into `config/openloader/data/ascendant_realms_guild/data/bountiful/`.

## Active Board Pools

| Board | Selected Targets |
|---|---:|
| `village_hunter_board` | 79 |
| `town_guild_board` | 23 |
| `major_guild_registry` | 51 |

## Reward Spine

- Village Hunter Boards reward `kubejs:guild_mark`, emeralds, arrows, and food.
- Town Guild Boards reward `kubejs:hunter_seal`, Guild Marks, iron, and XP bottles.
- Major Guild Registries reward `kubejs:ascendant_sigil`, Hunter Seals, diamonds, and rare totems.

## Safety Rules

- Technical entities, eggs, projectiles, CustomNPC internals, and Easy NPC internals are filtered out.
- This pass does not force every generated target live at once.
- Boss and dragon contracts are rare/major-board targets and still need balance tuning after worldgen validation.
