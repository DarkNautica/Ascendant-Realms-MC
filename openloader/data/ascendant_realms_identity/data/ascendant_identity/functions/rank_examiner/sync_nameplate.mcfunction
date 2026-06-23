# Sync the visible player team to the current public Guild rank score.
team leave @s
execute if score @s ar_guild_rank matches ..0 run team join ar_rank_unranked @s
execute if score @s ar_guild_rank matches 1 run team join ar_rank_e @s
execute if score @s ar_guild_rank matches 2 run team join ar_rank_d @s
execute if score @s ar_guild_rank matches 3 run team join ar_rank_c @s
execute if score @s ar_guild_rank matches 4 run team join ar_rank_b @s
execute if score @s ar_guild_rank matches 5 run team join ar_rank_a @s
execute if score @s ar_guild_rank matches 6.. run team join ar_rank_s @s
