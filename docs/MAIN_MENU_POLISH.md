# Main Menu Polish

Status: installed and playtest validated.

Goal: clean up the title screen, use the supplied Ascendant Realms title image, and keep the UI layer client-only.

Latest packaging status: Jayden's saved FancyMenu title-screen layout has been imported from the active CurseForge client instance into the Packwiz repo at `config/fancymenu/customization/custom_title_screen_layout.txt`. It is enabled for `title_screen` with `layout_index = 0`, so a fresh client reimport should load it as the default title-screen layout instead of requiring hand setup again.

Latest video repair: the title-screen MP4 was present and referenced correctly, but the active client log showed WaterMedia failing to resolve/play the old audio-first High-profile MP4 and FancyMenu auto-clearing the native video background after its watchdog timeout. The packaged MP4 has been re-encoded as a video-only H.264 Baseline 1920x1080/30fps file with fast-start metadata. The original supplied file remains preserved as `config/fancymenu/assets/ascendant_realms_background_original.mp4`.

## Installed

- FancyMenu: `fancymenu_forge_3.9.3_MC_1.20.1.jar`
- Konkrete: `konkrete_forge_1.8.0_MC_1.20-1.20.1.jar`
- Melody: `melody_forge_1.0.3_MC_1.20.1-1.20.4.jar`
- WATERMeDIA: Multimedia API: `watermedia-3.0.0.17.jar`
- WATERMeDIA: Binaries: `wm_binaries-3.0.0-rc.1.jar`
- Immersive UI: `ImmersiveUI-FORGE-0.3.0.jar`
- Drippy Loading Screen: `drippyloadingscreen_forge_3.1.2_MC_1.20.1.jar`
- SpiffyHUD: `spiffyhud_forge_3.1.2_MC_1.20.1.jar`

## Source And Compatibility Notes

- FancyMenu was installed from the CurseForge Minecraft 1.20.1 Forge file. Konkrete and Melody were installed as its required client dependencies.
- WATERMeDIA: Multimedia API and WATERMeDIA: Binaries were added through Packwiz because FancyMenu requires them for local video backgrounds.
- Immersive UI was installed from the Modrinth Minecraft 1.20.1 Forge file.
- Drippy Loading Screen and SpiffyHUD are FancyMenu add-ons for the loading screen and in-game HUD.
- All UI/menu/video-background mods in this section are client-only in Packwiz and should not be copied to a dedicated server.

## Staged Assets

The supplied title image and mist/fog background video are staged at:

- `config/fancymenu/assets/ascendant_realms_title.png`
- `config/fancymenu/assets/minecraft_title.png`
- `config/fancymenu/assets/ascendant_realms_background.mp4`
- `config/fancymenu/assets/ascendant_realms_background_original.mp4`
- `config/fancymenu/assets/ascendant_level_bar_spritesheet.png`
- `config/fancymenu/assets/ascendant_menu_status.txt`
- `config/fancymenu/assets/ascendant_pack_meta.json`

FancyMenu should use `ascendant_realms_title.png` as the main title graphic on the title screen. `minecraft_title.png` is kept as a compatibility alias so old FancyMenu layouts that still point at that filename now resolve to the same new title art. The MP4 is staged for a subtle cloud/fog animated background element.

`ascendant_level_bar_spritesheet.png` is staged here so SpiffyHUD/FancyMenu's in-game asset picker can browse the custom 182x10 Ascendant level bar. The same PNG is also mirrored as `kubejs/assets/kubejs/textures/gui/ascendant_level_bar_spritesheet.png` for a future KubeJS or custom-client overlay.

`ascendant_menu_status.txt` is the clean bottom-left status text source. It intentionally uses FancyMenu placeholders instead of hardcoded numbers:

```text
Ascendant Realms v{"placeholder":"json","values":{"source":"/config/fancymenu/assets/ascendant_pack_meta.json","json_path":"$.version"}}
{"placeholder":"loadedmods"} Mods
```

`ascendant_pack_meta.json` is generated from `pack.toml` by `scripts/update-fancymenu-status-assets.ps1` before client sync, so the version follows the Packwiz pack version. The mod count comes from FancyMenu's live `loadedmods` placeholder.

## Packaged Default Layout

The saved default layout is now packaged at:

- `config/fancymenu/customization/custom_title_screen_layout.txt`
- `config/fancymenu/options.txt`
- `config/fancymenu/customizablemenus.txt`
- `config/fancymenu/custom_gui_screens.txt`
- `config/fancymenu/video_element_controller_metas.json`
- `config/fancymenu/layout_editor/widgets/element_layer_order.txt`
- `config/drippyloadingscreen/options.txt`

The title layout currently references `config/fancymenu/assets/minecraft_title.png`, which is the compatibility alias for the current Ascendant Realms title art. It also includes a direct bottom-left text element using FancyMenu placeholders:

```text
{"placeholder":"loadedmods"} Mods
Ascendant Realms v{"placeholder":"json","values":{"source":"/config/fancymenu/assets/ascendant_pack_meta.json","json_path":"$.version"}}
```

The MP4 background asset is referenced in the saved layout, WaterMedia is included in the client export, and the saved video background block is enabled by default. If the title screen ever crashes or the video is too heavy, disable only the video element first while keeping FancyMenu, Drippy, SpiffyHUD, and the static title assets active.

