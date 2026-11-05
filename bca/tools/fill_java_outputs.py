#!/usr/bin/env python3
"""Compile and run every ```java fence in the given markdown files; insert the real stdout+stderr as an ```output fence
right after it (replacing an old one). Each fence must be one self-contained file (class name taken from the first
'public class' or 'class'). First-line markers: '// compile-only' (compile, do not run: GUI/servlet code), '// noexec' (skip).
Classpath: SQLite JDBC, H2, servlet-api 4.0 and slf4j from /usr/share/java; run with -Djava.awt.headless=true.
    python3 bca/tools/fill_java_outputs.py bca/course/semester-5/advanced-java/unit-*.md        exit 1 on any failure"""
import os, re, subprocess, sys, tempfile
J = "/usr/share/java/"
CP = ":".join(J + x for x in ("sqlite-jdbc.jar", "slf4j-api.jar", "servlet-api.jar", "h2.jar"))
pat = re.compile(r"(```java\n(.*?)```\n)(?:[ \t]*\n)?(?:```output\n.*?```\n)?", re.S)
bad = 0; ran = 0; compiled = 0
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    def repl(m):
        global bad, ran, compiled
        src = m.group(2); first = src.split("\n", 1)[0].strip()
        if first == "// noexec": return m.group(1)
        cm = re.search(r"public\s+(?:final\s+)?(?:class|interface|enum|record)\s+(\w+)", src) or re.search(r"\b(?:class|interface)\s+(\w+)", src)
        name = cm.group(1); d = tempfile.mkdtemp(); open(os.path.join(d, name + ".java"), "w", encoding="utf-8").write(src)
        c = subprocess.run(["javac", "-Xlint:none", "-cp", CP, name + ".java"], cwd=d, capture_output=True, text=True)
        label = f"{os.path.basename(path)}:{name}"
        if c.returncode: bad += 1; print("COMPILE FAIL", label, "\n", c.stderr[:800]); return m.group(1)
        compiled += 1
        if first == "// compile-only": print("ok (compiled only)", label); return m.group(1)
        r = subprocess.run(["java", "-Djava.awt.headless=true", "-cp", CP + ":.", name], cwd=d, capture_output=True, text=True, timeout=90)
        ran += 1; out = (r.stdout + r.stderr).replace(d + "/", "").rstrip("\n")
        if r.returncode: bad += 1; print("RUN FAIL", label, r.returncode, "\n", out[:800])
        else: print("ok", label)
        return m.group(1) + ("```output\n" + out + "\n```\n" if out else "")
    new = pat.sub(repl, text)
    if new != text: open(path, "w", encoding="utf-8").write(new)
print(f"{compiled} compiled, {ran} executed, {bad} failures"); sys.exit(1 if bad else 0)
