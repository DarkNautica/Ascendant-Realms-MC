# Visible player identity and Ascendant progression scoreboard for local multiplayer testing.
scoreboard objectives add ar_level level {"text":"Lv","color":"aqua"}
scoreboard objectives add ar_level_last dummy {"text":"Last Lv","color":"gray"}
scoreboard objectives add ar_skill_level dummy {"text":"Ascendant Lv","color":"aqua"}
scoreboard objectives add ar_skill_xp dummy {"text":"Ascendant XP","color":"dark_aqua"}
scoreboard objectives add ar_skill_xp_req dummy {"text":"XP Needed","color":"gray"}
scoreboard objectives add ar_skill_sp dummy {"text":"Skill Points","color":"gold"}
scoreboard objectives add ar_skill_spent dummy {"text":"Spent SP","color":"yellow"}
scoreboard objectives add ar_skill_total dummy {"text":"Total SP","color":"yellow"}
scoreboard objectives add ar_guild_rep dummy {"text":"Guild Rep","color":"gold"}
scoreboard objectives add ar_guild_rank dummy {"text":"Guild Rank","color":"gold"}
scoreboard objectives add ar_bounties_done dummy {"text":"Bounties","color":"yellow"}
scoreboard objectives add ar_structures_done dummy {"text":"Structures","color":"aqua"}
scoreboard objectives add ar_bosses_done dummy {"text":"Bosses","color":"red"}
scoreboard objectives add ar_dragons_done dummy {"text":"Dragons","color":"dark_purple"}
scoreboard objectives add ar_region_tier dummy {"text":"Region Tier","color":"dark_aqua"}
scoreboard objectives add ar_threat_tier dummy {"text":"Threat Tier","color":"dark_red"}
scoreboard objectives add ar_hunt_kills dummy {"text":"Hunt Kills","color":"green"}
scoreboard objectives add ar_elite_kills dummy {"text":"Elite Kills","color":"dark_purple"}
scoreboard objectives add ar_core_state dummy {"text":"AR Core","color":"gray"}
scoreboard objectives setdisplay belowName ar_skill_level
team add ar_ascendant {"text":"Ascendant","color":"aqua"}
team modify ar_ascendant prefix [{"text":"[","color":"dark_aqua"},{"text":"Ascendant","color":"aqua"},{"text":"] ","color":"dark_aqua"}]
team modify ar_ascendant color aqua
team modify ar_ascendant nametagVisibility always
team add ar_rank_unranked {"text":"Unranked","color":"gray"}
team modify ar_rank_unranked prefix [{"text":"[","color":"dark_gray"},{"text":"Unranked","color":"gray"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_unranked color gray
team modify ar_rank_unranked nametagVisibility always
team add ar_rank_e {"text":"E-Rank","color":"dark_green"}
team modify ar_rank_e prefix [{"text":"[","color":"dark_gray"},{"text":"E-Rank","color":"dark_green"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_e color dark_green
team modify ar_rank_e nametagVisibility always
team add ar_rank_d {"text":"D-Rank","color":"green"}
team modify ar_rank_d prefix [{"text":"[","color":"dark_gray"},{"text":"D-Rank","color":"green"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_d color green
team modify ar_rank_d nametagVisibility always
team add ar_rank_c {"text":"C-Rank","color":"aqua"}
team modify ar_rank_c prefix [{"text":"[","color":"dark_gray"},{"text":"C-Rank","color":"aqua"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_c color aqua
team modify ar_rank_c nametagVisibility always
team add ar_rank_b {"text":"B-Rank","color":"blue"}
team modify ar_rank_b prefix [{"text":"[","color":"dark_gray"},{"text":"B-Rank","color":"blue"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_b color blue
team modify ar_rank_b nametagVisibility always
team add ar_rank_a {"text":"A-Rank","color":"gold"}
team modify ar_rank_a prefix [{"text":"[","color":"dark_gray"},{"text":"A-Rank","color":"gold"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_a color gold
team modify ar_rank_a nametagVisibility always
team add ar_rank_s {"text":"S-Rank","color":"dark_purple"}
team modify ar_rank_s prefix [{"text":"[","color":"dark_gray"},{"text":"S-Rank","color":"dark_purple"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_s color dark_purple
team modify ar_rank_s nametagVisibility always
