# AI Modpack Handoff

Generated: 2026-06-16T20:55:15Z

Purpose: give another AI enough context to inspect or continue Ascendant Realms without rediscovering the modpack from scratch.

## Pack Facts

- Pack: Ascendant Realms `0.1.0-alpha`.
- Minecraft: `1.20.1`; Forge: `47.4.20`; Java target: `17`.
- Pack manager: Packwiz `pack-format = "packwiz:1.1.0"`.
- Active test instance path used in recent work: `C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)`.
- Do not treat `dist/server-pack-staging/` as source. It is generated export output.
- Pack entries in this handoff: 190 total.
- Kind counts: Local Forge helper mod=1, Mod=173, Resource Pack=15, Shader Pack=1.
- Side counts: both=129, client=61.

## Registry Snapshot

- `indexed_mobs`: 757.
- `indexed_structures`: 617.
- `gear_registry`: weapons=499, armor=601, shields=77, magic_items=273, spells=113, accessories_relics=160.
- `spawn_groups`: 23.
- `worldgen_audit`: biomes=802, structures=645, structure_sets=348, templates=4972, mobs_with_json_spawn_evidence=68.

## First-Read Source Order For Another AI

1. `docs/CURRENT_STATUS.md` for the newest live state, latest fixes, and retest checklist.
2. `docs/DOCS_INDEX.md` for which docs are authoritative versus generated or historical.
3. `docs/ATLAS_TERRAIN_VALIDATION_REPORT.md`, `docs/ATLAS_BIOME_POOL_REPORT.md`, and `docs/ATLAS_WORLDGEN_FAILURES.md` before judging whether Atlas terrain works.
4. `docs/ASCENDANT_ATLAS_WORLDGEN.md` before touching biomes, regions, snow, structures, roads, or finite-world rules.
5. `docs/SYSTEM_ECOSYSTEM_OVERVIEW.md` for the broad layer map.
6. `docs/WORLDGEN_CONTENT_AUDIT.md` and `docs/generated/worldgen_content_audit.json` before classifying biomes or structures.
7. `config/ascendant_index/*.json` for machine-readable mobs, structures, gear, spawn worklists, and integration thresholds.

## Core Architecture

- Ascendant Core is the pack-owned contract layer under `config/ascendant_core/`; KubeJS reads it and mirrors shared state into scoreboards.
- Ascendant Atlas is the region/worldgen layer under `config/ascendant_atlas/`; the local `ascendant_atlas_regions` helper jar owns the active regional biome source.
- OpenLoader carries datapack overrides, tags, functions, structure repairs, Guild structures, Codex data, and the Overworld dimension override.
- KubeJS carries runtime glue, tooltip/JEI polish, recipe/tag glue, rank/proof mirroring, and Atlas/progression bridge behavior.
- In Control applies coordinate-area spawn guardrails; it should follow Atlas regions instead of fighting them.
- Resource Pack Overrides controls visual pack order; do not assume a resource pack is active just because its file exists.

## Critical Interaction Hotspots

| Hotspot | Main Mods/Data | What Another AI Must Know |
|---|---|---|
| Atlas worldgen | `ascendant_atlas_regions`, Terralith, Tectonic, OpenLoader, KubeJS, In Control | Atlas chooses regional biome tables and biases climate; Tectonic-style terrain shape must remain. Do not pick biomes by name only. Use the audit JSON, `/ascatlas` commands, and fresh-world chunk evidence. |
| Warm-region snow | Weather2, Snow Real Magic, Serene Seasons, Terralith, Atlas configs | Recent bug: `terralith:gravel_desert` looked like a desert but had temperature `0.14` and accepted snow. Source configs now block snow buildup outside cold biomes and disable global seasonal snow/ice conversion. |
| Structure density | Sparse Structures, YUNG suite, IDAS, Integrated Villages, Towns and Towers, Structory, Moog structures, Aquamirae, Guild structures | The pack has enough structure volume. Tune density, spacing, biome fit, and loot before adding more structure mods. Aquamirae surface set is overridden wider. |
| Villages/NPCs | MCA Reborn, MCA Default Medieval, Easy NPC, CustomNPCs, Human Companions, Guard Villagers, Villager Names, Bountiful, Patchouli, FTB | The goal is a Guild/Hunter RPG spine. NPC visuals, guards, rivals, boards, and contracts must feel medieval/fantasy and survive hostile pressure. |
| Spawn pressure | In Control, Spawn Balance Utility, Scaling Health, Majrusz, Improved Mobs, Born in Chaos, Alex's Mobs, IceAndFire, Cataclysm, Mowzie, Aquamirae | Danger mods stay installed; tune pressure using regional caps and spawn groups rather than removing content first. Settlement safety is a known concern. |
| Combat/progression | Better Combat, Combat Roll, Simply Swords, Marium, Spartan Shields, Immersive/Fantasy Armor, Artifacts, Iron's Spells, Puffish Skills/Attributes | Gear and skills are indexed for rarity and future rank gates. Balance reward pacing with combat feel and mobility. |
| Recipes/materials | Create, Farmer's Delight, Alex's Delight, Slice & Dice, Every Compat, Almost Unified, Quark, Supplementaries, Macaw family, Polymorph | This is the material and recipe cohesion layer. Avoid adding recipes that bypass intended rank/loot progression. |
| UI clarity | Item Borders, Legendary Tooltips, JEI, Loot Beams, Loot Journal, MobHealthBar, Overflowing Bars, Traveler's Titles, FancyMenu, Drippy | UI should tell the RPG story: rarity, levels, biomes, loot feedback, and title/menu polish. Test visual overlap after changes. |
| Rendering/performance | Embeddium, Oculus, ModernFix, FerriteCore, Entity Culling, Sodium Dynamic Lights, EMF/ETF, Fresh Animations, shaders/resource packs | Large worldgen/content stack depends on this staying stable. Run client launch and visual checks after shader/resource changes. |

