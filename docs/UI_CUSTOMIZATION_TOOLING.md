# UI Customization Tooling

Status: installed through Packwiz. Packwiz refresh, check-pack, client export, and server staging export passed; in-game client review is still pending after reimport.

## Goal

Give Ascendant Realms enough UI tooling to make the pack feel custom without replacing the whole interface stack blindly.

## Installed

| Mod | Role | Side | Why it belongs |
|---|---|---|---|
| SpiffyHUD | FancyMenu HUD addon | Client | Best current path for custom HUD frames, images, and animated HUD elements. |
| Drippy Loading Screen | FancyMenu loading-screen addon | Client | Lets the loading screen use Ascendant Realms branding, tips, and visual styling. |
| Item Borders | Inventory rarity borders | Client | Connects directly to the universal rarity plan and makes rare loot readable. |
| Stylish Effects | Status-effect UI overhaul | Client | Makes buffs/debuffs from food, spells, bosses, seasons, and weather easier to read. |
| Overflowing Bars | Compact health/armor/toughness bars | Client | Helps the scaled health/armor stack stay readable without huge rows of icons. |
| AppleSkin | Food/hunger/saturation HUD | Both | Useful for Farmer's Delight, Alex's Delight, survival tuning, and accurate multiplayer food data. |

## Item Borders Rarity Source

Item Borders is now driven by the generated gear registry instead of item display-name colors.

- Source registry: `config/ascendant_index/gear_registry.json`
- Generated client config: `config/itemborders-common.toml`
- Generated KubeJS metadata: `kubejs/startup_scripts/ascendant_gear_rarity.js`
- Generated KubeJS tooltip text: `kubejs/client_scripts/ascendant_rarity_tooltips.js`
- Human indexes: `docs/WEAPON_INDEX.md`, `docs/ARMOR_INDEX.md`, `docs/SHIELD_INDEX.md`, `docs/MAGIC_INDEX.md`, and `docs/ACCESSORY_RELIC_INDEX.md`

`auto_borders` is disabled and `manual_borders` is filled with exact item IDs grouped by Ascendant rarity color. This means the colored item frame should match the assigned rarity tier even when a mod uses a custom display-name color.

The KubeJS file is intentionally no-op. It does not set vanilla `item.rarity`, because custom mod item classes can reject that mutation during startup. Item Borders is the source of truth for the colored frames.

Rarity tooltip text is handled separately in the generated client script. It uses KubeJS `ItemEvents.tooltip` to add only the rarity tier label while Legendary Tooltips styles the visible tooltip frame. The tooltip intentionally omits the old `Rarity:` prefix plus backend `Effect:`, `Index:`, and `Why:` lines. Only Legendary, Mythic, and Ascendant labels are bold; Mythic and Ascendant use clean tier text without side symbols or extra `Flame`/`Pulse` wording.

NBT-backed guide aliases are handled in `kubejs/client_scripts/ascendant_jei_aliases.js`. The current explicit alias is the Simply Swords Runic Grimoire, which is a `patchouli:guide_book` stack with `patchouli:book=simplyswords:runic_grimoire` rather than a standalone item ID.

## Dependencies

- SpiffyHUD -> FancyMenu, Konkrete, Melody.
- Drippy Loading Screen -> FancyMenu, Konkrete, Melody.
- Item Borders -> Iceberg and Prism, already present.
- Stylish Effects -> Puzzles Lib, already present.
- Overflowing Bars -> Puzzles Lib, already present.
- AppleSkin -> no additional dependency added by Packwiz.

## Delayed

- RPG-Hud is delayed as a separate A/B test. It is a stronger full-HUD replacement and may conflict with SpiffyHUD, STONEBORN, Immersive UI, Xaero's Minimap, YDM's MobHealthBar, and the current title/skill UI direction.

## What This Enables

- Branded title/loading flow: FancyMenu plus Drippy.
- Custom HUD composition: KubeJS Painter renders the live Ascendant Web XP bar, with the same Ascendant level bar art staged at `config/fancymenu/assets/ascendant_level_bar_spritesheet.png` for FancyMenu/SpiffyHUD browsing.
- Better rarity readability: Item Borders plus Legendary Tooltips plus Loot Beams.
- Gear hover clarity: KubeJS generated tooltip text plus Legendary Tooltips frame styling.
- Better effect readability: Stylish Effects.
- Better scaled-stat readability: Overflowing Bars.
- Better food/survival readability: AppleSkin.

