# Ascendant Realms Dungeons

This OpenLoader datapack defines the controlled ranked dungeon test dimension and the first rank-bounded dungeon loot tables.

The dimension is intentionally empty and flat/void-like. The helper builds one ranked dungeon instance at a time with `/ascdungeon open_test_rift <rank>`, then cleans it with `/ascdungeon cleanup_instance`.

Loot tables live under `data/ascendant_dungeons/loot_tables/`:

- `chests/ranked_supply.json` for the safe first room.
- `chests/<rank>_rank_room.json` for combat-room containers.
- `chests/<rank>_rank_boss.json` for final-room boss rewards.
- `entities/<rank>_rank_mob.json` for ranked mob drops.
- `entities/<rank>_rank_boss.json` for ranked boss drops.

Autonomous random dungeon spawning is still disabled.
