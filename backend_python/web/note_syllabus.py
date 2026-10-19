import json
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace

MANAGED_GRADES = ('Class 8', 'Class 10 / SEE', 'Class 11', 'Class 12')


def slug(value):
    return value.lower().replace(' / see', '-see').replace(' ', '-')


@lru_cache(maxsize=1)
def books():
    path = Path(__file__).resolve().parents[1] / 'api/data/note_syllabus.json'
    return json.loads(path.read_text(encoding='utf-8'))['books']


def entries_for(grade, subject):
    from api.models import SyllabusContent
    if grade not in MANAGED_GRADES:
        return list(SyllabusContent.objects.filter(grade_level__iexact=grade, subject__iexact=subject).order_by('order'))
    book = next((b for b in books() if b['grade'] == grade and b['subject'].lower() == subject.lower()), None)
    if not book:
        return []
    return [SimpleNamespace(
        chapter_id=ch['id'], chapter_title=ch['name'], text_content=ch['text_content'],
        question_answers=ch['question_answers'], source_resource_id='', source_label=book['source_label'],
        rich_content={}, study_meta={**ch, 'language': book['language']},
    ) for ch in book['chapters']]


def categories():
    from api.models import SyllabusContent
    groups = {}
    for book in books():
        groups.setdefault(book['grade'], []).append({
            'name': book['subject'], 'display_name': book['display_name'], 'slug': slug(book['subject']),
            'url': f"/subject/{slug(book['grade'])}/{slug(book['subject'])}/",
            'chapter_count': len(book['chapters']),
        })
    for grade, subject in SyllabusContent.objects.exclude(grade_level__in=MANAGED_GRADES).values_list('grade_level', 'subject').distinct():
        groups.setdefault(grade, []).append({'name': subject, 'display_name': subject, 'slug': slug(subject),
                                           'url': f'/subject/{slug(grade)}/{slug(subject)}/', 'chapter_count': 0})
    return [{'grade': grade, 'subjects': sorted(subjects, key=lambda s: s['name']),
             'order': MANAGED_GRADES.index(grade) if grade in MANAGED_GRADES else 999}
            for grade, subjects in sorted(groups.items(), key=lambda x: MANAGED_GRADES.index(x[0]) if x[0] in MANAGED_GRADES else 999)]


def navigation(grade):
    cats = categories()
    grades = [{'name': c['grade'], 'slug': slug(c['grade'])} for c in cats]
    subjects = [{'name': s['name'], 'slug': s['slug']} for c in cats if c['grade'] == grade for s in c['subjects']]
    return grades, subjects
