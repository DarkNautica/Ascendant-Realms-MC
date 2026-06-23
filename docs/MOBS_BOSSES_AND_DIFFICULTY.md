# Mobs, Bosses, And Difficulty

Goal: make the world dangerous but not stupid. Danger should create adventure, not random spawn grief.

## Batch E1 Installed Pressure Layer

Status: installed and validated.

Batch E1 responds to short survival feedback: the world is beautiful but too empty, not dangerous enough, and light on scary mobs and structures.

Installed:

- In Control!
- Mowzie's Mobs
- Alex's Mobs
- Guard Villagers
- Enhanced Boss Bars

Installed dependencies:

- GeckoLib
- Citadel

Enhanced Boss Bars is client-only. The gameplay-affecting mob and village-defense mods are both-side for multiplayer.

## Guardrail Rules

Batch E1 did not add:

- Magic
- Loot systems
- Ice and Fire
- Born in Chaos
- Bosses'Rise
- Aquamirae
- Enhanced Celestials
- Marium's Soulslike Weaponry
- Iron's Spells
- RPG Series modules

Batch E2 added and verified the approved loot/reward layer. Batch F is now installed and verified, adding magic, enemy escalation, dangerous events, ocean/ice danger, and expanded hostile variety.

Batch E2 validation passed:

- Client creative/system test passed.
- Dedicated server boot/join test passed.
- 10-minute stability check passed.
- No disposable survival test was required.
- Full difficulty, balance, and UI tuning happens later after the major stack is installed.

## In Control

`config/incontrol/spawn.json` now contains a high-density cap pass for Alex's Mobs, Mowzie's Mobs, Born in Chaos, Aquamirae, Bosses'Rise, IceAndFire CE, Cataclysm, Soulsweapons, Iron's Spells, and Majrusz Difficulty. The old conservative starter posture is superseded by `docs/MOB_SPAWN_DENSITY_PASS.md`.

The current config still does not add custom spawns, increase mob stats, change loot, or add distance scaling. It raises density through existing spawn weights, caps, and Majrusz spawn-rate/group pressure. See `docs/DANGER_SPAWN_TUNING.md` and `docs/MOB_SPAWN_DENSITY_PASS.md`.

`config/ascendant_core/mob_ecology.json` now owns the pack-level mob-role contract: passive wildlife, common hostile, village pressure, regional monsters, elite hunts, bosses, and dragon-tier threats. Use it to generate the next reviewed In Control draft instead of guessing from individual mod names.

## Difficulty Principles

- Spawn should be survivable near the starting area.
- First night should feel dangerous, not impossible.
- Caves, ruins, and wilderness should be threatening.
- Villages should survive better because Guard Villagers is installed.
- Bosses should feel discovered, not spammed.
- Difficulty should later rise by biome, distance, dimension, dungeon depth, and event type, but distance scaling remains deferred until the core feature stack is more complete.

## Batch F Installed Danger Layer

Status: installed and validated.

Batch F installed:

- Born in Chaos
- Aquamirae
- Enhanced Celestials
- Bosses'Rise

Supporting Batch F systems:

- Iron's Spells 'n Spellbooks
- Immersive Armors
- Spartan Shields
- Small Ships
- Snow! Real Magic

Danger tuning stance:

- Do not create reckless In Control spawn rules without a focused tuning pass.
- Do not nerf defaults blindly unless a specific catastrophic default is proven.
- If Born in Chaos or Aquamirae add too much pressure by default, document the first configs to tune during full balance review.
- Full balance tuning happens later after the major feature stack is installed.

Batch F validation passed:

- Client creative/system test passed.
- Dedicated server boot/join test passed.
- Iron's Spells, Born in Chaos, Aquamirae, Enhanced Celestials, Bosses'Rise, Immersive Armors, Spartan Shields, Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences/Walls are stable enough for the next batch.
- Variants & Ventures was removed after the Batch J startup crash because its 1.20.1 Forge file crashes with Entity Model Features during `variantsandventures:murk_skull` model registration.
- No disposable survival test is required for batch validation.

## Batch G Installed Dragon And Boss Layer

Status: installed and verified.

Installed Batch G danger systems:

- IceAndFire Community Edition
- L_Ender's Cataclysm
- Marium's Soulslike Weaponry

Supporting Batch G systems:

- Create
- Create Big Cannons
- Farmer's Delight
- Create: Structures Arise

Ice and Fire decision:

- Selected IceAndFire Community Edition.
- Original Ice and Fire is delayed because exactly one Ice and Fire variant may be active.
- IceAndFire Community Edition has a current Minecraft 1.20.1 Forge/NeoForge target and uses Jupiter and Uranus dependencies.
- It is a community fork and not a direct replacement path for existing original Ice and Fire saves. Ascendant Realms has no committed real survival world yet, so there is no active save-migration risk.

Danger tuning stance:

- Batch G client creative/system and dedicated server validation passed.
- Do not over-nerf before the later full balance pass.
- Full balance tuning happens later after the major feature stack is installed.
- See `docs/DRAGON_AND_BOSS_TUNING.md`.

Batch H is installed and verified but does not add new boss packs, dragon addons, mobs, combat systems, RPG Series modules, or extra Create addons.

## Batch J Add-On Risk

Status: installed and verified.

Batch J does not intentionally add a new danger batch. T.O Magic briefly pulled Alex's Caves and Apothic Attributes, but that chain is delayed after a Cataclysm `DungeonEyeItem` startup crash and should not be active in the current test set.

Validation focus:

- Confirm the delayed T.O Magic, Alex's Caves, Apothic Attributes, and Placebo jars are not still present in the active client or server.
- Confirm Iron's Spells still works after the `3.16.1` metadata update.
- Do not do full survival difficulty tuning during Batch J.

## Batch L Living World Pressure

Status: installed and validated; tuning active.

Batch L adds difficulty and spawn-ecology tools, not a new boss pack:

- Spawn Balance Utility
- Majrusz's Progressive Difficulty
- Improved Mobs

Dependencies:

- Majrusz Library
- TenshiLib

Tuning stance:

- Do not max out Majrusz, Improved Mobs, or Scaling Health at the same time.
- Do not make boss-tier mobs common.
- Do not add more dragon, boss, RPG Series, or horror systems in this batch.
- Validate boot, creative/system behavior, dedicated server join, and 10-minute stability first.
- Full survival pressure tuning happens later after the main feature stack is stable.

## Current Mob And Spawn Integration Pass

Status: staged and validated; tuning active.

The current integration pass copied generated config surfaces for the active mob/spawn stack into the pack source:

- `config/incontrol/spawn.json`
- `config/spawnbalanceutility-common.toml`
- `config/alexsmobs.toml`
- `config/alexsmobs/soul_vulture_spawns.json`
- `config/mowziesmobs-common.toml`
- `config/obscuria/aquamirae-common.toml`
- `config/cataclysm-common.toml`
- `config/soulsweapons/soulsweapons.json`
- `config/majruszsdifficulty.json`
- `config/guardvillagers-common.toml`
- `config/enhanced_boss_bars-common.toml`

Audit stance:

- No additional mob packs are needed for this pass.
- Confirm the installed mobs can appear through their own configs/tags before writing aggressive custom In Control spawn rules.
- If a mob family feels absent, tune its own config or biome tag first; only use In Control for cross-pack caps, spacing, and safety rules after the base behavior is understood.
- Full survival pressure tuning happens after the current client/server validation gates pass.

## Later Mob/Boss Candidates

Do not add until Jayden approves a later difficulty/boss batch:

- Cataclysm addons
- Ice and Fire addons
- Marium addons
