"""Query count, latency and size of the website's own server-rendered pages.

    cd backend_python
    DB_ENGINE=sqlite DEBUG=1 python scripts/web_probe.py --out /tmp/neb-perf/web-before
    ... change code ...
    DB_ENGINE=sqlite DEBUG=1 python scripts/web_probe.py --out /tmp/neb-perf/web-after
    python scripts/perf_probe.py --compare /tmp/neb-perf/web-before /tmp/neb-perf/web-after

perf_probe.py's harness (a fresh copy of the seed database, its frozen clock, cold and warm
queries, bodies with CSRF tokens and nonces masked) pointed at the pages a browser loads,
anonymously and signed in as the seeded student. The site signs people in by putting their
auth token in the session, not through django.contrib.auth (api.User is not the auth user
model, so Client.force_login does not apply); the probe signs in through /auth/token-login/,
which writes the same session keys every login path writes. Anonymous warm calls to the pages
AnonPageCacheMiddleware serves (/, library, forum, news, faq) are page-cache hits. Page views
are not queued: the analytics worker would write them from a second thread, and on SQLite its
lock shows up as noise in the timings. ``--profile PATH`` prints a cProfile of 200 warm renders
of one page.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import perf_probe  # noqa: E402
from perf_seed import VIEWER_TOKEN  # noqa: E402

BROWSER = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'


def pages(t):
    v, star, locked = t['viewer'], t['star'], t['locked']
    both, auth, anon = ('anon', 'viewer'), ('viewer',), ('anon',)
    return [
        ('landing', '/', both),
        ('home', '/app/', both),
        ('home_feed_more', '/ajax/home/feed/?offset=20', both),
        ('library', '/app/library/', both),
        ('library_filtered', '/app/library/?subject=Physics&grade=Class+12', both),
        ('library_newest', '/app/library/?sort=newest', both),
        ('library_trending', '/app/library/?sort=trending&type=Video', both),
        ('library_paid', '/app/library/?pricing=paid&sort=liked', both),
        ('library_p3', '/app/library/?page=3', both),
        ('library_categories', '/app/library/?tab=categories', both),
        ('past_papers', '/app/past-papers/', both),
        ('forum', '/app/forum/', both),
        ('forum_new', '/app/forum/?sort=new', both),
        ('forum_top_p2', '/app/forum/?sort=top&page=2', both),
        ('forum_category', '/app/forum/?category=Physics', both),
        ('forum_search', '/app/forum/?q=energy', both),
        ('forum_categories', '/app/forum/categories/', both),
        ('leaderboard', '/app/forum/leaderboard/', both),
        ('forum_post', f'/app/forum/post/{t["busy"].id}/', both),
        ('forum_post_rich', f'/app/forum/post/{t["rich"].id}/', both),
        ('reader', f'/app/reader/{t["res_busy"].id}/', both),
        ('reader_paid', f'/app/reader/{t["paid"].id}/', both),
        ('news', '/app/news/', both),
        ('news_detail', f'/app/news/{t["news"].slug}/', both),
        ('profile', f'/app/profile/{star.username}/', both),
        ('profile_locked', f'/app/profile/{locked.username}/', both),
        ('profile_self', f'/app/profile/{v.username}/', auth),
        ('achievements', f'/app/profile/{star.username}/achievements/', both),
        ('notifications', '/app/notifications/', auth),
        ('notifications_unread', '/app/notifications/?tab=unread', auth),
        ('notifications_p3', '/app/notifications/?page=3&page_size=50', auth),
        ('bookmarks', '/app/bookmarks/', auth),
        ('search', '/app/search/?q=physics', both),
        ('search_posts', '/app/search/?q=energy+force&tab=posts', both),
        ('search_users', '/app/search/?q=sharma&tab=users', both),
        ('syllabus', '/app/syllabus/', both),
        ('syllabus_grade', '/app/syllabus/11/', both),
        ('syllabus_subject', '/app/syllabus/12/physics/', both),
        ('syllabus_chapter', '/app/syllabus/12/physics/unit-1/', both),
        ('syllabus_bank', '/app/syllabus/12/physics/bank-1/', both),
        ('syllabus_guide', '/app/syllabus/12/physics/exam-guide/', both),
        ('subject_page', '/app/subject/class-12/accountancy/', both),
        ('resource_requests', '/app/requests/', both),
        ('faq', '/app/faq/', both),
        ('tools', '/app/tools/', both),
        ('interactive', '/app/interactive/', both),
        ('results', '/app/results/', both),
        ('settings', '/app/settings/', auth),
        ('edit_profile', '/app/profile/edit/', auth),
        ('credits', '/app/credits/', auth),
        ('analytics', '/app/analytics/', auth),
        ('upload', '/app/upload/', auth),
        ('create_post', '/app/forum/create/', auth),
        ('study_lab', '/app/study-lab/', auth),
        ('login', '/login/', anon),
        ('sitemap', '/sitemap.xml', anon),
    ]


def client_for(who):
    from django.test import Client
    client = Client(HTTP_USER_AGENT=BROWSER)
    if who == 'viewer':
        client.get(f'/auth/token-login/?token={VIEWER_TOKEN}')
    return client


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--seed-db', default='/tmp/neb-perf/seed.sqlite3')
    parser.add_argument('--out', default='/tmp/neb-perf/web')
    parser.add_argument('--repeat', type=int, default=5)
    parser.add_argument('--only', help='regex on page names')
    parser.add_argument('--profile', metavar='PATH')
    parser.add_argument('--who', default='viewer')
    args = parser.parse_args()
    if os.environ.get('PYTHONHASHSEED') != '0':  # the home page's people rail is picked out of a set
        os.environ['PYTHONHASHSEED'] = '0'
        os.execv(sys.executable, [sys.executable] + sys.argv)
    os.makedirs(args.out, exist_ok=True)
    perf_probe.setup(args.seed_db, os.path.join(args.out, 'work.sqlite3'))
    from nebians import analytics_queue
    analytics_queue.submit = lambda item: None
    if args.profile:
        perf_probe.profile(args.profile, args.who, 200, make_client=client_for)
        return
    perf_probe.run(args.out, args.repeat, args.only, pages=pages, make_client=client_for)


if __name__ == '__main__':
    main()
