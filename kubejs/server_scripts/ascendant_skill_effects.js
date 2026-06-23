// ============================================================
//  Ascendant Skill Effects - milestone/keystone behavior engine
//  Puffish Skills grants only passive stats; this script provides the
//  "milestone" gameplay. Each behavior node fires a Puffish command reward
//  that stamps a tag (ar_sk_<branch>_<id>) on the player; this engine reads
//  those tags and runs the on-hit / on-kill / tick behavior.
//  Tunables live in config/ascendant_skill_effects/effects.json.
//  Pattern + API usage mirror ascendant_effects.js / ascendant_hunter_progression.js.
// ============================================================

const SKE_JsonIO = typeof JsonIO !== "undefined" ? JsonIO : Java.loadClass("dev.latvian.mods.kubejs.util.JsonIO")

const SKE_DEFAULTS = {
  enabled: true,
  guard_breaker: { stacks_needed: 5, window_s: 3, stagger_s: 1, vuln_s: 4, vuln_pct: 0.15 },
  blood_momentum: { dur_s: 3 },
  titanheart: { hp50_resist_amp: 0, hp50_strength_amp: 0, hp25_resist_amp: 1, hp25_strength_amp: 1 },
  weak_point: { max_stacks: 4, pct_per: 0.05, dur_s: 5 },
  backstab: { pct: 0.35, mark_s: 4, behind_deg: 120 },
  assassins_chain: { empower_pct: 0.5, window_s: 5 },
  hunters_mark: { pct: 0.20, mark_s: 8 },
  longshot: { max_pct: 0.30, min_dist: 10, full_dist: 30 },
  apex_predator: { max_stacks: 6, pct_per: 0.06, window_s: 4 },
  wardbreaker: { pct: 0.20, armor_min: 8 },
  spell_siphon: { mana: 20, power_s: 5 },
  arcane_overflow: { absorb_amp: 1, full_frac: 0.99 },
  salvage_protocol: { chance: 0.15 },
  reinforced_plating: { resist_amp: 0 },
  emergency_protocols: { hp_frac: 0.4, cd_s: 90, absorb_amp: 1, absorb_s: 6, burst_dmg: 2, burst_radius: 4 },
  field_medic: { radius: 6, ally_frac: 0.5, regen_amp: 0 },
  campfire_recovery: { radius: 4, regen_amp: 0, healthboost_amp: 0 },
  unkillable_guide: { cd_s: 90, resist_s: 5 },
  dragon_vein: { build_deal: 10, build_take: 15, max: 100, burst_dmg: 6 },
  dragons_pride: { pct: 0.15 },
  wyrmblood_ascendance: { surge_s: 6, cd_s: 30 }
}

function skeIsObj(v) { return v !== null && typeof v === "object" && !Array.isArray(v) }
function skeMerge(b, o) { var r = {}; Object.keys(b || {}).forEach(k => { r[k] = skeIsObj(b[k]) ? skeMerge(b[k], {}) : b[k] }); Object.keys(o || {}).forEach(k => { r[k] = skeIsObj(o[k]) && skeIsObj(r[k]) ? skeMerge(r[k], o[k]) : o[k] }); return r }
function skeReadConfig() { try { var p = SKE_JsonIO.read("config/ascendant_skill_effects/effects.json"); if (p === null || p === undefined) return SKE_DEFAULTS; return skeMerge(SKE_DEFAULTS, p) } catch (e) { console.warn("[Ascendant Skills] config read failed: " + e); return SKE_DEFAULTS } }
let SKE_cfg = skeReadConfig()

const SKE = { now: 0, players: {}, marks: {}, busy: false }
function skeId(e) { try { return e.uuid.toString() } catch (x) { return "?" } }
function skeSt(p) { var id = skeId(p); if (!SKE.players[id]) SKE.players[id] = { tick: 0, gT: null, gC: 0, gTime: 0, aT: null, aC: 0, aTime: 0, empUntil: 0, drac: 0, cdAsc: 0, cdEmg: 0, cdUnk: 0, cdFire: 0 }; return SKE.players[id] }
function skeMark(uuid) { if (!SKE.marks[uuid]) SKE.marks[uuid] = { sunder: 0, wp: 0, wpUntil: 0, hunt: 0, backstab: 0 }; return SKE.marks[uuid] }
function skeHas(e, tag) { try { return e && e.tags && e.tags.contains(tag) } catch (x) { return false } }
function skeNum(v, d) { v = Number(v); return isFinite(v) ? v : d }

