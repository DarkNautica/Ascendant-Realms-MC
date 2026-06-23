# Smoky blue aura around any shadow mob tagged ar_shadow_glow. Runs every tick (cheap; only tagged mobs).
execute as @e[tag=ar_shadow_glow] at @s run particle minecraft:soul_fire_flame ~ ~0.7 ~ 0.32 0.6 0.32 0.005 2 normal
execute as @e[tag=ar_shadow_glow] at @s run particle minecraft:soul ~ ~0.5 ~ 0.3 0.5 0.3 0.01 1 normal
