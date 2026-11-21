#!/usr/bin/env python3
"""Static AST, secret-leak, security & M3X compliance guard for RSI pipeline v2."""
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


def check_admin_m3x_invariants() -> list[str]:
    errors: list[str] = []
    admin_css_dir = ROOT / "backend_python" / "web" / "static" / "web" / "css" / "admin"
    if admin_css_dir.is_dir():
        for path in admin_css_dir.glob("*.css"):
            txt = path.read_text(encoding="utf-8")
            for decl in re.findall(r"box-shadow\s*:\s*([^;}]+)", txt):
                val = decl.strip().replace("!important", "").strip()
                if val != "none":
                    errors.append(f"{path.name}: forbidden box-shadow: {decl.strip()}")
            for decl in re.findall(r"border-radius\s*:\s*([^;}]+)", txt):
                parts = decl.split("/")[0].split()
                if parts and all(p in ("0", "0px") for p in parts):
                    errors.append(f"{path.name}: forbidden square border-radius: {decl.strip()}")

    admin_tpl_dir = ROOT / "backend_python" / "web" / "templates" / "admin_panel"
    if admin_tpl_dir.is_dir():
        for path in admin_tpl_dir.rglob("*.html"):
            src = path.read_text(encoding="utf-8")
            if re.search(r"(?<![\w.])(confirm|alert)\(", src):
                errors.append(f"{path.name}: forbidden native confirm()/alert() dialog")
    return errors


def check_dialog_invariants() -> list[str]:
    """A native <dialog> pins to the top-left corner when the site reset zeroes its margin: keep `margin: auto`."""
    errors: list[str] = []
    css = ROOT / "backend_python" / "web" / "static" / "web" / "css"
    for rel in ("material3.css", "material3/01-tokens-typography.css"):
        path = css / rel
        if path.is_file() and not re.search(r"(?m)^dialog\s*\{\s*margin:\s*auto", path.read_text(encoding="utf-8")):
            errors.append(f"{rel}: lost `dialog {{ margin: auto }}` (every native dialog would stick to the top-left corner)")
    prof = ROOT / "backend_python" / "web" / "templates" / "web" / "profile.html"
    if prof.is_file() and re.search(r"sprite|\.webp|\.svg\"", prof.read_text(encoding="utf-8")):
        errors.append("profile.html: cover art is drawn by code (js/m3x-art.js), never a sprite, WebP or SVG file")
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
        if 'cleartextTrafficPermitted="false"' not in text or 'cleartextTrafficPermitted="true"' in text:
            errors.append("network_security_config.xml must strictly enforce cleartextTrafficPermitted=false")

    proguard = ROOT / "app" / "proguard-rules.pro"
    if proguard.is_file():
        text = proguard.read_text(encoding="utf-8")
        if "-renamesourcefileattribute" not in text or "-overloadaggressively" not in text or "-repackageclasses" not in text:
            errors.append("proguard-rules.pro missing irreversible R8 obfuscation / repackageclasses directives")
        if "-keep class com.neb.ians.data.api.**" in text:
            errors.append("proguard-rules.pro must not wildcard-keep com.neb.ians.data.api.** (de-obfuscates security interceptors)")

    manifest = ROOT / "app" / "src" / "main" / "AndroidManifest.xml"
    if manifest.is_file():
        mtext = manifest.read_text(encoding="utf-8")
        if 'android:fullBackupContent="@xml/backup_rules"' not in mtext or 'android:dataExtractionRules="@xml/data_extraction_rules"' not in mtext:
            errors.append("AndroidManifest.xml missing backup_rules / data_extraction_rules exclusions")

    jni_cpp = ROOT / "app" / "src" / "main" / "cpp" / "speech_jni.cpp"
    if jni_cpp.is_file():
        jtext = jni_cpp.read_text(encoding="utf-8")
        if "Java_com_neb_ians_" in jtext or "RegisterNatives" not in jtext:
            errors.append("speech_jni.cpp must use JNI_OnLoad RegisterNatives without exported Java_com_neb_ians_ symbols")
        if '"frida"' in jtext or '"apkkiller"' in jtext or '"signProof"' in jtext or '"envFlags"' in jtext:
            errors.append("speech_jni.cpp must not expose plaintext anti-tamper needles or JNI method names in .rodata")

    dsi = ROOT / "app" / "src" / "main" / "java" / "com" / "neb" / "ians" / "data" / "api" / "DeviceSignalInterceptor.kt"
    if dsi.is_file():
        dtext = dsi.read_text(encoding="utf-8")
        if "HmacSHA256" in dtext or '"X-Neb-Proof"' in dtext:
            errors.append("DeviceSignalInterceptor.kt must delegate HMAC signing to native C++ and obfuscate header strings")
    dep = ROOT / ".github" / "scripts" / "deploy_backend.py"
    if dep.is_file() and "deploy_changed.txt" not in dep.read_text(encoding="utf-8"):
        errors.append("deploy_backend.py must touch extracted files (unzip TZ skew makes collectstatic skip fresh static)")
    return errors


def check_undefined_names() -> list[str]:
    """NameError guard: every tracked backend .py file is scanned with pyflakes.

    Session 68: `Reply` was used in api/view_helpers.py without an import, every
    GET /api/posts/<id>/replies/ with at least one reply returned 500, and nothing
    flagged it because the scan only parsed syntax. Only *undefined name* findings
    fail the audit (unused imports and style are ignored)."""
    try:
        from pyflakes.api import check as _check  # noqa: F401
        from pyflakes import checker as _pf, messages as _pm
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--user",
                        "--break-system-packages", "pyflakes"], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            from pyflakes import checker as _pf, messages as _pm
        except ImportError:
            print("RSI AUDIT: pyflakes unavailable, undefined-name scan skipped", file=sys.stderr)
            return []
    try:
        files = subprocess.check_output(["git", "ls-files", "backend_python/*.py"], cwd=ROOT,
                                        text=True).split()
    except Exception:
        return []
    errors: list[str] = []
    for rel in files:
        if "/migrations/" in rel or "/scratch/" in rel:
            continue
        path = ROOT / rel
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        except (SyntaxError, OSError):
            continue
        for m in _pf.Checker(tree, rel).messages:
            if isinstance(m, _pm.UndefinedName):
                errors.append(f"undefined name {m.message_args[0]!r} at {rel}:{m.lineno}")
    return errors


def main() -> int:
    errors = (
        check_staged_secrets()
        + check_python_ast()
        + check_undefined_names()
        + check_admin_m3x_invariants()
        + check_dialog_invariants()
        + check_security_invariants()
    )
    if errors:
        for err in errors:
            print(f"RSI AUDIT FAIL: {err}", file=sys.stderr)
        return 1
    print("rsi v2 security + m3x + ast audit ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
