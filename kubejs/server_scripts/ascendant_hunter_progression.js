// ============================================================
//  Ascendant Realms - AI Hunter living progression (v1)
//  Rides on the ar_ai_hunter / ar_ai_rank_* tags + customnpcs entities the
//  ascendant-atlas-regions Hunter Director spawns. Adds the three things the
//  jar does NOT do:
//    1. KILL-DRIVEN leveling - a hunter that lands killing blows earns renown
//       and ranks up from its OWN fights (not just standing near a player).
//    2. GEAR UPGRADE on rank-up - re-equips the next rank's curated loadout.
//    3. CASTER MAGIC v1 - arcanist-loadout hunters get spell procs in combat.
//  Reloadable: edit + /reload (no jar rebuild). Gear/nameplate rendering on
//  CustomNPCs is the one thing to confirm in-game (see the test plan).
// ============================================================

const AH_RENOWN_OBJ = "ar_hunter_renown"
const AH_RANKS = ["d_rank", "c_rank", "b_rank", "a_rank", "s_rank"]

// Per-rank loadout mirrors HunterDirectorCommands.java profileForRank().
// caster:true marks the magic archetype (B-rank arcanist gear).
const AH_RANKDATA = {
  d_rank: { label: "D-Rank", color: "§a", lvl: 24, hp: 44, str: 0, res: 0,
    main: "minecraft:bow", off: "minecraft:iron_sword", head: "immersive_armors:bone_helmet", chest: "immersive_armors:bone_chestplate" },
  c_rank: { label: "C-Rank", color: "§b", lvl: 34, hp: 64, str: 0, res: 0,
    main: "irons_spellbooks:autoloader_crossbow", off: "simplyswords:watching_warglaive", head: "artifacts:night_vision_goggles", chest: "immersive_armors:prismarine_chestplate" },
  b_rank: { label: "B-Rank", color: "§6", lvl: 46, hp: 92, str: 1, res: 1, caster: true,
    main: "irons_spellbooks:magehunter", off: "irons_spellbooks:diamond_spell_book", head: "irons_spellbooks:archevoker_helmet", chest: "irons_spellbooks:archevoker_chestplate" },
  a_rank: { label: "A-Rank", color: "§e", lvl: 68, hp: 132, str: 2, res: 1,
    main: "iceandfire:dragonbone_sword_fire", off: "spartanshields:netherite_basic_shield", head: "fantasy_armor:dragonslayer_helmet", chest: "fantasy_armor:dragonslayer_chestplate" },
  s_rank: { label: "S-Rank", color: "§d", lvl: 90, hp: 180, str: 3, res: 2,
    main: "soulsweapons:pure_moonlight_shortsword", off: "cataclysm:gauntlet_of_bulwark", head: "soulsweapons:forlorn_helmet", chest: "soulsweapons:forlorn_chestplate" }
}

// Renown needed to advance FROM a rank to the next (s_rank is the cap).
const AH_RENOWN_TO_NEXT = { d_rank: 8, c_rank: 18, b_rank: 35, a_rank: 70 }

// How much renown a victim is worth, by mod namespace (mirrors the rank bridge).
const AH_NS_RENOWN = {
  cataclysm: 10, bossesrise: 10, block_factorys_bosses: 8, iceandfire: 12,
  mowziesmobs: 4, irons_spellbooks: 4, alexsmobs: 2, aquamirae: 2, born_in_chaos_v1: 2
}
const AH_BOSS_OVERRIDES = { "minecraft:wither": 10, "minecraft:warden": 10, "minecraft:ender_dragon": 14, "minecraft:elder_guardian": 4 }

