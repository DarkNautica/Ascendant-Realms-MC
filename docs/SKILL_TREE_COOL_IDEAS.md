# Ascendant Web - Cool Node Ideas (menu)

Status: **proposal menu, 2026-06-23.** Sourced from a full mod/system scan. Pick a batch and I build it
through the same generator + `ascendant_skill_effects.js` engine (no new mods; existing T1 patterns).

The idea: most of the 113 base nodes are pure "+X%". We keep the number but bolt a **trick** onto the
dullest ones (a "mixed" node), so the road itself gets interesting - not just the landmarks.

Feasibility: **T1** = doable now (proven on-hit/kill/tick patterns). **T2/T3** = bigger lifts (active
input, or a mod hook that needs a capability check). Confidence noted where an API needs verifying.

---

## A. Mixed-node upgrades (keep the stat, add a behavior) - all T1

### Warrior
- **Shield Craft -> Shield Bash**: while blocking, melee attackers are knocked back + briefly slowed. *(Spartan Shields; verify isBlocking API)*
- **Heavy Draw -> Cleave**: axe / heavy hits deal ~25% splash to enemies beside the target. *(Better Combat / Simply Swords)*
- **Giantslayer -> Giant Slayer**: bonus melee damage that scales with the target's max HP (shreds big mobs + bosses). *(Cataclysm / Mowzie)*

### Rogue
- **Knife Window -> Bleed**: hits stack a bleed that ticks damage over a few seconds. *(duelist fantasy)*
- **Silent Looter -> Pickpocket**: humanoid/illager kills have a chance to drop extra coin/loot. *(loot economy)*
- **Soft Landing -> Death From Above**: landing after a fall deals an AoE thud scaled by fall height (no self-damage). *(Combat Roll cliffs)*

### Ranger
- **Beast Breaker -> Pinning Shot**: fully charged arrows briefly root/slow what they hit. *(kiting Alex's Mobs / fliers)*
- **Pack Bond -> Shared Vigor**: your tamed pets gain Regeneration whenever you do / while near you. *(companions)*
- **Trophy Marks -> Trophy Hunter**: killing rare/elite/boss mobs drops bonus loot + skill XP. *(BossesRise / Mowzie trophies)*

### Arcanist
- **Spellblade Entry -> Spellstrike**: melee hits have a chance to proc a free Iron's spell. *(reuses the hunter AI's onCast proc - proven in-pack)*
- **Holy Channel -> Smite**: +damage vs undead, and undead kills heal you. *(Born in Chaos / undead)*
- **Frost Formula -> Frostbite**: your hits briefly slow + frost the target. *(Snow Real Magic)*

### Engineer
- **Provisioner -> Field Rations**: eating grants a short Haste + Speed burst. *(Farmer's Delight)*
- **Shipwright -> Sea Legs**: while on a boat/ship/mount you're fall-immune and faster. *(Small Ships)*
- **Ruin Reclaimer -> Prospector**: mining ore has a chance to drop bonus raw ore. *(Create resource loops)*

### Survivalist
- **Weather Sense -> Storm Strider**: during rain/thunder you gain speed and ignore weather slowdown. *(Weather, Storms & Tornadoes)*
- **Deep Delver -> Cave Sight**: underground / in low light you gain Night Vision. *(YUNG dungeons)*
- **Cold Resolve -> Frostwalker**: in snowy biomes you're freeze-immune + gain brief Resistance. *(Serene Seasons / Snow Real Magic)*

### Dragonbound
- **Dragon Hunter -> Dragonslayer**: bonus damage vs dragons and large flying mobs. *(Ice and Fire)*
- **Scale Tempering -> Scaleguard**: taking a heavy hit briefly grants fire + ice immunity (scales harden). *(elemental dragons)*
- **Mounted Legend -> Bonded Mount**: your mount takes ~30% less damage and shares your Resistance. *(dragon/ship riding)*

---

## B. Standout brand-new behavior nodes - T1

- **Lifesteal** (Warrior/Dragonbound): melee kills heal a chunk of HP. Predatory, satisfying.
- **Executioner's Instinct** (Warrior/Rogue): enemies below 30% HP take big bonus damage (clean finisher).
- **Chain Lightning** (Arcanist): a chance on hit to arc a small bolt to a nearby enemy. *(storm fantasy)*
- **Thornmail** (Warrior/Engineer): a portion of melee damage taken is reflected as a steam/spike burst.
- **Adrenaline Surge** (Rogue): dropping below 40% HP gives one burst of Speed + Haste on a cooldown.

---

## C. Bigger lifts (cool but heavier) - T2 / T3, flagged for later

- **Blood Moon Reaver** (Enhanced Celestials): during a blood moon, big damage + lifesteal. *(T2: read the celestial event)*
- **Bounty Hunter** (Bountiful): +damage and +reward vs your active bounty targets. *(T3: Bountiful hook + the skill_hook_registry mob map)*
- **Soul Reaper** (Marium's Soulslike): kills bank souls / heal from souls. *(T3: souls API)*
- **Season's Boon** (Serene Seasons): summer = offense, winter = defense, etc. *(T2: season read)*
- **Companion Captain** (Human Companions): your hired companions get your buffs + fight harder. *(T3: companion detection)*
- The deferred **active abilities** (Draconic Roar, Ascendant Form, Shadow Step dash, deployable turret) - true keybind/cooldown layer.

---

## Notes
- Mixed upgrades modify existing nodes in `generate-ascendant-skill-web.js` (add a tag + behavior; keep the stat). Tree size doesn't grow.
- New nodes (Section B) are added like the milestone pass; tree grows a little.
- Everything in A + B fits the existing engine; I'd verify the 3 "verify API" items (isBlocking, pet/mount buffing, player-side onCast) in-game on first build.
