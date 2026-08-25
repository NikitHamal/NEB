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

if ! pgrep -f "cloudflared.*8001" >/dev/null; then
    setsid nohup /home/consicac/.local/bin/cloudflared --protocol http2 --url http://127.0.0.1:8001 >> logs/cloudflared.log 2>&1 < /dev/null &
fi

sleep 3
echo "watcher: $(pgrep -f run_autofix_watch | wc -l) process(es); worker: $(pgrep -f run_background_agent_worker | wc -l) process(es); code_worker: $(pgrep -f run_code_agent_worker | wc -l) process(es); daphne: $(pgrep -f daphne | wc -l) process(es)"