## Category Counts

| Category | Count | Role |
|---|---:|---|
| Audio / Atmosphere | 11 | Feeds biome mood, storm feel, footsteps, sound reverb, ambient music, leaves, particles, and sky/weather presentation. |
| Cohesion / Recipes / Tags | 20 | Glue layer for recipes, wood sets, tags, material compatibility, structure palette cohesion, and pack-owned data overrides. |
| Combat / Gear | 9 | Feeds the RPG combat loop, rarity labels, loot tiers, skill synergies, and boss/contract rewards. |
| Custom / Local | 1 | Pack-owned code/data. This is the highest-priority layer to inspect before changing worldgen or runtime behavior. |
| Dependency / Library | 42 | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Loot / Contracts | 9 | Feeds Bountiful, loot tables, guide books, bounty objectives, and reward visibility. |
| Magic | 4 | Feeds spell progression, magical loot, skill hooks, boss rewards, and class fantasy. |
| Mobs / Bosses | 8 | Adds hostile/passive entity pressure, boss goals, structure inhabitants, drops, and bounty targets. |
| Performance | 5 | Keeps the large mod stack playable. Treat as infrastructure and verify after shader/UI/worldgen changes. |
| Resource Pack | 2 | Visual cohesion layer. Order matters because several packs intentionally override mod textures/models. |
| Shader / Visual Base | 12 | Client visual base: shaders, model features, animation support, particles, and rendering compatibility. |
| Skills / Difficulty | 8 | Owns player growth, level pressure, difficulty scaling, attributes, and future rank gates. |
| Storage / QoL | 4 | Convenience features that should not control balance unless linked to loot/progression. |
| UI / Presentation | 23 | Owns title screen, HUD, tooltips, rarity borders, titles, minimap, health bars, and player-facing clarity. |
| Villages / NPCs | 4 | Owns village population, medieval NPC presentation, Guild staff, guards, rivals, companions, and settlement safety. |
| Worldgen / Structures | 28 | Adds terrain, biomes, structures, villages, dungeons, roads, structure loot, and spawn surfaces. |

## Complete Pack Entry Breakdown

This table is generated from root Packwiz metadata plus the local Atlas helper jar. `Role / interaction` is intentionally practical: it tells the next AI what each entry touches in this pack.

### Audio / Atmosphere

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| AmbientSounds 6 | client | CurseForge | `AmbientSounds_FORGE_v6.3.8_mc1.20.1.jar` | Atmosphere layer tied to biome feel, weather, and shader/performance testing. |
| Auroras | client | Modrinth | `Auroras-1.20.1-1.6.2.jar` | Atmosphere layer tied to biome feel, weather, and shader/performance testing. |
| Biome Music[Forge/Fabric] | client | CurseForge | `biomemusic-1.20.1-3.5.jar` | Atmosphere layer tied to biome feel, weather, and shader/performance testing. |
| Enhanced Celestials | both | Modrinth | `Enhanced-Celestials-forge-1.20.1-5.0.3.2.jar` | Event/moon pressure layer; can affect mob danger and atmosphere. |
| Falling Leaves (NeoForge/Forge) | client | Modrinth | `fallingleaves-1.20.1-2.1.2.jar` | Atmosphere layer tied to biome feel, weather, and shader/performance testing. |
| Particular Reforged | both | Modrinth | `particular-1.20.1-Forge-1.5.0.jar` | Atmosphere layer tied to biome feel, weather, and shader/performance testing. |
| Presence Footsteps (Forge) | client | CurseForge | `PresenceFootsteps-1.20.1-1.9.1-beta.1.jar` | Feeds biome mood, storm feel, footsteps, sound reverb, ambient music, leaves, particles, and sky/weather presentation. |
| Serene Seasons | both | Modrinth | `SereneSeasons-forge-1.20.1-9.1.0.2.jar` | Weather/season/snow behavior. Atlas guards prevent warm-region snow and keep Frostmarch identity regional. |
| Sound Physics Remastered | client | Modrinth | `sound-physics-remastered-forge-1.20.1-1.3.1.jar` | Atmosphere layer tied to biome feel, weather, and shader/performance testing. |
| Subtle Effects | both | Modrinth | `SubtleEffects-forge-1.20.1-1.14.3.jar` | Atmosphere layer tied to biome feel, weather, and shader/performance testing. |
| Weather Storms & Tornadoes | both | Modrinth | `weather2-1.20.1-2.8.3.jar` | Weather/season/snow behavior. Atlas guards prevent warm-region snow and keep Frostmarch identity regional. |

