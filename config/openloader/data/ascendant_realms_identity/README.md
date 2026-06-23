# Ascendant Realms Identity

This OpenLoader datapack adds the multiplayer identity scoreboard and fallback team layer used by the custom progression HUD bridge.

It creates `ar_skill_level` for the player-facing Ascendant Web level below names, adds a static `[Ascendant]` team prefix for unnamed/unassigned players, defines Guild rank teams, and provides manual rank functions under `ascendant_identity:rank/*` for testing.

The live Rank Examiner bridge is NPC-facing: interact with a Rank Examiner profile NPC and the NPC runs the internal evaluation for the player. `/function ascendant_identity:rank_examiner/evaluate` is only the admin/test hook. It prints current proof counters, applies any earned public Guild rank, and syncs the visible player rank team.

`kubejs/server_scripts/ascendant_progression.js` reads Puffish Skills data, mirrors the current Ascendant Web level into `ar_skill_level`, and renders the custom skill-XP HUD bar.
