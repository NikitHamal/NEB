#!/bin/bash
# READ-ONLY server snapshot. Output goes through a redactor in the workflow, and
# nothing here prints env files, .htaccess or credentials (names or safe numbers only).
cd /home/consicac/nebians_api || exit 1
echo "== load / memory"
cat /proc/loadavg; free -m | sed -n 1,3p; nproc
echo "== our processes (rss kB, etime, command name)"
ps -u consicac -o rss=,etime=,comm= --sort=-rss 2>/dev/null | head -14
echo "== process counts by name"
ps -u consicac -o comm= | sort | uniq -c | sort -rn | head -8
echo "== redis?"
(pgrep -x redis-server >/dev/null && echo "redis-server running") || echo "no redis-server for this user"
echo "== env var names set in .env (names only)"
grep -oE '^[A-Z_]+=' .env 2>/dev/null | tr -d '=' | tr '\n' ' '; echo
echo "== safe env values"
grep -E '^(CACHE_BACKEND|DB_CONN_MAX_AGE|SESSION_ENGINE|PAGE_CACHE_TTL|DEBUG)=' .env 2>/dev/null | sed -E 's/(REDIS|LOCATION).*/\1=***/'
echo "== lsapi tuning names in htaccess (names + numbers)"
grep -oE 'LSAPI_[A-Z_]+[ =]+[0-9]+' ../nebians.consica.com.np/.htaccess 2>/dev/null | head
echo "== django view"
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
timeout 150 python manage.py shell -c "
import time
t0=time.time()
from django.conf import settings
print('cache', settings.CACHES['default']['BACKEND'])
db=settings.DATABASES['default']; print('db', db['ENGINE'].split('.')[-1], 'CONN_MAX_AGE', db.get('CONN_MAX_AGE'))
from django.db import connection
t=time.time(); c=connection.cursor(); c.execute('select 1'); print('db connect+select1 ms', round((time.time()-t)*1000))
t=time.time(); c.execute('select 1'); print('select1 again ms', round((time.time()-t)*1000))
c.execute('select table_name, round((data_length+index_length)/1048576,1) mb, table_rows from information_schema.tables where table_schema=database() order by (data_length+index_length) desc limit 12')
for r in c.fetchall(): print('tbl', r)
c.execute('select count(*) from django_session'); print('sessions rows', c.fetchone()[0])
c.execute('select count(*) from django_session where expire_date < now()'); print('expired sessions', c.fetchone()[0])
from django.test import Client
from django.test.utils import CaptureQueriesContext
cl=Client(HTTP_HOST='nebians.consica.com.np', HTTP_X_FORWARDED_PROTO='https')
for p in ['/', '/api/posts/', '/api/realtime/config/', '/app/forum/', '/app/library/', '/app/news/']:
    for i in range(2):
        with CaptureQueriesContext(connection) as q:
            t=time.time(); r=cl.get(p, secure=True); ms=round((time.time()-t)*1000)
        print('GET', p, i, r.status_code, ms, 'ms', len(q), 'queries', len(r.content), 'bytes')
" 2>&1 | cut -c1-220 | tail -50
echo "== done"
