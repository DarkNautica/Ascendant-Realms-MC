# Visual Shader Plan

Approved proof target: Minecraft 1.20.1 Forge 47.4.20.

## Shader Loader

Recommended for 1.20.1 Forge:

- Embeddium
- Oculus

Status: installed in Batch A.

Do not use OptiFine.

If the project pivots to Fabric:

- Sodium
- Iris

If the project pivots to 1.21.1 NeoForge:

- Sodium or Embeddium path must be checked for the chosen shader loader.
- Iris has NeoForge metadata for 1.21.1.

## Shaderpacks

Recommended first shaderpack:

- Complementary Reimagined

Status: installed through Packwiz as a Modrinth shaderpack.

Optional second test:

- Complementary Unbound
- Photon

Use one shaderpack at a time during testing.

## Client-Only Visual Mods

Installed client-only:

- Fresh Animations resource pack
- EMF
- ETF
- 3D Skin Layers
- Legendary Tooltips
- Enchantment Descriptions
- Traveler's Titles
- Visual Traveler's Titles resource pack
- Visual Traveler's Title Biomes Addon resource pack
- Ascendant Realms Traveler's Titles fallback resource pack
- Falling Leaves
- Loot Beams: Relooted
- Loot Journal: Pickup Notifier
- Auroras
- Beautiful Enchanted Books [MOD EDITION]
- Perception
- OctoLib/ShatterLib
- Wavey Capes
- Xaero's Minimap
- Advancement Plaques
- Icon Xaero's resource pack
- Icon Xaero's X FreshAnimations resource pack
- The Rename Compat Project resource pack
- Cubic Leaves resource pack
- Simply Swords Reforged resource pack
- Cubic Sun & Moon resource pack
- Embellished Stone resource pack
- STONEBORN UI resource pack
- Excalibur resource pack
- Vanilla Experience+ resource pack
- FancyMenu
- Konkrete
- Melody
- Immersive UI

Main menu polish:

- The supplied title image is packaged at `config/fancymenu/assets/ascendant_realms_title.png`.
- FancyMenu should save the final title-screen layout from the in-game editor during the next client boot.
- See `docs/MAIN_MENU_POLISH.md`.

Loot Beams E2 tuning:

- Config file: `config/lootbeams-client.toml`.
- Dropped-item look tooltips are enabled and configured to combine item name and rarity into one box.
- Beam color follows item rarity color instead of display-name color.
- Render distance is set to `24.0`, the native cap exposed by Loot Beams.
- Beams are limited to non-common rarity through Loot Beams' `only_rare` option. If the next test still shows beams below Epic, use blacklists or revisit the beam mod choice.

Installed visual mods treated as both-side for this pack:

- Particular Reforged
- Subtle Effects
- Fzzy Config
- Kotlin for Forge

Subtle Effects requires Forge 47.4.14 or newer and pulls Fzzy Config, which requires Kotlin for Forge 4.12.0 in this pack. Multiplayer validation showed Subtle Effects crashes when kept client-only on the dedicated server, so Subtle Effects, Fzzy Config, and Kotlin for Forge stay both-side while Subtle Effects remains active. Particular Reforged also stays both-side because the Forge multiplayer handshake required it.

Delayed:

- Continuity if connected textures are needed
- Pick Up Notifier, unless Loot Journal is rejected during E2 validation
- Enhanced Boss Bars
- Biome Edition Visual Traveler's Titles, because the verified Modrinth/CurseForge files target Minecraft 1.21.1 instead of the current 1.20.1 Forge pack
- Better Animations Collection, delayed because it overlaps with Fresh Animations, EMF, ETF, and the current visual stack
- Simple Clouds / Project Atmosphere, delayed because Weather, Storms & Tornadoes is the selected major weather path
- Neko's Enchanted Books, delayed because Beautiful Enchanted Books was selected for Batch H
- TravelersCrossroads, delayed because Packwiz rejected it for the configured 1.20.1 Forge target and the visible current files target 1.21.x NeoForge

