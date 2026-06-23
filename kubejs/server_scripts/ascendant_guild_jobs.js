// ============================================================
//  Ascendant Guild Jobs - logistics work loop (v2)
//  Workers run a physical loop: storage -> pull inputs -> walk to their
//  profession workstation -> craft -> walk back -> deposit product.
//  Storage = chests you bind one-by-one (right-click). Workstation = the
//  exact profession-appropriate block you right-click. Never radius.
//
//  Commands (/ascjob ...):
//    spawn <prof> | scout <prof> | locate | assign <prof> | status
//    setworkstation  - bind your nearest worker to the block you right-click next
//    storage         - toggle storage mode; right-click chests to add them
//    storage clear | storage list
// ============================================================

const AGJ_S = String.fromCharCode(0xA7)
const AGJ_TICK = 20          // game ticks between work steps (1s)
const AGJ_SPEED = 0.6
const AGJ_REACH = 2.7        // how close counts as "arrived"
const AGJ_STUCK = 20         // seconds of travel before a teleport-assist

const AGJ_PROFESSIONS = {
  guild_blacksmith: {
    cmd: "blacksmith", name: "Blacksmith", color: "6",
    gear: { main: "", skin: "customnpcs:textures/entity/dwarfmale/dwarf_blacksmith.png" },
    work: "Forging", particle: "minecraft:crit",
    recipes: [
      { min: 0,  inp: [["minecraft:iron_ingot", 3]],                              out: "minecraft:iron_sword",                  n: 1, cyc: 2, xp: 2, label: "Iron Sword" },
      { min: 2,  inp: [["minecraft:iron_ingot", 5], ["minecraft:coal", 2]],       out: "immersive_armors:steampunk_chestplate", n: 1, cyc: 3, xp: 3, label: "Steampunk Chestplate" },
      { min: 4, inp: [["minecraft:iron_ingot", 6], ["minecraft:coal", 3]],       out: "simplyswords:iron_longsword",           n: 1, cyc: 3, xp: 4, label: "Iron Longsword" },
      { min: 6, inp: [["minecraft:iron_ingot", 4], ["minecraft:diamond", 1]],    out: "immersive_armors:warrior_chestplate",   n: 1, cyc: 4, xp: 5, label: "Warrior Chestplate" },
      { min: 9, inp: [["minecraft:netherite_ingot", 1], ["minecraft:iron_ingot", 4]], out: "simplyswords:netherite_rapier",   n: 1, cyc: 5, xp: 7, label: "Netherite Rapier" }
    ]
  },
  guild_arcanist: {
    cmd: "arcanist", name: "Arcanist", color: "d",
    gear: { main: "irons_spellbooks:graybeard_staff", skin: "customnpcs:textures/entity/humanmale/magesteve.png" },
    work: "Scribing", particle: "minecraft:enchant",
    recipes: [
      { min: 0,  inp: [["minecraft:paper", 3], ["minecraft:lapis_lazuli", 2]],    out: "irons_spellbooks:artificer_cane",       n: 1, cyc: 2, xp: 2, label: "Artificer's Cane" },
      { min: 3, inp: [["minecraft:paper", 4], ["minecraft:gold_ingot", 2]],      out: "irons_spellbooks:graybeard_staff",      n: 1, cyc: 3, xp: 3, label: "Graybeard Staff" },
      { min: 6, inp: [["minecraft:book", 1], ["minecraft:diamond", 2]],          out: "irons_spellbooks:diamond_spell_book",   n: 1, cyc: 4, xp: 5, label: "Enchanted Spell Book" }
    ]
  },
  guild_cook: {
    cmd: "cook", name: "Cook", color: "e",
    gear: { main: "", skin: "customnpcs:textures/entity/humanmale/chefsteve.png" },
    work: "Cooking", particle: "minecraft:happy_villager",
    recipes: [
      { min: 0,  inp: [["minecraft:wheat", 3]],                                   out: "minecraft:bread",         n: 2, cyc: 1, xp: 1, label: "Bread" },
      { min: 2,  inp: [["minecraft:carrot", 1], ["minecraft:gold_ingot", 1]],     out: "minecraft:golden_carrot", n: 1, cyc: 2, xp: 2, label: "Golden Carrot" },
      { min: 4, inp: [["minecraft:pumpkin", 1], ["minecraft:sugar", 1], ["minecraft:egg", 1]], out: "minecraft:pumpkin_pie", n: 1, cyc: 2, xp: 2, label: "Pumpkin Pie" }
    ]
  },
  guild_healer: {
    cmd: "healer", name: "Healer", color: "a",
    gear: { main: "irons_spellbooks:artificer_cane", skin: "customnpcs:textures/entity/humanmale/prieststeve.png" },
    work: "Mending", particle: "minecraft:heart",
    recipes: [
      { min: 0,  inp: [["minecraft:apple", 1], ["minecraft:gold_ingot", 2]],      out: "minecraft:golden_apple", n: 1, cyc: 3, xp: 3, label: "Golden Apple" },
      { min: 4, inp: [["minecraft:golden_carrot", 2], ["minecraft:glowstone_dust", 2]], out: "minecraft:golden_apple", n: 2, cyc: 3, xp: 4, label: "Golden Apples" }
    ]
  },
  guild_courier: {
    cmd: "courier", name: "Courier", color: "b",
    gear: { main: "minecraft:filled_map", skin: "customnpcs:textures/entity/humanmale/mailmansteve.png" },
    work: "Trading", particle: "minecraft:happy_villager",
    recipes: [
      { min: 0,  inp: [["minecraft:wheat", 6]],   out: "minecraft:emerald",     n: 1, cyc: 3, xp: 2, label: "Crop Sale" },
      { min: 3,  inp: [["minecraft:leather", 4]], out: "minecraft:emerald",     n: 2, cyc: 4, xp: 3, label: "Goods Run" },
      { min: 6, inp: [["minecraft:emerald", 4]], out: "minecraft:ender_pearl", n: 1, cyc: 4, xp: 4, label: "Rare Acquisition" }
    ]
  }
}

