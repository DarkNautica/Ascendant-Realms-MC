#!/usr/bin/env python3
"""Full Ascendant Codex content (Patchouli external-folder book, namespace `patchouli`).
Writes categories + entries to the external patchouli_books folder in BOTH the repo and the
active instance. Uses spotlight(item)/entity(mob)/image pages with verified IDs for visuals.
Run:  python scripts/generate-ascendant-codex-content.py
"""
import json, os, shutil

ROOTS = [
  "patchouli_books/ascendant_codex/en_us",  # repo (relative to cwd)
  "/sessions/loving-amazing-gates/mnt/Ascendant Realms (2)/patchouli_books/ascendant_codex/en_us",  # instance
]

# (id, name, description, icon, sortnum)
CATS = [
  ("getting_started","Getting Started","Where to begin, the controls, and surviving your first days.","minecraft:compass",-100),
  ("hunters_path","The Hunter's Path","How you grow: the core loop, Guild ranks, and where to go next.","minecraft:nether_star",-90),
  ("guild","The Guild & Bounties","Hunter Boards, contracts, and the quest log that guides you.","minecraft:bell",-80),
  ("combat","Combat","Blades, dodging, shields, runes, and ranged fighting.","minecraft:iron_sword",-70),
  ("magic","Magic & Mana","Spellbooks, casting, schools of magic, and growing your power.","irons_spellbooks:gold_spell_book",-60),
  ("ascendant_web","The Ascendant Web","Your skill tree: points, the seven lanes, and planning.","minecraft:experience_bottle",-50),
  ("gear","Gear, Loot & Rarity","Rarity tiers, reading loot, and carrying it all.","minecraft:diamond_chestplate",-40),
  ("world","The World","Regions, settlements, maps, seasons, and ruins.","minecraft:grass_block",-30),
  ("gates","Gates & Rifts","Solo-Leveling-style breaches into ranked danger.","minecraft:end_portal_frame",-20),
  ("threats","Threats & Bosses","What hunts you, the dragons, and the great beasts.","minecraft:wither_skeleton_skull",-10),
  ("survival","Survival & Comforts","Food, building, and the tools that make life easier.","minecraft:cooked_beef",0),
]

ENTRIES = []

def T(title, text): return {"type":"patchouli:text","title":title,"text":text}
def TX(text): return {"type":"patchouli:text","text":text}
def SPOT(item, title, text): return {"type":"patchouli:spotlight","item":item,"title":title,"text":text}
def ENT(entity, name, text): return {"type":"patchouli:entity","entity":entity,"name":name,"text":text}
def IMG(img, title, text): return {"type":"patchouli:image","images":[img],"title":title,"border":False,"text":text}
def QUOTE(title, text): return {"type":"patchouli:text","text":('$(o)"'+text+'"$()$(br2)$(gold)'+title+'$()') if title else ('$(o)"'+text+'"$()')}
def E(cat, name, icon, sortnum, pages): ENTRIES.append({"category":"patchouli:"+cat,"name":name,"icon":icon,"sortnum":sortnum,"pages":pages})

