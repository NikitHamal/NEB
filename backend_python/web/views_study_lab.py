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
import secrets
import string
from collections import Counter

from django.core.cache import cache
from django.db import connection, transaction
from django.db.models import Avg, Count, F, Max, Q, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .view_helpers import *  # noqa: F401,F403
from api.models import (
    Bookmark,
    Follow,
    GenerationJob,
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
    StudySpace,
    StudySpaceShare,
    StudySpaceMember,
    StudySpaceNote,
    StudySpacePresence,
    StudySpaceQuiz,
    StudySpaceQuizQuestion,
    StudySpaceQuizAttempt,
    StudySpaceFlashcard,
    StudySpaceFlashcardReview,
    SocialLinkClick,
)
from api.utils import now_ms, uuid_str
from api.generation import enqueue, serialize_job, get_job, mark_processing, mark_completed, mark_failed
from api.generation_executors import EXECUTORS
from api.qwen_utils.client import QwenClient
from api.qwen_utils.file_upload import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from api.qwen_utils.text_extraction import extract_text_from_file, MAX_TEXT_CHARS as QWEN_MAX_TEXT_CHARS
from api.qwen_utils.prompts import (
    summary_system_prompt, quiz_system_prompt, flashcard_system_prompt,
    MINDMAP_SYSTEM_PROMPT, TUTOR_SYSTEM_PROMPT, PLANNER_SYSTEM_PROMPT,
    summary_outline_prompt, summary_full_prompt,
    MINDMAP_OUTLINE_PROMPT, MINDMAP_FULL_PROMPT,
    quiz_outline_prompt, quiz_full_prompt,
    flashcard_outline_prompt, flashcard_full_prompt,
    exclusion_block,
)
from api.qwen_utils.parsing import (
    clean_ai_markdown, normalize_formulas, parse_json_response,
    parse_json_object_response, dedupe_questions, dedupe_flashcards,
)
from api.qwen_utils.doc_parser import start_parse, reparse as doc_reparse, get_parse_status, PARSE_STATUS_READY, PARSE_STATUS_FAILED
from api.realtime import broadcast_note_content

logger = logging.getLogger(__name__)

MAX_TEXT_CHARS = 50000
PRESENCE_STALE_MS = 90000
ROLE_RANK = {
    StudySpaceMember.ROLE_MEMBER: 1,
    StudySpaceMember.ROLE_MODERATOR: 2,
    StudySpaceMember.ROLE_ADMIN: 3,
    StudySpaceMember.ROLE_OWNER: 4,
}


def _role_rank(role):
    return ROLE_RANK.get((role or '').lower(), 0)


def _space_permission_allows(space, user_id, minimum_role_attr):
    role = _space_membership_role(space, user_id)
    if not role and space.user_id == user_id:
        role = StudySpaceMember.ROLE_OWNER
    required = getattr(space, minimum_role_attr, StudySpaceMember.ROLE_OWNER) or StudySpaceMember.ROLE_OWNER
    return _role_rank(role) >= _role_rank(required)


def _ensure_space_note(space):
    note = StudySpaceNote.objects.filter(space=space).select_related('updated_by').first()
    if note:
        return note
    now = now_ms()
    return StudySpaceNote.objects.create(
        id=uuid_str(),
        space=space,
        content='',
        updated_by_id=space.user_id,
        version=1,
        created_at=now,
        updated_at=now,
    )


def _prune_space_presence(space):
    cutoff = now_ms() - PRESENCE_STALE_MS
    StudySpacePresence.objects.filter(space=space, last_seen_at__lt=cutoff).delete()


def _serialize_presence_row(row):
    user = row.user
    return {
        'id': user.id,
        'username': user.username,
        'displayName': user.display_name or user.username,
        'photoUrl': user.photo_url or getattr(user, 'profile_photo_url', '') or '',
        'role': _space_membership_role(row.space, user.id),
        'status': row.status,
        'currentTab': row.current_tab,
        'currentDocumentId': row.current_document_id,
        'detail': row.detail,
        'isTyping': bool(row.is_typing),
        'lastSeenAt': row.last_seen_at,
    }


def _space_analytics(space):
    member_count = StudySpaceMember.objects.filter(space=space).count()
    active_now = StudySpacePresence.objects.filter(space=space).count()
    quiz_count = StudySpaceQuiz.objects.filter(space=space).count()
    attempt_stats = StudySpaceQuizAttempt.objects.filter(quiz__space=space).aggregate(
        avg_score=Avg('score'),
        avg_total=Avg('total_questions'),
    )
    avg_score = attempt_stats.get('avg_score') or 0
    avg_total = attempt_stats.get('avg_total') or 0
    completion_pct = round((avg_score / avg_total) * 100, 1) if avg_total else 0
    reviews_count = StudySpaceFlashcardReview.objects.filter(flashcard__space=space).count()
    due_count = StudySpaceFlashcardReview.objects.filter(flashcard__space=space, next_review_at__lte=now_ms()).count()
    return {
        'memberCount': member_count,
        'activeNow': active_now,
        'docCount': space.documents.count(),
        'quizCount': quiz_count,
        'attemptCount': StudySpaceQuizAttempt.objects.filter(quiz__space=space).count(),
        'avgQuizCompletion': completion_pct,
        'flashcardCount': StudySpaceFlashcard.objects.filter(space=space).count(),
        'reviewsCount': reviews_count,
        'dueFlashcards': due_count,
        'resourceViews': space.documents.count() * max(member_count, 1),
        'revisionStreakHint': due_count == 0 and reviews_count > 0,
    }


# ── Qwen client ────────────────────────────────────────────────────────────

def _qwen():
    return QwenClient()


# ── Rate limiting ──────────────────────────────────────────────────────────

# (scope, limit, window_seconds)
THROTTLE_GENERATE = ('generate', 10, 600)   # AI generation: 10 per 10 minutes
THROTTLE_TUTOR = ('tutor', 20, 600)         # AI tutor: 20 per 10 minutes
THROTTLE_UPLOAD = ('upload', 20, 3600)      # File uploads: 20 per hour


def _throttle(request, scope, limit, window_seconds):
    """Cache-based fixed-window rate limiter keyed on the authenticated user id.

    Returns an error JsonResponse (HTTP 429) if the rate limit is exceeded,
    else None. Uses cache.add() to atomically create the window counter and
    cache.incr() afterwards, so concurrent requests cannot reset the window.
    """
    user_id = _get_user_id(request)
    if not user_id:
        return None
    key = f'throttle:study_lab:{scope}:{user_id}'
    try:
        if cache.add(key, 1, timeout=window_seconds):
            count = 1
        else:
            try:
                count = cache.incr(key)
            except ValueError:
                # Key expired between add() and incr() — start a new window.
                cache.add(key, 1, timeout=window_seconds)
                count = 1
    except Exception:
        logger.exception('Rate limit cache failure for %s', key)
        return None
    if count > limit:
        return JsonResponse({'error': 'Too many requests. Please wait a moment.'}, status=429)
    return None


def _throttled(request, rule):
    scope, limit, window_seconds = rule
    return _throttle(request, scope, limit, window_seconds)


# ── Page views ─────────────────────────────────────────────────────────────


def study_lab(request):
    """Study Lab landing page. Shows spaces for authenticated users."""
    user_id = _get_user_id(request)
    if not user_id:
        ctx = _ctx(request, page='study_lab')
        return render(request, 'web/study_lab.html', ctx)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        ctx = _ctx(request, page='study_lab')
        return render(request, 'web/study_lab.html', ctx)

    spaces = list(
        StudySpace.objects.filter(user=user)
        .select_related('user')
        .annotate(
            member_count_agg=Count('members', distinct=True),
            doc_count_agg=Count('documents', distinct=True),
        )
        .order_by('-updated_at')[:MAX_SPACES_PER_USER]
    )
    for space in spaces:
        _ensure_space_owner_member(space)
        _ensure_space_invite_code(space)
    space_list = [
        _serialize_space_list_item(s, member_count=s.member_count_agg, doc_count=s.doc_count_agg)
        for s in spaces
    ]

    unassigned_docs = StudyDocument.objects.filter(user=user, space__isnull=True).order_by('-updated_at')[:20]
    doc_list = [_serialize_study_doc_list_item(d) for d in unassigned_docs]

    public_spaces = (
        StudySpace.objects.filter(visibility=StudySpace.VISIBILITY_PUBLIC)
        .exclude(user=user)
        .select_related('user')
        .annotate(
            member_count_agg=Count('members', distinct=True),
            doc_count_agg=Count('documents', distinct=True),
        )
        .order_by('-updated_at')[:12]
    )
    ctx = _ctx(
        request,
        spaces=space_list,
        public_spaces=[
            _serialize_space_list_item(s, user_id, member_count=s.member_count_agg, doc_count=s.doc_count_agg)
            for s in public_spaces
        ],
        documents=doc_list,
        page='study_lab',
    )
    return render(request, 'web/study_lab.html', ctx)



def study_lab_shared(request, token):
    """Backward-compatible Study Lab share route.

    Study Lab documents now live inside Study Spaces. A legacy document share
    token is migrated lazily into a one-document Study Space and then routed to
    the Study Space invite flow instead of crashing on removed document fields.
    """
    user_id = _get_user_id(request)
    if not user_id:
        return redirect(f"{reverse('web:login')}?next={request.path}")

    space = _migrate_legacy_shared_doc_to_space(token, user_id)
    if not space:
        raise Http404('Shared study space not found')
    return redirect('web:study_space_shared', token=space.share_token)


# ── Study Space page views ───────────────────────────────────────────────────


def study_space_page(request, space_id):
    """Fullscreen study space workspace page."""
    user_id = _get_user_id(request)
    if not user_id:
        return redirect(f"{reverse('web:login')}?next={request.path}")

    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err

    space_data = _serialize_space_detail(space, user_id)
    ctx = _ctx(request, space=space_data, space_id=space_id, page='study_space')
    return render(request, 'web/study_space.html', ctx)


def study_space_shared(request, token):
    """Open a Study Space invite link. Signed-in users see a join prompt."""
    user_id = _get_user_id(request)
    if not user_id:
        return redirect(f"{reverse('web:login')}?next={request.path}")

    try:
        space = StudySpace.objects.select_related('user').get(share_token=token)
    except StudySpace.DoesNotExist:
        raise Http404('Shared space not found')

    if not _space_can_be_joined_by_link(space, user_id):
        return render(request, 'web/study_lab_shared_denied.html', _ctx(request, page='study_lab'), status=403)

    # Remember that this session presented the valid share token. Link-share
    # access checks in _accessible_space() require this session marker so a
    # bare space id can never be used to read an unlisted link-shared space.
    request.session[f'space_token_{space.id}'] = space.share_token

    if _space_membership_role(space, user_id) or space.user_id == user_id:
        return redirect('web:study_space_page', space_id=space.id)

    _ensure_space_invite_code(space)
    owner = space.user
    ctx = _ctx(
        request,
        space=_serialize_space_list_item(space, user_id),
        owner={
            'username': owner.username,
            'displayName': owner.display_name or owner.username,
            'photoUrl': owner.photo_url or getattr(owner, 'profile_photo_url', '') or '',
        },
        join_url=reverse('web:ajax_space_join_shared', args=[token]),
        page='study_space',
    )
    return render(request, 'web/study_space_join.html', ctx)


