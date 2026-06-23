# Spawn Tuning Worklist

Generated: 2026-06-14T15:41:03.2735019-04:00

This worklist turns the generated mob registry into reviewable spawn-tuning groups. The first live unification pass now changes active In Control rules only through the already proven cap pattern in `config/incontrol/spawn.json`.

| Namespace | Entities Requiring Review | Suggested Policy |
| --- | ---: | --- |
| `alexsmobs` | 73 | Separate passive wildlife from predators; avoid blanket danger treatment. |
| `aquamirae` | 10 | Keep cold/ocean danger thematic; connect coastal contracts. |
| `artifacts` | 1 | Review biome/config spawn behavior and connect to threat tier. |
| `block_factorys_bosses` | 13 | Review biome/config spawn behavior and connect to threat tier. |
| `born_in_chaos_v1` | 77 | Use night, ruin, graveyard, and event pressure; avoid overwhelming settlements. |
| `cataclysm` | 74 | Keep boss and elite content structure/milestone driven. |
| `create` | 7 | Review biome/config spawn behavior and connect to threat tier. |
| `customnpcs` | 1 | Review biome/config spawn behavior and connect to threat tier. |
| `easy_npc` | 2 | Review biome/config spawn behavior and connect to threat tier. |
| `enhancedcelestials` | 2 | Review biome/config spawn behavior and connect to threat tier. |
| `farmersdelight` | 1 | Review biome/config spawn behavior and connect to threat tier. |
| `geckolib` | 8 | Review biome/config spawn behavior and connect to threat tier. |
| `handcrafted` | 1 | Review biome/config spawn behavior and connect to threat tier. |
| `humancompanions` | 1 | Review biome/config spawn behavior and connect to threat tier. |
| `iceandfire` | 39 | Distance-gate dragon-tier spawns and keep dragon contracts late-game. |
| `irons_spellbooks` | 72 | Review biome/config spawn behavior and connect to threat tier. |
| `majruszsdifficulty` | 6 | Review biome/config spawn behavior and connect to threat tier. |
| `mca` | 1 | Review biome/config spawn behavior and connect to threat tier. |
| `mowziesmobs` | 18 | Review biome/config spawn behavior and connect to threat tier. |
| `quark` | 14 | Review biome/config spawn behavior and connect to threat tier. |
| `smallships` | 7 | Review biome/config spawn behavior and connect to threat tier. |
| `soulsweapons` | 46 | Review biome/config spawn behavior and connect to threat tier. |
| `supplementaries` | 2 | Review biome/config spawn behavior and connect to threat tier. |

## Active Config Note

The current active `config/incontrol/spawn.json` still uses broad per-mod caps, but the caps are now tuned around the latest village-survival log:

| Namespace | Active Cap |
| --- | ---: |
| `alexsmobs` | 64 |
| `mowziesmobs` | 8 |
| `born_in_chaos_v1` | 14 |
| `aquamirae` | 10 |
| `bossesrise` | 4 |
| `iceandfire` | 5 |
| `cataclysm` | 4 |
| `block_factorys_bosses` | 4 |
| `soulsweapons` | 5 |
| `irons_spellbooks` | 12 |
| `majruszsdifficulty` | 8 |

This is intentionally a preservation fix: it keeps all mobs installed, lowers burst pressure near loaded chunks, and adds cap coverage for boss/elite namespaces that previously had none. The second cap pass was made after the latest live log still showed MCA villagers and guards dying quickly in villages to Born in Chaos pressure mobs. `spawner.json` custom additions, structure-tag deny rules, and rank-aware dynamic spawns remain deferred until copied-world tests prove them stable.
