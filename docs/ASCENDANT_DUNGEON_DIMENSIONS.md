# Ascendant Dungeon Dimensions

Status: controlled random rift testing active.

The first playable ranked dungeon loop now uses a pack-owned OpenLoader dimension:

- Dimension ID: `ascendant_dungeons:ranked_dungeon`
- Datapack: `config/openloader/data/ascendant_realms_dungeons/`
- Policy: `config/ascendant_dungeons/dungeon_dimension_policy.json`
- Helper command: `/ascdungeon open_test_rift <rank>`

## What Works Now

- `/ascdungeon open_test_rift <rank>` creates a visible ranked gate at the player.
- The helper builds a randomized room chain inside `ascendant_dungeons:ranked_dungeon`.
- The helper force-loads the dungeon build area, uses chunk-safe fill slices, and writes a guaranteed spawn platform before saving the teleport target.
- The first room is a safe entry room with no hostile mob spawns and only supply-tier utility loot.
- Every generated run ends with a boss room.
- Rank changes room count, enemy count, modded mob pool, palette, boss identity, boss strength, and loot ceiling.
- Chests, barrels, mob drops, and boss drops use pack-owned `ascendant_dungeons` loot tables instead of vanilla simple-dungeon placeholder loot.
- Gate visuals are frameless: item-display gate texture, invisible light, rank-colored particles, and nearby ambient portal sound.
- `/ascdungeon open_test_rift <rank>` and random rifts attempt a direct Immersive Portals visual surface for the entrance first. The return-side surface is created only after boss defeat.
- Walking into the overworld gate sends the player into the dungeon.
- `/ascdungeon spawn_random_now` creates a timed random world rift near the player for direct spawn testing.
- Gate visuals are fixed-facing item displays with randomized rank-scaled size ranges.
- The boss-room return gate is not built at dungeon creation. It spawns only after the tagged boss is defeated.
- Walking into the boss-room return gate sends the player back near the original gate after the boss is dead.
- `/ascdungeon enter_latest` and `/ascdungeon return_latest` exist as fallbacks.
- `/ascdungeon return_latest` is locked until boss defeat.
- `/ascdungeon cleanup_instance` removes the latest generated dungeon volume, force-load entry, test mobs, entrance marker, gate display, and hologram.
- `/ascdungeon cleanup_rank <rank>` removes only that rank's generated dungeon/rift slot so other active ranks can stay open.

## What Is Still Test/Placeholder

- The room generator is command-built test geometry, not final authored structure-pool content.
- Room visuals are a first V1 pass using vanilla-safe structure shells plus modded dungeon decor assets where available.
- Enemy and boss pools are rank-scaled but still need Jayden visual/combat review.
- Immersive Portals visual surfaces are now attempted, but native Immersive Portals teleporting is intentionally disabled for this pass. The helper's server-side walk-in trigger remains the travel authority so room spawn safety is preserved.
- Autonomous random dungeon spawning is enabled only as a controlled one-active-rift-per-rank live test. It is not the final event director.

## Gate Art

Jayden's five gate assets from `gate-art/` are now staged in:

`resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/gate/`

The current frameless gates render those textures through `minecraft:item_display` entities using `minecraft:paper` CustomModelData. The display models use the runtime copies under `resourcepacks/ascendant-dungeon-gates/assets/ascendant_dungeons/textures/item/` so Minecraft stitches them into the item atlas correctly:

- D rank: 9101, blue gate.
- C rank: 9102, green gate.
- B rank: 9103, purple gate.
- A rank: 9104, gold gate.
- S rank: 9105, red gate.

The resource pack `file/ascendant-dungeon-gates` must stay enabled in `options.txt` and `config/resourcepackoverrides.json`. `config/ascendant_dungeons/reports/dungeon_instance_latest.json` records whether Immersive Portals visual surfaces were created.

## Test Route

Use a fresh or safe creative world after sync/relaunch:

```mcfunction
/ascdungeon status
/ascdungeon spawn_random_now
```

Then walk into the gate. You should land on a solid built floor inside a safe first room, not fall through the sky/void and not immediately get mob-swarmed. Confirm the return gate is absent before the boss dies, defeat the boss, then confirm the return gate appears.

Fallbacks:

```mcfunction
/ascdungeon enter_latest
/ascdungeon return_latest after boss defeat
/ascdungeon cleanup_instance
```

Repeat for higher ranks only after D-rank works:

```mcfunction
/ascdungeon open_test_rift c_rank
/ascdungeon open_test_rift b_rank
/ascdungeon open_test_rift a_rank
/ascdungeon open_test_rift s_rank
```

Clean between same-rank runs with `/ascdungeon cleanup_rank <rank>`, or clear the latest test run with `/ascdungeon cleanup_instance`.

## Current Dungeon Content Expectations

- Safe entry room: no mobs, supply barrel/chest only.
- Combat rooms: connected room chain, modded decorative assets, rank-scaled hostile packs, occasional room loot.
- Final room: boss spawn and boss reward chest. Return gate appears after boss defeat.
- D/C ranks should feel like real early dungeon content without dropping endgame gear.
- B/A/S ranks are now technically generated but should be treated as combat and loot review targets before random spawning is enabled.
