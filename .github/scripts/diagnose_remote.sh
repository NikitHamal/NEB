#!/bin/bash
# READ-ONLY server snapshot. Output goes through a redactor in the workflow, and
# nothing here prints env files, .htaccess or credentials (names or safe numbers only).
cd /home/consicac/nebians_api || exit 1
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
echo "== load"; cat /proc/loadavg
echo "== lswsgi tree (pid ppid etime rss args)"
ps -u consicac -o pid=,ppid=,etime=,rss=,args= 2>/dev/null | grep -E 'lswsgi|daphne' | grep -v grep | cut -c1-150 | head -20
echo "== lswsgi script"
LS=$(command -v lswsgi || ls /usr/local/lsws/fcgi-bin/lswsgi* 2>/dev/null | head -1); echo "$LS"
grep -nE 'preload|load_source|import_module|spec_from|exec\(|LSAPI_|fork|-m |--' "$LS" 2>/dev/null | cut -c1-150 | head -25
echo "== lsapi / litespeed env names visible to our workers"
ls /usr/local/lsws/conf 2>/dev/null | head -3
echo "== cold-process timing (fresh interpreter, like a new worker)"
timeout 170 python - <<'PY' 2>&1 | cut -c1-200 | tail -30
import os, sys, time
sys.path.insert(0, '/home/consicac/nebians_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
t0 = time.time()
from nebians.wsgi import application
t1 = time.time(); print('wsgi import ms', round((t1 - t0) * 1000))
from django.urls import get_resolver
get_resolver()._populate(); t2 = time.time(); print('urlconf populate ms', round((t2 - t1) * 1000))
from django.test import Client
cl = Client(HTTP_HOST='nebians.consica.com.np')
for p in ['/api/posts/', '/api/posts/', '/app/news/', '/api/realtime/config/']:
    t = time.time(); r = cl.get(p, secure=True); print('GET', p, r.status_code, round((time.time() - t) * 1000), 'ms')
import sys
mods = sorted(sys.modules); print('modules loaded', len(mods))
PY
echo "== done"