// ---- helpers ----------------------------------------------------------
function ahIsHunter(entity) {
  try { return entity && entity.tags && entity.tags.contains("ar_ai_hunter") } catch (e) { return false }
}
function ahRankOf(entity) {
  try { for (var i = AH_RANKS.length - 1; i >= 0; i--) { if (entity.tags.contains("ar_ai_rank_" + AH_RANKS[i])) return AH_RANKS[i] } } catch (e) {}
  return null
}
function ahFindKiller(source) {
  if (!source) return null
  var c = []
  try { c.push(source.player) } catch (e) {}
  try { c.push(source.actual) } catch (e) {}
  try { c.push(source.entity) } catch (e) {}
  try { if (source.getActual) c.push(source.getActual()) } catch (e) {}
  try { if (source.getEntity) c.push(source.getEntity()) } catch (e) {}
  for (var i = 0; i < c.length; i++) { if (c[i] && c[i].tags) return c[i] }
  return null
}
function ahRenownForVictim(entity) {
  try {
    var id = String(entity.type)
    if (AH_BOSS_OVERRIDES[id] !== undefined) return AH_BOSS_OVERRIDES[id]
    var ns = id.split(":")[0]
    if (AH_NS_RENOWN[ns] !== undefined) return AH_NS_RENOWN[ns]
    // vanilla hostiles count for 1; skip passive/critters to avoid farming chickens
    if (entity.living && entity.monster) return 1
  } catch (e) {}
  return 0
}

ServerEvents.loaded((event) => {
  event.server.runCommandSilent(`scoreboard objectives add ${AH_RENOWN_OBJ} dummy {"text":"Hunter Renown","color":"green"}`)
  console.info("[Ascendant Hunters] Living progression v1 loaded (kill leveling + gear upgrade + caster magic).")
})

// Auto-flag arcanist hunters (carrying the magehunter staff) as casters every ~5s,
// so jar-spawned Serens cast real spells without any manual tagging.
let AH_castTagTick = 0
ServerEvents.tick((event) => {
  AH_castTagTick++
  if (AH_castTagTick % 100 !== 0) return
  try { event.server.runCommandSilent(`tag @e[type=customnpcs:customnpc,tag=ar_ai_hunter,nbt={HandItems:[{id:"irons_spellbooks:magehunter"}]}] add ar_ai_caster`) } catch (e) {}
})

// ---- apply a rank to a hunter: gear + stats + tags + nameplate ----------
function ahApplyRank(entity, rank) {
  var d = AH_RANKDATA[rank]; if (!d) return
  var s = entity.server, u = entity.uuid.toString()
  // rank tags
  AH_RANKS.forEach((r) => s.runCommandSilent(`tag ${u} remove ar_ai_rank_${r}`))
  s.runCommandSilent(`tag ${u} add ar_ai_rank_${rank}`)
  // gear: write the CustomNPCs (Weapons/Armor slot arrays) AND vanilla
  // (HandItems/ArmorItems) inventories so the NPC renders the new loadout.
  // Format mirrors the jar's spawn_<name> functions. Drop chances 0 = no farming.
  var gear = `{Weapons:[{Slot:0,id:"${d.main}",Count:1b},{Slot:2,id:"${d.off}",Count:1b}],` +
    `Armor:[{Slot:2,id:"${d.chest}",Count:1b},{Slot:3,id:"${d.head}",Count:1b}],` +
    `HandItems:[{id:"${d.main}",Count:1b},{id:"${d.off}",Count:1b}],` +
    `ArmorItems:[{},{},{id:"${d.chest}",Count:1b},{id:"${d.head}",Count:1b}],` +
    `HandDropChances:[0.0f,0.0f],ArmorDropChances:[0.0f,0.0f,0.0f,0.0f]}`
  s.runCommandSilent(`data merge entity ${u} ${gear}`)
  // stats
  s.runCommandSilent(`attribute ${u} minecraft:generic.max_health base set ${d.hp}`)
  s.runCommandSilent(`execute as ${u} run data merge entity @s {Health:${d.hp}.0f,PersistenceRequired:1b}`)
  if (d.str > 0) s.runCommandSilent(`effect give ${u} minecraft:strength 999999 ${d.str} true`)
  if (d.res > 0) s.runCommandSilent(`effect give ${u} minecraft:resistance 999999 ${d.res} true`)
  s.runCommandSilent(`effect give ${u} minecraft:instant_health 1 4 true`)
  // stored data so the CustomNPCs identity script renders the new rank/level
  s.runCommandSilent(`data merge entity ${u} {ForgeData:{CNPCStoredData:{ar_rank:"${d.label}",ar_level:"${d.lvl}",ar_growth_stage:"${AH_RANKS.indexOf(rank) + 1}"}}}`)
  // caster flag tag for the magic layer
  if (d.caster) s.runCommandSilent(`tag ${u} add ar_ai_caster`); else s.runCommandSilent(`tag ${u} remove ar_ai_caster`)
}

