param(
    [string]$MinecraftInstall = "C:\Users\Jayden\curseforge\minecraft\Install",
    [string]$OutputJar = "mods\ascendant-nametags-0.1.0.jar"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ModRoot = Join-Path $RepoRoot "local-mods\ascendant-nametags"
$SourceRoot = Join-Path $ModRoot "src\main\java"
$ResourcesRoot = Join-Path $ModRoot "src\main\resources"
$BuildRoot = Join-Path $ModRoot "build"
$ClassesRoot = Join-Path $BuildRoot "classes"
$ResolvedOutputJar = [System.IO.Path]::GetFullPath((Join-Path $RepoRoot $OutputJar))

if (-not $ResolvedOutputJar.StartsWith($RepoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to write Ascendant Nametags jar outside the repo: $ResolvedOutputJar"
}

if (-not (Test-Path -LiteralPath $MinecraftInstall)) {
    throw "Minecraft install libraries folder was not found: $MinecraftInstall"
}

$javac = Get-Command javac -ErrorAction SilentlyContinue
if (-not $javac) {
    throw "javac is required. Install or select a Java 17 JDK before building Ascendant Nametags."
}

Add-Type -AssemblyName System.IO.Compression.FileSystem

function Test-ZipJar {
    param([Parameter(Mandatory = $true)][string]$Path)

    try {
        $zip = [System.IO.Compression.ZipFile]::OpenRead($Path)
        $zip.Dispose()
        return $true
    }
    catch {
        return $false
    }
}

$libraryJars = Get-ChildItem -LiteralPath (Join-Path $MinecraftInstall "libraries") -Recurse -Filter "*.jar" |
    Where-Object {
        $_.Length -gt 0 -and
        (Test-ZipJar -Path $_.FullName) -and
        $_.FullName -notmatch "\\net\\minecraftforge\\forge\\1\.12\.2-" -and
        $_.FullName -notmatch "\\net\\minecraftforge\\[^\\]+\\1\.20\.1-47\.4\.(0|10)\\"
    } |
    ForEach-Object { $_.FullName }

if (-not $libraryJars -or $libraryJars.Count -eq 0) {
    throw "No Minecraft/Forge library jars were found under $MinecraftInstall\libraries."
}

if (Test-Path -LiteralPath $BuildRoot) {
    Remove-Item -LiteralPath $BuildRoot -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $ClassesRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $ResolvedOutputJar) | Out-Null

$sources = Get-ChildItem -LiteralPath $SourceRoot -Recurse -Filter "*.java" | ForEach-Object { $_.FullName }
if (-not $sources -or $sources.Count -eq 0) {
    throw "No Java sources found under $SourceRoot."
}

function Quote-JavacArg {
    param([Parameter(Mandatory = $true)][string]$Value)
    return '"' + ($Value -replace '\\', '\\' -replace '"', '\"') + '"'
}

$classpath = ($libraryJars -join ";")
$argFile = Join-Path $BuildRoot "javac.args"
$javacArgs = New-Object System.Collections.Generic.List[string]
$javacArgs.Add("-encoding")
$javacArgs.Add("UTF-8")
$javacArgs.Add("-source")
$javacArgs.Add("17")
$javacArgs.Add("-target")
$javacArgs.Add("17")
$javacArgs.Add("-classpath")
$javacArgs.Add((Quote-JavacArg $classpath))
$javacArgs.Add("-d")
$javacArgs.Add((Quote-JavacArg $ClassesRoot))
foreach ($source in $sources) {
    $javacArgs.Add((Quote-JavacArg $source))
}
[System.IO.File]::WriteAllLines($argFile, [string[]]$javacArgs, [System.Text.UTF8Encoding]::new($false))

& $javac.Source "@$argFile"
if ($LASTEXITCODE -ne 0) {
    throw "Ascendant Nametags javac build failed."
}

$manifestPath = Join-Path $BuildRoot "MANIFEST.MF"
@(
    "Manifest-Version: 1.0",
    "Specification-Title: Ascendant Nametags",
    "Specification-Version: 0.1.0",
    "Implementation-Title: Ascendant Nametags",
    "Implementation-Version: 0.1.0",
    ""
) | Set-Content -LiteralPath $manifestPath -Encoding ASCII

if (Test-Path -LiteralPath $ResolvedOutputJar) {
    Remove-Item -LiteralPath $ResolvedOutputJar -Force
}

& jar --create --file $ResolvedOutputJar --manifest $manifestPath -C $ClassesRoot . -C $ResourcesRoot .
if ($LASTEXITCODE -ne 0) {
    throw "Ascendant Nametags jar packaging failed."
}

Write-Host "Built $OutputJar"