### Cohesion / Recipes / Tags

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Alex's Delight | both | CurseForge | `alexsdelight-1.5.jar` | Crafting/food/mechanical economy. Recipe/tag unification and reward pacing matter. |
| Almost Unified | both | Modrinth | `almostunified-forge-1.20.1-0.11.0.jar` | Compatibility/material glue. Watch recipes, wood families, tags, and duplicate outputs. |
| Almost Unify Everything | both | Modrinth | `unifyeverything-1.20.1-1.0.2.9.jar` | Compatibility/material glue. Watch recipes, wood families, tags, and duplicate outputs. |
| Amendments | both | Modrinth | `amendments-1.20-2.2.5.jar` | Glue layer for recipes, wood sets, tags, material compatibility, structure palette cohesion, and pack-owned data overrides. |
| Create | both | Modrinth | `create-1.20.1-6.0.8.jar` | Crafting/food/mechanical economy. Recipe/tag unification and reward pacing matter. |
| Create Slice & Dice | both | Modrinth | `sliceanddice-forge-3.6.0.jar` | Crafting/food/mechanical economy. Recipe/tag unification and reward pacing matter. |
| Create: Structures Arise | both | Modrinth | `create_structures_arise-176.49.48 Forge 1.20.1.jar` | Create-themed structure layer; check loot and mechanical block palette fit with world regions. |
| Decorative Blocks | both | Modrinth | `decorative_blocks-forge-1.20.1-4.1.3.jar` | Glue layer for recipes, wood sets, tags, material compatibility, structure palette cohesion, and pack-owned data overrides. |
| Every Compat (Wood Good) | both | Modrinth | `everycomp-1.20-2.9.23-forge.jar` | Compatibility/material glue. Watch recipes, wood families, tags, and duplicate outputs. |
| Farmer's Delight | both | CurseForge | `FarmersDelight-1.20.1-1.3.2.jar` | Crafting/food/mechanical economy. Recipe/tag unification and reward pacing matter. |
| Handcrafted | both | Modrinth | `handcrafted-forge-1.20.1-3.0.6.jar` | Glue layer for recipes, wood sets, tags, material compatibility, structure palette cohesion, and pack-owned data overrides. |
| KubeJS | both | Modrinth | `kubejs-forge-2001.6.5-build.26.jar` | Runtime/data glue for Ascendant Core, Atlas status, progression HUD, recipes, tags, JEI aliases, and tooltips. |
| Macaw's Bridges | both | Modrinth | `mcw-bridges-3.1.2-mc1.20.1forge.jar` | Decorative/building palette. Bridges are especially relevant to future Atlas road/river seam fixes. |
| Macaw's Fences and Walls | both | Modrinth | `mcw-mcwfences-1.2.1-mc1.20.1forge.jar` | Decorative/building palette. Bridges are especially relevant to future Atlas road/river seam fixes. |
| Macaw's Lights and Lamps | both | CurseForge | `mcw-lights-1.1.5-mc1.20.1forge.jar` | Decorative/building palette. Bridges are especially relevant to future Atlas road/river seam fixes. |
| Open Loader | both | Modrinth | `OpenLoader-Forge-1.20.1-19.0.5.jar` | Datapack loader for pack-owned tags, dimension overrides, structures, loot, functions, and integration repairs. |
| Polymorph | both | Modrinth | `polymorph-forge-0.49.10+1.20.1.jar` | Compatibility/material glue. Watch recipes, wood families, tags, and duplicate outputs. |
| Quark | both | Modrinth | `Quark-4.0-462.jar` | Compatibility/material glue. Watch recipes, wood families, tags, and duplicate outputs. |
| Supplementaries | both | Modrinth | `supplementaries-1.20-3.1.43-forge.jar` | Compatibility/material glue. Watch recipes, wood families, tags, and duplicate outputs. |
| Zeta | both | Modrinth | `Zeta-1.0-31.jar` | Compatibility/material glue. Watch recipes, wood families, tags, and duplicate outputs. |

### Combat / Gear

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Better Combat | both | Modrinth | `bettercombat-forge-1.9.0+1.20.1.jar` | Core combat animation/hit system. Weapon balance, animation packs, and shields must be tested through it. |
| Combat Roll | both | Modrinth | `combatroll-forge-1.3.3+1.20.1.jar` | Player mobility layer. Changes encounter difficulty and boss readability. |
| Create Big Cannons | both | Modrinth | `createbigcannons-5.11.4-mc.1.20.1-forge.jar` | Crafting/food/mechanical economy. Recipe/tag unification and reward pacing matter. |
| Immersive Armors | both | Modrinth | `immersive_armors-1.7.2+1.20.1-forge.jar` | Armor/shield pool. Indexed for rarity and NPC/loot identity. |
| Marium's Soulslike Weaponry | both | CurseForge | `soulslike-weaponry-1.3.1-1.20.1-forge.jar` | High-value weapon pool. Indexed for rarity, loot tiers, JEI aliases, and skill hooks. |
| Projectile Damage Attribute | both | Modrinth | `projectile_damage-forge-3.2.2+1.20.1.jar` | Feeds the RPG combat loop, rarity labels, loot tiers, skill synergies, and boss/contract rewards. |
| Simply Swords | both | Modrinth | `simplyswords-forge-1.56.0-1.20.1.jar` | High-value weapon pool. Indexed for rarity, loot tiers, JEI aliases, and skill hooks. |
| Simply Swords Reforged | client | Modrinth | `Simply Swords Reforged v1.zip` | High-value weapon pool. Indexed for rarity, loot tiers, JEI aliases, and skill hooks. |
| Spartan Shields | both | Modrinth | `SpartanShields-1.20.1-forge-3.1.1.jar` | Armor/shield pool. Indexed for rarity and NPC/loot identity. |

### Custom / Local

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Ascendant Atlas Regions | both | Local source | `ascendant-atlas-regions-0.1.0.jar` | Pack-owned Forge helper. The coordinate-aware Overworld biome source and Atlas land-bias override were implemented, then disabled by Jayden on 2026-06-18 to restore random Tectonic/Terralith generation. The jar may remain for diagnostics/history, but active Overworld JSON must not reference it while random mode is selected. |
| Ascendant Nametags | client | Local source | `ascendant-nametags-0.1.0.jar` | Pack-owned Forge helper for player and AI hunter rank nameplates. Recreates the requested CustomNameTags-style behavior in Forge, adds `/ascnametag preview_self`, and deliberately does not install the Fabric CustomNameTags jar. |

