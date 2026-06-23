// ============================================================
//  Ascendant Guild Jobs - PHASE 2 (work tick) + PHASE 3 (breadth)
//  Companion to ascendant_guild_director.js (Phase 1 recruit loop).
//  Coupling is world-state only (entity tags + persistentData), never JS scope.
//
//  Phase 2 - the work tick:
//    An employed specialist bound to a storage chest pulls inputs and forges a
//    REAL MODDED output, gated by a per-NPC skill that rises with every craft.
//  Phase 3 - breadth:
//    5 professions (blacksmith / arcanist / cook / healer / courier), each with a
//    themed loadout + skill-gated modded recipe ladder; random traits that modify
//    work speed + skill gain; physical far-recruitment via /ascjob scout; auto-labeling.
//
//  Commands (separate /ascjob tree - no clash with /ascguild):
//    /ascjob spawn   <prof>   - place a recruitable specialist at your feet (quick test)
//    /ascjob scout   <prof>   - send out a lead; specialist appears out in the world to go find
//    /ascjob locate           - point to the nearest recruitable you haven't hired yet
//    /ascjob setstation       - bind your nearest guild member to the nearest chest (their forge)
//    /ascjob assign  <prof>   - re-profession your nearest guild member
//    /ascjob status           - what every member of yours is doing right now
//  Recruiting is still /ascguild recruit (profession-agnostic - works on any spawned specialist).
// ============================================================

const AGJ_S = String.fromCharCode(0xA7) // section sign for color codes (SNBT-safe)
const AGJ_WORK_INTERVAL = 100            // ticks between work pulses (5s)

