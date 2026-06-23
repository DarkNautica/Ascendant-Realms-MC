# System Ecosystem Overview

Status: ecosystem health pass complete; source exports are ready, and active-client sync is waiting for Minecraft to close.

This document is the current one-page map for Ascendant Realms as a whole. It is not a replacement for the deeper batch docs. Use it to see what is active, what was fixed in the latest pass, and what should happen next.

## Current Target

- Minecraft: 1.20.1.
- Loader: Forge 47.4.20.
- Java: 17.
- Pack version: 0.1.0-alpha.
- Latest active client instance target: `C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)`.
- Current sync state: pending because Minecraft was still running during the worldgen helper export pass.

## Active System Layers

- Foundation: Packwiz, Forge, performance stack, Embeddium/Oculus shader path, Fresh Animations/resource polish, and QoL.
- Worldgen and structures: Terralith, Tectonic, Serene Seasons, Sparse Structures, YUNG suite, Towns and Towers, Structory, Moog structures, Integrated Villages, IDAS, Create: Structures Arise, Cataclysm/IceAndFire/Marium structures, standalone Ascendant Guild structures, and Ascendant Atlas finite-world runtime plus coordinate-aware biome source.
- Mobs and danger: Alex's Mobs, Mowzie's Mobs, Born in Chaos, Aquamirae, Enhanced Celestials, Bosses'Rise, IceAndFire CE, Cataclysm, Scaling Health, Improved Mobs, Majrusz's Progressive Difficulty, and Spawn Balance Utility.
- Combat and gear: Better Combat, Combat Roll, Simply Swords, Simply Swords Reforged, Marium, Spartan Shields, Immersive Armors, Fantasy Armor, Artifacts, and the generated Ascendant gear rarity index.
- Magic and progression: Iron's Spells, custom Puffish Skills Ascendant Web, Pufferfish's Attributes/Skills, and progression docs for future boss/contract hooks.
- Loot and contracts: Bountiful, Loot Integrations, Artifacts, Loot Beams, Loot Journal, generated bounty target indexes, and Guild/Hunter contract scaffolds.
- Villages and NPCs: MCA Reborn, MCA - Default Medieval, Guard Villagers, Villager Names, Human Companions, Easy NPC, CustomNPCs-Unofficial, generated Guild NPC profiles, generated CustomNPC spawn functions, and standalone Guild structures.
- UI and presentation: FancyMenu, Drippy Loading Screen, SpiffyHUD, Immersive UI, Item Borders, Legendary Tooltips, Stylish Effects, Overflowing Bars, Xaero's Minimap, YDM's MobHealthBar, Traveler's Titles resource packs, and the custom title-screen assets.
- Cohesion tools: Ascendant Core JSON contracts, KubeJS, Open Loader, Almost Unified, Almost Unify Everything, Polymorph, Every Compat, Create Slice & Dice, Alex's Delight, Supplementaries, Quark, Zeta, and targeted resource/data compatibility shims.

## Latest Fixes Applied

- Active-instance sync: helper scripts now target the newest `Ascendant Realms*` CurseForge instance instead of assuming the original folder.
- Safer options sync: client sync now merges only the `resourcePacks` and `incompatibleResourcePacks` lines into `options.txt`, preserving controls, graphics, audio, and other personal settings.
- MCA resource guard: `scripts/check-pack.py` now requires MCA - Default Medieval to be enabled whenever MCA Reborn is active.
- FancyMenu video: the packaged title-screen layout now enables the MP4 background block by default because WATERMeDIA and WATERMeDIA Binaries are installed.
- JEI/KubeJS alias: the Runic Grimoire alias now passes the NBT Patchouli stack directly to JEI instead of wrapping it in a list shape that could trigger `ingredients must not be empty`.
- Armor texture aliases: the compatibility resource pack now provides missing Iron's Spells and IceAndFire armor texture paths as visual-only fallbacks.
- Registry scripts: content and gear registry generators now auto-detect the newest active CurseForge instance when no path is passed.
- CustomNPC tooling: hero/identity audit tooling now follows the newest instance and skips world entity repair cleanly if the selected import has no saves yet.
- World audit refreshed: `docs/WORLD_INTEGRATION_AUDIT.md` now reflects the latest active imported jar set.
- Progression HUD bridge: `kubejs/server_scripts/ascendant_progression.js` now reads Puffish Skills Ascendant Web data, renders Jayden's custom XP bar, mirrors skill points, fires level-up visuals, and syncs `ar_skill_level` for multiplayer nameplates.
- Ascendant Core bridge: `config/ascendant_core/` now defines the pack-owned contracts for ranks, regions, mob ecology, structures, loot, NPC roles, materials, progression hooks, runtime rules, and custom modules. `kubejs/server_scripts/ascendant_core_integration.js` loads the manifest/runtime rules, checks linked files, creates shared Guild/progression/world-state scoreboards, mirrors region tier, promotes rank from proof counters, and awards conservative reputation/proofs from known player-killed threats.
- Ascendant Atlas runtime: `config/ascendant_atlas/` now defines region, ring, climate, biome, settlement, structure, mob, loot, ore, naming, runtime, road/bridge contracts, and generated Terralith-backed biome tables. `kubejs/server_scripts/ascendant_atlas_runtime.js` applies the 30000-block playable border and mirrors regions into scoreboards; `ascendant_atlas_regions` supplies the active Overworld biome source with a 50000-block visual buffer beyond the square border; `config/incontrol/areas.json` provides coordinate boxes for spawn guardrails. The old waymarks are debug-only assets, not natural worldgen.
- KubeJS config-read hotfix: the active client log showed `ascendant_core_integration.js` and `ascendant_progression.js` failing first on blocked `java.nio.file.Files` style access, then on blocked `java.io.File`. Both scripts now use KubeJS `JsonIO` with `KubeJSPaths.CONFIG`, and `scripts/check-pack.py` rejects the blocked Java file APIs.
- Bountiful warning fix: the one invalid major Guild objective `iceandfire:black_frost_dragon` was replaced with `iceandfire:ice_dragon`; the broader IceAndFire/dragon contract system stays active.
- Stability/performance cleanup: Vanilla Experience+ now downloads as ASCII `Vanilla Experience Plus.zip`, Resource Pack Overrides retries only twice per failed reload, the active sync script installs URL-backed Packwiz resource packs and removes stale color-code filenames, ModernFix/Embeddium/EntityCulling/Sodium Dynamic Lights/Sound Physics configs are now tracked, and the compatibility resource pack mirrors the latest missing armor texture paths from active jars.
- Settlement pressure cleanup: In Control caps were tightened after the latest live log still showed MCA villagers/guards dying quickly to Born in Chaos pressure mobs. This keeps all danger mods installed while reducing burst density.

