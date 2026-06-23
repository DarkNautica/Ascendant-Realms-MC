# Ascendant Core

Status: active data-first integration layer.

This folder is the pack-owned source of truth that explains how Ascendant Realms stitches the installed mods together. The files here do not replace the generated indexes under `config/ascendant_index/`; they organize those indexes into gameplay rules that other systems can safely consume.

Current live behavior:

- `kubejs/server_scripts/ascendant_core_integration.js` loads `core_manifest.json` on server load.
- The same bridge loads `runtime_rules.json` for editable rank thresholds, region-tier bands, and conservative kill rewards.
- The loader verifies that the linked registries exist.
- The loader creates shared scoreboard objectives for rank, bounty, structure, boss, dragon, region, and threat tracking.
- The loader mirrors each player's current region tier from dimension/distance and promotes Guild rank when configured score requirements are met.
- Known hostile, elite, boss, and dragon-tier player kills add small Guild reputation/proof counters. This is not a replacement for Bountiful contracts.
- Open Loader identity functions also create the same objectives as a datapack fallback.
- Open Loader core helpers expose `/function ascendant_core:status` and debug proof functions for validation.

Current non-invasive policy:

- No coordinate-aware worldgen, mob-spawn rewrites, or village-pool injection happens directly from this folder yet.
- Rules marked `runtime_state: contract_active` are real authored contracts, but they still need an owning bridge such as In Control rules, Bountiful pools, Open Loader data, KubeJS, or a future custom Forge helper before they change live gameplay.
- Rules marked `runtime_state: live` are already being used by an active config, datapack, KubeJS script, or generated system.

Next custom-code threshold:

- Build `Ascendant Core` as a Forge helper mod when JSON contracts need packet sync, commands, dynamic entity/nameplate rendering, or runtime structure/NPC behavior that KubeJS/datapacks cannot provide safely.