// ---- professions: themed gear + a skill-gated ladder of REAL modded outputs ----
// All output IDs are sourced from config/ascendant_guild/npc_loadouts.json (registry-verified).
const AGJ_PROFESSIONS = {
  guild_blacksmith: {
    cmd: "blacksmith", name: "Blacksmith", color: "6",
    gear: { main: "minecraft:iron_axe", head: "immersive_armors:steampunk_helmet", chest: "immersive_armors:steampunk_chestplate" },
    work: "Forging", particle: "minecraft:crit",
    recipes: [
      { min: 0,  inp: [["minecraft:iron_ingot", 3]],                              out: "minecraft:iron_sword",                    n: 1, cyc: 2, xp: 2, label: "Iron Sword" },
      { min: 6,  inp: [["minecraft:iron_ingot", 5], ["minecraft:coal", 2]],       out: "immersive_armors:steampunk_chestplate",   n: 1, cyc: 3, xp: 3, label: "Steampunk Chestplate" },
      { min: 14, inp: [["minecraft:iron_ingot", 6], ["minecraft:coal", 3]],       out: "simplyswords:iron_longsword",             n: 1, cyc: 3, xp: 4, label: "Iron Longsword" },
      { min: 22, inp: [["minecraft:iron_ingot", 4], ["minecraft:diamond", 1]],    out: "immersive_armors:warrior_chestplate",     n: 1, cyc: 4, xp: 5, label: "Warrior Chestplate" },
      { min: 32, inp: [["minecraft:netherite_ingot", 1], ["minecraft:iron_ingot", 4]], out: "simplyswords:netherite_rapier",     n: 1, cyc: 5, xp: 7, label: "Netherite Rapier" }
    ]
  },
  guild_arcanist: {
    cmd: "arcanist", name: "Arcanist", color: "d",
    gear: { main: "irons_spellbooks:graybeard_staff", off: "irons_spellbooks:diamond_spell_book", head: "irons_spellbooks:archevoker_helmet", chest: "irons_spellbooks:archevoker_chestplate" },
    work: "Scribing", particle: "minecraft:enchant",
    recipes: [
      { min: 0,  inp: [["minecraft:paper", 3], ["minecraft:lapis_lazuli", 2]],    out: "irons_spellbooks:artificer_cane",         n: 1, cyc: 2, xp: 2, label: "Artificer's Cane" },
      { min: 10, inp: [["minecraft:paper", 4], ["minecraft:gold_ingot", 2]],      out: "irons_spellbooks:graybeard_staff",        n: 1, cyc: 3, xp: 3, label: "Graybeard Staff" },
      { min: 20, inp: [["minecraft:book", 1], ["minecraft:diamond", 2]],          out: "irons_spellbooks:diamond_spell_book",     n: 1, cyc: 4, xp: 5, label: "Enchanted Spell Book" }
    ]
  },
  guild_cook: {
    cmd: "cook", name: "Cook", color: "e",
    gear: { main: "minecraft:golden_carrot", head: "artifacts:novelty_drinking_hat", chest: "immersive_armors:robe_chestplate" },
    work: "Cooking", particle: "minecraft:happy_villager",
    recipes: [
      { min: 0,  inp: [["minecraft:wheat", 3]],                                   out: "minecraft:bread",                         n: 2, cyc: 1, xp: 1, label: "Bread" },
      { min: 5,  inp: [["minecraft:carrot", 1], ["minecraft:gold_ingot", 1]],     out: "minecraft:golden_carrot",                 n: 1, cyc: 2, xp: 2, label: "Golden Carrot" },
      { min: 12, inp: [["minecraft:pumpkin", 1], ["minecraft:sugar", 1], ["minecraft:egg", 1]], out: "minecraft:pumpkin_pie",      n: 1, cyc: 2, xp: 2, label: "Pumpkin Pie" }
    ]
  },
  guild_healer: {
    cmd: "healer", name: "Healer", color: "a",
    gear: { main: "irons_spellbooks:artificer_cane", head: "artifacts:villager_hat", chest: "immersive_armors:robe_chestplate" },
    work: "Mending", particle: "minecraft:heart",
    recipes: [
      { min: 0,  inp: [["minecraft:apple", 1], ["minecraft:gold_ingot", 2]],      out: "minecraft:golden_apple",                  n: 1, cyc: 3, xp: 3, label: "Golden Apple" },
      { min: 12, inp: [["minecraft:golden_carrot", 2], ["minecraft:glowstone_dust", 2]], out: "minecraft:golden_apple",           n: 2, cyc: 3, xp: 4, label: "Golden Apples" }
    ]
  },
  guild_courier: {
    cmd: "courier", name: "Courier", color: "b",
    gear: { main: "minecraft:filled_map", head: "artifacts:night_vision_goggles", chest: "immersive_armors:prismarine_chestplate" },
    work: "Trading", particle: "minecraft:happy_villager",
    recipes: [
      { min: 0,  inp: [["minecraft:wheat", 6]],                                   out: "minecraft:emerald",                       n: 1, cyc: 3, xp: 2, label: "Crop Sale" },
      { min: 8,  inp: [["minecraft:leather", 4]],                                 out: "minecraft:emerald",                       n: 2, cyc: 4, xp: 3, label: "Goods Run" },
      { min: 18, inp: [["minecraft:emerald", 4]],                                 out: "minecraft:ender_pearl",                   n: 1, cyc: 4, xp: 4, label: "Rare Acquisition" }
    ]
  }
}

// ---- traits: random on spawn, modify work speed + skill gain ----
const AGJ_TRAITS = {
  master:   { name: "Master",   workMul: 0.6, xpMul: 1.5, weight: 1 },
  gifted:   { name: "Gifted",   workMul: 0.9, xpMul: 1.6, weight: 2 },
  diligent: { name: "Diligent", workMul: 0.8, xpMul: 1.2, weight: 3 },
  steady:   { name: "Steady",   workMul: 1.0, xpMul: 1.0, weight: 6 },
  lazy:     { name: "Lazy",     workMul: 1.4, xpMul: 0.8, weight: 3 }
}

function agjPickTrait() {
  var total = 0, k
  for (k in AGJ_TRAITS) total += AGJ_TRAITS[k].weight
  var r = Math.random() * total
  for (k in AGJ_TRAITS) { r -= AGJ_TRAITS[k].weight; if (r <= 0) return k }
  return "steady"
}

