param(
    [string]$ClientModsPath = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Add-Type -AssemblyName System.IO.Compression.FileSystem

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

if ([string]::IsNullOrWhiteSpace($ClientModsPath)) {
    $instancesRoot = "C:\Users\Jayden\curseforge\minecraft\Instances"
    $latestInstance = Get-ChildItem -LiteralPath $instancesRoot -Directory -Filter "Ascendant Realms*" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if (-not $latestInstance) {
        throw "Could not find an Ascendant Realms CurseForge instance under $instancesRoot. Pass -ClientModsPath explicitly."
    }
    $ClientModsPath = Join-Path $latestInstance.FullName "mods"
}

$clientMods = [System.IO.Path]::GetFullPath($ClientModsPath)
$outputDir = Join-Path $root "config\ascendant_index"
$docsDir = Join-Path $root "docs"

if (-not (Test-Path -LiteralPath $clientMods)) {
    throw "ClientModsPath does not exist: $clientMods"
}

function Read-ZipEntryText {
    param(
        [System.IO.Compression.ZipArchive]$Zip,
        [string]$Name
    )

    $entry = $Zip.GetEntry($Name)
    if (-not $entry) {
        return ""
    }

    $reader = [System.IO.StreamReader]::new($entry.Open())
    try {
        return $reader.ReadToEnd()
    }
    finally {
        $reader.Dispose()
    }
}

function Get-ModInfo {
    param([System.IO.Compression.ZipArchive]$Zip)

    $modsToml = Read-ZipEntryText -Zip $Zip -Name "META-INF/mods.toml"
    $displayName = ""
    $modId = ""

    if ($modsToml -match '(?m)^\s*displayName\s*=\s*"([^"]+)"') {
        $displayName = $Matches[1]
    }
    if ($modsToml -match '(?m)^\s*modId\s*=\s*"([^"]+)"') {
        $modId = $Matches[1]
    }

    [PSCustomObject]@{
        ModId = $modId
        DisplayName = $displayName
    }
}

function ConvertTo-PlainName {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ""
    }
    return ($Value -replace '\s+', ' ').Trim()
}

function Test-ContainsAny {
    param(
        [string]$Text,
        [string[]]$Needles
    )
    foreach ($needle in $Needles) {
        if ($Text -like "*$needle*") {
            return $true
        }
    }
    return $false
}

function Get-EntityThreatTier {
    param(
        [string]$Namespace,
        [string]$Id,
        [string]$Name,
        [string]$SourceMod
    )

    $hay = "$Namespace $Id $Name $SourceMod".ToLowerInvariant()

    if (Test-ContainsAny $hay @("projectile", "arrow", "bolt", "bullet", "fireball", "missile", "laser", "beam", "cloud", "effect", "part", "seat", "dummy", "marker", "falling", "portal", "spell_", "magic_missile", "anchor", "cage", "cannon", "cannonball", "crate", "fire_area", "glacial_shove", "ice_spike", "poison_area", "poison_spit", "shockwave", "sword_wave", "thrown_", "rift", "mark", "sand_column", "tentacle", "pile_of_bones", "warning")) {
        return "technical_or_projectile"
    }
    if (Test-ContainsAny $hay @("dragon", "hydra", "gorgon", "cyclops", "dread", "death_worm", "cockatrice", "myrmex", "wyrm")) {
        return "dragon_tier"
    }
    if (Test-ContainsAny $hay @("boss", "monstrosity", "leviathan", "ignis", "harbinger", "scylla", "ender_guardian", "netherite_monstrosity", "maledictus", "ancient_remnant", "prowler", "dead_king", "night_lich", "ferrous_wroughtnaut", "frostmaw")) {
        return "boss"
    }
    if (Test-ContainsAny $hay @("stalker", "reaper", "hound", "knight", "brute", "champion", "mutant", "berserker", "wraith", "specter", "phantom", "ogre", "giant", "guardian", "miniboss")) {
        return "elite"
    }
    if (Test-ContainsAny $hay @("villager", "guard", "npc", "human", "companion", "citizen", "clerk", "merchant", "mca")) {
        return "civilian_or_ally"
    }
    if (Test-ContainsAny $hay @("zombie", "skeleton", "creeper", "spider", "slime", "raider", "illager", "pillager", "witch", "ghoul", "demon", "undead", "parasite", "serpent", "shark", "crocodile", "bear", "tiger", "mosquito", "anaconda", "mimic")) {
        return "dangerous_hostile"
    }
    if (Test-ContainsAny $hay @("fish", "bird", "butterfly", "bee", "frog", "rabbit", "deer", "raccoon", "squirrel", "crow", "duck", "seal", "whale", "horse", "cow", "pig", "sheep", "chicken", "goat", "camel", "snail", "slug", "lobster", "crab", "kangaroo", "elephant", "gazelle", "platypus", "anteater", "eagle", "blue_jay", "monkey", "bison", "emu", "fly", "hummingbird", "humming bird", "roadrunner", "skunk", "sugar_glider", "toucan", "turtle", "worm", "flutter", "bunfungus")) {
        return "passive_or_wildlife"
    }
    if (Test-ContainsAny $hay @("mowziesmobs", "born_in_chaos", "aquamirae", "cataclysm", "soulsweapons", "bosses")) {
        return "dangerous_hostile"
    }
    return "uncategorized_mob"
}

