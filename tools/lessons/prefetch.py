"""Synthesise every narration line of a lesson script before rendering, in parallel."""
import ast
import sys
from concurrent.futures import ThreadPoolExecutor

from kit.voice import speak

ARGS = {"say": [0], "tip": [1], "quiz": [3, 4], "recap": [1], "outro": [0], "roadmap": [0], "section": [1]}
KW = {"narration", "intro", "reveal", "text"}


def texts(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    lang = "en"
    voice = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            n = node.targets[0].id
            if n in ("LANG", "VOICE") and isinstance(node.value, ast.Constant):
                if n == "LANG":
                    lang = node.value.value
                else:
                    voice = node.value.value
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in ARGS:
            for i in ARGS[node.func.attr]:
                if i < len(node.args) and isinstance(node.args[i], ast.Constant) and isinstance(node.args[i].value, str):
                    out.append(node.args[i].value)
            for k in node.keywords:
                if k.arg in KW and isinstance(k.value, ast.Constant) and isinstance(k.value.value, str):
                    out.append(k.value.value)
    v = voice or ("ne" if lang == "ne" else "en")
    return [t for t in dict.fromkeys(out) if t.strip()], v


def prefetch(path, workers=4):
    ts, v = texts(path)
    with ThreadPoolExecutor(workers) as ex:
        durs = list(ex.map(lambda t: speak(t, v)[1], ts))
    return len(ts), sum(durs)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        n, d = prefetch(p)
        print(f"{p}: {n} lines, {d / 60:.1f} min of narration")
