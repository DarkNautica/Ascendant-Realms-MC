# RPG Combat And Classes

Goal: class-like progression without forcing a single giant questline.

## Batch C Installed Combat Foundation

Status: installed and validated.

- Better Combat
- Combat Roll
- Simply Swords

Packwiz-resolved dependencies:

- playerAnimator
- Cloth Config API
- Architectury API

Batch C is combat foundation only. It does not include skills/classes, magic, mobs, bosses, Ice and Fire, RPG Series modules, Bountiful, or Artifacts.

Batch C validation passed for both client and dedicated server. Better Combat, Combat Roll, Simply Swords, playerAnimator, Cloth Config API, and Architectury API are stable enough for the next batch.

## Batch D Installed

Status: installed and validated.

Installed Batch D foundation:

- Pufferfish's Attributes
- Pufferfish's Skills

Packwiz-resolved dependencies:

- No additional dependency mods were added by Packwiz.

Default Skill Trees was originally used to validate the Pufferfish/Puffish framework, then removed from active Packwiz metadata once the custom Ascendant Realms tree was approved.

Batch D goal: first skills/classes/stat foundation. It does not add magic, mobs, bosses, loot systems, Ice and Fire, RPG Series modules, Alex's Mobs, Mowzie's Mobs, Guard Villagers, Create, ParCool, Bountiful, or Artifacts.

Real survival tuning is active now that the core feature stack has passed validation. Final balance is not complete.

## Batch E2 Installed Loot/Progression Hooks

Status: installed and validated.

Installed Batch E2 loot and contract foundation:

- Artifacts
- Bountiful
- Loot Beams: Relooted
- Villager Names
- Loot Journal: Pickup Notifier
- Loot Integrations

Packwiz-resolved dependencies:

- Kambrik
- Collective
- Fragmentum
- Curios API
- Cupboard

Batch E2 adds reward visibility and non-linear contracts only. It does not add magic, mobs, bosses, Ice and Fire, RPG Series modules, Create, Iron's Spells, or additional worldgen.

Batch E2 validation passed for client creative/system testing and dedicated server boot/join plus 10-minute stability. Artifacts, Bountiful, Villager Names, Loot Integrations, Kambrik, Collective, and Fragmentum are stable enough for the next batch. Loot Beams: Relooted and Loot Journal: Pickup Notifier remained client-only. No disposable survival test is required for batch validation, and full balance/UI tuning happens later after the major stack is installed.

## Next-Batch Recommendation Only

Superseded by approved and validated Batch F. Do not install any further RPG/combat batch until Jayden approves it.

## Batch F Installed Arcane / Gear Layer

Status: installed and validated.

Batch F adds the first major magic and gear escalation layer:

- Iron's Spells 'n Spellbooks
- Immersive Armors
- Spartan Shields
- Born in Chaos
- Aquamirae
- Enhanced Celestials
- Bosses'Rise
- Small Ships
- Snow! Real Magic
- Handcrafted
- Macaw's Bridges
- Macaw's Fences and Walls

Packwiz-resolved Batch F dependencies:

- CorgiLib
- Data Anchor
- Iron's Lib
- Obscure API
- Kiwi
- Resourceful Lib
- Curios API, GeckoLib, and Citadel were already present.

Batch F is intentionally larger than prior batches. It does not add Ice and Fire, Marium's Soulslike Weaponry, Cataclysm, RPG Series modules, Ars Nouveau, Theurgy, Create, or additional worldgen/village overhauls.

Batch F validation passed for client creative/system testing and dedicated server boot/join plus 10-minute stability. Iron's Spells, Born in Chaos, Aquamirae, Enhanced Celestials, Bosses'Rise, Immersive Armors, Spartan Shields, Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences/Walls are stable enough for the next batch. Variants & Ventures was later removed after the Batch J startup crash with Entity Model Features and `variantsandventures:murk_skull`.

Real survival tuning is active now that the core feature stack has passed validation. Final balance is not complete.

## Batch G Installed Dragonforge Cataclysm Layer

Status: installed and verified.

Batch G adds the large escalation layer:

- IceAndFire Community Edition for dragon-tier fantasy threats.
- L_Ender's Cataclysm for endgame boss pressure and boss structures.
- Marium's Soulslike Weaponry for legendary weapon progression and bosses.
- Create for engineering and contraptions.
- Create Big Cannons for siege/artillery options.
- Farmer's Delight for food/survival depth.
- Create: Structures Arise as the single approved Create structure addon.

Packwiz-resolved Batch G dependencies:

- Jupiter
- Uranus
- Lionfish API
- AttributeFix
- Projectile Damage Attribute
- Ritchie's Projectile Library
- Curios API and GeckoLib were already present.

Batch G client creative/system and dedicated server validation passed. Batch H, Batch J, Batch K, Batch L, Batch M, and Batch N have also passed validation. Real survival tuning is active.

Batch H is installed but does not add combat, skills/classes, magic, mobs, bosses, RPG Series modules, or extra weapon systems.

## Custom Ascendant Realms Skill Tree

Status: implemented through `config/puffish_skills/`, tooltip clarity and unique-identity passes implemented, playtest passed.

Active path:

- `config/puffish_skills/`

Fallback/source path:

- `datapacks/ascendant_realms_skills/`

Branches:

