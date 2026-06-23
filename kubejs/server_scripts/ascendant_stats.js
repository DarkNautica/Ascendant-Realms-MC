// ============================================================
//  Ascendant Stats - live player stat readout
//  Reads the attributes the Ascendant Web (and gear) affect, mirrors the
//  bonus values to ar_stat_* scoreboards (so FancyMenu can show them on the
//  skills screen / a stats tab), and adds /ascstats for an instant chat panel.
//  Bonus = current attribute value minus its base (what perks + gear add).
// ============================================================

const AST_RL = Java.loadClass("net.minecraft.resources.ResourceLocation")
const AST_REG = Java.loadClass("net.minecraftforge.registries.ForgeRegistries")

// [scoreboard key, label, attribute id, kind]  kind: "pct" -> +N%, "flat" -> +N
const AST_STATS = [
  ["melee",    "Melee Damage",       "puffish_attributes:melee_damage",     "pct",  "off"],
  ["ranged",   "Ranged Damage",      "puffish_attributes:ranged_damage",    "pct",  "off"],
  ["spellpow", "Spell Power",        "irons_spellbooks:spell_power",        "pct",  "off"],
  ["atkdmg",   "Attack Damage",      "generic.attack_damage",               "flat", "off"],
  ["atkspd",   "Attack Speed",       "generic.attack_speed",                "pct",  "off"],
  ["shred",    "Armor Shred",        "puffish_attributes:armor_shred",      "pct",  "off"],
  ["armor",    "Armor",              "generic.armor",                       "flat", "def"],
  ["tough",    "Armor Toughness",    "generic.armor_toughness",             "flat", "def"],
  ["resist",   "Damage Resistance",  "puffish_attributes:resistance",       "pct",  "def"],
  ["magres",   "Magic Resistance",   "puffish_attributes:magic_resistance", "pct",  "def"],
  ["knock",    "Knockback Resist",   "generic.knockback_resistance",        "pct",  "def"],
  ["maxmana",  "Max Mana",           "irons_spellbooks:max_mana",           "flat", "mag"],
  ["manareg",  "Mana Regen",         "irons_spellbooks:mana_regen",         "pct",  "mag"],
  ["cdr",      "Cooldown Reduction", "irons_spellbooks:cooldown_reduction", "pct",  "mag"],
  ["spelres",  "Spell Resistance",   "irons_spellbooks:spell_resist",       "pct",  "mag"],
  ["movespd",  "Movement Speed",     "generic.movement_speed",              "pct",  "util"],
  ["luck",     "Luck",               "generic.luck",                        "flat", "util"],
  ["fortune",  "Fortune",            "puffish_attributes:fortune",          "pct",  "util"],
  ["healing",  "Healing",            "puffish_attributes:healing",          "pct",  "util"],
  ["mining",   "Mining Speed",       "puffish_attributes:mining_speed",     "pct",  "util"],
]
const AST_GROUPS = [["off", "Offense", "#FF8A6B"], ["def", "Defense", "#7FC8FF"], ["mag", "Magic", "#B98CFF"], ["util", "Utility", "#7FE0A0"]]

function astAttr(player, id) {
  try {
    var parts = id.split(":")
    var rl = parts.length === 2 ? new AST_RL(parts[0], parts[1]) : new AST_RL("minecraft", id)
    var attr = AST_REG.ATTRIBUTES.getValue(rl)
    if (!attr) return null
    var inst = player.getAttribute(attr)
    if (!inst) return null
    return Number(inst.getValue()) - Number(inst.getBaseValue())
  } catch (e) { return null }
}
function astFmt(bonus, kind) {
  if (bonus === null) return null
  if (kind === "pct") { var v = Math.round(bonus * 100); return (v >= 0 ? "+" : "") + v + "%" }
  var f = Math.round(bonus * 10) / 10; return (f >= 0 ? "+" : "") + f
}
function astScore(bonus, kind) { if (bonus === null) return 0; return kind === "pct" ? Math.round(bonus * 100) : Math.round(bonus) }

ServerEvents.loaded(event => {
  var s = event.server
  AST_STATS.forEach(st => { try { s.runCommandSilent(`scoreboard objectives add ar_stat_${st[0]} dummy {"text":"${st[1]}"}`) } catch (e) {} })
  console.info("[Ascendant Stats] loaded; " + AST_STATS.length + " stats tracked.")
})

PlayerEvents.tick(event => {
  var p = event.player; if (!p) return
  if ((p.age || 0) % 10 !== 0) return
  try {
    var u = p.uuid.toString(), srv = p.server
    AST_STATS.forEach(st => {
      var b = astAttr(p, st[2])
      srv.runCommandSilent(`scoreboard players set ${u} ar_stat_${st[0]} ${astScore(b, st[3])}`)
    })
  } catch (e) { if (!global.__astTickWarn) { global.__astTickWarn = true; console.warn("[Ascendant Stats] tick: " + e) } }
})

function astShow(player) {
  try {
    player.tell(Text.of("").append(Text.of("—— ").color("#5A6472")).append(Text.of("Ascendant Stats").color("#FFD27A").bold(true)).append(Text.of(" ——").color("#5A6472")))
    AST_GROUPS.forEach(g => {
      var rows = AST_STATS.filter(st => st[4] === g[0])
      var any = false, line = Text.of("")
      rows.forEach(st => {
        var b = astAttr(player, st[2]); var f = astFmt(b, st[3])
        if (f === null || b === 0) return
        any = true
        line.append(Text.of("  " + st[1] + " ").color("#C8CEDA")).append(Text.of(f).color("#86E58A").bold(true))
      })
      if (any) { player.tell(Text.of(g[1]).color(g[2]).bold(true)); player.tell(line) }
    })
  } catch (e) { console.warn("[Ascendant Stats] show: " + e) }
}

ServerEvents.commandRegistry(event => {
  try {
    event.register(event.commands.literal("ascstats").executes(ctx => { var p = ctx.source.player || ctx.source.getEntity(); if (p) astShow(p); return 1 }))
  } catch (e) { console.warn("[Ascendant Stats] command register: " + e) }
})
