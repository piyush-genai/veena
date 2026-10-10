#!/usr/bin/env bash
# Usage: ./push_to_github.sh <github-username> [repo-name]
# Creates a PRIVATE repo with the GitHub CLI (gh auth login first) and pushes.
set -euo pipefail
USER_NAME="${1:?GitHub username required}"
REPO="${2:-veena}"
git init -b main
git add .
git commit -m "Initial Veena scaffold: architecture, roadmap, Phase 0 guide, kickoff prompt"
if command -v gh >/dev/null 2>&1; then
  gh repo create "$USER_NAME/$REPO" --private --source=. --remote=origin --push
else
  echo "gh not found. Create an empty private repo named '$REPO' on github.com, then run:"
  echo "  git remote add origin git@github.com:$USER_NAME/$REPO.git && git push -u origin main"
fi
