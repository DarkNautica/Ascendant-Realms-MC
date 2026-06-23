# NPC Visual Validation Report

Generated: 2026-06-17T04:48:43Z

Status: audit/control scaffold only. This pass did not place NPCs, inject villages, add NPC mods, or enable new world NPC population behavior.

## Summary

- MCA Reborn installed: True.
- MCA Default Medieval metadata present: True.
- MCA Default Medieval active in `options.txt`: True.
- MCA medieval clothing PNGs counted: 974.
- CustomNPC bridged MCA-style skins: 12 in the compatibility resource pack and 12 in the CustomNPCs native folder.
- Requested important profession silhouettes covered: 9/9.
- Rival hunters with loadout, nameplate, and drop policy: 5/5.
- Loadout item IDs missing from `gear_registry.json`: 0.
- Visual-only skins without an equivalent gear note: 0.
- Modern/unknown MCA skin filename flags: 0.

## Mod And Tool Audit

| Layer | Status | Evidence |
| --- | --- | --- |
| customnpcs_unofficial | present | mods/customnpcs-unofficial.pw.toml |
| easy_npc_bundle | present | mods/easy-npc.pw.toml |
| easy_npc_config_ui | present | mods/easy-npc-config-ui.pw.toml |
| easy_npc_core | present | mods/easy-npc-core.pw.toml |
| guard_villagers | present | mods/guard-villagers.pw.toml |
| human_companions | present | mods/human-companions.pw.toml |
| mca_default_medieval_resource_pack | present | resourcepacks/mca-default-medieval-by-de4th4sh.pw.toml |
| mca_reborn | present | mods/minecraft-comes-alive-reborn.pw.toml |
| villager_names | present | mods/villager-names-serilum.pw.toml |

## Important Profession Silhouettes

| Profession | Tool | Rank | Silhouette | Visible Gear |
| --- | --- | --- | --- | --- |
| Guild Clerk | Easy NPC | d_rank | ledger cane, villager hat, simple robe, approachable Guild colors | mainhand: `irons_spellbooks:artificer_cane`, head: `artifacts:villager_hat`, chest: `immersive_armors:robe_chestplate` |
| Rank Examiner | Easy NPC | b_rank | judgment blade, crown or formal headpiece, heroic armor | mainhand: `irons_spellbooks:truthseeker`, head: `irons_spellbooks:gold_crown`, chest: `fantasy_armor:hero_chestplate` |
| Bounty Master | Easy NPC | c_rank | crossbow, heavy field armor, practical hunter stance | mainhand: `minecraft:crossbow`, head: `immersive_armors:heavy_helmet`, chest: `immersive_armors:heavy_chestplate` |
| Guild Arcanist | Easy NPC | b_rank | staff, visible spellbook, academy mage coat | mainhand: `irons_spellbooks:graybeard_staff`, offhand: `irons_spellbooks:diamond_spell_book`, head: `irons_spellbooks:archevoker_helmet`, chest: `irons_spellbooks:archevoker_chestplate` |
| Quartermaster | Easy NPC | d_rank | utility armor, practical weapon, workshop gear | mainhand: `minecraft:iron_sword`, head: `immersive_armors:steampunk_helmet`, chest: `immersive_armors:steampunk_chestplate` |
| Guard Captain | CustomNPCs or Guard Villagers where combat is required | c_rank | longsword, shield, warrior armor, clear captain profile | mainhand: `simplyswords:iron_longsword`, offhand: `spartanshields:iron_basic_shield`, head: `immersive_armors:warrior_helmet`, chest: `immersive_armors:warrior_chestplate` |
| Tavern Keeper | Easy NPC | d_rank | warm tavern clothing, rumor prop, visible noncombat role | mainhand: `artifacts:universal_attractor`, head: `artifacts:novelty_drinking_hat`, chest: `immersive_armors:robe_chestplate` |
| Village Elder | Easy NPC | d_rank | cane, villager hat, elder robe, low-threat posture | mainhand: `irons_spellbooks:artificer_cane`, head: `artifacts:villager_hat`, chest: `immersive_armors:robe_chestplate` |
| Rival Hunter | CustomNPCs-Unofficial for combat-capable prototypes; Easy NPC for social versions | varies_by_roster | class-specific gear, visible rank palette, distinct weapon profile | None recorded |
| Wounded Hunter | CustomNPCs for encounter prototypes | c_rank | bow, damaged-looking hunter armor, field survival read | mainhand: `minecraft:bow`, head: `immersive_armors:bone_helmet`, chest: `immersive_armors:bone_chestplate` |

## Rival Hunter Visual Contract

| Rival | Rank | Class | Gear Tier | Drop Policy | Visible Gear |
| --- | --- | --- | --- | --- | --- |
| Mira Ash | C-Rank | Scout | epic | rival_story_safe_drops | mainhand: `irons_spellbooks:autoloader_crossbow`, offhand: `simplyswords:watching_warglaive`, head: `artifacts:night_vision_goggles`, chest: `immersive_armors:prismarine_chestplate` |
| Darius Crowe | B-Rank | Duelist | legendary | rival_story_safe_drops | mainhand: `simplyswords:netherite_rapier`, offhand: `spartanshields:diamond_basic_shield`, head: `fantasy_armor:thief_helmet`, chest: `fantasy_armor:thief_chestplate` |
| Seren Valehart | B-Rank | Arcanist | legendary | rival_story_safe_drops | mainhand: `irons_spellbooks:magehunter`, offhand: `irons_spellbooks:diamond_spell_book`, head: `irons_spellbooks:archevoker_helmet`, chest: `irons_spellbooks:archevoker_chestplate` |
| Kael Vorn | A-Rank | Monster Hunter | mythic | rival_story_safe_drops | mainhand: `iceandfire:dragonbone_sword_fire`, offhand: `spartanshields:netherite_basic_shield`, head: `fantasy_armor:dragonslayer_helmet`, chest: `fantasy_armor:dragonslayer_chestplate` |
| The Black Hound | S-Rank | Unknown | ascendant | boss_tier_curated | mainhand: `soulsweapons:pure_moonlight_shortsword`, offhand: `cataclysm:gauntlet_of_bulwark`, head: `soulsweapons:forlorn_helmet`, chest: `soulsweapons:forlorn_chestplate` |

## Validation Notes

- MCA medieval pack status: clean.
- Missing important silhouettes: none.
- Missing rival contracts: none.
- Missing bridged skins: none.
- Unknown or modern-looking MCA asset names: none found by filename scan.

## Boundary

Easy NPC remains the preferred tool for social NPCs. CustomNPCs remains the preferred tool for combat-capable rival prototypes and current generated test profiles. Human Companions is still generic hunter/companion review material, not the authored rival roster. Guard Villagers and Villager Names support village identity but are not used here to create new placed NPC content.