### Dependency / Library

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Architectury API | both | CurseForge | `architectury-9.2.14-forge.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| AttributeFix | both | CurseForge | `AttributeFix-Forge-1.20.1-21.0.5.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Bookshelf | client | Modrinth | `Bookshelf-Forge-1.20.1-20.2.15.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Citadel | both | CurseForge | `citadel-2.6.3-1.20.1.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Cloth Config API | both | Modrinth | `cloth-config-11.1.136-forge.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Collective | both | Modrinth | `collective-1.20.1-8.25.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| CorgiLib | both | Modrinth | `Corgilib-Forge-1.20.1-4.0.3.4.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| CoroUtil | both | Modrinth | `coroutil-forge-1.20.1-1.3.7.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| CreativeCore | client | CurseForge | `CreativeCore_FORGE_v2.12.38_mc1.20.1.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Cristel Lib | both | Modrinth | `cristellib-1.1.6-forge.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Cupboard | both | CurseForge | `cupboard-1.20.1-3.7.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Curios API (Forge/NeoForge) | both | CurseForge | `curios-forge-5.14.1+1.20.1.jar` | Accessory/relic layer. Curios is infrastructure; Artifacts feeds loot, rarity, and build identity. |
| Data Anchor | both | Modrinth | `Data_Anchor-forge-1.20.1-1.0.0.20.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Easy NPC: Core | both | CurseForge | `easy_npc-forge-1.20.1-6.19.0.jar` | NPC population/role layer. Interacts with Guild staff, guards, rivals, settlements, and spawn safety. |
| Excalibur | client | Modrinth | `Excalibur_V1.20.zip` | Visual resource/model polish. Order and client-only side metadata matter. |
| Fragmentum | both | Modrinth | `fragmentum-forge-1.20.1-1.3.0.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| FTB Library (NeoForge) | both | CurseForge | `ftb-library-forge-2001.2.13.jar` | Quest/rank/team infrastructure for future formal rank trials and Guild progression. |
| Fzzy Config | both | Modrinth | `fzzy_config-0.7.6+1.20.1+forge.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| GeckoLib | both | CurseForge | `geckolib-forge-1.20.1-4.8.3.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| GlitchCore | both | Modrinth | `GlitchCore-forge-1.20.1-0.0.1.1.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Iceberg | client | Modrinth | `Iceberg-1.20.1-forge-1.1.25.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Jupiter | both | Modrinth | `jupiter-2.3.7-1.20.1-forge.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Kambrik | both | Modrinth | `Kambrik-6.1.1+1.20.1-forge.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Kiwi | both | Modrinth | `Kiwi-1.20.1-Forge-11.10.2.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Konkrete | client | CurseForge | `konkrete_forge_1.8.0_MC_1.20-1.20.1.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Kotlin for Forge | both | Modrinth | `kotlinforforge-4.12.0-all.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Lionfish API | both | CurseForge | `lionfishapi-3.0.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Melody | client | CurseForge | `melody_forge_1.0.3_MC_1.20.1-1.20.4.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Moonlight Lib | both | Modrinth | `moonlight-1.20-2.16.33-forge.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| playerAnimator | both | CurseForge | `player-animation-lib-forge-1.0.2-rc1+1.20.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Prism | client | Modrinth | `Prism-1.20.1-forge-1.0.5.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Puzzles Lib | both | CurseForge | `PuzzlesLib-v8.1.33-1.20.1-Forge.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Resourceful Lib | both | Modrinth | `resourcefullib-forge-1.20.1-2.1.29.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Rhino | both | Modrinth | `rhino-forge-2001.2.3-build.10.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Ritchie's Projectile Library | both | Modrinth | `ritchiesprojectilelib-2.1.1+mc.1.20.1-forge.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| ShatterLib \| OctoLib | client | Modrinth | `OctoLib-FORGE-0.5.0.1+1.20.1.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Silent Lib | both | Modrinth | `silent-lib-1.20.1-8.0.0.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Sodium Options API | client | Modrinth | `sodiumoptionsapi-forge-1.0.10-1.20.1.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| TenshiLib (Forge/NeoForge) | both | CurseForge | `tenshilib-1.20.1-1.7.6-forge.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| Uranus | both | Modrinth | `uranus-2.2.6-bugfix.2-1.20.1-forge.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| WATERMeDIA: Binaries | client | CurseForge | `wm_binaries-3.0.0-rc.1.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |
| WATERMeDIA: Multimedia API | client | CurseForge | `watermedia-3.0.0.17.jar` | Required API/runtime support. Usually do not tune directly, but side and version compatibility matter. |

