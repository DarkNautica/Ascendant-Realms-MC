const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const SKILL_ROOTS = [
  path.join(ROOT, "config", "puffish_skills"),
  path.join(ROOT, "datapacks", "ascendant_realms_skills", "data", "ascendant_realms", "puffish_skills"),
  path.join(ROOT, "openloader", "data", "ascendant_realms_skills", "data", "ascendant_realms", "puffish_skills"),
];

const BRANCH_ANGLES = {
  warrior: -90,
  rogue: -39,
  ranger: 12,
  arcanist: 63,
  engineer: 114,
  survivalist: 165,
  dragonbound: 216,
};

const REWARD_MODS = {
  "puffish_attributes:": "puffish_attributes",
  "irons_spellbooks:": "irons_spellbooks",
  "projectile_damage:": "projectile_damage",
};

function reward(attribute, value, operation = "multiply_total") {
  return {
    type: "puffish_skills:attribute",
    data: { attribute, value, operation },
  };
}

function textComponent(text, color = "gray", italic = false, extra = undefined) {
  const component = { text, color, italic };
  if (extra && extra.length > 0) component.extra = extra;
  return component;
}

function modsForRewards(rewards) {
  const mods = new Set();
  for (const entry of rewards) {
    const attribute = entry.data.attribute;
    for (const [prefix, modId] of Object.entries(REWARD_MODS)) {
      if (attribute.startsWith(prefix)) mods.add(modId);
    }
  }
  return Array.from(mods).sort();
}

function nodeDefinition(node) {
  const mods = modsForRewards(node.rewards);
  const extra = [
    {
      text: "\nSP pacing: Puffish awards 1 skill point per Ascendant Web level; higher-tier nodes cost more.",
      color: "dark_gray",
      italic: false,
    },
    {
      text: "\nLayout: clean branch lanes keep choices broad without the old crossing-line web.",
      color: "dark_gray",
      italic: false,
    },
    { text: `\nBranch: ${node.branch}.`, color: "dark_gray", italic: false },
  ];

  if (node.required_spent_points) {
    extra.push({
      text: `\nRequires ${node.required_spent_points} spent points in the unified web.`,
      color: "dark_gray",
      italic: false,
    });
  }

  if (mods.length > 0) {
    extra.push({
      text: `\nRequires loaded mod(s): ${mods.join(", ")}.`,
      color: "dark_gray",
      italic: false,
    });
  }

  if (node.links) {
    extra.push({
      text: `\nPack links: ${node.links}.`,
      color: "dark_aqua",
      italic: false,
    });
  }

  const definition = {
    title: node.title,
    description: textComponent(node.flavor, "gray", true, [
      { text: "\nEffect: ", color: "gold", italic: false },
      { text: node.effect, color: "green", italic: false },
    ]),
    frame: { type: "advancement", data: { frame: node.frame } },
    icon: { type: "item", data: { item: node.icon } },
    cost: node.cost,
    rewards: node.rewards,
    extra_description: textComponent(`Cost: ${node.cost} point${node.cost === 1 ? "" : "s"}.`, "dark_gray", false, extra),
  };

  if (node.required_spent_points) definition.required_spent_points = node.required_spent_points;
  if (mods.length > 0) definition.required_mods = mods;
  return definition;
}

const rootNode = {
  id: "ascendant_oath",
  branch: "Core",
  title: "Ascendant Oath",
  cost: 1,
  frame: "goal",
  icon: "minecraft:nether_star",
  flavor: "The realm remembers every path you choose.",
  effect: "Increases Luck by +0.5 and Damage Resistance by +1%.",
  links: "unified starting point for combat, magic, exploration, crafting, hunting, survival, and dragon-tier paths",
  rewards: [reward("generic.luck", 0.5, "addition"), reward("puffish_attributes:resistance", 0.01)],
};

