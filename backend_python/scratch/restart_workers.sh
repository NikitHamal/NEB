#!/bin/bash
# Restart the long-running daemons after a code deploy.
#
# Only daphne is (re)started here. The background coding agent, the Neby Code
# worker and the Lazy agent were removed from the codebase on 2026-10-31
# (commit a74d5821), and the cloudflared tunnel is intentionally OFF because
# outbound 7844 is firewalled on this box. Re-enable the DISABLED block below
# when the provider opens 7844.
cd /home/consicac/nebians_api || exit 1
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate

# Realtime port override: a box whose 8001 is taken (e.g. live box .186, where a
# foreign uvicorn squats 8001) keeps its port in .realtime_port (e.g. "8003").
# Default 8001 everywhere else.
REALTIME_PORT="$(cat .realtime_port 2>/dev/null || echo 8001)"
REALTIME_PORT="$(echo "$REALTIME_PORT" | tr -cd '0-9')"
[ -z "$REALTIME_PORT" ] && REALTIME_PORT=8001
echo "realtime port: $REALTIME_PORT"

for pid in $(pgrep -f "daphne.*${REALTIME_PORT}"); do kill -TERM "$pid" 2>/dev/null; done
sleep 2
for pid in $(pgrep -f "daphne.*${REALTIME_PORT}"); do kill -KILL "$pid" 2>/dev/null; done

# The agent workers were removed with their features on 2026-10-31; any process
# still running one is stale and gets killed so it cannot resurrect.
for pat in run_background_agent_worker run_code_agent_worker run_autofix_watch; do
    for pid in $(pgrep -f "$pat"); do kill -TERM "$pid" 2>/dev/null; done
done
sleep 1
for pat in run_background_agent_worker run_code_agent_worker run_autofix_watch; do
    for pid in $(pgrep -f "$pat"); do kill -KILL "$pid" 2>/dev/null; done
done

# Realtime uses hosted Ably (api/realtime_ably.py) unless WS_PUBLIC_URL or ENABLE_DAPHNE=1 is set.
# Starting daphne when WS_PUBLIC_URL is unset wastes ~127 MB RAM and ~64 LVE threads on shared cPanel.
WANT_DAPHNE="$(python3 -c "import os; from dotenv import load_dotenv; load_dotenv('.env'); print('1' if (os.environ.get('WS_PUBLIC_URL','').strip() or os.environ.get('ENABLE_DAPHNE','')=='1') else '0')" 2>/dev/null || echo 0)"
if [ "$WANT_DAPHNE" = "1" ]; then
    setsid nohup daphne -b 127.0.0.1 -p "${REALTIME_PORT}" nebians.asgi:application >> logs/daphne.log 2>&1 < /dev/null &
else
    echo "WS_PUBLIC_URL unset (hosted Ably active) - keeping daphne retired to save ~127 MB RAM and 64 threads."
fi

# Deduplicate cloudflared - quick tunnel should be single process; old logs remain valid but extra workers waste RAM
# DISABLED 2026-10-18 (owner request): the tunnel cannot connect (outbound 7844
# firewalled) and a retrying cloudflared burns ~30 threads of the shared LVE
# nproc limit. Re-enable when the provider opens 7844.
if false && [ $(pgrep -f "cloudflared.*${REALTIME_PORT}" | wc -l) -gt 1 ]; then
    echo "killing duplicate cloudflared processes..."
    pkill -f "cloudflared.*${REALTIME_PORT}"; sleep 2
fi
if false && ! pgrep -f "cloudflared.*${REALTIME_PORT}" >/dev/null; then
    echo "cloudflared not running - starting ..."
    setsid nohup /home/consicac/.local/bin/cloudflared --protocol http2 --url "http://127.0.0.1:${REALTIME_PORT}" >> logs/cloudflared.log 2>&1 < /dev/null &
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
echo "daphne: $(pgrep -f daphne | wc -l) process(es); cloudflared: $(pgrep -f cloudflared | wc -l) process(es)"
