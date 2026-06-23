param(
    [Parameter(Mandatory = $true)]
    [Alias("ActiveClientModsPath")]
    [string]$ClientModsPath,

    [Parameter(Mandatory = $true)]
    [string]$ServerFolder,

    [switch]$Clean
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$clientMods = [System.IO.Path]::GetFullPath($ClientModsPath)
$serverRoot = [System.IO.Path]::GetFullPath($ServerFolder)
$serverMods = Join-Path $serverRoot "mods"

if (-not (Test-Path -LiteralPath $clientMods)) {
    throw "ClientModsPath does not exist: $clientMods"
}

New-Item -ItemType Directory -Force -Path $serverMods | Out-Null

Get-ChildItem -LiteralPath $serverMods -Filter "*.pw.toml" -File -ErrorAction SilentlyContinue |
    Remove-Item -Force

if ($Clean) {
    Get-ChildItem -LiteralPath $serverMods -Filter "*.jar" -File -ErrorAction SilentlyContinue |
        Remove-Item -Force
}

function New-ModGroup {
    param(
        [string]$Name,
        [string[]]$Regexes
    )

    [PSCustomObject]@{
        Name = $Name
        Regexes = $Regexes
    }
}

$requiredGroups = @(
    New-ModGroup -Name "ModernFix" -Regexes @("modernfix")
    New-ModGroup -Name "FerriteCore" -Regexes @("ferritecore")
    New-ModGroup -Name "Puzzles Lib" -Regexes @("puzzleslib")
    New-ModGroup -Name "Visual Workbench" -Regexes @("visualworkbench")
    New-ModGroup -Name "Sophisticated Backpacks" -Regexes @("sophisticatedbackpacks")
    New-ModGroup -Name "Sophisticated Core" -Regexes @("sophisticatedcore")
    New-ModGroup -Name "Particular Reforged" -Regexes @("particular")
    New-ModGroup -Name "Subtle Effects" -Regexes @("subtleeffects", "subtle[-_]?effects")
    New-ModGroup -Name "Fzzy Config" -Regexes @("fzzy[_-]?config", "fzzyconfig")
    New-ModGroup -Name "Kotlin for Forge" -Regexes @("kotlinforforge", "kffmod")
    New-ModGroup -Name "Terralith" -Regexes @("terralith")
    New-ModGroup -Name "Tectonic" -Regexes @("tectonic")
    New-ModGroup -Name "Serene Seasons" -Regexes @("sereneseasons")
    New-ModGroup -Name "GlitchCore" -Regexes @("glitchcore")
    New-ModGroup -Name "Towns and Towers" -Regexes @("towns.*towers", "townsandtowers")
    New-ModGroup -Name "Cristel Lib" -Regexes @("cristel.*lib", "cristellib")
    New-ModGroup -Name "Structory" -Regexes @("structory")
    New-ModGroup -Name "Sparse Structures" -Regexes @("sparse", "sparsestructures")
    New-ModGroup -Name "YUNG's API" -Regexes @("yungsapi", "yung.*api")
    New-ModGroup -Name "YUNG's Better Mineshafts" -Regexes @("yungsbettermineshafts", "yung.*better.*mineshaft")
    New-ModGroup -Name "YUNG's Better Strongholds" -Regexes @("yungsbetterstrongholds", "yung.*better.*stronghold")
    New-ModGroup -Name "YUNG's Better Dungeons" -Regexes @("yungsbetterdungeons", "yung.*better.*dungeon")
    New-ModGroup -Name "YUNG's Bridges" -Regexes @("yungsbridges", "yung.*bridges")
    New-ModGroup -Name "Better Combat" -Regexes @("bettercombat", "better.*combat")
    New-ModGroup -Name "Combat Roll" -Regexes @("combatroll", "combat.*roll")
    New-ModGroup -Name "Simply Swords" -Regexes @("simplyswords", "simply.*swords")
    New-ModGroup -Name "playerAnimator" -Regexes @("playeranimator", "playeranimationlib", "player.*animation")
    New-ModGroup -Name "Architectury API" -Regexes @("architectury")
    New-ModGroup -Name "Cloth Config API" -Regexes @("clothconfig", "cloth.*config")
    New-ModGroup -Name "Pufferfish's Attributes" -Regexes @("puffish.*attributes", "pufferfish.*attributes", "puffishattributes")
    New-ModGroup -Name "Pufferfish's Skills" -Regexes @("puffish.*skills", "pufferfish.*skills", "puffishskills")
    New-ModGroup -Name "In Control!" -Regexes @("incontrol", "in.*control")
    New-ModGroup -Name "Mowzie's Mobs" -Regexes @("mowziesmobs", "mowzie.*mobs")
    New-ModGroup -Name "GeckoLib" -Regexes @("geckolib", "gecko.*lib")
    New-ModGroup -Name "Immersive Portals" -Regexes @("immersive.*portals", "immersiveportals", "imm[_-]?ptl")
    New-ModGroup -Name "Ascendant Dwarf" -Regexes @("ascendant-1\.20\.1", "ascendant120")
    New-ModGroup -Name "Alex's Mobs" -Regexes @("alexsmobs", "alex.*mobs")
    New-ModGroup -Name "Citadel" -Regexes @("citadel")
    New-ModGroup -Name "Guard Villagers" -Regexes @("guardvillagers", "guard.*villagers")
    New-ModGroup -Name "MVS - Moog's Voyager Structures" -Regexes @("moogs.*voyager", "moog.*voyager", "moogsvoyagerstructures", "^mvs")
    New-ModGroup -Name "Moog's Structure Lib" -Regexes @("moogs.*structures", "moog.*structure.*lib", "moogsstructures")
    New-ModGroup -Name "YUNG's Extras" -Regexes @("yungsextras", "yung.*extras")
    New-ModGroup -Name "Artifacts" -Regexes @("artifacts")
    New-ModGroup -Name "Bountiful" -Regexes @("bountiful")
    New-ModGroup -Name "Kambrik" -Regexes @("kambrik")
    New-ModGroup -Name "Villager Names" -Regexes @("villagernames", "villager.*names")
    New-ModGroup -Name "Collective" -Regexes @("collective")
    New-ModGroup -Name "Loot Integrations" -Regexes @("lootintegrations", "loot.*integrations")
    New-ModGroup -Name "Cupboard" -Regexes @("cupboard")
    New-ModGroup -Name "Curios API" -Regexes @("curios")
    New-ModGroup -Name "Fragmentum" -Regexes @("fragmentum")
    New-ModGroup -Name "Iron's Spells 'n Spellbooks" -Regexes @("irons[_-]?spellbooks", "irons", "spellbooks")
    New-ModGroup -Name "Iron's Lib" -Regexes @("irons[_-]?lib", "ironslib")
    New-ModGroup -Name "Born in Chaos" -Regexes @("born.*chaos", "borninchaos", "born[_-]?in[_-]?chaos")
    New-ModGroup -Name "Aquamirae" -Regexes @("aquamirae")
    New-ModGroup -Name "Obscure API" -Regexes @("obscure[_-]?api", "obscureapi")
    New-ModGroup -Name "Enhanced Celestials" -Regexes @("enhanced.*celestials", "enhancedcelestials")
    New-ModGroup -Name "CorgiLib" -Regexes @("corgilib", "corgi.*lib")
    New-ModGroup -Name "Data Anchor" -Regexes @("data[_-]?anchor", "data.*anchor")
    New-ModGroup -Name "Bosses'Rise" -Regexes @("bosses.*rise", "bossesrise", "block[_-]?factorys[_-]?bosses")
    New-ModGroup -Name "Immersive Armors" -Regexes @("immersive.*armors", "immersivearmors")
    New-ModGroup -Name "Spartan Shields" -Regexes @("spartan.*shields", "spartanshields")
    New-ModGroup -Name "Small Ships" -Regexes @("small.*ships", "smallships")
    New-ModGroup -Name "Snow! Real Magic" -Regexes @("snow.*real.*magic", "snowrealmagic")
    New-ModGroup -Name "Kiwi" -Regexes @("kiwi")
    New-ModGroup -Name "Handcrafted" -Regexes @("handcrafted")
    New-ModGroup -Name "Resourceful Lib" -Regexes @("resourceful.*lib", "resourcefullib")
    New-ModGroup -Name "Macaw's Bridges" -Regexes @("macaw.*bridges", "mcw.*bridges", "mcwbridges")
    New-ModGroup -Name "Macaw's Fences and Walls" -Regexes @("macaw.*fences", "macaw.*walls", "mcw.*fences", "mcwfences")
    New-ModGroup -Name "IceAndFire Community Edition" -Regexes @("ice.*fire", "iceandfire", "iceandfirece", "iaf")
    New-ModGroup -Name "Jupiter" -Regexes @("jupiter")
    New-ModGroup -Name "Uranus" -Regexes @("uranus")
    New-ModGroup -Name "L_Ender's Cataclysm" -Regexes @("l.*ender.*cataclysm", "lenderscataclysm", "cataclysm")
    New-ModGroup -Name "Lionfish API" -Regexes @("lionfish.*api", "lionfishapi")
    New-ModGroup -Name "Marium's Soulslike Weaponry" -Regexes @("soulslike", "marium", "weaponry")
    New-ModGroup -Name "AttributeFix" -Regexes @("attributefix", "attribute.*fix")
    New-ModGroup -Name "Projectile Damage Attribute" -Regexes @("projectile.*damage", "projectiledamage")
    New-ModGroup -Name "Create" -Regexes @("^create[-_][0-9]", "^create[0-9]", "create[-_]1\.20\.1", "create[-_]mc")
    New-ModGroup -Name "Create Big Cannons" -Regexes @("createbigcannons", "create.*big.*cannons", "big.*cannons")
    New-ModGroup -Name "Ritchie's Projectile Library" -Regexes @("ritchies.*projectile", "ritchiesprojectilelib", "rpl")
    New-ModGroup -Name "Farmer's Delight" -Regexes @("farmersdelight", "farmer.*delight")
    New-ModGroup -Name "Create: Structures Arise" -Regexes @("create.*structures.*arise", "create.*arise", "createstructuresarise", "create_structures_arise")
    New-ModGroup -Name "Villages & Pillages" -Regexes @("villages.*pillage", "villagesandpillages")
    New-ModGroup -Name "MSS - Moog's Soaring Structures" -Regexes @("moogs.*soaring", "moog.*soaring", "moogssoaringstructures", "^mss")
    New-ModGroup -Name "MES - Moog's End Structures" -Regexes @("moogs.*end", "moog.*end", "moogsendstructures", "^mes")
    New-ModGroup -Name "Medieval Buildings [End Edition]" -Regexes @("medieval.*end", "medievalend")
    New-ModGroup -Name "Medieval Buildings [Nether Edition]" -Regexes @("medieval.*nether", "medieval_buildings_nether", "medievalbuildingsnether")
    New-ModGroup -Name "Fantasy Armor (Medieval Series)" -Regexes @("fantasy.*armor", "fantasy_armor")
    New-ModGroup -Name "Malfu Combat Animation" -Regexes @("malfu.*combat", "malfucombat")
    New-ModGroup -Name "Titles" -Regexes @("^titles", "aurilux.*titles")
    New-ModGroup -Name "Scaling Health" -Regexes @("scalinghealth", "scaling.*health")
    New-ModGroup -Name "Silent Lib" -Regexes @("silentlib", "silent.*lib")
    New-ModGroup -Name "Weather, Storms & Tornadoes" -Regexes @("weather2", "weather.*storms.*tornadoes", "weather.*tornado")
    New-ModGroup -Name "CoroUtil" -Regexes @("coroutil", "coro.*util")
    New-ModGroup -Name "Spawn Balance Utility" -Regexes @("spawnbalance", "spawn.*balance", "spawnbalanceutility")
    New-ModGroup -Name "Majrusz's Progressive Difficulty" -Regexes @("majrusz.*difficulty", "majruszs.*difficulty", "progressive.*difficulty")
    New-ModGroup -Name "Majrusz Library" -Regexes @("majrusz.*library", "majruszlibrary")
    New-ModGroup -Name "Improved Mobs" -Regexes @("improvedmobs", "improved.*mobs")
    New-ModGroup -Name "TenshiLib" -Regexes @("tenshilib", "tenshi.*lib")
    New-ModGroup -Name "KubeJS" -Regexes @("kubejs")
    New-ModGroup -Name "Rhino" -Regexes @("rhino")
    New-ModGroup -Name "Open Loader" -Regexes @("openloader", "open.*loader")
    New-ModGroup -Name "Almost Unified" -Regexes @("almostunified", "almost.*unified")
    New-ModGroup -Name "Almost Unify Everything" -Regexes @("unifyeverything", "almost.*unify.*everything", "unify.*everything")
    New-ModGroup -Name "Polymorph" -Regexes @("polymorph")
    New-ModGroup -Name "Every Compat (Wood Good)" -Regexes @("everycomp", "every.*compat", "woodgood", "wood.*good")
    New-ModGroup -Name "Moonlight Lib" -Regexes @("moonlight", "moonlight.*lib")
    New-ModGroup -Name "Create Slice & Dice" -Regexes @("sliceanddice", "slice.*dice")
    New-ModGroup -Name "Alex's Delight" -Regexes @("alexsdelight", "alex.*delight", "alex.*mobs.*delight")
    New-ModGroup -Name "Integrated Villages" -Regexes @("integrated.*villages", "integrated_villages", "integratedvillages")
    New-ModGroup -Name "Integrated Dungeons and Structures" -Regexes @("idas", "integrated.*dungeons", "integrated.*structures")
    New-ModGroup -Name "Integrated API" -Regexes @("integrated.*api", "integrated_api", "integratedapi")
    New-ModGroup -Name "Supplementaries" -Regexes @("supplementaries")
    New-ModGroup -Name "Quark" -Regexes @("quark")
    New-ModGroup -Name "Zeta" -Regexes @("zeta")
    New-ModGroup -Name "Amendments" -Regexes @("amendments")
    New-ModGroup -Name "Macaw's Lights and Lamps" -Regexes @("macaw.*lights", "macaw.*lamps", "mcw.*lights", "mcwlights")
    New-ModGroup -Name "Decorative Blocks" -Regexes @("decorative.*blocks", "decorativeblocks")
    New-ModGroup -Name "AppleSkin" -Regexes @("appleskin", "apple.*skin")
    New-ModGroup -Name "Patchouli" -Regexes @("patchouli")
    New-ModGroup -Name "FTB Library" -Regexes @("ftblibrary", "ftb.*library")
    New-ModGroup -Name "FTB Teams" -Regexes @("ftbteams", "ftb.*teams")
    New-ModGroup -Name "FTB Quests" -Regexes @("ftbquests", "ftb.*quests")
    New-ModGroup -Name "FTB Ranks" -Regexes @("ftbranks", "ftb.*ranks")
    New-ModGroup -Name "Easy NPC Bundle" -Regexes @("easy[_-]?npc[_-]?bundle", "easy.*npc.*bundle")
    New-ModGroup -Name "Easy NPC Core" -Regexes @("easy[_-]?npc[-_]?forge", "easynpcforge")
    New-ModGroup -Name "Easy NPC Config UI" -Regexes @("easy[_-]?npc[_-]?config", "easy.*npc.*config")
    New-ModGroup -Name "CustomNPCs Unofficial" -Regexes @("customnpcs", "custom.*npc")
    New-ModGroup -Name "Human Companions" -Regexes @("humancompanions", "human.*companions")
    New-ModGroup -Name "MCA Reborn" -Regexes @("minecraft[_-]?comes[_-]?alive", "mca[_-]?reborn", "comes[_-]?alive")
)

$optionalGroups = @(
    New-ModGroup -Name "Chunky (pregenerator, server-side)" -Regexes @("^chunky", "chunkypregen", "chunky.*pregen")
    New-ModGroup -Name "TRender" -Regexes @("trender")
    New-ModGroup -Name "TRansition" -Regexes @("transition")
    New-ModGroup -Name "YUNG Structures Addon for Loot Integrations" -Regexes @("yung.*loot", "lootintegration.*yung", "lootintegrations[_-]?yungs")
    New-ModGroup -Name "Batch K optional - IntegratedPlaytime" -Regexes @("integratedplaytime", "integrated.*playtime")
    New-ModGroup -Name "Batch N optional - Item Obliterator" -Regexes @("item.*obliterator", "itemobliterator")
)

$forbiddenRegexes = @(
    "embeddium",
    "oculus",
    "entitymodelfeatures",
    "entitytexturefeatures",
    "entityculling",
    "^jei",
    "freshanimations",
    "complementaryreimagined",
    "skinlayers3d",
    "legendarytooltips",
    "enchantmentdescriptions",
    "enhancedbossbars",
    "enhanced.*boss.*bars",
    "fallingleaves",
    "travelerstitles",
    "lootbeams",
    "loot.*beams",
    "lootjournal",
    "loot.*journal",
    "pickupnotifier",
    "pick.*up.*notifier",
    "auroras",
    "perception",
    "beautiful.*enchanted.*books",
    "^beb",
    "octolib",
    "shatter.*lib",
    "waveycapes",
    "wavey.*capes",
    "xaerominimap",
    "xaero.*minimap",
    "advancementplaques",
    "advancement.*plaques",
    "mobhealthbar",
    "ydm.*mob.*health",
    "soundphysics",
    "sound.*physics",
    "firstperson",
    "first.*person",
    "notenoughanimations",
    "not.*enough.*animations",
    "ambientsounds",
    "ambient.*sounds",
    "creativecore",
    "creative.*core",
    "presencefootsteps",
    "presence.*footsteps",
    "biomemusic",
    "biome.*music",
    "betteranimationscollection",
    "better.*animations.*collection",
    "simpleclouds",
    "simple.*clouds",
    "projectatmosphere",
    "project.*atmosphere",
    "betterclouds",
    "better.*clouds",
    "immersivestorms",
    "immersive.*storms",
    "healthindicators",
    "health.*indicators",
    "customnametags",
    "custom.*name.*tags",
    "champions",
    "sodiumdynamiclights",
    "sodium.*dynamic.*lights",
    "sodiumoptionsapi",
    "sodium.*options.*api",
    "immersivelanterns",
    "immersive.*lanterns",
    "accessories",
    "txnilib",
    "fancymenu",
    "fancy.*menu",
    "konkrete",
    "melody",
    "watermedia",
    "wmbinaries",
    "wm.*binaries",
    "immersiveui",
    "immersive.*ui",
    "spiffyhud",
    "spiffy.*hud",
    "drippyloadingscreen",
    "drippy.*loading",
    "itemborders",
    "item.*borders",
    "stylisheffects",
    "stylish.*effects",
    "overflowingbars",
    "overflowing.*bars"
)

$clientJarFiles = @(
    Get-ChildItem -LiteralPath $clientMods -File -Filter "*.jar" -ErrorAction SilentlyContinue
)

$copied = @()
$missing = @()

function Get-NormalizedName {
    param([string]$Name)

    $lower = $Name.ToLowerInvariant()
    [regex]::Replace($lower, "[^a-z0-9]+", "")
}

function Find-MatchingFiles {
    param([string[]]$Regexes)

    $found = foreach ($file in $clientJarFiles) {
        $lowerName = $file.Name.ToLowerInvariant()
        $normalizedName = Get-NormalizedName -Name $file.Name
        foreach ($regex in $Regexes) {
            if ($lowerName -match $regex -or $normalizedName -match $regex) {
                $file
                break
            }
        }
    }

    $found | Sort-Object FullName -Unique
}

function Copy-MatchingGroup {
    param(
        [object]$Group,
        [bool]$Required
    )

    $matches = @(Find-MatchingFiles -Regexes $Group.Regexes)
    if ($matches.Count -eq 0) {
        if ($Required) {
            $script:missing += $Group.Name
        }
        return
    }

    foreach ($match in $matches) {
        $destination = Join-Path $serverMods $match.Name
        Copy-Item -LiteralPath $match.FullName -Destination $destination -Force
        $script:copied += $match.Name
    }
}

foreach ($group in $requiredGroups) {
    Copy-MatchingGroup -Group $group -Required $true
}

foreach ($group in $optionalGroups) {
    Copy-MatchingGroup -Group $group -Required $false
}

Write-Host "Copied jars:"
$copiedUnique = @($copied | Sort-Object -Unique)
$missingUnique = @($missing | Sort-Object -Unique)

if ($copiedUnique.Count -eq 0) {
    Write-Host " - none"
} else {
    $copiedUnique | ForEach-Object { Write-Host " - $_" }
}

Write-Host "Missing required categories:"
if ($missingUnique.Count -eq 0) {
    Write-Host " - none"
} else {
    $missingUnique | ForEach-Object { Write-Host " - $_" }
}

$forbiddenFound = @()
foreach ($file in Get-ChildItem -LiteralPath $serverMods -File -Filter "*.jar" -ErrorAction SilentlyContinue) {
    $normalizedName = Get-NormalizedName -Name $file.Name
    foreach ($regex in $forbiddenRegexes) {
        if ($normalizedName -match $regex) {
            $forbiddenFound += $file
            break
        }
    }
}

if ($forbiddenFound.Count -gt 0) {
    Write-Warning "Client-only files are present in the server mods folder. Review and remove if not intentionally proven server-required:"
    $forbiddenFound | Sort-Object Name -Unique | ForEach-Object {
        Write-Warning " - $($_.Name)"
    }
}

Write-Host "Server mods materialized at $serverMods"
Write-Host "Final server jar list:"
Get-ChildItem -LiteralPath $serverMods -File -Filter "*.jar" -ErrorAction SilentlyContinue |
    Sort-Object Name |
    ForEach-Object { Write-Host " - $($_.Name)" }

if ($missingUnique.Count -gt 0) {
    throw "Missing required server/both-side jars. Import the latest client export into the active CurseForge instance, then rerun this script with the active instance mods path."
}
