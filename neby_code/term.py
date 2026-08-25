"""Terminal command execution with streamed output."""
import os
import subprocess
import threading
import time
import uuid

MAX_TAIL = 16000


class Terminal:
    def __init__(self, cwd: str, emit):
        self.cwd = cwd
        self._emit = emit
        self._procs = {}

    def run(self, command: str, timeout_sec: int = 300, session_id: str = '', call_id: str = '') -> dict:
        timeout_sec = max(3, min(int(timeout_sec or 300), 1800))
        shell = True
        kwargs = {}
        creationflags = 0
        if os.name == 'nt':
            creationflags = subprocess.CREATE_NO_WINDOW
            kwargs['creationflags'] = creationflags
        t0 = time.monotonic()
        proc = subprocess.Popen(
            command, shell=shell, cwd=self.cwd,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, errors='replace', bufsize=1,
            start_new_session=(os.name != 'nt'),
            **kwargs,
        )
        self._procs[call_id] = proc
        tail = []
        try:
            for line in iter(proc.stdout.readline, ''):
                if not line:
                    break
                tail.append(line)
                if len(tail) <= 400:
                    self._stream(call_id, session_id, line)
                if time.monotonic() - t0 > timeout_sec:
                    self._kill(proc)
                    break
        finally:
            try:
                proc.stdout.close()
            except Exception:  # noqa: BLE001
                pass
        code = None
        try:
            code = proc.wait(timeout=10)
        except Exception:  # noqa: BLE001
            self._kill(proc)
            code = -1
        duration_ms = int((time.monotonic() - t0) * 1000)
        self._procs.pop(call_id, None)
        text_tail = ''.join(tail[-200:])
        return {
            'exit_code': code,
            'duration_ms': duration_ms,
            'stdout_tail': text_tail[-MAX_TAIL:],
            'stderr_tail': '',
        }

    def _stream(self, call_id: str, session_id: str, chunk: str):
        try:
            self._emit({
                'action': 'code.term.data',
                'call_id': call_id,
                'session_id': session_id,
                'chunk': chunk,
                'stream': 'out',
            })
        except Exception:  # noqa: BLE001
            pass

    @staticmethod
    def _kill(proc):
        try:
            if os.name == 'nt':
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(proc.pid)],
                               capture_output=True)
            else:
                import signal
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except Exception:  # noqa: BLE001
            try:
                proc.kill()
            except Exception:  # noqa: BLE001
                pass

    def kill_all(self):
        for proc in list(self._procs.values()):
            self._kill(proc)


def new_call_id() -> str:
    return uuid.uuid4().hex[:16]


def stream_thread(fn):
    t = threading.Thread(target=fn, daemon=True)
    t.start()
    return t