- Warrior: Better Combat timing, Simply Swords pressure, Spartan Shields defense, Immersive Armors durability, and Marium/Soulslike armor-shred identity.
- Rogue / Duelist: Combat Roll mobility, fast weapons, stealth, luck, Artifacts/Bountiful opportunism, and duelist tempo.
- Ranger / Hunter: Alex's Mobs and Mowzie hunting, projectile pressure, companion support, monster resistances, trophy luck, and dragon scouting.
- Arcanist: Iron's Spells max mana, mana regeneration, cooldown reduction, cast time reduction, spell resistance, school spell power, spellblade identity, and Aquamirae/Enhanced Celestials flavor.
- Engineer / Artificer: Create workshop utility, Create Big Cannons projectile scaling, Small Ships travel, Farmer's Delight provisioning, and structure/material payoff.
- Survivalist / Explorer: Serene Seasons sustain, Snow Real Magic travel pressure, structure delving, Bountiful/Loot Integrations reward sense, and expedition recovery.
- Dragonbound / Endgame: IceAndFire CE dragon bond, Cataclysm survival, Marium boss pressure, mounted/tamed scaling, and Iron's Spells endgame hybrid support.

Implemented now:

- 67 designed nodes across seven categories.
- Early/mid/late/capstone structure.
- Direct attribute rewards where attributes are documented or detected.
- Iron's Spells attributes are now live in the custom tree: max mana, mana regeneration, cooldown reduction, cast time reduction, spell resistance, and school spell power.
- More specialized Pufferfish attributes are now live: stealth, tamed damage/resistance, fortune, shred, damage reflection, fall reduction, projectile speed, mount speed, and sustain.
- Existing item icons only.
- Styled Puffish skill tooltips with a fantasy sentence, exact visible `Effect:` line, and Shift-only cost/branch metadata.

Still later:

- True boss/dragon unlock gates.
- Contract-based skill rewards.
- Combat Roll-specific cooldown/stamina integration if exposed and verified.
- KubeJS/advancement glue if datapack-only hooks are not enough.

## Batch L Body And Animation Layer

Status: installed and validated.

Batch L currently keeps:

- Not Enough Animations

First-person Model was removed because Jayden disliked seeing the player body in first person.

These are client-only presentation mods, but they must be tested against the combat stack:

- Better Combat
- Combat Roll
- Simply Swords
- Spartan Shields
- Iron's Spells casting
- Fresh Animations, EMF, ETF, and shaders

Better Animations Collection is delayed because it overlaps with the current Fresh Animations/EMF/ETF stack.

## Batch J Combat And Magic Add-On Notes

Status: installed and verified.

Batch J adds one active gameplay-adjacent piece to the combat stack:

- Malfu Combat Animation for Better Combat animation polish.

Dependency and risk notes:

- T.O Magic pulled Alex's Caves, Apothic Attributes, and Placebo, but all four are delayed after `traveloptics-6.3.0-1.20.1.jar` crashed against Cataclysm `3.30` with missing `DungeonEyeItem`.
- Iron's Spells remains updated to `3.16.1` plus Iron's Lib to `1.1.0`; validate those versions with existing spellbooks, mana/cooldown attributes, and the Arcanist skill branch.
- Malfu Combat Animation must be tested with Better Combat, Simply Swords, playerAnimator, Wavey Capes, and shaders.

Batch J does not validate a new class system or a new balance pass. If it boots cleanly, deeper spell/attribute tuning still belongs in the later integration pass.

## Later Class/RPG Candidates

Do not install until Jayden approves a later batch:

- ParCool
- Theurgy

## Delayed RPG Series Stack

Delay the RPG Series modules for the preliminary Forge path because many key modules are Fabric-only on 1.20.1 or move to 1.21.1 NeoForge:

- Skill Tree
- Arsenal
- Armory
- Relics
- Critical Strike
- Village Taverns
- Spell Engine class stack
- Archers/Wizards/Rogues/Paladins modules

Revisit if Jayden chooses a 1.21.1 NeoForge/Fabric direction.

## Possible Classes

- Warrior: shields, heavy weapons, armor, melee skills.
- Ranger: bows, mobility, exploration tools, lightweight armor.
- Rogue: daggers/fast weapons, combat roll, loot bonuses.
- Battlemage: Iron's Spells plus melee weapons.
- Priest/Paladin: defensive magic, shields, healing/support rules if available.
- Explorer: mobility, backpacks, artifacts, bounty progression.
- Engineer/Artificer: Create, utility gear, crafted progression.

## Skill System Choice

Preliminary Forge path:

- Pufferfish's Skills + Pufferfish's Attributes.
- Unified custom Ascendant Web loaded from `config/puffish_skills/`.
- 113 nodes in one shared web with Warrior, Rogue, Ranger, Arcanist, Engineer, Survivalist, and Dragonbound branch clusters.
- Shared XP source from killed mob dropped XP plus killed mob max health, naturally linking Scaling Health stronger enemies into skill progression.

Reason: available on 1.20.1 Forge and flexible enough for class-like progression.

## Weapon System Choice

Batch C:

- Better Combat
- Simply Swords

Batch F/G:

- Spartan Shields or Immersive Armors
- Marium's Soulslike Weaponry

## Magic System Choice

Batch F:

- Iron's Spells 'n Spellbooks.

Delay:

- Theurgy, unless the pack wants a deeper alchemy/magic progression layer.

## Loot Rarity Approach

Use:

- Simply Swords for weapon chase items.
- Artifacts for rare utility loot.
- Bountiful for non-linear objectives.
- Loot Beams/Legendary Tooltips for readability.
- Custom loot tables later through datapacks/KubeJS/Loot Integrations after E2 validation.

## Anti-Power-Creep Rules

- Do not put legendary weapons in early village/chest pools.
- Boss loot should unlock options, not trivialize all combat.
- Gate high-tier spellbooks and artifacts by dungeon tier, distance, dimension, or boss category.
- Keep repair/enchant access meaningful.
