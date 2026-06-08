"""Study Lab and private analytics views.

Production notes:
- Study Lab calls Qwen for summaries, mindmaps, quizzes, and flashcards.
- User generated AI material is scoped to the authenticated owner only.
- Existing single ``summary`` values are kept as a backward-compatible compact summary.
"""
import json
import logging
import os
import re
from collections import Counter

from django.db.models import Avg, Max, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .view_helpers import *  # noqa: F401,F403
from api.models import (
    Bookmark,
    Follow,
    Notification,
    Post,
    PostLike,
    Reply,
    ReplyLike,
    Resource,
    ResourceComment,
    ResourceCommentLike,
    ResourceLike,
    StudyDocument,
    StudyDocumentShare,
    StudyFlashcard,
    StudyFlashcardReview,
    StudyQuiz,
    StudyQuizAttempt,
    StudyQuizQuestion,
)
from api.utils import now_ms, uuid_str
from api import qwen_proxy
from api.qwen_utils.file_upload import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, upload_file_from_bytes

logger = logging.getLogger(__name__)

MAX_TEXT_CHARS = 50000
MAX_EXCLUSION_CHARS = 8000


# ── Qwen helpers ───────────────────────────────────────────────────────────

_QWEN_MODEL_CACHE = None


def _qwen_model():
    """Return the default Qwen model ID for Study Lab generations."""
    global _QWEN_MODEL_CACHE
    if _QWEN_MODEL_CACHE:
        return _QWEN_MODEL_CACHE
    try:
        from api.qwen_utils.models import get_default_model
        model = get_default_model()
        _QWEN_MODEL_CACHE = model
        return model
    except Exception:
        return 'qwen3.7-plus'


def _new_qwen_session():
    """Create and prepare a Qwen session with the required anti-bot headers."""
    qwen_session, _ = qwen_proxy._get_session()
    midtoken = qwen_proxy.get_midtoken(qwen_session)
    if midtoken:
        qwen_session.headers['bx-umidtoken'] = midtoken
        qwen_session.headers['bx-v'] = '2.5.31'
    return qwen_session


def _create_qwen_chat(qwen_session):
    return qwen_proxy.create_chat(qwen_session, model=_qwen_model())


def _send_doc_task(prepared, file_prompt, text_prompt, system_prompt):
    """Run a Qwen task against either uploaded file(s) or extracted text."""
    qwen_session = _new_qwen_session()
    chat_id = _create_qwen_chat(qwen_session)
    if not chat_id:
        return None, 'Could not start AI session — try again'

    if prepared.get('has_file') or prepared.get('is_image'):
        result = qwen_proxy.send_message(
            qwen_session,
            chat_id,
            file_prompt,
            model=_qwen_model(),
            parent_id=None,
            uploaded_files=prepared.get('uploaded_files') or [],
            system_prompt=system_prompt,
        )
    else:
        result = qwen_proxy.send_message(
            qwen_session,
            chat_id,
            text_prompt + "\n\n--- DOCUMENT CONTENT ---\n" + (prepared.get('text_content') or '') + "\n--- END ---",
            model=_qwen_model(),
            parent_id=None,
            system_prompt=system_prompt,
        )

    if not result:
        return None, 'AI returned an empty response'
    return result, None


# ── Prompt templates ───────────────────────────────────────────────────────


def _summary_system_prompt(mode):
    if mode == 'detailed':
        length_rule = (
            "Create a detailed study summary that teaches the material clearly. Include enough context, "
            "definitions, step-by-step logic, key formulas, examples when helpful, and exam-focused notes."
        )
    else:
        length_rule = (
            "Create a compact study summary. Prioritize the highest-yield ideas, definitions, formulas, "
            "relationships, and exam points. Keep it concise but complete enough for quick revision."
        )
    return (
        "You are an expert study assistant for Nepali students following the NEB curriculum. "
        f"{length_rule} "
        "Return ONLY the summary content. Do not add an intro sentence, apology, or meta-commentary. "
        "Never start with phrases like 'Here is', 'Here's', 'Below is', or 'I have'. "
        "Start directly with a useful markdown heading. Use clear headings, short paragraphs, bullets, "
        "numbered steps where needed, and **bold** key terms. Write in English unless the source is in Nepali."
    )


_QUIZ_SYSTEM_PROMPT = (
    "You are an expert quiz generator for Nepali students following the NEB curriculum. "
    "Generate fresh, exam-style multiple-choice questions from the provided material. "
    "Do not repeat or lightly paraphrase any existing questions listed by the user. "
    "You MUST respond with ONLY a valid JSON array, no markdown and no extra text. Each element must have: "
    '"question" (string), "options" (array of exactly 4 strings in A/B/C/D order), '
    '"correct" (string: "A", "B", "C", or "D"), "explanation" (string). '
    "Generate exactly {count} questions. Make them progressively harder and avoid vague wording."
)

_FLASHCARD_SYSTEM_PROMPT = (
    "You are an expert flashcard creator for Nepali students following the NEB curriculum. "
    "Create fresh flashcards from the provided material. Do not repeat or lightly paraphrase any existing "
    "flashcards listed by the user. "
    "You MUST respond with ONLY a valid JSON array, no markdown and no extra text. Each element must have: "
    '"front" (string: the question, cue, or key term), "back" (string: the answer or explanation). '
    "Generate exactly {count} flashcards. Cover important concepts, definitions, formulas, comparisons, and likely exam points."
)

