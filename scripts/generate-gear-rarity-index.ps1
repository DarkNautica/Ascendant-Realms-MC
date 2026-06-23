param(
    [string]$ModsPath = "",
    [string]$ActiveConfigPath = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$DocsDir = Join-Path $Root "docs"
$IndexDir = Join-Path $Root "config\ascendant_index"
$ItemBordersPath = Join-Path $Root "config\itemborders-common.toml"
$KubeJsPath = Join-Path $Root "kubejs\startup_scripts\ascendant_gear_rarity.js"
$KubeJsTooltipPath = Join-Path $Root "kubejs\client_scripts\ascendant_rarity_tooltips.js"

if ([string]::IsNullOrWhiteSpace($ModsPath) -or [string]::IsNullOrWhiteSpace($ActiveConfigPath)) {
    $instancesRoot = "C:\Users\Jayden\curseforge\minecraft\Instances"
    $latestInstance = Get-ChildItem -LiteralPath $instancesRoot -Directory -Filter "Ascendant Realms*" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if (-not $latestInstance) {
        throw "Could not find an Ascendant Realms CurseForge instance under $instancesRoot. Pass -ModsPath and -ActiveConfigPath explicitly."
    }
    if ([string]::IsNullOrWhiteSpace($ModsPath)) {
        $ModsPath = Join-Path $latestInstance.FullName "mods"
    }
    if ([string]::IsNullOrWhiteSpace($ActiveConfigPath)) {
        $ActiveConfigPath = Join-Path $latestInstance.FullName "config"
    }
}

New-Item -ItemType Directory -Force -Path $IndexDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $ItemBordersPath) | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $KubeJsPath) | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $KubeJsTooltipPath) | Out-Null

Add-Type -AssemblyName System.IO.Compression.FileSystem

function Write-Utf8NoBom {
    param(
        [string]$Path,
        [string]$Value
    )
    $encoding = New-Object System.Text.UTF8Encoding -ArgumentList $false
    [System.IO.File]::WriteAllText($Path, $Value, $encoding)
}

$rarityOrder = @("common", "uncommon", "rare", "epic", "legendary", "mythic", "ascendant")
$rarityLabels = @{
    common = "Common"
    uncommon = "Uncommon"
    rare = "Rare"
    epic = "Epic"
    legendary = "Legendary"
    mythic = "Mythic"
    ascendant = "Ascendant"
}
$rarityColors = [ordered]@{
    common = "#9CA3AF"
    uncommon = "#55FF55"
    rare = "#55AAFF"
    epic = "#D966FF"
    legendary = "#FFE66D"
    mythic = "#FF3B00"
    ascendant = "#E6FBFF"
}

$items = @{}
$spells = @{}
$weaponAttributes = @{}
$sourceMods = @{}

function Convert-IdToName {
    param([string]$Id)
    $leaf = ($Id -split ":", 2)[-1]
    (($leaf -replace "[_/]+", " ").Trim() -split "\s+" | ForEach-Object {
        if ($_.Length -eq 0) { "" } else { $_.Substring(0, 1).ToUpperInvariant() + $_.Substring(1) }
    }) -join " "
}

function Normalize-Text {
    param([string]$Value)
    if (-not $Value) { return "" }
    ($Value -replace "\s+", " ").Trim()
}

function Add-SetValue {
    param(
        [hashtable]$Entry,
        [string]$Key,
        [string]$Value
    )
    if (-not $Entry.ContainsKey($Key)) {
        $Entry[$Key] = New-Object System.Collections.Generic.HashSet[string]
    }
    [void]$Entry[$Key].Add($Value)
}

function Get-OrCreateItem {
    param(
        [string]$Id,
        [string]$Name = "",
        [string]$Source = "",
        [string]$Jar = ""
    )
    if (-not $Id -or $Id -notmatch "^[a-z0-9_.-]+:[a-z0-9_./-]+$") {
        return $null
    }
    $cleanId = $Id.ToLowerInvariant()
    if (-not $items.ContainsKey($cleanId)) {
        $modId = ($cleanId -split ":", 2)[0]
        $items[$cleanId] = [ordered]@{
            id = $cleanId
            name = $(if ($Name) { Normalize-Text $Name } else { Convert-IdToName $cleanId })
            mod_id = $modId
            source_mod = $(if ($Source) { $Source } else { $modId })
            jar = $Jar
            domains = New-Object System.Collections.Generic.HashSet[string]
            tags = New-Object System.Collections.Generic.HashSet[string]
            evidence = New-Object System.Collections.Generic.HashSet[string]
            damage = ""
            damage_status = "not exposed in scanned data"
            attack_speed = ""
            armor = ""
            armor_toughness = ""
            durability = ""
            better_combat_category = ""
            attack_range = ""
            max_damage_multiplier = ""
            rarity = ""
            rarity_color = ""
            rarity_reason = ""
            notes = New-Object System.Collections.Generic.HashSet[string]
        }
    } elseif ($Name -and $items[$cleanId].name -eq (Convert-IdToName $cleanId)) {
        $items[$cleanId].name = Normalize-Text $Name
    }
    if ($Source) { $items[$cleanId].source_mod = $Source }
    if ($Jar) { $items[$cleanId].jar = $Jar }
    return $items[$cleanId]
}

function Add-Spell {
    param(
        [string]$Id,
        [string]$Name,
        [string]$Source = "Iron's Spells 'n Spellbooks"
    )
    if (-not $Id -or $Id -notmatch "^[a-z0-9_.-]+:[a-z0-9_./-]+$") { return }
    $cleanId = $Id.ToLowerInvariant()
    if ($cleanId.EndsWith(":none")) { return }
    if (-not $spells.ContainsKey($cleanId)) {
        $spells[$cleanId] = [ordered]@{
            id = $cleanId
            name = $(if ($Name) { Normalize-Text $Name } else { Convert-IdToName $cleanId })
            source_mod = $Source
            domain = "spell"
            damage = "varies by spell level/config"
            damage_status = "spell scaling not exposed as item attack damage"
            rarity = ""
            rarity_color = ""
            rarity_reason = ""
            notes = New-Object System.Collections.Generic.HashSet[string]
        }
    }
}

function Read-ZipText {
    param(
        [System.IO.Compression.ZipArchive]$Zip,
        [System.IO.Compression.ZipArchiveEntry]$Entry
    )
    $stream = $Entry.Open()
    try {
        $reader = [System.IO.StreamReader]::new($stream)
        try { return $reader.ReadToEnd() } finally { $reader.Dispose() }
    } finally {
        $stream.Dispose()
    }
}

function Read-JsonLoose {
    param([string]$Text)
    try {
        return ($Text | ConvertFrom-Json)
    } catch {
        return $null
    }
}

function Get-JsonPropertyMap {
    param($Object)
    $map = @{}
    if ($null -eq $Object) { return $map }
    foreach ($prop in $Object.PSObject.Properties) {
        $map[$prop.Name] = $prop.Value
    }
    return $map
}

function Get-ModNameFromToml {
    param([string]$Text, [string]$Fallback)
    if ($Text -match '(?m)^\s*displayName\s*=\s*"([^"]+)"') { return $Matches[1] }
    if ($Text -match '(?m)^\s*modId\s*=\s*"([^"]+)"') { return $Matches[1] }
    return $Fallback
}

