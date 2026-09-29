"""Creator marketplace -- ready-made pages a creator can start from.

Nobody's first page should be a blank form. The research on mobile builders is
blunt about it: composing block-by-block on a phone is painful, inserting a
finished section is not, and the builders people actually finish pages in put a
pattern gallery in front of the blank canvas.

So a template here is a *whole page*: a theme, a layout, and a full set of
sections already written in the voice of a Nepali tutor or institute. Applying
one leaves a creator with a page they could publish as-is and then edit down,
instead of twenty-five section names and no idea which they need.

`{name}` and `{subject}` in any string are filled in from the creator's own
profile as the template is applied, so the copy reads as theirs from the first
second. Anything the creator has already written is never overwritten by a
template -- see `apply_template()` for exactly what it touches.
"""
from .creator_themes import DEFAULT_PALETTE, palette


def _style(palette, scheme='light', hero='art', font='sans', pattern='none',
           card='elevated', radius='round', density='comfortable', width='standard',
           gallery_columns=3, show_stats=True, show_contact=True, show_verified=True):
    return {
        'palette': palette, 'scheme': scheme, 'hero': hero, 'font': font,
        'pattern': pattern, 'card': card, 'radius': radius, 'density': density,
        'width': width, 'gallery_columns': gallery_columns,
        'show_stats': show_stats, 'show_contact': show_contact,
        'show_verified': show_verified,
    }


def _b(block_type, **fields):
    """One section of a template.

    The id defaults to the type so a template's own buttons can link to it --
    `#courses`, `#pricing`, `#contact` are the most useful links a storefront
    has, and they only work if the target's anchor is predictable. Duplicates
    are renumbered by `sanitize_blocks`, so a second shelf is still safe.
    """
    fields.setdefault('id', block_type)
    return dict(type=block_type, **fields)


