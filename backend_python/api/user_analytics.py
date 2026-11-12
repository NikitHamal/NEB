"""A member's own analytics (`GET /api/users/me/analytics/`).

Everything here is first-party and about the signed-in member only. Nothing reads another
person's data and nothing is sent anywhere. Days are cut at local midnight in Nepal
(UTC+05:45, no daylight saving), the same rule the admin analytics use.

Shape (v2). Legacy keys (`stats`, `activityDays`, `topCategories`, `topSubjects`, `topPosts`,
`topResources`, `suggestions`) stay so installed app versions keep working.

    standing     score, level, progress to the next level, top-percent rank
    range        the window the overview and trend describe (7, 30 or 90 days)
    overview     six KPIs, each with previous period, change and a sparkline
    trend        one row per day of the window
    streak       current and longest run of active days
    heatmap      17 weeks of daily activity, Monday first
    rhythm       activity by hour and by weekday (last 90 days)
    mix          what the member did in the window
    reach        lifetime views, likes, replies and engagement, plus readers in the window
    helpfulness  reply kinds written and the labels they earned
    library      saves by type and likes given
    milestones   goals with progress
    insights     short, data-driven notes, most useful first

Cost is a fixed number of queries (see test_api_query_budget): raw timestamps for the last
180 days are pulled once per source and bucketed in Python, never one query per day.
"""
import math
from collections import Counter
from datetime import date, timedelta

from django.core.cache import cache
from django.db.models import Count, Q, Sum

from .models import (Bookmark, Follow, Notification, PollVote, Post, PostView, Reply, Resource, ResourceComment,
                     ResourceLike, User)
from .utils import now_ms

NPT_MS = (5 * 60 + 45) * 60 * 1000
DAY_MS = 86_400_000
WINDOW_DAYS = 180
RANGES = (7, 30, 90)
DEFAULT_RANGE = 30
HEAT_WEEKS = 17
STAMP_CAP = 20_000

LEVELS = (
    (0, 'Newcomer'), (20, 'Learner'), (60, 'Contributor'), (150, 'Regular'), (300, 'Mentor'),
    (600, 'Scholar'), (1200, 'Expert'), (2500, 'Master'), (5000, 'Legend'),
)
LIKE_VERBS = ('like_post', 'like_reply', 'like_resource', 'like_resource_comment')
RESPONSE_VERBS = ('reply', 'reply_reply', 'resource_comment', 'resource_comment_reply')
GOOD_LABELS = ('accepted', 'correct', 'helpful')
KIND_ORDER = ('answer', 'solution', 'hint', 'formula', 'comment')
WEEKDAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
WEEKDAYS_LONG = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')


# ---------------------------------------------------------------- time helpers

def day_of(ts):
    """Local day number (days since 1970-01-01) of a millisecond timestamp."""
    return (ts + NPT_MS) // DAY_MS


def hour_of(ts):
    return ((ts + NPT_MS) % DAY_MS) // 3_600_000


def weekday_of(day):
    """Monday = 0. Day 0 (1970-01-01) was a Thursday."""
    return (day + 3) % 7


def date_of(day):
    return date(1970, 1, 1) + timedelta(days=day)


def hour_label(hour):
    h12 = hour % 12 or 12
    return f'{h12} {"AM" if hour < 12 else "PM"}'


def pct_change(current, previous):
    """Whole-percent change, or None when there is nothing to compare with."""
    if not previous:
        return None
    return round((current - previous) / previous * 100)


def _stamps(qs, field, since):
    return list(qs.filter(**{f'{field}__gte': since}).order_by().values_list(field, flat=True)[:STAMP_CAP])


def _per_day(stamps):
    return Counter(day_of(s) for s in stamps)


# ---------------------------------------------------------------- pieces

