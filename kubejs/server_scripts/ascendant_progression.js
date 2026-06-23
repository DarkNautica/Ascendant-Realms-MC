// Ascendant Realms unified player HUD + skill-point bridge.
// Puffish Skills owns XP/level/points; Iron's Spells owns mana (MagicData).
// HUD is drawn with the KubeJS Painter API. Bars are drawn as rectangles (Painter's
// dynamic texture-fill path is unreliable); the level badge + skill gem are static
// textures; all text is the native Minecraft font at scale 1.

const AscendantSkillsAPI = Java.loadClass("net.puffish.skillsmod.api.SkillsAPI")
const AscendantResourceLocation = Java.loadClass("net.minecraft.resources.ResourceLocation")
const AscendantProgressionJsonIO = typeof JsonIO !== "undefined"
  ? JsonIO : Java.loadClass("dev.latvian.mods.kubejs.util.JsonIO")

let IronMagicData = null, IronAttributeRegistry = null, ascendantManaWarned = false
function loadIronManaClasses() {
  if (IronMagicData === null) { try { IronMagicData = Java.loadClass("io.redspace.ironsspellbooks.api.magic.MagicData") } catch (e) { IronMagicData = false } }
  if (IronAttributeRegistry === null) { try { IronAttributeRegistry = Java.loadClass("io.redspace.ironsspellbooks.api.registry.AttributeRegistry") } catch (e) { IronAttributeRegistry = false } }
}
function getAscendantMana(player) {
  loadIronManaClasses()
  if (!IronMagicData) return null
  try {
    var md = IronMagicData.getPlayerMagicData(player)
    if (!md) return null
    var mana = Number(md.getMana())
    var maxMana = 0
    try { maxMana = Number(md.getMaxMana()) } catch (e1) {
      try { maxMana = Number(player.getAttributeValue(IronAttributeRegistry.MAX_MANA.get())) } catch (e2) { maxMana = 0 }
    }
    if (maxMana > 0) return { mana: mana, maxMana: maxMana, frac: Math.max(0, Math.min(1, mana / maxMana)) }
  } catch (error) {
    if (!ascendantManaWarned) { console.warn(`[Ascendant Progression] Mana read failed once; hiding mana bar: ${error}`); ascendantManaWarned = true }
  }
  return null
}

const ASCENDANT_PROGRESSION_CONFIG_PATH = "config/ascendant_progression/progression.json"
const ASCENDANT_PROGRESSION_LAST_LEVEL = "ar_progression_last_display_level"
const ASCENDANT_PROGRESSION_MANAGED_BONUS = "ar_progression_managed_bonus_points"
const ASCENDANT_HUD_TEX = "ascendant:textures/gui/hud/"

const ASCENDANT_PROGRESSION_DEFAULTS = {
  enabled: true,
  category_ids: ["puffish_skills:ascendant", "minecraft:ascendant", "ascendant"],
  display_level_offset: 1, display_level_cap: 120, sync_interval_ticks: 5,
  managed_bonus_points: { enabled: true, milestones: [
    { level: 10, points: 1 }, { level: 20, points: 1 }, { level: 35, points: 1 },
    { level: 50, points: 1 }, { level: 70, points: 1 }, { level: 90, points: 1 }, { level: 110, points: 1 } ] },
  scoreboard: { enabled: true, level_objective: "ar_skill_level", xp_objective: "ar_skill_xp",
    xp_required_objective: "ar_skill_xp_req", points_left_objective: "ar_skill_sp",
    points_spent_objective: "ar_skill_spent", points_total_objective: "ar_skill_total" },
  hud: { enabled: true, style: "vanilla_blue_segments", draw_mode: "ingame", hide_in_creative: true, hide_in_spectator: true,
    mana_enabled: true, show_values: true, x: "25", y: "$screenH - 13",
    track_x: "25", track_y: "$screenH - 13", fill_x: "25", fill_y: "$screenH - 13",
    level_text_y: "$screenH - 66", xp_text_y: "$screenH - 66", width: 182, height: 3, fill_height: 3, segment_count: 20,
    track_color: "#66002133", track_border_color: "#CC001C2E", segment_track_color: "#553E5B7A",
    segment_fill_color: "#FF43B7FF", segment_pulse_color: "#FFFFFFFF",
    level_text_color: "#FFC8E8FF", sp_text_color: "#FFB6E6FF", value_text_color: "#FFCFEFFF" },
  level_up: { enabled: true, title_text: "Level Up!", subtitle_text: "Ascendant Web",
    banner_ticks: 70, xp_pulse_ticks: 35, sound: "minecraft:ui.toast.challenge_complete", volume: 0.85, pitch: 1.15 }
}

