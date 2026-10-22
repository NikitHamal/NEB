"""Query count, latency and payload size of every endpoint the Android app calls.

    cd backend_python
    DB_ENGINE=sqlite DEBUG=1 python scripts/perf_seed.py --db /tmp/neb-perf/seed.sqlite3   # once
    DB_ENGINE=sqlite DEBUG=1 python scripts/perf_probe.py --out /tmp/neb-perf/before
    ... change code ...
    DB_ENGINE=sqlite DEBUG=1 python scripts/perf_probe.py --out /tmp/neb-perf/after
    python scripts/perf_probe.py --compare /tmp/neb-perf/before /tmp/neb-perf/after

Each run copies the seed database (so probes never see each other's writes), applies any new
migrations to the copy, freezes time.time() at the seed's clock (feed scores, poll expiry and
``generatedAt`` are then reproducible) and calls every endpoint anonymously and as the seeded
student with ``Authorization: Bearer <token>``, exactly like the app. Per call it records the
status, the queries of a cold call (cache cleared first) and of a warm one, the cold time, the
median of --repeat warm calls, and the response size; bodies go to OUT/bodies, the cold SQL to
OUT/sql. ``--compare`` diffs two runs' bodies and prints the before/after table.
``--profile PATH`` prints a cProfile of 200 warm calls to one URL (middleware overhead).
"""
import argparse
import functools
import json
import os
import re
import shutil
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from perf_seed import FROZEN_NOW_MS, TEACHER_TOKEN, VIEWER_TOKEN  # noqa: E402

FROZEN = FROZEN_NOW_MS / 1000.0
_NONCE = re.compile(r'(nonce-?[=:"\' ]*["\']?)[A-Za-z0-9_\-]{16,}', re.I)
_CSRF = re.compile(r'[A-Za-z0-9]{64}')


def setup(seed_db, work_db):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
    os.environ['DB_ENGINE'] = 'sqlite'
    os.environ.setdefault('DEBUG', '1')
    os.environ['ALLOWED_HOSTS'] = 'testserver,localhost,127.0.0.1'
    for scope in ('ANON', 'USER', 'AUTH', 'SEARCH', 'WRITE_ACTION', 'VIEW_INCREMENT'):
        os.environ[f'DRF_{scope}_THROTTLE'] = '100000000/hour'
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if work_db:
        shutil.copyfile(seed_db, work_db)
    # Freeze the clock before anything imports it. A partial, not a lambda: DRF keeps
    # `timer = time.time` as a class attribute, and a plain function would bind as a method.
    time.time = functools.partial(float, FROZEN)
    import django
    from django.conf import settings
    settings.DATABASES['default']['NAME'] = work_db or seed_db
    django.setup()
    if work_db:
        from django.core.management import call_command
        call_command('migrate', verbosity=0, interactive=False)


def targets():
    from api.models import Announcement, Post, Resource, User
    viewer = User.objects.get(username='perf_viewer')
    live = Post.objects.filter(is_archived=False, user__email_verified=True, is_anonymous=False)
    rich = (live.filter(images__isnull=False, poll__isnull=False).order_by('-created_at', 'id').first()
            or live.filter(images__isnull=False).order_by('-created_at', 'id').first())
    busy = live.order_by('-reply_count', 'id').first()
    res = Resource.objects.filter(approval_status='approved', is_lead=True)
    res_busy = res.order_by('-comment_count', 'id').first()
    paid = res.filter(is_paid=True).exclude(uploaded_by=viewer).order_by('id').first()
    people = User.objects.filter(is_locked=False, email_verified=True, is_bot=False, is_banned=False)
    star = people.exclude(pk=viewer.pk).order_by('-follower_count', 'id').first()
    locked = User.objects.filter(is_locked=True, email_verified=True).order_by('-follower_count', 'id').first()
    news = Announcement.objects.filter(status='published').order_by('-published_at', 'id').first()
    return dict(viewer=viewer, rich=rich, busy=busy, res_busy=res_busy, paid=paid, star=star, locked=locked, news=news)


