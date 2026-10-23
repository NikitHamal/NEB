"""People the signed-in user might want to follow: GET /api/users/suggestions/?limit=12.

The Android app used to assemble this itself (PeopleSuggestionRepository): the user's
followers, the following lists of four random followees, two user searches, three forum
pages, then a popup and a stats call per shortlisted person to drop locked, private,
followed and requested accounts -- about 43 requests. This is the same result from a
handful of queries:

candidates  the user's followers; everyone a followee follows (mutual_count = how many of
            the user's followees follow them, counted over all followees); people from the
            same school; people in the same class; authors of the 60 most recent
            non-anonymous, non-bot forum posts.
excluded    the user; anyone they follow or have a pending follow request to; locked
            (private), banned, unverified and bot accounts -- the popup's
            is_self/is_locked/is_following and the stats endpoint's
            is_private/is_following/is_requested, plus bans.
score       120 if they follow you + 28 per mutual connection (max 4) + 34 same school
            + 16 same class + 12 active in the forum + min(followers, 60) // 5;
            ties by username.

"Same class" compares class levels the way map_profile_grade() reads them, so a "12"
and a "Class 12" are in the same class. Same-school and same-class people are only
looked at through a LIMITed query (their best `limit` by that part of the score), which
gives the same top `limit` as scoring all of them: anyone left out is outranked by
`limit` people who were kept.
"""
from django.db.models import Case, CharField, Count, F, Func, IntegerField, Q, Value, When

from .badges import user_badge_info
from .models import Follow, FollowRequest, Post, User
from .services import AVATAR_FIELDS, avatar_or_photo_url

DEFAULT_LIMIT = 12
MAX_LIMIT = 30
FEED_POSTS = 60

FOLLOWS_YOU = 120
PER_MUTUAL = 28
MAX_MUTUALS = 4
SAME_SCHOOL = 34
SAME_CLASS = 16
FEED_ACTIVE = 12

# map_profile_grade() spellings, lower-cased, of the classes it knows.
_GRADE_SPELLINGS = (
    ('11', 'grade 11', 'class 11'),
    ('12', 'grade 12', 'class 12'),
    ('10', 'see', 'class 10', 'class 10 / see'),
    ('9', 'class 9'),
    ('8', 'class 8'),
)
_CARD_FIELDS = ('id', 'display_name', 'class_level', 'is_bot', 'is_admin', 'moderator_level', 'role',
                'teacher_verified', 'institution_verified', 'verification_level') + AVATAR_FIELDS


def parse_limit(raw):
    try:
        limit = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_LIMIT
    return max(1, min(MAX_LIMIT, limit))


def _class_spellings(class_level):
    value = (class_level or '').strip().lower()
    if not value:
        return ()
    for spellings in _GRADE_SPELLINGS:
        if value in spellings:
            return spellings
    return (value,)


def _match(field, values):
    q = Q()
    for value in values:
        q |= Q(**{f'{field}__iexact': value})
    return q


def _flag(q, points):
    if q is None:
        return Value(0)
    return Case(When(q, then=Value(points)), default=Value(0), output_field=IntegerField())


def _follower_points():
    """min(follower_count, 60) // 5 in SQL, without relying on a backend's integer division."""
    return Case(*[When(follower_count__gte=5 * k, then=Value(k)) for k in range(12, 0, -1)],
                default=Value(0), output_field=IntegerField())


class _CodePointOrder(Func):
    """A text column as bytes, so ORDER BY compares it the way Python compares str (UTF-8
    byte order is code-point order) instead of by a case-insensitive collation. Works
    whatever the column's character set is."""
    template = '%(expressions)s'
    output_field = CharField()

    def as_mysql(self, compiler, connection, **extra):
        return self.as_sql(compiler, connection, template='CAST(%(expressions)s AS BINARY)', **extra)

    def as_sqlite(self, compiler, connection, **extra):
        return self.as_sql(compiler, connection, template='CAST(%(expressions)s AS BLOB)', **extra)

    def as_postgresql(self, compiler, connection, **extra):
        return self.as_sql(compiler, connection, template='%(expressions)s COLLATE "C"', **extra)


def _by_username():
    """ORDER BY username in the order Python sorts the final list in."""
    return _CodePointOrder('username').asc()


def _reason(follows_you, mutual_count, same_school, same_class):
    if follows_you:
        return 'Follows you'
    if mutual_count == 1:
        return '1 mutual connection'
    if mutual_count > 1:
        return f'{mutual_count} mutual connections'
    if same_school:
        return 'From your school'
    if same_class:
        return 'In your class'
    return 'Active in the forum'