// ---- gear NBT (CustomNPCs format, mirrors the hunter loadout system) ----
function agjGearNbt(g) {
  var main = g.main || "minecraft:air"
  var off = g.off ? '{id:"' + g.off + '",Count:1b}' : '{}'
  var chest = g.chest || "minecraft:air"
  var head = g.head || "minecraft:air"
  var weapons = 'Weapons:[{Slot:0,id:"' + main + '",Count:1b}' + (g.off ? ',{Slot:1,id:"' + g.off + '",Count:1b}' : '') + ']'
  var armor = 'Armor:[{Slot:2,id:"' + chest + '",Count:1b},{Slot:3,id:"' + head + '",Count:1b}]'
  var hands = 'HandItems:[{id:"' + main + '",Count:1b},' + off + ']'
  var armorItems = 'ArmorItems:[{},{},{id:"' + chest + '",Count:1b},{id:"' + head + '",Count:1b}]'
  return weapons + ',' + armor + ',' + hands + ',' + armorItems + ',HandDropChances:[0.0f,0.0f],ArmorDropChances:[0.0f,0.0f,0.0f,0.0f]'
}

function agjRecruitNbt(pid, trait) {
  var P = AGJ_PROFESSIONS[pid]
  var name = AGJ_S + P.color + "[Recruit] " + AGJ_S + "f" + P.name + " " + AGJ_S + "8| " + AGJ_S + "7" + AGJ_TRAITS[trait].name
  return '{Name:"' + name + '",ShowName:1,Title:"",PersistenceRequired:1b,' + agjGearNbt(P.gear) + ',' +
    'Tags:["ar_recruitable","ar_guild_npc","ar_profile_' + pid + '","ar_trait_' + trait + '"],' +
    'ForgeData:{CNPCStoredData:{ar_profile:"' + pid + '",ar_trait:"' + trait + '",ar_recruitable:"true",ar_contract_item:"minecraft:iron_ingot",ar_contract_count:"10"}}}'
}

// ---- tag readers ----
function agjTagWith(npc, prefix) {
  try {
    var it = npc.tags.iterator()
    while (it.hasNext()) { var t = it.next(); if (t.indexOf(prefix) === 0) return t.substring(prefix.length) }
  } catch (e) {}
  return null
}
function agjProfOf(npc) { return agjTagWith(npc, "ar_profile_") }
function agjTraitOf(npc) { return agjTagWith(npc, "ar_trait_") || "steady" }

// ---- inventory helpers (KubeJS block.inventory IItemHandler wrapper) ----
function agjInv(level, x, y, z) {
  try { var b = level.getBlock(x, y, z); var inv = b ? b.inventory : null; return (inv && inv.getSlots() > 0) ? inv : null } catch (e) { return null }
}
function agjItemMatch(stack, id) {
  try { return !stack.isEmpty() && stack.getItem() === Item.of(id).getItem() } catch (e) { return false }
}
function agjCount(inv, id) {
  var n = 0
  for (var i = 0; i < inv.getSlots(); i++) { var s = inv.getStackInSlot(i); if (agjItemMatch(s, id)) n += s.getCount() }
  return n
}
function agjConsume(inv, id, need) {
  for (var i = 0; i < inv.getSlots() && need > 0; i++) {
    var s = inv.getStackInSlot(i)
    if (agjItemMatch(s, id)) { var take = Math.min(need, s.getCount()); inv.extractItem(i, take, false); need -= take }
  }
  return need <= 0
}
function agjHasAll(inv, recipe) {
  for (var i = 0; i < recipe.inp.length; i++) { if (agjCount(inv, recipe.inp[i][0]) < recipe.inp[i][1]) return false }
  return true
}
function agjOutput(level, sx, sy, sz, npcUuid, id, count, server) {
  var inv = agjInv(level, sx, sy, sz)
  var stack = Item.of(id, count)
  if (inv) { for (var i = 0; i < inv.getSlots() && !stack.isEmpty(); i++) { stack = inv.insertItem(i, stack, false) } }
  if (!stack.isEmpty()) { server.runCommandSilent('execute as ' + npcUuid + ' at @s run summon item ~ ~1 ~ {Item:{id:"' + id + '",Count:' + stack.getCount() + 'b}}') }
  return true
}

