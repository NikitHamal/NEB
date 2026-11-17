#!/usr/bin/env python3
"""RSI (Recursive Self-Improvement) Pipeline v2 & Anti-Session-Loss Engine.

Commands:
  python3 tools/rsi/rsi.py pickup              # 1-call session orientation & CI digest
  python3 tools/rsi/rsi.py map <query>         # Instant git ls-files path & line-count mapper
  python3 tools/rsi/rsi.py bundle              # Rebuild all CSS bundles (tools/css/bundle.py)
  python3 tools/rsi/rsi.py verify              # Auto-bundle CSS + run all Android/CSS/AST/Security guards
  python3 tools/rsi/rsi.py checkpoint "msg"    # Verify + stage + secret-scan + commit + push to origin/main
  python3 tools/rsi/rsi.py ci                  # Poll GitHub Actions runs + auto-fetch failure log tails
  python3 tools/rsi/rsi.py deploy              # Dispatch deploy-backend.yml via GitHub API
"""
from __future__ import annotations

import json
import os
import pathlib
import re
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


def _gh_api(path: str, method: str = "GET", payload: dict | None = None, raw_text: bool = False):
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
        if raw_text:
            return raw.decode("utf-8", errors="replace")
        return json.loads(raw.decode()) if raw else {}


def cmd_pickup() -> int:
    print("=== RSI v2 PICKUP: GIT & WORKSPACE ===")
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


def cmd_map(query: str) -> int:
    out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    rx = re.compile(query or ".", re.I)
    matches = [p for p in out.splitlines() if rx.search(p)]
    print(f"=== RSI MAP ({len(matches)} matches for '{query}') ===")
    for rel in matches[:60]:
        fp = ROOT / rel
        try:
            n = sum(1 for _ in fp.open("rb")) if fp.is_file() else 0
            print(f"  {rel} ({n} lines)")
        except Exception:
            print(f"  {rel}")
    if len(matches) > 60:
        print(f"  ... and {len(matches) - 60} more")
    return 0


def cmd_bundle() -> int:
    return subprocess.run(["python3", "tools/css/bundle.py"], cwd=ROOT).returncode


def cmd_verify() -> int:
    # Auto-rebuild CSS bundles if source CSS changed so checkpoints never fail on stale bundles.
    if subprocess.run(["python3", "tools/css/bundle.py", "--check"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
        print("RSI VERIFY: auto-rebuilding CSS bundles via tools/css/bundle.py...")
        subprocess.run(["python3", "tools/css/bundle.py"], cwd=ROOT, check=False)
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
        seen_names: set[str] = set()
        for r in data.get("workflow_runs", []):
            rid = r.get("id")
            name = r.get("name") or ""
            is_latest_for_workflow = name not in seen_names
            seen_names.add(name)
            status = r.get("status")
            conc = r.get("conclusion")
            print(f"  [{name}] id={rid} status={status} conclusion={conc} sha={r.get('head_sha', '')[:7]}")
            if status == "in_progress" and rid:
                for j in _gh_api(f"actions/runs/{rid}/jobs").get("jobs", []):
                    for s in j.get("steps", []):
                        if s.get("status") == "in_progress":
                            print(f"    -> active step: {s.get('name')}")
            elif status == "completed" and conc == "failure" and rid and is_latest_for_workflow:
                for j in _gh_api(f"actions/runs/{rid}/jobs").get("jobs", []):
                    for s in j.get("steps", []):
                        if s.get("conclusion") == "failure":
                            print(f"    -> FAILED STEP in {j.get('name')}: {s.get('name')}")
                    if j.get("conclusion") == "failure" and j.get("id"):
                        try:
                            tok = _token()
                            log_txt = subprocess.check_output(
                                ["curl", "-sL", "-H", f"Authorization: token {tok}",
                                 f"https://api.github.com/repos/{REPO}/actions/jobs/{j['id']}/logs"],
                                text=True, timeout=15,
                            )
                            tail = [ln for ln in log_txt.splitlines() if any(w in ln.lower() for w in ("error", "fail", "exception", "traceback", "line "))][-12:]
                            for ln in tail:
                                print(f"       {ln[:160]}")
                        except Exception:
                            pass
    except Exception as exc:
        print(f"CI query warning: {exc}", file=sys.stderr)
    return 0


def cmd_deploy(static_dir: str = "") -> int:
    payload = {"ref": "main"}
    if static_dir:
        payload["inputs"] = {"static_resync_dir": static_dir}
    _gh_api("actions/workflows/deploy-backend.yml/dispatches", method="POST", payload=payload)
    print(f"RSI DEPLOY: dispatched deploy-backend.yml on main (static resync: {static_dir or 'none'})")
    return 0


# asset -> a selector the repo copy has and an old copy lacks (live files are minified, so no byte compare)
LIVE_ASSETS = {
    "web/static/web/css/admin.css": ".an-insight",
    "web/static/web/css/admin/03-analytics.css": ".an-insight",
}


def cmd_live() -> int:
    """Compare the shipped static files with the repo (catches a deploy that went green but dropped files)."""
    import urllib.request
    bad = 0
    for rel, marker in LIVE_ASSETS.items():
        local = os.path.join("backend_python", rel)
        if not os.path.exists(local):
            continue
        url = "https://nebians.consica.com.np/static/" + rel[len("web/static/"):]
        try:
            req = urllib.request.Request(url + "?rsi=1", headers={"User-Agent": "rsi-live"})
            live = urllib.request.urlopen(req, timeout=25).read()
        except Exception as exc:  # noqa: BLE001
            print(f"  ?? {rel}: {exc}")
            continue
        same = marker.encode() in live or marker.encode() not in open(local, "rb").read()
        print(f"  {'OK   ' if same else 'STALE'} {rel} live={len(live)}B repo={os.path.getsize(local)}B")
        bad += 0 if same else 1
    if bad:
        print("STALE static on live: run `python3 tools/rsi/rsi.py deploy web/static/web/css`")
    return 1 if bad else 0


def main() -> int:
    arg = sys.argv[1] if len(sys.argv) > 1 else "pickup"
    if arg == "pickup":
        return cmd_pickup()
    if arg == "map":
        return cmd_map(" ".join(sys.argv[2:]))
    if arg == "bundle":
        return cmd_bundle()
    if arg in ("verify", "audit"):
        return cmd_verify()
    if arg == "checkpoint":
        return cmd_checkpoint(" ".join(sys.argv[2:]))
    if arg == "ci":
        return cmd_ci()
    if arg == "deploy":
        return cmd_deploy(sys.argv[2] if len(sys.argv) > 2 else "")
    if arg == "live":
        return cmd_live()
    print(f"Unknown command: {arg}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