let ascendantProgressionConfig = readAscendantProgressionConfig()
let ascendantProgressionCategory = null
let ascendantProgressionState = {}
let ascendantProgressionWarnedMissingCategory = false

function isObject(v) { return v !== null && typeof v === "object" && !Array.isArray(v) }
function mergeObjects(base, override) {
  var result = {}
  Object.keys(base || {}).forEach((k) => { result[k] = isObject(base[k]) ? mergeObjects(base[k], {}) : base[k] })
  Object.keys(override || {}).forEach((k) => { result[k] = isObject(override[k]) && isObject(result[k]) ? mergeObjects(result[k], override[k]) : override[k] })
  return result
}
function readAscendantProgressionConfig() {
  try {
    var rel = String(ASCENDANT_PROGRESSION_CONFIG_PATH).replace(/\\/g, "/").replace(/^config\//, "")
    var parsed = AscendantProgressionJsonIO.read(`config/${rel}`)
    if (parsed === null || parsed === undefined) return ASCENDANT_PROGRESSION_DEFAULTS
    return mergeObjects(ASCENDANT_PROGRESSION_DEFAULTS, parsed)
  } catch (error) { console.warn(`[Ascendant Progression] config read failed: ${error}`); return ASCENDANT_PROGRESSION_DEFAULTS }
}
function toAscendantResourceLocation(id) {
  var v = String(id)
  return v.indexOf(":") >= 0 ? new AscendantResourceLocation(v) : new AscendantResourceLocation("puffish_skills", v)
}
function getAscendantCategory() {
  if (ascendantProgressionCategory !== null) return ascendantProgressionCategory
  var ids = ascendantProgressionConfig.category_ids || []
  for (var i = 0; i < ids.length; i++) {
    try { var r = AscendantSkillsAPI.getCategory(toAscendantResourceLocation(ids[i]))
      if (r.isPresent()) { ascendantProgressionCategory = r.get(); return ascendantProgressionCategory } } catch (e) {}
  }
  try {
    var cats = AscendantSkillsAPI.streamCategories().toArray()
    for (var j = 0; j < cats.length; j++) {
      var id = String(cats[j].getId())
      if (id === "ascendant" || id.endsWith(":ascendant")) { ascendantProgressionCategory = cats[j]; return ascendantProgressionCategory }
    }
  } catch (e) {}
  if (!ascendantProgressionWarnedMissingCategory) { console.warn("[Ascendant Progression] Ascendant Web category not found yet."); ascendantProgressionWarnedMissingCategory = true }
  return null
}

function getAscendantPlayerId(player) {
  try { if (player && player.uuid) return String(player.uuid) } catch (e) {}
  try { if (player && player.name) return String(player.name) } catch (e) {}
  return "player"
}
function getPlayerState(player) {
  var id = getAscendantPlayerId(player)
  if (!ascendantProgressionState[id]) ascendantProgressionState[id] = { delay: 0, levelUpTicks: 0, xpPulseTicks: 0, lastCurrentXp: -1, loggedReady: false, warnedPaint: false }
  return ascendantProgressionState[id]
}
function clampInt(v, mn, mx) { return Math.max(mn, Math.min(mx, Math.floor(Number(v) || 0))) }
function getDisplayLevel(rawLevel) {
  var off = Number(ascendantProgressionConfig.display_level_offset || 0), cap = Number(ascendantProgressionConfig.display_level_cap || 0)
  var dl = Math.floor(Number(rawLevel) + off)
  if (cap > 0) dl = Math.min(dl, cap)
  return Math.max(1, dl)
}
function calculateManagedBonusPoints(displayLevel) {
  var b = ascendantProgressionConfig.managed_bonus_points || {}
  if (!b.enabled) return 0
  var t = 0, m = b.milestones || []
  for (var i = 0; i < m.length; i++) if (displayLevel >= Number(m[i].level || 0)) t += Number(m[i].points || 0)
  return Math.max(0, Math.floor(t))
}
function applyManagedBonusPoints(player, category, displayLevel) {
  var data = player.getPersistentData()
  var next = calculateManagedBonusPoints(displayLevel)
  var prev = data.contains(ASCENDANT_PROGRESSION_MANAGED_BONUS) ? data.getInt(ASCENDANT_PROGRESSION_MANAGED_BONUS) : 0
  var cur = category.getExtraPoints(player)
  var manual = Math.max(0, cur - prev)
  if (next !== prev || cur !== manual + next) { category.setExtraPoints(player, manual + next); data.putInt(ASCENDANT_PROGRESSION_MANAGED_BONUS, next) }
}
function ensureAscendantProgressionScoreboards(server) {
  if (!server || !ascendantProgressionConfig.scoreboard.enabled) return
  var s = ascendantProgressionConfig.scoreboard
  server.runCommandSilent(`scoreboard objectives add ${s.level_objective} dummy {"text":"Ascendant Lv","color":"aqua"}`)
  server.runCommandSilent(`scoreboard objectives add ${s.xp_objective} dummy {"text":"Ascendant XP","color":"dark_aqua"}`)
  server.runCommandSilent(`scoreboard objectives add ${s.xp_required_objective} dummy {"text":"XP Needed","color":"gray"}`)
  server.runCommandSilent(`scoreboard objectives add ${s.points_left_objective} dummy {"text":"Skill Points","color":"gold"}`)
  server.runCommandSilent(`scoreboard objectives add ${s.points_spent_objective} dummy {"text":"Spent SP","color":"yellow"}`)
  server.runCommandSilent(`scoreboard objectives add ${s.points_total_objective} dummy {"text":"Total SP","color":"yellow"}`)
  server.runCommandSilent(`scoreboard objectives setdisplay belowName ${s.level_objective}`)
}
function setAscendantScore(player, obj, val) { player.runCommandSilent(`scoreboard players set @s ${obj} ${Math.floor(Number(val) || 0)}`) }
function mirrorProgressionScoreboards(player, p) {
  if (!ascendantProgressionConfig.scoreboard.enabled) return
  var s = ascendantProgressionConfig.scoreboard
  setAscendantScore(player, s.level_objective, p.displayLevel); setAscendantScore(player, s.xp_objective, p.currentXp)
  setAscendantScore(player, s.xp_required_objective, p.requiredXp); setAscendantScore(player, s.points_left_objective, p.pointsLeft)
  setAscendantScore(player, s.points_spent_objective, p.pointsSpent); setAscendantScore(player, s.points_total_objective, p.pointsTotal)
}
function triggerAscendantLevelUp(player, state, p) {
  var lu = ascendantProgressionConfig.level_up
  if (!lu.enabled) return
  state.levelUpTicks = clampInt(lu.banner_ticks, 0, 200)
  state.xpPulseTicks = Math.max(state.xpPulseTicks, clampInt(lu.xp_pulse_ticks, 0, 120))
  var tt = JSON.stringify(`${String(lu.title_text || "Level Up!")} `), st = JSON.stringify(String(lu.subtitle_text || "Ascendant Web"))
  player.runCommandSilent("title @s times 8 55 14")
  player.runCommandSilent(`title @s title [{"text":${tt},"color":"aqua","bold":true},{"text":"${p.displayLevel}","color":"gold","bold":true}]`)
  player.runCommandSilent(`title @s subtitle {"text":${st},"color":"dark_aqua","italic":true}`)
  player.runCommandSilent(`playsound ${lu.sound} player @s ~ ~ ~ ${Number(lu.volume || 0.85)} ${Number(lu.pitch || 1.15)}`)
}
function collectAscendantProgression(player) {
  var category = getAscendantCategory()
  if (category === null) return null
  var eo = category.getExperience()
  if (!eo.isPresent()) return null
  var exp = eo.get(), rawLevel = exp.getLevel(player), displayLevel = getDisplayLevel(rawLevel)
  applyManagedBonusPoints(player, category, displayLevel)
  var currentXp = Math.max(0, exp.getCurrent(player)), requiredXp = Math.max(0, exp.getRequired(player, rawLevel))
  return {
    categoryId: String(category.getId()), rawLevel: rawLevel, displayLevel: displayLevel,
    currentXp: currentXp, requiredXp: requiredXp,
    pointsLeft: Math.max(0, category.getPointsLeft(player)), pointsSpent: Math.max(0, category.getSpentPoints(player)),
    pointsTotal: Math.max(0, category.getPointsTotal(player)),
    progress: requiredXp <= 0 ? 1 : Math.max(0, Math.min(1, currentXp / requiredXp)),
    mana: getAscendantMana(player)
  }
}
function shouldHideAscendantProgressionHud(player) {
  var hud = ascendantProgressionConfig.hud || {}
  if (hud.hide_in_creative !== false) { try { if (player.isCreative()) return true } catch (e) {} try { if (player.getAbilities().instabuild) return true } catch (e) {} }
  if (hud.hide_in_spectator !== false) { try { if (player.isSpectator()) return true } catch (e) {} }
  return false
}

const ASCENDANT_HUD_ELEMENT_IDS = [
  "ar_hud_mana_border", "ar_hud_mana_groove", "ar_hud_mana_top", "ar_hud_mana_mid", "ar_hud_mana_bot",
  "ar_hud_xp_border", "ar_hud_xp_groove", "ar_hud_xp_top", "ar_hud_xp_mid", "ar_hud_xp_bot",
  "ar_hud_level_badge", "ar_hud_level_text", "ar_hud_sp_gem", "ar_hud_sp_text", "ar_hud_mana_value", "ar_hud_levelup_banner"
]
function clearAscendantProgressionHud(player, state) {
  // Only send the clear once per hide-transition. Previously this re-sent ~112 type-less
  // {remove:true} objects EVERY sync (incl. legacy/segment ids that no longer exist), which
  // spammed the client with "Unknown Painter type:" 97k+ times in a single session.
  if (state && state.hudCleared) return
  try {
    var els = {}
    ASCENDANT_HUD_ELEMENT_IDS.forEach((id) => { els[id] = { remove: true } })
    player.paint(els)
    if (state) state.hudCleared = true
  } catch (error) { if (state && !state.warnedPaint) { console.warn(`[Ascendant Progression] HUD clear failed once: ${error}`); state.warnedPaint = true } }
}

function paintAscendantProgressionHud(player, state, progress) {
  var hud = ascendantProgressionConfig.hud
  if (!hud.enabled) return
  var draw = String(hud.draw_mode || "ingame")
  var xpFrac = Math.max(0, Math.min(1, progress.progress)), xpW = Math.max(0, Math.round(88 * xpFrac))
  var mana = progress.mana, manaShown = mana !== null && hud.mana_enabled !== false
  var manaFrac = manaShown ? mana.frac : 0, manaW = Math.max(0, Math.round(88 * manaFrac))
  var showValues = hud.show_values !== false
  var pulseOn = state.xpPulseTicks > 0 && Math.floor(state.xpPulseTicks / 5) % 2 === 0
  var BORDER = "#FF0C1826", GROOVE = "#FF05101A", WHITE = "#FFFFFFFF"
  var XPT = pulseOn ? "#FFFFFFFF" : "#FF93D2FF", XPM = "#FF4F9CEC", XPB = "#FF295FBE"
  var MNT = "#FFACEDFF", MNM = "#FF4FC4F0", MNB = "#FF2A82BE"
  try {
    var els = {
      // ----- bottom-left cluster (moved out of the crowded center) -----
      ar_hud_mana_border: { type: "rectangle", draw: draw, visible: manaShown, x: "25", y: "$screenH - 23", z: 41, w: 90, h: 5, color: BORDER },
      ar_hud_mana_groove: { type: "rectangle", draw: draw, visible: manaShown, x: "26", y: "$screenH - 22", z: 42, w: 88, h: 3, color: GROOVE },
      ar_hud_mana_top: { type: "rectangle", draw: draw, visible: manaShown && manaW > 0, x: "26", y: "$screenH - 22", z: 43, w: manaW, h: 1, color: MNT },
      ar_hud_mana_mid: { type: "rectangle", draw: draw, visible: manaShown && manaW > 0, x: "26", y: "$screenH - 21", z: 43, w: manaW, h: 1, color: MNM },
      ar_hud_mana_bot: { type: "rectangle", draw: draw, visible: manaShown && manaW > 0, x: "26", y: "$screenH - 20", z: 43, w: manaW, h: 1, color: MNB },
      ar_hud_xp_border: { type: "rectangle", draw: draw, visible: true, x: "25", y: "$screenH - 13", z: 41, w: 90, h: 5, color: BORDER },
      ar_hud_xp_groove: { type: "rectangle", draw: draw, visible: true, x: "26", y: "$screenH - 12", z: 42, w: 88, h: 3, color: GROOVE },
      ar_hud_xp_top: { type: "rectangle", draw: draw, visible: xpW > 0, x: "26", y: "$screenH - 12", z: 43, w: xpW, h: 1, color: XPT },
      ar_hud_xp_mid: { type: "rectangle", draw: draw, visible: xpW > 0, x: "26", y: "$screenH - 11", z: 43, w: xpW, h: 1, color: XPM },
      ar_hud_xp_bot: { type: "rectangle", draw: draw, visible: xpW > 0, x: "26", y: "$screenH - 10", z: 43, w: xpW, h: 1, color: XPB },
      ar_hud_level_badge: { type: "rectangle", draw: draw, visible: true, x: "4", y: "$screenH - 25", z: 45, w: 18, h: 18, texture: ASCENDANT_HUD_TEX + "level_badge.png", color: WHITE },
      ar_hud_level_text: { type: "text", draw: draw, visible: true, x: "13", y: "$screenH - 19", z: 47, text: `${progress.displayLevel}`, color: hud.level_text_color || "#FFC8E8FF", centered: true, shadow: true, scale: 1 },
      ar_hud_sp_gem: { type: "rectangle", draw: draw, visible: true, x: "118", y: "$screenH - 13", z: 45, w: 9, h: 9, texture: ASCENDANT_HUD_TEX + "sp_gem.png", color: WHITE },
      ar_hud_sp_text: { type: "text", draw: draw, visible: true, x: "129", y: "$screenH - 12", z: 47, text: `${progress.pointsLeft}`, color: hud.sp_text_color || "#FFB6E6FF", centered: false, shadow: true, scale: 1 },
      ar_hud_mana_value: { type: "text", draw: draw, visible: manaShown && showValues, x: "70", y: "$screenH - 33", z: 47, text: manaShown ? `${Math.floor(mana.mana)} / ${Math.floor(mana.maxMana)}` : "", color: hud.value_text_color || "#FFCFEFFF", centered: true, shadow: true, scale: 1 },
      ar_hud_levelup_banner: { type: "text", draw: draw, visible: state.levelUpTicks > 0, x: "$screenW / 2", y: "$screenH / 2 - 72", z: 60, text: `Level Up!  ${progress.displayLevel}`, color: pulseOn ? "#FFFFFFFF" : "#FFFFD166", centered: true, shadow: true, scale: 1.5 }
    }
    player.paint(els)
    if (state) state.hudCleared = false
  } catch (error) { if (!state.warnedPaint) { console.warn(`[Ascendant Progression] HUD paint failed once: ${error}`); state.warnedPaint = true } }
}

function syncAscendantProgression(player, server, force) {
  if (!ascendantProgressionConfig.enabled || !player) return
  var state = getPlayerState(player)
  if (!force) { state.delay -= 1; if (state.delay > 0) return }
  state.delay = clampInt(ascendantProgressionConfig.sync_interval_ticks, 1, 200)
  ensureAscendantProgressionScoreboards(server || player.getServer())
  var progress = collectAscendantProgression(player)
  if (progress === null) return
  if (state.lastCurrentXp >= 0 && progress.currentXp > state.lastCurrentXp) state.xpPulseTicks = Math.max(state.xpPulseTicks, clampInt(ascendantProgressionConfig.level_up.xp_pulse_ticks, 0, 120))
  state.lastCurrentXp = progress.currentXp
  var data = player.getPersistentData()
  if (!data.contains(ASCENDANT_PROGRESSION_LAST_LEVEL)) data.putInt(ASCENDANT_PROGRESSION_LAST_LEVEL, progress.displayLevel)
  var prev = data.getInt(ASCENDANT_PROGRESSION_LAST_LEVEL)
  if (progress.displayLevel > prev) triggerAscendantLevelUp(player, state, progress)
  if (progress.displayLevel !== prev) data.putInt(ASCENDANT_PROGRESSION_LAST_LEVEL, progress.displayLevel)
  mirrorProgressionScoreboards(player, progress)
  if (!ascendantProgressionConfig.hud.enabled || shouldHideAscendantProgressionHud(player)) clearAscendantProgressionHud(player, state)
  else paintAscendantProgressionHud(player, state, progress)
  if (!state.loggedReady) { console.info(`[Ascendant Progression] HUD active: Lv ${progress.displayLevel}, ${progress.currentXp}/${progress.requiredXp} XP, ${progress.pointsLeft} SP, mana ${progress.mana ? "on" : "off"}.`); state.loggedReady = true }
  if (state.levelUpTicks > 0) state.levelUpTicks = Math.max(0, state.levelUpTicks - state.delay)
  if (state.xpPulseTicks > 0) state.xpPulseTicks = Math.max(0, state.xpPulseTicks - state.delay)
}

ServerEvents.loaded((event) => { ascendantProgressionConfig = readAscendantProgressionConfig(); ascendantProgressionCategory = null; ensureAscendantProgressionScoreboards(event.server) })
PlayerEvents.loggedIn((event) => { syncAscendantProgression(event.player, event.server, true) })
PlayerEvents.respawned((event) => { syncAscendantProgression(event.player, event.server, true) })
PlayerEvents.tick((event) => { syncAscendantProgression(event.player, event.server, false) })
