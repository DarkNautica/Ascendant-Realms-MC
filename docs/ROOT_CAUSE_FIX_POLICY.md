# Root Cause Fix Policy

Status: active project policy.

Ascendant Realms should preserve working gameplay whenever possible. A crash, warning, missing texture, broken loot table, bad tag, or ugly UI conflict is not automatically a reason to remove a mod.

## Default Response

1. Reproduce or inspect the exact failure.
2. Identify the smallest broken bridge: config value, tag, loot table, recipe, resource path, processor list, dependency, script, or client-only/server-only split.
3. Patch that bridge with Packwiz metadata, config, OpenLoader data, resource-pack assets, KubeJS, or a small custom Forge helper only when data/config is not enough.
4. Keep the original mod/content active unless testing proves the upstream feature is unfixable or unstable.
5. Document the exact cause, the exact override path, and the gameplay impact.
6. Retest client boot, creative/system behavior, dedicated server boot/join, and 10-minute stability before calling the pass stable.

## Removal Threshold

Remove or delay a mod only when one of these is true:

- The selected file is not actually compatible with Minecraft 1.20.1 Forge.
- The crash is inside a closed Java path that cannot be avoided with config/data/resource/script patches.
- Keeping it active corrupts worlds, prevents server boot, or breaks multiplayer handshakes after a focused fix attempt.
- It duplicates another installed system so heavily that the two cannot be configured into a coherent single behavior.

## Custom Mod Threshold

Build a small Ascendant-owned Forge helper mod only when datapacks/config/KubeJS cannot safely solve the need. Current likely future targets:

- Polished animated player/NPC nameplates and enemy level display.
- A second HUD XP bar tied to Puffish Skills progress.
- Automatic important-NPC equipment assignment from `config/ascendant_guild/npc_loadouts.json`.
- Runtime settlement role assignment or safer village-pool integration.
- Cross-mod rarity/loot hooks that need live registry inspection beyond datapack limits.

Until one of those thresholds is hit, prefer documented OpenLoader/KubeJS/resource-pack shims because they are easier to audit and remove.
