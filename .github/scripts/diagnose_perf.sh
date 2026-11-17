#!/bin/bash
# READ-ONLY. Numbers and names only: no env values (except LSAPI_* tuning), no .htaccess, no credentials.
cd /home/consicac/nebians_api || exit 1
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
echo "== load"; cat /proc/loadavg
echo "== LSAPI tuning seen by our lswsgi processes (LSAPI_* only)"
for p in $(pgrep -u consicac -f 'lswsgi -m /home/consicac/nebians_api' | head -3); do
  echo "pid $p: $(tr '\0' '\n' < /proc/$p/environ 2>/dev/null | grep -E '^(LSAPI_|LSWSGI_|NEB_WARMUP|DB_CONN_MAX_AGE|DEBUG$)' | tr '\n' ' ')"
done
echo "== stderr.log: max-children warnings"
ls -la --time-style=long-iso stderr.log 2>/dev/null | awk '{print $5, $6, $7}'
grep -c 'max children' stderr.log 2>/dev/null
grep -o 'Reached max children process limit: [0-9]*, extra: [0-9]*' stderr.log 2>/dev/null | sort | uniq -c | head -5
echo "== access logs available (names/sizes)"
ls -la --time-style=long-iso ~/access-logs/ ~/logs/ 2>/dev/null | awk '{print $5, $6, $7, $8}' | head -14
echo "== slowest app endpoints by access log time (if the log carries it)"
timeout 60 python - <<'PY' 2>&1 | cut -c1-200 | tail -40
import glob, os, re, collections
cands = [f for f in glob.glob(os.path.expanduser('~/access-logs/*')) + glob.glob(os.path.expanduser('~/logs/*'))
         if os.path.isfile(f) and 'nebians' in f and not f.endswith(('.gz', 'ftpxferlog'))]
print('candidates', [os.path.basename(c) for c in cands][:6])
for f in cands[:2]:
    try:
        size = os.path.getsize(f)
        with open(f, 'rb') as fh:
            fh.seek(max(0, size - 6_000_000))
            lines = fh.read().decode('utf-8', 'ignore').splitlines()[1:]
    except Exception as e:
        print('read failed', type(e).__name__); continue
    print(os.path.basename(f), 'lines', len(lines))
    if lines: print('sample:', re.sub(r'^\S+', 'IP', lines[-1])[:180])
    c = collections.Counter(); st = collections.Counter(); byt = collections.Counter()
    rx = re.compile(r'"(?:GET|POST|PUT|PATCH|DELETE|HEAD) (\S+)[^"]*" (\d{3}) (\d+|-)')
    for l in lines:
        m = rx.search(l)
        if not m: continue
        path = re.sub(r'\d+', 'N', m.group(1).split('?')[0])[:60]
        c[path] += 1; st[m.group(2)] += 1
        if m.group(3).isdigit(): byt[path] += int(m.group(3))
    print('status', dict(st.most_common(8)))
    for p, n in c.most_common(14): print('  %5d  %6.1f MB  %s' % (n, byt[p] / 1e6, p))
    print('top by bytes:')
    for p, n in byt.most_common(8): print('  %6.1f MB  %5d  %s' % (n / 1e6, c[p], p))
PY
echo "== database facts"
timeout 60 python - <<'PY' 2>&1 | cut -c1-200 | tail -40
import os, sys
sys.path.insert(0, '/home/consicac/nebians_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
import django; django.setup()
from django.db import connection as c
cur = c.cursor()
for q in ("SHOW GLOBAL VARIABLES WHERE Variable_name IN ('max_connections','max_user_connections','wait_timeout','innodb_buffer_pool_size','slow_query_log','long_query_time','query_cache_type')",
          "SHOW GLOBAL STATUS WHERE Variable_name IN ('Threads_connected','Threads_running','Slow_queries','Max_used_connections','Aborted_connects','Connections','Uptime')"):
    cur.execute(q); print({r[0]: r[1] for r in cur.fetchall()})
cur.execute("SELECT table_name, table_rows, ROUND((data_length+index_length)/1048576,1) mb FROM information_schema.tables WHERE table_schema=DATABASE() ORDER BY (data_length+index_length) DESC LIMIT 14")
for r in cur.fetchall(): print('  table', r[0], 'rows~', r[1], 'MB', r[2])
cur.execute("SELECT COUNT(*) FROM information_schema.processlist WHERE user=SUBSTRING_INDEX(USER(),'@',1)")
print('my connections now', cur.fetchone()[0])
PY
echo "== warm endpoint timings (2nd call), SQL count and SQL ms, anonymous"
timeout 170 python - <<'PY' 2>&1 | cut -c1-200 | tail -50
import os, sys, time
sys.path.insert(0, '/home/consicac/nebians_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
from nebians.wsgi import application
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.test import Client
cl = Client(HTTP_HOST='nebians.consica.com.np')
paths = ['/api/realtime/config/', '/api/posts/', '/api/posts/?page=2', '/app/', '/app/library/', '/app/news/', '/app/search/',
         '/app/syllabus/8/nepali/unit-11/', '/app/forum/', '/api/news/', '/api/notifications/unread-count/', '/api/search/?q=math']
for p in paths:
    try:
        cl.get(p, secure=True)
        with CaptureQueriesContext(connection) as ctx:
            t = time.time(); r = cl.get(p, secure=True); ms = round((time.time() - t) * 1000)
        sql = sum(float(q['time']) for q in ctx.captured_queries) * 1000
        body = len(getattr(r, 'content', b'') or b'')
        print('%-34s %s %5d ms  sql %3d q %5.0f ms  %6d B' % (p, r.status_code, ms, len(ctx.captured_queries), sql, body))
    except Exception as e:
        print(p, 'ERR', type(e).__name__, str(e)[:80])
PY
echo "== done"
