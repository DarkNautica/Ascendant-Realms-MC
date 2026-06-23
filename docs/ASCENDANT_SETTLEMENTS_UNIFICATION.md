# Ascendant Settlements Unification

Status: data-driven standalone Guild structure layer is active. No direct third-party village pool injection is active from this pass.

The pack already has many settlement and structure systems. The goal is not to throw another village overhaul on top. The goal is to make one Ascendant-owned layer that decides how villages, Guild boards, guards, names, contracts, and NPCs connect.

## Current Decision

Datapack/config is enough for the next step. A custom Forge helper mod is approved in principle, but not needed until we need runtime NPC-equipment automation, animated nameplate rendering, automatic village role assignment, or deep jigsaw conflict handling that datapacks cannot control safely.

## Ownership Model

The source contract lives in `config/ascendant_settlements/settlement_unification.json`.

- Vanilla villages remain the base settlement layer.
- Integrated Villages stays active with the shared workstation/POI processor repair in `config/openloader/data/ascendant_realms_world_integration`.
- Towns and Towers, Villages & Pillages, MVS/MSS/MES, Medieval Buildings, IDAS, and YUNG structures are destination and landmark layers.
- Bountiful owns the contract board function.
- Supplementaries owns notice-board dressing.
- Guard Villagers owns baseline village defense.
- Easy NPC owns social Guild NPCs.
- CustomNPCs-Unofficial owns rivals and combat-capable special NPCs.

## Hunter Board Workflow

The first active build is now a standalone Hunter Board structure set, not an injected village pool piece.

1. Generate `hunter_board_village_standard`, `roadside_hunter_camp`, and `frontier_guild_outpost` through `scripts/generate-ascendant-guild-worldgen.py`.
2. Keep spacing conservative while villages are already dense: `192/80`, `224/96`, and `288/128`.
3. Use multiple written Supplementaries notice boards per structure for rankings, rules, rumors, and frontier notes.
4. Use `ascendant_guild:chests/*` loot tables for Guild containers.
5. Keep notice boards facing outward and use Macaw wall lantern blocks for wall-adjacent lantern dressing.
6. Prove `/locate`, natural generation, generated NPC spawn sets, notice boards, loot, and server stability.
7. Only then inject rare board pieces into selected village pools.

This keeps crashes isolated. If a standalone structure fails, it does not corrupt every village generation path.

## Custom Mod Threshold

Build `Ascendant Settlements` as a small Forge helper mod only if we hit one of these:

- NPCs need runtime/randomized equipment assignment beyond the current generated `npc_loadouts.json` spawn NBT.
- NPCs need guaranteed runtime faction defense/hostile targeting across the full modded enemy stack.
- Villages need runtime role assignment based on biome, rank, danger, or nearby structures.
- Nameplates need custom animated rendering over players and NPCs.
- Datapack pool injection cannot safely control conflicts between third-party village mods.

Until then, keep the layer data-driven and testable.
