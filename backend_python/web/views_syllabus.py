import re
import unicodedata
from functools import lru_cache

from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control

from . import study_data, syllabus_data
from .view_helpers import _ctx


def syllabus_hub_context(grade=None):
    data = syllabus_data.index()
    grades = data.get("grades", [])
    current = syllabus_data.normalize_grade(grade) or (grades[-1]["grade"] if grades else None)
    return {
        "syllabus_grades": grades,
        "syllabus_current_grade": current,
        "syllabus_totals": syllabus_data.summary(),
    }


def syllabus_hub(request, grade=None):
    grade = grade or request.GET.get("grade")
    ctx = _ctx(request, **syllabus_hub_context(grade))
    return render(request, "web/syllabus/hub.html", ctx)


def _exam_rows(exam):
    """'3hr, FM 75 written (+25 internal) | Group A MCQ 11x1=11 | ...' -> head + rows."""
    parts = [p.strip() for p in (exam or "").split("|") if p.strip()]
    if not parts:
        return "", []
    rows = []
    for p in parts[1:]:
        m = re.match(r"^(.*?)\s*(\d+)\s*[x×]\s*(\d+)\s*=\s*(\d+)\s*$", p)
        if m:
            rows.append({"label": m.group(1).strip(" :-"), "count": m.group(2), "each": m.group(3), "total": m.group(4)})
        else:
            rows.append({"label": p, "count": "", "each": "", "total": ""})
    return parts[0], rows


def _area_weights(units):
    hours, total = {}, 0
    for u in units:
        if u["hours"]:
            hours[u["area"] or "Units"] = hours.get(u["area"] or "Units", 0) + u["hours"]
            total += u["hours"]
    return [{"area": a, "hours": h, "pct": round(100.0 * h / total, 1)} for a, h in sorted(hours.items(), key=lambda kv: -kv[1])] if total else []


def _subject_ctx(grade, subject):
    data = syllabus_data.subject(grade, subject)
    if not data:
        raise Http404("Syllabus not found")
    data = dict(data, units=[dict(u) for u in data["units"]])   # the loader's copy is cached; never annotate it
    study = study_data.subject_index(data["grade"], subject)
    by_no = {u["no"]: u for u in study["units"]}
    hours_total = sum(u["hours"] or 0 for u in data["units"])
    for unit in data["units"]:
        unit["share"] = round(100.0 * unit["hours"] / hours_total, 2) if unit["hours"] and hours_total else 0
        unit["study"] = by_no.get(unit["no"])
    return data, study, hours_total


def syllabus_subject(request, grade, subject):
    data, study, hours_total = _subject_ctx(grade, subject)
    if grade != data["grade"]:
        return redirect("web:syllabus_subject", grade=data["grade"], subject=subject, permanent=True)
    prev_s, next_s = syllabus_data.neighbours(data["grade"], subject)
    exam_head, exam_rows = _exam_rows(data.get("exam"))
    ctx = _ctx(
        request,
        syl=data,
        study=study,
        syl_prev=prev_s,
        syl_next=next_s,
        syl_hours_total=hours_total,
        syl_exam_head=exam_head,
        syl_exam_rows=exam_rows,
        syl_area_weights=_area_weights(data["units"]),
        syl_read_min=sum(u.get("read_min", 0) for u in study["units"]),
        syl_siblings=(syllabus_data.grade_entry(data["grade"]) or {}).get("subjects", []),
        seo_title="%s %s — Syllabus, Chapter Notes and Question Bank | NEBians" % (data["grade_label"], data["name"]),
        seo_description="%s %s: all %d units of the syllabus with full chapter notes, worked examples, practice questions with answers and a question bank in the board's pattern." % (
            data["grade_label"], data["name"], data["unit_count"]),
    )
    return render(request, "web/syllabus/subject.html", ctx)