TEMPLATES = [
    {
        'id': 'tuition-classic',
        'name': 'Tuition Classic',
        'summary': 'The dependable one. Batches, timetable, parents reassured.',
        'best_for': 'A tutor running regular batches who wants to look established',
        'kinds': ('tutor', 'institute'),
        'layout': 'editorial',
        'style': _style('teal', hero='art', font='sans', pattern='dots'),
        'blocks': [
            _b('hero', title='{name}', subtitle='{subject} classes that actually make sense.',
               cta_label='See this year’s batches', cta_url='#courses'),
            _b('stats', title='', items=[
                {'label': 'Years teaching', 'value': '8'},
                {'label': 'Students taught', 'value': '600+'},
                {'label': 'Batch size', 'value': '20 max'},
            ], settings={'tone': 'soft', 'align': 'center'}),
            _b('about', title='About me',
               body='I have been teaching {subject} in Nepal for years, and I teach the way I '
                    'wish I had been taught: work the problem on the board, then hand the chalk '
                    'over. Every class ends with something you can do on your own that evening.'),
            _b('courses', title='Batches running now', subtitle='Paid and free'),
            _b('schedule', title='Weekly timetable', items=[
                {'day': 'Sun / Tue / Thu', 'time': '6:30 - 8:00 AM', 'title': 'Grade 12 {subject}',
                 'note': 'Board-focused, full syllabus'},
                {'day': 'Mon / Wed / Fri', 'time': '5:00 - 6:30 PM', 'title': 'Grade 11 {subject}',
                 'note': 'Foundations, from scratch'},
                {'day': 'Saturday', 'time': '9:00 - 11:00 AM', 'title': 'Doubt clearing',
                 'note': 'Free for enrolled students'},
            ]),
            _b('testimonials', title='What my students say', items=[
                {'name': 'Aashish K.', 'role': 'Grade 12, 2081 batch',
                 'quote': 'I went from failing the terminal to an A in the boards. He does not '
                          'move on until the last person in the room has it.'},
                {'name': 'Prasamsa T.', 'role': 'Grade 11',
                 'quote': 'The notes alone are worth it. Everything is in order and nothing is missing.'},
            ]),
            _b('faq', title='Before you join', items=[
                {'q': 'Can I join mid-term?', 'a': 'Yes. I will give you the recordings and notes '
                                                  'for everything you missed, at no extra cost.'},
                {'q': 'Is there a trial class?', 'a': 'Come to any class free once. Decide after.'},
                {'q': 'How do I pay?', 'a': 'eSewa, Khalti or cash. Monthly or for the full course.'},
            ]),
            _b('resources', title='Free notes', subtitle='Everything I hand out in class'),
            _b('contact', title='Get in touch',
               body='Message me any time. I answer within a day, usually much sooner.'),
        ],
    },
    {
        'id': 'institute-bold',
        'name': 'Institute Bold',
        'summary': 'Dark, confident, prospectus-grade. Built to be trusted.',
        'best_for': 'An institute with faculty, results and a building',
        'kinds': ('institute', 'admin'),
        'layout': 'magazine',
        'style': _style('ink', scheme='dark', hero='banner', font='display',
                        pattern='glow', card='flat', radius='sharp', width='wide'),
        'blocks': [
            _b('hero', title='{name}', subtitle='Preparing Nepal’s next batch of doctors, '
                                                'engineers and analysts.',
               cta_label='Admissions open', cta_url='#courses'),
            _b('banner', title='Admissions for the 2082 session are open',
               subtitle='Entrance test every Saturday, 10 AM', cta_label='Book a seat',
               cta_url='#contact', settings={'tone': 'accent'}),
            _b('stats', title='', items=[
                {'label': 'Students', 'value': '2,400+'},
                {'label': 'Faculty', 'value': '38'},
                {'label': 'Board A+ last year', 'value': '112'},
                {'label': 'Years', 'value': '15'},
            ], settings={'tone': 'contrast'}),
            _b('about', title='Who we are',
               body='{name} has been teaching in Kathmandu for fifteen years. We run small '
                    'sections, we publish our results, and every teacher here is somebody we '
                    'would send our own children to.'),
            _b('courses', title='Programmes', subtitle='Science, Management and entrance preparation'),
            _b('team', title='Faculty', subtitle='The people who will actually teach you', items=[
                {'name': 'Dr. S. Adhikari', 'role': 'Physics — MSc, 12 years',
                 'note': 'Entrance specialist. Has taught over 3,000 students.'},
                {'name': 'R. Maharjan', 'role': 'Mathematics — MSc',
                 'note': 'Board topper mentor for six consecutive years.'},
                {'name': 'A. Gurung', 'role': 'Chemistry — MSc',
                 'note': 'Writes our practical manual.'},
            ]),
            _b('timeline', title='Our results, year by year', items=[
                {'label': '2081', 'title': '112 A+ in the board exam', 'note': 'Out of 340 appearing'},
                {'label': '2080', 'title': '96 A+, 4 in the national top 50', 'note': ''},
                {'label': '2079', 'title': 'Best Science result in the district', 'note': ''},
            ]),
            _b('gallery', title='Inside the institute', subtitle='Classrooms, labs and library', images=[]),
            _b('testimonials', title='Parents and students', items=[
                {'name': 'Sita Rai', 'role': 'Parent',
                 'quote': 'They called me every month with an honest report. Not once did I have '
                          'to chase them for information.'},
            ]),
            _b('logos', title='Affiliations and partners', items=[]),
            _b('contact', title='Visit us', body='Walk in any weekday between 7 AM and 6 PM.'),
        ],
    },
    {
        'id': 'minimal-tutor',
        'name': 'Quiet Minimal',
        'summary': 'Serif, generous white space, nothing shouting. Very high trust.',
        'best_for': 'A tutor whose reputation does the selling',
        'kinds': ('tutor', 'institute'),
        'layout': 'stack',
        'style': _style('slate', hero='center', font='serif', pattern='none',
                        card='flat', radius='soft', density='airy', width='narrow',
                        show_stats=False),
        'blocks': [
            _b('hero', title='{name}', subtitle='{subject}. One-to-one and small groups.',
               cta_label='Enquire', cta_url='#contact', settings={'align': 'center'}),
            _b('about', title='',
               body='I teach {subject} to students who want to understand it rather than "finish" '
                    'it. Sessions are one hour, twice a week, and I take a small number of students '
                    'at a time so that I actually know how each one is doing.',
               settings={'align': 'center'}),
            _b('quote', title='Teach the student in front of you, not the syllabus behind them.',
               subtitle='', settings={'align': 'center'}),
            _b('courses', title='What I offer', subtitle=''),
            _b('divider'),
            _b('links', title='Elsewhere', items=[]),
            _b('contact', title='Get in touch', body=''),
        ],
    },
    {
        'id': 'course-studio',
        'name': 'Course Studio',
        'summary': 'Offer first. Price, proof, one button. Built to convert.',
        'best_for': 'Selling a specific course rather than general tuition',
        'kinds': ('tutor', 'institute', 'admin'),
        'layout': 'spotlight',
        'style': _style('violet', hero='split', font='sans', pattern='mesh', card='elevated'),
        'blocks': [
            _b('hero', title='Pass {subject}. Properly.',
               subtitle='A complete course by {name} — recorded lessons, live doubt sessions '
                        'and every note you need.',
               cta_label='See what is included', cta_url='#pricing'),
            _b('steps', title='How it works', subtitle='Three steps, no surprises', items=[
                {'title': 'Enrol', 'note': 'Pay through eSewa or Khalti. Access opens immediately.'},
                {'title': 'Learn at your pace', 'note': 'Watch lessons whenever. Notes attached to each.'},
                {'title': 'Ask anything', 'note': 'Live doubt session every Saturday, for as long as you need.'},
            ]),
            _b('video', title='A look inside', subtitle='One full lesson, free', media_url=''),
            _b('pricing', title='What it costs', subtitle='One payment. No renewals.', items=[
                {'name': 'Self-paced', 'price': '2,500', 'period': 'one time',
                 'features': 'All recorded lessons\nEvery note and past paper\nLifetime access',
                 'cta_label': 'Start now', 'cta_url': '#courses'},
                {'name': 'Guided', 'price': '5,000', 'period': 'one time', 'badge': 'Most chosen',
                 'features': 'Everything in Self-paced\nWeekly live doubt session\n'
                             'Assignments marked by me\nA WhatsApp group that I am in',
                 'cta_label': 'Join the batch', 'cta_url': '#courses'},
            ]),
            _b('courses', title='Enrol', subtitle=''),
            _b('testimonials', title='From students who finished it', items=[
                {'name': 'Bibek S.', 'role': 'Completed 2081',
                 'quote': 'I had given up on {subject}. Four months later it was my highest mark.'},
            ]),
            _b('faq', title='Questions', items=[
                {'q': 'How long do I have access?', 'a': 'Forever. It does not expire.'},
                {'q': 'What if it is not for me?', 'a': 'Tell me within a week and I will refund you in full.'},
            ]),
            _b('cta', title='Ready when you are', subtitle='Seats in the guided batch are limited.',
               cta_label='Enrol now', cta_url='#courses', settings={'tone': 'accent', 'align': 'center'}),
        ],
    },
    {
        'id': 'exam-prep',
        'name': 'Exam Countdown',
        'summary': 'Urgent and organised. Results up front, timetable next.',
        'best_for': 'Board and entrance preparation with a deadline',
        'kinds': ('tutor', 'institute'),
        'layout': 'editorial',
        'style': _style('crimson', hero='gradient', font='sans', pattern='rays', radius='soft'),
        'blocks': [
            _b('banner', title='Board exams begin in Chaitra',
               subtitle='Revision batch starts this Sunday', cta_label='Reserve a seat',
               cta_url='#contact', settings={'tone': 'accent'}),
            _b('hero', title='{name}', subtitle='Board and entrance preparation for {subject}.',
               cta_label='See the revision plan', cta_url='#schedule'),
            _b('stats', title='', items=[
                {'label': 'A+ last year', 'value': '41'},
                {'label': 'Pass rate', 'value': '98%'},
                {'label': 'Mock tests', 'value': '24'},
            ], settings={'tone': 'soft'}),
            _b('timeline', title='Results', subtitle='Published every year, unedited', items=[
                {'label': '2081', 'title': '41 A+', 'note': 'From 96 students'},
                {'label': '2080', 'title': '33 A+', 'note': 'From 88 students'},
            ]),
            _b('courses', title='Revision batches', subtitle='Starting this month'),
            _b('schedule', title='The plan, week by week', items=[
                {'day': 'Weeks 1-3', 'time': '', 'title': 'Full syllabus sweep',
                 'note': 'Chapter by chapter, with a test after each'},
                {'day': 'Weeks 4-5', 'time': '', 'title': 'Past papers',
                 'note': 'Ten years of board questions, timed'},
                {'day': 'Week 6', 'time': '', 'title': 'Weak areas only',
                 'note': 'Built from your own test results'},
            ]),
            _b('documents', title='Past papers and model sets', subtitle='Free to download'),
            _b('faq', title='Common questions', items=[
                {'q': 'Is it too late to join?', 'a': 'No. Tell me where you are and I will tell you '
                                                     'honestly what we can cover in the time left.'},
            ]),
            _b('cta', title='Start this week', subtitle='Every week you wait is a chapter.',
               cta_label='Message me', cta_url='#contact', settings={'tone': 'accent', 'align': 'center'}),
        ],
    },
    {
        'id': 'notes-shop',
        'name': 'Notes Shop',
        'summary': 'A storefront for material. Notes first, everything else after.',
        'best_for': 'Selling notes, guides and past papers',
        'kinds': ('tutor', 'institute', 'admin'),
        'layout': 'grid',
        'style': _style('amber', hero='banner', font='rounded', pattern='grid',
                        card='outlined', radius='round'),
        'blocks': [
            _b('hero', title='{name}', subtitle='Handwritten {subject} notes, typed up and kept current.',
               cta_label='Browse the shelf', cta_url='#resources'),
            _b('resources', title='On the shelf', subtitle='Notes, papers and guides'),
            _b('documents', title='Free samples', subtitle='Read a few pages before you buy'),
            _b('pricing', title='Bundles', subtitle='Cheaper together', items=[
                {'name': 'Single chapter', 'price': '50', 'period': 'each',
                 'features': 'One chapter, fully worked\nPDF, print-ready'},
                {'name': 'Full year', 'price': '600', 'period': 'one time', 'badge': 'Best value',
                 'features': 'Every chapter\nPast paper solutions\nFree updates all year'},
            ]),
            _b('testimonials', title='Reviews', items=[
                {'name': 'Nirajan P.', 'role': 'Grade 12',
                 'quote': 'Clearer than the textbook and a third of the length.'},
            ]),
            _b('about', title='Why these notes exist',
               body='I wrote these for my own students because the textbook buries the point. '
                    'Every chapter is the shortest version I could write that still holds up in '
                    'the board exam.'),
            _b('contact', title='Questions about a set?', body=''),
        ],
    },
    {
        'id': 'portfolio-grid',
        'name': 'Portfolio Grid',
        'summary': 'Picture-led. For work that has to be seen to be believed.',
        'best_for': 'Art, design, practicals, project-based teaching',
        'kinds': ('tutor', 'institute'),
        'layout': 'grid',
        'style': _style('rose', hero='cover', font='display', pattern='none',
                        card='flat', radius='sharp', gallery_columns=2, show_stats=False),
        'blocks': [
            _b('hero', title='{name}', subtitle='{subject}, taught by making things.',
               cta_label='See student work', cta_url='#gallery'),
            _b('gallery', title='Student work', subtitle='From the last two batches', images=[]),
            _b('showcase', title='Selected projects', subtitle='', items=[
                {'title': 'Working model — Grade 12', 'subtitle': 'Built in four weeks', 'badge': 'Award'},
            ]),
            _b('about', title='How I teach',
               body='Theory in the first half hour, hands on the table for the rest. Everything '
                    'my students make ends up on this page.'),
            _b('courses', title='Join a batch', subtitle=''),
            _b('contact', title='Get in touch', body=''),
        ],
    },
    {
        'id': 'link-hub',
        'name': 'Link Hub',
        'summary': 'One screen, everything you point people to. Very phone-first.',
        'best_for': 'A bio link — short, scannable, all thumbs',
        'kinds': ('tutor', 'institute', 'admin'),
        'layout': 'stack',
        'style': _style('sky', hero='center', font='rounded', pattern='waves',
                        card='elevated', radius='pill', density='compact',
                        width='narrow', show_stats=False),
        'blocks': [
            _b('hero', title='{name}', subtitle='{subject} — everything in one place.',
               cta_label='', cta_url='', settings={'align': 'center'}),
            _b('links', title='', items=[], settings={'align': 'center'}),
            _b('courses', title='Classes', subtitle=''),
            _b('resources', title='Free notes', subtitle=''),
            _b('posts', title='Latest', subtitle=''),
            _b('contact', title='Reach me', body='', settings={'align': 'center'}),
        ],
    },
    {
        'id': 'night-editorial',
        'name': 'Night Editorial',
        'summary': 'Black page, serif type, long reads. Quietly expensive-looking.',
        'best_for': 'A teacher who writes, and wants the writing to carry',
        'kinds': ('tutor', 'institute', 'admin'),
        'layout': 'magazine',
        'style': _style('ink', scheme='dark', hero='plain', font='serif',
                        pattern='none', card='flat', radius='sharp',
                        density='airy', width='narrow', show_stats=False),
        'blocks': [
            _b('hero', title='{name}', subtitle='On teaching {subject}.',
               cta_label='Read', cta_url='#posts'),
            _b('about', title='',
               body='I have taught {subject} long enough to know that most students do not have '
                    'a maths problem or a physics problem. They have a "nobody ever explained the '
                    'first step" problem. This page is where I explain first steps.'),
            _b('quote', title='Every hard subject is an easy subject with a missing sentence.',
               subtitle='', settings={'align': 'center'}),
            _b('posts', title='Writing', subtitle=''),
            _b('courses', title='Classes', subtitle=''),
            _b('richtext', title='The long version', subtitle='',
               body='If you want the full argument rather than the summary, start here.',
               cta_label='Read the essay', cta_url=''),
            _b('contact', title='Correspondence', body=''),
        ],
    },
    {
        'id': 'academy-pro',
        'name': 'Academy Pro',
        'summary': 'The full prospectus: faculty, fees, timetable, FAQ. Everything answered.',
        'best_for': 'An institute that gets the same ten questions every day',
        'kinds': ('institute', 'admin'),
        'layout': 'editorial',
        'style': _style('forest', hero='split', font='sans', pattern='dots', width='wide'),
        'blocks': [
            _b('hero', title='{name}', subtitle='{subject} — taught properly, priced honestly.',
               cta_label='Fees and batches', cta_url='#pricing'),
            _b('stats', title='', items=[
                {'label': 'Running batches', 'value': '9'},
                {'label': 'Students', 'value': '380'},
                {'label': 'Teachers', 'value': '14'},
            ], settings={'tone': 'soft'}),
            _b('about', title='About {name}',
               body='We are a small academy and we intend to stay one. Twenty students to a '
                    'section, one teacher who knows every name, and a monthly report that goes '
                    'to the parent whether the news is good or not.'),
            _b('courses', title='Batches', subtitle='Open for enrolment'),
            _b('pricing', title='Fees', subtitle='Published, so nobody has to ask', items=[
                {'name': 'Single subject', 'price': '1,800', 'period': 'month',
                 'features': 'Three classes a week\nMonthly test\nAll notes'},
                {'name': 'Science package', 'price': '4,500', 'period': 'month', 'badge': 'Popular',
                 'features': 'Physics, Chemistry, Maths\nLab sessions\nWeekly mock test\n'
                             'Doubt hours every day'},
            ]),
            _b('team', title='Our teachers', subtitle='', items=[]),
            _b('schedule', title='Timetable', items=[]),
            _b('faq', title='Frequently asked', items=[
                {'q': 'Do you run a demo class?', 'a': 'Yes, any day of the week. Just walk in.'},
                {'q': 'Is the fee monthly or for the course?',
                 'a': 'Monthly. You can stop any month, and we do not ask for a deposit.'},
                {'q': 'Do you help with the entrance exam?',
                 'a': 'Yes — a dedicated batch starts after the board exams finish.'},
            ]),
            _b('contact', title='Come and see the place', body='We would rather you visited than '
                                                               'took our word for it.'),
        ],
    },
]

