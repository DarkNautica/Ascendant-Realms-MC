// ============================================================
//  Ascendant Guild UI - right-click NPC menu
//  Primary: MCA-style CustomNPCs CUSTOM GUI PANEL (portrait + info + buttons),
//           built and handled entirely from KubeJS via the CNPCs API.
//  Fallbacks: native dialog window -> clickable chat menu (never regress to nothing).
// ============================================================

const AGUI_S = String.fromCharCode(0xA7)
const AGUI_DLG_RECRUIT = 9001
const AGUI_DLG_MANAGE = 9002
const AGUI_PROF_NAMES = { guild_blacksmith: "Blacksmith", guild_arcanist: "Arcanist", guild_cook: "Cook", guild_healer: "Healer", guild_courier: "Courier" }
const AGUI_TRAIT_NAMES = { master: "Master", gifted: "Gifted", diligent: "Diligent", steady: "Steady", lazy: "Lazy" }

function aguiTagVal(npc, prefix) {
  try { var it = npc.tags.iterator(); while (it.hasNext()) { var t = "" + it.next(); if (t.indexOf(prefix) === 0) return t.substring(prefix.length) } } catch (e) {}
  return null
}
function aguiRun(player, cmd) { try { player.server.runCommandSilent("execute as " + player.username + " run " + cmd) } catch (e) {} }
function aguiClose(player) { try { player.closeMenu() } catch (e) { try { player.closeContainer() } catch (e2) {} } }

// top-level helpers (Rhino does not hoist nested function declarations)
function aguiLbl(gui, id, text, x, y) { try { gui.addLabel(id, text, x, y, 134, 12) } catch (e) {} }
function aguiAddBtn(gui, id, label, x, y, w, h, fn) {
  var b = null
  try { b = gui.addButton(id, label, x, y, w, h) } catch (e) { try { b = gui.addButton(id, label, x, y) } catch (e2) { return null } }
  if (b && fn) { try { b.setOnPress(fn) } catch (e3) {} }
  return b
}

