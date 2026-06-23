team leave @s
team join ar_rank_b @s
scoreboard players set @s ar_guild_rank 4
tellraw @s [{"text":"Guild rank set: ","color":"gold"},{"text":"B-Rank","color":"blue","bold":true}]
title @s times 10 55 15
title @s title [{"text":"B-Rank","color":"blue","bold":true}]
title @s subtitle {"text":"Guild evaluation recorded","color":"gold","italic":true}
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1.0
