# Ascendant Web - Milestone & Keystone Design

Status: **Phase 1 IMPLEMENTED (2026-06-23).** 21 milestone/keystone nodes (3 per branch: 2 Majors + 1 Keystone) were ADDED to the tree (expansion, not conversion - all original nodes kept), tree is now 134 nodes / 133 unidirectional connections / 260 max-cost (~50% buyable by L120). Behaviors run through the new T1 engine `kubejs/server_scripts/ascendant_skill_effects.js` (config: `config/ascendant_skill_effects/effects.json`). T2 active abilities (Shadow Step, Draconic Roar, Ascendant Form, turrets, true Spell Echo) remain deferred per scope.
Author pass: 2026-06-23. Supersedes the "every node is a stat" model with a milestone/keystone layer.

This doc is the canonical spec for turning the Ascendant Web from a stat spreadsheet into a tree
with a soul. It captures Jayden's full design vision, tiers every proposed node by what the modpack
can actually do, gives concrete (tunable) mechanics, and sequences the build. Read this before
touching `generate-ascendant-skill-web.js` or writing any KubeJS effect.

Related docs: `SKILL_TREE_DESIGN.md` (current shape), `SKILL_TREE_BALANCE_NOTES.md` (pacing),
`SKILL_TREE_INTEGRATION_HOOKS.md` (hook intent), `ASCENDANT_PLAYER_PROGRESSION.md` (rank spine).

---

## 1. Design philosophy

The tree keeps small stat nodes as the **road** - the little taxes players pay to reach the fun
stuff - but every few levels the road hits a **landmark**. Node grammar, per Jayden's rule:

| Kind | Role | Frame / art | Typical cost | What it does |
| --- | --- | --- | --- | --- |
| Small | passive number | normal | 1 | flat attribute (the current nodes) |
| Medium | noticeable modifier | normal | 1-2 | bigger attribute / multi-stat |
| **Major** | new gameplay behavior | notable | 2 | a real mechanic unlock (trigger or active) |
| **Keystone** | branch-defining power | major | 3 | the identity payoff at the end of a lane |

Target cadence inside a lane: `Small -> Small -> Medium -> Small -> Major -> Small -> Medium -> Keystone`.
Players still spend points constantly, but they regularly hit something that feels like evolution
instead of "+2% movement speed (again)."

---

## 2. Feasibility tiers - what the engine can actually do

Puffish Skills can only hand out **passive rewards** (attribute modifiers, or fire a command on
unlock/lock). It cannot do on-hit logic, meters, "below X% HP," active abilities, or summons.
Everything beyond a flat stat has to be driven by a **KubeJS effects engine** that reads which nodes
a player has unlocked. Every proposed node is tagged with one of these tiers:

| Tier | Meaning | How it's built | Risk |
| --- | --- | --- | --- |
| **T0 Native** | flat passive stat | `puffish_skills:attribute` reward (current system) | none |
| **T1 Auto-trigger** | procs automatically on hit / kill / hurt / tick | command-tag reward + KubeJS event handler | low - proven patterns in pack |
| **T2 Active** | player presses a key / uses a trigger to fire it | KubeJS keybind or trigger-item + cooldown | medium - heavier, phase 2 |
| **T3 Mod-gated** | depends on Create / gate / guild internals | needs a capability check first | varies - verify before promising |

**~70% of Jayden's milestone list is T1** and lands in phase 1. The flashy actives (shouts, dashes,
breaths, turrets, transform) are T2. A handful (Create machine sensing, gate-room detection) are T3
and gated behind capability checks in Section 11.

Confirmed foundations (already true in this pack):
- Puffish `0.18.0` supports `puffish_skills:command` rewards with `unlock_command` / `lock_command`,
  executed at function permission level. (Verified against puffish.net docs.)
- KubeJS already runs `EntityEvents.hurt`, `EntityEvents.death`, `PlayerEvents.tick`,
  `ItemEvents.entityInteracted`, and `BlockEvents.rightClicked` successfully in this pack
  (`ascendant_hunter_progression.js`, `ascendant_core_integration.js`, `ascendant_regional_difficulty.js`).
- `ascendant_progression.js` already loads `net.puffish.skillsmod.api.SkillsAPI` and reads Iron's
  Spells `MagicData` mana - so mana-aware Arcanist nodes are feasible.
