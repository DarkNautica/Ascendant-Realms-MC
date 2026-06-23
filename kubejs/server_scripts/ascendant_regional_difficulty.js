// Ascendant regional difficulty bridge.
//
// This keeps the pack's danger multiplier tied to Atlas region/ring location
// instead of world time, day count, or chunk residence duration. It does not
// add boss spawns; it only tags and buffs eligible hostile mobs that already
// spawned from the normal mob stack.

const ARD_JsonIO = typeof JsonIO !== "undefined"
  ? JsonIO
  : Java.loadClass("dev.latvian.mods.kubejs.util.JsonIO")

const ARD_CONFIG_PATH = "config/ascendant_core/regional_difficulty_policy.json"

const ARD_DEFAULTS = {
  enabled: true,
  implementation: {
    region_scoreboard: "ar_atlas_region",
    ring_scoreboard: "ar_atlas_ring",
    nearest_player_radius: 112
  },
  eligibility: {
    hostile_only: true,
    exclude_npc_namespaces: ["customnpcs", "easy_npc", "mca"],
    excluded_entity_ids: [
      "minecraft:player",
      "minecraft:armor_stand",
      "minecraft:item",
      "minecraft:experience_orb",
      "minecraft:ender_dragon",
      "minecraft:wither"
    ]
  },
  region_profiles: {},
  ring_escalation: { enabled: false, profiles: [] }
}

let ascendantRegionalDifficultyConfig = ardReadConfig()
let ascendantRegionalDifficultyWarned = false

function ardIsObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value)
}

function ardMergeObjects(base, override) {
  var result = {}
  Object.keys(base || {}).forEach((key) => {
    result[key] = ardIsObject(base[key]) ? ardMergeObjects(base[key], {}) : base[key]
  })
  Object.keys(override || {}).forEach((key) => {
    result[key] = ardIsObject(override[key]) && ardIsObject(result[key])
      ? ardMergeObjects(result[key], override[key])
      : override[key]
  })
  return result
}

function ardReadConfig() {
  try {
    var parsed = ARD_JsonIO.read(ARD_CONFIG_PATH)
    if (parsed === null || parsed === undefined) {
      console.warn("[Ascendant Regional Difficulty] Missing policy config; using safe defaults.")
      return ARD_DEFAULTS
    }
    return ardMergeObjects(ARD_DEFAULTS, parsed)
  } catch (error) {
    console.warn("[Ascendant Regional Difficulty] Could not read policy config: " + error)
    return ARD_DEFAULTS
  }
}

function ardEntityId(entity) {
  try {
    if (entity && entity.type) return String(entity.type)
  } catch (error) {}
  try {
    if (entity && entity.getType) return String(entity.getType())
  } catch (error) {}
  return ""
}

function ardNamespace(entityId) {
  var text = String(entityId || "")
  var split = text.indexOf(":")
  return split >= 0 ? text.substring(0, split) : text
}

function ardListContains(list, value) {
  if (!Array.isArray(list)) return false
  for (var i = 0; i < list.length; i++) {
    if (String(list[i]) === String(value)) return true
  }
  return false
}

function ardSafeTag(value) {
  return String(value || "unknown").toLowerCase().replace(/[^a-z0-9_]/g, "_")
}

function ardSafeObjective(value, fallback) {
  var text = String(value || fallback || "")
  return /^[A-Za-z0-9_.+-]+$/.test(text) ? text : String(fallback || "ar_atlas_region")
}

function ardNumber(value, fallback) {
  var number = Number(value)
  return isNaN(number) ? fallback : number
}

function ardRun(entity, command) {
  try {
    entity.runCommandSilent(command)
  } catch (error) {
    if (!ascendantRegionalDifficultyWarned) {
      console.warn("[Ascendant Regional Difficulty] Command failed once: " + error)
      ascendantRegionalDifficultyWarned = true
    }
  }
}

function ardShouldScale(entity) {
  if (!ascendantRegionalDifficultyConfig.enabled || !entity) return false
  try {
    if (entity.isPlayer && entity.isPlayer()) return false
  } catch (error) {}

  var entityId = ardEntityId(entity)
  if (entityId === "") return false

  var eligibility = ascendantRegionalDifficultyConfig.eligibility || {}
  if (ardListContains(eligibility.excluded_entity_ids, entityId)) return false
  if (ardListContains(eligibility.exclude_npc_namespaces, ardNamespace(entityId))) return false

  if (eligibility.hostile_only !== false) {
    try {
      if (entity.isMonster && !entity.isMonster()) return false
    } catch (error) {
      return false
    }
  }

  return true
}

