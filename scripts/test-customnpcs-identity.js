#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const scriptPath = path.join(root, "customnpcs", "scripts", "ecmascript", "ascendant_npc_identity.js");
const nameplatesPath = path.join(root, "config", "ascendant_guild", "nameplates.json");
const scriptText = fs.readFileSync(scriptPath, "utf8");
const nameplates = JSON.parse(fs.readFileSync(nameplatesPath, "utf8"));

function createNpc(initialName, initialStoredData) {
  const stored = { ...(initialStoredData || {}) };
  const executedCommands = [];
  const display = {
    name: initialName,
    title: "old title",
    showName: 1,
    setName(value) {
      this.name = value;
    },
    getName() {
      return this.name;
    },
    setTitle(value) {
      this.title = value;
    },
    getTitle() {
      return this.title;
    },
    setShowName(value) {
      this.showName = value;
    },
  };

  return {
    display,
    updated: false,
    getDisplay() {
      return display;
    },
    getStoreddata() {
      return {
        has(key) {
          return Object.prototype.hasOwnProperty.call(stored, key);
        },
        get(key) {
          return stored[key];
        },
        put(key, value) {
          stored[key] = value;
        },
      };
    },
    updateClient() {
      this.updated = true;
    },
    executeCommand(command) {
      executedCommands.push(command);
      return "ok";
    },
    sayTo(player, message) {
      if (player && player.messages) {
        player.messages.push(message);
      }
    },
    stored,
    executedCommands,
  };
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(scriptText, sandbox, { filename: scriptPath });

function runCase(name, initialName, initialStoredData, expectedNamePart, expectedRank) {
  const npc = createNpc(initialName, initialStoredData);
  sandbox.init({ npc });
  assert(npc.display.name.includes(expectedNamePart), `${name}: expected name to include ${expectedNamePart}, got ${npc.display.name}`);
  assert(npc.display.title === "", `${name}: title should be cleared, got ${npc.display.title}`);
  assert(npc.display.showName === 0, `${name}: showName should be 0, got ${npc.display.showName}`);
  assert(npc.updated, `${name}: updateClient should be called`);
  assert(npc.stored.ar_rank === expectedRank, `${name}: stored ar_rank should be ${expectedRank}, got ${npc.stored.ar_rank}`);
  return npc;
}

const rankLabels = {
  unranked: "Unranked",
  e_rank: "E-Rank",
  d_rank: "D-Rank",
  c_rank: "C-Rank",
  b_rank: "B-Rank",
  a_rank: "A-Rank",
  s_rank: "S-Rank",
};

runCase(
  "fresh profile key",
  "ar:rank_examiner",
  {},
  "[B-Rank] \u00a7fRank Examiner \u00a78| \u00a77Lv.52 \u00a76Examiner",
  "B-Rank"
);

runCase(
  "stale guild style id",
  "\u00a7b[Guild] \u00a7fRank Examiner",
  {
    ar_profile: "rank_examiner",
    ar_name: "Rank Examiner",
    ar_rank: "guild_staff",
    ar_role: "Examiner",
    ar_level: "52.0",
  },
  "[B-Rank] \u00a7fRank Examiner \u00a78| \u00a77Lv.52 \u00a76Examiner",
  "B-Rank"
);

runCase(
  "stale unranked display",
  "\u00a77[Unranked] \u00a7fRank Examiner",
  {
    ar_profile: "rank_examiner",
    ar_name: "Rank Examiner",
    ar_rank: "B-Rank",
    ar_role: "Examiner",
    ar_level: "52",
  },
  "[B-Rank] \u00a7fRank Examiner \u00a78| \u00a77Lv.52 \u00a76Examiner",
  "B-Rank"
);

runCase(
  "stale unranked stored rank",
  "ar:rank_examiner",
  {
    ar_profile: "rank_examiner",
    ar_name: "Rank Examiner",
    ar_rank: "Unranked",
    ar_role: "Examiner",
    ar_level: "52",
  },
  "[B-Rank] \u00a7fRank Examiner \u00a78| \u00a77Lv.52 \u00a76Examiner",
  "B-Rank"
);

runCase(
  "mira rival",
  "ar:mira_ash",
  {},
  "[C-Rank] \u00a7fMira Ash \u00a78| \u00a77Lv.34 \u00a79Scout",
  "C-Rank"
);

for (const [profileId, profile] of Object.entries(nameplates.profiles)) {
  const expectedRank = rankLabels[profile.rank] || "Unranked";
  const expectedLevel = String(profile.level);
  const expectedRole = String(profile.profession);
  const expectedDisplay = String(profile.display);
  const npc = createNpc(`ar:${profileId}`, {});
  sandbox.init({ npc });
  assert(
    npc.display.name.includes(`[${expectedRank}]`),
    `${profileId}: expected public rank ${expectedRank}, got ${npc.display.name}`
  );
  assert(
    npc.display.name.includes(expectedDisplay),
    `${profileId}: expected display ${expectedDisplay}, got ${npc.display.name}`
  );
  assert(
    npc.display.name.includes(`Lv.${expectedLevel}`),
    `${profileId}: expected level ${expectedLevel}, got ${npc.display.name}`
  );
  assert(
    npc.display.name.includes(expectedRole),
    `${profileId}: expected role ${expectedRole}, got ${npc.display.name}`
  );
  assert(
    npc.stored.ar_rank === expectedRank,
    `${profileId}: expected stored rank ${expectedRank}, got ${npc.stored.ar_rank}`
  );
}

{
  const npc = createNpc("ar:rank_examiner", {});
  const player = {
    messages: [],
    getName() {
      return "zedyy";
    },
  };
  sandbox.interact({ npc, player });
  assert(
    npc.executedCommands.includes("execute as zedyy run function ascendant_identity:rank_examiner/evaluate"),
    `rank examiner interact should execute evaluation as player, got ${npc.executedCommands.join(", ")}`
  );
  assert(
    !player.messages.some((message) => String(message).includes("/function")),
    `rank examiner interact must not tell player to type a command, got ${player.messages.join(" | ")}`
  );
}

{
  const npc = createNpc("ar:mira_ash", {});
  const player = {
    messages: [],
    getName() {
      return "zedyy";
    },
  };
  sandbox.interact({ npc, player });
  assert(
    npc.executedCommands.length === 0,
    `non-examiner NPCs must not execute commands, got ${npc.executedCommands.join(", ")}`
  );
  assert(
    player.messages.some((message) => String(message).includes("I do not scout for strangers")),
    `Mira should use relationship dialogue, got ${player.messages.join(" | ")}`
  );
  assert(
    player.messages.some((message) => String(message).includes("I do not take orders from strangers")),
    `first interaction should make command boundary clear, got ${player.messages.join(" | ")}`
  );
  assert(
    npc.stored.ar_rel_zedyy_mira_ash_talks === "1",
    `Mira should record per-player familiarity, got ${JSON.stringify(npc.stored)}`
  );
}

{
  const npc = createNpc("ar:guard_captain", {});
  const player = {
    messages: [],
    getName() {
      return "zedyy";
    },
  };
  sandbox.interact({ npc, player });
  sandbox.interact({ npc, player });
  assert(
    npc.executedCommands.length === 0,
    `Guard Captain must not execute player command bridges, got ${npc.executedCommands.join(", ")}`
  );
  assert(
    npc.stored.ar_last_relation_tier === "familiar",
    `second interaction should reach familiar relation tier, got ${npc.stored.ar_last_relation_tier}`
  );
  assert(
    player.messages.some((message) => String(message).includes("not a follower")),
    `familiar dialogue should still refuse follower behavior, got ${player.messages.join(" | ")}`
  );
}

console.log("CustomNPCs identity script tests passed.");