_MINDMAP_SYSTEM_PROMPT = (
    "You are an expert visual mindmap architect for Nepali learners. Build a true study mindmap, not a summary. "
    "Create balanced, visual branches that radiate from the main idea and help a learner remember relationships. "
    "You MUST respond with ONLY a valid JSON object, no markdown and no extra text. Use this schema exactly: "
    '{"title":"Main topic","nodes":[{"title":"Branch","note":"optional short note",'
    '"children":[{"title":"Sub-branch","note":"optional short note","children":[]}]}]}. '
    "Use 5 to 7 strong main branches when content allows. Use concise labels of 1-5 words. "
    "Notes must be short memory cues, never paragraph summaries. Use 2 to 4 levels, avoid repeating branch names, "
    "group causes/processes/examples/formulas/comparisons separately, and do not invent facts outside the document."
)


# ── Page views ─────────────────────────────────────────────────────────────


def study_lab(request):
    """Study Lab landing page. Shows sign-in prompt for unauthenticated users."""
    user_id = _get_user_id(request)
    if not user_id:
        ctx = _ctx(request, documents=[], page='study_lab')
        return render(request, 'web/study_lab.html', ctx)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        ctx = _ctx(request, documents=[], page='study_lab')
        return render(request, 'web/study_lab.html', ctx)

    documents = StudyDocument.objects.filter(user=user).order_by('-updated_at')[:50]
    doc_list = [_serialize_study_doc_list_item(d) for d in documents]

    ctx = _ctx(request, documents=doc_list, page='study_lab')
    return render(request, 'web/study_lab.html', ctx)



def study_lab_shared(request, token):
    """Signed-in shared Study Lab document view.

    Owners can share documents as link-access or with named users. Viewers can
    read summaries/mindmaps and interact with existing quizzes and flashcards,
    while generation/editing remains owner-only.
    """
    user_id = _get_user_id(request)
    if not user_id:
        return redirect(f"{reverse('web:login')}?next={request.path}")

    try:
        doc = StudyDocument.objects.select_related('user').get(share_token=token)
    except StudyDocument.DoesNotExist:
        raise Http404('Shared document not found')

    if not _can_access_shared_doc(doc, user_id):
        return render(request, 'web/study_lab_shared_denied.html', _ctx(request, page='study_lab'), status=403)

    owner = doc.user
    quizzes = doc.quizzes.all().order_by('-created_at')
    flashcards = doc.flashcards.all().order_by('card_number')
    ctx = _ctx(
        request,
        page='study_lab',
        shared_doc=_serialize_study_doc_detail(doc),
        shared_owner={
            'username': owner.username,
            'displayName': owner.display_name or owner.username,
            'photoUrl': owner.photo_url or '',
        },
        mindmap=_mindmap_value(doc),
        quizzes=[_serialize_quiz_list_item(q, user_id) for q in quizzes],
        flashcards=[_serialize_flashcard(fc, user_id) for fc in flashcards],
        is_owner=(doc.user_id == user_id),
    )
    return render(request, 'web/study_lab_shared.html', ctx)