// ---- damage source -> player attacker (mirrors ahFindKiller) ----
function skeAttacker(source) {
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
function skeIsPlayer(e) { try { return e && ("" + e.type) === "minecraft:player" } catch (x) { return false } }
function skeRanged(source) {
  try {
    var t = ("" + (source.type || "")).toLowerCase()
    if (t.indexOf("arrow") >= 0 || t.indexOf("trident") >= 0 || t.indexOf("projectile") >= 0) return true
    try { if (source.actual && source.entity && skeId(source.actual) !== skeId(source.entity)) return true } catch (e) {}
  } catch (e) {}
  return false
}
function skeBase(event) { try { var d = event.damage; if (d === undefined && event.getDamage) d = event.getDamage(); d = Number(d); return isFinite(d) && d > 0 ? d : 0 } catch (e) { return 0 } }
function skeDist(a, b) { try { return Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2) + Math.pow(a.z - b.z, 2)) } catch (e) { return 0 } }
function skeBehind(att, vic, deg) {
  try {
    var vy = vic.yaw; if (vy === undefined || vy === null) vy = vic.getYRot()
    vy = Number(vy)
    var dx = att.x - vic.x, dz = att.z - vic.z
    var ang = Math.atan2(-dx, dz) * 180 / Math.PI
    var d = Math.abs(((ang - vy + 540) % 360) - 180)
    return d > deg
  } catch (e) { return false }
}
function skeEff(server, sel, id, secs, amp) { try { server.runCommandSilent("effect give " + sel + " " + id + " " + secs + " " + amp + " true") } catch (e) {} }
function skeBonus(server, attUuid, vic, amount) {
  if (!(amount > 0)) return
  try { SKE.busy = true; global.__arSkBusy = true; server.runCommandSilent("damage " + skeId(vic) + " " + (Math.round(amount * 100) / 100) + " minecraft:player_attack by " + attUuid) } catch (e) {} finally { SKE.busy = false; global.__arSkBusy = false }
}
function skeArmor(p) { try { return skeNum(p.armorValue, 0) } catch (e) { try { return skeNum(p.getArmorValue(), 0) } catch (x) { return 0 } } }
function skeMana(p) {
  try {
    var MD = Java.loadClass("io.redspace.ironsspellbooks.api.magic.MagicData")
    var md = MD.getPlayerMagicData(p); if (!md) return null
    var mana = Number(md.getMana()), max = 0
    try { max = Number(md.getMaxMana()) } catch (e) {}
    if (max > 0) return { mana: mana, max: max, frac: mana / max, md: md }
  } catch (e) {}
  return null
}

// ===== clock =====
ServerEvents.tick(event => { SKE.now++ })