# ===================== 1. GETTING STARTED =====================
E("getting_started","Welcome, Hunter","minecraft:ender_eye",0,[
  IMG("ascendant_realms:textures/gui/codex/banner_getting_started.png","Ascendant Codex","$(soft)First Edition$()"),
  T("Welcome, Hunter","The realm of $(rune)Ascendant$() is no quiet frontier. Villages need protectors, the Guild keeps the ledger of who is worth their salt, and the roads between are thick with $(em)contracts, rivals, and worse$().$(br2)You begin as $(soft)nobody$() — $(gold)Unranked$(). What you become is written by what you survive."),
  T("How to Use This Book","Each chapter is a system you will actually use. Start with $(rune)Getting Started$(), then $(rune)The Hunter's Path$().$(br2)$(soft)Some mods carry their own deeper guides — Iron's Guidebook for magic, Simply Swords' Runic Grimoire for weapons, the Bestiary for dragons. This Codex tells you how it all fits together.$()"),
  QUOTE("- The Guild","Your name matters when people know what you survived."),
])
E("getting_started","Your First Day","minecraft:campfire",1,[
  T("Your First Day","Spawn, then $(rune)move with purpose$(). Daylight is short and the first night decides a lot.$(br2)$(gold)1.$() Punch wood, make tools, grab food.$(br)$(gold)2.$() Find a $(rune)village$() — beds, safety, a $(gold)Hunter Board$().$(br)$(gold)3.$() Take a $(em)low-rank bounty$() you can survive.$(br)$(gold)4.$() Clear it, return alive, and grow."),
  ENT("minecraft:zombie","Night Brings Teeth","When the sun drops, the dark fills with things that were once people — and shadows that never were. This realm spawns enemies $(warn)thicker than vanilla$(), even by day in dark places. Carry $(gold)light$() and keep your back to a wall."),
  SPOT("minecraft:torch","Light Pushes Back","A torch is the cheapest life-insurance in the realm. Mark your path, ring your camp, and never dig straight down toward a sound."),
  T("Don't Overreach","Mobs scale and regions get deadlier the farther out you roam. Build a small base near a village, bank a bed, and grow your gear before chasing distant danger. $(soft)The world rewards patience, then boldness.$()"),
])
E("getting_started","Controls & Keybinds","minecraft:oak_sign",2,[
  T("Core Controls","Your RPG surfaces live on simple keys:$(br2)$(gold)K$() — Ascendant Web (skills)$(br)$(gold)L$() — Quest Log$(br)$(gold)R$() — Spell wheel$(br)$(gold)V$() — Cast spell$(br)$(gold)Left Alt$() — Spell-bar modifier$(br)$(gold)Z$() — Combat roll (dodge)"),
  T("More Keys","$(gold)B$() — Backpack$(br)$(gold)G$() — Curios (trinket slots)$(br)$(gold)U$() — Waypoints (Xaero)$(br)$(gold)Y$() — Minimap settings$(br2)$(rune)Recipe lookup (JEI):$()$(br)$(gold)Ctrl+R$() — how to craft the hovered item$(br)$(gold)Ctrl+U$() — what the hovered item is used for$(br2)$(soft)Movement, inventory, and attack stay on their vanilla keys.$()"),
])
E("getting_started","Reading Your HUD","minecraft:clock",3,[
  T("Your HUD","Around your hotbar you'll see the signs of a hunter:$(br2)$(rune)Health & armor$() — vanilla rows; health can scale as you progress.$(br)$(rune)Hunger$() — keep it high; it fuels healing and rolling.$(br)$(gold)Blue XP bar$() — your $(rune)Ascendant level$(); each level grants a $(gold)skill point$()."),
  T("Level, Mana & More","A $(gold)level badge$() sits at the left of the XP bar.$(br)The $(rune)blue mana bar$() shows your spell fuel (see Magic & Mana).$(br2)$(soft)Mob health bars, loot beams, and biome/region titles also appear as you play — they are reading aids, not clutter.$()"),
])

# ===================== 2. THE HUNTER'S PATH =====================
E("hunters_path","The Core Loop","minecraft:compass",0,[
  T("The Core Loop","Everything in Ascendant orbits four verbs:$(br2)$(rune)Explore$() — find settlements, ruins, and danger.$(br)$(rune)Hunt$() — take bounties and clear threats.$(br)$(rune)Grow$() — every level is a skill point; better gear and spells follow.$(br)$(rune)Rank up$() — prove yourself and rise in the Guild."),
  T("Two Kinds of Power","Keep these straight:$(br2)$(gold)Skill points$() (the Ascendant Web) are your $(em)personal power$() — they make you stronger.$(br2)$(gold)Guild rank$() is your $(em)public status$() — proof of what you've achieved. One does not buy the other; you earn both by playing."),
])
E("hunters_path","Guild Ranks: E to S","minecraft:golden_helmet",1,[
  T("The Rank Ladder","The Guild sorts hunters by proven record:$(br2)$(soft)Unranked$() — barely registered (lvl 1-9)$(br)$(gold)E$() — unknown survivor (10-19)$(br)$(gold)D$() — field adventurer (20-34)$(br)$(gold)C$() — licensed monster hunter (35-49)"),
  T("The High Ranks","$(gold)B$() — elite dungeon clearer (50-69)$(br)$(gold)A$() — realm-class fighter (70-89)$(br)$(gold)S$() — ascendant-class myth (90-120)$(br2)$(soft)Level bands are a guide, not a gate. Rank reflects deeds — bounties, bosses, and structures cleared — not just your number.$()"),
])
E("hunters_path","Earning Your Rank","minecraft:writable_book",2,[
  T("How You Rise","The Guild judges your record, not a checklist. What counts:$(br2)$(li)Bounties completed$(li)Bosses and dangerous mobs slain$(li)Structures and dungeons cleared$(li)Dimensions discovered$(li)Villages defended$(li)Rare gear and magic milestones"),
  T("Reputation","Hunting recognized threats and finishing contracts builds standing with the Guild. Track your goals in the $(gold)Quest Log$() ($(gold)L$()). $(soft)Rank is the realm noticing you — chase deeds, and the title follows.$()"),
])
E("hunters_path","Where to Go Next","minecraft:filled_map",3,[
  T("Early Game","Settle near a village. Clear small ruins, take village bounties, mine for your first real gear, and open your first $(rune)spell school$(). Spend early skill points where you fight most."),
  T("Mid & Late","Push into tougher regions for $(gold)epic$() and $(gold)legendary$() loot, hunt mini-bosses, and chase $(rune)dragons$() and $(rune)Gates$(). The far Nether Front and End Expanse are S-rank country — go there $(warn)prepared, not curious$()."),
])

