param(
    [string]$RepoName = "AI-Career-Risk-Analytics",
    [switch]$Private
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

git init
git add .
git commit -m "Initial AI career risk analytics project"

$Visibility = if ($Private) { "--private" } else { "--public" }
gh auth status
gh repo create $RepoName $Visibility --source . --remote origin --push

Write-Host "Uploaded to GitHub repo: $RepoName"

