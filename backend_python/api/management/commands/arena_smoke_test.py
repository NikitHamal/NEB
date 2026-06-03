"""Run a live smoke test of the AI4Bharat proxy module.

Usage:
    python manage.py arena_smoke_test
"""
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Smoke-test the AI4Bharat proxy against the live arena.'

    def handle(self, *args, **options):
        from api.ai4bharat_proxy import (
            _new_anonymous_token, list_models, create_session, stream_chat,
            commit_token_use, mark_token_dead, pool_stats, new_message_id,
        )

        self.stdout.write('== Live arena smoke test: multi-turn + threading ==')
        entry = _new_anonymous_token()
        token = entry['token']
        self.stdout.write('Got token: ' + token[:12] + '...')
        self.stdout.write('Initial pool stats: ' + str(pool_stats()))

        models = list_models(token)
        pick = next(m for m in models if not m.get('random_only'))
        self.stdout.write('Picked: ' + pick['display_name'])

        sess = create_session(token, pick['id'])
        self.stdout.write('Session: ' + sess['id'])

        # Turn 1
        u1, a1 = new_message_id(), new_message_id()
        out1, fin1 = '', None
        for chunk in stream_chat(token, sess['id'], 'Hi', pick['id'], u1, a1, []):
            if chunk['type'] == 'content':
                out1 += chunk['text']
            elif chunk['type'] == 'done':
                fin1 = chunk
        commit_token_use(token, message_used=True, session_opened=True)
        self.stdout.write('T1 finish: ' + str(fin1))
        self.stdout.write('T1 reply length: ' + str(len(out1)))
        self.stdout.write('T1 reply: ' + out1[:200])

        # Turn 2 (with parent_message_ids referencing a1)
        u2, a2 = new_message_id(), new_message_id()
        out2, fin2 = '', None
        for chunk in stream_chat(token, sess['id'], 'What is 2+2?', pick['id'], u2, a2, [a1]):
            if chunk['type'] == 'content':
                out2 += chunk['text']
            elif chunk['type'] == 'done':
                fin2 = chunk
        commit_token_use(token, message_used=True, session_opened=False)
        self.stdout.write('T2 finish: ' + str(fin2))
        self.stdout.write('T2 reply length: ' + str(len(out2)))
        self.stdout.write('T2 reply: ' + out2[:200])

        # Test mark_token_dead + pool stats
        mark_token_dead(token)
        self.stdout.write('After marking dead, pool stats: ' + str(pool_stats()))

        self.stdout.write('ALL OK')
