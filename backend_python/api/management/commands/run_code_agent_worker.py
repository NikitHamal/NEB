"""Background worker for Neby Code agent sessions.

Polls CodeSession rows with status='queued', claims one at a time, and
runs the LLM <-> daemon tool loop. Run alongside the other workers:

    python manage.py run_code_agent_worker
"""
import time

from django.core.management.base import BaseCommand
from django.db import close_old_connections

from api.code_agent import run_session
from api.models import CodeSession


class Command(BaseCommand):
    help = 'Runs queued Neby Code agent sessions.'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=float, default=1.5)

    def handle(self, *args, **options):
        interval = float(options['interval'])
        self.stdout.write(self.style.SUCCESS('code agent worker started'))
        while True:
            try:
                close_old_connections()
                job = self._claim_next()
                if not job:
                    time.sleep(interval)
                    continue
                self.stdout.write(f'running code session {job}')
                self._reset_cancel(job)
                try:
                    run_session(job)
                    self.stdout.write(self.style.SUCCESS(f'done {job}'))
                except Exception as exc:  # noqa: BLE001
                    self.stderr.write(f'code session {job} crashed: {exc}')
                    CodeSession.objects.filter(id=job).update(
                        status='error', error=str(exc)[:2000],
                        updated_at=int(time.time() * 1000))
            except KeyboardInterrupt:
                self.stdout.write('stopping')
                return
            except Exception as exc:  # noqa: BLE001
                self.stderr.write(f'worker loop error: {exc}')
                time.sleep(3)

    @staticmethod
    def _claim_next():
        now = int(time.time() * 1000)
        candidate = (CodeSession.objects.filter(status='queued')
                     .order_by('updated_at').values_list('id', flat=True).first())
        if not candidate:
            return None
        claimed = (CodeSession.objects.filter(id=candidate, status='queued')
                   .update(status='running', updated_at=now))
        return candidate if claimed else None

    @staticmethod
    def _reset_cancel(session_id):
        CodeSession.objects.filter(id=session_id).update(cancel_flag=False)
