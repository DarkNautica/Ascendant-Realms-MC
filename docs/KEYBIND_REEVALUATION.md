# Keybind Reevaluation

Last updated: 2026-06-18.

## Status

Active keybind cleanup policy is tracked in `config/ascendant_ui/keybind_policy.json`.

The active CurseForge instance options file remains the real Minecraft keybind storage, but `scripts/sync-active-client-files.ps1` now applies the tracked policy after preserving the normal resource-pack lines. This avoids blindly replacing Jayden's graphics, audio, and other personal options while still keeping the pack's core controls sane.

## Design Rules

- Preserve vanilla movement, combat, inventory, chat, hotbar, command, screenshot, and perspective keys.
- Keep core RPG actions on simple keys.
- Move secondary gameplay actions onto modifier chords or mouse side buttons.
- Unbind visual/debug/menu actions that do not need prime keys during play.
- Do not use shader reload/toggle keys for normal gameplay space.

## Primary Controls

| Action | Binding | Reason |
| --- | --- | --- |
| Ascendant Web / Puffish Skills | `K` | Main progression surface. Kept on the original easy key. |
| Quest Log | `L` | Public quest/progression reference. Vanilla advancements is unbound. |
| Iron's Spells spell wheel | `R` | Core combat magic action. Claims the old overloaded `R` conflict. |
| Iron's Spells cast | `V` | Core spell execution. |
| Iron's Spells bar modifier | `Left Alt` | Spell-bar modifier stays close to cast/wheel controls. |
| Combat Roll | `Z` | Core movement/combat defense. |
| Backpack | `B` | Common inventory action. |
| Backpack inventory interaction | `C` | Kept simple because it is an active inventory action. |
| Curios | `G` | Equipment/accessory surface. |
| Xaero waypoints | `U` | Map planning surface. |
| Xaero minimap settings | `Y` | Map settings surface. |
| New waypoint | `Ctrl+N` | Still available without stealing `B`. |

## Conflict Decisions

| Old conflict | Decision |
| --- | --- |
| `R` had shader reload, Combat Roll, JEI recipe, dragon fire, Small Ships sail, Souls parry, Quark variant selector, and Iron's spell wheel. | Iron's spell wheel owns `R`; Combat Roll moved to `Z`; JEI recipe moved to `Ctrl+R`; dragon fire moved to `Alt+R`; Small Ships sail moved to `Alt+S`; Souls parry moved to mouse side button; shader reload unbound. |
| `K` had Puffish Skills and shader toggle. | Puffish Skills owns `K`; shader toggle is unbound. |
| `V` had Cataclysm boots, Souls collect summons, and Iron's cast. | Iron's cast owns `V`; Cataclysm boots moved to `Alt+V`; Souls collect summons moved to `Ctrl+V`. |
| `Left Alt` had Souls ability, Create tool menus, and Iron's spell modifier. | Iron's modifier owns `Left Alt`; Souls ability moved to `mouse.5`; Create menus moved to `Ctrl+C` and `Ctrl+B`. |
| `B` had Xaero new waypoint, backpack, and Souls switch weapon. | Backpack owns `B`; new waypoint moved to `Ctrl+N`; Souls switch weapon moved to `Alt+B`. |
| Mouse left/right/middle had vanilla and JEI cheat/recipe/use conflicts. | Vanilla attack/use/pick remain unchanged; JEI mouse cheat and duplicate recipe/use binds are unbound or moved to keyboard chords. |

## Intentionally Unbound

- Oculus shader reload, shader toggle, and shader-pack selection.
- FancyMenu scene start/pause/reset controls.
- Titles title-selection menu.
- MCA skin library.
- Presence Footsteps settings.
- Vanilla creative toolbar save/load.
- Vanilla advancements, because the pack-facing quest/progression entry is the Quest Log.
- JEI cheat-mode mouse shortcuts that conflicted with vanilla attack/use.

## Gameplay Notes

- Soulslike parry is now `mouse.4` and Souls weapon ability is now `mouse.5`. If the mouse does not expose side buttons correctly, remap only those two in-game.
- JEI recipe lookup is `Ctrl+R`, JEI uses lookup is `Ctrl+U`, and JEI bookmark is `Ctrl+A`.
- Create Ponder is `Ctrl+P`; Create tool menu is `Ctrl+C`; Create toolbelt is `Ctrl+B`.
- Cataclysm active abilities remain available on `X`, `Alt+C`, `Alt+Y`, and `Alt+V`.
- Dragon mount controls moved to `Alt+R`, `Alt+G`, and `Ctrl+X`.

## Test Checklist

Use any loaded world; a new world is not required for keybind testing.

1. Press `K` and confirm Ascendant Web opens.
2. Press `L` and confirm Quest Log opens.
3. Hold a spellbook and confirm `R`, `V`, and `Left Alt` operate Iron's Spells controls.
4. Press `Z` and confirm Combat Roll works.
5. Press `B` and confirm backpack opens.
6. Press `G` and confirm Curios opens.
7. Press `U`, `Y`, and `Ctrl+N` and confirm waypoint/map controls are sensible.
8. Confirm `R` no longer reloads shaders and `K` no longer toggles shaders.
9. Confirm attack/use/pick block still work on mouse left/right/middle.

## Current Boundary

This pass changes client controls only. It does not alter terrain, mobs, structures, roads, villages, loot, recipes, magic gates, rank gates, or NPC placement.