// profession -> acceptable workstation blocks
const AGJ_WORKSTATIONS = {
  guild_blacksmith: ["minecraft:anvil", "minecraft:chipped_anvil", "minecraft:damaged_anvil", "minecraft:smithing_table"],
  guild_arcanist: ["minecraft:enchanting_table", "minecraft:lectern"],
  guild_cook: ["minecraft:furnace", "minecraft:smoker", "minecraft:blast_furnace", "minecraft:campfire", "minecraft:soul_campfire"],
  guild_healer: ["minecraft:brewing_stand", "minecraft:cauldron", "minecraft:water_cauldron"],
  guild_courier: ["minecraft:cartography_table", "minecraft:barrel", "minecraft:lectern", "minecraft:loom"]
}
const AGJ_CONTAINERS = ["minecraft:chest", "minecraft:trapped_chest", "minecraft:barrel"]

// ---- names (deterministic per worker) + leveling curve (slows progression) ----
const AGJ_NAMES = ["Bjorn","Kara","Doran","Mira","Soren","Yara","Hadrin","Vesna","Torsten","Elowen","Garrick","Isolde","Bram","Sable","Corvin","Renna","Aldric","Thora","Magnus","Wrenn","Joran","Lyssa","Edda","Falk","Greta","Hale","Ingmar","Juno","Korin","Liesel","Marek","Nyla","Osric","Perrin","Rolf","Signe","Ulric","Vada","Wymar","Yorick"]
function agjNameFor(npc) { try { var u = "" + npc.uuid.toString(); var h = 0; for (var i = 0; i < u.length; i++) h = (h * 31 + u.charCodeAt(i)) | 0; return AGJ_NAMES[Math.abs(h) % AGJ_NAMES.length] } catch (e) { return "Hunter" } }
const AGJ_LEVEL_XP = [0, 30, 80, 160, 280, 450, 680, 1000, 1450, 2050, 2800, 3800]
function agjLevel(xp) { var lv = 1; for (var i = 1; i < AGJ_LEVEL_XP.length; i++) { if (xp >= AGJ_LEVEL_XP[i]) lv = i + 1; else break } return lv }
if (typeof global !== "undefined") { global.agNameFor = agjNameFor; global.agLevel = agjLevel }

