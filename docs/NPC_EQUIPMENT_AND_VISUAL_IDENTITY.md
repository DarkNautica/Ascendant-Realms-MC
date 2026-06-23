# NPC Equipment And Visual Identity

Status: formal registry scaffold implemented. Generated CustomNPC spawn sets are active for testing, but automatic village population is not enabled yet.

Ascendant Realms now has a real NPC equipment contract at `config/ascendant_guild/npc_loadouts.json`. The goal is simple: important NPCs should look like they belong to the same world the player loots, crafts, and fights through.

Latest generated-spawn repair: CustomNPCs visible gear is now written to top-level `Weapons` and `Armor` tags, while `NpcInv` is kept empty because it is the CustomNPCs drop-table inventory. Mainhand uses weapon slot `0`, visible offhand uses weapon slot `2`, and vanilla `HandItems`/`ArmorItems` remain as fallback data. Generated NPCs now use MCA-medieval-style bridge skins under `customnpcs:textures/entity/ascendant_mca/`; those PNGs are mirrored into both the Ascendant compatibility resource pack and the CustomNPCs-native `customnpcs/assets/customnpcs/textures/entity/ascendant_mca/` folder to prevent magenta missing skins.

## Rules

- Important social NPCs use Easy NPC first.
- Combat-capable rivals and elite encounters use CustomNPCs-Unofficial first.
- Every visible gear piece in the registry points at a real item from `config/ascendant_index/gear_registry.json`.
- Social NPCs use no-drop identity gear.
- Rival hunters use curated gear and story-safe drop policies instead of dropping full equipment by default.
- Rank controls the normal rarity ceiling: D-Rank is mostly rare, C-Rank can reach epic, B-Rank can reach legendary, A-Rank can reach mythic, and S-Rank can carry ascendant gear.

## Starting Profiles

- Guild Clerk: robe, villager hat, artificer cane.
- Rank Examiner: crown, hero armor, Truthseeker.
- Bounty Master: heavy armor and crossbow.
- Guild Arcanist: archevoker gear, staff, spell book.
- Quartermaster: steampunk armor and basic supply weapon.
- Guard Captain: warrior armor, Simply Swords weapon, Spartan shield.
- Mira Ash: scout crossbow, night-vision goggles, light armor.
- Darius Crowe: duelist armor, rapier, shield.
- Seren Valehart: arcanist armor, Magehunter, spell book.
- Kael Vorn: dragon-hunter gear and dragonbone weapon.
- The Black Hound: mythic Forlorn gear and ascendant signature weapon.

## Validation

`scripts/check-pack.py` now checks that loadout items exist in the generated gear registry, rank rarity ceilings are respected unless an override is documented, named rivals have drop policies, matching nameplate profiles exist, generated MCA-style bridge skins exist, and generated spawn functions use CustomNPCs' visible `Weapons`/`Armor` fields rather than nesting gear inside `NpcInv`.

## Next Implementation Steps

1. Open a creative test copy.
2. Create Easy NPC templates for Guild Clerk, Rank Examiner, Bounty Master, Arcanist, Quartermaster, Tavern Keeper, and Village Elder.
3. Create CustomNPCs templates for Mira Ash, Darius Crowe, Seren Valehart, Kael Vorn, and The Black Hound.
4. Use the registry as the equipment source, then screenshot/verify each NPC silhouette.
5. Only after templates look good, place them near Hunter Board and Guild Outpost structures.
