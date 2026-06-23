// Ascendant Atlas finite-world runtime.
//
// This is the live testable control layer for the authored 30000-block Atlas map:
// it applies the world border, mirrors player region/ring/sector into
// scoreboards, and gives a lightweight actionbar when a player crosses into
// a different Atlas region.

const AscendantAtlasJsonIO = typeof JsonIO !== "undefined"
  ? JsonIO
  : Java.loadClass("dev.latvian.mods.kubejs.util.JsonIO")

const ASCENDANT_ATLAS_RUNTIME_PATH = "config/ascendant_atlas/runtime.json"

const ASCENDANT_ATLAS_DEFAULTS = {
  enabled: true,
  world_center: { x: 0, z: 0 },
  world_radius_blocks: 30000,
  worldborder: {
    enabled: true,
    diameter_blocks: 60000,
    warning_distance: 120,
    warning_time: 20
  },
  sync_interval_ticks: 20,
  announce_region_changes: true,
  scoreboards: {
    region: "ar_atlas_region",
    ring: "ar_atlas_ring",
    sector: "ar_atlas_sector",
    distance: "ar_atlas_distance",
    x: "ar_atlas_x",
    z: "ar_atlas_z"
  },
  region_ids: {
    hearthlands: 0,
    frostmarch: 1,
    sunreach: 2,
    verdant_coast: 3,
    stoneback_highlands: 4,
    north_east_marches: 5,
    north_west_marches: 6,
    south_east_wilds: 7,
    south_west_wilds: 8,
    outer_rim: 9,
    nether_front: 10,
    end_expanse: 11
  },
  sector_ids: {
    center: 0,
    north: 1,
    south: 2,
    east: 3,
    west: 4,
    north_east: 5,
    north_west: 6,
    south_east: 7,
    south_west: 8,
    outer: 9,
    nether: 10,
    end: 11
  },
  rings: [
    { id: 0, min_distance: 0, max_distance: 1500 },
    { id: 1, min_distance: 1501, max_distance: 3500 },
    { id: 2, min_distance: 3501, max_distance: 6500 },
    { id: 3, min_distance: 6501, max_distance: 10000 },
    { id: 4, min_distance: 10001, max_distance: 14000 },
    { id: 5, min_distance: 14001, max_distance: 30000 }
  ],
  regions: [
    { id: "hearthlands", display: "Hearthlands", sector: "center", color: "green" },
    { id: "frostmarch", display: "Frostmarch", sector: "north", color: "aqua" },
    { id: "sunreach", display: "Sunreach", sector: "south", color: "gold" },
    { id: "verdant_coast", display: "Verdant Coast", sector: "east", color: "dark_aqua" },
    { id: "stoneback_highlands", display: "Stoneback Highlands", sector: "west", color: "gray" }
  ]
}

let ascendantAtlasConfig = readAscendantAtlasRuntime()
let ascendantAtlasTickDelay = {}

function atlasIsObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value)
}

function atlasMergeObjects(base, override) {
  var result = {}
  Object.keys(base || {}).forEach((key) => {
    result[key] = atlasIsObject(base[key]) ? atlasMergeObjects(base[key], {}) : base[key]
  })
  Object.keys(override || {}).forEach((key) => {
    result[key] = atlasIsObject(override[key]) && atlasIsObject(result[key])
      ? atlasMergeObjects(result[key], override[key])
      : override[key]
  })
  return result
}

