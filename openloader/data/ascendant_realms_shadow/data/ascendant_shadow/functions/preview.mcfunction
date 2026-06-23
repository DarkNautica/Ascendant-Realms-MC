# Ascendant Shadow Army - spawn a frozen line of every shadow mob in front of you.
# REQUIRES the "Ascendant Shadow Army" resource pack to be ENABLED to see the shadow look.
# Sets night + clear weather so undead do not burn while you inspect them.
weather clear
time set night
summon minecraft:zombie ~-11 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Zombie","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
summon minecraft:husk ~-9 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Husk","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
summon minecraft:drowned ~-7 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Drowned","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
summon minecraft:zombie_villager ~-5 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Villager","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
summon minecraft:skeleton ~-3 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Skeleton","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
summon minecraft:wither_skeleton ~-1 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Wither Skeleton","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
summon minecraft:stray ~1 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Stray","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
summon minecraft:creeper ~3 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Creeper","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
summon minecraft:enderman ~5 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Enderman","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
summon minecraft:spider ~7 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Spider","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
summon minecraft:cave_spider ~9 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Cave Spider","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
summon minecraft:wolf ~11 ~ ~4 {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,CustomNameVisible:1b,CustomName:'{"text":"Shadow Wolf","color":"aqua"}',Tags:["ascendant_shadow_preview"]}
tellraw @p [{"text":"[Shadow Army] ","color":"dark_purple","bold":true},{"text":"Preview line spawned in front of you. ","color":"white"},{"text":"Enable the resource pack if you haven't. Run ","color":"gray"},{"text":"/function ascendant_shadow:clear","color":"aqua"},{"text":" to remove.","color":"gray"}]
