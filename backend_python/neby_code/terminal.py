from __future__ import annotations

import os
import signal
import subprocess
import threading
import time
from pathlib import Path


class TerminalRunner:
    def __init__(self, workspace, emit):
        self.workspace = workspace
        self.emit = emit
        self._processes = {}
        self._lock = threading.Lock()

    def run(self, call_id, session_id, command, cwd='.', timeout_sec=900):
        cwd_path = self.workspace.rel(cwd)
        if not cwd_path.is_dir():
            raise RuntimeError(f'Working directory not found: {cwd}')
        timeout_sec = max(1, min(int(timeout_sec or 900), 7200))
        started = time.monotonic()
        creationflags = 0
        preexec_fn = None
        if os.name == 'nt':
            creationflags = getattr(subprocess, 'CREATE_NO_WINDOW', 0) | getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0)
        else:
            preexec_fn = os.setsid
        process = subprocess.Popen(
            command,
            cwd=str(cwd_path),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,
            creationflags=creationflags,
            preexec_fn=preexec_fn,
        )
        with self._lock:
            self._processes[call_id] = process
        tails = {'out': [], 'err': []}

        def pump(stream, name):
            try:
                for chunk in iter(stream.readline, ''):
                    if not chunk:
                        break
                    tails[name].append(chunk)
                    if sum(len(x) for x in tails[name]) > 16000:
                        tails[name] = [''.join(tails[name])[-12000:]]
                    self.emit({
                        'action': 'code.term.data',
                        'call_id': call_id,
                        'session_id': session_id,
                        'stream': name,
                        'chunk': chunk,
                    })
            finally:
                try:
                    stream.close()
                except Exception:
                    pass

        out_thread = threading.Thread(target=pump, args=(process.stdout, 'out'), daemon=True)
        err_thread = threading.Thread(target=pump, args=(process.stderr, 'err'), daemon=True)
        out_thread.start()
        err_thread.start()
        timed_out = False
        try:
            process.wait(timeout=timeout_sec)
        except subprocess.TimeoutExpired:
            timed_out = True
            self._terminate_process(process)
            process.wait(timeout=10)
        finally:
            out_thread.join(timeout=2)
            err_thread.join(timeout=2)
            with self._lock:
                self._processes.pop(call_id, None)
        elapsed = int((time.monotonic() - started) * 1000)
        result = {
            'exit_code': process.returncode,
            'duration_ms': elapsed,
            'timed_out': timed_out,
            'stdout_tail': ''.join(tails['out'])[-12000:],
            'stderr_tail': ''.join(tails['err'])[-12000:],
        }
        self.emit({
            'action': 'code.term.exit',
            'call_id': call_id,
            'session_id': session_id,
            'exit_code': process.returncode,
            'duration_ms': elapsed,
            'stream': 'out',
            'chunk': '',
        })
        return result

    def cancel(self, call_id):
        with self._lock:
            process = self._processes.get(call_id)
        if not process:
            return False
        self._terminate_process(process)
        return True

    def cancel_all(self):
        with self._lock:
            processes = list(self._processes.values())
        for process in processes:
            self._terminate_process(process)

    @staticmethod
    def _terminate_process(process):
        if process.poll() is not None:
            return
        try:
            if os.name == 'nt':
                subprocess.run(
                    ['taskkill', '/PID', str(process.pid), '/T', '/F'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10,
                )
            else:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except Exception:
            try:
                process.kill()
            except Exception:
                pass