# ── Study Space AJAX endpoints ──────────────────────────────────────────────


def ajax_space_list(request):
    """List the authenticated user's study spaces."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    spaces = (
        StudySpace.objects.filter(user_id=user_id)
        .select_related('user')
        .annotate(
            member_count_agg=Count('members', distinct=True),
            doc_count_agg=Count('documents', distinct=True),
        )
        .order_by('-updated_at')[:50]
    )
    return JsonResponse({'spaces': [
        _serialize_space_list_item(s, user_id, member_count=s.member_count_agg, doc_count=s.doc_count_agg)
        for s in spaces
    ]})


def ajax_space_create(request):
    """Create a new study space. Max 5 per user."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    existing = StudySpace.objects.filter(user_id=user_id).count()
    if existing >= MAX_SPACES_PER_USER:
        return JsonResponse({'error': f'You can have at most {MAX_SPACES_PER_USER} study spaces'}, status=400)

    body = _json_body(request)
    title = (body.get('title') or '').strip()[:200]
    description = (body.get('description') or '').strip()[:2000]

    now = now_ms()
    space = StudySpace.objects.create(
        id=uuid_str(),
        user_id=user_id,
        title=title,
        description=description,
        share_token=uuid_str(),
        invite_code=_generate_unique_invite_code(),
        created_at=now,
        updated_at=now,
    )
    _ensure_space_owner_member(space)
    return JsonResponse(_serialize_space_detail(space, user_id), status=201)


def ajax_space_public_list(request):
    """List public Study Spaces for discovery with simple search and filters."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    q = (request.GET.get('q') or '').strip()
    level = (request.GET.get('level') or '').strip()
    subject = (request.GET.get('subject') or '').strip()
    exam = (request.GET.get('exam') or '').strip()
    sort = (request.GET.get('sort') or 'recent').strip()

    spaces = (
        StudySpace.objects.filter(visibility=StudySpace.VISIBILITY_PUBLIC)
        .select_related('user')
        .annotate(
            member_count_agg=Count('members', distinct=True),
            doc_count_agg=Count('documents', distinct=True),
        )
    )
    if q:
        spaces = spaces.filter(title__icontains=q)
    if level:
        spaces = spaces.filter(study_level__icontains=level)
    if subject:
        spaces = spaces.filter(subject__icontains=subject)
    if exam:
        spaces = spaces.filter(exam__icontains=exam)

    if sort == 'members':
        rows = list(spaces.order_by('-member_count_agg', '-updated_at')[:60])
    else:
        rows = list(spaces.order_by('-updated_at')[:60])
    return JsonResponse({'spaces': [
        _serialize_space_list_item(s, user_id, member_count=s.member_count_agg, doc_count=s.doc_count_agg)
        for s in rows
    ]})


def ajax_space_join_code(request):
    """Join a Study Space by invite code."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    code = str(_json_body(request).get('code') or '').strip().upper()
    if not code:
        return JsonResponse({'error': 'Invite code is required'}, status=400)

    try:
        space = StudySpace.objects.get(invite_code=code)
    except StudySpace.DoesNotExist:
        return JsonResponse({'error': 'No study space found for that invite code'}, status=404)

    if not getattr(space, 'allow_join_by_code', True):
        return JsonResponse({'error': 'This invite code is not accepting new members'}, status=403)

    _join_space(space, user_id, invited_by_id=space.user_id)
    return JsonResponse({'success': True, 'space': _serialize_space_detail(space, user_id), 'redirectUrl': reverse('web:study_space_page', args=[space.id])})


def ajax_space_join_shared(request, token):
    """Join a Study Space from its invite/share link."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        space = StudySpace.objects.get(share_token=token)
    except StudySpace.DoesNotExist:
        return JsonResponse({'error': 'Study space not found'}, status=404)

    if not _space_can_be_joined_by_link(space, user_id):
        return JsonResponse({'error': 'This invite link is not active'}, status=403)

    _join_space(space, user_id, invited_by_id=space.user_id)
    return JsonResponse({'success': True, 'spaceId': space.id, 'redirectUrl': reverse('web:study_space_page', args=[space.id])})


def ajax_space_detail(request, space_id):
    """Get full detail of a study space."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err

    return JsonResponse(_serialize_space_detail(space, user_id))


def ajax_space_update(request, space_id):
    """Update a study space's title or description. Owner only."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    space, err = _manageable_space(space_id, user_id)
    if err:
        return err

    body = _json_body(request)
    if 'title' in body:
        space.title = (body['title'] or '').strip()[:200]
    if 'description' in body:
        space.description = (body['description'] or '').strip()[:2000]
    space.updated_at = now_ms()
    space.save(update_fields=['title', 'description', 'updated_at'])

    return JsonResponse(_serialize_space_detail(space, user_id))


def ajax_space_delete(request, space_id):
    """Delete a study space. Owner only."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    space, err = _owned_space(space_id, user_id)
    if err:
        return err

    space.delete()
    return JsonResponse({'success': True})


def ajax_space_share(request, space_id):
    """Update share settings for a study space. Owner only."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    space, err = _manageable_space(space_id, user_id)
    if err:
        return err

    body = _json_body(request)
    mode = body.get('mode', '').strip()
    visibility = body.get('visibility', '').strip() or getattr(space, 'visibility', StudySpace.VISIBILITY_PRIVATE)
    allow_join_by_code = bool(body.get('allowJoinByCode', getattr(space, 'allow_join_by_code', True)))

    if mode not in (StudySpace.SHARE_PRIVATE, StudySpace.SHARE_LINK, StudySpace.SHARE_SPECIFIC):
        return JsonResponse({'error': 'Invalid share mode'}, status=400)
    if visibility not in (StudySpace.VISIBILITY_PRIVATE, StudySpace.VISIBILITY_UNLISTED, StudySpace.VISIBILITY_PUBLIC):
        return JsonResponse({'error': 'Invalid visibility'}, status=400)

    with transaction.atomic():
        _ensure_space_invite_code(space)
        space.share_mode = mode
        space.visibility = visibility
        space.allow_join_by_code = allow_join_by_code
        if mode != StudySpace.SHARE_PRIVATE or visibility == StudySpace.VISIBILITY_PUBLIC:
            space.shared_at = now_ms()
        else:
            space.shared_at = 0
            StudySpaceShare.objects.filter(space=space).delete()

        if mode == StudySpace.SHARE_SPECIFIC:
            raw_users = body.get('users', [])
            resolved, missing = _resolve_share_users(raw_users, user_id)
            existing_ids = set(
                StudySpaceShare.objects.filter(space=space).values_list('user_id', flat=True)
            )
            new_grants = [
                StudySpaceShare(
                    id=uuid_str(),
                    space=space,
                    user_id=user.id,
                    granted_by_id=user_id,
                    created_at=now_ms(),
                )
                for user in resolved if user.id not in existing_ids
            ]
            if new_grants:
                StudySpaceShare.objects.bulk_create(new_grants)
            resolved_set = {u.id for u in resolved}
            StudySpaceShare.objects.filter(space=space).exclude(user_id__in=resolved_set).delete()
        else:
            missing = []

        space.updated_at = now_ms()
        space.save(update_fields=['share_mode', 'visibility', 'allow_join_by_code', 'shared_at', 'updated_at', 'invite_code'])

    data = _serialize_space_detail(space, user_id)
    if missing:
        data['missingUsers'] = missing
    return JsonResponse(data)


def ajax_space_member_role(request, space_id, member_user_id):
    """Assign admin/moderator/member role. Owner only for safety."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    space, err = _owned_space(space_id, user_id)
    if err:
        return err
    if member_user_id == space.user_id:
        return JsonResponse({'error': 'The creator must remain owner'}, status=400)

    role = str(_json_body(request).get('role') or '').strip().lower()
    if role not in (StudySpaceMember.ROLE_ADMIN, StudySpaceMember.ROLE_MODERATOR, StudySpaceMember.ROLE_MEMBER):
        return JsonResponse({'error': 'Invalid member role'}, status=400)

    try:
        member = StudySpaceMember.objects.select_related('user').get(space=space, user_id=member_user_id)
    except StudySpaceMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)

    member.role = role
    member.updated_at = now_ms()
    member.save(update_fields=['role', 'updated_at'])
    return JsonResponse({'success': True, 'member': _serialize_space_member(member), 'space': _serialize_space_detail(space, user_id)})


def ajax_space_member_remove(request, space_id, member_user_id):
    """Remove a non-owner member from the space. Admins can remove members; only owner can remove admins/moderators."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    space, err = _manageable_space(space_id, user_id)
    if err:
        return err
    if member_user_id == space.user_id:
        return JsonResponse({'error': 'The creator cannot be removed'}, status=400)

    try:
        member = StudySpaceMember.objects.get(space=space, user_id=member_user_id)
    except StudySpaceMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)

    if member.role in (StudySpaceMember.ROLE_ADMIN, StudySpaceMember.ROLE_MODERATOR) and space.user_id != user_id:
        return JsonResponse({'error': 'Only the creator can remove admins or moderators'}, status=403)

    member.delete()
    return JsonResponse({'success': True, 'space': _serialize_space_detail(space, user_id)})



def ajax_space_settings(request, space_id):
    """Update space metadata and permission thresholds."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    space, err = _manageable_space(space_id, user_id)
    if err:
        return err

    body = _json_body(request)
    allowed_roles = {StudySpaceMember.ROLE_OWNER, StudySpaceMember.ROLE_ADMIN, StudySpaceMember.ROLE_MODERATOR, StudySpaceMember.ROLE_MEMBER}
    text_fields = {
        'title': 200,
        'description': 2000,
        'study_level': 80,
        'subject': 120,
        'exam': 120,
    }
    for key, limit in text_fields.items():
        if key in body:
            setattr(space, key, str(body.get(key) or '').strip()[:limit])

    permission_fields = ['generate_min_role', 'upload_min_role', 'invite_min_role', 'moderate_min_role', 'publish_min_role']
    for key in permission_fields:
        value = str(body.get(key) or '').strip().lower()
        if value in allowed_roles:
            setattr(space, key, value)

    visibility = str(body.get('visibility') or '').strip()
    if visibility in (StudySpace.VISIBILITY_PRIVATE, StudySpace.VISIBILITY_UNLISTED, StudySpace.VISIBILITY_PUBLIC):
        if visibility == StudySpace.VISIBILITY_PUBLIC and not _space_permission_allows(space, user_id, 'publish_min_role'):
            return JsonResponse({'error': 'You do not have permission to publish this space publicly'}, status=403)
        space.visibility = visibility

    space.updated_at = now_ms()
    space.save(update_fields=['title', 'description', 'study_level', 'subject', 'exam', 'generate_min_role', 'upload_min_role', 'invite_min_role', 'moderate_min_role', 'publish_min_role', 'visibility', 'updated_at'])
    return JsonResponse(_serialize_space_detail(space, user_id))