### Loot / Contracts

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Artifacts | both | Modrinth | `artifacts-forge-9.5.19.jar` | Accessory/relic layer. Curios is infrastructure; Artifacts feeds loot, rarity, and build identity. |
| Bountiful | both | Modrinth | `Bountiful-6.0.4+1.20.1-forge.jar` | Bounty/contract system. Receives generated Guild objectives and reward pools. |
| FTB Quests (NeoForge) | both | CurseForge | `ftb-quests-forge-2001.4.22.jar` | Quest/rank/team infrastructure for future formal rank trials and Guild progression. |
| FTB Ranks (NeoForge) | both | CurseForge | `ftb-ranks-forge-2001.1.7.jar` | Quest/rank/team infrastructure for future formal rank trials and Guild progression. |
| FTB Teams (NeoForge) | both | CurseForge | `ftb-teams-forge-2001.3.2.jar` | Quest/rank/team infrastructure for future formal rank trials and Guild progression. |
| Loot Beams: Relooted! | client | Modrinth | `lootbeams-1.20.1-1.2.2.jar` | Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback. |
| Loot Integrations | both | CurseForge | `lootintegrations-1.20.1-4.7.jar` | Feeds Bountiful, loot tables, guide books, bounty objectives, and reward visibility. |
| Loot Journal: Pickup Notifier | client | Modrinth | `loot_journal-forge-1.20.1-6.2.1.jar` | Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback. |
| Patchouli | both | CurseForge | `Patchouli-1.20.1-85-FORGE.jar` | Ascendant Codex guidebook surface through OpenLoader data. |

### Magic

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Iron's Lib | both | CurseForge | `irons_lib-1.20.1-1.1.0.jar` | Magic progression and spell loot. Needs skill tree hooks, rank gates, and boss/structure rewards. |
| Iron's Spells 'n Spellbooks | both | CurseForge | `irons_spellbooks-1.20.1-3.16.1.jar` | Magic progression and spell loot. Needs skill tree hooks, rank gates, and boss/structure rewards. |
| Obscure API | both | Modrinth | `obscure_api-18.jar` | Feeds spell progression, magical loot, skill hooks, boss rewards, and class fantasy. |
| Snow! Real Magic! | both | Modrinth | `SnowRealMagic-1.20.1-Forge-10.7.0.jar` | Weather/season/snow behavior. Atlas guards prevent warm-region snow and keep Frostmarch identity regional. |

### Mobs / Bosses

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Alex's Mobs | both | CurseForge | `alexsmobs-1.22.9.jar` | Animal/monster ecology. Spawns are part of regional feel and bounty candidate pool. |
| Aquamirae | both | Modrinth | `aquamirae-forge-1.20.1-6.4.0.jar` | Ocean/frozen-ocean structure and mob layer. Surface structure set is overridden to reduce dense spawn clusters. |
| Born in Chaos | both | Modrinth | `born_in_chaos_[Forge]1.20.1_1.7.5.jar` | High-pressure hostile ecology. Interacts with In Control caps, villages, and early-game safety. |
| Bosses'Rise | both | Modrinth | `block_factorys_bosses-2.1.2-forge-1.20.1.jar` | Adds hostile/passive entity pressure, boss goals, structure inhabitants, drops, and bounty targets. |
| Enhanced Boss Bars | client | Modrinth | `enhanced_boss_bars-1.20.1-1.0.0.jar` | Adds hostile/passive entity pressure, boss goals, structure inhabitants, drops, and bounty targets. |
| IceAndFire Community Edition | both | Modrinth | `IceAndFireCE-1.2.5-1.20.1-forge.jar` | Dragon/mythic ecology plus structures, loot, armor, and ores. Needs boss/biome/rank tuning. |
| L_Ender's Cataclysm | both | Modrinth | `L_Enders_Cataclysm-3.30.jar` | Major boss/dungeon layer. Treat as late-game content and wire rewards to rank/progression. |
| Mowzie's Mobs | both | Modrinth | `mowziesmobs-1.8.2.jar` | Boss/mob layer with structures. Good for bounty targets and regional danger spikes. |

### Performance

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Embeddium | client | Modrinth | `embeddium-0.3.31+mc1.20.1.jar` | Client/performance/rendering stack. Verify after shaders, particles, animations, or large worldgen changes. |
| Entity Culling | client | Modrinth | `entityculling-forge-1.10.2-mc1.20.1.jar` | Client/performance/rendering stack. Verify after shaders, particles, animations, or large worldgen changes. |
| FerriteCore | both | Modrinth | `ferritecore-6.0.1-forge.jar` | Client/performance/rendering stack. Verify after shaders, particles, animations, or large worldgen changes. |
| ModernFix | both | Modrinth | `modernfix-forge-5.27.50+mc1.20.1.jar` | Client/performance/rendering stack. Verify after shaders, particles, animations, or large worldgen changes. |
| Sodium Dynamic Lights | client | Modrinth | `sodiumdynamiclights-forge-1.0.10-1.20.1.jar` | Client/performance/rendering stack. Verify after shaders, particles, animations, or large worldgen changes. |

### Resource Pack

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Embellished Stone (Advancements Plaques) | client | Modrinth | `EmbellishedStone-1.20.1-1.0.0.zip` | Visual cohesion layer. Order matters because several packs intentionally override mod textures/models. |
| Vanilla Experience+ | client | Modrinth | `Vanilla Experience Plus.zip` | Visual resource/model polish. Order and client-only side metadata matter. |