# ===================== 3. GUILD & BOUNTIES =====================
E("guild","The Guild","minecraft:bell",0,[
  T("The Guild","The Guild is the realm's backbone — it organizes hunters, posts work, and grants the ranks that say who you are. You'll find its halls and boards in towns and larger settlements.$(br2)$(soft)This is not a town-building pack. You are a hunter, not a mayor — the Guild points you at danger and rewards you for meeting it.$()"),
])
E("guild","Hunter Boards","bountiful:bountyboard",1,[
  SPOT("bountiful:bountyboard","The Bounty Board","Found in villages and Guild stations. Right-click to see posted $(rune)bounties$() — the realm's contracts. Take one you can handle."),
  T("Working a Board","Each bounty asks for items, kills, or deeds and pays out in rewards and standing. Boards refresh over time, so check back often.$(br2)$(gold)Tip:$() match bounties to your strength. A village pest-control job is a fine E-rank start; a dungeon contract is not."),
])
E("guild","Contracts & Rewards","minecraft:paper",2,[
  T("Kinds of Work","As you rise, the work changes:$(br2)$(li)$(soft)Local errands & village requests$() (Unranked-E)$(li)$(soft)Road patrols & small ruins$() (D)$(li)$(soft)Dungeon contracts & rival sightings$() (C)$(li)$(soft)Miniboss & arcane recovery$() (B)$(li)$(warn)Realm threats, dragon & boss hunts$() (A-S)"),
  T("Rewards","Contracts pay in loot, currency, and reputation toward your next rank. Higher-tier work risks more and pays more. $(soft)Don't grind one board — spread your deeds across the realm and the Guild notices faster.$()"),
])
E("guild","The Quest Log","minecraft:book",3,[
  T("Your Quest Log","Press $(gold)L$() to open the $(rune)Quest Log$(). It tracks milestones and points you toward what to do next — your guide to the realm's systems and your rise through the Guild.$(br2)$(soft)When you're unsure what to do, open the log. It turns a big world into a clear next step.$()"),
])

