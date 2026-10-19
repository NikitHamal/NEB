import unicodedata
from functools import lru_cache

from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control

from . import syllabus_data
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


def syllabus_subject(request, grade, subject):
    data = syllabus_data.subject(grade, subject)
    if not data:
        raise Http404("Syllabus not found")
    if grade != data["grade"]:
        return redirect("web:syllabus_subject", grade=data["grade"], subject=subject, permanent=True)
    prev_s, next_s = syllabus_data.neighbours(data["grade"], subject)
    hours_total = sum(u["hours"] or 0 for u in data["units"])
    for unit in data["units"]:
        unit["share"] = round(100.0 * unit["hours"] / hours_total, 2) if unit["hours"] and hours_total else 0
    ctx = _ctx(
        request,
        syl=data,
        syl_prev=prev_s,
        syl_next=next_s,
        syl_hours_total=hours_total,
        syl_siblings=(syllabus_data.grade_entry(data["grade"]) or {}).get("subjects", []),
        seo_title="%s %s Syllabus — Units, Topics and Exam Pattern | NEBians" % (data["grade_label"], data["name"]),
        seo_description="Complete %s %s syllabus: %d units, %d topics, working hours, exam pattern and key points from the NEBians study book." % (
            data["grade_label"], data["name"], data["unit_count"], data["topic_count"]),
    )
    return render(request, "web/syllabus/subject.html", ctx)


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