// ---- rarity (sets hire cost in Guild Marks + how many perks) ----
const AGJ_RARITIES = {
  common:   { name: "Common",   color: "f", weight: 56, cost: 15,  perks: 1 },
  uncommon: { name: "Uncommon", color: "a", weight: 30, cost: 45,  perks: 2 },
  rare:     { name: "Rare",     color: "b", weight: 11, cost: 120, perks: 3 },
  epic:     { name: "Epic",     color: "5", weight: 3,  cost: 300, perks: 4 }
}
const AGJ_PERKS = {
  prolific:   { name: "Prolific",   desc: "25% chance for +1 output" },
  frugal:     { name: "Frugal",     desc: "25% chance to not use inputs" },
  masterwork: { name: "Masterwork", desc: "10% chance to craft one tier up" },
  prodigy:    { name: "Prodigy",    desc: "+50% experience" },
  swift:      { name: "Swift",      desc: "+30% work speed" }
}
function agjPickRarity() { var keys = ["common", "uncommon", "rare", "epic"], total = 0, i; for (i = 0; i < keys.length; i++) total += AGJ_RARITIES[keys[i]].weight; var r = Math.random() * total; for (i = 0; i < keys.length; i++) { r -= AGJ_RARITIES[keys[i]].weight; if (r <= 0) return keys[i] } return "common" }
function agjRollPerks(n) { var pool = ["prolific", "frugal", "masterwork", "prodigy", "swift"], out = []; for (var i = 0; i < n && pool.length > 0; i++) { var idx = Math.floor(Math.random() * pool.length); out.push(pool[idx]); pool.splice(idx, 1) } return out }
function agjRarityOf(npc) { return agjTagWith(npc, "ar_rarity_") || "common" }
function agjPerksOf(npc) { var out = []; try { var it = npc.tags.iterator(); while (it.hasNext()) { var t = "" + it.next(); if (t.indexOf("ar_perk_") === 0) out.push(t.substring(8)) } } catch (e) {} return out }
function agjCostOf(npc) { var t = agjTagWith(npc, "ar_cost_"); return t ? parseInt(t) : 15 }
function agjMods(w) {
  var tr = AGJ_TRAITS[agjTraitOf(w)] || AGJ_TRAITS.steady
  var m = { workMul: tr.workMul, xpMul: tr.xpMul, prolific: false, frugal: false, masterwork: false }
  var perks = agjPerksOf(w)
  if (perks.indexOf("swift") >= 0) m.workMul *= 0.7
  if (perks.indexOf("prodigy") >= 0) m.xpMul *= 1.5
  if (perks.indexOf("prolific") >= 0) m.prolific = true
  if (perks.indexOf("frugal") >= 0) m.frugal = true
  if (perks.indexOf("masterwork") >= 0) m.masterwork = true
  return m
}
if (typeof global !== "undefined") {
  global.agRarity = function (npc) { var r = agjRarityOf(npc), R = AGJ_RARITIES[r] || AGJ_RARITIES.common; return { key: r, name: R.name, color: R.color } }
  global.agPerks = function (npc) { var ks = agjPerksOf(npc), o = []; for (var i = 0; i < ks.length; i++) if (AGJ_PERKS[ks[i]]) o.push(AGJ_PERKS[ks[i]].name); return o }
  global.agCost = function (npc) { return agjCostOf(npc) }
  global.agRecipes = function (npc) { var pid = agjProfOf(npc), prof = pid ? AGJ_PROFESSIONS[pid] : null, out = []; if (prof) for (var i = 0; i < prof.recipes.length; i++) out.push({ idx: i, label: prof.recipes[i].label, min: prof.recipes[i].min }); return out }
  global.agRecipeChoice = function (npc) { try { return npc.persistentData.getInt("ar_recipe_choice") } catch (e) { return 0 } }
}

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

function agjGearNbt(g) {
  var weapons = g.main ? ('Weapons:[{Slot:0,id:"' + g.main + '",Count:1b}],') : ''
  var hands = 'HandItems:[' + (g.main ? ('{id:"' + g.main + '",Count:1b}') : '{}') + ',{}]'
  return weapons + hands + ',ArmorItems:[{},{},{},{}],HandDropChances:[0.0f,0.0f],ArmorDropChances:[0.0f,0.0f,0.0f,0.0f]'
}
function agjRecruitNbt(pid, trait, rarity, perks) {
  var P = AGJ_PROFESSIONS[pid], R = AGJ_RARITIES[rarity] || AGJ_RARITIES.common
  var name = AGJ_S + R.color + "[Recruit] " + AGJ_S + "f" + P.name + " " + AGJ_S + "8(" + AGJ_S + R.color + R.name + AGJ_S + "8)"
  var tags = '"ar_recruitable","ar_guild_npc","ar_profile_' + pid + '","ar_trait_' + trait + '","ar_rarity_' + rarity + '","ar_cost_' + R.cost + '"'
  for (var i = 0; i < perks.length; i++) tags += ',"ar_perk_' + perks[i] + '"'
  return '{Name:"' + name + '",ShowName:1,Texture:"' + P.gear.skin + '",Title:"",PersistenceRequired:1b,' + agjGearNbt(P.gear) + ',' +
    'Tags:[' + tags + '],' +
    'ForgeData:{CNPCStoredData:{ar_profile:"' + pid + '",ar_trait:"' + trait + '",ar_rarity:"' + rarity + '",ar_recruitable:"true",ar_contract_item:"kubejs:guild_mark",ar_contract_count:"' + R.cost + '"}}}'
}

function agjTagWith(npc, prefix) {
  try { var it = npc.tags.iterator(); while (it.hasNext()) { var t = it.next(); if (t.indexOf(prefix) === 0) return t.substring(prefix.length) } } catch (e) {}
  return null
}
function agjProfOf(npc) { return agjTagWith(npc, "ar_profile_") }
function agjTraitOf(npc) { return agjTagWith(npc, "ar_trait_") || "steady" }
function agjShortNames(list) { var o = []; for (var i = 0; i < list.length; i++) o.push(("" + list[i]).replace("minecraft:", "")); return o.join(", ") }

// ---- container inventory helpers ----
function agjInv(level, x, y, z) {
  try { var b = level.getBlock(x, y, z); var inv = b ? b.inventory : null; return (inv && inv.getSlots() > 0) ? inv : null } catch (e) { return null }
}
function agjItemMatch(stack, id) { try { return !stack.isEmpty() && stack.getItem() === Item.of(id).getItem() } catch (e) { return false } }
function agjInvCount(inv, id) { var n = 0; for (var i = 0; i < inv.getSlots(); i++) { if (agjItemMatch(inv.getStackInSlot(i), id)) n += inv.getStackInSlot(i).getCount() } return n }

