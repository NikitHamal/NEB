#!/bin/bash
# Restart background agent worker + autofix watcher + code agent worker + Daphne reliably.
cd /home/consicac/nebians_api || exit 1
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate

for pid in $(pgrep -f run_background_agent_worker); do kill -TERM "$pid" 2>/dev/null; done
for pid in $(pgrep -f run_autofix_watch); do kill -TERM "$pid" 2>/dev/null; done
for pid in $(pgrep -f run_code_agent_worker); do kill -TERM "$pid" 2>/dev/null; done
for pid in $(pgrep -f "daphne.*8001"); do kill -TERM "$pid" 2>/dev/null; done
sleep 2
for pid in $(pgrep -f run_background_agent_worker); do kill -KILL "$pid" 2>/dev/null; done
for pid in $(pgrep -f run_autofix_watch); do kill -KILL "$pid" 2>/dev/null; done
for pid in $(pgrep -f run_code_agent_worker); do kill -KILL "$pid" 2>/dev/null; done
for pid in $(pgrep -f "daphne.*8001"); do kill -KILL "$pid" 2>/dev/null; done

setsid nohup python manage.py run_background_agent_worker --recover-after 120 >> logs/worker.log 2>&1 < /dev/null &
setsid nohup python manage.py run_autofix_watch >> logs/autofix.log 2>&1 < /dev/null &
setsid nohup python manage.py run_code_agent_worker >> logs/code_worker.log 2>&1 < /dev/null &
setsid nohup daphne -b 127.0.0.1 -p 8001 nebians.asgi:application >> logs/daphne.log 2>&1 < /dev/null &

# Deduplicate cloudflared — quick tunnel should be single process; old logs remain valid but extra workers waste RAM
if [ $(pgrep -f "cloudflared.*8001" | wc -l) -gt 1 ]; then
    echo "killing duplicate cloudflared processes..."
    pkill -f "cloudflared.*8001"; sleep 2
fi
if ! pgrep -f "cloudflared.*8001" >/dev/null; then
    echo "cloudflared not running — starting ..."
    setsid nohup /home/consicac/.local/bin/cloudflared --protocol http2 --url http://127.0.0.1:8001 >> logs/cloudflared.log 2>&1 < /dev/null &
    # Wait for quick tunnel URL to appear, then refresh ws_url.txt
    for i in 1 2 3 4 5 6 7 8 9 10; do
        sleep 2
        if grep -q "trycloudflare.com" logs/cloudflared.log 2>/dev/null; then break; fi
    done
fi

# Refresh ws_url.txt from newest log (mirrors deploy.ps1 logic — ws_url.txt is fallback only)
python3 << 'PYEOF' 2>/dev/null || true
import glob, re, os
candidates = []
for p in ['/home/consicac/nebians_api/logs/start_ws_tunnel.log', 'logs/start_ws_tunnel.log', '/home/consicac/nebians_api/logs/cloudflared.log', 'logs/cloudflared.log'] + sorted(glob.glob('/tmp/cf_quick*.log'), reverse=True):
    try:
        with open(p) as f: c = f.read()
        ms = re.findall(r'(?:wss?|https?)://([a-z0-9-]+\.trycloudflare\.com)', c)
        if ms:
            u = 'wss://' + ms[-1] + '/ws/'
            try: mtime = os.path.getmtime(p)
            except: mtime = 0
            candidates.append((mtime, u))
    except: continue
if candidates:
    candidates.sort(key=lambda x: x[0], reverse=True)
    u = candidates[0][1]
    try:
        with open('ws_url.txt', 'r') as f: old = f.read().strip()
    except: old = ''
    if old != u:
        with open('ws_url.txt','w') as f: f.write(u+'\n')
        print(f'ws_url.txt refreshed: {u}')
else:
    # fallback to ws_url.txt content if no log has URL
    try:
        with open('ws_url.txt') as f: old = f.read().strip()
        if old:
            print(f'ws_url.txt kept (no log candidate): {old}')
    except: pass
PYEOF

sleep 1
echo "watcher: $(pgrep -f run_autofix_watch | wc -l) process(es); worker: $(pgrep -f run_background_agent_worker | wc -l) process(es); code_worker: $(pgrep -f run_code_agent_worker | wc -l) process(es); daphne: $(pgrep -f daphne | wc -l) process(es); cloudflared: $(pgrep -f cloudflared | wc -l) process(es)"