const branchData = {
  warrior: {
    label: "Warrior",
    nodes: [
      ["battle_rhythm", "Battle Rhythm", "The first swing teaches the second where to land.", "Increases Melee Damage by +3% and Attack Speed by +2%.", "minecraft:iron_sword", [reward("puffish_attributes:melee_damage", 0.03), reward("generic.attack_speed", 0.02, "addition")], "Better Combat baseline tempo"],
      ["shield_craft", "Shield Craft", "Hold the line when the world starts pushing back.", "Increases Knockback Resistance by +5% and Damage Reflection by +2%.", "minecraft:shield", [reward("generic.knockback_resistance", 0.05, "addition"), reward("puffish_attributes:damage_reflection", 0.02)], "Spartan Shields"],
      ["heavy_draw", "Heavy Draw", "A heavy blade should feel inevitable.", "Increases Axe Damage by +5% and Attack Damage by +1.", "minecraft:netherite_axe", [reward("puffish_attributes:axe_damage", 0.05), reward("generic.attack_damage", 1, "addition")], "Simply Swords and heavy Better Combat patterns"],
      ["plate_step", "Plate Step", "Armor is not an excuse to stand still.", "Increases Armor by +1 and Movement Speed by +2%.", "minecraft:iron_boots", [reward("generic.armor", 1, "addition"), reward("generic.movement_speed", 0.02, "addition")], "Immersive Armors movement"],
      ["edge_pressure", "Edge Pressure", "Make armor panic before the wearer does.", "Increases Armor Shred by +4% and Melee Damage by +3%.", "minecraft:stonecutter", [reward("puffish_attributes:armor_shred", 0.04, "addition"), reward("puffish_attributes:melee_damage", 0.03)], "Marium boss armor pressure"],
      ["sword_forms", "Sword Forms", "The same blade can ask three different questions.", "Increases Sword Damage by +6%.", "minecraft:diamond_sword", [reward("puffish_attributes:sword_damage", 0.06)], "Simply Swords"],
      ["guard_break", "Guard Break", "Hit the stance, not the body.", "Increases Toughness Shred by +3% and Knockback Dealt by +3%.", "minecraft:anvil", [reward("puffish_attributes:toughness_shred", 0.03, "addition"), reward("puffish_attributes:knockback", 0.03)], "shielded enemies and armored bosses"],
      ["unyielding_mail", "Unyielding Mail", "Let the monster learn what commitment feels like.", "Increases Armor Toughness by +1 and Melee Resistance by +3%.", "minecraft:netherite_chestplate", [reward("generic.armor_toughness", 1, "addition"), reward("puffish_attributes:melee_resistance", 0.03)], "Immersive Armors and boss melee"],
      ["counter_weight", "Counterweight", "Every block becomes a promise to answer.", "Increases Damage Reflection by +4% and Damage Resistance by +2%.", "minecraft:lodestone", [reward("puffish_attributes:damage_reflection", 0.04), reward("puffish_attributes:resistance", 0.02)], "Spartan Shields counterplay"],
      ["weapon_momentum", "Weapon Momentum", "Keep the chain alive until the room goes quiet.", "Increases Melee Damage by +6% and Attack Speed by +3%.", "minecraft:golden_sword", [reward("puffish_attributes:melee_damage", 0.06), reward("generic.attack_speed", 0.03, "addition")], "Better Combat combos"],
      ["bulwark_training", "Bulwark Training", "The best retreat is a wall that walks forward.", "Increases Knockback Resistance by +8% and Armor by +1.", "minecraft:netherite_leggings", [reward("generic.knockback_resistance", 0.08, "addition"), reward("generic.armor", 1, "addition")], "frontline dungeon pressure"],
      ["soul_edge", "Soul Edge", "Some weapons remember the boss before you meet it.", "Increases Armor Shred by +5% and Sword Damage by +4%.", "minecraft:netherite_sword", [reward("puffish_attributes:armor_shred", 0.05, "addition"), reward("puffish_attributes:sword_damage", 0.04)], "Marium and Cataclysm armor checks"],
      ["warlord_command", "Warlord Command", "Your timing becomes the party metronome.", "Increases Melee Damage by +8% and Damage Resistance by +3%.", "minecraft:white_banner", [reward("puffish_attributes:melee_damage", 0.08), reward("puffish_attributes:resistance", 0.03)], "group fights and village defense"],
      ["bastion_oath", "Bastion Oath", "The line breaks after you do, which is to say never.", "Increases Armor by +2, Armor Toughness by +1, and Damage Reflection by +3%.", "minecraft:netherite_chestplate", [reward("generic.armor", 2, "addition"), reward("generic.armor_toughness", 1, "addition"), reward("puffish_attributes:damage_reflection", 0.03)], "tank capstone"],
      ["giantslayer", "Giantslayer", "Make tall things discover the ground.", "Increases Melee Damage by +10% and Toughness Shred by +5%.", "minecraft:netherite_axe", [reward("puffish_attributes:melee_damage", 0.1), reward("puffish_attributes:toughness_shred", 0.05, "addition")], "Cataclysm, Mowzie, and dragon fights"],
      ["realm_champion", "Realm Champion", "Steel, stance, and nerve become one clean answer.", "Increases Melee Damage by +7%, Attack Speed by +4%, and Armor Shred by +4%.", "minecraft:nether_star", [reward("puffish_attributes:melee_damage", 0.07), reward("generic.attack_speed", 0.04, "addition"), reward("puffish_attributes:armor_shred", 0.04, "addition")], "Warrior capstone"],
    ],
  },
  rogue: {
    label: "Rogue / Duelist",
    nodes: [
      ["quick_step", "Quick Step", "Move before the blade decides where you are.", "Increases Movement Speed by +3% and Sprinting Speed by +4%.", "minecraft:leather_boots", [reward("generic.movement_speed", 0.03, "addition"), reward("puffish_attributes:sprinting_speed", 0.04)], "Combat Roll mobility"],
      ["light_grip", "Light Grip", "A light weapon wins by asking faster questions.", "Increases Attack Speed by +5% and Sword Damage by +3%.", "minecraft:golden_sword", [reward("generic.attack_speed", 0.05, "addition"), reward("puffish_attributes:sword_damage", 0.03)], "Better Combat light weapons"],
      ["soft_landing", "Soft Landing", "The ground is just another escape route.", "Increases Fall Damage Reduction by +8%.", "minecraft:feather", [reward("puffish_attributes:fall_reduction", 0.08)], "Combat Roll cliffs and ruins"],
      ["luckbearer", "Luckbearer", "Who says there is no luck?", "Increases Luck by +1 and Stealth by +3%.", "minecraft:rabbit_foot", [reward("generic.luck", 1, "addition"), reward("puffish_attributes:stealth", 0.03)], "Artifacts, Bountiful, and rare drops"],
      ["knife_window", "Knife Window", "Small openings become full sentences.", "Increases Sword Damage by +5% and Armor Shred by +2%.", "minecraft:shears", [reward("puffish_attributes:sword_damage", 0.05), reward("puffish_attributes:armor_shred", 0.02, "addition")], "duelist finishers"],
      ["roll_recovery", "Roll Recovery", "Exit danger with enough breath to punish it.", "Increases Sprinting Speed by +6% and Damage Resistance by +2%.", "minecraft:ender_pearl", [reward("puffish_attributes:sprinting_speed", 0.06), reward("puffish_attributes:resistance", 0.02)], "Combat Roll recovery"],
      ["silent_looter", "Silent Looter", "The chest opens because it knows better.", "Increases Stealth by +6% and Luck by +0.5.", "minecraft:chest", [reward("puffish_attributes:stealth", 0.06), reward("generic.luck", 0.5, "addition")], "Artifacts and dungeon loot"],
      ["duelist_rhythm", "Duelist Rhythm", "One target, one answer, no wasted motion.", "Increases Melee Damage by +5% and Attack Speed by +3%.", "minecraft:diamond_sword", [reward("puffish_attributes:melee_damage", 0.05), reward("generic.attack_speed", 0.03, "addition")], "Better Combat single-target pressure"],
      ["shadowstep", "Shadowstep", "Arrive in the blind spot and leave a rumor.", "Increases Movement Speed by +4% and Stealth by +5%.", "minecraft:black_dye", [reward("generic.movement_speed", 0.04, "addition"), reward("puffish_attributes:stealth", 0.05)], "scouting dangerous structures"],
      ["artifact_sense", "Artifact Sense", "Treasure has a sound if you are greedy enough.", "Increases Luck by +1 and Fortune by +3%.", "minecraft:emerald", [reward("generic.luck", 1, "addition"), reward("puffish_attributes:fortune", 0.03)], "Artifacts and Loot Integrations"],
      ["backstab_pressure", "Backline Pressure", "The safest enemy is the one that never turns around.", "Increases Armor Shred by +4% and Melee Damage by +4%.", "minecraft:iron_sword", [reward("puffish_attributes:armor_shred", 0.04, "addition"), reward("puffish_attributes:melee_damage", 0.04)], "fast elite kills"],
      ["panic_gap", "Panic Gap", "A bad moment is a doorway if you are fast enough.", "Increases Fall Damage Reduction by +6% and Damage Resistance by +3%.", "minecraft:phantom_membrane", [reward("puffish_attributes:fall_reduction", 0.06), reward("puffish_attributes:resistance", 0.03)], "escape tools"],
      ["cutpurse_legend", "Cutpurse Legend", "The world drops better loot when it respects you.", "Increases Luck by +2 and Stealth by +5%.", "minecraft:gold_ingot", [reward("generic.luck", 2, "addition"), reward("puffish_attributes:stealth", 0.05)], "loot-focused capstone"],
      ["redline_duelist", "Redline Duelist", "Risk becomes rhythm when the fight gets close.", "Increases Attack Speed by +7% and Sword Damage by +6%.", "minecraft:netherite_sword", [reward("generic.attack_speed", 0.07, "addition"), reward("puffish_attributes:sword_damage", 0.06)], "duelist capstone"],
      ["glass_knife", "Glass Knife", "Hit first, hit clean, and do not be there for the answer.", "Increases Melee Damage by +8% and Armor Shred by +5%.", "minecraft:amethyst_shard", [reward("puffish_attributes:melee_damage", 0.08), reward("puffish_attributes:armor_shred", 0.05, "addition")], "high-risk pressure"],
      ["night_market", "Night Market", "The right hands find the impossible things.", "Increases Luck by +1.5, Fortune by +4%, and Movement Speed by +3%.", "minecraft:ender_chest", [reward("generic.luck", 1.5, "addition"), reward("puffish_attributes:fortune", 0.04), reward("generic.movement_speed", 0.03, "addition")], "Rogue capstone"],
    ],
  },
  ranger: {
    label: "Ranger / Hunter",
    nodes: [
      ["field_hunter", "Field Hunter", "Tracks are promises written by things with teeth.", "Increases Ranged Damage by +4% and Tamed Damage by +3%.", "minecraft:bow", [reward("puffish_attributes:ranged_damage", 0.04), reward("puffish_attributes:tamed_damage", 0.03)], "Alex mobs, Mowzie targets, companions"],
      ["tracker_eye", "Tracker Eye", "The wild gives away more than it means to.", "Increases Luck by +1 and Fortune by +3%.", "minecraft:spyglass", [reward("generic.luck", 1, "addition"), reward("puffish_attributes:fortune", 0.03)], "structure scouting and trophies"],
      ["monster_lore", "Monster Lore", "Name the threat and it gets smaller.", "Increases Melee Resistance by +3% and Ranged Resistance by +3%.", "minecraft:writable_book", [reward("puffish_attributes:melee_resistance", 0.03), reward("puffish_attributes:ranged_resistance", 0.03)], "Born in Chaos and Aquamirae"],
      ["bow_tension", "Bow Tension", "The string remembers the horizon.", "Increases Bow Projectile Speed by +7% and Ranged Damage by +3%.", "minecraft:crossbow", [reward("puffish_attributes:bow_projectile_speed", 0.07), reward("puffish_attributes:ranged_damage", 0.03)], "flying and fast mobs"],
      ["beast_breaker", "Beast Breaker", "Big prey needs ugly math.", "Increases Projectile Damage by +1 and Armor Shred by +2%.", "minecraft:arrow", [reward("projectile_damage:generic", 1, "addition"), reward("puffish_attributes:armor_shred", 0.02, "addition")], "large mob hunts"],
      ["pack_bond", "Pack Bond", "A good companion turns distance into courage.", "Increases Tamed Damage by +5% and Tamed Resistance by +4%.", "minecraft:bone", [reward("puffish_attributes:tamed_damage", 0.05), reward("puffish_attributes:tamed_resistance", 0.04)], "companions and pets"],
      ["hide_armor", "Hide Armor", "Light armor should disappear into the brush.", "Increases Armor by +1 and Stealth by +3%.", "minecraft:leather_chestplate", [reward("generic.armor", 1, "addition"), reward("puffish_attributes:stealth", 0.03)], "field armor"],
      ["trophy_marks", "Trophy Marks", "Every scar is a map to the next hunt.", "Increases Luck by +0.75 and Ranged Damage by +4%.", "minecraft:goat_horn", [reward("generic.luck", 0.75, "addition"), reward("puffish_attributes:ranged_damage", 0.04)], "Mowzie and BossesRise trophies"],
      ["venom_reading", "Venom Reading", "The bite is less frightening when you know the animal.", "Increases Damage Resistance by +2% and Magic Resistance by +3%.", "minecraft:spider_eye", [reward("puffish_attributes:resistance", 0.02), reward("puffish_attributes:magic_resistance", 0.03)], "Aquamirae and monster status pressure"],
      ["marksman_breath", "Marksman Breath", "Hold still until the world lines up.", "Increases Ranged Damage by +6% and Bow Projectile Speed by +5%.", "minecraft:tipped_arrow", [reward("puffish_attributes:ranged_damage", 0.06), reward("puffish_attributes:bow_projectile_speed", 0.05)], "boss ranged windows"],
      ["tamed_guard", "Tamed Guard", "The bond goes both ways.", "Increases Tamed Resistance by +8% and Damage Resistance by +2%.", "minecraft:lead", [reward("puffish_attributes:tamed_resistance", 0.08), reward("puffish_attributes:resistance", 0.02)], "companion survivability"],
      ["apex_instinct", "Apex Instinct", "When the big shadow moves, you already moved.", "Increases Movement Speed by +3% and Ranged Resistance by +5%.", "minecraft:rabbit_hide", [reward("generic.movement_speed", 0.03, "addition"), reward("puffish_attributes:ranged_resistance", 0.05)], "dragons and projectile mobs"],
      ["skyshot", "Skyshot", "Bring down anything arrogant enough to fly.", "Increases Projectile Damage by +2 and Bow Projectile Speed by +8%.", "minecraft:spectral_arrow", [reward("projectile_damage:generic", 2, "addition"), reward("puffish_attributes:bow_projectile_speed", 0.08)], "dragons and aerial threats"],
      ["wild_bond", "Wild Bond", "The pack hunts like one nervous system.", "Increases Tamed Damage by +8% and Tamed Resistance by +8%.", "minecraft:name_tag", [reward("puffish_attributes:tamed_damage", 0.08), reward("puffish_attributes:tamed_resistance", 0.08)], "companion capstone"],
      ["monster_slayer", "Monster Slayer", "The realm has many monsters and one answer.", "Increases Melee Damage by +5%, Ranged Damage by +7%, and Armor Shred by +4%.", "minecraft:netherite_sword", [reward("puffish_attributes:melee_damage", 0.05), reward("puffish_attributes:ranged_damage", 0.07), reward("puffish_attributes:armor_shred", 0.04, "addition")], "monster capstone"],
      ["relic_tracker", "Relic Tracker", "You know which ruins are lying about being empty.", "Increases Luck by +1.5, Fortune by +4%, and Damage Resistance by +2%.", "minecraft:compass", [reward("generic.luck", 1.5, "addition"), reward("puffish_attributes:fortune", 0.04), reward("puffish_attributes:resistance", 0.02)], "Ranger capstone"],
    ],
  },
  arcanist: {
    label: "Arcanist",
    nodes: [
      ["spark_focus", "Spark Focus", "A small spell is still a door opening.", "Increases Max Mana by +25 and Spell Power by +3%.", "minecraft:enchanted_book", [reward("irons_spellbooks:max_mana", 25, "addition"), reward("irons_spellbooks:spell_power", 0.03, "addition")], "Iron's Spells basic casting"],
      ["mana_discipline", "Mana Discipline", "Spend power like you expect to survive.", "Increases Mana Regeneration by +10% and Cooldown Reduction by +4%.", "minecraft:lapis_lazuli", [reward("irons_spellbooks:mana_regen", 0.1, "addition"), reward("irons_spellbooks:cooldown_reduction", 0.04, "addition")], "Iron's Spells mana economy"],
      ["warding_glyph", "Warding Glyph", "A ward is a polite refusal to die.", "Increases Spell Resistance by +4% and Magic Resistance by +3%.", "minecraft:amethyst_shard", [reward("irons_spellbooks:spell_resist", 0.04, "addition"), reward("puffish_attributes:magic_resistance", 0.03)], "spell-heavy enemies"],
      ["spellblade_entry", "Spellblade Entry", "The blade is a wand with better manners.", "Increases Spell Power by +4% and Melee Damage by +3%.", "minecraft:golden_sword", [reward("irons_spellbooks:spell_power", 0.04, "addition"), reward("puffish_attributes:melee_damage", 0.03)], "Iron spellblade and Better Combat"],
      ["holy_channel", "Holy Channel", "Mend the wound before it becomes a story.", "Increases Holy Spell Power by +7% and Healing by +4%.", "minecraft:golden_apple", [reward("irons_spellbooks:holy_spell_power", 0.07, "addition"), reward("puffish_attributes:healing", 0.04)], "support magic"],
      ["frost_formula", "Frost Formula", "Cold makes panic move slower.", "Increases Ice Spell Power by +7% and Spell Resistance by +2%.", "minecraft:blue_ice", [reward("irons_spellbooks:ice_spell_power", 0.07, "addition"), reward("irons_spellbooks:spell_resist", 0.02, "addition")], "Aquamirae and frost spells"],
      ["storm_glyph", "Storm Glyph", "Lightning is a shortcut with opinions.", "Increases Lightning Spell Power by +7% and Cast Time Reduction by +3%.", "minecraft:lightning_rod", [reward("irons_spellbooks:lightning_spell_power", 0.07, "addition"), reward("irons_spellbooks:cast_time_reduction", 0.03, "addition")], "storm magic"],
      ["arcane_armor", "Arcane Armor", "A robe is armor if the math is mean enough.", "Increases Armor by +1 and Spell Resistance by +3%.", "minecraft:chainmail_chestplate", [reward("generic.armor", 1, "addition"), reward("irons_spellbooks:spell_resist", 0.03, "addition")], "magic defense gear"],
      ["mana_reservoir", "Mana Reservoir", "Carry enough silence to answer any room.", "Increases Max Mana by +40 and Mana Regeneration by +6%.", "minecraft:ender_eye", [reward("irons_spellbooks:max_mana", 40, "addition"), reward("irons_spellbooks:mana_regen", 0.06, "addition")], "Iron's Spells sustained casting"],
      ["ritual_recovery", "Ritual Recovery", "The circle closes and the body remembers.", "Increases Healing by +7% and Cooldown Reduction by +4%.", "minecraft:glowstone_dust", [reward("puffish_attributes:healing", 0.07), reward("irons_spellbooks:cooldown_reduction", 0.04, "addition")], "recovery after boss spells"],
      ["elemental_weave", "Elemental Weave", "Ice and lightning agree only when you insist.", "Increases Ice Spell Power by +5% and Lightning Spell Power by +5%.", "minecraft:prismarine_crystals", [reward("irons_spellbooks:ice_spell_power", 0.05, "addition"), reward("irons_spellbooks:lightning_spell_power", 0.05, "addition")], "elemental builds"],
      ["spellguard", "Spellguard", "Let hostile magic break itself on the way in.", "Increases Spell Resistance by +6% and Magic Resistance by +4%.", "minecraft:shield", [reward("irons_spellbooks:spell_resist", 0.06, "addition"), reward("puffish_attributes:magic_resistance", 0.04)], "Aquamirae and Iron spell mobs"],
      ["battle_mage", "Battle Mage", "Cast through the swing, then swing through the spell.", "Increases Spell Power by +7%, Melee Damage by +5%, and Cast Time Reduction by +4%.", "minecraft:netherite_sword", [reward("irons_spellbooks:spell_power", 0.07, "addition"), reward("puffish_attributes:melee_damage", 0.05), reward("irons_spellbooks:cast_time_reduction", 0.04, "addition")], "spellblade capstone"],
      ["archmage", "Archmage", "The book opens because it recognizes the hand.", "Increases Max Mana by +60, Spell Power by +8%, and Cooldown Reduction by +6%.", "minecraft:nether_star", [reward("irons_spellbooks:max_mana", 60, "addition"), reward("irons_spellbooks:spell_power", 0.08, "addition"), reward("irons_spellbooks:cooldown_reduction", 0.06, "addition")], "Iron's Spells capstone"],
      ["moonlit_invoker", "Moonlit Invoker", "Night is not darkness. It is fuel.", "Increases Spell Power by +5%, Mana Regeneration by +8%, and Spell Resistance by +4%.", "minecraft:ender_pearl", [reward("irons_spellbooks:spell_power", 0.05, "addition"), reward("irons_spellbooks:mana_regen", 0.08, "addition"), reward("irons_spellbooks:spell_resist", 0.04, "addition")], "Enhanced Celestials nights"],
      ["portal_scholar", "Portal Scholar", "Some doors are not built. They are convinced.", "Increases Cooldown Reduction by +7% and Cast Time Reduction by +5%.", "minecraft:ender_eye", [reward("irons_spellbooks:cooldown_reduction", 0.07, "addition"), reward("irons_spellbooks:cast_time_reduction", 0.05, "addition")], "utility and portal spell pacing"],
    ],
  },
  engineer: {
    label: "Engineer / Artificer",
    nodes: [
      ["tinkers_eye", "Tinkers Eye", "Ore, gear, and ruin all have the same grammar.", "Increases Mining Speed by +4% and Pickaxe Speed by +4%.", "minecraft:iron_pickaxe", [reward("puffish_attributes:mining_speed", 0.04), reward("puffish_attributes:pickaxe_speed", 0.04)], "Create setup"],
      ["workshop_habits", "Workshop Habits", "A clean bench saves more lives than a sharp sword.", "Increases Block Breaking Speed by +5% and Axe Tool Speed by +4%.", "minecraft:crafting_table", [reward("puffish_attributes:breaking_speed", 0.05), reward("puffish_attributes:axe_speed", 0.04)], "base building and Handcrafted"],
      ["belt_logistics", "Belt Logistics", "The machine works better when you do not trip over it.", "Increases Movement Speed by +3% and Sprinting Speed by +4%.", "minecraft:chain", [reward("generic.movement_speed", 0.03, "addition"), reward("puffish_attributes:sprinting_speed", 0.04)], "Create factories"],
      ["provisioner", "Provisioner", "No expedition survives on courage alone.", "Increases Eating/Drinking Speed by +8% and Natural Regeneration by +3%.", "minecraft:bread", [reward("puffish_attributes:consuming_speed", 0.08), reward("puffish_attributes:natural_regeneration", 0.03)], "Farmer's Delight"],
      ["brass_frame", "Brass Frame", "Good engineering makes danger boring.", "Increases Armor by +1 and Damage Resistance by +2%.", "minecraft:copper_ingot", [reward("generic.armor", 1, "addition"), reward("puffish_attributes:resistance", 0.02)], "Create machinery safety"],
      ["cannon_math", "Cannon Math", "If the numbers are right, the wall is temporary.", "Increases Projectile Damage by +1 and Crossbow Projectile Speed by +5%.", "minecraft:crossbow", [reward("projectile_damage:generic", 1, "addition"), reward("puffish_attributes:crossbow_projectile_speed", 0.05)], "Create Big Cannons"],
      ["shipwright", "Shipwright", "A boat is a base that learned courage.", "Increases Mount Speed by +8% and Fall Damage Reduction by +3%.", "minecraft:oak_boat", [reward("puffish_attributes:mount_speed", 0.08), reward("puffish_attributes:fall_reduction", 0.03)], "Small Ships"],
      ["field_repairs", "Field Repairs", "Patch the kit before the kit becomes the problem.", "Increases Healing by +4% and Armor by +1.", "minecraft:iron_ingot", [reward("puffish_attributes:healing", 0.04), reward("generic.armor", 1, "addition")], "long dungeons and sieges"],
      ["factory_stride", "Factory Stride", "Walk the line like you own every gear.", "Increases Sprinting Speed by +6% and Block Breaking Speed by +5%.", "minecraft:rail", [reward("puffish_attributes:sprinting_speed", 0.06), reward("puffish_attributes:breaking_speed", 0.05)], "Create base traversal"],
      ["siege_loader", "Siege Loader", "Load faster, aim calmer, leave less wall.", "Increases Projectile Damage by +1 and Armor Shred by +3%.", "minecraft:tnt", [reward("projectile_damage:generic", 1, "addition"), reward("puffish_attributes:armor_shred", 0.03, "addition")], "Create Big Cannons and boss armor"],
      ["kitchen_engineer", "Kitchen Engineer", "A good meal is applied logistics.", "Increases Eating/Drinking Speed by +10% and Natural Regeneration by +4%.", "minecraft:cake", [reward("puffish_attributes:consuming_speed", 0.1), reward("puffish_attributes:natural_regeneration", 0.04)], "Farmer's Delight and Slice & Dice"],
      ["ruin_reclaimer", "Ruin Reclaimer", "Old stone pays rent when you know where to hit it.", "Increases Mining Speed by +6% and Fortune by +4%.", "minecraft:diamond_pickaxe", [reward("puffish_attributes:mining_speed", 0.06), reward("puffish_attributes:fortune", 0.04)], "structure salvage"],
      ["master_artificer", "Master Artificer", "The workshop becomes a second nervous system.", "Increases Mining Speed by +8%, Block Breaking Speed by +8%, and Fortune by +5%.", "minecraft:netherite_pickaxe", [reward("puffish_attributes:mining_speed", 0.08), reward("puffish_attributes:breaking_speed", 0.08), reward("puffish_attributes:fortune", 0.05)], "crafting capstone"],
      ["siege_engineer", "Siege Engineer", "Some problems need an answer measured in recoil.", "Increases Projectile Damage by +2 and Armor Shred by +4%.", "minecraft:target", [reward("projectile_damage:generic", 2, "addition"), reward("puffish_attributes:armor_shred", 0.04, "addition")], "siege capstone"],
      ["logistics_lord", "Logistics Lord", "Nothing heroic happens without someone moving the supplies.", "Increases Movement Speed by +4%, Eating/Drinking Speed by +8%, and Healing by +5%.", "minecraft:barrel", [reward("generic.movement_speed", 0.04, "addition"), reward("puffish_attributes:consuming_speed", 0.08), reward("puffish_attributes:healing", 0.05)], "party supply capstone"],
      ["fortress_maker", "Fortress Maker", "A home is a machine for surviving tomorrow.", "Increases Armor by +2, Damage Resistance by +3%, and Block Breaking Speed by +5%.", "minecraft:bricks", [reward("generic.armor", 2, "addition"), reward("puffish_attributes:resistance", 0.03), reward("puffish_attributes:breaking_speed", 0.05)], "Engineer capstone"],
    ],
  },
  survivalist: {
    label: "Survivalist / Explorer",
    nodes: [
      ["weather_sense", "Weather Sense", "The sky tells the truth before the logs do.", "Increases Natural Regeneration by +3% and Movement Speed by +2%.", "minecraft:clock", [reward("puffish_attributes:natural_regeneration", 0.03), reward("generic.movement_speed", 0.02, "addition")], "Serene Seasons and weather"],
      ["cold_resolve", "Cold Resolve", "Cold bites less when you bite back.", "Increases Damage Resistance by +2% and Fall Damage Reduction by +4%.", "minecraft:snowball", [reward("puffish_attributes:resistance", 0.02), reward("puffish_attributes:fall_reduction", 0.04)], "Snow Real Magic"],
      ["trail_rations", "Trail Rations", "Pack enough food to make panic optional.", "Increases Eating/Drinking Speed by +8% and Healing by +3%.", "minecraft:cooked_beef", [reward("puffish_attributes:consuming_speed", 0.08), reward("puffish_attributes:healing", 0.03)], "Farmer's Delight exploration"],
      ["hard_travel", "Hard Travel", "Every mountain is just a longer stair.", "Increases Movement Speed by +3% and Sprinting Speed by +4%.", "minecraft:leather_boots", [reward("generic.movement_speed", 0.03, "addition"), reward("puffish_attributes:sprinting_speed", 0.04)], "Terralith and Tectonic travel"],
      ["relic_sense", "Relic Sense", "Ruins do not hide treasure. They test manners.", "Increases Luck by +1 and Fortune by +3%.", "minecraft:compass", [reward("generic.luck", 1, "addition"), reward("puffish_attributes:fortune", 0.03)], "Bountiful and Loot Integrations"],
      ["camp_medic", "Camp Medic", "A small fire and steady hands can reset a disaster.", "Increases Healing by +7% and Natural Regeneration by +3%.", "minecraft:campfire", [reward("puffish_attributes:healing", 0.07), reward("puffish_attributes:natural_regeneration", 0.03)], "field recovery"],
      ["deep_delver", "Deep Delver", "The dark is a room, not an enemy.", "Increases Armor by +1, Melee Resistance by +3%, and Ranged Resistance by +3%.", "minecraft:lantern", [reward("generic.armor", 1, "addition"), reward("puffish_attributes:melee_resistance", 0.03), reward("puffish_attributes:ranged_resistance", 0.03)], "YUNG and Moog dungeons"],
      ["season_keeper", "Season Keeper", "Let the year turn without taking you with it.", "Increases Natural Regeneration by +5% and Damage Resistance by +3%.", "minecraft:wheat", [reward("puffish_attributes:natural_regeneration", 0.05), reward("puffish_attributes:resistance", 0.03)], "Serene Seasons pacing"],
      ["storm_walker", "Storm Walker", "Bad weather is just cover with thunder.", "Increases Movement Speed by +3% and Magic Resistance by +3%.", "minecraft:lightning_rod", [reward("generic.movement_speed", 0.03, "addition"), reward("puffish_attributes:magic_resistance", 0.03)], "Weather, Storms & Tornadoes"],
      ["contract_runner", "Contract Runner", "Every board has a job. Every job has a road.", "Increases Sprinting Speed by +6% and Luck by +0.5.", "minecraft:paper", [reward("puffish_attributes:sprinting_speed", 0.06), reward("generic.luck", 0.5, "addition")], "Bountiful contracts"],
      ["safe_camp", "Safe Camp", "A good camp turns night into planning time.", "Increases Healing by +5% and Damage Resistance by +3%.", "minecraft:soul_campfire", [reward("puffish_attributes:healing", 0.05), reward("puffish_attributes:resistance", 0.03)], "night survival"],
      ["cliff_reader", "Cliff Reader", "The fall starts lying before your foot slips.", "Increases Fall Damage Reduction by +10% and Movement Speed by +2%.", "minecraft:goat_horn", [reward("puffish_attributes:fall_reduction", 0.1), reward("generic.movement_speed", 0.02, "addition")], "Tectonic cliffs"],
      ["pathfinder", "Pathfinder", "The map gets smaller when you stop arguing with it.", "Increases Movement Speed by +5%, Luck by +1, and Fall Damage Reduction by +5%.", "minecraft:map", [reward("generic.movement_speed", 0.05, "addition"), reward("generic.luck", 1, "addition"), reward("puffish_attributes:fall_reduction", 0.05)], "travel capstone"],
      ["hearthkeeper", "Hearthkeeper", "Home is wherever you can recover before sunrise.", "Increases Healing by +8%, Natural Regeneration by +6%, and Damage Resistance by +4%.", "minecraft:campfire", [reward("puffish_attributes:healing", 0.08), reward("puffish_attributes:natural_regeneration", 0.06), reward("puffish_attributes:resistance", 0.04)], "sustain capstone"],
      ["expedition_master", "Expedition Master", "The farther you go, the better prepared you become.", "Increases Luck by +1, Fortune by +4%, and Sprinting Speed by +5%.", "minecraft:lodestone", [reward("generic.luck", 1, "addition"), reward("puffish_attributes:fortune", 0.04), reward("puffish_attributes:sprinting_speed", 0.05)], "structure expedition capstone"],
      ["winter_blood", "Winter Blood", "The harsh world wastes its teeth on you.", "Increases Damage Resistance by +4%, Melee Resistance by +4%, and Ranged Resistance by +4%.", "minecraft:powder_snow_bucket", [reward("puffish_attributes:resistance", 0.04), reward("puffish_attributes:melee_resistance", 0.04), reward("puffish_attributes:ranged_resistance", 0.04)], "Survivalist capstone"],
    ],
  },
  dragonbound: {
    label: "Dragonbound / Endgame",
    nodes: [
      ["wyrm_oath", "Wyrm Oath", "The old fire knows when you are serious.", "Increases Tamed Damage by +4% and Tamed Resistance by +4%.", "minecraft:dragon_head", [reward("puffish_attributes:tamed_damage", 0.04), reward("puffish_attributes:tamed_resistance", 0.04)], "IceAndFire dragon bond"],
      ["scale_tempering", "Scale Tempering", "Armor should remember the element that made it.", "Increases Armor by +1, Fire Magic Resistance by +3%, and Ice Magic Resistance by +3%.", "minecraft:netherite_chestplate", [reward("generic.armor", 1, "addition"), reward("irons_spellbooks:fire_magic_resist", 0.03, "addition"), reward("irons_spellbooks:ice_magic_resist", 0.03, "addition")], "dragon-scale survival"],
      ["dragon_hunter", "Dragon Hunter", "Do not fight the legend. Fight the joints.", "Increases Melee Damage by +5% and Armor Shred by +3%.", "minecraft:netherite_sword", [reward("puffish_attributes:melee_damage", 0.05), reward("puffish_attributes:armor_shred", 0.03, "addition")], "dragon fights"],
      ["boss_sense", "Boss Sense", "The arena feels wrong before the music starts.", "Increases Luck by +1 and Resistance Shred by +3%.", "minecraft:ender_eye", [reward("generic.luck", 1, "addition"), reward("puffish_attributes:resistance_shred", 0.03, "addition")], "Cataclysm and BossesRise"],
      ["abyssal_will", "Abyssal Will", "The void can stare. It does not get to take you.", "Increases Eldritch Magic Resistance by +6%, Ender Magic Resistance by +5%, and Magic Resistance by +4%.", "minecraft:ender_pearl", [reward("irons_spellbooks:eldritch_magic_resist", 0.06, "addition"), reward("irons_spellbooks:ender_magic_resist", 0.05, "addition"), reward("puffish_attributes:magic_resistance", 0.04)], "L_Ender's Cataclysm"],
      ["titanbreaker", "Titanbreaker", "Large health bars are invitations.", "Increases Armor Shred by +5% and Toughness Shred by +4%.", "minecraft:netherite_axe", [reward("puffish_attributes:armor_shred", 0.05, "addition"), reward("puffish_attributes:toughness_shred", 0.04, "addition")], "Cataclysm and Marium bosses"],
      ["mounted_legend", "Mounted Legend", "A mount is not transport. It is a pact.", "Increases Mount Speed by +10% and Tamed Damage by +5%.", "minecraft:saddle", [reward("puffish_attributes:mount_speed", 0.1), reward("puffish_attributes:tamed_damage", 0.05)], "dragons and Small Ships"],
      ["cataclysm_ready", "Cataclysm Ready", "When the room becomes a boss fight, breathe first.", "Increases Damage Resistance by +3% and Damage Reflection by +4%.", "minecraft:totem_of_undying", [reward("puffish_attributes:resistance", 0.03), reward("puffish_attributes:damage_reflection", 0.04)], "late-game survival"],
      ["flame_ward", "Flame Ward", "Fire is a language. Learn the grammar.", "Increases Fire Magic Resistance by +6% and Armor Toughness by +1.", "minecraft:blaze_powder", [reward("irons_spellbooks:fire_magic_resist", 0.06, "addition"), reward("generic.armor_toughness", 1, "addition")], "fire dragons"],
      ["frost_ward", "Frost Ward", "Cold loses its courage around old blood.", "Increases Ice Magic Resistance by +6% and Damage Resistance by +2%.", "minecraft:blue_ice", [reward("irons_spellbooks:ice_magic_resist", 0.06, "addition"), reward("puffish_attributes:resistance", 0.02)], "ice dragons and Aquamirae"],
      ["legendary_pressure", "Legendary Pressure", "Boss armor is only temporary confidence.", "Increases Resistance Shred by +4% and Melee Damage by +5%.", "minecraft:netherite_scrap", [reward("puffish_attributes:resistance_shred", 0.04, "addition"), reward("puffish_attributes:melee_damage", 0.05)], "endgame damage checks"],
      ["dragon_rider", "Dragon Rider", "The sky stops being scenery.", "Increases Mount Speed by +12% and Tamed Resistance by +6%.", "minecraft:elytra", [reward("puffish_attributes:mount_speed", 0.12), reward("puffish_attributes:tamed_resistance", 0.06)], "dragon riding fantasy"],
      ["dragonlord", "Dragonlord", "A pact with a dragon should change the weather in your chest.", "Increases Tamed Damage by +8%, Tamed Resistance by +8%, and Mount Speed by +10%.", "minecraft:dragon_head", [reward("puffish_attributes:tamed_damage", 0.08), reward("puffish_attributes:tamed_resistance", 0.08), reward("puffish_attributes:mount_speed", 0.1)], "dragon capstone"],
      ["realm_ender", "Realm-Ender", "The oldest things in the world learn your name late.", "Increases Spell Power by +8%, Ranged Damage by +8%, and Cooldown Reduction by +6%.", "minecraft:end_crystal", [reward("irons_spellbooks:spell_power", 0.08, "addition"), reward("puffish_attributes:ranged_damage", 0.08), reward("irons_spellbooks:cooldown_reduction", 0.06, "addition")], "Cataclysm and Iron spell capstone"],
      ["mythbreaker", "Mythbreaker", "Stories stop being warnings after you survive them.", "Increases Armor Shred by +5%, Toughness Shred by +5%, and Damage Resistance by +4%.", "minecraft:nether_star", [reward("puffish_attributes:armor_shred", 0.05, "addition"), reward("puffish_attributes:toughness_shred", 0.05, "addition"), reward("puffish_attributes:resistance", 0.04)], "boss-kill capstone"],
      ["ascendant_dragon", "Ascendant Dragon", "The realm makes room when you arrive.", "Increases Melee Damage by +6%, Spell Power by +6%, and Damage Resistance by +5%.", "minecraft:dragon_egg", [reward("puffish_attributes:melee_damage", 0.06), reward("irons_spellbooks:spell_power", 0.06, "addition"), reward("puffish_attributes:resistance", 0.05)], "Dragonbound capstone"],
    ],
  },
};

