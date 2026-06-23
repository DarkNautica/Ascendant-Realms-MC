# Guild Hunter Implementation Status

Status: first Guild/Hunter spine installed and scaffolded. It still needs client boot validation, dedicated server validation, and in-game authoring before it is considered playable content.

## Installed Tooling

All Guild/Hunter tools are currently marked both-side for the private multiplayer workflow because they affect NPCs, quests, ranks, guidebook data, or companion entities.

| Tool | Packwiz file | Side | Purpose |
|---|---|---|---|
| Patchouli | `Patchouli-1.20.1-85-FORGE.jar` | Both | Ascendant Codex in-game guidebook |
| FTB Quests | `ftb-quests-forge-2001.4.22.jar` | Both | Rank milestones, guided questlines, hidden progress |
| FTB Library | `ftb-library-forge-2001.2.13.jar` | Both | FTB dependency |
| FTB Teams | `ftb-teams-forge-2001.3.2.jar` | Both | FTB Quests team/progression dependency |
| FTB Ranks | `ftb-ranks-forge-2001.1.7.jar` | Both | Guild rank and permission/display experiments |
| Easy NPC | `easy_npc_bundle-forge-1.20.1-6.19.0.jar` | Both | Guild clerks, Rank Examiners, social NPCs |
| Easy NPC Core | `easy_npc-forge-1.20.1-6.19.0.jar` | Both | Easy NPC dependency |
| Easy NPC Config UI | `easy_npc_config_ui-forge-1.20.1-6.19.0.jar` | Both | Easy NPC dependency/config UI |
| CustomNPCs-Unofficial | `CustomNPCs-1.20.1-GBPort-Unofficial-1.20.1.20260227.jar` | Both | Named rivals and combat-capable special NPCs |
| Human Companions | `humancompanions-1.20.1-1.7.6.jar` | Both | Generic hunter presence and companion testing |

## Generated Pack Data

- `config/ascendant_guild/ranks.json` defines Unranked, E, D, C, B, A, and S ranks.
- `config/ascendant_guild/rival_hunters.json` defines Mira Ash, Darius Crowe, Seren Valehart, Kael Vorn, and The Black Hound.
- `config/ascendant_guild/bounty_categories.json` defines village requests, monster hunts, dungeon contracts, rescue missions, rival-claimed contracts, and realm threats.
- `config/ascendant_guild/hunter_boards.json` defines village, town, and major Guild board standards.
- `config/ascendant_guild/npc_roster.json` defines starter Guild roles.
- `config/ascendant_guild/tool_audit.json` records installed tools and delayed pieces.
- `config/ascendant_guild/generated_npc_profiles.json` and `generated_npc_spawn_sets.json` now create non-manual Guild NPC spawn sets.
- `config/ascendant_guild/live_bountiful_pools.json` records the active Bountiful contract pool slice.
- `config/openloader/data/ascendant_realms_guild/` now carries generated NPC functions, Bountiful contract pools, and standalone Guild/Hunter structures.
- `config/openloader/data/ascendant_realms_codex/` contains the active Patchouli Ascendant Codex pack.
- `openloader/data/ascendant_realms_codex/` and `datapacks/ascendant_realms_codex/` are source/fallback mirrors.
- `config/openloader/data/ascendant_realms_identity/` now includes Guild rank function scaffolds.
- `kubejs/startup_scripts/ascendant_guild_items.js` adds starter Guild currency concept items: `guild_mark`, `hunter_seal`, and `ascendant_sigil`.

## Delayed Or Not Finished

- MCA Reborn is installed with MCA - Default Medieval default-enabled, but remains unverified until village skin/control and server behavior testing passes.
- FTB quest chapter files are not authored yet. Use the in-game FTB Quests editor or generated SNBT only after the current file format is confirmed in this pack.
- FTB Ranks config is not authored yet. Let the first boot generate the expected config shape before scripting rank assignment.
- NPC placement is not done. Easy NPC and CustomNPCs need in-game prototypes for Guild Clerk, Rank Examiner, Bounty Master, and the first rival hunters.
- CustomNPCs identity automation exists. Use `node scripts\test-customnpcs-identity.js` for script logic, `powershell -ExecutionPolicy Bypass -File scripts\sync-active-client-files.ps1` to sync active client files, and `python scripts\customnpcs-identity-audit.py` to audit/repair saved NPC entities, including stale embedded script copies. The Rank Examiner `[Unranked]` bug is traced to stale saved entity data plus the old script accepting placeholder `Unranked`; the script now falls back to the profile baseline rank.
- Hunter Board structures are not built yet. The first target is the "Hunter Board - Village Standard" from the master rundown.
- Guild currency item textures/models are placeholder-only.
- The Ascendant Codex is a starter outline, not the final guidebook.

## Client Test Plan

- Import the latest client ZIP into the active CurseForge instance.
- Launch the client and confirm no missing dependency screen.
- Confirm KubeJS creates `guild_mark`, `hunter_seal`, and `ascendant_sigil`.
- Confirm Patchouli loads and the Ascendant Codex appears.
- Confirm FTB Quests UI opens.
- Confirm FTB Ranks commands/config are available enough for later rank testing.
- Confirm Easy NPC menus/items work.
- Confirm CustomNPCs tools/items or creative access works.
- Confirm Human Companions can spawn or appear without visual/server errors.
- Create or load a creative test world.
- Run the rank functions manually in a copied test world if commands are available.
- Save/reload.

## Dedicated Server Test Plan

- Export server staging.
- Reimport the latest client ZIP before materializing server jars.
- Materialize from the active CurseForge mods folder with `-Clean`.
- Confirm the final server jar list includes the Guild/Hunter tooling set.
- Boot Forge 1.20.1-47.4.20 with Java 17.
- Join localhost and confirm no mod mismatch.
- Confirm KubeJS startup has no errors.
- Confirm the Ascendant Codex datapack is present server-side.
- Confirm FTB Quests/Ranks do not reject the client.
- Confirm Easy NPC, CustomNPCs, and Human Companions do not crash on entity/NPC testing.
- Disconnect/rejoin.
- Let the server run 10 minutes.

## Recommended Next Steps

1. Reimport the new client ZIP into CurseForge.
2. Complete the Guild/Hunter client boot and creative/system test.
3. Materialize the server after the client import and complete the dedicated server boot/join test.
4. In a creative copy, build the first Hunter Board - Village Standard.
5. Use the FTB Quests in-game editor to author the first Guild evaluation questline, then export its files into the pack.
6. Use Easy NPC or CustomNPCs to create Guild Clerk, Rank Examiner, Bounty Master, and one rival prototype.
7. Polish the Ascendant Codex entries once the first board and NPCs exist in-world.
8. Validate MCA Reborn and MCA - Default Medieval in a fresh client/server pass before marking the Guild/Hunter NPC layer stable.