function aguiOpenPanel(player, npc, mode) {
  try {
    var NpcAPIClass = Java.loadClass("noppes.npcs.api.NpcAPI")
    var api = NpcAPIClass.Instance()
    if (!api) return false
    var iplayer = api.getIEntity(player)
    if (!iplayer) return false
    var gui = api.createCustomGui(947, 288, 202, false, iplayer)
    if (!gui) return false

    var prof = aguiTagVal(npc, "ar_profile_") || "guild_blacksmith"
    var trait = aguiTagVal(npc, "ar_trait_") || "steady"
    var profName = AGUI_PROF_NAMES[prof] || "Specialist"
    var traitName = AGUI_TRAIT_NAMES[trait] || "Steady"
    var skill = 0
    try { skill = npc.persistentData.getInt("ar_skill") } catch (e) {}
    var npcTitle = (mode === "recruit") ? "Wandering Specialist" : ((global.agNameFor ? global.agNameFor(npc) : "Member") + " the " + profName)

    var rar = global.agRarity ? global.agRarity(npc) : { name: "Common", color: "f" }
    var perks = global.agPerks ? global.agPerks(npc) : []
    aguiLbl(gui, 0, AGUI_S + "6" + AGUI_S + "lASCENDANT GUILD", 10, 8)
    aguiLbl(gui, 1, AGUI_S + "f" + AGUI_S + "l" + npcTitle, 12, 26)
    aguiLbl(gui, 8, AGUI_S + "7Rarity: " + AGUI_S + rar.color + rar.name, 12, 40)
    aguiLbl(gui, 2, AGUI_S + "7Profession: " + AGUI_S + "e" + profName, 12, 54)
    if (mode !== "recruit") aguiLbl(gui, 4, AGUI_S + "7Level: " + AGUI_S + "a" + (global.agLevel ? global.agLevel(skill) : skill), 12, 68)
    aguiLbl(gui, 9, AGUI_S + "7Perks: " + AGUI_S + "f" + (perks.length ? perks.join(", ") : "none"), 12, 82)

    try {
      var inpc = api.getIEntity(npc)
      var disp = null // portrait disabled until coords are tuned
      try { disp.setScale(30) } catch (e) {}
      try { disp.setRotation(0) } catch (e) {}
      try { disp.setEntitySyncedById(npc.id) } catch (e) {}
    } catch (ed) {}

    var bx = 184, bw = 96, bh = 18, gap = 23
    if (mode === "recruit") {
      var cost = global.agCost ? global.agCost(npc) : 15
      try { gui.addItemRenderer(118, 30, 1, 1, 1, Item.of("kubejs:guild_mark", Math.min(64, cost))) } catch (ir) {}
      aguiAddBtn(gui, 10, "Hire  -  " + cost + " Marks", bx, 30, bw, bh, function () { aguiRun(player, "ascguild recruit"); aguiClose(player) })
      aguiAddBtn(gui, 11, "Guild Roster", bx, 30 + gap, bw, bh, function () { aguiRun(player, "ascguild roster"); aguiClose(player) })
      aguiAddBtn(gui, 19, "Close", bx, 30 + gap * 2, bw, bh, function () { aguiClose(player) })
    } else {
      aguiAddBtn(gui, 12, "Set Workstation", bx, 28, bw, 18, function () { aguiRun(player, "ascjob setworkstation"); aguiClose(player) })
      aguiAddBtn(gui, 22, "Set Recipe", bx, 48, bw, 18, function () { aguiOpenRecipePicker(player, npc) })
      aguiAddBtn(gui, 21, "Bind Storage", bx, 68, bw, 18, function () { aguiRun(player, "ascjob storage"); aguiClose(player) })
      aguiAddBtn(gui, 13, "Workforce Status", bx, 88, bw, 18, function () { aguiRun(player, "ascjob status"); aguiClose(player) })
      aguiAddBtn(gui, 14, "Dismiss", bx, 108, bw, 18, function () { aguiRun(player, "ascguild dismiss"); aguiClose(player) })
      aguiAddBtn(gui, 19, "Close", bx, 128, bw, 18, function () { aguiClose(player) })
      aguiLbl(gui, 5, AGUI_S + "7Reassign profession:", 12, 150)
      var ay = 165, aw = 44, ah = 16
      aguiAddBtn(gui, 15, "Smith", 12, ay, aw, ah, function () { aguiRun(player, "ascjob assign blacksmith"); aguiClose(player) })
      aguiAddBtn(gui, 16, "Arcane", 62, ay, aw, ah, function () { aguiRun(player, "ascjob assign arcanist"); aguiClose(player) })
      aguiAddBtn(gui, 17, "Cook", 112, ay, aw, ah, function () { aguiRun(player, "ascjob assign cook"); aguiClose(player) })
      aguiAddBtn(gui, 18, "Heal", 162, ay, aw, ah, function () { aguiRun(player, "ascjob assign healer"); aguiClose(player) })
      aguiAddBtn(gui, 20, "Courier", 212, ay, aw, ah, function () { aguiRun(player, "ascjob assign courier"); aguiClose(player) })
    }

    iplayer.showCustomGui(gui)
    if (!global.__aguiPanelOk) { global.__aguiPanelOk = true; console.info("[Ascendant Guild UI] MCA-style custom GUI panel shown.") }
    return true
  } catch (e) {
    if (!global.__aguiPanelErr) { global.__aguiPanelErr = true; console.warn("[Ascendant Guild UI] custom GUI panel failed (" + e + "); falling back to dialog/chat.") }
    return false
  }
}

function aguiOpenRecipePicker(player, npc) {
  try {
    var api = Java.loadClass("noppes.npcs.api.NpcAPI").Instance()
    var iplayer = api.getIEntity(player); if (!iplayer) { aguiRun(player, "ascjob status"); return }
    var gui = api.createCustomGui(948, 256, 202, false, iplayer)
    var recipes = global.agRecipes ? global.agRecipes(npc) : []
    var cur = global.agRecipeChoice ? global.agRecipeChoice(npc) : 0
    aguiLbl(gui, 0, AGUI_S + "6" + AGUI_S + "lCHOOSE RECIPE", 10, 8)
    aguiLbl(gui, 1, AGUI_S + "7What should this worker craft?", 12, 24)
    aguiAddBtn(gui, 100, (cur === 0 ? "> " : "") + "Auto (best available)", 12, 42, 220, 18, function () { try { npc.persistentData.putInt("ar_recipe_choice", 0) } catch (e) {} player.tell(Text.green("Recipe set to Auto (best available).")); aguiClose(player) })
    var y = 66
    for (var i = 0; i < recipes.length; i++) {
      (function (rc) {
        aguiAddBtn(gui, 110 + rc.idx, (cur === rc.idx + 1 ? "> " : "") + rc.label + "  (Lv" + rc.min + "+)", 12, y, 220, 18, function () { try { npc.persistentData.putInt("ar_recipe_choice", rc.idx + 1) } catch (e) {} player.tell(Text.green("Recipe set to " + rc.label + ".")); aguiClose(player) })
      })(recipes[i])
      y += 22
    }
    iplayer.showCustomGui(gui)
  } catch (e) { try { player.tell(Text.red("Recipe picker failed: " + e)) } catch (e2) {} }
}