function Get-BountyTier {
    param([string]$ThreatTier)
    switch ($ThreatTier) {
        "dragon_tier" { return "dragon" }
        "boss" { return "boss" }
        "elite" { return "elite" }
        "dangerous_hostile" { return "dangerous" }
        "uncategorized_mob" { return "review" }
        default { return "none" }
    }
}

function Get-EntitySkillHooks {
    param(
        [string]$ThreatTier,
        [string]$Namespace,
        [string]$Id,
        [string]$Name
    )

    $hay = "$Namespace $Id $Name".ToLowerInvariant()
    $hooks = [System.Collections.Generic.List[string]]::new()

    if ($ThreatTier -in @("dangerous_hostile", "elite", "boss", "dragon_tier")) {
        $hooks.Add("warrior")
        $hooks.Add("ranger")
    }
    if ($ThreatTier -in @("elite", "boss")) {
        $hooks.Add("rogue")
    }
    if ($ThreatTier -eq "dragon_tier") {
        $hooks.Add("dragonbound")
    }
    if (Test-ContainsAny $hay @("spell", "mage", "magic", "arcan", "lich", "wizard", "sorcer")) {
        $hooks.Add("arcanist")
    }
    if ($ThreatTier -in @("passive_or_wildlife", "dangerous_hostile")) {
        $hooks.Add("survivalist")
    }

    @($hooks | Select-Object -Unique)
}

function Get-StructureClass {
    param(
        [string]$StructureId,
        [string]$SourceMod
    )

    $hay = "$StructureId $SourceMod".ToLowerInvariant()

    if (Test-ContainsAny $hay @("dragon", "iceandfire", "dragon_roost", "dragon_cave")) {
        return "dragon_tier_zone"
    }
    if (Test-ContainsAny $hay @("cataclysm", "boss", "arena", "monstrosity", "leviathan", "ignis", "maledictus", "soul", "cursed_pyramid")) {
        return "boss_arena"
    }
    if (Test-ContainsAny $hay @("village", "town", "settlement", "market", "guild", "outpost", "camp")) {
        return "settlement"
    }
    if (Test-ContainsAny $hay @("dungeon", "stronghold", "mineshaft", "crypt", "catacomb", "tower", "fortress", "temple", "labyrinth", "keep", "castle", "bastion")) {
        return "dangerous_dungeon"
    }
    if (Test-ContainsAny $hay @("ship", "ruin", "well", "house", "hut", "shrine", "grave", "monument", "bridge", "road")) {
        return "landmark_or_ruin"
    }
    if (Test-ContainsAny $hay @("nether")) {
        return "nether_landmark"
    }
    if (Test-ContainsAny $hay @("end")) {
        return "end_landmark"
    }
    return "uncategorized_structure"
}

function Get-StructureLootTier {
    param([string]$StructureClass)
    switch ($StructureClass) {
        "settlement" { return "village_supplies" }
        "landmark_or_ruin" { return "minor_ruin" }
        "dangerous_dungeon" { return "rare_to_epic" }
        "boss_arena" { return "legendary_to_mythic" }
        "dragon_tier_zone" { return "mythic_to_ascendant" }
        "nether_landmark" { return "rare_to_legendary" }
        "end_landmark" { return "epic_to_mythic" }
        default { return "review" }
    }
}

function Get-StructureHooks {
    param(
        [string]$StructureClass,
        [string]$StructureId
    )

    $hooks = [System.Collections.Generic.List[string]]::new()
    switch ($StructureClass) {
        "settlement" {
            $hooks.Add("guild")
            $hooks.Add("bountiful")
            $hooks.Add("mca")
            $hooks.Add("guard_villagers")
        }
        "dangerous_dungeon" {
            $hooks.Add("loot_integrations")
            $hooks.Add("bountiful")
            $hooks.Add("skill_milestone")
        }
        "boss_arena" {
            $hooks.Add("boss_bounty")
            $hooks.Add("skill_milestone")
            $hooks.Add("rarity_loot")
        }
        "dragon_tier_zone" {
            $hooks.Add("dragonbound")
            $hooks.Add("boss_bounty")
            $hooks.Add("rarity_loot")
        }
        default {
            $hooks.Add("world_lore")
        }
    }
    if ($StructureId -like "*create*") {
        $hooks.Add("engineer")
    }
    @($hooks | Select-Object -Unique)
}