FancyMenu layout files are safest to revise from the in-game editor. After edits, copy the active instance's `config/fancymenu/` and `config/drippyloadingscreen/` files back into this repo before exporting.

## Layout Direction

The latest playtest passed with the packaged Ascendant Realms title asset.

Recommended title-screen layout:

- Hide or replace the vanilla Minecraft logo.
- Add an image element using `config/fancymenu/assets/ascendant_realms_title.png`.
- Add a video/background element using `config/fancymenu/assets/ascendant_realms_background.mp4` if FancyMenu exposes it cleanly in the editor.
- Anchor the title image near the upper center.
- Keep the title image large, but leave room for the menu buttons and panorama/background.
- Place the main buttons in a clean centered stack below the image.
- Keep accessibility buttons and version/modlist access visible.
- Avoid covering the splash text or let FancyMenu hide it if the new title art makes it noisy.

## Client Test

- Import the latest client export.
- Launch the client.
- Confirm there is no missing dependency screen.
- Confirm FancyMenu and Immersive UI load.
- Confirm WATERMeDIA loads without a startup dependency warning.
- Confirm Drippy Loading Screen loads and exposes loading-screen customization.
- Confirm SpiffyHUD loads and exposes HUD customization.
- Open the FancyMenu editor from the title screen.
- Confirm `custom_title_screen_layout.txt` loads automatically on the title screen.
- Confirm `ascendant_realms_title.png`, `minecraft_title.png`, and `ascendant_realms_background.mp4` are visible in FancyMenu assets.
- Confirm `ascendant_level_bar_spritesheet.png` is visible in FancyMenu/SpiffyHUD assets for HUD layout work.
- Confirm the bottom-left status text uses live mod count and Packwiz version placeholders, not hardcoded values.
- Confirm the MP4 background appears in FancyMenu outside the editor. If it still shows purple/black or falls back to the old/static background, check `logs/latest.log` for WaterMedia or FancyMenu watchdog messages before changing the layout.
- Confirm the main menu is readable at 1920x1080 and one smaller window size.
- Confirm buttons are clickable and not overlapped.
- Confirm resource packs and STONEBORN still render menus readably.

## Server Test

- Confirm FancyMenu, Konkrete, Melody, WATERMeDIA, WATERMeDIA Binaries, Immersive UI, Drippy Loading Screen, and SpiffyHUD are absent from the materialized dedicated-server `mods` folder.
- If any of those jars appear on the server, remove them unless a future multiplayer test proves they are required.

## Risks

- FancyMenu is powerful and layout files are sensitive to the screen/editor format. Do not hand-edit a complex layout unless a saved known-good file exists.
- FancyMenu video backgrounds are picky about local media. Keep `ascendant_realms_background.mp4` video-only H.264 Baseline unless a later in-game test proves another encoding is accepted.
- Immersive UI changes screen presentation. If a menu becomes unreadable, disable Immersive UI first before removing FancyMenu.
- Resource packs such as STONEBORN and Vanilla Experience+ may visually clash with FancyMenu styling; treat this as polish unless it blocks navigation.


## Custom art background (Arcane Void)
The title screen now uses a hand-stylized **art background** instead of the mist video:
`config/fancymenu/assets/ascendant_realms_menu_art.png` (1920x1080) — a bright, painterly Mojang-splash-style sunset vista — a forest-framed view over a reflective
lake to a far treeline, glowing sun, a lone hunter on a dock, and a subtle distant gate. Soft
edges (not pixel art), palette chosen to complement the blue/teal/green title logo. Regenerate with
`python scripts/generate-ascendant-menu-art.py` (composition + palette constants at the top).

In `config/fancymenu/customization/custom_title_screen_layout.txt` the `image` menu_background
is enabled (`show_background = true`, `source` -> the art) and the `video` menu_background is
disabled. To restore the mist video, flip those two `show_background` flags back.


## Animated ambient title background
The title screen uses an animated loop built from `AscendantBackgroundImage.png`:
`config/fancymenu/assets/ascendant_realms_menu_anim.mp4` (1920x1080, H.264 Constrained
Baseline, 30fps, ~5s seamless loop, video-only + faststart = WaterMedia-friendly). Subtle
ambience: breathing glow on the sun/gate/lanterns, drifting + twinkling fireflies, water-
reflection shimmer, faint star twinkle, and a gentle camera drift.

FancyMenu wiring: the `video` menu_background plays the loop (primary); the `image`
menu_background shows `ascendant_realms_menu_still.png` (the still) as a fallback if WaterMedia
fails. Rebuild the loop with `python scripts/generate-ascendant-menu-anim.py <start> <end>`
then re-encode with ffmpeg (libx264 baseline, yuv420p, +faststart). Effect strength/counts
are constants near the top of that script.


## GOTCHA: FancyMenu background field keys
FancyMenu `menu_background` blocks use DIFFERENT texture keys per type:
- `background_type = image`  -> key is **`image = ...`** (supports animated GIF/APNG)
- `background_type = video`  -> key is **`source = ...`** (WaterMedia; unreliable here)
Using `source =` on an image background silently fails (no texture) and the menu falls back
to the vanilla `light_dirt_background.png` (which the medieval resource packs recolor to
parchment). Also keep EXACTLY ONE `show_background = true` across all blocks. Current active
background: animated APNG `ascendant_realms_menu_live.png` via the `image` key.
