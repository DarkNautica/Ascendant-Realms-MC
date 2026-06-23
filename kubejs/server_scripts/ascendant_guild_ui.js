// ============================================================
//  Ascendant Guild UI - right-click NPC menu
//  Primary: MCA-style CustomNPCs CUSTOM GUI PANEL (portrait + info + buttons),
//           built and handled entirely from KubeJS via the CNPCs API.
//  Fallbacks: native dialog window -> clickable chat menu (never regress to nothing).
//  Trigger: KubeJS entityInteracted (independent of CNPCs script attachment).
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
function aguiRun(player, cmd) {
  try { player.server.runCommandSilent("execute as " + player.username + " run " + cmd) } catch (e) {}
}
function aguiClose(player) {
  try { player.closeMenu() } catch (e) { try { player.closeContainer() } catch (e2) {} }
}

// ---- the MCA-style custom GUI panel ----
function aguiOpenPanel(player, npc, mode) {
  try {
    var NpcAPIClass = Java.loadClass("noppes.npcs.api.NpcAPI")
    var api = NpcAPIClass.Instance()
    if (!api) return false
    var iplayer = api.getIEntity(player)
    if (!iplayer) return false
    var W = 256, H = 200
    var gui = api.createCustomGui(947, W, H, false, iplayer)
    if (!gui) return false

    var prof = aguiTagVal(npc, "ar_profile_") || "guild_blacksmith"
    var trait = aguiTagVal(npc, "ar_trait_") || "steady"
    var profName = AGUI_PROF_NAMES[prof] || "Specialist"
    var traitName = AGUI_TRAIT_NAMES[trait] || "Steady"
    var skill = 0
    try { skill = npc.persistentData.getInt("ar_skill") } catch (e) {}
    var npcTitle = (mode === "recruit") ? "Wandering Specialist" : profName

    function addBtn(id, label, x, y, w, h, fn) {
      var b
      try { b = gui.addButton(id, label, x, y, w, h) } catch (e) { try { b = gui.addButton(id, label, x, y) } catch (e2) { return null } }
      if (b && fn) { try { b.setOnPress(fn) } catch (e3) {} }
      return b
    }
    function lbl(id, text, x, y) { try { gui.addLabel(id, text, x, y, 132, 12) } catch (e) {} }

    // header + info panel (left)
    lbl(0, AGUI_S + "6" + AGUI_S + "lASCENDANT GUILD", 10, 8)
    lbl(1, AGUI_S + "f" + AGUI_S + "l" + npcTitle, 12, 28)
    lbl(2, AGUI_S + "7Profession: " + AGUI_S + "e" + profName, 12, 44)
    lbl(3, AGUI_S + "7Trait: " + AGUI_S + "b" + traitName, 12, 58)
    if (mode !== "recruit") lbl(4, AGUI_S + "7Level: " + AGUI_S + "a" + skill, 12, 72)

    // NPC portrait
    try {
      var inpc = api.getIEntity(npc)
      var disp = gui.addEntityDisplay(60, 168, 46, inpc)
      try { disp.setEntitySyncedById(npc.id) } catch (e) {}
      try { disp.setRotation(0) } catch (e) {}
    } catch (ed) {}

    var bx = 150, bw = 96, bh = 18, gap = 23
    if (mode === "recruit") {
      try { gui.addItemRenderer(118, 30, 1, 1, 1, Item.of("minecraft:iron_ingot", 10)) } catch (ir) {}
      addBtn(10, "Hire  -  10 Iron", bx, 30, bw, bh, function () { aguiRun(player, "ascguild recruit"); aguiClose(player) })
      addBtn(11, "Guild Roster", bx, 30 + gap, bw, bh, function () { aguiRun(player, "ascguild roster"); aguiClose(player) })
      addBtn(19, "Close", bx, 30 + gap * 2, bw, bh, function () { aguiClose(player) })
    } else {
      addBtn(12, "Set Station", bx, 30, bw, bh, function () { aguiRun(player, "ascjob setstation"); aguiClose(player) })
      addBtn(13, "Workforce Status", bx, 30 + gap, bw, bh, function () { aguiRun(player, "ascjob status"); aguiClose(player) })
      addBtn(14, "Dismiss", bx, 30 + gap * 2, bw, bh, function () { aguiRun(player, "ascguild dismiss"); aguiClose(player) })
      lbl(5, AGUI_S + "7Reassign profession:", 12, 150)
      var ay = 164, aw = 44, ah = 16
      addBtn(15, "Smith", 12, ay, aw, ah, function () { aguiRun(player, "ascjob assign blacksmith"); aguiClose(player) })
      addBtn(16, "Arcane", 12 + 48, ay, aw, ah, function () { aguiRun(player, "ascjob assign arcanist"); aguiClose(player) })
      addBtn(17, "Cook", 12 + 96, ay, aw, ah, function () { aguiRun(player, "ascjob assign cook"); aguiClose(player) })
      addBtn(18, "Heal", 12 + 144, ay, aw, ah, function () { aguiRun(player, "ascjob assign healer"); aguiClose(player) })
      addBtn(20, "Courier", 12 + 192, ay, aw, ah, function () { aguiRun(player, "ascjob assign courier"); aguiClose(player) })
      addBtn(19, "Close", bx, 30 + gap * 3, bw, bh, function () { aguiClose(player) })
    }

    iplayer.showCustomGui(gui)
    if (!global.__aguiPanelOk) { global.__aguiPanelOk = true; console.info("[Ascendant Guild UI] MCA-style custom GUI panel shown.") }
    return true
  } catch (e) {
    if (!global.__aguiPanelErr) { global.__aguiPanelErr = true; console.warn("[Ascendant Guild UI] custom GUI panel failed (" + e + "); falling back to dialog/chat.") }
    return false
  }
}

// ---- fallback 1: native dialog window ----
function aguiOpenDialog(player, dialogId, name) {
  try {
    var NpcAPIClass = Java.loadClass("noppes.npcs.api.NpcAPI")
    var api = NpcAPIClass.Instance()
    if (!api) return false
    var ient = api.getIEntity(player)
    if (!ient) return false
    ient.showDialog(dialogId, name)
    return true
  } catch (e) { return false }
}

// ---- fallback 2: clickable chat menu ----
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
    var tags = npc.tags
    var isRecruit = false, isMember = false
    try { isRecruit = tags.contains("ar_recruitable") } catch (e1) {}
    try { isMember = tags.contains("ar_guild_member") } catch (e2) {}
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

try {
  ItemEvents.entityInteracted(aguiOnInteract)
  console.info("[Ascendant Guild UI] hooked entityInteracted (custom GUI panel + dialog + chat fallbacks)")
} catch (e) {
  console.warn("[Ascendant Guild UI] entityInteracted unavailable (" + e + ").")
}
ServerEvents.loaded((event) => { console.info("[Ascendant Guild UI] loaded - right-click a [Recruit]/[Guild] NPC for the panel.") })