def ajax_space_presence(request, space_id):
    """Heartbeat endpoint for near-real-time StudySpace presence."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err

    _ensure_space_owner_member(space)
    _prune_space_presence(space)
    now = now_ms()

    if request.method == 'POST':
        body = _json_body(request)
        status = str(body.get('status') or StudySpacePresence.STATUS_INSIDE).strip().lower()
        if status not in dict(StudySpacePresence.STATUS_CHOICES):
            status = StudySpacePresence.STATUS_INSIDE
        current_tab = str(body.get('currentTab') or '')[:40]
        current_document_id = str(body.get('currentDocumentId') or '')[:36]
        detail = str(body.get('detail') or '')[:120]
        is_typing = bool(body.get('isTyping'))
        session_id = str(body.get('sessionId') or '')[:64]
        presence, created = StudySpacePresence.objects.get_or_create(
            space=space,
            user_id=user_id,
            defaults={
                'id': uuid_str(),
                'status': status,
                'current_tab': current_tab,
                'current_document_id': current_document_id,
                'detail': detail,
                'is_typing': is_typing,
                'session_id': session_id,
                'last_seen_at': now,
                'updated_at': now,
            }
        )
        if not created:
            presence.status = status
            presence.current_tab = current_tab
            presence.current_document_id = current_document_id
            presence.detail = detail
            presence.is_typing = is_typing
            presence.session_id = session_id
            presence.last_seen_at = now
            presence.updated_at = now
            presence.save(update_fields=['status','current_tab','current_document_id','detail','is_typing','session_id','last_seen_at','updated_at'])

    rows = StudySpacePresence.objects.filter(space=space).select_related('user').order_by('-last_seen_at')[:40]
    return JsonResponse({
        'presence': [_serialize_presence_row(r) for r in rows],
        'activeNow': len(rows),
    })


def ajax_space_notes(request, space_id):
    """Shared collaborative notes for a StudySpace with autosave."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err

    note = _ensure_space_note(space)
    if request.method == 'POST':
        if not _space_permission_allows(space, user_id, 'generate_min_role'):
            return JsonResponse({'error': 'You do not have permission to edit collaborative notes'}, status=403)
        body = _json_body(request)
        content = str(body.get('content') or '')
        if len(content) > 2000000:
            return JsonResponse({'error': 'Note is too long'}, status=400)
        note.content = content
        note.updated_by_id = user_id
        note.version = int(note.version or 0) + 1
        note.updated_at = now_ms()
        note.save(update_fields=['content', 'updated_by_id', 'version', 'updated_at'])
        broadcast_note_content(space.id, content, note.version, user_id)
    updater = note.updated_by
    return JsonResponse({
        'note': {
            'id': note.id,
            'content': note.content,
            'version': note.version,
            'updatedAt': note.updated_at,
            'updatedBy': {
                'id': updater.id,
                'username': updater.username,
                'displayName': updater.display_name or updater.username,
            } if updater else None,
        }
    })


def ajax_space_tutor(request, space_id):
    """Ask an AI tutor grounded in the space documents and cite document titles."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    throttled = _throttled(request, THROTTLE_TUTOR)
    if throttled:
        return throttled

    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err
    if not _space_permission_allows(space, user_id, 'generate_min_role'):
        return JsonResponse({'error': 'You do not have permission to use the AI tutor here'}, status=403)

    question = str(_json_body(request).get('question') or '').strip()
    if not question:
        return JsonResponse({'error': 'Question is required'}, status=400)

    texts, _parsing, _failed = _get_space_texts(space)
    if not texts:
        if _parsing:
            return JsonResponse({'error': 'Documents are still being parsed. Please wait a moment and try again.', 'parseStatus': 'parsing'}, status=202)
        if _failed:
            return JsonResponse({'error': 'Some documents failed to parse. Try re-uploading them or click retry.', 'parseStatus': 'failed'}, status=422)
        return JsonResponse({'error': 'No readable documents in this space'}, status=400)

    chunks = []
    citations = []
    total = 0
    for t in texts:
        excerpt = t['content'][:3000]
        total += len(excerpt)
        if total > MAX_TEXT_CHARS:
            break
        chunks.append(f"=== SOURCE: {t['title']} ===\n{excerpt}")
        citations.append({'title': t['title']})
    prompt = (
        "Answer the learner's question using ONLY the provided sources. "
        "Be clear and helpful. At the end, include a short section titled 'Citations' "
        "listing the source titles you used.\n\n"
        f"Question: {question}\n\n--- SOURCES ---\n" + "\n\n".join(chunks) + "\n--- END ---"
    )
    result, err = _qwen().simple_chat(prompt, system_prompt=TUTOR_SYSTEM_PROMPT)
    if err:
        return JsonResponse({'error': err}, status=502)
    return JsonResponse({'answer': clean_ai_markdown(result), 'citations': citations})


def ajax_space_learning_path(request, space_id):
    """Generate a daily learning path grounded in the space documents."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    throttled = _throttled(request, THROTTLE_GENERATE)
    if throttled:
        return throttled

    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err
    if not _space_permission_allows(space, user_id, 'generate_min_role'):
        return JsonResponse({'error': 'You do not have permission to generate learning paths here'}, status=403)

    days = _bounded_int(_json_body(request).get('days'), 3, 30, 7)
    texts, _parsing, _failed = _get_space_texts(space)
    if not texts:
        if _parsing:
            return JsonResponse({'error': 'Documents are still being parsed. Please wait a moment and try again.', 'parseStatus': 'parsing'}, status=202)
        if _failed:
            return JsonResponse({'error': 'Some documents failed to parse. Try re-uploading them or click retry.', 'parseStatus': 'failed'}, status=422)
        return JsonResponse({'error': 'No readable documents in this space'}, status=400)
    combined = '\n\n'.join(f"=== {t['title']} ===\n{t['content'][:2500]}" for t in texts)[:MAX_TEXT_CHARS]
    prompt = (
        f"Create a {days}-day learning path from these study materials. "
        "For each day include: focus topic, study tasks, quiz/revision task, and an outcome checkpoint. "
        "Return clear markdown with one heading per day.\n\n--- DOCUMENTS ---\n" + combined + "\n--- END ---"
    )
    result, err = _qwen().simple_chat(prompt, system_prompt=PLANNER_SYSTEM_PROMPT)
    if err:
        return JsonResponse({'error': err}, status=502)
    plan_text = clean_ai_markdown(result)
    # persist to space
    space.learning_plan = plan_text
    space.learning_plan_days = days
    space.save(update_fields=['learning_plan', 'learning_plan_days'])
    return JsonResponse({'plan': plan_text, 'days': days})


def ajax_space_list_available_docs(request, space_id):
    """List all StudyDocuments owned by the user, for adding to a space."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err

    docs = StudyDocument.objects.filter(user_id=user_id).order_by('-updated_at')[:100]
    doc_list = []
    for d in docs:
        doc_list.append({
            'id': d.id,
            'title': d.title or d.file_name or 'Untitled',
            'fileName': d.file_name,
            'fileSize': d.file_size,
            'spaceId': d.space_id,
            'status': d.status,
        })
    return JsonResponse({'documents': doc_list})


def ajax_space_list_resources(request, space_id):
    """List Resources uploaded by the user that can be added to a space."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err

    resources = Resource.objects.filter(
        uploaded_by_id=user_id,
        approval_status='approved',
    ).order_by('-added_at')[:100]
    res_list = []
    for r in resources:
        res_list.append({
            'id': r.id,
            'title': r.title or 'Untitled',
            'subject': r.subject,
            'type': r.type,
            'fileSize': r.file_size,
            'fileUrl': r.file_url or '',
        })
    return JsonResponse({'resources': res_list})


def ajax_space_add_document(request, space_id):
    """Attach an existing StudyDocument to a study space. Max 5 docs per space."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    space, err = _manageable_space(space_id, user_id)
    if err:
        return err
    if not _space_permission_allows(space, user_id, 'upload_min_role'):
        return JsonResponse({'error': 'You do not have permission to add files to this space'}, status=403)

    if space.documents.count() >= MAX_DOCS_PER_SPACE:
        return JsonResponse({'error': f'Maximum {MAX_DOCS_PER_SPACE} documents per space'}, status=400)

    body = _json_body(request)
    doc_id = body.get('document_id', '').strip()
    if not doc_id:
        return JsonResponse({'error': 'document_id is required'}, status=400)

    try:
        doc = StudyDocument.objects.get(pk=doc_id, user_id=user_id)
    except StudyDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

    now = now_ms()

    if doc.space_id == space_id:
        # Already attached to this space. Treat as success so repeated clicks or
        # stale UI state do not produce a confusing 400.
        return JsonResponse(_serialize_space_detail(space, user_id))

    if doc.space_id and doc.space_id != space_id:
        # A StudyDocument belongs to one space, but users expect "Select existing
        # file" to re-use/copy a file from another space. Clone metadata and any
        # parsed AI-ready text so the new space can use it immediately without
        # moving/removing the original document.
        doc = StudyDocument.objects.create(
            id=uuid_str(),
            space=space,
            user_id=user_id,
            title=doc.title,
            file_url=doc.file_url,
            file_name=doc.file_name,
            file_size=doc.file_size,
            mime_type=doc.mime_type,
            page_count=doc.page_count,
            status=doc.status,
            parse_status=doc.parse_status,
            parsed_text=doc.parsed_text,
            parsed_at=doc.parsed_at,
            parse_error=doc.parse_error,
            qwen_file_id=doc.qwen_file_id,
            summary_compact=doc.summary_compact,
            summary_detailed=doc.summary_detailed,
            summary_generated_at=doc.summary_generated_at,
            summary_updated_at=doc.summary_updated_at,
            mindmap_json=doc.mindmap_json,
            mindmap_generated_at=doc.mindmap_generated_at,
            created_at=now,
            updated_at=now,
        )
    else:
        doc.space = space
        doc.updated_at = now
        doc.save(update_fields=['space', 'updated_at'])

    space.updated_at = now
    space.save(update_fields=['updated_at'])

    return JsonResponse(_serialize_space_detail(space, user_id))


def ajax_space_add_resource(request, space_id):
    """Import a Resource into a study space as a new StudyDocument. Max 5 docs per space."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    space, err = _manageable_space(space_id, user_id)
    if err:
        return err
    if not _space_permission_allows(space, user_id, 'upload_min_role'):
        return JsonResponse({'error': 'You do not have permission to add files to this space'}, status=403)

    if space.documents.count() >= MAX_DOCS_PER_SPACE:
        return JsonResponse({'error': f'Maximum {MAX_DOCS_PER_SPACE} documents per space'}, status=400)

    body = _json_body(request)
    resource_id = body.get('resource_id', '').strip()
    if not resource_id:
        return JsonResponse({'error': 'resource_id is required'}, status=400)

    try:
        resource = Resource.objects.get(pk=resource_id, uploaded_by_id=user_id, approval_status='approved')
    except Resource.DoesNotExist:
        return JsonResponse({'error': 'Resource not found'}, status=404)

    file_url = resource.file_url or ''
    if resource.file:
        file_url = resource.file.url

    now = now_ms()
    doc = StudyDocument.objects.create(
        id=uuid_str(),
        space=space,
        user_id=user_id,
        title=resource.title,
        file_url=file_url,
        file_name=os.path.basename(file_url) if file_url else resource.title,
        file_size=resource.file_size,
        mime_type='application/pdf' if resource.type == 'PDF' else 'application/octet-stream',
        status='ready',
        created_at=now,
        updated_at=now,
    )

    space.updated_at = now
    space.save(update_fields=['updated_at'])

    return JsonResponse(_serialize_space_detail(space, user_id), status=201)


