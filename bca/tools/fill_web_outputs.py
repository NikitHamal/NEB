#!/usr/bin/env python3
"""Run ```js fences with node and ```jquery fences in jsdom (HTML fixture, a line '//---', then the script) and
insert the real console output as an ```output fence. Also checks every ```xml fence is well-formed (xmllint).
    NODE_PATH=/tmp/jsd/node_modules python3 bca/tools/fill_web_outputs.py bca/course/semester-3/web-technology-1/unit-*.md"""
import json, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
pat = re.compile(r"(```(js|jquery)\n(.*?)```\n)(?:\s*```output\n.*?```\n)?", re.S)
env = dict(os.environ, NODE_PATH=os.environ.get("NODE_PATH", "/tmp/jsd/node_modules"))
bad = 0
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    def repl(m):
        kind, src = m.group(2), m.group(3)
        if kind == "js":
            f = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False); f.write(src); f.close()
            r = subprocess.run(["node", f.name], capture_output=True, text=True, timeout=20, env=env); os.unlink(f.name)
        else:
            html, js = src.split("//---\n", 1)
            r = subprocess.run(["node", os.path.join(HERE, "jq_runner.js")], input=json.dumps({"html": html, "js": js}),
                               capture_output=True, text=True, timeout=20, env=env)
        out = (r.stdout + r.stderr).rstrip("\n")
        if r.returncode or "ERROR:" in out: print("PROBLEM", path, out[:300])
        return m.group(1) + (f"```output\n{out}\n```\n" if out else "")
    new = pat.sub(repl, text)
    for i, m in enumerate(re.finditer(r"```xml\n(.*?)```", new, re.S), 1):
        if "<!--SKIP-->" in m.group(1) or not m.group(1).lstrip().startswith(("<?xml", "<!DOCTYPE")): continue
        f = tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False); f.write(m.group(1)); f.close()
        r = subprocess.run(["xmllint", "--noout", "--valid", f.name] if "<!DOCTYPE" in m.group(1) and "[" in m.group(1) else ["xmllint", "--noout", f.name], capture_output=True, text=True)
        os.unlink(f.name)
        if r.returncode: bad += 1; print("XML PROBLEM", path, "block", i, r.stderr[:300])
    if new != text: open(path, "w", encoding="utf-8").write(new)
    print(path, "js/jquery blocks:", len(pat.findall(text)))
sys.exit(1 if bad else 0)