def _reader(request, grade, subject, doc, kind, number=None):
    data, study, _ = _subject_ctx(grade, subject)
    if not doc:
        raise Http404("Not found")
    prev_no = next_no = None
    unit = None
    if kind == "unit":
        prev_no, next_no = study_data.chapter_neighbours(data["grade"], subject, number)
        unit = next((u for u in data["units"] if u["no"] == number), None)
    elif kind == "bank":
        nos = [b["no"] for b in study["banks"]]
        if number in nos:
            i = nos.index(number)
            prev_no = nos[i - 1] if i > 0 else None
            next_no = nos[i + 1] if i + 1 < len(nos) else None
    title = doc["title"]
    label = {"unit": "Unit %s" % number, "bank": "Question bank", "guide": "Exam guide"}[kind]
    ctx = _ctx(
        request,
        syl=data,
        study=study,
        doc=doc,
        doc_kind=kind,
        doc_no=number,
        doc_label=label,
        doc_unit=unit,
        doc_prev=prev_no,
        doc_next=next_no,
        doc_key="%s/%s/%s%s" % (data["grade"], subject, kind, number or ""),
        seo_title="%s — %s %s %s | NEBians" % (title, data["grade_label"], data["name"], "notes" if kind == "unit" else label.lower()),
        seo_description=("%s %s, %s: %s. Full notes with worked examples, figures and practice questions with answers." % (
            data["grade_label"], data["name"], label, title))[:300],
    )
    return render(request, "web/syllabus/reader.html", ctx)


def syllabus_chapter(request, grade, subject, unit_no):
    data = syllabus_data.subject(grade, subject)
    if data and grade != data["grade"]:
        return redirect("web:syllabus_chapter", grade=data["grade"], subject=subject, unit_no=unit_no, permanent=True)
    return _reader(request, grade, subject, study_data.chapter(grade, subject, unit_no), "unit", unit_no)


def syllabus_bank(request, grade, subject, bank_no):
    return _reader(request, grade, subject, study_data.bank(grade, subject, bank_no), "bank", bank_no)


def syllabus_guide(request, grade, subject):
    return _reader(request, grade, subject, study_data.guide(grade, subject), "guide")


def _fold(text):
    text = unicodedata.normalize("NFKD", text or "")
    return "".join(c for c in text if not unicodedata.combining(c) or "\u0900" <= c <= "\u097f").lower()


@lru_cache(maxsize=1)
def _search_rows():
    rows = []
    for g in syllabus_data.index().get("grades", []):
        for s in g.get("subjects", []):
            data = syllabus_data.subject(g["grade"], s["subject"]) or {}
            for u in data.get("units", []):
                fields = [(4, u["title"])] + [(3, t) for t in u["topics"]]
                fields += [(2, x["title"]) for x in u.get("sections", [])] + [(2, t) for t in u.get("terms", [])]
                fields += [(1, p) for p in u.get("summary", [])]
                rows.append({"grade": g["grade"], "subject": s["subject"], "name": s["name"],
                             "unit": u["no"], "title": u["title"],
                             "fields": [(w, text, _fold(text)) for w, text in fields]})
    return rows


def _snippet(text, term, width=110):
    i = _fold(text).find(term)
    if len(text) <= width or i < 0:
        return text[:width] + ("…" if len(text) > width else "")
    start = max(0, i - width // 3)
    return ("…" if start else "") + text[start:start + width] + ("…" if start + width < len(text) else "")


def search_payload(q, grade=None):
    q = (q or "").strip()[:80]
    grade = syllabus_data.normalize_grade(grade)
    terms = [t for t in _fold(q).split() if t]
    hits = []
    if terms:
        for row in _search_rows():
            score, ok = 0.0, True
            for term in terms:
                found = [(w, text) for w, text, folded in row["fields"] if term in folded]
                if not found:
                    ok = False
                    break
                score += max(w for w, _ in found) + min(len(found), 4) * 0.25
            if not ok:
                continue
            if row["grade"] == grade:
                score += 3
            inner = [(w, text) for w, text, folded in row["fields"][1:] if terms[0] in folded]
            match = max(inner, key=lambda f: f[0])[1] if inner else (row["fields"][1][1] if len(row["fields"]) > 1 else "")
            hits.append((score, {"grade": row["grade"], "subject": row["subject"], "name": row["name"],
                                 "unit": row["unit"], "title": row["title"], "match": _snippet(match, terms[0])}))
    hits.sort(key=lambda h: -h[0])
    return {"q": q, "results": [h[1] for h in hits[:30]], "total": len(hits)}


@cache_control(public=True, max_age=600)
def syllabus_search(request):
    return JsonResponse(search_payload(request.GET.get("q"), request.GET.get("grade")),
                        json_dumps_params={"ensure_ascii": False})
