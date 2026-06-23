# Ascendant Shadow Army - modded test mobs (Born in Chaos + Mowzie's), frozen + glowing aura.
# REQUIRES the resource pack enabled. Some are bosses; spawned with NoAI so they hold still.
weather clear
time set night
team add ar_shadow_glow
team modify ar_shadow_glow color aqua
summon born_in_chaos_v1:bone_imp ~-10 ~ ~5 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Bone Imp","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon born_in_chaos_v1:baby_skeleton ~-7 ~ ~5 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Baby Skeleton","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon born_in_chaos_v1:bloody_gadfly ~-4 ~1 ~5 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Bloody Gadfly","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon born_in_chaos_v1:barrel_zombie ~-1 ~ ~5 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Barrel Zombie","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon born_in_chaos_v1:bonescaller ~3 ~ ~5 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Bonescaller","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon mowziesmobs:foliaath ~7 ~ ~5 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Foliaath","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon mowziesmobs:frostmaw ~13 ~ ~7 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Frostmaw","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
team join ar_shadow_glow @e[tag=ar_shadow_glow]
effect give @e[tag=ar_shadow_glow] minecraft:glowing 1000000 0 true
tellraw @p [{"text":"[Shadow Army] ","color":"dark_purple","bold":true},{"text":"Modded test mobs spawned (Born in Chaos + Mowzie's). ","color":"white"},{"text":"/function ascendant_shadow:clear","color":"aqua"},{"text":" to remove.","color":"gray"}]
