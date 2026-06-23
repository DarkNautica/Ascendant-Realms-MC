# Remove preview mobs and strip the glowing aura from anything that has it.
kill @e[tag=ascendant_shadow_preview]
effect clear @e[tag=ar_shadow_glow] minecraft:glowing
team leave @e[tag=ar_shadow_glow]
tag @e[tag=ar_shadow_glow] remove ar_shadow_glow
tellraw @p [{"text":"[Shadow Army] ","color":"dark_purple","bold":true},{"text":"Preview cleared and aura removed.","color":"white"}]
