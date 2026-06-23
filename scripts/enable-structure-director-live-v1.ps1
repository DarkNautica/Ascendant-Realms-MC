param(
    [string]$InstancePath = "C:\Users\Jayden\curseforge\minecraft\Instances\Ascendant Realms (2)"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$policyPath = Join-Path $root "config\ascendant_structures\live_structure_policy.json"
$livePath = Join-Path $root "config\openloader\data\ascendant_structure_director_live"
$disabledPath = Join-Path $root "config\openloader\data\ascendant_structure_director_live.disabled"

if ((-not (Test-Path -LiteralPath $livePath)) -and (Test-Path -LiteralPath $disabledPath)) {
    Rename-Item -LiteralPath $disabledPath -NewName "ascendant_structure_director_live"
}

if (-not (Test-Path -LiteralPath $livePath)) {
    throw "Live datapack folder is missing: $livePath"
}

if (Test-Path -LiteralPath $policyPath) {
    $policy = Get-Content -LiteralPath $policyPath -Raw | ConvertFrom-Json
    $policy.enabled = $true
    $policy | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $policyPath -Encoding UTF8
}

Write-Host "Structure Director Live v1 enabled in source. Run sync/export before testing an active instance."
