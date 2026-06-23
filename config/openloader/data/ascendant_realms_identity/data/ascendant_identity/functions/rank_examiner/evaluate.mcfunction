# Rank Examiner evaluation. This is the current public bridge until FTB Quest trials are authored.
scoreboard players add @s ar_guild_rank 0
scoreboard players add @s ar_guild_rep 0
scoreboard players add @s ar_hunt_kills 0
scoreboard players add @s ar_elite_kills 0
scoreboard players add @s ar_bounties_done 0
scoreboard players add @s ar_structures_done 0
scoreboard players add @s ar_bosses_done 0
scoreboard players add @s ar_dragons_done 0
scoreboard players add @s ar_skill_level 0
scoreboard players add @s ar_skill_sp 0
function ascendant_identity:rank_examiner/sync_nameplate
tellraw @s [{"text":"Rank Examiner","color":"gold","bold":true},{"text":": Your proof will be judged.","color":"gray"}]
function ascendant_identity:rank_examiner/debug_scores
execute if score @s ar_guild_rank matches ..0 if score @s ar_guild_rep matches 10.. run function ascendant_identity:rank/e_rank
execute if score @s ar_guild_rank matches ..1 if score @s ar_guild_rep matches 35.. if score @s ar_hunt_kills matches 10.. run function ascendant_identity:rank/d_rank
execute if score @s ar_guild_rank matches ..2 if score @s ar_guild_rep matches 90.. if score @s ar_hunt_kills matches 35.. run function ascendant_identity:rank/c_rank
execute if score @s ar_guild_rank matches ..3 if score @s ar_guild_rep matches 210.. if score @s ar_bosses_done matches 1.. run function ascendant_identity:rank/b_rank
execute if score @s ar_guild_rank matches ..4 if score @s ar_guild_rep matches 500.. if score @s ar_bosses_done matches 4.. run function ascendant_identity:rank/a_rank
execute if score @s ar_guild_rank matches ..5 if score @s ar_guild_rep matches 1200.. if score @s ar_bosses_done matches 8.. if score @s ar_dragons_done matches 2.. run function ascendant_identity:rank/s_rank
function ascendant_identity:rank_examiner/sync_nameplate
tellraw @s [{"text":"Evaluation complete.","color":"gold"},{"text":" Your public nameplate now reflects the highest rank your proof supports.","color":"gray"}]
execute if score @s ar_guild_rank matches ..0 run tellraw @s [{"text":"Next trial: ","color":"gray"},{"text":"E-Rank","color":"dark_green","bold":true},{"text":" requires 10 Guild reputation.","color":"gray"}]
execute if score @s ar_guild_rank matches 1 run tellraw @s [{"text":"Next trial: ","color":"gray"},{"text":"D-Rank","color":"green","bold":true},{"text":" requires 35 Guild reputation and 10 hunt kills.","color":"gray"}]
execute if score @s ar_guild_rank matches 2 run tellraw @s [{"text":"Next trial: ","color":"gray"},{"text":"C-Rank","color":"aqua","bold":true},{"text":" requires 90 Guild reputation and 35 hunt kills.","color":"gray"}]
execute if score @s ar_guild_rank matches 3 run tellraw @s [{"text":"Next trial: ","color":"gray"},{"text":"B-Rank","color":"blue","bold":true},{"text":" requires 210 Guild reputation and 1 boss proof.","color":"gray"}]
execute if score @s ar_guild_rank matches 4 run tellraw @s [{"text":"Next trial: ","color":"gray"},{"text":"A-Rank","color":"gold","bold":true},{"text":" requires 500 Guild reputation and 4 boss proofs.","color":"gray"}]
execute if score @s ar_guild_rank matches 5 run tellraw @s [{"text":"Next trial: ","color":"gray"},{"text":"S-Rank","color":"dark_purple","bold":true},{"text":" requires 1200 Guild reputation, 8 boss proofs, and 2 dragon proofs.","color":"gray"}]
execute if score @s ar_guild_rank matches 6.. run tellraw @s [{"text":"No higher public rank is currently defined.","color":"dark_purple","bold":true}]
