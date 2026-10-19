"""Syllabus for the native apps, read from the same export as the website."""
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from web import syllabus_data
from web.views_syllabus import search_payload
from .throttles import SearchRateThrottle


@api_view(['GET'])
@permission_classes([AllowAny])
def syllabus_index(request):
    data = dict(syllabus_data.index())
    data['totals'] = syllabus_data.summary()
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def syllabus_subject(request, grade, subject):
    data = syllabus_data.subject(grade, subject)
    if not data:
        return Response({'detail': 'Syllabus not found.'}, status=404)
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([SearchRateThrottle])
def syllabus_search(request):
    return Response(search_payload(request.GET.get('q'), request.GET.get('grade')))


def legacy_categories():
    categories = []
    for order, g in enumerate(syllabus_data.index().get('grades', [])):
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
    for u in data['units']:
        guide = [{'id': 'topics', 'title': 'Topics', 'content': _bullets(u['topics'])}]
        if u['summary']:
            guide.append({'id': 'key-points', 'title': 'Key points', 'content': _bullets(u['summary'])})
        if u['terms']:
            guide.append({'id': 'key-terms', 'title': 'Key terms', 'content': ', '.join(u['terms'])})
        if u['sections'] and len(u['sections']) != len(u['topics']):
            guide.append({'id': 'book', 'title': 'What the study book covers',
                          'content': _bullets('%s %s' % (s['no'], s['title']) for s in u['sections'])})
        chapters.append({'id': 'unit-%d' % u['no'], 'name': 'Unit %d: %s' % (u['no'], u['title']),
                         'guide_sections': guide, 'qa_sections': [], 'notes': [], 'solutions': [],
                         'papers': [], 'textbooks': [], 'other': [], 'count': 0})
    entry = syllabus_data.grade_entry(data['grade']) or {'subjects': []}
    return {
        'grade': data['grade_label'],
        'subject': data['name'],
        'grade_slug': 'class-%s' % data['grade'],
        'subject_slug': data['subject'],
        'grade_list': [{'name': g['label'], 'slug': 'class-%s' % g['grade']} for g in syllabus_data.index().get('grades', [])],
        'subject_list': [{'name': s['name'], 'slug': s['subject']} for s in entry['subjects']],
        'chapters': chapters,
        'total_count': 0,
    }
