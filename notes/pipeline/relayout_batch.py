#!/usr/bin/env python3
"""Rebuild books with the page-economy layout (split tables, floated figures), keep copies in
sync, audit holes before/after, commit and push every N books.

    /tmp/v/bin/python notes/pipeline/relayout_batch.py [--every 3] school:math10 bca:semester-4/numerical-methods ...
    targets: school:<slug>  (notes/pdf; ioe-* also copied to ioe/pdfs, bca-* to bca/entrance + viewer)
             bca:<semester-N/dir>   (bca/course, built by bca/tools/nebpdf.py)
Appends one line per book to /tmp/relayout_results.tsv. Never rebuilds a book whose slug is in
notes/pipeline/relayout_done.txt (written after a successful push).
"""
import glob, os, shutil, subprocess, sys, time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PY = "/tmp/v/bin/python"
ENV = dict(os.environ, GIT_ASKPASS="/tmp/gitenv.sh", GIT_TERMINAL_PROMPT="0")
DONE = os.path.join(REPO, "notes", "pipeline", "relayout_done.txt")
sys.path.insert(0, os.path.join(REPO, "notes", "pipeline"))


def run(cmd, cwd=REPO, check=True):
    return subprocess.run(cmd, cwd=cwd, env=ENV, shell=isinstance(cmd, str), capture_output=True, text=True)


def audit(path):
    if not os.path.exists(path):
        return (0, 0, 0.0)
    import warnings; warnings.filterwarnings("ignore")
    import gapaudit
    n, out, w = gapaudit.audit(path, 25)
    return (n, len(out), w)


def pdf_for(t):
    kind, name = t.split(":", 1)
    if kind == "school":
        import spine
        return os.path.join(REPO, "notes", "pdf", spine.pdf_name(name))
    sem = name.split("/")[0]
    return sorted(glob.glob(os.path.join(REPO, "bca", "course", sem, "pdfs", "*.pdf")), key=os.path.getmtime)[-1]


def build(t):
    kind, name = t.split(":", 1)
    if kind == "school":
        r = run([PY, "build_pdf.py", name], cwd=os.path.join(REPO, "notes", "pipeline"))
        import spine
        pdf = os.path.join(REPO, "notes", "pdf", spine.pdf_name(name))
        copies = []
        if name.startswith("ioe-"):
            copies = [os.path.join(REPO, "ioe", "pdfs", os.path.basename(pdf))]
        if name.startswith("bca-"):
            copies = [os.path.join(REPO, "bca", "entrance", "pdfs", os.path.basename(pdf)),
                      os.path.join(REPO, "notes", "bca-viewer", "public", "bca", "pdf", os.path.basename(pdf))]
        return r, pdf, copies
    before = {p: os.path.getmtime(p) for p in glob.glob(os.path.join(REPO, "bca", "course", "*", "pdfs", "*.pdf"))}
    r = run([PY, "bca/tools/nebpdf.py", "course/" + name])
    new = [p for p in before if os.path.getmtime(p) > before[p]]
    return r, (new[0] if new else None), []


def push(msg):
    run("git add -A")
    run(["git", "commit", "-qm", msg])
    for _ in range(2):
        r = run("git push origin HEAD:main")
        if r.returncode == 0:
            return True
        run("git pull --rebase --autostash -q origin main")
    return False


def main():
    a = sys.argv[1:]
    every = 3
    if "--every" in a:
        k = a.index("--every"); every = int(a[k + 1]); del a[k:k + 2]
    done = set(open(DONE).read().split()) if os.path.exists(DONE) else set()
    pending = []
    for t in a:
        if t in done:
            continue
        old = pdf_for(t) if t.startswith("school") or True else None
        b0 = audit(old)
        t0 = time.time()
        r, pdf, copies = build(t)
        if not pdf or not os.path.exists(pdf) or time.time() - os.path.getmtime(pdf) > 3600 * 3:
            line = f"{t}\tFAILED\t{r.stdout[-300:]!r}{r.stderr[-300:]!r}"
        else:
            b1 = audit(pdf)
            for c in copies:
                os.makedirs(os.path.dirname(c), exist_ok=True); shutil.copy(pdf, c)
            line = f"{t}\tpages {b0[0]}->{b1[0]}\tholes {b0[1]}->{b1[1]}\twasted_pg {b0[2]:.1f}->{b1[2]:.1f}\t{time.time() - t0:.0f}s"
            pending.append(t)
        open("/tmp/relayout_results.tsv", "a").write(line + "\n")
        if len(pending) >= every:
            if push(f"Rebuild PDFs with page-economy layout: {', '.join(pending)}"):
                open(DONE, "a").write("\n".join(pending) + "\n")
                pending = []
    if pending and push(f"Rebuild PDFs with page-economy layout: {', '.join(pending)}"):
        open(DONE, "a").write("\n".join(pending) + "\n")
    open("/tmp/relayout_results.tsv", "a").write("ALLDONE\n")


if __name__ == "__main__":
    main()
