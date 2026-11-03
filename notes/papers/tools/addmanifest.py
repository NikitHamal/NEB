"""Add/refresh ONE paper's record in manifest.json without rebuilding every PDF (build_paper --all is slow and rewrites all PDFs).
usage: python3 tools/addmanifest.py <id> [<id> ...]"""
import sys, os, json
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import build_paper as bp
mp = os.path.join(HERE, "manifest.json")
man = json.load(open(mp))
for pid in sys.argv[1:]:
    meta = bp.render(pid)
    man = [m for m in man if m.get("file") != meta.get("file")] + [meta]
man.sort(key=lambda m: m.get("file", ""))
json.dump(man, open(mp, "w"), indent=1)
print(len(man), "records")