function Add-VanillaItems {
    $vanilla = @(
        @{ id = "minecraft:wooden_sword"; name = "Wooden Sword"; domain = "weapon"; damage = "4"; speed = "1.6"; rarity = "common"; reason = "Vanilla baseline wooden weapon" },
        @{ id = "minecraft:stone_sword"; name = "Stone Sword"; domain = "weapon"; damage = "5"; speed = "1.6"; rarity = "common"; reason = "Vanilla baseline stone weapon" },
        @{ id = "minecraft:iron_sword"; name = "Iron Sword"; domain = "weapon"; damage = "6"; speed = "1.6"; rarity = "uncommon"; reason = "Standard early metal weapon" },
        @{ id = "minecraft:golden_sword"; name = "Golden Sword"; domain = "weapon"; damage = "4"; speed = "1.6"; rarity = "uncommon"; reason = "Low damage but special material/enchanting value" },
        @{ id = "minecraft:diamond_sword"; name = "Diamond Sword"; domain = "weapon"; damage = "7"; speed = "1.6"; rarity = "rare"; reason = "Vanilla high-tier pre-Netherite weapon" },
        @{ id = "minecraft:netherite_sword"; name = "Netherite Sword"; domain = "weapon"; damage = "8"; speed = "1.6"; rarity = "epic"; reason = "Vanilla endgame weapon baseline" },
        @{ id = "minecraft:bow"; name = "Bow"; domain = "weapon"; damage = "projectile variable"; speed = ""; rarity = "common"; reason = "Baseline ranged weapon" },
        @{ id = "minecraft:crossbow"; name = "Crossbow"; domain = "weapon"; damage = "projectile variable"; speed = ""; rarity = "uncommon"; reason = "Baseline stronger ranged utility" },
        @{ id = "minecraft:trident"; name = "Trident"; domain = "weapon"; damage = "9 melee / 8 thrown"; speed = "1.1"; rarity = "rare"; reason = "Rare vanilla weapon drop" },
        @{ id = "minecraft:shield"; name = "Shield"; domain = "shield"; damage = "defensive"; speed = ""; rarity = "common"; reason = "Baseline defensive item" },
        @{ id = "minecraft:leather_helmet"; name = "Leather Helmet"; domain = "armor"; armor = "1"; toughness = "0"; rarity = "common"; reason = "Vanilla baseline armor" },
        @{ id = "minecraft:leather_chestplate"; name = "Leather Tunic"; domain = "armor"; armor = "3"; toughness = "0"; rarity = "common"; reason = "Vanilla baseline armor" },
        @{ id = "minecraft:leather_leggings"; name = "Leather Pants"; domain = "armor"; armor = "2"; toughness = "0"; rarity = "common"; reason = "Vanilla baseline armor" },
        @{ id = "minecraft:leather_boots"; name = "Leather Boots"; domain = "armor"; armor = "1"; toughness = "0"; rarity = "common"; reason = "Vanilla baseline armor" },
        @{ id = "minecraft:iron_helmet"; name = "Iron Helmet"; domain = "armor"; armor = "2"; toughness = "0"; rarity = "uncommon"; reason = "Standard early metal armor" },
        @{ id = "minecraft:iron_chestplate"; name = "Iron Chestplate"; domain = "armor"; armor = "6"; toughness = "0"; rarity = "uncommon"; reason = "Standard early metal armor" },
        @{ id = "minecraft:iron_leggings"; name = "Iron Leggings"; domain = "armor"; armor = "5"; toughness = "0"; rarity = "uncommon"; reason = "Standard early metal armor" },
        @{ id = "minecraft:iron_boots"; name = "Iron Boots"; domain = "armor"; armor = "2"; toughness = "0"; rarity = "uncommon"; reason = "Standard early metal armor" },
        @{ id = "minecraft:diamond_helmet"; name = "Diamond Helmet"; domain = "armor"; armor = "3"; toughness = "2"; rarity = "rare"; reason = "Vanilla high-tier armor" },
        @{ id = "minecraft:diamond_chestplate"; name = "Diamond Chestplate"; domain = "armor"; armor = "8"; toughness = "2"; rarity = "rare"; reason = "Vanilla high-tier armor" },
        @{ id = "minecraft:diamond_leggings"; name = "Diamond Leggings"; domain = "armor"; armor = "6"; toughness = "2"; rarity = "rare"; reason = "Vanilla high-tier armor" },
        @{ id = "minecraft:diamond_boots"; name = "Diamond Boots"; domain = "armor"; armor = "3"; toughness = "2"; rarity = "rare"; reason = "Vanilla high-tier armor" },
        @{ id = "minecraft:netherite_helmet"; name = "Netherite Helmet"; domain = "armor"; armor = "3"; toughness = "3"; rarity = "epic"; reason = "Vanilla endgame armor baseline" },
        @{ id = "minecraft:netherite_chestplate"; name = "Netherite Chestplate"; domain = "armor"; armor = "8"; toughness = "3"; rarity = "epic"; reason = "Vanilla endgame armor baseline" },
        @{ id = "minecraft:netherite_leggings"; name = "Netherite Leggings"; domain = "armor"; armor = "6"; toughness = "3"; rarity = "epic"; reason = "Vanilla endgame armor baseline" },
        @{ id = "minecraft:netherite_boots"; name = "Netherite Boots"; domain = "armor"; armor = "3"; toughness = "3"; rarity = "epic"; reason = "Vanilla endgame armor baseline" }
    )
    foreach ($entry in $vanilla) {
        $item = Get-OrCreateItem -Id $entry.id -Name $entry.name -Source "Minecraft"
        Add-SetValue $item "domains" $entry.domain
        Add-SetValue $item "evidence" "vanilla baseline"
        if ($entry.ContainsKey("damage")) { $item.damage = $entry.damage; $item.damage_status = "exact vanilla value or vanilla projectile variable" }
        if ($entry.ContainsKey("speed")) { $item.attack_speed = $entry.speed }
        if ($entry.ContainsKey("armor")) { $item.armor = $entry.armor }
        if ($entry.ContainsKey("toughness")) { $item.armor_toughness = $entry.toughness }
        $item.rarity = $entry.rarity
        $item.rarity_color = $rarityColors[$entry.rarity]
        $item.rarity_reason = $entry.reason
    }
}

