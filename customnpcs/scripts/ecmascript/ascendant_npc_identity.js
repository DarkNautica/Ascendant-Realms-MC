// Ascendant Realms CustomNPCs identity script.
// Safe fallback: CustomNPCs only renders display titles inside close range, so
// the public rank, level, and role are kept in the always-visible name line.

function init(event) {
  arRunIdentity(event);
}

function interact(event) {
  arRunIdentity(event);
  arHandleInteraction(event);
}

function tick(event) {
  // Intentionally empty. Rewriting display data every tick caused noisy script
  // errors on existing NPCs and is not needed after init/interact refreshes.
}

function arRunIdentity(event) {
  if (event == null || event.npc == null) {
    return;
  }

  try {
    if (arIsGuildWorker("" + event.npc.getDisplay().getName())) {
      return; // Ascendant Guild workers own their own nameplates (managed by KubeJS); skip identity rewrite.
    }
    arApplyIdentity(event.npc);
  } catch (error) {
    if (event.player != null) {
      event.player.message("\u00a7cAscendant NPC identity script error: \u00a77" + error);
    }
  }
}

function arApplyIdentity(npc) {
  var display = npc.getDisplay();
  var rawName = "" + display.getName();
  var profile = arResolveProfile(npc, rawName);
  var data = arStoredData(npc);
  var profileChanged = arClean(arDataValue(data, "ar_profile", "")) !== profile.id;

  var storedRank = arDataValue(data, "ar_rank", "");
  var storedLevel = arDataValue(data, "ar_level", "");
  var name = profileChanged ? profile.name : arDataValue(data, "ar_name", profile.name);
  var rank = profileChanged || arShouldUseProfileRank(storedRank, profile.rank) ? profile.rank : storedRank;
  var role = profileChanged ? profile.role : arDataValue(data, "ar_role", profile.role);
  var level = arNormalizeLevel(profileChanged ? profile.level : arDataValue(data, "ar_level", profile.level));
  var color = arRankColor(rank);

  arDataPut(data, "ar_profile", profile.id);
  arDataPut(data, "ar_name", name);
  arDataPut(data, "ar_rank", rank);
  arDataPut(data, "ar_role", role);
  arDataPut(data, "ar_level", level);
  arDataPut(data, "ar_legacy_rank_was", storedRank);
  arDataPut(data, "ar_legacy_level_was", storedLevel);

  display.setShowName(0);
  display.setName(color + "[" + rank + "] \u00a7f" + name + " \u00a78| \u00a77Lv." + level + " " + color + role);
  display.setTitle("");
  npc.updateClient();
}

function arTryRankExaminerEvaluation(event) {
  if (event == null || event.npc == null || event.player == null) {
    return;
  }

  var display = event.npc.getDisplay();
  var profile = arResolveProfile(event.npc, "" + display.getName());
  if (profile.id !== "rank_examiner") {
    return;
  }

  var playerName = arCommandSafePlayerName(event.player);
  if (playerName === "") {
    event.npc.sayTo(event.player, "\u00a76Rank Examiner\u00a77: I cannot read your Guild record yet.");
    return;
  }

  var command = "execute as " + playerName + " run function ascendant_identity:rank_examiner/evaluate";
  if (arTryNpcCommand(event, command)) {
    return;
  }

  event.npc.sayTo(event.player, "\u00a76Rank Examiner\u00a77: The Guild ledger is unavailable. Tell Jayden the Rank Examiner bridge did not execute.");
}

function arHandleInteraction(event) {
  if (event == null || event.npc == null || event.player == null) {
    return;
  }

  var display = event.npc.getDisplay();
  var guildName = "" + display.getName();
  if (arIsGuildWorker(guildName)) {
    arGuildMenu(event, guildName);
    return;
  }
  var profile = arResolveProfile(event.npc, "" + display.getName());
  var relation = arRecordInteraction(event, profile);

  if (profile.id === "rank_examiner") {
    arTryRankExaminerEvaluation(event);
    return;
  }

  arSayRoleLine(event, profile, relation);
}