### Shader / Visual Base

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| 3D Skin Layers | client | Modrinth | `skinlayers3d-forge-1.11.1-mc1.20.1.jar` | Visual resource/model polish. Order and client-only side metadata matter. |
| [EMF] Entity Model Features | client | Modrinth | `entity_model_features-3.2.4-1.20.1-forge.jar` | Visual resource/model polish. Order and client-only side metadata matter. |
| [ETF] Entity Texture Features | client | Modrinth | `entity_texture_features_1.20.1-forge-7.1.jar` | Visual resource/model polish. Order and client-only side metadata matter. |
| AppleSkin | both | CurseForge | `appleskin-forge-mc1.20.1-2.5.1.jar` | Client visual base: shaders, model features, animation support, particles, and rendering compatibility. |
| Complementary Shaders - Reimagined | client | Modrinth | `ComplementaryReimagined_r5.8.1.zip` | Client visual base: shaders, model features, animation support, particles, and rendering compatibility. |
| Cubic Leaves | client | Modrinth | `Cubic Leaves 2.3 (performance).zip` | Visual resource/model polish. Order and client-only side metadata matter. |
| Cubic Sun & Moon | client | Modrinth | `cubic-sun-moon-v1.8.5.zip` | Visual resource/model polish. Order and client-only side metadata matter. |
| Fresh Animations | client | Modrinth | `FreshAnimations_v1.10.4.zip` | Visual resource/model polish. Order and client-only side metadata matter. |
| Malfu Combat Animation | both | Modrinth | `malfu-combat-animation-3.1.jar` | Client visual base: shaders, model features, animation support, particles, and rendering compatibility. |
| Not Enough Animations | client | Modrinth | `notenoughanimations-forge-1.12.3-mc1.20.1.jar` | Client visual base: shaders, model features, animation support, particles, and rendering compatibility. |
| Oculus | client | Modrinth | `oculus-mc1.20.1-1.8.0.jar` | Client/performance/rendering stack. Verify after shaders, particles, animations, or large worldgen changes. |
| Wavey Capes | client | Modrinth | `waveycapes-forge-1.9.2-mc1.20.1.jar` | Client visual base: shaders, model features, animation support, particles, and rendering compatibility. |

### Skills / Difficulty

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Improved Mobs (Forge, NeoForge) | both | CurseForge | `improvedmobs-1.20.1-1.13.6-forge.jar` | Difficulty/spawn-pressure modifier. Must be balanced against early villages, Guild ranks, and In Control caps. |
| In Control! | both | Modrinth | `incontrol-1.20-9.4.6.jar` | Spawn guardrail layer using Atlas coordinate areas and settlement safety caps. |
| Majrusz Library | both | CurseForge | `majrusz-library-forge-1.20.1-7.0.8.jar` | Difficulty/spawn-pressure modifier. Must be balanced against early villages, Guild ranks, and In Control caps. |
| Majrusz's Progressive Difficulty | both | CurseForge | `majruszs-difficulty-forge-1.20.1-1.9.10.jar` | Difficulty/spawn-pressure modifier. Must be balanced against early villages, Guild ranks, and In Control caps. |
| Pufferfish's Attributes | both | Modrinth | `puffish_attributes-0.8.2-1.20-forge.jar` | Skill/attribute foundation. Ascendant Web and HUD bridge depend on it. |
| Pufferfish's Skills | both | Modrinth | `puffish_skills-0.18.0-1.20-forge.jar` | Owns player growth, level pressure, difficulty scaling, attributes, and future rank gates. |
| Scaling Health | both | Modrinth | `ScalingHealth-1.20.1-8.0.2+9.jar` | Difficulty/spawn-pressure modifier. Must be balanced against early villages, Guild ranks, and In Control caps. |
| Spawn Balance Utility | both | CurseForge | `spawnbalanceutility-1.20-46.13.7.jar` | Difficulty/spawn-pressure modifier. Must be balanced against early villages, Guild ranks, and In Control caps. |

### Storage / QoL

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Just Enough Items (JEI) | client | Modrinth | `jei-1.20.1-forge-15.20.0.130.jar` | Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback. |
| Sophisticated Backpacks | both | Modrinth | `sophisticatedbackpacks-1.20.1-3.24.53.1877.jar` | Storage QoL. Make sure storage access does not trivialize intended loot pacing. |
| Sophisticated Core | both | Modrinth | `sophisticatedcore-1.20.1-1.3.50.2005.jar` | Storage QoL. Make sure storage access does not trivialize intended loot pacing. |
| Visual Workbench | both | Modrinth | `VisualWorkbench-v8.0.1-1.20.1-Forge.jar` | Visual resource/model polish. Order and client-only side metadata matter. |

