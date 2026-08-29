"""Smoke check for the rebuilt Lazy workspace page."""

import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')

import django
django.setup()

from django.conf import settings
from django.test import Client

settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver', 'localhost']

from api.models import User

results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(('PASS ' if ok else 'FAIL ') + name + ((' | ' + str(detail)) if detail else ''))


user = User.objects.exclude(id='').first()
check('a usable user exists', user is not None)

from django.contrib.sessions.backends.db import SessionStore

client = Client()
# The project's User model has no last_login, so force_login() cannot be used;
# the views read request.session['user_id'], so seed the session directly.
session = SessionStore()
session['user_id'] = user.id
session.create()
client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key

res = client.get('/lazy/')
check('/lazy/ returns 200', res.status_code == 200, res.status_code)

if res.status_code != 200:
    print('\nSKIPPING remaining checks — page did not render')
    failed = [n for n, ok, _ in results if not ok]
    sys.exit(1)

html = res.content.decode('utf-8')

check('new stylesheets loaded', 'lazy_agent.css' in html)
check('legacy harness css dropped', 'lazy_harness.css' not in html)
for script in ('lazy_agent/api.js', 'lazy_agent/dom.js', 'lazy_agent/stream.js', 'lazy_agent/workspace.js'):
    check(f'script {script} referenced', script in html)

for marker in ('lzStream', 'lzThreads', 'lzPlan', 'lzActivity', 'lzFiles', 'lzViewer', 'lzPrompt', 'lzCancel'):
    check(f'markup id {marker}', f'id="{marker}"' in html)

check('config blob present', 'window.LAZY_AGENT_CONFIG' in html)
check('endpoints injected',
      bool(re.search(r'\brun:\s*"/ajax/lazy/agent/run/"', html))
      and bool(re.search(r'\bhistory:\s*"/ajax/lazy/agent/session/__ID__/history/"', html))
      and bool(re.search(r'\bartifact:\s*"/ajax/lazy/agent-artifact/__RID__/"', html)))

from django.contrib.staticfiles import finders
for asset in ('web/css/lazy_agent.css', 'web/js/lazy_agent/api.js', 'web/js/lazy_agent/dom.js',
              'web/js/lazy_agent/stream.js', 'web/js/lazy_agent/workspace.js'):
    path = finders.find(asset)
    check(f'static asset resolves: {asset}', path and os.path.exists(path), path)

css_path = finders.find('web/css/lazy_agent.css')
css = open(css_path, encoding='utf-8').read()
check('css defines figure styles', '.lzdoc-figure' in css)
check('css defines conversation styles', '.lz-msg--user' in css)
check('css has responsive rules', '@media (max-width: 860px)' in css)

js_path = finders.find('web/js/lazy_agent/workspace.js')
js = open(js_path, encoding='utf-8').read()
check('workspace references srcId', 'srcId' in js)
check('workspace has no stale pendingSources', 'pendingSources' not in js)

# Every id the JS looks up must exist in the template.
ids = set(re.findall(r"getElementById\('([^']+)'\)", js))
missing = [i for i in ids if f'id="{i}"' not in html]
check('all getElementById targets exist in markup', not missing, missing)

failed = [n for n, ok, _ in results if not ok]
print('\n%d/%d passed' % (len(results) - len(failed), len(results)))
if failed:
    print('FAILED:', ', '.join(failed))
    sys.exit(1)
print('OK')