// ---- guild storage (list of bound containers, stored on the player) ----
function agjStorageList(p) {
  var s = ""; try { s = "" + p.persistentData.getString("ar_storage") } catch (e) {}
  var out = []; if (!s) return out
  var parts = s.split("|")
  for (var i = 0; i < parts.length; i++) { var c = parts[i].split(","); if (c.length === 3) out.push({ x: parseInt(c[0]), y: parseInt(c[1]), z: parseInt(c[2]) }) }
  return out
}
function agjStorageSave(p, list) { var s = ""; for (var i = 0; i < list.length; i++) { if (i > 0) s += "|"; s += list[i].x + "," + list[i].y + "," + list[i].z } p.persistentData.putString("ar_storage", s) }
function agjStorageAdd(p, x, y, z) { var l = agjStorageList(p); for (var i = 0; i < l.length; i++) if (l[i].x === x && l[i].y === y && l[i].z === z) return false; l.push({ x: x, y: y, z: z }); agjStorageSave(p, l); return true }
function agjStorageTotal(level, list, id) { var n = 0; for (var i = 0; i < list.length; i++) { var inv = agjInv(level, list[i].x, list[i].y, list[i].z); if (inv) n += agjInvCount(inv, id) } return n }
function agjStorageHasAll(level, list, recipe) { for (var i = 0; i < recipe.inp.length; i++) if (agjStorageTotal(level, list, recipe.inp[i][0]) < recipe.inp[i][1]) return false; return true }
function agjStorageConsume(level, list, recipe) {
  if (!agjStorageHasAll(level, list, recipe)) return false
  for (var i = 0; i < recipe.inp.length; i++) {
    var id = recipe.inp[i][0], need = recipe.inp[i][1]
    for (var j = 0; j < list.length && need > 0; j++) {
      var inv = agjInv(level, list[j].x, list[j].y, list[j].z); if (!inv) continue
      for (var s = 0; s < inv.getSlots() && need > 0; s++) { var st = inv.getStackInSlot(s); if (agjItemMatch(st, id)) { var take = Math.min(need, st.getCount()); inv.extractItem(s, take, false); need -= take } }
    }
  }
  return true
}
function agjStorageDeposit(level, list, id, count, server, drop) {
  var stack = Item.of(id, count)
  for (var j = 0; j < list.length && !stack.isEmpty(); j++) {
    var inv = agjInv(level, list[j].x, list[j].y, list[j].z); if (!inv) continue
    for (var s = 0; s < inv.getSlots() && !stack.isEmpty(); s++) stack = inv.insertItem(s, stack, false)
  }
  if (!stack.isEmpty() && drop) server.runCommandSilent('summon item ' + drop.x + ' ' + (drop.y + 1) + ' ' + drop.z + ' {Item:{id:"' + id + '",Count:' + stack.getCount() + 'b}}')
}
function agjBestRecipeIdx(level, prof, skill, list) {
  var best = -1, bmin = -1
  var lv = agjLevel(skill); for (var i = 0; i < prof.recipes.length; i++) { var r = prof.recipes[i]; if (lv >= r.min && agjStorageHasAll(level, list, r)) { if (r.min > bmin) { bmin = r.min; best = i } } }
  return best
}
function agjNearestStorageTo(w, list) { var best = null, bd = 1e18; for (var i = 0; i < list.length; i++) { var dx = w.x - (list[i].x + 0.5), dz = w.z - (list[i].z + 0.5), d = dx * dx + dz * dz; if (d < bd) { bd = d; best = list[i] } } return best }
function agjIsContainer(id) { return AGJ_CONTAINERS.indexOf(id) >= 0 }

// ---- scans ----
function agjOwnedMembers(p, radius) {
  try { return p.level.getEntitiesWithin(p.getBoundingBox().inflate(radius)).filter((e) => { try { return e.tags.contains("ar_guild_member") && e.tags.contains("ar_owner_" + p.username) } catch (err) { return false } }) } catch (e) { return [] }
}
function agjNearestOwned(p, radius) { var m = agjOwnedMembers(p, radius); if (m.length === 0) return null; var npc = m[0], bd = 1e18; m.forEach((x) => { var dx = x.x - p.x, dz = x.z - p.z, d = dx * dx + dz * dz; if (d < bd) { bd = d; npc = x } }); return npc }
function agjFindOwnedByUuid(p, uuid) { var m = agjOwnedMembers(p, 48); for (var i = 0; i < m.length; i++) if (m[i].uuid.toString() === uuid) return m[i]; return null }
function agjNearestRecruitable(p, radius) {
  var best = null, bd = 1e9
  try { p.level.getEntitiesWithin(p.getBoundingBox().inflate(radius)).forEach((e) => { try { if (!e.tags.contains("ar_recruitable")) return; var dx = e.x - p.x, dz = e.z - p.z, d = Math.sqrt(dx * dx + dz * dz); if (d < bd) { bd = d; best = e } } catch (err) {} }) } catch (e) {}
  return best
}