def _detail(user):
    if (user.class_level or '').strip():
        return user.class_level
    badge = user_badge_info(user) or {}
    label = badge.get('label')
    return label if label and str(label).strip() else None


def suggest_people(viewer, limit=DEFAULT_LIMIT):
    """The top `limit` suggestions for `viewer`, best first, as API dicts."""
    me = viewer.pk

    followees, followers = set(), set()
    for follower_id, following_id in (Follow.objects.filter(Q(follower_id=me) | Q(following_id=me))
                                      .order_by().values_list('follower_id', 'following_id')):
        if follower_id == me:
            followees.add(following_id)
        else:
            followers.add(follower_id)
    requested = set(FollowRequest.objects.filter(sender_id=me).order_by().values_list('receiver_id', flat=True))
    excluded = followees | requested | {me}

    mutual = {}
    if followees:
        for following_id, n in (Follow.objects
                                .filter(follower_id__in=Follow.objects.filter(follower_id=me).values('following_id'))
                                .order_by().values('following_id').annotate(n=Count('pk'))
                                .values_list('following_id', 'n')):
            if following_id not in excluded:
                mutual[following_id] = n

    feed = set()
    recent = (Post.objects.filter(is_archived=False, is_anonymous=False, user__email_verified=True, user__is_bot=False)
              .order_by('-created_at').values_list('user_id', flat=True)[:FEED_POSTS])
    for user_id in recent:
        if user_id not in excluded:
            feed.add(user_id)

    school = (viewer.school or '').strip()
    school_q = Q(school__iexact=school) if school else None
    spellings = _class_spellings(viewer.class_level)
    class_q = _match('class_level', spellings) if spellings else None

    eligible = User.objects.filter(is_locked=False, is_banned=False, is_bot=False, email_verified=True)
    scored = {}

    def take(rows):
        for user_id, username, follower_count, ss, sc in rows:
            scored[user_id] = (username, follower_count, bool(ss), bool(sc))

    known = (followers | set(mutual) | feed) - excluded
    if known:
        take(eligible.filter(pk__in=known)
             .annotate(_ss=_flag(school_q, 1), _sc=_flag(class_q, 1))
             .values_list('id', 'username', 'follower_count', '_ss', '_sc'))
    if school_q is not None or class_q is not None:
        pool = school_q if class_q is None else class_q if school_q is None else school_q | class_q
        take(eligible.filter(pool)
             .exclude(pk=me)
             .exclude(pk__in=Follow.objects.filter(follower_id=me).values('following_id'))
             .exclude(pk__in=FollowRequest.objects.filter(sender_id=me).values('receiver_id'))
             .annotate(_ss=_flag(school_q, 1), _sc=_flag(class_q, 1),
                       _points=_flag(school_q, SAME_SCHOOL) + _flag(class_q, SAME_CLASS) + _follower_points())
             .order_by(F('_points').desc(), _by_username())
             .values_list('id', 'username', 'follower_count', '_ss', '_sc')[:limit])

    ranked = []
    for user_id, (username, follower_count, same_school, same_class) in scored.items():
        follows_you = user_id in followers
        mutual_count = mutual.get(user_id, 0)
        score = ((FOLLOWS_YOU if follows_you else 0)
                 + min(mutual_count, MAX_MUTUALS) * PER_MUTUAL
                 + (SAME_SCHOOL if same_school else 0)
                 + (SAME_CLASS if same_class else 0)
                 + (FEED_ACTIVE if user_id in feed else 0)
                 + min(follower_count, 60) // 5)
        ranked.append((-score, username, user_id, follows_you, mutual_count, same_school, same_class))
    ranked.sort()
    ranked = ranked[:limit]
    if not ranked:
        return []

    cards = {u.pk: u for u in User.objects.filter(pk__in=[r[2] for r in ranked]).only(*_CARD_FIELDS)}
    results = []
    for _neg, username, user_id, follows_you, mutual_count, same_school, same_class in ranked:
        user = cards.get(user_id)
        if user is None:  # deleted between the queries
            continue
        results.append({
            'id': str(user.pk),
            'username': user.username,
            'display_name': user.display_name if (user.display_name or '').strip() else user.username,
            'photo_url': avatar_or_photo_url(user) or None,
            'detail': _detail(user),
            'reason': _reason(follows_you, mutual_count, same_school, same_class),
            'follows_you': follows_you,
            'mutual_count': mutual_count,
        })
    return results
