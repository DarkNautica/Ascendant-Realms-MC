param(
    [Parameter(Mandatory = $true)]
    [Alias("ActiveClientModsPath")]
    [string]$ClientModsPath,

    [string]$OutputPath = "docs/WORLD_INTEGRATION_AUDIT.md"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Add-Type -AssemblyName System.IO.Compression.FileSystem

$clientMods = [System.IO.Path]::GetFullPath($ClientModsPath)
$output = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $OutputPath))

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

function New-CountBucket {
    param(
        [string]$Label,
        [scriptblock]$Filter
    )

    [PSCustomObject]@{
        Label = $Label
        Filter = $Filter
    }
}

$buckets = @(
    New-CountBucket -Label "Structures" -Filter { param($name) $name -match '^data/.+/worldgen/structure/.+\.json$' }
    New-CountBucket -Label "Structure Sets" -Filter { param($name) $name -match '^data/.+/worldgen/structure_set/.+\.json$' }
    New-CountBucket -Label "Template Pools" -Filter { param($name) $name -match '^data/.+/worldgen/template_pool/.+\.json$' }
    New-CountBucket -Label "Placed Features" -Filter { param($name) $name -match '^data/.+/worldgen/placed_feature/.+\.json$' }
    New-CountBucket -Label "Configured Features" -Filter { param($name) $name -match '^data/.+/worldgen/configured_feature/.+\.json$' }
    New-CountBucket -Label "Biome Modifiers" -Filter { param($name) $name -match '^data/.+/forge/biome_modifier/.+\.json$' }
    New-CountBucket -Label "Biome Tags" -Filter { param($name) $name -match '^data/.+/tags/worldgen/biome/.+\.json$' }
    New-CountBucket -Label "Loot Tables" -Filter { param($name) $name -match '^data/.+/loot_tables/.+\.json$' }
    New-CountBucket -Label "Recipes" -Filter { param($name) $name -match '^data/.+/recipes/.+\.json$' }
    New-CountBucket -Label "Item Tags" -Filter { param($name) $name -match '^data/.+/tags/items/.+\.json$' }
    New-CountBucket -Label "Entity Type Tags" -Filter { param($name) $name -match '^data/.+/tags/entity_types/.+\.json$' }
)

$rows = @()

foreach ($jar in Get-ChildItem -LiteralPath $clientMods -Filter "*.jar" -File | Sort-Object Name) {
    $zip = [System.IO.Compression.ZipFile]::OpenRead($jar.FullName)
    try {
        $info = Get-ModInfo -Zip $zip
        $entryNames = @($zip.Entries | ForEach-Object { $_.FullName })
        $counts = @{}
        foreach ($bucket in $buckets) {
            $counts[$bucket.Label] = @($entryNames | Where-Object { & $bucket.Filter $_ }).Count
        }

        $rows += [PSCustomObject]@{
            Jar = $jar.Name
            ModId = $info.ModId
            DisplayName = $info.DisplayName
            Counts = $counts
        }
    }
    finally {
        $zip.Dispose()
    }
}

$contentMods = $rows | Where-Object {
    $_.Counts["Structures"] -gt 0 -or
    $_.Counts["Structure Sets"] -gt 0 -or
    $_.Counts["Template Pools"] -gt 0 -or
    $_.Counts["Placed Features"] -gt 0 -or
    $_.Counts["Configured Features"] -gt 0 -or
    $_.Counts["Biome Modifiers"] -gt 0 -or
    $_.Counts["Loot Tables"] -gt 0 -or
    $_.Counts["Recipes"] -gt 0
}

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add("# World Integration Audit")
$lines.Add("")
$lines.Add("Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')")
$lines.Add("")
$lines.Add("Client mods path: ``$clientMods``")
$lines.Add("")
$lines.Add("This audit scans jar data files for structures, world features, biome modifiers, loot tables, recipes, and tags. It does not prove in-game balance by itself; it gives us the inventory to tune against.")
$lines.Add("")
$lines.Add("## Crash Repair")
$lines.Add("")
$lines.Add("- ``config/openloader/data/ascendant_realms_world_integration`` repairs the shared Integrated Villages ``integrated_api:workstation_processor`` POI-cast crash path with static ``minecraft:rule`` workstation replacements.")
$lines.Add("- ``integrated_villages:airship_village``, ``integrated_villages:mossy_mounds``, and ``integrated_villages:marketstead_village`` remain enabled for retest.")
$lines.Add("- Integrated Villages' ``minecraft:village`` structure tag is repaired because the jar references nonexistent ``integrated_villages:swamp_village``.")
$lines.Add("- Root cause note: inspect processor/template paths before disabling more structures. Use structure removal only as a temporary emergency fallback.")
$lines.Add("")
$lines.Add("## Summary")
$lines.Add("")
$lines.Add("| Scope | Count |")
$lines.Add("| --- | ---: |")
$lines.Add("| Jars scanned | $($rows.Count) |")
$lines.Add("| Jars with world/data integration surfaces | $($contentMods.Count) |")
foreach ($bucket in $buckets) {
    $total = ($rows | ForEach-Object { $_.Counts[$bucket.Label] } | Measure-Object -Sum).Sum
    $lines.Add("| $($bucket.Label) | $total |")
}
$lines.Add("")
$lines.Add("## Per-Mod Integration Surface")
$lines.Add("")
$lines.Add("| Mod | Mod ID | Jar | Structures | Sets | Pools | Features | Biome Modifiers | Loot | Recipes | Tags |")
$lines.Add("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")

foreach ($row in $contentMods) {
    $name = if ($row.DisplayName) { $row.DisplayName } else { "(unknown)" }
    $modId = if ($row.ModId) { $row.ModId } else { "(unknown)" }
    $structures = $row.Counts["Structures"]
    $sets = $row.Counts["Structure Sets"]
    $pools = $row.Counts["Template Pools"]
    $features = $row.Counts["Placed Features"] + $row.Counts["Configured Features"]
    $biomeModifiers = $row.Counts["Biome Modifiers"]
    $loot = $row.Counts["Loot Tables"]
    $recipes = $row.Counts["Recipes"]
    $tags = $row.Counts["Biome Tags"] + $row.Counts["Item Tags"] + $row.Counts["Entity Type Tags"]
    $lines.Add("| $name | ``$modId`` | ``$($row.Jar)`` | $structures | $sets | $pools | $features | $biomeModifiers | $loot | $recipes | $tags |")
}

$lines.Add("")
$lines.Add("## Follow-Up Checks")
$lines.Add("")
$lines.Add("- Run this after each CurseForge import using the active instance mods folder.")
$lines.Add("- Confirm mob-heavy mods with few/no biome modifiers are controlled through their config files or In Control caps.")
$lines.Add("- Confirm structure-heavy mods with many structure sets are represented in `config/sparsestructures.json5`, dedicated mod configs, or documented density policy.")
$lines.Add("- Confirm loot-heavy mods feed `Loot Integrations`, Bountiful contracts, the skill tree, or delayed KubeJS scripts.")

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $output) | Out-Null
$lines | Set-Content -LiteralPath $output -Encoding UTF8

Write-Host "World integration audit written to $output"