### UI / Presentation

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Advancement Plaques | client | Modrinth | `AdvancementPlaques-1.20.1-forge-1.6.9.jar` | Owns title screen, HUD, tooltips, rarity borders, titles, minimap, health bars, and player-facing clarity. |
| Beautiful Enchanted Books [MOD EDITION] | client | Modrinth | `BEB-Forge-1.20.1-6.0.0.jar` | Visual resource/model polish. Order and client-only side metadata matter. |
| Drippy Loading Screen | client | CurseForge | `drippyloadingscreen_forge_3.1.2_MC_1.20.1.jar` | Main-menu/loading presentation. Depends on packaged assets and resource-pack order. |
| Enchantment Descriptions | client | Modrinth | `EnchantmentDescriptions-Forge-1.20.1-17.1.21.jar` | Owns title screen, HUD, tooltips, rarity borders, titles, minimap, health bars, and player-facing clarity. |
| FancyMenu | client | CurseForge | `fancymenu_forge_3.9.3_MC_1.20.1.jar` | Main-menu/loading presentation. Depends on packaged assets and resource-pack order. |
| Icon Fresh | client | Modrinth | `Icon Fresh 1.2.zip` | Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback. Visual resource/model polish. Order and client-only side metadata matter. |
| Icon Xaero's | client | Modrinth | `Icon Xaero's 1.22.zip` | Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback. Visual resource/model polish. Order and client-only side metadata matter. |
| Immersive UI | client | Modrinth | `ImmersiveUI-FORGE-0.3.0.jar` | Owns title screen, HUD, tooltips, rarity borders, titles, minimap, health bars, and player-facing clarity. |
| Item Borders [Neo/Forge] | client | CurseForge | `ItemBorders-1.20.1-forge-1.2.2.jar` | Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback. |
| Legendary Tooltips | client | Modrinth | `LegendaryTooltips-1.20.1-forge-1.4.5.jar` | Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback. |
| Overflowing Bars | client | CurseForge | `OverflowingBars-v8.0.1-1.20.1-Forge.jar` | Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback. |
| Perception | client | Modrinth | `Perception-FORGE-0.1.4+1.20.1.jar` | Owns title screen, HUD, tooltips, rarity borders, titles, minimap, health bars, and player-facing clarity. |
| Resource Pack Overrides | client | Modrinth | `ResourcePackOverrides-v8.0.3-1.20.1-Forge.jar` | Forces resource-pack order so visual fallbacks and UI packs load reliably. |
| SpiffyHUD | client | CurseForge | `spiffyhud_forge_3.1.2_MC_1.20.1.jar` | Owns title screen, HUD, tooltips, rarity borders, titles, minimap, health bars, and player-facing clarity. |
| STONEBORN UI Overhaul | client | Modrinth | `STONEBORN+-+1.20-1.20.1+-+V3.2.3.zip` | Visual resource/model polish. Order and client-only side metadata matter. |
| Stylish Effects | client | CurseForge | `StylishEffects-v8.0.2-1.20.1-Forge.jar` | Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback. |
| The Rename Compat Project | client | Modrinth | `Rename Compat Project.zip` | Owns title screen, HUD, tooltips, rarity borders, titles, minimap, health bars, and player-facing clarity. |
| Titles | both | CurseForge | `Titles-1.20.1-3.8.3.jar` | Biome/dimension title presentation and region flavor. |
| Traveler's Titles | client | Modrinth | `TravelersTitles-1.20-Forge-4.0.2.jar` | Biome/dimension title presentation and region flavor. |
| Visual Traveler's Title Biomes Addon | client | Modrinth | `Visual Travelers Titles Biomes Addon.zip` | Moog structure family. High structure volume; tune density and biome fit before adding more structure mods. Biome/dimension title presentation and region flavor. |
| Visual Traveler's Titles | client | Modrinth | `Visual Titles 1.3.zip` | Biome/dimension title presentation and region flavor. |
| Xaero's Minimap | client | Modrinth | `xaerominimap-forge-1.20.1-26.1.0.jar` | Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback. |
| YDM's MobHealthBar | client | Modrinth | `mobhealthbar-forge-1.20.x-2.3.0.jar` | Player-facing clarity: rarity, drops, search, health/state, minimap, and loot feedback. |

### Villages / NPCs

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| CustomNPCs-Unofficial | both | CurseForge | `CustomNPCs-1.20.1-GBPort-Unofficial-1.20.1.20260227.jar` | NPC population/role layer. Interacts with Guild staff, guards, rivals, settlements, and spawn safety. |
| Easy NPC | both | CurseForge | `easy_npc_bundle-forge-1.20.1-6.19.0.jar` | NPC population/role layer. Interacts with Guild staff, guards, rivals, settlements, and spawn safety. |
| Easy NPC: Config UI | both | CurseForge | `easy_npc_config_ui-forge-1.20.1-6.19.0.jar` | NPC population/role layer. Interacts with Guild staff, guards, rivals, settlements, and spawn safety. |
| Human Companions | both | CurseForge | `humancompanions-1.20.1-1.7.6.jar` | NPC population/role layer. Interacts with Guild staff, guards, rivals, settlements, and spawn safety. |

### Worldgen / Structures

| Entry | Side | Source | File | Role / interaction |
|---|---|---|---|---|
| Fantasy Armor (Medieval Series) | both | Modrinth | `fantasy_armor-forge-1.2.4-1.20.1.jar` | Armor/shield pool. Indexed for rarity and NPC/loot identity. |
| Guard Villagers | both | Modrinth | `guardvillagers-1.20.1-1.6.18.jar` | NPC population/role layer. Interacts with Guild staff, guards, rivals, settlements, and spawn safety. |
| Integrated API | both | Modrinth | `integrated_api-1.7.2+1.20.1-forge.jar` | Adds terrain, biomes, structures, villages, dungeons, roads, structure loot, and spawn surfaces. |
| Integrated Dungeons and Structures | both | Modrinth | `idas_forge-1.13.0+1.20.1.jar` | Large dungeon/structure source. Check biome tags, loot, and density before moving structures. |
| Integrated Villages | both | Modrinth | `integrated_villages-1.3.2+1.20.1-forge.jar` | Village expansion layer with known processor/tag repairs in the world-integration datapack. |
| MCA - Default Medieval | client | CurseForge | `MCAR_VanillaMedieval_Universal_1.20.x_Only_Clothes_byDE4THR4SH_v4.zip` | Village NPC identity layer. Medieval clothing/resource pack is required for tone. |
| MCA Reborn [Fabric/Forge] | both | CurseForge | `minecraft-comes-alive-7.6.16+1.20.1-universal.jar` | Moog structure family. High structure volume; tune density and biome fit before adding more structure mods. Village NPC identity layer. Medieval clothing/resource pack is required for tone. |
| Medieval Buildings [End Edition] | both | Modrinth | `forge-medievalend-1.0.1.jar` | Adds terrain, biomes, structures, villages, dungeons, roads, structure loot, and spawn surfaces. |
| Medieval Buildings [Nether Edition] | both | Modrinth | `medieval_buildings_nether_edition-1.20.1-1.0.2-forge.jar` | Adds terrain, biomes, structures, villages, dungeons, roads, structure loot, and spawn surfaces. |
| Medieval Music | client | CurseForge | `MedievalMusic.zip` | Adds terrain, biomes, structures, villages, dungeons, roads, structure loot, and spawn surfaces. |
| MES - Moog's End Structures | both | Modrinth | `MoogsEndStructures-1.20-2.0.3.jar` | Moog structure family. High structure volume; tune density and biome fit before adding more structure mods. |
| Moog's Structure Lib (moogs_structures) | both | Modrinth | `moogs_structures-1.20-1.20.4-alpha-3.0.0-forge.jar` | Moog structure family. High structure volume; tune density and biome fit before adding more structure mods. |
| MSS - Moog's Soaring Structures | both | Modrinth | `MoogsSoaringStructures-1.20-2.1.0.jar` | Moog structure family. High structure volume; tune density and biome fit before adding more structure mods. |
| MVS - Moog's Voyager Structures | both | Modrinth | `MoogsVoyagerStructures-1.20-5.0.6.jar` | Moog structure family. High structure volume; tune density and biome fit before adding more structure mods. |
| Small Ships | both | Modrinth | `smallships-forge-1.20.1-2.0.0-b1.4.jar` | Adds terrain, biomes, structures, villages, dungeons, roads, structure loot, and spawn surfaces. |
| Sparse Structures | both | Modrinth | `sparsestructures-forge-1.20.1-3.0.jar` | Global structure-spacing pressure valve. Use alongside per-structure-set overrides, not as the only density fix. |
| Structory | both | Modrinth | `Structory_1.20.x_v1.3.5.jar` | Ambient structure layer; tune for density and biome identity rather than blanket disabling. |
| Tectonic | both | Modrinth | `tectonic-mod-1.19.3-v2.2.1.jar` | Terrain/noise shape layer. Atlas controls biome source while Tectonic-style terrain shape must remain intact. |
| Terralith | both | Modrinth | `Terralith_1.20.x_v2.5.4.jar` | Primary biome table provider for Atlas worldgen. Do not classify its biomes by name alone; inspect biome JSON and Terralith climate entries. |
| Towns and Towers | both | Modrinth | `Towns-and-Towers-1.12-Fabric+Forge.jar` | Major village/outpost structure provider. Interacts heavily with Integrated Villages, MCA, roads, and Guild settlement tuning. |
| Villager Names | both | Modrinth | `villagernames-1.20.1-8.5.jar` | Moog structure family. High structure volume; tune density and biome fit before adding more structure mods. NPC population/role layer. Interacts with Guild staff, guards, rivals, settlements, and spawn safety. |
| Villages&Pillages | both | Modrinth | `villagesandpillages-forge-mc1.20.1-1.0.2.jar` | Adds terrain, biomes, structures, villages, dungeons, roads, structure loot, and spawn surfaces. |
| YUNG's API | both | Modrinth | `YungsApi-1.20-Forge-4.0.6.jar` | Dungeon/bridge/stronghold/mineshaft/extras overhaul family. Good content, but bridge/road/river seams need field validation. |
| YUNG's Better Dungeons | both | Modrinth | `YungsBetterDungeons-1.20-Forge-4.0.4.jar` | Dungeon/bridge/stronghold/mineshaft/extras overhaul family. Good content, but bridge/road/river seams need field validation. |
| YUNG's Better Mineshafts | both | Modrinth | `YungsBetterMineshafts-1.20-Forge-4.0.4.jar` | Dungeon/bridge/stronghold/mineshaft/extras overhaul family. Good content, but bridge/road/river seams need field validation. |
| YUNG's Better Strongholds | both | Modrinth | `YungsBetterStrongholds-1.20-Forge-4.0.3.jar` | Dungeon/bridge/stronghold/mineshaft/extras overhaul family. Good content, but bridge/road/river seams need field validation. |
| YUNG's Bridges | both | Modrinth | `YungsBridges-1.20-Forge-4.0.3.jar` | Dungeon/bridge/stronghold/mineshaft/extras overhaul family. Good content, but bridge/road/river seams need field validation. |
| YUNG's Extras | both | Modrinth | `YungsExtras-1.20-Forge-4.0.3.jar` | Dungeon/bridge/stronghold/mineshaft/extras overhaul family. Good content, but bridge/road/river seams need field validation. |

## Operational Rules For The Next AI

- Before changing worldgen, regenerate or inspect `docs/WORLDGEN_CONTENT_AUDIT.md`; biome names are not reliable enough.
- Before changing structures, inspect structure sets, template pools, block palettes, and biome tags. Do not assume by structure name only.
- Before changing mobs, inspect biome spawns, structure spawn overrides, In Control rules, and settlement safety pressure.
- Prefer datapack/config/KubeJS fixes when they are enough. Use helper mods only for behavior that data cannot express safely.
- Never sync into the active CurseForge instance while Minecraft is running.
- Fresh world or ungenerated chunks are required to judge worldgen changes; existing chunks keep old terrain and placed blocks.
- Run `python scripts\check-pack.py` after edits. Run the Atlas generator/audit/build scripts after worldgen edits.

## Generated From

- `pack.toml` and `index.toml`.
- Root `mods/*.pw.toml`, `resourcepacks/*.pw.toml`, and `shaderpacks/*.pw.toml`.
- Local helper jar `mods/ascendant-atlas-regions-0.1.0.jar`.
- `docs/UNIVERSAL_MOD_INDEX.md` category and integration-target rows.
- `config/ascendant_index/*.json` registry counts.
- `docs/generated/worldgen_content_audit.json` worldgen audit counts.