- `ascendant_progression.js` already mirrors level/XP/points to `ar_skill_*` scoreboards.

No new mods are required, which keeps us inside the `AGENTS.md` "do not add mods" rule.

---

## 3. Architecture

### 3.1 The command-tag bridge

Each behavior node carries a Puffish `command` reward that stamps a scoreboard **tag** on the player
when the node is unlocked and strips it when refunded:

```json
{
  "type": "puffish_skills:command",
  "data": {
    "unlock_command": "tag @s add ar_sk_warrior_blood_momentum",
    "lock_command":   "tag @s remove ar_sk_warrior_blood_momentum"
  }
}
```

Tag convention: `ar_sk_<branch>_<short_id>` (underscores only - tags must be whitespace-free).
A node may carry **both** an attribute reward (a small baked-in stat) and a command-tag reward, so a
Major can give a number *and* a mechanic.

### 3.2 The KubeJS effects engine

New file `kubejs/server_scripts/ascendant_skill_effects.js`, built in the same config-driven style as
`ascendant_effects.js`. All tunable numbers live in `config/ascendant_skill_effects/effects.json` so
balancing never requires a code edit. The engine binds:

- `EntityEvents.hurt` - attacker-side (on-hit procs: Guard Breaker, Backstab, Cleaving Force, Weak
  Point, Wardbreaker, Boss Hunter) and victim-side (Unshaken, Last Stand, Unkillable Guide).
- `EntityEvents.death` - on-kill procs (Blood Momentum, Cutpurse, Monster Harvest, Ancient Appetite,
  Forbidden Insight, Trophy Claim).
- `PlayerEvents.tick` - sustained / conditional states (Titanheart, Campfire Recovery, Deep Miner,
  Dragon Vein decay, aura nodes, cooldown + meter bookkeeping).
- `ItemEvents.entityInteracted` / `BlockEvents.rightClicked` - phase-1 "active-lite" triggers
  (Field Repair, Hunter's Mark, Field Medic) before true keybinds land in phase 2.

Guard pattern (every handler): `if (!player.tags.contains("ar_sk_<id>")) return;` then apply the
configured effect. Cheap, and absent tags cost nothing.

### 3.3 Meters, stacks, and cooldowns

Stacking mechanics and cooldowns use per-player **scoreboard objectives** (same approach as the
existing `ar_skill_*` objectives), decremented on `PlayerEvents.tick`:

- `ar_sk_guard_stacks` - Guard Breaker stagger meter (decays after 3s without a hit).
- `ar_sk_weakpoint_stacks` - Weak Point vulnerability stacks on the target (stored via Glowing + a
  short MobEffect, or an entity-side scoreboard).
- `ar_sk_draconic` - Dragonbound charge meter.
- `ar_sk_cd_<ability>` - active-ability cooldown timers.

### 3.4 Active-ability path (phase 2)

Two options, decided at phase-2 start (see Section 11, open question 6):
- **True keybind**: KubeJS client script registers a key, sends a packet to the server handler.
  Cleanest UX, more plumbing.
- **Trigger item / gesture**: a bound "focus" item or sneak+interact fires the ability. Faster to
  ship, no client packet code. Good for an early playable pass.

Where a mod already provides the fantasy, we lean on it instead of rebuilding: Combat Roll for
dodges, Iron's Spells for blink/aura, Iron's Spells summons for turret-like allies.

---

## 4. Generator schema changes

`generate-ascendant-skill-web.js` node tuples gain optional fields (back-compatible - existing nodes
are untouched):

- `kind`: `"small" | "medium" | "major" | "keystone"` (drives frame + default cost).
- `tags`: list of skill tags to emit as command rewards (adds the command reward automatically).
- `tier_override` / `cost_override`: when a soul node needs a specific depth or price.

`nodeDefinition()` learns to emit a `puffish_skills:command` reward when `tags` is present, alongside
any attribute rewards. Frames map `major -> goal (notable art)`, `keystone -> challenge (major art)`,
which the existing art pipeline already supports (48 frame PNGs cover all lanes x tiers x states).
The layout + art scripts need **no** changes - they place and skin whatever the generator emits.

---

## 5. Per-lane node catalogs

Each lane below lists its **soul nodes** (Majors + Keystone) with concrete, tunable starting values.
"Source" marks whether a node is NEW or a CONVERT of an existing stat node (so we control total tree
size). The existing small/medium stat nodes remain as the road between them. All values are phase-1
proposals and live in config.

Legend: tier in brackets; cost in points; gate = required spent points.

### 5.1 Warrior - melee dominance, boss pressure, armor break, survival

| Node | Kind [tier] | Trigger | Effect (proposed) | Cost | Gate | Source |
| --- | --- | --- | --- | --- | --- | --- |
| **Guard Breaker** | Major [T1] | on-hit same target | Repeated hits build Guard stacks; at 5, target staggers (Slow III 1s) and takes +15% melee for 4s | 2 | 14 | NEW |
| **Cleaving Force** | Major [T1] | on-hit, heavy weapon | Heavy hits deal 40% splash to enemies within 2.5b arc | 2 | 14 | convert `edge_pressure` |
| **Blood Momentum** | Major [T1] | on-kill | Kill grants Speed I + Strength I for 3s (refreshes on chain) | 2 | 14 | NEW (first-wave pick) |
| **Titanheart** | Keystone [T1] | tick, low-HP | Below 50% HP: scaling Resistance up to +25% DR and up to +20% melee; healing received -20% while active | 3 | 32 | convert `realm_champion` |

Other Warrior ideas folded into the road as Medium nodes: Executioner's Instinct (on-hit bonus vs
targets under 30% HP), Unshaken (post-big-hit knockback resist + DR), Armor Splitter (heavy hits shred
resistance), Last Stand (one-per-cooldown shield under low HP). **War Cry** (active party buff/shout)
is T2 - phase 2.

