#!/usr/bin/env python3
"""Delta backend deploy over an SSH exec channel (same protocol as
backend_python/scratch/deploy.ps1, which is PowerShell and Windows-only).

Runs on the GitHub Actions ubuntu-latest runner. All inputs come from
environment variables whose values are repository secrets or fixed
constants; the private key never appears in logs and the key file is
deleted on exit.

Why an exec channel and not SCP/SFTP: the cPanel box kills SFTP
subsystem and scp connections, but allows exec channels, and the
delta ZIP plus the restart script are streamed through them with
`ssh ... "cat > dest"`.

Deploy contract (identical to deploy.ps1):
  1. Build a local manifest (relpath -> MD5) of the payload.
  2. Fetch the server manifest and diff it.
  3. Stream ONLY changed files plus the new manifest over one SSH
     exec channel. Deleted files are listed for removal.
  4. Upload the remote bash script and run it detached with a pid
     file lock and a status file, then poll the status file to
     completion. Losing the runner mid-deploy cannot half-apply
     anything: the script either does not start or runs to the end.
  5. On the box, migrations run BEFORE collectstatic, pip install
     only runs when requirements.txt changed, and LSAPI workers are
     recycled only when something changed.

Environment (set by .github/workflows/deploy-backend.yml):
  SSH_HOST    - server IP or hostname (secret: SSH_HOST)
  SSH_KEY     - PEM private key text (secret: SSH_KEY)
  SSH_USER    - fixed (consicac)
  REMOTE_DIR  - fixed (/home/consicac/nebians_api)
  VENV_PY     - fixed (/home/consicac/virtualenv/nebians_api/3.13/bin/python)
"""
import collections
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import uuid
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND = os.path.join(REPO_ROOT, "backend_python")
RESTART_WORKERS = os.path.join(BACKEND, "scratch", "restart_workers.sh")

ITEMS = [
    "api",
    "nebians",
    "web",
    "services",
    "public",
    "manage.py",
    "requirements.txt",
    "passenger_wsgi.py",
]

SSH_HOST = os.environ.get("SSH_HOST", "").strip()
SSH_KEY = os.environ.get("SSH_KEY", "")
SSH_USER = os.environ.get("SSH_USER", "consicac").strip() or "consicac"
REMOTE_DIR = os.environ.get("REMOTE_DIR", "/home/consicac/nebians_api").strip() or "/home/consicac/nebians_api"
VENV_PY = os.environ.get("VENV_PY", "/home/consicac/virtualenv/nebians_api/3.13/bin/python").strip()

if not SSH_HOST or not SSH_KEY:
    print("ERROR: SSH_HOST / SSH_KEY not set. The workflow must inject both secrets.", file=sys.stderr)
    sys.exit(2)


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest():
    manifest = {}
    for item in ITEMS:
        full = os.path.join(BACKEND, item)
        if os.path.isfile(full):
            manifest[item] = md5(full)
        elif os.path.isdir(full):
            for root, dirs, files in os.walk(full):
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                for name in files:
                    if name.endswith(".pyc"):
                        continue
                    fpath = os.path.join(root, name)
                    rel = os.path.relpath(fpath, BACKEND).replace("\\", "/")
                    try:
                        manifest[rel] = md5(fpath)
                    except Exception as exc:
                        print(f"Warning skipping {fpath}: {exc}", file=sys.stderr)
    return manifest