def standing(user):
    score = user.contribution_score or 0
    index = 0
    for i, (floor, _name) in enumerate(LEVELS):
        if score >= floor:
            index = i
    floor, name = LEVELS[index]
    nxt = LEVELS[index + 1] if index + 1 < len(LEVELS) else None
    if nxt:
        progress = round((score - floor) / (nxt[0] - floor) * 100)
    else:
        progress = 100

    def rank():
        above = User.objects.filter(contribution_score__gt=score, is_banned=False).count()
        total = User.objects.filter(contribution_score__gt=0, is_banned=False).count()
        return {'above': above, 'total': total}

    r = cache.get_or_set(f'ua:rank:{score}', rank, 600) if score > 0 else {'above': 0, 'total': 0}
    top_percent = None
    if score > 0 and r['total']:
        top_percent = max(1, min(100, math.ceil((r['above'] + 1) / r['total'] * 100)))
    return {
        'score': score,
        'level': index + 1,
        'levelName': name,
        'levelFloor': floor,
        'nextLevelAt': nxt[0] if nxt else None,
        'nextLevelName': nxt[1] if nxt else '',
        'progress': max(0, min(100, progress)),
        'topPercent': top_percent,
        'memberSince': user.created_at or 0,
    }


def streaks(active_days, today):
    """Current and longest run of consecutive active days (current may end yesterday)."""
    current = 0
    cursor = today if today in active_days else today - 1
    while cursor in active_days:
        current += 1
        cursor -= 1
    longest = run = 0
    prev = None
    for d in sorted(active_days):
        run = run + 1 if prev is not None and d == prev + 1 else 1
        longest = max(longest, run)
        prev = d
    return {
        'current': current,
        'longest': longest,
        'activeToday': today in active_days,
        'atRisk': current > 0 and today not in active_days,
        'activeDays30': sum(1 for d in active_days if today - 29 <= d <= today),
    }


def heatmap(per_day, today):
    """17 Monday-first week columns ending with the current week. Level 0-4, -1 = not yet."""
    monday = today - weekday_of(today)
    start = monday - (HEAT_WEEKS - 1) * 7
    counts = [per_day.get(start + i, 0) if start + i <= today else -1 for i in range(HEAT_WEEKS * 7)]
    peak = max([c for c in counts if c > 0] or [1])
    cells = []
    for i, c in enumerate(counts):
        if c < 0:
            level = -1
        elif c == 0:
            level = 0
        else:
            level = min(4, 1 + int((c - 1) * 4 / max(peak, 1)))
        cells.append({'date': date_of(start + i).isoformat(), 'count': max(c, 0), 'level': level})
    return {'weeks': HEAT_WEEKS, 'start': date_of(start).isoformat(), 'max': max(counts), 'cells': cells}


def rhythm(own_stamps, today):
    since = (today - 89) * DAY_MS - NPT_MS
    hours, weekdays = [0] * 24, [0] * 7
    for s in own_stamps:
        if s >= since:
            hours[hour_of(s)] += 1
            weekdays[weekday_of(day_of(s))] += 1
    total = sum(hours)
    peak_hour = hours.index(max(hours)) if total else None
    peak_day = weekdays.index(max(weekdays)) if total else None
    return {
        'hours': hours,
        'weekdays': weekdays,
        'total': total,
        'peakHour': peak_hour,
        'peakHourLabel': hour_label(peak_hour) if peak_hour is not None else '',
        'peakWeekday': peak_day,
        'peakWeekdayLabel': WEEKDAYS_LONG[peak_day] if peak_day is not None else '',
    }


def _counter_rows(counter, limit=6):
    top = counter.most_common(limit)
    peak = top[0][1] if top else 1
    return [{'label': k, 'count': v, 'width': max(8, round(v / peak * 100))} for k, v in top]