def analytics(request):
    """Private analytics dashboard. Only the authenticated user can see their own insights."""
    user_id = _get_user_id(request)
    if not user_id:
        return redirect(f"{reverse('web:login')}?next={request.path}")

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:login')

    now = now_ms()
    day_ms = 86400000
    cutoff_30 = now - 30 * day_ms
    cutoff_14 = now - 14 * day_ms

    posts = Post.objects.filter(user=user, is_archived=False)
    replies = Reply.objects.filter(user=user, is_archived=False)
    resources = Resource.objects.filter(uploaded_by=user)
    resource_comments = ResourceComment.objects.filter(user=user)
    study_docs = StudyDocument.objects.filter(user=user)
    quizzes = StudyQuiz.objects.filter(user=user)
    quiz_attempts = StudyQuizAttempt.objects.filter(user=user)
    flashcards = StudyFlashcard.objects.filter(user=user)
    flash_reviews = StudyFlashcardReview.objects.filter(user=user)

    post_views = posts.aggregate(total=Sum('view_count')).get('total') or 0
    post_likes_received = posts.aggregate(total=Sum('thumbs_up_count')).get('total') or 0
    post_replies_received = posts.aggregate(total=Sum('reply_count')).get('total') or 0
    resource_views = resources.aggregate(total=Sum('view_count')).get('total') or 0
    resource_likes_received = resources.aggregate(total=Sum('like_count')).get('total') or 0
    resource_comments_received = resources.aggregate(total=Sum('comment_count')).get('total') or 0

    latest_attempt = quiz_attempts.order_by('-completed_at').first()
    quiz_stats = quiz_attempts.aggregate(avg=Avg('score'), best=Max('score'), xp=Sum('xp_earned'))
    total_attempt_questions = quiz_attempts.aggregate(total=Sum('total_questions')).get('total') or 0
    total_attempt_score = quiz_attempts.aggregate(total=Sum('score')).get('total') or 0
    quiz_accuracy = round((total_attempt_score / total_attempt_questions) * 100) if total_attempt_questions else 0

    easy_reviews = flash_reviews.filter(confidence='easy').count()
    medium_reviews = flash_reviews.filter(confidence='medium').count()
    hard_reviews = flash_reviews.filter(confidence='hard').count()
    reviewed_total = easy_reviews + medium_reviews + hard_reviews

    today_start = now - (now % day_ms)
    activity_days = []
    max_activity = 1
    for i in range(13, -1, -1):
        start = today_start - i * day_ms
        end = start + day_ms
        counts = {
            'posts': posts.filter(created_at__gte=start, created_at__lt=end).count(),
            'replies': replies.filter(created_at__gte=start, created_at__lt=end).count(),
            'resources': resources.filter(added_at__gte=start, added_at__lt=end).count(),
            'study': quiz_attempts.filter(completed_at__gte=start, completed_at__lt=end).count()
                + StudyFlashcardReview.objects.filter(user=user, last_reviewed_at__gte=start, last_reviewed_at__lt=end).count(),
        }
        total = sum(counts.values())
        max_activity = max(max_activity, total)
        activity_days.append({
            'label': 'Today' if i == 0 else f'{i}d',
            'total': total,
            'counts': counts,
            'height': 0,
        })
    for d in activity_days:
        d['height'] = max(8, round((d['total'] / max_activity) * 100)) if d['total'] else 8

    category_counter = Counter(posts.values_list('category', flat=True))
    subject_counter = Counter()
    for subject in resources.values_list('subject', flat=True):
        for part in (subject or '').split(','):
            part = part.strip()
            if part:
                subject_counter[part] += 1

    top_categories = _counter_rows(category_counter, limit=5)
    top_subjects = _counter_rows(subject_counter, limit=5)

    summaries_count = study_docs.filter(summary_compact__gt='').count() + study_docs.filter(summary_detailed__gt='').count()
    if not summaries_count:
        summaries_count = study_docs.exclude(summary='').count()
    mindmaps_count = study_docs.exclude(mindmap_json='').count()

    suggestions = []
    if study_docs.count() and summaries_count < study_docs.count():
        suggestions.append('Generate compact summaries for documents that still have no summary.')
    if study_docs.count() and mindmaps_count < study_docs.count():
        suggestions.append('Create mindmaps for your main notes to see topic relationships faster.')
    if quizzes.count() and not quiz_attempts.exists():
        suggestions.append('Take at least one generated quiz to start tracking exam readiness.')
    if quiz_attempts.exists() and quiz_accuracy < 70:
        suggestions.append('Review hard flashcards, then generate a fresh quiz from the same document.')
    if hard_reviews:
        suggestions.append(f'Revisit {hard_reviews} hard flashcard review{pluralize_count(hard_reviews)} today.')
    if not resources.exists():
        suggestions.append('Upload one useful resource to build your contribution footprint.')
    if not suggestions:
        suggestions.append('Keep using Study Lab regularly; your recent learning loop looks healthy.')

    ctx = _ctx(
        request,
        page='analytics',
        stats={
            'posts': posts.count(),
            'replies': replies.count(),
            'postViews': post_views,
            'postLikesReceived': post_likes_received,
            'postRepliesReceived': post_replies_received,
            'resources': resources.count(),
            'resourceViews': resource_views,
            'resourceLikesReceived': resource_likes_received,
            'resourceCommentsReceived': resource_comments_received,
            'resourceCommentsMade': resource_comments.count(),
            'followers': Follow.objects.filter(following=user).count(),
            'following': Follow.objects.filter(follower=user).count(),
            'bookmarks': Bookmark.objects.filter(user=user).count(),
            'notificationsUnread': Notification.objects.filter(recipient=user, is_read=False).count(),
            'studyDocs': study_docs.count(),
            'summaries': summaries_count,
            'mindmaps': mindmaps_count,
            'quizzes': quizzes.count(),
            'quizAttempts': quiz_attempts.count(),
            'quizAccuracy': quiz_accuracy,
            'quizXp': quiz_stats.get('xp') or 0,
            'flashcards': flashcards.count(),
            'flashReviews': reviewed_total,
            'easyReviews': easy_reviews,
            'mediumReviews': medium_reviews,
            'hardReviews': hard_reviews,
            'recentPosts': posts.filter(created_at__gte=cutoff_30).count(),
            'recentReplies': replies.filter(created_at__gte=cutoff_30).count(),
            'recentStudyActions': quiz_attempts.filter(completed_at__gte=cutoff_30).count() + flash_reviews.filter(last_reviewed_at__gte=cutoff_30).count(),
        },
        activity_days=activity_days,
        top_categories=top_categories,
        top_subjects=top_subjects,
        top_posts=list(posts.order_by('-view_count', '-thumbs_up_count')[:5]),
        top_resources=list(resources.order_by('-view_count', '-like_count')[:5]),
        recent_docs=list(study_docs.order_by('-updated_at')[:5]),
        recent_attempts=list(quiz_attempts.order_by('-completed_at')[:5]),
        latest_attempt=latest_attempt,
        suggestions=suggestions[:5],
    )
    return render(request, 'web/analytics.html', ctx)


def pluralize_count(n):
    return '' if n == 1 else 's'


def _counter_rows(counter, limit=5):
    if not counter:
        return []
    max_count = max(counter.values()) or 1
    rows = []
    for label, count in counter.most_common(limit):
        rows.append({'label': label, 'count': count, 'width': max(6, round((count / max_count) * 100))})
    return rows


# ── Document upload/list/detail ────────────────────────────────────────────


