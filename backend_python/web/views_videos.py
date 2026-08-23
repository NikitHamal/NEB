"""Dedicated Videos hub — listing + watch page.

Aggregates forum-attached videos (PostMedia kind='video') onto a first-class
Videos surface so every video has a true watch page for Google Video indexing.

Design matches existing M3 minimal surface language: top bar, tab header,
responsive grid, same color tokens and Material Symbols.
"""
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render

from api.models import Post, PostMedia

from .view_helpers import (
    _avatar_url,
    _ctx,
    _get_user_id,
    _make_abs_url,
    _user_badge_info,
    cache,
)


def _video_title(media, post):
    name = (media.name or "").strip()
    if name and name.lower() not in ("video", "attachment"):
        return name
    if post and post.title:
        return post.title.strip()
    return media.name or "Untitled video"


def _video_description(media, post):
    if post and post.content:
        txt = post.content.strip()
        if len(txt) > 240:
            return txt[:237] + "..."
        return txt
    return media.name or "Video from NEBians community"


def _serialize_video_row(media, idx=0):
    post = None
    author = None
    category = ""
    post_id = ""
    created_at = media.created_at or 0
    try:
        if media.post_id:
            post = media.post
        elif media.reply_id and getattr(media, "reply", None):
            post = media.reply.post if hasattr(media.reply, "post") else None
            if not post and media.reply:
                try:
                    post = Post.objects.select_related("user").get(pk=media.reply.post_id)
                except Exception:
                    post = None
    except Exception:
        post = None

    if post:
        try:
            author = post.user
            category = post.category or ""
            post_id = post.id
            created_at = post.created_at or media.created_at or 0
        except Exception:
            pass

    anon = bool(post and getattr(post, "is_anonymous", False))
    if anon:
        author_name = "Anonymous Nebian"
        author_photo = ""
        badge = None
    elif author:
        author_name = author.display_name or author.username
        author_photo = _avatar_url(author)
        badge = _user_badge_info(author)
    else:
        author_name = "NEBians"
        author_photo = ""
        badge = None

    thumb = _make_abs_url(media.thumbnail_url) if media.thumbnail_url else ""
    video_url = _make_abs_url(media.url) if media.url else ""

    return {
        "id": media.id,
        "url": video_url,
        "thumbnail_url": thumb,
        "thumbnailUrl": thumb,
        "name": media.name or "",
        "title": _video_title(media, post),
        "description": _video_description(media, post),
        "category": category,
        "author_name": author_name,
        "author_photo": author_photo,
        "author_badge": badge,
        "is_anonymous": anon,
        "post_id": post_id,
        "post_title": post.title if post else "",
        "created_at": created_at,
        "size_bytes": media.size_bytes or 0,
        "mime_type": media.mime_type or "",
    }


