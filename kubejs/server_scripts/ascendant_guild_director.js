// ============================================================
//  Ascendant Guild Director - PHASE 1 (recruit loop, escort-only)
//  Decisions locked: pure CustomNPCs, escort-only travel, simple jobs (Phase 2),
//  custom rival sim (Phase 4).
//
//  Vertical slice proven here:
//    /ascguild sethall          - mark your guild hall (your position)
//    /ascguild spawn_recruit     - place a recruitable blacksmith nearby (a real NPC)
//    /ascguild recruit           - stand by them, pay the contract (10 iron) -> they join
//                                  your guild and physically walk to your hall to live there
//    /ascguild roster            - how many specialists you've recruited
//    /ascguild dismiss           - release the nearest guild member
//  Nothing auto-spawns. The NPC is physical and walks to the hall (escort-only v1).
// ============================================================

const AGD_SPEED = 0.55
const AGD_CONTRACT_ITEM = "minecraft:iron_ingot"
const AGD_CONTRACT_COUNT = 10
// Section sign (color-code prefix) built at runtime. Minecraft SNBT rejects \\u escapes,
// so we must inject the real char rather than write "\\u00a7" into a command string.
const AGD_S = String.fromCharCode(0xA7)

function agdHallOf(player) {
  var d = player.persistentData
  if (!d.getBoolean("ar_guild_hall_set")) return null
  return { x: d.getInt("ar_guild_hall_x"), y: d.getInt("ar_guild_hall_y"), z: d.getInt("ar_guild_hall_z") }
}

function agdSetHall(source) {
  var p = source.player; if (!p) return 0
  var d = p.persistentData
  d.putBoolean("ar_guild_hall_set", true)
  d.putInt("ar_guild_hall_x", Math.floor(p.x)); d.putInt("ar_guild_hall_y", Math.floor(p.y)); d.putInt("ar_guild_hall_z", Math.floor(p.z))
  p.tell(Text.green("Guild hall set at " + Math.floor(p.x) + " " + Math.floor(p.y) + " " + Math.floor(p.z) + ". Recruited specialists will travel here."))
  return 1
}

// Build the recruitable blacksmith CustomNPC summon NBT (mirrors your spawn_* functions).
function agdBlacksmithNbt() {
  var C = AGD_S
  var name = C + "6[Recruit] " + C + "fWandering Blacksmith " + C + "8| " + C + "7Smith"
  var gear = 'Weapons:[{Slot:0,id:"minecraft:iron_axe",Count:1b}],' +
    'Armor:[{Slot:2,id:"immersive_armors:steampunk_chestplate",Count:1b},{Slot:3,id:"immersive_armors:steampunk_helmet",Count:1b}],' +
    'HandItems:[{id:"minecraft:iron_axe",Count:1b},{}],' +
    'ArmorItems:[{},{},{id:"immersive_armors:steampunk_chestplate",Count:1b},{id:"immersive_armors:steampunk_helmet",Count:1b}],' +
    'HandDropChances:[0.0f,0.0f],ArmorDropChances:[0.0f,0.0f,0.0f,0.0f]'
  return '{Name:"' + name + '",ShowName:1,Title:"",PersistenceRequired:1b,' + gear + ',' +
    'Tags:["ar_recruitable","ar_guild_npc","ar_profile_guild_blacksmith"],' +
    'ForgeData:{CNPCStoredData:{ar_profile:"guild_blacksmith",ar_role:"Smith",ar_recruitable:"true",ar_contract_item:"' + AGD_CONTRACT_ITEM + '",ar_contract_count:"' + AGD_CONTRACT_COUNT + '"}}}'
}

function agdSpawnRecruit(source) {
  var p = source.player; if (!p) return 0
  var r = p.server.runCommandSilent('execute as ' + p.username + ' at @s run summon customnpcs:customnpc ~ ~ ~ ' + agdBlacksmithNbt())
  if (r > 0) {
    p.tell(Text.gold("A wandering blacksmith spawned right where you're standing - step back to see them, then use ") .append(Text.yellow("/ascguild recruit")) .append(Text.gold(". They want " + AGD_CONTRACT_COUNT + "x Iron Ingot.")))
  } else {
    p.tell(Text.red("Spawn FAILED (summon returned " + r + "). The NPC NBT was rejected - tell Claude."))
  }
  return r > 0 ? 1 : 0
}

function agdNearby(p, radius, tag) {
  try {
    return p.level.getEntitiesWithin(p.getBoundingBox().inflate(radius)).filter((e) => {
      try { return e.tags.contains(tag) } catch (err) { return false }
    })
  } catch (e) { return [] }
}

function agdCostOf(npc) {
  try { var it = npc.tags.iterator(); while (it.hasNext()) { var t = "" + it.next(); if (t.indexOf("ar_cost_") === 0) { var n = parseInt(t.substring(8)); if (!isNaN(n)) return n } } } catch (e) {}
  return 15
}

