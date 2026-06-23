# Skill Tree Design

Status: unified Ascendant Web implemented, playtest passed, tuning active.

The active Ascendant Realms skill system is now one large Puffish Skills category instead of seven separate tabs. The category is `Ascendant Web`, loaded from `config/puffish_skills/`, mirrored into `datapacks/ascendant_realms_skills/`, and mirrored into Open Loader under `openloader/data/ascendant_realms_skills/`.

## Current Shape

- One category: `Ascendant Web`.
- 113 nodes.
- 196 bidirectional connections after the readability pass.
- Two starting points.
- Seven cleaner branch lanes inside one web: Warrior, Rogue / Duelist, Ranger / Hunter, Arcanist, Engineer / Artificer, Survivalist / Explorer, Dragonbound / Endgame.
- Default Puffish pacing: 1 skill point per web level.
- Managed milestone bonus points from `config/ascendant_progression/progression.json` at levels 10, 20, 35, 50, 70, 90, and 110.
- Higher-tier nodes cost 2-3 points, so players can mix branches but cannot instantly max everything.
- The old dense diagonal and cross-branch link web was removed because it made progression lines hard to read. Each branch now uses horizontal tier choices plus direct outward tier bridges.

## Tooltip Convention

Every node must stay readable without guessing:

- Name: clear fantasy skill name.
- First line: short flavor sentence.
- Visible `Effect:` line: exact stat gain from the real reward data.
- Shift metadata: cost, branch, requirement, loaded-mod requirement, and pack-system link.

Example:

```text
Luckbearer
Who says there is no luck?
Effect: Increases Luck by +1 and Stealth by +3%.
```

## Progression Link

The web uses killed mob dropped XP plus killed mob max health for skill XP. That means Scaling Health, Improved Mobs, Majrusz's Progressive Difficulty, boss mobs, and other stronger enemy systems should naturally feed more skill XP without inventing commands or unsupported hooks.

## Branch Identity

| Branch | Identity focus |
|---|---|
| Warrior | Better Combat melee tempo, shields, armor, shred, and boss-frontline survival. |
| Rogue / Duelist | Combat Roll mobility, light weapon speed, stealth, luck, artifacts, and dungeon loot payoff. |
| Ranger / Hunter | Bows, projectile damage, tamed companion scaling, monster knowledge, and trophy/relic hunting. |
| Arcanist | Iron's Spells mana, regen, cooldowns, spell resistance, school power, spellblade play, and portal utility. |
| Engineer / Artificer | Create, Create Big Cannons, Farmer's Delight, Slice & Dice, Small Ships, workshop utility, and siege tools. |
| Survivalist / Explorer | Serene Seasons, Snow Real Magic, weather, travel, Bountiful contracts, recovery, and long expedition sustain. |
| Dragonbound / Endgame | IceAndFire CE, Cataclysm, Marium, dragon/tamed scaling, elemental resistances, mount speed, and endgame boss pressure. |

## Guardrails

- Do not re-add Default Skill Trees unless the custom web is explicitly rolled back.
- Do not add unsupported commands for skill points; use Puffish Skills data or the managed milestone bonus-point bridge.
- Boss-kill gates, Bountiful contract rewards, Create milestones, and title unlocks are later integration hooks, not active behavior yet.
- Existing worlds may carry old skill data from the previous seven-tab tree; validate with a fresh world when possible.
- The live HUD bridge reads Puffish Skills through KubeJS and renders the Ascendant level bar with KubeJS Painter. Keep `config/ascendant_progression/progression.json` and `kubejs/server_scripts/ascendant_progression.js` synced with any future skill-tree pacing changes.