# ===================== 4. COMBAT =====================
E("combat","The Art of the Blade","minecraft:iron_sword",0,[
  SPOT("minecraft:iron_sword","Better Combat","Fighting here is physical. Each weapon type has its own $(rune)moveset$() and reach — swords sweep, spears poke, hammers crash. Hold attack to chain combos."),
  T("Fight Smart","Different weapons suit different foes and ranges. Time your swings, use reach, and don't just spam-click — $(rune)combos$() and positioning beat button-mashing.$(br2)$(soft)Dual-wielding and heavy weapons each change your rhythm. Try a few and keep what fits your style.$()"),
])
E("combat","Dodge & Defend","minecraft:shield",1,[
  T("The Combat Roll","Press $(gold)Z$() to $(rune)roll$() — a quick dodge with brief invulnerability. It is your best answer to a dragon's bite or a boss wind-up.$(br2)$(soft)Rolling costs stamina/hunger, so keep fed. A well-timed roll beats armor against the biggest hits.$()"),
  SPOT("minecraft:shield","Shields & Parry","A shield blocks and can $(rune)parry$() if timed well, opening foes to a counter. Enhanced shields add real defensive options against heavy attackers."),
])
E("combat","Weapons & Runes","simplyswords:soulkeeper",2,[
  SPOT("simplyswords:soulkeeper","Unique Weapons","Simply Swords adds $(rune)unique weapons$() with special effects — like the Soulkeeper. They drop, craft, or are earned, and reward a focused build."),
  SPOT("simplyswords:runefused_gem","Gems & Runes","$(rune)Gems$() socket into unique weapons; $(rune)runes$() can be etched for extra power. Mix and match to tune a weapon to your fight."),
  T("Go Deeper","For full crafting, gem socketing, and rune etching, open Simply Swords' own guide — the $(rune)Runic Grimoire$(). $(soft)It is the companion volume to this chapter.$()"),
])
E("combat","Bows & Ranged","minecraft:bow",3,[
  SPOT("minecraft:bow","Ranged Fighting","Some foes are best met from range — flying dragons, chargers, and casters. Keep a $(rune)bow$() or crossbow and a stack of arrows for the fights you shouldn't take face-first."),
  T("Pick Your Range","Ranged damage is boosted by the realm's attribute systems, so a hunter who invests in it stays deadly at distance. $(soft)Carry both: a blade for the close work, a bow for the rest.$()"),
])

# ===================== 5. MAGIC & MANA =====================
E("magic","The Arcane","irons_spellbooks:gold_spell_book",0,[
  SPOT("irons_spellbooks:gold_spell_book","Spellbooks","Magic runs through $(rune)Iron's Spells$(). A $(rune)spell book$() holds your known spells; better books hold more and stronger ones."),
  T("Mana","Casting spends $(rune)mana$() — the blue bar on your HUD. It refills over time, and gear and attributes raise your maximum and recovery.$(br2)$(soft)Mana is your spell stamina: spend it, let it breathe, spend again.$()"),
])
E("magic","Casting Spells","minecraft:blaze_rod",1,[
  T("How to Cast","$(gold)1.$() Hold a spell book.$(br)$(gold)2.$() Press $(gold)R$() to open the $(rune)spell wheel$() and pick a spell.$(br)$(gold)3.$() Press $(gold)V$() to $(rune)cast$() the selected spell.$(br)$(gold)4.$() Hold $(gold)Left Alt$() (spell-bar modifier) to swap quickly mid-fight."),
  T("Spend Wisely","Each spell has a mana cost and cooldown. Stronger spells cost more — open with control, finish with your heavy hitter. $(soft)A dead caster is one who emptied the bar at the wrong time.$()"),
])
E("magic","Schools of Magic","minecraft:amethyst_shard",2,[
  T("The Schools","Spells come in schools, each with a feel: $(em)Fire, Ice, Lightning, Holy, Ender, Blood, Evocation, Nature,$() and $(em)Eldritch$(). Build around one or two rather than dabbling in all."),
  T("Where They Lean","The realm hides magic by theme:$(br2)$(li)$(rune)Frost/Ice$() — the cold Frostmarch$(li)$(rune)Fire/Sun$() — arid Sunreach & the Nether$(li)$(rune)Nature/Water/Storm$() — the Verdant Coast$(li)$(rune)Earth/Force/Evocation$() — Stoneback highlands$(li)$(warn)Dark/Void/Eldritch/Blood$() — outer, corrupted, End"),
])
E("magic","Growing Your Power","irons_spellbooks:netherite_spell_book",3,[
  SPOT("irons_spellbooks:netherite_spell_book","Better Books","Higher-grade spell books (up to the $(rune)Ancient Codex$()) hold more spell slots and rarer spells. Upgrade as you find or craft them."),
  T("Scrolls, Upgrades & More","Find spells as scrolls and loot in dangerous structures; upgrade your casting with the mod's own systems. For the full magic deep-dive — schools, upgrades, and every spell — open $(rune)Iron's Guidebook$(). $(soft)This chapter is the map; that book is the territory.$()"),
])

