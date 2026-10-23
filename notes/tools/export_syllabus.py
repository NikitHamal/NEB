#!/usr/bin/env python3
"""Export the syllabus that the website and the app show, from the books.

The spines in `notes/curriculum/` are the official unit lists (title, working
hours, syllabus bullets, exam pattern); the chapters in `notes/content/` add
what each unit actually teaches (its sections, its summary points, its key
terms). This script joins the two for grades 8, 10, 11 and 12 and writes

    backend_python/web/data/syllabus/index.json
    backend_python/web/data/syllabus/<grade>-<subject>.json

Run it after a spine or a chapter changes:  python3 notes/tools/export_syllabus.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(NOTES, "pipeline"))
import spine  # noqa: E402

OUT = os.path.join(os.path.dirname(NOTES), "backend_python", "web", "data", "syllabus")

GRADES = {
    "8": {"label": "Class 8", "label_ne": "कक्षा ८", "exam": "Basic Level Examination (BLE)"},
    "10": {"label": "Class 10", "label_ne": "कक्षा १०", "exam": "Secondary Education Examination (SEE)"},
    "11": {"label": "Class 11", "label_ne": "कक्षा ११", "exam": "NEB Grade 11 examination"},
    "12": {"label": "Class 12", "label_ne": "कक्षा १२", "exam": "NEB Grade 12 examination"},
}

SUBJECTS = {
    "nep": ("nepali", "Nepali", "नेपाली", "translate", "compulsory"),
    "eng": ("english", "English", "अङ्ग्रेजी", "menu_book", "compulsory"),
    "math": ("mathematics", "Mathematics", "गणित", "calculate", "compulsory"),
    "sci": ("science", "Science and Technology", "विज्ञान तथा प्रविधि", "science", "compulsory"),
    "soc": ("social-studies", "Social Studies and Human Value Education", "सामाजिक अध्ययन तथा मानव मूल्य शिक्षा", "public", "compulsory"),
    "health": ("health-physical-creative-arts", "Health, Physical and Creative Arts", "स्वास्थ्य, शारीरिक तथा सिर्जनात्मक कला", "self_improvement", "compulsory"),
    "omath": ("optional-mathematics", "Optional Mathematics", "ऐच्छिक गणित", "functions", "optional"),
    "acc": ("accountancy", "Accountancy", "कार्यालय सञ्चालन तथा लेखा", "account_balance", "optional"),
    "eco": ("economics", "Economics", "अर्थशास्त्र", "trending_up", "optional"),
    "phy": ("physics", "Physics", "भौतिक विज्ञान", "bolt", "science"),
    "chem": ("chemistry", "Chemistry", "रसायन विज्ञान", "experiment", "science"),
    "bio": ("biology", "Biology", "जीवविज्ञान", "biotech", "science"),
    "cs": ("computer-science", "Computer Science", "कम्प्युटर विज्ञान", "terminal", "science"),
}

ORDER = ["nep", "eng", "math", "sci", "soc", "health", "omath", "acc", "eco", "phy", "chem", "bio", "cs"]

SUMMARY_HEADS = ("Chapter summary", "पाठको सार", "एकाइको सार", "अध्यायको सारांश", "अध्यायको सार", "सारांश")
DEVA_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
NE_DIGITS = str.maketrans("0123456789", "०१२३४५६७८९")


LATEX = {"Delta": "Δ", "delta": "δ", "times": "×", "div": "÷", "alpha": "α", "beta": "β",
         "gamma": "γ", "theta": "θ", "lambda": "λ", "mu": "μ", "pi": "π", "omega": "ω",
         "Omega": "Ω", "sigma": "σ", "rho": "ρ", "phi": "φ", "epsilon": "ε", "eta": "η",
         "nu": "ν", "tau": "τ", "infty": "∞", "le": "≤", "ge": "≥", "leq": "≤", "geq": "≥",
         "neq": "≠", "ne": "≠", "approx": "≈", "propto": "∝", "rightarrow": "→", "to": "→",
         "leftarrow": "←", "Rightarrow": "⇒", "rightleftharpoons": "⇌", "pm": "±", "cdot": "·",
         "circ": "°", "degree": "°", "sqrt": "√", "angle": "∠", "triangle": "△", "parallel": "∥",
         "perp": "⊥", "in": "∈", "cup": "∪", "cap": "∩", "subset": "⊂", "sum": "Σ", "int": "∫"}


def latex(expr):
    expr = re.sub(r"\\(?:text|mathrm|mathbf|operatorname|vec|overline|hat|bar)\s*\{([^{}]*)\}", r"\1", expr)
    expr = re.sub(r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"(\1)/(\2)", expr)
    expr = re.sub(r"\\([A-Za-z]+)", lambda m: LATEX.get(m.group(1), m.group(1)), expr)
    expr = re.sub(r"\^\{([^{}]*)\}", r"^\1", expr)
    expr = re.sub(r"_\{([^{}]*)\}", r"\1", expr)
    expr = re.sub(r"_(\w)", r"\1", expr)
    return expr.replace("{", "").replace("}", "").replace("\\,", " ").replace("\\", "")


def clean(text):
    text = re.sub(r"\$([^$]*)\$", lambda m: latex(m.group(1)), text)
    text = re.sub(r"\*\*|__|`", "", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)([^*]+)\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*\[[\d०-९]+\]$", "", text)
    return text.strip(" -–—:;")


def split_slug(slug):
    m = re.match(r"([a-z]+?)(\d+)$", slug)
    return (m.group(1), m.group(2)) if m else (None, None)


def read_unit(slug, no):
    path = os.path.join(NOTES, "content", slug, "unit-%02d.md" % no)
    if not os.path.exists(path):
        return None
    lines = open(path, encoding="utf-8").read().split("\n")
    sections, summary, terms = [], [], []
    words = figures = examples = 0
    in_fence = False
    current = None
    for line in lines:
        if line.startswith("```"):
            if not in_fence and line.startswith("```figure"):
                figures += 1
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        words += len(line.split())
        if line.startswith("## "):
            head = line[3:].strip()
            current = head
            m = re.match(r"^([\d०-९]+[.][\d०-९]+)\s+(.+)$", head)
            if m:
                sections.append({"no": m.group(1).translate(DEVA_DIGITS), "title": clean(m.group(2))})
            continue
        if line.startswith("::: definition"):
            term = clean(line[len("::: definition"):])
            if term and term not in terms:
                terms.append(term)
        if line.startswith("::: example"):
            examples += 1
        if current and current.startswith(SUMMARY_HEADS):
            if re.match(r"^\s*[-*]\s+", line):
                summary.append(re.sub(r"^\s*[-*]\s+", "", line))
            elif line.strip() and summary and not line.startswith((":::", "|", "#")):
                summary[-1] += " " + line.strip()
    summary = [clean(p)[:340] for p in summary[:8] if clean(p)]
    return {"sections": sections, "summary": summary, "terms": terms[:10],
            "words": words, "figures": figures, "examples": examples}


def topics_for(unit, body):
    topics = [clean(t) for t in unit["sub"] if clean(t)]
    sections = [s["title"] for s in body.get("sections", [])]
    return topics if len(topics) >= 2 or not sections else sections


def parse_exam(notes):
    for note in notes:
        if note.startswith(("EXAM", "PATTERN", "GRID")):
            return re.sub(r"^(EXAM|PATTERN|GRID):\s*", "", note)
    return ""


def total_hours(head, units):
    for key in ("working_hours", "theory_hours", "hours"):
        value = (head.get(key) or "").translate(DEVA_DIGITS)
        if value.isdigit() and int(value) > 0:
            return int(value)
    hours = [int(u["hours"]) for u in units if str(u["hours"]).isdigit()]
    return sum(hours) or None


def export(slug):
    prefix, grade = split_slug(slug)
    if prefix not in SUBJECTS or grade not in GRADES:
        return None
    key, name, name_ne, icon, group = SUBJECTS[prefix]
    if prefix == "cs" and int(grade) <= 10:
        group = "optional"
    head, units = spine.load(slug)
    nepali = prefix in ("nep", "soc", "health")
    out_units = []
    for u in units:
        body = read_unit(slug, u["no"]) or {}
        out_units.append({
            "no": u["no"],
            "title": clean(u["title"]),
            "hours": int(u["hours"]) if str(u["hours"]).isdigit() and int(u["hours"]) > 0 else None,
            "area": clean(u.get("area") or ""),
            "topics": topics_for(u, body),
            "sections": body.get("sections", []),
            "summary": body.get("summary", []),
            "terms": body.get("terms", []),
            "stats": {k: body.get(k, 0) for k in ("words", "figures", "examples")},
            "has_notes": bool(body),
        })
    areas = []
    for u in out_units:
        if u["area"] and u["area"] not in areas:
            areas.append(u["area"])
    hours = total_hours(head, units)
    data = {
        "grade": grade,
        "grade_label": GRADES[grade]["label"],
        "grade_label_ne": GRADES[grade]["label_ne"],
        "subject": key,
        "name": name,
        "name_ne": name_ne,
        "icon": icon,
        "group": group,
        "color": spine.SUBJECTS.get(prefix, ("", "#4A42D6"))[1],
        "lang": "ne" if nepali else "en",
        "code": head.get("code", ""),
        "hours": hours,
        "exam": parse_exam(head.get("notes", [])),
        "areas": areas,
        "units": out_units,
        "unit_count": len(out_units),
        "topic_count": sum(len(u["topics"]) for u in out_units),
        "notes_ready": sum(1 for u in out_units if u["has_notes"]),
    }
    return data


def main():
    os.makedirs(OUT, exist_ok=True)
    grades = {g: [] for g in GRADES}
    for slug in spine.ALL:
        data = export(slug)
        if not data:
            continue
        name = "%s-%s.json" % (data["grade"], data["subject"])
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
        prefix = split_slug(slug)[0]
        grades[data["grade"]].append((ORDER.index(prefix), {
            k: data[k] for k in ("subject", "name", "name_ne", "icon", "group", "color",
                                 "lang", "hours", "unit_count", "topic_count", "notes_ready")}))
        print("%-8s -> %-34s units=%-3d topics=%d" % (slug, name, data["unit_count"], data["topic_count"]))
    index = {"grades": [dict(GRADES[g], grade=g, subjects=[s for _, s in sorted(grades[g], key=lambda t: t[0])])
                        for g in GRADES]}
    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
