"""Read the syllabus exported from the NEBians books.

`notes/tools/export_syllabus.py` writes one JSON file per grade and subject
into `web/data/syllabus/`; the website and the app both read them through
this module, so the two always show the same syllabus.
"""
import json
import os
from functools import lru_cache

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "syllabus")
GRADES = ("8", "10", "11", "12")
LIBRARY_GRADE = {"8": "Class 8", "10": "Class 10 / SEE", "11": "Class 11", "12": "Class 12"}


@lru_cache(maxsize=1)
def index():
    path = os.path.join(DATA_DIR, "index.json")
    if not os.path.exists(path):
        return {"grades": []}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def normalize_grade(value):
    value = (value or "").lower().replace("class", "").replace("grade", "").replace("-see", "")
    value = value.strip(" -_/")
    return value if value in GRADES else None


@lru_cache(maxsize=64)
def subject(grade, subject_key):
    grade = normalize_grade(grade)
    if not grade or not subject_key.replace("-", "").isalnum():
        return None
    path = os.path.join(DATA_DIR, "%s-%s.json" % (grade, subject_key))
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    data["library_grade"] = LIBRARY_GRADE[grade]
    return data


def grade_entry(grade):
    grade = normalize_grade(grade)
    for entry in index().get("grades", []):
        if entry.get("grade") == grade:
            return entry
    return None


def summary():
    grades = index().get("grades", [])
    subjects = sum(len(g.get("subjects", [])) for g in grades)
    units = sum(s.get("unit_count", 0) for g in grades for s in g.get("subjects", []))
    topics = sum(s.get("topic_count", 0) for g in grades for s in g.get("subjects", []))
    return {"grades": len(grades), "subjects": subjects, "units": units, "topics": topics}


def neighbours(grade, subject_key):
    entry = grade_entry(grade) or {}
    keys = [s["subject"] for s in entry.get("subjects", [])]
    if subject_key not in keys:
        return None, None
    i = keys.index(subject_key)
    prev_s = entry["subjects"][i - 1] if i > 0 else None
    next_s = entry["subjects"][i + 1] if i + 1 < len(keys) else None
    return prev_s, next_s