function arRecordInteraction(event, profile) {
  var data = arStoredData(event.npc);
  var playerKey = arClean(arCommandSafePlayerName(event.player));
  if (playerKey === "") {
    playerKey = "unknown";
  }
  var profileKey = arClean(profile.id);
  var countKey = "ar_rel_" + playerKey + "_" + profileKey + "_talks";
  var scoreKey = "ar_rel_" + playerKey + "_" + profileKey + "_trust";
  var count = arIntDataValue(data, countKey, 0) + 1;
  var score = arIntDataValue(data, scoreKey, 0);
  if (count <= 1) {
    score += profile.trustOnFirstMeet;
  } else {
    score += profile.trustPerTalk;
  }
  if (score > 100) {
    score = 100;
  }
  arDataPut(data, countKey, "" + count);
  arDataPut(data, scoreKey, "" + score);
  arDataPut(data, "ar_last_player", playerKey);
  arDataPut(data, "ar_last_relation_tier", arRelationTier(score, count));
  return {
    playerKey: playerKey,
    interactions: count,
    trust: score,
    tier: arRelationTier(score, count)
  };
}

function arSayRoleLine(event, profile, relation) {
  var prefix = arRankColor(profile.rank) + profile.name + "\u00a77: ";
  if (profile.canFollow || profile.canTakeOrders) {
    event.npc.sayTo(event.player, prefix + profile.line);
    return;
  }
  if (relation.tier === "stranger") {
    event.npc.sayTo(event.player, prefix + profile.line + " \u00a78(Relation: stranger. I do not take orders from strangers.)");
    return;
  }
  if (relation.tier === "familiar") {
    event.npc.sayTo(event.player, prefix + profile.familiarLine + " \u00a78(Relation: familiar, not a follower.)");
    return;
  }
  event.npc.sayTo(event.player, prefix + profile.trustedLine + " \u00a78(Relation: trusted contact. Companion orders are still locked.)");
}

function arRelationTier(score, interactions) {
  if (score >= 60 || interactions >= 5) {
    return "trusted";
  }
  if (score >= 25 || interactions >= 2) {
    return "familiar";
  }
  return "stranger";
}

function arIntDataValue(data, key, fallback) {
  var text = arDataValue(data, key, "" + fallback);
  var value = parseInt(text, 10);
  if (isNaN(value)) {
    return fallback;
  }
  return value;
}

function arTryNpcCommand(event, command) {
  try {
    if (event.npc.executeCommand != null) {
      event.npc.executeCommand(command);
      return true;
    }
  } catch (error) {
  }
  try {
    if (event.API != null && event.API.executeCommand != null) {
      event.API.executeCommand(event.npc.getWorld(), command);
      return true;
    }
  } catch (error) {
  }
  try {
    if (API != null && API.executeCommand != null) {
      API.executeCommand(event.npc.getWorld(), command);
      return true;
    }
  } catch (error) {
  }
  return false;
}

function arCommandSafePlayerName(player) {
  var name = "";
  try {
    name = "" + player.getName();
  } catch (error) {
  }
  if (name === "" || name === "undefined" || name === "null") {
    try {
      name = "" + player.getDisplayName();
    } catch (error2) {
    }
  }

  var clean = "";
  for (var index = 0; index < name.length; index++) {
    var character = name.charAt(index);
    if (
      (character >= "a" && character <= "z") ||
      (character >= "A" && character <= "Z") ||
      (character >= "0" && character <= "9") ||
      character === "_"
    ) {
      clean += character;
    }
  }
  return clean;
}

function arResolveProfile(npc, rawName) {
  var data = arStoredData(npc);
  var storedProfile = arClean(arDataValue(data, "ar_profile", ""));
  var key = arClean(rawName);

  if (arKnownProfileKey(key)) {
    return arProfileByKey(key);
  }

  if (storedProfile !== "") {
    var profileFromData = arProfileByKey(storedProfile);
    if (profileFromData.id !== "guild_clerk" || arContains(storedProfile, "guild_clerk")) {
      return profileFromData;
    }
  }

  return arProfileByKey(key);
}

function arKnownProfileKey(key) {
  return arContains(key, "guild_clerk") || arContains(key, "guildclerk") ||
    arContains(key, "rank_examiner") || arContains(key, "rankexaminer") ||
    arContains(key, "bounty_master") || arContains(key, "bountymaster") ||
    arContains(key, "guild_arcanist") || arContains(key, "guildarcanist") ||
    arContains(key, "hunter_quartermaster") || arContains(key, "hunterquartermaster") ||
    arContains(key, "guard_captain") || arContains(key, "guardcaptain") ||
    arContains(key, "tavern_keeper") || arContains(key, "tavernkeeper") ||
    arContains(key, "village_elder") || arContains(key, "villageelder") ||
    arContains(key, "wounded_hunter") || arContains(key, "woundedhunter") ||
    arContains(key, "mira_ash") || arContains(key, "miraash") ||
    arContains(key, "darius_crowe") || arContains(key, "dariuscrowe") ||
    arContains(key, "seren_valehart") || arContains(key, "serenvalehart") ||
    arContains(key, "kael_vorn") || arContains(key, "kaelvorn") ||
    arContains(key, "black_hound") || arContains(key, "blackhound");
}