# ===================== 6. THE ASCENDANT WEB =====================
E("ascendant_web","Your Skill Tree","minecraft:experience_bottle",0,[
  T("The Ascendant Web","Press $(gold)K$() to open the $(rune)Ascendant Web$() — your personal skill tree, themed as a glowing arcane void.$(br2)Every Ascendant $(gold)level$() grants one $(gold)skill point$(). Spend points to unlock nodes along seven lanes and shape how you fight."),
  T("Unlock Order","Nodes connect in chains — you must unlock what comes before to reach what comes after. Glowing lane-colored lines show paths you've opened; follow a lane outward toward its capstone."),
])
E("ascendant_web","The Seven Lanes","minecraft:amethyst_cluster",1,[
  T("Choose Your Path","Seven lanes, each a fantasy:$(br2)$(li)$(#FF6B6B)Warrior$() — frontline might$(li)$(#C792EA)Rogue / Duelist$() — speed & crits$(li)$(#9EE493)Ranger / Hunter$() — ranged & mobility$(li)$(#7CB7FF)Arcanist$() — magic & mana"),
  T("...and three more","$(li)$(#FFD98A)Engineer / Artificer$() — tools & utility$(li)$(#5FE3D0)Survivalist / Explorer$() — toughness & travel$(li)$(#FF9E5A)Dragonbound / Endgame$() — late-game mastery$(br2)$(soft)Most hunters spend deep in one or two lanes and dip into others for key perks.$()"),
])
E("ascendant_web","Spending Wisely","minecraft:lapis_lazuli",2,[
  T("Plan Your Build","You earn one point per level, plus $(gold)bonus points$() at milestone levels ($(gold)10, 20, 35, 50, 70, 90, 110$()). Points are precious early — put them where you actually play."),
  T("Don't Spread Thin","A focused build beats a shallow one. Rush the perks that fix your weakness — survivability if you keep dying, damage if fights drag. $(soft)You can always branch later; you can't get early levels back.$()"),
])

# ===================== 7. GEAR, LOOT & RARITY =====================
E("gear","Rarity Tiers","minecraft:diamond",0,[
  T("Reading Rarity","Every piece of gear has a rarity, shown by its color:$(br2)$(li)$(#9CA3AF)Common$()$(li)$(#55FF55)Uncommon$()$(li)$(#55AAFF)Rare$()$(li)$(#D966FF)Epic$()"),
  T("The High Tiers","$(li)$(#FFE66D)Legendary$()$(li)$(#FF3B00)Mythic$()$(li)$(#E6FBFF)Ascendant$()$(br2)Higher rarity means stronger stats and rarer sources. $(soft)Ascendant gear is the stuff of myth — earned at the edges of the world.$()"),
])
E("gear","Reading Loot","minecraft:gold_ingot",1,[
  T("Loot at a Glance","The realm makes good loot easy to spot:$(br2)$(li)$(rune)Item borders$() tint a slot by rarity.$(li)$(rune)Loot beams$() shine over dropped gear in its rarity color.$(li)$(rune)Tooltips$() add a clear rarity line and source.$(br2)$(soft)Bright beam, bright border — worth the detour.$()"),
  T("Where Gear Comes From","Rarity lines up with danger: villages and small ruins give common-to-rare; real dungeons, bosses, and far regions give epic and beyond. $(soft)If you want better loot, go somewhere scarier.$()"),
])
E("gear","Carrying It All","sophisticatedbackpacks:backpack",2,[
  SPOT("sophisticatedbackpacks:backpack","Backpacks","Press $(gold)B$() to open your equipped $(rune)backpack$(). They upgrade with more storage, auto-pickup, and filters — a hunter's best friend on long expeditions."),
  SPOT("artifacts:cloud_in_a_bottle","Curios & Artifacts","Press $(gold)G$() to open your $(rune)Curios$() slots — rings, belts, charms, and $(rune)artifacts$() like the Cloud in a Bottle. Passive power you wear, not wield."),
])

