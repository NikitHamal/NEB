"""Deterministic, realistic dataset for measuring the API (see scripts/perf_probe.py).

    cd backend_python
    DB_ENGINE=sqlite DEBUG=1 python scripts/perf_seed.py --db /tmp/neb-perf/seed.sqlite3

Builds a fresh SQLite database (runs every migration first) holding ~600 users (photos,
badges, schools, class levels, private, banned, unverified, bots), a follow graph with pending
requests, ~4000 posts (images, polls, attachments, likes, bookmarks, ~12k replies), ~2600
resources (lead and non-lead, paid, comments, likes), notifications and news. The same seed
always produces byte-identical rows, and every timestamp is relative to FROZEN_NOW_MS, the
clock the probe freezes, so two probe runs over the same file can be diffed.

Two bearer tokens are stored (raw values printed at the end and in perf_probe.py):
``perf_viewer`` (a Class 12 student) and ``perf_teacher`` (a "global" user).
"""
import argparse
import hashlib
import os
import random
import sys
import time
import uuid

FROZEN_NOW_MS = 1_792_700_000_000          # 2026-10-23 ~05:33 UTC; the probe freezes time.time() here
SEED = 20261022
VIEWER_TOKEN = 'perf-viewer-token-0123456789abcdef0123456789abcdef'
TEACHER_TOKEN = 'perf-teacher-token-0123456789abcdef0123456789abcdef'
DAY = 86_400_000
HOUR = 3_600_000

N_USERS = 600
N_POSTS = 4000
N_RESOURCES = 2600

WORDS = ('the of and to in is for on that with as by this are from be at it an or which was '
         'energy force motion wave light atom cell organism equation function matrix limit '
         'derivative integral reaction acid base salt bond electron proton neutron gene protein '
         'enzyme market demand supply cost revenue profit ledger journal account balance trial '
         'grammar essay poem story novel tense clause verb noun nepal history geography civics '
         'computer program algorithm array loop variable database network question answer exam '
         'board model paper solution notes chapter unit exercise practice important syllabus '
         'class grade marks result routine teacher student school college please help explain').split()
FIRST = ('aarav sita ram gita hari shyam nisha pooja bibek sujan anil sunita rohan prakash kiran '
         'manish rajesh sarita binod anju deepak sabina suman nabin asmita roshan bikash srijana '
         'dipesh pratik aakash sneha rupa yubraj sagar laxmi samir puja niraj kabita').split()
LAST = ('sharma thapa shrestha adhikari khadka karki gurung tamang rai magar poudel bhandari '
        'koirala basnet regmi neupane ghimire pandey joshi bista').split()
SCHOOLS = ('Budhanilkantha School', "St. Xavier's College", 'Trinity International College',
           'Kathmandu Model College', 'Golden Gate International College', 'Pentagon College',
           'Little Angels School', 'Rato Bangala School', 'Global College of Management',
           'Uniglobe College', 'KMC Bagbazar', 'Xavier Academy', 'Shuvatara School',
           'Gyanodaya School', 'Pokhara Valley School', 'Biratnagar Secondary School')
CLASS_LEVELS = ('8', '9', '10', '11', '12', '12', '11', 'Class 12', 'Class 11', 'SEE',
                '+2 Passout', 'Bachelor', '')
SUBJECT_SETS = ('Physics,Chemistry,Mathematics', 'Biology,Chemistry,Physics', 'Accountancy,Economics',
                'Computer Science,Mathematics', 'English,Nepali,Social Studies', 'Mathematics,Science', '')
POST_CATEGORIES = ('Physics', 'Chemistry', 'Biology', 'Mathematics', 'English', 'Nepali',
                   'Computer Science', 'Accountancy', 'Economics', 'General', 'Social Studies', 'Career')
RES_SUBJECTS = ('Physics', 'Chemistry', 'Biology', 'Mathematics', 'English', 'Nepali',
                'Computer Science', 'Accountancy', 'Economics', 'Social Studies', 'Science',
                'Physics, Chemistry')
GRADES = ('Class 8', 'Class 9', 'Class 10 / SEE', 'Class 11', 'Class 12', 'Class 12', 'Class 11',
          'Bachelor', 'Diploma')