// ===== ON-HIT (attacker procs + victim survival) =====
try {
  EntityEvents.hurt(event => {
    if (SKE.busy || global.__arSkBusy) return
    if (!SKE_cfg.enabled) return
    var victim = event.entity; if (!victim) return
    var now = SKE.now

    // ---------- victim is a player: survival keystones ----------
    if (skeIsPlayer(victim)) {
      try {
        var vp = victim, vs = skeSt(vp), vu = skeId(vp), server = vp.server
        if (skeHas(vp, "ar_sk_dragonbound_dragon_vein")) { var dv = SKE_cfg.dragon_vein; vs.drac = Math.min(dv.max, vs.drac + dv.build_take) }
        var hp = skeNum(vp.health, 20), mx = skeNum(vp.maxHealth, 20), incoming = skeBase(event)
        // Unkillable Guide - cheat death
        if (skeHas(vp, "ar_sk_survivalist_unkillable_guide") && (hp - incoming) <= 0.5 && vs.cdUnk <= now) {
          event.cancel(); try { vp.setHealth(1) } catch (e) {}
          skeEff(server, vu, "minecraft:resistance", SKE_cfg.unkillable_guide.resist_s, 2)
          skeEff(server, vu, "minecraft:regeneration", 4, 1)
          vs.cdUnk = now + SKE_cfg.unkillable_guide.cd_s * 20
          try { server.runCommandSilent("execute at " + vu + " run particle minecraft:totem_of_undying ~ ~1 ~ 0.5 0.6 0.5 0.1 40") } catch (e) {}
          return
        }
        // Emergency Protocols - steam burst when a heavy hit drops you low
        if (skeHas(vp, "ar_sk_engineer_emergency_protocols") && (hp - incoming) <= SKE_cfg.emergency_protocols.hp_frac * mx && vs.cdEmg <= now) {
          var ep = SKE_cfg.emergency_protocols
          skeEff(server, vu, "minecraft:absorption", ep.absorb_s, ep.absorb_amp)
          skeEff(server, vu, "minecraft:resistance", ep.absorb_s, 0)
          vs.cdEmg = now + ep.cd_s * 20
          try {
            server.runCommandSilent("execute at " + vu + " run particle minecraft:cloud ~ ~0.6 ~ 1.2 0.4 1.2 0.05 60")
            server.runCommandSilent("execute at " + vu + " run playsound minecraft:block.fire.extinguish neutral @a[distance=..16] ~ ~ ~ 0.8 0.6")
            server.runCommandSilent("execute at " + vu + " run damage @e[distance=0.1.." + ep.burst_radius + ",type=!minecraft:player,limit=10] " + ep.burst_dmg + " minecraft:explosion by " + vu)
          } catch (e) {}
        }
      } catch (e) { if (!global.__skeHurtVWarn) { global.__skeHurtVWarn = true; console.warn("[Ascendant Skills] victim hook: " + e) } }
      return
    }

    // ---------- attacker is a player: offensive procs ----------
    var att = skeAttacker(event.source); if (!att || !skeIsPlayer(att)) return
    try {
      var server2 = att.server, au = skeId(att), vu2 = skeId(victim), st = skeSt(att)
      var ranged = skeRanged(event.source), base = skeBase(event)
      var mk = skeMark(vu2), frac = 0, flat = 0

      // Weak Point - target carries stacking vulnerability (affects everyone's hits)
      if (mk.wp > 0 && now < mk.wpUntil) frac += mk.wp * SKE_cfg.weak_point.pct_per
      if (skeHas(att, "ar_sk_rogue_weak_point")) { var wpc = SKE_cfg.weak_point; mk.wp = Math.min(wpc.max_stacks, mk.wp + 1); mk.wpUntil = now + wpc.dur_s * 20 }

      // Guard Breaker - melee stagger meter
      if (!ranged && skeHas(att, "ar_sk_warrior_guard_breaker")) {
        var gb = SKE_cfg.guard_breaker
        if (st.gT === vu2 && (now - st.gTime) <= gb.window_s * 20) st.gC += 1; else { st.gC = 1; st.gT = vu2 }
        st.gTime = now
        if (st.gC >= gb.stacks_needed) { st.gC = 0; mk.sunder = now + gb.vuln_s * 20; skeEff(server2, vu2, "minecraft:slowness", gb.stagger_s, 2); try { server2.runCommandSilent("execute at " + vu2 + " run particle minecraft:crit ~ ~1 ~ 0.4 0.4 0.4 0.2 20") } catch (e) {} }
      }
      if (mk.sunder > now && skeHas(att, "ar_sk_warrior_guard_breaker")) frac += SKE_cfg.guard_breaker.vuln_pct

      // Backstab - behind-arc bonus + mark
      if (!ranged && skeHas(att, "ar_sk_rogue_backstab") && skeBehind(att, victim, SKE_cfg.backstab.behind_deg)) {
        frac += SKE_cfg.backstab.pct; mk.backstab = now + SKE_cfg.backstab.mark_s * 20
        skeEff(server2, vu2, "minecraft:glowing", SKE_cfg.backstab.mark_s, 0)
      }

      // Hunter's Mark - ranged mark + bonus vs marked
      if (ranged && skeHas(att, "ar_sk_ranger_hunters_mark")) {
        if (mk.hunt <= now) skeEff(server2, vu2, "minecraft:glowing", SKE_cfg.hunters_mark.mark_s, 0)
        mk.hunt = now + SKE_cfg.hunters_mark.mark_s * 20
      }
      if (ranged && mk.hunt > now && skeHas(att, "ar_sk_ranger_hunters_mark")) frac += SKE_cfg.hunters_mark.pct

      // Longshot - distance scaling
      if (ranged && skeHas(att, "ar_sk_ranger_longshot")) {
        var ls = SKE_cfg.longshot, dd = skeDist(att, victim)
        if (dd > ls.min_dist) frac += Math.min(ls.max_pct, (dd - ls.min_dist) / (ls.full_dist - ls.min_dist) * ls.max_pct)
      }

      // Apex Predator - no-miss stacks vs marked target
      if (ranged && skeHas(att, "ar_sk_ranger_apex_predator") && mk.hunt > now) {
        var ap = SKE_cfg.apex_predator
        if (st.aT === vu2 && (now - st.aTime) <= ap.window_s * 20) st.aC = Math.min(ap.max_stacks, st.aC + 1); else { st.aC = 1; st.aT = vu2 }
        st.aTime = now; frac += st.aC * ap.pct_per
      }

      // Wardbreaker - vs armored / resistant
      if (skeHas(att, "ar_sk_arcanist_wardbreaker")) { try { if (skeNum(victim.armorValue, 0) >= SKE_cfg.wardbreaker.armor_min) frac += SKE_cfg.wardbreaker.pct } catch (e) {} }

      // Dragon's Pride - vs tougher enemies (bosses/elites)
      if (skeHas(att, "ar_sk_dragonbound_dragons_pride")) { try { if (skeNum(victim.maxHealth, 0) > skeNum(att.maxHealth, 20)) frac += SKE_cfg.dragons_pride.pct } catch (e) {} }

      // Dragon Vein - build meter on hit; release a burst when full
      if (skeHas(att, "ar_sk_dragonbound_dragon_vein")) {
        var dv2 = SKE_cfg.dragon_vein
        if (st.drac >= dv2.max) { flat += dv2.burst_dmg; st.drac = 0; try { server2.runCommandSilent("execute at " + vu2 + " run particle minecraft:flame ~ ~1 ~ 0.4 0.5 0.4 0.05 40") } catch (e) {} }
        else st.drac = Math.min(dv2.max, st.drac + dv2.build_deal)
      }

      // Assassin's Chain - empowered next hit (set on kill of a marked target)
      if (st.empUntil > now) { frac += SKE_cfg.assassins_chain.empower_pct; st.empUntil = 0 }

      if (frac > 0 || flat > 0) skeBonus(server2, au, victim, base * frac + flat)
    } catch (e) { if (!global.__skeHurtAWarn) { global.__skeHurtAWarn = true; console.warn("[Ascendant Skills] attacker hook: " + e) } }
  })
} catch (e) { console.warn("[Ascendant Skills] EntityEvents.hurt unavailable: " + e) }