def milestones(stats, helpful, streak):
    likes = stats['postLikesReceived'] + stats['resourceLikesReceived']
    views = stats['postViews'] + stats['resourceViews']
    rows = [
        ('first_post', 'Start a discussion', stats['posts'], 1),
        ('replies_10', 'Write 10 replies', stats['replies'], 10),
        ('first_helpful', 'Earn a helpful or accepted label', helpful, 1),
        ('first_resource', 'Share a resource', stats['resources'], 1),
        ('streak_7', 'Be active 7 days in a row', streak['longest'], 7),
        ('likes_50', 'Receive 50 likes', likes, 50),
        ('followers_25', 'Reach 25 followers', stats['followers'], 25),
        ('views_1000', 'Reach 1,000 views', views, 1000),
    ]
    out = []
    for key, title, progress, target in rows:
        out.append({'id': key, 'title': title, 'progress': min(progress, target), 'target': target,
                    'done': progress >= target})
    out.sort(key=lambda m: (m['done'], -m['progress'] / m['target']))
    return out


def insights(ctx):
    """Short notes picked from real numbers. Each: id, tone (good|info|action), title, body."""
    out = []
    streak, kpis, rhy = ctx['streak'], ctx['kpis'], ctx['rhythm']
    days = ctx['days']
    if streak['atRisk']:
        out.append({'id': 'streak_risk', 'tone': 'action', 'title': f'{streak["current"]}-day streak ends today',
                    'body': 'One reply, post or read today keeps it going.'})
    elif streak['current'] >= 3:
        out.append({'id': 'streak', 'tone': 'good', 'title': f'{streak["current"]} days in a row',
                    'body': f'Your longest run is {streak["longest"]} days.'})
    likes = kpis['likes']
    if likes['previous'] and likes['value'] and likes['change'] is not None and likes['change'] >= 25:
        out.append({'id': 'likes_up', 'tone': 'good', 'title': f'Likes up {likes["change"]}%',
                    'body': f'{likes["value"]} in the last {days} days, {likes["previous"]} before.'})
    elif likes['previous'] and likes['change'] is not None and likes['change'] <= -25:
        out.append({'id': 'likes_down', 'tone': 'info', 'title': f'Likes down {abs(likes["change"])}%',
                    'body': 'Answer a question or share a resource to bring them back.'})
    fol = kpis['followers']
    if fol['value']:
        out.append({'id': 'followers', 'tone': 'good',
                    'title': f'{fol["value"]} new follower{"" if fol["value"] == 1 else "s"}',
                    'body': f'In the last {days} days.'})
    if rhy['peakHour'] is not None and rhy['total'] >= 8:
        out.append({'id': 'rhythm', 'tone': 'info', 'title': f'Most active around {rhy["peakHourLabel"]}',
                    'body': f'{rhy["peakWeekdayLabel"]} is your busiest day.'})
    if ctx['unanswered']:
        n = ctx['unanswered']
        out.append({'id': 'unanswered', 'tone': 'action', 'title': f'{n} of your posts have no replies',
                    'body': 'Add detail or a picture, or reshare it with a clearer title.'})
    best = ctx['bestPost']
    if best and best['viewCount'] >= 10:
        out.append({'id': 'best_post', 'tone': 'good', 'title': 'Your best post',
                    'body': f'"{best["title"][:60]}" has {best["viewCount"]} views and {best["replyCount"]} replies.'})
    if not ctx['stats']['resources']:
        out.append({'id': 'share_resource', 'tone': 'action', 'title': 'Share a resource',
                    'body': 'Notes and papers you upload reach every student in the library.'})
    if not ctx['stats']['replies'] and ctx['stats']['posts']:
        out.append({'id': 'start_replying', 'tone': 'action', 'title': 'Answer someone else',
                    'body': 'Replies earn helpful labels and grow your score.'})
    if not out:
        out.append({'id': 'start', 'tone': 'info', 'title': 'Your numbers start here',
                    'body': 'Post, reply or share a resource and this page fills in.'})
    return out[:6]


# ---------------------------------------------------------------- the report

def clamp_range(raw):
    try:
        days = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_RANGE
    return days if days in RANGES else DEFAULT_RANGE


