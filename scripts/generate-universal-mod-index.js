const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const OUTPUT_DOC = path.join(ROOT, "docs", "UNIVERSAL_MOD_INDEX.md");
const OUTPUT_RARITY_DOC = path.join(ROOT, "docs", "UNIVERSAL_RARITY_AND_INTEGRATION.md");
const OUTPUT_SCHEMA = path.join(ROOT, "config", "ascendant_index", "rarity_schema.json");

const SCAN_DIRS = [
  { folder: "mods", type: "Mod" },
  { folder: "resourcepacks", type: "Resource Pack" },
  { folder: "shaderpacks", type: "Shader Pack" },
];

function read(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

function tomlString(text, key) {
  const match = text.match(new RegExp(`^${key}\\s*=\\s*"([^"]*)"`, "m"));
  return match ? match[1] : "";
}

function sourceFor(text) {
  if (text.includes("[update.curseforge]")) return "CurseForge";
  if (text.includes("[update.modrinth]")) return "Modrinth";
  if (/mode\s*=\s*"metadata:curseforge"/.test(text)) return "CurseForge";
  if (/cdn\.modrinth\.com/.test(text)) return "Modrinth";
  return "Manual/Unknown";
}

function sanitizeCell(value) {
  return String(value || "").replace(/\|/g, "\\|").replace(/\r?\n/g, " ").trim();
}

function inferCategory(entry) {
  const haystack = `${entry.name} ${entry.filename} ${entry.relative}`.toLowerCase();
  const rules = [
    ["Performance", ["modernfix", "ferrite", "embeddium", "entityculling"]],
    ["Shader / Visual Base", ["oculus", "complementary", "entity model", "entity texture", "fresh animations", "3d skin", "cubic", "wavey", "malfu", "not enough animations", "emf", "etf"]],
    ["UI / Presentation", ["tooltip", "enchantment descriptions", "advancement plaques", "fancymenu", "immersive ui", "stoneborn", "rename compat", "xaero", "mobhealthbar", "titles", "traveler", "perception", "beautiful enchanted"]],
    ["Audio / Atmosphere", ["ambient", "sound physics", "biome music", "auroras", "weather", "storm", "tornado", "presence footsteps", "falling leaves", "subtle effects", "particular"]],
    ["Worldgen / Structures", ["terralith", "tectonic", "towns", "towers", "structory", "yung", "sparse", "moog", "mss", "mes", "mvs", "medieval", "integrated", "village", "idas", "ctov"]],
    ["Mobs / Bosses", ["alexs mobs", "mowzie", "born", "aquamirae", "bosses", "cataclysm", "iceandfire", "guard villagers", "variants", "ventures"]],
    ["Combat / Gear", ["better combat", "combat roll", "simply swords", "spartan", "armor", "marium", "fantasy_armor", "projectile damage", "big cannons"]],
    ["Magic", ["iron", "spell", "obscure", "traveloptics"]],
    ["Skills / Difficulty", ["skills", "attributes", "scaling health", "improved mobs", "majrusz", "in control", "spawn balance"]],
    ["Loot / Contracts", ["artifacts", "bountiful", "loot", "villager names"]],
    ["Cohesion / Recipes / Tags", ["kubejs", "open loader", "almost", "polymorph", "every compat", "wood good", "create", "farmers", "delight", "slice", "supplementaries", "amendments", "quark", "zeta", "decorative blocks", "handcrafted", "macaw"]],
    ["Storage / QoL", ["jei", "sophisticated", "backpacks", "visual workbench"]],
    ["Dependency / Library", [" api", "lib", "library", "core", "cloth", "architectury", "curios", "geckolib", "citadel", "moonlight", "resourceful", "rhino", "kotlin", "kambrik", "kiwi", "konkrete", "melody", "puzzles", "silent", "cristel", "corgi", "coro", "cupboard", "bookshelf", "attributefix", "fzzy", "jupiter", "lionfish", "prism", "shatterbyte", "tenshi", "uranus", "data anchor", "fragmentum"]],
  ];

  for (const [category, needles] of rules) {
    if (needles.some((needle) => haystack.includes(needle))) return category;
  }
  return entry.type;
}

function integrationTarget(category, entry) {
  if (entry.type === "Shader Pack") return "Visual profile only";
  if (entry.type === "Resource Pack") return "Resource priority / visual cohesion";
  if (category === "Mobs / Bosses") return "Mob tiers, spawn ecology, drops, bounties, skill milestones";
  if (category === "Worldgen / Structures") return "Structure rarity, biome placement, loot pools, bounty hooks";
  if (category === "Combat / Gear") return "Item rarity, combat roles, skill synergies, loot tiers";
  if (category === "Magic") return "Spell rarity, arcanist milestones, scroll/book loot tiers";
  if (category === "Loot / Contracts") return "Loot tiers, bounty rewards, artifact rarity, reward visibility";
  if (category === "Skills / Difficulty") return "Progression curve, enemy scaling, skill-point pacing";
  if (category === "Cohesion / Recipes / Tags") return "Recipe unification, block palettes, village/dungeon integration";
  if (category === "Audio / Atmosphere") return "Atmosphere profile and biome/dimension mood";
  if (category === "UI / Presentation") return "HUD, tooltip, title, and menu styling";
  return "Track for compatibility and side split";
}

function rarityScope(category, entry) {
  if (entry.type === "Resource Pack" || entry.type === "Shader Pack") return "None";
  if (["Mobs / Bosses", "Worldgen / Structures", "Combat / Gear", "Magic", "Loot / Contracts", "Skills / Difficulty"].includes(category)) {
    return "Required";
  }
  if (category === "Cohesion / Recipes / Tags") return "Conditional";
  return "None";
}

function loadEntries() {
  const entries = [];
  for (const scan of SCAN_DIRS) {
    const dir = path.join(ROOT, scan.folder);
    if (!fs.existsSync(dir)) continue;
    for (const fileName of fs.readdirSync(dir).filter((name) => name.endsWith(".pw.toml")).sort()) {
      const filePath = path.join(dir, fileName);
      const text = read(filePath);
      const entry = {
        relative: `${scan.folder}/${fileName}`.replace(/\\/g, "/"),
        type: scan.type,
        name: tomlString(text, "name") || fileName.replace(/\.pw\.toml$/, ""),
        filename: tomlString(text, "filename"),
        side: tomlString(text, "side") || "unknown",
        source: sourceFor(text),
      };
      entry.category = inferCategory(entry);
      entry.rarityScope = rarityScope(entry.category, entry);
      entry.integrationTarget = integrationTarget(entry.category, entry);
      entries.push(entry);
    }
  }
  return entries.sort((a, b) => a.category.localeCompare(b.category) || a.name.localeCompare(b.name));
}

function writeIndex(entries) {
  const generated = new Date().toISOString();
  const categoryCounts = entries.reduce((acc, entry) => {
    acc[entry.category] = (acc[entry.category] || 0) + 1;
    return acc;
  }, {});

  const lines = [
    "# Universal Mod Index",
    "",
    `Generated by \`scripts/generate-universal-mod-index.js\` on ${generated}.`,
    "",
    "This is the working index for making Ascendant Realms feel like one pack instead of a pile of separate mods. It does not change gameplay by itself; it tells us which mods need rarity, loot, spawn, structure, skill, recipe, UI, or atmosphere integration.",
    "",
    "## Category Counts",
    "",
    "| Category | Count |",
    "|---|---:|",
    ...Object.entries(categoryCounts).sort().map(([category, count]) => `| ${sanitizeCell(category)} | ${count} |`),
    "",
    "## Active Entries",
    "",
    "| Name | Type | Category | Side | Source | Rarity Scope | Integration Target | Metadata |",
    "|---|---|---|---|---|---|---|---|",
  ];

  for (const entry of entries) {
    lines.push(
      `| ${sanitizeCell(entry.name)} | ${sanitizeCell(entry.type)} | ${sanitizeCell(entry.category)} | ${sanitizeCell(entry.side)} | ${sanitizeCell(entry.source)} | ${sanitizeCell(entry.rarityScope)} | ${sanitizeCell(entry.integrationTarget)} | \`${sanitizeCell(entry.relative)}\` |`
    );
  }

  lines.push(
    "",
    "## Next Integration Pass",
    "",
    "- Assign explicit rarity to every Required entry before final survival tuning.",
    "- Use structure rarity to separate village density, dungeon density, rare landmarks, boss arenas, and dragon-tier content.",
    "- Use mob tiers to keep early-game enemies dangerous but not impossible, while keeping elite mobs and bosses lethal later.",
    "- Use skill milestones to connect Arcanist, Engineer, Hunter, Survivalist, Warrior, Rogue, and Dragonbound nodes to actual pack systems.",
    "- Use tooltip styling to show both flavor and exact effects for every custom progression reward."
  );

  fs.writeFileSync(OUTPUT_DOC, `${lines.join("\n")}\n`);
}

function writeRarityDoc(entries) {
  const required = entries.filter((entry) => entry.rarityScope === "Required").length;
  const conditional = entries.filter((entry) => entry.rarityScope === "Conditional").length;
  const lines = [
    "# Universal Rarity And Integration",
    "",
    "## Purpose",
    "",
    "Ascendant Realms needs one shared rarity language across loot, mobs, structures, skills, bounties, boss drops, and tooltips. This file is the design contract for that language.",
    "",
    "## Current Coverage",
    "",
    `- Required rarity/integration entries: ${required}`,
    `- Conditional rarity/integration entries: ${conditional}`,
    "",
    "## Rarity Tiers",
    "",
    "| Tier | Use | Color Direction |",
    "|---|---|---|",
    "| Common | Vanilla baseline, simple materials, routine village supplies | Soft gray/white |",
    "| Uncommon | Early modded gear, helpful food, minor structure loot | Green |",
    "| Rare | Dangerous structure rewards, strong mob drops, branch-defining skill rewards | Blue |",
    "| Epic | Boss-adjacent gear, rare artifacts, major spells, elite bounties | Purple |",
    "| Legendary | Boss drops, dragon materials, late-game weapons, signature artifacts | Gold |",
    "| Mythic | Cataclysm/dragon-tier chase rewards and major pack milestones | Red/orange |",
    "| Ascendant | Pack-defining capstones, final skill-web rewards, named relics | Cyan/white |",
    "",
    "## What Gets A Rarity",
    "",
    "- Items with gameplay power: weapons, armor, artifacts, spell books, scrolls, food buffs, trophies, dragon materials, boss drops.",
    "- Mobs and bosses: passive/ambient, common hostile, dangerous hostile, elite, boss, dragon-tier.",
    "- Structures: common villages, minor ruins, dangerous dungeons, rare landmarks, boss arenas, dragon-tier zones.",
    "- Skills: early utility, branch identity, tier-three specialization, capstone, cross-system milestone.",
    "- Bounties and contracts: normal tasks, dangerous contracts, elite hunts, boss contracts, dragon contracts.",
    "",
    "## HUD And Tooltip Contract",
    "",
    "Every custom skill, relic, bounty reward, or tuned item should have both flavor and exact math:",
    "",
    "- Example name: `Luckbearer`",
    "- Example flavor: `Who says there is no luck?`",
    "- Example exact effect: `Increases Luck by +1 and Stealth by +3%.`",
    "",
    "The exact effect line matters more than the flavor line. If the player cannot tell what they gain, the integration is not finished.",
    "",
    "## Enemy Threat Contract",
    "",
    "Scaling Health is allowed to make mobs stronger, but the pack still needs a separate visual threat layer if we want numeric enemy levels above mobs. Current configs support health bars and difficulty scaling; they do not expose a clean enemy-level nameplate by themselves.",
    "",
    "## Skill Tree Contract",
    "",
    "The Ascendant Web should feel flexible, not like a forced straight build. The current generator keeps one unified tree, broad horizontal choices inside each tier, and cleaner branch lanes to reduce confusing line crossings.",
    "",
    "## Generated Schema",
    "",
    "The matching machine-readable schema lives at `config/ascendant_index/rarity_schema.json`."
  ];

  fs.writeFileSync(OUTPUT_RARITY_DOC, `${lines.join("\n")}\n`);
}

function writeSchema(entries) {
  fs.mkdirSync(path.dirname(OUTPUT_SCHEMA), { recursive: true });
  const schema = {
    version: 1,
    generated_at: new Date().toISOString(),
    tiers: [
      { id: "common", label: "Common", color: "#f2f2f2", use: "Baseline vanilla and routine supplies" },
      { id: "uncommon", label: "Uncommon", color: "#55ff55", use: "Early modded rewards and helpful utility" },
      { id: "rare", label: "Rare", color: "#55aaff", use: "Dangerous structure rewards and branch identity" },
      { id: "epic", label: "Epic", color: "#d966ff", use: "Elite hunts, major artifacts, and powerful spells" },
      { id: "legendary", label: "Legendary", color: "#ffd166", use: "Boss drops, dragon materials, and late-game gear" },
      { id: "mythic", label: "Mythic", color: "#ff6b35", use: "Dragon-tier and Cataclysm-tier chase rewards" },
      { id: "ascendant", label: "Ascendant", color: "#7df9ff", use: "Pack-defining capstones and named relics" },
    ],
    domains: {
      items: ["common", "uncommon", "rare", "epic", "legendary", "mythic", "ascendant"],
      mobs: ["ambient", "common_hostile", "dangerous_hostile", "elite", "boss", "dragon_tier"],
      structures: ["common_village", "minor_ruin", "dangerous_dungeon", "rare_landmark", "boss_arena", "dragon_tier_zone"],
      skills: ["early_utility", "branch_identity", "specialization", "capstone", "cross_system_milestone"],
      bounties: ["routine", "dangerous", "elite", "boss", "dragon"],
    },
    entries_needing_rarity: entries
      .filter((entry) => entry.rarityScope !== "None")
      .map((entry) => ({
        name: entry.name,
        metadata: entry.relative,
        category: entry.category,
        side: entry.side,
        rarity_scope: entry.rarityScope,
        integration_target: entry.integrationTarget,
      })),
  };

  fs.writeFileSync(OUTPUT_SCHEMA, `${JSON.stringify(schema, null, 2)}\n`);
}

const entries = loadEntries();
writeIndex(entries);
writeRarityDoc(entries);
writeSchema(entries);
console.log(`Generated universal index for ${entries.length} entries.`);