TEMPLATES_BY_ID = {entry['id']: entry for entry in TEMPLATES}


def template_list(kind=None):
    """The gallery payload. `kind` filters to what this creator can use."""
    return [
        {
            'id': entry['id'],
            'name': entry['name'],
            'summary': entry['summary'],
            'best_for': entry['best_for'],
            'kinds': list(entry['kinds']),
            'layout': entry['layout'],
            'style': entry['style'],
            # Resolved here so a gallery card can paint itself in the template's
            # own colours. A thumbnail that is the wrong colour is worse than no
            # thumbnail: it is the one thing a creator is choosing by.
            'colors': palette(entry['style']['palette'], entry['style'].get('scheme', 'light')),
            'sections': [block['type'] for block in entry['blocks']],
            'section_count': len(entry['blocks']),
        }
        for entry in TEMPLATES
        if kind is None or kind in entry['kinds']
    ]


def _fill(value, name, subject):
    if not isinstance(value, str) or '{' not in value:
        return value
    return value.replace('{name}', name).replace('{subject}', subject)


def _fill_deep(value, name, subject):
    if isinstance(value, str):
        return _fill(value, name, subject)
    if isinstance(value, list):
        return [_fill_deep(item, name, subject) for item in value]
    if isinstance(value, dict):
        return {key: _fill_deep(item, name, subject) for key, item in value.items()}
    return value


def template_payload(template_id, name='', subject=''):
    """A template resolved for one creator, ready to hand to `sanitize_*`.

    Returns `(layout, style, blocks)` or `None` for an id we do not have. The
    caller decides what to do with them -- this function neither saves nor
    validates, which keeps the same code path in front of template blocks and
    hand-written ones.
    """
    entry = TEMPLATES_BY_ID.get(template_id)
    if not entry:
        return None
    display = name.strip() or 'Your page'
    topic = (subject or '').strip() or 'your subject'
    blocks = _fill_deep(entry['blocks'], display, topic)
    return entry['layout'], dict(entry['style']), blocks


DEFAULT_TEMPLATE_STYLE = _style(DEFAULT_PALETTE)
