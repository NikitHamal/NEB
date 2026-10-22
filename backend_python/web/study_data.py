"""Read the chapters and question banks exported from the NEBians books.

`notes/tools/export_study.py` writes, per grade and subject,

    web/data/study/<grade>-<subject>/index.json      chapters and banks that exist
    web/data/study/<grade>-<subject>/unit-NN.json    one chapter: toc + html
    web/data/study/<grade>-<subject>/bank-NN.json    one question-bank chapter
    web/data/study/<grade>-<subject>/guide.json      the exam guide of the grade

The website's reader and the app's API both read through this module. Chapters are big
(30-200 KB of HTML), so only the small indexes are cached for the life of the process;
chapters are cached a few at a time.
"""
import json
import os
from functools import lru_cache

from . import syllabus_data

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "study")
BANK_KINDS = {
    "objective": ("Objective questions", "Multiple choice and very short answers, unit by unit"),
    "subjective": ("Subjective questions", "Short and long answers with model solutions"),
    "model": ("Model sets and predicted questions", "Full papers in the board's pattern, with keys"),
}


def _folder(grade, subject_key):
    grade = syllabus_data.normalize_grade(grade)
    if not grade or not subject_key or not subject_key.replace("-", "").isalnum():
        return None
    path = os.path.join(DATA_DIR, "%s-%s" % (grade, subject_key))
    return path if os.path.isdir(path) else None


@lru_cache(maxsize=64)
def subject_index(grade, subject_key):
    folder = _folder(grade, subject_key)
    if not folder or not os.path.exists(os.path.join(folder, "index.json")):
        return {"units": [], "banks": [], "guide": None}
    with open(os.path.join(folder, "index.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    data.setdefault("units", [])
    data.setdefault("banks", [])
    data.setdefault("guide", None)
    for b in data["banks"]:
        label, blurb = BANK_KINDS.get(b.get("kind"), (b.get("title", ""), ""))
        b["label"], b["blurb"] = label, blurb
    return data


@lru_cache(maxsize=48)
def _read(grade, subject_key, name):
    folder = _folder(grade, subject_key)
    if not folder:
        return None
    path = os.path.join(folder, name)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def chapter(grade, subject_key, unit_no):
    try:
        unit_no = int(unit_no)
    except (TypeError, ValueError):
        return None
    return _read(grade, subject_key, "unit-%02d.json" % unit_no)


def bank(grade, subject_key, bank_no):
    try:
        bank_no = int(bank_no)
    except (TypeError, ValueError):
        return None
    return _read(grade, subject_key, "bank-%02d.json" % bank_no)


def guide(grade, subject_key):
    return _read(grade, subject_key, "guide.json")


def chapter_neighbours(grade, subject_key, unit_no):
    units = [u["no"] for u in subject_index(grade, subject_key)["units"]]
    if unit_no not in units:
        return None, None
    i = units.index(unit_no)
    return (units[i - 1] if i > 0 else None), (units[i + 1] if i + 1 < len(units) else None)