// ---- REAL Iron's Spellbooks casting (caster hunters) -------------------
// Loads the IS API lazily (same pattern the mana HUD uses). Casts as a MOB so
// no player mana is required. Falls back to a vanilla arcane burst if the API
// shape differs on this IS build. Spell pool + level scale by rank.
let AH_IS_SpellRegistry = null, AH_IS_MagicData = null, AH_IS_CastSource = null, AH_IS_RL = null, AH_IS_ready = null
function ahLoadIS() {
  if (AH_IS_ready !== null) return AH_IS_ready
  try {
    AH_IS_SpellRegistry = Java.loadClass("io.redspace.ironsspellbooks.api.registry.SpellRegistry")
    AH_IS_MagicData = Java.loadClass("io.redspace.ironsspellbooks.api.magic.MagicData")
    AH_IS_CastSource = Java.loadClass("io.redspace.ironsspellbooks.api.spells.CastSource")
    AH_IS_RL = Java.loadClass("net.minecraft.resources.ResourceLocation")
    AH_IS_ready = true
  } catch (e) { AH_IS_ready = false; console.warn("[Ascendant Hunters] Iron's Spells API not reachable; casters use fallback FX: " + e) }
  return AH_IS_ready
}
const AH_SPELLS = {
  b_rank: { lvl: 2, pool: ["irons_spellbooks:magic_missile", "irons_spellbooks:fireball", "irons_spellbooks:icicle"] },
  a_rank: { lvl: 4, pool: ["irons_spellbooks:fireball", "irons_spellbooks:firebolt", "irons_spellbooks:icicle"] },
  s_rank: { lvl: 6, pool: ["irons_spellbooks:fireball", "irons_spellbooks:magic_missile"] }
}
function ahResolveSpell(spellId) {
  try { if (AH_IS_SpellRegistry.getSpell) return AH_IS_SpellRegistry.getSpell(spellId) } catch (e) {}
  try { return AH_IS_SpellRegistry.getSpell(AH_IS_RL.tryParse ? AH_IS_RL.tryParse(spellId) : new AH_IS_RL(spellId)) } catch (e) {}
  return null
}
function ahNewMagicData() {
  try { return new AH_IS_MagicData(false) } catch (e) {}
  try { return new AH_IS_MagicData() } catch (e) {}
  return null
}
function ahCastSpell(caster, victim, rank) {
  if (!ahLoadIS()) return false
  var conf = AH_SPELLS[rank]; if (!conf) return false
  try {
    var spellId = conf.pool[Math.floor(Math.random() * conf.pool.length)]
    var spell = ahResolveSpell(spellId); if (!spell) return false
    var md = ahNewMagicData(); if (!md) return false
    var s = caster.server, au = caster.uuid.toString(), vu = victim.uuid.toString()
    s.runCommandSilent(`execute as ${au} run tp ${au} ~ ~ ~ facing entity ${vu} eyes`)
    spell.onCast(caster.level, conf.lvl, caster, AH_IS_CastSource.MOB, md)
    return true
  } catch (e) {
    if (!global.__ahCastWarned) { console.warn("[Ascendant Hunters] IS onCast failed once (using fallback FX): " + e); global.__ahCastWarned = true }
    return false
  }
}
function ahArcaneBurstFallback(attacker, victim) {
  var s = attacker.server, vu = victim.uuid.toString()
  s.runCommandSilent(`execute at ${vu} run summon minecraft:evoker_fangs ~ ~ ~`)
  s.runCommandSilent(`execute at ${vu} run particle minecraft:enchant ~ ~1 ~ 0.6 0.8 0.6 1 30`)
  s.runCommandSilent(`execute at ${attacker.uuid.toString()} run playsound minecraft:entity.illusioner.cast_spell hostile @a[distance=..32] ~ ~ ~ 0.8 1.0`)
}

