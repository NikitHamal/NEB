import json, sys
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))

def norm(v):
    """The two harnesses spell the default stroke cap differently ('butt' vs
    None). That is a harness detail, not a difference in the drawing."""
    if isinstance(v, list):
        return [norm(x) for x in v]
    if v == "butt":
        return None
    if isinstance(v, float):
        return round(v, 4)
    return v

a = {k: norm(v) for k, v in json.load(open(os.path.join(_HERE, "js.json"))).items()}
b = {k: norm(v) for k, v in json.load(open(os.path.join(_HERE, "py.json"))).items()}
ka, kb = set(a), set(b)
only_a, only_b = sorted(ka - kb), sorted(kb - ka)
both = sorted(ka & kb)
bad = [k for k in both if a[k] != b[k]]
print("streams: js=%d py=%d shared=%d" % (len(ka), len(kb), len(both)))
print("js-only: %s" % (only_a or "none"))
print("py-only: %s" % (only_b or "none"))
print("identical: %d / %d" % (len(both) - len(bad), len(both)))
for k in bad[:3]:
    print("\nDIFF", k)
    for i, (x, y) in enumerate(zip(a[k], b[k])):
        if x != y:
            print("  op %d\n   js %s\n   py %s" % (i, json.dumps(x)[:300], json.dumps(y)[:300]))
            break
sys.exit(1 if (bad or only_a or only_b) else 0)