def endpoints(t):
    v, star, locked = t['viewer'], t['star'], t['locked']
    both, auth = ('anon', 'viewer'), ('viewer',)
    return [
        ('posts', '/api/posts/', both),
        ('posts_p2', '/api/posts/?page=2', both),
        ('posts_category', '/api/posts/?category=Physics', both),
        ('posts_hot', '/api/posts/?sort=hot', both),
        ('posts_top', '/api/posts/?sort=top', both),
        ('posts_discussed', '/api/posts/?sort=discussed', both),
        ('posts_search', '/api/posts/?search=energy', both),
        ('posts_by_user', f'/api/posts/?username={star.username}', both),
        ('post_detail', f'/api/posts/{t["rich"].id}/', both),
        ('post_replies', f'/api/posts/{t["busy"].id}/replies/', both),
        ('resources', '/api/resources/?page_size=50', both),
        ('resources_newest', '/api/resources/?sort=newest&page_size=50', both),
        ('resources_trending', '/api/resources/?sort=trending&page_size=50', both),
        ('resources_liked', '/api/resources/?sort=liked&page_size=50', both),
        ('resources_p3', '/api/resources/?page=3&page_size=50', both),
        ('resources_filtered', '/api/resources/?subject=Physics&grade=Class%2012&page_size=50', both),
        ('resources_type', '/api/resources/?type=Video&sort=trending&page_size=50', both),
        ('resources_teacher', '/api/resources/?sort=newest&page_size=50', ('teacher',)),
        ('resource_detail', f'/api/resources/{t["res_busy"].id}/', both),
        ('resource_detail_paid', f'/api/resources/{t["paid"].id}/', both),
        ('resource_comments', f'/api/resources/{t["res_busy"].id}/comments/', both),
        ('feed_suggested', '/api/feed/suggested/', both),
        ('notifications', '/api/notifications/', auth),
        ('notifications_p2', '/api/notifications/?page=2', auth),
        ('notifications_unread', '/api/notifications/unread-count/', auth),
        ('bookmarks', '/api/bookmarks/', auth),
        ('search', '/api/search/?q=physics', both),
        ('search_posts', '/api/search/?q=energy%20force&tab=posts', both),
        ('search_people', '/api/search/?q=sharma&tab=people', both),
        ('profile', f'/api/users/profile/{star.username}/', both),
        ('profile_locked', f'/api/users/profile/{locked.username}/', both),
        ('profile_self', f'/api/users/profile/{v.username}/', auth),
        ('profile_stats', f'/api/users/profile/{star.username}/stats/', both),
        ('profile_stats_self', f'/api/users/profile/{v.username}/stats/', auth),
        ('followers', f'/api/users/{star.id}/followers/', both),
        ('following', f'/api/users/{star.id}/following/', both),
        ('followers_self', f'/api/users/{v.id}/followers/', auth),
        ('following_self', f'/api/users/{v.id}/following/', auth),
        ('follow_requests', '/api/users/me/follow-requests/', auth),
        ('users_search', '/api/users/search/?q=sharma', both),
        ('me_analytics', '/api/users/me/analytics/', auth),
        ('me_photos', '/api/users/me/photos/', auth),
        ('user_popup', f'/ajax/user-popup/{star.username}/', both),
        ('user_popup_self', f'/ajax/user-popup/{v.username}/', auth),
        ('profile_activity', f'/ajax/profile/{star.username}/activity/?offset=0&limit=10', both),
        ('suggestions', '/api/users/suggestions/?limit=12', both),
        ('news', '/app/news/', both),
        ('news_detail', f'/app/news/{t["news"].slug}/', both),
        ('site_theme', '/api/site-theme/', both),
        ('realtime_config', '/api/realtime/config/', both),
        ('credits_balance', '/api/credits/balance/', auth),
        ('syllabus_v2', '/api/syllabus/v2/', both),
        ('app_features', '/api/app/features/', both),
    ]


def client_for(who):
    from django.test import Client
    headers = {'HTTP_USER_AGENT': 'okhttp/4.12.0'}
    if who == 'viewer':
        headers['HTTP_AUTHORIZATION'] = f'Bearer {VIEWER_TOKEN}'
    elif who == 'teacher':
        headers['HTTP_AUTHORIZATION'] = f'Bearer {TEACHER_TOKEN}'
    return Client(**headers)


def normalise(body, ctype):
    if 'json' in ctype:
        try:
            return json.dumps(json.loads(body), indent=1, sort_keys=True, ensure_ascii=False)
        except ValueError:
            pass
    text = body.decode('utf-8', 'replace')
    return _CSRF.sub('<csrf>', _NONCE.sub(r'\1<n>', text))


