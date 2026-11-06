#!/usr/bin/env python3
"""Run each ```python block and write its stdout into the ```text block that follows (insert if missing)."""
import re, subprocess, sys, tempfile, os
pat = re.compile(r"(```python\n(.*?)```\n)(?:\s*```text\n.*?```\n)?", re.S)
for path in sys.argv[1:]:
    t = open(path, encoding="utf-8").read()
    def repl(m):
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh: fh.write(m.group(2))
        r = subprocess.run([sys.executable, fh.name], capture_output=True, text=True); os.unlink(fh.name)
        if r.returncode: sys.exit(f"{path}: python block failed\n{r.stderr}")
        return m.group(1) + "\n```text\n" + r.stdout.rstrip("\n") + "\n```\n"
    n = pat.sub(repl, t)
    if n != t: open(path, "w", encoding="utf-8").write(n)
print("text blocks filled")
