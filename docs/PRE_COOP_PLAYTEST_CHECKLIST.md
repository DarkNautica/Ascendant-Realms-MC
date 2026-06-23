# Pre Co-op Playtest Checklist

Status: planning checklist for a multi-hour Jayden + brother playtest.
Date: 2026-06-22.

This is the short list of things to fix or verify before treating the pack as ready for a real several-hour session. It separates true blockers from issues that can be watched and recorded during play.

## Must Fix Before The Session

1. Resource Pack Overrides mismatch is fixed and synced.
   - Source and active `Ascendant Realms (2)` now list `file/ascendant-realms-buttons` in `config/resourcepackoverrides.json`.
   - Resource packs should stay aligned with `options.txt`.

2. KubeJS client script syntax fix is applied and synced.
   - `kubejs/client_scripts/ascendant_jei_aliases.js` now closes the `if (Platform.isLoaded('jei'))` block with a plain closing brace.
   - This should clear the latest active-log `client_scripts:ascendant_jei_aliases.js#14` syntax error after relaunch.

3. Missing IDAS savanna biome tag fix is applied and synced.
   - The Structure Director generator now filters missing `projectvibrantjourneys:baobab_fields` out of generated live biome tags.
   - Source and active Structure Director Live v1 datapack hashes match at `540DD32065EE85CF861812B268BE567E51CB088112F1A844CD00569D570ABDDD`.
   - This should clear the latest active-log `Couldn't load tag idas:has_structure/savannas` error after relaunch.

4. Re-run the basic pack checks after any new fixes.
   - `packwiz refresh`
   - `python scripts/check-pack.py`
   - Latest source result after the village-audio and resource-pack fixes: check passed with warnings only.

5. Sync the active instance after fixes while Minecraft is closed.
   - Use the existing active-client sync workflow.
   - Confirm the active instance has the same fixed configs/scripts as source.

6. Test the synced village audio reverb fix.
   - Sound Physics settings were reduced after villages sounded like caves.
   - After relaunch, test one open village and one village near cliffs or stone buildings.

## Must Verify In A Short Smoke Test

1. Launch `Ascendant Realms (2)` and reach the main menu without crash.
2. Create or load a fresh test world and confirm no invalid-player-data bounce.
3. Check the latest log for:
   - no KubeJS script errors
   - no OpenLoader/datapack load errors
   - no CustomNPCs script errors
   - no missing required shader/resource-pack pack failures
4. Confirm resource packs stay enabled after one restart.
5. Confirm Complementary/Reimagined shaders either work acceptably or are intentionally disabled for the playtest.
6. Confirm JEI opens and the Runic Grimoire/Patchouli guide search does not error.
7. Confirm death waypoint behavior:
   - current/latest death visible
   - old repeated deaths do not flood the screen.
8. Confirm keybind basics:
   - `K` Ascendant Web
   - `L` Quest Log
   - `R` spell wheel
   - `V` cast
   - `B` backpack
   - `G` Curios
   - `U` waypoints
   - `Y` minimap settings
9. Confirm village audio:
   - open-air villages should no longer sound like caves
   - caves/dungeons should still have stronger enclosed reverb

## Co-op Specific Setup

1. Decide whether the session is local single-player LAN or dedicated server.
2. If dedicated server:
   - rebuild/materialize server staging from the current active client
   - boot server
   - both players join
   - run a 10 to 15 minute stability test near spawn and one generated village.
3. If LAN:
   - host enters first, opens LAN
   - brother joins
   - both disconnect/rejoin once before committing to the long session.
4. Confirm both clients use the same pack state and resource packs.

## Gameplay Systems To Spot Check

1. Mob density.
   - Hostile/daytime spawning was intentionally increased.
   - Before the long session, walk around day and night for 10 minutes.
   - Confirm the world feels active without instant spawn-camping or village wipeouts.

2. Villages and guards.
   - Visit one village during day and night.
   - Confirm Guard Villagers/MCA villagers do not instantly collapse under the new spawn pressure.

3. Rank/nameplates.
   - Run `/ascnametag status`.
   - Use `/ascnametag preview_self` briefly if the player plate needs a visual check.
   - Spawn or find an AI hunter only in a test world if needed.

4. NPC relationship behavior.
   - Spawn a small generated NPC set in a test world.
   - Confirm NPCs no longer say generic `hello <player>`.
   - Confirm non-examiner NPCs do not behave like instant followers.
   - Confirm Rank Examiner right-click still works.

5. Ranked dungeons.
   - Rifts are visually signed off for v1, but dungeon-side play is still young.
   - Before the long session, test one low-rank rift together.
   - Confirm both players can enter before the gate closes.
   - Confirm safe room, combat rooms, boss room, boss-locked return gate, and cleanup work.

6. Structure placement.
   - Structure Director Live v1 is active, but field review is not complete.
   - During the playtest, record any land structures spawning as islands, especially dragon roosts and IDAS vineyard-like structures.
   - Do not treat structure placement as fully signed off yet.

## Known Non-Blockers For The Session

- Loot/recipe/magic balance audits still warn about high-tier items in low-tier places. This can make progression messy, but it does not block a fun exploratory playtest if you record bad finds.
- Structure loot tiers are not fully assigned. Record obviously overpowered chest loot.
- Roads/bridges are not tuned yet. Record bad cliffs, floating roads, missing bridges, or roads to nowhere.
- Travel network and civilization placement are not final.
- Atlas directional terrain steering is disabled; random Tectonic/Terralith generation is the current direction.
- Shader uniform warnings from Oculus/Complementary should be watched for visual issues, but they are not automatically a crash blocker unless they cause broken visuals or performance problems.

## Minimum Green Light

The pack is ready for the multi-hour playtest when:

- `python scripts/check-pack.py` has no blocking issues.
- The active log has no KubeJS syntax errors.
- The active log has no OpenLoader/datapack load errors from Ascendant files.
- Both players can join, leave, and rejoin.
- Resource packs and shaders are stable after restart.
- One short dungeon/rift test works or dungeons are explicitly skipped for the session.
- Mob density feels playable for at least 10 minutes of real exploration.
