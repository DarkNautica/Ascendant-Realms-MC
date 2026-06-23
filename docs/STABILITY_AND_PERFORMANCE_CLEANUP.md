# Stability And Performance Cleanup

Status: staged in source; needs fresh client import or active-client sync and restart.

## What Was Fixed

- Resource-pack persistence: Vanilla Experience+ now uses the ASCII filename `Vanilla Experience Plus.zip` instead of a section-sign colored filename. The root `options.txt`, Resource Pack Overrides config, Packwiz metadata, and pack checker all agree on that exact path.
- Resource-pack retry loop: Resource Pack Overrides now retries failed reloads at most twice per session instead of five times. That keeps the auto-repair behavior without creating long failed-reload loops during startup.
- Active sync reliability: `scripts/sync-active-client-files.ps1` now installs URL-backed Packwiz resource packs into the active CurseForge instance, removes stale color-code Vanilla Experience+ filenames, copies tracked performance configs, and still preserves personal options by merging only resource-pack lines into `options.txt`.
- Missing armor texture warnings: the compatibility resource pack now mirrors missing vanilla-namespace armor texture paths for Iron's Spells and Mowzie's Mobs renderers. This is visual-only and does not change gameplay.
- Settlement pressure: In Control broad caps were tightened after the latest log still showed MCA villagers and guards dying quickly to Born in Chaos pressure mobs.
- Performance configs: ModernFix, Embeddium, EntityCulling, Sodium Dynamic Lights, and Sound Physics Remastered configs are now tracked so fresh imports stop falling back to defaults.
- Server staging hygiene: `scripts/export-server-pack.ps1` now prunes known client-only visual, HUD, audio, render, menu, dynamic-light, and resource-pack override configs from `dist/server-pack-staging` after copying shared config. This does not remove any server/both-side gameplay config.

## Safe Performance Choices

- Sodium Dynamic Lights stays active but uses `FAST` instead of `REALTIME`.
- Sound Physics Remastered keeps immersive occlusion/reverb but uses fewer evaluation rays and bounces.
- Embeddium keeps entity culling, fog occlusion, compact vertices, block face culling, deferred chunk updates, and animated-visible-textures.
- EntityCulling culls through-wall nameplates and lowers tracing distance from the active default.
- ModernFix keeps high-risk shortcuts disabled: dynamic resources, dynamic entity renderers, and faster item rendering stay off until the full resource/FancyMenu/tooltip stack has more clean launches.

## What Was Not Removed

- No gameplay mods were removed.
- No village, mob, worldgen, NPC, loot, skill, or UI system was removed.
- No structure pack was disabled.
- No resource pack was dropped from the intended stack.

## Next Test Pass

- Reimport the latest client export or run `scripts/sync-active-client-files.ps1` while Minecraft is closed.
- Launch once and check that the resource packs remain selected after restart.
- Confirm the latest log no longer reports `Failed to load options`.
- Confirm missing texture warnings for `cultist_layer_1`, `wandering_magician_layer_2`, `netherite_layer_*_overlay`, `geomancer_armor_layer_1`, `wizard_layer_1`, or `plagued_layer_1` are gone.
- Visit a village at night and confirm the world is still dangerous but MCA villagers are not being erased instantly.
- Check launch timing again from Forge logs. The target is not instant startup; the goal is fewer failed reloads and less repeated fallback work.
- For server retest, use the refreshed `dist/server-pack-staging` output and confirm client-only config files such as FancyMenu, Embeddium, EntityCulling, Sound Physics, Resource Pack Overrides, and Sodium Dynamic Lights are absent from the server staging config.
