# Ascendant Nameplates

Status: live modular Forge renderer implemented. The current layer uses the client-side `Ascendant Nametags` helper for players and AI hunters, scripted CustomNPCs display names for authored NPCs, and a Rank Examiner function bridge for public rank evaluation.

The target presentation is a clean two-line identity plate:

```text
[ C-Rank ] Mira Ash
Lv. 34 Scout
```

## Important Compatibility Note

The linked/attached CustomNameTags-style approach is not the right direct install path for this Forge client/server modpack. The visible CustomNameTags jar is Fabric/server-side, so Ascendant Realms treats that look as visual reference only. For Forge, the active path is:

1. `Ascendant Nametags` client renderer for player rank/name/level plates.
2. `Ascendant Nametags` client renderer for AI hunter rank/profile plates.
3. `Ascendant Nametags` world-space animated text effects for rank gradients, glow, and self-preview.
4. Vanilla teams plus `ar_skill_level` below-name as backup/context.
5. CustomNPCs scripted display names for important authored NPCs.
6. Rank Examiner NPC interaction for live rank evaluation.

## Config

The source contracts live at:

- `config/ascendant_guild/nameplates.json`
- `config/ascendant_guild/rank_nameplate_policy.json`
- `config/ascendant_guild/rank_examiner_policy.json`

The nameplate renderer lives in `ascendant-nametags-0.1.0.jar` and rewrites rendered player and AI hunter name tags at client render time. It now draws the visible plate itself instead of only changing the text content, which allows animated per-character gradients, rank-colored glow passes, bold high-rank plates, and a true third-person self-preview. AI hunters use a level-stage world overlay fallback because CustomNPCs can bypass Forge's normal name-tag event; the renderer resolves hunters from synced tags when available and from the CustomNPC display/custom name when tags are not visible client-side. Its source lives under `local-mods/ascendant-nametags/`. The starter CustomNPC script lives at `customnpcs/scripts/ecmascript/ascendant_npc_identity.js`. It reads a temporary profile key such as `ar:mira_ash`, then rewrites authored NPC display names into one visible rank/name/level/role line.

The Rank Examiner function lives at `config/openloader/data/ascendant_realms_identity/data/ascendant_identity/functions/rank_examiner/evaluate.mcfunction`. It is hidden plumbing for the NPC interaction. The manual command is for admin/testing only:

```mcfunction
/function ascendant_identity:rank_examiner/evaluate
```

The Rank Examiner NPC runs that internal function as the interacting player. It prints the player's current proof counters, attempts any earned Guild rank promotion, syncs the visible rank team, and reports the next public rank requirement.

Root-cause note: CustomNPCs-Unofficial renders the separate `title` slot only within close range and wraps it in angle brackets. The script keeps level and role in the always-visible name line and clears the title slot. The current Ascendant Nametags renderer fixes player and AI hunter labels first; a later more polished two-line animated overlay can still replace this v1 presentation.

MobHealthBar note: `config/mobhealthbar-client.toml` keeps health bars enabled but disables the plain mob name line. That prevents a white duplicate rank/name label from appearing above AI hunters while the Ascendant Nametags renderer draws the styled plate.

Existing NPC repair note: early Rank Examiner prototypes stored `ar_rank = guild_staff`, then `Unranked`, instead of the public `B-Rank` value. CustomNPCs also embeds a copy of the script inside each saved NPC. The script now sanitizes stale style ids and stale placeholder ranks, and `scripts/customnpcs-identity-audit.py` scans/repairs saved NPC names, stored profile data, and embedded script copies. `/function ascendant_identity:npc_test/fix_rank_examiner` is only a quick in-game profile reset; the offline audit/repair tool is the authoritative fix for already placed NPCs.

It defines:

- rank palette
- player fallback
- Guild staff styles
- rival hunter styles
- important NPC profiles
- intended visibility behavior

## Rules

- Every NPC loadout profile needs a matching nameplate profile.
- Rival hunters need rank, level, profession, and style.
- Nameplate rank must match the NPC equipment rank.
- Rank colors must stay inside the shared palette so tooltips, item borders, titles, and NPC plates feel like one system.
- Animated effects must remain rank-readable first: S/A can be flashy, but lower ranks should stay clean and legible.

## Next Steps

Use Ascendant Nametags for players and AI hunters, scripted CustomNPCs identity for authored NPCs, and the Rank Examiner NPC bridge for public rank evaluation. Do not force a Fabric/Bukkit/Paper nameplate system into the Forge pack.
