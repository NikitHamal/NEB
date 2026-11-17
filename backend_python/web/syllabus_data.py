"""Read the syllabus exported from the NEBians books.

`notes/tools/export_syllabus.py` writes one JSON file per grade and subject
into `web/data/syllabus/`; the website and the app both read them through
this module, so the two always show the same syllabus.

index.json lists the school grades (8, 10, 11, 12; "kind": "school") and then
the entrance-examination tracks that have chapters written ("cee", later
"ioe", "csit", "bca"; "kind": "entrance"). A track is addressed exactly like a
grade (/app/syllabus/cee/physics/), and "short" is what a page prints where a
class number would go ("Class 11", "CEE").
"""
import json
import os
from functools import lru_cache

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "syllabus")
SCHOOL_GRADES = ("8", "10", "11", "12")
GRADES = SCHOOL_GRADES   # the school grades; grade_keys() adds the tracks present in index.json
LIBRARY_GRADE = {"8": "Class 8", "10": "Class 10 / SEE", "11": "Class 11", "12": "Class 12"}
TRACK_LIBRARY_GRADE = "Entrance Prep"
COURSE_LIBRARY_GRADE = "Bachelor"       # the BCA course books (kind "course") sit under Bachelor


def _defaults(entry):
    grade = str(entry.get("grade", ""))
    school = grade in SCHOOL_GRADES
    entry.setdefault("kind", "school" if school else "entrance")
    entry.setdefault("short", ("Class %s" % grade) if school else grade.upper())
    return entry


@lru_cache(maxsize=1)
def index():
    path = os.path.join(DATA_DIR, "index.json")
    if not os.path.exists(path):
        return {"grades": []}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    for entry in data.get("grades", []):
        _defaults(entry)
    return data


def grade_keys():
    """The school grades and every track key present in index.json."""
    keys = list(SCHOOL_GRADES)
    for entry in index().get("grades", []):
        if entry.get("grade") and entry["grade"] not in keys:
            keys.append(entry["grade"])
    return tuple(keys)


def is_school(grade):
    return grade in SCHOOL_GRADES


def school_entries():
    return [g for g in index().get("grades", []) if g.get("kind") == "school"]


def track_entries():
    return [g for g in index().get("grades", []) if g.get("kind") != "school"]


def normalize_grade(value):
    value = (value or "").lower().replace("class", "").replace("grade", "").replace("-see", "")
    value = value.strip(" -_/")
    return value if value in grade_keys() else None


@lru_cache(maxsize=96)
def subject(grade, subject_key):
    grade = normalize_grade(grade)
    if not grade or not subject_key.replace("-", "").isalnum():
        return None
    path = os.path.join(DATA_DIR, "%s-%s.json" % (grade, subject_key))
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    _defaults(data)
    data.setdefault("questions", None)
    data["library_grade"] = LIBRARY_GRADE.get(grade) or (
        COURSE_LIBRARY_GRADE if data.get("kind") == "course" else TRACK_LIBRARY_GRADE)
    return data


def grade_entry(grade):
    grade = normalize_grade(grade)
    for entry in index().get("grades", []):
        if entry.get("grade") == grade:
            return entry
    return None


def summary():
    """Counts for the hub and the app. "grades" counts school grades only: installed app
    versions print it as a number of classes; the tracks are counted apart. The app prints
    "units" as chapters with notes, so a track adds only the chapters already written."""
    grades = index().get("grades", [])
    subjects = sum(len(g.get("subjects", [])) for g in grades)
    units = sum(s.get("unit_count", 0) if g.get("kind") == "school" else s.get("notes_ready", 0)
                for g in grades for s in g.get("subjects", []))
    topics = sum(s.get("topic_count", 0) for g in grades for s in g.get("subjects", []))
    return {"grades": len(school_entries()), "tracks": len(track_entries()),
            "subjects": subjects, "units": units, "topics": topics}


def neighbours(grade, subject_key):
    entry = grade_entry(grade) or {}
    keys = [s["subject"] for s in entry.get("subjects", [])]
    if subject_key not in keys:
        return None, None
    i = keys.index(subject_key)
    prev_s = entry["subjects"][i - 1] if i > 0 else None
    next_s = entry["subjects"][i + 1] if i + 1 < len(keys) else None
    return prev_s, next_s


@lru_cache(maxsize=1)
def practice_counts():
    """(grade, subject) -> question banks, model papers and whether an exam guide exists.

    Read from the exported books once per worker; they only change with a deploy. The hub and
    the apps use it to say where the practice material is instead of burying it in each subject."""
    from . import study_data
    out = {}
    for entry in index().get("grades", []):
        grade = str(entry.get("grade", ""))
        for card in entry.get("subjects", []):
            try:
                info = study_data.subject_index(grade, card.get("subject"))
            except Exception:
                continue
            banks = info.get("banks") or []
            out[(grade, card.get("subject"))] = {
                "bank_count": sum(1 for b in banks if b.get("kind") != "model"),
                "model_count": sum(1 for b in banks if b.get("kind") == "model"),
                "has_guide": bool(info.get("guide")),
            }
    return out


def with_practice(entries):
    """Copies of grade entries whose subject cards carry the counts above."""
    counts = practice_counts()
    out = []
    for entry in entries:
        entry = dict(entry)
        grade = str(entry.get("grade", ""))
        entry["subjects"] = [dict(c, **counts.get((grade, c.get("subject")), {"bank_count": 0, "model_count": 0, "has_guide": False}))
                             for c in entry.get("subjects", [])]
        out.append(entry)
    return out