// ---- best recipe the NPC's skill allows AND whose inputs are present ----
function agjBestRecipe(prof, skill, inv) {
  var best = null
  for (var i = 0; i < prof.recipes.length; i++) {
    var r = prof.recipes[i]
    if (skill >= r.min && agjHasAll(inv, r)) { if (!best || r.min > best.min) best = r }
  }
  return best
}

// ---- ownership / station scans ----
function agjOwnedMembers(p, radius) {
  try {
    return p.level.getEntitiesWithin(p.getBoundingBox().inflate(radius)).filter((e) => {
      try { return e.tags.contains("ar_guild_member") && e.tags.contains("ar_owner_" + p.username) } catch (err) { return false }
    })
  } catch (e) { return [] }
}
function agjNearestRecruitable(p, radius) {
  var best = null, bd = 1e9
  try {
    p.level.getEntitiesWithin(p.getBoundingBox().inflate(radius)).forEach((e) => {
      try {
        if (!e.tags.contains("ar_recruitable")) return
        var dx = e.x - p.x, dz = e.z - p.z, d = Math.sqrt(dx * dx + dz * dz)
        if (d < bd) { bd = d; best = e }
      } catch (err) {}
    })
  } catch (e) {}
  return best
}
function agjNearestChest(p, radius) {
  var px = Math.floor(p.x), py = Math.floor(p.y), pz = Math.floor(p.z)
  var best = null, bd = 1e9
  for (var dx = -radius; dx <= radius; dx++) for (var dy = -3; dy <= 3; dy++) for (var dz = -radius; dz <= radius; dz++) {
    try {
      var b = p.level.getBlock(px + dx, py + dy, pz + dz)
      var id = b ? String(b.id) : ""
      if (id === "minecraft:chest" || id === "minecraft:barrel" || id === "minecraft:trapped_chest") {
        var d = dx * dx + dy * dy + dz * dz
        if (d < bd) { bd = d; best = { x: px + dx, y: py + dy, z: pz + dz, id: id } }
      }
    } catch (e) {}
  }
  return best
}

// ---- labeling ----
function agjLabel(npc, server) {
  try {
    var pid = agjProfOf(npc); if (!pid || !AGJ_PROFESSIONS[pid]) return
    var P = AGJ_PROFESSIONS[pid], tr = AGJ_TRAITS[agjTraitOf(npc)]
    var skill = npc.persistentData.getInt("ar_skill")
    var nm = AGJ_S + "a[Guild] " + AGJ_S + P.color + P.name + " " + AGJ_S + "8| " + AGJ_S + "7" + tr.name + " " + AGJ_S + "8Lv" + AGJ_S + "f" + skill
    server.runCommandSilent('data merge entity ' + npc.uuid.toString() + ' {Name:"' + nm + '"}')
    npc.persistentData.putByte("ar_labeled", 1)
  } catch (e) {}
}

// ============================================================
//  COMMANDS  (/ascjob ...)
// ============================================================
function agjSpawn(source, pid) {
  var p = source.player; if (!p) return 0
  var P = AGJ_PROFESSIONS[pid]; if (!P) { p.tell(Text.red("Unknown profession.")); return 0 }
  var trait = agjPickTrait()
  var r = p.server.runCommandSilent('execute as ' + p.username + ' at @s run summon customnpcs:customnpc ~ ~ ~ ' + agjRecruitNbt(pid, trait))
  if (r > 0) {
    p.tell(Text.gold("A " + P.name + " (" + AGJ_TRAITS[trait].name + ") spawned at your feet. ").append(Text.yellow("/ascguild recruit")).append(Text.gold(" to hire (10x Iron Ingot), then ")).append(Text.yellow("/ascjob setstation")).append(Text.gold(" by a chest.")))
  } else { p.tell(Text.red("Spawn FAILED (summon returned " + r + ") - tell Claude.")) }
  return r > 0 ? 1 : 0
}

