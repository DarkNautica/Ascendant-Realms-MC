// ============================================================
//  Ascendant Skill Effects - EXTRAS (cool-ideas pass)
//  Companion to ascendant_skill_effects.js. Implements the 21 mixed-node
//  upgrades + 7 new behavior nodes. Self-contained (SX_ prefix) so the core
//  engine is untouched. Shares the re-entrancy flag global.__arSkBusy.
//  Tunables: config/ascendant_skill_effects/extras.json
// ============================================================

const SX_JsonIO = typeof JsonIO !== "undefined" ? JsonIO : Java.loadClass("dev.latvian.mods.kubejs.util.JsonIO")
const SX_DEFAULTS = {
  enabled: true,
  shield_bash: { knockback: 1.0, slow_s: 2, slow_amp: 2 },
  cleave: { pct: 0.25, radius: 2.5 },
  giant_slayer: { pct_per_10hp: 0.02, max_pct: 0.5 },
  bleed: { wither_s: 4, wither_amp: 0 },
  pickpocket: { chance: 0.25, drops: ["minecraft:emerald", "minecraft:gold_nugget"] },
  death_from_above: { min_fall: 4.0, dmg_per_block: 0.5, max_dmg: 12, radius: 3 },
  pinning_shot: { slow_s: 2, slow_amp: 2 },
  shared_vigor: { radius: 8, regen_amp: 0 },
  trophy_hunter: { boss_hp: 80, xp: 15, drop: "minecraft:emerald" },
  spellstrike: { chance: 0.25, bonus: 3 },
  smite: { pct: 0.25, heal: 3 },
  frostbite: { slow_s: 2, slow_amp: 1 },
  field_rations: { haste_s: 6, speed_amp: 0 },
  sea_legs: { speed_amp: 0 },
  prospector: { chance: 0.30, drop: "minecraft:raw_iron" },
  storm_strider: { speed_amp: 0 },
  cave_sight: { y_below: 52 },
  frostwalker: { resist_amp: 0, temp_below: 0.15 },
  dragonslayer: { pct: 0.20 },
  scaleguard: { hp_frac: 0.45, fireres_s: 5 },
  bonded_mount: { resist_amp: 1 },
  rampage: { max_stacks: 5, reset_frac: 0.15, buff_s: 6, decay_s: 8 },
  executioner: { hp_frac: 0.30, pct: 0.5 },
  explosive_shot: { dmg: 3, radius: 2.5 },
  chain_lightning: { chance: 0.25, dmg: 3, radius: 5 },
  thornmail: { pct: 0.25, max: 6 },
  second_wind: { hp_frac: 0.35, heal: 8, cd_s: 60 },
  full_moon_frenzy: { lifesteal_frac: 0.15, dmg_pct: 0.15 }
}
function sxIsObj(v) { return v !== null && typeof v === "object" && !Array.isArray(v) }
function sxMerge(b, o) { var r = {}; Object.keys(b || {}).forEach(k => { r[k] = sxIsObj(b[k]) ? sxMerge(b[k], {}) : b[k] }); Object.keys(o || {}).forEach(k => { r[k] = sxIsObj(o[k]) && sxIsObj(r[k]) ? sxMerge(r[k], o[k]) : o[k] }); return r }
function sxReadConfig() { try { var p = SX_JsonIO.read("config/ascendant_skill_effects/extras.json"); if (p === null || p === undefined) return SX_DEFAULTS; return sxMerge(SX_DEFAULTS, p) } catch (e) { console.warn("[Ascendant Skills+] config read failed: " + e); return SX_DEFAULTS } }
let SX_cfg = sxReadConfig()