## Server Pack

Do not upload shader loaders, shaderpacks, resource packs, or client-only UI/animation mods to the dedicated server unless a selected provider file or validation result proves a server component is required. Subtle Effects and Particular Reforged are proven server-required for this pack's current multiplayer setup.

## Shaderpack Path

For launcher instances:

```text
.minecraft/shaderpacks/
```

For a Packwiz-managed client later, shaderpacks can be documented for manual install or added as Packwiz resource files only if licensing/distribution allows it.

## Resource Pack Load Order

Managed resource-pack priority:

Ascendant Realms now ships a root `options.txt` with the intended enabled resource-pack order and `config/resourcepackoverrides.json` to reapply that order through the client-only Resource Pack Overrides mod. The root `options.txt` must include `version:3465`; without a modern options version, Minecraft can run the old keybind migration path and fail on modern key names such as `key.keyboard.left.alt`, which collapses the selected pack list back to defaults. In Minecraft's saved `resourcePacks` list, later entries win. Vanilla Experience+ includes vanilla `textures/environment/sun.png` and `moon_phases.png`, so it must stay below Cubic Sun & Moon. Its downloaded filename is normalized to `Vanilla Experience Plus.zip` because section-sign color codes in a pack filename can make Packwiz, options, and Resource Pack Overrides disagree about the same pack.

Critical saved-order tail:

1. `file/Vanilla Experience Plus.zip`
2. `file/cubic-sun-moon-v1.8.5.zip`
3. `file/Visual Titles 1.3.zip`
4. `file/Visual Travelers Titles Biomes Addon.zip`
5. `file/ascendant-realms-travelers-titles`
6. `file/ascendant-realms-compat-fixes`

This keeps Vanilla Experience+ active, lets Cubic Sun & Moon override the sky textures, and lets the Traveler's Titles visual/fallback packs override broad font/title resources so biome and dimension popups do not fall back to plain white text. Resource Pack Overrides also marks the external visual/music packs required and force-compatible, which should prevent the repeated manual re-enable problem after restarts or resource reload failures.

Active-instance repair rule: if packs disable themselves again, first confirm `ResourcePackOverrides-v8.0.3-1.20.1-Forge.jar` exists in the active CurseForge instance `mods` folder, then confirm active `options.txt` still has `version:3465` and the full resource-pack list. The sync script intentionally removes `.pw.toml` metadata and stale color-code Vanilla Experience+ filenames from the live `resourcepacks` folder so Minecraft does not log Packwiz metadata files as non-pack entries or chase the old filename.

Traveler's Titles coverage:

- Visual Traveler's Titles covers vanilla dimensions and several common modded dimension packs.
- Visual Traveler's Title Biomes Addon covers vanilla biomes on Minecraft 1.20.x.
- Ascendant Realms Traveler's Titles fallback adds readable titles and colors for the current 1.20.1 pack gaps: 99 Terralith biomes, IceAndFire CE's Dreadlands dimension and dread biomes, and Iron's Spells' pocket dimension.
- `config/travelerstitles-forge-1_20.toml` is tracked and synced so title timing, enabled state, and Ascendant default colors survive CurseForge reimports.

Batch J visual validation notes:

- Check STONEBORN, Excalibur, and Vanilla Experience+ together; they overlap broad UI/texture surfaces and may need order changes.
- Keep Cubic Sun & Moon above Vanilla Experience+ so the dedicated 3D sun/moon textures are not overridden.
- Check Icon Xaero's and Icon Fresh with Xaero's Minimap after importing the client pack.
- Check Advancement Plaques with Embellished Stone after earning a simple advancement.
- Treat ugly overlaps as polish issues unless the client crashes or menus become unreadable.

## Performance Settings

Start with:

- Complementary Reimagined medium preset.
- Shadows medium.
- Volumetric lighting low or medium.
- Reflections low.
- Entity shadows on.
- Render distance 10-12 for client testing.
- Simulation distance 6-8 for local integrated testing.

Increase only after the MVP client boots smoothly.
