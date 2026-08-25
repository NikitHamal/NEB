from __future__ import annotations

import argparse
import asyncio
import json
import os
import platform
import socket
import sys
import threading
import time
import uuid
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from . import __version__
from .terminal import TerminalRunner
from .workspace import Workspace, WorkspaceError


class NebyCodeDaemon:
    def __init__(self, workspace, ws_url, ticket='', token='', daemon_id=''):
        self.workspace = Workspace(workspace)
        self.ws_url = self._auth_url(ws_url, ticket)
        self.token = token
        self.daemon_id = daemon_id or uuid.uuid4().hex[:16]
        self.loop = None
        self.outbox = None
        self.terminal = TerminalRunner(self.workspace, self.emit_threadsafe)
        self.started_at = int(time.time())

    @staticmethod
    def _auth_url(ws_url, ticket):
        url = str(ws_url or '').strip()
        if not url:
            raise RuntimeError('--ws-url is required')
        if not ticket:
            return url
        parsed = urlparse(url)
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        query['code_ticket'] = ticket
        return urlunparse(parsed._replace(query=urlencode(query)))

    def info(self):
        git = self.workspace.git_snapshot()
        shell = os.environ.get('COMSPEC') if os.name == 'nt' else os.environ.get('SHELL')
        return {
            'daemon_id': self.daemon_id,
            'version': __version__,
            'platform': platform.platform(),
            'hostname': socket.gethostname(),
            'python': platform.python_version(),
            'cwd': str(self.workspace.root),
            'workspace_label': self.workspace.root.name,
            'shell': shell or '',
            'started_at': self.started_at,
            **git,
        }

    def emit_threadsafe(self, payload):
        if not self.loop or not self.outbox:
            return
        self.loop.call_soon_threadsafe(self._put_nowait, payload)

    def _put_nowait(self, payload):
        try:
            self.outbox.put_nowait(payload)
        except asyncio.QueueFull:
            pass

    async def run_forever(self):
        try:
            import websockets
        except ImportError as exc:
            raise RuntimeError('Install the local daemon dependency with: pip install websockets>=12') from exc
        self.loop = asyncio.get_running_loop()
        delay = 1
        while True:
            try:
                headers = [('Authorization', f'Bearer {self.token}')] if self.token else []
                connect_kwargs = {'ping_interval': None, 'close_timeout': 5, 'max_size': 4 * 1024 * 1024}
                if headers:
                    connect_kwargs['additional_headers'] = headers
                try:
                    connection = websockets.connect(self.ws_url, **connect_kwargs)
                except TypeError:
                    if headers:
                        connect_kwargs.pop('additional_headers', None)
                        connect_kwargs['extra_headers'] = headers
                    connection = websockets.connect(self.ws_url, **connect_kwargs)
                async with connection as ws:
                    print(f'[neby-code] ✓ Connected to {self.ws_url}', flush=True)
                    delay = 1
                    self.outbox = asyncio.Queue(maxsize=1000)
                    await ws.send(json.dumps({'action': 'code.daemon.hello', 'info': self.info()}))
                    sender = asyncio.create_task(self._sender(ws))
                    pinger = asyncio.create_task(self._pinger())
                    dispatches = set()
                    try:
                        async for raw in ws:
                            try:
                                message = json.loads(raw)
                            except Exception:
                                continue
                            if message.get('type') == 'ping' or message.get('action') == 'ping':
                                await self.outbox.put({'action': 'pong', 'type': 'pong', 'time': time.time()})
                                continue
                            if message.get('type') == 'code.hello_ok':
                                print('[neby-code] ✓ Authenticated with server! Local machine is online & active.', flush=True)
                                continue
                            if message.get('type') == 'error':
                                print(f'[neby-code] Server error: {message.get("message") or message.get("code")}', file=sys.stderr, flush=True)
                                continue
                            task = asyncio.create_task(self._dispatch(message))
                            dispatches.add(task)
                            task.add_done_callback(dispatches.discard)
                    finally:
                        self.terminal.cancel_all()
                        sender.cancel()
                        pinger.cancel()
                        for task in tuple(dispatches):
                            task.cancel()
                        await asyncio.gather(sender, pinger, *dispatches, return_exceptions=True)
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                print(f'[neby-code] disconnected: {exc}; retrying in {delay}s', file=sys.stderr, flush=True)
                await asyncio.sleep(delay)
                delay = min(delay * 2, 20)

    async def _sender(self, ws):
        while True:
            payload = await self.outbox.get()
            await ws.send(json.dumps(payload, ensure_ascii=False, default=str))

    async def _pinger(self):
        while True:
            await asyncio.sleep(25)
            await self.outbox.put({'action': 'code.daemon.ping', 'daemon_id': self.daemon_id})

    async def _dispatch(self, message):
        action = str(message.get('action') or '')
        call_id = str(message.get('call_id') or '')
        session_id = str(message.get('session_id') or '')
        args = message.get('args') or {}
        if not call_id:
            return
        print(f'[neby-code] ➜ {action}', flush=True)
        if action == 'term.run':
            await self._run_terminal(call_id, session_id, args)
            return
        if action == 'term.cancel':
            ok = self.terminal.cancel(str(args.get('call_id') or ''))
            await self._result(call_id, ok, {'cancelled': ok}, '' if ok else 'command_not_found')
            return
        try:
            data = await asyncio.to_thread(self._invoke, action, args)
            await self._result(call_id, True, data, '')
        except Exception as exc:
            await self._result(call_id, False, None, str(exc)[:8000])

    async def _run_terminal(self, call_id, session_id, args):
        command = str(args.get('command') or '').strip()
        if not command:
            await self._result(call_id, False, None, 'command is required')
            return
        detached = bool(args.get('detached'))
        timeout_sec = int(args.get('timeout_sec') or 900)
        cwd = str(args.get('cwd') or '.')
        if detached:
            await self._result(call_id, True, {'started': True, 'call_id': call_id}, '')

            def background():
                try:
                    self.terminal.run(call_id, session_id, command, cwd, timeout_sec)
                except Exception as exc:
                    self.emit_threadsafe({
                        'action': 'code.term.data', 'call_id': call_id, 'session_id': session_id,
                        'stream': 'err', 'chunk': f'{exc}\n',
                    })
                    self.emit_threadsafe({
                        'action': 'code.term.exit', 'call_id': call_id, 'session_id': session_id,
                        'exit_code': -1, 'duration_ms': 0, 'stream': 'err', 'chunk': '',
                    })
            threading.Thread(target=background, daemon=True).start()
            return
        try:
            data = await asyncio.to_thread(self.terminal.run, call_id, session_id, command, cwd, timeout_sec)
            await self._result(call_id, True, data, '')
        except Exception as exc:
            await self._result(call_id, False, None, str(exc)[:8000])

    async def _result(self, call_id, ok, data, error):
        await self.outbox.put({
            'action': 'code.result',
            'call_id': call_id,
            'daemon_id': self.daemon_id,
            'ok': bool(ok),
            'data': data,
            'error': error,
        })

    def _invoke(self, action, args):
        if action == 'fs.list':
            return self.workspace.list_dir(args.get('path', '.'), args.get('include_hidden', True))
        if action == 'fs.tree':
            return self.workspace.tree(args.get('path', '.'), args.get('depth', 4), args.get('include_hidden', False))
        if action == 'fs.read':
            return self.workspace.read_file(args.get('path', ''), args.get('start_line', 1), args.get('end_line', 0))
        if action == 'fs.info':
            return self.workspace.info(args.get('path', ''))
        if action == 'fs.find':
            return self.workspace.find_files(args.get('pattern', '*'), args.get('path', '.'), args.get('max_results', 1000))
        if action == 'fs.search':
            return self.workspace.search_files(
                args.get('query', ''), args.get('path', '.'), args.get('glob', '*'),
                args.get('regex', False), args.get('case_sensitive', False), args.get('max_results', 400),
            )
        if action == 'fs.write':
            return self.workspace.write_file(args.get('path', ''), args.get('content', ''), args.get('create_parents', True))
        if action == 'fs.append':
            return self.workspace.append_file(args.get('path', ''), args.get('content', ''), args.get('create_parents', True))
        if action == 'fs.edit':
            return self.workspace.edit_file(args.get('path', ''), args.get('old_text', ''), args.get('new_text', ''), args.get('replace_all', False))
        if action == 'fs.patch':
            return self.workspace.apply_patch(args.get('patch', ''))
        if action == 'fs.mkdir':
            return self.workspace.mkdir(args.get('path', ''))
        if action == 'fs.move':
            return self.workspace.move(args.get('source', ''), args.get('destination', ''), args.get('overwrite', False))
        if action == 'fs.delete':
            return self.workspace.delete(args.get('path', ''), args.get('recursive', False))
        if action == 'git.status':
            return self.workspace.git_status()
        if action == 'git.diff':
            return self.workspace.git_diff(args.get('path', ''), args.get('staged', False), args.get('context', 3))
        if action == 'git.log':
            return self.workspace.git_log(args.get('limit', 30))
        raise WorkspaceError(f'Unsupported action: {action}')


def build_parser():
    parser = argparse.ArgumentParser(prog='neby-code', description='Connect a local workspace to Neby Code')
    parser.add_argument('--workspace', default='.')
    parser.add_argument('--ws-url', default=os.environ.get('NEBY_CODE_WS_URL', ''))
    parser.add_argument('--ticket', default=os.environ.get('NEBY_CODE_TICKET', ''))
    parser.add_argument('--token', default=os.environ.get('NEBY_CODE_TOKEN', ''))
    parser.add_argument('--daemon-id', default='')
    return parser


def main():
    args = build_parser().parse_args()
    daemon = NebyCodeDaemon(args.workspace, args.ws_url, ticket=args.ticket, token=args.token, daemon_id=args.daemon_id)
    print(f'[neby-code] workspace: {daemon.workspace.root}', flush=True)
    print('[neby-code] connecting…', flush=True)
    try:
        asyncio.run(daemon.run_forever())
    except KeyboardInterrupt:
        print('\n[neby-code] stopped', flush=True)


if __name__ == '__main__':
    main()