// ===== ON-KILL =====
try {
  EntityEvents.death(event => {
    if (!SKE_cfg.enabled) return
    var killer = skeAttacker(event.source); if (!killer || !skeIsPlayer(killer)) return
    try {
      var server = killer.server, ku = skeId(killer), st = skeSt(killer), victim = event.entity
      if (skeHas(killer, "ar_sk_warrior_blood_momentum")) { var d = SKE_cfg.blood_momentum.dur_s; skeEff(server, ku, "minecraft:speed", d, 0); skeEff(server, ku, "minecraft:strength", d, 0) }
      if (skeHas(killer, "ar_sk_rogue_assassins_chain") && victim) { var mk = SKE.marks[skeId(victim)]; if (mk && (mk.hunt > SKE.now || mk.backstab > SKE.now)) st.empUntil = SKE.now + SKE_cfg.assassins_chain.window_s * 20 }
      if (skeHas(killer, "ar_sk_arcanist_spell_siphon")) {
        skeEff(server, ku, "minecraft:regeneration", 2, 0)
        var m = skeMana(killer); if (m && m.md) { try { m.md.setMana(Math.min(m.max, m.mana + SKE_cfg.spell_siphon.mana)) } catch (e) {} }
      }
      if (victim) delete SKE.marks[skeId(victim)]
    } catch (e) { if (!global.__skeDeathWarn) { global.__skeDeathWarn = true; console.warn("[Ascendant Skills] death hook: " + e) } }
  })
} catch (e) { console.warn("[Ascendant Skills] EntityEvents.death unavailable: " + e) }