function Classify-Item {
    param([hashtable]$Item)
    $id = $Item.id
    $name = $Item.name
    $haystack = "$id $name".ToLowerInvariant()
    $mod = $Item.mod_id
    $leaf = ($id -split ":", 2)[1]
    $hasTagEvidence = @($Item.evidence | Where-Object { $_ -like "item tag *" }).Count -gt 0
    $hasRealItemEvidence = $Item.evidence.Contains("lang item key") -or $Item.evidence.Contains("vanilla baseline") -or $Item.evidence.Contains("Better Combat weapon attributes") -or $hasTagEvidence
    $tokens = [System.Collections.Generic.HashSet[string]]::new()
    foreach ($token in ([regex]::Split("$leaf $name".ToLowerInvariant(), "[^a-z0-9]+"))) {
        if ($token) { [void]$tokens.Add($token) }
    }

    if ($leaf -match "spawn_egg") {
        Add-SetValue $Item "notes" "Spawn egg; not treated as gear for rarity borders."
        return
    }

    if ($leaf -match "/") {
        Add-SetValue $Item "notes" "Compatibility or submodel resource path; not treated as active player gear."
        return
    }

    if ($leaf -match '_(hand|model|inventory|blocking)$') {
        Add-SetValue $Item "notes" "Render/model variant; not treated as active player gear."
        return
    }

    if (-not $hasRealItemEvidence -and $Item.evidence.Contains("item model")) {
        Add-SetValue $Item "notes" "Render/model-only evidence; not treated as player gear until a lang key, tag, or config proves it is a real item."
        return
    }

    $utilityBlade = $false
    if ($haystack -match "knife" -and $mod -match "farmersdelight|alexsdelight|sliceanddice") {
        $utilityBlade = $true
        Add-SetValue $Item "domains" "utility"
        Add-SetValue $Item "notes" "Excluded from weapon rarity expectations because it is a cooking/processing knife."
    }

    $weaponTokens = @("sword", "blade", "dagger", "katana", "rapier", "spear", "glaive", "halberd", "scythe", "saber", "sabre", "cutlass", "claymore", "greataxe", "greathammer", "hammer", "mace", "staff", "wand", "bow", "crossbow", "trident", "lance", "cannon", "pistol", "blunderbuss", "gun", "chakram", "warglaive", "warblade", "axe", "flamberge", "athame", "incinerator", "ceraunus", "astrape", "mjolnir", "excalibur", "moonveil", "nightfall", "dragonbane", "spellbreaker", "truthseeker", "magehunter", "misery", "firebrand", "hellrazor", "bloodthirster", "dawnbreaker")
    $hasWeaponToken = $false
    foreach ($token in $weaponTokens) {
        if ($tokens.Contains($token)) {
            $hasWeaponToken = $true
            break
        }
    }
    if (-not $hasWeaponToken -and $leaf -match "greatsword|shortsword|longsword|twinblade|battleaxe|waraxe|sawblade|bowblade|netherite_sai|iron_sai|gold_sai|diamond_sai") {
        $hasWeaponToken = $true
    }

    if (-not $utilityBlade -and $hasWeaponToken -and $mod -ne "createbigcannons") {
        if ($haystack -notmatch "pickaxe|hoe|shovel|helmet|chestplate|leggings|boots|ingot|nugget|template|fragment|core|handle|hilt|blade_fragment") {
            if ($haystack -notmatch "spawn_egg|blocking|inventory|_hand$|_model$|glass|seed|sapling|grass|leaves|fur$|music_disc|banner_pattern|painting|statue") {
                Add-SetValue $Item "domains" "weapon"
            }
        }
    }

    if (-not $utilityBlade -and $Item.evidence.Contains("Better Combat weapon attributes")) {
        if ($haystack -notmatch "pickaxe|hoe|shovel|helmet|chestplate|leggings|boots|ingot|nugget|template|fragment|core|handle|hilt|blade_fragment") {
            Add-SetValue $Item "domains" "weapon"
        }
    }

    if ($haystack -match "shield|buckler|bulwark") {
        Add-SetValue $Item "domains" "shield"
        if ($Item.damage -eq "") { $Item.damage = "defensive"; $Item.damage_status = "shield/defensive item" }
    }

    if ($haystack -match "helmet|chestplate|leggings|boots|armor|robe|robes|hood|crown|mask|greaves|cuirass") {
        if ($haystack -notmatch "armor_trim|horse_armor|armor_stand|armor_pile") {
            Add-SetValue $Item "domains" "armor"
        }
    }

    if ($haystack -match "ring|amulet|necklace|belt|glove|gloves|gauntlet|charm|talisman|artifact|relic|cape|scarf|cloud_in_a_bottle|flippers|bunny_hoppers|antidote|bracelet|pendant|pouch|quiver|boots_of_speed|night_vision_goggles|kitty_slippers|plastic_drinking_hat") {
        Add-SetValue $Item "domains" "accessory_relic"
    }

    if ($haystack -match "spell_book|spellbook|scroll|manuscript|arcane|tome|codex|grimoire|necronomicon|staff|wand") {
        Add-SetValue $Item "domains" "magic_item"
    }
}

function Get-RarityForItem {
    param([hashtable]$Item)
    if ($Item.rarity) { return @($Item.rarity, $Item.rarity_reason) }
    $leaf = ($Item.id -split ":", 2)[1]
    $haystack = "$leaf $($Item.name)".ToLowerInvariant()
    $mod = $Item.mod_id
    $domains = @($Item.domains)
    $damageNumber = $null
    if ($Item.damage -match "^-?\d+(\.\d+)?$") {
        $damageNumber = [double]$Item.damage
    } elseif ($Item.damage -match "exact\s+(-?\d+(\.\d+)?)") {
        $damageNumber = [double]$Matches[1]
    }
    $maxMultiplier = $null
    if ($Item.max_damage_multiplier -match "^\d+(\.\d+)?$") {
        $maxMultiplier = [double]$Item.max_damage_multiplier
    }

    if ($domains -contains "weapon" -and $null -ne $damageNumber) {
        if ($damageNumber -ge 14) { return @("ascendant", "Exact/configured damage is realm-capstone tier.") }
        if ($damageNumber -ge 11) { return @("mythic", "Exact/configured damage is boss/dragon-tier.") }
        if ($damageNumber -ge 8) { return @("legendary", "Exact/configured damage is late-game or boss-adjacent.") }
        if ($damageNumber -ge 7) { return @("epic", "Exact/configured damage beats diamond baseline.") }
        if ($damageNumber -ge 6) { return @("rare", "Exact/configured damage is iron-to-diamond tier.") }
        if ($damageNumber -ge 4) { return @("uncommon", "Exact/configured damage is useful but early-tier.") }
        return @("common", "Exact/configured damage is baseline.")
    }

    if ($domains -contains "weapon" -and $null -ne $maxMultiplier) {
        if ($maxMultiplier -ge 1.5) { return @("legendary", "Better Combat combo multiplier marks this as heavy/chase combat gear.") }
        if ($maxMultiplier -ge 1.25) { return @("epic", "Better Combat combo multiplier marks this as advanced combat gear.") }
        if ($maxMultiplier -ge 1.1) { return @("rare", "Better Combat combo multiplier marks this as specialized combat gear.") }
    }

    if ($domains -contains "armor" -and $Item.armor -match "^\d+(\.\d+)?$") {
        $armor = [double]$Item.armor
        $toughness = if ($Item.armor_toughness -match "^\d+(\.\d+)?$") { [double]$Item.armor_toughness } else { 0.0 }
        if ($armor -ge 8 -and $toughness -ge 3) { return @("legendary", "Armor/toughness is stronger than diamond baseline.") }
        if ($armor -ge 6 -and $toughness -ge 2) { return @("epic", "Armor/toughness is high-tier.") }
        if ($armor -ge 3 -and $toughness -ge 2) { return @("rare", "Armor/toughness is diamond-tier.") }
        if ($armor -ge 2) { return @("uncommon", "Armor is practical early-to-mid gear.") }
        return @("common", "Armor is baseline.")
    }

    if ($haystack -match "ascendant|annihilator|the_incinerator|void_forge|infernal_forge|pure_moonlight|supernova|darkin|leviathan|frostmourne|master_sword|nights_edge") {
        return @("ascendant", "Named capstone/boss-tier identity.")
    }
    if ($haystack -match "dragonsteel|dragonbone|dragonbone|dragon_|dragon |soul_|soulreaper|withered|forlorn|moonlight|excalibur|mjolnir|dawnbreaker|skofnung|boss|legendary|mythic") {
        return @("mythic", "Dragon, boss, or Soulslike chase item.")
    }
    if ($haystack -match "netherite|ancient|runic|unique|artifact|relic|spellbreaker|magehunter|truthseeker|misery|firebrand|hellrazor|dragon|obsidian|wither|infernal|dead_king|necronomicon") {
        return @("legendary", "Late-game, unique, or major-system reward.")
    }
    if ($haystack -match "diamond|amethyst|mithril|druidic|frost|blaze|evoker|illusion|gold|rare|arcan|paladin|pyromancer|cryomancer|battlemage") {
        return @("epic", "High-tier material, spell-school, or rare loot identity.")
    }
    if ($haystack -match "iron|steel|silver|bronze|copper|uncommon|cultist|priest|plagued|rotten|villager") {
        return @("rare", "Mid-tier material or specialized role item.")
    }
    if ($domains -contains "weapon" -and $mod -eq "cataclysm") {
        return @("legendary", "Cataclysm combat gear is boss-system gear even when exact damage is not exposed.")
    }
    if ($domains -contains "weapon" -and $mod -eq "iceandfire") {
        return @("legendary", "Ice and Fire combat gear is dragon-system gear unless a stronger dragon material rule applies.")
    }
    if ($domains -contains "weapon" -and $mod -eq "born_in_chaos_v1") {
        return @("epic", "Born in Chaos combat gear is dangerous-world progression gear.")
    }
    if ($domains -contains "weapon" -and $mod -eq "block_factorys_bosses") {
        return @("mythic", "Bosses'Rise combat gear is boss-system gear.")
    }
    if ($domains -contains "accessory_relic") {
        return @("rare", "Relic/accessory item with likely gameplay utility.")
    }
    if ($domains -contains "magic_item") {
        return @("rare", "Magic item with progression utility.")
    }
    if ($domains -contains "shield") {
        return @("uncommon", "Defensive gear baseline unless material indicates higher rarity.")
    }
    if ($domains -contains "weapon" -or $domains -contains "armor") {
        return @("uncommon", "Combat gear without stronger exposed stat data.")
    }
    return @("common", "Baseline or utility item.")
}