function Escape-Md {
    param([object]$Value)
    return ([string]$Value -replace '\|', '\|' -replace "`r?`n", " ").Trim()
}

$entities = [System.Collections.Generic.List[object]]::new()
$structures = [System.Collections.Generic.List[object]]::new()
$structureSetMap = @{}

foreach ($jar in Get-ChildItem -LiteralPath $clientMods -Filter "*.jar" -File | Sort-Object Name) {
    $zip = [System.IO.Compression.ZipFile]::OpenRead($jar.FullName)
    try {
        $info = Get-ModInfo -Zip $zip
        $sourceMod = if ($info.DisplayName) { $info.DisplayName } elseif ($info.ModId) { $info.ModId } else { $jar.BaseName }
        $entryNames = @($zip.Entries | ForEach-Object { $_.FullName })

        foreach ($entryName in $entryNames | Where-Object { $_ -match '^data/.+/worldgen/structure_set/.+\.json$' }) {
            $jsonText = Read-ZipEntryText -Zip $zip -Name $entryName
            if (-not $jsonText) {
                continue
            }
            try {
                $json = $jsonText | ConvertFrom-Json
                $spacing = if ($json.PSObject.Properties.Name -contains "spacing") { [int]$json.spacing } else { $null }
                $separation = if ($json.PSObject.Properties.Name -contains "separation") { [int]$json.separation } else { $null }
                $setId = ($entryName -replace '^data/([^/]+)/worldgen/structure_set/(.+)\.json$', '$1:$2')
                if ($json.PSObject.Properties.Name -contains "structures") {
                    foreach ($structureRef in @($json.structures)) {
                        $structureId = ""
                        if ($structureRef -is [string]) {
                            $structureId = $structureRef
                        }
                        elseif ($structureRef.PSObject.Properties.Name -contains "structure") {
                            $structureId = [string]$structureRef.structure
                        }
                        if ($structureId) {
                            if (-not $structureSetMap.ContainsKey($structureId)) {
                                $structureSetMap[$structureId] = [System.Collections.Generic.List[object]]::new()
                            }
                            $structureSetMap[$structureId].Add([PSCustomObject]@{
                                structure_set = $setId
                                spacing = $spacing
                                separation = $separation
                            })
                        }
                    }
                }
            }
            catch {
                continue
            }
        }

        foreach ($entryName in $entryNames | Where-Object { $_ -match '^assets/.+/lang/en_us\.json$' }) {
            $langText = Read-ZipEntryText -Zip $zip -Name $entryName
            if (-not $langText) {
                continue
            }
            try {
                $lang = $langText | ConvertFrom-Json
                foreach ($property in $lang.PSObject.Properties) {
                    if ($property.Name -notmatch '^entity\.([^.]+)\.([^.]+)$') {
                        continue
                    }
                    $namespace = $Matches[1]
                    $id = $Matches[2]
                    $entityId = "$namespace`:$id"
                    if ($entityId -like "minecraft:*") {
                        continue
                    }
                    $displayName = ConvertTo-PlainName ([string]$property.Value)
                    $tier = Get-EntityThreatTier -Namespace $namespace -Id $id -Name $displayName -SourceMod $sourceMod
                    $entities.Add([PSCustomObject]@{
                        entity_id = $entityId
                        name = $displayName
                        source_mod = $sourceMod
                        jar = $jar.Name
                        threat_tier = $tier
                        bounty_tier = Get-BountyTier $tier
                        skill_hooks = @(Get-EntitySkillHooks -ThreatTier $tier -Namespace $namespace -Id $id -Name $displayName)
                        spawn_review = if ($tier -in @("dangerous_hostile", "elite", "boss", "dragon_tier", "uncategorized_mob")) { "required" } else { "optional" }
                        notes = "Generated from language/entity keys; verify exact spawn behavior from configs, biome modifiers, and in-game checks."
                    })
                }
            }
            catch {
                continue
            }
        }

        foreach ($entryName in $entryNames | Where-Object { $_ -match '^data/.+/worldgen/structure/.+\.json$' }) {
            $structureId = ($entryName -replace '^data/([^/]+)/worldgen/structure/(.+)\.json$', '$1:$2')
            $class = Get-StructureClass -StructureId $structureId -SourceMod $sourceMod
            $sets = @()
            if ($structureSetMap.ContainsKey($structureId)) {
                $sets = @($structureSetMap[$structureId])
            }
            $structures.Add([PSCustomObject]@{
                structure_id = $structureId
                source_mod = $sourceMod
                jar = $jar.Name
                structure_class = $class
                loot_tier = Get-StructureLootTier $class
                integration_hooks = @(Get-StructureHooks -StructureClass $class -StructureId $structureId)
                structure_sets = $sets
                density_review = if ($class -in @("settlement", "dangerous_dungeon", "boss_arena", "dragon_tier_zone", "uncategorized_structure")) { "required" } else { "optional" }
                notes = "Generated from worldgen structure JSON; verify spacing, biome tags, and template processors before pool injection."
            })
        }
    }
    finally {
        $zip.Dispose()
    }
}

