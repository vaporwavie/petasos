#!/usr/bin/env bash
# usage: petasos/sync.sh
# Merges fathah/hermes-desktop main into the current branch.
set -euo pipefail

git fetch --quiet --no-tags https://github.com/fathah/hermes-desktop.git "+refs/heads/main:refs/remotes/upstream/main"
git merge --no-edit -m "chore(petasos): sync upstream" upstream/main