// ---- KILL-DRIVEN LEVELING ----------------------------------------------
EntityEvents.death((event) => {
  try {
    var killer = ahFindKiller(event.source)
    if (!ahIsHunter(killer)) return
    var rank = ahRankOf(killer); if (!rank) return
    var gain = ahRenownForVictim(event.entity); if (gain <= 0) return
    var s = killer.server, u = killer.uuid.toString()
    s.runCommandSilent(`scoreboard players add ${u} ${AH_RENOWN_OBJ} ${gain}`)
    var need = AH_RENOWN_TO_NEXT[rank]
    if (need === undefined) return // s_rank = cap, keep farming renown for show
    var have = s.runCommandSilent(`scoreboard players get ${u} ${AH_RENOWN_OBJ}`)
    if (have < need) return
    // ascend one rank
    s.runCommandSilent(`scoreboard players set ${u} ${AH_RENOWN_OBJ} 0`)
    var next = AH_RANKS[AH_RANKS.indexOf(rank) + 1]
    ahApplyRank(killer, next)
    var nd = AH_RANKDATA[next]
    s.runCommandSilent(`execute at ${u} run particle minecraft:totem_of_undying ~ ~1 ~ 0.6 1 0.6 0.2 60`)
    s.runCommandSilent(`execute at ${u} run playsound minecraft:ui.toast.challenge_complete neutral @a[distance=..40] ~ ~ ~ 0.7 0.9`)
    s.runCommandSilent(`execute at ${u} run title @a[distance=..40] actionbar [{"text":"A hunter has ascended to ","color":"gray"},{"text":"${nd.label}","color":"${next === 's_rank' ? 'light_purple' : (next === 'a_rank' ? 'yellow' : 'gold')}","bold":true}]`)
  } catch (e) {
    if (!global.__ahDeathWarned) { console.warn("[Ascendant Hunters] kill-leveling skipped once: " + e); global.__ahDeathWarned = true }
  }
})

// ---- CASTER MAGIC v1 ----------------------------------------------------
// Hunters carrying the arcanist loadout (ar_ai_caster, set when promoted to
// B-rank) get a spell proc when they strike a living target: an erupting
// arcane burst at the victim. Reliable + vanilla-safe. v2 path: swap the
// evoker_fangs proc for a real Iron's Spellbooks cast via its API / a
// spellcasting entity once we confirm the exact spell ids in-game.
EntityEvents.hurt((event) => {
  try {
    var attacker = ahFindKiller(event.source)
    if (!attacker || !attacker.tags || !attacker.tags.contains("ar_ai_caster")) return
    if (!ahIsHunter(attacker)) return
    if (Math.random() > 0.28) return
    var victim = event.entity; if (!victim) return
    // Real Iron's Spellbooks cast (rank-scaled); arcane-burst fallback if the API differs.
    var rank = ahRankOf(attacker) || "b_rank"
    if (!ahCastSpell(attacker, victim, rank)) ahArcaneBurstFallback(attacker, victim)
  } catch (e) {
    if (!global.__ahHurtWarned) { console.warn("[Ascendant Hunters] caster proc skipped once: " + e); global.__ahHurtWarned = true }
  }
})

// Manual test (no custom command needed):
//   /aschunter spawn_near d_rank   - spawn a low hunter
//   let it fight (or /summon zombies near it); after ~8 renown it ascends to
//   C-rank with new gear, then keeps climbing. /aschunterx not used to keep
//   this script dependency-free and robust on reload.
