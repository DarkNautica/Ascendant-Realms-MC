# Version And Loader Decision

Status: approved for the initial proof target and initialized in Packwiz. Current Forge target is 47.4.20.

## Options Compared

### Minecraft 1.20.1 Forge

Strengths:

- Strong overlap with the candidate worldgen, structures, mobs, bosses, visuals, and shader stack.
- Oculus supports shaders on Forge 1.20.1.
- Embeddium, ModernFix, FerriteCore, Entity Culling, EMF, and ETF are available for strong client performance/visual support.
- Create, Iron's Spells, Better Combat, Combat Roll, Pufferfish's Skills/Attributes, Simply Swords, Artifacts, Theurgy, Alex's Mobs, Mowzie's Mobs, Ice and Fire, Aquamirae, Born in Chaos, Guard Villagers, Terralith, Tectonic, and YUNG's suite all have good 1.20.1 Forge signals.

Weaknesses:

- The newer RPG Series ecosystem is not fully available on 1.20.1 Forge. Many modules are Fabric-only on 1.20.1 or move to 1.21.1 NeoForge.
- Some visual candidates are resource packs or ambiguous CurseForge-only projects that still need manual verification.

### Minecraft 1.20.1 NeoForge

Strengths:

- Some mods support 1.20.1 NeoForge.
- Could bridge toward newer NeoForge ecosystem.

Weaknesses:

- 1.20.1 Forge is the stronger historical target for many classic Forge mods.
- Does not solve the RPG Series issue as cleanly as 1.21.1 NeoForge.

### Minecraft 1.21.1 NeoForge

Strengths:

- Stronger support for modern RPG Series modules: Skill Tree, Arsenal, Armory, Relics, Critical Strike, Village Taverns, and newer Spell Engine stack.
- Iris/NeoForge shader path exists for 1.21.1.
- Many visual/worldgen mods have 1.21.1 NeoForge support.

Weaknesses:

- Some key boss/mob candidates are weaker or missing on 1.21.1, including Alex's Mobs and Ice and Fire from current metadata.
- Create exists on 1.21.1 NeoForge, but many addon ecosystems may differ.
- More moving parts and potentially newer-mod instability.

### Minecraft 1.20.1 Fabric

Strengths:

- Good for Spell Engine/RPG Series legacy 1.20.1 modules.
- Iris/Sodium visual path is mature.

Weaknesses:

- Loses or complicates several Forge-centered boss, mob, and visual candidates.
- User explicitly warned not to use Fabric-only mods in a Forge/NeoForge pack without a deliberate strategy.

## Approved Initial Target

Choose Minecraft 1.20.1 Forge 47.4.20 for the first proof build.

Reason: it maximizes the broader candidate list for a beautiful vanilla+++ medieval fantasy exploration pack: terrain, structures, bosses, mobs, shader support, Better Combat, Iron's Spells, Pufferfish's Skills, Simply Swords, Create, and visual polish.

Patch note: the initial 47.4.10 target was raised to 47.4.20 because Subtle Effects 1.20.1-1.14.3 requires Forge 47.4.14 or newer.

## Explicit Tradeoff

This means the RPG Series ecosystem should be delayed or partly replaced:

- Use Pufferfish's Skills/Attributes for class-like progression.
- Use Better Combat + Combat Roll + Simply Swords for action combat.
- Use Iron's Spells for magic.
- Use Artifacts/Bountiful/loot tables for progression.

If Jayden later decides the RPG Series class ecosystem is more important than Alex's Mobs/Ice and Fire/Iron's Spells/Forge worldgen overlap, revisit 1.21.1 NeoForge in a separate direction change.

## Do Not Do

- Do not use Sinytra Connector.
- Do not mix Fabric-only RPG Series modules into the main Forge path.
- Do not add worldgen, combat/RPG systems, mobs, bosses, Ice and Fire, or RPG Series modules until their staged phases are approved.
