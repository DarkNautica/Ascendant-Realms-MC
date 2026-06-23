param(
    [string]$OutputDir = "dist\server-pack-staging"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

if (-not (Test-Path -LiteralPath "pack.toml") -or -not (Test-Path -LiteralPath "index.toml")) {
    throw "Packwiz metadata is missing. Approve the version/loader decision, initialize Packwiz, then export."
}

$staging = [System.IO.Path]::GetFullPath((Join-Path $RepoRoot $OutputDir))
if (-not $staging.StartsWith($RepoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to write server export outside the repo: $staging"
}

New-Item -ItemType Directory -Force -Path $staging | Out-Null
Get-ChildItem -LiteralPath $staging -Force | Remove-Item -Recurse -Force

Copy-Item -LiteralPath "pack.toml", "index.toml" -Destination $staging
foreach ($dir in @("config", "customnpcs", "datapacks", "docs", "kubejs", "openloader")) {
    if (Test-Path -LiteralPath $dir) {
        Copy-Item -LiteralPath $dir -Destination (Join-Path $staging $dir) -Recurse
    }
}

$clientOnlyConfigPaths = @(
    "config\drippyloadingscreen",
    "config\fancymenu",
    "config\sound_physics_remastered",
    "config\amendments-client.toml",
    "config\embeddium-mixins.properties",
    "config\embeddium-options.json",
    "config\entityculling.json",
    "config\irons_spellbooks-client.toml",
    "config\itemborders-common.toml",
    "config\lootbeams-client.toml",
    "config\mobhealthbar-client.toml",
    "config\overflowingbars-client.toml",
    "config\resourcepackoverrides.json",
    "config\sodiumdynamiclights-client.toml",
    "config\travelerstitles-forge-1_20.toml"
)

foreach ($relativePath in $clientOnlyConfigPaths) {
    $target = Join-Path $staging $relativePath
    if (Test-Path -LiteralPath $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }
}

if (Test-Path -LiteralPath "mods") {
    New-Item -ItemType Directory -Force -Path (Join-Path $staging "mods") | Out-Null
    Get-ChildItem -LiteralPath "mods" -Filter "*.pw.toml" | ForEach-Object {
        $text = Get-Content -Raw -LiteralPath $_.FullName
        if ($text -notmatch '(?m)^side\s*=\s*"client"') {
            Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $staging "mods")
        }
    }
    Get-ChildItem -LiteralPath "mods" -Filter "*.jar" -File | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $staging "mods") -Force
    }
}

@(
    "# Server Pack Review Required",
    "",
    "This staging folder is generated from Packwiz metadata.",
    "It is not a runnable server mods folder until real .jar files are materialized.",
    "Review client/server side metadata before upload.",
    "Use scripts/materialize-server-mods-from-client.ps1 with a working client mods folder to copy approved server/both-side jars.",
    "Local helper jars from mods are copied into mods automatically.",
    "Do not upload shaderpacks, resource packs, or client-only visual/render/UI mods to the server."
) | Set-Content -LiteralPath (Join-Path $staging "SERVER_PACK_TODO.md") -Encoding UTF8

Write-Host "Server staging created at $OutputDir"