function Get-RarityForSpell {
    param([hashtable]$Spell)
    $haystack = "$($Spell.id) $($Spell.name)".ToLowerInvariant()
    if ($haystack -match "portal|eldritch|black_hole|blood_step|raise_dead|summon_horse|summon_vex|dragon|planar|abyss|dead_king") {
        return @("legendary", "Major utility, summon, or high-impact spell.")
    }
    if ($haystack -match "fireball|fire_breath|ray|storm|chain|meteor|quake|fang|wisp|teleport|heal|wall|cloud|cone|slash") {
        return @("epic", "Combat-defining or strong utility spell.")
    }
    if ($haystack -match "missile|bolt|icicle|dash|shield|root|slow|poison|blood|electrocute") {
        return @("rare", "Practical combat spell.")
    }
    return @("uncommon", "Basic or utility spell.")
}

function Apply-SimplySwordsConfig {
    $configPath = Join-Path $ActiveConfigPath "simplyswords_main\weapon_attributes.json5"
    if (-not (Test-Path -LiteralPath $configPath)) { return }
    $data = Read-JsonLoose (Get-Content -LiteralPath $configPath -Raw)
    if ($null -eq $data) { return }
    $map = Get-JsonPropertyMap $data
    $types = @("longsword", "twinblade", "rapier", "katana", "sai", "spear", "glaive", "warglaive", "cutlass", "claymore", "greataxe", "greathammer", "chakram", "scythe", "halberd")
    foreach ($item in $items.Values) {
        if ($item.mod_id -ne "simplyswords") { continue }
        $leaf = ($item.id -split ":", 2)[1]
        $directKey = "${leaf}_damageModifier"
        if ($map.ContainsKey($directKey)) {
            $item.damage = "config modifier +$($map[$directKey])"
            $item.damage_status = "Simply Swords config modifier; final display adds the mod item base"
            Add-SetValue $item "domains" "weapon"
            Add-SetValue $item "evidence" "simplyswords_main/weapon_attributes.json5"
        }
        $speedKey = "${leaf}_attackSpeed"
        if ($map.ContainsKey($speedKey)) {
            $item.attack_speed = "$($map[$speedKey]) modifier"
        }
        foreach ($type in $types) {
            if ($leaf.EndsWith("_$type")) {
                $material = $leaf.Substring(0, $leaf.Length - $type.Length - 1)
                $materialKey = "${material}_damageModifier"
                $positiveKey = "${type}_positiveDamageModifier"
                $negativeKey = "${type}_negativeDamageModifier"
                $speedTypeKey = "${type}_attackSpeed"
                $total = 0.0
                $found = $false
                foreach ($key in @($materialKey, $positiveKey)) {
                    if ($map.ContainsKey($key)) {
                        $total += [double]$map[$key]
                        $found = $true
                    }
                }
                if ($map.ContainsKey($negativeKey)) {
                    $total -= [double]$map[$negativeKey]
                    $found = $true
                }
                if ($found -and -not $item.damage) {
                    $item.damage = "config modifier +$total"
                    $item.damage_status = "Simply Swords material/type modifier; final display adds the item base"
                    Add-SetValue $item "domains" "weapon"
                    Add-SetValue $item "evidence" "simplyswords_main/weapon_attributes.json5"
                }
                if ($map.ContainsKey($speedTypeKey) -and -not $item.attack_speed) {
                    $item.attack_speed = "$($map[$speedTypeKey]) modifier"
                }
            }
        }
    }
}

function Apply-SoulsWeaponsConfig {
    $configPath = Join-Path $Root "config\soulsweapons\soulsweapons.json"
    if (-not (Test-Path -LiteralPath $configPath)) {
        $configPath = Join-Path $ActiveConfigPath "soulsweapons\soulsweapons.json"
    }
    if (-not (Test-Path -LiteralPath $configPath)) { return }
    $data = Read-JsonLoose (Get-Content -LiteralPath $configPath -Raw)
    if ($null -eq $data) { return }
    $map = Get-JsonPropertyMap $data
    foreach ($prop in $map.Keys) {
        if ($prop -match "^(.+?)_damage$" -and $prop -notmatch "ability|projectile|bonus|self|bleed|fall|shockwave|lightning|fire|fog|heal|per_level|modifier") {
            $leaf = $Matches[1]
            $id = "soulsweapons:$leaf"
            if ($items.ContainsKey($id)) {
                $items[$id].damage = "$($map[$prop])"
                $items[$id].damage_status = "exact Marium's Soulslike Weaponry config damage"
                Add-SetValue $items[$id] "domains" "weapon"
                Add-SetValue $items[$id] "evidence" "soulsweapons/soulsweapons.json"
            }
        }
        if ($prop -match "^(.+?)_normal_damage$") {
            $leaf = $Matches[1]
            $id = "soulsweapons:$leaf"
            if ($items.ContainsKey($id)) {
                $items[$id].damage = "$($map[$prop])"
                $items[$id].damage_status = "exact Marium's Soulslike Weaponry normal config damage"
                Add-SetValue $items[$id] "domains" "weapon"
                Add-SetValue $items[$id] "evidence" "soulsweapons/soulsweapons.json"
            }
        }
        if ($prop -match "^(.+?)_attack_speed$") {
            $leaf = $Matches[1]
            $id = "soulsweapons:$leaf"
            if ($items.ContainsKey($id)) {
                $items[$id].attack_speed = "$($map[$prop])"
            }
        }
    }
}

function Apply-FantasyArmorConfig {
    $configPath = Join-Path $ActiveConfigPath "fantasy_armor-armor_attributes.toml"
    if (-not (Test-Path -LiteralPath $configPath)) { return }
    $currentSet = ""
    $currentPiece = ""
    foreach ($line in Get-Content -LiteralPath $configPath) {
        if ($line -match '^\s*\["Armor Attributes"\.([a-z0-9_]+)\.([a-z0-9_]+)\]\s*$') {
            $currentSet = $Matches[1]
            $currentPiece = $Matches[2]
            continue
        }
        if (-not $currentSet -or -not $currentPiece) { continue }
        $id = "fantasy_armor:${currentSet}_${currentPiece}"
        if (-not $items.ContainsKey($id)) { continue }
        if ($line -match '^\s*armor\s*=\s*([0-9.]+)') { $items[$id].armor = $Matches[1]; Add-SetValue $items[$id] "evidence" "fantasy_armor-armor_attributes.toml" }
        if ($line -match '^\s*armorToughness\s*=\s*([0-9.]+)') { $items[$id].armor_toughness = $Matches[1] }
        if ($line -match '^\s*durability\s*=\s*([0-9.]+)') { $items[$id].durability = $Matches[1] }
    }
}

