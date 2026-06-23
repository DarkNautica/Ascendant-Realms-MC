# Danger Spawn Tuning

Batch E1 added world pressure without turning the first test world into uncontrolled chaos.

## Current Config Status

In Control is installed in Batch E1 and `config/incontrol/spawn.json` has conservative starter rules.

The starter config does not add new spawn entries. It only caps total loaded Alex's Mobs and Mowzie's Mobs spawns in the Overworld using the current In Control 1.20 `spawn.json` `mincount` syntax. This keeps the first pressure layer conservative before adding heavier custom spawn rules.

Batch F is installed and verified. It adds Born in Chaos, Aquamirae, Enhanced Celestials, and Bosses'Rise. Variants & Ventures was removed after a client startup crash with Entity Model Features and `variantsandventures:murk_skull`. Do not add new In Control rules for the active danger mods until a focused balance/config tuning pass identifies exact pressure problems.

Batch G is installed and verified. It adds IceAndFire Community Edition, L_Ender's Cataclysm, and Marium's Soulslike Weaponry. Do not add custom dragon or boss spawn rules until a focused balance/config tuning pass identifies exact pressure problems.

Batch H is installed and verified. It adds civilization, atmosphere, and structure density, not new danger-spawn systems.

Batch L is installed and validated. It adds Spawn Balance Utility, Majrusz's Progressive Difficulty, and Improved Mobs as the first dedicated spawn ecology and long-term enemy pressure layer. The 2026-06-18 density pass now uses those existing configs aggressively enough that ordinary travel should show multiple mobs nearby. The follow-up hostile pass also enables `config/incontrol/spawner.json` so daytime wilderness can spawn enemies instead of relying only on night/cave rules.

## Current Rules

- Cap Alex's Mobs entities at 120.
- Cap Mowzie's Mobs entities at 18.
- Cap Born in Chaos entities at 36.
- Cap Aquamirae entities at 24.
- Cap Bosses'Rise entities at 8.
- Cap IceAndFire CE entities at 10.
- Cap Cataclysm entities at 8.
- Cap Block Factory boss entities at 8.
- Cap Soulsweapons entities at 10.
- Cap Iron's Spells entities at 24.
- Cap Majrusz Difficulty entities at 24.
- Apply caps only in `minecraft:overworld`.
- Do not alter health, damage, AI, XP, loot, or biome rules yet.
- Do not add distance scaling yet.
- Spawn Balance Utility and Majrusz spawn pressure are now deliberately raised; see `docs/MOB_SPAWN_DENSITY_PASS.md`.
- `config/incontrol/spawner.json` is active for common hostile daytime/cave pressure; see `docs/HOSTILE_DAY_SPAWN_PASS.md`.
- Do not stack high Scaling Health, Majrusz, and Improved Mobs values before a creative/system pass proves the overlap is stable.
- Do not pre-nerf Born in Chaos, Aquamirae, Enhanced Celestials, or Bosses'Rise without evidence from focused tuning.
- Do not pre-nerf IceAndFire Community Edition, Cataclysm, or Marium's Soulslike Weaponry without evidence from focused tuning.
- If any cap uses a wrong mod ID, fix the ID after checking the latest client log or jar `mods.toml`; do not replace these caps with broad entity-specific deny rules until entity IDs are confirmed.

## Design Intent

- Spawn area and early world should be busy, but boss/dragon-tier mobs should still not become routine.
- Day and night should both have visible hostile pressure in wilderness.
- Night should still feel substantially more dangerous than the earlier conservative pass.
- Caves, ruins, and wilderness should become more threatening through the installed mob mods.
- Villages should survive better because Guard Villagers is installed.
- Farther travel can become more dangerous later, but distance scaling is intentionally deferred until the core feature stack is more complete.

## Later Survival Tuning Notes

Disposable survival throwaway tests are no longer required after every batch. During later full survival tuning, record whether the world feels:

- Too safe, dangerous, or unfair.
- Too empty, balanced, or too crowded.
- Too few structures, good density, or spammed.

If the world is still too sparse, raise the reviewed In Control `spawner.json` rates first after checking in-game behavior. If it is too chaotic or TPS-heavy, lower `spawner.json` `persecond` first, then Majrusz spawn-rate, then Spawn Balance Utility weights, then caps.

Batch L first configs to review during full balance tuning:

- Spawn Balance Utility biome/structure weighting and group size configs.
- Majrusz's Progressive Difficulty scaling and modded-mob handling.
- Improved Mobs gear, AI, stat, and special ability chances.
- Scaling Health early-game scaling and blight rarity.

Batch F first configs to review during full balance tuning, if pressure is too high:

- Born in Chaos spawn/common config.
- Aquamirae spawn/biome config.
- Enhanced Celestials lunar event frequency/config.
- Bosses'Rise spawn/boss configuration.

Batch G first configs to review during full balance tuning, if pressure is too high:

- IceAndFire Community Edition dragon spawn frequency.
- Dragon griefing or block damage, if configurable.
- Dragon roost and cave spacing.
- Dragon taming and riding access.
- Cataclysm boss structure spacing.
- Marium boss health/damage.
- Legendary weapon damage and ability cooldowns.
- Create Big Cannons griefing/server rules.

Do not invent commands or rules for progression, skill points, loot, bosses, or magic.
