"""Views Profile extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403
from api.view_helpers import _profile_incomplete, _can_view_locked_profile
from io import BytesIO
from pathlib import Path


def bookmarks(request):
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    try:
        current_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect('web:login')

    bookmarks_qs = list(Bookmark.objects.filter(user_id=user_id).order_by('-created_at')[:200])
    post_ids = [b.target_id for b in bookmarks_qs if b.target_type == 'post']
    reply_ids = [b.target_id for b in bookmarks_qs if b.target_type == 'reply']
    resource_ids = [b.target_id for b in bookmarks_qs if b.target_type == 'resource']

    posts = {p.id: p for p in Post.objects.select_related('user').filter(id__in=post_ids)}
    replies = {r.id: r for r in Reply.objects.select_related('user', 'post').filter(id__in=reply_ids)}
    resources = {r.id: r for r in Resource.objects.select_related('uploaded_by').filter(id__in=resource_ids)}

    items = []
    counts = {'all': 0, 'post': 0, 'reply': 0, 'resource': 0}
    for bm in bookmarks_qs:
        data = None
        title = ''
        url = '#'
        excerpt = ''
        meta = ''
        if bm.target_type == 'post' and bm.target_id in posts:
            obj = posts[bm.target_id]
            data = _serialize_post(obj, user_id=user_id, _bookmarked_ids={obj.id})
            title = obj.title or 'Untitled discussion'
            url = reverse('web:forum_post', kwargs={'post_id': obj.id})
            excerpt = obj.content or ''
            meta = f"{obj.user.display_name or obj.user.username} · {obj.reply_count} replies"
        elif bm.target_type == 'reply' and bm.target_id in replies:
            obj = replies[bm.target_id]
            data = _serialize_reply(obj, user_id=user_id, _bookmarked_ids={obj.id})
            title = f"Reply on {obj.post.title if obj.post else 'discussion'}"
            url = reverse('web:forum_post', kwargs={'post_id': obj.post_id}) + f"#reply-{obj.id}"
            excerpt = obj.content or ''
            meta = f"{obj.user.display_name or obj.user.username} · Reply"
        elif bm.target_type == 'resource' and bm.target_id in resources:
            obj = resources[bm.target_id]
            if obj.approval_status != 'approved' and obj.uploaded_by_id != user_id:
                continue
            data = _serialize_resource(obj)
            title = obj.title or 'Untitled resource'
            url = reverse('web:reader', kwargs={'resource_id': obj.id})
            excerpt = obj.description or ''
            meta = f"{obj.subject or 'Resource'} · {obj.grade_level or 'All levels'}"
        else:
            continue
        counts['all'] += 1
        counts[bm.target_type] += 1
        items.append({
            'type': bm.target_type,
            'created_at': bm.created_at,
            'title': title,
            'url': url,
            'excerpt': excerpt,
            'meta': meta,
            'data': data,
            'id': bm.target_id,
        })

    return render(request, 'web/bookmarks.html', _ctx(request,
        current_user=current_user,
        bookmark_items=items,
        bookmark_counts=counts,
    ))

def profile(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")

    viewer_user = None
    if user_id:
        try:
            viewer_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            viewer_user = None
    is_self = bool(viewer_user and viewer_user.pk == profile_user.pk)
    profile_private = not _can_view_locked_profile(viewer_user, profile_user)
    is_following_profile = False
    if viewer_user and not is_self:
        is_following_profile = Follow.objects.filter(follower_id=viewer_user.pk, following_id=profile_user.pk).exists()

    badge_info = _user_badge_info(profile_user)

    banner_type = ''
    banner_deco_text = 'nebian'
    banner_text_color = ''
    if not profile_user.banner_url:
        if profile_user.is_bot:
            banner_type = 'gradient-bot'
            banner_deco_text = 'neby ai'
            banner_text_color = 'rgba(255,255,255,0.25)'
        elif profile_user.is_admin:
            banner_type = 'gradient-admin'
            banner_deco_text = 'admin'
            banner_text_color = 'rgba(255,255,255,0.25)'
        elif profile_user.moderator_level and profile_user.moderator_level > 0:
            banner_type = 'gradient-moderator'
            banner_deco_text = 'moderator'
            banner_text_color = 'rgba(255,255,255,0.22)'
        elif profile_user.verification_level and profile_user.verification_level > 0:
            banner_type = 'gradient-verified'
            banner_deco_text = 'nebian'
            banner_text_color = 'rgba(255,255,255,0.20)'
        elif getattr(profile_user, 'role', '') == 'teacher':
            banner_type = 'gradient-tutor'
            banner_deco_text = 'tutor'
            banner_text_color = 'rgba(255,255,255,0.28)'
        elif getattr(profile_user, 'role', '') == 'institution':
            banner_type = 'gradient-institution'
            banner_deco_text = 'nebian'
            banner_text_color = 'rgba(255,255,255,0.25)'

    profile_data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'email': profile_user.email,
        'photo_url': profile_user.photo_url,
        'banner_url': profile_user.banner_url,
        'banner_type': banner_type,
        'banner_deco_text': banner_deco_text,
        'banner_text_color': banner_text_color,
        'display_name': profile_user.display_name,
        'role': profile_user.role,
        'dob': profile_user.dob,
        'gender': profile_user.gender,
        'class_level': profile_user.class_level,
        'class': profile_user.class_level,
        'subjects': profile_user.subjects,
        'teaching_subjects': profile_user.teaching_subjects,
        'institution_type': profile_user.institution_type,
        'pradesh': profile_user.pradesh,
        'district': profile_user.district,
        'school': profile_user.school,
        'bio': profile_user.bio,
        'is_locked': 1 if profile_user.is_locked else 0,
        'created_at': profile_user.created_at,
        'verification_level': profile_user.verification_level,
        'moderator_level': profile_user.moderator_level,
        'is_admin': profile_user.is_admin,
        'is_bot': profile_user.is_bot,
        'teacher_verified': profile_user.teacher_verified,
        'achievement_badges': profile_user.achievement_badges,
        'badge_info': badge_info,
        'achievement_info': _user_achievement_badges(profile_user),
    }

    if profile_private:
        profile_data.update({
            'email': '', 'dob': '', 'gender': '', 'class_level': '', 'class': '',
            'subjects': '', 'pradesh': '', 'district': '', 'school': '',
        })

    stats = _build_local_stats(profile_user) if not profile_private else {
        'post_count': 0, 'reply_count': 0, 'likes_given': 0, 'likes_received': 0, 'contribution_score': 0,
    }
    follower_count = Follow.objects.filter(following_id=profile_user.id).count() if not profile_private else 0
    following_count = Follow.objects.filter(follower_id=profile_user.id).count() if not profile_private else 0
    stats['follower_count'] = follower_count
    stats['following_count'] = following_count
    stats['is_following'] = is_following_profile
    stats['is_self'] = is_self

    if not profile_private:
        if is_self:
            uploaded_resources_count = Resource.objects.filter(uploaded_by_id=profile_user.id).count()
        else:
            uploaded_resources_count = Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved').count()
    else:
        uploaded_resources_count = 0
    stats['uploaded_resources_count'] = uploaded_resources_count

    user_posts_qs = Post.objects.none() if profile_private else Post.objects.select_related('user').filter(user_id=profile_user.id).order_by('-created_at')[:10]
    user_posts = _serialize_posts(user_posts_qs, user_id)

    user_replies_qs = Reply.objects.none() if profile_private else Reply.objects.select_related('user', 'post').filter(user_id=profile_user.id).order_by('-created_at')[:10]
    user_replies = _serialize_replies(user_replies_qs, user_id)

    user_resources = []
    if not profile_private:
        if is_self:
            user_resources_qs = Resource.objects.filter(uploaded_by_id=profile_user.id).order_by('-added_at')
        else:
            user_resources_qs = Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved').order_by('-added_at')

        liked_res_ids = set()
        if user_id and user_resources_qs:
            liked_res_ids = set(ResourceLike.objects.filter(
                resource_id__in=[r.id for r in user_resources_qs], user_id=user_id
            ).values_list('resource_id', flat=True))

        for r in user_resources_qs:
            user_resources.append({
                'id': r.id,
                'title': r.title,
                'description': r.description or '',
                'subject': r.subject,
                'grade_level': r.grade_level,
                'type': r.type,
                'file_size': r.file_size,
                'added_at': r.added_at,
                'view_count': r.view_count,
                'like_count': r.like_count,
                'comment_count': r.comment_count,
                'approval_status': r.approval_status,
                'rejection_reason': r.rejection_reason or '',
                'is_liked': r.id in liked_res_ids,
            })

    user_photos = []
    if user_id and user_id == profile_user.id:
        user_photos = list(UserPhoto.objects.filter(user_id=profile_user.id).values('id', 'url', 'uploaded_at', 'is_current'))

    return render(request, 'web/profile.html', _ctx(request,
        profile_user=profile_data,
        username=username,
        stats=stats,
        user_photos=user_photos,
        user_posts=user_posts,
        user_replies=user_replies,
        user_resources=user_resources,
        profile_private=profile_private,
        badge_info=profile_data.get('badge_info'),
        badge_info_json=json.dumps(profile_data.get('badge_info')),
        achievement_info_json=json.dumps(profile_data.get('achievement_info', [])),
        profile_user_json=json.dumps(profile_data),
    ))

def profile_achievements(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")

    viewer_user = None
    if user_id:
        try:
            viewer_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            viewer_user = None
    if not _can_view_locked_profile(viewer_user, profile_user):
        return redirect('web:profile', username=username)

    profile_data = {
        'id': profile_user.id,
        'username': profile_user.username,
        'email': profile_user.email,
        'photo_url': profile_user.photo_url,
        'banner_url': profile_user.banner_url,
        'display_name': profile_user.display_name,
        'role': profile_user.role,
        'dob': profile_user.dob,
        'gender': profile_user.gender,
        'class_level': profile_user.class_level,
        'class': profile_user.class_level,
        'subjects': profile_user.subjects,
        'teaching_subjects': profile_user.teaching_subjects,
        'institution_type': profile_user.institution_type,
        'pradesh': profile_user.pradesh,
        'district': profile_user.district,
        'school': profile_user.school,
        'bio': profile_user.bio,
        'is_locked': 1 if profile_user.is_locked else 0,
        'created_at': profile_user.created_at,
        'verification_level': profile_user.verification_level,
        'moderator_level': profile_user.moderator_level,
        'is_admin': profile_user.is_admin,
        'teacher_verified': profile_user.teacher_verified,
        'achievement_badges': profile_user.achievement_badges,
        'badge_info': _user_badge_info(profile_user),
        'achievement_info': _user_achievement_badges(profile_user),
    }

    stats = _build_local_stats(profile_user)
    follower_count = Follow.objects.filter(following_id=profile_user.id).count()
    following_count = Follow.objects.filter(follower_id=profile_user.id).count()
    stats['follower_count'] = follower_count
    stats['following_count'] = following_count
    stats['is_following'] = False
    stats['is_self'] = False
    if user_id:
        stats['is_self'] = (user_id == profile_user.id)
        if not stats['is_self']:
            stats['is_following'] = Follow.objects.filter(follower_id=user_id, following_id=profile_user.id).exists()

    return render(request, 'web/achievements.html', _ctx(request,
        profile_user=profile_data,
        username=username,
        stats=stats,
        achievement_info=_user_achievement_badges(profile_user),
    ))


def _profile_card_banner_style(user):
    if user.is_admin:
        return ('ADMIN', (252, 177, 31), (120, 64, 0))
    if getattr(user, 'is_bot', False):
        return ('NEBY AI', (114, 78, 252), (60, 24, 150))
    if getattr(user, 'moderator_level', 0):
        return ('MODERATOR', (15, 118, 110), (10, 65, 62))
    if getattr(user, 'verification_level', 0):
        return ('NEBIAN', (38, 99, 235), (14, 116, 144))
    if getattr(user, 'role', '') == 'teacher':
        return ('TUTOR', (16, 185, 129), (6, 95, 70))
    if getattr(user, 'role', '') == 'institution':
        return ('NEBIAN', (79, 70, 229), (55, 48, 163))
    return ('NEBIAN', (0, 84, 214), (14, 165, 233))


def _load_profile_card_font(weight='regular', size=32):
    base = Path('/usr/share/fonts/truetype/dejavu')
    names = {
        'bold': 'DejaVuSans-Bold.ttf',
        'semibold': 'DejaVuSans-Bold.ttf',
        'regular': 'DejaVuSans.ttf',
    }
    try:
        from PIL import ImageFont
        return ImageFont.truetype(str(base / names.get(weight, 'DejaVuSans.ttf')), size)
    except Exception:
        from PIL import ImageFont
        return ImageFont.load_default()


def _draw_text_ellipsis(draw, xy, text, font, fill, max_width):
    text = str(text or '')
    if draw.textlength(text, font=font) <= max_width:
        draw.text(xy, text, font=font, fill=fill)
        return text
    ell = '…'
    while text and draw.textlength(text + ell, font=font) > max_width:
        text = text[:-1]
    draw.text(xy, text + ell, font=font, fill=fill)
    return text + ell


def _profile_card_avatar(user, size=152):
    from PIL import Image, ImageDraw, ImageOps
    img = Image.new('RGBA', (size, size), (239, 242, 246, 255))
    src = None
    url = (getattr(user, 'photo_url', '') or '').strip()

    def _load_local_media(media_path):
        try:
            rel = media_path.replace(settings.MEDIA_URL, '', 1).lstrip('/')
            src_path = Path(settings.MEDIA_ROOT) / rel
            if src_path.exists() and src_path.is_file():
                return Image.open(src_path).convert('RGBA')
        except Exception:
            return None
        return None

    if url:
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            media_url = settings.MEDIA_URL or '/media/'
            if url.startswith(media_url):
                src = _load_local_media(url)
            elif parsed.scheme in ('http', 'https') and parsed.path.startswith(media_url):
                src = _load_local_media(parsed.path)
            elif parsed.scheme == 'https':
                # Most social-card photos come from OAuth profile photos. Load them
                # only after NEBians' external URL validation and with a tiny cap.
                from api.security import validate_profile_photo_url
                import requests
                validate_profile_photo_url(url)
                resp = requests.get(
                    url,
                    timeout=2.5,
                    stream=True,
                    headers={'User-Agent': 'NEBians social card renderer'},
                )
                resp.raise_for_status()
                ctype = (resp.headers.get('content-type') or '').lower()
                if ctype.startswith('image/'):
                    max_bytes = 3 * 1024 * 1024
                    content = resp.raw.read(max_bytes + 1, decode_content=True)
                    if len(content) <= max_bytes:
                        src = Image.open(BytesIO(content)).convert('RGBA')
        except Exception:
            src = None

    if src:
        img = ImageOps.fit(src, (size, size), method=Image.LANCZOS, centering=(0.5, 0.5))
    else:
        d = ImageDraw.Draw(img)
        initial = (user.display_name or user.username or 'N')[:1].upper()
        f = _load_profile_card_font('bold', int(size * 0.43))
        bbox = d.textbbox((0, 0), initial, font=f)
        d.text(((size-(bbox[2]-bbox[0]))/2, (size-(bbox[3]-bbox[1]))/2-4), initial, font=f, fill=(0, 75, 212, 255))
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size-1, size-1), fill=255)
    out = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    out.paste(img, (0, 0), mask)
    return out


def profile_card_image(request, username):
    """Open Graph/social card PNG for profile sharing."""
    try:
        from PIL import Image, ImageDraw, ImageFilter
    except Exception:
        raise Http404('Image support is unavailable')
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404('User not found')

    W, H = 1200, 630
    img = Image.new('RGB', (W, H), (248, 250, 252))
    d = ImageDraw.Draw(img)

    # Outer card
    x0, y0, x1, y1 = 56, 46, 1144, 584
    d.rounded_rectangle((x0, y0, x1, y1), radius=36, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

    # Banner kept compact so the preview always shows identity details.
    deco, c1, c2 = _profile_card_banner_style(profile_user)
    banner_h = 184
    banner = Image.new('RGB', (x1 - x0, banner_h), c1)
    bd = ImageDraw.Draw(banner)
    for x in range(banner.width):
        t = x / max(1, banner.width - 1)
        col = tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))
        bd.line((x, 0, x, banner_h), fill=col)
    bd.ellipse((-160, 72, 440, 284), fill=tuple(min(255, v + 34) for v in c1))
    bd.ellipse((520, 40, 1280, 290), fill=tuple(max(0, v - 12) for v in c2))
    banner = banner.filter(ImageFilter.GaussianBlur(radius=0.45))
    img.paste(banner, (x0, y0))
    d = ImageDraw.Draw(img)

    # Small NEBians brand mark in the banner.
    logo_path = Path(settings.BASE_DIR) / 'web/static/web/img/n-logo-512.png'
    try:
        logo = Image.open(logo_path).convert('RGBA')
        logo.thumbnail((46, 46), Image.LANCZOS)
        img.paste(logo, (92, 82), logo)
    except Exception:
        pass
    d.text((150, 91), 'NEBians', font=_load_profile_card_font('bold', 32), fill=(255, 255, 255))

    deco_font = _load_profile_card_font('bold', 42)
    deco_text = (deco or 'NEBIAN').upper()
    deco_w = d.textlength(deco_text, font=deco_font)
    d.text((x1 - 92 - deco_w, 91), deco_text, font=deco_font, fill=(255, 255, 255))

    # Big profile area.
    avatar_size = 178
    avatar = _profile_card_avatar(profile_user, avatar_size)
    ring_size = avatar_size + 18
    ring = Image.new('RGBA', (ring_size, ring_size), (255, 255, 255, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse((0, 0, ring_size - 1, ring_size - 1), fill=(255, 255, 255, 255))
    rd.ellipse((4, 4, ring_size - 5, ring_size - 5), outline=(226, 232, 240, 255), width=2)
    ring.alpha_composite(avatar, (9, 9))
    img.paste(ring, (94, 174), ring)

    d = ImageDraw.Draw(img)
    display = profile_user.display_name or profile_user.username
    name_font = _load_profile_card_font('bold', 58)
    handle_font = _load_profile_card_font('regular', 31)
    bio_font = _load_profile_card_font('regular', 27)
    stat_font = _load_profile_card_font('bold', 38)
    label_font = _load_profile_card_font('regular', 18)

    _draw_text_ellipsis(d, (318, 226), display, name_font, (15, 23, 42), 690)
    _draw_text_ellipsis(d, (320, 300), '@' + (profile_user.username or 'nebian'), handle_font, (71, 85, 105), 650)

    headline = 'NEBians Member'
    if profile_user.is_admin:
        headline = 'Admin'
    elif profile_user.is_bot:
        headline = 'AI Study Companion'
    elif profile_user.role == 'teacher':
        headline = 'Teacher'
    elif profile_user.role == 'institution':
        headline = 'Institution'
    elif profile_user.class_level:
        headline = profile_user.class_level if profile_user.class_level != 'Passout' else '+2 Passout'
    _draw_text_ellipsis(d, (320, 342), headline, bio_font, (71, 85, 105), 650)
    if profile_user.bio:
        _draw_text_ellipsis(d, (96, 406), profile_user.bio, bio_font, (71, 85, 105), 980)
    else:
        _draw_text_ellipsis(d, (96, 406), 'Learning, sharing, and growing with the NEBians community.', bio_font, (71, 85, 105), 980)

    followers = Follow.objects.filter(following_id=profile_user.id).count()
    following = Follow.objects.filter(follower_id=profile_user.id).count()
    posts = Post.objects.filter(user_id=profile_user.id).count()
    resources = Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved').count()
    stats = [('Posts', posts), ('Followers', followers), ('Following', following), ('Resources', resources)]
    d.line((96, 466, 1104, 466), fill=(226, 232, 240), width=2)
    for i, (label, val) in enumerate(stats):
        col_w = 252
        cx = 96 + col_w * i + col_w / 2
        txt = str(val)
        tw = d.textlength(txt, font=stat_font)
        d.text((cx - tw / 2, 490), txt, font=stat_font, fill=(15, 23, 42))
        lw = d.textlength(label.upper(), font=label_font)
        d.text((cx - lw / 2, 540), label.upper(), font=label_font, fill=(100, 116, 139))

    site = request.get_host() or 'nebians.consica.com.np'
    site_font = _load_profile_card_font('regular', 22)
    sw = d.textlength(site, font=site_font)
    d.text((1104 - sw, 596), site, font=site_font, fill=(148, 163, 184))

    buf = BytesIO()
    img.save(buf, format='PNG', optimize=True)
    resp = HttpResponse(buf.getvalue(), content_type='image/png')
    resp['Cache-Control'] = 'public, max-age=86400, stale-while-revalidate=604800'
    resp['X-Content-Type-Options'] = 'nosniff'
    return resp


def ajax_profile_activity(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    viewer_user = None
    if user_id:
        try:
            viewer_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            viewer_user = None
    if not _can_view_locked_profile(viewer_user, profile_user):
        return JsonResponse({'error': 'This profile is private'}, status=403)

    try:
        offset = max(0, int(request.GET.get('offset', 0)))
        limit = min(25, max(1, int(request.GET.get('limit', 10))))
    except ValueError:
        offset = 0
        limit = 10

    user_posts_qs = Post.objects.select_related('user').filter(user_id=profile_user.id).order_by('-created_at')[offset:offset+limit]
    user_posts = _serialize_posts(user_posts_qs, user_id)

    total_count = Post.objects.filter(user_id=profile_user.id).count()
    has_more = (offset + len(user_posts)) < total_count

    return JsonResponse({
        'posts': user_posts,
        'has_more': has_more,
        'total_count': total_count
    })

def ajax_profile_replies(request, username):
    user_id = _get_user_id(request)
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    viewer_user = None
    if user_id:
        try:
            viewer_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            viewer_user = None
    if not _can_view_locked_profile(viewer_user, profile_user):
        return JsonResponse({'error': 'This profile is private'}, status=403)

    try:
        offset = max(0, int(request.GET.get('offset', 0)))
        limit = min(25, max(1, int(request.GET.get('limit', 10))))
    except ValueError:
        offset = 0
        limit = 10

    replies_qs = Reply.objects.select_related('user', 'post').filter(user_id=profile_user.id).order_by('-created_at')[offset:offset+limit]
    replies = _serialize_replies(replies_qs, user_id)

    total_count = Reply.objects.filter(user_id=profile_user.id).count()
    has_more = (offset + len(replies)) < total_count

    return JsonResponse({
        'replies': replies,
        'has_more': has_more,
        'total_count': total_count
    })

def edit_profile(request):
    token = api.get_session_token(request)
    if not token:
        return redirect('web:login')
    user = api.get_session_user(request)
    if not user:
        return redirect('web:login')
    try:
        db_user = User.objects.get(id=user.get('id'))
    except User.DoesNotExist:
        return redirect('web:login')
    has_password = bool(db_user.password_hash)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        dob = request.POST.get('dob', '').strip()
        display_name = request.POST.get('display_name', '').strip()
        gender = request.POST.get('gender', '').strip()
        role = request.POST.get('role', db_user.role).strip().lower()
        class_level = request.POST.get('class_level', '').strip()
        if role not in ('student', 'teacher', 'institution', 'explorer'):
            role = db_user.role or 'student'
        if not username or not dob:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Username and Date of Birth are required.'))
        if not display_name:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Display Name is required.'))
        if not gender:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Gender is required.'))
        if role == 'student' and not class_level:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Class is required for students.'))
        if role == 'teacher' and not request.POST.get('teaching_subjects', '').strip():
            return render(request, 'web/edit_profile.html', _ctx(request, error='Teaching subjects are required for teachers.'))
        if role == 'institution' and not request.POST.get('school', '').strip():
            return render(request, 'web/edit_profile.html', _ctx(request, error='Institution name is required.'))
        conflict = User.objects.filter(username__iexact=username).exclude(pk=db_user.id).exists()
        if conflict:
            return render(request, 'web/edit_profile.html', _ctx(request, error='Username already taken.'))
        db_user.username = username
        db_user.email = request.POST.get('email', '').strip() or db_user.email or ''
        db_user.display_name = display_name or db_user.display_name or ''
        db_user.role = role
        db_user.dob = dob
        db_user.gender = gender or db_user.gender or ''
        db_user.class_level = class_level or db_user.class_level or ''
        db_user.subjects = request.POST.get('subjects', '') or db_user.subjects or ''
        db_user.teaching_subjects = request.POST.get('teaching_subjects', '') or db_user.teaching_subjects or ''
        db_user.institution_type = request.POST.get('institution_type', '') or db_user.institution_type or ''
        db_user.pradesh = request.POST.get('pradesh', '') or db_user.pradesh or ''
        db_user.district = request.POST.get('district', '').strip() or db_user.district or ''
        db_user.school = request.POST.get('school', '').strip() or db_user.school or ''
        db_user.bio = request.POST.get('bio', '').strip()
        db_user.is_locked = request.POST.get('is_locked') == 'on'
        db_user.save()
        _clear_page_cache()
        updated_data = {
            'id': db_user.id,
            'username': db_user.username,
            'email': db_user.email,
            'photo_url': db_user.photo_url,
            'display_name': db_user.display_name,
            'role': db_user.role,
            'dob': db_user.dob,
            'gender': db_user.gender,
            'class_level': db_user.class_level,
            'class': db_user.class_level,
            'subjects': db_user.subjects,
            'teaching_subjects': db_user.teaching_subjects,
            'institution_type': db_user.institution_type,
            'pradesh': db_user.pradesh,
            'district': db_user.district,
            'school': db_user.school,
            'bio': db_user.bio,
            'is_locked': 1 if db_user.is_locked else 0,
            'created_at': db_user.created_at,
        }
        api.set_session_auth(request, token, updated_data)
        return redirect('web:home')
    profile_incomplete = _profile_incomplete(db_user)
    _default_subjects = [
        'Physics', 'Chemistry', 'Mathematics', 'Biology', 'English', 'Nepali',
        'Computer Science', 'Economics', 'Accountancy', 'Business Studies',
        'Social Studies', 'History', 'Geography', 'Civics', 'Health & Physical Education',
        'Environment Science', 'Science', 'General Science', 'Life Science',
        'Physical Science', 'Earth Science', 'Applied Mathematics',
        'Business Mathematics', 'Statistics', 'Probability',
        'Microeconomics', 'Macroeconomics',
        'Financial Accounting', 'Cost Accounting', 'Auditing',
        'Marketing', 'Office Management', 'Hotel Management',
        'Computer Engineering', 'Electronics', 'Electrical Engineering',
        'Civil Engineering', 'Mechanical Engineering', 'Architecture',
        'Mechanics', 'Thermodynamics', 'Optics', 'Electricity & Magnetism',
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Botany', 'Zoology', 'Genetics', 'Ecology',
        'English Grammar', 'English Literature', 'Creative Writing',
        'Nepali Grammar', 'Nepali Literature', 'Essay Writing',
        'Population Studies', 'Sociology', 'Psychology', 'Philosophy',
        'Education', 'Pedagogy', 'Curriculum Development',
        'Law', 'Constitutional Law', 'International Law',
        'Medicine', 'Pharmacy', 'Nursing', 'Public Health',
        'Agriculture', 'Forestry', 'Veterinary Science',
        'Management', 'Human Resource Management', 'Entrepreneurship',
        'Information Technology', 'Programming', 'Web Development',
        'Database Management', 'Networking', 'Cybersecurity',
        'Machine Learning', 'Artificial Intelligence', 'Data Science',
        'C Programming', 'C++ Programming', 'Python Programming', 'Java Programming',
        'Digital Logic', 'Operating Systems', 'Software Engineering',
        'Surveying', 'Estimating & Costing', 'Building Construction',
        'Fluid Mechanics', 'Strength of Materials', 'Engineering Drawing',
        'Purana Veda', 'Upanishad', 'Sanskrit', 'Maithili',
    ]
    db_subjects = []
    for s_str in Resource.objects.values_list('subject', flat=True):
        if s_str:
            for s in s_str.split(','):
                s_stripped = s.strip()
                if s_stripped:
                    db_subjects.append(s_stripped)
    subjects = sorted(set(_default_subjects + db_subjects))
    return render(request, 'web/edit_profile.html', _ctx(request, has_password=has_password, profile_incomplete=profile_incomplete, subjects=subjects))
