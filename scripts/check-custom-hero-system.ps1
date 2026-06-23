param(
    [switch]$SyncClient,
    [switch]$Apply,
    [string]$InstancePath = "",
    [string]$WorldPath = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($InstancePath)) {
    $instancesRoot = "C:\Users\Jayden\curseforge\minecraft\Instances"
    $latestAscendantInstance = Get-ChildItem -LiteralPath $instancesRoot -Directory |
        Where-Object { $_.Name -like "Ascendant Realms*" } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if ($null -eq $latestAscendantInstance) {
        throw "Could not find an Ascendant Realms CurseForge instance under $instancesRoot"
    }

    $InstancePath = $latestAscendantInstance.FullName
}

if ([string]::IsNullOrWhiteSpace($WorldPath)) {
    $savesPath = Join-Path $InstancePath "saves"
    if (Test-Path -LiteralPath $savesPath) {
        $latestWorld = Get-ChildItem -LiteralPath $savesPath -Directory |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1
        if ($null -ne $latestWorld) {
            $WorldPath = $latestWorld.FullName
        }
    }
}

Write-Host "== Ascendant Custom Hero System Check =="
Write-Host "Instance: $InstancePath"
if (-not [string]::IsNullOrWhiteSpace($WorldPath)) {
    Write-Host "World: $WorldPath"
}

if ($SyncClient) {
    Write-Host "Syncing current client-side data/config files..."
    powershell -ExecutionPolicy Bypass -File scripts\sync-active-client-files.ps1 -InstancePath $InstancePath
}

Write-Host "Checking CustomNPCs identity script logic..."
node scripts\test-customnpcs-identity.js

Write-Host "Auditing active CustomNPC world data..."
if ([string]::IsNullOrWhiteSpace($WorldPath)) {
    Write-Host "No world save found to audit; skipping world entity audit."
}
elseif ($Apply) {
    python scripts\customnpcs-identity-audit.py --world $WorldPath --apply
} else {
    python scripts\customnpcs-identity-audit.py --world $WorldPath
}

Write-Host "Running full pack validation..."
python scripts\check-pack.py

Write-Host "Custom hero system check completed."
