#!/usr/bin/env python3
"""Static AST, secret-leak, security & M3X compliance guard for RSI pipeline."""
from __future__ import annotations

import ast
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{40,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
]


def check_staged_secrets() -> list[str]:
    errors: list[str] = []
    try:
        diff = subprocess.check_output(
            ["git", "diff", "--cached", "-U0"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        )
    except Exception:
        diff = ""
    for line in diff.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(line):
                errors.append(f"blocked secret pattern in staged diff: {pat.pattern[:28]}...")
    return errors


def check_python_ast() -> list[str]:
    errors: list[str] = []
    try:
        out = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        )
        changed = [
            ROOT / line[3:].strip()
            for line in out.splitlines()
            if line[3:].strip().endswith(".py")
        ]
    except Exception:
        changed = []

    targets = changed or list((ROOT / "backend_python" / "nebians").glob("*.py"))
    for path in targets:
        if not path.is_file():
            continue
        try:
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            rel = path.relative_to(ROOT)
            errors.append(f"syntax error in {rel}:{exc.lineno}: {exc.msg}")
    return errors


def check_security_invariants() -> list[str]:
    errors: list[str] = []
    mw = ROOT / "backend_python" / "nebians" / "middleware.py"
    if mw.is_file():
        text = mw.read_text(encoding="utf-8")
        if "Content-Security-Policy" not in text:
            errors.append("middleware.py missing Content-Security-Policy header")
        if "X-Content-Type-Options" not in text:
            errors.append("middleware.py missing X-Content-Type-Options header")

    sec = ROOT / "backend_python" / "api" / "security.py"
    if sec.is_file():
        text = sec.read_text(encoding="utf-8")
        if "_is_private_or_local_host" not in text:
            errors.append("api/security.py missing SSRF _is_private_or_local_host guard")

    auth = ROOT / "backend_python" / "web" / "views_auth.py"
    if auth.is_file():
        text = auth.read_text(encoding="utf-8")
        if "def _safe_next_url" not in text:
            errors.append("web/views_auth.py missing _safe_next_url open-redirect guard")

    net_cfg = ROOT / "app" / "src" / "main" / "res" / "xml" / "network_security_config.xml"
    if net_cfg.is_file():
        text = net_cfg.read_text(encoding="utf-8")
        if 'cleartextTrafficPermitted="false"' not in text:
            errors.append("network_security_config.xml missing base cleartextTrafficPermitted=false")

    proguard = ROOT / "app" / "proguard-rules.pro"
    if proguard.is_file():
        text = proguard.read_text(encoding="utf-8")
        if "-renamesourcefileattribute" not in text or "-overloadaggressively" not in text:
            errors.append("proguard-rules.pro missing irreversible R8 obfuscation directives")
    return errors


def main() -> int:
    errors = check_staged_secrets() + check_python_ast() + check_security_invariants()
    if errors:
        for err in errors:
            print(f"RSI AUDIT FAIL: {err}", file=sys.stderr)
        return 1
    print("rsi security + ast audit ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
