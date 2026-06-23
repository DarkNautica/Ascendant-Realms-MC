# FancyMenu Assets

`assets/ascendant_realms_title.png` and `assets/minecraft_title.png` both point to the current Ascendant Realms title image for the custom title screen. The second filename exists so FancyMenu's asset picker exposes a clearly named new option instead of only showing the older title filename.

`assets/ascendant_realms_background.mp4` is the staged cloud/fog video background. It should stay video-only H.264 Baseline 1920x1080/30fps because the old audio-first High-profile MP4 was found by WaterMedia but failed native playback and got auto-cleared by FancyMenu's watchdog. `assets/ascendant_realms_background_original.mp4` preserves the supplied source file for future re-encoding.

`assets/ascendant_level_bar_spritesheet.png` is Jayden's 182x10 Ascendant level bar, staged for FancyMenu/SpiffyHUD asset browsing. A mirrored copy also lives at `kubejs/assets/kubejs/textures/gui/ascendant_level_bar_spritesheet.png` for future client-overlay work.

`assets/ascendant_menu_status.txt` is the bottom-left status text source. It uses FancyMenu placeholders for live loaded mod count and reads the Ascendant pack version from `assets/ascendant_pack_meta.json`, which is generated from `pack.toml` during client sync. Do not replace it with a hardcoded mod count.

On first client boot, open FancyMenu's title-screen editor and save the actual layout from inside the game. Use this image as the title graphic, keep the main buttons centered below it, and verify the menu at desktop and smaller window sizes before calling the menu pass validated.
