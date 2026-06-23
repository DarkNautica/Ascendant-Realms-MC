# Ascendant Ranked Dungeons

Status: rank-slot random world rifts active.

Ascendant Ranked Dungeons are the next progression layer after the random-worldgen rollback and Structure Director work. The intent is to create rare dungeon rifts that are ranked like Guild content: D, C, B, A, and S. These are not normal village structures, not Hunter Boards, and not road/civilization content.

## What Is Live Now

- Immersive Portals is now a Packwiz-managed dependency for the dungeon portal layer.
- Elite Holograms is Packwiz-managed for future dungeon rank text above rifts, but helper auto-creation is disabled in the current visual pass because it displayed an unwanted editor-instruction helper line.
- `config/ascendant_dungeons/` owns the ranked dungeon policy, rank registry, spawn policy, portal policy, and first dungeon templates.
- The local helper exposes the current command surface:
  - `/ascdungeon status`
  - `/ascdungeon roll <rank>`
  - `/ascdungeon preview_here <rank>`
  - `/ascdungeon spawn_test_here <rank>`
  - `/ascdungeon spawn_visual_here <rank>`
  - `/ascdungeon spawn_test_all_ranks <spacing>`
  - `/ascdungeon open_test_rift <rank>`
  - `/ascdungeon enter_latest`
  - `/ascdungeon return_latest`
  - `/ascdungeon cleanup_instance`
  - `/ascdungeon cleanup_rank <rank>`
  - `/ascdungeon cleanup_test`
  - `/ascdungeon dump_policy`
- The spawn-test commands create temporary frameless ranked entrances with animated gate textures, invisible light blocks, rank-colored particles, nearby ambient sound, reports, and cleanup.
- `/ascdungeon spawn_test_here <rank>` and `/ascdungeon open_test_rift <rank>` create one generated dungeon instance in `ascendant_dungeons:ranked_dungeon`, with force-loaded build safety, a safe no-mob entry room, connected randomized rooms, modded decor assets, rank-scaled modded enemy pools, bounded dungeon loot tables, and a mandatory boss room.
- `/ascdungeon spawn_visual_here <rank>` and `/ascdungeon spawn_test_all_ranks <spacing>` are visual-only gate-art checks and do not teleport.
- `/ascdungeon spawn_random_now` force-creates the same kind of timed random world rift near the player for direct testing.
- The timed random scheduler is enabled as a controlled live-test layer: after an initial delay it attempts rare safe-surface rifts while keeping one active rift per rank, for five active rifts total.
- Portal gate art is fixed-facing instead of billboarded, and portal size is randomized by rank. Higher ranks have larger size ranges and lower spawn weights. Current size ranges are D `3.8-4.7`, C `4.2-5.3`, B `4.9-6.4`, A `5.8-7.5`, and S `6.8-9.0`.
- `/ascdungeon open_test_rift <rank>` and random world rifts create a direct circular Immersive Portals surface for the overworld entrance. The surface is teleportable and should own normal walk-through travel; helper enter/return commands are fallback/admin tools only.
- Walking into the gate enters the dungeon.
- After the first player enters, the entrance remains open for 5 seconds for party members, then shrinks out before removal.
- The boss-room return gate does not spawn during initial generation. It appears only after the tagged dungeon boss is defeated, and `/ascdungeon return_latest` is locked until then.

## Controlled Random Spawn Rules

- One active dungeon rift may exist for each rank: D, C, B, A, and S. That means five active rifts total, but never two of the same rank.
- Natural timed attempts start after about 12 minutes in a world, then check about every 90 seconds with a low spawn chance.
- Rifts choose a safe solid surface near a player and avoid water, lava, ice, air, and magma surfaces.
- D-rank is the common test case; C/B/A/S are progressively rarer and distance-gated.
- A rift entrance is timed. If nobody enters before it expires, it cleans itself up. If a player has entered, the entrance closes but the dungeon remains active until boss/cleanup flow is resolved.
- First entry starts a short party grace timer instead of instantly closing the entrance.
- No exit gate spawns until the boss is defeated.

This is still a controlled V1, not the final authored event director. The current multi-rift behavior is intentionally limited to one slot per rank.

## Rank Model

- D-Rank: first public dungeon tier, small breach, common to uncommon rewards with a light rare edge.
- C-Rank: standard contract dungeon, uncommon to rare rewards.
- B-Rank: major dungeon, rare rewards with controlled epic material chances.
- A-Rank: elite breach, epic rewards with very limited legendary material chances.
- S-Rank: ascendant breach, legendary material chase rewards only under manual review before live spawning.

The current policy keeps rank as guidance and validation. It does not hard-lock content yet.

## Implementation Boundary

This pass does not:

- add new structure mods;
- inject villages;
- place Hunter Boards or Guild Halls;
- rewrite loot;
- rewrite recipes;
- enable magic or rank gates;
- change roads or bridges;
- change terrain.

## Next Test

In a fresh or safe creative test world, run:

```mcfunction
/ascdungeon status
/ascdungeon spawn_random_now
walk into the gate or run /ascdungeon enter_latest
confirm there is no return gate before the boss is defeated
defeat the boss
confirm the return gate appears
/ascdungeon return_latest
/ascdungeon cleanup_instance
/ascdungeon dump_policy
```

Use `/ascdungeon cleanup_rank <rank>` when you only want to clear one rank slot and keep the other active rifts alive.

If those pass and the generated rooms feel acceptable as a first test loop, the next implementation step is visual balance/template refinement and tightening the generated dungeon room set. The portal should already be a circular teleportable Immersive Portals surface, not a square visual plate behind the gate art.

## Dungeon Side V1

The current generated dungeon side is still command-built, but it is no longer a bare placeholder loop:

- Room 1 is a safe entry room with no mob spawns and supply-only utility loot.
- Middle rooms use connected halls, rank-colored accents, Create-style metal/bar decor where available, Born in Chaos/Block Factory style dark dungeon dressing where available, containers, debris, and elite encounter variations.
- Combat mobs now use rank-scaled modded pools from Born in Chaos, Iron's Spells, Cataclysm, Mowzie's Mobs, and Block Factory's Bosses where appropriate.
- Mob deaths point at `ascendant_dungeons:entities/<rank>_rank_mob` and boss deaths point at `ascendant_dungeons:entities/<rank>_rank_boss`.
- Chest/barrel rewards point at `ascendant_dungeons:chests/ranked_supply`, `<rank>_rank_room`, and `<rank>_rank_boss`.
- Rewards are intentionally rank-bounded. They should feel better than normal trash loot, but D/C should not hand out endgame gear and S-rank remains manual-review content.
