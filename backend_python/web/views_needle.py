import json
import logging
import re
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count

from web.rate_limit import web_rate_limit

logger = logging.getLogger(__name__)

ALLOWED_TOOLS = {'search_resources', 'find_notes', 'get_forum_posts', 'get_subjects'}

CLOUD_SYSTEM_PROMPT = """You are Neby, the AI assistant inside NEBians — a Nepali learning community platform for teachers, learners, explorers, students, and parents across all levels, faculties, disciplines, and fields (not restricted to NEB curriculum or NEB grades).
You have access to platform tools but NOT native function calling, so you must emit tool requests as strict JSON.
Decide which of these fits the user's intent:

Tools (emit ONE of these when the user wants that action):
- search_resources: arguments {"query": "...", "subject"?: "...", "resource_type"?: "PDF|Note|Past Paper|Textbook|Video|Link"} — find learning materials and resources
- find_notes: arguments {"subject": "...", "grade_level"?: "e.g. Class 11, Class 12, SEE, Bachelor, Master", "exam_type"?: "Notes|Board|Final|SEE|Mock|Reference"} — find notes or past papers for a subject and level
- get_forum_posts: arguments {"category"?: "...", "sort"?: "recent|popular"} — forum discussions across topics
- get_subjects: arguments {} — list all available subjects and topics
- navigate_to: arguments {"page": "home|library|forum|search|news|settings|bookmarks|upload|results|leaderboard|tools"} — move the user to a page

Rules:
1. If the user's request maps to a tool, reply with EXACTLY one JSON object and nothing else:
   {"tool_call": {"name": "find_notes", "arguments": {"subject": "Physics", "grade_level": "Class 12"}}}
2. Otherwise reply as a friendly, helpful AI assistant for all learners, educators, and explorers. Your reply MUST be a JSON object:
   {"chat": "your friendly reply here"}
3. Never wrap JSON in markdown fences. Never add text outside the JSON object.
4. Keep chat replies concise, clear, and informative. When users ask what platform this is or what it covers, clarify that NEBians is a Nepali learning community platform for teachers, learners, explorers, students, and parents across all levels, faculties, and fields."""


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


@require_POST
@web_rate_limit('neby-cloud', limit=15, window=60)
def ajax_neby_cloud(request):
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    query = (body.get('query') or '').strip()[:500]
    if not query:
        return JsonResponse({'error': 'query required'}, status=400)

    local_guess = body.get('localGuess')
    if not isinstance(local_guess, dict) or not isinstance(local_guess.get('name'), str):
        local_guess = None

    mode, payload = _cloud_route(query, local_guess)
    if mode is None:
        return JsonResponse({'error': 'Cloud AI unavailable. Try again in a moment.'}, status=502)
    return JsonResponse({'mode': mode, **payload})


def _cloud_route(query, local_guess=None):
    system_prompt = CLOUD_SYSTEM_PROMPT
    if local_guess:
        guess_json = json.dumps(local_guess)
        system_prompt += (
            "\n\nThe on-device model guessed this action with low confidence: "
            + guess_json
            + "\nIf the guess is sensible, emit it as your tool_call. Otherwise emit "
            "the correct tool_call or a chat reply."
        )

    raw = None
    try:
        from api import qwencloud_proxy
        raw = qwencloud_proxy.simple_chat(query, system_prompt=system_prompt,
                                          model='qwen-flash', thinking=False)
        if raw and raw.startswith('[Error]'):
            raw = None
    except Exception as exc:
        logger.warning('neby cloud: qwencloud failed: %s', exc)
        raw = None

    if not raw:
        try:
            from api import inception_proxy
            raw = inception_proxy.simple_chat(
                user_message=query,
                system_prompt=system_prompt,
                reasoning_effort='low',
            )
        except Exception as exc:
            logger.warning('neby cloud: inception failed: %s', exc)
            raw = None

    if raw:
        parsed = _parse_cloud_reply(raw)
        if parsed is not None:
            kind, name, args, text = parsed
            if kind == 'tool' and name in ALLOWED_TOOLS:
                try:
                    result = _execute_tool(name, args)
                    return 'tool', {'tool': name, 'args': args, 'result': result}
                except Exception as exc:
                    logger.warning('neby cloud: tool %s failed: %s', name, exc)
            if kind == 'tool' and name == 'navigate_to':
                return 'tool', {'tool': 'navigate_to', 'args': args, 'result': None}
            if kind == 'chat' and text:
                return 'chat', {'text': text}

    fallback = None
    try:
        from api import qwen_proxy
        fallback = qwen_proxy.call_qwen(
            CLOUD_SYSTEM_PROMPT,
            query,
            model='qwen3.8-max',
            max_tokens=300,
        )
    except Exception as exc:
        logger.warning('neby cloud: qwen fallback failed: %s', exc)
        fallback = None

    if fallback:
        parsed = _parse_cloud_reply(fallback)
        if parsed is not None:
            kind, name, args, text = parsed
            if kind == 'tool' and name in ALLOWED_TOOLS:
                try:
                    result = _execute_tool(name, args)
                    return 'tool', {'tool': name, 'args': args, 'result': result}
                except Exception as exc:
                    logger.warning('neby cloud: fallback tool %s failed: %s', name, exc)
            if kind == 'tool' and name == 'navigate_to':
                return 'tool', {'tool': 'navigate_to', 'args': args, 'result': None}
            if kind == 'chat' and text:
                return 'chat', {'text': text}

    return None, {}


def _parse_cloud_reply(raw):
    """Parse Mercury's reply into (kind, name, args, text) or None.

    Accepts {"tool_call": {"name": ..., "arguments": {...}}} and
    {"chat": "..."}, with or without markdown fences around the JSON.
    """
    text = (raw or '').strip()
    if not text:
        return None

    candidate = text
    if candidate.startswith('```'):
        candidate = re.sub(r'^```(?:json)?\s*|\s*```$', '', candidate, flags=re.S).strip()

    data = None
    for attempt in (candidate, text):
        try:
            data = json.loads(attempt)
            break
        except (json.JSONDecodeError, ValueError):
            match = re.search(r'\{.*\}', attempt, re.S)
            if match:
                try:
                    data = json.loads(match.group(0))
                    break
                except (json.JSONDecodeError, ValueError):
                    pass

    if isinstance(data, dict):
        tc = data.get('tool_call')
        if isinstance(tc, dict):
            name = str(tc.get('name') or '').strip()
            args = tc.get('arguments')
            if name and isinstance(args, dict):
                return ('tool', name, args, '')
        chat = data.get('chat')
        if isinstance(chat, str) and chat.strip():
            return ('chat', '', {}, chat.strip())

    return None


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
    import os
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
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
