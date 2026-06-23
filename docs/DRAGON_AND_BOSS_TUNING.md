# Dragon And Boss Tuning

Batch G is installed and verified. Do not over-nerf before the later full balance pass.

This page records likely later tuning targets only. Do not invent config keys; inspect generated configs after a test client/server has created them.

## Installed Batch G Escalation

- IceAndFire Community Edition
- L_Ender's Cataclysm
- Marium's Soulslike Weaponry
- Create
- Create Big Cannons
- Farmer's Delight
- Create: Structures Arise

## Ice And Fire Decision

Selected: IceAndFire Community Edition.

Reason: provider metadata shows a current Minecraft 1.20.1 Forge/NeoForge file for IceAndFire Community Edition, while the original Ice and Fire path is an older 1.20.1 beta line. The community edition has clear both-side multiplayer metadata and explicit dependency metadata through Jupiter and Uranus.

Warning: IceAndFire Community Edition is a community fork, not a direct save-replacement path for existing Ice and Fire worlds. The project warns that directly replacing the original mod in existing saves can corrupt those saves. Ascendant Realms has no committed real survival world yet, so this is not an active migration risk, but do not swap variants after a real world starts without a separate migration plan.

## Later Tuning Targets

- Dragon spawn frequency.
- Dragon griefing or block damage, if configurable.
- Dragon roost and cave spacing.
- Dragon taming and riding access.
- Cataclysm boss structure spacing.
- Cataclysm boss loot and access pacing.
- Marium boss health and damage.
- Legendary weapon damage and ability cooldowns.
- Create Big Cannons block damage, griefing, and server rules.
- Farmer's Delight food saturation and hunger balance.
- In Control compatibility options for dragon, boss, and dangerous mob gating.

## Validation Safety

- Batch G client creative/system test passed.
- Batch G dedicated server boot/join and 10-minute stability check passed.
- Spawn one controlled dragon or Ice and Fire creature in an isolated area.
- Spawn one controlled Cataclysm enemy, not a full boss rush.
- Test one Marium weapon.
- Do not spawn multiple dragons, multiple Cataclysm bosses, or multiple Marium bosses at once during validation.
- The first goal is stability, not balance.
