"""Views Profile extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403
from api.view_helpers import _profile_incomplete, _can_view_locked_profile
from api import store_catalog
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
            meta = f'{obj.user.display_name or obj.user.username} · {obj.reply_count} replies'
        elif bm.target_type == 'reply' and bm.target_id in replies:
            obj = replies[bm.target_id]
            data = _serialize_reply(obj, user_id=user_id, _bookmarked_ids={obj.id})
            title = f"Reply on {obj.post.title if obj.post else 'discussion'}"
            url = reverse('web:forum_post', kwargs={'post_id': obj.post_id}) + f"#reply-{obj.id}"
            excerpt = obj.content or ''
            meta = f'{obj.user.display_name or obj.user.username} · Reply'
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
    equipped_banner = getattr(profile_user, 'equipped_banner', '') or ''
    if not profile_user.banner_url and equipped_banner:
        banner_item = store_catalog.get_item(equipped_banner)
        if banner_item and banner_item['kind'] == 'banner':
            banner_type = equipped_banner
            banner_deco_text = banner_item.get('deco_text') or 'nebian'
            banner_text_color = banner_item.get('deco_color') or ''
    if not profile_user.banner_url and not banner_type:
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
        'flair_badge': _user_flair_badge(profile_user),
        'avatar_border': getattr(profile_user, 'equipped_border', '') or '',
    }

    if profile_private:
        profile_data.update({
            'email': '', 'dob': '', 'gender': '', 'class_level': '', 'class': '',
            'subjects': '', 'pradesh': '', 'district': '', 'school': '',
        })

    stats = _build_local_stats(profile_user) if not profile_private else {
        'post_count': 0, 'reply_count': 0, 'likes_given': 0, 'likes_received': 0, 'contribution_score': 0,
    }
    follower_count = (getattr(profile_user, 'follower_count', 0) or 0) if not profile_private else 0
    following_count = (getattr(profile_user, 'following_count', 0) or 0) if not profile_private else 0
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
            user_resources_qs = list(Resource.objects.filter(uploaded_by_id=profile_user.id).order_by('-added_at')[:60])
        else:
            user_resources_qs = list(Resource.objects.filter(uploaded_by_id=profile_user.id, approval_status='approved').order_by('-added_at')[:60])

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
                'file_url': r.file_url or '',
                'thumbnail_url': r.thumbnail_url or '',
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
    equipped_banner = getattr(user, 'equipped_banner', '') or ''
    if equipped_banner:
        card_style = store_catalog.banner_card_style(equipped_banner)
        if card_style:
            return card_style
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
    from PIL import ImageFont
    base = Path(settings.BASE_DIR) / 'web/static/web/fonts'
    names = {
        'bold': 'poppins_bold.ttf',
        'semibold': 'poppins_medium.ttf',
        'medium': 'poppins_medium.ttf',
        'regular': 'poppins_regular.ttf',
    }
    try:
        return ImageFont.truetype(str(base / names.get(weight, 'poppins_regular.ttf')), size)
    except Exception:
        pass
    # Fallback to system fonts
    fallbacks = []
    if weight in ('bold', 'semibold'):
        fallbacks = [
            '/usr/share/fonts/urw-base35/NimbusSans-Bold.t1',
            '/usr/share/fonts/google-droid-sans-fonts/DroidSansFallbackFull.ttf',
        ]
    else:
        fallbacks = [
            '/usr/share/fonts/urw-base35/NimbusSans-Regular.t1',
            '/usr/share/fonts/google-droid-sans-fonts/DroidSansFallbackFull.ttf',
        ]
    for path in fallbacks:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
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
    """Open Graph/social card PNG for profile sharing.

    Two-panel: left = role-colored with large avatar, right = white with name, handle, bio, branding.
    """
    if _rate_limit(request, 'profile_card_image', 30, 60, by_ip=True):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        from PIL import Image, ImageDraw, ImageFilter
    except Exception:
        raise Http404('Image support is unavailable')
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404('User not found')

    # Cache the rendered PNG keyed on the username + a hash of all fields
    # that influence the rendering (photo, name, role, verification fields).
    import hashlib as _hashlib
    _sig_src = '|'.join([
        str(profile_user.photo_url or ''),
        str(profile_user.display_name or ''),
        str(profile_user.username or ''),
        str(getattr(profile_user, 'role', '') or ''),
        str(profile_user.is_admin),
        str(getattr(profile_user, 'is_bot', False)),
        str(getattr(profile_user, 'moderator_level', 0) or 0),
        str(getattr(profile_user, 'verification_level', 0) or 0),
        str(getattr(profile_user, 'teacher_verified', False)),
    ])
    _sig = _hashlib.sha256(_sig_src.encode('utf-8')).hexdigest()[:20]
    cache_key = f'profile_card_png:{username}:{_sig}'
    cached_png = cache.get(cache_key)
    if cached_png is not None:
        resp = HttpResponse(cached_png, content_type='image/png')
        resp['Cache-Control'] = 'public, max-age=3600'
        resp['X-Content-Type-Options'] = 'nosniff'
        return resp

    W, H = 1200, 630
    deco, c1, c2 = _profile_card_banner_style(profile_user)

    img = Image.new('RGB', (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # ── Left panel: role-colored background with avatar ──
    panel_w = 440
    for y in range(H):
        t = y / max(1, H - 1)
        col = tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))
        d.line((0, y, panel_w, y), fill=col)

    accent = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ad = ImageDraw.Draw(accent)
    ad.polygon([(0, H - 300), (panel_w, H), (0, H)], fill=(255, 255, 255, 15))
    ad.polygon([(0, 0), (panel_w, 0), (panel_w, 200), (0, 350)], fill=(0, 0, 0, 12))
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, accent)
    img = img_rgba.convert('RGB')
    d = ImageDraw.Draw(img)

    # Avatar — centered in the left panel
    avatar_size = 240
    avatar = _profile_card_avatar(profile_user, avatar_size)
    ring_size = avatar_size + 16
    ring = Image.new('RGBA', (ring_size, ring_size), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse((0, 0, ring_size - 1, ring_size - 1), fill=(255, 255, 255, 255))
    rd.ellipse((4, 4, ring_size - 5, ring_size - 5), fill=(255, 255, 255, 0))
    ring.alpha_composite(avatar, (8, 8))
    av_x = (panel_w - ring_size) // 2
    av_y = (H - ring_size) // 2 - 15
    img.paste(ring, (av_x, av_y), ring)
    d = ImageDraw.Draw(img)

    # ── Right panel: white with name, handle, NEBians logo ──
    right_x = panel_w + 70
    right_w = W - right_x - 60

    # Name — big, bold, centered in space above the logo
    display = profile_user.display_name or profile_user.username
    name_font = _load_profile_card_font('bold', 88)
    handle = '@' + (profile_user.username or 'nebian')
    handle_font = _load_profile_card_font('regular', 36)
    name_bbox = d.textbbox((0, 0), display, font=name_font)
    name_h = name_bbox[3] - name_bbox[1]
    handle_bbox = d.textbbox((0, 0), handle, font=handle_font)
    handle_h = handle_bbox[3] - handle_bbox[1]
    gap = 28
    block_h = name_h + gap + handle_h
    available_h = H - 50 - block_h
    block_y = int(available_h / 2)
    _draw_text_ellipsis(d, (right_x, block_y), display, name_font, (15, 23, 42), right_w)
    _draw_text_ellipsis(d, (right_x, block_y + name_h + gap), handle, handle_font, (100, 116, 139), right_w)

    # NEBians logo + text — bottom-right corner
    logo_path = Path(settings.BASE_DIR) / 'web/static/web/img/n-logo-512.png'
    logo_size = 72
    try:
        logo = Image.open(logo_path).convert('RGBA')
        logo.thumbnail((logo_size, logo_size), Image.LANCZOS)
        logo_x = W - logo_size - 60
        logo_y = H - logo_size - 50
        img.paste(logo, (logo_x, logo_y), logo)
    except Exception:
        pass
    brand_font = _load_profile_card_font('bold', 32)
    brand = 'NEBians'
    bw = d.textlength(brand, font=brand_font)
    d.text((logo_x - bw - 10, logo_y + (logo_size - 36) // 2), brand, font=brand_font, fill=(100, 116, 139))

    buf = BytesIO()
    img.save(buf, format='PNG', optimize=True)
    png_bytes = buf.getvalue()
    cache.set(cache_key, png_bytes, 3600)
    resp = HttpResponse(png_bytes, content_type='image/png')
    resp['Cache-Control'] = 'public, max-age=3600'
    resp['X-Content-Type-Options'] = 'nosniff'
    return resp


def _draw_text_ellipsis_multiline(draw, xy, text, font, fill, max_width, max_lines=3):
    """Draw text that wraps across multiple lines with ellipsis on the last line."""
    text = str(text or '')
    words = text.split()
    lines = []
    current = ''
    for word in words:
        test = (current + ' ' + word).strip()
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
            if len(lines) >= max_lines - 1:
                break
    if current:
        lines.append(current)
    # Truncate last line with ellipsis if needed
    if len(lines) >= max_lines and lines:
        last = lines[-1]
        ell = '\u2026'
        while last and draw.textlength(last + ell, font=font) > max_width:
            last = last[:-1]
        lines[-1] = last + ell
    elif len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        ell = '\u2026'
        while last and draw.textlength(last + ell, font=font) > max_width:
            last = last[:-1]
        lines[-1] = last + ell
    x, y = xy
    for line in lines[:max_lines]:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + 8


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
    db_subjects = _get_distinct_subjects()
    subjects = sorted(set(_default_subjects + db_subjects))
    return render(request, 'web/edit_profile.html', _ctx(request, has_password=has_password, profile_incomplete=profile_incomplete, subjects=subjects))