### 5.2 Rogue / Duelist - burst, stealth, mobility, weak points, loot

| Node | Kind [tier] | Trigger | Effect (proposed) | Cost | Gate | Source |
| --- | --- | --- | --- | --- | --- | --- |
| **Backstab** | Major [T1] | on-hit from behind | Behind-arc hits +35% damage and mark target (Glowing 4s) | 2 | 14 | NEW (replaces a stat slot) |
| **Weak Point** | Major [T1] | on-crit | Crits stack Vulnerability (+5% damage taken, max 4, 5s) | 2 | 14 | convert `knife_window` |
| **Shadow Step** | Major [T2] | active | Short dash toward target / away from danger, 12s CD. *Phase-1 proxy:* sneak-trigger blink + Invis 1s | 2 | 14 | NEW (first-wave pick) |
| **Assassin's Chain** | Keystone [T1/T2] | on-kill marked | Killing a marked enemy refunds dash CD and empowers next hit (+50% melee, 5s) | 3 | 32 | convert `night_market` |

Folded as Medium road nodes: Smoke Veil (on-kill brief reduced aggro), Silent Footing (sneak detection
range down), Cutpurse (humanoid/elite kills drop bonus coin/guild token - ties to economy cluster),
Deadly Opening (first hit on unaware enemy big crit), Phantom Recovery (clean dodge restores a little
stamina/mana).

### 5.3 Ranger / Hunter - tracking, precision, ranged control, hunting

| Node | Kind [tier] | Trigger | Effect (proposed) | Cost | Gate | Source |
| --- | --- | --- | --- | --- | --- | --- |
| **Hunter's Mark** | Major [T1->T2] | on ranged hit (phase-1) / active (phase-2) | Marks target: +20% ranged damage to it, Glowing-through-walls 8s | 2 | 14 | NEW (first-wave pick) |
| **Longshot** | Major [T1] | on projectile hit | Arrow damage scales with travel distance, up to +30% at 30+ blocks | 2 | 14 | convert `bow_tension` |
| **Apex Predator** | Keystone [T1] | on-hit marked, no-miss | Consecutive hits on the marked target without missing stack +6% damage (max 6); resets on a miss | 3 | 32 | convert `relic_tracker` |

Folded as Medium road nodes: Piercing Shot (charged shots pierce +1 - *verify projectile re-hit in
KubeJS*), Quick Draw (faster next charge after weapon swap), Beast Sense (crouch pulses nearby
elites/rares - pairs with the hunter board), Volley Technique (several hits add spectral arrows),
Snare Trap (placeable root - T2, phase 2).

### 5.4 Arcanist - mana control, spell combos, elemental, eldritch