## Current Audit Snapshot

- Jars scanned: 172.
- Jars with world/data integration surfaces: 64.
- Structures: 623.
- Structure sets: 333.
- Template pools: 1,586.
- Placed features: 696.
- Configured features: 631.
- Biome modifiers: 98.
- Biome tags: 614.
- Loot tables: 4,324.
- Recipes: 10,551.
- Item tags: 1,065.
- Entity type tags: 145.

## Remaining Gaps

- Newest import launch confirmation: source/export artifacts and active `Ascendant Realms (2)` are synced for the current Atlas terrain pass; the next client launch is the real confirmation.
- MCA visuals: MCA - Default Medieval is enabled by default, but naturally spawned MCA villagers still need in-game visual validation.
- Generated CustomNPC visuals: bridge skins and visible gear are generated and mirrored into CustomNPCs' native resource path; in-game retest still needs to confirm no magenta skins and no missing gear.
- NPC combat behavior: CustomNPC guards/rivals have better defaults, but real hostile defense may need a future Ascendant NPC Runtime helper mod.
- Player/NPC nameplates: current fallback uses vanilla scoreboard/title mechanics. Polished dynamic nameplates, player ranks, NPC ranks, and enemy levels likely require a small client/server helper mod.
- Skill HUD: the KubeJS/Puffish bridge now loads through safe `JsonIO`; it still needs in-game visual retest for overlap, pacing, and popup polish.
- Structure density: the world has enough content volume now; the latest pass widened Integrated Villages, Towns and Towers, Sparse Structures, and Guild structures. The next work is fresh-world validation, road/bridge coordinate notes, loot, and biome fit rather than more structure packs.
- Rarity and loot balance: item borders and tooltip rarity labels exist, but loot tables and drop chances still need a full reward-curve pass.
- Ascendant Core enforcement: the registry layer and first runtime bridge are live, but biome/structure-aware regions, generated In Control rules, formal FTB-style rank trials, NPC runtime behavior, and final nameplates still need their own bridges.

## Next Steps

1. Launch the latest imported client and confirm no KubeJS startup errors, missing dependency screen, or resource-pack load failure.
2. Confirm the title screen uses the new title art, live mod/version status text, and enabled MP4 background without blocking buttons.
3. Open JEI and search for `Runic Grimoire`; confirm it appears and does not trigger the old JEI plugin warning.
4. Generate or locate Guild structures; confirm notice boards face outward, containers have loot, NPCs show MCA-style skins, and role gear renders.
5. Run `/function ascendant_atlas:status` at spawn and at north/south/east/west test coordinates to confirm region/ring/sector scoring and worldborder behavior.
6. Visit villages with MCA villagers; confirm the medieval clothing pack is active and no common modern/off-tone skins appear.
7. Materialize a fresh dedicated server from the latest active client mods path and run boot/join/10-minute stability.
8. Run a focused structure-density survey around multiple villages, IDAS structures, YUNG structures, Moog structures, Integrated Villages, roads, rivers, cliffs, and YUNG/Macaw bridge opportunities.
9. Use `config/ascendant_core/` as the source for the first In Control draft, structure loot pass, FTB Quest rank trials, and NPC runtime decisions.
10. Consider additional helper code only for problems data/config cannot solve: terrain-aware road/bridge substitution, dynamic nameplates, enemy levels, deeper HUD animation, runtime NPC role/combat behavior, or structure-pool conflict resolution.
11. Begin the real balance pass: early danger, long-term growth curve, bounty rewards, structure loot, boss/dragon rewards, and rarity-to-drop-rate consistency.
