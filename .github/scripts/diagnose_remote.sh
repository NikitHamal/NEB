#!/bin/bash
# READ-ONLY server snapshot. Output goes through a redactor in the workflow, and
# nothing here prints env files, .htaccess or credentials.
cd /home/consicac/nebians_api || exit 1
for f in watchdog.sh scratch/guard_neby_tasks.sh; do
  echo "== $f ($(wc -l < $f 2>/dev/null) lines)"; grep -vE '^\s*#|^\s*$' "$f" 2>/dev/null | cut -c1-170 | head -40
done
echo "== watchdog log tail"; tail -n 6 logs/watchdog.log 2>/dev/null | cut -c1-170
echo "== WS_PUBLIC_URL set anywhere?"
grep -lE 'WS_PUBLIC_URL[= ]+[^ ]+' .env ../nebians.consica.com.np/.htaccess 2>/dev/null | sed 's#.*/##' | tr '\n' ' '; echo "(file names only)"
echo "== done"