def ajax_study_upload(request):
    """Upload a PDF/image/document/text file for study. Returns document metadata."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    f = request.FILES.get('file')
    if not f:
        return JsonResponse({'error': 'No file provided'}, status=400)

    ext = os.path.splitext(f.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return JsonResponse({'error': f'Unsupported file type: {ext}'}, status=400)
    if f.size > MAX_FILE_SIZE:
        return JsonResponse({'error': f'File too large (max {MAX_FILE_SIZE // (1024 * 1024)}MB)'}, status=400)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile

    file_data = f.read()
    file_name = f.name
    mime_type = f.content_type or 'application/octet-stream'

    storage_path = f'study_lab/{user_id}/{uuid_str()}{ext}'
    saved_path = default_storage.save(storage_path, ContentFile(file_data))
    file_url = default_storage.url(saved_path)

    now = now_ms()
    doc = StudyDocument.objects.create(
        id=uuid_str(),
        user=user,
        title=os.path.splitext(file_name)[0],
        file_url=file_url,
        file_name=file_name,
        file_size=f.size,
        mime_type=mime_type,
        status='ready',
        created_at=now,
        updated_at=now,
    )

    return JsonResponse({'document': _serialize_study_doc_list_item(doc)}, status=201)


def ajax_study_documents(request):
    """List user's study documents."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    documents = StudyDocument.objects.filter(user=user).order_by('-updated_at')[:50]
    return JsonResponse({'documents': [_serialize_study_doc_list_item(d) for d in documents]})


def ajax_study_document_detail(request, doc_id):
    """Get document detail with summaries, mindmap, quizzes, and flashcards."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    doc, error = _accessible_doc(doc_id, user_id)
    if error:
        return error

    quizzes = doc.quizzes.all().order_by('-created_at')
    flashcards = doc.flashcards.all().order_by('card_number')

    return JsonResponse({
        'document': _serialize_study_doc_detail(doc),
        'mindmap': _mindmap_value(doc),
        'quizzes': [_serialize_quiz_list_item(q, user_id) for q in quizzes],
        'flashcards': [_serialize_flashcard(fc, user_id) for fc in flashcards],
        'totalFlashcards': flashcards.count(),
    })


def ajax_study_delete_document(request, doc_id):
    """Delete a study document and all related quizzes/flashcards."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error
    doc.delete()
    return JsonResponse({'success': True})



def ajax_study_share_settings(request, doc_id):
    """Read/update sharing settings for an owned Study Lab document."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error

    if request.method == 'GET':
        return JsonResponse(_serialize_share_settings(doc, request))
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    body = _json_body(request)
    mode = (body.get('mode') or StudyDocument.SHARE_PRIVATE).strip().lower()
    if mode not in (StudyDocument.SHARE_PRIVATE, StudyDocument.SHARE_LINK, StudyDocument.SHARE_SPECIFIC):
        return JsonResponse({'error': 'Invalid sharing option'}, status=400)

    now = now_ms()
    doc.share_mode = mode
    doc.shared_at = now if mode != StudyDocument.SHARE_PRIVATE else 0
    doc.updated_at = now
    doc.save(update_fields=['share_mode', 'shared_at', 'updated_at'])

    if mode in (StudyDocument.SHARE_PRIVATE, StudyDocument.SHARE_LINK):
        doc.share_grants.all().delete()
    else:
        identifiers = body.get('users') or body.get('recipients') or ''
        resolved, missing = _resolve_share_users(identifiers, owner_id=user_id)
        if missing:
            return JsonResponse({'error': 'Some users were not found', 'missing': missing}, status=400)
        existing_ids = set(doc.share_grants.values_list('user_id', flat=True))
        wanted_ids = set(u.id for u in resolved)
        doc.share_grants.exclude(user_id__in=wanted_ids).delete()
        for u in resolved:
            if u.id in existing_ids:
                continue
            StudyDocumentShare.objects.create(id=uuid_str(), document=doc, user=u, granted_by_id=user_id, created_at=now)

    return JsonResponse(_serialize_share_settings(doc, request))

# ── Summary ────────────────────────────────────────────────────────────────


def ajax_study_generate_summary(request, doc_id):
    """Generate a compact or detailed summary for a document using Qwen."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error

    body = _json_body(request)
    mode = _summary_mode(body.get('mode'))

    prepared = _prepare_doc_for_qwen(doc)
    if not prepared:
        logger.error('Study Lab summary failed: could not read document content')
        return JsonResponse({'error': 'Could not read document content'}, status=502)

    prompt_label = 'detailed' if mode == 'detailed' else 'compact'
    file_prompt = (
        f"Create a {prompt_label} study summary from this file. Start directly with the summary heading. "
        "Do not include any introductory sentence."
    )
    text_prompt = (
        f"Create a {prompt_label} study summary from this document. Start directly with the summary heading. "
        "Do not include any introductory sentence."
    )
    result, err = _send_doc_task(prepared, file_prompt, text_prompt, _summary_system_prompt(mode))
    if err:
        logger.error('Study Lab summary failed: %s', err)
        return JsonResponse({'error': err}, status=502)

    summary = _clean_ai_markdown(result)
    _save_summary(doc, mode, summary)

    return JsonResponse({
        'mode': mode,
        'summary': summary,
        'summaryCompact': doc.summary_compact or doc.summary,
        'summaryDetailed': doc.summary_detailed,
    })