function Apply-SpartanShieldConfig {
    $configPath = Join-Path $ActiveConfigPath "spartanshields-common.toml"
    if (-not (Test-Path -LiteralPath $configPath)) { return }
    $section = ""
    foreach ($line in Get-Content -LiteralPath $configPath) {
        if ($line -match '^\s*\[[^\]]+\.([a-z0-9_]+)\]\s*$') {
            $section = $Matches[1]
            continue
        }
        if ($section -and $line -match '^\s*durability\s*=\s*([0-9.]+)') {
            foreach ($prefix in @("shield", "tower_shield")) {
                foreach ($candidate in @("spartanshields:${section}_${prefix}", "spartanshields:${prefix}_${section}")) {
                    if ($items.ContainsKey($candidate)) {
                        $items[$candidate].durability = $Matches[1]
                        Add-SetValue $items[$candidate] "evidence" "spartanshields-common.toml"
                    }
                }
            }
        }
    }
}

function Scan-Jar {
    param([System.IO.FileInfo]$Jar)
    $zip = [System.IO.Compression.ZipFile]::OpenRead($Jar.FullName)
    try {
        $jarName = $Jar.Name
        $localModNames = @{}
        foreach ($entry in $zip.Entries) {
            if ($entry.FullName -eq "META-INF/mods.toml") {
                $toml = Read-ZipText -Zip $zip -Entry $entry
                $display = Get-ModNameFromToml -Text $toml -Fallback $Jar.BaseName
                if ($toml -match '(?m)^\s*modId\s*=\s*"([^"]+)"') {
                    $localModNames[$Matches[1]] = $display
                    $sourceMods[$Matches[1]] = $display
                }
            }
        }

        foreach ($entry in $zip.Entries) {
            $full = $entry.FullName
            if ($full -match '^assets/([^/]+)/lang/en_us\.json$') {
                $modId = $Matches[1]
                $source = if ($sourceMods.ContainsKey($modId)) { $sourceMods[$modId] } else { $modId }
                $json = Read-JsonLoose (Read-ZipText -Zip $zip -Entry $entry)
                if ($null -eq $json) { continue }
                foreach ($prop in $json.PSObject.Properties) {
                    $key = $prop.Name
                    $value = [string]$prop.Value
                    if ($key -match '^item\.([a-z0-9_.-]+)\.([a-z0-9_./-]+)$') {
                        if ($Matches[1] -ne $modId) { continue }
                        $item = Get-OrCreateItem -Id "$($Matches[1]):$($Matches[2])" -Name $value -Source $source -Jar $jarName
                        if ($item) { Add-SetValue $item "evidence" "lang item key" }
                    } elseif ($key -match '^spell\.([a-z0-9_.-]+)\.([a-z0-9_./-]+)$') {
                        if ($Matches[1] -ne $modId) { continue }
                        Add-Spell -Id "$($Matches[1]):$($Matches[2])" -Name $value -Source $source
                    }
                }
            } elseif ($full -match '^assets/([^/]+)/models/item/([^/.]+)\.json$') {
                $modId = $Matches[1]
                $leaf = $Matches[2]
                $source = if ($sourceMods.ContainsKey($modId)) { $sourceMods[$modId] } else { $modId }
                $item = Get-OrCreateItem -Id "${modId}:${leaf}" -Source $source -Jar $jarName
                if ($item) { Add-SetValue $item "evidence" "item model" }
            } elseif ($full -match '^data/([^/]+)/tags/items/(.+)\.json$') {
                $tag = "$($Matches[1]):$($Matches[2])"
                $json = Read-JsonLoose (Read-ZipText -Zip $zip -Entry $entry)
                if ($null -eq $json -or $null -eq $json.values) { continue }
                foreach ($value in @($json.values)) {
                    $id = ""
                    if ($value -is [string]) {
                        $id = $value
                    } elseif ($value.PSObject.Properties["id"]) {
                        $id = [string]$value.id
                    }
                    if (-not $id -or $id.StartsWith("#") -or $id -notmatch ":") { continue }
                    $item = Get-OrCreateItem -Id $id
                    if ($item) {
                        Add-SetValue $item "tags" $tag
                        Add-SetValue $item "evidence" "item tag $tag"
                    }
                }
            } elseif ($full -match '^data/([^/]+)/weapon_attributes/([^/.]+)\.json$') {
                $modId = $Matches[1]
                $leaf = $Matches[2]
                $json = Read-JsonLoose (Read-ZipText -Zip $zip -Entry $entry)
                if ($null -eq $json -or -not $json.PSObject.Properties["attributes"] -or $null -eq $json.attributes) { continue }
                $attr = $json.attributes
                $maxMult = ""
                if ($attr.PSObject.Properties["attacks"] -and $attr.attacks) {
                    $multipliers = @($attr.attacks | ForEach-Object {
                        if ($_.PSObject.Properties["damage_multiplier"]) { [double]$_.damage_multiplier }
                    })
                    if ($multipliers.Count -gt 0) { $maxMult = ($multipliers | Measure-Object -Maximum).Maximum }
                }
                $weaponAttributes["${modId}:${leaf}"] = [ordered]@{
                    category = $(if ($attr.PSObject.Properties["category"]) { [string]$attr.category } else { "" })
                    attack_range = $(if ($attr.PSObject.Properties["attack_range"]) { [string]$attr.attack_range } else { "" })
                    max_damage_multiplier = "$maxMult"
                    source = $full
                }
                if ($modId -notin @("bettercombat", "minecraft")) {
                    $item = Get-OrCreateItem -Id "${modId}:${leaf}" -Jar $jarName
                    if ($item) {
                        Add-SetValue $item "domains" "weapon"
                        Add-SetValue $item "evidence" "Better Combat weapon attributes"
                    }
                }
            }
        }
    } finally {
        $zip.Dispose()
    }
}

if (-not (Test-Path -LiteralPath $ModsPath)) {
    throw "ModsPath does not exist: $ModsPath"
}

Add-VanillaItems

$allowedJarNames = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
Get-ChildItem -LiteralPath (Join-Path $Root "mods") -Filter "*.pw.toml" -File | ForEach-Object {
    $text = Get-Content -LiteralPath $_.FullName -Raw
    if ($text -match '(?m)^filename\s*=\s*"([^"]+\.jar)"') {
        [void]$allowedJarNames.Add($Matches[1])
    }
}
if ($allowedJarNames.Count -eq 0) {
    throw "No Packwiz jar filenames were found in mods/*.pw.toml"
}

$missingActiveJars = @()
foreach ($jarName in $allowedJarNames) {
    if (-not (Test-Path -LiteralPath (Join-Path $ModsPath $jarName))) {
        $missingActiveJars += $jarName
    }
}

Get-ChildItem -LiteralPath $ModsPath -Filter "*.jar" -File |
    Where-Object { $allowedJarNames.Contains($_.Name) } |
    Sort-Object Name |
    ForEach-Object {
    Scan-Jar -Jar $_
}

foreach ($item in $items.Values) {
    Classify-Item -Item $item
}