RES_TYPES = ('PDF', 'PDF', 'PDF', 'Note', 'Video', 'Link', 'Image', 'Audio')
EXAM_TYPES = ('', '', 'Board', 'Final', 'Notes', 'Reference', 'Mock', 'SEE')
VERBS = ('like_post', 'like_reply', 'reply', 'reply_reply', 'follow', 'mention', 'like_resource',
         'resource_comment', 'resource_approved', 'system')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--db', default='/tmp/neb-perf/seed.sqlite3', help='SQLite file to (re)create')
    args = parser.parse_args()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
    os.environ['DB_ENGINE'] = 'sqlite'
    os.environ.setdefault('DEBUG', '1')
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.makedirs(os.path.dirname(os.path.abspath(args.db)), exist_ok=True)
    if os.path.exists(args.db):
        os.remove(args.db)

    import django
    from django.conf import settings
    settings.DATABASES['default']['NAME'] = args.db
    django.setup()
    from django.core.management import call_command
    t0 = time.time()
    call_command('migrate', verbosity=0, interactive=False)
    print(f'migrated in {time.time() - t0:.0f}s')
    seed()


def seed():
    from django.db import connection, transaction
    from api.models import (
        Announcement, BlogComment, Bookmark, Follow, FollowRequest, Notification, PaymentVerification,
        Poll, PollOption, PollVote, Post, PostImage, PostLike, PostMedia, Reply, ReplyLike, Resource,
        ResourceComment, ResourceCommentLike, ResourceCommentMedia, ResourceLike, User, UserAuthToken,
        UserPhoto,
    )

    rng = random.Random(SEED)

    def new_id():
        return str(uuid.UUID(int=rng.getrandbits(128), version=4))

    def text(lo, hi):
        return ' '.join(rng.choice(WORDS) for _ in range(rng.randint(lo, hi)))

    def ago(max_days, *, recent_bias=2.0):
        """A timestamp up to max_days ago, skewed towards now."""
        return FROZEN_NOW_MS - int((rng.random() ** recent_bias) * max_days * DAY) - rng.randint(0, HOUR)

    # ------------------------------------------------------------------ users
    users = []
    taken = set()
    for i in range(N_USERS):
        if i == 0:
            username = 'perf_viewer'
        elif i == 1:
            username = 'perf_teacher'
        elif i < 5:
            username = ('neby', 'neby_helper', 'quizbot')[i - 2]
        else:
            while True:
                username = f'{rng.choice(FIRST)}{rng.choice(LAST)}{rng.randint(1, 999)}'
                if username not in taken:
                    break
        taken.add(username)
        # Google accounts have numeric ids, email signups uuids.
        uid = str(10**20 + rng.getrandbits(60)) if rng.random() < 0.6 else new_id()
        role = 'student'
        roll = rng.random()
        if roll < 0.07:
            role = 'teacher'
        elif roll < 0.10:
            role = 'institution'
        elif roll < 0.15:
            role = 'explorer'
        u = User(
            id=uid, username=username, email=f'{username}@example.np',
            display_name=f'{username.title()}' if rng.random() < 0.85 else '',
            role=role, dob='2007-01-01', gender=rng.choice(('male', 'female', 'other')),
            class_level=rng.choice(CLASS_LEVELS) if role == 'student' else '',
            subjects=rng.choice(SUBJECT_SETS),
            school=rng.choice(SCHOOLS) if rng.random() < 0.7 else '',
            district=rng.choice(('Kathmandu', 'Lalitpur', 'Kaski', 'Morang', '')),
            bio=text(10, 60) if rng.random() < 0.6 else '',
            email_verified=rng.random() > 0.05,
            is_locked=rng.random() < 0.08,
            is_banned=rng.random() < 0.01,
            created_at=ago(400, recent_bias=1.0),
            last_active=ago(30),
            achievement_badges='top_contributor,scholar' if rng.random() < 0.1 else '',
            verification_level=rng.randint(1, 4) if rng.random() < 0.1 else 0,
            moderator_level=rng.randint(1, 3) if rng.random() < 0.02 else 0,
            teacher_verified=role == 'teacher' and rng.random() < 0.5,
            institution_verified=role == 'institution' and rng.random() < 0.5,
            nebians_points=rng.randint(0, 500),
            free_credits=10, free_credits_month='2026-10',
        )
        if rng.random() < 0.3:
            u.photo_url = f'https://lh3.googleusercontent.com/a/ACg8oc{rng.getrandbits(64):x}=s96-c'
        if rng.random() < 0.12:
            u.avatar_use_pp = rng.random() < 0.7
            u.avatar_hue = rng.randint(0, 359)
            u.avatar_tone = round(rng.random(), 2)
            u.avatar_bg = rng.choice(('square', 'circle', 'squircle'))
            u.avatar_shape = rng.choice(('round', 'boxy', 'cloud'))
            u.avatar_expression = rng.choice(('happy', 'wink', 'thinking'))
            u.avatar_color = '#%06x' % rng.getrandbits(24)
        users.append(u)

    viewer, teacher = users[0], users[1]
    viewer.class_level, viewer.school, viewer.role = '12', SCHOOLS[0], 'student'
    viewer.subjects, viewer.is_locked, viewer.is_banned, viewer.email_verified = 'Physics,Chemistry,Mathematics', False, False, True
    viewer.photo_url = 'https://lh3.googleusercontent.com/a/perf-viewer=s96-c'
    viewer.display_name = 'Perf Viewer'
    teacher.role, teacher.class_level, teacher.teacher_verified = 'teacher', '', True
    teacher.is_locked, teacher.is_banned, teacher.email_verified = False, False, True
    for b in users[2:5]:
        b.is_bot, b.is_locked, b.is_banned, b.email_verified = True, False, False, True
    for a in users[5:7]:
        a.is_admin, a.is_locked, a.is_banned, a.email_verified = True, False, False, True
    # A handful of classmates from the viewer's school, so "From your school" has candidates.
    for u in users[7:40]:
        if rng.random() < 0.5:
            u.school = SCHOOLS[0]
    for u in users:
        u.auth_token = None
    for u, raw in ((viewer, VIEWER_TOKEN), (teacher, TEACHER_TOKEN)):
        u.auth_token = hashlib.sha256(raw.encode()).hexdigest()

    # Activity weights: a few very active members, a long tail.
    weight = [1.0 / ((i % 97) + 1) ** 0.9 + 0.01 for i in range(N_USERS)]
    rng.shuffle(weight)
    weight[0] = 0.3
    active = [u for u in users if u.email_verified and not u.is_banned]

    def pick_user(pool=None):
        pool = pool or users
        return rng.choices(pool, weights=[weight[users_index[u.id]] for u in pool])[0]

    users_index = {u.id: i for i, u in enumerate(users)}

    # ------------------------------------------------------------------ follows
    follows = {}
    requests = {}
    popularity = [w ** 0.7 for w in weight]
    for i, u in enumerate(users):
        k = min(70, int(rng.expovariate(1 / 12)))
        if i == 0:
            k = 0
        targets = set(rng.choices(range(N_USERS), weights=popularity, k=k))
        for t in targets:
            if t == i:
                continue
            target = users[t]
            if target.is_locked and rng.random() < 0.35:
                requests[(i, t)] = ago(60)
            else:
                follows[(i, t)] = ago(300, recent_bias=1.0)
    # The viewer: follows 40 people (some popular, some classmates), followed by 30, with
    # pending requests both ways.
    viewer_follows = rng.sample(range(5, N_USERS), 40)
    for t in viewer_follows:
        if users[t].is_locked and rng.random() < 0.3:
            requests[(0, t)] = ago(30)
        else:
            follows[(0, t)] = ago(200, recent_bias=1.0)
    for f in rng.sample(range(5, N_USERS), 30):
        follows[(f, 0)] = ago(200, recent_bias=1.0)
    for s in rng.sample(range(5, N_USERS), 4):
        if (s, 0) not in follows:
            requests[(s, 0)] = ago(10)
    locked = [i for i, u in enumerate(users) if u.is_locked and i > 4]
    for t in locked[:3]:
        if (0, t) not in follows:
            requests[(0, t)] = ago(10)

    follow_rows = [Follow(follower_id=users[a].id, following_id=users[b].id, created_at=ts)
                   for (a, b), ts in sorted(follows.items())]
    request_rows = [FollowRequest(id=new_id(), sender_id=users[a].id, receiver_id=users[b].id, created_at=ts)
                    for (a, b), ts in sorted(requests.items()) if (a, b) not in follows]
    follower_count = [0] * N_USERS
    following_count = [0] * N_USERS
    for a, b in follows:
        following_count[a] += 1
        follower_count[b] += 1

    # ------------------------------------------------------------------ posts
    posts, images, polls, options, media = [], [], [], [], []
    authors = [u for u in active if not u.is_banned]
    for n in range(N_POSTS):
        author = pick_user(authors)
        category = rng.choice(POST_CATEGORIES)
        long_content = rng.random() < 0.15
        p = Post(
            id=new_id(), user_id=author.id,
            title=f'{category}: {text(4, 12)}?'[:300],
            content=text(150, 700) if long_content else text(10, 120),
            category=category,
            view_count=int(rng.expovariate(1 / 60)),
            is_anonymous=rng.random() < 0.03,
            is_archived=rng.random() < 0.02,
            created_at=ago(300),
        )
        if rng.random() < 0.05:
            p.is_edited, p.edited_at = True, p.created_at + HOUR
        posts.append(p)
        if rng.random() < 0.15:
            for o in range(rng.randint(1, 3)):
                images.append(PostImage(id=new_id(), post_id=p.id, order=o, created_at=p.created_at,
                                        image_url=f'https://nebians.consica.com.np/media/post_images/{p.id}_{o}.jpg'))
        if rng.random() < 0.05:
            poll = Poll(id=new_id(), post_id=p.id, question=text(4, 10)[:300],
                        poll_type=rng.choice(('voting', 'mcq')), allow_multiple=rng.random() < 0.2,
                        explanation=text(5, 30) if rng.random() < 0.5 else '',
                        duration_ms=rng.choice((0, 86400000, 604800000)), created_at=p.created_at)
            polls.append(poll)
            for o in range(rng.randint(2, 5)):
                options.append(PollOption(id=new_id(), poll_id=poll.id, text=text(1, 5)[:200], order=o,
                                           is_correct=(o == 0 and poll.poll_type == 'mcq')))
        if rng.random() < 0.02:
            kind = rng.choice(('audio', 'file', 'video'))
            media.append(PostMedia(id=new_id(), post_id=p.id, kind=kind, name=f'{kind}.bin',
                                   url=f'https://nebians.consica.com.np/media/forum/{p.id}.{"mp4" if kind == "video" else "pdf"}',
                                   mime_type='application/octet-stream', size_bytes=rng.randint(1000, 10**7),
                                   created_at=p.created_at))
    post_index = {p.id: p for p in posts}

    # likes
    likes = set()
    for p in posts:
        k = min(150, int(rng.expovariate(1 / 4)))
        for u in rng.sample(users, k):
            likes.add((p.id, u.id))
    viewer_liked = rng.sample(posts, 120)
    for p in viewer_liked:
        likes.add((p.id, viewer.id))
    like_rows = [PostLike(post_id=pid, user_id=uid) for pid, uid in sorted(likes)]
    like_counts = {}
    for pid, _ in likes:
        like_counts[pid] = like_counts.get(pid, 0) + 1
    for p in posts:
        p.thumbs_up_count = like_counts.get(p.id, 0)

    # poll votes
    votes = []
    opts_by_poll = {}
    for o in options:
        opts_by_poll.setdefault(o.poll_id, []).append(o)
    for poll in polls:
        voters = rng.sample(users, min(len(users), int(rng.expovariate(1 / 15))))
        if rng.random() < 0.4 and viewer not in voters:
            voters.append(viewer)
        for v in voters:
            opt = rng.choice(opts_by_poll[poll.id])
            votes.append(PollVote(id=new_id(), poll_id=poll.id, option_id=opt.id, user_id=v.id,
                                  created_at=poll.created_at + HOUR))
            opt.vote_count += 1
        poll.total_votes = len(voters)

    # replies
    replies = []
    for p in posts:
        k = min(120, int(rng.expovariate(1 / 3)))
        thread = []
        for _ in range(k):
            parent = rng.choice(thread) if thread and rng.random() < 0.25 else None
            r = Reply(id=new_id(), post_id=p.id, user_id=pick_user(authors).id,
                      parent_reply_id=parent.id if parent else None,
                      content=text(5, 80), is_anonymous=rng.random() < 0.03,
                      created_at=p.created_at + rng.randint(60_000, 20 * DAY))
            if parent:
                parent.reply_count += 1
            thread.append(r)
            replies.append(r)
        p.reply_count = k
    reply_likes = set()
    for r in replies:
        for u in rng.sample(users, min(30, int(rng.expovariate(1 / 1.2)))):
            reply_likes.add((r.id, u.id))
    for r in rng.sample(replies, 60):
        reply_likes.add((r.id, viewer.id))
    reply_like_counts = {}
    for rid, _ in reply_likes:
        reply_like_counts[rid] = reply_like_counts.get(rid, 0) + 1
    for r in replies:
        r.thumbs_up_count = reply_like_counts.get(r.id, 0)
    reply_like_rows = [ReplyLike(reply_id=rid, user_id=uid) for rid, uid in sorted(reply_likes)]

    # ------------------------------------------------------------------ resources
    resources = []
    admins = users[5:7]
    for n in range(N_RESOURCES):
        source_type = 'user' if rng.random() < 0.6 else 'admin'
        uploader = pick_user(authors) if source_type == 'user' else rng.choice(admins + [None])
        status = 'approved' if n < 2500 else rng.choice(('pending', 'rejected'))
        subject = rng.choice(RES_SUBJECTS)
        paid = rng.random() < 0.04
        r = Resource(
            id=new_id(), title=f'{subject} {text(2, 8)}'[:255], description=text(20, 400),
            subject=subject, grade_level=rng.choice(GRADES), faculty=rng.choice(('Science', 'Management', '')),
            program=rng.choice(('+2 Science', 'BSc CSIT', '')), year=rng.choice(('2080', '2081', '2079', '')),
            exam_type=rng.choice(EXAM_TYPES), school=rng.choice(SCHOOLS) if rng.random() < 0.2 else '',
            tags=','.join(rng.choice(WORDS) for _ in range(rng.randint(0, 6))),
            type=rng.choice(RES_TYPES),
            file_url=f'https://nebians.consica.com.np/media/resources/2026/10/{n}.pdf',
            thumbnail_url=f'https://nebians.consica.com.np/media/thumbs/{n}.jpg' if rng.random() < 0.5 else '',
            file_size=rng.randint(10_000, 30_000_000), added_at=ago(500),
            view_count=int(rng.expovariate(1 / 150)), author_name=rng.choice(('', 'NEB', 'CDC')),
            source_type=source_type, uploaded_by_id=uploader.id if uploader else None,
            source_label=rng.choice(('', 'NEB Official', 'Contributed by students')),
            approval_status=status, is_lead=rng.random() < 0.8,
            upload_group_id=new_id(), is_paid=paid, price=rng.choice((50, 99, 150)) if paid else 0,
        )
        resources.append(r)
    # The viewer uploaded a few, one of them paid and one pending.
    for r in resources[:6]:
        r.uploaded_by_id, r.source_type = viewer.id, 'user'
    resources[2500].uploaded_by_id = viewer.id
    approved = [r for r in resources if r.approval_status == 'approved']
    res_likes = set()
    for r in approved:
        for u in rng.sample(users, min(80, int(rng.expovariate(1 / 3)))):
            res_likes.add((r.id, u.id))
    for r in rng.sample(approved, 50):
        res_likes.add((r.id, viewer.id))
    res_like_counts = {}
    for rid, _ in res_likes:
        res_like_counts[rid] = res_like_counts.get(rid, 0) + 1
    comments, comment_media = [], []
    for r in approved:
        r.like_count = res_like_counts.get(r.id, 0)
        k = min(60, int(rng.expovariate(1 / 2)))
        thread = []
        for _ in range(k):
            parent = rng.choice(thread) if thread and rng.random() < 0.3 else None
            c = ResourceComment(id=new_id(), resource_id=r.id, user_id=pick_user(authors).id,
                                parent_comment_id=parent.id if parent else None, content=text(3, 60),
                                created_at=r.added_at + rng.randint(60_000, 30 * DAY))
            if parent:
                parent.reply_count += 1
            thread.append(c)
            comments.append(c)
            if rng.random() < 0.03:
                comment_media.append(ResourceCommentMedia(id=new_id(), comment_id=c.id, kind='audio',
                                                          url=f'https://nebians.consica.com.np/media/voice/{c.id}.m4a',
                                                          name='voice.m4a', mime_type='audio/mp4', size_bytes=40000,
                                                          created_at=c.created_at))
        r.comment_count = k
    comment_likes = set()
    for c in comments:
        for u in rng.sample(users, min(20, int(rng.expovariate(1 / 0.8)))):
            comment_likes.add((c.id, u.id))
    comment_like_counts = {}
    for cid, _ in comment_likes:
        comment_like_counts[cid] = comment_like_counts.get(cid, 0) + 1
    for c in comments:
        c.like_count = comment_like_counts.get(c.id, 0)
    paid = [r for r in approved if r.is_paid and r.uploaded_by_id != viewer.id]
    purchases = []
    for r, status in zip(paid[:3], ('approved', 'approved', 'pending')):
        purchases.append(PaymentVerification(id=new_id(), buyer_id=viewer.id, resource_id=r.id,
                                             seller_id=r.uploaded_by_id or admins[0].id, amount=r.price,
                                             status=status, created_at=FROZEN_NOW_MS - 5 * DAY))

    # ------------------------------------------------------------------ bookmarks
    marks = set()
    for p in rng.sample(posts, 30):
        marks.add((viewer.id, 'post', p.id))
    for r in rng.sample(replies, 10):
        marks.add((viewer.id, 'reply', r.id))
    for r in rng.sample(approved, 20):
        marks.add((viewer.id, 'resource', r.id))
    for _ in range(3000):
        u = rng.choice(users)
        kind = rng.choice(('post', 'post', 'resource', 'reply'))
        target = rng.choice(posts if kind == 'post' else approved if kind == 'resource' else replies)
        marks.add((u.id, kind, target.id))
    bookmark_rows = [Bookmark(id=new_id(), user_id=u, target_type=k, target_id=t, created_at=ago(120))
                     for u, k, t in sorted(marks)]

    # ------------------------------------------------------------------ notifications
    notes = []
    unread = [0] * N_USERS
    for i in range(N_USERS):
        k = 400 if i == 0 else min(80, int(rng.expovariate(1 / 12)))
        for j in range(k):
            verb = rng.choice(VERBS)
            actor = rng.choice(users) if verb not in ('system', 'resource_approved') else None
            target_type = {'follow': 'user', 'like_resource': 'resource', 'resource_comment': 'resource',
                           'resource_approved': 'resource', 'system': 'system'}.get(verb, 'post')
            is_read = rng.random() < (0.94 if i == 0 else 0.7)
            if not is_read:
                unread[i] += 1
            notes.append(Notification(
                id=new_id(), recipient_id=users[i].id, actor_id=actor.id if actor else None,
                actor_anonymous=rng.random() < 0.03, verb=verb, target_type=target_type,
                target_id=rng.choice(posts).id, reference_type='post' if verb.startswith('reply') else '',
                reference_id=rng.choice(posts).id if verb.startswith('reply') else '',
                message=text(4, 14), is_read=is_read, created_at=ago(90)))

    # ------------------------------------------------------------------ photos, news
    photos = []
    for i, u in enumerate(users[:120]):
        for k in range(5 if i == 0 else rng.randint(0, 3)):
            photos.append(UserPhoto(user_id=u.id, url=f'https://nebians.consica.com.np/media/profile/{u.username}_{k}.jpg',
                                    uploaded_at=ago(200), is_current=(k == 0)))
    news, blog_comments = [], []
    for n in range(90):
        published = n < 80
        a = Announcement(id=new_id(), title=f'Notice {n}: {text(4, 10)}'[:255], slug=f'notice-{n}-{rng.getrandbits(24):x}',
                         summary=text(10, 30)[:500], content=text(100, 1200),
                         category=rng.choice(('exam_results', 'notice', 'event', 'update', 'alert', 'general')),
                         status='published' if published else 'draft', is_pinned=published and n < 6,
                         cover_image_url=f'https://nebians.consica.com.np/media/news/{n}.jpg' if rng.random() < 0.5 else '',
                         tags='neb,results' if rng.random() < 0.3 else 'notice',
                         author_id=admins[n % 2].id, published_at=ago(200), created_at=ago(200),
                         view_count=rng.randint(0, 5000))
        news.append(a)
        if published:
            for _ in range(rng.randint(0, 8)):
                blog_comments.append(BlogComment(id=new_id(), announcement_id=a.id, author_id=pick_user(authors).id,
                                                 text=text(3, 40), created_at=a.published_at + rng.randint(60_000, 5 * DAY)))

    # ------------------------------------------------------------------ denormalised counters
    post_counts, reply_counts = {}, {}
    for p in posts:
        post_counts[p.user_id] = post_counts.get(p.user_id, 0) + 1
    for r in replies:
        reply_counts[r.user_id] = reply_counts.get(r.user_id, 0) + 1
    given = {}
    for _, uid in likes:
        given[uid] = given.get(uid, 0) + 1
    received = {}
    for pid, _ in likes:
        owner = post_index[pid].user_id
        received[owner] = received.get(owner, 0) + 1
    for i, u in enumerate(users):
        u.follower_count = follower_count[i]
        u.following_count = following_count[i]
        u.post_count = post_counts.get(u.id, 0)
        u.reply_count = reply_counts.get(u.id, 0)
        u.likes_given_count = given.get(u.id, 0)
        u.likes_received_count = received.get(u.id, 0)
        u.contribution_score = u.post_count * 3 + u.reply_count * 2 + u.likes_given_count + u.likes_received_count * 2
        u.unread_notification_count = unread[i]

    token_rows = [UserAuthToken(id=new_id(), user_id=u.id, token_hash=u.auth_token, created_at=FROZEN_NOW_MS - DAY,
                                last_used_at=FROZEN_NOW_MS - DAY, revoked_at=0,
                                expires_at=FROZEN_NOW_MS + 365 * DAY)
                  for u in (viewer, teacher)]

    t0 = time.time()
    batch = 2000
    with transaction.atomic():
        User.objects.bulk_create(users, batch_size=batch)
        UserAuthToken.objects.bulk_create(token_rows)
        Follow.objects.bulk_create(follow_rows, batch_size=batch)
        FollowRequest.objects.bulk_create(request_rows, batch_size=batch)
        Post.objects.bulk_create(posts, batch_size=batch)
        PostImage.objects.bulk_create(images, batch_size=batch)
        PostMedia.objects.bulk_create(media, batch_size=batch)
        Poll.objects.bulk_create(polls, batch_size=batch)
        PollOption.objects.bulk_create(options, batch_size=batch)
        PollVote.objects.bulk_create(votes, batch_size=batch)
        PostLike.objects.bulk_create(like_rows, batch_size=batch)
        # Parents first: a reply's parent is always created earlier in its thread.
        Reply.objects.bulk_create(replies, batch_size=batch)
        ReplyLike.objects.bulk_create(reply_like_rows, batch_size=batch)
        Resource.objects.bulk_create(resources, batch_size=batch)
        ResourceLike.objects.bulk_create([ResourceLike(resource_id=r, user_id=u) for r, u in sorted(res_likes)],
                                         batch_size=batch)
        ResourceComment.objects.bulk_create(comments, batch_size=batch)
        ResourceCommentMedia.objects.bulk_create(comment_media, batch_size=batch)
        ResourceCommentLike.objects.bulk_create([ResourceCommentLike(comment_id=c, user_id=u)
                                                 for c, u in sorted(comment_likes)], batch_size=batch)
        PaymentVerification.objects.bulk_create(purchases)
        Bookmark.objects.bulk_create(bookmark_rows, batch_size=batch)
        Notification.objects.bulk_create(notes, batch_size=batch)
        UserPhoto.objects.bulk_create(photos, batch_size=batch)
        Announcement.objects.bulk_create(news, batch_size=batch)
        BlogComment.objects.bulk_create(blog_comments, batch_size=batch)
    with connection.cursor() as cur:
        cur.execute('ANALYZE')
    print(f'inserted in {time.time() - t0:.1f}s:', ', '.join(f'{m.__name__}={m.objects.count()}' for m in (
        User, Follow, FollowRequest, Post, PostImage, Poll, PostLike, Reply, ReplyLike, Resource, ResourceLike,
        ResourceComment, Bookmark, Notification, Announcement)))
    print(f'viewer={viewer.username} id={viewer.id} token={VIEWER_TOKEN}')
    print(f'teacher={teacher.username} id={teacher.id} token={TEACHER_TOKEN}')


if __name__ == '__main__':
    main()