function buildNode(branchKey, index, tuple) {
  const [shortId, title, flavor, effect, icon, rewards, links] = tuple;
  const tier = Math.floor(index / 4) + 1;
  const cost = tier === 1 ? 1 : tier === 2 ? (index % 4 < 2 ? 1 : 2) : tier === 3 ? 2 : 3;
  const required_spent_points = tier === 2 ? 4 : tier === 3 ? 14 : tier === 4 ? 32 : undefined;
  const frame = tier === 4 ? "challenge" : tier === 3 ? "goal" : "task";

  return {
    id: `${branchKey}_${shortId}`,
    branch: branchData[branchKey].label,
    title,
    flavor,
    effect,
    icon,
    rewards,
    links,
    cost,
    required_spent_points,
    frame,
  };
}

function addConnection(connections, a, b) {
  const key = [a, b].sort().join("|");
  if (!connections.some((entry) => entry.slice().sort().join("|") === key)) {
    connections.push([a, b]);
  }
}

function buildTree() {
  const definitions = { [rootNode.id]: nodeDefinition(rootNode) };
  const skills = { [rootNode.id]: { x: 0, y: 0, definition: rootNode.id, root: true } };
  const connections = [];
  const branchNodeIds = {};

  for (const [branchKey, branch] of Object.entries(branchData)) {
    const angle = (BRANCH_ANGLES[branchKey] * Math.PI) / 180;
    const dx = Math.cos(angle);
    const dy = Math.sin(angle);
    const px = -dy;
    const py = dx;
    branchNodeIds[branchKey] = [];

    branch.nodes.forEach((tuple, index) => {
      const node = buildNode(branchKey, index, tuple);
      definitions[node.id] = nodeDefinition(node);
      branchNodeIds[branchKey].push(node.id);

      const tier = Math.floor(index / 4);
      const withinTier = index % 4;
      const radius = [190, 365, 555, 760][tier];
      const spreads = [
        [-66, -22, 22, 66],
        [-84, -28, 28, 84],
        [-102, -34, 34, 102],
        [-120, -40, 40, 120],
      ];
      const spread = spreads[tier][withinTier];
      skills[node.id] = {
        x: Math.round(dx * radius + px * spread),
        y: Math.round(dy * radius + py * spread),
        definition: node.id,
      };
    });

    for (let i = 0; i < 4; i += 1) addConnection(connections, rootNode.id, branchNodeIds[branchKey][i]);

    for (let tier = 0; tier < 4; tier += 1) {
      const start = tier * 4;
      for (let i = 0; i < 3; i += 1) {
        addConnection(connections, branchNodeIds[branchKey][start + i], branchNodeIds[branchKey][start + i + 1]);
      }
    }

    for (let tier = 0; tier < 3; tier += 1) {
      const start = tier * 4;
      const next = (tier + 1) * 4;
      for (let i = 0; i < 4; i += 1) {
        addConnection(connections, branchNodeIds[branchKey][start + i], branchNodeIds[branchKey][next + i]);
      }
    }
  }

  return {
    config: { version: 3, categories: ["ascendant"] },
    category: {
      unlocked_by_default: true,
      starting_points: 2,
      title: "Ascendant Web",
      description: "One unified progression web with cleaner branch lanes for combat, magic, travel, crafting, hunting, survival, and dragon-tier mastery.",
      icon: { type: "item", data: { item: "minecraft:nether_star" } },
      background: "textures/gui/advancements/backgrounds/adventure.png",
    },
    definitions,
    skills,
    connections: { normal: { bidirectional: connections } },
    experience: {
      level_limit: 120,
      experience_per_level: {
        type: "expression",
        data: { expression: "min(55 + level ^ 1.82 * 11, 2400)" },
      },
      sources: [
        {
          type: "puffish_skills:kill_entity",
          data: {
            variables: {
              dropped_xp: { operations: [{ type: "get_dropped_experience" }] },
              max_health: { operations: [{ type: "get_killed_living_entity" }, { type: "get_max_health" }] },
            },
            experience: "dropped_xp * 0.75 + max_health / 24",
            anti_farming: { limit_per_chunk: 12, reset_after_seconds: 420 },
          },
        },
      ],
    },
  };
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function writeSkillRoot(skillRoot, tree) {
  fs.rmSync(path.join(skillRoot, "categories"), { recursive: true, force: true });
  fs.mkdirSync(path.join(skillRoot, "categories", "ascendant"), { recursive: true });
  writeJson(path.join(skillRoot, "config.json"), tree.config);
  writeJson(path.join(skillRoot, "categories", "ascendant", "category.json"), tree.category);
  writeJson(path.join(skillRoot, "categories", "ascendant", "definitions.json"), tree.definitions);
  writeJson(path.join(skillRoot, "categories", "ascendant", "skills.json"), tree.skills);
  writeJson(path.join(skillRoot, "categories", "ascendant", "connections.json"), tree.connections);
  writeJson(path.join(skillRoot, "categories", "ascendant", "experience.json"), tree.experience);
}

const tree = buildTree();
for (const skillRoot of SKILL_ROOTS) writeSkillRoot(skillRoot, tree);

console.log(
  `Generated Ascendant Web with ${Object.keys(tree.definitions).length} nodes and ${tree.connections.normal.bidirectional.length} connections in ${SKILL_ROOTS.length} load paths.`
);
