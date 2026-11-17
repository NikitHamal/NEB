#!/bin/bash
# READ-ONLY. Aggregate counts only (this repo is public, so no usernames, emails or IPs are printed).
# Measures the blast radius of the Session 68 NameError on GET /api/posts/<id>/replies/.
cd /home/consicac/nebians_api || exit 1
source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
echo "== server_errors.log: HTTP 5xx on replies, per hour (server clock)"
grep -h "HTTP 50[0-9] | GET /api/posts/.*/replies/" logs/server_errors.log* 2>/dev/null \
  | sed -E 's/^\[([0-9-]+ [0-9]{2}):.*HTTP ([0-9]+).*/\1h \2/' | sort | uniq -c | tail -30
echo "== distinct client IPs hit / distinct posts hit / total (replies 5xx, since 2026-11-17)"
grep -h "HTTP 50[0-9] | GET /api/posts/.*/replies/" logs/server_errors.log* 2>/dev/null | grep -E '^\[2026-11-(17|18)' > /tmp/rep5xx.txt
wc -l < /tmp/rep5xx.txt
sed -E 's/.*IP: ([^ ]+).*/\1/' /tmp/rep5xx.txt | sort -u | wc -l
sed -E 's/.*posts\/([^/]+)\/replies.*/\1/' /tmp/rep5xx.txt | sort -u | wc -l
echo "first / last:"; head -1 /tmp/rep5xx.txt | cut -c1-22; tail -1 /tmp/rep5xx.txt | cut -c1-22
echo "== nebians.log: NameError occurrences"
grep -h "name 'Reply' is not defined" logs/nebians.log* 2>/dev/null | wc -l
echo "== other 5xx paths since 2026-11-17 (top 10, ids masked)"
grep -h "HTTP 50[0-9]" logs/server_errors.log* 2>/dev/null | grep -E '^\[2026-11-(17|18)' \
  | sed -E 's/.*HTTP ([0-9]+) \| ([A-Z]+) ([^ ]+).*/\1 \2 \3/; s/[0-9a-f]{8}-[0-9a-f-]{27}/<id>/g' | sort | uniq -c | sort -rn | head -10
echo "== live health probe (anonymous, local worker)"
timeout 60 python - <<'PY' 2>&1 | tail -12 | cut -c1-200
import os, sys
sys.path.insert(0, '/home/consicac/nebians_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
import django; django.setup()
from django.test import Client
from api.models import Reply, User
import time
since = int((time.time() - 3 * 3600) * 1000)
pid = Reply.objects.order_by('-created_at').values_list('post_id', flat=True).first()
c = Client(HTTP_HOST='nebians.consica.com.np')
r = c.get(f'/api/posts/{pid}/replies/', secure=True)
print('latest replied post GET replies ->', r.status_code)
print('replies written in the last 3 h:', Reply.objects.filter(created_at__gte=since).count())
print('users with last_active in the last 3 h (aggregate):', User.objects.filter(last_active__gte=since).count())
PY
