# Progressive Difficulty Tuning

Status: Batch L installed and validated; high-density tuning active as of 2026-06-18.

Majrusz's Progressive Difficulty is installed as the long-term enemy pressure layer:

- Majrusz's Progressive Difficulty: `majruszs-difficulty-forge-1.20.1-1.9.10.jar`
- Majrusz Library: `majrusz-library-forge-1.20.1-7.0.8.jar`

Purpose:

- Make the world become more threatening over time.
- Support the "RLCraft-like pressure, but controlled" direction.
- Avoid front-loading the early game so hard that the first base is miserable.

## Tuning Direction

The original Batch L pass started conservative. The current direction is denser:

- Early-game spawn pressure has now been raised substantially after Jayden reported the world still felt too empty.
- Watch overlap with Scaling Health and Improved Mobs.
- Keep special/elite threats rare.
- Do not assume modded mobs are fully balanced until the long-form tuning world has more hours on it.
- Do not use disposable survival tests as the main balance signal; tune from the current long-form world.

Current values:

- CRD penalty: expert `0.20`, master `0.42`.
- Mob group chances: skeletons `0.35`, undead `0.32`, zombie miners `0.40`, piglins `0.35`.
- Spawn rate multiplier: default `1.75`, expert `2.05`, master `2.4`.
- Stronger mob health bonus: default `0.08`, expert `0.22`, master `0.45`.
- Stronger mob damage bonus: default `0.04`, expert `0.14`, master `0.28`.

Intent:

- The start should feel populated and dangerous.
- Progression should make the player noticeably stronger.
- Late-game/master-stage enemies should still be able to kill careless geared players.

## Systems It Overlaps

| System | Overlap risk | Direction |
|---|---|---|
| Scaling Health | Extra mob health/damage can stack with progressive difficulty | Keep both conservative |
| Improved Mobs | AI/stat/ability upgrades can stack sharply | Watch early nights and caves |
| Born in Chaos | More dangerous base mob pool | Avoid over-spawning |
| IceAndFire CE | Dragon-tier threat should stay rare | Do not make dragons common |
| Cataclysm/Marium | Boss-tier pressure | Keep structure/boss encounters deliberate |

## Validation Notes

Client:

- Confirm the client reaches the main menu and a creative test world.
- Fight a few vanilla and modded mobs.
- Watch for UI overlap with mob health bars or titles.

Server:

- Confirm Majrusz's Progressive Difficulty and Majrusz Library are copied server-side.
- Join localhost with no mismatch.
- Fight mobs and disconnect/rejoin.
- Run 10 minutes and inspect logs for difficulty/progression errors.
