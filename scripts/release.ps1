# Обновление версии и создание релиза (PowerShell).
# Использование: .\scripts\release.ps1 patch|minor|major|X.Y.Z [-NoGit] [-Release] [-DryRun]

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateNotNullOrEmpty()]
    [string]$Bump,

    [switch]$NoGit,
    [switch]$Release,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$PyprojectPath = Join-Path $RepoRoot "pyproject.toml"
$InitPyPath = Join-Path $RepoRoot "src\wbsdk\__init__.py"

Set-Location $RepoRoot

if (-not (Test-Path $PyprojectPath)) {
    Write-Error "Ошибка: pyproject.toml не найден в $RepoRoot"
    exit 1
}
if (-not (Test-Path $InitPyPath)) {
    Write-Error "Ошибка: src\wbsdk\__init__.py не найден"
    exit 1
}

# Чтение текущей версии из pyproject.toml
$pyprojectContent = Get-Content -Raw -Encoding UTF8 $PyprojectPath
if ($pyprojectContent -notmatch 'version\s*=\s*"([^"]+)"') {
    Write-Error "Ошибка: не удалось прочитать version из pyproject.toml"
    exit 1
}
$CurrentVersion = $Matches[1]

# Вычисление новой версии
function Get-NewVersion {
    param([string]$BumpType, [string]$Current)

    if ($BumpType -match '^\d+\.\d+\.\d+$') {
        return $BumpType
    }

    $parts = $Current -split '\.'
    $major = [int]($parts[0])
    $minor = if ($parts.Length -gt 1) { [int]($parts[1]) } else { 0 }
    $patch = if ($parts.Length -gt 2) { [int]($parts[2]) } else { 0 }

    switch ($BumpType) {
        "patch" {
            $patch++
            return "$major.$minor.$patch"
        }
        "minor" {
            $minor++
            $patch = 0
            return "$major.$minor.$patch"
        }
        "major" {
            $major++
            $minor = 0
            $patch = 0
            return "$major.$minor.$patch"
        }
        default {
            Write-Error "Некорректный тип версии: $BumpType. Ожидается patch, minor, major или X.Y.Z"
            exit 1
        }
    }
}

$validBumps = @("patch", "minor", "major")
if ($validBumps -notcontains $Bump -and $Bump -notmatch '^\d+\.\d+\.\d+$') {
    Write-Error "Некорректный аргумент: $Bump. Ожидается patch, minor, major или X.Y.Z"
    exit 1
}

$NewVersion = Get-NewVersion -BumpType $Bump -Current $CurrentVersion

Write-Host "Текущая версия: $CurrentVersion"
Write-Host "Новая версия:  $NewVersion"

if ($DryRun) {
    Write-Host "[dry-run] Будет обновлено: pyproject.toml, src\wbsdk\__init__.py"
    if (-not $NoGit) {
        Write-Host "[dry-run] Будет: git add, commit «Bump version to $NewVersion», tag v$NewVersion, push"
    }
    if ($Release) {
        Write-Host "[dry-run] Будет: gh release create v$NewVersion --generate-notes"
    }
    exit 0
}

# Обновление pyproject.toml
$pyprojectContent = $pyprojectContent -replace ('version\s*=\s*"' + [regex]::Escape($CurrentVersion) + '"'), "version = `"$NewVersion`""
# Сохраняем без лишнего перевода строки в конце
[System.IO.File]::WriteAllText($PyprojectPath, $pyprojectContent, [System.Text.UTF8Encoding]::new($false))

# Обновление __init__.py
$initContent = Get-Content -Raw -Encoding UTF8 $InitPyPath
$initContent = $initContent -replace ('__version__\s*=\s*"' + [regex]::Escape($CurrentVersion) + '"'), "__version__ = `"$NewVersion`""
[System.IO.File]::WriteAllText($InitPyPath, $initContent, [System.Text.UTF8Encoding]::new($false))

Write-Host "Обновлены pyproject.toml и src\wbsdk\__init__.py"

if ($NoGit) {
    Write-Host "Флаг -NoGit: git-операции пропущены."
    exit 0
}

# Git: add, commit, tag, push
git add $PyprojectPath $InitPyPath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git commit -m "Bump version to $NewVersion"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git tag -a "v$NewVersion" -m "Release v$NewVersion"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git push
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git push --tags
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if ($Release) {
    $gh = Get-Command gh -ErrorAction SilentlyContinue
    if (-not $gh) {
        Write-Error "Ошибка: gh (GitHub CLI) не найден. Установите gh и выполните авторизацию."
        exit 1
    }
    gh release create "v$NewVersion" --generate-notes
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "GitHub Release v$NewVersion создан. Workflow публикации в PyPI должен запуститься."
}