def ajax_study_update_summary(request, doc_id):
    """Allow the owner to edit and save generated compact/detailed summaries."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error

    body = _json_body(request)
    mode = _summary_mode(body.get('mode'))
    summary = (body.get('summary') or '').strip()
    if not summary:
        return JsonResponse({'error': 'Summary cannot be empty'}, status=400)
    if len(summary) > 200000:
        return JsonResponse({'error': 'Summary is too long'}, status=400)

    _save_summary(doc, mode, summary)
    return JsonResponse({
        'mode': mode,
        'summary': summary,
        'summaryCompact': doc.summary_compact or doc.summary,
        'summaryDetailed': doc.summary_detailed,
    })


# ── Mindmap ────────────────────────────────────────────────────────────────


def ajax_study_generate_mindmap(request, doc_id):
    """Generate a hierarchical mindmap JSON object for a document using Qwen."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error

    prepared = _prepare_doc_for_qwen(doc)
    if not prepared:
        return JsonResponse({'error': 'Could not read document content'}, status=502)

    file_prompt = 'Create a study mindmap from this file. Return only the JSON object.'
    text_prompt = 'Create a study mindmap from this document. Return only the JSON object.'
    result, err = _send_doc_task(prepared, file_prompt, text_prompt, _MINDMAP_SYSTEM_PROMPT)
    if err:
        return JsonResponse({'error': err}, status=502)

    mindmap = _parse_json_object_response(result)
    if not mindmap:
        return JsonResponse({'error': 'Failed to parse mindmap from AI response'}, status=502)

    mindmap = _normalize_mindmap(mindmap, doc)
    now = now_ms()
    doc.mindmap_json = json.dumps(mindmap, ensure_ascii=False)
    doc.mindmap_generated_at = now
    doc.updated_at = now
    doc.save(update_fields=['mindmap_json', 'mindmap_generated_at', 'updated_at'])

    return JsonResponse({'mindmap': mindmap})


# ── Quiz ───────────────────────────────────────────────────────────────────


def ajax_study_generate_quiz(request, doc_id):
    """Generate a fresh MCQ quiz from a document using Qwen."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error

    body = _json_body(request)
    question_count = _bounded_int(body.get('count', 10), 5, 40, 10)

    prepared = _prepare_doc_for_qwen(doc)
    if not prepared:
        return JsonResponse({'error': 'Could not read document content'}, status=502)

    exclusions = _quiz_exclusions(doc)
    exclusion_text = _exclusion_block('Existing questions to avoid', exclusions)
    file_prompt = f"Generate {question_count} NEW MCQ questions from this file.\n{exclusion_text}"
    text_prompt = f"Generate {question_count} NEW MCQ questions from this document.\n{exclusion_text}"
    result, err = _send_doc_task(prepared, file_prompt, text_prompt, _QUIZ_SYSTEM_PROMPT.format(count=question_count))
    if err:
        return JsonResponse({'error': err}, status=502)

    questions = _parse_json_response(result)
    questions = _dedupe_questions(questions, set(q.lower().strip() for q in exclusions))[:question_count]
    if not questions:
        return JsonResponse({'error': 'Failed to parse fresh quiz questions from AI response'}, status=502)

    now = now_ms()
    quiz = StudyQuiz.objects.create(
        id=uuid_str(),
        document=doc,
        user_id=user_id,
        title=f"Quiz: {doc.title or doc.file_name or 'Untitled'}",
        question_count=len(questions),
        created_at=now,
    )

    for i, q in enumerate(questions):
        options = q.get('options', []) if isinstance(q, dict) else []
        StudyQuizQuestion.objects.create(
            id=uuid_str(),
            quiz=quiz,
            question_number=i + 1,
            question_text=(q.get('question', '') if isinstance(q, dict) else '').strip(),
            option_a=options[0] if len(options) > 0 else '',
            option_b=options[1] if len(options) > 1 else '',
            option_c=options[2] if len(options) > 2 else '',
            option_d=options[3] if len(options) > 3 else '',
            correct_answer=((q.get('correct', 'A') if isinstance(q, dict) else 'A') or 'A').upper()[:1],
            explanation=(q.get('explanation', '') if isinstance(q, dict) else '').strip(),
        )

    doc.updated_at = now
    doc.save(update_fields=['updated_at'])

    return JsonResponse({'quiz': _serialize_quiz_detail(quiz, user_id)}, status=201)


def ajax_study_quiz_detail(request, quiz_id):
    """Get quiz questions without correct answers."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        quiz = StudyQuiz.objects.select_related('document').get(pk=quiz_id)
    except StudyQuiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    if not _can_access_study_doc(quiz.document, user_id):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    return JsonResponse({'quiz': _serialize_quiz_detail(quiz, user_id)})


