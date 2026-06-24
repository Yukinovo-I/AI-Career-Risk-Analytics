param(
    [string]$RepoName = "AI-Career-Risk-Analytics",
    [string]$Owner = "Yukinovo-I",
    [switch]$Private
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Test-Path ".git")) {
    git init
    git branch -m main
}

git add .
$HasStagedChanges = git diff --cached --quiet; $StagedExit = $LASTEXITCODE
if ($StagedExit -ne 0) {
    git commit -m "Update AI career risk analytics project"
}

$Visibility = if ($Private) { "--private" } else { "--public" }
$FullRepo = "$Owner/$RepoName"

gh auth status
$PreviousErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"
gh repo view $FullRepo *> $null
$RepoExists = $LASTEXITCODE -eq 0
$ErrorActionPreference = $PreviousErrorActionPreference
if (-not $RepoExists) {
    if ((git remote) -contains "origin") {
        gh repo create $FullRepo $Visibility --source .
    } else {
        gh repo create $FullRepo $Visibility --source . --remote origin
    }
}

if ((git remote) -contains "origin") {
    git remote set-url origin "https://github.com/$FullRepo.git"
} else {
    git remote add origin "https://github.com/$FullRepo.git"
}
git push -u origin main

Write-Host "Uploaded to GitHub repo: https://github.com/$FullRepo"
