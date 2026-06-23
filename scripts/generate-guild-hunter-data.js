const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), "utf8"));
}

function writeJson(relativePath, data) {
  const target = path.join(root, relativePath);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${JSON.stringify(data, null, 2)}\n`);
}

function writeText(relativePath, text) {
  const target = path.join(root, relativePath);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, text.replace(/\r?\n/g, "\n"));
}

const gearRegistry = readJson("config/ascendant_index/gear_registry.json");
const gearById = new Map();
for (const collection of ["weapons", "armor", "shields", "magic_items", "accessories_relics"]) {
  for (const entry of gearRegistry[collection] || []) {
    if (!gearById.has(entry.id)) {
      gearById.set(entry.id, entry);
    }
  }
}

const rarityRank = {
  common: 1,
  uncommon: 2,
  rare: 3,
  epic: 4,
  legendary: 5,
  mythic: 6,
  ascendant: 7
};

function gear(id) {
  const entry = gearById.get(id);
  if (!entry) {
    throw new Error(`NPC loadout item is missing from gear registry: ${id}`);
  }
  return entry;
}

function slot(id, note, options = {}) {
  const entry = gear(id);
  return {
    item: id,
    name: entry.name,
    source_mod: entry.source_mod,
    rarity: entry.rarity,
    slot_note: note,
    player_obtainable: true,
    override_reason: options.overrideReason || ""
  };
}

const ranks = [
  {
    id: "unranked",
    order: 0,
    name: "Unranked",
    prefix: "[Unranked]",
    color: "gray",
    description: "Not formally recognized by the Guild.",
    evaluation_hint: "Starting state for new players or visitors.",
    suggested_requirements: {
      guild_reputation: 0,
      bounties_completed: 0,
      structure_clears: 0,
      boss_kills: 0,
      notes: "No gate."
    }
  },
  {
    id: "e_rank",
    order: 1,
    name: "E-Rank",
    prefix: "[E-Rank]",
    color: "dark_green",
    description: "A barely registered hunter trusted with simple village requests.",
    evaluation_hint: "Prove survival basics and complete a small local request.",
    suggested_requirements: {
      guild_reputation: 10,
      bounties_completed: 1,
      structure_clears: 0,
      boss_kills: 0,
      notes: "Early game. No dungeon clear required."
    }
  },
  {
    id: "d_rank",
    order: 2,
    name: "D-Rank",
    prefix: "[D-Rank]",
    color: "green",
    description: "A field adventurer who can protect a village from common threats.",
    evaluation_hint: "Complete multiple village requests and survive basic monster hunts.",
    suggested_requirements: {
      guild_reputation: 35,
      bounties_completed: 3,
      structure_clears: 1,
      boss_kills: 0,
      notes: "Should happen after the player has basic gear and one small structure clear."
    }
  },
  {
    id: "c_rank",
    order: 3,
    name: "C-Rank",
    prefix: "[C-Rank]",
    color: "aqua",
    description: "A licensed monster hunter trusted with crypts, towers, and dangerous roads.",
    evaluation_hint: "Clear real structures, complete contract chains, and prove combat competence.",
    suggested_requirements: {
      guild_reputation: 90,
      bounties_completed: 8,
      structure_clears: 3,
      boss_kills: 0,
      notes: "First real social recognition tier."
    }
  },
  {
    id: "b_rank",
    order: 4,
    name: "B-Rank",
    prefix: "[B-Rank]",
    color: "blue",
    description: "An elite hunter able to clear serious dungeons and survive modded threats.",
    evaluation_hint: "Defeat elite mobs, clear larger structures, and outpace rival hunters.",
    suggested_requirements: {
      guild_reputation: 210,
      bounties_completed: 18,
      structure_clears: 8,
      boss_kills: 1,
      notes: "Should require a meaningful boss or miniboss proof."
    }
  },
  {
    id: "a_rank",
    order: 5,
    name: "A-Rank",
    prefix: "[A-Rank]",
    color: "gold",
    description: "A realm-class fighter called when towns expect disaster.",
    evaluation_hint: "Defeat major bosses, protect high-risk settlements, and handle dragon-tier zones.",
    suggested_requirements: {
      guild_reputation: 500,
      bounties_completed: 35,
      structure_clears: 18,
      boss_kills: 4,
      notes: "Late midgame. Should not happen from ordinary grind."
    }
  },
  {
    id: "s_rank",
    order: 6,
    name: "S-Rank",
    prefix: "[S-Rank]",
    color: "dark_purple",
    description: "An ascendant-class anomaly whose actions become public history.",
    evaluation_hint: "Clear realm-level threats and prove command of the full pack stack.",
    suggested_requirements: {
      guild_reputation: 1200,
      bounties_completed: 60,
      structure_clears: 35,
      boss_kills: 10,
      notes: "Endgame myth tier. Should require curated achievements, not simple counters."
    }
  }
];

const rivals = [
  {
    id: "mira_ash",
    name: "Mira Ash",
    rank: "C-Rank",
    class: "Scout",
    home: "frontier guild outposts",
    personality: "careful, observant, loyal when helped",
    preferred_regions: ["forests", "roads", "ruined towers"],
    combat_style: "bow, light blade, evasive movement",
    initial_status: "active",
    relationship_hooks: ["rescue from dungeon", "share map data", "warn about nearby structures"],
    first_rumor: "Mira Ash was seen marking ruins north of the old road.",
    first_encounter: "A wrecked scout camp outside a crypt, with Mira wounded deeper inside."
  },
  {
    id: "darius_crowe",
    name: "Darius Crowe",
    rank: "B-Rank",
    class: "Duelist",
    home: "larger towns and taverns",
    personality: "competitive, proud, theatrical",
    preferred_regions: ["towns", "guild halls", "dungeon entrances"],
    combat_style: "fast sword, shield pressure, duels",
    initial_status: "active",
    relationship_hooks: ["rival bounty race", "formal duel", "tavern bragging"],
    first_rumor: "Darius Crowe has accepted a B-Rank contract before anyone else could sign.",
    first_encounter: "Outside a Guild Hall, challenging the player after repeated contract wins."
  },
  {
    id: "seren_valehart",
    name: "Seren Valehart",
    rank: "B-Rank",
    class: "Arcanist",
    home: "spell libraries and fortified towns",
    personality: "measured, cryptic, curious about corruption",
    preferred_regions: ["ancient ruins", "magic-heavy structures", "celestial event sites"],
    combat_style: "Iron's Spells, wards, spellblade support",
    initial_status: "active",
    relationship_hooks: ["magic milestone advice", "corruption investigation", "shared relic analysis"],
    first_rumor: "Seren Valehart is studying spell residue near a ruined tower.",
    first_encounter: "A magic circle at a structure entrance with Seren warning the player to turn back."
  },
  {
    id: "kael_vorn",
    name: "Kael Vorn",
    rank: "A-Rank",
    class: "Monster Hunter",
    home: "walled hunter towns",
    personality: "quiet, scarred, practical",
    preferred_regions: ["monster dens", "boss approach zones", "snow and mountain roads"],
    combat_style: "heavy weapon, shield, monster trophies",
    initial_status: "rare",
    relationship_hooks: ["aftermath evidence", "rare rescue", "mentor warning"],
    first_rumor: "Kael Vorn returned wounded from the black tower and would not name what followed him.",
    first_encounter: "A cleared monster camp with Kael leaving one warning line before walking away."
  },
  {
    id: "black_hound",
    name: "The Black Hound",
    rank: "S-Rank",
    class: "Unknown",
    home: "unlisted",
    personality: "silent, mythic, unsettling",
    preferred_regions: ["cathedrals", "endgame ruins", "boss aftermath zones"],
    combat_style: "unknown",
    initial_status: "rumored",
    relationship_hooks: ["evidence only", "rare one-line meeting", "S-Rank evaluation context"],
    first_rumor: "The Black Hound was sighted near a ruined cathedral. The monsters were already dead.",
    first_encounter: "Broken weapons, dead monsters, and no visible hunter."
  }
];

const bountyCategories = [
  {
    id: "village_requests",
    name: "Village Requests",
    ranks: ["Unranked", "E-Rank", "D-Rank"],
    purpose: "Make small villages matter and give early players direction.",
    examples: ["deliver medicine", "recover stolen supplies", "clear livestock predators", "repair defenses"]
  },
  {
    id: "monster_hunts",
    name: "Monster Hunts",
    ranks: ["E-Rank", "D-Rank", "C-Rank", "B-Rank"],
    purpose: "Point players toward modded mobs without overwhelming spawn density.",
    examples: ["kill a named undead", "bring monster parts", "clear a night road", "protect villagers"]
  },
  {
    id: "dungeon_contracts",
    name: "Dungeon Contracts",
    ranks: ["C-Rank", "B-Rank", "A-Rank"],
    purpose: "Turn structure exploration into Guild work.",
    examples: ["clear a crypt", "recover a relic", "map a tower", "defeat a structure guardian"]
  },
  {
    id: "rescue_missions",
    name: "Rescue Missions",
    ranks: ["D-Rank", "C-Rank", "B-Rank"],
    purpose: "Create emotional village/rival stakes.",
    examples: ["find a wounded hunter", "escort a villager", "recover a missing scout"]
  },
  {
    id: "rival_claimed_contracts",
    name: "Rival Claimed Contracts",
    ranks: ["C-Rank", "B-Rank", "A-Rank"],
    purpose: "Create competition with named hunters.",
    examples: ["beat Darius to a bounty", "help Mira finish a scout contract", "investigate Kael's aftermath"]
  },
  {
    id: "realm_threats",
    name: "Realm Threats",
    ranks: ["A-Rank", "S-Rank"],
    purpose: "Reserve major bosses and dragon-tier threats for public Guild history.",
    examples: ["defeat a major boss", "secure a dragon zone", "survive a realm event"]
  }
];

const hunterBoards = [
  {
    id: "village_standard",
    name: "Hunter Board - Village Standard",
    size: { width: 7, height: 5, depth: 2 },
    palette: ["dark_oak", "spruce", "deepslate", "lantern", "banner"],
    functional_blocks: ["bountiful:bountyboard", "supplementaries:notice_board"],
    layout: {
      center: "Bountiful board",
      left: "Supplementaries notice board",
      right: "Rank sign or plaque",
      top: "Guild banner and lanterns",
      bottom: "barrel, crate, trophy dressing"
    },
    purpose: "Small village identity and local requests."
  },
  {
    id: "town_guild_board",
    name: "Hunter Board - Town Guild Board",
    size: { width: 9, height: 6, depth: 3 },
    palette: ["dark_oak", "spruce", "deepslate", "iron_bars", "chains", "gold_trim"],
    functional_blocks: ["bountiful:bountyboard", "supplementaries:notice_board"],
    layout: {
      center: "Active contracts",
      left: "Local notices and missing persons",
      right: "Rank postings and hunter sightings",
      top: "large Guild banner",
      bottom: "crates, candles, broken weapons, map table"
    },
    purpose: "Town-scale hub with Guild Clerk and Bounty Master nearby."
  },
  {
    id: "major_registry",
    name: "Hunter Registry - Major Guild Hall",
    size: { width: 13, height: 8, depth: 3 },
    palette: ["deepslate", "dark_oak", "iron", "gold", "soul_lantern"],
    functional_blocks: ["bountiful:bountyboard", "supplementaries:notice_board"],
    layout: {
      center: "Realm contracts",
      left: "S/A/B/C/D/E rank plaques",
      right: "Rival hunter status and major threats",
      top: "Guild crest",
      bottom: "trophy wall and evaluation desk"
    },
    purpose: "Major Guild Hall social identity and rank evaluation."
  }
];

const npcRoster = [
  { id: "guild_registrar", name: "Guild Registrar", role: "registers new hunters and explains the Guild" },
  { id: "rank_examiner", name: "Rank Examiner", role: "evaluates hidden milestones and assigns public rank" },
  { id: "bounty_master", name: "Bounty Master", role: "directs players to local and regional contracts" },
  { id: "guild_clerk", name: "Guild Clerk", role: "small-board social anchor in villages" },
  { id: "hunter_quartermaster", name: "Hunter Quartermaster", role: "spends Guild currency on rank-appropriate supplies" },
  { id: "weapon_appraiser", name: "Weapon Appraiser", role: "ties Simply Swords, Marium, Spartan Shields, and boss loot to rank identity" },
  { id: "arcanist", name: "Guild Arcanist", role: "explains Iron's Spells, magical threats, and corrupted areas" },
  { id: "tavern_keeper", name: "Tavern Keeper", role: "shares rival sightings and local rumors" },
  { id: "guard_captain", name: "Guard Captain", role: "connects Guard Villagers and settlement defense contracts" },
  { id: "wounded_hunter", name: "Wounded Hunter", role: "encounter NPC for rescue and warning events" }
];

const toolAudit = {
  installed: [
    "Bountiful",
    "Guard Villagers",
    "Villager Names",
    "Supplementaries",
    "KubeJS",
    "Open Loader",
    "In Control",
    "Titles",
    "Integrated Villages",
    "IDAS",
    "Loot Integrations",
    "Patchouli",
    "FTB Quests",
    "FTB Ranks",
    "Easy NPC",
    "CustomNPCs-Unofficial",
    "Human Companions",
    "MCA Reborn"
  ],
  delayed: [
    {
      name: "FTB quest chapter data",
      reason: "Installed, but actual quest chapters should be created in-game/exported or generated after confirming current FTB Quests SNBT format."
    },
    {
      name: "FTB rank config",
      reason: "Installed, but public rank assignment config should be generated after first boot creates the expected config structure."
    }
  ]
};

const rankRules = {
  unranked: {
    label: "Unranked",
    allowed_rarities: ["common", "uncommon"],
    max_default_rarity: "uncommon"
  },
  e_rank: {
    label: "E-Rank",
    allowed_rarities: ["common", "uncommon"],
    max_default_rarity: "uncommon"
  },
  d_rank: {
    label: "D-Rank",
    allowed_rarities: ["common", "uncommon", "rare"],
    max_default_rarity: "rare"
  },
  c_rank: {
    label: "C-Rank",
    allowed_rarities: ["common", "uncommon", "rare", "epic"],
    max_default_rarity: "epic"
  },
  b_rank: {
    label: "B-Rank",
    allowed_rarities: ["common", "uncommon", "rare", "epic", "legendary"],
    max_default_rarity: "legendary"
  },
  a_rank: {
    label: "A-Rank",
    allowed_rarities: ["common", "uncommon", "rare", "epic", "legendary", "mythic"],
    max_default_rarity: "mythic"
  },
  s_rank: {
    label: "S-Rank",
    allowed_rarities: ["common", "uncommon", "rare", "epic", "legendary", "mythic", "ascendant"],
    max_default_rarity: "ascendant"
  }
};

const npcLoadouts = {
  version: 1,
  source_registry: "config/ascendant_index/gear_registry.json",
  status: "design contract only; not yet auto-spawned",
  policy: {
    purpose: "Important NPCs and rival hunters should visibly wear gear that players can obtain in the same world.",
    town_npc_tool: "Easy NPC for clerks, examiners, merchants, and dialogue-first social NPCs.",
    combat_npc_tool: "CustomNPCs-Unofficial for rival hunters, elite guards, and combat-capable prototypes.",
    glue_layer: "KubeJS keeps this registry aligned with the generated gear registry and future quest/contract hooks.",
    no_random_junk_rule: "Rivals and important NPCs use curated rank/archetype pools instead of random any-item equipment."
  },
  rank_rules: rankRules,
  drop_policies: {
    not_combatant_no_drops: "Social NPC. No gear drops; the visible gear is identity only.",
    guard_low_value: "Guard profile. Drop normal vanilla/modded loot only if the NPC tool supports safe death handling.",
    rival_story_safe_drops: "Named rival. Do not drop full gear by default; use quest rewards, fragments, trophies, or scripted post-fight rewards.",
    boss_tier_curated: "Myth/S rank profile. Drops must be curated manually so capstone gear is not farmed accidentally."
  },
  archetypes: {
    guild_clerk: {
      rank: "d_rank",
      tool: "Easy NPC",
      purpose: "Village board helper and small-town Guild identity.",
      equipment: {
        mainhand: slot("irons_spellbooks:artificer_cane", "ledger cane / staff silhouette"),
        head: slot("artifacts:villager_hat", "civilian Guild helper identity"),
        chest: slot("immersive_armors:robe_chestplate", "simple robe silhouette")
      },
      drop_policy: "not_combatant_no_drops"
    },
    rank_examiner: {
      rank: "b_rank",
      tool: "Easy NPC",
      purpose: "Formal Guild evaluator with visible authority.",
      equipment: {
        mainhand: slot("irons_spellbooks:truthseeker", "judgment weapon and authority prop"),
        head: slot("irons_spellbooks:gold_crown", "rank authority marker"),
        chest: slot("fantasy_armor:hero_chestplate", "formal heroic armor")
      },
      drop_policy: "not_combatant_no_drops"
    },
    bounty_master: {
      rank: "c_rank",
      tool: "Easy NPC",
      purpose: "Contract board anchor and local danger dispatcher.",
      equipment: {
        mainhand: slot("minecraft:crossbow", "contract hunter sidearm"),
        head: slot("immersive_armors:heavy_helmet", "practical field armor"),
        chest: slot("immersive_armors:heavy_chestplate", "practical field armor")
      },
      drop_policy: "not_combatant_no_drops"
    },
    guild_arcanist: {
      rank: "b_rank",
      tool: "Easy NPC",
      purpose: "Magic systems, spell research, corruption warnings, and arcanist contracts.",
      equipment: {
        mainhand: slot("irons_spellbooks:graybeard_staff", "visible spellcaster staff"),
        offhand: slot("irons_spellbooks:diamond_spell_book", "spellbook identity"),
        head: slot("irons_spellbooks:archevoker_helmet", "academy mage silhouette"),
        chest: slot("irons_spellbooks:archevoker_chestplate", "academy mage silhouette")
      },
      drop_policy: "not_combatant_no_drops"
    },
    hunter_quartermaster: {
      rank: "d_rank",
      tool: "Easy NPC",
      purpose: "Rank vendor prototype and equipment exchange identity.",
      equipment: {
        mainhand: slot("minecraft:iron_sword", "basic supply weapon"),
        head: slot("immersive_armors:steampunk_helmet", "utility workshop silhouette"),
        chest: slot("immersive_armors:steampunk_chestplate", "utility workshop silhouette")
      },
      drop_policy: "not_combatant_no_drops"
    },
    guard_captain: {
      rank: "c_rank",
      tool: "Easy NPC or CustomNPCs-Unofficial",
      purpose: "Visible village defense leader and guard contract source.",
      equipment: {
        mainhand: slot("simplyswords:iron_longsword", "ranked guard weapon"),
        offhand: slot("spartanshields:iron_basic_shield", "ranked guard shield"),
        head: slot("immersive_armors:warrior_helmet", "guard captain silhouette"),
        chest: slot("immersive_armors:warrior_chestplate", "guard captain silhouette")
      },
      drop_policy: "guard_low_value"
    },
    tavern_keeper: {
      rank: "d_rank",
      tool: "Easy NPC",
      purpose: "Rumor hub for rival sightings and village requests.",
      equipment: {
        mainhand: slot("artifacts:universal_attractor", "odd rumor-keeper trinket"),
        head: slot("artifacts:novelty_drinking_hat", "tavern visual identity"),
        chest: slot("immersive_armors:robe_chestplate", "civilian clothing")
      },
      drop_policy: "not_combatant_no_drops"
    },
    village_elder: {
      rank: "d_rank",
      tool: "Easy NPC",
      purpose: "Local representative who connects village needs to the Guild.",
      equipment: {
        mainhand: slot("irons_spellbooks:artificer_cane", "elder cane"),
        head: slot("artifacts:villager_hat", "village authority marker"),
        chest: slot("immersive_armors:robe_chestplate", "civilian clothing")
      },
      drop_policy: "not_combatant_no_drops"
    },
    wounded_hunter: {
      rank: "c_rank",
      tool: "CustomNPCs-Unofficial",
      purpose: "Rescue encounter profile for dungeons, roads, and failed contracts.",
      equipment: {
        mainhand: slot("minecraft:bow", "damaged scout weapon"),
        head: slot("immersive_armors:bone_helmet", "rough field gear"),
        chest: slot("immersive_armors:bone_chestplate", "rough field gear")
      },
      drop_policy: "rival_story_safe_drops"
    }
  },
  npc_profiles: {
    mira_ash: {
      rank: "c_rank",
      archetype: "rival_scout",
      tool: "CustomNPCs-Unofficial",
      purpose: "C-Rank scout rival who maps ruins, needs rescue, and races the player to structure intel.",
      equipment: {
        mainhand: slot("irons_spellbooks:autoloader_crossbow", "scout crossbow"),
        offhand: slot("simplyswords:watching_warglaive", "light close-range backup"),
        head: slot("artifacts:night_vision_goggles", "scout identity"),
        chest: slot("immersive_armors:prismarine_chestplate", "light field armor")
      },
      drop_policy: "rival_story_safe_drops"
    },
    darius_crowe: {
      rank: "b_rank",
      archetype: "rival_duelist",
      tool: "CustomNPCs-Unofficial",
      purpose: "B-Rank duelist rival who challenges the player and competes for high-value contracts.",
      equipment: {
        mainhand: slot("simplyswords:netherite_rapier", "duelist signature weapon"),
        offhand: slot("spartanshields:diamond_basic_shield", "duelist shield"),
        head: slot("fantasy_armor:thief_helmet", "fast duelist silhouette"),
        chest: slot("fantasy_armor:thief_chestplate", "fast duelist silhouette")
      },
      drop_policy: "rival_story_safe_drops"
    },
    seren_valehart: {
      rank: "b_rank",
      archetype: "rival_arcanist",
      tool: "CustomNPCs-Unofficial",
      purpose: "B-Rank arcanist rival tied to Iron's Spells, corruption, and magic contract escalation.",
      equipment: {
        mainhand: slot("irons_spellbooks:magehunter", "mage-hunter spellblade"),
        offhand: slot("irons_spellbooks:diamond_spell_book", "spellbook identity"),
        head: slot("irons_spellbooks:archevoker_helmet", "arcanist identity"),
        chest: slot("irons_spellbooks:archevoker_chestplate", "arcanist identity")
      },
      drop_policy: "rival_story_safe_drops"
    },
    kael_vorn: {
      rank: "a_rank",
      archetype: "rival_monster_hunter",
      tool: "CustomNPCs-Unofficial",
      purpose: "A-Rank monster hunter who appears around boss approaches, dragon zones, and aftermath scenes.",
      equipment: {
        mainhand: slot("iceandfire:dragonbone_sword_fire", "dragon-tier hunter blade"),
        offhand: slot("spartanshields:netherite_basic_shield", "late-game shield"),
        head: slot("fantasy_armor:dragonslayer_helmet", "dragon hunter silhouette"),
        chest: slot("fantasy_armor:dragonslayer_chestplate", "dragon hunter silhouette")
      },
      drop_policy: "rival_story_safe_drops"
    },
    black_hound: {
      rank: "s_rank",
      archetype: "mythic_rival",
      tool: "CustomNPCs-Unofficial",
      purpose: "S-Rank myth rival, mostly evidence and rare appearances.",
      equipment: {
        mainhand: slot("soulsweapons:pure_moonlight_shortsword", "ascendant signature weapon"),
        offhand: slot("cataclysm:gauntlet_of_bulwark", "boss-tier defensive relic"),
        head: slot("soulsweapons:forlorn_helmet", "mythic hooded silhouette"),
        chest: slot("soulsweapons:forlorn_chestplate", "mythic silhouette")
      },
      drop_policy: "boss_tier_curated"
    }
  }
};

const nameplatePalette = {
  unranked: { label: "Unranked", color: "#9CA3AF", frame: "thin_gray" },
  e_rank: { label: "E-Rank", color: "#2E8B57", frame: "green_worn" },
  d_rank: { label: "D-Rank", color: "#55FF55", frame: "green_clean" },
  c_rank: { label: "C-Rank", color: "#55AAFF", frame: "blue_steel" },
  b_rank: { label: "B-Rank", color: "#3366FF", frame: "blue_gold" },
  a_rank: { label: "A-Rank", color: "#FFE66D", frame: "gold_engraved" },
  s_rank: { label: "S-Rank", color: "#D966FF", frame: "violet_mythic" },
  guild_staff: { label: "Guild", color: "#E6FBFF", frame: "guild_silver" }
};

const nameplateProfiles = {
  guild_clerk: { display: "Guild Clerk", rank: "d_rank", level: 18, profession: "Clerk", style: "guild_staff", visibility: "nearby_interaction" },
  rank_examiner: { display: "Rank Examiner", rank: "b_rank", level: 52, profession: "Examiner", style: "guild_staff", visibility: "guild_hall" },
  bounty_master: { display: "Bounty Master", rank: "c_rank", level: 38, profession: "Contracts", style: "guild_staff", visibility: "board_area" },
  guild_arcanist: { display: "Guild Arcanist", rank: "b_rank", level: 49, profession: "Arcanist", style: "guild_staff", visibility: "guild_hall" },
  hunter_quartermaster: { display: "Quartermaster", rank: "d_rank", level: 24, profession: "Supplies", style: "guild_staff", visibility: "nearby_interaction" },
  guard_captain: { display: "Guard Captain", rank: "c_rank", level: 36, profession: "Captain", style: "c_rank", visibility: "settlement_defense" },
  tavern_keeper: { display: "Tavern Keeper", rank: "d_rank", level: 16, profession: "Rumors", style: "guild_staff", visibility: "nearby_interaction" },
  village_elder: { display: "Village Elder", rank: "d_rank", level: 22, profession: "Elder", style: "guild_staff", visibility: "nearby_interaction" },
  wounded_hunter: { display: "Wounded Hunter", rank: "c_rank", level: 31, profession: "Hunter", style: "c_rank", visibility: "encounter" },
  mira_ash: { display: "Mira Ash", rank: "c_rank", level: 34, profession: "Scout", style: "c_rank", visibility: "rival" },
  darius_crowe: { display: "Darius Crowe", rank: "b_rank", level: 47, profession: "Duelist", style: "b_rank", visibility: "rival" },
  seren_valehart: { display: "Seren Valehart", rank: "b_rank", level: 45, profession: "Arcanist", style: "b_rank", visibility: "rival" },
  kael_vorn: { display: "Kael Vorn", rank: "a_rank", level: 68, profession: "Monster Hunter", style: "a_rank", visibility: "rare_rival" },
  black_hound: { display: "The Black Hound", rank: "s_rank", level: 90, profession: "Unknown", style: "s_rank", visibility: "mythic_rumor" }
};

const nameplates = {
  version: 1,
  status: "starter dynamic CustomNPCs identity script implemented; custom client overlay still reserved for the final animated nameplate layer",
  reference_style: "clean two-line nameplate: [ C-Rank ] Mira Ash / Lv. 34 Scout",
  forge_policy: {
    do_not_install_bukkit_plugins: true,
    current_fallback: "FTB Ranks and vanilla scoreboard/team prefixes for players; CustomNPCs scripted always-visible rank/name/level/role line for authored NPCs.",
    likely_custom_mod: "Ascendant Nameplates client overlay if vanilla/NPC fallbacks cannot render the final styled two-line plate."
  },
  palette: nameplatePalette,
  player_default: {
    display: "Player",
    rank: "unranked",
    level_source: "vanilla XP fallback now; Puffish Skills level later if a client overlay can read it cleanly",
    title_source: "Titles mod plus future Guild rank milestones"
  },
  profiles: nameplateProfiles
};

const settlementUnification = {
  version: 1,
  status: "planning/config contract only; no new live template-pool injection in this pass",
  namespace: "ascendant_settlements",
  active_worldgen_changes: [],
  current_safe_overrides: [
    "config/openloader/data/ascendant_realms_world_integration repairs the shared Integrated Villages workstation/POI processor crash path while keeping repaired villages enabled for retest.",
    "Vanilla village/town density is tuned through existing config files, not a new structure injector."
  ],
  custom_mod_threshold: {
    not_needed_yet_for: [
      "curated NPC loadout registry",
      "nameplate data contract",
      "settlement ownership map",
      "Hunter Board blueprint planning",
      "future OpenLoader datapack structure definitions"
    ],
    likely_needed_for: [
      "automatic NPC spawn/equip hooks inside third-party village pieces",
      "polished animated multi-line nameplates over all NPCs and players",
      "fine-grained jigsaw conflict resolution beyond datapack pool injection",
      "runtime village role assignment based on rank, biome, and nearby threats"
    ],
    decision: "Start data-driven. Build the first custom Forge helper mod only when placement, NPC equipment automation, or nameplate rendering requires runtime code."
  },
  ownership: [
    { system: "Vanilla villages", owner: "base settlement layer", action: "keep enabled and denser; add Hunter Board later through controlled templates" },
    { system: "Integrated Villages", owner: "major integrated village layer", action: "keep after workstation processor repair; audit processor/template paths before removal" },
    { system: "Towns and Towers", owner: "town/tower landmark layer", action: "keep density tuned; no direct pool edits yet" },
    { system: "Villages & Pillages", owner: "village flavor layer", action: "keep both-side; watch overlap with village board placement" },
    { system: "IDAS", owner: "dungeon/structure discovery layer", action: "keep as bounty target pool; do not merge into villages blindly" },
    { system: "MVS/MSS/MES/Moogs", owner: "landmark and road-trip layer", action: "keep as exploration destinations and contract targets" },
    { system: "Guard Villagers", owner: "defense layer", action: "use config for guards now; later map guard captains to settlement rank" },
    { system: "Bountiful", owner: "contract board layer", action: "board center for Hunter Board templates" },
    { system: "Supplementaries", owner: "notice board and settlement dressing", action: "notice board sidecar for warnings, rumors, and local identity" },
    { system: "Easy NPC", owner: "social NPC layer", action: "clerks, examiners, merchants, tavern keepers" },
    { system: "CustomNPCs-Unofficial", owner: "rival/combat NPC layer", action: "named rivals, elite guards, scripted combat encounters" },
    { system: "MCA Reborn", owner: "villager social texture/life layer", action: "separate validation only; keep medieval skin control under watch" }
  ],
  first_blueprints: [
    {
      id: "hunter_board_village_standard",
      status: "build in creative, then export template",
      target_size: "7x5x2",
      required_blocks: ["bountiful:bountyboard", "supplementaries:notice_board", "minecraft:dark_oak_planks", "minecraft:deepslate", "minecraft:lantern"],
      npc_hooks: ["guild_clerk", "bounty_master"],
      generation_policy: "standalone locate/test structure first; no village-pool injection until template is stable"
    },
    {
      id: "guild_outpost_frontier",
      status: "design next",
      target_size: "small compound",
      required_rooms: ["Hunter Board", "Rank Examiner desk", "tavern corner", "guard post"],
      npc_hooks: ["rank_examiner", "guard_captain", "mira_ash"]
    }
  ],
  delayed_injection_workflow: [
    "Build structure templates in a creative copy.",
    "Add standalone structures under an OpenLoader datapack and prove /locate plus generation.",
    "Only after standalone proof, inject rare pieces into vanilla or modded village pools.",
    "If pool injection cannot avoid third-party conflicts cleanly, move to a small Ascendant Settlements Forge helper mod."
  ]
};

const npcEquipmentDoc = `# NPC Equipment And Visual Identity

Status: formal registry scaffold implemented. This is not yet auto-spawned into villages.

Ascendant Realms now has a real NPC equipment contract at \`config/ascendant_guild/npc_loadouts.json\`. The goal is simple: important NPCs should look like they belong to the same world the player loots, crafts, and fights through.

## Rules

- Important social NPCs use Easy NPC first.
- Combat-capable rivals and elite encounters use CustomNPCs-Unofficial first.
- Every visible gear piece in the registry points at a real item from \`config/ascendant_index/gear_registry.json\`.
- Social NPCs use no-drop identity gear.
- Rival hunters use curated gear and story-safe drop policies instead of dropping full equipment by default.
- Rank controls the normal rarity ceiling: D-Rank is mostly rare, C-Rank can reach epic, B-Rank can reach legendary, A-Rank can reach mythic, and S-Rank can carry ascendant gear.

## Starting Profiles

- Guild Clerk: robe, villager hat, artificer cane.
- Rank Examiner: crown, hero armor, Truthseeker.
- Bounty Master: heavy armor and crossbow.
- Guild Arcanist: archevoker gear, staff, spell book.
- Quartermaster: steampunk armor and basic supply weapon.
- Guard Captain: warrior armor, Simply Swords weapon, Spartan shield.
- Mira Ash: scout crossbow, night-vision goggles, light armor.
- Darius Crowe: duelist armor, rapier, shield.
- Seren Valehart: arcanist armor, Magehunter, spell book.
- Kael Vorn: dragon-hunter gear and dragonbone weapon.
- The Black Hound: mythic Forlorn gear and ascendant signature weapon.

## Validation

\`scripts/check-pack.py\` now checks that loadout items exist in the generated gear registry, rank rarity ceilings are respected unless an override is documented, named rivals have drop policies, and matching nameplate profiles exist.

## Next Implementation Steps

1. Open a creative test copy.
2. Create Easy NPC templates for Guild Clerk, Rank Examiner, Bounty Master, Arcanist, Quartermaster, Tavern Keeper, and Village Elder.
3. Create CustomNPCs templates for Mira Ash, Darius Crowe, Seren Valehart, Kael Vorn, and The Black Hound.
4. Use the registry as the equipment source, then screenshot/verify each NPC silhouette.
5. Only after templates look good, place them near Hunter Board and Guild Outpost structures.
`;

const settlementsDoc = `# Ascendant Settlements Unification

Status: data-driven planning layer implemented. No new live village injection is active from this pass.

The pack already has many settlement and structure systems. The goal is not to throw another village overhaul on top. The goal is to make one Ascendant-owned layer that decides how villages, Guild boards, guards, names, contracts, and NPCs connect.

## Current Decision

Datapack/config is enough for the next step. A custom Forge helper mod is approved in principle, but not needed until we need runtime NPC-equipment automation, animated nameplate rendering, or deep jigsaw conflict handling that datapacks cannot control safely.

## Ownership Model

The source contract lives in \`config/ascendant_settlements/settlement_unification.json\`.

- Vanilla villages remain the base settlement layer.
- Integrated Villages stays active with the shared workstation/POI processor repair in \`config/openloader/data/ascendant_realms_world_integration\`.
- Towns and Towers, Villages & Pillages, MVS/MSS/MES, Medieval Buildings, IDAS, and YUNG structures are destination and landmark layers.
- Bountiful owns the contract board function.
- Supplementaries owns notice-board dressing.
- Guard Villagers owns baseline village defense.
- Easy NPC owns social Guild NPCs.
- CustomNPCs-Unofficial owns rivals and combat-capable special NPCs.

## Hunter Board Workflow

The first active build should be a standalone Hunter Board structure, not an injected village pool piece.

1. Build \`hunter_board_village_standard\` in creative.
2. Export the structure template.
3. Add it as a standalone datapack structure through OpenLoader.
4. Prove \`/locate\` and natural generation.
5. Only then inject rare board pieces into selected village pools.

This keeps crashes isolated. If a standalone structure fails, it does not corrupt every village generation path.

## Custom Mod Threshold

Build \`Ascendant Settlements\` as a small Forge helper mod only if we hit one of these:

- NPCs need automatic equipment assignment from \`npc_loadouts.json\`.
- Villages need runtime role assignment based on biome, rank, danger, or nearby structures.
- Nameplates need custom animated rendering over players and NPCs.
- Datapack pool injection cannot safely control conflicts between third-party village mods.

Until then, keep the layer data-driven and testable.
`;

const nameplatesDoc = `# Ascendant Nameplates

Status: design contract implemented. The current fallback remains vanilla teams/scoreboard for players and NPC display names for Easy NPC / CustomNPCs.

The target presentation is a clean two-line identity plate:

\`\`\`text
[ C-Rank ] Mira Ash
Lv. 34 Scout
\`\`\`

## Important Compatibility Note

The linked CustomNameplates-style approach is a server-plugin style solution, not the right direct install path for a Forge client/server modpack. Ascendant Realms should treat that look as visual reference only. For Forge, the safe path is:

1. FTB Ranks plus vanilla teams for player rank prefixes.
2. Easy NPC / CustomNPCs display names for important NPCs.
3. A future internal \`Ascendant Nameplates\` client overlay if we need polished animated multi-line plates above every player and NPC.

## Config

The source contract lives at \`config/ascendant_guild/nameplates.json\`.

It defines:

- rank palette
- player fallback
- Guild staff styles
- rival hunter styles
- important NPC profiles
- intended visibility behavior

## Rules

- Every NPC loadout profile needs a matching nameplate profile.
- Rival hunters need rank, level, profession, and style.
- Nameplate rank must match the NPC equipment rank.
- Rank colors must stay inside the shared palette so tooltips, item borders, titles, and NPC plates feel like one system.

## Next Steps

Use fallback nameplates for now. If the fallback still feels flat after NPC templates exist, build the small custom Forge overlay instead of trying to force a Bukkit/Paper nameplate plugin into the Forge pack.
`;

const codexCategories = [
  {
    id: "guild",
    name: "The Guild",
    icon: "minecraft:bell",
    description: "Ranks, evaluation, and the public identity of hunters."
  },
  {
    id: "boards",
    name: "Hunter Boards",
    icon: "minecraft:map",
    description: "Contracts, village requests, notices, and hunter sightings."
  },
  {
    id: "settlements",
    name: "Villages And Towns",
    icon: "minecraft:spruce_door",
    description: "Why settlements matter and how the Guild protects them."
  },
  {
    id: "rivals",
    name: "Rival Hunters",
    icon: "minecraft:iron_sword",
    description: "Named hunters, rumors, competition, and off-screen activity."
  },
  {
    id: "paths",
    name: "Paths Of Power",
    icon: "minecraft:nether_star",
    description: "Combat, magic, skill paths, bounties, and long-term growth."
  }
];

const codexEntries = [
  {
    category: "guild",
    id: "welcome",
    name: "Welcome",
    icon: "minecraft:compass",
    text: "Ascendant Realms is not an empty wilderness. Villages need hunters, Guilds track rank, and the roads are full of contracts. Your name matters when people know what you survived."
  },
  {
    category: "guild",
    id: "ranks",
    name: "Hunter Ranks",
    icon: "minecraft:gold_ingot",
    text: "Guild rank is public reputation, not normal level. Unranked hunters become E, D, C, B, A, and eventually S-Rank by proving real achievements: bounties, structures, bosses, village defense, magic, and weapon mastery."
  },
  {
    category: "guild",
    id: "evaluation",
    name: "Evaluation",
    icon: "minecraft:written_book",
    text: "A Rank Examiner should judge your record at Guild boards or Guild Halls. The first implementation uses tracked milestones and safe visible fallbacks. Later passes can connect FTB Quests, FTB Ranks, and NPC dialogue."
  },
  {
    category: "boards",
    id: "hunter_boards",
    name: "Hunter Boards",
    icon: "minecraft:map",
    text: "A Hunter Board is the center of local Guild life. The Bountiful board handles contracts, the notice board handles warnings and rumors, and rank plaques show what kind of hunter the town expects."
  },
  {
    category: "boards",
    id: "contract_types",
    name: "Contract Types",
    icon: "minecraft:paper",
    text: "Contracts should include village requests, monster hunts, dungeon contracts, rescues, rival-claimed contracts, and realm threats. The board should guide players into existing modded structures instead of leaving them to wander blindly."
  },
  {
    category: "settlements",
    id: "villages_matter",
    name: "Villages Matter",
    icon: "minecraft:oak_door",
    text: "Villages are not decoration. They need guards, names, boards, requests, nearby dangers, and reasons to return. A protected village should feel different from a neglected one."
  },
  {
    category: "settlements",
    id: "guild_towns",
    name: "Guild Towns",
    icon: "minecraft:stone_bricks",
    text: "Major towns should be rare hubs with a Guild Hall, Hunter Board, Rank Examiner, Bounty Master, tavern, market, training yard, and visible rival hunters."
  },
  {
    category: "rivals",
    id: "rival_director",
    name: "Rival Director",
    icon: "minecraft:clock",
    text: "Rival hunters should be real when you can see them and simulated when you cannot. Rumors, camps, claimed contracts, and aftermath scenes make the world move without forcing expensive AI simulation."
  },
  {
    category: "rivals",
    id: "first_rivals",
    name: "First Rivals",
    icon: "minecraft:name_tag",
    text: "Mira Ash scouts ruins. Darius Crowe races you for contracts. Seren Valehart studies magic. Kael Vorn clears monsters before you arrive. The Black Hound is mostly evidence and fear."
  },
  {
    category: "paths",
    id: "guild_marks",
    name: "Guild Marks",
    icon: "minecraft:emerald",
    text: "Guild Marks are the first currency concept. They should come from contracts and rank work, then buy maps, scrolls, food, materials, and rank-appropriate supplies."
  },
  {
    category: "paths",
    id: "early_goals",
    name: "Early Goals",
    icon: "minecraft:campfire",
    text: "Find a village, inspect the Hunter Board, complete a local request, survive the road, clear a small structure, and return for evaluation. The world should explain itself through play."
  }
];

function writeCodexPack(base) {
  writeJson(`${base}/pack.mcmeta`, {
    pack: {
      pack_format: 15,
      description: "Ascendant Realms Guild and Hunter Codex"
    }
  });

  writeText(
    `${base}/README.md`,
    "# Ascendant Realms Codex\n\nThis datapack provides the Patchouli Ascendant Codex outline for Guild ranks, Hunter Boards, villages, rival hunters, and early goals.\n\nThe active OpenLoader load path is `config/openloader/data/ascendant_realms_codex/`.\n"
  );

  writeJson(`${base}/data/ascendant_realms/patchouli_books/ascendant_codex/book.json`, {
    name: "Ascendant Codex",
    landing_text:
      "A field manual for hunters entering Ascendant Realms. Use it to understand Guild ranks, Hunter Boards, villages, rival hunters, and the first path through danger.",
    version: 1,
    use_resource_pack: false
  });

  for (const category of codexCategories) {
    writeJson(`${base}/data/ascendant_realms/patchouli_books/ascendant_codex/en_us/categories/${category.id}.json`, {
      name: category.name,
      description: category.description,
      icon: category.icon
    });
  }

  for (const entry of codexEntries) {
    writeJson(
      `${base}/data/ascendant_realms/patchouli_books/ascendant_codex/en_us/entries/${entry.category}/${entry.id}.json`,
      {
        name: entry.name,
        icon: entry.icon,
        category: `ascendant_realms:${entry.category}`,
        pages: [
          {
            type: "patchouli:text",
            text: entry.text
          }
        ]
      }
    );
  }
}

const loadFunction = `# Visible player identity and Ascendant progression scoreboard for local multiplayer testing.
scoreboard objectives add ar_level level {"text":"Lv","color":"aqua"}
scoreboard objectives add ar_level_last dummy {"text":"Last Lv","color":"gray"}
scoreboard objectives add ar_skill_level dummy {"text":"Ascendant Lv","color":"aqua"}
scoreboard objectives add ar_skill_xp dummy {"text":"Ascendant XP","color":"dark_aqua"}
scoreboard objectives add ar_skill_xp_req dummy {"text":"XP Needed","color":"gray"}
scoreboard objectives add ar_skill_sp dummy {"text":"Skill Points","color":"gold"}
scoreboard objectives add ar_skill_spent dummy {"text":"Spent SP","color":"yellow"}
scoreboard objectives add ar_skill_total dummy {"text":"Total SP","color":"yellow"}
scoreboard objectives add ar_guild_rep dummy {"text":"Guild Rep","color":"gold"}
scoreboard objectives add ar_guild_rank dummy {"text":"Guild Rank","color":"gold"}
scoreboard objectives setdisplay belowName ar_skill_level
team add ar_ascendant {"text":"Ascendant","color":"aqua"}
team modify ar_ascendant prefix [{"text":"[","color":"dark_aqua"},{"text":"Ascendant","color":"aqua"},{"text":"] ","color":"dark_aqua"}]
team modify ar_ascendant color aqua
team modify ar_ascendant nametagVisibility always
team add ar_rank_unranked {"text":"Unranked","color":"gray"}
team modify ar_rank_unranked prefix [{"text":"[","color":"dark_gray"},{"text":"Unranked","color":"gray"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_unranked color gray
team modify ar_rank_unranked nametagVisibility always
team add ar_rank_e {"text":"E-Rank","color":"dark_green"}
team modify ar_rank_e prefix [{"text":"[","color":"dark_gray"},{"text":"E-Rank","color":"dark_green"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_e color dark_green
team modify ar_rank_e nametagVisibility always
team add ar_rank_d {"text":"D-Rank","color":"green"}
team modify ar_rank_d prefix [{"text":"[","color":"dark_gray"},{"text":"D-Rank","color":"green"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_d color green
team modify ar_rank_d nametagVisibility always
team add ar_rank_c {"text":"C-Rank","color":"aqua"}
team modify ar_rank_c prefix [{"text":"[","color":"dark_gray"},{"text":"C-Rank","color":"aqua"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_c color aqua
team modify ar_rank_c nametagVisibility always
team add ar_rank_b {"text":"B-Rank","color":"blue"}
team modify ar_rank_b prefix [{"text":"[","color":"dark_gray"},{"text":"B-Rank","color":"blue"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_b color blue
team modify ar_rank_b nametagVisibility always
team add ar_rank_a {"text":"A-Rank","color":"gold"}
team modify ar_rank_a prefix [{"text":"[","color":"dark_gray"},{"text":"A-Rank","color":"gold"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_a color gold
team modify ar_rank_a nametagVisibility always
team add ar_rank_s {"text":"S-Rank","color":"dark_purple"}
team modify ar_rank_s prefix [{"text":"[","color":"dark_gray"},{"text":"S-Rank","color":"dark_purple"},{"text":"] ","color":"dark_gray"}]
team modify ar_rank_s color dark_purple
team modify ar_rank_s nametagVisibility always
`;

const tickFunction = `# Keep the fallback visible without taking over custom rank teams that may be added later.
# KubeJS mirrors Puffish Skills Ascendant Web level data into ar_skill_level.
team join ar_ascendant @a[team=]
`;

function rankFunction(rank) {
  const team = rank.id === "unranked" ? "ar_rank_unranked" : `ar_rank_${rank.id[0]}`;
  return `team leave @s
team join ${team} @s
scoreboard players set @s ar_guild_rank ${rank.order}
tellraw @s [{"text":"Guild rank set: ","color":"gold"},{"text":"${rank.name}","color":"${rank.color}","bold":true}]
title @s times 10 55 15
title @s title [{"text":"${rank.name}","color":"${rank.color}","bold":true}]
title @s subtitle {"text":"Guild evaluation recorded","color":"gold","italic":true}
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1.0
`;
}

function writeIdentity(base) {
  writeText(`${base}/data/ascendant_identity/functions/load.mcfunction`, loadFunction);
  writeText(`${base}/data/ascendant_identity/functions/tick.mcfunction`, tickFunction);
  for (const rank of ranks) {
    writeText(`${base}/data/ascendant_identity/functions/rank/${rank.id}.mcfunction`, rankFunction(rank));
  }
  writeText(
    `${base}/README.md`,
    "# Ascendant Realms Identity\n\nThis OpenLoader datapack adds the multiplayer identity scoreboard and fallback team layer used by the custom progression HUD bridge.\n\nIt creates `ar_skill_level` for the player-facing Ascendant Web level below names, adds a static `[Ascendant]` team prefix for unnamed/unassigned players, defines Guild rank teams, and provides manual rank functions under `ascendant_identity:rank/*` for testing.\n\n`kubejs/server_scripts/ascendant_progression.js` reads Puffish Skills data, mirrors the current Ascendant Web level into `ar_skill_level`, and renders the custom skill-XP HUD bar.\n"
  );
}

writeText(
  "config/ascendant_guild/README.md",
  "# Ascendant Guild Data\n\nThis folder contains safe data/design scaffolds for the Guild/Hunter system. These JSON files are not a live quest database yet. They define the rank ladder, rival hunters, bounty categories, NPC roles, and Hunter Board blueprints so FTB Quests, FTB Ranks, Easy NPC, CustomNPCs, Bountiful, and KubeJS can be wired deliberately after boot validation.\n"
);
writeJson("config/ascendant_guild/ranks.json", { version: 1, ranks });
writeJson("config/ascendant_guild/rival_hunters.json", { version: 1, rivals });
writeJson("config/ascendant_guild/bounty_categories.json", { version: 1, categories: bountyCategories });
writeJson("config/ascendant_guild/hunter_boards.json", { version: 1, boards: hunterBoards });
writeJson("config/ascendant_guild/npc_roster.json", { version: 1, npcs: npcRoster });
writeJson("config/ascendant_guild/tool_audit.json", { version: 1, ...toolAudit });
writeJson("config/ascendant_guild/npc_loadouts.json", npcLoadouts);
writeJson("config/ascendant_guild/nameplates.json", nameplates);
writeText(
  "config/ascendant_settlements/README.md",
  "# Ascendant Settlements\n\nThis folder owns the village, town, Hunter Board, Guild Outpost, NPC hook, and worldgen-unification planning contracts.\n\nNothing in this folder injects live structures by itself. Keep standalone structure templates and pool injections separate until they pass focused client and server tests.\n"
);
writeJson("config/ascendant_settlements/settlement_unification.json", settlementUnification);
writeText(
  "config/ascendant_settlements/data_scaffold/README.md",
  "# Ascendant Settlements Data Scaffold\n\nReserved namespace for future OpenLoader datapack work after a Hunter Board or Guild Outpost structure template exists.\n\nPlanned paths:\n\n- `data/ascendant_settlements/structures/hunter_board/`\n- `data/ascendant_settlements/worldgen/structure/`\n- `data/ascendant_settlements/worldgen/structure_set/`\n- `data/ascendant_settlements/worldgen/template_pool/`\n\nDo not add live worldgen JSON here until the matching structure template has been built and tested in a creative copy.\n"
);
writeText("docs/NPC_EQUIPMENT_AND_VISUAL_IDENTITY.md", npcEquipmentDoc);
writeText("docs/ASCENDANT_SETTLEMENTS_UNIFICATION.md", settlementsDoc);
writeText("docs/ASCENDANT_NAMEPLATES.md", nameplatesDoc);

for (const base of [
  "config/openloader/data/ascendant_realms_codex",
  "datapacks/ascendant_realms_codex",
  "openloader/data/ascendant_realms_codex"
]) {
  writeCodexPack(base);
}

for (const base of [
  "config/openloader/data/ascendant_realms_identity",
  "openloader/data/ascendant_realms_identity"
]) {
  writeIdentity(base);
}

console.log("Generated Guild/Hunter data, NPC loadouts, settlement contracts, Codex datapack, and rank function scaffolds.");