const SX = { now: 0, players: {} }
function sxId(e) { try { return e.uuid.toString() } catch (x) { return "?" } }
function sxSt(p) { var id = sxId(p); if (!SX.players[id]) SX.players[id] = { tick: 0, ramp: 0, rampTime: 0, cdWind: 0, lastFood: 20 }; return SX.players[id] }
function sxHas(e, tag) { try { return e && e.tags && e.tags.contains(tag) } catch (x) { return false } }
function sxNum(v, d) { v = Number(v); return isFinite(v) ? v : d }
function sxIsPlayer(e) { try { return e && ("" + e.type) === "minecraft:player" } catch (x) { return false } }
function sxAttacker(source) {
  if (!source) return null
  var c = []
  try { c.push(source.player) } catch (e) {}
  try { c.push(source.actual) } catch (e) {}
  try { c.push(source.entity) } catch (e) {}
  try { if (source.getActual) c.push(source.getActual()) } catch (e) {}
  try { if (source.getEntity) c.push(source.getEntity()) } catch (e) {}
  for (var i = 0; i < c.length; i++) { try { if (c[i] && ("" + c[i].type) === "minecraft:player") return c[i] } catch (e) {} }
  return null
}
function sxRanged(source) { try { var t = ("" + (source.type || "")).toLowerCase(); if (t.indexOf("arrow") >= 0 || t.indexOf("trident") >= 0 || t.indexOf("projectile") >= 0) return true; try { if (source.actual && source.entity && sxId(source.actual) !== sxId(source.entity)) return true } catch (e) {} } catch (e) {} return false }
function sxSrcIs(source, key) { try { return ("" + (source.type || "")).toLowerCase().indexOf(key) >= 0 } catch (e) { return false } }
function sxBase(event) { try { var d = event.damage; if (d === undefined && event.getDamage) d = event.getDamage(); d = Number(d); return isFinite(d) && d > 0 ? d : 0 } catch (e) { return 0 } }
function sxDist(a, b) { try { return Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2) + Math.pow(a.z - b.z, 2)) } catch (e) { return 99 } }
function sxEff(server, sel, id, secs, amp) { try { server.runCommandSilent("effect give " + sel + " " + id + " " + secs + " " + amp + " true") } catch (e) {} }
function sxCmd(server, cmd) { try { global.__arSkBusy = true; server.runCommandSilent(cmd) } catch (e) {} finally { global.__arSkBusy = false } }
function sxBonus(server, attUuid, vic, amount) { if (!(amount > 0)) return; sxCmd(server, "damage " + sxId(vic) + " " + (Math.round(amount * 100) / 100) + " minecraft:player_attack by " + attUuid) }
function sxArea(server, attUuid, center, amount, radius, near) { if (!(amount > 0)) return; sxCmd(server, "execute at " + sxId(center) + " run damage @e[distance=" + (near || 0.1) + ".." + radius + ",type=!minecraft:player,limit=8] " + (Math.round(amount * 100) / 100) + " minecraft:player_attack by " + attUuid) }
function sxHeal(p, amt) { try { p.setHealth(Math.min(sxNum(p.maxHealth, 20), sxNum(p.health, 20) + amt)) } catch (e) {} }
var SX_UNDEAD = ["zombie", "skeleton", "wither", "drowned", "husk", "stray", "phantom", "zoglin", "zombified", "vex", "bone", "undead", "ghoul", "wraith", "lich", "revenant", "ghast", "pumpkin", "decay", "chaos"]
var SX_DRAGON = ["dragon", "wyvern", "wyrm", "hydra", "drake", "naga", "cockatrice"]
function sxTypeHas(e, list) { try { var t = ("" + e.type).toLowerCase(); for (var i = 0; i < list.length; i++) if (t.indexOf(list[i]) >= 0) return true } catch (x) {} return false }
function sxMoonFull(level) { try { var ph = level.getMoonPhase ? level.getMoonPhase() : level.moonPhase; return Number(ph) === 0 } catch (e) { return false } }
function sxIsNight(level) { try { var t = Number(level.dayTime !== undefined ? level.dayTime : level.getDayTime()) % 24000; return t >= 13000 && t <= 23000 } catch (e) { return false } }
function sxTemp(p) { try { return Number(p.block.biome.value().getBaseTemperature()) } catch (e) { try { return Number(p.level.getBiome(p.blockPosition()).value().getBaseTemperature()) } catch (x) { return 0.8 } } }
function sxFood(p) { try { return Number(p.foodData.foodLevel) } catch (e) { try { return Number(p.getFoodData().getFoodLevel()) } catch (x) { return 20 } } }
function sxVehicle(p) { try { return p.vehicle || (p.getVehicle ? p.getVehicle() : null) } catch (e) { return null } }

ServerEvents.tick(event => { SX.now++ })

