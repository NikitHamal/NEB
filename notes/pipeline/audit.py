#!/usr/bin/env python3
"""Parallel QA audit across all chapters: math fails, unpaired $, figure fails."""
import sys, os, re, json, glob, subprocess
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))

def one(path):
    r = subprocess.run([sys.executable, os.path.join(HERE, "check.py"), path],
                       capture_output=True, text=True, cwd=HERE)
    return path, r.returncode, r.stdout + r.stderr

if __name__ == "__main__":
    pats = sys.argv[1:] or [os.path.join(HERE, "..", "content", "*", "*.md")]
    files = sorted(f for p in pats for f in glob.glob(p))
    bad = 0
    with ProcessPoolExecutor(max_workers=12) as ex:
        for path, rc, out in ex.map(one, files):
            tail = [l for l in out.splitlines() if l.strip()][-1] if out.strip() else "?"
            if rc:
                bad += 1
                print(f"\n########## {path}")
                print(out.strip()[:3000])
            else:
                print(f"ok  {path}  | {tail.split(':',1)[-1].strip()}")
    print(f"\n==== {len(files)} files, {bad} FAILED")