foreach ($id in $weaponAttributes.Keys) {
    if ($items.ContainsKey($id)) {
        $attr = $weaponAttributes[$id]
        $items[$id].better_combat_category = $attr.category
        $items[$id].attack_range = $attr.attack_range
        $items[$id].max_damage_multiplier = $attr.max_damage_multiplier
        Add-SetValue $items[$id] "evidence" $attr.source
        if (-not $items[$id].damage -and $attr.max_damage_multiplier) {
            $items[$id].damage = "Better Combat max multiplier $($attr.max_damage_multiplier)x"
            $items[$id].damage_status = "base attack damage is hardcoded or inherited; multiplier exact from weapon_attributes"
        }
    }
}

Apply-SimplySwordsConfig
Apply-SoulsWeaponsConfig
Apply-FantasyArmorConfig
Apply-SpartanShieldConfig

foreach ($item in $items.Values) {
    $leaf = ($item.id -split ":", 2)[1]
    if ($leaf -match "spawn_egg") {
        Add-SetValue $item "notes" "Spawn egg; not treated as gear for rarity borders."
        $item.domains.Clear()
        continue
    }
    if ($leaf -match "/") {
        Add-SetValue $item "notes" "Compatibility or submodel resource path; not treated as active player gear."
        $item.domains.Clear()
        continue
    }
    if ($leaf -match '_(hand|model|inventory|blocking)$') {
        Add-SetValue $item "notes" "Render/model variant; not treated as active player gear."
        $item.domains.Clear()
        continue
    }
    if ($item.mod_id -eq "createbigcannons" -and $item.domains.Contains("weapon")) {
        [void]$item.domains.Remove("weapon")
        Add-SetValue $item "notes" "Create Big Cannons machinery/ammunition is not treated as personal weapon gear for rarity borders."
    }
}

foreach ($item in $items.Values) {
    $rarity = Get-RarityForItem -Item $item
    $item.rarity = $rarity[0]
    $item.rarity_color = $rarityColors[$item.rarity]
    $item.rarity_reason = $rarity[1]
}

foreach ($spell in $spells.Values) {
    $rarity = Get-RarityForSpell -Spell $spell
    $spell.rarity = $rarity[0]
    $spell.rarity_color = $rarityColors[$spell.rarity]
    $spell.rarity_reason = $rarity[1]
}

function Convert-SetToArray {
    param($Set)
    if ($null -eq $Set) { return @() }
    return @($Set | Sort-Object)
}

function To-RegistryObject {
    param([hashtable]$Item)
    [ordered]@{
        id = $Item.id
        name = $Item.name
        mod_id = $Item.mod_id
        source_mod = $Item.source_mod
        domains = Convert-SetToArray $Item.domains
        rarity = $Item.rarity
        rarity_color = $Item.rarity_color
        rarity_reason = $Item.rarity_reason
        damage = $Item.damage
        damage_status = $Item.damage_status
        attack_speed = $Item.attack_speed
        armor = $Item.armor
        armor_toughness = $Item.armor_toughness
        durability = $Item.durability
        better_combat_category = $Item.better_combat_category
        attack_range = $Item.attack_range
        max_damage_multiplier = $Item.max_damage_multiplier
        tags = Convert-SetToArray $Item.tags
        evidence = Convert-SetToArray $Item.evidence
        notes = Convert-SetToArray $Item.notes
    }
}

function Shorten-TooltipText {
    param(
        [string]$Text,
        [int]$Max = 130
    )
    if (-not $Text) { return "" }
    $clean = (($Text -replace "\s+", " ").Trim())
    if ($clean.Length -le $Max) { return $clean }
    return $clean.Substring(0, $Max - 3).TrimEnd() + "..."
}

function Get-TooltipDomainLabel {
    param([hashtable]$Item)
    $domains = @(Convert-SetToArray $Item.domains)
    if ($domains -contains "weapon") { return "Weapon" }
    if ($domains -contains "armor") { return "Armor" }
    if ($domains -contains "shield") { return "Shield" }
    if ($domains -contains "magic_item") { return "Magic" }
    if ($domains -contains "accessory_relic") { return "Accessory" }
    return "Gear"
}

function Add-TooltipPart {
    param(
        [System.Collections.Generic.List[string]]$Parts,
        [string]$Label,
        [string]$Value
    )
    if ($Value -and $Value.Trim().Length -gt 0) {
        $Parts.Add("${Label}: $($Value.Trim())")
    }
}

function Get-TooltipEffectLine {
    param([hashtable]$Item)
    $domain = Get-TooltipDomainLabel $Item
    $parts = New-Object System.Collections.Generic.List[string]

    if ($domain -eq "Weapon") {
        Add-TooltipPart $parts "Damage" $Item.damage
        Add-TooltipPart $parts "Speed" $Item.attack_speed
        Add-TooltipPart $parts "Combat" $Item.better_combat_category
        Add-TooltipPart $parts "Range" $Item.attack_range
        Add-TooltipPart $parts "Max" $Item.max_damage_multiplier
        if ($parts.Count -eq 0 -and $Item.damage_status) {
            Add-TooltipPart $parts "Damage" $Item.damage_status
        }
        if ($parts.Count -eq 0) {
            $parts.Add("Combat stats are supplied by the item's native attribute tooltip.")
        }
    } elseif ($domain -eq "Armor") {
        Add-TooltipPart $parts "Armor" $Item.armor
        Add-TooltipPart $parts "Toughness" $Item.armor_toughness
        Add-TooltipPart $parts "Durability" $Item.durability
        if ($parts.Count -eq 0) {
            $parts.Add("Armor stats are supplied by the item's native equipment tooltip.")
        }
    } elseif ($domain -eq "Shield") {
        Add-TooltipPart $parts "Block" "defensive off-hand gear"
        Add-TooltipPart $parts "Durability" $Item.durability
    } elseif ($domain -eq "Magic") {
        Add-TooltipPart $parts "Magic" $Item.damage
        if ($parts.Count -eq 0 -and $Item.damage_status) {
            Add-TooltipPart $parts "Scaling" $Item.damage_status
        }
        if ($parts.Count -eq 0) {
            $parts.Add("Magic item; exact spell behavior is shown by the mod tooltip or spell book.")
        }
    } elseif ($domain -eq "Accessory") {
        $parts.Add("Relic/accessory gear; equip effect is shown by the mod tooltip or Curios slot behavior.")
    } else {
        $parts.Add("Indexed gear in the Ascendant rarity registry.")
    }

    return "Effect: " + (Shorten-TooltipText (($parts.ToArray()) -join "; ") 150)
}

function Get-RarityTooltipLabel {
    param([string]$Rarity)
    switch ($Rarity) {
        "legendary" { return "LEGENDARY" }
        "mythic" { return "MYTHIC" }
        "ascendant" { return "ASCENDANT" }
        default { return $rarityLabels[$Rarity] }
    }
}

function Get-RarityTooltipAura {
    param([string]$Rarity)
    return ""
}

$allGear = @($items.Values | Where-Object { $_.domains.Count -gt 0 } | Sort-Object @{Expression = { $_.mod_id }}, @{Expression = { $_.id }})
$weapons = @($allGear | Where-Object { $_.domains.Contains("weapon") })
$armor = @($allGear | Where-Object { $_.domains.Contains("armor") })
$shields = @($allGear | Where-Object { $_.domains.Contains("shield") })
$magicItems = @($allGear | Where-Object { $_.domains.Contains("magic_item") })
$accessories = @($allGear | Where-Object { $_.domains.Contains("accessory_relic") })
$utility = @($allGear | Where-Object { $_.domains.Contains("utility") })

function MdCell {
    param([string]$Value)
    if ($null -eq $Value -or $Value -eq "") { return " " }
    return (($Value -replace "\|", "\\|") -replace "`r?`n", " ").Trim()
}