function agjScout(source, pid) {
  var p = source.player; if (!p) return 0
  var P = AGJ_PROFESSIONS[pid]; if (!P) { p.tell(Text.red("Unknown profession.")); return 0 }
  var trait = agjPickTrait()
  var dirs = [["north", 0, -1], ["east", 1, 0], ["south", 0, 1], ["west", -1, 0], ["northeast", 1, -1], ["southeast", 1, 1], ["southwest", -1, 1], ["northwest", -1, -1]]
  var d = dirs[Math.floor(Math.random() * dirs.length)]
  var dist = 48 + Math.floor(Math.random() * 40) // 48..88 blocks - inside render so chunks load
  var tx = Math.floor(p.x) + d[1] * dist, tz = Math.floor(p.z) + d[2] * dist, ty = Math.floor(p.y)
  var r = p.server.runCommandSilent('execute positioned ' + tx + ' ' + ty + ' ' + tz + ' run summon customnpcs:customnpc ~ ~ ~ ' + agjRecruitNbt(pid, trait))
  if (r > 0) {
    p.tell(Text.gold("Lead: a wandering " + P.name + " (" + AGJ_TRAITS[trait].name + ") was spotted ~" + dist + " blocks " + d[0] + " (near " + tx + " " + ty + " " + tz + "). Travel there and ").append(Text.yellow("/ascguild recruit")).append(Text.gold(". ")).append(Text.gray("/ascjob locate")).append(Text.gold(" to home in.")))
  } else { p.tell(Text.red("Scout FAILED (summon returned " + r + ") - tell Claude.")) }
  return r > 0 ? 1 : 0
}

function agjLocate(source) {
  var p = source.player; if (!p) return 0
  var e = agjNearestRecruitable(p, 256)
  if (!e) { p.tell(Text.red("No recruitable specialist within 256 blocks. Use /ascjob scout <prof> for a lead.")); return 0 }
  var dx = e.x - p.x, dz = e.z - p.z, dist = Math.round(Math.sqrt(dx * dx + dz * dz))
  var dir = (Math.abs(dx) > Math.abs(dz)) ? (dx > 0 ? "east" : "west") : (dz > 0 ? "south" : "north")
  p.tell(Text.gold("Nearest recruit: ~" + dist + " blocks " + dir + " (" + Math.floor(e.x) + " " + Math.floor(e.y) + " " + Math.floor(e.z) + ")."))
  return 1
}

function agjSetStation(source) {
  var p = source.player; if (!p) return 0
  var mem = agjOwnedMembers(p, 12)
  if (mem.length === 0) { p.tell(Text.red("No guild member of yours within 12 blocks. Stand near the one you want to station.")); return 0 }
  var npc = mem[0], bd = 1e9
  mem.forEach((m) => { var dx = m.x - p.x, dz = m.z - p.z, d = dx * dx + dz * dz; if (d < bd) { bd = d; npc = m } })
  var chest = agjNearestChest(p, 6)
  if (!chest) { p.tell(Text.red("No chest/barrel within 6 blocks. Place one and stand by it.")); return 0 }
  var pd = npc.persistentData
  pd.putInt("ar_station_x", chest.x); pd.putInt("ar_station_y", chest.y); pd.putInt("ar_station_z", chest.z)
  var u = npc.uuid.toString()
  p.server.runCommandSilent("tag " + u + " add ar_stationed")
  p.server.runCommandSilent("tag " + u + " remove ar_guild_escorting")
  p.server.runCommandSilent("tag " + u + " add ar_guild_home")
  var pid = agjProfOf(npc), pn = (pid && AGJ_PROFESSIONS[pid]) ? AGJ_PROFESSIONS[pid].name : "Member"
  p.tell(Text.green("Stationed your " + pn + " at the " + chest.id.replace("minecraft:", "") + " (" + chest.x + " " + chest.y + " " + chest.z + "). Stock it with inputs and they'll start working."))
  return 1
}

