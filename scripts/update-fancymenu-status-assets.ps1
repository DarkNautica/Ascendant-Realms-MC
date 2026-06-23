param()

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$PackToml = Join-Path $RepoRoot "pack.toml"
$AssetDir = Join-Path $RepoRoot "config\fancymenu\assets"
$MetaPath = Join-Path $AssetDir "ascendant_pack_meta.json"

if (-not (Test-Path -LiteralPath $PackToml)) {
    throw "pack.toml is missing; cannot update FancyMenu pack metadata."
}

$packText = Get-Content -Raw -LiteralPath $PackToml
$nameMatch = [regex]::Match($packText, '(?m)^name\s*=\s*"([^"]+)"')
$versionMatch = [regex]::Match($packText, '(?m)^version\s*=\s*"([^"]+)"')

if (-not $nameMatch.Success) {
    throw "pack.toml is missing a name value."
}
if (-not $versionMatch.Success) {
    throw "pack.toml is missing a version value."
}

New-Item -ItemType Directory -Force -Path $AssetDir | Out-Null

[ordered]@{
    name = $nameMatch.Groups[1].Value
    version = $versionMatch.Groups[1].Value
} | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath $MetaPath -Encoding UTF8

Write-Host "Updated FancyMenu pack metadata: $MetaPath"
