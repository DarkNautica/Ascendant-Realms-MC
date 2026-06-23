# Spawn Ecology Plan

Status: Batch L installed and validated; high-density tuning active as of 2026-06-18.

Batch L added the first dedicated spawn ecology layer. The current direction is now much denser than the original conservative pass: ordinary exploration should feel populated, and Jayden should rarely be able to walk through the world without seeing multiple mobs nearby.

Installed tools:

- Spawn Balance Utility: `spawnbalanceutility-1.20-46.13.7.jar`
- In Control!: already installed from Batch E1
- Majrusz's Progressive Difficulty: `majruszs-difficulty-forge-1.20.1-1.9.10.jar`
- Improved Mobs: `improvedmobs-1.20.1-1.13.6-forge.jar`

Important distinction:

- Spawn Balance Utility changes spawn mixture, weights, and group sizes by biome/structure. It does not change the global spawn cap.
- In Control is still the safer place for hard caps, deny rules, and future biome/distance gates.
- Scaling Health, Majrusz's Progressive Difficulty, and Improved Mobs all increase danger. Tune them together, not separately.

## Current Direction

Batch L validation passed. The 2026-06-18 pass intentionally raises pressure through existing config levers before adding custom spawn injectors.

Current values:

- Spawn Balance Utility minimum spawn weight raised to `20`.
- Spawn Balance Utility maximum spawn weight raised to `180`.
- Majrusz spawn-rate multiplier is now default `1.75`, expert `2.05`, master `2.4`.
- Majrusz group pressure and scaling are tuned in `docs/PROGRESSIVE_DIFFICULTY_TUNING.md` and summarized in `docs/MOB_SPAWN_DENSITY_PASS.md`.
- In Control remains a hard-cap/deny-rule layer, not a broad spawn injector yet.

Use these pressure pools for the ongoing balance pass:

| Area | Common pressure | Rare pressure | Keep rare |
|---|---|---|---|
| Forests | vanilla undead, spiders, Alex's Mobs wildlife | Born in Chaos ambush mobs | Mowzie's Mobs encounters |
| Plains | vanilla patrol pressure, Alex's Mobs wildlife | raiders, Born in Chaos night threats | Bosses'Rise encounters |
| Mountains | skeletons, strays, goats/wildlife | IceAndFire CE foothill danger | dragons and roost pressure |
| Deserts | husks, spiders, Alex's Mobs desert wildlife | Aquamirae only near water/coasts | dragon-tier threats |
| Swamps | slimes, witches, swamp wildlife | Born in Chaos night pressure | boss-tier mobs |
| Oceans/coasts | drowned, Aquamirae | storm/night pressure | boss-tier aquatic threats |
| Frozen biomes | strays, Aquamirae/ice pressure where appropriate | IceAndFire CE cold-region pressure | dragon-tier threats |
| Caves | vanilla cave mobs, Born in Chaos | Cataclysm/Marium-adjacent danger only through structures | bosses |
| Villages | vanilla raids and patrols | limited night spillover | no common boss/dragon pressure |
| Far wilderness | denser hostile mix | elite/rare modded threats | dragon/boss escalation |

## Server Safety Rules

- The 2026-06-18 pass intentionally raised live pressure. If TPS suffers, lower Majrusz spawn-rate first before deleting mob content.
- Do not add new dragon or boss spawn rules until exact entity IDs are confirmed.
- Keep villages protected from constant rare mob spawns.
- Prefer biome-specific weights over everywhere-spawn rules.
- Prefer dense common wildlife/hostile presence over making boss-tier mobs common.

## Validation Focus

- Fresh creative test world loads.
- Normal night is more active without immediate unfair swarming.
- Villages remain usable.
- Boss/dragon-tier mobs are not common around spawn.
- Dedicated server stays stable for 10 minutes.
- Long open-land walks should no longer feel empty.

Sources checked during Batch L:

- Spawn Balance Utility CurseForge page: https://www.curseforge.com/minecraft/mc-mods/spawn-balance-utility
- Majrusz's Progressive Difficulty CurseForge page: https://www.curseforge.com/minecraft/mc-mods/majruszs-progressive-difficulty
- Improved Mobs CurseForge page: https://www.curseforge.com/minecraft/mc-mods/improved-mobs
