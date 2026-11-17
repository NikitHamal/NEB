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
