# Magic, UI, And Skill Handoff

Last updated: 2026-06-18.

This is the short AI handoff for the systems Jayden asked future sessions not to guess about.

## What Is Live

- Iron's Spells is the primary spellcasting system.
- Puffish Skills is the active player skill tree system.
- The active Puffish category is the custom `Ascendant Web` under `config/puffish_skills/`.
- The Ascendant Web is also mirrored through `datapacks/ascendant_realms_skills/` and `openloader/data/ascendant_realms_skills/`.
- KubeJS powers the current rarity tooltip/readability layer and Ascendant progression bridge scripts.
- Item Borders, Legendary Tooltips, Loot Beams, JEI, MobHealthBar, Overflowing Bars, Traveler's Titles, FancyMenu, SpiffyHUD/Immersive UI resources, and the visual resource-pack stack are the current UI presentation layer.
- Complementary Reimagined is the selected shaderpack through `config/oculus.properties`.
- `config/ascendant_ui/keybind_policy.json` owns the curated keybind policy that sync applies to the active client.

## What Is Policy Or Audit-Only

- This section is audit-only unless a file below is explicitly described as live behavior.
- `config/ascendant_magic/*.json` is a progression policy scaffold. It does not hard-gate spells yet.
- `config/ascendant_progression/*.json` is a rank/skill/region guidance scaffold. It does not lock players out of content yet.
- `config/ascendant_ui/*.json` describes tooltip, rarity, mob danger, title, and keybind policy. Only already-existing UI scripts/configs and the keybind policy are active behavior.
- Mob danger tiers are documented, but there is not yet a live threat-tier overlay.
- Atlas coordinate-region titles are policy-only. Traveler's Titles biome/dimension titles are live.
- Magic loot and recipe audits are not broad rewrites. Do not enable magic gates or recipe gates without explicit approval.

## Magic System

Authoritative docs:

- `docs/MAGIC_INDEX.md`
- `docs/ASCENDANT_MAGIC_PROGRESSION.md`
- `docs/SPELL_REGION_AND_RANK_INDEX.md`
- `docs/MAGIC_LOOT_AND_RECIPE_AUDIT.md`

Core policy:

- Beginner magic should be discoverable but not overwhelming.
- High-tier magic should come from dangerous structures, bosses, rare materials, higher-rank contracts, or late-game exploration.
- Frost and ice magic lean Frostmarch/cold identity.
- Fire, sun, blaze, and desert magic lean Sunreach, southern arid routes, and Nether-adjacent content.
- Nature, poison, water, and storm magic lean Verdant Coast and wet/eastern routes.
- Earth, force, gravity, metal, and battle evocation lean Stoneback/highland routes or dangerous structures.
- Dark, void, eldritch, ancient, necromantic, and blood magic lean outer, corrupted, Nether, End, or high-rank routes.

Important numbers from the latest audit:

- Indexed spells: 113.
- Indexed magic items: 273.
- Magic loot sources: 154.
- Magic recipe entries: 206.

Keybinds:

- Spell wheel: `R`.
- Spell cast: `V`.
- Spell bar modifier: `Left Alt`.

## Skill Tree

Authoritative docs:

- `docs/SKILL_TREE_DESIGN.md`
- `docs/SKILL_TREE_IMPLEMENTATION_PLAN.md`
- `docs/SKILL_TREE_ATTRIBUTE_MAPPING.md`
- `docs/SKILL_TREE_BALANCE_NOTES.md`
- `docs/SKILL_TREE_TESTING.md`
- `docs/SKILL_TREE_INTEGRATION_HOOKS.md`
- `docs/SKILL_TREE_INTEGRATION_PLAN.md`
- `docs/ASCENDANT_PLAYER_PROGRESSION.md`
- `docs/GUILD_RANK_REQUIREMENT_MATRIX.md`

Current shape:

- One custom category: `Ascendant Web`.
- 113 nodes.
- 196 bidirectional connections after readability cleanup.
- Two starting points.
- Seven branch lanes: Warrior, Rogue / Duelist, Ranger / Hunter, Arcanist, Engineer / Artificer, Survivalist / Explorer, and Dragonbound / Endgame.
- Default Puffish pacing is 1 skill point per web level.
- Managed milestone bonus points come from `config/ascendant_progression/progression.json` at levels 10, 20, 35, 50, 70, 90, and 110.

Design boundary:

- Skill points are player power growth.
- Guild rank is public status and proof of achievements.
- Do not turn rank into a narrow XP checklist.
- Do not hard-lock existing skills by rank yet.
- Future rank trials may use bounties, bosses, regional survival, structure clears, and skill milestones, but that is not live enforcement yet.

Keybind:

- Ascendant Web: `K`.

## UI And Item Identity

Authoritative docs:

- `docs/UI_CLARITY_AND_FEEDBACK_AUDIT.md`
- `docs/RARITY_TOOLTIP_VISUAL_POLICY.md`
- `docs/MOB_DANGER_UI_POLICY.md`
- `docs/REGION_TITLE_UI_POLICY.md`
- `docs/ASCENDANT_NAMEPLATES.md`

Core item identity:

- `config/ascendant_index/gear_registry.json` is the canonical item rarity/source registry.
- `config/ascendant_index/rarity_schema.json` defines the rarity language and palette.
- Item Borders owns border color.
- KubeJS adds the readable Ascendant rarity tooltip line.
- Legendary Tooltips styles frames and should not override Item Borders colors.
- Loot Beams should use rarity color and stay rare enough that common drops do not flood the screen.

Canonical rarity colors:

| Rarity | Color |
| --- | --- |
| Common | `#9CA3AF` |
| Uncommon | `#55FF55` |
| Rare | `#55AAFF` |
| Epic | `#D966FF` |
| Legendary | `#FFE66D` |
| Mythic | `#FF3B00` |
| Ascendant | `#E6FBFF` |

## Progression Spine

Authoritative docs:

- `docs/ASCENDANT_PLAYER_PROGRESSION.md`
- `docs/GUILD_RANK_REQUIREMENT_MATRIX.md`
- `docs/SKILL_TREE_INTEGRATION_PLAN.md`
- `docs/ASCENDANT_LOOT_ECONOMY.md`
- `docs/RECIPE_PROGRESSION_AUDIT.md`

Rank intent:

- Unranked / E / D / C / B / A / S ranks should feel like evaluation, not grind.
- Rank should guide players toward suitable content without suffocating free exploration.
- Gear rarity, spell tier, bounty tier, boss milestones, and region readiness should line up.
- No rank gates are live yet unless a future approved pass explicitly enables them.

## Keybind Policy

Authoritative doc/config:

- `docs/KEYBIND_REEVALUATION.md`
- `config/ascendant_ui/keybind_policy.json`

Primary controls:

- `K`: Ascendant Web.
- `L`: Quest Log.
- `R`: Iron's spell wheel.
- `V`: Iron's spell cast.
- `Left Alt`: Iron's spell modifier.
- `Z`: Combat Roll.
- `B`: Backpack.
- `G`: Curios.
- `U`: Xaero waypoints.
- `Y`: Xaero minimap settings.

Non-gameplay shader/menu/debug keys are intentionally unbound. Do not put shader reload back on `R` or shader toggle back on `K`.

## Do Not Guess

- Do not add new magic mods.
- Do not enable magic gates, recipe gates, rank gates, or loot rewrites without explicit approval.
- Do not regenerate rarity blindly.
- Do not treat audit JSON as live enforcement unless a doc explicitly says it is active.
- Do not redesign the menu from this handoff.
- Do not use Atlas coordinate-region title policy as if it were already live.
