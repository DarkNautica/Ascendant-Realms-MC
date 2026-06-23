param(
    [string]$InstancePath = "",
    [switch]$AllowWhileRunning
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

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

$target = Resolve-Path -LiteralPath $InstancePath -ErrorAction Stop

Write-Host "Syncing Ascendant Realms client files to $target"

if (-not $AllowWhileRunning) {
    $runningMinecraft = Get-Process -ErrorAction SilentlyContinue |
        Where-Object {
            ($_.ProcessName -eq "java" -or $_.ProcessName -eq "javaw") -and
            ($_.Path -like "*\curseforge\minecraft\Install\java\*")
        } |
        Select-Object -First 1

    if ($null -ne $runningMinecraft) {
        throw "Minecraft appears to be running (process $($runningMinecraft.Id)). Close the client before syncing configs, options.txt, or client-only jars."
    }
}

& (Join-Path $root "scripts\update-fancymenu-status-assets.ps1")

function Copy-Directory {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        return
    }

    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Get-ChildItem -LiteralPath $Source -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $Destination -Recurse -Force
    }
}

function Copy-File {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        return
    }

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Destination) | Out-Null
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
}

function Remove-StaleAtlasStructureSets {
    param(
        [Parameter(Mandatory = $true)][string]$InstanceRoot
    )

    $stalePath = Join-Path $InstanceRoot "config\openloader\data\ascendant_realms_atlas\data\ascendant_atlas\worldgen\structure_set"
    if (Test-Path -LiteralPath $stalePath) {
        Remove-Item -LiteralPath $stalePath -Recurse -Force
        Write-Host "Removed retired Ascendant Atlas waymark structure_set files."
    }
}

function Remove-AtlasWorldgenInfluenceIfDisabled {
    param(
        [Parameter(Mandatory = $true)][string]$InstanceRoot
    )

    $policyPath = Join-Path $root "config\ascendant_atlas\worldgen_override_policy.json"
    if (-not (Test-Path -LiteralPath $policyPath)) {
        return
    }

    $policy = Get-Content -LiteralPath $policyPath -Raw | ConvertFrom-Json
    if ($policy.worldgen_override_enabled -ne $false) {
        return
    }

    $staleAtlasWorldgenFiles = @(
        "config\openloader\data\ascendant_realms_atlas\data\minecraft\dimension\overworld.json",
        "config\openloader\data\ascendant_realms_atlas\data\minecraft\worldgen\density_function\overworld\continents.json"
    )

    foreach ($relativePath in $staleAtlasWorldgenFiles) {
        $targetPath = Join-Path $InstanceRoot $relativePath
        if (Test-Path -LiteralPath $targetPath) {
            Remove-Item -LiteralPath $targetPath -Force
            Write-Host "Removed disabled Atlas worldgen influence file: $relativePath"
        }
    }
}

function Write-Utf8NoBomLines {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][object[]]$Lines
    )

    $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
    [System.IO.File]::WriteAllLines($Path, [string[]]$Lines, $utf8NoBom)
}

function Ensure-ModernOptionsVersion {
    param(
        [Parameter(Mandatory = $true)][object[]]$Lines
    )

    $modernVersion = "version:3465"
    $result = [System.Collections.Generic.List[string]]::new()
    $hasVersion = $false

    foreach ($line in $Lines) {
        if ($line -like "version:*") {
            $hasVersion = $true
            $result.Add($modernVersion)
        }
        else {
            $result.Add($line)
        }
    }

    if (-not $hasVersion) {
        $result.Insert(0, $modernVersion)
    }

    return $result
}

function Copy-ResourcePacks {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        return
    }

    New-Item -ItemType Directory -Force -Path $Destination | Out-Null

    Get-ChildItem -LiteralPath $Destination -Filter "*.pw.toml" -File -ErrorAction SilentlyContinue |
        Remove-Item -Force

    Get-ChildItem -LiteralPath $Destination -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -like "*Vanilla Experience*" -and $_.Name -ne "Vanilla Experience Plus.zip" } |
        ForEach-Object {
            Remove-Item -LiteralPath $_.FullName -Force
            Write-Host "Removed stale resource pack filename: $($_.Name)"
        }

    Get-ChildItem -LiteralPath $Source -Force |
        Where-Object { -not ($_.PSIsContainer -eq $false -and $_.Name -like "*.pw.toml") } |
        ForEach-Object {
            Copy-Item -LiteralPath $_.FullName -Destination $Destination -Recurse -Force
        }
}