$entities = @($entities | Sort-Object entity_id -Unique)
$structures = @($structures | Sort-Object structure_id -Unique)

New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
New-Item -ItemType Directory -Force -Path $docsDir | Out-Null

$generatedAt = (Get-Date).ToString("o")

$mobRegistry = [PSCustomObject]@{
    version = 1
    generated_at = $generatedAt
    client_mods_path = $clientMods
    source = "Generated from active client jar language/entity keys."
    confidence_note = "This registry classifies discovered entity IDs for integration planning. It is not a final spawn proof by itself."
    mobs = $entities
}

$structureRegistry = [PSCustomObject]@{
    version = 1
    generated_at = $generatedAt
    client_mods_path = $clientMods
    source = "Generated from active client jar worldgen structure and structure_set JSON."
    confidence_note = "This registry classifies structures for density, loot, bounty, and settlement planning. It is not a final in-game placement proof by itself."
    structures = $structures
}

$matrix = [PSCustomObject]@{
    version = 1
    generated_at = $generatedAt
    coverage = [PSCustomObject]@{
        mobs_indexed = $entities.Count
        structures_indexed = $structures.Count
        mobs_requiring_spawn_review = @($entities | Where-Object { $_.spawn_review -eq "required" }).Count
        structures_requiring_density_review = @($structures | Where-Object { $_.density_review -eq "required" }).Count
    }
    implementation_layers = @(
        [PSCustomObject]@{ layer = "Config"; use = "Mod-exposed spawn, UI, density, health, audio, and visual settings." },
        [PSCustomObject]@{ layer = "Open Loader datapacks"; use = "Tags, loot tables, structure tags, recipes, advancements, and function fallbacks." },
        [PSCustomObject]@{ layer = "KubeJS"; use = "Tooltips, item registration, JEI aliases, tags, recipe glue, and light event glue." },
        [PSCustomObject]@{ layer = "Custom Forge helper mods"; use = "Dynamic nameplates, skill HUD, runtime NPC profiles, encounter director, and synced rarity/progression data." }
    )
    custom_mod_candidates = @(
        [PSCustomObject]@{ id = "ascendant_core"; priority = "high"; reason = "Shared registry loader, client/server sync, commands, and integration APIs." },
        [PSCustomObject]@{ id = "ascendant_nameplates"; priority = "very_high"; reason = "Styled dynamic player, NPC, rival, and enemy labels beyond vanilla scoreboard limits." },
        [PSCustomObject]@{ id = "ascendant_progression_hud"; priority = "very_high"; reason = "Second skill XP bar, level-up popups, and rank milestone presentation." },
        [PSCustomObject]@{ id = "ascendant_npc_runtime"; priority = "high"; reason = "Profile-driven NPC setup, equipment, rank/level identity, and repair without embedded script drift." },
        [PSCustomObject]@{ id = "ascendant_settlement_engine"; priority = "medium_high"; reason = "Safe Hunter Board/Guild structure placement and NPC population once standalone structures are proven." },
        [PSCustomObject]@{ id = "ascendant_encounter_director"; priority = "medium"; reason = "Player/rank-aware spawn pressure if config and In Control rules are not enough." }
    )
}

function Get-BountyBoard {
    param([string]$BountyTier)
    switch ($BountyTier) {
        "dangerous" { return "village_hunter_board" }
        "elite" { return "town_guild_board" }
        "boss" { return "major_guild_registry" }
        "dragon" { return "major_guild_registry" }
        default { return "review" }
    }
}

function Get-BountyRewardRarity {
    param([string]$BountyTier)
    switch ($BountyTier) {
        "dangerous" { return "rare" }
        "elite" { return "epic" }
        "boss" { return "legendary" }
        "dragon" { return "mythic" }
        default { return "review" }
    }
}

$bountyTargets = @(
    $entities |
        Where-Object { $_.bounty_tier -notin @("none", "review") } |
        ForEach-Object {
            [PSCustomObject]@{
                target_id = $_.entity_id
                name = $_.name
                source_mod = $_.source_mod
                threat_tier = $_.threat_tier
                bounty_tier = $_.bounty_tier
                recommended_board = Get-BountyBoard $_.bounty_tier
                reward_rarity = Get-BountyRewardRarity $_.bounty_tier
                skill_hooks = $_.skill_hooks
                contract_note = "Generated target. Confirm exact spawn rate, drops, and fairness before making it a live contract."
            }
        } |
        Sort-Object bounty_tier, target_id
)