function atlasReadJson(pathString) {
  var relativePath = String(pathString).replace(/\\/g, "/").replace(/^config\//, "")
  return AscendantAtlasJsonIO.read(`config/${relativePath}`)
}

function readAscendantAtlasRuntime() {
  try {
    var parsed = atlasReadJson(ASCENDANT_ATLAS_RUNTIME_PATH)
    if (parsed === null || parsed === undefined) {
      console.warn(`[Ascendant Atlas] Missing ${ASCENDANT_ATLAS_RUNTIME_PATH}; using defaults.`)
      return ASCENDANT_ATLAS_DEFAULTS
    }
    return atlasMergeObjects(ASCENDANT_ATLAS_DEFAULTS, parsed)
  } catch (error) {
    console.warn(`[Ascendant Atlas] Could not read ${ASCENDANT_ATLAS_RUNTIME_PATH}: ${error}`)
    return ASCENDANT_ATLAS_DEFAULTS
  }
}

function atlasSafeObjective(value, fallback) {
  var text = String(value || fallback || "")
  if (!/^[A-Za-z0-9_.+-]+$/.test(text)) {
    return String(fallback || "ar_atlas_invalid")
  }
  return text
}

function atlasObjective(server, id, label, color) {
  var objective = atlasSafeObjective(id, "")
  server.runCommandSilent(`scoreboard objectives add ${objective} dummy {"text":"${label}","color":"${color}"}`)
}

function ensureAscendantAtlasScoreboards(server) {
  if (!server) return
  var boards = ascendantAtlasConfig.scoreboards || {}
  atlasObjective(server, boards.region, "Atlas Region", "aqua")
  atlasObjective(server, boards.ring, "Atlas Ring", "gold")
  atlasObjective(server, boards.sector, "Atlas Sector", "dark_aqua")
  atlasObjective(server, boards.distance, "Spawn Distance", "gray")
  atlasObjective(server, boards.x, "Atlas X", "gray")
  atlasObjective(server, boards.z, "Atlas Z", "gray")
}

function applyAscendantAtlasWorldBorder(server) {
  if (!server || !ascendantAtlasConfig.enabled) return
  var border = ascendantAtlasConfig.worldborder || {}
  if (!border.enabled) return

  var center = ascendantAtlasConfig.world_center || { x: 0, z: 0 }
  var diameter = Math.max(1000, Math.floor(Number(border.diameter_blocks || 60000)))
  var warningDistance = Math.max(0, Math.floor(Number(border.warning_distance || 120)))
  var warningTime = Math.max(0, Math.floor(Number(border.warning_time || 20)))
  server.runCommandSilent(`worldborder center ${Math.floor(Number(center.x) || 0)} ${Math.floor(Number(center.z) || 0)}`)
  server.runCommandSilent(`worldborder set ${diameter}`)
  server.runCommandSilent(`worldborder warning distance ${warningDistance}`)
  server.runCommandSilent(`worldborder warning time ${warningTime}`)
}

function atlasPlayerId(player) {
  try {
    if (player && player.uuid) return String(player.uuid)
  } catch (error) {}
  try {
    if (player && typeof player.getUUID === "function") return String(player.getUUID())
  } catch (error) {}
  try {
    if (player && player.name) return String(player.name)
  } catch (error) {}
  return "player"
}

function atlasDimension(player) {
  try {
    return String(player.level.dimension)
  } catch (error) {}
  try {
    return String(player.getLevel().dimension())
  } catch (error) {}
  return "minecraft:overworld"
}

function atlasFindRing(distance) {
  var rings = ascendantAtlasConfig.rings || []
  for (var i = 0; i < rings.length; i++) {
    var ring = rings[i]
    if (distance >= Number(ring.min_distance || 0) && distance <= Number(ring.max_distance || 0)) {
      return Math.floor(Number(ring.id) || 0)
    }
  }
  return 4
}

function atlasRegionMeta(id) {
  var regions = ascendantAtlasConfig.regions || []
  for (var i = 0; i < regions.length; i++) {
    if (regions[i].id === id) return regions[i]
  }
  return { id: id, display: id, sector: "outer", color: "gray" }
}

function classifyAscendantAtlasPosition(player) {
  var dimension = atlasDimension(player).toLowerCase()
  if (dimension.indexOf("the_nether") >= 0) {
    return { region: "nether_front", sector: "nether", ring: 4, distance: 0, x: 0, z: 0 }
  }
  if (dimension.indexOf("the_end") >= 0) {
    return { region: "end_expanse", sector: "end", ring: 5, distance: 0, x: 0, z: 0 }
  }

  var center = ascendantAtlasConfig.world_center || { x: 0, z: 0 }
  var x = Math.floor(Number(player.x || 0) - Number(center.x || 0))
  var z = Math.floor(Number(player.z || 0) - Number(center.z || 0))
  var absX = Math.abs(x)
  var absZ = Math.abs(z)
  var distance = Math.floor(Math.sqrt(x * x + z * z))
  var radius = Math.floor(Number(ascendantAtlasConfig.world_radius_blocks || 30000))

  if (distance > radius) {
    return { region: "outer_rim", sector: "outer", ring: 5, distance: distance, x: x, z: z }
  }
  if (distance <= 650) {
    return { region: "hearthlands", sector: "center", ring: atlasFindRing(distance), distance: distance, x: x, z: z }
  }
  if (absZ >= absX * 1.25) {
    return {
      region: z < 0 ? "frostmarch" : "sunreach",
      sector: z < 0 ? "north" : "south",
      ring: atlasFindRing(distance),
      distance: distance,
      x: x,
      z: z
    }
  }
  if (absX >= absZ * 1.25) {
    return {
      region: x > 0 ? "verdant_coast" : "stoneback_highlands",
      sector: x > 0 ? "east" : "west",
      ring: atlasFindRing(distance),
      distance: distance,
      x: x,
      z: z
    }
  }

  var north = z < 0
  var east = x > 0
  if (north && east) return { region: "north_east_marches", sector: "north_east", ring: atlasFindRing(distance), distance: distance, x: x, z: z }
  if (north && !east) return { region: "north_west_marches", sector: "north_west", ring: atlasFindRing(distance), distance: distance, x: x, z: z }
  if (!north && east) return { region: "south_east_wilds", sector: "south_east", ring: atlasFindRing(distance), distance: distance, x: x, z: z }
  return { region: "south_west_wilds", sector: "south_west", ring: atlasFindRing(distance), distance: distance, x: x, z: z }
}

function atlasSetScore(player, objective, value) {
  player.runCommandSilent(`scoreboard players set @s ${atlasSafeObjective(objective, "ar_atlas_invalid")} ${Math.floor(Number(value) || 0)}`)
}

function atlasAnnounceRegion(player, classification, previousRegionId) {
  if (!ascendantAtlasConfig.announce_region_changes || classification.region === previousRegionId) return
  var meta = atlasRegionMeta(classification.region)
  var regionText = JSON.stringify(String(meta.display || classification.region))
  var color = String(meta.color || "gray").replace(/[^a-z_]/g, "") || "gray"
  player.runCommandSilent(
    `title @s actionbar [{"text":${regionText},"color":"${color}","bold":true},{"text":" | Ring ${classification.ring} | ${classification.distance}m from origin","color":"gray"}]`
  )
}

function syncAscendantAtlasPlayer(player, server, force) {
  if (!ascendantAtlasConfig.enabled || !player) return

  var id = atlasPlayerId(player)
  if (!ascendantAtlasTickDelay[id]) ascendantAtlasTickDelay[id] = 0
  if (!force) {
    ascendantAtlasTickDelay[id] -= 1
    if (ascendantAtlasTickDelay[id] > 0) return
  }
  ascendantAtlasTickDelay[id] = Math.max(1, Math.floor(Number(ascendantAtlasConfig.sync_interval_ticks || 20)))

  ensureAscendantAtlasScoreboards(server || player.getServer())
  var classification = classifyAscendantAtlasPosition(player)
  var regionIds = ascendantAtlasConfig.region_ids || {}
  var sectorIds = ascendantAtlasConfig.sector_ids || {}
  var boards = ascendantAtlasConfig.scoreboards || {}
  var previousRegion = ""
  try {
    previousRegion = String(player.getPersistentData().getString("ar_atlas_region_id"))
  } catch (error) {}

  atlasSetScore(player, boards.region, regionIds[classification.region] || 0)
  atlasSetScore(player, boards.ring, classification.ring)
  atlasSetScore(player, boards.sector, sectorIds[classification.sector] || 0)
  atlasSetScore(player, boards.distance, classification.distance)
  atlasSetScore(player, boards.x, classification.x)
  atlasSetScore(player, boards.z, classification.z)
  atlasAnnounceRegion(player, classification, previousRegion)

  try {
    player.getPersistentData().putString("ar_atlas_region_id", classification.region)
  } catch (error) {}
}

ServerEvents.loaded((event) => {
  ascendantAtlasConfig = readAscendantAtlasRuntime()
  ensureAscendantAtlasScoreboards(event.server)
  applyAscendantAtlasWorldBorder(event.server)
  console.info("[Ascendant Atlas] Finite-world coordinate runtime loaded.")
})

PlayerEvents.loggedIn((event) => {
  syncAscendantAtlasPlayer(event.player, event.server, true)
})

PlayerEvents.respawned((event) => {
  syncAscendantAtlasPlayer(event.player, event.server, true)
})

PlayerEvents.tick((event) => {
  syncAscendantAtlasPlayer(event.player, event.server, false)
})