def ajax_space_remove_document(request, space_id, doc_id):
    """Detach a document from a study space. Owner only."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    space, err = _manageable_space(space_id, user_id)
    if err:
        return err

    try:
        doc = StudyDocument.objects.get(pk=doc_id, space=space)
    except StudyDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not in this space'}, status=404)

    doc.space = None
    doc.updated_at = now_ms()
    doc.save(update_fields=['space', 'updated_at'])

    space.updated_at = now_ms()
    space.save(update_fields=['updated_at'])

    return JsonResponse(_serialize_space_detail(space, user_id))


def ajax_space_upload(request, space_id):
    """Upload a file directly into a study space. Max 5 docs per space."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    throttled = _throttled(request, THROTTLE_UPLOAD)
    if throttled:
        return throttled

    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err
    if not _space_permission_allows(space, user_id, 'upload_min_role'):
        return JsonResponse({'error': 'You do not have permission to add files to this space'}, status=403)

    if space.documents.count() >= MAX_DOCS_PER_SPACE:
        return JsonResponse({'error': f'Maximum {MAX_DOCS_PER_SPACE} documents per space'}, status=400)

    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return JsonResponse({'error': 'No file provided'}, status=400)

    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return JsonResponse({'error': f'File type {ext} is not supported'}, status=400)

    if uploaded_file.size > SPACE_UPLOAD_MAX_FILE_SIZE:
        return JsonResponse({'error': f'File is too large (max {SPACE_UPLOAD_MAX_FILE_SIZE // (1024 * 1024)} MB)'}, status=400)

    from django.core.files.storage import default_storage

    file_name = uploaded_file.name
    safe_name = f"study/{user_id}/{uuid_str()}{ext}"
    try:
        uploaded_file.seek(0)
        saved_path = default_storage.save(safe_name, uploaded_file)
    except Exception as e:  # noqa: BLE001
        logger.exception('StudySpace upload storage failed for user=%s space=%s file=%s', user_id, space_id, file_name)
        return JsonResponse({'error': 'Could not save uploaded file. Please try again.'}, status=500)

    try:
        file_url = default_storage.url(saved_path)
    except Exception:  # noqa: BLE001
        file_url = f"/media/{saved_path}"

    now = now_ms()
    doc = StudyDocument.objects.create(
        id=uuid_str(),
        space=space,
        user_id=user_id,
        title=os.path.splitext(file_name)[0],
        file_url=file_url,
        file_name=file_name,
        file_size=uploaded_file.size,
        mime_type=uploaded_file.content_type or 'application/octet-stream',
        status='ready',
        created_at=now,
        updated_at=now,
    )

    space.updated_at = now
    space.save(update_fields=['updated_at'])

    is_media = doc.mime_type.startswith('video/') or doc.mime_type.startswith('audio/') or ext in SPACE_MEDIA_EXTENSIONS
    if not is_media:
        try:
            start_parse(doc.id)
        except Exception as e:  # noqa: BLE001
            logger.exception('StudySpace upload parse start failed for doc=%s: %s', doc.id, e)

    return JsonResponse({
        'success': True,
        'document': _serialize_study_doc_list_item(doc),
        'space': _serialize_space_detail(space, user_id),
        'fileUrl': file_url,
        'file_url': file_url,
        'fileName': file_name,
        'fileSize': uploaded_file.size,
        'mimeType': uploaded_file.content_type or 'application/octet-stream',
    }, status=201)


# ── Async generation job status ─────────────────────────────────────────────


def ajax_generation_status(request, job_id):
    """Poll the status of an async generation job."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    job = get_job(job_id)
    if not job:
        return JsonResponse({'error': 'Job not found'}, status=404)
    if job.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    return JsonResponse(serialize_job(job))


def _enqueue_or_process(job_type, user_id, space_id, params, request):
    """Enqueue a generation job and return 202, or process synchronously as fallback.

    Returns (job, is_async). If is_async=True, the view should return 202 with
    the job ID. If is_async=False, the job was processed inline and the result
    is already stored in job.result.
    """
    job = enqueue(job_type, user_id, space_id=space_id, params=params)

    # Try to process synchronously if no worker is likely running.
    # This ensures the feature works even without a separate worker process.
    worker_ping = cache.get('generation:worker:ping')
    worker_alive = worker_ping and (now_ms() - int(worker_ping)) < 30000  # 30s grace

    if not worker_alive:
        # No worker detected — process inline (synchronous fallback)
        executor = EXECUTORS.get(job_type)
        if executor:
            try:
                mark_processing(job)
                job.refresh_from_db()
                executor(job)
                job.refresh_from_db()
            except Exception as e:
                logger.exception('Inline generation failed for job %s: %s', job.id, e)
                job.refresh_from_db()
                if job.status == GenerationJob.STATUS_PROCESSING:
                    mark_failed(job, str(e)[:2000])
                    job.refresh_from_db()
        return job, False

    return job, True


def _job_result(job):
    """Extract the result dict from a completed GenerationJob."""
    import json
    if not job.result:
        return {'error': 'No result'}
    try:
        return json.loads(job.result)
    except (json.JSONDecodeError, TypeError):
        return {'error': job.result}


# ── Study Space generation views ─────────────────────────────────────────────


def ajax_space_generate_summary(request, space_id):
    """Generate a linked summary across all documents in the space (async with sync fallback)."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    throttled = _throttled(request, THROTTLE_GENERATE)
    if throttled:
        return throttled
    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err
    if not _space_permission_allows(space, user_id, 'generate_min_role'):
        return JsonResponse({'error': 'You do not have permission to generate content in this space'}, status=403)

    texts, _parsing, _failed = _get_space_texts(space)
    if not texts:
        if _parsing:
            return JsonResponse({'error': 'Documents are still being parsed. Please wait a moment and try again.', 'parseStatus': 'parsing'}, status=202)
        if _failed:
            return JsonResponse({'error': 'Some documents failed to parse. Try re-uploading them or click retry.', 'parseStatus': 'failed'}, status=422)
        return JsonResponse({'error': 'No readable documents in this space'}, status=400)

    body = _json_body(request)
    mode = _summary_mode(body.get('mode'))

    job, is_async = _enqueue_or_process(
        GenerationJob.TYPE_SUMMARY, user_id, space_id=space_id,
        params={'mode': mode}, request=request,
    )
    if is_async:
        return JsonResponse({'jobId': job.id, 'status': job.status, 'jobType': job.job_type}, status=202)
    if job.status == GenerationJob.STATUS_FAILED:
        return JsonResponse({'error': job.error or 'Generation failed'}, status=502)
    return JsonResponse(_job_result(job))

def ajax_space_update_summary(request, space_id):
    """Allow the owner to edit and save the linked summary."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    space, err = _owned_space(space_id, user_id)
    if err:
        return err

    body = _json_body(request)
    mode = _summary_mode(body.get('mode'))
    summary = (body.get('summary') or '').strip()
    if not summary:
        return JsonResponse({'error': 'Summary cannot be empty'}, status=400)
    if len(summary) > 200000:
        return JsonResponse({'error': 'Summary is too long'}, status=400)

    if mode == 'detailed':
        space.link_summary_detailed = summary
    else:
        space.link_summary_compact = summary
    space.updated_at = now_ms()
    space.save(update_fields=['link_summary_compact', 'link_summary_detailed', 'updated_at'])

    return JsonResponse({
        'mode': mode,
        'summary': summary,
        'summaryCompact': space.link_summary_compact,
        'summaryDetailed': space.link_summary_detailed,
    })


def ajax_space_generate_mindmap(request, space_id):
    """Generate a linked mindmap across all space documents (async with sync fallback)."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    throttled = _throttled(request, THROTTLE_GENERATE)
    if throttled:
        return throttled
    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err
    if not _space_permission_allows(space, user_id, 'generate_min_role'):
        return JsonResponse({'error': 'You do not have permission to generate content in this space'}, status=403)

    texts, _parsing, _failed = _get_space_texts(space)
    if not texts:
        if _parsing:
            return JsonResponse({'error': 'Documents are still being parsed. Please wait a moment and try again.', 'parseStatus': 'parsing'}, status=202)
        if _failed:
            return JsonResponse({'error': 'Some documents failed to parse. Try re-uploading them or click retry.', 'parseStatus': 'failed'}, status=422)
        return JsonResponse({'error': 'No readable documents in this space'}, status=400)

    job, is_async = _enqueue_or_process(
        GenerationJob.TYPE_MINDMAP, user_id, space_id=space_id,
        params={}, request=request,
    )
    if is_async:
        return JsonResponse({'jobId': job.id, 'status': job.status, 'jobType': job.job_type}, status=202)
    if job.status == GenerationJob.STATUS_FAILED:
        return JsonResponse({'error': job.error or 'Generation failed'}, status=502)
    return JsonResponse(_job_result(job))

def ajax_space_generate_quiz(request, space_id):
    """Generate a quiz across all space documents (async with sync fallback)."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    throttled = _throttled(request, THROTTLE_GENERATE)
    if throttled:
        return throttled
    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err
    if not _space_permission_allows(space, user_id, 'generate_min_role'):
        return JsonResponse({'error': 'You do not have permission to generate content in this space'}, status=403)

    body = _json_body(request)
    count = _bounded_int(body.get('count'), 3, 20, 5)

    texts, _parsing, _failed = _get_space_texts(space)
    if not texts:
        if _parsing:
            return JsonResponse({'error': 'Documents are still being parsed. Please wait a moment and try again.', 'parseStatus': 'parsing'}, status=202)
        if _failed:
            return JsonResponse({'error': 'Some documents failed to parse. Try re-uploading them or click retry.', 'parseStatus': 'failed'}, status=422)
        return JsonResponse({'error': 'No readable documents in this space'}, status=400)

    job, is_async = _enqueue_or_process(
        GenerationJob.TYPE_QUIZ, user_id, space_id=space_id,
        params={'count': count}, request=request,
    )
    if is_async:
        return JsonResponse({'jobId': job.id, 'status': job.status, 'jobType': job.job_type}, status=202)
    if job.status == GenerationJob.STATUS_FAILED:
        return JsonResponse({'error': job.error or 'Generation failed'}, status=502)
    return JsonResponse(_job_result(job))

def ajax_space_quiz_detail(request, quiz_id):
    """Get quiz detail with questions for a space-level quiz."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        quiz = StudySpaceQuiz.objects.get(pk=quiz_id)
    except StudySpaceQuiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    space, err = _accessible_space(quiz.space_id, user_id, request)
    if err:
        return err

    questions = quiz.questions.all().order_by('question_number')
    # correctAnswer/explanation are intentionally omitted before submission.
    return JsonResponse({
        'quiz': {
            'id': quiz.id,
            'title': quiz.title,
            'questionCount': quiz.question_count,
            'createdAt': quiz.created_at,
            'questions': [
                {
                    'id': q.id,
                    'questionNumber': q.question_number,
                    'questionText': q.question_text,
                    'optionA': q.option_a,
                    'optionB': q.option_b,
                    'optionC': q.option_c,
                    'optionD': q.option_d,
                }
                for q in questions
            ],
        },
    })