| Node | Kind [tier] | Trigger | Effect (proposed) | Cost | Gate | Source |
| --- | --- | --- | --- | --- | --- | --- |
| **Spell Echo** | Major [T2*] | on spell cast | Every 4th Iron's spell, next spell repeats at 40% power | 2 | 14 | NEW (first-wave pick) |
| **Wardbreaker** | Major [T1] | on spell/magic hit | +20% magic damage vs high-armor / magic-resist targets | 2 | 14 | convert `spellguard` |
| **Forbidden Conduit** | Keystone [T2] | on-cast at low mana | Cast while near-empty mana by spending HP; those casts deal +20% and apply eldritch corruption | 3 | 32 | convert `archmage` or NEW |

Eldritch sub-path lives here (Jayden's eldritch upgrade icon): Eldritch Tolerance (stacking eldritch
resist that overloads the next spell). Folded as Medium road: Mana Overflow (full-mana excess regen ->
temp arcane shield), Arcane Rotation (different-school casts stack a bonus), Forbidden Insight (magic
kills -> temp mana regen + spell power). **Rift Blink** and **Rune Anchor** are T2 mobility - phase 2.
`*` Spell Echo + Forbidden Conduit need an Iron's Spells cast/mana-spend hook - see Section 11 q2
(mana **read** is already proven; cast-event + mana **write** need a check).

### 5.5 Engineer / Artificer - weaponized industry, gadgets, repair

| Node | Kind [tier] | Trigger | Effect (proposed) | Cost | Gate | Source |
| --- | --- | --- | --- | --- | --- | --- |
| **Field Repair** | Major [T1] | active-lite (right-click w/ ingot) | Consume iron/brass to repair held tool/armor a chunk, 30s CD | 2 | 14 | convert `field_repairs` |
| **Portable Gearbox** | Major [T2] | active | Deploy a temporary field-utility device (field crafting / emergency setup) | 2 | 14 | NEW (first-wave pick) |
| **Master Artificer** | Keystone [T2/T3] | active | Deploy a short-lived combat machine (brass turret / kinetic saw zone) that fights beside you | 3 | 32 | convert `master_artificer` |

Folded as Medium road: Salvage Protocol (breaking machines/mech mobs refunds parts), Overclock
(risk/reward speed burst), Brass Hands (placement/reach), Emergency Ejector (steam burst negates a
fall, on-tick). T3 (capability check, Section 11 q3): Mechanist's Eye, Kinetic Shielding, Contraption
Rider all read Create machine/contraption state.

### 5.6 Survivalist / Explorer - endurance, expedition, sustain

| Node | Kind [tier] | Trigger | Effect (proposed) | Cost | Gate | Source |
| --- | --- | --- | --- | --- | --- | --- |
| **Field Medic** | Major [T1] | on heal-item use | Healing yourself also heals an ally within 6b for 50% (co-op with Josh) | 2 | 14 | NEW (first-wave pick) |
| **Campfire Recovery** | Major [T1] | tick near fire | Near campfire/fire: Regeneration + temporary +2 max health | 2 | 14 | convert `safe_camp` |
| **Unkillable Guide** | Keystone [T1] | on lethal hit | Once / 90s, fatal damage leaves you at 1 HP + Resistance 5s - only if you hold food/water/survival item | 3 | 32 | convert `winter_blood` |

Folded as Medium road: Trailblazer (terrain-type movement bonus), Hardened Traveler (weather / hazard
resist), Forager's Instinct (natural-block bonus drops), Emergency Ration (auto-eat at starving),
Deep Miner (underground haste + hazard resist), Monster Harvest (mobs drop extra craft mats).

### 5.7 Dragonbound / Endgame - ancient power, late-game identity

| Node | Kind [tier] | Trigger | Effect (proposed) | Cost | Gate | Source |
| --- | --- | --- | --- | --- | --- | --- |
| **Dragon Vein** | Major [T1] | on deal/take damage | Builds a Draconic meter; at thresholds your next attack/spell gains bonus elemental damage | 2 | 14 | convert `boss_sense` |
| **Draconic Roar** | Major [T2] | active | Roar: nearby lesser enemies feared/weakened/staggered; bosses resist (small debuff only) | 3 | 32 | NEW (first-wave pick) |
| **Ascendant Form** | Keystone [T2] | active | Temporary draconic state: Resistance + elemental damage + mana regen + intimidation aura, long CD | 3 | 32 | convert `ascendant_dragon` |

