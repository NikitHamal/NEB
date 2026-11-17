#!/bin/bash
# READ-ONLY server snapshot #2. Env files are reduced to key names; no values printed.
cd /home/consicac/nebians_api || exit 1
echo "== env key names"; grep -E '^[A-Z_0-9]+=' .env 2>/dev/null | sed -E 's/=.*//' | tr '\n' ' '; echo
for k in WS_PUBLIC_URL PAGE_CACHE_TTL STATIC_MINIFY CACHE_LOCATION REDIS_URL SESSION_ENGINE; do v=$(grep -E "^$k=" .env | head -1 | sed -E 's/:[^:@/]*@/:***@/'); echo "${v:-$k=<unset>}"; done
echo "== crontab (commands only)"; crontab -l 2>/dev/null | grep -v '^#' | cut -c1-200
echo "== lsapi/htaccess"; grep -iE "lsapi|PassengerEnv|SetEnv|python|restart" .htaccess ../nebians.consica.com.np/.htaccess 2>/dev/null | cut -c1-200 | head -15
echo "== process counts"; ps -u consicac -o args 2>/dev/null | awk '{print $1" "$2" "$3}' | sed -E 's#.*/##' | sort | uniq -c | sort -rn | head -10
echo "== lswsgi ages (nebians_api)"; ps -u consicac -o etimes,rss,args 2>/dev/null | grep "nebians_api/passenger" | grep -v grep | awk '{print $1"s "$2"KB"}' | tr '\n' ' '; echo
echo "== log errors last 400 lines of nebians.log (counts)"
tail -n 400 logs/nebians.log 2>/dev/null | grep -oE "(ERROR|WARNING|CRITICAL) [a-zA-Z_.]+" | sort | uniq -c | sort -rn | head -8
tail -n 400 logs/nebians.log 2>/dev/null | grep -iE "error|timeout|too many|lost connection|killed" | tail -6 | cut -c1-220
echo "== daphne"; tail -n 3 logs/daphne.log 2>/dev/null | cut -c1-200
echo "== mysql"
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
python manage.py shell 2>&1 <<'PY' | tail -25
from django.db import connection
with connection.cursor() as c:
    for q in ("SHOW VARIABLES LIKE 'max_user_connections'","SHOW VARIABLES LIKE 'max_connections'","SHOW STATUS LIKE 'Threads_connected'","SHOW STATUS LIKE 'Slow_queries'","SELECT COUNT(*) FROM page_views","SELECT COUNT(*) FROM agent_actions"):
        c.execute(q); print(q[:40], c.fetchall())
PY
echo "== done"
