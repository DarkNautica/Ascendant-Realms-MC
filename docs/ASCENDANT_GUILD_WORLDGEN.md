# Ascendant Guild Worldgen

Status: standalone generated worldgen test is active. This is the first custom Ascendant worldgen layer.

This pass does not inject directly into vanilla, Integrated Villages, Towns and Towers, IDAS, or other third-party village pools. It adds standalone Guild/Hunter structures that can be located and tested in fresh chunks first.

## Generated Structures

| Structure | Spacing/Separation | Purpose | Test Command |
|---|---:|---|---|
| `ascendant_guild:hunter_board_village_standard` | 192/80 | `Small standalone village-facing Hunter Board with one Bountiful board and a multi-board Guild notice roster.` | `/locate structure ascendant_guild:hunter_board_village_standard` |
| `ascendant_guild:roadside_hunter_camp` | 224/96 | `Roadside camp for wounded hunters, tavern rumors, and scout/rival encounters.` | `/locate structure ascendant_guild:roadside_hunter_camp` |
| `ascendant_guild:frontier_guild_outpost` | 288/128 | `Small Guild outpost prototype for Rank Examiner, Arcanist, and Quartermaster placement.` | `/locate structure ascendant_guild:frontier_guild_outpost` |

## Why Standalone First

Standalone structures let us prove that custom NBT, Bountiful boards, written notice boards, loot containers, biome placement, and server sync work before touching modded village pools. If a structure has a bad block state or worldgen issue, it is isolated to the Ascendant Guild datapack instead of crashing every village generator.

## Current Tuning Notes

- Village Hunter Boards were widened and moved from `42/18` to `96/40`, then to `192/80`, after a test village produced too many board structures nearby.
- Roadside Hunter Camps moved from `54/22` to `128/56`, then to `224/96`.
- Frontier Guild Outposts moved from `72/30` to `160/64`, then to `288/128`.
- Notice boards are still part of the design, but the roster is split across several written boards so each board stays readable.
- Notice boards are generated facing outward after the first test found them rotated into their support wall.
- Roadside and frontier containers now use `ascendant_guild:chests/*` loot tables instead of empty default containers.
- Wall-adjacent lanterns use Macaw's Lights wall lantern blocks where the structure has a wall behind the lantern.
- The roadside camp lantern supports use real oak fence posts and standing lanterns, not floating hanging lanterns.

## Test Plan

Client creative/system test:

- Create a fresh creative test world.
- Run each `/locate structure ascendant_guild:<id>` command.
- Teleport to each result and inspect the structure.
- Confirm Bountiful bounty boards and multiple written Supplementaries notice boards render.
- Confirm notice boards show readable rank, roster, rumor, rule, or frontier text.
- Confirm notice boards face outward rather than into the wall.
- Confirm wall-mounted lanterns on Hunter/Frontier structures use Macaw wall lanterns, while freestanding roadside post lanterns remain standing lanterns.
- Confirm camp/outpost containers are not empty.
- Confirm camp/outpost blocks do not cause missing-block or block-entity errors.
- Spawn generated NPC sets near the structures.
- Save and reload.

Dedicated server test:

- Sync the latest client files.
- Export server staging.
- Materialize server mods from the active client instance.
- Boot the Forge 47.4.20 server.
- Join localhost or LAN.
- Generate fresh chunks and locate each Ascendant Guild structure.
- Let the server run 10 minutes.

## Next Gate

Only after this passes should we inject rare Guild pieces into village pools. If datapack pool injection proves too brittle, build the `Ascendant Settlements` Forge helper mod rather than removing village functionality.
