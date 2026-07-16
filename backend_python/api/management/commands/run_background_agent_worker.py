"""Durable worker for autonomous background coding sessions and GitHub actions."""
from __future__ import annotations

import logging
import os
import signal
import socket
import threading
import time

from django.core.management.base import BaseCommand
from django.db import close_old_connections, transaction

from api.background_agent.actions import process_action
from api.background_agent.runner import BackgroundAgentRunner
from api.models import BackgroundAgentAction, BackgroundAgentSession, BackgroundAgentWorker
from api.utils import now_ms

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run the durable NEBians background coding agent worker'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=float, default=2.0)
        parser.add_argument('--once', action='store_true')
        parser.add_argument('--recover-after', type=int, default=900, help='Requeue stale running sessions after N seconds')

    def handle(self, *args, **options):
        self.running = True
        self.worker_id = f'{socket.gethostname()}:{os.getpid()}'
        self.hostname = socket.gethostname()
        self.current_kind = ''
        self.current_id = ''
        self.heartbeat_stop = threading.Event()
        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)
        self._recover(options['recover_after'])
        self.last_recovery_at = time.monotonic()
        self._write_worker_heartbeat('starting')
        heartbeat_thread = threading.Thread(target=self._heartbeat_loop, name='background-agent-heartbeat', daemon=True)
        heartbeat_thread.start()
        self.stdout.write(self.style.SUCCESS(f'Background agent worker started as {self.worker_id}'))
        try:
            while self.running:
                close_old_connections()
                if time.monotonic() - self.last_recovery_at >= 60:
                    self._recover(options['recover_after'])
                    self.last_recovery_at = time.monotonic()
                did_work = False
                action = self._claim_action()
                if action:
                    did_work = True
                    self._set_current('action', str(action.id))
                    process_action(action)
                    self._set_current('', '')
                else:
                    session = self._claim_session()
                    if session:
                        did_work = True
                        self._set_current('session', str(session.id))
                        BackgroundAgentRunner(session).run()
                        self._set_current('', '')
                if options['once']:
                    break
                if not did_work:
                    time.sleep(max(0.25, options['interval']))
        finally:
            self.heartbeat_stop.set()
            heartbeat_thread.join(timeout=2)
            self._write_worker_heartbeat('stopping')
        self.stdout.write('Background agent worker stopped.')

    def _set_current(self, kind, identifier):
        self.current_kind = kind
        self.current_id = identifier
        self._write_worker_heartbeat('busy' if kind else 'idle')

    def _heartbeat_loop(self):
        while not self.heartbeat_stop.wait(10):
            close_old_connections()
            try:
                self._write_worker_heartbeat('busy' if self.current_kind else 'idle')
            except Exception:
                logger.exception('Unable to persist background-agent worker heartbeat')
            finally:
                close_old_connections()

    def _write_worker_heartbeat(self, status):
        now = now_ms()
        worker, _ = BackgroundAgentWorker.objects.get_or_create(
            worker_id=self.worker_id,
            defaults={
                'hostname': self.hostname,
                'process_id': os.getpid(),
                'started_at': now,
            },
        )
        worker.hostname = self.hostname
        worker.process_id = os.getpid()
        worker.status = status
        worker.current_kind = self.current_kind
        worker.current_id = self.current_id
        worker.last_heartbeat_at = now
        worker.save(update_fields=[
            'hostname', 'process_id', 'status', 'current_kind',
            'current_id', 'last_heartbeat_at',
        ])

    def _claim_session(self):
        with transaction.atomic():
            query = BackgroundAgentSession.objects.select_related(
                'project__credential', 'bot_config'
            ).filter(status='queued').order_by('created_at')
            try:
                session = query.select_for_update(skip_locked=True).first()
            except Exception:
                session = query.select_for_update().first()
            if not session:
                return None
            session.status = 'preparing'
            session.worker_id = self.worker_id
            session.last_heartbeat_at = now_ms()
            session.updated_at = now_ms()
            session.save(update_fields=['status', 'worker_id', 'last_heartbeat_at', 'updated_at'])
            return session

    def _claim_action(self):
        with transaction.atomic():
            query = BackgroundAgentAction.objects.select_related(
                'session__project__credential'
            ).filter(status='queued').order_by('created_at')
            try:
                action = query.select_for_update(skip_locked=True).first()
            except Exception:
                action = query.select_for_update().first()
            if not action:
                return None
            action.status = 'processing'
            action.started_at = now_ms()
            action.worker_id = self.worker_id
            action.save(update_fields=['status', 'started_at', 'worker_id'])
            return action

    def _recover(self, recover_after):
        cutoff = now_ms() - max(60, int(recover_after)) * 1000
        worker_cutoff = now_ms() - 30000
        active_worker_ids = list(BackgroundAgentWorker.objects.filter(
            last_heartbeat_at__gte=worker_cutoff,
            status__in=['starting', 'idle', 'busy'],
        ).values_list('worker_id', flat=True))
        count = BackgroundAgentSession.objects.filter(
            status__in=['preparing', 'running'],
            last_heartbeat_at__lt=cutoff,
        ).exclude(worker_id__in=active_worker_ids).update(
            status='queued',
            worker_id='',
            progress_label='Recovered after stale worker heartbeat',
            updated_at=now_ms(),
        )
        BackgroundAgentAction.objects.filter(
            status='processing', started_at__lt=cutoff,
        ).exclude(worker_id__in=active_worker_ids).update(
            status='queued', started_at=0, worker_id='', error='Recovered after stale worker heartbeat'
        )
        if count:
            self.stdout.write(self.style.WARNING(f'Requeued {count} stale session(s)'))

    def _stop(self, signum, frame):
        self.running = False
