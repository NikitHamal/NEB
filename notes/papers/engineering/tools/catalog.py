"""Build the engineering paper catalog from manifests + the git tree (no PDFs need to be checked out).

    python3 notes/papers/engineering/tools/catalog.py     # -> engineering/catalog.json, CATALOG.md

Only files that exist on disk (in the branch tree) are listed; rows whose original was deduped are skipped.
"""
import os, re, json, glob, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(ENG, "..", "..", ".."))
SRC = "notes/papers/engineering/sources/"

ORD = {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8"}
UNI = {"tu-ioe": "Tribhuvan University (IOE)", "pokhara-university": "Pokhara University",
       "purbanchal-university": "Purbanchal University", "kathmandu-university": "Kathmandu University",
       "ioe-entrance": "IOE Entrance", "ndds-ioe-entrance": "IOE Entrance", "nec-licence": "Nepal Engineering Council",
       "ctevt": "CTEVT", "promod-blog": "Purbanchal University", "github": None}


def tree():
    out = subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "--", SRC[:-1]], cwd=ROOT,
                         capture_output=True, text=True).stdout.split("\n")
    return {p[len(SRC):] for p in out if p.startswith(SRC)}


def semnum(s):
    m = re.search(r"(\d)\s*(?:st|nd|rd|th)?[\s-]*sem", s, re.I) or re.search(r"(?:sem(?:ester)?)[\s-]*(\d)", s, re.I)
    return m.group(1) if m else ""


def year_season(s):
    y = re.search(r"(20[01]\d|2020|2021|2022|2023|2024|2025)", s)
    se = re.search(r"(fall|spring|autumn)", s, re.I)
    yy = y.group(1) if y else ""
    if not yy:
        m = re.search(r"\b(1\d|2[0-5])\s*(?:fall|spring)", s, re.I) or re.search(r"[_\s-](2[0-5])\b", s)
        yy = "20" + m.group(1) if m else ""
    return yy, (se.group(1).title() if se else "")


def clean(n):
    n = os.path.splitext(os.path.basename(n))[0]
    n = re.sub(r"__[\w-]{0,8}$", "", n)
    return re.sub(r"\s+", " ", re.sub(r"[_]+", " ", n)).strip(" -")


PAPER_EXT = {"pdf", "doc", "docx", "rtf", "dot", "jpg", "jpeg", "png"}
REPO_UNI = [("waraunika|ProJ-Yeet|itsbhupesh00|iamshishirgaire|tech-noob|xpsaroj", "Tribhuvan University (IOE)"),
            ("pujandhakal|pramesh61|Just-Binod|harmless-beep|pranit-mishra|adhikari-arpan|ujjwalnp", "Pokhara University"),
            ("Prashznt|studywithnpandey", "Purbanchal University"), ("SamirWagle|Abhishek|Sandesh", "Nepal Engineering Council")]


def classify(dest, meta, row):
    g = dest.split("/")[0]
    if g == "github":
        for pat, u in REPO_UNI:
            if re.search(pat, dest.split("/")[1]):
                meta = dict(meta, university=u)
    rec = dict(path=dest, university=UNI.get(g) or meta.get("university") or "Other", program="", semester="",
               subject="", year="", season="", course="", kind="Past question", ext=os.path.splitext(dest)[1].lower().lstrip("."),
               pages=row.get("pages"), source=meta.get("aggregator") or meta.get("repo") or g)
    base = os.path.basename(dest)
    if "past-questions-bani" in dest:
        m = re.match(r"^(\w+) Semester . (.*) \((.*?) Course\)", meta.get("label", ""))
        rec.update(semester=semnum(meta.get("label", "")), subject=m.group(2) if m else clean(base), course=m.group(3) if m else "")
        pm = re.search(r"for ([A-Za-z, ]+?) .{1,3} IOE", meta.get("description", ""))
        rec["program"] = pm.group(1).replace(" ", "") if pm else "BE"
    elif "tu-ioe/past-questions/" in dest:
        rec.update(program=meta.get("program", "").upper(), semester=meta.get("semester", ""),
                   subject=meta.get("subject", "").replace("-", " ").title())
    elif "past-questions-subesh" in dest:
        n = clean(base).split("_")[0]
        m = re.match(r"^(.*?)-(\d)(?:st|nd|rd|th)-sem", n)
        el = re.match(r"^(.*?)-elective-(i+)", n)
        rec["semester"] = m.group(2) if m else ("Elective " + el.group(2).upper() if el else "")
        rec["subject"] = (m.group(1) if m else el.group(1) if el else n).replace("-", " ")
        rec["program"] = "BE (IOE)"
    elif "ioeqnbank" in dest or "ndds" in dest:
        rec.update(subject=(row.get("title") or "")[:80] or clean(base), program="BE (IOE)")
        if "ndds" in dest or "entrance" in dest:
            rec.update(kind="Entrance model", year="2080", program="IOE Entrance")
    elif "curriculum" in dest:
        rec.update(kind="Syllabus", subject=clean(base), program="IOE")
    elif g == "pokhara-university" or "PU-BE-Old" in dest:
        yr, se = year_season(dest if "ujjwalnp" not in dest else base)
        if "PU-BE-Old" in dest:
            k = re.search(r"(Final|UT|Assessment)", dest.split("/")[2], re.I)
            rec["kind"] = {"ut": "Unit test", "final": "Final", "assessment": "Assessment"}.get((k.group(1) if k else "").lower(), "Past question")
            rec["semester"] = semnum(dest.split("/")[-2])
            sub = re.sub(r"[-_ ]*(final|ut|assessment|20\d\d|fall|spring|doc|docx|unit test)\b.*$", "", clean(base), flags=re.I)
        else:
            sub = clean(base)
            m = re.search(r"be-(computer|software)-new-(\d)", dest)
            if m:
                rec.update(program="BE " + m.group(1).title(), semester=m.group(2), course="New (2018+)")
                yr, se = year_season(base)
        rec.update(subject=sub.strip(" -.") or clean(base), year=yr, season=se, program=rec["program"] or "BE (all)")
    else:
        rec.update(subject=clean(base), program=meta.get("program", ""))
        rec["year"], rec["season"] = year_season(base)
    rec["subject"] = re.sub(r"\s+", " ", rec["subject"]).strip().title() if rec["subject"].islower() else rec["subject"]
    return rec


def main():
    have = tree()
    recs, seen = [], set()
    for mf in sorted(glob.glob(os.path.join(ENG, "manifests", "*.jsonl"))):
        for ln in open(mf, encoding="utf-8"):
            try:
                row = json.loads(ln)
            except ValueError:
                continue
            d = row.get("dest")
            if row.get("status") not in ("ok", "exists") or d not in have or d in seen:
                continue
            if os.path.splitext(d)[1].lower().lstrip(".") not in PAPER_EXT:
                continue
            seen.add(d)
            recs.append(classify(d, row.get("meta") or {}, row))
    for i, r in enumerate(sorted(recs, key=lambda r: (r["university"], r["program"], r["semester"], r["subject"], r["year"])), 1):
        r["id"] = i
    recs.sort(key=lambda r: r["id"])
    json.dump(recs, open(os.path.join(ENG, "catalog.json"), "w"), ensure_ascii=False, indent=0)
    print(len(recs), "records")
    c = collections.Counter((r["university"], r["ext"]) for r in recs)
    for k, v in sorted(c.items()):
        print(k, v)


if __name__ == "__main__":
    main()