$spawnGroups = @(
    $entities |
        Where-Object { $_.spawn_review -eq "required" } |
        ForEach-Object {
            $namespace = ($_.entity_id -split ":", 2)[0]
            [PSCustomObject]@{
                namespace = $namespace
                entity_id = $_.entity_id
                name = $_.name
                source_mod = $_.source_mod
                threat_tier = $_.threat_tier
                bounty_tier = $_.bounty_tier
            }
        } |
        Group-Object namespace |
        ForEach-Object {
            $tierCounts = @{}
            foreach ($tierGroup in $_.Group | Group-Object threat_tier) {
                $tierCounts[$tierGroup.Name] = $tierGroup.Count
            }
            [PSCustomObject]@{
                namespace = $_.Name
                count = $_.Count
                tier_counts = $tierCounts
                suggested_policy = if ($_.Name -eq "iceandfire") {
                    "Distance-gate dragon-tier spawns and keep dragon contracts late-game."
                } elseif ($_.Name -eq "alexsmobs") {
                    "Separate passive wildlife from predators; avoid blanket danger treatment."
                } elseif ($_.Name -eq "born_in_chaos_v1") {
                    "Use night, ruin, graveyard, and event pressure; avoid overwhelming settlements."
                } elseif ($_.Name -eq "aquamirae") {
                    "Keep cold/ocean danger thematic; connect coastal contracts."
                } elseif ($_.Name -eq "cataclysm") {
                    "Keep boss and elite content structure/milestone driven."
                } else {
                    "Review biome/config spawn behavior and connect to threat tier."
                }
                entities = @($_.Group | Select-Object entity_id, name, source_mod, threat_tier, bounty_tier)
            }
        } |
        Sort-Object namespace
)

$bountyPoolGroups = @(
    $bountyTargets |
        Group-Object recommended_board, bounty_tier, reward_rarity |
        ForEach-Object {
            $parts = $_.Name -split ", "
            [PSCustomObject]@{
                board = $parts[0]
                bounty_tier = $parts[1]
                reward_rarity = $parts[2]
                target_count = $_.Count
                targets = @($_.Group | Select-Object target_id, name, source_mod, threat_tier, skill_hooks)
            }
        } |
        Sort-Object board, bounty_tier, reward_rarity
)

$branches = @("warrior", "rogue", "ranger", "arcanist", "engineer", "survivalist", "dragonbound")
$skillHookData = [ordered]@{
    version = 1
    generated_at = $generatedAt
    source = "Generated from mob and structure registries."
    branches = [ordered]@{}
}

foreach ($branch in $branches) {
    $mobHooks = @($entities | Where-Object { $_.skill_hooks -contains $branch } | Select-Object -ExpandProperty entity_id)
    $structureHooks = @()
    switch ($branch) {
        "warrior" {
            $structureHooks = @($structures | Where-Object { $_.integration_hooks -contains "skill_milestone" -or $_.integration_hooks -contains "boss_bounty" } | Select-Object -ExpandProperty structure_id)
        }
        "rogue" {
            $structureHooks = @($structures | Where-Object { $_.structure_class -in @("dangerous_dungeon", "landmark_or_ruin") } | Select-Object -ExpandProperty structure_id)
        }
        "ranger" {
            $structureHooks = @($structures | Where-Object { $_.integration_hooks -contains "bountiful" -or $_.structure_class -in @("landmark_or_ruin", "dangerous_dungeon") } | Select-Object -ExpandProperty structure_id)
        }
        "arcanist" {
            $structureHooks = @($structures | Where-Object { $_.structure_id -match "magic|mage|spell|tower|crypt|cataclysm|soul|end" } | Select-Object -ExpandProperty structure_id)
        }
        "engineer" {
            $structureHooks = @($structures | Where-Object { $_.integration_hooks -contains "engineer" -or $_.structure_id -match "create|factory|workshop|bridge" } | Select-Object -ExpandProperty structure_id)
        }
        "survivalist" {
            $structureHooks = @($structures | Where-Object { $_.structure_class -in @("settlement", "landmark_or_ruin") } | Select-Object -ExpandProperty structure_id)
        }
        "dragonbound" {
            $structureHooks = @($structures | Where-Object { $_.integration_hooks -contains "dragonbound" -or $_.structure_class -eq "dragon_tier_zone" } | Select-Object -ExpandProperty structure_id)
        }
    }

    $skillHookData.branches[$branch] = [PSCustomObject]@{
        mob_hooks = @($mobHooks | Sort-Object -Unique)
        structure_hooks = @($structureHooks | Sort-Object -Unique)
        implementation_note = "Generated hook candidates. Wire into Puffish Skills, FTB Quests, advancements, or a custom Ascendant helper mod only after validation."
    }
}