Folded as Medium road: Scalehide (post-heavy-hit temp armor), Dragon's Pride (more damage vs higher-
rank enemies), Ancient Appetite (elite kills restore HP/mana/hunger), Hoard Sense (rare-loot reveal),
Wing Guard (block creates a frontal guard). **Wyrmstep** (aerial dash) and **Ancestral Breath** (cone)
are T2 - phase 2.

---

## 6. Cross-branch hybrid nodes

Hybrids reward two-branch investment and live in the gap between two lanes. **Gating method:** a hybrid
node connects to one deep node in each parent branch, so it only unlocks if you've reached both. This
depends on Puffish multi-parent semantics being "requires ALL parents" - flagged in Section 11 q1; if
it's "ANY," we gate via `required_spent_points` + a KubeJS tag check on both branches instead.

| Hybrid | Branches | Kind [tier] | Effect (proposed) |
| --- | --- | --- | --- |
| **Kinetic Brutality** | Warrior + Engineer | Major [T1/T3] | Melee near active machinery / after a device use deals bonus knockback + armor shred |
| **Voidstep Assassin** | Rogue + Arcanist | Major [T2] | After a magic blink/move, next melee is a guaranteed crit or applies eldritch damage |
| **Apex Tracker** | Ranger + Survivalist | Major [T1] | Marked enemies leave a trail; killing them yields extra food/materials/contract reward |
| **Expedition Rig** | Engineer + Survivalist | Major [T2] | Deploy a field station: compact camp + repair point + minor crafting |
| **Ancient Spellblood** | Arcanist + Dragonbound | Major [T1] | Spells gain bonus effects scaled by current Draconic charge |
| **Wyrm-Blooded Berserker** | Warrior + Dragonbound | Major [T1] | Taking heavy damage charges your next melee with draconic force |
| **Silent Hunter** | Rogue + Ranger | Major [T1] | Stealth hits mark enemies and raise loot/contract reward chance |

---

## 7. Shared clusters - Boss, Gate, and Guild

Three small node groups that sit near the center / between relevant lanes and tie the tree into the
pack's bigger systems.

### 7.1 Boss Trials (reads a curated boss entity-type list in config)

| Node | Kind [tier] | Effect |
| --- | --- | --- |
| Boss Hunter | Major [T1] | +damage to boss-tagged enemies after surviving near them 10s |
| Break the Giant | Major [T1] | Repeated hits on large/boss mobs build a stagger meter |
| Trophy Claim | Medium [T1] | First boss kill of each rank grants bonus XP / guild rep / rare currency |
| Desperation Art | Medium [T1] | Fighting a boss below 30% HP grants mana regen + Resistance |
| Slayer's Memory | Keystone [T1] | After first kill of a boss type, gain lasting minor resistance vs that type (progression-as-learning) |

### 7.2 Gatefarer (dungeon / ranked-gate integration - T3, capability check q4)

Gate Sense (detect nearby gates/rifts/boss rooms), Rift Stabilizer (reduce in-gate corruption/drain),
Room Clear Bonus (fast clears grant a between-room buff), Boss Door Resolve (entering a boss room
grants a shield/mana surge), **Rift Extraction** (finishing a gate yields branch-flavored bonus loot:
Warrior=trophies, Engineer=parts, Arcanist=essence, Survivalist=materials, Dragonbound=fragments).

### 7.3 Guild Charter (economy / guild integration - hooks existing `ascendant_guild_*` scripts, q5)

Contract Negotiator (better hunter-board rewards), Guild Authority (recruited NPCs work faster / better
services), Master's Commission (guild crafters' outputs gain minor bonuses), Reputation Surge (elite
contracts grant bonus rep), Specialist Recruitment (higher chance to find skilled NPC recruits -
directly supports the "physically recruit NPCs" goal).

---

## 8. Point economy impact

Current: 113 nodes, **211** points to max everything, **~129** available by level 120
(2 start + ~120 levels + 7 milestone bonuses). Players can afford ~60% of the tree - identity is
already forced, which is the goal.

This proposal **converts** many soul nodes from existing stat slots (net node count barely rises) and
**adds** the hybrid/boss/gate/guild clusters (~25 new nodes). To keep the "you must choose an identity"
tension intact:

