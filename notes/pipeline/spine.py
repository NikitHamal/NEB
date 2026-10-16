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
def meta_for(slug):
    k = re.match(r"([a-z]+)(\d+)", slug)
    return SUBJECTS[k.group(1)][0], SUBJECTS[k.group(1)][1], int(k.group(2))
