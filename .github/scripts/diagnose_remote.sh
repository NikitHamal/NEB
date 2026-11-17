#!/bin/bash
# READ-ONLY server snapshot. Output goes through a redactor in the workflow, and
# nothing here prints env files, .htaccess or credentials (names or safe numbers only).
cd /home/consicac/nebians_api || exit 1
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
echo "== load"; cat /proc/loadavg
echo "== lswsgi tree (pid ppid etime rss args)"
ps -u consicac -o pid=,ppid=,etime=,rss=,args= 2>/dev/null | grep -E 'lswsgi|daphne' | grep -v grep | cut -c1-150 | head -20
echo "== limits and memory (account shared with other apps)"
ulimit -u 2>/dev/null | sed 's/^/ulimit -u /'; echo "procs of this user: $(ps -u consicac -o pid= 2>/dev/null | wc -l), threads: $(ps -u consicac -L -o tid= 2>/dev/null | wc -l)"
free -m 2>/dev/null | head -3
cat /proc/self/cgroup 2>/dev/null | head -3
for f in memory.max memory.current pids.max pids.current cpu.max; do for d in /sys/fs/cgroup /sys/fs/cgroup/$(cut -d: -f3 /proc/self/cgroup | head -1); do [ -r "$d/$f" ] && echo "$f=$(cat $d/$f 2>/dev/null)" && break; done; done
echo "== cron (names only, secrets masked) and watchdog"
crontab -l 2>/dev/null | sed -E 's/(KEY|TOKEN|SECRET|PASS)[A-Za-z_]*=[^ ]*/\1=***/Ig' | cut -c1-170 | head -20
[ -f watchdog.sh ] && sed -E 's/(KEY|TOKEN|SECRET|PASS)[A-Za-z_]*=[^ ]*/\1=***/Ig' watchdog.sh | cut -c1-170 | head -30
echo "== app logs (sizes only)"; ls -la logs 2>/dev/null | cut -c1-120 | head -15
echo "== recent 503 or limit hints in app stderr (last 8 lines)"; tail -n 8 stderr.log 2>/dev/null | cut -c1-200
echo "== traffic (page views, last 3 h, 30 min buckets) and log warnings"
timeout 100 python - <<'PY' 2>&1 | cut -c1-200 | tail -50
import os, sys, time, collections
sys.path.insert(0, '/home/consicac/nebians_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
import django; django.setup()
from api.models import PageView
now = int(time.time() * 1000); since = now - 3 * 3600 * 1000
rows = list(PageView.objects.filter(created_at__gte=since).values_list('created_at', 'is_bot', 'path', 'source', 'referrer_type', 'device_class'))
print('rows', len(rows), 'bots', sum(1 for r in rows if r[1]))
b = collections.Counter(((now - r[0]) // 1800000, r[1]) for r in rows)
for k in sorted({k[0] for k in b}): print('  bucket -%d0 min: humans %d bots %d' % (k * 3, b[(k, False)], b[(k, True)]))
print('top human paths:', collections.Counter(r[2][:50] for r in rows if not r[1]).most_common(8))
print('top bot paths:', collections.Counter(r[2][:50] for r in rows if r[1]).most_common(8))
print('sources:', collections.Counter(r[3] for r in rows).most_common(4), 'devices:', collections.Counter(r[5] for r in rows).most_common(4))
PY
for pat in 'Too many connections' 'OperationalError' 'Timeout' 'slow' 'WARNING' 'ERROR'; do echo "nebians.log last 20000 lines '$pat': $(tail -n 20000 logs/nebians.log 2>/dev/null | grep -c "$pat")"; done
tail -n 6 logs/server_errors.log 2>/dev/null | cut -c1-220
echo "== log message census (last 20000 lines of nebians.log)"
timeout 60 python - <<'PY' 2>&1 | cut -c1-230 | tail -40
import re, collections
lines = open('/home/consicac/nebians_api/logs/nebians.log', errors='replace').read().splitlines()[-20000:]
c = collections.Counter(); first = {}; last = {}
for l in lines:
    m = re.match(r'\[?(\d{4}-\d\d-\d\d[ T]\d\d:\d\d)[^\]]*\]?\s+(WARNING|ERROR|CRITICAL)\s+(\S+)\s+(.*)', l)
    if not m: continue
    key = (m.group(2), m.group(3), re.sub(r'[0-9a-f]{8,}|\d+', 'N', m.group(4))[:110])
    c[key] += 1; first.setdefault(key, m.group(1)); last[key] = m.group(1)
for k, n in c.most_common(18): print(n, k[0], k[1], '|', k[2], '|', first[k], '->', last[k])
PY
echo "== users.employment column"
timeout 40 python - <<'PY' 2>&1 | tail -5
import os, sys
sys.path.insert(0, '/home/consicac/nebians_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
import django; django.setup()
from django.db import connection
with connection.cursor() as c:
    c.execute("SHOW COLUMNS FROM users WHERE Field IN ('employment','experience_years')"); print(c.fetchall())
    c.execute("SELECT name FROM django_migrations WHERE app='api' ORDER BY id DESC LIMIT 3"); print(c.fetchall())
PY
echo "== cold first request profile (fresh interpreter)"
timeout 170 python - <<'PY' 2>&1 | cut -c1-190 | tail -60
import os, sys, time, cProfile, pstats, io
sys.path.insert(0, '/home/consicac/nebians_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
from nebians.wsgi import application
from django.urls import get_resolver
get_resolver()._populate()
from django.test import Client
cl = Client(HTTP_HOST='nebians.consica.com.np')
t = time.time(); cl.get('/api/realtime/config/', secure=True); print('middleware load + cfg ms', round((time.time() - t) * 1000))
pr = cProfile.Profile(); pr.enable()
t = time.time(); r = cl.get('/api/posts/', secure=True); ms = round((time.time() - t) * 1000)
pr.disable()
print('first GET /api/posts/', r.status_code, ms, 'ms (profiled)')
st = pstats.Stats(pr); st.sort_stats('cumulative')
buf = io.StringIO(); st.stream = buf; st.print_stats(400)
n = 0
for line in buf.getvalue().splitlines():
    if not any(k in line for k in ('nebians', 'api/', 'web/', 'importlib', 'redis', 'MySQLdb', 'pymysql', 'mysql', 'template', 'loader')) or 'whitenoise' in line:
        continue
    n += 1
    if n > 60:
        break
    if 'site-packages' in line:
        line = line.replace('/home/consicac/virtualenv/nebians_api/3.13/lib/python3.13/site-packages/', 'sp/')
    print(line.replace('/home/consicac/nebians_api/', ''))
PY
echo "== done"