// ===== TICK (sustained / conditional / cooldowns) =====
PlayerEvents.tick(event => {
  if (!SKE_cfg.enabled) return
  var p = event.player; if (!p) return
  var st = skeSt(p); st.tick++
  if (st.tick % 10 !== 0) return // 2x/sec is plenty
  try {
    var server = p.server, u = skeId(p), now = SKE.now
    var hp = skeNum(p.health, 20), mx = skeNum(p.maxHealth, 20), frac = mx > 0 ? hp / mx : 1

    // Titanheart - wounded scaling
    if (skeHas(p, "ar_sk_warrior_titanheart")) {
      var th = SKE_cfg.titanheart
      if (frac <= 0.25) { skeEff(server, u, "minecraft:resistance", 2, th.hp25_resist_amp); skeEff(server, u, "minecraft:strength", 2, th.hp25_strength_amp) }
      else if (frac <= 0.5) { skeEff(server, u, "minecraft:resistance", 2, th.hp50_resist_amp); skeEff(server, u, "minecraft:strength", 2, th.hp50_strength_amp) }
    }
    // Reinforced Plating - armor aura
    if (skeHas(p, "ar_sk_engineer_reinforced_plating") && skeArmor(p) > 0) skeEff(server, u, "minecraft:resistance", 2, SKE_cfg.reinforced_plating.resist_amp)
    // Arcane Overflow - full mana -> shield
    if (skeHas(p, "ar_sk_arcanist_arcane_overflow")) { var m = skeMana(p); if (m && m.frac >= SKE_cfg.arcane_overflow.full_frac) skeEff(server, u, "minecraft:absorption", 3, SKE_cfg.arcane_overflow.absorb_amp) }
    // Campfire Recovery - near fire
    if (skeHas(p, "ar_sk_survivalist_campfire_recovery") && st.tick % 20 === 0) {
      if (skeNearFire(p, SKE_cfg.campfire_recovery.radius)) { skeEff(server, u, "minecraft:regeneration", 3, SKE_cfg.campfire_recovery.regen_amp); skeEff(server, u, "minecraft:health_boost", 5, SKE_cfg.campfire_recovery.healthboost_amp) }
    }
    // Field Medic - mend a wounded ally nearby
    if (skeHas(p, "ar_sk_survivalist_field_medic") && frac > 0.5) {
      try {
        var fm = SKE_cfg.field_medic, players = p.level.players
        for (var i = 0; i < players.size(); i++) { var o = players.get(i); if (!o || skeId(o) === u) continue; if (skeDist(p, o) <= fm.radius && skeNum(o.health, 20) < fm.ally_frac * skeNum(o.maxHealth, 20)) skeEff(server, skeId(o), "minecraft:regeneration", 2, fm.regen_amp) }
      } catch (e) {}
    }
    // Wyrmblood Ascendance - auto-surge when the Draconic meter fills
    if (skeHas(p, "ar_sk_dragonbound_wyrmblood_ascendance") && st.drac >= SKE_cfg.dragon_vein.max && st.cdAsc <= now) {
      var wa = SKE_cfg.wyrmblood_ascendance; st.drac = 0; st.cdAsc = now + wa.cd_s * 20
      skeEff(server, u, "minecraft:resistance", wa.surge_s, 1); skeEff(server, u, "minecraft:strength", wa.surge_s, 1); skeEff(server, u, "minecraft:regeneration", wa.surge_s, 1); skeEff(server, u, "minecraft:speed", wa.surge_s, 0)
      try { server.runCommandSilent("execute at " + u + " run particle minecraft:dragon_breath ~ ~1 ~ 0.6 0.8 0.6 0.02 60"); server.runCommandSilent("execute at " + u + " run playsound minecraft:entity.ender_dragon.flap hostile @a[distance=..24] ~ ~ ~ 0.9 0.8") } catch (e) {}
    }
  } catch (e) { if (!global.__skeTickWarn) { global.__skeTickWarn = true; console.warn("[Ascendant Skills] tick hook: " + e) } }
})

function skeNearFire(p, r) {
  try {
    var lvl = p.level, bx = Math.floor(p.x), by = Math.floor(p.y), bz = Math.floor(p.z)
    for (var dx = -r; dx <= r; dx++) for (var dy = -1; dy <= 1; dy++) for (var dz = -r; dz <= r; dz++) {
      var id = "" + lvl.getBlock(bx + dx, by + dy, bz + dz).id
      if (id.indexOf("campfire") >= 0 || id === "minecraft:fire" || id === "minecraft:lava" || id.indexOf("soul_fire") >= 0) return true
    }
  } catch (e) {}
  return false
}

// ===== SALVAGE (block break) =====
try {
  BlockEvents.broken(event => {
    if (!SKE_cfg.enabled) return
    var p = event.player; if (!p || !skeHas(p, "ar_sk_engineer_salvage_protocol")) return
    try {
      if (Math.random() > SKE_cfg.salvage_protocol.chance) return
      var id = "" + event.block.id
      if (id.indexOf("ore") < 0 && id.indexOf("stone") < 0 && id.indexOf("deepslate") < 0) return
      var drop = id.indexOf("ore") >= 0 ? "minecraft:raw_iron" : "minecraft:cobblestone"
      try { p.give(Item.of(drop)) } catch (e) { try { p.server.runCommandSilent("give " + skeId(p) + " " + drop) } catch (e2) {} }
    } catch (e) { if (!global.__skeSalvWarn) { global.__skeSalvWarn = true; console.warn("[Ascendant Skills] salvage hook: " + e) } }
  })
} catch (e) { console.warn("[Ascendant Skills] BlockEvents.broken unavailable: " + e) }

ServerEvents.loaded(() => { SKE_cfg = skeReadConfig(); console.info("[Ascendant Skills] effects engine loaded. enabled=" + SKE_cfg.enabled) })
