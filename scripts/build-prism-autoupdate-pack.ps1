param(
    [string]$PackTomlUrl = "https://raw.githubusercontent.com/DarkNautica/Ascendant-Realms-MC/main/pack.toml",
    [string]$Output = "dist\Ascendant-Realms-Prism-AutoUpdate.zip",
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

if ($ForceBootstrapDownload -or -not (Test-Path -LiteralPath $bootstrap)) {
    $headers = @{ "User-Agent" = "Ascendant-Realms-Prism-Pack" }
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/packwiz/packwiz-installer-bootstrap/releases/latest" -Headers $headers
    $asset = $release.assets | Where-Object { $_.name -eq "packwiz-installer-bootstrap.jar" } | Select-Object -First 1
    if (-not $asset) { throw "Could not find packwiz-installer-bootstrap.jar in the latest release." }
    Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $bootstrap -Headers $headers
}

$preLaunch = '"$INST_JAVA" -jar "$INST_MC_DIR/packwiz-installer-bootstrap.jar" ' + $PackTomlUrl
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
