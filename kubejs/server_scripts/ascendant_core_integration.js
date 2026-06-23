// Ascendant Realms core integration bridge.
//
// This bridge stays defensive: it loads pack-owned core data, checks linked
// registries, creates shared objectives, mirrors region tier, promotes Guild
// rank from existing proof scoreboards, and awards small proof counters from
// player kills. It does not rewrite worldgen, mob spawns, loot tables, or mob
// stats.

const AscendantCoreJsonIO = typeof JsonIO !== "undefined"
  ? JsonIO
  : Java.loadClass("dev.latvian.mods.kubejs.util.JsonIO")

const ASCENDANT_CORE_MANIFEST_PATH = "config/ascendant_core/core_manifest.json"
const ASCENDANT_CORE_RUNTIME_RULES_PATH = "config/ascendant_core/runtime_rules.json"

const ASCENDANT_CORE_DEFAULT_RULES = {
  enabled: true,
  sync_interval_ticks: 40,
  scoreboards: {
    rank_order: "ar_guild_rank",
    reputation: "ar_guild_rep",
    bounties_completed: "ar_bounties_done",
    structures_cleared: "ar_structures_done",
    bosses_defeated: "ar_bosses_done",
    dragons_defeated: "ar_dragons_done",
    region_tier: "ar_region_tier",
    threat_tier: "ar_threat_tier",
    hunt_kills: "ar_hunt_kills",
    elite_kills: "ar_elite_kills"
  },
  rank_promotions: [],
  region_tiers: [],
  kill_rewards: {},
  minecraft_hostiles: [],
  namespace_roles: {},
  entity_overrides: {}
}

let ascendantCoreRuntimeRules = ASCENDANT_CORE_DEFAULT_RULES
let ascendantCorePlayerTickDelay = {}
let ascendantCoreDeathHookWarned = false

function ascendantCoreReadJson(pathString) {
  const relativePath = String(pathString).replace(/\\/g, "/").replace(/^config\//, "")
  const value = AscendantCoreJsonIO.read(`config/${relativePath}`)
  if (value === null || value === undefined) {
    throw new Error(`missing or empty file: ${pathString}`)
  }
  return value
}

function ascendantCoreIsObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value)
}

function ascendantCoreMergeObjects(base, override) {
  const result = {}
  Object.keys(base || {}).forEach((key) => {
    result[key] = ascendantCoreIsObject(base[key]) ? ascendantCoreMergeObjects(base[key], {}) : base[key]
  })
  Object.keys(override || {}).forEach((key) => {
    result[key] = ascendantCoreIsObject(override[key]) && ascendantCoreIsObject(result[key])
      ? ascendantCoreMergeObjects(result[key], override[key])
      : override[key]
  })
  return result
}