function agjLabel(npc, server) {
  try {
    var pid = agjProfOf(npc); if (!pid || !AGJ_PROFESSIONS[pid]) return
    var P = AGJ_PROFESSIONS[pid], R = AGJ_RARITIES[agjRarityOf(npc)] || AGJ_RARITIES.common, skill = npc.persistentData.getInt("ar_skill")
    var nm = AGJ_S + "a[Guild] " + AGJ_S + R.color + agjNameFor(npc) + " " + AGJ_S + "7the " + AGJ_S + P.color + P.name + " " + AGJ_S + "8| " + AGJ_S + R.color + R.name + " " + AGJ_S + "8Lv" + AGJ_S + "f" + agjLevel(skill)
    server.runCommandSilent('data merge entity ' + npc.uuid.toString() + ' {Name:"' + nm + '",ShowName:1}')
    npc.persistentData.putByte("ar_labeled", 1)
  } catch (e) {}
}

// ============================================================
//  COMMANDS
// ============================================================
function agjSpawn(source, pid) {
  var p = source.player; if (!p) return 0
  var P = AGJ_PROFESSIONS[pid]; if (!P) { p.tell(Text.red("Unknown profession.")); return 0 }
  var trait = agjPickTrait(), rarity = agjPickRarity(), perks = agjRollPerks(AGJ_RARITIES[rarity].perks)
  var r = p.server.runCommandSilent('execute as ' + p.username + ' at @s run summon customnpcs:customnpc ~ ~ ~ ' + agjRecruitNbt(pid, trait, rarity, perks))
  if (r > 0) p.tell(Text.gold("A " + AGJ_RARITIES[rarity].name + " " + P.name + " appeared (hire: " + AGJ_RARITIES[rarity].cost + " Guild Marks). Right-click them to hire."))
  else p.tell(Text.red("Spawn FAILED (returned " + r + ")."))
  return r > 0 ? 1 : 0
}
function agjScout(source, pid) {
  var p = source.player; if (!p) return 0
  var P = AGJ_PROFESSIONS[pid]; if (!P) { p.tell(Text.red("Unknown profession.")); return 0 }
  var trait = agjPickTrait(), rarity = agjPickRarity(), perks = agjRollPerks(AGJ_RARITIES[rarity].perks)
  var dirs = [["north", 0, -1], ["east", 1, 0], ["south", 0, 1], ["west", -1, 0], ["northeast", 1, -1], ["southeast", 1, 1], ["southwest", -1, 1], ["northwest", -1, -1]]
  var d = dirs[Math.floor(Math.random() * dirs.length)]
  var dist = 48 + Math.floor(Math.random() * 40)
  var tx = Math.floor(p.x) + d[1] * dist, tz = Math.floor(p.z) + d[2] * dist, ty = Math.floor(p.y)
  var r = p.server.runCommandSilent('execute positioned ' + tx + ' ' + ty + ' ' + tz + ' run summon customnpcs:customnpc ~ ~ ~ ' + agjRecruitNbt(pid, trait, rarity, perks))
  if (r > 0) p.tell(Text.gold("Lead: a " + AGJ_RARITIES[rarity].name + " " + P.name + " was spotted ~" + dist + " blocks " + d[0] + " (near " + tx + " " + ty + " " + tz + "). ").append(Text.gray("/ascjob locate")).append(Text.gold(" to home in.")))
  else p.tell(Text.red("Scout FAILED (returned " + r + ")."))
  return r > 0 ? 1 : 0
}
function agjLocate(source) {
  var p = source.player; if (!p) return 0
  var e = agjNearestRecruitable(p, 256); if (!e) { p.tell(Text.red("No recruitable within 256 blocks. /ascjob scout <prof>.")); return 0 }
  var dx = e.x - p.x, dz = e.z - p.z, dist = Math.round(Math.sqrt(dx * dx + dz * dz))
  var dir = (Math.abs(dx) > Math.abs(dz)) ? (dx > 0 ? "east" : "west") : (dz > 0 ? "south" : "north")
  p.tell(Text.gold("Nearest recruit: ~" + dist + " blocks " + dir + " (" + Math.floor(e.x) + " " + Math.floor(e.y) + " " + Math.floor(e.z) + ")."))
  return 1
}
function agjAssign(source, pid) {
  var p = source.player; if (!p) return 0
  var P = AGJ_PROFESSIONS[pid]; if (!P) { p.tell(Text.red("Unknown profession.")); return 0 }
  var npc = agjNearestOwned(p, 8); if (!npc) { p.tell(Text.red("No guild member within 8 blocks.")); return 0 }
  var u = npc.uuid.toString(), old = agjProfOf(npc)
  if (old) p.server.runCommandSilent("tag " + u + " remove ar_profile_" + old)
  p.server.runCommandSilent("tag " + u + " add ar_profile_" + pid)
  p.server.runCommandSilent('data merge entity ' + u + ' {ShowName:1,Texture:"' + P.gear.skin + '",' + agjGearNbt(P.gear) + '}')
  // reassigning clears the old workstation (block may not suit the new job)
  npc.persistentData.putByte("ar_ws_set", 0); npc.persistentData.putString("ar_st", ""); npc.persistentData.putByte("ar_labeled", 0)
  agjLabel(npc, p.server)
  p.tell(Text.green("Reassigned to " + P.name + ". ").append(Text.yellow("Set their new workstation (right-click them).")))
  return 1
}
function agjSetWorkstation(source) {
  var p = source.player; if (!p) return 0
  var npc = agjNearestOwned(p, 12); if (!npc) { p.tell(Text.red("No guild member within 12 blocks. Stand next to the worker.")); return 0 }
  var prof = agjProfOf(npc), allowed = AGJ_WORKSTATIONS[prof] || []
  p.persistentData.putString("ar_bind", "ws:" + npc.uuid.toString())
  p.tell(Text.gold("Right-click the workstation block for your " + (AGJ_PROFESSIONS[prof] ? AGJ_PROFESSIONS[prof].name : "worker") + ". Allowed: ").append(Text.aqua(agjShortNames(allowed))).append(Text.gold(".")))
  return 1
}
function agjStorageCmd(source) {
  var p = source.player; if (!p) return 0
  var cur = ""; try { cur = "" + p.persistentData.getString("ar_bind") } catch (e) {}
  if (cur === "storage") { p.persistentData.putString("ar_bind", ""); p.tell(Text.green("Storage binding done - " + agjStorageList(p).length + " container(s) bound.")); return 1 }
  p.persistentData.putString("ar_bind", "storage")
  p.tell(Text.gold("Storage mode ON. Right-click each chest/barrel to add it. Run ").append(Text.yellow("/ascjob storage")).append(Text.gold(" again to finish.")))
  return 1
}
function agjStorageClear(source) { var p = source.player; if (!p) return 0; p.persistentData.putString("ar_storage", ""); p.tell(Text.yellow("Guild storage cleared.")); return 1 }
function agjStorageListCmd(source) {
  var p = source.player; if (!p) return 0; var l = agjStorageList(p)
  p.tell(Text.gold("Guild storage: " + l.length + " container(s)."))
  for (var i = 0; i < l.length && i < 16; i++) p.tell(Text.gray("  - " + l[i].x + " " + l[i].y + " " + l[i].z))
  return 1
}
function agjStatus(source) {
  var p = source.player; if (!p) return 0
  var mem = agjOwnedMembers(p, 128), stor = agjStorageList(p)
  p.tell(Text.gold("=== " + p.username + "'s Guild (" + mem.length + " workers | " + stor.length + " storage) ==="))
  if (stor.length === 0) p.tell(Text.gray("No storage yet - /ascjob storage to bind chests."))
  if (mem.length === 0) { p.tell(Text.gray("No members. /ascjob spawn <prof> + /ascguild recruit.")); return 1 }
  mem.forEach((npc) => {
    try {
      var pid = agjProfOf(npc), P = (pid && AGJ_PROFESSIONS[pid]) ? AGJ_PROFESSIONS[pid] : null
      var pd = npc.persistentData, skill = pd.getInt("ar_skill"), R = AGJ_RARITIES[agjRarityOf(npc)] || AGJ_RARITIES.common, pk = agjPerksOf(npc)
      var hasWs = pd.getByte("ar_ws_set") === 1, st = "" + pd.getString("ar_st"), doing
      if (!hasWs) doing = "no workstation (panel: Set Workstation)"
      else if (st === "fetch") doing = "fetching materials"
      else if (st === "work") doing = "walking to workstation"
      else if (st === "craft") doing = (P ? P.work : "working") + " (" + pd.getInt("ar_craft_left") + "s)"
      else if (st === "deposit") doing = "delivering to storage"
      else doing = (stor.length === 0) ? "idle (no storage)" : "idle / awaiting materials"
      p.tell(Text.white("- " + agjNameFor(npc) + " the " + (P ? P.name : "Member") + " ").append(Text.gray("[" + R.name + ", Lv" + agjLevel(skill) + "] ")).append(Text.yellow(doing)))
      if (pk.length > 0) { var pn = []; for (var z = 0; z < pk.length; z++) if (AGJ_PERKS[pk[z]]) pn.push(AGJ_PERKS[pk[z]].name); p.tell(Text.gray("    perks: " + pn.join(", "))) }
    } catch (e) {}
  })
  return 1
}