def build(user, days=DEFAULT_RANGE):
    now = now_ms()
    today = day_of(now)
    window_start_day = today - WINDOW_DAYS + 1
    since = window_start_day * DAY_MS - NPT_MS
    cutoff_30 = now - 30 * DAY_MS

    posts = Post.objects.filter(user=user, is_archived=False)
    replies = Reply.objects.filter(user=user, is_archived=False)
    resources = Resource.objects.filter(uploaded_by=user, is_lead=True)
    comments = ResourceComment.objects.filter(user=user)

    post_agg = posts.aggregate(total=Count('pk'), views=Sum('view_count'), likes=Sum('thumbs_up_count'),
                               replies=Sum('reply_count'), recent=Count('pk', filter=Q(created_at__gte=cutoff_30)),
                               solved=Count('pk', filter=Q(is_resolved=True)),
                               silent=Count('pk', filter=Q(reply_count=0, created_at__lt=now - DAY_MS)))
    reply_agg = replies.aggregate(total=Count('pk'), recent=Count('pk', filter=Q(created_at__gte=cutoff_30)),
                                  likes=Sum('thumbs_up_count'))
    res_agg = resources.aggregate(total=Count('pk'), views=Sum('view_count'), likes=Sum('like_count'),
                                  comments=Sum('comment_count'))
    comments_made = comments.count()

    # Raw timestamps, one query per source, bucketed below.
    s_posts = _stamps(posts, 'created_at', since)
    s_replies = _stamps(replies, 'created_at', since)
    s_resources = _stamps(resources, 'added_at', since)
    s_comments = _stamps(comments, 'created_at', since)
    s_votes = _stamps(PollVote.objects.filter(user=user), 'created_at', since)
    s_reads = _stamps(PostView.objects.filter(user=user), 'viewed_at', since)
    s_follows = _stamps(Follow.objects.filter(following=user), 'created_at', since)
    notes = list(Notification.objects.filter(recipient=user, verb__in=LIKE_VERBS + RESPONSE_VERBS,
                                             created_at__gte=since).order_by()
                 .values_list('verb', 'created_at')[:STAMP_CAP])
    s_likes = [t for v, t in notes if v in LIKE_VERBS]
    s_responses = [t for v, t in notes if v in RESPONSE_VERBS]
    readers = list(PostView.objects.filter(post__user=user, viewed_at__gte=since).exclude(user=user).order_by()
                   .values_list('user_id', 'viewed_at')[:STAMP_CAP])

    by = {
        'posts': _per_day(s_posts), 'replies': _per_day(s_replies), 'resources': _per_day(s_resources),
        'comments': _per_day(s_comments), 'votes': _per_day(s_votes), 'reads': _per_day(s_reads),
        'likes': _per_day(s_likes), 'responses': _per_day(s_responses), 'followers': _per_day(s_follows),
        'readers': _per_day([t for _u, t in readers]),
    }
    make_keys = ('posts', 'replies', 'resources', 'comments')
    active_keys = make_keys + ('votes', 'reads')
    per_day_actions = Counter()
    for key in active_keys:
        per_day_actions.update(by[key])
    active_days = {d for d, n in per_day_actions.items() if n > 0}

    def total(key, a, b):
        return sum(by[key].get(d, 0) for d in range(a, b + 1))

    first, prev_first = today - days + 1, today - 2 * days + 1
    prev_last = first - 1

    def kpi(key, label, series_key=None, fn=None):
        sk = series_key or key
        if fn:
            value, previous = fn(first, today), fn(prev_first, prev_last)
            series = [fn(d, d) for d in range(first, today + 1)]
        else:
            value, previous = total(sk, first, today), total(sk, prev_first, prev_last)
            series = [by[sk].get(d, 0) for d in range(first, today + 1)]
        return {'key': key, 'label': label, 'value': value, 'previous': previous,
                'change': pct_change(value, previous), 'series': series}

    def made(a, b):
        return sum(total(k, a, b) for k in make_keys)

    def active(a, b):
        return sum(1 for d in range(a, b + 1) if d in active_days)

    def readers_in(a, b):
        return len({u for u, t in readers if a <= day_of(t) <= b})

    kpis = {
        'contributions': kpi('contributions', 'Contributions', fn=made),
        'likes': kpi('likes', 'Likes received'),
        'responses': kpi('responses', 'Replies received'),
        'followers': kpi('followers', 'New followers'),
        'readers': kpi('readers', 'Readers', fn=readers_in),
        'activeDays': kpi('activeDays', 'Active days', fn=active),
    }

    trend = []
    for d in range(first, today + 1):
        dt = date_of(d)
        row = {'date': dt.isoformat(), 'label': f'{dt.day} {dt.strftime("%b")}',
               'weekday': WEEKDAYS[weekday_of(d)]}
        for key in ('posts', 'replies', 'resources', 'comments', 'reads', 'likes', 'responses', 'followers'):
            row[key] = by[key].get(d, 0)
        row['actions'] = sum(by[k].get(d, 0) for k in active_keys)
        trend.append(row)

    legacy_days = []
    peak = 1
    for i, d in enumerate(range(today - 13, today + 1)):
        n = sum(by[k].get(d, 0) for k in ('posts', 'replies', 'resources'))
        peak = max(peak, n)
        legacy_days.append({'label': 'Today' if d == today else f'{today - d}d', 'total': n,
                            'posts': by['posts'].get(d, 0), 'replies': by['replies'].get(d, 0),
                            'resources': by['resources'].get(d, 0), 'study': 0, 'height': 0})
    for row in legacy_days:
        row['height'] = max(8, round(row['total'] / peak * 100)) if row['total'] else 8

    mix = [
        {'key': 'posts', 'label': 'Posts', 'count': total('posts', first, today)},
        {'key': 'replies', 'label': 'Replies', 'count': total('replies', first, today)},
        {'key': 'resources', 'label': 'Resources', 'count': total('resources', first, today)},
        {'key': 'comments', 'label': 'Resource comments', 'count': total('comments', first, today)},
        {'key': 'votes', 'label': 'Poll votes', 'count': total('votes', first, today)},
        {'key': 'reads', 'label': 'Posts read', 'count': total('reads', first, today)},
    ]

    kind_rows = replies.order_by().values('kind', 'label').annotate(n=Count('pk'))
    kinds, labels = Counter(), Counter()
    for row in kind_rows:
        kinds[row['kind'] or 'comment'] += row['n']
        if row['label']:
            labels[row['label']] += row['n']
    good = sum(labels[k] for k in GOOD_LABELS)
    bm = dict(Bookmark.objects.filter(user=user).order_by().values_list('target_type').annotate(n=Count('pk')))

    categories = Counter(dict(posts.order_by().values_list('category').annotate(n=Count('pk'))))
    subjects = Counter()
    for subject in resources.values_list('subject', flat=True):
        for part in (subject or '').split(','):
            if part.strip():
                subjects[part.strip()] += 1

    top_posts = [{'id': p.id, 'title': p.title, 'category': p.category, 'view_count': p.view_count,
                  'like_count': p.thumbs_up_count, 'reply_count': p.reply_count, 'created_at': p.created_at}
                 for p in posts.order_by('-view_count', '-thumbs_up_count')[:5]]
    top_resources = [{'id': r.id, 'title': r.title, 'subject': r.subject, 'type': r.type,
                      'view_count': r.view_count, 'like_count': r.like_count, 'comment_count': r.comment_count,
                      'added_at': r.added_at} for r in resources.order_by('-view_count', '-like_count')[:5]]

    post_views = post_agg['views'] or 0
    post_likes = post_agg['likes'] or 0
    post_replies = post_agg['replies'] or 0
    res_views = res_agg['views'] or 0
    res_likes = res_agg['likes'] or 0
    res_comments = res_agg['comments'] or 0
    followers = Follow.objects.filter(following=user).count()
    following = Follow.objects.filter(follower=user).count()

    stats = {
        'posts': post_agg['total'], 'replies': reply_agg['total'],
        'postViews': post_views, 'postLikesReceived': post_likes, 'postRepliesReceived': post_replies,
        'resources': res_agg['total'], 'resourceViews': res_views, 'resourceLikesReceived': res_likes,
        'resourceCommentsReceived': res_comments, 'resourceCommentsMade': comments_made,
        'followers': followers, 'following': following,
        'bookmarks': sum(bm.values()),
        'notificationsUnread': Notification.objects.filter(recipient=user, is_read=False).count(),
        'recentPosts': post_agg['recent'], 'recentReplies': reply_agg['recent'],
        'contributionScore': user.contribution_score, 'likesGiven': user.likes_given_count,
    }
    streak = streaks(active_days, today)
    own_stamps = s_posts + s_replies + s_resources + s_comments + s_votes + s_reads
    rhy = rhythm(own_stamps, today)

    engagement = round((post_likes + post_replies) / post_views * 100, 1) if post_views else 0
    reach = {
        'views': post_views + res_views,
        'postViews': post_views, 'resourceViews': res_views,
        'likes': post_likes + res_likes + (reply_agg['likes'] or 0),
        'replies': post_replies, 'resourceComments': res_comments,
        'engagementRate': engagement,
        'avgViewsPerPost': round(post_views / post_agg['total']) if post_agg['total'] else 0,
        'avgViewsPerResource': round(res_views / res_agg['total']) if res_agg['total'] else 0,
        'uniqueReaders': kpis['readers']['value'],
        'readersPrevious': kpis['readers']['previous'],
    }
    best_post = None
    if top_posts:
        p = top_posts[0]
        best_post = {'id': p['id'], 'title': p['title'], 'viewCount': p['view_count'], 'replyCount': p['reply_count']}

    ctx = {'streak': streak, 'kpis': kpis, 'days': days, 'rhythm': rhy, 'unanswered': post_agg['silent'],
           'bestPost': best_post, 'stats': stats}

    return {
        'version': 2,
        'username': user.username,
        'generatedAt': now,
        'range': {'days': days, 'from': date_of(first).isoformat(), 'to': date_of(today).isoformat(),
                  'options': list(RANGES), 'timezone': 'Asia/Kathmandu'},
        'standing': standing(user),
        'stats': stats,
        'overview': [kpis[k] for k in ('contributions', 'likes', 'responses', 'followers', 'readers', 'activeDays')],
        'trend': trend,
        'streak': streak,
        'heatmap': heatmap(per_day_actions, today),
        'rhythm': rhy,
        'mix': mix,
        'reach': reach,
        'helpfulness': {
            'answersWritten': kinds['answer'] + kinds['solution'],
            'kinds': [{'key': k, 'count': kinds[k]} for k in KIND_ORDER if kinds[k]],
            'labels': [{'key': k, 'count': n} for k, n in labels.most_common()],
            'goodLabels': good,
            'solvedPosts': post_agg['solved'],
        },
        'library': {
            'saved': {'posts': bm.get('post', 0), 'replies': bm.get('reply', 0), 'resources': bm.get('resource', 0)},
            'likesGiven': user.likes_given_count,
            'resourceLikesGiven': ResourceLike.objects.filter(user=user).count(),
        },
        'milestones': milestones(stats, good, streak),
        'insights': insights(ctx),
        'activityDays': legacy_days,
        'topCategories': _counter_rows(categories),
        'topSubjects': _counter_rows(subjects),
        'topPosts': top_posts,
        'topResources': top_resources,
        'suggestions': [i['title'] + '. ' + i['body'] for i in insights(ctx) if i['tone'] == 'action'][:5],
    }
