"""Dump persisted steps/observations for one agent run."""

import json
import os
import sys

import django

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
django.setup()

from api.models import LazyAgentRun  # noqa: E402


def main():
    run_id = sys.argv[1] if len(sys.argv) > 1 else ''
    run = (LazyAgentRun.objects.filter(id=run_id).first()
           or LazyAgentRun.objects.order_by('-created_at').first())
    if not run:
        print('no run found')
        return
    print('run', run.id, 'status', run.status)
    print('goal', (run.goal or '')[:200])
    for s in run.steps.all():
        print(f'\n--- {s.index}. {s.kind} ---')
        try:
            detail = json.loads(s.detail or '{}')
        except Exception:
            detail = s.detail
        if s.kind == 'tool':
            print('args:', json.dumps(detail.get('args') or {}, ensure_ascii=False)[:900])
            print('obs :', str(detail.get('summary') or detail.get('result') or '')[:1200])
        else:
            print(json.dumps(detail, ensure_ascii=False)[:700])


if __name__ == '__main__':
    main()