function agdRecruit(source) {
  var p = source.player; if (!p) return 0
  var hall = agdHallOf(p)
  if (!hall) { p.tell(Text.red("Set your guild hall first: /ascguild sethall")); return 0 }
  var near = agdNearby(p, 6, "ar_recruitable")
  if (near.length === 0) { p.tell(Text.red("No recruitable specialist within 6 blocks. Use /ascguild spawn_recruit to place one.")); return 0 }
  var npc = near[0]; var s = p.server; var u = npc.uuid.toString()
  var cost = agdCostOf(npc)
  var have = s.runCommandSilent("clear " + p.username + " kubejs:guild_mark 0")
  if (have < cost) {
    p.tell(Text.red("This specialist costs " + cost + " Guild Marks - you have " + have + ". Earn marks from bounties, dungeons, and looted chests."))
    return 0
  }
  s.runCommandSilent("clear " + p.username + " kubejs:guild_mark " + cost)
  s.runCommandSilent("tag " + u + " remove ar_recruitable")
  s.runCommandSilent("tag " + u + " add ar_guild_member")
  s.runCommandSilent("tag " + u + " add ar_owner_" + p.username)
  s.runCommandSilent("tag " + u + " add ar_guild_escorting")
  try {
    npc.persistentData.putInt("ar_hall_x", hall.x); npc.persistentData.putInt("ar_hall_y", hall.y); npc.persistentData.putInt("ar_hall_z", hall.z)
    npc.persistentData.putString("ar_owner", p.username)
  } catch (e) {}
  var rnm = (global.agNameFor) ? (AGD_S + "a[Guild] " + AGD_S + ((global.agRarity) ? global.agRarity(npc).color : "f") + global.agNameFor(npc)) : (AGD_S + "a[Guild] Member")
  s.runCommandSilent('data merge entity ' + u + ' {PersistenceRequired:1b,ShowName:1,Name:"' + rnm + '"}')
  var d = p.persistentData; d.putInt("ar_guild_count", d.getInt("ar_guild_count") + 1)
  s.runCommandSilent("execute at " + u + " run playsound minecraft:entity.villager.yes neutral @a[distance=..16] ~ ~ ~ 1 1")
  p.tell(Text.green("Recruited " + ((global.agNameFor) ? global.agNameFor(npc) : "a specialist") + "! They've joined your guild - right-click them to assign a workstation."))
  return 1
}

function agdRoster(source) {
  var p = source.player; if (!p) return 0
  var c = p.persistentData.getInt("ar_guild_count"); var hall = agdHallOf(p)
  p.tell(Text.gold("=== " + p.username + "'s Guild ==="))
  p.tell(Text.white("Specialists recruited: ").append(Text.green("" + c)))
  if (hall) p.tell(Text.gray("Hall: " + hall.x + " " + hall.y + " " + hall.z)); else p.tell(Text.red("No hall set - use /ascguild sethall."))
  return 1
}

function agdDismiss(source) {
  var p = source.player; if (!p) return 0
  var near = agdNearby(p, 8, "ar_guild_member").filter((e) => { try { return e.tags.contains("ar_owner_" + p.username) } catch (err) { return false } })
  if (near.length === 0) { p.tell(Text.red("No guild member of yours within 8 blocks.")); return 0 }
  near[0].server.runCommandSilent("kill " + near[0].uuid.toString())
  var d = p.persistentData; d.putInt("ar_guild_count", Math.max(0, d.getInt("ar_guild_count") - 1))
  p.tell(Text.yellow("Released the nearest guild member.")); return 1
}

// ---- /ascguild command ----
ServerEvents.commandRegistry((event) => {
  const Commands = event.commands
  event.register(
    Commands.literal("ascguild")
      .requires((src) => src.hasPermission(0))
      .then(Commands.literal("sethall").executes((c) => agdSetHall(c.source)))
      .then(Commands.literal("spawn_recruit").executes((c) => agdSpawnRecruit(c.source)))
      .then(Commands.literal("recruit").executes((c) => agdRecruit(c.source)))
      .then(Commands.literal("roster").executes((c) => agdRoster(c.source)))
      .then(Commands.literal("dismiss").executes((c) => agdDismiss(c.source)))
  )
})

// ---- escort-only travel: recruited members walk to the hall, then settle ----
let AGD_tick = 0
ServerEvents.tick((event) => {
  AGD_tick++
  if (AGD_tick % 20 !== 0) return
  try {
    event.server.players.forEach((p) => {
      var members = agdNearby(p, 80, "ar_guild_escorting")
      members.forEach((npc) => {
        try {
          if (!npc.tags.contains("ar_owner_" + p.username)) return
          var hx = npc.persistentData.getInt("ar_hall_x")
          var hy = npc.persistentData.getInt("ar_hall_y")
          var hz = npc.persistentData.getInt("ar_hall_z")
          var dist = Math.sqrt((npc.x - hx) * (npc.x - hx) + (npc.z - hz) * (npc.z - hz))
          if (dist > 5) {
            try { npc.getNavigation().moveTo(hx + 0.5, hy, hz + 0.5, AGD_SPEED) } catch (e1) {}
          } else {
            var u = npc.uuid.toString()
            npc.server.runCommandSilent("tag " + u + " remove ar_guild_escorting")
            npc.server.runCommandSilent("tag " + u + " add ar_guild_home")
            npc.server.runCommandSilent("execute at " + u + " run particle minecraft:happy_villager ~ ~1 ~ 0.4 0.6 0.4 0.1 14")
            p.tell(Text.green("Your Blacksmith has arrived at the guild hall."))
          }
        } catch (e2) {}
      })
    })
  } catch (e) {
    if (!global.__agdTickWarned) { console.warn("[Ascendant Guild] escort tick skipped once: " + e); global.__agdTickWarned = true }
  }
})

ServerEvents.loaded((event) => {
  console.info("[Ascendant Guild] Director Phase 1 loaded (/ascguild sethall | spawn_recruit | recruit | roster | dismiss).")
})