// ===== ON-HIT =====
try {
  EntityEvents.hurt(event => {
    if (global.__arSkBusy) return
    if (!SX_cfg.enabled) return
    var victim = event.entity; if (!victim) return

    // ---- victim is a player ----
    if (sxIsPlayer(victim)) {
      try {
        var vp = victim, server = vp.server, vu = sxId(vp), vs = sxSt(vp)
        var hp = sxNum(vp.health, 20), mx = sxNum(vp.maxHealth, 20), inc = sxBase(event)
        var att = sxAttacker(event.source)
        if (sxHas(vp, "ar_sk_engineer_thornmail") && att && !sxRanged(event.source)) sxBonus(server, vu, att, inc * Math.min(SX_cfg.thornmail.max, SX_cfg.thornmail.pct * inc) / Math.max(inc, 0.01))
        if (sxHas(vp, "ar_sk_warrior_shield_bash") && att && !sxRanged(event.source)) { try { if (vp.isBlocking && vp.isBlocking()) { sxEff(server, sxId(att), "minecraft:slowness", SX_cfg.shield_bash.slow_s, SX_cfg.shield_bash.slow_amp); sxBonus(server, vu, att, 0.5) } } catch (e) {} }
        if (sxHas(vp, "ar_sk_dragonbound_scaleguard") && (hp - inc) <= SX_cfg.scaleguard.hp_frac * mx) sxEff(server, vu, "minecraft:fire_resistance", SX_cfg.scaleguard.fireres_s, 0)
        if (sxHas(vp, "ar_sk_survivalist_second_wind") && (hp - inc) <= SX_cfg.second_wind.hp_frac * mx && vs.cdWind <= SX.now) {
          vs.cdWind = SX.now + SX_cfg.second_wind.cd_s * 20; sxHeal(vp, SX_cfg.second_wind.heal)
          var bad = ["poison", "wither", "slowness", "weakness", "mining_fatigue", "hunger"]
          for (var b = 0; b < bad.length; b++) { try { server.runCommandSilent("effect clear " + vu + " minecraft:" + bad[b]) } catch (e) {} }
          try { server.runCommandSilent("execute at " + vu + " run particle minecraft:heart ~ ~1 ~ 0.5 0.6 0.5 0.1 12") } catch (e) {}
        }
        if (sxHas(vp, "ar_sk_rogue_death_from_above") && sxSrcIs(event.source, "fall") && inc > 1) sxArea(server, vu, vp, Math.min(SX_cfg.death_from_above.max_dmg, inc), SX_cfg.death_from_above.radius)
        if (sxHas(vp, "ar_sk_warrior_rampage") && inc >= SX_cfg.rampage.reset_frac * mx) vs.ramp = 0
      } catch (e) { if (!global.__sxHurtV) { global.__sxHurtV = true; console.warn("[Ascendant Skills+] victim hook: " + e) } }
      return
    }

    // ---- attacker is a player ----
    var att2 = sxAttacker(event.source); if (!att2 || !sxIsPlayer(att2)) return
    try {
      var server2 = att2.server, au = sxId(att2), base = sxBase(event), ranged = sxRanged(event.source)
      var vhp = sxNum(victim.health, 20), vmx = sxNum(victim.maxHealth, 20)
      var frac = 0, flat = 0
      if (!ranged && sxHas(att2, "ar_sk_warrior_cleave")) sxArea(server2, au, victim, base * SX_cfg.cleave.pct, SX_cfg.cleave.radius)
      if (sxHas(att2, "ar_sk_warrior_giant_slayer")) frac += Math.min(SX_cfg.giant_slayer.max_pct, (vmx / 10) * SX_cfg.giant_slayer.pct_per_10hp)
      if (sxHas(att2, "ar_sk_rogue_executioner") && vmx > 0 && (vhp / vmx) <= SX_cfg.executioner.hp_frac) frac += SX_cfg.executioner.pct
      if (sxHas(att2, "ar_sk_dragonbound_dragonslayer") && sxTypeHas(victim, SX_DRAGON)) frac += SX_cfg.dragonslayer.pct
      if (sxHas(att2, "ar_sk_arcanist_smite") && sxTypeHas(victim, SX_UNDEAD)) frac += SX_cfg.smite.pct
      if (sxHas(att2, "ar_sk_dragonbound_full_moon_frenzy") && sxMoonFull(att2.level) && sxIsNight(att2.level)) { frac += SX_cfg.full_moon_frenzy.dmg_pct; sxHeal(att2, base * SX_cfg.full_moon_frenzy.lifesteal_frac) }
      if (sxHas(att2, "ar_sk_rogue_bleed")) sxEff(server2, sxId(victim), "minecraft:wither", SX_cfg.bleed.wither_s, SX_cfg.bleed.wither_amp)
      if (sxHas(att2, "ar_sk_arcanist_frostbite")) { sxEff(server2, sxId(victim), "minecraft:slowness", SX_cfg.frostbite.slow_s, SX_cfg.frostbite.slow_amp); try { server2.runCommandSilent("execute at " + sxId(victim) + " run particle minecraft:snowflake ~ ~1 ~ 0.3 0.4 0.3 0.02 12") } catch (e) {} }
      if (ranged && sxHas(att2, "ar_sk_ranger_pinning_shot")) sxEff(server2, sxId(victim), "minecraft:slowness", SX_cfg.pinning_shot.slow_s, SX_cfg.pinning_shot.slow_amp)
      if (!ranged && sxHas(att2, "ar_sk_arcanist_spellstrike") && Math.random() < SX_cfg.spellstrike.chance) { try { server2.runCommandSilent("execute at " + sxId(victim) + " run summon minecraft:evoker_fangs ~ ~ ~"); server2.runCommandSilent("execute at " + sxId(victim) + " run particle minecraft:enchant ~ ~1 ~ 0.6 0.8 0.6 1 24") } catch (e) {}; flat += SX_cfg.spellstrike.bonus }
      if (sxHas(att2, "ar_sk_arcanist_chain_lightning") && Math.random() < SX_cfg.chain_lightning.chance) { sxArea(server2, au, victim, SX_cfg.chain_lightning.dmg, SX_cfg.chain_lightning.radius, 1.6); try { server2.runCommandSilent("execute at " + sxId(victim) + " run particle minecraft:electric_spark ~ ~1 ~ 0.6 0.6 0.6 0.4 20") } catch (e) {} }
      if (ranged && sxHas(att2, "ar_sk_ranger_explosive_shot")) { sxArea(server2, au, victim, SX_cfg.explosive_shot.dmg, SX_cfg.explosive_shot.radius); try { server2.runCommandSilent("execute at " + sxId(victim) + " run particle minecraft:explosion ~ ~0.5 ~ 0 0 0 0 1") } catch (e) {} }
      if (frac > 0 || flat > 0) sxBonus(server2, au, victim, base * frac + flat)
    } catch (e) { if (!global.__sxHurtA) { global.__sxHurtA = true; console.warn("[Ascendant Skills+] attacker hook: " + e) } }
  })
} catch (e) { console.warn("[Ascendant Skills+] hurt unavailable: " + e) }

