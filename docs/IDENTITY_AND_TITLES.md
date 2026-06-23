# Identity And Titles

Batch K is installed and validated. The latest multiplayer playtest found that Titles did not automatically make visible ranks/levels appear above player names, so an Ascendant scoreboard/team bridge has been staged through OpenLoader and KubeJS.

`docs/GUILD_HUNTER_SYSTEM_RUNDOWN.md` is the master direction for the larger Guild rank system. This file covers the current Titles/scoreboard identity layer; the Guild rundown defines Unranked through S-Rank evaluation, Rank Examiner NPCs, Hunter Board identity, and missing quest/rank tooling.

## Goal

Add earned player identity without turning playtime into the main rank system.

## Recommended Mods

| Candidate | Source | 1.20.1 Forge status | Side | Batch K decision |
|---|---|---|---|---|
| Titles | CurseForge | Installed: `Titles-1.20.1-3.8.3.jar` | Both | Installed |
| IntegratedPlaytime | CurseForge | Verified Forge 1.20.1 signal | Server-only by provider description | Optional/delayed secondary system only |
| CustomNameTags | Modrinth | Rejected for this pack: visible project is Fabric/server-side | Server-only on Fabric | Reject |

Sources:

- Titles: https://www.curseforge.com/minecraft/mc-mods/titles/files/6301038
- IntegratedPlaytime: https://www.curseforge.com/minecraft/mc-mods/integratedplaytime
- CustomNameTags: https://modrinth.com/project/TizFPouK

## Design Direction

Titles should represent achievement, not idle time. The first title set should come from:

- Skill branch identity: Warrior, Duelist, Hunter, Arcanist, Artificer, Explorer, Dragonbound.
- Boss kills: Cataclysm bosses, Bosses'Rise encounters, Mowzie's Mobs bosses, Aquamirae threats.
- Dragon milestones: first dragon encounter, first dragon kill, dragon gear progression.
- Major exploration milestones: first distant village chain, first End/Nether landmark, first bounty-board arc.
- Engineering milestones: Create machinery, cannon ownership/use, major workshop achievement.

Titles can be granted by advancement-style milestones because the Titles mod is advancement-driven. The custom implementation should avoid adding a separate always-on playtime ladder.

Packwiz did not add extra dependencies for Titles.

## Visible Level Display

Use the vanilla scoreboard display slot first, because it is predictable on a dedicated server:

- Preferred numeric level display: a scoreboard objective displayed below player names.
- Optional fixed identity label: teams with static prefixes such as `[Arcanist]` or `[Dragonbound]`.
- Do not assume dynamic score values inside team prefixes until tested in-game.

Active fallback:

- `config/openloader/data/ascendant_realms_identity/` creates `ar_skill_level` plus XP and skill-point mirror objectives.
- `kubejs/server_scripts/ascendant_progression.js` reads Puffish Skills Ascendant Web data and updates `ar_skill_level`.
- The `ar_skill_level` objective is displayed below player names.
- Players without an existing team are assigned to `ar_ascendant`, which adds a static `[Ascendant]` prefix.
- A `Level Up! <level>` title popup, sound, and HUD banner play when the Ascendant Web level increases.
- The custom Ascendant Web XP HUD bar is rendered by KubeJS Painter.

IntegratedPlaytime can be revisited later as a secondary cosmetic rank or `/playtime` tracker, but it should not drive the main Ascendant rank.

Future Guild rank work should evaluate FTB Quests plus FTB Ranks or a clean replacement before replacing the current fallback. Main rank should be earned from bounties, boss kills, village protection, structure clearing, magic/weapon milestones, and rival context rather than playtime.

## Guild/Hunter Tooling Update

FTB Quests and FTB Ranks are now installed for the Guild/Hunter spine, alongside the existing vanilla scoreboard fallback.

Current role split:

- Ascendant scoreboard bridge: active now for visible Puffish/Ascendant level below names, static `[Ascendant]` team prefix, skill-XP HUD bar, and `Level Up!` popup.
- FTB Quests: installed for future hidden Guild milestones, evaluation chapters, bounty/rank criteria, and rival-hunter quest arcs.
- FTB Ranks: installed for rank-display and permission experiments after the generated config format is confirmed.
- Titles: remains the achievement/title layer, not the main rank engine.

Do not remove the vanilla fallback yet. It remains the stable multiplayer-visible identity layer until FTB Quests/Ranks pass boot testing and an authored rank flow exists.

## Testing Plan

Client:

- Confirm Titles loads with no missing dependency screen.
- Confirm earned titles render near/with player names.
- Confirm title selection UI or commands work if exposed by the mod.
- Confirm `ar_skill_level` display works in third-person or from a second client.
- Confirm the `[Ascendant]` prefix appears for players without custom teams.
- Confirm the `Level Up!` popup appears after gaining an Ascendant Web level.
- Confirm the custom Ascendant XP bar updates after killing mobs.
- Confirm titles do not collide badly with Traveler's Titles, Xaero's Minimap, or mob health bars.

Server:

- Confirm no mod mismatch.
- Confirm titles persist after disconnect/rejoin.
- Confirm scoreboard objective persists after reconnect.
- Confirm static team prefix labels persist if used.
- Run a 10-minute stability check.
