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
}
ALL = [f"{k}{g}" for k in SUBJECTS for g in (11, 12)]
def meta_for(slug):
    k = re.match(r"([a-z]+)(\d+)", slug)
    return SUBJECTS[k.group(1)][0], SUBJECTS[k.group(1)][1], int(k.group(2))