def ajax_study_quiz_submit(request, quiz_id):
    """Submit answers for a quiz and get score + XP."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        quiz = StudyQuiz.objects.select_related('document').get(pk=quiz_id)
    except StudyQuiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)
    if not _can_access_study_doc(quiz.document, user_id):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    body = _json_body(request)
    answers = body.get('answers', {})
    if not answers:
        return JsonResponse({'error': 'No answers provided'}, status=400)

    questions = list(quiz.questions.all().order_by('question_number'))
    score = 0
    results = {}

    for q in questions:
        user_answer = (answers.get(str(q.question_number), '') or '').upper()
        is_correct = user_answer == q.correct_answer
        if is_correct:
            score += 1
        results[str(q.question_number)] = {
            'userAnswer': user_answer,
            'correctAnswer': q.correct_answer,
            'isCorrect': is_correct,
            'explanation': q.explanation,
        }

    xp_earned = score * 10
    now = now_ms()
    attempt = StudyQuizAttempt.objects.create(
        id=uuid_str(),
        quiz=quiz,
        user_id=user_id,
        score=score,
        total_questions=len(questions),
        answers=json.dumps(answers),
        xp_earned=xp_earned,
        completed_at=now,
        created_at=now,
    )

    User.objects.filter(pk=user_id).update(contribution_score=F('contribution_score') + xp_earned)

    return JsonResponse({
        'attempt': {
            'id': attempt.id,
            'score': attempt.score,
            'totalQuestions': attempt.total_questions,
            'xpEarned': attempt.xp_earned,
            'results': results,
        }
    })


# ── Flashcards ─────────────────────────────────────────────────────────────


def ajax_study_generate_flashcards(request, doc_id):
    """Generate fresh flashcards from a document using Qwen."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error

    body = _json_body(request)
    card_count = _bounded_int(body.get('count', 15), 5, 50, 15)

    prepared = _prepare_doc_for_qwen(doc)
    if not prepared:
        return JsonResponse({'error': 'Could not read document content'}, status=502)

    exclusions = _flashcard_exclusions(doc)
    exclusion_text = _exclusion_block('Existing flashcards to avoid', exclusions)
    file_prompt = f"Create {card_count} NEW flashcards from this file.\n{exclusion_text}"
    text_prompt = f"Create {card_count} NEW flashcards from this document.\n{exclusion_text}"
    result, err = _send_doc_task(prepared, file_prompt, text_prompt, _FLASHCARD_SYSTEM_PROMPT.format(count=card_count))
    if err:
        return JsonResponse({'error': err}, status=502)

    cards = _parse_json_response(result)
    cards = _dedupe_flashcards(cards, set(c.lower().strip() for c in exclusions))[:card_count]
    if not cards:
        return JsonResponse({'error': 'Failed to parse fresh flashcards from AI response'}, status=502)

    now = now_ms()
    max_card_number = StudyFlashcard.objects.filter(document=doc).aggregate(m=Max('card_number')).get('m') or 0
    flashcard_objs = []
    for i, c in enumerate(cards):
        fc = StudyFlashcard.objects.create(
            id=uuid_str(),
            document=doc,
            user_id=user_id,
            front=(c.get('front', '') if isinstance(c, dict) else '').strip(),
            back=(c.get('back', '') if isinstance(c, dict) else '').strip(),
            card_number=max_card_number + i + 1,
            created_at=now,
        )
        flashcard_objs.append(fc)

    doc.updated_at = now
    doc.save(update_fields=['updated_at'])

    return JsonResponse({
        'flashcards': [_serialize_flashcard(fc, user_id) for fc in flashcard_objs],
        'totalFlashcards': StudyFlashcard.objects.filter(document=doc).count(),
    }, status=201)


