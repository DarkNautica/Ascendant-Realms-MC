# Skill Tree Testing

Status: unified Ascendant Web implemented and playtest passed; tuning active.

## Client Test

- Import the latest client ZIP.
- Launch client.
- Create or load a fresh creative test world.
- Open Pufferfish's Skills.
- Confirm one `Ascendant Web` category appears.
- Confirm the previous seven separate custom tabs do not appear.
- Confirm Default Skill Trees tabs do not appear.
- Confirm the web has branch clusters for Warrior, Rogue, Ranger, Arcanist, Engineer, Survivalist, and Dragonbound.
- Confirm tooltips show a flavor line plus exact `Effect:` line.
- Confirm Shift metadata shows cost, branch, requirements, loaded mods, and pack links.
- Confirm the cleaner web layout has readable branch lanes and no confusing cross-branch spaghetti.
- Unlock the central root node.
- Unlock several early and mid nodes from different branches.
- Confirm attributes apply where visible.
- Fight vanilla and modded mobs with Better Combat, Simply Swords, bows, and Iron's Spells.
- Confirm killing stronger/scaled mobs advances web XP without crash.
- Save/reload.
- Reopen the web and confirm unlocks persist.

## Dedicated Server Test

- Export server staging.
- Materialize server mods from the active CurseForge instance with `-Clean`.
- Copy server configs from staging so `config/puffish_skills/` is present.
- Boot Forge 1.20.1-47.4.20 server.
- Join localhost.
- Confirm no mod mismatch.
- Open the skill UI.
- Confirm `Ascendant Web` appears.
- Unlock root and a few branch nodes.
- Confirm attributes apply server-side.
- Fight vanilla and modded mobs.
- Disconnect/rejoin.
- Confirm unlocks and attributes persist.
- Confirm the visible below-name level fallback and level-up popup work after the identity datapack loads.
- Let server run 10 minutes.

## Failure Triage

- If no tree appears, confirm `config/puffish_skills/config.json` lists `ascendant`.
- If old tabs appear, confirm stale client/server config folders were cleaned before importing.
- If a tooltip load error mentions `extra_description`, confirm no node has `extra: []`.
- If an attribute ID fails, remove only the failing node/reward and rerun the generator.
