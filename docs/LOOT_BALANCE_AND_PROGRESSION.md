# Loot Balance And Progression

## Batch N Cohesion Notes

Status: installed and validated; balance tuning active.

## Generated Gear Rarity Registry

Status: generated; in-game visual retest needed after client reimport.

The current gear rarity pass created separate indexes for weapons, armor, shields, magic/spells, and accessories/relics. The registry is meant to make loot readability consistent before deeper loot-table rewriting:

- `docs/WEAPON_INDEX.md`
- `docs/ARMOR_INDEX.md`
- `docs/SHIELD_INDEX.md`
- `docs/MAGIC_INDEX.md`
- `docs/ACCESSORY_RELIC_INDEX.md`
- `config/ascendant_index/gear_registry.json`

The rarity assignment uses exposed stats where possible, then falls back to material tier, mod system role, drop/source danger, and named boss/dragon/capstone identity. Damage is marked exact only when the source data exposes it; otherwise the row records whether the number is hardcoded/inherited or only Better Combat multiplier data was found.

Item Borders now uses exact manual item-ID groups from this registry, so the colored frame follows the assigned rarity color instead of the display-name color. This should make every indexed combat weapon, armor piece, shield, magic item, spell item, accessory, and relic visually consistent.

`config/ascendant_core/loot_rarity_rules.json` now owns the pack-level reward contract for rarity tiers, loot beams, rank floors, board reward ranges, boss rewards, and dragon-tier rewards. It does not rewrite loot tables by itself yet; it is the source for the next Bountiful/Open Loader loot generation pass.

Batch N does not actively rewrite loot yet. It adds the tools and structure context for later loot tuning:

- KubeJS is installed. Recipe/tag/loot scripts are still cautious scaffolds, while rarity tooltip, JEI alias, progression HUD, and Ascendant Core manifest bridges are active.
- LootJS is delayed until a focused loot scripting pass.
- IDAS adds more dungeon/structure contexts that may need loot review.
- Integrated Villages adds more village/civilization contexts that can support Bountiful contracts later.
- Almost Unified and Almost Unify Everything may affect duplicate commodity outputs, but unique boss, dragon, spell, Artifact, Bountiful, and skill milestone items are protected by policy.

Current integration audit:

- `docs/WORLD_INTEGRATION_AUDIT.md` found 4,324 loot tables and 10,551 recipes across the active jar set.
- This confirms the pack has enough loot and recipe surface for a real tuning pass; do not add another loot system before validating the current stack.
- Generated loot/integration configs from the active client are staged for Loot Integrations and Bountiful.

Later loot goals:

- dungeon chests can contain Iron's Spells scrolls and spell materials
- rare structures can contain Artifacts
- Cataclysm, Marium, and IceAndFire CE drops can receive clearer rarity/progression roles
- boss drops can feed skill-tree milestones and Bountiful contracts
- village bounties can request Born in Chaos parts, cooked foods, monster trophies, and dragon-tier materials

Validation focus for Batch N:

- Confirm chests open without item crashes.
- Confirm JEI still loads.
- Confirm structure loot from IDAS, YUNG, Moog structures, Cataclysm, Marium, IceAndFire CE, Iron's Spells, Artifacts, and Loot Integrations does not crash or produce missing items.
- Do not judge loot balance yet; full loot tuning happens after structural stability is proven.

Goal: rare loot should be exciting without making players overpowered too early.

## Batch E2 Verified Loot Layer

Status: installed and validated.

Installed through Packwiz:

- Artifacts
- Bountiful
- Loot Beams: Relooted
- Villager Names
- Loot Journal: Pickup Notifier
- Loot Integrations

Packwiz-resolved dependencies:

- Bountiful -> Kambrik.
- Villager Names -> Collective.
- Loot Journal -> Fragmentum.
- Artifacts -> Curios API.
- Loot Integrations -> Cupboard.

First E2 client load found the hidden dependency floor: Loot Integrations requires Cupboard `1.20.1-1.5.7` or above, and Artifacts requires Curios `5.8.1+1.20.1` or above. Cupboard `1.20.1-3.7` and Curios API `5.14.1+1.20.1` are installed now.

Loot Journal was selected over Pick Up Notifier because it has a current Minecraft 1.20.1 Forge file, explicit client-side metadata, and a richer pickup notification/journal feature set. Do not install both.

Loot Beams client tuning is staged in `config/lootbeams-client.toml`:

- Loot Beams' look-at-dropped-item tooltip is enabled, with item name and rarity combined into one box.
- Beam color uses item rarity color instead of item display-name color, so Epic items should render purple.
- Beam render distance is set to the mod's native maximum, `24.0`.
- All-item beams are disabled and `only_rare` is enabled. Loot Beams' native filter is non-common rarity rather than a true Epic-only threshold; if lower-rarity items still show beams, add exact item IDs to the blacklist after the next creative test or consider a replacement visual mod later.

Loot Journal client tuning is staged in `config/obscuria/loot_journal-client.toml`:

- Item pickup and overflow boxes remain enabled.
- XP pickup support, ray glow, and pickup sounds remain enabled.
- Loot Journal handles pickup notifications; Loot Beams handles the look-at-dropped-item world tooltip.

Loot Integrations is installed as a server-side loot bridge. YUNG Structures Addon for Loot Integrations is delayed because the visible 1.20.1-specific recent file was Fabric, not a clean Forge 1.20.1 target.

Batch E2 validation passed:

- Client creative/system test passed.
- Dedicated server boot/join test passed.
- 10-minute stability check passed.
- Artifacts, Bountiful, Villager Names, Loot Integrations, Kambrik, Collective, and Fragmentum are stable enough for the next batch.
- Loot Beams: Relooted and Loot Journal: Pickup Notifier remained client-only.
- No disposable survival test is required for batch validation.
- The previous loot-beam/UI concern is resolved and is not a Batch E2 blocker.

Full loot balance and UI tuning happens later after the major stack is installed.

## Batch F Installed Progression Pressure

Status: installed and validated.

Batch F adds magic, enemy escalation, events, ocean/ice danger, gear, travel, and medieval building polish. It passed client creative/system testing and dedicated server boot/join validation; deeper loot and reward balance still waits for the later full tuning pass.

Batch F systems that may affect progression:

- Iron's Spells 'n Spellbooks introduces spell progression and magic loot pressure.
- Born in Chaos, Aquamirae, Enhanced Celestials, and Bosses'Rise increase combat danger and reward expectations.
- Immersive Armors and Spartan Shields expand gear choices.
- Small Ships changes travel/exploration access.
- Handcrafted and Macaw's building mods add settlement polish without changing loot pools directly.

Batch F validation passed:

- Client creative/system test passed.
- Dedicated server boot/join test passed.
- Iron's Spells, Born in Chaos, Aquamirae, Enhanced Celestials, Bosses'Rise, Immersive Armors, Spartan Shields, Small Ships, Snow! Real Magic, Handcrafted, Macaw's Bridges, and Macaw's Fences/Walls are stable enough for the next batch.
- Variants & Ventures was removed after the Batch J startup crash with Entity Model Features and `variantsandventures:murk_skull`.
- No disposable survival test is required for batch validation.

Batch G later installed the approved dragon/boss/Create escalation set. Original Ice and Fire remains delayed because IceAndFire Community Edition was selected as the single active variant.

## Progression Shape

1. Survival and exploration.
2. First villages, backpacks, basic bounties.
3. Better movement and combat.
4. Low-tier dungeons and rare utility artifacts.
5. Skills/classes and early magic.
6. Minibosses and stronger dungeon loot.
7. Endgame bosses, dragons, and legendary equipment.

## Loot Sources

- Vanilla structures.
- YUNG structures.
- Towns and Towers / Structory.
- Bountiful bounty rewards.
- Boss/miniboss drops.
- Custom loot tables.

## Integration Goals

- Dungeon loot includes appropriate RPG weapons, spellbooks, artifacts, coins, and rare materials.
- Boss loot is meaningful but not universally best-in-slot.
- Magic and weapon progression should have multiple viable paths.
- Structure loot should match structure danger.

## Tools To Consider

- KubeJS.
- Datapacks.
- Loot Integrations, installed in E2.
- YUNG loot integration addons if an exact Forge 1.20.1-compatible project/file is confirmed.

## Prior Recommendation

Superseded by approved Batch G.

## Batch G Installed Progression Pressure

Status: installed and verified.

Batch G adds major progression pressure:

- IceAndFire Community Edition adds dragon materials, dragon gear, eggs, and dragon progression.
- L_Ender's Cataclysm adds boss loot and endgame structures.
- Marium's Soulslike Weaponry adds legendary weapons and boss-driven crafting.
- Create adds engineering progression and automation.
- Create Big Cannons adds artillery and griefing-risk tools.
- Farmer's Delight adds food and survival pacing.
- Create: Structures Arise adds Create-themed discovery content.

Batch G passed client and dedicated server validation. Do not deeply tune loot, food, dragon gear, boss drops, legendary weapons, Create automation, or cannon access until the later full balance pass.

Batch H adds civilization/atmosphere and Beautiful Enchanted Books, but it is not a loot-power expansion. Biome Music and Medieval Music were delayed from Batch H, then installed in Batch L as audio/presentation layers; Neko's Enchanted Books is delayed because Beautiful Enchanted Books was selected.

## Batch J Progression Risk

Status: installed and validated; balance tuning active.

Batch J adds several progression-adjacent pieces:

- Fantasy Armor adds new armor progression.
- T.O Magic was delayed after a Cataclysm `DungeonEyeItem` startup crash, so its spell add-on content is not active.
- Alex's Caves, Apothic Attributes, and Placebo were removed with T.O Magic because they were only added by that dependency chain.
- Iron's Spells remains updated to `3.16.1` and Iron's Lib to `1.1.0`; those versions need revalidation with the remaining Batch J set.
- Simply Swords Reforged, Excalibur, Vanilla Experience+, and other resource packs should be treated as visual layers, not new loot systems.

Do not tune loot tables or survival balance during Batch J validation. First confirm client boot, creative/system behavior, dedicated server join, and 10-minute stability.

Original Ice and Fire, Cataclysm addons, Marium addons, extra Ice and Fire addons, Create addon flood, Ars Nouveau, Theurgy, RPG Series modules, Dynamic Trees, Biomes O' Plenty, and additional structure packs beyond the Batch N Integrated Villages/IDAS test remain blocked.

## Anti-Overpower Checks

- Test early villages and surface structures for rare loot leaks.
- Keep high-tier spellbooks out of easy chests.
- Avoid stacking too many artifact/curio slots.
- Ensure mobs scale enough to challenge late gear.
- Keep Bountiful rewards and Artifacts chest access under review before committing a real survival world.