$mobRegistry | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $outputDir "mob_registry.json") -Encoding UTF8
$structureRegistry | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $outputDir "structure_registry.json") -Encoding UTF8
$matrix | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $outputDir "integration_matrix.json") -Encoding UTF8
$skillHookData | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $outputDir "skill_hook_registry.json") -Encoding UTF8
([PSCustomObject]@{
    version = 1
    generated_at = $generatedAt
    source = "Generated from config/ascendant_index/mob_registry.json."
    spawn_groups = $spawnGroups
}) | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $outputDir "spawn_tuning_worklist.json") -Encoding UTF8

$guildDir = Join-Path $root "config\ascendant_guild"
New-Item -ItemType Directory -Force -Path $guildDir | Out-Null
([PSCustomObject]@{
    version = 1
    generated_at = $generatedAt
    source = "Generated from config/ascendant_index/mob_registry.json."
    bounty_targets = $bountyTargets
}) | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $guildDir "generated_bounty_targets.json") -Encoding UTF8
([PSCustomObject]@{
    version = 1
    generated_at = $generatedAt
    source = "Generated from config/ascendant_guild/generated_bounty_targets.json."
    pool_groups = $bountyPoolGroups
}) | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $guildDir "bounty_pool_worklist.json") -Encoding UTF8

$mobLines = [System.Collections.Generic.List[string]]::new()
$mobLines.Add("# Mob Threat Index")
$mobLines.Add("")
$mobLines.Add("Generated: $generatedAt")
$mobLines.Add("")
$mobLines.Add("Source: active client jars at ``$clientMods``.")
$mobLines.Add("")
$mobLines.Add("This index is generated from entity language keys. It gives Ascendant Realms a single working mob/threat registry for spawn tuning, bounties, skill hooks, and nameplate planning. It does not prove exact spawn locations by itself.")
$mobLines.Add("")
$mobLines.Add("## Summary")
$mobLines.Add("")
$mobLines.Add("| Threat Tier | Count |")
$mobLines.Add("| --- | ---: |")
foreach ($group in $entities | Group-Object threat_tier | Sort-Object Name) {
    $mobLines.Add("| $(Escape-Md $group.Name) | $($group.Count) |")
}
$mobLines.Add("")
$mobLines.Add("## Full Registry")
$mobLines.Add("")
$mobLines.Add("| Entity ID | Name | Mod | Threat Tier | Bounty Tier | Skill Hooks | Review |")
$mobLines.Add("| --- | --- | --- | --- | --- | --- | --- |")
foreach ($entity in $entities) {
    $mobLines.Add("| ``$(Escape-Md $entity.entity_id)`` | $(Escape-Md $entity.name) | $(Escape-Md $entity.source_mod) | $(Escape-Md $entity.threat_tier) | $(Escape-Md $entity.bounty_tier) | $(Escape-Md (($entity.skill_hooks -join ', '))) | $(Escape-Md $entity.spawn_review) |")
}
$mobLines | Set-Content -LiteralPath (Join-Path $docsDir "MOB_THREAT_INDEX.md") -Encoding UTF8

$structureLines = [System.Collections.Generic.List[string]]::new()
$structureLines.Add("# Structure Index")
$structureLines.Add("")
$structureLines.Add("Generated: $generatedAt")
$structureLines.Add("")
$structureLines.Add("Source: active client jars at ``$clientMods``.")
$structureLines.Add("")
$structureLines.Add("This index gives Ascendant Realms a pack-owned structure registry for density tuning, loot tiers, bounties, settlement work, and crash-safe integration. It does not prove exact in-world placement by itself.")
$structureLines.Add("")
$structureLines.Add("## Summary")
$structureLines.Add("")
$structureLines.Add("| Structure Class | Count |")
$structureLines.Add("| --- | ---: |")
foreach ($group in $structures | Group-Object structure_class | Sort-Object Name) {
    $structureLines.Add("| $(Escape-Md $group.Name) | $($group.Count) |")
}
$structureLines.Add("")
$structureLines.Add("## Full Registry")
$structureLines.Add("")
$structureLines.Add("| Structure ID | Mod | Class | Loot Tier | Hooks | Sets / Spacing | Review |")
$structureLines.Add("| --- | --- | --- | --- | --- | --- | --- |")
foreach ($structure in $structures) {
    $setText = if ($structure.structure_sets.Count -gt 0) {
        (($structure.structure_sets | ForEach-Object {
            "$($_.structure_set) spacing=$($_.spacing) separation=$($_.separation)"
        }) -join "; ")
    } else {
        ""
    }
    $structureLines.Add("| ``$(Escape-Md $structure.structure_id)`` | $(Escape-Md $structure.source_mod) | $(Escape-Md $structure.structure_class) | $(Escape-Md $structure.loot_tier) | $(Escape-Md (($structure.integration_hooks -join ', '))) | $(Escape-Md $setText) | $(Escape-Md $structure.density_review) |")
}
$structureLines | Set-Content -LiteralPath (Join-Path $docsDir "STRUCTURE_INDEX.md") -Encoding UTF8

