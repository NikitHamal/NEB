#!/bin/bash
# Restart background agent worker + autofix watcher reliably.
cd /home/consicac/nebians_api || exit 1
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate

for pid in $(pgrep -f run_background_agent_worker); do kill -TERM "$pid" 2>/dev/null; done
for pid in $(pgrep -f run_autofix_watch); do kill -TERM "$pid" 2>/dev/null; done
sleep 3
for pid in $(pgrep -f run_background_agent_worker); do kill -KILL "$pid" 2>/dev/null; done
for pid in $(pgrep -f run_autofix_watch); do kill -KILL "$pid" 2>/dev/null; done

setsid nohup python manage.py run_background_agent_worker --recover-after 120 >> logs/worker.log 2>&1 < /dev/null &
setsid nohup python manage.py run_autofix_watch >> logs/autofix.log 2>&1 < /dev/null &
sleep 4
echo "watcher: $(pgrep -f run_autofix_watch | wc -l) process(es); worker: $(pgrep -f run_background_agent_worker | wc -l) process(es)"