function agjAssign(source, pid) {
  var p = source.player; if (!p) return 0
  var P = AGJ_PROFESSIONS[pid]; if (!P) { p.tell(Text.red("Unknown profession.")); return 0 }
  var mem = agjOwnedMembers(p, 8)
  if (mem.length === 0) { p.tell(Text.red("No guild member of yours within 8 blocks.")); return 0 }
  var npc = mem[0], bd = 1e9
  mem.forEach((m) => { var dx = m.x - p.x, dz = m.z - p.z, d = dx * dx + dz * dz; if (d < bd) { bd = d; npc = m } })
  var u = npc.uuid.toString(), old = agjProfOf(npc)
  if (old) p.server.runCommandSilent("tag " + u + " remove ar_profile_" + old)
  p.server.runCommandSilent("tag " + u + " add ar_profile_" + pid)
  p.server.runCommandSilent('data merge entity ' + u + ' {' + agjGearNbt(P.gear) + '}')
  npc.persistentData.putByte("ar_labeled", 0)
  agjLabel(npc, p.server)
  p.tell(Text.green("Reassigned your member to " + P.name + "."))
  return 1
}

function agjStatus(source) {
  var p = source.player; if (!p) return 0
  var mem = agjOwnedMembers(p, 96)
  p.tell(Text.gold("=== " + p.username + "'s Guild Workforce (" + mem.length + " nearby) ==="))
  if (mem.length === 0) { p.tell(Text.gray("None within 96 blocks. Recruit with /ascjob spawn <prof> + /ascguild recruit.")); return 1 }
  mem.forEach((npc) => {
    try {
      var pid = agjProfOf(npc), P = (pid && AGJ_PROFESSIONS[pid]) ? AGJ_PROFESSIONS[pid] : null
      var pd = npc.persistentData, skill = pd.getInt("ar_skill"), tr = AGJ_TRAITS[agjTraitOf(npc)]
      var nm = P ? P.name : "Member"
      var stationed = npc.tags.contains("ar_stationed")
      var doing
      if (pd.getInt("ar_craft_left") > 0) doing = (P ? P.work : "Working") + " " + pd.getString("ar_craft_label") + " (" + pd.getInt("ar_craft_left") + " left)"
      else if (!stationed) doing = "idle - needs /ascjob setstation"
      else doing = "waiting for materials"
      p.tell(Text.white("- " + nm + " ").append(Text.gray("[" + tr.name + ", Lv" + skill + "] ")).append(Text.yellow(doing)))
    } catch (e) {}
  })
  return 1
}

ServerEvents.commandRegistry((event) => {
  const Commands = event.commands
  var spawnNode = Commands.literal("spawn")
  var scoutNode = Commands.literal("scout")
  var assignNode = Commands.literal("assign")
  Object.keys(AGJ_PROFESSIONS).forEach((pid) => {
    var c = AGJ_PROFESSIONS[pid].cmd
    spawnNode.then(Commands.literal(c).executes((ctx) => agjSpawn(ctx.source, pid)))
    scoutNode.then(Commands.literal(c).executes((ctx) => agjScout(ctx.source, pid)))
    assignNode.then(Commands.literal(c).executes((ctx) => agjAssign(ctx.source, pid)))
  })
  event.register(
    Commands.literal("ascjob")
      .requires((src) => src.hasPermission(0))
      .then(spawnNode)
      .then(scoutNode)
      .then(assignNode)
      .then(Commands.literal("locate").executes((ctx) => agjLocate(ctx.source)))
      .then(Commands.literal("setstation").executes((ctx) => agjSetStation(ctx.source)))
      .then(Commands.literal("status").executes((ctx) => agjStatus(ctx.source)))
  )
})

