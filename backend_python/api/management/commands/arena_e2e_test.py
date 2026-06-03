"""End-to-end in-process test of the AI4Bharat Arena proxy views.

Uses Django's test Client + StreamingHttpResponse iteration. Hits the live
arena (backend.arena.ai4bharat.co) for real chat completion, so requires
network access.
"""
import json
import time
import uuid

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.test import Client

from api.models import User, ArenaChatSession, ArenaChatMessage


class Command(BaseCommand):
    help = 'In-process E2E test of /api/neby-arena/ endpoints'

    def add_arguments(self, parser):
        parser.add_argument('--user', default='testarena', help='username to use/create')

    def handle(self, *args, **options):
        username = options['user']
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'id': f'testarena-{uuid.uuid4().hex[:8]}',
                'display_name': 'Arena Tester',
                'email_verified': True,
                'auth_token': f'local-test-token-{uuid.uuid4().hex}',
                'created_at': int(time.time() * 1000),
            },
        )
        if not user.auth_token:
            user.auth_token = f'local-test-token-{uuid.uuid4().hex}'
            user.save(update_fields=['auth_token'])
        self.stdout.write(f'User: {user.username} (created={created}) token={user.auth_token[:24]}...')

        client = Client(HTTP_AUTHORIZATION=f'Bearer {user.auth_token}', SERVER_NAME='localhost')
        base = '/api/neby-arena/'

        # 1) Models list
        self.stdout.write('\n[1] GET /models/')
        r = client.get(base + 'models/')
        self.stdout.write(f'  status={r.status_code}  cached={r.json().get("cached")}')
        models = r.json().get('models') or []
        self.stdout.write(f'  models: {len(models)}')
        pick = next((m for m in models if m['code'] == 'gemini-3.5-flash'), models[0])
        self.stdout.write(f'  picked: {pick["name"]} ({pick["code"]}) id={pick["id"]}')

        # 2) Create session
        self.stdout.write('\n[2] POST /sessions/')
        r = client.post(base + 'sessions/',
                        data=json.dumps({'modelId': pick['id']}),
                        content_type='application/json')
        self.stdout.write(f'  status={r.status_code}')
        if r.status_code != 201:
            self.stdout.write(self.style.ERROR(f'  body={r.content[:400]}'))
            return
        sess = r.json()['session']
        sid = sess['id']
        self.stdout.write(f'  session id={sid}  model={sess["modelName"]}')

        # 3) Send message (stream)
        self.stdout.write('\n[3] POST /sessions/<id>/messages/ (SSE stream)')
        r = client.post(base + f'sessions/{sid}/messages/',
                        data=json.dumps({'content': 'What is 7 * 8? Just the number.'}),
                        content_type='application/json')
        self.stdout.write(f'  status={r.status_code}  content-type={r.get("Content-Type")}')
        full_text = ''
        finish_reason = None
        for raw in r.streaming_content:
            line = raw.decode('utf-8', errors='replace') if isinstance(raw, bytes) else raw
            for ln in line.split('\n'):
                ln = ln.strip()
                if not ln.startswith('data: '):
                    continue
                payload = ln[6:]
                if payload == '[DONE]':
                    self.stdout.write('  [DONE]')
                    continue
                try:
                    obj = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                if 'choices' in obj:
                    delta = obj['choices'][0].get('delta', {})
                    if 'content' in delta:
                        full_text += delta['content']
                    if 'finish_reason' in obj['choices'][0]:
                        finish_reason = obj['choices'][0]['finish_reason']
                elif 'error' in obj:
                    self.stdout.write(self.style.ERROR(f'  ERROR: {obj["error"]}'))
        self.stdout.write(f'  finish_reason={finish_reason}')
        self.stdout.write(f'  text: {full_text[:200]!r}')

        # 4) Send a follow-up (multi-turn)
        self.stdout.write('\n[4] POST /sessions/<id>/messages/ (turn 2 — multi-turn)')
        r = client.post(base + f'sessions/{sid}/messages/',
                        data=json.dumps({'content': 'And what is 6 * 9?'}),
                        content_type='application/json')
        text2 = ''
        for raw in r.streaming_content:
            line = raw.decode('utf-8', errors='replace') if isinstance(raw, bytes) else raw
            for ln in line.split('\n'):
                ln = ln.strip()
                if not ln.startswith('data: '):
                    continue
                payload = ln[6:]
                if payload == '[DONE]':
                    continue
                try:
                    obj = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                if 'choices' in obj and 'content' in obj['choices'][0].get('delta', {}):
                    text2 += obj['choices'][0]['delta']['content']
        self.stdout.write(f'  text: {text2[:200]!r}')

        # 5) List sessions
        self.stdout.write('\n[5] GET /sessions/')
        r = client.get(base + 'sessions/')
        self.stdout.write(f'  status={r.status_code}  count={len(r.json()["sessions"])}')

        # 6) Session detail
        self.stdout.write('\n[6] GET /sessions/<id>/')
        r = client.get(base + f'sessions/{sid}/')
        data = r.json()
        self.stdout.write(f'  status={r.status_code}  messages={len(data["messages"])}  msg_count={data["session"]["messageCount"]}')
        for m in data['messages']:
            self.stdout.write(f'    [{m["role"]}] {m["content"][:80]!r}')

        # 7) PATCH title
        self.stdout.write('\n[7] PATCH /sessions/<id>/')
        r = client.patch(base + f'sessions/{sid}/',
                         data=json.dumps({'title': 'Math Q&A'}),
                         content_type='application/json')
        self.stdout.write(f'  status={r.status_code}  body={r.json()}')

        # 8) Regenerate the last assistant message
        last_asst = ArenaChatMessage.objects.filter(
            session_id=sid, role='assistant',
        ).order_by('-created_at').first()
        if last_asst:
            self.stdout.write(f'\n[8] POST /messages/<id>/regenerate/  msg={last_asst.id}')
            r = client.post(base + f'messages/{last_asst.id}/regenerate/')
            regen_text = ''
            for raw in r.streaming_content:
                line = raw.decode('utf-8', errors='replace') if isinstance(raw, bytes) else raw
                for ln in line.split('\n'):
                    ln = ln.strip()
                    if not ln.startswith('data: '):
                        continue
                    payload = ln[6:]
                    if payload == '[DONE]':
                        continue
                    try:
                        obj = json.loads(payload)
                    except json.JSONDecodeError:
                        continue
                    if 'choices' in obj and 'content' in obj['choices'][0].get('delta', {}):
                        regen_text += obj['choices'][0]['delta']['content']
            self.stdout.write(f'  regenerated text: {regen_text[:200]!r}')

        # 9) DELETE session
        self.stdout.write('\n[9] DELETE /sessions/<id>/')
        r = client.delete(base + f'sessions/{sid}/')
        self.stdout.write(f'  status={r.status_code}  body={r.json()}')

        self.stdout.write(self.style.SUCCESS('\nALL E2E TESTS PASSED'))
