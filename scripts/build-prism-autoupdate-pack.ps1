param(
    [string]$PackTomlUrl = "https://raw.githubusercontent.com/DarkNautica/Ascendant-Realms-MC/main/pack.toml",
    [string]$Output = "dist\Ascendant-Realms-Prism-AutoUpdate.zip",
    [string]$ClientInstancePath = "C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)",
    [int]$MaxMemoryMB = 8192,
    [switch]$ForceBootstrapDownload
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

if (-not (Test-Path -LiteralPath "pack.toml")) {
    throw "pack.toml not found. Run this from the Ascendant Realms pack repo."
}

$dist = Join-Path $RepoRoot "dist"
$stageRoot = Join-Path $dist "prism-autoupdate"
$minecraftDir = Join-Path $stageRoot ".minecraft"
$bootstrap = Join-Path $minecraftDir "packwiz-installer-bootstrap.jar"
$resolvedStage = [IO.Path]::GetFullPath($stageRoot)
$resolvedDist = [IO.Path]::GetFullPath($dist)
if (-not $resolvedStage.StartsWith($resolvedDist, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to clean unexpected staging path: $resolvedStage"
}

New-Item -ItemType Directory -Force -Path $dist | Out-Null
if (Test-Path -LiteralPath $stageRoot) {
    Remove-Item -LiteralPath $stageRoot -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $minecraftDir | Out-Null

$manualFiles = @(
    @{
        Source = Join-Path $ClientInstancePath "mods\easy_npc_bundle-forge-1.20.1-6.19.0.jar"
        Dest = Join-Path $minecraftDir "mods\easy_npc_bundle-forge-1.20.1-6.19.0.jar"
        Sha1 = "4b28554590977817cac22499408d6dbc4f21b612"
    },
    @{
        Source = Join-Path $ClientInstancePath "resourcepacks\MCAR_VanillaMedieval_Universal_1.20.x_Only_Clothes_byDE4THR4SH_v4.zip"
        Dest = Join-Path $minecraftDir "resourcepacks\MCAR_VanillaMedieval_Universal_1.20.x_Only_Clothes_byDE4THR4SH_v4.zip"
        Sha1 = "3d50537c5a7e9d85ebabe317121897ef20ed4524"
    }
)

foreach ($file in $manualFiles) {
    if (-not (Test-Path -LiteralPath $file.Source)) {
        throw "Missing manual Prism bundle source file: $($file.Source)"
    }
    $actual = (Get-FileHash -Algorithm SHA1 -LiteralPath $file.Source).Hash.ToLowerInvariant()
    if ($actual -ne $file.Sha1) {
        throw "Manual Prism bundle file hash mismatch for $($file.Source). Expected $($file.Sha1), got $actual."
    }
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $file.Dest) | Out-Null
    Copy-Item -LiteralPath $file.Source -Destination $file.Dest -Force
}

if ($ForceBootstrapDownload -or -not (Test-Path -LiteralPath $bootstrap)) {
    $headers = @{ "User-Agent" = "Ascendant-Realms-Prism-Pack" }
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/packwiz/packwiz-installer-bootstrap/releases/latest" -Headers $headers
    $asset = $release.assets | Where-Object { $_.name -eq "packwiz-installer-bootstrap.jar" } | Select-Object -First 1
    if (-not $asset) { throw "Could not find packwiz-installer-bootstrap.jar in the latest release." }
    Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $bootstrap -Headers $headers
}

$preLaunch = '"$INST_JAVA" -jar "$INST_MC_DIR/packwiz-installer-bootstrap.jar" -g ' + $PackTomlUrl
$instanceCfg = @"
InstanceType=OneSix
name=Ascendant Realms
iconKey=default
OverrideCommands=true
PreLaunchCommand=$preLaunch
OverrideMemory=true
MinMemAlloc=1024
MaxMemAlloc=$MaxMemoryMB
PermGen=128
"@
[IO.File]::WriteAllText((Join-Path $stageRoot "instance.cfg"), $instanceCfg, (New-Object Text.UTF8Encoding($false)))

$mmcPack = @'
{
  "components": [
    {
      "important": true,
      "uid": "net.minecraft",
      "version": "1.20.1"
    },
    {
      "uid": "net.minecraftforge",
      "version": "47.4.20"
    }
  ],
  "formatVersion": 1
}
'@
[IO.File]::WriteAllText((Join-Path $stageRoot "mmc-pack.json"), $mmcPack, (New-Object Text.UTF8Encoding($false)))

$readme = @"
Ascendant Realms - Prism Auto Update

Import this ZIP in Prism Launcher with Add Instance > Import.
After the first import, Prism runs packwiz before each launch and pulls updates from:
$PackTomlUrl

This ZIP also bundles the CurseForge manual-only Easy NPC bundle and MCA medieval clothing resource pack so first launch does not require extra downloads.

Important: when importing in Prism, stay on the Import tab until you click OK.
"@
[IO.File]::WriteAllText((Join-Path $stageRoot "README_IMPORT.txt"), $readme, (New-Object Text.UTF8Encoding($false)))

$resolvedOutput = [IO.Path]::GetFullPath((Join-Path $RepoRoot $Output))
if (-not $resolvedOutput.StartsWith($resolvedDist, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to write Prism export outside dist: $resolvedOutput"
}
if (Test-Path -LiteralPath $resolvedOutput) {
    Remove-Item -LiteralPath $resolvedOutput -Force
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
[IO.Compression.ZipFile]::CreateFromDirectory($stageRoot, $resolvedOutput, [IO.Compression.CompressionLevel]::Optimal, $false)

Write-Host "Built Prism auto-update import:"
Write-Host "  $resolvedOutput"
Write-Host "Pack URL:"
Write-Host "  $PackTomlUrl"
