#!/bin/bash
# READ-ONLY server health snapshot. Prints no secret values: env files are
# reduced to KEY NAMES and a few non-sensitive switches.
cd /home/consicac/nebians_api || exit 1
echo "== load / memory"; uptime; free -m 2>/dev/null | head -3
echo "== lve limits"; (lveinfo 2>/dev/null | head -3) || true
echo "== processes (count by kind)"
ps -u consicac -o pid,etimes,rss,nlwp,args --sort=-rss 2>/dev/null | cut -c1-150 | head -14
echo "threads total: $(ps -u consicac -L 2>/dev/null | wc -l)"
echo "== disk"; df -h /home 2>/dev/null | tail -1; du -sh staticfiles logs tmp 2>/dev/null
echo "== env switches (names only, selected values)"
grep -E '^[A-Z_]+=' .env 2>/dev/null | sed -E 's/=.*//' | tr '\n' ' '; echo
for k in CACHE_BACKEND DB_CONN_MAX_AGE DB_HOST DEBUG PAGE_CACHE_TTL STATIC_MINIFY; do grep -E "^$k=" .env 2>/dev/null | sed -E 's/^(DB_PASSWORD).*/\1=***/'; done
echo "ABLY keys set: $(grep -cE '^ABLY_API_KEYS?=.+' .env 2>/dev/null)"
echo "== redis"; (redis-cli -h 127.0.0.1 ping 2>&1 | head -1) || true
echo "== mysql ping + slow bits"
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python manage.py shell 2>&1 <<'PY' | tail -40
import time
from django.db import connection
from django.core.cache import cache
from django.conf import settings
t=time.time(); 
with connection.cursor() as c:
    c.execute("SELECT 1"); c.fetchone()
print("db roundtrip ms", round((time.time()-t)*1000,1))
print("cache backend", settings.CACHES['default']['BACKEND'])
t=time.time(); cache.set('diag',1,5); cache.get('diag'); print("cache rt ms", round((time.time()-t)*1000,1))
from django.test.utils import CaptureQueriesContext
from rest_framework.test import APIRequestFactory
from api.views_forum import posts_endpoint
f=APIRequestFactory()
for n in range(3):
    with CaptureQueriesContext(connection) as q:
        t=time.time(); r=posts_endpoint(f.get('/api/posts/')); r.render(); dt=(time.time()-t)*1000
    print("posts_endpoint run",n,"ms",round(dt),"queries",len(q), "bytes",len(r.content))
    if n==0:
        for x in sorted(q.captured_queries,key=lambda z:-float(z['time']))[:4]:
            print("  slow q", x['time'], x['sql'][:140].replace('\n',' '))
with connection.cursor() as c:
    c.execute("SELECT table_name, ROUND((data_length+index_length)/1048576,1) mb, table_rows FROM information_schema.tables WHERE table_schema=DATABASE() ORDER BY (data_length+index_length) DESC LIMIT 8")
    for row in c.fetchall(): print("table", row)
PY
echo "== recent errors in logs"
for f in logs/*.log; do [ -f "$f" ] && echo "$f $(du -h "$f" | cut -f1)"; done 2>/dev/null | head -10
tail -n 5 logs/django_errors.log 2>/dev/null | cut -c1-200
echo "== done"