ServerEvents.commandRegistry((event) => {
  const Commands = event.commands
  var spawnNode = Commands.literal("spawn"), scoutNode = Commands.literal("scout"), assignNode = Commands.literal("assign")
  Object.keys(AGJ_PROFESSIONS).forEach((pid) => {
    var c = AGJ_PROFESSIONS[pid].cmd
    spawnNode.then(Commands.literal(c).executes((ctx) => agjSpawn(ctx.source, pid)))
    scoutNode.then(Commands.literal(c).executes((ctx) => agjScout(ctx.source, pid)))
    assignNode.then(Commands.literal(c).executes((ctx) => agjAssign(ctx.source, pid)))
  })
  event.register(
    Commands.literal("ascjob").requires((src) => src.hasPermission(0))
      .then(spawnNode).then(scoutNode).then(assignNode)
      .then(Commands.literal("locate").executes((ctx) => agjLocate(ctx.source)))
      .then(Commands.literal("setworkstation").executes((ctx) => agjSetWorkstation(ctx.source)))
      .then(Commands.literal("setstation").executes((ctx) => agjSetWorkstation(ctx.source)))
      .then(Commands.literal("status").executes((ctx) => agjStatus(ctx.source)))
      .then(Commands.literal("storage").executes((ctx) => agjStorageCmd(ctx.source))
        .then(Commands.literal("clear").executes((ctx) => agjStorageClear(ctx.source)))
        .then(Commands.literal("list").executes((ctx) => agjStorageListCmd(ctx.source))))
  )
})