def ajax_space_quiz_submit(request, quiz_id):
    """Submit answers for a space-level quiz."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        quiz = StudySpaceQuiz.objects.get(pk=quiz_id)
    except StudySpaceQuiz.DoesNotExist:
        return JsonResponse({'error': 'Quiz not found'}, status=404)

    space, err = _accessible_space(quiz.space_id, user_id, request)
    if err:
        return err

    body = _json_body(request)
    answers = body.get('answers', {})
    if not isinstance(answers, dict):
        return JsonResponse({'error': 'Invalid answers format'}, status=400)

    questions = list(quiz.questions.all().order_by('question_number'))
    correct = 0
    answer_records = []
    results = []
    for q in questions:
        given = str(answers.get(str(q.id), '')).upper()[:1]
        is_correct = given == q.correct_answer
        if is_correct:
            correct += 1
        answer_records.append({
            'questionId': q.id,
            'given': given,
            'correct': q.correct_answer,
            'isCorrect': is_correct,
        })
        results.append({
            'questionId': q.id,
            'question': q.question_text,
            'options': {'A': q.option_a, 'B': q.option_b, 'C': q.option_c, 'D': q.option_d},
            'userAnswer': given,
            'correctAnswer': q.correct_answer,
            'explanation': q.explanation,
            'isCorrect': is_correct,
        })

    now = now_ms()
    # XP is only credited on the FIRST attempt per (quiz, user) to prevent farming.
    is_first_attempt = not StudySpaceQuizAttempt.objects.filter(quiz=quiz, user_id=user_id).exists()
    xp = correct * 10 if is_first_attempt else 0
    attempt = StudySpaceQuizAttempt.objects.create(
        id=uuid_str(),
        quiz=quiz,
        user_id=user_id,
        score=correct,
        total_questions=len(questions),
        answers=json.dumps(answers),
        xp_earned=xp,
        completed_at=now,
        created_at=now,
    )
    if xp:
        User.objects.filter(pk=user_id).update(contribution_score=F('contribution_score') + xp)

    return JsonResponse({
        'attempt': {
            'id': attempt.id,
            'score': correct,
            'totalQuestions': len(questions),
            'xpEarned': xp,
            'firstAttempt': is_first_attempt,
            'answers': answer_records,
            'results': results,
        },
        'results': results,
    })


def ajax_space_quiz_history(request, space_id):
    """Get all quizzes for a space with attempt summary for the current user."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err

    quizzes = StudySpaceQuiz.objects.filter(space=space, user_id=user_id).order_by('-created_at')
    quiz_ids = [q.id for q in quizzes]

    attempt_agg = StudySpaceQuizAttempt.objects.filter(
        quiz_id__in=quiz_ids, user_id=user_id
    ).values('quiz_id').annotate(
        total=Count('id'), best=Max('score'), last_at=Max('completed_at')
    )
    attempt_map = {a['quiz_id']: a for a in attempt_agg}

    quiz_list = []
    for q in quizzes:
        agg = attempt_map.get(q.id, {})
        quiz_list.append({
            'id': q.id,
            'title': q.title,
            'questionCount': q.question_count,
            'createdAt': q.created_at,
            'attemptCount': agg.get('total', 0),
            'bestScore': agg.get('best', 0),
            'lastAttemptAt': agg.get('last_at'),
        })

    return JsonResponse({'quizzes': quiz_list})