// ===== ON-KILL =====
try {
  EntityEvents.death(event => {
    if (!SX_cfg.enabled) return
    var killer = sxAttacker(event.source); if (!killer || !sxIsPlayer(killer)) return
    try {
      var server = killer.server, ku = sxId(killer), st = sxSt(killer), victim = event.entity
      if (sxHas(killer, "ar_sk_rogue_pickpocket") && victim && Math.random() < SX_cfg.pickpocket.chance) { var t = ("" + victim.type).toLowerCase(); if (t.indexOf("villager") >= 0 || t.indexOf("pillager") >= 0 || t.indexOf("illager") >= 0 || t.indexOf("witch") >= 0 || t.indexOf("piglin") >= 0 || t.indexOf("human") >= 0 || t.indexOf("knight") >= 0 || t.indexOf("captain") >= 0 || t.indexOf("pirate") >= 0) { var dr = SX_cfg.pickpocket.drops; try { server.runCommandSilent("execute at " + sxId(victim) + " run summon minecraft:item ~ ~ ~ {Item:{id:\"" + dr[Math.floor(Math.random() * dr.length)] + "\",Count:1b}}") } catch (e) {} } }
      if (sxHas(killer, "ar_sk_ranger_trophy_hunter") && victim && sxNum(victim.maxHealth, 0) >= SX_cfg.trophy_hunter.boss_hp) { try { server.runCommandSilent("execute at " + sxId(victim) + " run summon minecraft:item ~ ~ ~ {Item:{id:\"" + SX_cfg.trophy_hunter.drop + "\",Count:1b}}"); killer.giveXP(SX_cfg.trophy_hunter.xp) } catch (e) {} }
      if (sxHas(killer, "ar_sk_arcanist_smite") && victim && sxTypeHas(victim, SX_UNDEAD)) sxHeal(killer, SX_cfg.smite.heal)
      if (sxHas(killer, "ar_sk_warrior_rampage")) {
        var rc = SX_cfg.rampage; st.ramp = Math.min(rc.max_stacks, st.ramp + 1); st.rampTime = SX.now
        var sAmp = st.ramp >= 4 ? 2 : st.ramp >= 2 ? 1 : 0
        sxEff(server, ku, "minecraft:strength", rc.buff_s, sAmp); sxEff(server, ku, "minecraft:speed", rc.buff_s, st.ramp >= 3 ? 1 : 0)
        try { server.runCommandSilent("execute at " + ku + " run particle minecraft:crit ~ ~1 ~ 0.4 0.5 0.4 0.3 " + (8 * st.ramp)) } catch (e) {}
      }
    } catch (e) { if (!global.__sxDeath) { global.__sxDeath = true; console.warn("[Ascendant Skills+] death hook: " + e) } }
  })
} catch (e) { console.warn("[Ascendant Skills+] death unavailable: " + e) }

