#!/bin/bash
# READ-ONLY. Counts only. IPs are never printed (hashed to a count of distinct values).
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
f=~/access-logs/nebians.consica.com.np-ssl_log
timeout 90 python - "$f" <<'PY' 2>&1 | cut -c1-220 | tail -90
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

print('--- bot analysis')
bots = [r for r in dyn if r[5].split('?')[0] in ('/login/', '/app/schools/verify/', '/auth/google/login/', '/auth/github/login/')]
uas = collections.Counter(re.sub(r'\d+', 'N', r[9])[:140] for r in bots); print('UA variants', len(uas))
for u, n in uas.most_common(4): print('  %4d %s' % (n, u))
print('bot hit first/last', bots[0][1], bots[0][2] + ':' + bots[0][3], bots[-1][2] + ':' + bots[-1][3])
perh = collections.Counter(r[2] for r in bots); print('bot hits per hour', sorted(perh.items()))
perm = collections.Counter((r[2], r[3]) for r in rows if r[6] == '503'); print('503 per minute (top)', perm.most_common(8))
allm = collections.Counter((r[2], r[3]) for r in dyn); print('dynamic req/min peak', allm.most_common(6))
bm = collections.Counter((r[2], r[3]) for r in bots); print('bot req/min peak', bm.most_common(6))
sch = [r for r in dyn if r[5].startswith('/app/schools/')]
print('school pages dyn hits', len(sch), 'distinct ips', len({r[0] for r in sch}), 'cls', dict(collections.Counter(cls(r[9]) for r in sch)))
print('referer on bot hits', collections.Counter('none' if r[8] == '-' else 'self' if 'nebians' in r[8] else 'other' for r in bots))
print('ips hitting bot paths also hitting other pages:', len({r[0] for r in bots} & {r[0] for r in dyn if r not in bots}))
PY
echo "== stderr.log: child kills by signal"; grep -o 'killed by signal: [0-9]*' ~/nebians_api/stderr.log 2>/dev/null | sort | uniq -c
echo "== stderr.log: other lines than max-children (last 12, truncated)"
grep -v 'max children' ~/nebians_api/stderr.log 2>/dev/null | tail -n 12 | cut -c1-200
echo "== done"
