# Ascendant AI Hunter Director

Status: live helper v1.

The Ascendant helper now includes an AI Hunter Director for ranked rival-style hunter encounters. This is not a village, road, Guild Hall, Hunter Board, or settlement system. It only creates ranked hunter NPC encounters and test hooks.

## Live Commands

- `/aschunter status`
- `/aschunter spawn_near <d_rank|c_rank|b_rank|a_rank|s_rank>`
- `/aschunter spawn_random_now`
- `/aschunter grow_near`
- `/aschunter cleanup_near`

## Current Behavior

- Low-frequency overworld hunter spawn attempts begin after a short delay.
- The director skips automatic spawns when another AI hunter is already close to the player.
- Hunters spawn on nearby solid surfaces, not water/lava/ice.
- Test spawns now use existing CustomNPC spawn functions first, then apply Ascendant hunter rank/profile tags, name data, and stats. This avoids the fragile direct summon NBT path that caused the in-game hunter command error.
- Hunters receive `ar_ai_hunter`, profile, rank, and AI-rank tags.
- Loaded hunters near players receive periodic growth/stat pressure.
- Loaded hunters near players now receive a helper-side combat pulse. Nearby hostile mobs and `ar_ai_hunter` NPCs are assigned to target each other, hunters path toward the target, and hunters melee when close enough. This is the current reliability bridge until final authored CustomNPC faction/behavior tuning exists.
- Spawn reports write to `config/ascendant_guild/reports/ai_hunter_latest.json`.

## Known Limits

- A-rank and S-rank use available rival texture assets until dedicated skins are created.
- A-rank and S-rank should still spawn with A/S identity, tags, and stats even while their visual skin is temporary.
- Combat behavior is helper-assisted v1. It should make field tests visibly work, but rivalry memory, threat selection, party rules, and reward outcomes still need later design.
- Rival memory, rank challenge rules, bounty linkage, defeat outcomes, and reward contracts are not implemented yet.
- This pass is meant to make hunters exist in-world and be testable; balance tuning comes after visual and combat testing.

## Nameplate Test

Player self-preview now lives in the modular Ascendant Nametags client helper:

- `/ascnametag status`
- `/ascnametag preview_self`
- `/ascnametag hide_preview`

The Atlas helper still owns AI hunter spawning/combat. The `ascendant-nametags-0.1.0.jar` client helper owns real player and AI hunter rank nameplates, including the animated rank gradients and glow effects used by player plates. The preview command renders Jayden's own player plate above the third-person model; the broader test is still looking at another player or an AI hunter in-world.