function ardSelectorForRegion(profile) {
  var impl = ascendantRegionalDifficultyConfig.implementation || {}
  var regionScore = ardSafeObjective(impl.region_scoreboard, "ar_atlas_region")
  var radius = Math.max(16, Math.floor(ardNumber(impl.nearest_player_radius, 112)))
  var regionId = Math.floor(ardNumber(profile.atlas_region_id, -1))
  return "@p[distance=.." + radius + ",scores={" + regionScore + "=" + regionId + "}]"
}

function ardEffectCommand(effect) {
  var id = String(effect.id || "")
  if (!/^[a-z0-9_.-]+:[a-z0-9_./-]+$/.test(id)) return ""
  var duration = Math.max(1, Math.floor(ardNumber(effect.duration_seconds, 999999)))
  var amplifier = Math.max(0, Math.floor(ardNumber(effect.amplifier, 0)))
  var hideParticles = effect.hide_particles === false ? "false" : "true"
  return "effect give @s " + id + " " + duration + " " + amplifier + " " + hideParticles
}

function ardApplyEffects(entity, profileTag, effects) {
  if (!Array.isArray(effects)) return
  for (var i = 0; i < effects.length; i++) {
    var command = ardEffectCommand(effects[i])
    if (command !== "") {
      ardRun(entity, "execute if entity @s[tag=" + profileTag + "] run " + command)
    }
  }
}

function ardTryRegionProfile(entity, profileKey, profile) {
  if (!ardIsObject(profile)) return
  var selector = ardSelectorForRegion(profile)
  var profileTag = "ar_region_diff_" + ardSafeTag(profileKey)

  ardRun(entity, "execute unless entity @s[tag=ar_region_scaled] if entity " + selector + " run tag @s add ar_region_scaled")
  ardRun(entity, "execute if entity @s[tag=ar_region_scaled] unless entity @s[tag=ar_region_profiled] if entity " + selector + " run tag @s add ar_region_profiled")
  ardRun(entity, "execute if entity @s[tag=ar_region_profiled] if entity " + selector + " run tag @s add " + profileTag)

  var tags = Array.isArray(profile.tags) ? profile.tags : []
  for (var i = 0; i < tags.length; i++) {
    var tag = ardSafeTag(tags[i])
    if (tag !== "") {
      ardRun(entity, "execute if entity @s[tag=" + profileTag + "] run tag @s add " + tag)
    }
  }

  ardApplyEffects(entity, profileTag, profile.effects)
}

function ardApplyRingEscalation(entity) {
  var ringConfig = ascendantRegionalDifficultyConfig.ring_escalation || {}
  if (!ringConfig.enabled || !Array.isArray(ringConfig.profiles)) return

  var impl = ascendantRegionalDifficultyConfig.implementation || {}
  var ringScore = ardSafeObjective(impl.ring_scoreboard, "ar_atlas_ring")
  var radius = Math.max(16, Math.floor(ardNumber(impl.nearest_player_radius, 112)))

  for (var i = 0; i < ringConfig.profiles.length; i++) {
    var profile = ringConfig.profiles[i]
    if (!ardIsObject(profile)) continue
    var minRing = Math.max(0, Math.floor(ardNumber(profile.min_ring, 99)))
    var tag = ardSafeTag(profile.tag || ("ar_region_ring_" + minRing))
    var selector = "@p[distance=.." + radius + ",scores={" + ringScore + "=" + minRing + "..}]"
    ardRun(entity, "execute if entity @s[tag=ar_region_scaled] if entity " + selector + " run tag @s add " + tag)
    ardApplyEffects(entity, tag, profile.effects)
  }
}

EntityEvents.spawned((event) => {
  var entity = event.entity
  if (!ardShouldScale(entity)) return

  var profiles = ascendantRegionalDifficultyConfig.region_profiles || {}
  Object.keys(profiles).forEach((profileKey) => {
    ardTryRegionProfile(entity, profileKey, profiles[profileKey])
  })
  ardApplyRingEscalation(entity)
})

ServerEvents.loaded(() => {
  ascendantRegionalDifficultyConfig = ardReadConfig()
  var profiles = Object.keys(ascendantRegionalDifficultyConfig.region_profiles || {}).length
  console.info("[Ascendant Regional Difficulty] loaded. enabled=" + ascendantRegionalDifficultyConfig.enabled + " profiles=" + profiles)
})