## Custom Ascendant HUD Binding

SpiffyHUD gives us visual HUD tooling, but it is no longer the source of the live skill-XP binding.

The live Ascendant Web bar is now driven by:

- `config/ascendant_progression/progression.json`
- `kubejs/server_scripts/ascendant_progression.js`
- `kubejs/assets/kubejs/textures/gui/ascendant_level_bar_spritesheet.png` for future asset browsing; the live HUD currently uses KubeJS rectangles instead of this texture because the texture path produced gray overlay artifacts.

The KubeJS bridge reads Puffish Skills, mirrors the level to `ar_skill_level`, draws the custom bar, shows XP/current required values, shows unspent skill points, and fires the level-up popup. It uses `draw_mode=ingame` and hides in creative/spectator so it does not sit over resource-pack screens or UI editors. SpiffyHUD remains useful for future decorative HUD experiments, but the active progress bar should be tested through normal gameplay.

Current boundary: the live bar is intentionally drawn with KubeJS rectangles because the imported custom PNG produced gray overlay artifacts. KubeJS can hide and draw the overlay cleanly, but it cannot shift vanilla heart/hunger/armor/XP anchors. If the exact final HUD stack still needs vanilla rows moved upward, build a lightweight client-only Forge HUD helper rather than adding another overlay mod.

Runic Grimoire JEI note: JEI rejected the exact NBT-backed Patchouli guide stack as an empty runtime ingredient. The safe alias now injects the base `patchouli:guide_book` into JEI while the real `patchouli:book=simplyswords:runic_grimoire` stack keeps its Ascendant tooltip styling.

## Client Test

- Launch the client.
- Confirm no missing dependency screen.
- Confirm SpiffyHUD config/editor is available with FancyMenu.
- Confirm `ascendant_level_bar_spritesheet.png` is available as an image/HUD asset for manual UI work.
- Confirm the KubeJS-rendered Ascendant Web XP bar appears in gameplay with level text above it.
- Confirm the KubeJS-rendered Ascendant Web XP bar does not show over resource-pack screens or creative mode.
- Confirm the latest log has no KubeJS `Path.resolve` ambiguity warning and no JEI `ingredients must not be empty` warning from `ascendant_jei_aliases.js`.
- Confirm killing mobs updates the Ascendant XP bar.
- Confirm the visible skill-point count matches the Ascendant Web.
- Confirm Drippy Loading Screen changes or exposes loading-screen customization.
- Confirm Item Borders renders rarity borders in inventory without fighting Legendary Tooltips.
- Confirm generated rarity label text appears in item hover tooltips without backend effect/index/reason lines.
- Confirm sample weapons from Simply Swords, Marium's Soulslike Weaponry, Cataclysm, IceAndFire CE, Born in Chaos, and Aquamirae have frame colors matching their index rarity.
- Confirm Farmer's Delight/Alex's Delight/Slice & Dice cooking knives do not receive combat-rarity borders unless later promoted manually.
- Confirm Stylish Effects changes status-effect display and remains readable with Xaero's Minimap.
- Confirm Overflowing Bars renders health/armor/toughness compactly with AttributeFix and scaled stats.
- Confirm AppleSkin shows food/hunger/saturation information for vanilla, Farmer's Delight, and Alex's Delight food.
- Confirm STONEBORN, Immersive UI, FancyMenu, SpiffyHUD, and Drippy do not make screens unreadable.

## Server Test

- Export server staging.
- Materialize server mods from the active CurseForge instance with `-Clean`.
- Confirm AppleSkin is copied server-side.
- Confirm SpiffyHUD, Drippy Loading Screen, Item Borders, Stylish Effects, and Overflowing Bars are absent from the dedicated server.
- Boot server.
- Join with the client.
- Confirm no mod mismatch.
- Confirm food/saturation info remains accurate with AppleSkin.
- Disconnect/rejoin.
