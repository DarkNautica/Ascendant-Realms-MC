# Rank Nameplate And Examiner System

Status: live modular Forge renderer implemented. No Fabric nameplate mod was installed.

The requested CustomNameTags look is useful as a style reference, but the attached/reference jar is Fabric/server-side and does not fit this Forge 1.20.1 pack. Ascendant Realms now recreates the needed behavior inside the local `Ascendant Nametags` Forge helper jar:

- Players: Forge client `RenderNameTagEvent` override renders `[Rank] Name | Lv.X` from `ar_guild_rank` and `ar_skill_level`.
- AI hunters: Forge client `RenderNameTagEvent` override renders rank/profile nameplates from `ar_ai_hunter` and profile tags.
- Self preview: `/ascnametag preview_self` temporarily renders the local player's styled nameplate above the actual third-person player model.
- Text effects: player, preview, and AI hunter plates now use the same world-space animated rank renderer with per-character gradients, rank-colored glow passes, and rank-specific motion styles.
- Backup/fallback: vanilla scoreboard teams for public Guild rank prefix and `ar_skill_level` below the name remain active.
- Authored NPCs: CustomNPCs scripted visible name line.
- Rank testing: talk to the Rank Examiner NPC. The function command is only a hidden/test hook.

## Player Nameplates

The active datapack is `config/openloader/data/ascendant_realms_identity`.

It creates:

- `ar_skill_level` below player names.
- `ar_guild_rank` as the public rank order.
- rank teams from `ar_rank_unranked` through `ar_rank_s`.
- `/function ascendant_identity:rank_examiner/sync_nameplate` to repair the visible team from the rank score.

Rank colors follow `config/ascendant_guild/rank_nameplate_policy.json`.

Live rank effects are implemented in the `Ascendant Nametags` client renderer:

| Rank | Effect | Motion | Glow |
| --- | --- | --- | --- |
| Unranked | soft slate drift | slow left-to-right | minimal |
| E-Rank | low ember | slow upward sweep | subtle |
| D-Rank | emerald sweep | left-to-right | subtle |
| C-Rank | tidal shimmer | right-to-left wave | moderate |
| B-Rank | arc wave | diagonal wave | moderate |
| A-Rank | solar gleam | fast center sweep | strong |
| S-Rank | void prism | multi-color prism cycle | strongest |

The active `ascendant-nametags-0.1.0.jar` renderer should stop the raw vanilla player nameplate from showing only the username. Expected player format:

```text
[E Rank] zedyy | Lv.3
```

## NPC And Rival Nameplates

The active script is `customnpcs/scripts/ecmascript/ascendant_npc_identity.js`.

It renders important NPCs and rival hunters in this fallback format:

```text
[C-Rank] Mira Ash | Lv.34 Scout
```

The target polished version is still:

```text
[ C-Rank ] Mira Ash
Lv. 34 Scout
```

That final two-line animated presentation can still become a more advanced internal Forge overlay later, but the current v1 renderer is now live enough for rank/name readability.

## Rank Examiner

The player-facing flow is:

```text
Player talks to Rank Examiner -> NPC evaluates Guild proof -> public rank/nameplate updates
```

The NPC script runs the internal evaluation as the interacting player. The player should never need to type a command for normal gameplay.

Generated Rank Examiner spawn functions still embed and enable `customnpcs/scripts/ecmascript/ascendant_npc_identity.js`, but the helper also has a Forge-side right-click bridge for reliability. If a player right-clicks a spawned `customnpcs:customnpc` tagged `ar_profile_rank_examiner`, the helper runs `ascendant_identity:rank_examiner/evaluate` as that player even if CustomNPCs falls back to its default greeting behavior.

The evaluation:

- prints current Guild proof counters,
- checks the same rank thresholds used by Ascendant Core,
- promotes the player if the proof supports it,
- refreshes the visible rank team,
- tells the player what the next rank requires.

The hidden/admin test hook is:

```mcfunction
/function ascendant_identity:rank_examiner/evaluate
```

Use that only for validation when no Rank Examiner NPC is available.

## Self Preview Commands

These are client-side testing hooks, not gameplay:

```mcfunction
/ascnametag status
/ascnametag preview_self
/ascnametag hide_preview
```

`/ascnametags` is also available as an alias. The preview renders in world-space above Jayden's own third-person character model for 12 seconds, using the same styled content as the plate another player should see.

`/ascnametag status` also reports the active rank effect label, which is the quick check that the animated renderer is active.

Current rank thresholds are intentionally simple:

| Rank | Current proof |
| --- | --- |
| E-Rank | 10 Guild reputation |
| D-Rank | 35 Guild reputation, 10 hunt kills |
| C-Rank | 90 Guild reputation, 35 hunt kills |
| B-Rank | 210 Guild reputation, 1 boss proof |
| A-Rank | 500 Guild reputation, 4 boss proofs |
| S-Rank | 1200 Guild reputation, 8 boss proofs, 2 dragon proofs |

## Boundary

This is not the final Guild quest system. It is the live bridge so players can see rank identity and test rank improvement through an NPC now. FTB Quest trials, Bountiful contract completion, ranked dungeon clears, structure-clear proof, and rival hunter events should feed the same rank ladder later.
