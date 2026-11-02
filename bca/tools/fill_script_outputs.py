#!/usr/bin/env python3
"""Run every ```python and ```php fence in the given markdown files and insert the real output (stdout then stderr)
as an ```output fence right after it (replacing an existing one). Each block must be self-contained.
A block whose first line is '# raises' (python) or '// raises' (php) may exit non-zero (it demonstrates an error).
Blocks whose first line is '# noexec' / '// noexec' / '-- noexec' are left alone. ```sql fences run through the MariaDB
(MySQL-compatible) client against a freshly created database `demo` (mysql -t: table output); '-- raises' allows an error.
    /tmp/v/bin/python bca/tools/fill_script_outputs.py unit-*.md        (python = the venv with numpy/pandas/matplotlib)
Exit status 1 if any block failed unexpectedly."""
import re, subprocess, sys, tempfile, os
PY = os.environ.get("NEB_PY", sys.executable)
pat = re.compile(r"(```(python|php|sql)\n(.*?)```\n)(?:[ \t]*\n)?(?:```output\n.*?```\n)?", re.S)
bad = 0
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    def repl(m):
        global bad
        lang, src = m.group(2), m.group(3)
        first = src.split("\n", 1)[0].strip()
        if first in ("# noexec", "// noexec", "-- noexec"): return m.group(1)
        d = tempfile.mkdtemp(); fn = {"python": "p.py", "php": "p.php", "sql": "p.sql"}[lang]
        open(os.path.join(d, fn), "w", encoding="utf-8").write(src)
        if lang == "sql":
            subprocess.run(["sudo", "mysql", "-e", "DROP DATABASE IF EXISTS demo; CREATE DATABASE demo"], check=True)
            cmd = ["sudo", "mysql", "-t", "-D", "demo", "-e", "source " + os.path.join(d, fn)]
        else: cmd = [PY, fn] if lang == "python" else ["php", "-d", "display_errors=1", "-d", "error_reporting=E_ALL", "-d", "html_errors=0", fn]
        env = dict(os.environ, PYTHONHASHSEED="0", MPLBACKEND="Agg", TZ="UTC")
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=d, env=env)
        expect_fail = first in ("# raises", "// raises", "-- raises")
        failed = r.returncode != 0 or (lang == "sql" and "ERROR" in r.stderr)   # the mysql client exits 0 after a sourced error
        if failed != expect_fail:
            bad += 1; print("UNEXPECTED STATUS", r.returncode, path, "\n", src[:200], "\n", r.stderr[-500:])
        out = (r.stdout + r.stderr).replace(d + "/", "").replace(d, "")
        out = out.rstrip("\n")
        if not out: return m.group(1)
        return m.group(1) + "```output\n" + out + "\n```\n"
    new = pat.sub(repl, text)
    if new != text: open(path, "w", encoding="utf-8").write(new)
sys.exit(1 if bad else 0)
