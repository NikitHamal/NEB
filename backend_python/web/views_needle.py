import json
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count

logger = logging.getLogger(__name__)

ALLOWED_TOOLS = {'search_resources', 'find_notes', 'get_forum_posts', 'get_subjects'}


@require_POST
def ajax_neby_assist(request):
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    tool = (body.get('tool') or '').strip()
    args = body.get('args') or {}

    if not tool:
        return JsonResponse({'error': 'tool required'}, status=400)
    if tool not in ALLOWED_TOOLS:
        return JsonResponse({'error': 'unknown tool'}, status=400)
    if not isinstance(args, dict):
        return JsonResponse({'error': 'args must be object'}, status=400)

    try:
        result = _execute_tool(tool, args)
        return JsonResponse({'result': result})
    except Exception as exc:
        logger.exception("Neby tool execution error (%s): %s", tool, exc)
        return JsonResponse({'error': 'Something went wrong.'}, status=500)


STOPWORDS = {'for', 'and', 'the', 'with', 'from', 'to', 'of', 'in', 'my', 'me',
             'find', 'show', 'give', 'need', 'want', 'please', 'some', 'any',
             'class', 'grade', 'notes', 'note', 'are', 'is', 'a', 'an', 'on',
             'it', 'this', 'that', 'there', 'have', 'has', 'get', 'about', 'can'}

TYPE_CANON = {}
for canon, aliases in (
    ('PDF', ['pdf']),
    ('Note', ['note', 'notes', 'document']),
    ('Video', ['video', 'videos']),
    ('DOCX', ['docx', 'doc', 'document']),
    ('Image', ['image', 'images']),
    ('Past Paper', ['past paper', 'past papers', 'pastpaper', 'board exam', 'board']),
    ('Textbook', ['textbook', 'textbooks', 'book', 'books']),
    ('Link', ['link', 'links', 'url', 'website']),
):
    for a in aliases:
        TYPE_CANON[a] = canon


def _search_resources(args, limit=5):
    from api.models import Resource

    query = str(args.get('query', ''))[:200]
    subject = str(args.get('subject', ''))[:100]
    resource_type = str(args.get('resource_type', ''))[:50]
    grade_level = str(args.get('grade_level', ''))[:50]
    exam_type = str(args.get('exam_type', ''))[:50]
    if subject.strip().lower() in TYPE_CANON or subject.strip().lower() in ('nebians', 'resources'):
        subject = ''

    base = Resource.objects.filter(approval_status='approved')

    def grade_from_query(q):
        import re
        m = re.search(r'(?:class|grade|gr|std)\s*[-:]?\s*(\d{1,2})', q, re.I)
        if m:
            return m.group(1)
        m = re.search(r'\b(?:SEE|ten|eleven|twelve)\b', q, re.I)
        return None

    auto_grade = grade_level or grade_from_query(query)
    tokens = [t for t in query.split() if len(t) > 2 and t.lower() not in STOPWORDS]

    rt = resource_type.strip().lower()
    normalized_type = TYPE_CANON.get(rt, resource_type)

    def run(with_query, with_type, with_grade, with_exam):
        qs = base
        if with_query and tokens:
            for t in tokens:
                qs = qs.filter(
                    Q(title__icontains=t) |
                    Q(description__icontains=t) |
                    Q(subject__icontains=t) |
                    Q(tags__icontains=t)
                )
        if subject:
            qs = qs.filter(subject__icontains=subject)
        if with_type and normalized_type:
            qs = qs.filter(type__iexact=normalized_type)
        if with_grade and auto_grade:
            qs = qs.filter(grade_level__icontains=auto_grade)
        if with_exam and exam_type:
            qs = qs.filter(exam_type__icontains=exam_type)
        return list(qs.order_by('-like_count', '-view_count').values(
            'id', 'title', 'subject', 'grade_level', 'type', 'exam_type', 'like_count'
        )[:limit])

    for combo in ((True, True, True, True), (True, False, True, True),
                  (True, False, False, True), (True, False, False, False),
                  (False, False, False, False)):
        results = run(*combo)
        if results:
            return {'count': len(results), 'resources': results, 'relaxed': combo != (True, True, True, True)}
    return {'count': 0, 'resources': [], 'relaxed': False}


def _execute_tool(tool, args):
    from api.models import Resource, Post

    if tool == 'search_resources':
        return _search_resources(args, limit=5)

    if tool == 'find_notes':
        return _search_resources(args, limit=6)

    if tool == 'get_forum_posts':
        category = str(args.get('category', ''))[:100]
        sort = str(args.get('sort', 'recent'))
        qs = Post.objects.filter(is_archived=False)
        if category and category.lower() not in ('popular', 'hot', 'all'):
            real_cats = list(
                Post.objects.filter(is_archived=False)
                .exclude(category='')
                .values_list('category', flat=True)
                .distinct()
            )
            matched = [c for c in real_cats if category.lower() in c.lower()]
            if matched:
                qs = qs.filter(category__in=matched)
        if sort == 'popular':
            qs = qs.order_by('-thumbs_up_count', '-created_at')
        else:
            qs = qs.order_by('-created_at')
        results = list(qs.values('id', 'title', 'category', 'thumbs_up_count', 'reply_count')[:5])
        return {'count': len(results), 'posts': results}

    if tool == 'get_subjects':
        data = list(
            Resource.objects.filter(approval_status='approved')
            .exclude(subject='')
            .values('subject')
            .annotate(count=Count('id'))
            .order_by('-count')[:15]
        )
        return {'subjects': data}

    return {}