function ascendantCoreSafeText(value, fallback) {
  const text = String(value || fallback || "")
  return text.replace(/["\\]/g, "")
}

function ascendantCoreObjective(server, id, label, color) {
  const objective = ascendantCoreSafeText(id, "")
  if (!/^[A-Za-z0-9_.+-]+$/.test(objective)) {
    console.warn(`[Ascendant Core] Skipping invalid scoreboard objective id: ${id}`)
    return
  }

  const displayLabel = ascendantCoreSafeText(label, objective)
  const displayColor = ascendantCoreSafeText(color, "gray")
  server.runCommandSilent(`scoreboard objectives add ${objective} dummy {"text":"${displayLabel}","color":"${displayColor}"}`)
}

function ascendantCoreLoadRuntimeRules() {
  try {
    return ascendantCoreMergeObjects(ASCENDANT_CORE_DEFAULT_RULES, ascendantCoreReadJson(ASCENDANT_CORE_RUNTIME_RULES_PATH))
  } catch (error) {
    console.warn(`[Ascendant Core] Could not load ${ASCENDANT_CORE_RUNTIME_RULES_PATH}: ${error}`)
    return ASCENDANT_CORE_DEFAULT_RULES
  }
}

function ascendantCoreLoadManifest() {
  try {
    return ascendantCoreReadJson(ASCENDANT_CORE_MANIFEST_PATH)
  } catch (error) {
    console.warn(`[Ascendant Core] Could not load ${ASCENDANT_CORE_MANIFEST_PATH}: ${error}`)
    return { enabled: false, source_registries: {}, domain_files: {}, runtime_scoreboards: [] }
  }
}

function ascendantCoreCheckLinkedFiles(manifest) {
  const linked = []
  const missing = []
  const sources = manifest.source_registries || {}
  const domains = manifest.domain_files || {}
  const runtimeBridge = manifest.runtime_bridge || {}

  Object.keys(sources).forEach((key) => linked.push({ key: key, path: sources[key] }))
  Object.keys(domains).forEach((key) => linked.push({ key: key, path: domains[key] }))
  if (runtimeBridge.runtime_rules) {
    linked.push({ key: "runtime_rules", path: runtimeBridge.runtime_rules })
  }

  linked.forEach((entry) => {
    try {
      const value = ascendantCoreReadJson(String(entry.path))
      if (value === null || value === undefined) {
        missing.push(`${entry.key} -> ${entry.path}`)
      }
    } catch (error) {
      missing.push(`${entry.key} -> ${entry.path}`)
    }
  })

  if (missing.length > 0) {
    console.warn(`[Ascendant Core] Missing linked files: ${missing.join(", ")}`)
  } else {
    console.info(`[Ascendant Core] Loaded ${linked.length} linked registry/domain files.`)
  }
}

function ascendantCoreRegisterScoreboards(server, manifest) {
  const scoreboards = manifest.runtime_scoreboards || []
  scoreboards.forEach((entry) => {
    ascendantCoreObjective(server, entry.id, entry.label, entry.color)
  })
  server.runCommandSilent("scoreboard players set #manifest ar_core_state 1")
  server.runCommandSilent(`scoreboard players set #scoreboards ar_core_state ${scoreboards.length}`)
}

function ascendantCoreRegisterRuntimeScoreboards(server) {
  const boards = ascendantCoreRuntimeRules.scoreboards || {}
  ascendantCoreObjective(server, boards.hunt_kills, "Hunt Kills", "green")
  ascendantCoreObjective(server, boards.elite_kills, "Elite Kills", "dark_purple")
}

function ascendantCoreScore(player, objective, value) {
  if (!player || !objective) {
    return
  }
  player.runCommandSilent(`scoreboard players set @s ${objective} ${Math.floor(Number(value) || 0)}`)
}

function ascendantCoreAddScore(player, objective, value) {
  if (!player || !objective || !value) {
    return
  }
  player.runCommandSilent(`scoreboard players add @s ${objective} ${Math.floor(Number(value) || 0)}`)
}

function ascendantCoreEnsureScore(player, objective, value) {
  if (!player || !objective) {
    return
  }
  const fallbackValue = Math.floor(Number(value) || 0)
  player.runCommandSilent(`execute unless score @s ${objective} matches .. run scoreboard players set @s ${objective} ${fallbackValue}`)
}

function ascendantCoreEnsurePlayerScores(player) {
  const boards = ascendantCoreRuntimeRules.scoreboards || {}
  ;[
    boards.rank_order,
    boards.reputation,
    boards.bounties_completed,
    boards.structures_cleared,
    boards.bosses_defeated,
    boards.dragons_defeated,
    boards.region_tier,
    boards.threat_tier,
    boards.hunt_kills,
    boards.elite_kills
  ].forEach((objective) => ascendantCoreEnsureScore(player, objective, 0))
}

function ascendantCoreApplyRankPromotions(player) {
  const rules = ascendantCoreRuntimeRules
  if (!rules.enabled || !player) {
    return
  }

  var boards = rules.scoreboards || {}
  var rankObjective = boards.rank_order || "ar_guild_rank"
  var promotions = rules.rank_promotions || []
  for (var i = 0; i < promotions.length; i++) {
    var promotion = promotions[i]
    var order = Math.floor(Number(promotion.order) || 0)
    var requirements = promotion.requirements || {}
    var checks = []
    if (requirements.reputation) checks.push(`if score @s ${boards.reputation} matches ${Math.floor(Number(requirements.reputation))}..`)
    if (requirements.hunt_kills) checks.push(`if score @s ${boards.hunt_kills} matches ${Math.floor(Number(requirements.hunt_kills))}..`)
    if (requirements.elite_kills) checks.push(`if score @s ${boards.elite_kills} matches ${Math.floor(Number(requirements.elite_kills))}..`)
    if (requirements.bounties_completed) checks.push(`if score @s ${boards.bounties_completed} matches ${Math.floor(Number(requirements.bounties_completed))}..`)
    if (requirements.structures_cleared) checks.push(`if score @s ${boards.structures_cleared} matches ${Math.floor(Number(requirements.structures_cleared))}..`)
    if (requirements.bosses_defeated) checks.push(`if score @s ${boards.bosses_defeated} matches ${Math.floor(Number(requirements.bosses_defeated))}..`)
    if (requirements.dragons_defeated) checks.push(`if score @s ${boards.dragons_defeated} matches ${Math.floor(Number(requirements.dragons_defeated))}..`)
    if (!promotion.function || checks.length <= 0) {
      continue
    }
    var command = `execute if score @s ${rankObjective} matches ..${order - 1} ${checks.join(" ")} run function ${promotion.function}`
    player.runCommandSilent(command)
  }
}

function ascendantCorePlayerDimension(player) {
  try {
    if (player.level && player.level.dimension) {
      return String(player.level.dimension)
    }
  } catch (error) {
    // fall through
  }
  try {
    if (player.getLevel && player.getLevel().dimension) {
      return String(player.getLevel().dimension())
    }
  } catch (error) {
    // fall through
  }
  return "minecraft:overworld"
}

function ascendantCorePlayerDistance(player) {
  try {
    const x = Number(player.x || 0)
    const z = Number(player.z || 0)
    return Math.floor(Math.sqrt(x * x + z * z))
  } catch (error) {
    return 0
  }
}

function ascendantCoreRegionTier(player) {
  var dimension = ascendantCorePlayerDimension(player)
  var distance = ascendantCorePlayerDistance(player)
  var tiers = ascendantCoreRuntimeRules.region_tiers || []
  var fallback = 0
  for (var i = 0; i < tiers.length; i++) {
    var tier = tiers[i]
    if (tier.dimension && String(tier.dimension) !== dimension) {
      continue
    }
    fallback = Math.max(fallback, Math.floor(Number(tier.tier) || 0))
    if (tier.dimension && !tier.max_distance) {
      return Math.floor(Number(tier.tier) || 0)
    }
    if (tier.max_distance && distance <= Number(tier.max_distance)) {
      return Math.floor(Number(tier.tier) || 0)
    }
  }
  return fallback
}

function ascendantCorePlayerId(player) {
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

function ascendantCoreSyncPlayer(player, force) {
  if (!ascendantCoreRuntimeRules.enabled || !player) {
    return
  }

  const id = ascendantCorePlayerId(player)
  if (!ascendantCorePlayerTickDelay[id]) {
    ascendantCorePlayerTickDelay[id] = 0
  }
  if (!force) {
    ascendantCorePlayerTickDelay[id] -= 1
    if (ascendantCorePlayerTickDelay[id] > 0) {
      return
    }
  }
  ascendantCorePlayerTickDelay[id] = Math.max(1, Math.floor(Number(ascendantCoreRuntimeRules.sync_interval_ticks) || 40))

  const boards = ascendantCoreRuntimeRules.scoreboards || {}
  ascendantCoreEnsurePlayerScores(player)
  ascendantCoreScore(player, boards.region_tier, ascendantCoreRegionTier(player))
  ascendantCoreApplyRankPromotions(player)
}

function ascendantCoreEntityId(entity) {
  if (!entity) {
    return ""
  }
  try {
    if (entity.type) {
      return String(entity.type)
    }
  } catch (error) {
    // fall through
  }
  try {
    if (entity.getType) {
      return String(entity.getType())
    }
  } catch (error) {
    // fall through
  }
  return ""
}

function ascendantCoreEntityNamespace(entityId) {
  return String(entityId || "").split(":")[0]
}

function ascendantCoreFindKiller(source) {
  var candidates = []
  try { candidates.push(source.player) } catch (error) {}
  try { candidates.push(source.actual) } catch (error) {}
  try { candidates.push(source.entity) } catch (error) {}
  try { if (source.getPlayer) candidates.push(source.getPlayer()) } catch (error) {}
  try { if (source.getEntity) candidates.push(source.getEntity()) } catch (error) {}

  var killerCandidate = null
  for (var i = 0; i < candidates.length; i++) {
    killerCandidate = candidates[i]
    if (killerCandidate && typeof killerCandidate.runCommandSilent === "function") {
      return killerCandidate
    }
  }
  return null
}

function ascendantCoreClassifyEntity(entityId) {
  const rules = ascendantCoreRuntimeRules
  const overrides = rules.entity_overrides || {}
  if (overrides[entityId]) {
    return overrides[entityId]
  }

  const minecraftHostiles = rules.minecraft_hostiles || []
  if (minecraftHostiles.indexOf(entityId) >= 0) {
    if (entityId === "minecraft:elder_guardian") {
      return "elite_hunt"
    }
    return "common_hostile"
  }

  const namespace = ascendantCoreEntityNamespace(entityId)
  const namespaceRoles = rules.namespace_roles || {}
  return namespaceRoles[namespace] || ""
}

function ascendantCoreAwardKill(player, entityId, role) {
  const rules = ascendantCoreRuntimeRules
  const boards = rules.scoreboards || {}
  const rewards = (rules.kill_rewards || {})[role]
  if (!rewards) {
    return
  }

  ascendantCoreAddScore(player, boards.reputation, rewards.reputation || 0)
  ascendantCoreAddScore(player, boards.hunt_kills, rewards.hunt_kills || 0)
  ascendantCoreAddScore(player, boards.elite_kills, rewards.elite_kills || 0)
  ascendantCoreAddScore(player, boards.bosses_defeated, rewards.bosses_defeated || 0)
  ascendantCoreAddScore(player, boards.dragons_defeated, rewards.dragons_defeated || 0)
  ascendantCoreScore(player, boards.threat_tier, rewards.threat_tier || 0)

  if (rewards.announce) {
    const label = role === "dragon_tier" ? "Dragon-tier proof recorded" : "Boss proof recorded"
    player.runCommandSilent("title @s times 8 45 12")
    player.runCommandSilent(`title @s subtitle {"text":"${label}","color":"gold","italic":true}`)
    player.runCommandSilent("playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.65 0.95")
  }

  ascendantCoreApplyRankPromotions(player)
}

ServerEvents.loaded((event) => {
  ascendantCoreRuntimeRules = ascendantCoreLoadRuntimeRules()
  const manifest = ascendantCoreLoadManifest()
  if (!manifest.enabled) {
    console.warn("[Ascendant Core] Manifest disabled or unavailable; core bridge is idle.")
    return
  }

  ascendantCoreCheckLinkedFiles(manifest)
  ascendantCoreRegisterScoreboards(event.server, manifest)
  ascendantCoreRegisterRuntimeScoreboards(event.server)
})

PlayerEvents.loggedIn((event) => {
  ascendantCoreSyncPlayer(event.player, true)
})

PlayerEvents.tick((event) => {
  ascendantCoreSyncPlayer(event.player, false)
})

EntityEvents.death((event) => {
  try {
    var deathKillerPlayer = ascendantCoreFindKiller(event.source)
    if (!deathKillerPlayer) {
      return
    }
    var deathEntityId = ascendantCoreEntityId(event.entity)
    var deathRole = ascendantCoreClassifyEntity(deathEntityId)
    if (!deathRole) {
      return
    }
    ascendantCoreAwardKill(deathKillerPlayer, deathEntityId, deathRole)
  } catch (error) {
    if (!ascendantCoreDeathHookWarned) {
      console.warn(`[Ascendant Core] Kill bridge skipped due to unexpected event shape: ${error}`)
      ascendantCoreDeathHookWarned = true
    }
  }
})