def ajax_space_generate_flashcards(request, space_id):
    """Generate flashcards across all space documents (async with sync fallback)."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    throttled = _throttled(request, THROTTLE_GENERATE)
    if throttled:
        return throttled
    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err
    if not _space_permission_allows(space, user_id, 'generate_min_role'):
        return JsonResponse({'error': 'You do not have permission to generate content in this space'}, status=403)

    body = _json_body(request)
    count = _bounded_int(body.get('count'), 3, 30, 8)

    texts, _parsing, _failed = _get_space_texts(space)
    if not texts:
        if _parsing:
            return JsonResponse({'error': 'Documents are still being parsed. Please wait a moment and try again.', 'parseStatus': 'parsing'}, status=202)
        if _failed:
            return JsonResponse({'error': 'Some documents failed to parse. Try re-uploading them or click retry.', 'parseStatus': 'failed'}, status=422)
        return JsonResponse({'error': 'No readable documents in this space'}, status=400)

    job, is_async = _enqueue_or_process(
        GenerationJob.TYPE_FLASHCARD, user_id, space_id=space_id,
        params={'count': count}, request=request,
    )
    if is_async:
        return JsonResponse({'jobId': job.id, 'status': job.status, 'jobType': job.job_type}, status=202)
    if job.status == GenerationJob.STATUS_FAILED:
        return JsonResponse({'error': job.error or 'Generation failed'}, status=502)
    return JsonResponse(_job_result(job))

def ajax_space_flashcard_review(request, card_id):
    """Review (rate confidence for) a space-level flashcard."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        card = StudySpaceFlashcard.objects.get(pk=card_id)
    except StudySpaceFlashcard.DoesNotExist:
        return JsonResponse({'error': 'Flashcard not found'}, status=404)

    space, err = _accessible_space(card.space_id, user_id, request)
    if err:
        return err

    body = _json_body(request)
    confidence = body.get('confidence', 'medium')
    if confidence not in ('easy', 'medium', 'hard'):
        confidence = 'medium'

    now = now_ms()
    next_review_at = now + (86400000 if confidence == 'hard' else 86400000 * 3 if confidence == 'medium' else 86400000 * 7)
    review, created = StudySpaceFlashcardReview.objects.get_or_create(
        flashcard=card,
        user_id=user_id,
        defaults={
            'id': uuid_str(),
            'confidence': confidence,
            'review_count': 1,
            'last_reviewed_at': now,
            'next_review_at': next_review_at,
        },
    )
    if not created:
        StudySpaceFlashcardReview.objects.filter(pk=review.pk).update(
            confidence=confidence,
            review_count=F('review_count') + 1,
            last_reviewed_at=now,
            next_review_at=next_review_at,
        )
        review.refresh_from_db(fields=['review_count'])

    return JsonResponse({
        'cardId': card.id,
        'confidence': confidence,
        'reviewCount': review.review_count,
    })


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

    summaries_count = study_docs.filter(Q(summary_compact__gt='') | Q(summary_detailed__gt='')).count()
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

    # Social link click analytics
    link_clicks = SocialLinkClick.objects.filter(user=user)
    total_link_clicks = link_clicks.count()
    link_clicks_30d = link_clicks.filter(created_at__gte=cutoff_30).count()
    link_clicks_unique = link_clicks.exclude(clicker_id__isnull=True).values('clicker_id').distinct().count()
    link_clicks_by_platform = list(
        link_clicks.values('platform')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]
    )
    link_clicks_by_day_14 = []
    for i in range(13, -1, -1):
        start = today_start - i * day_ms
        end = start + day_ms
        link_clicks_by_day_14.append(
            link_clicks.filter(created_at__gte=start, created_at__lt=end).count()
        )
    max_link_clicks_day = max(link_clicks_by_day_14) if link_clicks_by_day_14 else 1

    link_clicks_by_follower = list(
        link_clicks.values('is_follower')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    link_clicks_by_country = list(
        link_clicks.exclude(clicker_country='')
        .values('clicker_country')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]
    )
    link_clicks_by_gender = list(
        link_clicks.exclude(clicker_gender='')
        .values('clicker_gender')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    link_clicks_by_age_group = []
    age_groups = [('13-17', 13, 17), ('18-24', 18, 24), ('25-34', 25, 34), ('35-44', 35, 44), ('45+', 45, 200)]
    for label, lo, hi in age_groups:
        cnt = link_clicks.filter(clicker_age__gte=lo, clicker_age__lte=hi).count()
        if cnt:
            link_clicks_by_age_group.append({'group': label, 'total': cnt})
    lt13 = link_clicks.filter(clicker_age__lt=13, clicker_age__isnull=False).count()
    if lt13:
        link_clicks_by_age_group.insert(0, {'group': '<13', 'total': lt13})

    ctx.update({
        'link_clicks_total': total_link_clicks,
        'link_clicks_30d': link_clicks_30d,
        'link_clicks_unique': link_clicks_unique,
        'link_clicks_by_platform': link_clicks_by_platform,
        'link_clicks_by_follower': link_clicks_by_follower,
        'link_clicks_by_country': link_clicks_by_country,
        'link_clicks_by_gender': link_clicks_by_gender,
        'link_clicks_by_age_group': link_clicks_by_age_group,
        'link_clicks_by_day_14': link_clicks_by_day_14,
        'max_link_clicks_day': max_link_clicks_day,
    })
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

    throttled = _throttled(request, THROTTLE_UPLOAD)
    if throttled:
        return throttled

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

    start_parse(doc.id)

    return JsonResponse({'document': _serialize_study_doc_list_item(doc)}, status=201)


def ajax_study_parse_status(request, doc_id):
    """Get the parse status of a study document."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    doc, error = _accessible_doc(doc_id, user_id)
    if error:
        return error

    return JsonResponse(get_parse_status(doc_id))


def ajax_study_reparse(request, doc_id):
    """Re-parse a study document (e.g. after failure)."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    doc, error = _accessible_doc(doc_id, user_id)
    if error:
        return error

    force = str(request.GET.get('force') or request.POST.get('force') or '').lower() == 'true'
    if not force and doc.parse_status not in (PARSE_STATUS_FAILED, PARSE_STATUS_READY, 'pending'):
        return JsonResponse({'error': 'Document is already being parsed'}, status=400)

    ok = doc_reparse(doc_id)
    if not ok:
        return JsonResponse({'error': 'Could not start parsing'}, status=500)

    doc.refresh_from_db()
    return JsonResponse({
        'success': True,
        'parseStatus': doc.parse_status,
        'document': _serialize_study_doc_list_item(doc),
    })


def ajax_space_parse_status(request, space_id, doc_id):
    """Get the parse status of a document in a study space."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    space, err = _accessible_space(space_id, user_id, request)
    if err:
        return err

    try:
        doc = space.documents.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

    return JsonResponse(get_parse_status(doc_id))


def ajax_space_reparse(request, space_id, doc_id):
    """Re-parse a document in a study space."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    space, err = _manageable_space(space_id, user_id)
    if err:
        return err

    try:
        doc = space.documents.get(pk=doc_id)
    except StudyDocument.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

    force = str(request.GET.get('force') or request.POST.get('force') or '').lower() == 'true'
    if not force and doc.parse_status not in (PARSE_STATUS_FAILED, PARSE_STATUS_READY, 'pending'):
        return JsonResponse({'error': 'Document is already being parsed'}, status=400)

    ok = doc_reparse(doc_id)
    if not ok:
        return JsonResponse({'error': 'Could not start parsing'}, status=500)

    doc.refresh_from_db()
    return JsonResponse({
        'success': True,
        'parseStatus': doc.parse_status,
        'document': _serialize_study_doc_list_item(doc),
    })


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
    """Legacy per-document sharing endpoint.

    Per-document sharing was removed in migration 0052 — sharing now happens
    at the Study Space level. This endpoint returns 410 Gone instead of
    crashing on the removed StudyDocument share fields.
    """
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error

    return JsonResponse({
        'error': (
            'Per-document sharing has been replaced by Study Space sharing. '
            'Add this document to a Study Space and share the space instead.'
        ),
        'code': 'gone',
    }, status=410)

# ── Summary ────────────────────────────────────────────────────────────────


def ajax_study_generate_summary(request, doc_id):
    """Generate a compact or detailed summary for a document using Qwen."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    throttled = _throttled(request, THROTTLE_GENERATE)
    if throttled:
        return throttled

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error

    body = _json_body(request)
    mode = _summary_mode(body.get('mode'))

    prepared = _prepare_doc_for_qwen(doc)
    err = _check_prepared(prepared)
    if err:
        return err

    prompt_label = 'detailed' if mode == 'detailed' else 'compact'
    file_prompt = (
        f"Create a {prompt_label} study summary from this file. Start directly with the summary heading. "
        "Do not include any introductory sentence."
    )
    text_prompt = (
        f"Create a {prompt_label} study summary from this document. Start directly with the summary heading. "
        "Do not include any introductory sentence."
    )
    result, err = _qwen().send_doc_task(prepared, file_prompt, text_prompt, summary_system_prompt(mode))

    if err:
        logger.error('Study Lab summary failed: %s', err)
        return JsonResponse({'error': err}, status=502)

    summary = normalize_formulas(clean_ai_markdown(result))
    _save_summary(doc, mode, summary)

    return JsonResponse({
        'mode': mode,
        'summary': summary,
        'summaryCompact': doc.summary_compact,
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
        'summaryCompact': doc.summary_compact,
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

    throttled = _throttled(request, THROTTLE_GENERATE)
    if throttled:
        return throttled

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error

    prepared = _prepare_doc_for_qwen(doc)
    err = _check_prepared(prepared)
    if err:
        return err

    file_prompt = 'Create a study mindmap from this file. Return only the JSON object.'
    text_prompt = 'Create a study mindmap from this document. Return only the JSON object.'
    result, err = _qwen().send_doc_task(prepared, file_prompt, text_prompt, MINDMAP_SYSTEM_PROMPT)
    if err:
        return JsonResponse({'error': err}, status=502)

    mindmap = parse_json_object_response(result)
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

    throttled = _throttled(request, THROTTLE_GENERATE)
    if throttled:
        return throttled

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error

    body = _json_body(request)
    question_count = _bounded_int(body.get('count', 10), 5, 40, 10)

    prepared = _prepare_doc_for_qwen(doc)
    err = _check_prepared(prepared)
    if err:
        return err

    exclusions = _quiz_exclusions(doc)
    exclusion_text = exclusion_block('Existing questions to avoid', exclusions)
    file_prompt = f"Generate {question_count} NEW MCQ questions from this file.\n{exclusion_text}"
    text_prompt = f"Generate {question_count} NEW MCQ questions from this document.\n{exclusion_text}"
    result, err = _qwen().send_doc_task(prepared, file_prompt, text_prompt, QUIZ_SYSTEM_PROMPT.format(count=question_count))
    if err:
        return JsonResponse({'error': err}, status=502)

    questions = parse_json_response(result)
    questions = dedupe_questions(questions, set(q.lower().strip() for q in exclusions))[:question_count]
    if not questions:
        return JsonResponse({'error': 'Failed to parse fresh quiz questions from AI response'}, status=502)

    now = now_ms()
    with transaction.atomic():
        quiz = StudyQuiz.objects.create(
            id=uuid_str(),
            document=doc,
            user_id=user_id,
            title=f"Quiz: {doc.title or doc.file_name or 'Untitled'}",
            question_count=len(questions),
            created_at=now,
        )

        question_rows = []
        for i, q in enumerate(questions):
            options = q.get('options', []) if isinstance(q, dict) else []
            question_rows.append(StudyQuizQuestion(
                id=uuid_str(),
                quiz=quiz,
                question_number=i + 1,
                question_text=normalize_formulas((q.get('question', '') if isinstance(q, dict) else '').strip()),
                option_a=normalize_formulas(options[0]) if len(options) > 0 else '',
                option_b=normalize_formulas(options[1]) if len(options) > 1 else '',
                option_c=normalize_formulas(options[2]) if len(options) > 2 else '',
                option_d=normalize_formulas(options[3]) if len(options) > 3 else '',
                correct_answer=((q.get('correct', 'A') if isinstance(q, dict) else 'A') or 'A').upper()[:1],
                explanation=normalize_formulas((q.get('explanation', '') if isinstance(q, dict) else '').strip()),
            ))
        StudyQuizQuestion.objects.bulk_create(question_rows)

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

    # XP is only credited on the FIRST attempt per (quiz, user) to prevent farming.
    is_first_attempt = not StudyQuizAttempt.objects.filter(quiz=quiz, user_id=user_id).exists()
    xp_earned = score * 10 if is_first_attempt else 0
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

    if xp_earned:
        User.objects.filter(pk=user_id).update(contribution_score=F('contribution_score') + xp_earned)

    return JsonResponse({
        'attempt': {
            'id': attempt.id,
            'score': attempt.score,
            'totalQuestions': attempt.total_questions,
            'xpEarned': attempt.xp_earned,
            'firstAttempt': is_first_attempt,
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

    throttled = _throttled(request, THROTTLE_GENERATE)
    if throttled:
        return throttled

    doc, error = _owned_doc(doc_id, user_id)
    if error:
        return error

    body = _json_body(request)
    card_count = _bounded_int(body.get('count', 15), 5, 50, 15)

    prepared = _prepare_doc_for_qwen(doc)
    err_resp = _check_prepared(prepared)
    if err_resp:
        return err_resp

    exclusions = _flashcard_exclusions(doc)
    exclusion_text = exclusion_block('Existing flashcards to avoid', exclusions)
    file_prompt = f"Create {card_count} NEW flashcards from this file.\n{exclusion_text}"
    text_prompt = f"Create {card_count} NEW flashcards from this document.\n{exclusion_text}"
    result, err = _qwen().send_doc_task(prepared, file_prompt, text_prompt, FLASHCARD_SYSTEM_PROMPT.format(count=card_count))
    if err:
        return JsonResponse({'error': err}, status=502)

    cards = parse_json_response(result)
    cards = dedupe_flashcards(cards, set(c.lower().strip() for c in exclusions))[:card_count]
    if not cards:
        return JsonResponse({'error': 'Failed to parse fresh flashcards from AI response'}, status=502)

    now = now_ms()
    max_card_number = StudyFlashcard.objects.filter(document=doc).aggregate(m=Max('card_number')).get('m') or 0
    flashcard_objs = [
        StudyFlashcard(
            id=uuid_str(),
            document=doc,
            user_id=user_id,
            front=normalize_formulas((c.get('front', '') if isinstance(c, dict) else '').strip()),
            back=normalize_formulas((c.get('back', '') if isinstance(c, dict) else '').strip()),
            card_number=max_card_number + i + 1,
            created_at=now,
        )
        for i, c in enumerate(cards)
    ]
    with transaction.atomic():
        StudyFlashcard.objects.bulk_create(flashcard_objs)
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
    compact = getattr(d, 'summary_compact', '')
    detailed = getattr(d, 'summary_detailed', '')
    return {
        'id': d.id,
        'title': d.title or d.file_name or 'Untitled',
        'fileName': d.file_name,
        'fileSize': d.file_size,
        'status': d.status,
        'parseStatus': d.parse_status,
        'parsedTextLength': len(d.parsed_text) if d.parsed_text else 0,
        'parseError': d.parse_error,
        'summaryGenerated': bool(compact or detailed),
        'mindmapGenerated': bool(getattr(d, 'mindmap_json', '')),
        'quizCount': d.quizzes.count(),
        'flashcardCount': d.flashcards.count(),
        'createdAt': d.created_at,
        'updatedAt': d.updated_at,
        'shareMode': getattr(d, 'share_mode', StudySpace.SHARE_PRIVATE),
        'sharedAt': getattr(d, 'shared_at', 0),
    }


def _serialize_study_doc_detail(d):
    compact = getattr(d, 'summary_compact', '')
    detailed = getattr(d, 'summary_detailed', '')
    return {
        'id': d.id,
        'title': d.title or d.file_name or 'Untitled',
        'fileName': d.file_name,
        'fileSize': d.file_size,
        'mimeType': d.mime_type,
        'status': d.status,
        'parseStatus': d.parse_status,
        'parsedTextLength': len(d.parsed_text) if d.parsed_text else 0,
        'parseError': d.parse_error,
        'summary': compact,
        'summaryCompact': compact,
        'summaryDetailed': detailed,
        'summaryGenerated': bool(compact or detailed),
        'mindmapGenerated': bool(getattr(d, 'mindmap_json', '')),
        'createdAt': d.created_at,
        'updatedAt': d.updated_at,
        'shareMode': getattr(d, 'share_mode', StudySpace.SHARE_PRIVATE),
        'sharedAt': getattr(d, 'shared_at', 0),
        'shareToken': str(getattr(d, 'share_token', '') or ''),
    }


def _serialize_quiz_list_item(q, user_id):
    agg = q.attempts.filter(user_id=user_id).aggregate(c=Count('id'), best=Max('score'))
    return {
        'id': q.id,
        'title': q.title,
        'questionCount': q.question_count,
        'attemptCount': agg.get('c') or 0,
        'bestScore': agg.get('best') or 0,
        'createdAt': q.created_at,
    }


def _serialize_quiz_detail(quiz, viewer_user_id=None):
    viewer_user_id = viewer_user_id or quiz.user_id
    attempt_agg = quiz.attempts.filter(user_id=viewer_user_id).aggregate(c=Count('id'), best=Max('score'))
    questions = quiz.questions.all().order_by('question_number')
    return {
        'id': quiz.id,
        'title': quiz.title,
        'questionCount': quiz.question_count,
        'createdAt': quiz.created_at,
        'attemptCount': attempt_agg.get('c') or 0,
        'bestScore': attempt_agg.get('best') or 0,
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
    if getattr(doc, 'share_mode', StudySpace.SHARE_PRIVATE) == StudySpace.SHARE_LINK and getattr(doc, 'shared_at', 0):
        return True
    if getattr(doc, 'share_mode', StudySpace.SHARE_PRIVATE) == StudySpace.SHARE_SPECIFIC and getattr(doc, 'shared_at', 0):
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
    doc.summary_updated_at = now
    doc.summary_generated_at = now
    doc.updated_at = now
    fields = ['summary_updated_at', 'summary_generated_at', 'updated_at']
    if mode == 'detailed':
        fields.append('summary_detailed')
    else:
        fields.append('summary_compact')
    doc.save(update_fields=fields)


def _prepare_doc_for_qwen(doc):
    """Prepare a document for Qwen generation.

    Uses stored parsed_text when available (parse-once architecture).
    Falls back to on-the-fly file upload + Qwen parse for legacy docs.
    Returns a dict suitable for QwenClient.send_doc_task(), or None on failure.
    Returns a string error message starting with 'PARSE_' prefix if parsing
    is in progress or failed.
    """
    if doc.parse_status == PARSE_STATUS_READY and doc.parsed_text:
        return {
            'is_image': False,
            'has_file': False,
            'uploaded_files': None,
            'text_content': doc.parsed_text[:MAX_TEXT_CHARS],
        }

    if doc.parse_status in ('uploading', 'parsing', 'extracting'):
        return 'PARSE_IN_PROGRESS'

    if doc.parse_status == PARSE_STATUS_FAILED:
        return 'PARSE_FAILED'

    # Legacy fallback: trigger background parsing for pending docs so they'll
    # be cached next time, but also do on-the-fly parsing for immediate use.
    if doc.parse_status in ('pending', '') or (not doc.parse_status):
        start_parse(doc.id)

    if not doc.file_url:
        return None

    try:
        from api.qwen_utils.text_extraction import read_file_bytes
        file_data = read_file_bytes(doc.file_url)
    except Exception as e:
        logger.warning('Failed to read study document: %s', e)
        return None

    if file_data is None:
        return None

    client = _qwen()
    result = client.prepare_file_for_qwen(doc.file_name, file_data)
    if result and result.get('text_content'):
        result['text_content'] = result['text_content'][:MAX_TEXT_CHARS]
    return result


def _check_prepared(prepared):
    """Check the result of _prepare_doc_for_qwen and return a JsonResponse error if needed.

    Returns None if prepared is a valid dict (ready to use).
    Returns a JsonResponse error if prepared is a PARSE_ status string or None.
    """
    if prepared is None:
        return JsonResponse({'error': 'Could not read document content'}, status=502)
    if isinstance(prepared, str):
        if prepared == 'PARSE_IN_PROGRESS':
            return JsonResponse({'error': 'Document is still being parsed. Please wait a moment and try again.', 'parseStatus': 'parsing'}, status=202)
        if prepared == 'PARSE_FAILED':
            return JsonResponse({'error': 'Document parsing failed. Please try re-uploading or click retry.', 'parseStatus': 'failed'}, status=422)
        return JsonResponse({'error': 'Could not read document content'}, status=502)
    return None


def _quiz_exclusions(doc):
    qs = StudyQuizQuestion.objects.filter(quiz__document=doc).order_by('-quiz__created_at')[:120]
    return [q.question_text.strip() for q in qs if q.question_text.strip()]


def _flashcard_exclusions(doc):
    cards = StudyFlashcard.objects.filter(document=doc).order_by('-created_at')[:160]
    return [f"{c.front.strip()} — {c.back.strip()}" for c in cards if c.front.strip() or c.back.strip()]


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
    title = normalize_formulas(str(node.get('title') or node.get('name') or '').strip()[:140])
    note = normalize_formulas(str(node.get('note') or node.get('description') or '').strip()[:280])
    children = node.get('children') if isinstance(node.get('children'), list) else []
    return {
        'title': title or 'Topic',
        'note': note,
        'children': [_normalize_node(child) for child in children if isinstance(child, dict)][:8],
    }


# ── Study Space helpers ──────────────────────────────────────────────────────

MAX_SPACES_PER_USER = 5
MAX_DOCS_PER_SPACE = 5
SPACE_UPLOAD_MAX_FILE_SIZE = 100 * 1024 * 1024
SPACE_MEDIA_EXTENSIONS = {'.mp4', '.avi', '.mov', '.m4v', '.mkv', '.webm', '.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a'}


def _generate_unique_invite_code():
    alphabet = string.ascii_uppercase + string.digits
    for _ in range(20):
        code = ''.join(secrets.choice(alphabet) for _ in range(8))
        if not StudySpace.objects.filter(invite_code=code).exists():
            return code
    return uuid_str().replace('-', '')[:8].upper()


def _ensure_space_invite_code(space):
    if getattr(space, 'invite_code', ''):
        return space.invite_code
    space.invite_code = _generate_unique_invite_code()
    space.save(update_fields=['invite_code'])
    return space.invite_code


def _ensure_space_owner_member(space):
    now = now_ms()
    StudySpaceMember.objects.get_or_create(
        space=space,
        user_id=space.user_id,
        defaults={
            'id': uuid_str(),
            'role': StudySpaceMember.ROLE_OWNER,
            'joined_at': space.created_at or now,
            'updated_at': now,
        },
    )


def _space_membership_role(space, user_id):
    if not user_id:
        return ''
    if space.user_id == user_id:
        return StudySpaceMember.ROLE_OWNER
    member = StudySpaceMember.objects.filter(space=space, user_id=user_id).only('role').first()
    return member.role if member else ''


def _can_manage_space(space, user_id):
    role = _space_membership_role(space, user_id)
    return role in (StudySpaceMember.ROLE_OWNER, StudySpaceMember.ROLE_ADMIN)


def _can_moderate_space(space, user_id):
    role = _space_membership_role(space, user_id)
    return role in (StudySpaceMember.ROLE_OWNER, StudySpaceMember.ROLE_ADMIN, StudySpaceMember.ROLE_MODERATOR)


def _join_space(space, user_id, invited_by_id=None):
    if space.user_id == user_id:
        _ensure_space_owner_member(space)
        return StudySpaceMember.objects.get(space=space, user_id=user_id)
    now = now_ms()
    member, created = StudySpaceMember.objects.get_or_create(
        space=space,
        user_id=user_id,
        defaults={
            'id': uuid_str(),
            'role': StudySpaceMember.ROLE_MEMBER,
            'invited_by_id': invited_by_id,
            'joined_at': now,
            'updated_at': now,
        },
    )
    if not created and member.role not in dict(StudySpaceMember.ROLE_CHOICES):
        member.role = StudySpaceMember.ROLE_MEMBER
        member.updated_at = now
        member.save(update_fields=['role', 'updated_at'])
    return member


def _space_can_be_joined_by_link(space, user_id):
    if space.user_id == user_id:
        return True
    if getattr(space, 'visibility', StudySpace.VISIBILITY_PRIVATE) == StudySpace.VISIBILITY_PUBLIC:
        return True
    if space.share_mode == StudySpace.SHARE_LINK and space.shared_at:
        return True
    if space.share_mode == StudySpace.SHARE_SPECIFIC and space.shared_at:
        return StudySpaceShare.objects.filter(space=space, user_id=user_id).exists()
    return False


def _serialize_space_member(member):
    user = member.user
    return {
        'id': user.id,
        'username': user.username,
        'displayName': user.display_name or user.username,
        'photoUrl': user.photo_url or getattr(user, 'profile_photo_url', '') or '',
        'role': member.role,
        'joinedAt': member.joined_at,
    }


def _migrate_legacy_shared_doc_to_space(token, user_id):
    """Convert a pre-StudySpace document share token into a one-doc space.

    Migration 0052 stopped exposing StudyDocument.share_token in the Django model,
    but existing production rows can still contain the old column. We resolve it
    with raw SQL, preserve the old token as the new StudySpace invite token, and
    attach the document to that space.
    """
    token = str(token or '').strip()
    if not token:
        return None

    # It may already be a StudySpace token.
    existing = StudySpace.objects.filter(share_token=token).first()
    if existing:
        _ensure_space_invite_code(existing)
        _ensure_space_owner_member(existing)
        return existing

    try:
        with connection.cursor() as cursor:
            columns = _legacy_table_columns(cursor, 'study_documents')
            if 'share_token' not in columns:
                return None
            cursor.execute(
                'SELECT id, user_id, title, file_name, share_mode, shared_at, summary_compact, summary_detailed, mindmap_json, created_at, updated_at, space_id '
                'FROM study_documents WHERE share_token=%s LIMIT 1',
                [token],
            )
            row = cursor.fetchone()
    except Exception as exc:
        logger.warning('Legacy Study Lab token lookup failed: %s', exc)
        return None

    if not row:
        return None

    (doc_id, owner_id, title, file_name, share_mode, shared_at, summary_compact,
     summary_detailed, mindmap_json, created_at, updated_at, existing_space_id) = row

    if existing_space_id:
        space = StudySpace.objects.filter(pk=existing_space_id).first()
        if space:
            if not StudySpace.objects.filter(share_token=token).exclude(pk=space.pk).exists():
                space.share_token = token
            if share_mode in (StudySpace.SHARE_LINK, StudySpace.SHARE_SPECIFIC):
                space.share_mode = share_mode
                space.shared_at = shared_at or now_ms()
                space.visibility = StudySpace.VISIBILITY_UNLISTED
            _ensure_space_invite_code(space)
            space.save(update_fields=['share_token', 'share_mode', 'shared_at', 'visibility', 'invite_code'])
            _copy_legacy_doc_grants_to_space(doc_id, space, owner_id)
            _ensure_space_owner_member(space)
            return space

    if share_mode not in (StudySpace.SHARE_LINK, StudySpace.SHARE_SPECIFIC):
        share_mode = StudySpace.SHARE_LINK
    now = now_ms()
    with transaction.atomic():
        space = StudySpace.objects.create(
            id=uuid_str(),
            user_id=owner_id,
            title=title or file_name or 'Shared study document',
            description='Migrated from a legacy Study Lab document share.',
            share_token=token,
            invite_code=_generate_unique_invite_code(),
            share_mode=share_mode,
            visibility=StudySpace.VISIBILITY_UNLISTED,
            shared_at=shared_at or now,
            link_summary_compact=summary_compact or '',
            link_summary_detailed=summary_detailed or '',
            link_summary_generated_at=updated_at or now,
            link_mindmap_json=mindmap_json or '',
            link_mindmap_generated_at=updated_at or now,
            created_at=created_at or now,
            updated_at=updated_at or now,
        )
        StudyDocument.objects.filter(pk=doc_id).update(space=space, updated_at=now)
        _ensure_space_owner_member(space)
        _copy_legacy_doc_grants_to_space(doc_id, space, owner_id)
    return space


def _copy_legacy_doc_grants_to_space(doc_id, space, owner_id):
    grants = StudyDocumentShare.objects.filter(document_id=doc_id).values_list('user_id', flat=True)
    now = now_ms()
    for uid in grants:
        if uid == owner_id:
            continue
        StudySpaceShare.objects.get_or_create(
            space=space,
            user_id=uid,
            defaults={'id': uuid_str(), 'granted_by_id': owner_id, 'created_at': now},
        )


def _legacy_table_columns(cursor, table):
    vendor = connection.vendor
    if vendor == 'sqlite':
        cursor.execute(f'PRAGMA table_info({table})')
        return {row[1] for row in cursor.fetchall()}
    cursor.execute(f'SHOW COLUMNS FROM `{table}`')
    return {row[0] for row in cursor.fetchall()}


def _serialize_space_list_item(space, user_id=None, member_count=None, doc_count=None):
    """Read-only list serializer.

    Must NOT write to the database (no invite-code/owner-member/presence
    upkeep) — it is called in loops over many spaces. Callers can pass
    precomputed ``member_count``/``doc_count`` annotations to avoid
    per-space COUNT queries.
    """
    if doc_count is None:
        doc_count = space.documents.count()
    if member_count is None:
        member_count = StudySpaceMember.objects.filter(space=space).count()
    has_summary = bool(space.link_summary_compact or space.link_summary_detailed)
    has_mindmap = bool(space.link_mindmap_json)
    has_quiz = StudySpaceQuiz.objects.filter(space=space).exists()
    has_flashcards = StudySpaceFlashcard.objects.filter(space=space).exists()
    active_now = StudySpacePresence.objects.filter(space=space).count()
    owner = getattr(space, 'user', None)
    role = _space_membership_role(space, user_id) if user_id else ''
    owner_badge = ''
    if owner:
        if getattr(owner, 'teacher_verified', False):
            owner_badge = 'verified_teacher'
        elif getattr(owner, 'role', '') == getattr(User, 'ROLE_INSTITUTION', 'institution'):
            owner_badge = 'institution'
    return {
        'id': space.id,
        'title': space.title or 'Untitled Space',
        'description': space.description[:120] + '...' if len(space.description) > 120 else space.description,
        'docCount': doc_count,
        'memberCount': member_count,
        'activeNow': active_now,
        'shareMode': space.share_mode,
        'visibility': getattr(space, 'visibility', StudySpace.VISIBILITY_PRIVATE),
        'inviteCode': getattr(space, 'invite_code', ''),
        'shareToken': space.share_token,
        'studyLevel': getattr(space, 'study_level', ''),
        'subject': getattr(space, 'subject', ''),
        'exam': getattr(space, 'exam', ''),
        'isJoined': bool(role),
        'memberRole': role,
        'owner': {
            'id': owner.id if owner else space.user_id,
            'username': owner.username if owner else '',
            'displayName': (owner.display_name or owner.username) if owner else '',
            'photoUrl': (owner.photo_url or getattr(owner, 'profile_photo_url', '') or '') if owner else '',
            'badge': owner_badge,
        },
        'createdAt': space.created_at,
        'updatedAt': space.updated_at,
        'hasSummary': has_summary,
        'hasMindmap': has_mindmap,
        'hasQuiz': has_quiz,
        'hasFlashcards': has_flashcards,
    }


def _serialize_space_detail(space, user_id):
    _ensure_space_invite_code(space)
    _ensure_space_owner_member(space)
    _prune_space_presence(space)
    note = _ensure_space_note(space)
    try:
        cu = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        cu = None
    current_user_data = {
        'id': cu.id if cu else '',
        'username': cu.username if cu else '',
        'displayName': cu.display_name or cu.username if cu else 'Anonymous',
    }
    docs = space.documents.all().order_by('-updated_at')
    doc_list = []
    for d in docs:
        doc_list.append({
            'id': d.id,
            'title': d.title or d.file_name or 'Untitled',
            'fileName': d.file_name,
            'fileSize': d.file_size,
            'mimeType': d.mime_type,
            'pageCount': d.page_count,
            'status': d.status,
            'parseStatus': d.parse_status,
            'parsedTextLength': len(d.parsed_text) if d.parsed_text else 0,
            'parseError': d.parse_error,
            'summaryCompact': d.summary_compact or '',
            'summaryDetailed': d.summary_detailed or '',
            'mindmapJson': d.mindmap_json or '',
            'createdAt': d.created_at,
            'updatedAt': d.updated_at,
        })
    quizzes = StudySpaceQuiz.objects.filter(space=space, user_id=user_id).order_by('-created_at')[:10]
    quiz_ids = [q.id for q in quizzes]
    attempt_agg = StudySpaceQuizAttempt.objects.filter(quiz_id__in=quiz_ids, user_id=user_id).values('quiz_id').annotate(
        total=Count('id'), best=Max('score'), last_at=Max('completed_at')
    )
    attempt_map = {a['quiz_id']: a for a in attempt_agg}
    quiz_list = []
    for q in quizzes:
        agg = attempt_map.get(q.id, {})
        quiz_list.append({
            'id': q.id,
            'title': q.title,
            'questionCount': q.question_count,
            'createdAt': q.created_at,
            'attemptCount': agg.get('total', 0),
            'bestScore': agg.get('best', 0),
            'lastAttemptAt': agg.get('last_at'),
        })
    flashcard_count = StudySpaceFlashcard.objects.filter(space=space, user_id=user_id).count()
    flashcards_qs = StudySpaceFlashcard.objects.filter(space=space, user_id=user_id).order_by('card_number')[:50]
    flashcard_list = []
    for fc in flashcards_qs:
        flashcard_list.append({
            'id': fc.id,
            'front': fc.front,
            'back': fc.back,
            'cardNumber': fc.card_number,
            'createdAt': fc.created_at,
        })
    is_owner = space.user_id == user_id
    member_role = _space_membership_role(space, user_id)
    can_manage = _can_manage_space(space, user_id)
    can_moderate = _can_moderate_space(space, user_id)
    shared_users = []
    if can_manage and space.share_mode == 'specific':
        for s in space.share_grants.select_related('user').all():
            shared_users.append({
                'id': s.user.id,
                'username': s.user.username,
                'displayName': s.user.display_name or s.user.username,
                'photoUrl': s.user.photo_url or getattr(s.user, 'profile_photo_url', '') or '',
            })
    members = [_serialize_space_member(m) for m in space.members.select_related('user').order_by('role', '-joined_at')[:80]]
    presence = [_serialize_presence_row(r) for r in StudySpacePresence.objects.filter(space=space).select_related('user').order_by('-last_seen_at')[:40]]
    analytics = _space_analytics(space)
    owner = getattr(space, 'user', None)
    owner_badge = ''
    if owner:
        if getattr(owner, 'teacher_verified', False):
            owner_badge = 'verified_teacher'
        elif getattr(owner, 'role', '') == getattr(User, 'ROLE_INSTITUTION', 'institution'):
            owner_badge = 'institution'
    return {
        'id': space.id,
        'title': space.title or 'Untitled Space',
        'description': space.description,
        'docCount': len(doc_list),
        'documents': doc_list,
        'quizzes': quiz_list,
        'flashcardCount': flashcard_count,
        'flashcards': flashcard_list,
        'shareMode': space.share_mode,
        'visibility': getattr(space, 'visibility', StudySpace.VISIBILITY_PRIVATE),
        'allowJoinByCode': getattr(space, 'allow_join_by_code', True),
        'inviteCode': getattr(space, 'invite_code', ''),
        'shareToken': space.share_token,
        'studyLevel': getattr(space, 'study_level', ''),
        'subject': getattr(space, 'subject', ''),
        'exam': getattr(space, 'exam', ''),
        'sharedUsers': shared_users,
        'members': members,
        'presence': presence,
        'memberRole': member_role,
        'isOwner': is_owner,
        'canManage': can_manage,
        'canModerate': can_moderate,
        'permissions': {
            'generateMinRole': getattr(space, 'generate_min_role', 'moderator'),
            'uploadMinRole': getattr(space, 'upload_min_role', 'member'),
            'inviteMinRole': getattr(space, 'invite_min_role', 'admin'),
            'moderateMinRole': getattr(space, 'moderate_min_role', 'moderator'),
            'publishMinRole': getattr(space, 'publish_min_role', 'owner'),
            'canGenerate': _space_permission_allows(space, user_id, 'generate_min_role'),
            'canUpload': _space_permission_allows(space, user_id, 'upload_min_role'),
            'canInvite': _space_permission_allows(space, user_id, 'invite_min_role'),
            'canPublish': _space_permission_allows(space, user_id, 'publish_min_role'),
        },
        'currentUser': current_user_data,
        'owner': {
            'id': owner.id if owner else space.user_id,
            'username': owner.username if owner else '',
            'displayName': (owner.display_name or owner.username) if owner else '',
            'photoUrl': (owner.photo_url or getattr(owner, 'profile_photo_url', '') or '') if owner else '',
            'badge': owner_badge,
        },
        'note': {
            'id': note.id,
            'content': note.content,
            'version': note.version,
            'updatedAt': note.updated_at,
            'updatedBy': note.updated_by.display_name if note.updated_by else '',
        },
        'analytics': analytics,
        'linkSummaryCompact': space.link_summary_compact,
        'linkSummaryDetailed': space.link_summary_detailed,
        'linkSummaryGeneratedAt': space.link_summary_generated_at,
        'linkMindmapJson': space.link_mindmap_json,
        'linkMindmapGeneratedAt': space.link_mindmap_generated_at,
        'learningPlan': space.learning_plan,
        'learningPlanDays': space.learning_plan_days,
        'createdAt': space.created_at,
        'updatedAt': space.updated_at,
    }


def _manageable_space(space_id, user_id):
    try:
        space = StudySpace.objects.get(pk=space_id)
    except StudySpace.DoesNotExist:
        return None, JsonResponse({'error': 'Space not found'}, status=404)
    if not _can_manage_space(space, user_id):
        return None, JsonResponse({'error': 'Only space admins can manage this space'}, status=403)
    return space, None


def _owned_space(space_id, user_id):
    try:
        space = StudySpace.objects.get(pk=space_id, user_id=user_id)
    except StudySpace.DoesNotExist:
        return None, JsonResponse({'error': 'Space not found'}, status=404)
    return space, None


def _accessible_space(space_id, user_id, request=None):
    try:
        space = StudySpace.objects.get(pk=space_id)
    except StudySpace.DoesNotExist:
        return None, JsonResponse({'error': 'Space not found'}, status=404)
    if space.user_id == user_id:
        _ensure_space_owner_member(space)
        return space, None
    if _space_membership_role(space, user_id):
        return space, None
    if getattr(space, 'visibility', StudySpace.VISIBILITY_PRIVATE) == StudySpace.VISIBILITY_PUBLIC:
        return space, None
    if space.share_mode == StudySpace.SHARE_LINK and space.shared_at:
        # Link-share access requires that this session actually presented the
        # share token (set in study_space_shared). A bare space id is NOT
        # enough to read an unlisted link-shared space.
        if (
            request is not None
            and request.session.get(f'space_token_{space.id}') == space.share_token
        ):
            return space, None
    if space.share_mode == StudySpace.SHARE_SPECIFIC and space.shared_at:
        if StudySpaceShare.objects.filter(space=space, user_id=user_id).exists():
            return space, None
    return None, JsonResponse({'error': 'Access denied'}, status=403)


def _get_space_texts(space):
    """Extract text content from all ready documents in a space for linked generation.

    Uses stored parsed_text when available (parse-once architecture).
    Falls back to local extraction for legacy docs without parsed_text.
    Skips documents that are still being parsed or failed to parse.

    Returns a tuple: (texts_list, parsing_count, failed_count)
    """
    texts = []
    parsing_count = 0
    failed_count = 0
    docs = space.documents.filter(status='ready').order_by('created_at')
    for doc in docs:
        if doc.parse_status == PARSE_STATUS_READY and doc.parsed_text:
            text = doc.parsed_text
        elif doc.parse_status in ('uploading', 'parsing', 'extracting'):
            parsing_count += 1
            continue
        elif doc.parse_status == PARSE_STATUS_FAILED:
            failed_count += 1
            continue
        else:
            # Legacy/pending doc — trigger background parsing and treat as "parsing"
            start_parse(doc.id)
            parsing_count += 1
            text = ''
        if text and text.strip():
            texts.append({
                'title': doc.title or doc.file_name or 'Document',
                'content': text[:MAX_TEXT_CHARS],
            })
    return texts, parsing_count, failed_count


def _extract_local_text(doc):
    """Extract text locally from a document for the combined space prompt.
    
    Delegates to api.qwen_utils.text_extraction.
    """
    return extract_text_from_file(doc.file_url, doc.file_name or '')


def _space_quiz_exclusions(space):
    qs = StudySpaceQuizQuestion.objects.filter(quiz__space=space).order_by('-quiz__created_at')[:120]
    return [q.question_text.strip() for q in qs if q.question_text.strip()]


def _space_flashcard_exclusions(space):
    cards = StudySpaceFlashcard.objects.filter(space=space).order_by('-created_at')[:160]
    return [f"{c.front.strip()} — {c.back.strip()}" for c in cards if c.front.strip() or c.back.strip()]