// ---- right-click binding (storage chests + workstation block) ----
BlockEvents.rightClicked((event) => {
  try {
    var p = event.player; if (!p) return
    var bind = ""; try { bind = "" + p.persistentData.getString("ar_bind") } catch (e) {}
    if (!bind) return
    var b = event.block; var id = "" + b.id, x = b.x, y = b.y, z = b.z
    if (bind === "storage") {
      if (agjIsContainer(id)) { if (agjStorageAdd(p, x, y, z)) p.tell(Text.green("+ storage: " + id.replace("minecraft:", "") + " at " + x + " " + y + " " + z + ".  (/ascjob storage to finish)")); else p.tell(Text.yellow("Already bound.")) }
      else p.tell(Text.red("Not a container. Right-click a chest/barrel, or /ascjob storage to finish."))
      event.cancel(); return
    }
    if (bind.indexOf("ws:") === 0) {
      var w = agjFindOwnedByUuid(p, bind.substring(3))
      if (!w) { p.tell(Text.red("Lost that worker - stand by them and use Set Workstation again.")); p.persistentData.putString("ar_bind", ""); event.cancel(); return }
      var prof = agjProfOf(w), allowed = AGJ_WORKSTATIONS[prof] || []
      if (allowed.indexOf(id) < 0) { p.tell(Text.red((AGJ_PROFESSIONS[prof] ? AGJ_PROFESSIONS[prof].name : "They") + " can't use a " + id.replace("minecraft:", "") + ". Needs: " + agjShortNames(allowed) + ".")); event.cancel(); return }
      var pd = w.persistentData
      pd.putInt("ar_ws_x", x); pd.putInt("ar_ws_y", y); pd.putInt("ar_ws_z", z); pd.putByte("ar_ws_set", 1); pd.putString("ar_st", "")
      p.server.runCommandSilent("tag " + w.uuid.toString() + " remove ar_guild_escorting")
      p.persistentData.putString("ar_bind", "")
      p.tell(Text.green("Workstation set: " + id.replace("minecraft:", "") + " at " + x + " " + y + " " + z + ". ").append(agjStorageList(p).length === 0 ? Text.yellow("Now bind storage: /ascjob storage") : Text.gray("They'll start working.")))
      event.cancel(); return
    }
  } catch (e) {}
})