function arProfileByKey(key) {
  if (arContains(key, "rank_examiner") || arContains(key, "rankexaminer")) {
    return arProfile("rank_examiner", "Rank Examiner", "B-Rank", "Examiner", "52", "Bring proof and I will read the ledger.", "Your record is getting clearer.", "The Guild recognizes your work.", "public_authority", 10, 3, false, false);
  }
  if (arContains(key, "bounty_master") || arContains(key, "bountymaster")) {
    return arProfile("bounty_master", "Bounty Master", "C-Rank", "Contracts", "38", "The board is public. Private work is earned.", "Finish clean contracts and I will remember you.", "I can point you toward harder work, not follow your orders.", "contract_broker", 5, 4, false, false);
  }
  if (arContains(key, "guild_arcanist") || arContains(key, "guildarcanist")) {
    return arProfile("guild_arcanist", "Guild Arcanist", "B-Rank", "Arcanist", "49", "Magic leaves evidence. Bring me something worth reading.", "Your spellwork is becoming less reckless.", "I will advise your path, not serve as field artillery.", "expert_advisor", 4, 4, false, false);
  }
  if (arContains(key, "hunter_quartermaster") || arContains(key, "hunterquartermaster") || arContains(key, "quartermaster")) {
    return arProfile("hunter_quartermaster", "Quartermaster", "D-Rank", "Supplies", "24", "Guild supplies are issued by rank and need, not charm.", "I can set aside basics once your marks are in order.", "You have credit here. Do not waste it.", "supplier", 8, 5, false, false);
  }
  if (arContains(key, "guard_captain") || arContains(key, "guardcaptain")) {
    return arProfile("guard_captain", "Guard Captain", "C-Rank", "Captain", "36", "I command the watch. Outsiders do not command me.", "Help the village and my people will notice.", "You have my respect. My post still comes first.", "settlement_guard", 3, 3, false, false);
  }
  if (arContains(key, "tavern_keeper") || arContains(key, "tavernkeeper")) {
    return arProfile("tavern_keeper", "Tavern Keeper", "D-Rank", "Rumors", "16", "Buy a meal, hear a rumor. That is the trade.", "You listen better than most hunters.", "I will pass you names before they reach the board.", "rumor_source", 8, 6, false, false);
  }
  if (arContains(key, "village_elder") || arContains(key, "villageelder")) {
    return arProfile("village_elder", "Village Elder", "D-Rank", "Elder", "22", "Trust is built by keeping villages alive.", "The children know your name now.", "You have helped us enough that I will speak plainly.", "settlement_elder", 10, 6, false, false);
  }
  if (arContains(key, "wounded_hunter") || arContains(key, "woundedhunter")) {
    return arProfile("wounded_hunter", "Wounded Hunter", "C-Rank", "Hunter", "31", "Do not mistake a warning for a recruitment offer.", "You came back. That counts.", "I can share what mauled me, but I am not marching yet.", "field_contact", 6, 5, false, false);
  }
  if (arContains(key, "mira_ash") || arContains(key, "miraash") || arContains(key, "mira")) {
    return arProfile("mira_ash", "Mira Ash", "C-Rank", "Scout", "34", "I do not scout for strangers.", "You move quietly enough to talk to.", "I may share a route. Do not call it friendship yet.", "rival_hunter", 2, 5, false, false);
  }
  if (arContains(key, "darius_crowe") || arContains(key, "dariuscrowe")) {
    return arProfile("darius_crowe", "Darius Crowe", "B-Rank", "Duelist", "47", "Win something before giving orders.", "You are at least entertaining.", "If we fight together, it is because the target earned it.", "rival_hunter", 0, 4, false, false);
  }
  if (arContains(key, "seren_valehart") || arContains(key, "serenvalehart")) {
    return arProfile("seren_valehart", "Seren Valehart", "B-Rank", "Arcanist", "45", "Your aura is loud. Your authority is not.", "You survived contact with worse things than gossip.", "I can compare notes. I do not take assignments from you.", "rival_hunter", 0, 4, false, false);
  }
  if (arContains(key, "kael_vorn") || arContains(key, "kaelvorn")) {
    return arProfile("kael_vorn", "Kael Vorn", "A-Rank", "Monster Hunter", "68", "Do not confuse proximity with command.", "You have survived long enough to be useful.", "When I move, it is for the hunt, not your convenience.", "elite_hunter", 0, 3, false, false);
  }
  if (arContains(key, "black_hound") || arContains(key, "blackhound")) {
    return arProfile("black_hound", "The Black Hound", "S-Rank", "Unknown", "90", "No.", "You are still alive. Interesting.", "Do not ask twice.", "mythic_hunter", 0, 1, false, false);
  }

  return arProfile("guild_clerk", "Guild Clerk", "D-Rank", "Clerk", "18", "Contracts are on the board. Orders are not.", "Your name is appearing in the ledger.", "I can explain Guild business. I cannot fight your battles.", "guild_staff", 8, 5, false, false);
}

