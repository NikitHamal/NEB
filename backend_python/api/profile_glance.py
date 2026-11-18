"""Profile overview data: the three glance tiles and the "Studying now" card (Profile v3).

Public data only: counts of what the member published, never their reading history, saves
or private activity. One shared builder for the JSON API (`/api/users/profile/<u>/stats`)
and the web profile page, so the app and the site always show the same numbers.

    glance    three tiles {icon, value, label, tone}; icon is a Material Symbols name
    studying  {subject, title, postId, today, streak, week[7], weekDays[7]} or None

Cost: four aggregate/timestamp queries, cached for two minutes per member.
"""
from collections import Counter

from django.core.cache import cache
from django.db.models import Count, Q, Sum

from .models import Post, Reply, Resource, ResourceComment
from .user_analytics import DAY_MS, NPT_MS, STAMP_CAP, WEEKDAYS, day_of, streaks, weekday_of
from .utils import now_ms

STREAK_WINDOW_DAYS = 120
CACHE_SECONDS = 120


def short(n):
    """12400 -> 12.4k, 1200000 -> 1.2M."""
    n = int(n or 0)
    if n >= 1_000_000:
        return f'{n / 1_000_000:.1f}'.rstrip('0').rstrip('.') + 'M'
    if n >= 10_000:
        return f'{n / 1000:.0f}k'
    if n >= 1000:
        return f'{n / 1000:.1f}'.rstrip('0').rstrip('.') + 'k'
    return str(n)


def _stamps(qs, field, since):
    return list(qs.filter(**{f'{field}__gte': since}).order_by().values_list(field, flat=True)[:STAMP_CAP])


def build(user, now=None):
    """Return {'glance': [...], 'studying': {...} | None} for one member."""
    key = f'pg:{user.pk}'
    hit = cache.get(key)
    if hit is not None:
        return hit
    now = now or now_ms()
    today = day_of(now)
    since = (today - STREAK_WINDOW_DAYS + 1) * DAY_MS - NPT_MS

    # Six queries on a cold cache (seven for an uploader): two aggregates, three timestamp pulls, one count.
    res = Resource.objects.filter(uploaded_by=user, is_lead=True, approval_status='approved').aggregate(
        n=Count('pk'), views=Sum('view_count'), downloads=Sum('download_count'), likes=Sum('like_count'))
    contributor = (res['n'] or 0) > 0
    public_posts = Post.objects.filter(user=user, is_archived=False, is_anonymous=False)
    post_views = public_posts.aggregate(views=Sum('view_count'))['views']
    recent_posts = list(public_posts.filter(created_at__gte=since).order_by()
                        .values('id', 'title', 'category', 'created_at')[:STAMP_CAP])
    replies = Reply.objects.filter(user=user, is_archived=False, is_anonymous=False)
    reply_agg = replies.aggregate(answers=Count('pk', filter=Q(kind__in=('answer', 'solution'))),
                                  accepted=Count('pk', filter=Q(label__in=('accepted', 'correct'))))
    stamps = [p['created_at'] for p in recent_posts]
    stamps += _stamps(replies, 'created_at', since)
    stamps += _stamps(ResourceComment.objects.filter(user=user), 'created_at', since)
    if contributor:
        stamps += _stamps(Resource.objects.filter(uploaded_by=user, is_lead=True, approval_status='approved'),
                          'added_at', since)
    per_day = Counter(day_of(t) for t in stamps)
    streak = streaks(set(per_day), today)['current']
    answers, accepted = reply_agg['answers'], reply_agg['accepted']

    if contributor:
        glance = [
            {'icon': 'visibility', 'value': short(res['views']), 'label': 'Total reads', 'tone': 3},
            {'icon': 'download', 'value': short(res['downloads']), 'label': 'Downloads', 'tone': 1},
            {'icon': 'thumb_up', 'value': short(res['likes']), 'label': 'Likes', 'tone': 2},
        ]
    else:
        glance = [
            {'icon': 'visibility', 'value': short(post_views), 'label': 'Reads on my posts', 'tone': 1},
            {'icon': 'verified' if accepted else 'check_circle', 'value': short(accepted or answers),
             'label': 'Accepted answers' if accepted else 'Answers', 'tone': 2},
            {'icon': 'local_fire_department', 'value': short(streak), 'label': 'Day streak', 'tone': 3},
        ]

    latest = max(recent_posts, key=lambda p: p['created_at'], default=None)
    studying = None
    if latest and now - latest['created_at'] <= 30 * DAY_MS and not contributor:
        monday = today - weekday_of(today)
        studying = {
            'subject': latest['category'], 'title': latest['title'], 'postId': latest['id'],
            'today': per_day.get(today, 0), 'streak': streak,
            'week': [per_day.get(monday + i, 0) if monday + i <= today else 0 for i in range(7)],
            'weekDays': list(WEEKDAYS), 'todayIndex': weekday_of(today),
        }
    out = {'glance': glance, 'studying': studying}
    cache.set(key, out, CACHE_SECONDS)
    return out
