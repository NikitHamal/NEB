"""Parse curriculum spine files into structured data."""
import os, re
CUR = os.path.join(os.path.dirname(__file__), "..", "curriculum")

def load(slug):
    path = os.path.join(CUR, slug + ".md")
    head, units, area, part = {}, [], None, None
    notes = []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("# SUBJECT:"):
            for seg in line[2:].split("|"):
                if ":" in seg:
                    k, v = seg.split(":", 1)
                    head[k.strip().lower()] = v.strip()
        elif line.startswith("# AREA:"):
            m = re.match(r"# AREA:\s*(.+?)\s*(?:\((\d+)\))?$", line)
            area = m.group(1)
        elif line.startswith("# PART:"):
            part = line.split(":", 1)[1].strip()
            area = part
        elif line.startswith("## "):
            m = re.match(r"##\s*(\d+)\.\s*(.+?)\s*(?:\[([^\]]*)\])?\s*$", line)
            if not m:
                continue
            tag = (m.group(3) or "").strip()
            hrs = tag if tag.isdigit() else ""
            units.append({"no": int(m.group(1)), "title": m.group(2).strip(),
                          "hours": hrs, "tag": "" if hrs else tag,
                          "area": area or "", "sub": []})
        elif line.startswith("#"):
            notes.append(line.lstrip("# ").strip())
        elif line.startswith("- ") and units:
            units[-1]["sub"].append(line[2:].strip())
    head["notes"] = notes
    head["slug"] = slug
    return head, units

SUBJECTS = {
 "phy": ("Physics",            "#4A42D6"),
 "chem":("Chemistry",          "#A8271F"),
 "bio": ("Biology",            "#0B6A62"),
 "math":("Mathematics",        "#8F5507"),
 "cs":  ("Computer Science",   "#2E4057"),
 "eng": ("Compulsory English", "#6B3FA0"),
 "nep": ("अनिवार्य नेपाली",       "#A8551F"),
 "sci": ("Science and Technology", "#0B6A62"),
 "soc": ("सामाजिक अध्ययन तथा मानव मूल्य शिक्षा", "#2F6B3A"),
 "omath": ("Optional Mathematics", "#7A3E8E"),
 "acc": ("Accountancy", "#9D174D"),
 "eco": ("Economics", "#C2410C"),
 "health": ("स्वास्थ्य, शारीरिक तथा सिर्जनात्मक कला", "#0F766E"),
 "qbank": ("Question Bank",    "#B02A5B"),
 "qbankacc": ("Accountancy Question Bank", "#B02A5B"),
 "qbankeco": ("Economics Question Bank", "#B02A5B"),
 "qbankc": ("Commerce Question Bank", "#B02A5B"),
}
# Every subject-grade that actually has a spine file, so a bare
# `build_pdf.py` covers the whole library — grade 10 (the SEE series), the
# grade 11/12 science stream, the language papers and the question bank — and
# any spine added later (grade 8, for instance) joins the build by itself.
ALL = sorted(f[:-3] for f in os.listdir(CUR) if f.endswith(".md"))
# The basic level (grades 1-8) names two subjects differently from the
# secondary level: Nepali is not yet "compulsory", and science is "Science".
BASIC_NAMES = {"nep": "नेपाली"}

# Entrance-examination and bachelor-programme books are not graded by class:
# their slug is `<track>-<subject>` (cee-phy, ioe-math, csit-eng, cee-mock).
# `short` is what the site and the app print where a class number would go;
# `minutes` and `negative` (marks lost per wrong answer, as a fraction of the
# question's marks) drive the timed model-paper mode of the reader.
TRACKS = {
 "cee":  {"short": "CEE", "kind": "entrance", "order": 1,
          "label": "CEE · MECEE-BL Medical Entrance",
          "exam": "Medical Education Common Entrance Examination, Bachelor Level (MEC)",
          "minutes": 180, "negative": 0.25},
 "ioe":  {"short": "IOE", "kind": "entrance", "order": 2,
          "label": "IOE · BE/BArch Engineering Entrance",
          "exam": "Institute of Engineering (TU) BE/BArch entrance examination",
          "minutes": 120, "negative": 0.1},
 "csit": {"short": "CSIT", "kind": "entrance", "order": 3,
          "label": "CSIT · BSc CSIT Entrance",
          "exam": "BSc CSIT entrance examination (IOST, Tribhuvan University)",
          "minutes": 120, "negative": 0},
 "bca":  {"short": "BCA", "kind": "entrance", "order": 4,
          "label": "BCA · BCA Entrance",
          "exam": "BCA entrance examination (FOHSS, Tribhuvan University)",
          "minutes": 120, "negative": 0},
}
TRACK_SUBJECTS = {
 "phy":  ("Physics",                     "#4A42D6"),
 "chem": ("Chemistry",                   "#A8271F"),
 "zoo":  ("Zoology",                     "#0B6A62"),
 "bot":  ("Botany",                      "#2F7D32"),
 "mat":  ("Mental Agility Test",         "#7A3E8E"),
 "math": ("Mathematics",                 "#8F5507"),
 "eng":  ("English",                     "#6B3FA0"),
 "comp": ("Computer Knowledge",          "#2E4057"),
 "gk":   ("General Knowledge and IT",    "#C2410C"),
 "mock": ("Model Papers and Mock Tests", "#B02A5B"),
}


def track_of(slug):
    m = re.match(r"([a-z]+[0-9]*)-([a-z]+)$", slug or "")
    if m and m.group(1) in TRACKS and m.group(2) in TRACK_SUBJECTS:
        return m.group(1), m.group(2)
    return None, None


def meta_for(slug):
    track, subj = track_of(slug)
    if track:
        name, colour = TRACK_SUBJECTS[subj]
        return name, colour, TRACKS[track]["short"]
    k = re.match(r"([a-z]+)(\d+)", slug)
    name, colour = SUBJECTS[k.group(1)]
    grade = int(k.group(2))
    if grade <= 8:
        name = BASIC_NAMES.get(k.group(1), name)
    return name, colour, grade


def pdf_name(slug):
    name, _, grade = meta_for(slug)
    track, _ = track_of(slug)
    if track:
        return f"NEBians-{TRACKS[track]['short']}-Entrance-{name.replace(' ', '-')}.pdf"
    return f"NEBians-{name.replace(' ', '-')}-Grade-{grade}.pdf"
