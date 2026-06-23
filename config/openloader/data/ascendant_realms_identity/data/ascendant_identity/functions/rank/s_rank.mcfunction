team leave @s
team join ar_rank_s @s
scoreboard players set @s ar_guild_rank 6
tellraw @s [{"text":"Guild rank set: ","color":"gold"},{"text":"S-Rank","color":"dark_purple","bold":true}]
title @s times 10 55 15
title @s title [{"text":"S-Rank","color":"dark_purple","bold":true}]
title @s subtitle {"text":"Guild evaluation recorded","color":"gold","italic":true}
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1.0