function Sync-OptionsResourcePacks {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        return
    }

    $sourceLines = Get-Content -LiteralPath $Source
    $resourcePackLine = $sourceLines | Where-Object { $_ -like "resourcePacks:*" } | Select-Object -First 1
    $incompatibleLine = $sourceLines | Where-Object { $_ -like "incompatibleResourcePacks:*" } | Select-Object -First 1

    if (-not $resourcePackLine) {
        return
    }

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Destination) | Out-Null

    if (-not (Test-Path -LiteralPath $Destination)) {
        $newLines = Ensure-ModernOptionsVersion -Lines $sourceLines
        Write-Utf8NoBomLines -Path $Destination -Lines $newLines
        return
    }

    $targetLines = [System.Collections.Generic.List[string]]::new()
    foreach ($line in Get-Content -LiteralPath $Destination) {
        if ($line -like "resourcePacks:*") {
            $targetLines.Add($resourcePackLine)
        }
        elseif ($line -like "incompatibleResourcePacks:*") {
            if ($incompatibleLine) {
                $targetLines.Add($incompatibleLine)
            }
        }
        else {
            $targetLines.Add($line)
        }
    }

    if (-not ($targetLines | Where-Object { $_ -like "resourcePacks:*" })) {
        $targetLines.Add($resourcePackLine)
    }
    if ($incompatibleLine -and -not ($targetLines | Where-Object { $_ -like "incompatibleResourcePacks:*" })) {
        $targetLines.Add($incompatibleLine)
    }

    $targetLines = Ensure-ModernOptionsVersion -Lines $targetLines
    Write-Utf8NoBomLines -Path $Destination -Lines $targetLines
}

function Apply-KeybindPolicy {
    param(
        [Parameter(Mandatory = $true)][string]$PolicyPath,
        [Parameter(Mandatory = $true)][string]$DestinationOptions
    )

    if (-not (Test-Path -LiteralPath $PolicyPath)) {
        return
    }

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $DestinationOptions) | Out-Null

    if (-not (Test-Path -LiteralPath $DestinationOptions)) {
        Write-Utf8NoBomLines -Path $DestinationOptions -Lines @("version:3465")
    }

    $policy = Get-Content -LiteralPath $PolicyPath -Raw | ConvertFrom-Json
    if ($null -eq $policy.bindings) {
        return
    }

    $bindings = @{}
    foreach ($property in $policy.bindings.PSObject.Properties) {
        $bindings[$property.Name] = [string]$property.Value
    }

    if ($bindings.Count -eq 0) {
        return
    }

    $targetLines = [System.Collections.Generic.List[string]]::new()
    $seenBindings = [System.Collections.Generic.HashSet[string]]::new()

    foreach ($line in Get-Content -LiteralPath $DestinationOptions) {
        if ($line -match "^([^:]+):(.*)$") {
            $keyName = $Matches[1]
            if ($bindings.ContainsKey($keyName)) {
                $targetLines.Add(("{0}:{1}" -f $keyName, $bindings[$keyName]))
                [void]$seenBindings.Add($keyName)
                continue
            }
        }
        $targetLines.Add($line)
    }

    foreach ($keyName in $bindings.Keys | Sort-Object) {
        if (-not $seenBindings.Contains($keyName)) {
            $targetLines.Add(("{0}:{1}" -f $keyName, $bindings[$keyName]))
        }
    }

    $targetLines = Ensure-ModernOptionsVersion -Lines $targetLines
    Write-Utf8NoBomLines -Path $DestinationOptions -Lines $targetLines
    Write-Host "Applied Ascendant keybind policy: $($bindings.Count) bindings."
}

function Set-KeyValueLine {
    param(
        [Parameter(Mandatory = $true)][object[]]$Lines,
        [Parameter(Mandatory = $true)][string]$Key,
        [Parameter(Mandatory = $true)][string]$Value
    )

    $result = [System.Collections.Generic.List[string]]::new()
    $found = $false
    $pattern = "^\s*$([regex]::Escape($Key))\s*="

    foreach ($line in $Lines) {
        if ($line -match $pattern) {
            $result.Add(("{0} = {1}" -f $Key, $Value))
            $found = $true
        }
        else {
            $result.Add($line)
        }
    }

    if (-not $found) {
        $result.Add(("{0} = {1}" -f $Key, $Value))
    }

    return $result
}

