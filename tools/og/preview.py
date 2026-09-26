#!/usr/bin/env python3
"""Render one of each OG card to /tmp/og-preview/ for design review.

No Django. The card module is deliberately free of it, so the drawing can be
iterated on in a loop that takes a second rather than a deploy.

    tools/og/preview.py [outdir]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'backend_python'))

from web import og_cards as og  # noqa: E402

SAMPLES = [
    ('home.png', dict(kind='page', title="Nepal's Learning Community",
                      kicker='NEBians', hero='mark',
                      meta=('Free study material', 'nebians.consica.com.np'))),
    ('resource.png', dict(kind='resource', hero='paper', subject='Physics',
                          kicker='Past Paper',
                          title='NEB Class 12 Physics Board Exam 2081',
                          meta=('Class 12', 'Physics', '2081'))),
    ('resource2.png', dict(kind='resource', hero='paper', subject='Accountancy',
                           kicker='Model Question',
                           title='Accountancy Model Set with Full Solutions',
                           meta=('Class 11', 'Accountancy'))),
    ('post.png', dict(kind='post', hero='bubbles', subject='Mathematics',
                      kicker='Forum',
                      title='Why does integration by parts work the way it does?',
                      meta=('Mathematics', '24 replies'))),
    ('profile.png', dict(kind='profile', hero='avatar', subject='',
                         kicker='Profile', title='Nikit Hamal',
                         meta=('@nikit', '48 resources', '1.2k followers'))),
    ('library.png', dict(kind='page', hero='books', subject='Biology',
                         kicker='Library',
                         title='Every NEB subject, in one place',
                         meta=('Past papers', 'Notes', 'Model questions'))),
    ('faq.png', dict(kind='page', hero='question', kicker='Help centre',
                     title='Questions, answered.',
                     meta=('28 answers', 'nebians.consica.com.np'))),
    ('canvas.png', dict(kind='page', hero='graph', subject='Computer Science',
                        kicker='Canvas',
                        title='Think out loud, on an infinite board',
                        meta=('AI study tools',))),
    ('studylab.png', dict(kind='page', hero='flask', subject='Chemistry',
                          kicker='Study Lab',
                          title='Turn any document into a quiz',
                          meta=('Summaries', 'Mindmaps', 'Flashcards'))),
    ('subject.png', dict(kind='subject', hero='books', subject='Nepali',
                         kicker='Class 12', title='Nepali',
                         meta=('Past papers', 'Notes', 'Discussions'))),
    ('long.png', dict(kind='news', hero='paper', subject='Exam Tips',
                      kicker='Blog',
                      title='NEB publishes the Class 12 examination routine for 2082, '
                            'with practicals moved ahead of the written papers',
                      meta=('Blog', '6 min read'))),
]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/og-preview'
    os.makedirs(out, exist_ok=True)
    for name, kw in SAMPLES:
        img = og.render(**kw)
        path = os.path.join(out, name)
        with open(path, 'wb') as f:
            f.write(og.to_png(img))
        print('%-16s %6.1f KB  %s' % (name, os.path.getsize(path) / 1024.0, path))


if __name__ == '__main__':
    main()
