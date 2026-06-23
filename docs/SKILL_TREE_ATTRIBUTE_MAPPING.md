# Skill Tree Attribute Mapping

Status: updated for the unified Ascendant Web.

## Reward Sources Used

The generated web uses only attribute reward types already proven or detected in the pack:

- Vanilla generic attributes.
- Pufferfish's Attributes.
- Iron's Spells attributes.
- Projectile Damage Attribute.

## Branch Mapping

| Branch | Primary attributes |
|---|---|
| Core | `generic.luck`, `puffish_attributes:resistance` |
| Warrior | `puffish_attributes:melee_damage`, `generic.attack_speed`, `generic.knockback_resistance`, `puffish_attributes:damage_reflection`, `puffish_attributes:axe_damage`, `generic.attack_damage`, `generic.armor`, `generic.movement_speed`, `puffish_attributes:armor_shred`, `puffish_attributes:sword_damage`, `puffish_attributes:toughness_shred`, `puffish_attributes:knockback`, `generic.armor_toughness`, `puffish_attributes:melee_resistance` |
| Rogue / Duelist | `generic.movement_speed`, `puffish_attributes:sprinting_speed`, `generic.attack_speed`, `puffish_attributes:sword_damage`, `puffish_attributes:fall_reduction`, `generic.luck`, `puffish_attributes:stealth`, `puffish_attributes:armor_shred`, `puffish_attributes:resistance`, `puffish_attributes:melee_damage`, `puffish_attributes:fortune` |
| Ranger / Hunter | `puffish_attributes:ranged_damage`, `puffish_attributes:tamed_damage`, `generic.luck`, `puffish_attributes:fortune`, `puffish_attributes:melee_resistance`, `puffish_attributes:ranged_resistance`, `puffish_attributes:bow_projectile_speed`, `projectile_damage:generic`, `puffish_attributes:armor_shred`, `puffish_attributes:tamed_resistance`, `generic.armor`, `puffish_attributes:stealth`, `puffish_attributes:resistance`, `puffish_attributes:magic_resistance`, `generic.movement_speed`, `puffish_attributes:melee_damage` |
| Arcanist | `irons_spellbooks:max_mana`, `irons_spellbooks:spell_power`, `irons_spellbooks:mana_regen`, `irons_spellbooks:cooldown_reduction`, `irons_spellbooks:spell_resist`, `puffish_attributes:magic_resistance`, `puffish_attributes:melee_damage`, `irons_spellbooks:holy_spell_power`, `puffish_attributes:healing`, `irons_spellbooks:ice_spell_power`, `irons_spellbooks:lightning_spell_power`, `irons_spellbooks:cast_time_reduction`, `generic.armor` |
| Engineer / Artificer | `puffish_attributes:mining_speed`, `puffish_attributes:pickaxe_speed`, `puffish_attributes:breaking_speed`, `puffish_attributes:axe_speed`, `generic.movement_speed`, `puffish_attributes:sprinting_speed`, `puffish_attributes:consuming_speed`, `puffish_attributes:natural_regeneration`, `generic.armor`, `puffish_attributes:resistance`, `projectile_damage:generic`, `puffish_attributes:crossbow_projectile_speed`, `puffish_attributes:mount_speed`, `puffish_attributes:fall_reduction`, `puffish_attributes:healing`, `puffish_attributes:armor_shred`, `puffish_attributes:fortune` |
| Survivalist / Explorer | `puffish_attributes:natural_regeneration`, `generic.movement_speed`, `puffish_attributes:resistance`, `puffish_attributes:fall_reduction`, `puffish_attributes:consuming_speed`, `puffish_attributes:healing`, `puffish_attributes:sprinting_speed`, `generic.luck`, `puffish_attributes:fortune`, `generic.armor`, `puffish_attributes:melee_resistance`, `puffish_attributes:ranged_resistance`, `puffish_attributes:magic_resistance` |
| Dragonbound / Endgame | `puffish_attributes:tamed_damage`, `puffish_attributes:tamed_resistance`, `generic.armor`, `irons_spellbooks:fire_magic_resist`, `irons_spellbooks:ice_magic_resist`, `puffish_attributes:melee_damage`, `puffish_attributes:armor_shred`, `generic.luck`, `puffish_attributes:resistance_shred`, `irons_spellbooks:eldritch_magic_resist`, `irons_spellbooks:ender_magic_resist`, `puffish_attributes:magic_resistance`, `puffish_attributes:toughness_shred`, `puffish_attributes:mount_speed`, `puffish_attributes:resistance`, `puffish_attributes:damage_reflection`, `generic.armor_toughness`, `irons_spellbooks:spell_power`, `puffish_attributes:ranged_damage`, `irons_spellbooks:cooldown_reduction` |

## Notes

- Attribute IDs should not be changed by hand in generated JSON. Update `scripts/generate-ascendant-skill-web.js` and regenerate.
- If the game rejects an attribute, remove or replace only the failing reward and rerun the generator.
- Keep `Effect:` text synchronized with actual reward values.
