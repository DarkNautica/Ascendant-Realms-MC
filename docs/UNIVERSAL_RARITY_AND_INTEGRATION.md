# Universal Rarity And Integration

## Purpose

Ascendant Realms needs one shared rarity language across loot, mobs, structures, skills, bounties, boss drops, and tooltips. This file is the design contract for that language.

## Current Coverage

- Required rarity/integration entries: 55
- Conditional rarity/integration entries: 20

## Rarity Tiers

| Tier | Use | Color Direction |
|---|---|---|
| Common | Vanilla baseline, simple materials, routine village supplies | Soft gray/white |
| Uncommon | Early modded gear, helpful food, minor structure loot | Green |
| Rare | Dangerous structure rewards, strong mob drops, branch-defining skill rewards | Blue |
| Epic | Boss-adjacent gear, rare artifacts, major spells, elite bounties | Purple |
| Legendary | Boss drops, dragon materials, late-game weapons, signature artifacts | Gold |
| Mythic | Cataclysm/dragon-tier chase rewards and major pack milestones | Red/orange |
| Ascendant | Pack-defining capstones, final skill-web rewards, named relics | Cyan/white |

Visual rule: Common through Epic should stay readable and unbolded. Legendary, Mythic, and Ascendant are the only bold rarity labels. Mythic and Ascendant should use clean tier text only: `MYTHIC` and `ASCENDANT`, with no side symbols, no `Flame`/`Pulse` wording, and no obfuscated side characters.

## What Gets A Rarity

- Items with gameplay power: weapons, armor, artifacts, spell books, scrolls, food buffs, trophies, dragon materials, boss drops.
- Mobs and bosses: passive/ambient, common hostile, dangerous hostile, elite, boss, dragon-tier.
- Structures: common villages, minor ruins, dangerous dungeons, rare landmarks, boss arenas, dragon-tier zones.
- Skills: early utility, branch identity, tier-three specialization, capstone, cross-system milestone.
- Bounties and contracts: normal tasks, dangerous contracts, elite hunts, boss contracts, dragon contracts.

## HUD And Tooltip Contract

Every custom skill, relic, bounty reward, or tuned item should have both flavor and exact math:

- Example name: `Luckbearer`
- Example flavor: `Who says there is no luck?`
- Example exact effect: `Increases Luck by +1 and Stealth by +3%.`

The exact effect line matters more than the flavor line. If the player cannot tell what they gain, the integration is not finished.

Generated gear item tooltips should show the rarity tier as its own label without the old `Rarity:` prefix. The label belongs directly under native damage/speed/stat lines and before green attack range, combat behavior, chance, cooldown, or spell-behavior text. Player-facing item tooltips should not expose generated backend `Effect:`, `Index:`, or `Why:` lines because the native mod tooltip already carries combat stats and item behavior.

## Enemy Threat Contract

Scaling Health is allowed to make mobs stronger, but the pack still needs a separate visual threat layer if we want numeric enemy levels above mobs. Current configs support health bars and difficulty scaling; they do not expose a clean enemy-level nameplate by themselves.

## Skill Tree Contract

The Ascendant Web should feel flexible, not like a forced straight build. The current generator keeps one unified tree, broad horizontal choices inside each tier, and cleaner branch lanes to reduce confusing line crossings.

## Generated Schema

The matching machine-readable schema lives at `config/ascendant_index/rarity_schema.json`.
