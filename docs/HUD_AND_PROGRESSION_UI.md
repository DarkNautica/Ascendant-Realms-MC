# HUD And Progression UI

Status: implemented through a KubeJS server-side Puffish Skills bridge; hotfixed for the KubeJS/Rhino runtime errors seen in the live console; needs in-game visual retest after full client restart/reimport.

Latest root-cause fix: the active log showed the bridge could not read JSON configs because Rhino first treated direct Java `Path.resolve(String)` as ambiguous, then KubeJS blocked `java.io.File`. The bridge now builds config paths from the allowed `KubeJSPaths.CONFIG` handle and passes those paths to KubeJS `JsonIO`, so the HUD should use `config/ascendant_progression/progression.json` instead of default fallback values without loading blocked Java file/path classes.

## Source Of Truth

The Ascendant Realms level system is not a separate fake XP layer.

- Puffish Skills owns Ascendant Web XP, level, earned skill points, spent skill points, and remaining skill points.
- `config/puffish_skills/categories/ascendant/experience.json` owns the XP curve and kill-XP source.
- `config/puffish_skills/categories/ascendant/category.json` owns the 2 starting points.
- `kubejs/server_scripts/ascendant_progression.js` reads Puffish data and mirrors it into HUD, popups, and scoreboards.
- `config/ascendant_progression/progression.json` owns HUD placement, sync rate, display offset, and milestone bonus-point tuning.
- FancyMenu/SpiffyHUD can browse the bar art, but the live data binding comes from KubeJS Painter, not the layout-editor preview.

## Live Features

- Custom second XP bar rendered as a blue 20-segment vanilla-style strip through KubeJS Painter.
- Compact `Lv <number>` text above the bar.
- Current XP / required XP text inside the bar.
- Remaining skill-point count beside the level text.
- Short pulse when Ascendant XP increases.
- `Level Up! <level>` title, subtitle, sound cue, and temporary HUD banner when the Ascendant Web level increases.
- Real multiplayer nameplate number through the `ar_skill_level` scoreboard objective.
- Compact visual layout: no large backing slab, no custom texture crop, a blue segmented fill that echoes the vanilla XP bar, and `draw_mode=ingame` so resource-pack screens, menus, and FancyMenu editors do not show the live HUD.
- Creative/spectator safety: `config/ascendant_progression/progression.json` sets `hide_in_creative=true` and `hide_in_spectator=true`; the KubeJS bridge clears old Painter elements when those modes are active.

## Vertical Stack

Intended bottom HUD order:

- Hotbar.
- Vanilla green XP bar and vanilla XP level.
- Ascendant blue skill-XP bar.
- Health, armor, hunger, and mana/status rows above the Ascendant bar.

The Ascendant bar is positioned by `config/ascendant_progression/progression.json`. The current KubeJS layer keeps the custom strip thin and moves it above the vanilla heart/armor rows so it stops covering them. Iron's Spells mana is nudged upward by one row in `config/irons_spellbooks-client.toml`. Overflowing Bars is tracked in `config/overflowingbars-client.toml` so its chat and vanilla XP-level handling stays stable. If the vanilla health/hunger rows must be physically shifted to make the exact requested stack, build a tiny client HUD helper mod instead of faking it with another large overlay.

Research note: KubeJS Painter supports `ingame` draw mode for hiding from menus, but it is still an overlay layer. It can draw the Ascendant bar and clear it in creative/spectator/menu contexts; it cannot truly move Minecraft's vanilla health, hunger, armor, or XP rows. The clean long-term version is an `Ascendant HUD Helper` client-side Forge mod that registers a proper HUD overlay and/or shifts vanilla GUI anchors deliberately.

## Skill Point Backend

Puffish Skills remains responsible for the normal earned point pacing. The current design is:

- 2 starting points from the Puffish category config.
- Default Puffish earned points from the Ascendant Web level track.
- Managed milestone bonus points from `config/ascendant_progression/progression.json`.

Current milestone bonuses add 1 extra skill point at player-facing levels:

- 10
- 20
- 35
- 50
- 70
- 90
- 110

