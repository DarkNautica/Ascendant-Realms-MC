# Give the glowing aura to every hostile mob within 24 blocks (test the aura on egg-spawned/natural mobs).
team add ar_shadow_glow
team modify ar_shadow_glow color aqua
tag @e[type=#minecraft:skeletons,distance=..24] add ar_shadow_glow
tag @e[type=zombie,distance=..24] add ar_shadow_glow
tag @e[type=husk,distance=..24] add ar_shadow_glow
tag @e[type=drowned,distance=..24] add ar_shadow_glow
tag @e[type=zombie_villager,distance=..24] add ar_shadow_glow
tag @e[type=creeper,distance=..24] add ar_shadow_glow
tag @e[type=enderman,distance=..24] add ar_shadow_glow
tag @e[type=spider,distance=..24] add ar_shadow_glow
tag @e[type=cave_spider,distance=..24] add ar_shadow_glow
tag @e[type=wolf,distance=..24] add ar_shadow_glow
team join ar_shadow_glow @e[tag=ar_shadow_glow]
effect give @e[tag=ar_shadow_glow] minecraft:glowing 1000000 0 true
tellraw @p [{"text":"[Shadow Army] ","color":"dark_purple","bold":true},{"text":"Aura applied to nearby shadow mobs.","color":"white"}]