def videos(request):
    q = (request.GET.get("q") or "").strip()[:100]
    category = (request.GET.get("category") or "").strip()
    sort = (request.GET.get("sort") or "newest").strip().lower()
    if sort not in ("newest", "popular", "oldest"):
        sort = "newest"
    page_num = request.GET.get("page", 1)

    qs = PostMedia.objects.filter(kind="video").select_related("post", "post__user", "reply", "reply__post", "reply__user").order_by("-created_at")

    # In-memory post filter for correctness (keeps query simple, videos count is small < few k)
    all_media = list(qs[:1200])
    filtered = []
    for m in all_media:
        post = None
        if m.post_id:
            post = m.post
        elif m.reply_id and getattr(m, "reply", None):
            try:
                post = m.reply.post
            except Exception:
                try:
                    post = Post.objects.select_related("user").get(pk=m.reply.post_id)
                except Exception:
                    post = None
        if not post:
            continue
        if getattr(post, "is_archived", False):
            continue
        # skip unverified authors for SEO cleanliness
        try:
            if post.user and not post.user.email_verified:
                continue
        except Exception:
            pass
        if category and (post.category or "").lower() != category.lower():
            continue
        if q:
            hay = f"{post.title or ''} {post.content or ''} {m.name or ''}".lower()
            if q.lower() not in hay:
                continue
        filtered.append(m)

    # Sorting — archived last, then by requested sort
    def _archived_key(m):
        p = m.post if m.post_id else None
        if not p and m.reply_id:
            try:
                p = m.reply.post
            except Exception:
                p = None
        return 1 if p and getattr(p, "is_archived", False) else 0

    if sort == "popular":
        def _pop(m):
            p = m.post if m.post_id else (m.reply.post if m.reply and hasattr(m.reply, "post") else None)
            if not p:
                return 0
            return (p.thumbs_up_count or 0) * 3 + (p.reply_count or 0) * 2 + (p.view_count or 0) * 0.05
        filtered.sort(key=lambda m: (_archived_key(m), -_pop(m)))
    elif sort == "oldest":
        filtered.sort(key=lambda m: (_archived_key(m), m.created_at or 0))
    else:
        filtered.sort(key=lambda m: (_archived_key(m), -(m.created_at or 0)))

    # Category counts for filter chips
    cat_counts = {}
    for m in filtered:
        p = m.post if m.post_id else None
        if not p and m.reply_id:
            try:
                p = m.reply.post
            except Exception:
                p = None
        cat = (p.category if p and p.category else "General")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    categories_data = sorted(cat_counts.items(), key=lambda x: (-x[1], x[0]))
    categories_data = [{"name": k, "count": v} for k, v in categories_data]

    paginator = Paginator(filtered, 12)
    try:
        page_obj = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    videos_data = [_serialize_video_row(m) for m in page_obj.object_list]

    # Trending for sidebar / empty-state spark
    trending = sorted(all_media, key=lambda m: m.created_at or 0, reverse=True)[:6]
    trending_data = [_serialize_video_row(m) for m in trending if _make_abs_url(m.url)]

    ctx = _ctx(
        request,
        videos=videos_data,
        page_obj=page_obj,
        query=q,
        current_category=category,
        current_sort=sort,
        categories_data=categories_data,
        trending=trending_data,
        total_count=paginator.count,
    )
    return render(request, "web/videos.html", ctx)


def video_watch(request, media_id):
    try:
        media = (
            PostMedia.objects.select_related("post", "post__user", "reply", "reply__post", "reply__user").get(
                pk=media_id, kind="video"
            )
        )
    except PostMedia.DoesNotExist:
        raise Http404("Video not found")

    post = None
    if media.post_id:
        post = media.post
    elif media.reply_id and getattr(media, "reply", None):
        try:
            post = media.reply.post
        except Exception:
            try:
                post = Post.objects.select_related("user").get(pk=media.reply.post_id)
            except Exception:
                post = None

    if not post:
        raise Http404("Video not found")

    # Allow archived posts — watch page is canonical for Google Video indexing
    # (GSC example was an archived post).

    data = _serialize_video_row(media)
    # Build related videos: same category or same author
    related_qs = (
        PostMedia.objects.filter(kind="video")
        .select_related("post", "post__user")
        .exclude(pk=media_id)
        .order_by("-created_at")[:40]
    )
    related = []
    for m in related_qs:
        p = m.post if m.post_id else None
        if not p:
            continue
        is_arch = bool(getattr(p, "is_archived", False))
        rel = 0
        if p.category and data.get("category") and p.category == data["category"]:
            rel += 2
        if p.user_id and post.user_id and p.user_id == post.user_id:
            rel += 1
        if is_arch:
            rel -= 5
        related.append((rel, m))
        if len(related) >= 12:
            break
    related.sort(key=lambda x: (-x[0], -(x[1].created_at or 0)))
    related_data = [_serialize_video_row(m) for _, m in related[:8]]

    # SEO helpers
    video_url = _make_abs_url(media.url)
    thumb_url = _make_abs_url(media.thumbnail_url) if media.thumbnail_url else "https://nebians.consica.com.np/static/web/img/n-logo-social-1200.png"
    upload_iso = ""
    try:
        from django.utils import timezone
        import datetime

        ts = media.created_at or post.created_at or 0
        if ts:
            dt = timezone.datetime.fromtimestamp(ts / 1000, tz=timezone.get_current_timezone())
            upload_iso = dt.isoformat()
        else:
            upload_iso = timezone.now().isoformat()
    except Exception:
        from django.utils import timezone

        upload_iso = timezone.now().isoformat()

    ctx = _ctx(
        request,
        video=media,
        video_data=data,
        post=post,
        post_id=post.id if post else "",
        video_url=video_url,
        thumb_url=thumb_url,
        upload_iso=upload_iso,
        related=related_data,
        media_id=media_id,
    )
    return render(request, "web/video_watch.html", ctx)