def ajax_study_flashcard_review(request, card_id):
    """Mark a flashcard's confidence level."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        card = StudyFlashcard.objects.get(pk=card_id)
    except StudyFlashcard.DoesNotExist:
        return JsonResponse({'error': 'Flashcard not found'}, status=404)
    if not _can_access_study_doc(card.document, user_id):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    body = _json_body(request)
    confidence = body.get('confidence', 'medium')
    if confidence not in ('easy', 'medium', 'hard'):
        return JsonResponse({'error': 'Invalid confidence level'}, status=400)

    now = now_ms()
    intervals = {'easy': 7 * 86400000, 'medium': 2 * 86400000, 'hard': 30 * 60000}
    review, created = StudyFlashcardReview.objects.update_or_create(
        flashcard=card,
        user_id=user_id,
        defaults={
            'confidence': confidence,
            'review_count': 1,
            'last_reviewed_at': now,
            'next_review_at': now + intervals.get(confidence, 2 * 86400000),
        },
    )
    if not created:
        StudyFlashcardReview.objects.filter(pk=review.pk).update(review_count=F('review_count') + 1)
        review.review_count += 1

    return JsonResponse({
        'flashcardId': card.id,
        'confidence': confidence,
        'reviewCount': review.review_count,
        'nextReviewAt': review.next_review_at,
    })


# ── Serialization helpers ─────────────────────────────────────────────────


def _serialize_study_doc_list_item(d):
    compact = getattr(d, 'summary_compact', '') or d.summary
    detailed = getattr(d, 'summary_detailed', '')
    return {
        'id': d.id,
        'title': d.title or d.file_name or 'Untitled',
        'fileName': d.file_name,
        'fileSize': d.file_size,
        'status': d.status,
        'summaryGenerated': bool(compact or detailed),
        'mindmapGenerated': bool(getattr(d, 'mindmap_json', '')),
        'quizCount': d.quizzes.count(),
        'flashcardCount': d.flashcards.count(),
        'createdAt': d.created_at,
        'updatedAt': d.updated_at,
        'shareMode': getattr(d, 'share_mode', StudyDocument.SHARE_PRIVATE),
        'sharedAt': getattr(d, 'shared_at', 0),
    }


def _serialize_study_doc_detail(d):
    compact = getattr(d, 'summary_compact', '') or d.summary
    detailed = getattr(d, 'summary_detailed', '')
    return {
        'id': d.id,
        'title': d.title or d.file_name or 'Untitled',
        'fileName': d.file_name,
        'fileSize': d.file_size,
        'mimeType': d.mime_type,
        'status': d.status,
        'summary': compact,
        'summaryCompact': compact,
        'summaryDetailed': detailed,
        'summaryGenerated': bool(compact or detailed),
        'mindmapGenerated': bool(getattr(d, 'mindmap_json', '')),
        'createdAt': d.created_at,
        'updatedAt': d.updated_at,
        'shareMode': getattr(d, 'share_mode', StudyDocument.SHARE_PRIVATE),
        'sharedAt': getattr(d, 'shared_at', 0),
        'shareToken': str(getattr(d, 'share_token', '') or ''),
    }


def _serialize_quiz_list_item(q, user_id):
    attempts = q.attempts.filter(user_id=user_id)
    return {
        'id': q.id,
        'title': q.title,
        'questionCount': q.question_count,
        'attemptCount': attempts.count(),
        'bestScore': max((a.score for a in attempts), default=0),
        'createdAt': q.created_at,
    }


def _serialize_quiz_detail(quiz, viewer_user_id=None):
    viewer_user_id = viewer_user_id or quiz.user_id
    previous_attempts = quiz.attempts.filter(user_id=viewer_user_id).order_by('-completed_at')
    questions = quiz.questions.all().order_by('question_number')
    return {
        'id': quiz.id,
        'title': quiz.title,
        'questionCount': quiz.question_count,
        'createdAt': quiz.created_at,
        'attemptCount': previous_attempts.count(),
        'bestScore': max((a.score for a in previous_attempts), default=0),
        'questions': [
            {
                'id': q.id,
                'number': q.question_number,
                'question': q.question_text,
                'optionA': q.option_a,
                'optionB': q.option_b,
                'optionC': q.option_c,
                'optionD': q.option_d,
            }
            for q in questions
        ],
    }


def _serialize_flashcard(fc, user_id):
    review = fc.reviews.filter(user_id=user_id).first()
    return {
        'id': fc.id,
        'front': fc.front,
        'back': fc.back,
        'cardNumber': fc.card_number,
        'confidence': review.confidence if review else 'new',
    }


# ── Data and parsing helpers ───────────────────────────────────────────────


def _owned_doc(doc_id, user_id):
    try:
        doc = StudyDocument.objects.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        return None, JsonResponse({'error': 'Document not found'}, status=404)
    if doc.user_id != user_id:
        return None, JsonResponse({'error': 'Forbidden'}, status=403)
    return doc, None



def _accessible_doc(doc_id, user_id):
    try:
        doc = StudyDocument.objects.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        return None, JsonResponse({'error': 'Document not found'}, status=404)
    if not _can_access_study_doc(doc, user_id):
        return None, JsonResponse({'error': 'Forbidden'}, status=403)
    return doc, None


def _can_access_shared_doc(doc, user_id):
    if doc.user_id == user_id:
        return True
    if getattr(doc, 'share_mode', StudyDocument.SHARE_PRIVATE) == StudyDocument.SHARE_LINK and getattr(doc, 'shared_at', 0):
        return True
    if getattr(doc, 'share_mode', StudyDocument.SHARE_PRIVATE) == StudyDocument.SHARE_SPECIFIC and getattr(doc, 'shared_at', 0):
        return StudyDocumentShare.objects.filter(document=doc, user_id=user_id).exists()
    return False


def _can_access_study_doc(doc, user_id):
    return _can_access_shared_doc(doc, user_id)


def _resolve_share_users(raw, owner_id):
    if isinstance(raw, list):
        parts = raw
    else:
        parts = re.split(r'[\s,;]+', str(raw or ''))
    identifiers = []
    for part in parts:
        ident = str(part or '').strip()
        if ident.startswith('@'):
            ident = ident[1:]
        if ident and ident not in identifiers:
            identifiers.append(ident)
    resolved = []
    missing = []
    for ident in identifiers[:50]:
        user = User.objects.filter(Q(username__iexact=ident) | Q(email__iexact=ident)).first()
        if not user or user.id == owner_id:
            if ident:
                missing.append(ident)
            continue
        resolved.append(user)
    return resolved, missing


def _serialize_share_settings(doc, request):
    grants = doc.share_grants.select_related('user').order_by('user__username')
    link = request.build_absolute_uri(reverse('web:study_lab_shared', args=[doc.share_token]))
    return {
        'mode': getattr(doc, 'share_mode', StudyDocument.SHARE_PRIVATE),
        'shareUrl': link,
        'sharedAt': getattr(doc, 'shared_at', 0),
        'users': [
            {
                'id': g.user_id,
                'username': g.user.username,
                'displayName': g.user.display_name or g.user.username,
                'photoUrl': g.user.photo_url or '',
            }
            for g in grants
        ],
    }

def _json_body(request):
    try:
        return json.loads(request.body) if request.body else {}
    except ValueError:
        return {}


def _bounded_int(value, low, high, default):
    try:
        n = int(value)
    except (ValueError, TypeError):
        n = default
    return min(max(n, low), high)


def _summary_mode(mode):
    return 'detailed' if mode == 'detailed' else 'compact'


def _save_summary(doc, mode, summary):
    now = now_ms()
    if mode == 'detailed':
        doc.summary_detailed = summary
    else:
        doc.summary_compact = summary
        doc.summary = summary  # backward compatibility for old reads/templates
    doc.summary_updated_at = now
    doc.summary_generated_at = now
    doc.updated_at = now
    fields = ['summary_updated_at', 'summary_generated_at', 'updated_at']
    if mode == 'detailed':
        fields.append('summary_detailed')
    else:
        fields.extend(['summary_compact', 'summary'])
    doc.save(update_fields=fields)


def _clean_ai_markdown(text):
    """Remove common AI preambles and code fences while preserving markdown."""
    if not text:
        return ''
    cleaned = text.strip()
    if cleaned.startswith('```'):
        cleaned = re.sub(r'^```[a-zA-Z0-9_-]*\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned).strip()
    preamble_re = re.compile(
        r"^(?:\s*(?:sure[,!\s]*)?)?(?:#+\s*)?(?:here(?:'s| is)|below is|this is|i have prepared|i've prepared)\b[^\n]{0,240}\n+",
        re.IGNORECASE,
    )
    for _ in range(3):
        new = preamble_re.sub('', cleaned).strip()
        if new == cleaned:
            break
        cleaned = new
    return cleaned


def _prepare_doc_for_qwen(doc):
    """Read document and return Qwen context for file upload or extracted text."""
    if not doc.file_url:
        return None

    try:
        from django.core.files.storage import default_storage
        file_path = doc.file_url
        if file_path.startswith('/media/'):
            file_path = file_path[len('/media/'):]
        elif file_path.startswith('/'):
            file_path = file_path.lstrip('/')
        if not default_storage.exists(file_path):
            return None
        with default_storage.open(file_path, 'rb') as f:
            file_data = f.read()
    except Exception as e:
        logger.warning('Failed to read study document: %s', e)
        return None

    ext = os.path.splitext(doc.file_name)[1].lower()

    if ext == '.txt':
        try:
            text = file_data.decode('utf-8')
            if text.strip():
                return {'is_image': False, 'has_file': False, 'uploaded_files': None, 'text_content': text[:MAX_TEXT_CHARS]}
        except UnicodeDecodeError:
            pass

    if ext in ALLOWED_EXTENSIONS:
        try:
            qwen_session = _new_qwen_session()
            req_headers = dict(qwen_session.headers)
            file_obj = upload_file_from_bytes(doc.file_name, file_data, qwen_session, req_headers)
            if file_obj:
                is_image = ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg')
                return {'is_image': is_image, 'has_file': True, 'uploaded_files': [file_obj], 'text_content': None}
        except Exception as e:
            logger.warning('Qwen upload failed for %s: %s', doc.file_name, e)
            return None

    logger.warning('Could not extract content from %s', doc.file_name)
    return None


def _parse_json_response(text):
    """Extract a JSON array from Qwen's response text."""
    if not text:
        return []
    stripped = _strip_code_fence(text)
    try:
        parsed = json.loads(stripped)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        match = re.search(r'\[.*\]', stripped, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                pass
    logger.warning('Failed to parse Qwen JSON array response: %s...', text[:200])
    return []


def _parse_json_object_response(text):
    """Extract a JSON object from Qwen's response text."""
    if not text:
        return None
    stripped = _strip_code_fence(text)
    try:
        parsed = json.loads(stripped)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', stripped, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
                return parsed if isinstance(parsed, dict) else None
            except json.JSONDecodeError:
                pass
    logger.warning('Failed to parse Qwen JSON object response: %s...', text[:200])
    return None


def _strip_code_fence(text):
    stripped = (text or '').strip()
    if stripped.startswith('```'):
        stripped = re.sub(r'^```[a-zA-Z0-9_-]*\s*', '', stripped)
        stripped = re.sub(r'\s*```$', '', stripped).strip()
    return stripped


def _quiz_exclusions(doc):
    qs = StudyQuizQuestion.objects.filter(quiz__document=doc).order_by('-quiz__created_at')[:120]
    return [q.question_text.strip() for q in qs if q.question_text.strip()]


def _flashcard_exclusions(doc):
    cards = StudyFlashcard.objects.filter(document=doc).order_by('-created_at')[:160]
    return [f"{c.front.strip()} — {c.back.strip()}" for c in cards if c.front.strip() or c.back.strip()]


def _exclusion_block(title, items):
    if not items:
        return f"{title}: none yet."
    text = '\n'.join(f"- {item}" for item in items)
    if len(text) > MAX_EXCLUSION_CHARS:
        text = text[:MAX_EXCLUSION_CHARS] + '\n- ...'
    return f"{title}:\n{text}"


def _dedupe_questions(items, existing_normalized):
    seen = set(existing_normalized)
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        q = (item.get('question') or '').strip()
        options = item.get('options') or []
        if not q or len(options) < 4:
            continue
        key = q.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _dedupe_flashcards(items, existing_normalized):
    seen = set(existing_normalized)
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        front = (item.get('front') or '').strip()
        back = (item.get('back') or '').strip()
        if not front or not back:
            continue
        key = f'{front} — {back}'.lower()
        if key in seen or front.lower() in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _mindmap_value(doc):
    raw = getattr(doc, 'mindmap_json', '') or ''
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
        return _normalize_mindmap(parsed, doc)
    except (TypeError, ValueError):
        return None


def _normalize_mindmap(mindmap, doc):
    if not isinstance(mindmap, dict):
        mindmap = {}
    title = str(mindmap.get('title') or doc.title or doc.file_name or 'Mindmap').strip()
    nodes = mindmap.get('nodes')
    if not isinstance(nodes, list):
        nodes = []
    return {'title': title, 'nodes': [_normalize_node(n) for n in nodes if isinstance(n, dict)][:10]}


def _normalize_node(node):
    title = str(node.get('title') or node.get('name') or '').strip()[:140]
    note = str(node.get('note') or node.get('description') or '').strip()[:280]
    children = node.get('children') if isinstance(node.get('children'), list) else []
    return {
        'title': title or 'Topic',
        'note': note,
        'children': [_normalize_node(child) for child in children if isinstance(child, dict)][:8],
    }
