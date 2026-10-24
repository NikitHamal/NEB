#!/usr/bin/env python3
"""Render the share cards to a folder for design review.

No Django and no database for the page cards: the drawing module is
deliberately free of both, so iterating on a card takes a second rather than a
deploy. The routes that need the database (subjects, profiles, courses) are
covered by the tests instead.

    python3 tools/og/preview.py [outdir]

Writes one PNG per card plus a contact sheet of everything.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'backend_python'))

from PIL import Image  # noqa: E402

from web import og_cards as og  # noqa: E402

SAMPLES = [
    # name, title, kwargs
    ('home', "Nepal's Learning Community",
     dict(kind='page', kicker='NEBians', hero='mark', subject='',
          meta=('Free study material', 'nebians.consica.com.np'))),
    ('library', 'Every paper, note and book in one place',
     dict(kind='page', kicker='Library', hero='books', subject='Biology',
          meta=('Free to read', 'Free to download'))),
    ('past-paper', 'NEB Class 12 Physics Board Exam 2081',
     dict(kind='resource', kicker='Past Paper', hero='paper', subject='Physics',
          meta=('Class 12', 'Physics', '2081'))),
    ('notes', 'Accountancy Model Set with Full Solutions',
     dict(kind='resource', kicker='Model Question', hero='paper', subject='Accountancy',
          meta=('Class 11', 'Accountancy'))),
    ('forum', 'Why does integration by parts work the way it does?',
     dict(kind='post', kicker='Forum', hero='bubbles', subject='Mathematics',
          meta=('Mathematics', '24 replies'))),
    ('study-lab', 'Turn any document into a way to study',
     dict(kind='page', kicker='Study Lab', hero='flask', subject='Chemistry',
          meta=('Summaries', 'Quizzes', 'Flashcards'))),
    ('canvas', 'Think out loud on an infinite board',
     dict(kind='page', kicker='Canvas', hero='graph', subject='Computer Science',
          meta=('AI study canvas',))),
    ('faq', 'Questions, answered.',
     dict(kind='page', kicker='Help centre', hero='question', subject='',
          meta=('28 answers', 'nebians.consica.com.np'))),
    ('marketplace', 'Learn from teachers who have sat the exam',
     dict(kind='page', kicker='Marketplace', hero='cards', subject='Accountancy',
          meta=('Courses', 'Storefronts'))),
    ('leaderboard', 'The people who keep NEBians running',
     dict(kind='page', kicker='Forum', hero='spark', subject='English',
          meta=('Leaderboard',))),
    ('subject', 'Physics',
     dict(kind='subject', kicker='Class 12', hero='books', subject='Physics',
          meta=('Class 12', 'Notes, papers, solutions'))),
    ('profile', 'Nikit Hamal',
     dict(kind='profile', kicker='Profile', hero='avatar', subject='',
          meta=('@nikit', '48 posts', '1.2k followers'))),
    ('long-title', 'NEB publishes the Class 12 examination routine for 2082, '
                   'with practicals moved ahead of the written papers',
     dict(kind='news', kicker='Blog', hero='paper', subject='Exam Tips',
          meta=('Blog', '6 min read'))),
    ('one-word', 'Chemistry',
     dict(kind='subject', kicker='Class 11', hero='books', subject='Chemistry',
          meta=('Class 11', 'Notes, papers, solutions'))),
]


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    made = []
    for name, title, kw in SAMPLES:
        img = og.render(kw.pop('kind'), title, **kw)
        path = os.path.join(outdir, name + '.png')
        img.save(path)
        made.append((name, img, len(og.to_png(img))))
        print('%-12s %7.1f KB  %s' % (name, made[-1][2] / 1024.0, path))

    # A contact sheet: nine cards at a third size is the fastest way to see
    # whether the set holds together, which is the only question that matters
    # once the individual cards are right.
    cols, rows = 3, 3
    pick = [m for m in made if m[0] != 'home'][:cols * rows]
    if pick:
        sheet = Image.new('RGB', (1200 * cols, 630 * rows), (8, 10, 18))
        for i, (_, img, _) in enumerate(pick):
            sheet.paste(img, ((i % cols) * 1200, (i // cols) * 630))
        sheet = sheet.resize((1800, 945), Image.LANCZOS)
        sheet.save(os.path.join(outdir, 'contact-sheet.png'))
        print('contact-sheet  %s' % os.path.join(outdir, 'contact-sheet.png'))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '/tmp/og-preview')
