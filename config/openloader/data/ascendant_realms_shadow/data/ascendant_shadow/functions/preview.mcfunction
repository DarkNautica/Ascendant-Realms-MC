# Ascendant Shadow Army - frozen preview line of every shadow mob, with a glowing aura.
# REQUIRES the "Ascendant Shadow Army" resource pack ENABLED to see the shadow look.
weather clear
time set night
team add ar_shadow_glow
team modify ar_shadow_glow color aqua
team modify ar_shadow_glow nametagVisibility always
summon minecraft:zombie ~-11 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Zombie","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon minecraft:husk ~-9 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Husk","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon minecraft:drowned ~-7 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Drowned","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon minecraft:zombie_villager ~-5 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Villager","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon minecraft:skeleton ~-3 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Skeleton","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon minecraft:wither_skeleton ~-1 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Wither Skeleton","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon minecraft:stray ~1 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Stray","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon minecraft:creeper ~3 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Creeper","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon minecraft:enderman ~5 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Enderman","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon minecraft:spider ~7 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Spider","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon minecraft:cave_spider ~9 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Cave Spider","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
summon minecraft:wolf ~11 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Wolf","color":"aqua"}',Tags:["ascendant_shadow_preview","ar_shadow_glow"]}
team join ar_shadow_glow @e[tag=ar_shadow_glow]
effect give @e[tag=ar_shadow_glow] minecraft:glowing 1000000 0 true
tellraw @p [{"text":"[Shadow Army] ","color":"dark_purple","bold":true},{"text":"Preview spawned with glowing aura. ","color":"white"},{"text":"/function ascendant_shadow:clear","color":"aqua"},{"text":" to remove.","color":"gray"}]