// ============================================================
//  THE WORK TICK
// ============================================================
let AGJ_tick = 0
ServerEvents.tick((event) => {
  AGJ_tick++
  if (AGJ_tick % AGJ_WORK_INTERVAL !== 0) return
  var server = event.server
  try {
    server.players.forEach((p) => {
      var members = agjOwnedMembers(p, 64).filter((e) => { try { return e.tags.contains("ar_stationed") } catch (err) { return false } })
      members.forEach((npc) => {
        try {
          if (npc.persistentData.getByte("ar_labeled") !== 1) agjLabel(npc, server)
          var pid = agjProfOf(npc); var prof = pid ? AGJ_PROFESSIONS[pid] : null; if (!prof) return
          var pd = npc.persistentData
          var sx = pd.getInt("ar_station_x"), sy = pd.getInt("ar_station_y"), sz = pd.getInt("ar_station_z")
          var u = npc.uuid.toString()
          var left = pd.getInt("ar_craft_left")
          if (left > 0) {
            server.runCommandSilent('execute at ' + u + ' run particle ' + prof.particle + ' ~ ~1.2 ~ 0.3 0.4 0.3 0.02 6')
            left -= 1
            if (left <= 0) {
              var outId = pd.getString("ar_craft_out"), outN = pd.getInt("ar_craft_outn")
              agjOutput(p.level, sx, sy, sz, u, outId, outN, server)
              var gain = Math.max(1, Math.round(pd.getInt("ar_craft_xp") * AGJ_TRAITS[agjTraitOf(npc)].xpMul))
              var ns = pd.getInt("ar_skill") + gain; pd.putInt("ar_skill", ns)
              pd.putInt("ar_craft_left", 0); pd.putByte("ar_labeled", 0)
              server.runCommandSilent('execute at ' + u + ' run playsound minecraft:block.anvil.use neutral @a[distance=..24] ~ ~ ~ 0.5 1.4')
              p.tell(Text.green("Your " + prof.name + " finished a ").append(Text.white(pd.getString("ar_craft_label"))).append(Text.green(" (skill -> " + ns + ").")))
            } else { pd.putInt("ar_craft_left", left) }
            return
          }
          var inv = agjInv(p.level, sx, sy, sz); if (!inv) return
          var skill = pd.getInt("ar_skill")
          var recipe = agjBestRecipe(prof, skill, inv); if (!recipe) return
          for (var i = 0; i < recipe.inp.length; i++) agjConsume(inv, recipe.inp[i][0], recipe.inp[i][1])
          var cyc = Math.max(1, Math.round(recipe.cyc * AGJ_TRAITS[agjTraitOf(npc)].workMul))
          pd.putInt("ar_craft_left", cyc); pd.putString("ar_craft_out", recipe.out); pd.putInt("ar_craft_outn", recipe.n)
          pd.putInt("ar_craft_xp", recipe.xp); pd.putString("ar_craft_label", recipe.label)
          server.runCommandSilent('execute at ' + u + ' run playsound minecraft:block.smithing_table.use neutral @a[distance=..24] ~ ~ ~ 0.5 1')
          if (!global.__agjWorkProven) { console.info("[Ascendant Guild Jobs] First craft started: " + prof.name + " -> " + recipe.label); global.__agjWorkProven = true }
        } catch (e2) { if (!global.__agjMemberWarned) { console.warn("[Ascendant Guild Jobs] member tick skipped: " + e2); global.__agjMemberWarned = true } }
      })
    })
  } catch (e) { if (!global.__agjTickWarned) { console.warn("[Ascendant Guild Jobs] work tick skipped once: " + e); global.__agjTickWarned = true } }
})

ServerEvents.loaded((event) => {
  console.info("[Ascendant Guild Jobs] v2/v3 loaded - 5 professions, work tick every " + AGJ_WORK_INTERVAL + " ticks (/ascjob spawn|scout|locate|setstation|assign|status).")
})
