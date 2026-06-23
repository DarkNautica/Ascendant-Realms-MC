scoreboard players set @s ar_guild_rep 0
scoreboard players set @s ar_guild_rank 0
scoreboard players set @s ar_bounties_done 0
scoreboard players set @s ar_structures_done 0
scoreboard players set @s ar_bosses_done 0
scoreboard players set @s ar_dragons_done 0
scoreboard players set @s ar_hunt_kills 0
scoreboard players set @s ar_elite_kills 0
scoreboard players set @s ar_threat_tier 0
team leave @s
team join ar_rank_unranked @s
tellraw @s {"text":"Ascendant debug counters reset for this player.","color":"gray"}
function ascendant_core:status
