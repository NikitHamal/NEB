"""Views Ajax extracted from views.py."""
from django.views.decorators.http import require_http_methods

import json
from api import cleanup as _cleanup, realtime as _rt, services
from api.models import (
    AiFeedback,
    BlogComment,
    Bookmark,
    EditHistory,
    Follow,
    Post,
    PostImage,
    PostMedia,
    Reply,
    Report,
    Resource,
    ResourceComment,
    User,
)
from api.security import (
    get_user_by_auth_token,
    save_post_image_upload,
    save_profile_image_upload,
    validate_profile_photo_url,
)
from api.serializers import UserSerializer
from api.utils import now_ms, uuid_str
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from . import api_client as api
from .json_endpoint import signed_in_member
from .view_helpers import (
    _avatar_url,
    _clear_page_cache,
    _get_user_id,
    _get_valid_token,
    _normalize_user_data,
    _rate_limit,
    _serialize_post,
    _serialize_post_images,
    _serialize_replies,
    _serialize_reply,
    _user_badge_info,
    _viewer_for_locked_check,
    logger,
)
from api.view_helpers import _can_view_locked_profile
from api.security import POST_IMAGE_MAX_COUNT, validate_forum_attachments
from django.core.exceptions import ValidationError


def _parse_web_attachments(data):
    """Validate the optional `attachments` list from an ajax JSON payload.

    Attachments must have been uploaded beforehand via the forum media upload
    endpoint (validation enforces that urls point at our own MEDIA_URL).
    Returns (attachments, error_message); exactly one of the two is set.
    """
    try:
        return validate_forum_attachments(data.get('attachments')), None
    except ValidationError as exc:
        message = exc.messages[0] if getattr(exc, 'messages', None) else str(exc)
        return None, message