// ============================================================
//  THE WORK LOOP  (storage -> workstation -> storage)
// ============================================================
function agjSetTarget(pd, x, y, z) { pd.putInt("ar_tx", x); pd.putInt("ar_ty", y); pd.putInt("ar_tz", z); pd.putInt("ar_travel", 0) }
function agjArrive(p, w, pd) {
  var tx = pd.getInt("ar_tx"), ty = pd.getInt("ar_ty"), tz = pd.getInt("ar_tz")
  var dx = w.x - (tx + 0.5), dz = w.z - (tz + 0.5), d = Math.sqrt(dx * dx + dz * dz)
  if (d <= AGJ_REACH && Math.abs(w.y - ty) <= 3) { pd.putInt("ar_travel", 0); return true }
  try { w.getNavigation().moveTo(tx + 0.5, ty + 1, tz + 0.5, AGJ_SPEED) } catch (e) {}
  var tv = pd.getInt("ar_travel") + 1; pd.putInt("ar_travel", tv)
  if (tv >= AGJ_STUCK) { try { p.server.runCommandSilent("tp " + w.uuid.toString() + " " + (tx + 0.5) + " " + (ty + 1) + " " + (tz + 0.5)) } catch (e) {} pd.putInt("ar_travel", 0); return true }
  return false
}
function agjWorkStep(p, w, storage, server) {
  if (w.persistentData.getByte("ar_labeled") !== 1) agjLabel(w, server)
  var pid = agjProfOf(w); var prof = pid ? AGJ_PROFESSIONS[pid] : null; if (!prof) return
  var pd = w.persistentData, level = p.level, st = "" + pd.getString("ar_st")
  if (st === "" || st === "idle") {
    if (storage.length === 0) return
    var skl = pd.getInt("ar_skill"), ridx = -1, rc = pd.getInt("ar_recipe_choice")
    if (rc > 0) { var ci = rc - 1, cr = prof.recipes[ci]; if (cr && agjLevel(skl) >= cr.min && agjStorageHasAll(level, storage, cr)) ridx = ci }
    else ridx = agjBestRecipeIdx(level, prof, skl, storage)
    if (ridx < 0) return
    var sc = agjNearestStorageTo(w, storage); if (!sc) return
    pd.putInt("ar_ridx", ridx); agjSetTarget(pd, sc.x, sc.y, sc.z); pd.putString("ar_st", "fetch"); return
  }
  if (st === "fetch") {
    if (agjArrive(p, w, pd)) {
      var r = prof.recipes[pd.getInt("ar_ridx")]
      var fm = agjMods(w)
      var got = r ? ((fm.frugal && Math.random() < 0.25) ? agjStorageHasAll(level, storage, r) : agjStorageConsume(level, storage, r)) : false
      if (got) { agjSetTarget(pd, pd.getInt("ar_ws_x"), pd.getInt("ar_ws_y"), pd.getInt("ar_ws_z")); pd.putString("ar_st", "work") }
      else pd.putString("ar_st", "")
    }
    return
  }
  if (st === "work") {
    if (agjArrive(p, w, pd)) {
      var r = prof.recipes[pd.getInt("ar_ridx")]; if (!r) { pd.putString("ar_st", ""); return }
      pd.putInt("ar_craft_left", Math.max(2, Math.round(r.cyc * agjMods(w).workMul * 2))); pd.putString("ar_st", "craft")
      server.runCommandSilent('execute at ' + w.uuid.toString() + ' run playsound minecraft:block.smithing_table.use neutral @a[distance=..24] ~ ~ ~ 0.5 1')
      if (!global.__agjWorkProven) { console.info("[Ascendant Guild Jobs] craft started: " + prof.name + " -> " + r.label); global.__agjWorkProven = true }
    }
    return
  }
  if (st === "craft") {
    server.runCommandSilent('execute at ' + w.uuid.toString() + ' run particle ' + prof.particle + ' ~ ~1.2 ~ 0.3 0.4 0.3 0.02 6')
    var left = pd.getInt("ar_craft_left") - 1
    if (left <= 0) { var sc = agjNearestStorageTo(w, storage); if (sc) agjSetTarget(pd, sc.x, sc.y, sc.z); pd.putString("ar_st", "deposit") } else pd.putInt("ar_craft_left", left)
    return
  }
  if (st === "deposit") {
    if (agjArrive(p, w, pd)) {
      var r = prof.recipes[pd.getInt("ar_ridx")]
      if (r) {
        var dm = agjMods(w), outId = r.out, outN = r.n
        if (dm.masterwork && Math.random() < 0.10) { var nr = prof.recipes[pd.getInt("ar_ridx") + 1]; if (nr) { outId = nr.out; outN = nr.n } }
        if (dm.prolific && Math.random() < 0.25) outN += 1
        agjStorageDeposit(level, storage, outId, outN, server, { x: pd.getInt("ar_tx"), y: pd.getInt("ar_ty"), z: pd.getInt("ar_tz") })
        var gain = Math.max(1, Math.round(r.xp * dm.xpMul)), ns = pd.getInt("ar_skill") + gain; pd.putInt("ar_skill", ns); pd.putByte("ar_labeled", 0)
        server.runCommandSilent('execute at ' + w.uuid.toString() + ' run playsound minecraft:block.anvil.use neutral @a[distance=..24] ~ ~ ~ 0.5 1.4')
        p.tell(Text.green(agjNameFor(w) + " the " + prof.name + " stocked a ").append(Text.white(outN + "x " + r.label)).append(Text.green(" (Lv -> " + agjLevel(ns) + ").")))
      }
      pd.putString("ar_st", "")
    }
    return
  }
}

let AGJ_tick = 0
ServerEvents.tick((event) => {
  AGJ_tick++
  if (AGJ_tick % AGJ_TICK !== 0) return
  var server = event.server
  try {
    server.players.forEach((p) => {
      var storage = agjStorageList(p)
      var workers = agjOwnedMembers(p, 128).filter((e) => { try { return e.persistentData.getByte("ar_ws_set") === 1 } catch (err) { return false } })
      workers.forEach((w) => { try { agjWorkStep(p, w, storage, server) } catch (e2) { if (!global.__agjMemberWarned) { console.warn("[Ascendant Guild Jobs] worker step: " + e2); global.__agjMemberWarned = true } } })
    })
  } catch (e) { if (!global.__agjTickWarned) { console.warn("[Ascendant Guild Jobs] tick: " + e); global.__agjTickWarned = true } }
})

ServerEvents.loaded((event) => { console.info("[Ascendant Guild Jobs] logistics loop loaded - storage<->workstation. /ascjob storage + Set Workstation.") })