function arProfile(id, name, rank, role, level, line, familiarLine, trustedLine, relationshipGate, trustOnFirstMeet, trustPerTalk, canFollow, canTakeOrders) {
  return {
    id: id,
    name: name,
    rank: rank,
    role: role,
    level: level,
    line: line,
    familiarLine: familiarLine,
    trustedLine: trustedLine,
    relationshipGate: relationshipGate,
    trustOnFirstMeet: trustOnFirstMeet,
    trustPerTalk: trustPerTalk,
    canFollow: canFollow === true,
    canTakeOrders: canTakeOrders === true
  };
}

function arRankColor(rank) {
  if (rank === "S-Rank") {
    return "\u00a7d";
  }
  if (rank === "A-Rank") {
    return "\u00a7e";
  }
  if (rank === "B-Rank") {
    return "\u00a76";
  }
  if (rank === "C-Rank") {
    return "\u00a79";
  }
  if (rank === "D-Rank") {
    return "\u00a7a";
  }
  if (rank === "E-Rank") {
    return "\u00a72";
  }
  return "\u00a77";
}

function arIsPublicRank(rank) {
  return rank === "S-Rank" || rank === "A-Rank" || rank === "B-Rank" ||
    rank === "C-Rank" || rank === "D-Rank" || rank === "E-Rank" ||
    rank === "Unranked";
}

function arShouldUseProfileRank(storedRank, profileRank) {
  if (!arIsPublicRank(storedRank)) {
    return true;
  }
  if (storedRank === "Unranked" && profileRank !== "Unranked") {
    return true;
  }
  return false;
}

function arNormalizeLevel(level) {
  var text = "" + level;
  var dot = text.indexOf(".");
  if (dot > 0) {
    text = text.substring(0, dot);
  }
  if (text === "" || text === "NaN" || text === "undefined" || text === "null") {
    return "1";
  }
  return text;
}

function arStoredData(npc) {
  try {
    return npc.getStoreddata();
  } catch (error) {
    return null;
  }
}

function arDataValue(data, key, fallback) {
  try {
    if (data != null && data.has(key)) {
      var value = data.get(key);
      if (value != null && ("" + value) !== "") {
        return "" + value;
      }
    }
  } catch (error) {
  }
  return "" + fallback;
}

function arDataPut(data, key, value) {
  try {
    if (data != null) {
      data.put(key, "" + value);
    }
  } catch (error) {
  }
}

function arClean(value) {
  var text = arStripFormatting("" + value).toLowerCase();
  text = arReplaceAll(text, "ar:", "");
  text = arReplaceAll(text, "\\r", "_");
  text = arReplaceAll(text, "\\n", "_");
  text = arReplaceAll(text, "\r", "_");
  text = arReplaceAll(text, "\n", "_");
  text = arReplaceAll(text, " ", "_");
  text = arReplaceAll(text, "-", "_");
  text = arReplaceAll(text, "[", "");
  text = arReplaceAll(text, "]", "");
  text = arReplaceAll(text, "|", "_");
  text = arReplaceAll(text, ".", "");
  return text;
}

function arStripFormatting(value) {
  var text = "" + value;
  var clean = "";
  var skip = false;
  for (var index = 0; index < text.length; index++) {
    var character = text.charAt(index);
    if (skip) {
      skip = false;
      continue;
    }
    if (character === "\u00a7") {
      skip = true;
      continue;
    }
    clean += character;
  }
  return clean;
}