function Write-ItemIndex {
    param(
        [string]$Path,
        [string]$Title,
        [array]$Rows,
        [string]$DomainNote,
        [string[]]$Columns
    )
    $lines = @(
        "# $Title",
        "",
        "Generated by `scripts/generate-gear-rarity-index.ps1`.",
        "",
        $DomainNote,
        "",
        "Rarity colors are the Ascendant Realms manual Item Borders colors, not the item display-name color.",
        "",
        "| Rarity | Color |",
        "|---|---|"
    )
    foreach ($tier in $rarityOrder) {
        $lines += "| $($rarityLabels[$tier]) | " + ([char]96 + $rarityColors[$tier] + [char]96) + " |"
    }
    $headerLine = "| " + ($Columns -join " | ") + " |"
    $separatorLine = "| " + (($Columns | ForEach-Object { "---" }) -join " | ") + " |"
    $lines += @(
        "",
        "## Index",
        "",
        $headerLine,
        $separatorLine
    )
    foreach ($row in $Rows) {
        $values = foreach ($column in $Columns) {
            switch ($column) {
                "Item ID" { ([char]96 + $row.id + [char]96) }
                "Spell ID" { ([char]96 + $row.id + [char]96) }
                "Name" { MdCell $row.name }
                "Mod" { MdCell $row.source_mod }
                "Rarity" { MdCell $rarityLabels[$row.rarity] }
                "Color" { ([char]96 + $row.rarity_color + [char]96) }
                "Damage / Effect" { MdCell $row.damage }
                "Damage Status" { MdCell $row.damage_status }
                "Attack Speed" { MdCell $row.attack_speed }
                "Armor" { MdCell $row.armor }
                "Toughness" { MdCell $row.armor_toughness }
                "Durability" { MdCell $row.durability }
                "Better Combat" {
                    $pieces = @()
                    if ($row.better_combat_category) { $pieces += "category $($row.better_combat_category)" }
                    if ($row.attack_range) { $pieces += "range $($row.attack_range)" }
                    if ($row.max_damage_multiplier) { $pieces += "max $($row.max_damage_multiplier)x" }
                    MdCell ($pieces -join "; ")
                }
                "Reason" { MdCell $row.rarity_reason }
                "Notes" { MdCell ((Convert-SetToArray $row.notes) -join "; ") }
                default { " " }
            }
        }
        $lines += "| " + ($values -join " | ") + " |"
    }
    Write-Utf8NoBom -Path $Path -Value ($lines -join "`n")
}

Write-ItemIndex -Path (Join-Path $DocsDir "WEAPON_INDEX.md") -Title "Weapon Index" -Rows $weapons -DomainNote "This is the full scanned weapon registry from the active Ascendant Realms client instance plus vanilla baselines. Farmer's Delight/Alex's Delight cooking knives are excluded into utility notes instead of treated as combat weapons." -Columns @("Item ID", "Name", "Mod", "Rarity", "Color", "Damage / Effect", "Damage Status", "Attack Speed", "Better Combat", "Reason", "Notes")
Write-ItemIndex -Path (Join-Path $DocsDir "ARMOR_INDEX.md") -Title "Armor Index" -Rows $armor -DomainNote "This index covers wearable armor and armor-like gear. Exact armor/toughness is filled where vanilla or scanned config exposes it." -Columns @("Item ID", "Name", "Mod", "Rarity", "Color", "Armor", "Toughness", "Durability", "Reason", "Notes")
Write-ItemIndex -Path (Join-Path $DocsDir "SHIELD_INDEX.md") -Title "Shield Index" -Rows $shields -DomainNote "This index covers shields, bucklers, bulwarks, and defensive off-hand gear." -Columns @("Item ID", "Name", "Mod", "Rarity", "Color", "Damage / Effect", "Durability", "Reason", "Notes")
Write-ItemIndex -Path (Join-Path $DocsDir "MAGIC_INDEX.md") -Title "Magic And Spell Index" -Rows (@($magicItems) + @($spells.Values | Sort-Object id)) -DomainNote "This index covers spell books, scroll-like magic items, magic weapons, and Iron's Spells spell IDs. Spell damage varies by spell level and config, so spell rows track rarity/effect tier rather than melee attack damage." -Columns @("Spell ID", "Name", "Mod", "Rarity", "Color", "Damage / Effect", "Damage Status", "Reason", "Notes")
Write-ItemIndex -Path (Join-Path $DocsDir "ACCESSORY_RELIC_INDEX.md") -Title "Accessory And Relic Index" -Rows $accessories -DomainNote "This index covers Artifacts, curios-style gear, talismans, rings, charms, relics, and other non-armor wearable power items." -Columns @("Item ID", "Name", "Mod", "Rarity", "Color", "Damage / Effect", "Damage Status", "Reason", "Notes")

$registry = [ordered]@{
    version = 1
    generated_at = (Get-Date).ToString("o")
    source_mods_path = $ModsPath
    source_config_path = $ActiveConfigPath
    scanned_packwiz_jars = $allowedJarNames.Count
    missing_active_packwiz_jars = @($missingActiveJars | Sort-Object)
    rarity_tiers = foreach ($tier in $rarityOrder) {
        [ordered]@{ id = $tier; label = $rarityLabels[$tier]; color = $rarityColors[$tier] }
    }
    counts = [ordered]@{
        weapons = $weapons.Count
        armor = $armor.Count
        shields = $shields.Count
        magic_items = $magicItems.Count
        spells = $spells.Count
        accessories_relics = $accessories.Count
        utility_excluded = $utility.Count
        total_indexed_gear = $allGear.Count
    }
    weapons = @($weapons | ForEach-Object { To-RegistryObject $_ })
    armor = @($armor | ForEach-Object { To-RegistryObject $_ })
    shields = @($shields | ForEach-Object { To-RegistryObject $_ })
    magic_items = @($magicItems | ForEach-Object { To-RegistryObject $_ })
    spells = @($spells.Values | Sort-Object id | ForEach-Object {
        [ordered]@{
            id = $_.id
            name = $_.name
            source_mod = $_.source_mod
            domain = $_.domain
            rarity = $_.rarity
            rarity_color = $_.rarity_color
            rarity_reason = $_.rarity_reason
            damage = $_.damage
            damage_status = $_.damage_status
            notes = Convert-SetToArray $_.notes
        }
    })
    accessories_relics = @($accessories | ForEach-Object { To-RegistryObject $_ })
    utility_excluded = @($utility | ForEach-Object { To-RegistryObject $_ })
}

$registryPath = Join-Path $IndexDir "gear_registry.json"
Write-Utf8NoBom -Path $registryPath -Value ($registry | ConvertTo-Json -Depth 20)

$borderGroups = [ordered]@{}
foreach ($tier in $rarityOrder) {
    $borderGroups[$rarityColors[$tier]] = New-Object System.Collections.Generic.List[string]
}
foreach ($item in $allGear) {
    if ($item.domains.Contains("utility")) { continue }
    $color = $rarityColors[$item.rarity]
    if ($borderGroups.Contains($color)) {
        $borderGroups[$color].Add($item.id)
    }
}

function TomlQuote {
    param([string]$Value)
    '"' + ($Value -replace '\\', '\\' -replace '"', '\"') + '"'
}

function JsQuote {
    param([string]$Value)
    return ($Value | ConvertTo-Json -Compress)
}