# ===================== 8. THE WORLD =====================
E("world","Regions of the Realm","minecraft:filled_map",0,[
  T("A Realm of Regions","The world rises in danger as you travel:$(br2)$(li)$(#9EE493)The Crownlands$() — safe starting heart$(li)$(#7CB7FF)Verdant Coast$() — wet, wild east$(li)$(#FFD98A)Sunreach$() — arid south$(li)$(#BFefff)Frostmarch$() — frozen north$(li)$(#C9B6FF)Stoneback Highlands$() — rugged peaks"),
  T("The Deep & Beyond","$(li)$(warn)Deep Wilds$() — true wilderness$(li)$(#FF7A6E)Dragon Scars$() — dragon country$(li)$(#FF9E5A)Nether Front$() & $(#E6FBFF)End Expanse$() — endgame$(br2)$(soft)Each region favors certain magic, mobs, and loot. Match your rank to the threat before you settle in.$()"),
])
E("world","Settlements & Villages","minecraft:bell",1,[
  ENT("minecraft:villager","Living Settlements","Villages are real hubs — homes, trades, beds, and $(gold)Hunter Boards$(). Their people remember you, and some can be befriended or recruited. Protect them; the realm is harsher than vanilla."),
  T("Guards & Defense","Settlements have $(rune)guards$(), but danger mobs hit hard. Helping defend a village is honest early work — and good standing with the Guild."),
])
E("world","Maps & Waypoints","minecraft:compass",2,[
  T("Never Get Lost","A $(rune)minimap$() sits on your screen. Press $(gold)U$() to manage $(rune)waypoints$() — mark your base, a village, or a dungeon. Press $(gold)Y$() for minimap settings.$(br2)$(soft)Your most recent death leaves a marker so you can recover your gear; old ones are hidden to reduce clutter.$()"),
])
E("world","Seasons & Weather","minecraft:snowball",3,[
  T("A Living Sky","The realm runs $(rune)seasons$() — temperature and growth shift across spring, summer, autumn, and winter, so plan crops and travel.$(br2)$(warn)Storms$() can turn violent. Take cover from the worst weather, and respect the cold of the far north."),
])
E("world","Ruins & Dungeons","minecraft:mossy_cobblestone",4,[
  T("Places Worth Clearing","The land is dense with $(rune)structures$() — overhauled dungeons, mineshafts, strongholds, towers, sunken ruins, and whole built towns. Each hides loot scaled to its danger.$(br2)$(soft)Bring light, food, and an escape plan. The best rewards sit behind the worst rooms.$()"),
])

# ===================== 9. GATES & RIFTS =====================
E("gates","What Is a Gate?","minecraft:ender_eye",0,[
  IMG("ascendant_realms:textures/gui/codex/banner_gate.png","Gates","$(soft)Breaches into ranked danger.$()"),
  T("What Is a Gate?","A $(rune)Gate$() is a swirling rift torn into the world — a breach into a sealed, ranked pocket of danger and reward, in the spirit of Solo Leveling.$(br2)Its $(rune)color$() warns of its threat: $(#7CF2FF)blue$() and $(#7CFF9E)green$() for the careful, $(#FFD98A)gold$() for the bold, $(#C79BFF)violet$() and $(#FF7A6E)red$() for the truly dangerous."),
  T("A Note","The Guild is still charting the realm's Gates, so they are opening in stages. When you meet one, treat its color as gospel — a red Gate will not forgive an unready hunter."),
])
E("gates","Surviving a Gate","minecraft:ender_pearl",1,[
  T("Before You Enter","$(li)Match the Gate's $(rune)color$() to your rank and gear.$(li)Carry food, light, healing, and an escape.$(li)Know the way back — every Gate has a $(rune)return$().$(br2)$(warn)Do not step through unprepared.$() What waits inside is tuned to be harder than the open world."),
  T("The Reward","Clear a Gate's depths — and its $(rune)boss$() — for loot above what the surface gives. The deeper the rank, the richer the prize. $(soft)Gates are where hunters become legends, or cautionary tales.$()"),
])