// ===== TICK =====
var SX_PETS = ["minecraft:wolf", "minecraft:cat", "minecraft:fox", "minecraft:horse", "minecraft:donkey", "minecraft:mule", "minecraft:llama", "minecraft:parrot"]
PlayerEvents.tick(event => {
  if (!SX_cfg.enabled) return
  var p = event.player; if (!p) return
  var st = sxSt(p); st.tick++
  if (st.tick % 10 !== 0) return
  try {
    var server = p.server, u = sxId(p), lvl = p.level
    if (sxHas(p, "ar_sk_survivalist_storm_strider")) { try { if (lvl.isRaining() || lvl.isThundering()) sxEff(server, u, "minecraft:speed", 2, SX_cfg.storm_strider.speed_amp) } catch (e) {} }
    if (sxHas(p, "ar_sk_survivalist_cave_sight") && sxNum(p.y, 100) < SX_cfg.cave_sight.y_below) sxEff(server, u, "minecraft:night_vision", 12, 0)
    if (sxHas(p, "ar_sk_survivalist_frostwalker") && sxTemp(p) < SX_cfg.frostwalker.temp_below) sxEff(server, u, "minecraft:resistance", 2, SX_cfg.frostwalker.resist_amp)
    if (sxHas(p, "ar_sk_engineer_sea_legs") && sxVehicle(p)) { sxEff(server, u, "minecraft:speed", 2, SX_cfg.sea_legs.speed_amp); sxEff(server, u, "minecraft:slow_falling", 2, 0) }
    if (sxHas(p, "ar_sk_dragonbound_bonded_mount")) { var v = sxVehicle(p); if (v) sxEff(server, sxId(v), "minecraft:resistance", 2, SX_cfg.bonded_mount.resist_amp) }
    if (sxHas(p, "ar_sk_engineer_field_rations")) { var f = sxFood(p); if (f > st.lastFood) { sxEff(server, u, "minecraft:haste", SX_cfg.field_rations.haste_s, 0); sxEff(server, u, "minecraft:speed", SX_cfg.field_rations.haste_s, SX_cfg.field_rations.speed_amp) } st.lastFood = f }
    if (sxHas(p, "ar_sk_ranger_shared_vigor") && st.tick % 20 === 0) { var R = SX_cfg.shared_vigor.radius; for (var i = 0; i < SX_PETS.length; i++) { try { server.runCommandSilent("execute at " + u + " run effect give @e[type=" + SX_PETS[i] + ",distance=.." + R + "] minecraft:regeneration 3 " + SX_cfg.shared_vigor.regen_amp + " true") } catch (e) {} } }
    if (sxHas(p, "ar_sk_dragonbound_full_moon_frenzy") && sxMoonFull(lvl) && sxIsNight(lvl) && st.tick % 20 === 0) { try { server.runCommandSilent("execute at " + u + " run particle minecraft:dragon_breath ~ ~1 ~ 0.3 0.5 0.3 0.01 8") } catch (e) {} }
    if (st.ramp > 0 && (SX.now - st.rampTime) > SX_cfg.rampage.decay_s * 20) st.ramp = 0
  } catch (e) { if (!global.__sxTick) { global.__sxTick = true; console.warn("[Ascendant Skills+] tick hook: " + e) } }
})

// ===== BLOCK BREAK (Prospector) =====
try {
  BlockEvents.broken(event => {
    if (!SX_cfg.enabled) return
    var p = event.player; if (!p || !sxHas(p, "ar_sk_engineer_prospector")) return
    try { var id = "" + event.block.id; if (id.indexOf("ore") < 0) return; if (Math.random() < SX_cfg.prospector.chance) { try { p.give(Item.of(SX_cfg.prospector.drop)) } catch (e) { try { p.server.runCommandSilent("give " + sxId(p) + " " + SX_cfg.prospector.drop) } catch (e2) {} } } } catch (e) {}
  })
} catch (e) { console.warn("[Ascendant Skills+] broken unavailable: " + e) }

// Shield Bash note: handled here if blocking is detectable, else a near no-op.
ServerEvents.loaded(() => { SX_cfg = sxReadConfig(); console.info("[Ascendant Skills+] extras engine loaded. enabled=" + SX_cfg.enabled) })
