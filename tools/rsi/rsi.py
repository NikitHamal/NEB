#!/usr/bin/env python3
"""RSI (Recursive Self-Improvement) Pipeline & Anti-Session-Loss Engine.

Commands:
  python3 tools/rsi/rsi.py pickup              # 1-call session orientation & CI digest
  python3 tools/rsi/rsi.py verify              # Run all Android/CSS/AST/Security guards
  python3 tools/rsi/rsi.py checkpoint "msg"    # Verify + stage + commit + push to origin/main
  python3 tools/rsi/rsi.py ci                  # Poll GitHub Actions runs & failure logs
  python3 tools/rsi/rsi.py deploy              # Dispatch deploy-backend.yml via GitHub API
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
REPO = "NikitHamal/NEB"
GUARDS = [
    ["python3", "tools/android/check_scrollers.py"],
    ["python3", "tools/android/check_insets.py"],
    ["python3", "tools/android/check_sheets.py"],
    ["python3", "tools/android/check_text_fit.py"],
    ["python3", "tools/css/bundle.py", "--check"],
    ["python3", "tools/rsi/security_and_m3x_audit.py"],
]


def _token() -> str:
    helper = pathlib.Path("/tmp/gitenv.sh")
    if helper.is_file():
        try:
            return subprocess.check_output([str(helper)], text=True).strip()
        except Exception:
            pass
    return os.environ.get("GH_PAT", "").strip()


def _gh_api(path: str, method: str = "GET", payload: dict | None = None):
    tok = _token()
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "neb-rsi"}
    if tok:
        headers["Authorization"] = f"token {tok}"
    data = json.dumps(payload).encode() if payload is not None else None
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read()
        return json.loads(raw.decode()) if raw else {}


def cmd_pickup() -> int:
    print("=== RSI PICKUP: GIT & WORKSPACE ===")
    subprocess.run(["git", "status", "-sb"], cwd=ROOT, check=False)
    subprocess.run(["git", "log", "-n", "6", "--oneline"], cwd=ROOT, check=False)
    status_md = ROOT / "ANDROID_STATUS.md"
    if status_md.is_file():
        lines = status_md.read_text(encoding="utf-8").splitlines()
        sessions = [i for i, l in enumerate(lines) if l.startswith("# Session ")]
        start = sessions[-1] if sessions else max(0, len(lines) - 40)
        print("\n=== LATEST ANDROID_STATUS.md SESSION ===")
        print("\n".join(lines[start : start + 35]))
    print("\n=== LATEST GITHUB ACTIONS RUNS ===")
    return cmd_ci()


def cmd_verify() -> int:
    for cmd in GUARDS:
        r = subprocess.run(cmd, cwd=ROOT)
        if r.returncode != 0:
            print(f"RSI VERIFY FAILED on: {' '.join(cmd)}", file=sys.stderr)
            return r.returncode
    return 0


def cmd_checkpoint(msg: str) -> int:
    if not msg.strip():
        print("ERROR: commit message required", file=sys.stderr)
        return 2
    if cmd_verify() != 0:
        return 1
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    # Never stage sandbox-only package.json if excluded
    subprocess.run(["git", "reset", "-q", "HEAD", "--", "package.json"], cwd=ROOT, check=False)
    if subprocess.run(["python3", "tools/rsi/security_and_m3x_audit.py"], cwd=ROOT).returncode != 0:
        return 1
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if diff.returncode == 0:
        print("RSI CHECKPOINT: clean working tree, nothing to commit.")
        return 0
    subprocess.run(["git", "commit", "-m", msg], cwd=ROOT, check=True)
    env = {**os.environ, "GIT_ASKPASS": "/tmp/gitenv.sh", "GIT_TERMINAL_PROMPT": "0"}
    subprocess.run(["git", "pull", "--rebase", "--autostash", "origin", "main"], cwd=ROOT, env=env, check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, env=env, check=True)
    print(f"RSI CHECKPOINT PUSHED: {msg}")
    return 0


def cmd_ci() -> int:
    try:
        data = _gh_api("actions/runs?branch=main&per_page=5")
        for r in data.get("workflow_runs", []):
            rid = r.get("id")
            status = r.get("status")
            conc = r.get("conclusion")
            print(f"  [{r.get('name')}] id={rid} status={status} conclusion={conc} sha={r.get('head_sha', '')[:7]}")
            if status == "in_progress" and rid:
                jobs = _gh_api(f"actions/runs/{rid}/jobs").get("jobs", [])
                for j in jobs:
                    for s in j.get("steps", []):
                        if s.get("status") == "in_progress":
                            print(f"    -> active step: {s.get('name')}")
            elif status == "completed" and conc == "failure" and rid:
                jobs = _gh_api(f"actions/runs/{rid}/jobs").get("jobs", [])
                for j in jobs:
                    for s in j.get("steps", []):
                        if s.get("conclusion") == "failure":
                            print(f"    -> FAILED STEP in {j.get('name')}: {s.get('name')}")
    except Exception as exc:
        print(f"CI query warning: {exc}", file=sys.stderr)
    return 0


def cmd_deploy() -> int:
    _gh_api("actions/workflows/deploy-backend.yml/dispatches", method="POST", payload={"ref": "main"})
    print("RSI DEPLOY: dispatched deploy-backend.yml on main")
    return 0


def main() -> int:
    arg = sys.argv[1] if len(sys.argv) > 1 else "pickup"
    if arg == "pickup":
        return cmd_pickup()
    if arg == "verify":
        return cmd_verify()
    if arg == "checkpoint":
        return cmd_checkpoint(" ".join(sys.argv[2:]))
    if arg == "ci":
        return cmd_ci()
    if arg == "deploy":
        return cmd_deploy()
    print(f"Unknown command: {arg}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
