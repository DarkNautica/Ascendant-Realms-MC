# Remove all mobs spawned by the shadow-army preview.
kill @e[tag=ascendant_shadow_preview]
tellraw @p [{"text":"[Shadow Army] ","color":"dark_purple","bold":true},{"text":"Preview mobs cleared.","color":"white"}]
