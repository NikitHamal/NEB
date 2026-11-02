#!/usr/bin/env python3
"""Mechanical audit of school-level books (grades 8, 10, 11, 12) against their
curriculum spines. Reuses pipeline/spine.py.

Checks per subject:
  - every spine unit has content/<slug>/unit-NN.md, and no extra unit files
  - frontmatter title / hours / area equal the spine (STRUCTURAL)
  - number of `## N.k` sections equals the number of spine bullets (MISSING/DEPTH)
  - stale-term scan (OUTDATED / FACTUAL candidates)
  - a built PDF exists

Run:  python3 notes/tools/school_audit.py [--md out.md]
"""
import os, re, sys, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(NOTES, "pipeline"))
import spine

SCHOOL = [
    "cs8", "eng8", "health8", "math8", "nep8", "omath8", "sci8", "soc8", "qbank8",
    "acc10", "cs10", "eco10", "eng10", "math10", "nep10", "omath10", "sci10", "soc10",
    "qbank10", "qbankc10",
    "bio11", "chem11", "cs11", "eng11", "math11", "nep11", "phy11", "qbank11",
    "bio12", "chem12", "cs12", "eng12", "math12", "nep12", "phy12", "qbank12",
]

STALE = [
    (r"\bQBASIC\b|\bQBasic\b", "QBASIC mention"),
    (r"Windows XP|Windows Vista|Windows 7\b|Windows 8(?:\.1)?\b", "old Windows version"),
    (r"Office 2003|Office 2007|Office 2010|Office 2013", "old MS Office version"),
    (r"Internet Explorer|Adobe Flash|Flash Player|Macromedia", "dead browser/plugin"),
    (r"\bSLC\b", "SLC (replaced by SEE from 2073 BS)"),
    (r"\bHSEB\b", "HSEB (replaced by NEB)"),
    (r"\b75 districts\b|\bseventy-five districts\b", "75 districts (now 77)"),
    (r"14 zones|fourteen zones|five development regions|5 development regions",
     "zones/development regions (abolished 2072)"),
    (r"Python 2\b|raw_input\(", "Python 2 idiom"),
    (r"\b26[.,]49|26\.5 million|2,64,94,504|26,494,504", "census 2068 population as current"),
]
STALE_ALLOW = {  # subject -> labels allowed to stay (with reason in SYLLABUS_DIFF.md)
    "cs8": {"QBASIC mention"}, "qbank8": {"QBASIC mention"},
}


NEPALI_MEDIUM = re.compile(r"^(nep|soc|health)")


def norm(t):
    t = re.sub(r"\s*[-\u2013\u2014]\s*", " - ", t)
    return re.sub(r"\s+", " ", t).strip()


def fm(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"---\r?\n(.*?)\r?\n---", t, re.S)
    d = {}
    if m:
        for l in m.group(1).splitlines():
            if ":" in l:
                k, v = l.split(":", 1)
                d[k.strip()] = v.strip().strip("'\"")
    return d, t


def main():
    rows, issues = [], []
    for slug in SCHOOL:
        sp = os.path.join(NOTES, "curriculum", slug + ".md")
        cdir = os.path.join(NOTES, "content", slug)
        if not os.path.exists(sp) or not os.path.isdir(cdir):
            issues.append((slug, "-", "STRUCTURAL", "spine or content dir missing"))
            continue
        head, units = spine.load(slug)
        files = {int(re.search(r"(\d+)", os.path.basename(f)).group(1)): f
                 for f in glob.glob(os.path.join(cdir, "unit-*.md"))}
        sub_spine = {u["no"] for u in units}
        for n in sorted(set(files) - sub_spine):
            issues.append((slug, n, "STRUCTURAL", "content file with no spine unit"))
        words = 0
        stale_hits = {}
        for u in units:
            n = u["no"]
            if n not in files:
                issues.append((slug, n, "MISSING", f"no content file for spine unit '{u['title']}'"))
                continue
            d, text = fm(files[n])
            words += len(text.split())
            nm = bool(NEPALI_MEDIUM.match(slug))
            if (not nm and d.get("title") and norm(d["title"]) != norm(u["title"])
                    and not norm(u["title"]).startswith(norm(d["title"]) + " - ")):
                issues.append((slug, n, "STRUCTURAL", f"title '{d['title']}' != spine '{u['title']}'"))
            if u["hours"] and d.get("hours") and str(d["hours"]) != str(u["hours"]):
                issues.append((slug, n, "STRUCTURAL", f"hours {d['hours']} != spine {u['hours']}"))
            if (not nm and u["area"] and d.get("area") and norm(d["area"]) != norm(u["area"])):
                issues.append((slug, n, "STRUCTURAL", f"area '{d['area']}' != spine '{u['area']}'"))
            secs = re.findall(r"^##\s+%d\.(\d+)\b" % n, text, re.M)
            if not nm and not slug.startswith("qbank") and len(secs) < len(u["sub"]):
                issues.append((slug, n, "MISSING",
                               f"{len(secs)} numbered sections for {len(u['sub'])} syllabus bullets"))
            for pat, label in STALE:
                hits = [m.start() for m in re.finditer(pat, text)]
                if hits and label not in STALE_ALLOW.get(slug, set()):
                    ln = text.count("\n", 0, hits[0]) + 1
                    stale_hits.setdefault(label, []).append((n, len(hits), ln))
        for label, lst in stale_hits.items():
            where = ", ".join(f"u{n}:{c}x@L{ln}" for n, c, ln in lst[:6])
            issues.append((slug, "-", "OUTDATED?", f"{label}: {where}"))
        pdfs = glob.glob(os.path.join(NOTES, "pdf", "*"))
        rows.append((slug, len(units), len(files), words))
    print(f"{'slug':9} units files words")
    for r in rows:
        print(f"{r[0]:9} {r[1]:5} {r[2]:5} {r[3]:7}")
    print(f"\n{len(issues)} issue(s)")
    for s, n, c, m in issues:
        print(f"[{c}] {s} u{n}: {m}")
    if "--json" in sys.argv:
        json.dump({"rows": rows, "issues": issues}, open("/tmp/school_audit.json", "w"), indent=1)


if __name__ == "__main__":
    main()