function Disable-XaeroOldDeathWaypoints {
    param(
        [Parameter(Mandatory = $true)][string]$InstanceRoot
    )

    $waypointRoot = Join-Path $InstanceRoot "xaero\minimap"
    if (-not (Test-Path -LiteralPath $waypointRoot)) {
        return 0
    }

    $disabledCount = 0
    Get-ChildItem -LiteralPath $waypointRoot -Filter "waypoints.txt" -File -Recurse | ForEach-Object {
        $lines = Get-Content -LiteralPath $_.FullName
        $changed = $false
        $nextLines = [System.Collections.Generic.List[string]]::new()

        foreach ($line in $lines) {
            if ($line -like "waypoint:gui.xaero_deathpoint_old:*") {
                $parts = $line -split ":"
                if ($parts.Count -gt 7 -and $parts[7] -ne "true") {
                    $parts[7] = "true"
                    $nextLines.Add(($parts -join ":"))
                    $changed = $true
                    $disabledCount += 1
                    continue
                }
            }
            $nextLines.Add($line)
        }

        if ($changed) {
            Write-Utf8NoBomLines -Path $_.FullName -Lines $nextLines
        }
    }

    return $disabledCount
}

function Apply-DeathWaypointPolicy {
    param(
        [Parameter(Mandatory = $true)][string]$PolicyPath,
        [Parameter(Mandatory = $true)][string]$InstanceRoot
    )

    if (-not (Test-Path -LiteralPath $PolicyPath)) {
        return
    }

    $policy = Get-Content -LiteralPath $PolicyPath -Raw | ConvertFrom-Json
    if ($policy.owner -ne "xaeros_minimap") {
        return
    }

    $profilePath = Join-Path $InstanceRoot "config\xaero\minimap\profiles\default.cfg"
    if (Test-Path -LiteralPath $profilePath) {
        $profileLines = Get-Content -LiteralPath $profilePath
        $profileLines = Set-KeyValueLine -Lines $profileLines -Key "deathpoints" -Value "true"
        $profileLines = Set-KeyValueLine -Lines $profileLines -Key "old_deathpoints" -Value "false"
        Write-Utf8NoBomLines -Path $profilePath -Lines $profileLines
    }

    $disabledCount = 0
    if ($policy.implemented_behavior.existing_old_deathpoints_disabled_on_sync -eq $true) {
        $disabledCount = Disable-XaeroOldDeathWaypoints -InstanceRoot $InstanceRoot
    }

    Write-Host "Applied Ascendant death waypoint policy: current death visible, old deathpoints hidden; $disabledCount existing old markers disabled."
}

