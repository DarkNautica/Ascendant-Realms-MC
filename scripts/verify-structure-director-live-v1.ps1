param(
    [string]$InstancePath = "C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$policyPath = Join-Path $root "config\ascendant_structures\live_structure_policy.json"
$manifestPath = Join-Path $root "config\ascendant_structures\live_structure_manifest.json"
$datapackPath = Join-Path $root "config\openloader\data\ascendant_structure_director_live"
$rollbackPath = Join-Path $root "config\ascendant_structures\rollback\pre_structure_director_v1\rollback_manifest.json"
$helperPath = Join-Path $root "mods\ascendant-atlas-regions-0.1.0.jar"
$instanceRoot = Resolve-Path -LiteralPath $InstancePath -ErrorAction SilentlyContinue

function Get-DirectoryHash {
    param([Parameter(Mandatory = $true)][string]$Path)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $files = @(Get-ChildItem -LiteralPath $Path -Recurse -File |
            ForEach-Object {
                [pscustomobject]@{
                    File = $_
                    Relative = $_.FullName.Substring($Path.Length).TrimStart('\','/').Replace('\','/')
                }
            })
        [Array]::Sort($files, [System.Comparison[object]]{
            param($left, $right)
            return [System.StringComparer]::Ordinal.Compare($left.Relative, $right.Relative)
        })
        foreach ($entry in $files) {
            $file = $entry.File
            $relative = $entry.Relative
            $nameBytes = [System.Text.Encoding]::UTF8.GetBytes($relative.Replace('\','/'))
            $content = [System.IO.File]::ReadAllBytes($file.FullName)
            [void]$sha.TransformBlock($nameBytes, 0, $nameBytes.Length, $null, 0)
            [void]$sha.TransformBlock($content, 0, $content.Length, $null, 0)
        }
        [void]$sha.TransformFinalBlock([byte[]]::new(0), 0, 0)
        return ([System.BitConverter]::ToString($sha.Hash) -replace '-', '').ToUpperInvariant()
    }
    finally {
        $sha.Dispose()
    }
}

if (-not (Test-Path -LiteralPath $policyPath)) { throw "Missing live policy: $policyPath" }
if (-not (Test-Path -LiteralPath $manifestPath)) { throw "Missing live manifest: $manifestPath" }
if (-not (Test-Path -LiteralPath $datapackPath)) { throw "Missing live datapack: $datapackPath" }
if (-not (Test-Path -LiteralPath $rollbackPath)) { throw "Missing rollback manifest: $rollbackPath" }
if (-not (Test-Path -LiteralPath $helperPath)) { throw "Missing helper jar: $helperPath" }

$policy = Get-Content -LiteralPath $policyPath -Raw | ConvertFrom-Json
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$sourceDatapackHash = Get-DirectoryHash -Path $datapackPath
$sourceHelperHash = (Get-FileHash -LiteralPath $helperPath -Algorithm SHA256).Hash.ToUpperInvariant()

Write-Host "Structure Director Live v1 source verification"
Write-Host "enabled: $($policy.enabled)"
Write-Host "version: $($manifest.version)"
Write-Host "live changes: $($manifest.live_change_count)"
Write-Host "source datapack hash: $sourceDatapackHash"
Write-Host "source helper hash: $sourceHelperHash"

if ($instanceRoot) {
    $activeDatapack = Join-Path $instanceRoot "config\openloader\data\ascendant_structure_director_live"
    $activeHelper = Join-Path $instanceRoot "mods\ascendant-atlas-regions-0.1.0.jar"
    if (Test-Path -LiteralPath $activeDatapack) {
        Write-Host "active datapack hash: $(Get-DirectoryHash -Path $activeDatapack)"
    } else {
        Write-Host "active datapack missing"
    }
    if (Test-Path -LiteralPath $activeHelper) {
        Write-Host "active helper hash: $((Get-FileHash -LiteralPath $activeHelper -Algorithm SHA256).Hash.ToUpperInvariant())"
    } else {
        Write-Host "active helper missing"
    }
}
