#!/usr/bin/env bash
# Explicit, one-time publish. Requires local gh authentication and git.
set -euo pipefail
OWNER="${GITHUB_OWNER:-lenixeduardo}"
REPO="${GITHUB_REPO:-auto-validate}"
FULL="$OWNER/$REPO"
cd "$(dirname "$0")"
if ! command -v gh >/dev/null 2>&1; then
  echo 'Instale o GitHub CLI (gh) e autentique com: gh auth login' >&2
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo 'Autentique com: gh auth login' >&2
  exit 1
fi
if gh repo view "$FULL" >/dev/null 2>&1; then
  echo "Repositório $FULL já existe. Publicação interrompida para evitar sobrescrita." >&2
  exit 1
fi
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then git init -b main; fi
git add .
if ! git diff --cached --quiet; then git commit -m 'feat: publish Auto-Validate with reproducible demos'; fi
gh repo create "$FULL" --public --source . --remote origin --push
gh repo edit "$FULL" --description "$(cat .github/repo-about.txt)"
gh api -X PUT "repos/$FULL/topics" --input .github/repo-topics.json >/dev/null
printf '\nRepositório publicado: https://github.com/%s\n' "$FULL"
printf 'Defina o social preview em Settings > General com assets/cover.png\n'
