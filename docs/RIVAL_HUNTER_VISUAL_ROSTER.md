# Rival Hunter Visual Roster

Generated: 2026-06-17T04:48:43Z

Status: visual identity roster only. No rival placement, village injection, Hunter Board placement, or new NPC behavior was enabled.

## Roster

| Rival | Rank | Class | Style | Gear Tier | Nameplate | Loadout | Drop Policy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mira Ash | C-Rank | Scout | bow, light blade, evasive movement | epic | mira_ash | mira_ash | rival_story_safe_drops |
| Darius Crowe | B-Rank | Duelist | fast sword, shield pressure, duels | legendary | darius_crowe | darius_crowe | rival_story_safe_drops |
| Seren Valehart | B-Rank | Arcanist | Iron's Spells, wards, spellblade support | legendary | seren_valehart | seren_valehart | rival_story_safe_drops |
| Kael Vorn | A-Rank | Monster Hunter | heavy weapon, shield, monster trophies | mythic | kael_vorn | kael_vorn | rival_story_safe_drops |
| The Black Hound | S-Rank | Unknown | unknown | ascendant | black_hound | black_hound | boss_tier_curated |

## Equipment Reads

- **Mira Ash**: mainhand: `irons_spellbooks:autoloader_crossbow`, offhand: `simplyswords:watching_warglaive`, head: `artifacts:night_vision_goggles`, chest: `immersive_armors:prismarine_chestplate`
- **Darius Crowe**: mainhand: `simplyswords:netherite_rapier`, offhand: `spartanshields:diamond_basic_shield`, head: `fantasy_armor:thief_helmet`, chest: `fantasy_armor:thief_chestplate`
- **Seren Valehart**: mainhand: `irons_spellbooks:magehunter`, offhand: `irons_spellbooks:diamond_spell_book`, head: `irons_spellbooks:archevoker_helmet`, chest: `irons_spellbooks:archevoker_chestplate`
- **Kael Vorn**: mainhand: `iceandfire:dragonbone_sword_fire`, offhand: `spartanshields:netherite_basic_shield`, head: `fantasy_armor:dragonslayer_helmet`, chest: `fantasy_armor:dragonslayer_chestplate`
- **The Black Hound**: mainhand: `soulsweapons:pure_moonlight_shortsword`, offhand: `cataclysm:gauntlet_of_bulwark`, head: `soulsweapons:forlorn_helmet`, chest: `soulsweapons:forlorn_chestplate`

## Rules

- Rival hunters must communicate rank through `config/ascendant_guild/nameplates.json`.
- Rival hunters must communicate class through visible gear from `config/ascendant_index/gear_registry.json`.
- Named rivals should not drop full gear by default; use quest rewards, fragments, trophies, or scripted post-fight rewards.
- The Black Hound can remain rumor-first, but still needs a rank, nameplate profile, loadout profile, and drop policy so future implementation does not improvise.
