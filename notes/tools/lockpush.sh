#!/usr/bin/env bash
# Commit and push named paths from several agents working in one clone, one at a time.
#   notes/tools/lockpush.sh "notes: cee-phy unit 4 — Fluid Statics and Dynamics" notes/content/cee-phy/unit-04.md ...
# Serialises git through a lock file, commits only the paths given, rebases on the
# remote branch if it moved, and pushes. Never stages anything else in the tree.
set -euo pipefail
msg="$1"; shift
cd "$(git rev-parse --show-toplevel)"
branch="$(git rev-parse --abbrev-ref HEAD)"
exec 9>/tmp/neb-git.lock
flock -w 600 9
git add -- "$@"
if git diff --cached --quiet; then
  echo "lockpush: nothing to commit for: $*"
else
  git commit -q -m "$msg" -- "$@"
fi
for i in 1 2 3; do
  if git push -q origin "$branch" 2>/tmp/neb-push.err; then
    echo "lockpush: pushed $(git rev-parse --short HEAD) to $branch"
    exit 0
  fi
  git pull -q --rebase origin "$branch" || true
  sleep 3
done
sed 's/ghp_[A-Za-z0-9]*/***/g' /tmp/neb-push.err >&2
exit 1
