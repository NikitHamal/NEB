"""
Direct service functions for web views to call instead of HTTP API roundtrips.
These replicate the business logic from api/views.py but return Python dicts
instead of DRF Response objects, and accept User objects instead of DRF requests.
"""
import logging
import re

from django.core.cache import cache
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import User, Post, PostLike, PostImage, Poll, PollOption, PollVote, Reply, ReplyLike, Follow, UserPhoto, EditHistory, FollowRequest
from .models import Resource, ResourceLike, ResourceComment, ResourceCommentLike, Bookmark, Notification, FCMToken, ResourceRequest, AccountDeletionRequest
from .security import hash_password, issue_auth_token, verify_password, validate_profile_photo_url, validate_external_https_url, POST_IMAGE_MAX_COUNT
from .utils import now_ms, uuid_str
from . import counters as _counters
from . import notifications as _notif
from . import neby as _neby
from . import realtime as _rt
from . import content_images as _cimg

logger = logging.getLogger(__name__)


def _prep_inline_images(content):
    """Sanitise [[img:ID]] tokens in user content and flag the referenced
    uploads as used. Returns (cleaned_content, referenced_ids)."""
    cleaned = _cimg.clean_content(content)
    ids = _cimg.extract_image_ids(cleaned)
    if ids:
        _cimg.mark_used(ids)
    return cleaned, ids