class Ssh:
    def __init__(self, host, user, key_text):
        fd, self.key_path = tempfile.mkstemp(prefix="neb_ci_key_", suffix=".pem")
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w") as fh:
            fh.write(key_text if key_text.endswith("\n") else key_text + "\n")

    def base(self):
        return [
            "ssh", "-o", "ConnectTimeout=30", "-o", "StrictHostKeyChecking=no",
            "-o", "ServerAliveInterval=15", "-o", "ServerAliveCountMax=3",
            "-i", self.key_path, "-p", "22", f"{SSH_USER}@{SSH_HOST}",
        ]

    def run(self, remote_cmd, timeout=120, input_data=None, check=False):
        r = subprocess.run(self.base() + [remote_cmd], input=input_data,
                           capture_output=True, timeout=timeout)
        if check and r.returncode != 0:
            raise RuntimeError(f"ssh failed ({r.returncode}): {r.stderr.decode('utf-8', 'replace')[:400]}")
        return r

    def cat(self, remote_path, timeout=60):
        out = ""
        for attempt in range(1, 4):
            try:
                r = self.run(f"cat {remote_path} 2>/dev/null", timeout=timeout)
                out = r.stdout.decode("utf-8", "replace")
                break
            except subprocess.TimeoutExpired:
                print(f"cat attempt {attempt} timed out", file=sys.stderr)
                time.sleep(3)
        return out

    def upload(self, local_bytes, remote_path, desc, timeout=600):
        last = None
        for attempt in range(1, 6):
            try:
                r = self.run(f"cat > {remote_path}", timeout=timeout, input_data=local_bytes)
                if r.returncode == 0:
                    print(f"UPLOAD OK {desc} attempt={attempt} bytes={len(local_bytes)}")
                    return
                last = r.stderr.decode("utf-8", "replace")[:200]
            except subprocess.TimeoutExpired as exc:
                last = str(exc)
            print(f"UPLOAD {desc} attempt {attempt} failed: {last}", file=sys.stderr)
        raise RuntimeError(f"Failed to upload {desc} after 5 attempts ({last}).")