$matrixLines = [System.Collections.Generic.List[string]]::new()
$matrixLines.Add("# Ascendant Integration Matrix")
$matrixLines.Add("")
$matrixLines.Add("Generated: $generatedAt")
$matrixLines.Add("")
$matrixLines.Add("This matrix turns the master integration plan into implementation layers that can be tested without manual play-feel checks.")
$matrixLines.Add("")
$matrixLines.Add("## Coverage")
$matrixLines.Add("")
$matrixLines.Add("| Area | Count |")
$matrixLines.Add("| --- | ---: |")
$matrixLines.Add("| Mobs indexed | $($entities.Count) |")
$matrixLines.Add("| Structures indexed | $($structures.Count) |")
$matrixLines.Add("| Mobs requiring spawn review | $(@($entities | Where-Object { $_.spawn_review -eq 'required' }).Count) |")
$matrixLines.Add("| Structures requiring density review | $(@($structures | Where-Object { $_.density_review -eq 'required' }).Count) |")
$matrixLines.Add("")
$matrixLines.Add("## Implementation Layers")
$matrixLines.Add("")
$matrixLines.Add("| Layer | Use |")
$matrixLines.Add("| --- | --- |")
foreach ($layer in $matrix.implementation_layers) {
    $matrixLines.Add("| $(Escape-Md $layer.layer) | $(Escape-Md $layer.use) |")
}
$matrixLines.Add("")
$matrixLines.Add("## Custom Mod Candidates")
$matrixLines.Add("")
$matrixLines.Add("| Candidate | Priority | Why |")
$matrixLines.Add("| --- | --- | --- |")
foreach ($candidate in $matrix.custom_mod_candidates) {
    $matrixLines.Add("| ``$(Escape-Md $candidate.id)`` | $(Escape-Md $candidate.priority) | $(Escape-Md $candidate.reason) |")
}
$matrixLines.Add("")
$matrixLines.Add("## Automated Next Steps")
$matrixLines.Add("")
$matrixLines.Add("- Use `config/ascendant_index/mob_registry.json` to drive the next In Control and bounty tuning pass.")
$matrixLines.Add("- Use `config/ascendant_index/structure_registry.json` to drive settlement, loot, and density tuning.")
$matrixLines.Add("- Use `config/ascendant_index/integration_matrix.json` as the machine-readable custom-mod threshold list.")
$matrixLines.Add("- Keep runtime overlays and entity behavior out of datapacks if the data cannot be read or synced safely.")
$matrixLines | Set-Content -LiteralPath (Join-Path $docsDir "ASCENDANT_INTEGRATION_MATRIX.md") -Encoding UTF8

$bountyLines = [System.Collections.Generic.List[string]]::new()
$bountyLines.Add("# Bounty Target Index")
$bountyLines.Add("")
$bountyLines.Add("Generated: $generatedAt")
$bountyLines.Add("")
$bountyLines.Add("This file turns the generated mob threat registry into first-pass Guild/Hunter bounty targets. It is not live quest content yet; it is the reviewable target list for Bountiful, FTB Quests, and future Hunter Boards.")
$bountyLines.Add("")
$bountyLines.Add("## Summary")
$bountyLines.Add("")
$bountyLines.Add("| Bounty Tier | Count |")
$bountyLines.Add("| --- | ---: |")
foreach ($group in $bountyTargets | Group-Object bounty_tier | Sort-Object Name) {
    $bountyLines.Add("| $(Escape-Md $group.Name) | $($group.Count) |")
}
$bountyLines.Add("")
$bountyLines.Add("## Targets")
$bountyLines.Add("")
$bountyLines.Add("| Target | Name | Mod | Tier | Board | Reward Rarity | Skill Hooks |")
$bountyLines.Add("| --- | --- | --- | --- | --- | --- | --- |")
foreach ($target in $bountyTargets) {
    $bountyLines.Add("| ``$(Escape-Md $target.target_id)`` | $(Escape-Md $target.name) | $(Escape-Md $target.source_mod) | $(Escape-Md $target.bounty_tier) | $(Escape-Md $target.recommended_board) | $(Escape-Md $target.reward_rarity) | $(Escape-Md (($target.skill_hooks -join ', '))) |")
}
$bountyLines | Set-Content -LiteralPath (Join-Path $docsDir "BOUNTY_TARGET_INDEX.md") -Encoding UTF8