@require_POST
@signed_in_member
def ajax_like_post(request, post_id, user):
    try:
        result = services.toggle_post_like(user, post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    cache.delete_many(['home_posts', 'forum_all_posts'])
    return JsonResponse(result)

@require_POST
@signed_in_member
def ajax_like_reply(request, reply_id, user):
    try:
        result = services.toggle_reply_like(user, reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    return JsonResponse(result)

@require_POST
@signed_in_member
def ajax_create_reply(request, post_id, user):
    if _rate_limit(request, 'create_reply', 20, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        parent_id = data.get('parentReplyId')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    if len(content) > 10000:
        return JsonResponse({'error': 'Content must be 10000 characters or fewer'}, status=400)
    if parent_id and not Reply.objects.filter(pk=parent_id, post_id=post_id).exists():
        return JsonResponse({'error': 'Invalid parent reply'}, status=400)
    is_anonymous = bool(data.get('isAnonymous') or data.get('is_anonymous'))
    attachments, attach_error = _parse_web_attachments(data)
    if attach_error:
        return JsonResponse({'error': attach_error}, status=400)
    from api import polls as _polls
    poll_data, poll_error = _polls.clean_poll_input(data.get('poll'))
    if poll_error:
        return JsonResponse({'error': poll_error}, status=400)
    if poll_data and parent_id:
        return JsonResponse({'error': 'Polls can only be added to top-level comments'}, status=400)
    # Voice notes / attachments / a poll can be the entire reply.
    if not attachments and not content and not poll_data:
        return JsonResponse({'error': 'Content required'}, status=400)
    result = services.create_reply(user, post_id, content, parent_id,
                                   is_anonymous=is_anonymous, attachments=attachments, poll_data=poll_data)
    if result:
        from . import forum_labels
        kind = forum_labels.clean_kind(data.get('kind')) if not parent_id else 'comment'
        if kind != 'comment' and result.get('id'):
            Reply.objects.filter(pk=result['id']).update(kind=kind)
            result['kind'] = kind
            result['kindInfo'] = forum_labels.kind_info(kind)
        _clear_page_cache()
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Failed'}, status=500)

@require_POST
@signed_in_member
def ajax_like_resource(request, resource_id, user):
    try:
        result = services.toggle_resource_like(user, resource_id)
    except Resource.DoesNotExist:
        return JsonResponse({'error': 'Resource not found'}, status=404)
    return JsonResponse(result)

@require_POST
@signed_in_member
def ajax_like_resource_comment(request, comment_id, user):
    try:
        result = services.toggle_resource_comment_like(user, comment_id)
    except ResourceComment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    return JsonResponse(result)

@require_POST
def ajax_resource_comment(request, resource_id):
    user_id = _get_user_id(request)
    user = None
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            user = None
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        parent_id = data.get('parentCommentId')
        is_anonymous = bool(data.get('isAnonymous'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    attachments, attach_error = _parse_web_attachments(data)
    if attach_error:
        return JsonResponse({'error': attach_error}, status=400)
    # Voice notes / attachments can be the entire comment.
    if not attachments and not content:
        return JsonResponse({'error': 'Content required'}, status=400)
    result = services.create_resource_comment(user, resource_id, content, parent_id, attachments=attachments, is_anonymous=is_anonymous)
    if result:
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Failed'}, status=500)

@require_POST
@signed_in_member
def ajax_delete_resource_comment(request, comment_id, user):
    is_admin = bool(user.is_admin)
    ok = services.delete_resource_comment(user, comment_id, is_admin=is_admin)
    if ok:
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Permission denied or comment not found'}, status=403)

@require_POST
@signed_in_member
def ajax_like_blog_comment(request, comment_id, user):
    try:
        result = services.toggle_blog_comment_like(user, comment_id)
    except BlogComment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    return JsonResponse(result)

# The NEBians Android app deletes comments with an HTTP DELETE request while
# the website uses POST, so both verbs must be accepted here.
@require_http_methods(["POST", "DELETE"])
@signed_in_member
def ajax_delete_blog_comment(request, comment_id, user):
    is_admin = bool(user.is_admin)
    ok = services.delete_blog_comment(user, comment_id, is_admin=is_admin)
    if ok:
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Permission denied or comment not found'}, status=403)

@require_POST
@signed_in_member
def ajax_create_post(request, user):
    if _rate_limit(request, 'create_post', 10, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    if not getattr(user, 'email_verified', False):
        return JsonResponse({'error': 'Please verify your email before posting.'}, status=403)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    category = data.get('category', '').strip()
    image_urls = data.get('images', [])
    poll_data = data.get('poll')
    if len(title) > 200:
        return JsonResponse({'error': 'Title must be 200 characters or fewer'}, status=400)
    if len(content) > 20000:
        return JsonResponse({'error': 'Content must be 20000 characters or fewer'}, status=400)
    if image_urls and len(image_urls) > POST_IMAGE_MAX_COUNT:
        return JsonResponse({'error': f'Maximum {POST_IMAGE_MAX_COUNT} images per post'}, status=400)
    from api import polls as _polls
    poll_data, poll_error = _polls.clean_poll_input(poll_data)
    if poll_error:
        return JsonResponse({'error': poll_error}, status=400)
    is_anonymous = bool(data.get('isAnonymous') or data.get('is_anonymous'))
    from api import post_look as _look
    look, look_error = _look.clean(data.get('look'))
    if look_error:
        return JsonResponse({'error': look_error}, status=400)
    attachments, attach_error = _parse_web_attachments(data)
    if attach_error:
        return JsonResponse({'error': attach_error}, status=400)
    result = services.create_post(user, title, content, category, image_urls=image_urls, poll_data=poll_data,
                                  is_anonymous=is_anonymous, attachments=attachments,
                                  own_tag=bool(data.get('custom_category')), look=look)
    if result:
        _clear_page_cache()
        try:
            from django.template.loader import render_to_string
            from .view_helpers import _serialize_post
            from api.models import Post
            created_post_obj = Post.objects.select_related('user').filter(pk=result.get('id')).first()
            if created_post_obj:
                serialized = _serialize_post(created_post_obj, user_id=user.id)
                result['html'] = render_to_string('web/_forum_post_card.html', {'post': serialized, 'user': user, 'request': request}, request=request)
        except Exception as e:
            logger.warning('Failed to render post card HTML for ajax response: %s', e)
        return JsonResponse(result, status=201)
    return JsonResponse({'error': 'Missing fields'}, status=400)

@require_POST
@signed_in_member
def ajax_bookmark_toggle(request, user):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    target_type = data.get('target_type', '').strip()
    target_id = data.get('target_id', '').strip()
    if target_type not in ('post', 'reply', 'resource'):
        return JsonResponse({'error': 'Invalid target type'}, status=400)
    if not target_id:
        return JsonResponse({'error': 'target_id required'}, status=400)
    if target_type == 'post':
        if not Post.objects.filter(pk=target_id).exists():
            return JsonResponse({'error': 'Post not found'}, status=404)
    elif target_type == 'reply':
        if not Reply.objects.filter(pk=target_id).exists():
            return JsonResponse({'error': 'Reply not found'}, status=404)
    elif target_type == 'resource':
        if not Resource.objects.filter(pk=target_id).exists():
            return JsonResponse({'error': 'Resource not found'}, status=404)
    existing = Bookmark.objects.filter(user=user, target_type=target_type, target_id=target_id).first()
    if existing:
        existing.delete()
        return JsonResponse({'isBookmarked': False})
    Bookmark.objects.create(
        id=uuid_str(),
        user=user,
        target_type=target_type,
        target_id=target_id,
        created_at=now_ms(),
    )
    return JsonResponse({'isBookmarked': True})

@require_POST
def ajax_bookmark_check(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'isBookmarked': False})
    # Read from the POST JSON body first; fall back to GET query params for
    # backwards compatibility with older clients.
    target_type = ''
    target_id = ''
    if request.body:
        try:
            data = json.loads(request.body)
            target_type = str(data.get('target_type', '') or '').strip()
            target_id = str(data.get('target_id', '') or '').strip()
        except (json.JSONDecodeError, AttributeError):
            pass
    if not target_type:
        target_type = request.GET.get('target_type', '').strip()
    if not target_id:
        target_id = request.GET.get('target_id', '').strip()
    is_bookmarked = Bookmark.objects.filter(
        user_id=user_id, target_type=target_type, target_id=target_id
    ).exists()
    return JsonResponse({'isBookmarked': is_bookmarked})

@require_POST
@signed_in_member
def ajax_report(request, user):
    if _rate_limit(request, 'report', 10, 3600):
        return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    target_type = str(data.get('target_type', '') or '').strip()
    target_id = str(data.get('target_id', '') or '').strip()
    reason = str(data.get('reason', 'other') or 'other').strip()
    description = str(data.get('description', '') or '').strip()
    valid_types = {'post', 'reply', 'user', 'resource'}
    if target_type not in valid_types:
        return JsonResponse({'error': 'Invalid target type'}, status=400)
    if not target_id:
        return JsonResponse({'error': 'target_id required'}, status=400)
    if reason not in dict(Report.REASON_CHOICES):
        return JsonResponse({'error': 'Invalid reason'}, status=400)

    target_exists = {
        'post': lambda pk: Post.objects.filter(pk=pk).exists(),
        'reply': lambda pk: Reply.objects.filter(pk=pk).exists(),
        'user': lambda pk: User.objects.filter(pk=pk).exists(),
        'resource': lambda pk: Resource.objects.filter(pk=pk).exists(),
    }[target_type](target_id)
    if not target_exists:
        return JsonResponse({'error': 'Reported target no longer exists'}, status=404)

    detail_lines = []
    if description:
        detail_lines.append(description)
    context_path = str(data.get('context_path', '') or request.META.get('HTTP_REFERER', '') or '').strip()
    if context_path:
        detail_lines.append(f'Context: {context_path[:300]}')
    user_agent = str(request.META.get('HTTP_USER_AGENT', '') or '').strip()
    if user_agent:
        detail_lines.append(f'User-Agent: {user_agent[:300]}')
    description = '\n\n'.join(detail_lines)
    if len(description) > 2000:
        return JsonResponse({'error': 'Description must be 2000 characters or fewer'}, status=400)
    report = Report.objects.create(
        id=uuid_str(),
        reporter=user,
        target_type=target_type,
        target_id=target_id,
        reason=reason,
        description=description,
        status='open',
        created_at=now_ms(),
    )
    logger.info("ajax_report: user %s reported %s/%s (reason=%s)", user.username, target_type, target_id, reason)
    return JsonResponse({'success': True, 'id': report.id})

@require_POST
def ajax_archive_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    if reply.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    reply.is_archived = not reply.is_archived
    reply.save(update_fields=['is_archived'])
    _clear_page_cache()
    _rt.broadcast_reply_deleted(reply.post_id, reply_id, deleted_by='archive')
    return JsonResponse({'success': True, 'isArchived': reply.is_archived})

@require_POST
def ajax_delete_post(request, post_id):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    try:
        cur_user = User.objects.get(pk=user_id)
        is_admin = bool(getattr(cur_user, 'is_admin', False) or getattr(cur_user, 'moderator_level', 0) > 0)
    except User.DoesNotExist:
        is_admin = False
    if post.user_id != user_id and not is_admin:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    try:
        _cleanup.delete_post_with_cleanup(post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    _clear_page_cache()
    _rt.broadcast_post_deleted(post_id)
    return JsonResponse({'success': True})

def _parse_edit_attachments(data):
    """(cleaned, error_response) for the optional ordered `attachments` list of an edit.
    None means the client did not send the field, so the stored media stays as it is."""
    if 'attachments' not in data:
        return None, None
    raw = data.get('attachments')
    try:
        return validate_forum_attachments(raw if raw else []), None
    except ValidationError as exc:
        msg = exc.messages[0] if getattr(exc, 'messages', None) else 'Invalid attachments'
        return None, JsonResponse({'error': msg}, status=400)


def _replace_media(target, cleaned, now, user_id):
    """Swap a post's or reply's PostMedia for `cleaned`, in order, and log it in the edit history.
    Rows whose url survives keep their id, so a pure reorder never re-creates a file row."""
    is_post = isinstance(target, Post)
    rows = PostMedia.objects.filter(**({'post': target} if is_post else {'reply': target})).order_by('order', 'created_at')
    old = list(rows)
    if [m.url for m in old] == [a['url'] for a in cleaned]:
        return False
    by_url = {m.url: m for m in old}
    keep = set()
    for order, a in enumerate(cleaned):
        row = by_url.get(a['url'])
        if row:
            row.order = order
            row.name = a['name'] or row.name
            row.save(update_fields=['order', 'name'])
            keep.add(row.id)
        else:
            PostMedia.objects.create(
                id=uuid_str(), kind=a['kind'], url=a['url'], thumbnail_url=a.get('thumbnail_url', ''),
                name=a['name'], mime_type=a['mime_type'], size_bytes=a['size_bytes'], order=order, created_at=now,
                **({'post': target} if is_post else {'reply': target}))
    for m in old:
        if m.id not in keep:
            m.delete()
    EditHistory.objects.create(
        id=uuid_str(), target_type='post' if is_post else 'reply', target_id=target.id, field='attachments',
        old_value='\n'.join(m.url for m in old), new_value='\n'.join(a['url'] for a in cleaned),
        edited_by_id=user_id, edited_at=now)
    return True


@require_POST
def ajax_edit_post(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    if post.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    if 'title' in data and len(str(data['title']).strip()) > 200:
        return JsonResponse({'error': 'Title must be 200 characters or fewer'}, status=400)
    if 'content' in data and len(str(data['content']).strip()) > 20000:
        return JsonResponse({'error': 'Content must be 20000 characters or fewer'}, status=400)
    image_urls = data.get('image_urls', data.get('images', None))
    cleaned_image_urls = None
    if image_urls is not None:
        if not isinstance(image_urls, list):
            return JsonResponse({'error': 'image_urls must be a list'}, status=400)
        cleaned_image_urls = [str(url or '').strip() for url in image_urls if str(url or '').strip()]
        if len(cleaned_image_urls) > POST_IMAGE_MAX_COUNT:
            return JsonResponse({'error': f'Maximum {POST_IMAGE_MAX_COUNT} images per post'}, status=400)

    cleaned_media, bad = _parse_edit_attachments(data)
    if bad:
        return bad
    now = now_ms()
    if 'title' in data:
        title = str(data['title']).strip()
        EditHistory.objects.create(
            id=uuid_str(), target_type='post', target_id=post.id,
            field='title', old_value=post.title, new_value=title,
            edited_by_id=user_id, edited_at=now
        )
        post.title = title
    if 'content' in data:
        content = str(data['content']).strip()
        content = services._prep_inline_images(content)[0]
        EditHistory.objects.create(
            id=uuid_str(), target_type='post', target_id=post.id,
            field='content', old_value=post.content, new_value=content,
            edited_by_id=user_id, edited_at=now
        )
        post.content = content
    if 'category' in data:
        category = str(data['category']).strip()
        EditHistory.objects.create(
            id=uuid_str(), target_type='post', target_id=post.id,
            field='category', old_value=post.category, new_value=category,
            edited_by_id=user_id, edited_at=now
        )
        post.category = category
    if cleaned_image_urls is not None:
        old_urls = list(PostImage.objects.filter(post=post).order_by('order', 'created_at').values_list('image_url', flat=True))
        if old_urls != cleaned_image_urls:
            EditHistory.objects.create(
                id=uuid_str(), target_type='post', target_id=post.id,
                field='images', old_value='\n'.join(old_urls), new_value='\n'.join(cleaned_image_urls),
                edited_by_id=user_id, edited_at=now
            )
            PostImage.objects.filter(post=post).delete()
            for order, url in enumerate(cleaned_image_urls):
                PostImage.objects.create(
                    id=uuid_str(), post=post, image_url=url, order=order, created_at=now
                )
    if cleaned_media is not None:
        _replace_media(post, cleaned_media, now, user_id)
    post.is_edited = True
    post.edited_at = now
    post.save()
    _clear_page_cache()
    _rt.broadcast_post_updated(post.id, {
        'title': post.title, 'content': post.content, 'category': post.category,
        'is_edited': True, 'edited_at': now,
        'images': _serialize_post_images(post.id),
    })
    return JsonResponse(_serialize_post(post, user_id))

@require_POST
def ajax_archive_post(request, post_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    if post.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    post.is_archived = not post.is_archived
    post.save(update_fields=['is_archived'])
    _clear_page_cache()
    _rt.broadcast_post_deleted(post_id)
    return JsonResponse({'success': True, 'isArchived': post.is_archived})

@require_POST
def ajax_edit_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    if reply.user_id != user_id:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    content = data.get('content', '').strip()
    cleaned_media, bad = _parse_edit_attachments(data)
    if bad:
        return bad
    if not content and not (cleaned_media if cleaned_media is not None else PostMedia.objects.filter(reply=reply).exists()):
        return JsonResponse({'error': 'Content required'}, status=400)
    content = services._prep_inline_images(content)[0] if content else ''
    now = now_ms()
    if cleaned_media is not None:
        _replace_media(reply, cleaned_media, now, user_id)
    EditHistory.objects.create(
        id=uuid_str(), target_type='reply', target_id=reply.id,
        field='content', old_value=reply.content, new_value=content,
        edited_by_id=user_id, edited_at=now
    )
    reply.content = content
    reply.is_edited = True
    reply.edited_at = now
    reply.save()
    _clear_page_cache()
    _rt.broadcast_reply_updated(reply.post_id, reply.id, {
        'content': reply.content, 'is_edited': True, 'edited_at': now,
    })
    return JsonResponse(_serialize_reply(reply, user_id))

@require_POST
def ajax_delete_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        reply = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    try:
        cur_user = User.objects.get(pk=user_id)
        is_admin = bool(getattr(cur_user, 'is_admin', False) or getattr(cur_user, 'moderator_level', 0) > 0)
    except User.DoesNotExist:
        is_admin = False
    if reply.user_id != user_id and not is_admin:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    try:
        _cleanup.delete_reply_with_cleanup(reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    _clear_page_cache()
    _rt.broadcast_reply_deleted(reply.post_id, reply_id, deleted_by=str(user_id))
    return JsonResponse({'success': True})

def ajax_edit_history(request, target_type, target_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    if target_type not in ('post', 'reply'):
        return JsonResponse({'error': 'Invalid target type'}, status=400)
    entries = EditHistory.objects.filter(
        target_type=target_type, target_id=target_id
    ).select_related('edited_by').order_by('-edited_at')[:20]
    data = []
    for e in entries:
        data.append({
            'id': e.id, 'field': e.field, 'oldValue': e.old_value, 'newValue': e.new_value,
            'editedByUsername': e.edited_by.username, 'editedByPhotoUrl': _avatar_url(e.edited_by),
            'editedAt': e.edited_at,
        })
    return JsonResponse(data, safe=False)

def ajax_reply_thread(request, reply_id):
    user_id = _get_user_id(request)
    try:
        parent = Reply.objects.get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    parent_data = _serialize_reply(parent, user_id)
    parent_data['authorFollowed'] = False
    if user_id and parent.user_id != user_id:
        parent_data['authorFollowed'] = Follow.objects.filter(
            follower_id=user_id, following_id=parent.user_id
        ).exists()
    all_descendants = Reply.objects.select_related('user', 'post').filter(
        post_id=parent.post_id, parent_reply__isnull=False
    ).order_by('created_at')
    all_replies = _serialize_replies(all_descendants, user_id)
    id_to_reply = {r['id']: r for r in all_replies}
    children_map = {}
    for r in all_replies:
        pid = r['parentReplyId']
        children_map.setdefault(pid, []).append(r)
    def build_tree(parent_id):
        children = children_map.get(parent_id, [])
        for child in children:
            child['children'] = build_tree(child['id'])
        return children
    thread_replies = build_tree(reply_id)
    return JsonResponse({
        'parent': parent_data,
        'replies': thread_replies,
    }, safe=False)

def ajax_user_popup(request, username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    user_id = _get_user_id(request)
    viewer_user = _viewer_for_locked_check(user_id, u)
    is_private = not _can_view_locked_profile(viewer_user, u)
    data = {
        'id': u.id,
        'username': u.username,
        'displayName': u.display_name or u.username,
        'photoUrl': _avatar_url(u),
        'bio': '' if is_private else (u.bio or ''),
        'classLevel': '' if is_private else (u.class_level or ''),
        'isLocked': u.is_locked,
        'badgeInfo': _user_badge_info(u),
    }
    if not is_private:
        data['postCount'] = Post.objects.filter(user_id=u.id, is_anonymous=False).count()
        data['replyCount'] = Reply.objects.filter(user_id=u.id, is_anonymous=False).count()
        data['followerCount'] = getattr(u, 'follower_count', 0) or 0
    else:
        data['postCount'] = 0
        data['replyCount'] = 0
        data['followerCount'] = 0
    if user_id:
        data['isFollowing'] = Follow.objects.filter(follower_id=user_id, following_id=u.id).exists()
        data['isSelf'] = (user_id == u.id)
    else:
        data['isFollowing'] = False
        data['isSelf'] = False
    return JsonResponse(data)

def ajax_user_search(request):
    by_ip = not _get_user_id(request)
    if _rate_limit(request, 'user_search', 60, 60, by_ip=by_ip):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse([], safe=False)
    # One letter is enough for the composer's @mention list: people whose handle starts with it. Longer terms
    # match anywhere in the handle or the display name; handle-prefix matches come first.
    from django.db.models import Case, IntegerField, Q, Value, When
    match = Q(username__istartswith=q) if len(q) < 2 else (Q(username__icontains=q) | Q(display_name__icontains=q))
    users = User.objects.filter(
        match, is_locked=False, email_verified=True
    ).annotate(
        _rank=Case(When(username__istartswith=q, then=Value(0)), default=Value(1), output_field=IntegerField())
    ).order_by('_rank', 'username').values('id', 'username', 'display_name', 'photo_url')[:8]
    results = []
    for u in users:
        results.append({
            'id': u['id'],
            'username': u['username'],
            'displayName': u['display_name'] or u['username'],
            'photoUrl': u['photo_url'] or '',
        })
    return JsonResponse(results, safe=False)

def ajax_check_username(request):
    username = request.GET.get('username', '').strip()
    if not username:
        return JsonResponse({'available': False})
    result = services.check_username_available(username)
    return JsonResponse(result)

@require_POST
def ajax_set_theme(request):
    try:
        data = json.loads(request.body)
        theme = data.get('theme', 'light')
        request.session['theme'] = 'dark' if theme == 'dark' else 'light'
    except (json.JSONDecodeError, KeyError):
        pass
    return JsonResponse({'status': 'ok'})

@require_POST
def ajax_follow_user(request, user_id):
    user_id_obj = _get_user_id(request)
    if not user_id_obj:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    if _rate_limit(request, 'follow_user', 30, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        user = User.objects.get(pk=user_id_obj)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    desired = None
    try:
        payload = json.loads(request.body or b'{}')
        desired = (payload.get('action') or payload.get('intent') or '').strip().lower() or None
    except Exception:
        desired = None
    result = services.toggle_follow(user, user_id, desired=desired)
    if isinstance(result, tuple):
        return JsonResponse(result[0], status=result[1])
    return JsonResponse(result)

def ajax_user_photos(request):
    token = _get_valid_token(request)
    if not token:
        return JsonResponse({'error': 'Please log in again.'}, status=401)

    from api.models import UserPhoto
    try:
        current_user = get_user_by_auth_token(token)
    except User.DoesNotExist:
        api.clear_session_auth(request)
        return JsonResponse({'error': 'Please log in again.'}, status=401)

    if request.method == 'GET':
        try:
            photos = UserPhoto.objects.filter(user=current_user)
            # Manual serialization to avoid DRF serializer context issues in vanilla Django views
            photos_data = []
            for photo in photos:
                photos_data.append({
                    'id': photo.id,
                    'url': photo.url,
                    'uploaded_at': photo.uploaded_at,
                    'is_current': photo.is_current,
                })
            return JsonResponse({'photos': photos_data})
        except Exception as e:
            logger.error("Failed to retrieve user photos: %s", e)
            return JsonResponse({'error': f"Failed to retrieve photos: {str(e)}"}, status=500)

    elif request.method == 'POST':
        from django.db import transaction

        file_obj = request.FILES.get('file')
        if file_obj:
            try:
                url = save_profile_image_upload(request, current_user, file_obj)
            except ValidationError as exc:
                return JsonResponse({'error': ' '.join(exc.messages)}, status=400)
        else:
            # Fallback to URL
            url = ''
            content_type = request.META.get('CONTENT_TYPE', '')
            if 'application/json' in content_type:
                try:
                    data = json.loads(request.body)
                    url = data.get('url', '').strip()
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Invalid JSON request'}, status=400)
            else:
                url = request.POST.get('url', '').strip()

            if not url:
                return JsonResponse({'error': 'Either URL or file is required'}, status=400)
            try:
                url = validate_profile_photo_url(url)
            except ValidationError as exc:
                return JsonResponse({'error': ' '.join(exc.messages)}, status=400)

        try:
            with transaction.atomic():
                UserPhoto.objects.filter(user=current_user).update(is_current=False)
                photo = UserPhoto.objects.create(
                    user=current_user,
                    url=url,
                    uploaded_at=now_ms(),
                    is_current=True,
                )
                current_user.photo_url = url
                current_user.save(update_fields=['photo_url'])
        except Exception as e:
            logger.error("Failed to save user photo database record: %s", e)
            return JsonResponse({'error': f"Database error (run migrations on live server): {str(e)}"}, status=500)

        # Update user in session
        try:
            user_data = api.get_session_user(request)
            if user_data:
                user_data['photo_url'] = url
                user_data['photoUrl'] = url
                api.set_session_auth(request, token, user_data)
        except Exception as e:
            logger.error("Failed to update user session avatar: %s", e)

        return JsonResponse({
            'id': photo.id,
            'url': url,
            'uploaded_at': photo.uploaded_at,
            'is_current': True
        }, status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@require_POST
@signed_in_member
def ajax_set_password(request, user):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    password = data.get('password', '')
    if not password or len(password) < 8:
        return JsonResponse({'error': 'Password must be at least 8 characters'}, status=400)
    result, status_code = services.set_password(user, password)
    if result.get('status') == 'success':
        _clear_page_cache()
        user_data = _normalize_user_data(UserSerializer(user).data)
        user_data['hasPassword'] = True
        api.set_session_auth(request, api.get_session_token(request), user_data)
        return JsonResponse({'status': 'success', 'message': 'Password set successfully'})
    return JsonResponse({'error': result.get('error', 'Failed to set password')}, status=status_code or 400)

@require_POST
@signed_in_member
def ajax_change_password(request, user):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    current_password = data.get('currentPassword', '')
    new_password = data.get('newPassword', '')
    if not current_password or not new_password:
        return JsonResponse({'error': 'Current password and new password are required'}, status=400)
    result, status_code = services.change_password(user, current_password, new_password)
    if result.get('status') == 'success':
        _clear_page_cache()
        new_token = result.get('authToken') or api.get_session_token(request)
        user_data = _normalize_user_data(UserSerializer(user).data)
        api.set_session_auth(request, new_token, user_data)
        return JsonResponse({'status': 'success', 'message': 'Password changed successfully'})
    return JsonResponse({'error': result.get('error', 'Failed to change password')}, status=status_code or 400)

@require_POST
@signed_in_member
def ajax_activate_photo(request, photo_id, user):
    result = services.activate_photo(user, photo_id)
    if result:
        new_url = result.get('photo_url') or result.get('url')
        if new_url:
            user_data = api.get_session_user(request)
            if user_data:
                user_data['photo_url'] = new_url
                user_data['photoUrl'] = new_url
                token = api.get_session_token(request)
                if token:
                    api.set_session_auth(request, token, user_data)
        return JsonResponse(result)
    return JsonResponse({'error': 'Failed'}, status=500)


@require_POST
@signed_in_member
def ajax_upload_post_image(request, user):
    if _rate_limit(request, 'upload_post_image', 20, 3600):
        return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)
    file_obj = request.FILES.get('image')
    if not file_obj:
        return JsonResponse({'error': 'No image file provided'}, status=400)
    try:
        url = save_post_image_upload(request, file_obj)
    except ValidationError as e:
        logger.warning('Upload rejected: name=%s content_type=%s size=%s error=%s',
                       getattr(file_obj, 'name', '?'), getattr(file_obj, 'content_type', '?'),
                       getattr(file_obj, 'size', '?'), e)
        return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'url': url})


@require_POST
@signed_in_member
def ajax_poll_vote(request, poll_id, user):
    if _rate_limit(request, 'poll_vote', 30, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    option_ids = data.get('option_ids', [])
    if not option_ids:
        option_id = data.get('option_id', '').strip()
        if option_id:
            option_ids = [option_id]
    if not option_ids:
        return JsonResponse({'error': 'Option ID is required'}, status=400)
    result = services.vote_poll(user, poll_id, option_ids)
    if isinstance(result, tuple):
        result, status_code = result
        if 'error' in result:
            return JsonResponse(result, status=status_code)
    return JsonResponse(result)


@require_POST
def ajax_poll_option(request, poll_id):
    """Add an option to a poll that allows it (JSON {text, vote})."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    if _rate_limit(request, 'poll_option', 12, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        user = User.objects.get(pk=user_id)
        data = json.loads(request.body or b'{}')
    except (User.DoesNotExist, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid request'}, status=400)
    from api import polls as _polls
    payload, code = _polls.add_option(user, poll_id, data.get('text', ''), vote=bool(data.get('vote', True)))
    if code < 300:
        _clear_page_cache()
    return JsonResponse(payload, status=code)


@require_POST
@signed_in_member
def ajax_poll_retract(request, poll_id, user):
    """Take the viewer's vote back so they can pick again."""
    from api import polls as _polls
    payload, code = _polls.retract_vote(user, poll_id)
    return JsonResponse(payload, status=code)


@require_POST
def ajax_post_view(request, post_id):
    """Record a view / dwell time for a post (guests and members)."""
    from api import post_reach
    from api.models import Post as _Post
    try:
        post = _Post.objects.get(pk=post_id)
    except _Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    try:
        data = json.loads(request.body or b'{}')
    except json.JSONDecodeError:
        data = {}
    user_id = _get_user_id(request)
    user = User.objects.filter(pk=user_id).first() if user_id else None
    try:
        dwell = int(data.get('dwell_ms') or 0)
    except (TypeError, ValueError):
        dwell = 0
    out = post_reach.record_view(request, post, user, surface=str(data.get('surface') or ''), dwell_ms=dwell)
    return JsonResponse(out)


@require_POST
def ajax_post_impressions(request):
    from api import post_reach
    try:
        data = json.loads(request.body or b'{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    ids = data.get('ids')
    if not isinstance(ids, list):
        return JsonResponse({'error': 'ids must be a list'}, status=400)
    if _rate_limit(request, 'post_impressions', 60, 60):
        return JsonResponse({'recorded': 0}, status=429)
    return JsonResponse({'recorded': post_reach.record_impressions(request, ids)})


def ajax_post_insights(request, post_id):
    """Author (or staff) insights for one post, as JSON."""
    from api import post_insights
    from api.models import Post as _Post
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    user = User.objects.filter(pk=user_id).first()
    try:
        post = _Post.objects.get(pk=post_id)
    except _Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    if not user or (post.user_id != user.id and not user.is_admin):
        return JsonResponse({'error': 'Only the author can see these insights'}, status=403)
    try:
        days = int(request.GET.get('days', 30))
    except ValueError:
        days = 30
    return JsonResponse(post_insights.build(post, days=days, staff=bool(user.is_admin)))


@require_POST
def ajax_accept_follow_request(request, request_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    
    from api.models import FollowRequest, Follow
    from api.utils import now_ms
    try:
        req = FollowRequest.objects.get(pk=request_id, receiver_id=user_id)
    except FollowRequest.DoesNotExist:
        return JsonResponse({'error': 'Follow request not found.'}, status=404)
        
    sender = req.sender
    receiver = req.receiver
    
    with transaction.atomic():
        req.delete()
        Follow.objects.get_or_create(
            follower=sender,
            following=receiver,
            defaults={'created_at': now_ms()}
        )
        follower_count = Follow.objects.filter(following=receiver).count()
        following_count = Follow.objects.filter(follower=sender).count()
        User.objects.filter(pk=receiver.id).update(follower_count=follower_count)
        User.objects.filter(pk=sender.id).update(following_count=following_count)
        
    from api import notifications as _notif
    from api import realtime as _rt
    _notif.notify_cancel_follow_request(sender.id, receiver.id)
    _notif.notify_new_follow(sender.id, receiver.id)
    _rt.broadcast_follow_changed(receiver.id, follower_count)
    
    return JsonResponse({'status': 'success'})


@require_POST
def ajax_reject_follow_request(request, request_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
        
    from api.models import FollowRequest
    try:
        req = FollowRequest.objects.get(pk=request_id, receiver_id=user_id)
    except FollowRequest.DoesNotExist:
        return JsonResponse({'error': 'Follow request not found.'}, status=404)
        
    sender_id = req.sender_id
    req.delete()
    
    from api import notifications as _notif
    _notif.notify_cancel_follow_request(sender_id, user_id)
    
    return JsonResponse({'status': 'success'})


@require_POST
def ajax_ai_feedback(request):
    """Record thumbs up/down on an AI reply (Neby chat / admin chat / elsewhere)."""
    import time, uuid as _uuid
    user_id = _get_user_id(request)
    try:
        data = json.loads(request.body) if request.body else {}
    except ValueError:
        return JsonResponse({'error': 'Invalid request body'}, status=400)
    try:
        vote = int(data.get('vote') or 0)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid vote'}, status=400)
    if vote not in (1, -1):
        return JsonResponse({'error': 'Invalid vote'}, status=400)
    if _rate_limit(request, 'ai_feedback', 30, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    surface = str(data.get('surface') or 'neby')[:30]
    AiFeedback.objects.create(
        id=str(_uuid.uuid4()),
        user_id=str(user_id or ''),
        surface=surface,
        vote=vote,
        provider=str(data.get('provider') or '')[:60],
        model_name=str(data.get('modelName') or data.get('model') or '')[:120],
        query=str(data.get('query') or '')[:5000],
        created_at=int(time.time() * 1000),
    )
    return JsonResponse({'ok': True})