def main():
    local = build_manifest()
    print(f"Local manifest: {len(local)} files")
    ssh = Ssh(SSH_HOST, SSH_USER, SSH_KEY)
    try:
        raw = ssh.cat(f"{REMOTE_DIR}/.deploy_manifest.json")
        remote = {}
        if raw and len(raw.strip()) > 2:
            try:
                # The box may hold `.deploy_manifest.json` with no newline at end;
                # a trailing NUL or implicit truncation is handled by json.loads.
                remote = json.loads(raw)
                print(f"Server manifest: {len(remote)} files")
            except Exception:
                print("Server manifest unreadable - treating as empty (full upload).")
        else:
            print("No server manifest yet - this deploy uploads the full payload.")

        changed = sorted(k for k in local if remote.get(k) != local[k])
        deleted = sorted(k for k in remote if k not in local)
        py_changed = any(k.endswith(".py") for k in changed)
        req_changed = "requirements.txt" in changed
        static_changed = any(k.startswith("web/static/") for k in changed)
        static_deleted = any(k.startswith("web/static/") for k in deleted)
        any_changed = bool(changed or deleted)
        print(f"Delta: {len(changed)} changed, {len(deleted)} removed "
              f"(py={py_changed} req={req_changed} static={static_changed} staticGone={static_deleted})")
        if 0 < len(changed) <= 30:
            for rel in changed:
                print(f"  ~ {rel}")

        deploy_zip = None
        if any_changed:
            fd, zip_path = tempfile.mkstemp(prefix="neb_ci_deploy_", suffix=".zip")
            os.close(fd)
            try:
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for rel in changed:
                        zf.write(os.path.join(BACKEND, rel), rel)
                    # The manifest lands atomically AFTER extraction (see remote script).
                    manifest_json = json.dumps(local, sort_keys=True).encode()
                    zf.writestr(".deploy_manifest.json.tmp", manifest_json)
                    if deleted:
                        zf.writestr(".deploy_delete.txt", "\n".join(deleted) + "\n")
                print(f"DELTAZIP entries={len(changed)} bytes={os.path.getsize(zip_path)}")
                with open(zip_path, "rb") as fh:
                    data = fh.read()
                ssh.upload(data, f"{REMOTE_DIR}/deploy.zip", "deploy.zip")
            finally:
                os.unlink(zip_path)

        if os.path.exists(RESTART_WORKERS):
            with open(RESTART_WORKERS, "rb") as fh:
                ssh.upload(fh.read(), "/tmp/restart_workers.sh", "restart_workers.sh", timeout=60)
        else:
            print(f"WARNING: restart workers script not found at {RESTART_WORKERS} - skipping.", file=sys.stderr)

        stamp = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
        status_file = f"/tmp/neb_deploy_{stamp}.status"
        log_file = f"/tmp/neb_deploy_{stamp}.log"
        runner_path = f"/tmp/neb_deploy_{stamp}.sh"

        remote = [
            f"echo 'STATUS: RUNNING' > {status_file}",
            "LOCK=/tmp/neb_deploy.lock",
            'if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then '
            f'echo "STATUS: FAILED another deploy (pid $(cat "$LOCK")) is still running" > {status_file}; exit 9; fi',
            'echo $$ > "$LOCK"',
            'trap "rm -f $LOCK" EXIT',
            f"cd {REMOTE_DIR}",
        ]
        if any_changed:
            remote.append("echo 'Extracting changed file(s)...'")
            # Zip entries carry the runner's UTC wall clock with no zone; unzip reads them as the
            # box's local time (UTC+5:45), so extracted files looked ~6 h OLD. collectstatic skips a
            # file whose copy is newer than its source, so any static edit shipped within 6 h of the
            # previous deploy was silently dropped (admin analytics CSS stayed stale for days).
            # Stamp every extracted file with the real time right after extraction.
            remote.append("unzip -Z1 deploy.zip | grep -v '^[.]deploy_' > .deploy_changed.txt || true")
            # The manifest is committed only after migrate and collectstatic passed (see STATUS: OK below). Moving it
            # here left it ahead of the server when a later step failed, so the next delta skipped the files.
            remote.append("unzip -o deploy.zip >/dev/null || { echo 'UNZIP FAILED'; exit 1; }")
            remote.append("xargs -d '\\n' -r touch < .deploy_changed.txt; rm -f .deploy_changed.txt")
            remote.append("rm -f deploy.zip")
            if deleted:
                remote.append("echo 'Removing retired file(s)...'")
                remote.append("xargs -d '\\n' -r rm -f < .deploy_delete.txt")
                remote.append("rm -f .deploy_delete.txt")
        else:
            remote.append("echo 'No file changes - payload already up to date.'")
            remote.append("rm -f deploy.zip .deploy_manifest.json.tmp")

        if py_changed:
            remote.append("echo 'Clearing Python bytecode cache...'")
            remote.append("find . -name '*.pyc' -delete 2>/dev/null")
            remote.append("find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null")
            # Recycle LSAPI workers BEFORE migrate as well so no old worker with dropped ORM fields
            # can execute SELECT against a column while/after migrate drops it.
            remote.append(f"pkill -f 'lswsgi -m {REMOTE_DIR}/passenger_wsg[i].py' 2>/dev/null || true")
            remote.append("echo 'Cache cleared and stale workers recycled.'")

        # Keep server-side cron watchdog.sh aligned with restart_workers.sh (retire daphne when WS_PUBLIC_URL is unset).
        remote.append(
            "if [ -f watchdog.sh ] && ! grep -q 'WANT_DAPHNE' watchdog.sh 2>/dev/null; then "
            "sed -i 's|if ! pgrep -f \"daphne.\\*\\$REALTIME_PORT\" > /dev/null; then|"
            "WANT_DAPHNE=$(grep -E \"^(WS_PUBLIC_URL=.+|ENABLE_DAPHNE=1)\" \"$APP/.env\" 2>/dev/null \\| head -1); "
            "if [ -n \"$WANT_DAPHNE\" ] \\&\\& ! pgrep -f \"daphne.*$REALTIME_PORT\" > /dev/null; then|' watchdog.sh || true; "
            "fi"
        )

        remote.append("echo 'Removing retired files no longer shipped in the payload...'")
        remote.append("rm -f api/ai4bharat_proxy.py")
        remote.append("rm -f api/management/commands/arena_smoke_test.py")
        remote.append("rm -f api/management/commands/arena_e2e_test.py")
        remote.append("rm -f api/coding_agent/queue.py")
        remote.append("echo 'Retired files cleaned.'")

        remote.append(f"source /home/consicac/virtualenv/nebians_api/3.13/bin/activate")
        remote.append("export OPENBLAS_NUM_THREADS=1")
        remote.append("export OMP_NUM_THREADS=1")
        remote.append("export MKL_NUM_THREADS=1")

        # No separate `manage.py check`: migrate runs the same system checks, and
        # every extra Django boot costs 10-30 s on the loaded shared host.

        if req_changed:
            remote.append("echo 'Installing dependencies...'")
            remote.append("pip install -r requirements.txt")

        # Migrations BEFORE collectstatic, identical ordering to deploy.ps1.
        if py_changed:
            remote.append("echo 'Running database migrations (before collectstatic, so code never runs ahead of schema)...'")
            remote.append(f"python manage.py migrate || {{ echo 'MIGRATE FAILED - stopping before static/restart'; echo 'STATUS: FAILED migrate' > {status_file}; exit 1; }}")
            # Immediately recycle LSAPI workers right after migrate so no running worker
            # keeps old ORM model fields in memory while background backfills/collectstatic run.
            remote.append(f"pkill -f 'lswsgi -m {REMOTE_DIR}/passenger_wsg[i].py' 2>/dev/null || true")
            # Bounded: videos ffmpeg cannot read stay "without cover" and were retried
            # in full on every deploy. A few per deploy, never more than two minutes.
            remote.append("echo 'Backfilling video thumbnails (bounded)...'")
            remote.append("timeout 120 python manage.py backfill_video_thumbnails --limit 10 || true")
            # Avatars were stored as uploaded (1 to 1.4 MB). Writes small WebP copies next to
            # them and repoints the URL columns; originals are kept. No-op once all are done.
            remote.append("echo 'Shrinking oversized profile photos (bounded, originals kept)...'")
            remote.append("timeout 150 python manage.py optimize_profile_photos --limit 40 || true")
            # Small list copies (192 px avatars, 480 px covers) that feeds and cards prefer.
            # Time-boxed, newest first, originals untouched; the rest finishes on later deploys.
            remote.append("echo 'Writing small list copies of avatars and covers (bounded)...'")
            remote.append("timeout 100 python manage.py make_list_copies --seconds 70 || true")

        resync = os.environ.get("STATIC_RESYNC_DIR", "").strip()
        if resync and re.fullmatch(r"web/static/[A-Za-z0-9_./-]*", resync) and ".." not in resync:
            # One-time repair for static files an earlier deploy dropped (see the unzip note above).
            remote.append(f"echo 'Re-stamping {resync} so collectstatic re-copies it...'")
            remote.append(f"find {resync} -type f -size -1M -exec touch {{}} +")
            static_changed = True
        if static_changed or static_deleted:
            clear = "--clear" if static_deleted else ""
            remote.append("echo 'Running collectstatic...'")
            remote.append(f"python manage.py collectstatic --noinput {clear} || {{ echo 'COLLECTSTATIC FAILED - stopping before restart'; echo 'STATUS: FAILED collectstatic' > {status_file}; exit 1; }}")

        remote.append("echo 'Deploying favicon.ico to site root for /favicon.ico serving...'")
        remote.append("cp -f web/static/web/img/favicon.ico public/favicon.ico")
        remote.append("cp -f web/static/web/img/favicon.ico /home/consicac/nebians.consica.com.np/favicon.ico 2>/dev/null || true")

        ws_py = (
            "import glob, re, os\n"
            "candidates = []\n"
            "paths = [\n"
            "    '/home/consicac/nebians_api/logs/start_ws_tunnel.log',\n"
            "    '/home/consicac/nebians_api/logs/cloudflared.log',\n"
            "    'logs/cloudflared.log',\n"
            "] + sorted(glob.glob('/tmp/cf_quick*.log'), reverse=True)\n"
            "for p in paths:\n"
            "    try:\n"
            "        with open(p) as f:\n"
            "            c = f.read()\n"
            "        ms = re.findall(r'(?:wss?|https?)://([a-z0-9-]+\\.trycloudflare\\.com)', c)\n"
            "        if ms:\n"
            "            u = 'wss://' + ms[-1] + '/ws/'\n"
            "            try:\n"
            "                mtime = os.path.getmtime(p)\n"
            "            except:\n"
            "                mtime = 0\n"
            "            candidates.append((mtime, u, p))\n"
            "    except Exception:\n"
            "        continue\n"
            "if candidates:\n"
            "    candidates.sort(key=lambda x: x[0], reverse=True)\n"
            "    u = candidates[0][1]\n"
            "    src = candidates[0][2]\n"
            "    with open('ws_url.txt', 'w') as wf:\n"
            "        wf.write(u + '\\n')\n"
            "    print(f'WS URL: {u} (from {src} mtime={candidates[0][0]})')\n"
            "else:\n"
            "    try:\n"
            "        with open('ws_url.txt') as f:\n"
            "            c = f.read().strip()\n"
            "        m = re.search(r'([a-z0-9-]+\\.trycloudflare\\.com)', c)\n"
            "        if m:\n"
            "            u = 'wss://' + m.group(1) + '/ws/'\n"
            "            print(f'WS URL (fallback ws_url.txt): {u}')\n"
            "        else:\n"
            "            print('WARNING: could not resolve WS tunnel URL from logs or ws_url.txt')\n"
            "    except Exception:\n"
            "        print('WARNING: could not resolve WS tunnel URL')\n"
            "    if not os.path.exists('ws_url.txt'):\n"
            "        with open('ws_url.txt', 'w') as wf:\n"
            "            wf.write('\\n')\n"
        )
        remote.append("python3 << 'PYEOF'")
        remote.extend(ws_py.rstrip("\n").split("\n"))
        remote.append("PYEOF")

        if py_changed:
            remote.append("echo 'Restarting background agent worker (autofix watcher removed Sep 2026)...'")
            remote.append("tr -d '\\r' < /tmp/restart_workers.sh | bash")

        if any_changed or static_changed:
            # WhiteNoise indexes static files (size, mtime) at worker start. A worker that outlives a
            # collectstatic sends the old Content-Length with the new bytes: HTTP/2 PROTOCOL_ERROR and
            # an unstyled page. So recycle workers whenever static was re-copied, even with no delta.
            remote.append("echo 'Restarting LSAPI workers (touch restart.txt alone does NOT recycle healthy workers)...'")
            # Bracket trick so the remote shell running this script does not
            # match its own cmdline and kill this SSH session.
            remote.append(f"pkill -f 'lswsgi -m {REMOTE_DIR}/passenger_wsg[i].py' 2>/dev/null || true")
            remote.append("sleep 2")
            # The next request forks a new LSAPI parent (it imports Django and warms the
            # site, several seconds on this host). Make that request ours, not a visitor's.
            remote.append("echo 'Warming the new workers...'")
            remote.append("for i in 1 2 3; do curl -s -m 60 -o /dev/null -w 'warm %{http_code} %{time_total}s\\n' https://nebians.consica.com.np/api/realtime/config/ && break; sleep 3; done || true")
            remote.append("curl -s -m 60 -o /dev/null -w 'posts %{http_code} %{time_total}s\\n' https://nebians.consica.com.np/api/posts/ || true")

        remote.append("[ -f .deploy_manifest.json.tmp ] && mv -f .deploy_manifest.json.tmp .deploy_manifest.json || true")
        remote.append(f"echo 'STATUS: OK' > {status_file}")
        remote.append("echo 'DEPLOYMENT SUCCESSFUL'")

        # Time-stamp each step so a slow deploy shows where it spent the time.
        remote = [
            ("echo \"[$(date +%T)] " + r[len("echo '"):-1] + "\"")
            if r.startswith("echo '") and r.endswith("'") and "\"" not in r and "$" not in r and "`" not in r
            else r
            for r in remote
        ]
        script_text = "\n".join(remote) + "\n"
        ssh.upload(script_text.encode(), runner_path, "deploy runner", timeout=60)

        print("Launching server-side phase detached (log: %s)" % log_file)
        # Two SSH calls on purpose: chaining with && into one command makes
        # the trailing "&" background the WHOLE chain (&& binds tighter than
        # &), so the SSH channel stays open for the entire deploy and the
        # client blocks until collectstatic finishes instead of returning.
        # The first call only normalises the script; the second only launches.
        ssh.run(
            f"tr -d '\\r' < {runner_path} > {runner_path}.lf && mv -f {runner_path}.lf {runner_path} && chmod +x {runner_path} && echo PREPARED",
            timeout=30, check=True,
        )
        ssh.run(
            f"setsid nohup bash {runner_path} > {log_file} 2>&1 < /dev/null & echo LAUNCHED",
            timeout=30, check=True,
        )

        status = ""
        deadline = time.time() + 35 * 60
        while time.time() < deadline:
            time.sleep(5)
            status = ssh.cat(status_file, timeout=15).strip()
            if "STATUS: OK" in status or "STATUS: FAILED" in status:
                break
            print(".", end="", flush=True)
        print()
        print(f"Remote status: {status or 'UNKNOWN (status file empty - deploy may still be running)'}")
        print(f"--- remote log tail ({log_file}) ---")
        r = ssh.run(f"tail -n 40 {log_file} 2>/dev/null", timeout=30)
        sys.stdout.write(r.stdout.decode("utf-8", "replace"))
        if "STATUS: OK" not in status:
            print(f"ERROR: deploy did not report success (status: '{status}').", file=sys.stderr)
            print(f"Check: ssh ... tail -f {log_file}", file=sys.stderr)
            sys.exit(1)
        print("DEPLOYMENT SUCCESSFUL")
    finally:
        try:
            os.unlink(ssh.key_path)
        except Exception:
            pass


if __name__ == "__main__":
    main()