function aguiOpenDialog(player, dialogId, name) {
  try {
    var api = Java.loadClass("noppes.npcs.api.NpcAPI").Instance()
    if (!api) return false
    var ient = api.getIEntity(player); if (!ient) return false
    ient.showDialog(dialogId, name); return true
  } catch (e) { return false }
}

function aguiBtnJson(label, color, cmd, hover) {
  return '{"text":"' + label + '","color":"' + color + '","clickEvent":{"action":"run_command","value":"' + cmd + '"},"hoverEvent":{"action":"show_text","value":"' + hover + '"}}'
}
function aguiTell(player, json) { try { player.server.runCommandSilent("tellraw " + player.username + " " + json) } catch (e) {} }
function aguiRecruitMenu(player) {
  aguiTell(player, '["",{"text":"' + AGUI_S + '6Wandering Specialist' + AGUI_S + '7: ten iron and I join your guild.\\n"},{"text":"   "},' +
    aguiBtnJson("[ Hire - 10 Iron ]", "green", "/ascguild recruit", "Hire me") + ',{"text":"   "},' + aguiBtnJson("[ Roster ]", "yellow", "/ascguild roster", "Your guild") + "]")
}
function aguiManageMenu(player) {
  aguiTell(player, '["",{"text":"' + AGUI_S + 'a[Guild Member]' + AGUI_S + '7: orders?\\n"},{"text":"   "},' +
    aguiBtnJson("[ Set Station ]", "aqua", "/ascjob setstation", "Bind to nearest chest") + ',{"text":" "},' +
    aguiBtnJson("[ Status ]", "gold", "/ascjob status", "Workforce status") + ',{"text":" "},' +
    aguiBtnJson("[ Dismiss ]", "red", "/ascguild dismiss", "Release") + "]")
}

function aguiDedupe(player) {
  if (!global.__aguiLast) global.__aguiLast = {}
  var now = Date.now(), k = "" + player.username
  if (global.__aguiLast[k] && (now - global.__aguiLast[k]) < 350) return false
  global.__aguiLast[k] = now
  return true
}

function aguiOnInteract(event) {
  try {
    var player = event.player, npc = event.target
    if (!player || !npc) return
    var isRecruit = false, isMember = false
    try { isRecruit = npc.tags.contains("ar_recruitable") } catch (e1) {}
    try { isMember = npc.tags.contains("ar_guild_member") } catch (e2) {}
    if (!isRecruit && !isMember) return
    if (!aguiDedupe(player)) { try { event.cancel() } catch (ec0) {} return }
    try { event.cancel() } catch (ec) {}
    var mode = isRecruit ? "recruit" : "manage"
    if (aguiOpenPanel(player, npc, mode)) return
    if (aguiOpenDialog(player, isRecruit ? AGUI_DLG_RECRUIT : AGUI_DLG_MANAGE, isRecruit ? "Wandering Specialist" : "Guild Member")) return
    if (isRecruit) aguiRecruitMenu(player); else aguiManageMenu(player)
  } catch (e) {
    if (!global.__aguiErr) { global.__aguiErr = true; console.warn("[Ascendant Guild UI] handler error: " + e) }
  }
}

try { ItemEvents.entityInteracted(aguiOnInteract); console.info("[Ascendant Guild UI] hooked entityInteracted (panel + dialog + chat)") }
catch (e) { console.warn("[Ascendant Guild UI] entityInteracted unavailable (" + e + ").") }
ServerEvents.loaded((event) => { console.info("[Ascendant Guild UI] loaded - right-click a guild NPC for the panel.") })
