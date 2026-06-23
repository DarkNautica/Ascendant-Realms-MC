# Skill Tree Balance Notes

Status: first unified-web balance pass implemented and playtest passed; long-form tuning active.

## Pacing

- The web starts with 2 points.
- Puffish Skills is expected to award 1 skill point per Ascendant Web level.
- `config/ascendant_progression/progression.json` adds conservative milestone bonus points at levels 10, 20, 35, 50, 70, 90, and 110.
- The nameplate/popup/HUD bridge now uses Puffish Skills Ascendant Web data, not vanilla XP.
- Early nodes cost 1 point.
- Mid nodes cost 1-2 points.
- Late nodes and capstones cost 3 points.
- The web has more total node cost than the level cap can reasonably cover, so players must choose identity instead of maxing everything quickly.

## XP Curve

The current curve is:

```text
min(55 + level ^ 1.82 * 11, 2400)
```

XP source:

```text
dropped_xp * 0.75 + max_health / 24
```

Anti-farming:

```text
12 kills per chunk, reset after 420 seconds
```

Reason: Scaling Health and other difficulty systems raise enemy health and threat, so harder enemies still feed more skill XP naturally, but the slower curve gives the survival world room for long-term growth.

## Balance Risks To Watch

- Iron's Spells cooldown reduction and mana regeneration can snowball.
- Shred, toughness shred, and resistance shred can overperform against bosses.
- Tamed damage/resistance and mount speed may become too strong after dragons are practical.
- Luck/Fortune nodes can distort loot progression if stacked with Artifacts, Bountiful, Loot Integrations, and rare structures.
- Damage resistance and reflection can stack with armor, shields, Artifacts, and boss gear.

## Tuning Direction

- If progression feels too slow, lower the XP curve slightly before increasing points per level or adding more bonus milestones.
- If progression feels too fast, raise late-node costs first, then remove bonus milestones if needed.
- If combat gets too easy, reduce resistance/shred values before touching enemy mods.
- Disposable survival runs are no longer required after each batch. Use the current long-form tuning world to judge whether growth feels slow, meaningful, and still dangerous.
- Keep future growth slow enough that the player feels stronger over time without erasing lethal elite mobs, bosses, dragons, and bad-weather encounters.