The KubeJS bridge tracks how many bonus points it owns in player persistent data. If an admin or later quest system grants extra points manually, the script preserves those manual points instead of wiping them.

## Scoreboards

`config/openloader/data/ascendant_realms_identity/` creates the scoreboard objectives, and KubeJS keeps the values synced:

- `ar_skill_level` - player-facing Ascendant level; displayed below player names.
- `ar_skill_xp` - current Ascendant XP inside the current level.
- `ar_skill_xp_req` - XP required for the current level.
- `ar_skill_sp` - unspent skill points.
- `ar_skill_spent` - spent skill points.
- `ar_skill_total` - total available skill points.

The older vanilla XP fallback objectives `ar_level` and `ar_level_last` are retained only as compatibility leftovers. They should not drive the visible level anymore.

## Tuning

Edit `config/ascendant_progression/progression.json` for:

- `display_level_offset` if the player-facing level should start at 1 instead of raw Puffish level 0.
- `display_level_cap` for the maximum displayed level.
- `sync_interval_ticks` for HUD/scoreboard refresh frequency.
- `managed_bonus_points.milestones` for slow long-term skill-point pacing.
- `hud` colors, segmented vanilla-style bar sizing, placement, track styling, and draw mode.
- `config/irons_spellbooks-client.toml` for the mana row offset.
- `config/overflowingbars-client.toml` for vanilla stacked health/armor behavior and chat/XP-level placement.
- `level_up` sound, duration, and banner timing.

Edit `config/puffish_skills/categories/ascendant/experience.json` for the actual XP curve and XP sources.

## Client Test

- Reimport or sync the latest client files.
- Launch the client.
- Join a test world.
- Confirm the custom Ascendant bar appears near the hotbar.
- Confirm the custom Ascendant bar appears as a blue vanilla-style segmented strip and no longer covers the health/hunger/armor rows.
- Confirm `Lv <number>` appears above the Ascendant bar.
- Confirm current XP / required XP appears inside the bar.
- Confirm remaining skill points appear beside the level text.
- Confirm there is only one custom bar, not a gray texture slab or an empty bar above a blue strip.
- Confirm there is no large gray/black HUD panel behind the bar.
- Confirm health, hunger, armor, and Iron's Spells mana sit above the Ascendant bar.
- Open inventory, resource packs, and FancyMenu/SpiffyHUD customization screens; confirm the custom bar is hidden on menus.
- Switch to creative mode; confirm the custom bar clears while creative is active.
- Kill a few mobs and confirm the bar fill updates.
- Gain an Ascendant Web level and confirm the `Level Up! <level>` popup, sound, and HUD banner.
- Open the Ascendant Web and confirm available points match the HUD.
- Confirm the HUD does not overlap the hotbar, Xaero minimap, YDM mob bars, Stylish Effects, or Overflowing Bars.
- Confirm SpiffyHUD/FancyMenu still open normally; they are now visual tooling, not the source of the skill-XP binding.
- Check the latest log for `[Ascendant Progression] HUD bridge active`; if that appears but the bar is still invisible, the next fix is visual placement/layering rather than Puffish data binding.
- Check the latest log for absence of `Path.resolve` ambiguity, `java.io.File`, or class-filter warnings from `ascendant_progression.js`; if those warnings return, the bridge is falling back to defaults again.

## Server Test

- Boot the dedicated server with the synced `config/puffish_skills/`, `config/ascendant_progression/`, `config/openloader/`, and `kubejs/` folders.
- Join with the client.
- Confirm no mod mismatch.
- Confirm `ar_skill_level` appears below player names from another player's view.
- Confirm disconnect/rejoin preserves level, XP, and skill points.
- Confirm killing mobs updates the HUD after reconnect.
- Let the server run 10 minutes.

## Remaining Gap

Enemy numeric levels are still not implemented. Scaling Health is active for threat scaling, but the inspected configs do not expose a clean `Level X` nameplate. Keep YDM's MobHealthBar for enemy health readability until a dedicated enemy-level overlay is built or verified.