# ===================== 10. THREATS & BOSSES =====================
E("threats","Know Your Enemy","minecraft:rotten_flesh",0,[
  ENT("minecraft:zombie","A Harsher Night","Ordinary monsters spawn $(warn)thicker$() here, and can appear by day in caves and dark places. Numbers alone can overwhelm a careless hunter."),
  T("They Grow Stronger","Enemies $(rune)scale$() as the world and you progress — distant regions and deeper nights bring tougher versions. Upgrade gear and skills before pushing into new territory, and read $(rune)mob health bars$() to judge a fight."),
])
E("threats","Dragons & Great Beasts","minecraft:dragon_head",1,[
  ENT("iceandfire:fire_dragon","Dragons","$(warn)Dragons$() rule the skies and roosts of the realm — Fire, Ice, and Lightning. A grown dragon is a raid-class threat: fireproofing, cover, ranged attacks, and dodging ($(gold)Z$()) are survival, not luxury."),
  ENT("iceandfire:ice_dragon","Hoards & Horror","Dragons guard vast hoards — the realm's richest loot. Beyond dragons lurk other great beasts and deep-sea horrors.$(br2)$(soft)For lore and weaknesses of every creature, consult the Bestiary guide.$()"),
])
E("threats","Elite Bosses","minecraft:netherite_sword",2,[
  ENT("mowziesmobs:ferrous_wroughtnaut","Champions","Unique $(rune)bosses$() guard special arenas and structures — armored champions, primal terrors, and worse. Each has a pattern; learn it, dodge the wind-ups, and punish the openings."),
  ENT("cataclysm:netherite_monstrosity","Cataclysm-Tier","The deadliest foes are realm-shaking $(warn)Cataclysm bosses$(). Come with top gear, healing, and a plan — and never alone if you can help it. Their drops are among the best in the world."),
])
E("threats","The Shadow Army","minecraft:wither_skeleton_skull",3,[
  T("Shadows of the Fallen","Some enemies arise as $(rune)shadows$() — dark, blue-eyed echoes of slain creatures, wreathed in cold light. They are the realm's nod to the Monarch's army: familiar shapes turned to darkness.$(br2)$(soft)Recognize the silhouette, respect the glow, and remember — what falls in shadow does not always stay down.$()"),
])

# ===================== 11. SURVIVAL & COMFORTS =====================
E("survival","Food & Cooking","minecraft:cooked_beef",0,[
  SPOT("minecraft:cooked_beef","Eat Well","Hunger fuels healing and your combat roll, so never run empty. Hovering food shows its $(rune)saturation$() — richer meals last longer."),
  T("Cooking","The realm adds real $(rune)cooking$() — crops, skillets, and hearty meals that beat raw steak. Set up a small kitchen near base; good food is cheap power."),
])
E("survival","Building & Decor","minecraft:crafting_table",1,[
  T("Make It Yours","Beyond survival, the realm is full of $(rune)building$() blocks and decor — furniture, lamps, bridges, fences, shutters, and rustic furnishings. Build a base that feels like a hunter's lodge, not a dirt hut.$(br2)$(soft)A real home near a village gives you beds, storage, and a fast-travel anchor.$()"),
])
E("survival","Tips & Tools","minecraft:lectern",2,[
  T("Work Smarter","$(li)$(gold)Ctrl+R$() / $(gold)Ctrl+U$() — look up any recipe or use (JEI).$(li)Hover an enchanted book to read what the enchant does.$(li)Enchant conflicts? The realm helps you pick a valid option.$(li)Keep a backpack ($(gold)B$()) and curios ($(gold)G$()) filled."),
  T("When In Doubt","Open the $(gold)Quest Log$() ($(gold)L$()) for direction, check the $(gold)Hunter Board$() for work, and read this Codex for the how. $(soft)A prepared hunter rarely dies surprised.$()"),
])

# ===================== WRITE =====================
import re
def slug(s):
    s=s.lower().replace("&","and")
    s=re.sub(r"[^a-z0-9]+","_",s).strip("_")
    return re.sub(r"_+","_",s)

def write_all():
    for root in ROOTS:
        cats_dir=os.path.join(root,"categories"); ent_dir=os.path.join(root,"entries")
        for d in (cats_dir,ent_dir):
            if os.path.isdir(d): shutil.rmtree(d)
            os.makedirs(d,exist_ok=True)
        for cid,name,desc,icon,sn in CATS:
            json.dump({"name":name,"description":desc,"icon":icon,"sortnum":sn},
                      open(os.path.join(cats_dir,cid+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        for e in ENTRIES:
            cid=e["category"].split(":")[1]
            sub=os.path.join(ent_dir,cid); os.makedirs(sub,exist_ok=True)
            fn=slug(e["name"])+".json"
            json.dump(e,open(os.path.join(sub,fn),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        print("wrote",len(CATS),"categories,",len(ENTRIES),"entries ->",root)

if __name__=="__main__":
    write_all()