$skillLines = [System.Collections.Generic.List[string]]::new()
$skillLines.Add("# Skill Hook Registry")
$skillLines.Add("")
$skillLines.Add("Generated: $generatedAt")
$skillLines.Add("")
$skillLines.Add("This registry maps generated mob and structure content into Ascendant Web branch hooks. It is a safe planning layer for future Puffish Skills, FTB Quests, advancement, or custom helper-mod integration.")
$skillLines.Add("")
$skillLines.Add("| Branch | Mob Hooks | Structure Hooks |")
$skillLines.Add("| --- | ---: | ---: |")
foreach ($branch in $branches) {
    $branchData = $skillHookData.branches[$branch]
    $skillLines.Add("| $(Escape-Md $branch) | $($branchData.mob_hooks.Count) | $($branchData.structure_hooks.Count) |")
}
$skillLines.Add("")
$skillLines.Add("## Notes")
$skillLines.Add("")
$skillLines.Add("- Warrior and Ranger receive broad hostile/combat hooks.")
$skillLines.Add("- Rogue receives elite/dungeon hooks.")
$skillLines.Add("- Arcanist receives magic, soul, crypt, tower, end, and spell-adjacent hooks.")
$skillLines.Add("- Engineer receives Create/workshop/bridge hooks.")
$skillLines.Add("- Survivalist receives wildlife, settlement, and ruin hooks.")
$skillLines.Add("- Dragonbound receives dragon-tier and boss-tier hooks.")
$skillLines | Set-Content -LiteralPath (Join-Path $docsDir "SKILL_HOOK_REGISTRY.md") -Encoding UTF8

$spawnLines = [System.Collections.Generic.List[string]]::new()
$spawnLines.Add("# Spawn Tuning Worklist")
$spawnLines.Add("")
$spawnLines.Add("Generated: $generatedAt")
$spawnLines.Add("")
$spawnLines.Add("This worklist turns the generated mob registry into reviewable spawn-tuning groups. It does not change active In Control rules yet.")
$spawnLines.Add("")
$spawnLines.Add("| Namespace | Entities Requiring Review | Suggested Policy |")
$spawnLines.Add("| --- | ---: | --- |")
foreach ($group in $spawnGroups) {
    $spawnLines.Add("| ``$(Escape-Md $group.namespace)`` | $($group.count) | $(Escape-Md $group.suggested_policy) |")
}
$spawnLines.Add("")
$spawnLines.Add("## Active Config Note")
$spawnLines.Add("")
$spawnLines.Add("The current active `config/incontrol/spawn.json` uses broad per-mod caps. The next safe tuning pass should preserve those caps while adding specific biome, structure, distance, and tier rules only after reviewing these generated groups.")
$spawnLines | Set-Content -LiteralPath (Join-Path $docsDir "SPAWN_TUNING_WORKLIST.md") -Encoding UTF8

$poolLines = [System.Collections.Generic.List[string]]::new()
$poolLines.Add("# Bounty Pool Worklist")
$poolLines.Add("")
$poolLines.Add("Generated: $generatedAt")
$poolLines.Add("")
$poolLines.Add("This worklist groups generated bounty targets into future Hunter Board pools. It does not modify Bountiful configs yet.")
$poolLines.Add("")
$poolLines.Add("| Board | Bounty Tier | Reward Rarity | Targets |")
$poolLines.Add("| --- | --- | --- | ---: |")
foreach ($group in $bountyPoolGroups) {
    $poolLines.Add("| $(Escape-Md $group.board) | $(Escape-Md $group.bounty_tier) | $(Escape-Md $group.reward_rarity) | $($group.target_count) |")
}
$poolLines.Add("")
$poolLines.Add("## Active Config Note")
$poolLines.Add("")
$poolLines.Add("The current Bountiful config is still generic. Use this worklist to author board-specific pools after confirming each target's spawn behavior and reward fairness.")
$poolLines | Set-Content -LiteralPath (Join-Path $docsDir "BOUNTY_POOL_WORKLIST.md") -Encoding UTF8

Write-Host "Generated $($entities.Count) mob entries and $($structures.Count) structure entries."
Write-Host "Wrote config/ascendant_index/mob_registry.json"
Write-Host "Wrote config/ascendant_index/structure_registry.json"
Write-Host "Wrote config/ascendant_index/integration_matrix.json"
Write-Host "Wrote config/ascendant_index/skill_hook_registry.json"
Write-Host "Wrote config/ascendant_index/spawn_tuning_worklist.json"
Write-Host "Wrote config/ascendant_guild/generated_bounty_targets.json"
Write-Host "Wrote config/ascendant_guild/bounty_pool_worklist.json"
