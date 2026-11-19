"""Join parts of a long paper: content/_parts/<id>.<n>.md -> content/<id>.md (keeps each file small to edit).
usage: python3 tools/assemble.py <id> [<id> ...]"""
import sys, os, glob
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for pid in sys.argv[1:]:
    parts = sorted(glob.glob(os.path.join(HERE, "content", "_parts", pid + ".*.md")), key=lambda f: int(f.rsplit(".", 2)[1]))
    assert parts, "no parts for " + pid
    text = "".join(open(f, encoding="utf-8").read().rstrip("\n") + "\n\n" for f in parts)
    open(os.path.join(HERE, "content", pid + ".md"), "w", encoding="utf-8", newline="\n").write(text.rstrip("\n") + "\n")
    print(pid, len(parts), "parts,", text.count("\n"), "lines")
