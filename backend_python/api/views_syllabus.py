"""Syllabus for the native apps, read from the same export as the website."""
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from web import study_data, syllabus_data
from web.views_syllabus import search_payload
from .throttles import SearchRateThrottle


@api_view(['GET'])
@permission_classes([AllowAny])
def syllabus_index(request):
    """School grades under "grades" (installed app versions print every entry there as
    "Class N"); the entrance tracks (CEE, IOE, ...) under "tracks", in the same shape plus
    "short" ("CEE") and "kind" ("entrance")."""
    data = dict(syllabus_data.index())
    data['grades'] = syllabus_data.school_entries()
    data['tracks'] = syllabus_data.track_entries()
    data['totals'] = syllabus_data.summary()
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def syllabus_subject(request, grade, subject):
    data = syllabus_data.subject(grade, subject)
    if not data:
        return Response({'detail': 'Syllabus not found.'}, status=404)
    study = study_data.subject_index(data['grade'], subject)
    by_no = {u['no']: u for u in study['units']}
    data = dict(data)
    data['units'] = [dict(u, read_min=(by_no.get(u['no']) or {}).get('read_min', 0),
                          has_chapter=u['no'] in by_no,
                          exam=(by_no.get(u['no']) or {}).get('exam')) for u in data['units']]
    data['banks'] = study['banks']
    data['guide'] = study['guide']
    return Response(data)


def _doc_response(doc, kind, number, prev_no, next_no):
    if not doc:
        return Response({'detail': 'Not found.'}, status=404)
    # "exam" ({"minutes", "negative"}) only on the model papers of an entrance mock book
    out = {k: doc.get(k) for k in ('title', 'area', 'hours', 'lang', 'words', 'read_min', 'figures', 'toc', 'html', 'kind', 'exam')}
    out.update({'type': kind, 'no': number, 'prev': prev_no, 'next': next_no,
                'media_base': 'https://nebians.consica.com.np/'})
    return Response(out)


@api_view(['GET'])
@permission_classes([AllowAny])
def syllabus_chapter(request, grade, subject, unit_no):
    """One chapter of the book: its contents list and its HTML (maths as TeX in span.m)."""
    prev_no, next_no = study_data.chapter_neighbours(grade, subject, unit_no)
    return _doc_response(study_data.chapter(grade, subject, unit_no), 'unit', unit_no, prev_no, next_no)


@api_view(['GET'])
@permission_classes([AllowAny])
def syllabus_bank(request, grade, subject, bank_no):
    nos = [b['no'] for b in study_data.subject_index(grade, subject)['banks']]
    i = nos.index(bank_no) if bank_no in nos else -1
    prev_no = nos[i - 1] if i > 0 else None
    next_no = nos[i + 1] if 0 <= i < len(nos) - 1 else None
    return _doc_response(study_data.bank(grade, subject, bank_no), 'bank', bank_no, prev_no, next_no)


@api_view(['GET'])
@permission_classes([AllowAny])
def syllabus_guide(request, grade, subject):
    return _doc_response(study_data.guide(grade, subject), 'guide', None, None, None)


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def syllabus_search(request):
    """Installed app versions print every hit as "Class N", so the entrance books are searched
    only when the app asks for them (tracks=1, sent since the tracks reached the app) or the
    search comes from a track."""
    grade = syllabus_data.normalize_grade(request.GET.get('grade'))
    tracks = request.GET.get('tracks') == '1' or bool(grade and not syllabus_data.is_school(grade))
    return Response(search_payload(request.GET.get('q'), request.GET.get('grade'), tracks=tracks))


def _legacy_slug(grade):
    return 'class-%s' % grade if syllabus_data.is_school(grade) else grade


def legacy_categories():
    """The classes only: app versions from before api/syllabus/v2 open a category by slugifying
    its label ("Class 10" -> class-10), which an entrance track's label would not survive."""
    categories = []
    for order, g in enumerate(syllabus_data.school_entries()):
        categories.append({
            'grade': g['label'],
            'order': order,
            'subjects': [{'name': s['name'], 'slug': s['subject'],
                          'url': '/app/syllabus/%s/%s/' % (g['grade'], s['subject'])} for s in g['subjects']],
        })
    return categories


def _bullets(items):
    return '\n'.join('- %s' % item for item in items)


def legacy_subject_detail(grade_slug, subject_slug):
    data = syllabus_data.subject(grade_slug, subject_slug)
    if not data:
        return None
    chapters = []
    word = 'Unit' if data.get('kind', 'school') == 'school' else 'Chapter'
    for u in data['units']:
        guide = [{'id': 'topics', 'title': 'Topics', 'content': _bullets(u['topics'])}]
        if u['summary']:
            guide.append({'id': 'key-points', 'title': 'Key points', 'content': _bullets(u['summary'])})
        if u['terms']:
            guide.append({'id': 'key-terms', 'title': 'Key terms', 'content': ', '.join(u['terms'])})
        if u['sections'] and len(u['sections']) != len(u['topics']):
            guide.append({'id': 'book', 'title': 'What the study book covers',
                          'content': _bullets('%s %s' % (s['no'], s['title']) for s in u['sections'])})
        chapters.append({'id': 'unit-%d' % u['no'], 'name': '%s %d: %s' % (word, u['no'], u['title']),
                         'guide_sections': guide, 'qa_sections': [], 'notes': [], 'solutions': [],
                         'papers': [], 'textbooks': [], 'other': [], 'count': 0})
    entry = syllabus_data.grade_entry(data['grade']) or {'subjects': []}
    return {
        'grade': data['grade_label'],
        'subject': data['name'],
        'grade_slug': _legacy_slug(data['grade']),
        'subject_slug': data['subject'],
        # switching grade keeps to the same kind: the classes for a class, the tracks for a track
        'grade_list': [{'name': g['label'], 'slug': _legacy_slug(g['grade'])} for g in syllabus_data.index().get('grades', [])
                       if g.get('kind', 'school') == data.get('kind', 'school')],
        'subject_list': [{'name': s['name'], 'slug': s['subject']} for s in entry['subjects']],
        'chapters': chapters,
        'total_count': 0,
    }
