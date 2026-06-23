# Ascendant Dungeon Spawn Testing

Status: controlled random ranked rift testing active. Generated dungeon instance testing is available through `/ascdungeon spawn_test_here <rank>`, `/ascdungeon open_test_rift <rank>`, and `/ascdungeon spawn_random_now`.

This is the first real in-world visual entrance test surface for Ascendant Ranked Dungeons, plus the first controlled random world-rift pass. It gives Jayden commands that create frameless ranked dungeon entrances on demand, force one timed random rift near the player, then remove them cleanly.

Use `docs/ASCENDANT_DUNGEON_DIMENSIONS.md` for the playable generated-dungeon test route.

## Active Commands

```mcfunction
/ascdungeon status
/ascdungeon spawn_test_here d_rank
/ascdungeon spawn_visual_here d_rank
/ascdungeon spawn_test_all_ranks 12
/ascdungeon open_test_rift d_rank
/ascdungeon spawn_random_now
/ascdungeon enter_latest
/ascdungeon return_latest
/ascdungeon cleanup_instance
/ascdungeon cleanup_rank d_rank
/ascdungeon cleanup_test
```

## What The Spawn Test Creates

- A temporary frameless ranked entrance at the command location.
- An animated rank gate texture from `resourcepacks/ascendant-dungeon-gates`.
- A circular teleportable Immersive Portals surface fitted inside the gate art.
- A transparent-center gate item texture so the real portal view is visible through the circle instead of being covered by the art.
- Invisible light blocks so the rift illuminates nearby space.
- Rank-colored particles and portal ambient sound.
- No visible stone/glass frame blocks.
- No helper-created Elite Holograms label during this pass, because the mod currently adds an unwanted yellow editor-instruction helper line.
- No fallback armor-stand nameplate during this pass; the gate art and particles carry the visual identity.
- `config/ascendant_dungeons/reports/dungeon_spawn_test_latest.json`.

## What Random Rift Testing Adds

- `/ascdungeon spawn_random_now` forces one timed random rift near the player on safe footing if at least one eligible rank slot is open.
- Natural random rifts are enabled with one active rift per rank, an initial delay, low attempt chance, and rank rarity weights.
- Five active world rifts can exist at once: one D, one C, one B, one A, and one S.
- D-rank rifts are most common; higher ranks are rarer, larger, and distance-gated.
- The entrance closes after its timer. If nobody entered, the instance cleans up; if the player entered, the dungeon remains active.
- No exit/return gate exists before the boss dies.
- The return gate appears only after the tagged dungeon boss is defeated.
- After first entry, the entrance should stay open about 5 seconds, then shrink out before disappearing.

## What It Does Not Do Yet

- It does not support duplicate active rifts of the same rank.
- `/ascdungeon spawn_test_here <rank>` now opens a real generated dungeon rift, matching the intuitive test behavior.
- `/ascdungeon spawn_visual_here <rank>` and `/ascdungeon spawn_test_all_ranks <spacing>` are visual-only gate-art checks. They do not teleport.
- It does not rewrite loot, recipes, rank gates, Hunter Boards, Guild Halls, NPC placement, roads, villages, or structures.

## Visual Review

Run the all-ranks command in a safe creative test world:

```mcfunction
/ascdungeon spawn_test_all_ranks 12
```

Check:

- Do D/C/B/A/S ranks read clearly from a distance?
- Do the animated gate textures appear instead of vanilla paper or missing models?
- Is there no yellow Elite Holograms edit-instruction text?
- Do the rank colors feel right?
- Does the gate feel like a magical rift without visible support blocks?
- Do particles and nearby ambient sound feel cool without being obnoxious?
- Does `/ascdungeon cleanup_test` remove the gate displays, old nameplates, old holograms, and invisible light blocks?

The next implementation step after this passes is visually balancing the generated dungeon side and deciding which room shapes should become authored templates. The current helper creates circular teleportable Immersive Portals surfaces during `/ascdungeon open_test_rift <rank>`, `/ascdungeon spawn_test_here <rank>`, and `/ascdungeon spawn_random_now`, and now uses rank-bounded dungeon loot tables inside generated instances.

## Boss-Locked Exit Test

Use a safe creative world:

```mcfunction
/ascdungeon cleanup_instance
/ascdungeon status
/ascdungeon spawn_random_now
walk into the gate
confirm the entrance stays open briefly for a second player, then shrinks out
confirm the first room is safe
confirm there is no return gate in the boss room before boss defeat
defeat the boss
confirm the return gate appears
/ascdungeon return_latest
/ascdungeon cleanup_instance
```

Use `/ascdungeon cleanup_rank <rank>` if one rank slot needs to be cleared without removing the other active rifts.