def toggle_post_like(user, post_id):
    with transaction.atomic():
        try:
            post = Post.objects.select_for_update().get(pk=post_id)
        except Post.DoesNotExist:
            raise
        like, created = PostLike.objects.get_or_create(post=post, user=user)
        if created:
            Post.objects.filter(pk=post_id).update(thumbs_up_count=F('thumbs_up_count') + 1)
            is_thumbed_up = True
            current_count = post.thumbs_up_count + 1
            _counters.increment_user_likes_given(user.id)
            if post.user_id != user.id:
                _counters.increment_user_likes_received(post.user_id)
            _notif.notify_post_liked(user.id, post_id)
        else:
            like.delete()
            Post.objects.filter(pk=post_id, thumbs_up_count__gt=0).update(thumbs_up_count=F('thumbs_up_count') - 1)
            is_thumbed_up = False
            current_count = max(post.thumbs_up_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if post.user_id != user.id:
                _counters.decrement_user_likes_received(post.user_id)
            _notif.notify_post_unliked(user.id, post_id)
    _rt.broadcast_post_like_changed(post_id, current_count, is_thumbed_up_by_viewer_hint=is_thumbed_up, user_id=str(user.id))
    return {'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up}


def toggle_reply_like(user, reply_id):
    with transaction.atomic():
        try:
            reply = Reply.objects.select_for_update().get(pk=reply_id)
        except Reply.DoesNotExist:
            raise
        like, created = ReplyLike.objects.get_or_create(reply=reply, user=user)
        if created:
            Reply.objects.filter(pk=reply_id).update(thumbs_up_count=F('thumbs_up_count') + 1)
            is_thumbed_up = True
            current_count = reply.thumbs_up_count + 1
            _counters.increment_user_likes_given(user.id)
            if reply.user_id != user.id:
                _counters.increment_user_likes_received(reply.user_id)
            _notif.notify_reply_liked(user.id, reply_id)
        else:
            like.delete()
            Reply.objects.filter(pk=reply_id, thumbs_up_count__gt=0).update(thumbs_up_count=F('thumbs_up_count') - 1)
            is_thumbed_up = False
            current_count = max(reply.thumbs_up_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if reply.user_id != user.id:
                _counters.decrement_user_likes_received(reply.user_id)
            _notif.notify_reply_unliked(user.id, reply_id)
    _rt.broadcast_reply_like_changed(reply.post_id, reply_id, current_count, is_thumbed_up_by_viewer_hint=is_thumbed_up, user_id=str(user.id))
    return {'thumbsUpCount': current_count, 'isThumbedUp': is_thumbed_up}


def create_reply(user, post_id, content, parent_reply_id=None, is_anonymous=False, attachments=None):
    if not getattr(user, 'email_verified', False):
        return None
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return None
    content = content.strip()
    if not content and not attachments:
        return None
    if parent_reply_id and not Reply.objects.filter(pk=parent_reply_id, post_id=post_id).exists():
        # Invalid parent reply (missing or belongs to another post)
        return None
    content, _img_ids = _prep_inline_images(content)
    now = now_ms()
    with transaction.atomic():
        reply = Reply.objects.create(
            id=uuid_str(),
            post=post,
            parent_reply_id=parent_reply_id,
            user=user,
            content=content,
            thumbs_up_count=0,
            reply_count=0,
            is_anonymous=bool(is_anonymous),
            created_at=now,
        )
        Post.objects.filter(pk=post.pk).update(reply_count=F('reply_count') + 1)
        if parent_reply_id:
            Reply.objects.filter(pk=parent_reply_id).update(reply_count=F('reply_count') + 1)
        if attachments:
            from .models import PostMedia
            for order, item in enumerate(attachments):
                PostMedia.objects.create(
                    id=uuid_str(), reply=reply,
                    kind=item['kind'], url=item['url'], name=item['name'],
                    mime_type=item['mime_type'], size_bytes=item['size_bytes'],
                    order=order, created_at=now,
                )
    _counters.increment_user_reply_count(user.id)
    _notif.notify_new_reply(user.id, post_id, reply.id, anonymous_actor=is_anonymous)
    if parent_reply_id:
        _notif.notify_reply_to_reply(user.id, parent_reply_id, post_id, reply.id, anonymous_actor=is_anonymous)
    _neby.enqueue_if_reply_mention(reply)
    _notif.send_mention_all_if_eligible(user, content, 'reply', reply.id)
    from .serializers import ReplySerializer
    reply_data = ReplySerializer(reply).data
    _rt.broadcast_reply_created(post_id, reply_data)
    return reply_data


def create_post(user, title, content, category, image_urls=None, poll_data=None,
                is_anonymous=False, attachments=None):
    if not getattr(user, 'email_verified', False):
        return None
    title = title.strip()
    content = content.strip()
    category = category.strip()
    if not title or not content or not category:
        return None
    content, _img_ids = _prep_inline_images(content)
    now = now_ms()
    post = Post.objects.create(
        id=uuid_str(),
        user=user,
        title=title,
        content=content,
        category=category,
        thumbs_up_count=0,
        reply_count=0,
        is_anonymous=bool(is_anonymous),
        created_at=now,
    )
    if image_urls:
        for i, url in enumerate(image_urls[:POST_IMAGE_MAX_COUNT]):
            PostImage.objects.create(
                id=uuid_str(),
                post=post,
                image_url=url,
                order=i,
                created_at=now,
            )
    if attachments:
        from .models import PostMedia
        for order, item in enumerate(attachments):
            PostMedia.objects.create(
                id=uuid_str(), post=post,
                kind=item['kind'], url=item['url'], name=item['name'],
                mime_type=item['mime_type'], size_bytes=item['size_bytes'],
                order=order, created_at=now,
            )
    if poll_data:
        poll = Poll.objects.create(
            id=uuid_str(),
            post=post,
            question=poll_data.get('question', ''),
            poll_type=poll_data.get('poll_type', 'voting'),
            allow_multiple=poll_data.get('allow_multiple', False),
            explanation=poll_data.get('explanation', ''),
            duration_ms=poll_data.get('duration_ms', 0),
            total_votes=0,
            created_at=now,
        )
        poll_options = []
        for i, opt in enumerate(poll_data.get('options', [])):
            if isinstance(opt, dict):
                opt_text = opt.get('text', '').strip()
                is_correct = opt.get('is_correct', False)
            else:
                opt_text = opt.strip()
                is_correct = False
            if opt_text:
                poll_options.append(
                    PollOption(
                        id=uuid_str(),
                        poll=poll,
                        text=opt_text,
                        is_correct=is_correct,
                        vote_count=0,
                        order=i,
                    )
                )
        if poll_options:
            PollOption.objects.bulk_create(poll_options)
    _counters.increment_user_post_count(user.id)
    _neby.enqueue_if_post_mention(post)
    _notif.send_mention_all_if_eligible(user, f'{title} {content}', 'post', post.id)
    from .serializers import PostSerializer
    post_data = PostSerializer(post).data
    _rt.broadcast_post_created(post_data)
    return post_data


def vote_poll(user, poll_id, option_ids):
    """Vote on a poll. option_ids can be a single id or a list for multiple selection."""
    if isinstance(option_ids, str):
        option_ids = [option_ids]
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        return {'error': 'Poll not found'}, 404
    if poll.is_expired:
        return {'error': 'This poll has expired'}, 400
    valid_options = []
    for oid in option_ids:
        try:
            opt = PollOption.objects.get(pk=oid, poll=poll)
            valid_options.append(opt)
        except PollOption.DoesNotExist:
            return {'error': 'Invalid poll option'}, 400
    if not valid_options:
        return {'error': 'No options selected'}, 400
    if not poll.allow_multiple and len(valid_options) > 1:
        return {'error': 'This poll allows only one option'}, 400
    with transaction.atomic():
        if poll.allow_multiple:
            existing = PollVote.objects.filter(poll=poll, user=user, option__in=valid_options)
            if existing.exists():
                return {'error': 'You have already voted on one or more of these options'}, 400
            for opt in valid_options:
                PollVote.objects.create(
                    id=uuid_str(),
                    poll=poll,
                    option=opt,
                    user=user,
                    created_at=now_ms(),
                )
                PollOption.objects.filter(pk=opt.id).update(vote_count=F('vote_count') + 1)
            Poll.objects.filter(pk=poll_id).update(total_votes=F('total_votes') + len(valid_options))
        else:
            existing = PollVote.objects.filter(poll=poll, user=user).first()
            if existing:
                return {'error': 'You have already voted on this poll'}, 400
            opt = valid_options[0]
            PollVote.objects.create(
                id=uuid_str(),
                poll=poll,
                option=opt,
                user=user,
                created_at=now_ms(),
            )
            PollOption.objects.filter(pk=opt.id).update(vote_count=F('vote_count') + 1)
            Poll.objects.filter(pk=poll_id).update(total_votes=F('total_votes') + 1)
    poll.refresh_from_db()
    options = list(PollOption.objects.filter(poll=poll).order_by('order'))
    return {
        'id': poll.id,
        'question': poll.question,
        'pollType': poll.poll_type,
        'allowMultiple': poll.allow_multiple,
        'explanation': poll.explanation,
        'total_votes': poll.total_votes,
        'isExpired': poll.is_expired,
        'options': [{'id': o.id, 'text': o.text, 'is_correct': o.is_correct, 'vote_count': o.vote_count, 'order': o.order} for o in options],
        'userVote': [str(o.id) for o in valid_options] if poll.allow_multiple else str(valid_options[0].id),
    }, 200


def toggle_follow(user, target_user_id, desired=None):
    """Follow/unfollow a user or send/cancel follow request for private accounts.

    desired may be "follow" or "unfollow" for idempotent UI calls. When omitted,
    the toggle behavior is preserved.
    """
    desired = (desired or '').strip().lower() or None
    if desired not in (None, 'follow', 'unfollow'):
        desired = None
    if str(user.id) == str(target_user_id):
        return {'error': 'You cannot follow yourself'}, 400
    try:
        target_user = User.objects.get(pk=target_user_id)
    except User.DoesNotExist:
        return {'error': 'User not found'}, 404

    is_following = False
    requested = False
    notify_follow = False
    notify_unfollow = False
    notify_request = False
    notify_cancel_request = False
    
    with transaction.atomic():
        # Check if already following
        existing_follow = Follow.objects.select_for_update().filter(follower=user, following=target_user).first()
        
        # Check if there is a pending request
        existing_request = FollowRequest.objects.select_for_update().filter(sender=user, receiver=target_user).first()
        
        if target_user.is_locked:
            # For private profiles:
            if existing_follow:
                # If already following, we can unfollow
                if desired == 'follow':
                    is_following = True
                else:
                    existing_follow.delete()
                    is_following = False
                    notify_unfollow = True
            elif existing_request:
                # If there's a pending request, we can cancel it
                if desired == 'follow':
                    requested = True
                else:
                    existing_request.delete()
                    requested = False
                    notify_cancel_request = True
            else:
                # Neither exists
                if desired == 'unfollow':
                    pass
                else:
                    # Create a new follow request
                    FollowRequest.objects.create(
                        id=uuid_str(),
                        sender=user,
                        receiver=target_user,
                        created_at=now_ms()
                    )
                    requested = True
                    notify_request = True
        else:
            # For public profiles (standard logic):
            if existing_follow:
                if desired == 'follow':
                    is_following = True
                else:
                    existing_follow.delete()
                    is_following = False
                    notify_unfollow = True
            else:
                if desired == 'unfollow':
                    pass
                else:
                    Follow.objects.create(follower=user, following=target_user, created_at=now_ms())
                    is_following = True
                    notify_follow = True

        follower_count = Follow.objects.filter(following=target_user).count()
        following_count = Follow.objects.filter(follower=user).count()
        is_mutual = bool(is_following and Follow.objects.filter(follower=target_user, following=user).exists())
        User.objects.filter(pk=target_user.id).update(follower_count=follower_count)
        User.objects.filter(pk=user.id).update(following_count=following_count)

    if notify_follow:
        _notif.notify_new_follow(user.id, target_user.id)
    elif notify_unfollow:
        _notif.notify_unfollow(user.id, target_user.id)
    elif notify_request:
        _notif.notify_new_follow_request(user.id, target_user.id)
    elif notify_cancel_request:
        _notif.notify_cancel_follow_request(user.id, target_user.id)
        
    _rt.broadcast_follow_changed(target_user.id, follower_count)
    
    return {
        'is_following': is_following,
        'requested': requested,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_mutual': is_mutual,
    }, 200

def check_username_available(username):
    exists = User.objects.filter(username__iexact=username).exists()
    return {'available': not exists}


def avatar_path(username):
    from urllib.parse import quote
    return '/avatar/%s/' % quote((username or ''), safe='')


AVATAR_BACKGROUNDS = ('', 'square', 'circle', 'squircle')
AVATAR_ANIMATIONS = ('', 'bob', 'wave', 'spin', 'pulse')
AVATAR_SHAPES = ('', 'round', 'organic', 'boxy', 'capsule', 'nub', 'cloud',
                 'droplet', 'hexagon', 'sun', 'triangle')
AVATAR_EXPRESSIONS = ('', 'idle', 'happy', 'sad', 'mad', 'surprised', 'wink',
                      'sleepy', 'smug', 'unsure', 'scared', 'love', 'shy',
                      'sick', 'thinking')
_HEX_COLOR_RE = re.compile(r'^#[0-9a-fA-F]{6}$')


def avatar_options_for(user):
    opts = {}
    if getattr(user, 'avatar_hue', -1) >= 0:
        opts['hue'] = int(user.avatar_hue)
    if getattr(user, 'avatar_tone', -1.0) >= 0:
        opts['tone'] = float(user.avatar_tone)
    bg = getattr(user, 'avatar_bg', '') or ''
    if bg in AVATAR_BACKGROUNDS[1:]:
        opts['background'] = bg
    anim = getattr(user, 'avatar_anim', '') or ''
    if anim in AVATAR_ANIMATIONS[1:]:
        opts['anim'] = anim
    shape = getattr(user, 'avatar_shape', '') or ''
    if shape in AVATAR_SHAPES[1:]:
        opts['shape'] = shape
    expression = getattr(user, 'avatar_expression', '') or ''
    if expression in AVATAR_EXPRESSIONS[1:]:
        opts['expression'] = expression
    color = getattr(user, 'avatar_color', '') or ''
    if _HEX_COLOR_RE.match(color):
        opts['color'] = color.lower()
    bgcolor = getattr(user, 'avatar_bg_color', '') or ''
    if _HEX_COLOR_RE.match(bgcolor):
        opts['bgcolor'] = bgcolor.lower()
    eyecolor = getattr(user, 'avatar_eye_color', '') or ''
    if _HEX_COLOR_RE.match(eyecolor):
        opts['eyecolor'] = eyecolor.lower()
    return opts


def avatar_url_for(user):
    from urllib.parse import quote as _q
    username = getattr(user, 'username', '') or ''
    opts = avatar_options_for(user)
    url = '/avatar/%s/' % _q(username, safe='')
    if opts:
        url += '?' + '&'.join('%s=%s' % (k, _q(str(v), safe='')) for k, v in sorted(opts.items()))
    return url


def avatar_or_photo_url(user):
    """use_pp → generated avatar; else stored photo; else generated avatar so
    every user gets a consistent identity everywhere."""
    if getattr(user, 'avatar_use_pp', False):
        return avatar_url_for(user)
    photo = getattr(user, 'photo_url', None) or ''
    return photo or avatar_url_for(user)


def save_avatar_customization(user, payload=None, user_id=None):
    payload = payload or {}
    bg = str(payload.get('background', '') or '').strip()
    if bg not in AVATAR_BACKGROUNDS:
        return {'error': 'background must be one of: square, circle, squircle'}, 400
    anim = str(payload.get('anim', '') or '').strip()
    if anim not in AVATAR_ANIMATIONS:
        return {'error': 'anim must be one of: bob, wave, spin, pulse'}, 400
    shape = str(payload.get('shape', '') or '').strip()
    if shape not in AVATAR_SHAPES:
        return {'error': 'shape must be one of: ' + ', '.join(AVATAR_SHAPES[1:])}, 400
    expression = str(payload.get('expression', '') or '').strip()
    if expression not in AVATAR_EXPRESSIONS:
        return {'error': 'expression must be one of: ' + ', '.join(AVATAR_EXPRESSIONS[1:])}, 400
    color = str(payload.get('color', '') or '').strip()
    if color and not _HEX_COLOR_RE.match(color):
        return {'error': 'color must be a hex color like #a1b2c3'}, 400
    bgcolor = str(payload.get('bgcolor', '') or '').strip()
    if bgcolor and not _HEX_COLOR_RE.match(bgcolor):
        return {'error': 'bgcolor must be a hex color like #a1b2c3'}, 400
    eyecolor = str(payload.get('eyeColor', '') or '').strip()
    if eyecolor and not _HEX_COLOR_RE.match(eyecolor):
        return {'error': 'eyeColor must be a hex color like #a1b2c3'}, 400
    hue_raw = payload.get('hue', -1)
    if isinstance(hue_raw, bool) or not isinstance(hue_raw, (int, float, str)):
        return {'error': 'hue must be a number between 0 and 360'}, 400
    try:
        hue = int(float(hue_raw))
    except (TypeError, ValueError):
        return {'error': 'hue must be a number between 0 and 360'}, 400
    if hue < -1 or hue > 360:
        return {'error': 'hue must be a number between 0 and 360'}, 400
    tone_raw = payload.get('tone', -1)
    if isinstance(tone_raw, bool) or not isinstance(tone_raw, (int, float, str)):
        return {'error': 'tone must be a number between 0 and 1'}, 400
    try:
        tone = float(tone_raw)
    except (TypeError, ValueError):
        return {'error': 'tone must be a number between 0 and 1'}, 400
    if tone < -1.0 or tone > 1.0:
        return {'error': 'tone must be a number between 0 and 1'}, 400
    user.avatar_bg = bg
    user.avatar_hue = hue
    user.avatar_tone = tone
    user.avatar_anim = anim
    user.avatar_shape = shape
    user.avatar_expression = expression
    user.avatar_color = color.lower()
    user.avatar_bg_color = bgcolor.lower()
    user.avatar_eye_color = eyecolor.lower()
    update_fields = [
        'avatar_bg', 'avatar_hue', 'avatar_tone', 'avatar_anim',
        'avatar_shape', 'avatar_expression', 'avatar_color', 'avatar_bg_color',
        'avatar_eye_color',
    ]
    use_pp_raw = payload.get('use_pp', None)
    if use_pp_raw is not None:
        user.avatar_use_pp = str(use_pp_raw).strip().lower() in ('1', 'true', 'yes', 'on')
        update_fields.append('avatar_use_pp')
    user.save(update_fields=update_fields)
    return avatar_options_for(user), 200


USERNAME_COOLDOWN_DAYS = [7, 15, 30, 60, 100]
DAY_MS = 24 * 60 * 60 * 1000


def username_change_status(user, now=None):
    from .utils import now_ms
    now = now or now_ms()
    count = user.username_change_count or 0
    last = user.username_changed_at or 0
    if count <= 0 or not last:
        return {
            'allowed': True,
            'change_count': count,
            'cooldown_days': 0,
            'days_left': 0,
            'next_change_at': 0,
            'schedule': list(USERNAME_COOLDOWN_DAYS),
        }
    cooldown_days = USERNAME_COOLDOWN_DAYS[min(count - 1, len(USERNAME_COOLDOWN_DAYS) - 1)]
    next_change_at = last + cooldown_days * DAY_MS
    days_left = max(0, (next_change_at - now) / DAY_MS)
    return {
        'allowed': now >= next_change_at,
        'change_count': count,
        'cooldown_days': cooldown_days,
        'days_left': days_left,
        'next_change_at': next_change_at,
        'schedule': list(USERNAME_COOLDOWN_DAYS),
    }


def record_username_change(user, now=None):
    from .utils import now_ms
    now = now or now_ms()
    user.username_changed_at = now
    user.username_change_count = (user.username_change_count or 0) + 1


def validate_username_change(user, new_username, now=None):
    if new_username == user.username:
        return {'error': 'New username is the same as the current one.'}, 400
    if not new_username or len(new_username) < 3 or len(new_username) > 50 or not new_username.replace('_', '').isalnum():
        return {'error': 'Username must be 3-50 characters and can only contain letters, numbers, and underscores.'}, 400
    status = username_change_status(user, now)
    if not status['allowed']:
        from datetime import datetime
        ready = datetime.fromtimestamp(status['next_change_at'] / 1000.0)
        return {
            'error': 'You changed your username recently. You can change it again on %s (in %d days).' % (
                ready.strftime('%B %d, %Y'), int(status['days_left']) + 1),
            'status': status,
        }, 429
    conflict = User.objects.filter(username__iexact=new_username).exclude(pk=user.id).exists()
    if conflict:
        return {'error': 'Username already taken.'}, 409
    return None, 200


def set_password(user, password):
    from django.contrib.auth.password_validation import validate_password as django_validate_password
    try:
        django_validate_password(password)
    except DjangoValidationError as exc:
        return {'error': ' '.join(exc.messages)}, 400
    if user.password_hash:
        return {'error': 'Password already set. Use change-password instead.'}, 400
    user.password_hash = hash_password(password)
    user.email_verified = True
    user.save(update_fields=['password_hash', 'email_verified'])
    from .serializers import UserSerializer
    return {'status': 'success', 'message': 'Password set successfully', 'user': UserSerializer(user).data}, 200


def change_password(user, current_password, new_password):
    from django.contrib.auth.password_validation import validate_password as django_validate_password
    if not current_password or not new_password:
        return {'error': 'Current password and new password are required'}, 400
    try:
        django_validate_password(new_password)
    except DjangoValidationError as exc:
        return {'error': ' '.join(exc.messages)}, 400
    if not user.password_hash:
        return {'error': 'No password set. Use set-password instead.'}, 400
    password_ok, needs_rehash = verify_password(current_password, user.password_hash)
    if not password_ok:
        return {'error': 'Current password is incorrect'}, 401
    # Revoke every existing session BEFORE issuing the new token, so a
    # password change evicts attackers holding old bearer tokens.
    from .security import revoke_all_user_tokens
    revoke_all_user_tokens(user)
    user.password_hash = hash_password(new_password)
    auth_token = issue_auth_token(user, save=False)
    user.save(update_fields=['password_hash', 'auth_token'])
    from .serializers import UserSerializer
    return {
        'status': 'success',
        'message': 'Password changed successfully',
        'authToken': auth_token,
        'user': UserSerializer(user).data,
    }, 200


def activate_photo(user, photo_id):
    try:
        photo = UserPhoto.objects.get(pk=photo_id, user=user)
    except UserPhoto.DoesNotExist:
        return None
    UserPhoto.objects.filter(user=user).update(is_current=False)
    photo.is_current = True
    photo.save(update_fields=['is_current'])
    user.photo_url = photo.url
    user.save(update_fields=['photo_url'])
    return {'id': photo.id, 'url': photo.url, 'uploaded_at': photo.uploaded_at, 'is_current': True, 'success': True, 'photo_url': photo.url}


def toggle_resource_like(user, resource_id):
    with transaction.atomic():
        try:
            resource = Resource.objects.select_for_update().get(pk=resource_id)
        except Resource.DoesNotExist:
            raise
        like, created = ResourceLike.objects.get_or_create(resource=resource, user=user)
        if created:
            Resource.objects.filter(pk=resource_id).update(like_count=F('like_count') + 1)
            is_liked = True
            current_count = resource.like_count + 1
            _counters.increment_user_likes_given(user.id)
            if resource.uploaded_by_id and str(resource.uploaded_by_id) != str(user.id):
                _counters.increment_user_likes_received(resource.uploaded_by_id)
        else:
            like.delete()
            Resource.objects.filter(pk=resource_id, like_count__gt=0).update(like_count=F('like_count') - 1)
            is_liked = False
            current_count = max(resource.like_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if resource.uploaded_by_id and str(resource.uploaded_by_id) != str(user.id):
                _counters.decrement_user_likes_received(resource.uploaded_by_id)
    if is_liked:
        _notif.notify_resource_liked(user.id, resource_id)
    else:
        _notif.notify_resource_unliked(user.id, resource_id)
    _rt.broadcast_resource_like_changed(resource_id, current_count)
    return {'likeCount': current_count, 'isLiked': is_liked}


def toggle_resource_comment_like(user, comment_id):
    with transaction.atomic():
        try:
            comment = ResourceComment.objects.select_for_update().get(pk=comment_id)
        except ResourceComment.DoesNotExist:
            raise
        like, created = ResourceCommentLike.objects.get_or_create(comment=comment, user=user)
        if created:
            ResourceComment.objects.filter(pk=comment_id).update(like_count=F('like_count') + 1)
            is_liked = True
            current_count = comment.like_count + 1
            _counters.increment_user_likes_given(user.id)
            if comment.user_id and str(comment.user_id) != str(user.id):
                _counters.increment_user_likes_received(comment.user_id)
        else:
            like.delete()
            ResourceComment.objects.filter(pk=comment_id, like_count__gt=0).update(like_count=F('like_count') - 1)
            is_liked = False
            current_count = max(comment.like_count - 1, 0)
            _counters.decrement_user_likes_given(user.id)
            if comment.user_id and str(comment.user_id) != str(user.id):
                _counters.decrement_user_likes_received(comment.user_id)
    if is_liked:
        _notif.notify_resource_comment_liked(user.id, comment_id)
    else:
        _notif.notify_resource_comment_unliked(user.id, comment_id)
    # Comment-level like events broadcast on their own comment-scoped event;
    # the resource-level like_changed keeps carrying only resource counts.
    _rt.broadcast_resource_comment_like_changed(
        comment.resource_id, comment_id, current_count,
        is_liked_by_viewer_hint=is_liked, user_id=str(user.id),
    )
    return {'likeCount': current_count, 'isLiked': is_liked}


def create_resource_comment(user, resource_id, content, parent_comment_id=None, attachments=None):
    try:
        resource = Resource.objects.get(pk=resource_id)
    except Resource.DoesNotExist:
        return None
    content = content.strip()
    if not content and not attachments:
        return None
    content, _img_ids = _prep_inline_images(content)
    now = now_ms()
    with transaction.atomic():
        comment = ResourceComment.objects.create(
            id=uuid_str(),
            resource=resource,
            parent_comment_id=parent_comment_id,
            user=user,
            content=content,
            like_count=0,
            reply_count=0,
            created_at=now,
        )
        Resource.objects.filter(pk=resource_id).update(comment_count=F('comment_count') + 1)
        if parent_comment_id:
            ResourceComment.objects.filter(pk=parent_comment_id).update(reply_count=F('reply_count') + 1)
        if attachments:
            from .models import ResourceCommentMedia
            for order, item in enumerate(attachments):
                ResourceCommentMedia.objects.create(
                    id=uuid_str(), comment=comment,
                    kind=item['kind'], url=item['url'], name=item['name'],
                    mime_type=item['mime_type'], size_bytes=item['size_bytes'],
                    order=order, created_at=now,
                )
    if user:
        _counters.increment_user_reply_count(user.id)
        if parent_comment_id:
            _notif.notify_resource_comment_reply(user.id, parent_comment_id, resource_id, comment.id)
        else:
            _notif.notify_resource_comment(user.id, resource_id, comment.id)
    data = _serialize_resource_comment(comment)
    _rt.broadcast_resource_comment_created(resource_id, data)
    return data


def delete_resource_comment(user, comment_id, is_admin=False):
    try:
        comment = ResourceComment.objects.select_related('resource').get(pk=comment_id)
    except ResourceComment.DoesNotExist:
        return False
    if not is_admin and comment.user_id != user.id:
        return False
    resource_id = comment.resource_id
    parent_id = comment.parent_comment_id
    # Count this comment + all children for counter adjustment
    child_count = ResourceComment.objects.filter(parent_comment_id=comment_id).count()
    total_removed = 1 + child_count
    with transaction.atomic():
        # Delete children first (cascades anyway, but for counter accuracy)
        ResourceComment.objects.filter(parent_comment_id=comment_id).delete()
        comment.delete()
        Resource.objects.filter(pk=resource_id, comment_count__gt=0).update(
            comment_count=F('comment_count') - total_removed
        )
    if parent_id:
        ResourceComment.objects.filter(pk=parent_id, reply_count__gt=0).update(
            reply_count=F('reply_count') - 1
        )
    _counters.decrement_user_reply_count(user.id)
    _rt.broadcast_resource_comment_deleted(resource_id, comment_id)
    return True


def _serialize_media_payload(media_iterable):
    """PostMedia/ResourceCommentMedia rows → camelCase attachment dicts,
    same shape as PostMediaSerializer."""
    from .security import get_video_qualities
    res = []
    for m in media_iterable:
        thumb = getattr(m, 'thumbnail_url', '') or ''
        quals = get_video_qualities(m.url) if getattr(m, 'kind', '') == 'video' else []
        res.append({
            'id': m.id,
            'kind': m.kind,
            'url': m.url,
            'thumbnailUrl': thumb,
            'thumbnail_url': thumb,
            'qualities': quals,
            'name': m.name,
            'mimeType': m.mime_type,
            'sizeBytes': m.size_bytes,
            'order': m.order,
            'createdAt': m.created_at,
        })
    return res


def _serialize_resource_comment(comment):
    """Serialize a ResourceComment to a dict for JSON responses."""
    media = comment.media.all() if hasattr(comment, 'media') else []
    user = getattr(comment, 'user', None)
    if user:
        author_photo = avatar_or_photo_url(user) or ''
    else:
        author_photo = ''
    return {
        'id': comment.id,
        'resourceId': comment.resource_id,
        'authorId': comment.user_id or '',
        'authorName': comment.user.username if hasattr(comment, 'user') and comment.user else 'Anonymous',
        'authorPhoto': author_photo,
        'parentCommentId': comment.parent_comment_id or '',
        'content': comment.content,
        'likeCount': comment.like_count,
        'replyCount': comment.reply_count,
        'isEdited': comment.is_edited,
        'createdAt': comment.created_at,
        'attachments': _serialize_media_payload(media),
    }


# ── Blog Comment Services ──

def toggle_blog_comment_like(user, comment_id):
    with transaction.atomic():
        try:
            comment = BlogComment.objects.select_for_update().get(pk=comment_id)
        except BlogComment.DoesNotExist:
            raise
        like, created = BlogCommentLike.objects.get_or_create(comment=comment, user=user)
        if created:
            BlogComment.objects.filter(pk=comment_id).update(like_count=F('like_count') + 1)
            is_liked = True
            current_count = comment.like_count + 1
        else:
            like.delete()
            BlogComment.objects.filter(pk=comment_id, like_count__gt=0).update(like_count=F('like_count') - 1)
            is_liked = False
            current_count = max(comment.like_count - 1, 0)
    return {'likeCount': current_count, 'isLiked': is_liked}

def create_blog_comment(user, slug, content, parent_comment_id=None, attachments=None):
    try:
        announcement = Announcement.objects.get(slug=slug, status='published')
    except Announcement.DoesNotExist:
        return None
    content = content.strip()
    if not content and not attachments:
        return None
    content, _img_ids = _prep_inline_images(content)
    now = now_ms()
    with transaction.atomic():
        comment = BlogComment.objects.create(
            id=uuid_str(),
            announcement=announcement,
            parent_comment_id=parent_comment_id,
            author=user,
            text=content,
            like_count=0,
            reply_count=0,
            created_at=now,
        )
        if parent_comment_id:
            BlogComment.objects.filter(pk=parent_comment_id).update(reply_count=F('reply_count') + 1)
        _attach_forum_media(comment, attachments or [], 'blog_comment', now)
    return {'id': comment.id}

def delete_blog_comment(user, comment_id, is_admin=False):
    try:
        comment = BlogComment.objects.get(pk=comment_id)
    except BlogComment.DoesNotExist:
        return False
    if not is_admin and comment.author_id != str(user.id):
        return False
    parent_id = comment.parent_comment_id
    with transaction.atomic():
        BlogComment.objects.filter(parent_comment_id=comment_id).delete()
        comment.delete()
    if parent_id:
        BlogComment.objects.filter(pk=parent_id, reply_count__gt=0).update(
            reply_count=F('reply_count') - 1
        )
    return True


def delete_user_account(user_id, completed_by=None):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return False

    with transaction.atomic():
        # 1. Anonymize Resources uploaded by this user
        Resource.objects.filter(uploaded_by=user).update(
            uploaded_by=None,
            source_type='anonymous',
            author_name='Anonymous'
        )

        # 2. Anonymize ResourceRequests
        ResourceRequest.objects.filter(requested_by=user).update(
            requested_by=None,
            requester_name='Anonymous'
        )

        # 3. Bulk delete relations that do not have Meilisearch signals
        Bookmark.objects.filter(user=user).delete()
        Follow.objects.filter(follower=user).delete()
        Follow.objects.filter(following=user).delete()
        FCMToken.objects.filter(user=user).delete()
        Notification.objects.filter(recipient=user).delete()
        Notification.objects.filter(actor=user).delete()
        PollVote.objects.filter(user=user).delete()
        PostLike.objects.filter(user=user).delete()
        ReplyLike.objects.filter(user=user).delete()
        ResourceLike.objects.filter(user=user).delete()
        ResourceCommentLike.objects.filter(user=user).delete()
        ResourceComment.objects.filter(user=user).delete()
        BlogCommentLike.objects.filter(user=user).delete()
        BlogComment.objects.filter(author=user).delete()
        Reply.objects.filter(user=user).delete()
        EditHistory.objects.filter(edited_by=user).delete()
        UserPhoto.objects.filter(user=user).delete()

        # 4. Delete the User's posts (fires Meilisearch post_delete signals)
        posts = Post.objects.filter(user=user)
        for post in posts:
            post.delete()

        # 5. Delete the User object itself (fires Meilisearch user_deleted signal)
        user.delete()
        
        return True