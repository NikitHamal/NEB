#!/usr/bin/env python3
"""Compile and run every ```csharp fence in the given markdown files with Mono (mcs + mono); insert the real
stdout+stderr as an ```output fence right after it (replacing an old one). Each fence is one self-contained file.
First-line markers: '// compile-only' (compile, do not run: GUI, ASP.NET, input), '// noexec' (skip: modern C# 9+
syntax or snippets that need packages Mono does not have). Optional '// stdin: text' lines feed standard input.
Mono's mcs speaks C# 7; the book flags newer syntax with '// noexec'.
    python3 bca/tools/fill_cs_outputs.py bca/course/semester-7/dotnet-technology/unit-*.md     exit 1 on any failure"""
import os, re, subprocess, sys, tempfile
REFS = ["-r:System.Data.dll", "-r:Mono.Data.Sqlite.dll", "-r:System.Core.dll", "-r:System.Numerics.dll",
        "-r:System.Xml.dll", "-r:System.Xml.Linq.dll", "-r:System.Net.Http.dll", "-r:System.Windows.Forms.dll", "-r:System.Drawing.dll"]
pat = re.compile(r"(```csharp\n(.*?)```\n)(?:[ \t]*\n)?(?:```output\n.*?```\n)?(?:[ \t]*\n)*", re.S)
bad = ran = compiled = 0
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    def repl(m):
        global bad, ran, compiled
        src = m.group(2); first = src.split("\n", 1)[0].strip()
        label = f"{os.path.basename(path)}:{src.strip().splitlines()[0][:40]}"
        if first == "// noexec": return m.group(0)
        d = tempfile.mkdtemp(); open(os.path.join(d, "P.cs"), "w", encoding="utf-8").write(src)
        c = subprocess.run(["mcs", "-nowarn:0168,0219,0414,0649,0169,0067,0108", "-out:P.exe"] + REFS + ["P.cs"], cwd=d, capture_output=True, text=True)
        if c.returncode: bad += 1; print("COMPILE FAIL", label, "\n", (c.stdout + c.stderr)[:900]); return m.group(0)
        compiled += 1
        if first == "// compile-only": print("ok (compiled only)", label); return m.group(0)
        sm = re.search(r"^// stdin: (.*)$", src, re.M); stdin = (sm.group(1).replace("\\n", "\n") + "\n") if sm else ""
        r = subprocess.run(["mono", "P.exe"], cwd=d, input=stdin, capture_output=True, text=True, timeout=60)
        ran += 1; out = (r.stdout + r.stderr).replace(d + "/", "").rstrip("\n")
        if r.returncode: bad += 1; print("RUN FAIL", label, r.returncode, "\n", out[:900])
        else: print("ok", label)
        return m.group(1) + ("```output\n" + out + "\n```\n" if out else "") + "\n"
    new = pat.sub(repl, text)
    if new != text: open(path, "w", encoding="utf-8").write(new)
print(f"{compiled} compiled, {ran} executed, {bad} failures"); sys.exit(1 if bad else 0)
