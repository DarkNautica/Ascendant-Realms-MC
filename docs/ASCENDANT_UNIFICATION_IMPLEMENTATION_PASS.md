# Ascendant Unification Implementation Pass

Status: active first implementation pass.

This pass turns the generated registries into gameplay-facing systems without removing content. It is intentionally data-first: config and datapack outputs come before custom Java, and custom mods remain reserved for the pieces that cannot be made smooth through existing mod APIs.

## Research Findings

- In Control 1.20 keeps spawn filtering/stat rules in `spawn.json` and uses a separate `spawner.json` schema for adding new spawns. This pass only changes the already proven `spawn.json` cap pattern.
- Bountiful contract boards can be driven by datapack pool/decree JSON. The active Guild datapack already loads through Open Loader, so the safest next step is to regenerate its pools from the Ascendant mob registry.
- Open Loader is the correct delivery layer for the pack-owned datapacks because it loads global packs from `config/openloader/data/` for client and server.
- KubeJS remains the bridge for scoreboards, HUD, recipes, tags, tooltips, and lightweight runtime hooks, but it should not mutate worldgen or item Java fields during server load.

## Implemented Now

- Expanded Bountiful objectives from the full generated mob registry instead of the old first-pass sample.
- Live contract counts are now:
  - Village Hunter Board: 79 targets.
  - Town Guild Board: 23 targets.
  - Major Guild Registry: 51 targets.
- Friendly/tooling namespaces are filtered from kill contracts:
  - `customnpcs`
  - `easy_npc`
  - `humancompanions`
  - `mca`
  - `geckolib`
- Bounty rewards now include a slightly richer vanilla/Guild-currency ladder while avoiding risky unknown mod item IDs.
- `scripts/generate-ascendant-guild-worldgen.py` is the source of truth for these pools, so future worldgen regeneration will not stomp the expanded contracts.
- `config/incontrol/spawn.json` now has a cap-only settlement-safety pass:
  - Born in Chaos pressure lowered from `90` to `34`.
  - Mowzie's Mobs lowered from `20` to `12`.
  - Aquamirae lowered from `40` to `18`.
  - Cataclysm, IceAndFire, Bosses'Rise, Soulsweapons, Bosses'Rise internal namespace, Iron's Spells, and Majrusz Difficulty now have explicit cap rules.
- `config/ascendant_core/live_spawn_policy.json` records the spawn policy and what is intentionally deferred.

## Why This Is Not A Custom Mod Yet

A custom mod is justified when we need synced client overlays, automatic NPC runtime behavior, rank-aware encounter control, or precise settlement injection. This pass did not need that yet because:

- Bountiful pools are already data-driven.
- Open Loader already delivers the datapack.
- In Control already handles cap-based spawn safety.
- KubeJS already owns the current scoreboard/progression bridge.

The next custom modules remain likely, but they should start where data cannot solve the problem cleanly:

- `ascendant_nameplates` for polished player/NPC/enemy nameplates.
- `ascendant_progression_hud` if KubeJS Painter cannot fully satisfy the HUD layout.
- `ascendant_npc_runtime` for generated NPC equipment, aggression, faction defense, and schedules.
- `ascendant_settlement_engine` if one-board-per-settlement placement cannot be kept stable through datapacks.
- `ascendant_encounter_director` for rank/region-aware dynamic pressure.

## Deferred On Purpose

- Superseded on 2026-06-18: `config/incontrol/spawner.json` is now active for common hostile daytime/cave pressure. See `docs/HOSTILE_DAY_SPAWN_PASS.md`.
- No third-party village pool injection yet. Integrated Villages is already repaired and active; direct injection waits until the standalone Guild structures stay stable.
- No broad structure spacing rewrite in this pass. Integrated Villages already has a common village placement set and the Guild structures were previously widened after board spam.
- No custom Java module was compiled in this pass because the active wins were achievable through current data/config rails.

## Next Test Pass

Client:

- Reimport or sync the source pack.
- Launch client and confirm no In Control, Bountiful, Open Loader, or KubeJS startup errors.
- Open a Bountiful board and confirm village/town/major boards show a wider mix of modded targets.
- Visit a village at night and watch whether villagers/guards survive longer against the first pressure wave.
- Confirm no friendly NPCs appear as kill objectives.

Server:

- Export server staging.
- Materialize server mods from the active client with `-Clean`.
- Boot the Forge server and join.
- Confirm Open Loader injects all custom datapacks.
- Confirm Bountiful boards work server-side.
- Let the server run 10 minutes near a settlement and watch log pressure.

## Next Implementation Steps

1. Build the first `ascendant_npc_runtime` prototype if CustomNPCs/Easy NPC cannot make generated guards/rivals defend settlements reliably.
2. Generate a reviewed `spawner.json` draft for missing ambient/region mobs, then activate only a small copied-world test slice.
3. Add structure loot links from the structure registry into specific safe loot tables instead of blanket overriding every modded dungeon.
4. Convert rank trials into formal FTB Quest chapters using the existing Ascendant Core scoreboards.
5. Decide whether the HUD/nameplate polish now warrants a small client-side Forge helper mod.