function arContains(text, piece) {
  return text.indexOf(piece) >= 0;
}

function arReplaceAll(text, from, to) {
  while (text.indexOf(from) >= 0) {
    text = text.replace(from, to);
  }
  return text;
}

// ============================================================
//  Ascendant Guild interaction menus (right-click -> clickable menu)
//  Detection is by display name ([Recruit] / [Guild]) which KubeJS controls,
//  so this never fights the social-NPC identity system above. Each button is a
//  tellraw run_command, so clicking runs the matching /ascguild or /ascjob command
//  as the player - no typing. The KubeJS engine does the actual work.
// ============================================================
function arIsGuildWorker(rawName) {
  return arContains(rawName, "[Recruit]") || arContains(rawName, "[Guild]");
}

function arGuildMenu(event, rawName) {
  if (arContains(rawName, "[Recruit]")) {
    arRecruitMenu(event);
    return;
  }
  arManageMenu(event);
}

function arGuildButton(label, color, command, hover) {
  return '{"text":"' + label + '","color":"' + color +
    '","clickEvent":{"action":"run_command","value":"' + command +
    '"},"hoverEvent":{"action":"show_text","value":"' + hover + '"}}';
}

function arRecruitMenu(event) {
  var pname = arCommandSafePlayerName(event.player);
  if (pname === "") {
    event.npc.sayTo(event.player, "§cI cannot read your Guild record.");
    return;
  }
  event.npc.sayTo(event.player, "§6Wandering Specialist§7: Skilled hands for hire - ten iron and I join your guild.");
  var menu = '["",{"text":"   "},' +
    arGuildButton("[ Hire - 10 Iron ]", "green", "/ascguild recruit", "Pay 10 Iron Ingot to hire me into your guild") +
    ',{"text":"    "},' +
    arGuildButton("[ Roster ]", "yellow", "/ascguild roster", "See who is in your guild") +
    "]";
  arTryNpcCommand(event, "tellraw " + pname + " " + menu);
}

function arManageMenu(event) {
  var pname = arCommandSafePlayerName(event.player);
  if (pname === "") {
    event.npc.sayTo(event.player, "§cI cannot read your Guild record.");
    return;
  }
  if (!arOwnsThis(event.npc, pname)) {
    event.npc.sayTo(event.player, "§a[Guild]§7: I answer to another guild.");
    return;
  }
  event.npc.sayTo(event.player, "§a[Guild Member]§7: Your orders?");
  var row1 = '["",{"text":"   "},' +
    arGuildButton("[ Set Station ]", "aqua", "/ascjob setstation", "Bind me to the nearest chest as my workstation") +
    ',{"text":" "},' +
    arGuildButton("[ Status ]", "gold", "/ascjob status", "Show what your workforce is doing") +
    ',{"text":" "},' +
    arGuildButton("[ Dismiss ]", "red", "/ascguild dismiss", "Release the nearest guild member") +
    "]";
  arTryNpcCommand(event, "tellraw " + pname + " " + row1);
  var row2 = '["",{"text":"   Assign: ","color":"gray"},' +
    arGuildButton("[Smith]", "gold", "/ascjob assign blacksmith", "Reassign to Blacksmith") +
    ',{"text":" "},' +
    arGuildButton("[Arcanist]", "light_purple", "/ascjob assign arcanist", "Reassign to Arcanist") +
    ',{"text":" "},' +
    arGuildButton("[Cook]", "yellow", "/ascjob assign cook", "Reassign to Cook") +
    ',{"text":" "},' +
    arGuildButton("[Healer]", "green", "/ascjob assign healer", "Reassign to Healer") +
    ',{"text":" "},' +
    arGuildButton("[Courier]", "aqua", "/ascjob assign courier", "Reassign to Courier") +
    "]";
  arTryNpcCommand(event, "tellraw " + pname + " " + row2);
}

function arOwnsThis(npc, pname) {
  try {
    var ent = npc.getMCEntity();
    if (ent != null && ent.getTags != null) {
      var tags = ent.getTags();
      var iterator = tags.iterator();
      var hasOwner = false;
      var mine = false;
      while (iterator.hasNext()) {
        var tag = "" + iterator.next();
        if (tag.indexOf("ar_owner_") === 0) {
          hasOwner = true;
          if (tag === "ar_owner_" + pname) {
            mine = true;
          }
        }
      }
      if (hasOwner) {
        return mine;
      }
    }
  } catch (error) {
  }
  return true;
}