$manualParts = @()
foreach ($color in $borderGroups.Keys) {
    $ids = @($borderGroups[$color] | Sort-Object -Unique)
    if ($ids.Count -eq 0) { continue }
    $manualParts += "$(TomlQuote $color) = [$(($ids | ForEach-Object { TomlQuote $_ }) -join ", ")]"
}
$manualBordersLine = "		manual_borders = {$($manualParts -join ', ')}"

$itemBordersLines = @(
    "# Ascendant Realms generated Item Borders config.",
    "# Generated by scripts/generate-gear-rarity-index.ps1.",
    "# Manual borders are keyed by exact item ID so border color follows assigned rarity, not display-name color.",
    "",
    "[client]",
    "",
    "	[client.options]",
    "		hotbar = true",
    "		show_for_common = false",
    "		square_corners = true",
    "		full_border = false",
    "		over_items = false",
    "		extra_glow = true",
    "		auto_borders = false",
    "		legendary_tooltips_sync = false",
    $manualBordersLine
)
Write-Utf8NoBom -Path $ItemBordersPath -Value ($itemBordersLines -join "`n")

$tooltipById = [ordered]@{}
foreach ($item in $allGear) {
    if ($item.domains.Contains("utility")) { continue }
    if ($tooltipById.Contains($item.id)) { continue }
    $tooltipById[$item.id] = [ordered]@{
        label = Get-RarityTooltipLabel $item.rarity
        rarity = $item.rarity
        color = [Convert]::ToInt32($item.rarity_color.TrimStart("#"), 16)
        bold = $item.rarity -in @("legendary", "mythic", "ascendant")
    }
}

$tooltipJson = $tooltipById | ConvertTo-Json -Depth 10
$tooltipRegistrations = @()
foreach ($id in $tooltipById.Keys) {
    $quotedId = JsQuote $id
    $tooltipRegistrations += "  event.addAdvanced($quotedId, (item, advanced, text) => insertAscendantRarityLine(text, buildAscendantRarityLines(ASCENDANT_RARITY_TOOLTIPS[$quotedId])))"
}
$tooltipLines = @(
    "// Ascendant Realms generated rarity tooltips.",
    "// Generated by scripts/generate-gear-rarity-index.ps1.",
    "// Legendary Tooltips styles the tooltip frame; this script inserts only the player-facing rarity label.",
    "",
    "const ASCENDANT_RARITY_TOOLTIPS = $tooltipJson",
    "",
    "function buildAscendantRarityLines(data) {",
    "    let rarityLine = Text.of(data.label).color(data.color)",
    "    if (data.bold) {",
    "      rarityLine = rarityLine.bold(true)",
    "    }",
    "    return rarityLine",
    "}",
    "",
    "function ascendantTooltipLineText(line) {",
    "    if (line == null) {",
    "      return ''",
    "    }",
    "    if (typeof line.getString === 'function') {",
    "      return String(line.getString()).toLowerCase()",
    "    }",
    "    if (typeof line.getText === 'function') {",
    "      return String(line.getText()).toLowerCase()",
    "    }",
    "    if (typeof line.string === 'string') {",
    "      return line.string.toLowerCase()",
    "    }",
    "    return String(line).toLowerCase()",
    "}",
    "",
    "function ascendantTooltipSize(text) {",
    "    return typeof text.size === 'function' ? text.size() : text.length",
    "}",
    "",
    "function ascendantTooltipGet(text, index) {",
    "    return typeof text.get === 'function' ? text.get(index) : text[index]",
    "}",
    "",
    "function ascendantTooltipAdd(text, index, line) {",
    "    if (typeof text.add === 'function') {",
    "      text.add(index, line)",
    "    } else {",
    "      text.splice(index, 0, line)",
    "    }",
    "}",
    "",
    "function findAscendantRarityInsertIndex(text) {",
    "    var behaviorAnchors = [",
    "      'attack range',",
    "      'attack_range',",
    "      ' range',",
    "      'right click',",
    "      'hold right click',",
    "      'when released',",
    "      'warning',",
    "      'charge',",
    "      'summons',",
    "      'chance',",
    "      'cooldown',",
    "      'mana cost',",
    "      'spell power'",
    "    ]",
    "    var statAnchors = [",
    "      'attack damage',",
    "      'attack_damage',",
    "      'attack speed',",
    "      'attack_speed',",
    "      'armor toughness',",
    "      'armor_toughness',",
    "      'knockback resistance',",
    "      'knockback_resistance',",
    "      'armor'",
    "    ]",
    "    var lastStatIndex = -1",
    "    var tooltipSize = ascendantTooltipSize(text)",
    "    for (var scanIndex = 1; scanIndex < tooltipSize; scanIndex++) {",
    "      var scannedLine = ascendantTooltipLineText(ascendantTooltipGet(text, scanIndex))",
    "      if (behaviorAnchors.some(anchor => scannedLine.includes(anchor))) {",
    "        return scanIndex",
    "      }",
    "      if (statAnchors.some(anchor => scannedLine.includes(anchor))) {",
    "        lastStatIndex = scanIndex",
    "      }",
    "    }",
    "    if (lastStatIndex >= 0) {",
    "      return Math.min(tooltipSize, lastStatIndex + 1)",
    "    }",
    "    return Math.min(tooltipSize, 2)",
    "}",
    "",
    "function insertAscendantRarityLine(text, rarityLine) {",
    "    var rarityLabels = ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic', 'ascendant']",
    "    var tooltipSize = ascendantTooltipSize(text)",
    "    for (var existingIndex = 1; existingIndex < tooltipSize; existingIndex++) {",
    "      var existingLine = ascendantTooltipLineText(ascendantTooltipGet(text, existingIndex))",
    "      if (rarityLabels.some(label => existingLine === label || existingLine.includes('literal{' + label + '}'))) {",
    "        return",
    "      }",
    "    }",
    "    ascendantTooltipAdd(text, findAscendantRarityInsertIndex(text), rarityLine)",
    "}",
    "",
    "ItemEvents.tooltip(event => {"
) + $tooltipRegistrations + @(
    "})"
)
Write-Utf8NoBom -Path $KubeJsTooltipPath -Value ($tooltipLines -join "`n")

$rarityMetadata = [ordered]@{
    generatedAt = (Get-Date).ToString("o")
    registry = "config/ascendant_index/gear_registry.json"
    itemBorders = "config/itemborders-common.toml"
    reason = "Startup item rarity mutation is disabled because some custom mod item classes do not expose a writable rarity field."
    counts = $registry.counts
}
$metadataCommentLines = ($rarityMetadata | ConvertTo-Json -Depth 8) -split "`r?`n" | ForEach-Object { "// $_" }

$kubeLines = @(
    "// Ascendant Realms generated gear rarity metadata.",
    "// This file is intentionally no-op at startup.",
    "// Item Borders manual_borders is the authoritative visual rarity system.",
    "// Do not set item.rarity here; Iron's Spells InkItem and other custom item classes can crash KubeJS/Rhino.",
    ""
) + $metadataCommentLines
Write-Utf8NoBom -Path $KubeJsPath -Value ($kubeLines -join "`n")

Write-Host "Generated gear registry:"
Write-Host " - Weapons: $($weapons.Count)"
Write-Host " - Armor: $($armor.Count)"
Write-Host " - Shields: $($shields.Count)"
Write-Host " - Magic items: $($magicItems.Count)"
Write-Host " - Spells: $($spells.Count)"
Write-Host " - Accessories/relics: $($accessories.Count)"
Write-Host " - Utility excluded: $($utility.Count)"
Write-Host " - Registry: $registryPath"
Write-Host " - Item Borders: $ItemBordersPath"
Write-Host " - KubeJS rarity script: $KubeJsPath"
Write-Host " - KubeJS tooltip script: $KubeJsTooltipPath"
