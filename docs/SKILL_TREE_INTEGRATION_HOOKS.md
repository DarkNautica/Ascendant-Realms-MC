# Skill Tree Integration Hooks

Status: design hooks documented; active implementation includes direct attribute rewards plus the Puffish/KubeJS progression HUD and managed bonus-point bridge.

## Active Hooks

- Puffish skill XP comes from killed mob dropped XP plus killed mob max health.
- Scaling Health and other stronger-enemy systems therefore feed progression indirectly through higher max health.
- KubeJS reads Ascendant Web level/XP/points, renders the custom HUD bar, mirrors `ar_skill_level`, and grants managed milestone bonus points.
- Ascendant Core defines shared rank, bounty, structure, boss, dragon, region, and threat scoreboards in `config/ascendant_core/progression_hooks.json`. `config/ascendant_core/runtime_rules.json` now provides the first live bridge for region tier, kill reputation, boss/dragon proofs, and automatic Guild rank promotion.
- Arcanist uses Iron's Spells attributes.
- Engineer uses Create, Farmer's Delight, Slice & Dice, Small Ships, and Create Big Cannons themed attributes.
- Dragonbound uses IceAndFire CE, Cataclysm, Marium, and Iron's Spells themed attributes.
- Ranger uses tamed, projectile, luck, resistance, and trophy-hunter attributes.
- Rogue uses stealth, luck, movement, fall-reduction, and fast melee attributes.
- Survivalist uses travel, sustain, weather, season, loot, and expedition attributes.

## Future Hooks

- Boss kill milestones can unlock Dragonbound and Mythbreaker-style paths.
- Dragon kill/tame milestones can unlock Dragonlord and Dragon Rider paths.
- Bountiful contracts can feed Survivalist/Rogue/Ranger XP or titles.
- Create milestones can feed Engineer unlocks.
- Iron's Spells milestones can feed Arcanist unlocks.
- Titles can mirror major branch commitments and boss kills.
- KubeJS can later bridge recipes, loot, titles, and milestone advancement checks if datapack/config hooks are not enough.
- `config/ascendant_core/progression_hooks.json` is the current source for deciding which branch owns each cross-mod milestone.

## Current Guardrails

- Keep live KubeJS progression edits limited to the documented bridge until client and dedicated server retesting passes.
- Do not invent skill-point commands; adjust `config/ascendant_progression/progression.json` or Puffish config instead.
- Do not assume boss, contract, dragon, or Create events are available until exact schema/API support is verified.
