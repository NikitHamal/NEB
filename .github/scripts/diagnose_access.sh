#!/bin/bash
# READ-ONLY. Counts only. IPs are never printed (hashed to a count of distinct values).
f=~/access-logs/nebians.consica.com.np-ssl_log
timeout 90 python3 - "$f" <<'PY' 2>&1 | cut -c1-220 | tail -90
import sys, re, collections, os
f = sys.argv[1]
size = os.path.getsize(f)
with open(f, 'rb') as fh:
    fh.seek(max(0, size - 12_000_000)); lines = fh.read().decode('utf-8', 'ignore').splitlines()[1:]
rx = re.compile(r'^(\S+) \S+ \S+ \[(\d+/\w+/\d+):(\d\d):(\d\d):\d\d [^\]]+\] "(\w+) (\S+)[^"]*" (\d{3}) (\d+|-) "([^"]*)" "([^"]*)"')
rows = []
for l in lines:
    m = rx.match(l)
    if m: rows.append(m.groups())
print('lines', len(rows), 'from', rows[0][1], rows[0][2] + ':' + rows[0][3], 'to', rows[-1][1], rows[-1][2] + ':' + rows[-1][3])
def cls(ua):
    u = ua.lower()
    if any(k in u for k in ('bot', 'crawl', 'spider', 'slurp', 'curl', 'python', 'go-http', 'scrapy', 'headless', 'wget', 'okhttp/')) and 'nebians' not in u: return 'bot/tool'
    if 'okhttp' in u or 'nebians' in u: return 'app'
    return 'browser'
norm = lambda p: re.sub(r'[0-9a-f]{8}-[0-9a-f-]{27}', 'UUID', re.sub(r'\d+', 'N', p.split('?')[0]))[:58]
by_cls = collections.Counter(cls(r[9]) for r in rows); print('UA classes', dict(by_cls))
s503 = collections.Counter(norm(r[5]) for r in rows if r[6] == '503'); print('503 by path', s503.most_common(8))
s429 = collections.Counter(norm(r[5]) for r in rows if r[6] == '429'); print('429 by path', s429.most_common(5))
hourly = collections.Counter((r[1][:6], r[2]) for r in rows); print('requests per hour', sorted(hourly.items())[-12:])
h503 = collections.Counter((r[1][:6], r[2]) for r in rows if r[6] == '503'); print('503 per hour', sorted(h503.items())[-12:])
# dynamic requests only (workers): not /static/ /media/
dyn = [r for r in rows if not r[5].startswith(('/static/', '/media/', '/favicon', '/manifest', '/robots', '/sw.js'))]
print('dynamic', len(dyn), 'static/media', len(rows) - len(dyn))
for name in ('/login/', '/app/schools/verify/', '/auth/google/login/', '/auth/github/login/', '/ajax/resource/impressions/'):
    sub = [r for r in dyn if r[5].split('?')[0] == name or norm(r[5]) == name]
    print(name, 'n', len(sub), 'status', dict(collections.Counter(r[6] for r in sub).most_common(4)), 'distinct ips', len({r[0] for r in sub}),
          'cls', dict(collections.Counter(cls(r[9]) for r in sub)), 'methods', dict(collections.Counter(r[4] for r in sub)))
    if sub: print('   ua sample:', sub[-1][9][:90], '| ref:', sub[-1][8][:60])
ip = collections.Counter(r[0] for r in dyn); top = ip.most_common(5)
print('top dynamic talkers (anonymised) hits:', [n for _, n in top], 'distinct ips', len(ip))
print('top dyn paths:'); 
for p, n in collections.Counter(norm(r[5]) for r in dyn).most_common(18): print('  %5d %s' % (n, p))
print('status of dynamic', dict(collections.Counter(r[6] for r in dyn).most_common(8)))
PY
echo "== stderr.log: other lines than max-children (last 12, truncated)"
grep -v 'max children' ~/nebians_api/stderr.log 2>/dev/null | tail -n 12 | cut -c1-200
echo "== done"
