param(
    [string]$Output = "dist\ascendant-realms-client.zip"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

function Get-PackwizPath {
    $cmd = Get-Command packwiz -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $go = Get-Command go -ErrorAction SilentlyContinue
    if ($go) {
        $goPath = (& go env GOPATH).Trim()
        $candidate = Join-Path $goPath "bin\packwiz.exe"
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }

    throw "Packwiz is missing. Install it from https://github.com/packwiz/packwiz."
}

if (-not (Test-Path -LiteralPath "pack.toml")) {
    throw "Packwiz is not initialized yet. Approve the version/loader decision before exporting."
}

New-Item -ItemType Directory -Force -Path "dist" | Out-Null
$resolvedOutput = [System.IO.Path]::GetFullPath((Join-Path $RepoRoot $Output))
if (-not $resolvedOutput.StartsWith($RepoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to write client export outside the repo: $resolvedOutput"
}
if (Test-Path -LiteralPath $resolvedOutput) {
    Remove-Item -LiteralPath $resolvedOutput -Force
}
$packwiz = Get-PackwizPath
& $packwiz curseforge export --side client --output $resolvedOutput