def run(out, repeat, only):
    from django.core.cache import cache
    from django.db import connection
    from django.test.utils import CaptureQueriesContext

    os.makedirs(os.path.join(out, 'bodies'), exist_ok=True)
    os.makedirs(os.path.join(out, 'sql'), exist_ok=True)
    results = []
    todo = [(n, p, w) for n, p, w in endpoints(targets()) if not only or re.search(only, n)]
    for name, path, whos in todo:  # warm Python up (lazy imports, URL resolver, templates)
        for who in whos:
            client_for(who).get(path)
    for name, path, whos in todo:
        for who in whos:
            client = client_for(who)
            cache.clear()
            with CaptureQueriesContext(connection) as cold_q:
                t0 = time.perf_counter()
                resp = client.get(path)
                cold_ms = (time.perf_counter() - t0) * 1000
            body = resp.content
            times = []
            warm_n = 0
            for i in range(repeat):
                with CaptureQueriesContext(connection) as warm_q:
                    t0 = time.perf_counter()
                    again = client.get(path)
                    times.append((time.perf_counter() - t0) * 1000)
                warm_n = len(warm_q.captured_queries)
                if i == 0 and again.status_code == resp.status_code and 'json' in resp.get('Content-Type', ''):
                    if normalise(again.content, 'json') != normalise(body, 'json'):
                        print(f'  ! {name}/{who}: warm body differs from cold body')
            ctype = resp.get('Content-Type', '')
            with open(os.path.join(out, 'bodies', f'{name}__{who}.txt'), 'w') as fh:
                fh.write(f'{resp.status_code}\n{normalise(body, ctype)}\n')
            with open(os.path.join(out, 'sql', f'{name}__{who}.sql'), 'w') as fh:
                for q in cold_q.captured_queries:
                    fh.write(q['sql'] + ';\n')
            row = dict(name=name, who=who, path=path, status=resp.status_code, bytes=len(body),
                       cold_queries=len(cold_q.captured_queries), warm_queries=warm_n,
                       cold_ms=round(cold_ms, 2), warm_ms=round(statistics.median(times), 2))
            results.append(row)
            print(f'{name:22} {who:7} {row["status"]:3} q={row["cold_queries"]:4}/{row["warm_queries"]:<4} '
                  f'cold={row["cold_ms"]:8.1f}ms warm={row["warm_ms"]:8.1f}ms {row["bytes"]:9}B')
    with open(os.path.join(out, 'results.json'), 'w') as fh:
        json.dump(results, fh, indent=1)


def compare(a, b):
    import difflib
    ra = {(r['name'], r['who']): r for r in json.load(open(os.path.join(a, 'results.json')))}
    rb = {(r['name'], r['who']): r for r in json.load(open(os.path.join(b, 'results.json')))}
    print(f'{"endpoint":22} {"who":7} {"status":>7} {"cold q":>11} {"warm q":>11} {"cold ms":>15} {"warm ms":>15} {"bytes":>17}  body')
    for key in list(ra) + [k for k in rb if k not in ra]:
        x, y = ra.get(key), rb.get(key)
        if not x or not y:
            r = x or y
            side = 'before only' if x else 'after only'
            print(f'{key[0]:22} {key[1]:7} {r["status"]:>7} {r["cold_queries"]:>11} {r["warm_queries"]:>11} '
                  f'{r["cold_ms"]:>15} {r["warm_ms"]:>15} {r["bytes"]:>17}  {side}')
            continue
        fa = open(os.path.join(a, 'bodies', f'{key[0]}__{key[1]}.txt')).read()
        fb = open(os.path.join(b, 'bodies', f'{key[0]}__{key[1]}.txt')).read()
        same = 'same' if fa == fb else 'DIFF'
        print(f'{key[0]:22} {key[1]:7} {str(x["status"]) + ">" + str(y["status"]):>7} '
              f'{str(x["cold_queries"]) + "->" + str(y["cold_queries"]):>11} '
              f'{str(x["warm_queries"]) + "->" + str(y["warm_queries"]):>11} '
              f'{str(x["cold_ms"]) + "->" + str(y["cold_ms"]):>15} {str(x["warm_ms"]) + "->" + str(y["warm_ms"]):>15} '
              f'{str(x["bytes"]) + "->" + str(y["bytes"]):>17}  {same}')
        if fa != fb:
            diff = list(difflib.unified_diff(fa.splitlines(), fb.splitlines(), 'before', 'after', lineterm='', n=1))
            print('    ' + '\n    '.join(diff[:40]))


def profile(path, who, n):
    import cProfile
    import pstats
    client = client_for(who)
    client.get(path)
    prof = cProfile.Profile()
    t0 = time.perf_counter()
    prof.enable()
    for _ in range(n):
        client.get(path)
    prof.disable()
    print(f'{path} as {who}: {(time.perf_counter() - t0) * 1000 / n:.2f} ms/call over {n} calls')
    pstats.Stats(prof).sort_stats('cumulative').print_stats(45)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--seed-db', default='/tmp/neb-perf/seed.sqlite3')
    parser.add_argument('--out', default='/tmp/neb-perf/run')
    parser.add_argument('--repeat', type=int, default=5)
    parser.add_argument('--only', help='regex on endpoint names')
    parser.add_argument('--compare', nargs=2, metavar=('BEFORE', 'AFTER'))
    parser.add_argument('--profile', metavar='PATH')
    parser.add_argument('--who', default='viewer')
    args = parser.parse_args()
    if args.compare:
        compare(*args.compare)
        return
    os.makedirs(args.out, exist_ok=True)
    setup(args.seed_db, os.path.join(args.out, 'work.sqlite3'))
    if args.profile:
        profile(args.profile, args.who, 200)
        return
    run(args.out, args.repeat, args.only)


if __name__ == '__main__':
    main()
