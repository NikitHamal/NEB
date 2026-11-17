#!/bin/bash
# READ-ONLY server snapshot. Output goes through a redactor in the workflow, and
# nothing here prints env files, .htaccess or credentials (names or safe numbers only).
cd /home/consicac/nebians_api || exit 1
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
echo "== load"; cat /proc/loadavg
echo "== lswsgi tree (pid ppid etime rss args)"
ps -u consicac -o pid=,ppid=,etime=,rss=,args= 2>/dev/null | grep -E 'lswsgi|daphne' | grep -v grep | cut -c1-150 | head -20
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
pr = cProfile.Profile(); pr.enable()
t = time.time(); r = cl.get('/api/posts/', secure=True); ms = round((time.time() - t) * 1000)
pr.disable()
print('first GET /api/posts/', r.status_code, ms, 'ms (profiled)')
st = pstats.Stats(pr); st.sort_stats('cumulative')
buf = io.StringIO(); st.stream = buf; st.print_stats(45)
for line in buf.getvalue().splitlines():
    if 'site-packages' in line:
        line = line.replace('/home/consicac/virtualenv/nebians_api/3.13/lib/python3.13/site-packages/', 'sp/')
    print(line.replace('/home/consicac/nebians_api/', ''))
PY
echo "== done"
