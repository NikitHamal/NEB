"""Register one freshly built paper in manifest.json and refresh only its subject's bundle.

    python3 tools/add_paper.py 12-chem-2082-9111

Running bundle_papers.py rewrites every bundle (non-deterministic bytes); this restores the unrelated ones.
"""
import os, sys, json, subprocess
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, HERE)
import build_paper

pid = sys.argv[1]
meta = build_paper.render(pid)
mp = os.path.join(HERE, "manifest.json")
m = json.load(open(mp, encoding="utf-8"))
m = [r for r in m if r["id"] != pid] + [meta]
m.sort(key=lambda r: (r["subject"], -int(r["year_bs"]), r["stream"]))
json.dump(m, open(mp, "w", encoding="utf-8"), indent=1)
bp = os.path.join(HERE, "bundles.json")
old = json.load(open(bp, encoding="utf-8"))
subprocess.run([sys.executable, os.path.join(HERE, "bundle_papers.py")], cwd=HERE, check=True)
new = json.load(open(bp, encoding="utf-8"))
keep = {b["subject"]: b for b in old}
key = meta["subject"]
for b in new:
    if b["subject"] == key:
        keep[key] = b
json.dump(sorted(keep.values(), key=lambda b: b["subject"]), open(bp, "w", encoding="utf-8"), indent=1)
repo = os.path.abspath(os.path.join(HERE, "..", ".."))
for b in new:
    if b["subject"] != key:
        subprocess.run(["git", "checkout", "--", os.path.join("notes/papers/pdf", b["file"])], cwd=repo)
