param(
    [string]$RemoteUrl = "https://github.com/DarkNautica/Ascendant-Realms-MC.git",
    [string]$Branch = "main",
    [string]$Message = "",
    [switch]$NoPush,
    [switch]$StrictCheck,
    [switch]$SkipCheck
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

if (-not $Message) {
    $Message = "Update Ascendant Realms pack $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
}

$packwiz = Get-PackwizPath
& $packwiz refresh
if ($LASTEXITCODE -ne 0) { throw "packwiz refresh failed." }

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $SkipCheck -and $python -and (Test-Path -LiteralPath "scripts\check-pack.py")) {
    & $python.Source "scripts\check-pack.py"
    if ($LASTEXITCODE -ne 0) {
        if ($StrictCheck) { throw "pack check failed." }
        Write-Warning "Pack check reported issues. Continuing because -StrictCheck was not used."
    }
}

$gitDir = Join-Path $RepoRoot ".git"
if (-not (Test-Path -LiteralPath $gitDir)) {
    git init
    if ($LASTEXITCODE -ne 0) { throw "git init failed." }
    git checkout -B $Branch
    if ($LASTEXITCODE -ne 0) { throw "git branch setup failed." }
} else {
    git checkout -B $Branch
    if ($LASTEXITCODE -ne 0) { throw "git branch setup failed." }
}

$userName = (git config user.name)
if (-not $userName) { git config user.name "Jayden" }
$userEmail = (git config user.email)
if (-not $userEmail) { git config user.email "jayden@ascendant-realms.local" }

$remotes = @(git remote)
if ($remotes -contains "origin") {
    $origin = (git remote get-url origin)
    if ($origin.Trim() -ne $RemoteUrl) { git remote set-url origin $RemoteUrl }
} else {
    git remote add origin $RemoteUrl
}

git add -A
if ($LASTEXITCODE -ne 0) { throw "git add failed." }

$status = git status --short
if (-not $status) {
    Write-Host "No new pack changes to commit."
    if (-not $NoPush) {
        git push -u origin $Branch
        if ($LASTEXITCODE -ne 0) {
            throw "git push failed. Sign in to GitHub for DarkNautica/Ascendant-Realms-MC, then run this again."
        }
        Write-Host "Published existing local commits to GitHub."
    }
    exit 0
}

git commit -m $Message
if ($LASTEXITCODE -ne 0) { throw "git commit failed." }

if ($NoPush) {
    Write-Host "Committed locally. Skipping push because -NoPush was used."
    exit 0
}

git push -u origin $Branch
if ($LASTEXITCODE -ne 0) {
    throw "git push failed. Sign in to GitHub for DarkNautica/Ascendant-Realms-MC, then run this again."
}

Write-Host "Published Ascendant Realms to GitHub."