function Get-TomlStringValue {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$Key
    )

    $match = [regex]::Match($Text, "(?m)^\s*$([regex]::Escape($Key))\s*=\s*`"([^`"]+)`"")
    if (-not $match.Success) {
        throw "Could not read $Key from Packwiz metadata."
    }
    return $match.Groups[1].Value
}

function Try-GetTomlStringValue {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$Key
    )

    $match = [regex]::Match($Text, "(?m)^\s*$([regex]::Escape($Key))\s*=\s*`"([^`"]+)`"")
    if (-not $match.Success) {
        return $null
    }
    return $match.Groups[1].Value
}

function Try-GetTomlScalarValue {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$Key
    )

    $quoted = Try-GetTomlStringValue -Text $Text -Key $Key
    if (-not [string]::IsNullOrWhiteSpace($quoted)) {
        return $quoted
    }

    $match = [regex]::Match($Text, "(?m)^\s*$([regex]::Escape($Key))\s*=\s*([^#\r\n]+)")
    if (-not $match.Success) {
        return $null
    }
    return $match.Groups[1].Value.Trim()
}

function Get-CurseForgeEdgeUrl {
    param(
        [Parameter(Mandatory = $true)][string]$Metadata,
        [Parameter(Mandatory = $true)][string]$Filename
    )

    $fileIdText = Try-GetTomlScalarValue -Text $Metadata -Key "file-id"
    if ([string]::IsNullOrWhiteSpace($fileIdText)) {
        return $null
    }

    $fileId = [int]$fileIdText
    $first = [math]::Floor($fileId / 1000)
    $last = ($fileId % 1000).ToString("000")
    $escapedFilename = [uri]::EscapeDataString($Filename).Replace("%2B", "+")
    return "https://edge.forgecdn.net/files/$first/$last/$escapedFilename"
}

function Install-PackwizClientJar {
    param(
        [Parameter(Mandatory = $true)][string]$MetadataPath,
        [Parameter(Mandatory = $true)][string]$DestinationModsPath
    )

    if (-not (Test-Path -LiteralPath $MetadataPath)) {
        return
    }

    $metadata = Get-Content -LiteralPath $MetadataPath -Raw
    $filename = Get-TomlStringValue -Text $metadata -Key "filename"
    $url = Try-GetTomlStringValue -Text $metadata -Key "url"
    if ([string]::IsNullOrWhiteSpace($url)) {
        $url = Get-CurseForgeEdgeUrl -Metadata $metadata -Filename $filename
    }
    $hashFormat = Get-TomlStringValue -Text $metadata -Key "hash-format"
    $expectedHash = (Get-TomlStringValue -Text $metadata -Key "hash").ToLowerInvariant()
    $destination = Join-Path $DestinationModsPath $filename

    $algorithm = switch ($hashFormat) {
        "sha512" { "SHA512" }
        "sha1" { "SHA1" }
        default { "" }
    }

    if (Test-Path -LiteralPath $destination) {
        $actualExistingHash = ""
        if (-not [string]::IsNullOrWhiteSpace($algorithm)) {
            $actualExistingHash = (Get-FileHash -LiteralPath $destination -Algorithm $algorithm).Hash.ToLowerInvariant()
        }
        if ($actualExistingHash -eq $expectedHash) {
            Write-Host "Client jar already present: $filename"
            return
        }
    }

    if ([string]::IsNullOrWhiteSpace($url)) {
        throw "No downloadable URL or CurseForge file id found for $filename."
    }

    New-Item -ItemType Directory -Force -Path $DestinationModsPath | Out-Null
    $tempFile = Join-Path $env:TEMP $filename
    Invoke-WebRequest -Uri $url -OutFile $tempFile

    if (-not [string]::IsNullOrWhiteSpace($algorithm)) {
        $actualHash = (Get-FileHash -LiteralPath $tempFile -Algorithm $algorithm).Hash.ToLowerInvariant()
        if ($actualHash -ne $expectedHash) {
            throw "Hash mismatch for $filename. Expected $expectedHash, got $actualHash."
        }
    }

    Copy-Item -LiteralPath $tempFile -Destination $destination -Force
    Write-Host "Installed client jar: $filename"
}

function Install-ExportedClientMods {
    param(
        [Parameter(Mandatory = $true)][string]$ExportZipPath,
        [Parameter(Mandatory = $true)][string]$DestinationModsPath
    )

    if (-not (Test-Path -LiteralPath $ExportZipPath)) {
        Write-Host "Client export zip not found; skipping exported mod jar sync: $ExportZipPath"
        return
    }

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    New-Item -ItemType Directory -Force -Path $DestinationModsPath | Out-Null

    $zip = [System.IO.Compression.ZipFile]::OpenRead($ExportZipPath)
    $installed = 0
    $unchanged = 0

    try {
        $entries = $zip.Entries |
            Where-Object { $_.FullName -like "overrides/mods/*.jar" -and -not [string]::IsNullOrWhiteSpace($_.Name) }

        foreach ($entry in $entries) {
            $destination = Join-Path $DestinationModsPath $entry.Name
            if (Test-Path -LiteralPath $destination) {
                $existing = Get-Item -LiteralPath $destination
                if ($existing.Length -eq $entry.Length) {
                    $unchanged += 1
                    continue
                }
            }

            $inputStream = $entry.Open()
            $outputStream = [System.IO.File]::Create($destination)
            try {
                $inputStream.CopyTo($outputStream)
            }
            finally {
                $outputStream.Dispose()
                $inputStream.Dispose()
            }

            $installed += 1
        }
    }
    finally {
        $zip.Dispose()
    }

    Write-Host "Synced exported Packwiz mod jars: $installed installed/updated, $unchanged already current."
}

function Install-PackwizResourcePack {
    param(
        [Parameter(Mandatory = $true)][string]$MetadataPath,
        [Parameter(Mandatory = $true)][string]$DestinationResourcePacksPath
    )

    if (-not (Test-Path -LiteralPath $MetadataPath)) {
        return
    }

    $metadata = Get-Content -LiteralPath $MetadataPath -Raw
    $filename = Get-TomlStringValue -Text $metadata -Key "filename"
    $url = Try-GetTomlStringValue -Text $metadata -Key "url"
    $hashFormat = Try-GetTomlStringValue -Text $metadata -Key "hash-format"
    $expectedHash = Try-GetTomlStringValue -Text $metadata -Key "hash"
    $destination = Join-Path $DestinationResourcePacksPath $filename

    if (Test-Path -LiteralPath $destination) {
        Write-Host "Resource pack already present: $filename"
        return
    }

    if ([string]::IsNullOrWhiteSpace($url)) {
        Write-Host "Skipping metadata-only resource pack download; import/export must provide it: $filename"
        return
    }

    New-Item -ItemType Directory -Force -Path $DestinationResourcePacksPath | Out-Null
    $tempFile = Join-Path $env:TEMP $filename
    Invoke-WebRequest -Uri $url -OutFile $tempFile

    if (-not [string]::IsNullOrWhiteSpace($expectedHash)) {
        $algorithm = switch ($hashFormat) {
            "sha512" { "SHA512" }
            "sha1" { "SHA1" }
            default { "" }
        }

        if (-not [string]::IsNullOrWhiteSpace($algorithm)) {
            $actualHash = (Get-FileHash -LiteralPath $tempFile -Algorithm $algorithm).Hash.ToLowerInvariant()
            if ($actualHash -ne $expectedHash.ToLowerInvariant()) {
                throw "Hash mismatch for $filename. Expected $expectedHash, got $actualHash."
            }
        }
    }

    Copy-Item -LiteralPath $tempFile -Destination $destination -Force
    Write-Host "Installed resource pack: $filename"
}

function Install-PackwizResourcePacks {
    param(
        [Parameter(Mandatory = $true)][string]$MetadataDirectory,
        [Parameter(Mandatory = $true)][string]$DestinationResourcePacksPath
    )

    if (-not (Test-Path -LiteralPath $MetadataDirectory)) {
        return
    }

    Get-ChildItem -LiteralPath $MetadataDirectory -Filter "*.pw.toml" -File |
        ForEach-Object {
            Install-PackwizResourcePack -MetadataPath $_.FullName -DestinationResourcePacksPath $DestinationResourcePacksPath
        }
}

Copy-Directory -Source (Join-Path $root "customnpcs") -Destination (Join-Path $target "customnpcs")
Copy-Directory -Source (Join-Path $root "kubejs") -Destination (Join-Path $target "kubejs")
Copy-Directory -Source (Join-Path $root "config\openloader") -Destination (Join-Path $target "config\openloader")
Remove-StaleAtlasStructureSets -InstanceRoot $target
Remove-AtlasWorldgenInfluenceIfDisabled -InstanceRoot $target
Copy-Directory -Source (Join-Path $root "config\ascendant_guild") -Destination (Join-Path $target "config\ascendant_guild")
Copy-Directory -Source (Join-Path $root "config\ascendant_core") -Destination (Join-Path $target "config\ascendant_core")
Copy-Directory -Source (Join-Path $root "config\ascendant_atlas") -Destination (Join-Path $target "config\ascendant_atlas")
Copy-Directory -Source (Join-Path $root "config\ascendant_index") -Destination (Join-Path $target "config\ascendant_index")
Copy-Directory -Source (Join-Path $root "config\ascendant_dungeons") -Destination (Join-Path $target "config\ascendant_dungeons")
Copy-Directory -Source (Join-Path $root "config\ascendant_structures") -Destination (Join-Path $target "config\ascendant_structures")
Copy-Directory -Source (Join-Path $root "config\ascendant_progression") -Destination (Join-Path $target "config\ascendant_progression")
Copy-Directory -Source (Join-Path $root "config\ascendant_ui") -Destination (Join-Path $target "config\ascendant_ui")
Copy-Directory -Source (Join-Path $root "config\xaero") -Destination (Join-Path $target "config\xaero")
Copy-Directory -Source (Join-Path $root "config\ascendant_settlements") -Destination (Join-Path $target "config\ascendant_settlements")
Copy-Directory -Source (Join-Path $root "config\incontrol") -Destination (Join-Path $target "config\incontrol")
Copy-Directory -Source (Join-Path $root "config\towns_and_towers") -Destination (Join-Path $target "config\towns_and_towers")
Copy-Directory -Source (Join-Path $root "config\puffish_skills") -Destination (Join-Path $target "config\puffish_skills")
Copy-Directory -Source (Join-Path $root "config\ascendant_skill_effects") -Destination (Join-Path $target "config\ascendant_skill_effects")
Copy-Directory -Source (Join-Path $root "config\fancymenu") -Destination (Join-Path $target "config\fancymenu")
Copy-Directory -Source (Join-Path $root "config\drippyloadingscreen") -Destination (Join-Path $target "config\drippyloadingscreen")
Copy-Directory -Source (Join-Path $root "config\sound_physics_remastered") -Destination (Join-Path $target "config\sound_physics_remastered")
Copy-Directory -Source (Join-Path $root "config\obscuria") -Destination (Join-Path $target "config\obscuria")
Copy-ResourcePacks -Source (Join-Path $root "resourcepacks") -Destination (Join-Path $target "resourcepacks")
Install-PackwizResourcePacks -MetadataDirectory (Join-Path $root "resourcepacks") -DestinationResourcePacksPath (Join-Path $target "resourcepacks")
Install-PackwizResourcePacks -MetadataDirectory (Join-Path $root "shaderpacks") -DestinationResourcePacksPath (Join-Path $target "shaderpacks")
Install-ExportedClientMods -ExportZipPath (Join-Path $root "dist\ascendant-realms-client.zip") -DestinationModsPath (Join-Path $target "mods")
Copy-File -Source (Join-Path $root "mods\ascendant-atlas-regions-0.1.0.jar") -Destination (Join-Path $target "mods\ascendant-atlas-regions-0.1.0.jar")
Copy-File -Source (Join-Path $root "mods\ascendant-nametags-0.1.0.jar") -Destination (Join-Path $target "mods\ascendant-nametags-0.1.0.jar")
Install-PackwizClientJar -MetadataPath (Join-Path $root "mods\elite-holograms.pw.toml") -DestinationModsPath (Join-Path $target "mods")

$trackedConfigFiles = @(
    "alexsmobs.toml",
    "amendments-client.toml",
    "CustomNpcs.cfg",
    "create_structures_arise-server.toml",
    "embeddium-options.json",
    "embeddium-mixins.properties",
    "entityculling.json",
    "everycomp-common.toml",
    "everycomp-entries.toml",
    "everycomp-hazardous.toml",
    "guardvillagers-common.toml",
    "integrated_villages-forge-1_20.toml",
    "irons_spellbooks-client.toml",
    "itemborders-common.toml",
    "lootbeams-client.toml",
    "majruszsdifficulty.json",
    "mobhealthbar-client.toml",
    "modernfix-common.toml",
    "modernfix-mixins.properties",
    "oculus.properties",
    "overflowingbars-client.toml",
    "resourcepackoverrides.json",
    "sodiumdynamiclights-client.toml",
    "sparsestructures.json5",
    "spawnbalanceutility-common.toml",
    "supplementaries-common.toml",
    "travelerstitles-forge-1_20.toml"
)

foreach ($configFile in $trackedConfigFiles) {
    Copy-File -Source (Join-Path $root "config\$configFile") -Destination (Join-Path $target "config\$configFile")
}
Sync-OptionsResourcePacks -Source (Join-Path $root "options.txt") -Destination (Join-Path $target "options.txt")
Apply-KeybindPolicy -PolicyPath (Join-Path $root "config\ascendant_ui\keybind_policy.json") -DestinationOptions (Join-Path $target "options.txt")
Apply-DeathWaypointPolicy -PolicyPath (Join-Path $root "config\ascendant_ui\death_waypoint_policy.json") -InstanceRoot $target
Install-PackwizClientJar -MetadataPath (Join-Path $root "mods\resource-pack-overrides.pw.toml") -DestinationModsPath (Join-Path $target "mods")

Write-Host "Client file sync completed."
