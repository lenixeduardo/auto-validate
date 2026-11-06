# Publicação explícita no GitHub. Requer Git + GitHub CLI autenticado.
$ErrorActionPreference = 'Stop'
$owner = if ($env:GITHUB_OWNER) { $env:GITHUB_OWNER } else { 'lenixeduardo' }
$repo = if ($env:GITHUB_REPO) { $env:GITHUB_REPO } else { 'auto-validate' }
$full = "$owner/$repo"
Set-Location $PSScriptRoot
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw 'Instale o GitHub CLI (gh) e execute: gh auth login' }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Instale o Git.' }
& gh auth status 2>$null
if ($LASTEXITCODE -ne 0) { throw 'Autentique no GitHub com: gh auth login' }
& gh repo view $full *> $null
if ($LASTEXITCODE -eq 0) { throw "Repositório $full já existe. A publicação foi interrompida para evitar sobrescrita." }
& git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) { & git init -b main; if ($LASTEXITCODE -ne 0) { throw 'git init falhou' } }
& git add .
if ($LASTEXITCODE -ne 0) { throw 'git add falhou' }
& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { & git commit -m 'feat: publish Auto-Validate with reproducible demos'; if ($LASTEXITCODE -ne 0) { throw 'git commit falhou; configure user.name e user.email' } }
& gh repo create $full --public --source . --remote origin --push
if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar/enviar o repositório' }
$description = (Get-Content '.github/repo-about.txt' -Raw -Encoding utf8).Trim()
& gh repo edit $full --description $description
& gh api -X PUT "repos/$full/topics" --input .github/repo-topics.json
Write-Host "Repositório publicado: https://github.com/$full"
Write-Host 'Para social preview: Settings > General > Social preview > Upload assets/cover.png'