- Keystones cost 3 and sit at the 32-point gate; **consider making the seven lane Keystones a Puffish
  `exclusive` group** so a player commits to one or two, not all seven. (Decision flagged - see q7.)
- Hybrids cost 3 (they're a reward for double investment).
- If total buyable ratio drops too far below ~55%, prefer lowering the XP curve slightly over adding
  more bonus points (consistent with `SKILL_TREE_BALANCE_NOTES.md`).

A full economy re-count happens automatically when the generator runs; the build task will report the
new max-cost and buyable ratio.

---

## 9. Balance guardrails

Carry over the watch-list from `SKILL_TREE_BALANCE_NOTES.md`, plus milestone-specific risks:

- Stagger / stacking-vulnerability (Guard Breaker, Weak Point, Break the Giant) can trivialize bosses
  if they stack with shred. Cap stacks and exclude or de-rate against boss-tagged mobs.
- On-kill chains (Blood Momentum, Assassin's Chain) can snowball in dense rooms - short durations, no
  hard stacking.
- Survival "cheat death" (Unkillable Guide, Last Stand) must respect a real cooldown and a resource
  cost, never become permanent immortality.
- Co-op heals (Field Medic) should not double-dip with Iron's Spells holy healing.
- Active abilities (phase 2) need cooldowns that read on the HUD so Josh always knows what a point did.

All numbers live in `config/ascendant_skill_effects/effects.json`; tune there, never in old worlds.

---

## 10. Build phases

| Phase | Scope | Deliverable | Gate to start |
| --- | --- | --- | --- |
| **0** | this doc | feasibility + spec locked | **<- you are here; needs greenlight** |
| **1** | engine + all T1 soul nodes (most Majors, Titanheart/Apex/Unkillable/Slayer's Memory, T1 hybrids, Boss Trials) | working `ascendant_skill_effects.js` + regenerated tree + config + test plan | phase 0 approved |
| **2** | T2 actives (Shadow Step, Draconic Roar, Ascendant Form, Portable Gearbox, Master Artificer, Spell Echo, blinks) | keybind/trigger path + active abilities + cooldown HUD | phase 1 tested in-game |
| **3** | T3 mod-gated (Create-state nodes, Gatefarer, Guild Charter) | after capability checks in Section 11 pass | phases 1-2 stable |

Phase 1 is the big, safe, high-impact wave: it gives every branch a soul without the hard plumbing.

---

## 11. Open questions / capability checks before building

1. **Puffish multi-parent prerequisites** - does a node with two incoming connections require ALL
   parents or ANY? Determines how hybrids gate. (Fallback: KubeJS tag check on both branches.)
2. **Iron's Spells hooks** - is there a clean cast event and a mana-spend write? (Mana *read* is
   already done in `ascendant_progression.js`.) Affects Spell Echo, Forbidden Conduit.
3. **Create machine/contraption detection** - can KubeJS cheaply read nearby active kinetic blocks /
   whether the player rides a contraption? Affects Mechanist's Eye, Kinetic Shielding, Contraption
   Rider, Kinetic Brutality.
4. **Dungeon/gate events** - does the ranked-gate system expose room-enter / room-clear / gate-finish
   hooks? Affects the whole Gatefarer cluster.
5. **Guild API** - what do `ascendant_guild_jobs.js` / `ascendant_guild_director.js` expose for reward
   multipliers and recruitment odds? Affects Guild Charter.
6. **Active-ability input** - custom KubeJS keybind+packet, or a trigger-item/gesture for phase 2?
7. **Keystone exclusivity** - make the seven lane Keystones mutually exclusive (one identity) or let a
   maxed player eventually own several?
8. **`EntityEvents.hurt` damage edit** - confirm this KubeJS build lets us scale/cancel damage in that
   event (the pack already uses it in `ascendant_hunter_progression.js`, so likely yes - verify the
   exact field).

---

## 12. What is NOT changing

- The radial 7-lane layout, the art pipeline, and the XP curve stay as-is.
- The HUD bridge (`ascendant_progression.js`) and managed bonus points stay as-is (phase 2 may add a
  cooldown readout).
- The three synced skill roots (config / datapack / openloader) and the generator-is-source-of-truth
  rule stay as-is - all node changes go through `generate-ascendant-skill-web.js`, never hand-edited
  JSON.
