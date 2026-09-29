"""Creator marketplace — the block catalogue every surface renders from.

A storefront is data, not markup: this module is the single list of block
types, the fields each one carries, the labels the editors show and the style
vocabulary a page may use. The Django templates, the studio editor and the
Android builder all read `block_schema()`, so adding a section here is what
makes it appear on both platforms.
"""
import re

from .creator_themes import (
    BLOCK_ALIGNS, BLOCK_TONES, BLOCK_WIDTHS, CARD_STYLES, DENSITIES, FONTS,
    HERO_STYLES, PALETTES, PATTERNS, RADII, SCHEMES, WIDTHS, theme_vocabulary,
)
from .models import User


ELIGIBLE_ROLES = (User.ROLE_TEACHER, User.ROLE_INSTITUTION)

MAX_BLOCKS = 24
MAX_LIST_ITEMS = 24
ACCENT_RE = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')

LAYOUTS = ('editorial', 'spotlight', 'grid', 'classic', 'magazine', 'stack')

BLOCK_FIELDS = {
    'hero': ('title', 'subtitle', 'cta_label', 'cta_url', 'image_url'),
    'about': ('title', 'body'),
    'stats': ('title',),
    'courses': ('title', 'subtitle'),
    'resources': ('title', 'subtitle'),
    'posts': ('title', 'subtitle'),
    'showcase': ('title', 'subtitle'),
    'gallery': ('title', 'subtitle'),
    'testimonials': ('title',),
    'faq': ('title',),
    'schedule': ('title',),
    'contact': ('title', 'body'),
    'links': ('title',),
    'cta': ('title', 'subtitle', 'cta_label', 'cta_url'),
    'documents': ('title', 'subtitle'),
    # --- sections added with the theme work -------------------------------
    # Each one exists because a storefront could not say something without it:
    # what a batch costs, who teaches it, what last year's students scored.
    'pricing': ('title', 'subtitle'),
    'video': ('title', 'subtitle', 'media_url'),
    'team': ('title', 'subtitle'),
    'logos': ('title', 'subtitle'),
    'timeline': ('title', 'subtitle'),
    'steps': ('title', 'subtitle'),
    'quote': ('title', 'subtitle'),
    'banner': ('title', 'subtitle', 'cta_label', 'cta_url'),
    'richtext': ('title', 'subtitle', 'body', 'image_url', 'cta_label', 'cta_url'),
    'divider': (),
}

LIST_FIELDS = {
    'stats': 'items',
    'showcase': 'items',
    'gallery': 'images',
    'testimonials': 'items',
    'faq': 'items',
    'schedule': 'items',
    'links': 'items',
    'pricing': 'items',
    'team': 'items',
    'logos': 'items',
    'timeline': 'items',
    'steps': 'items',
}

ITEM_FIELDS = {
    'stats': ('label', 'value', 'icon'),
    'showcase': ('title', 'subtitle', 'image_url', 'link_url', 'badge'),
    'testimonials': ('name', 'role', 'quote', 'avatar_url'),
    'faq': ('q', 'a'),
    'schedule': ('day', 'time', 'title', 'note'),
    'links': ('label', 'url', 'icon'),
    'pricing': ('name', 'price', 'period', 'features', 'badge', 'cta_label', 'cta_url'),
    'team': ('name', 'role', 'avatar_url', 'note'),
    'logos': ('label', 'image_url', 'link_url'),
    'timeline': ('label', 'title', 'note'),
    'steps': ('title', 'note'),
}

# Every field whose value ends up in an href or src. `avatar_url` belongs here
# too: a testimonial's portrait is rendered by both surfaces, so it goes
# through the same scheme allowlist as any other creator-supplied link.
URL_FIELDS = ('cta_url', 'image_url', 'link_url', 'url', 'media_url', 'promo_url',
              'avatar_url')

SOCIAL_KEYS = (
    'website', 'facebook', 'instagram', 'youtube', 'tiktok', 'x', 'linkedin',
    'github', 'telegram', 'viber', 'whatsapp', 'email', 'phone',
)

DEFAULT_BLOCKS = [
    {'type': 'hero', 'title': '', 'subtitle': '', 'cta_label': 'Browse offerings',
     'cta_url': '', 'image_url': ''},
    {'type': 'about', 'title': 'About',
     'body': 'Tell students who you are, what you teach and how you teach it.'},
    {'type': 'courses', 'title': 'Courses and classes',
     'subtitle': 'Paid and free offerings'},
    {'type': 'resources', 'title': 'Resources', 'subtitle': 'Notes, papers and guides'},
    {'type': 'contact', 'title': 'Get in touch', 'body': ''},
]


BLOCK_LABELS = {
    'hero': 'Hero', 'about': 'About', 'stats': 'Numbers', 'courses': 'Courses',
    'resources': 'Resources', 'posts': 'Updates', 'showcase': 'Showcase',
    'gallery': 'Gallery', 'testimonials': 'Testimonials', 'faq': 'FAQ',
    'schedule': 'Schedule', 'contact': 'Contact', 'links': 'Links', 'cta': 'Call to action',
    'documents': 'Documents', 'pricing': 'Pricing', 'video': 'Video', 'team': 'Team',
    'logos': 'Partners', 'timeline': 'Milestones', 'steps': 'How it works',
    'quote': 'Pull quote', 'banner': 'Announcement', 'richtext': 'Text and image',
    'divider': 'Divider',
}

FIELD_LABELS = {
    'title': 'Heading', 'subtitle': 'Subheading', 'body': 'Text',
    'cta_label': 'Button label', 'cta_url': 'Button link', 'image_url': 'Image URL',
    'items': 'Items', 'images': 'Image URLs', 'media_url': 'Video link',
}

ITEM_LABELS = {
    'label': 'Label', 'value': 'Value', 'icon': 'Icon', 'title': 'Title',
    'subtitle': 'Subtitle', 'image_url': 'Image URL', 'link_url': 'Link',
    'badge': 'Badge', 'name': 'Name', 'role': 'Role', 'quote': 'Quote',
    'avatar_url': 'Avatar URL', 'q': 'Question', 'a': 'Answer', 'day': 'Day',
    'time': 'Time', 'note': 'Note', 'url': 'Link', 'price': 'Price',
    'period': 'Per', 'features': 'What is included',
}


#: What each section is *for*, in the creator's words. The pickers show this
#: under the name -- "Gallery" tells you nothing, "Photos of your classroom,
#: students and results" tells you whether you want one.
BLOCK_HINTS = {
    'hero': 'The top of your page: your name, one line about you, one button',
    'about': 'Who you are, what you teach and how you teach it',
    'stats': 'Three or four numbers you want seen first',
    'courses': 'Your paid and free offerings, pulled in automatically',
    'resources': 'Notes and papers you have published to the library',
    'posts': 'Your updates, newest first',
    'showcase': 'Picture cards for anything: results, batches, achievements',
    'gallery': 'Photos of your classroom, students and results',
    'testimonials': 'What your students say, in their words',
    'faq': 'The questions every parent asks before enrolling',
    'schedule': 'Your weekly timetable',
    'contact': 'How to reach you, and your social links',
    'links': 'A tidy list of anything you want to point at',
    'cta': 'One clear ask, on its own, hard to miss',
    'documents': 'Files a visitor can open or download',
    'pricing': 'What a batch costs, side by side',
    'video': 'A YouTube or Vimeo link, played in place',
    'team': 'The people who teach with you',
    'logos': 'Schools, boards and partners you work with',
    'timeline': 'Your milestones, or your students results by year',
    'steps': 'How joining works, in numbered steps',
    'quote': 'One line, set large. Good between two dense sections',
    'banner': 'A thin strip for an admission date or a discount',
    'richtext': 'A paragraph beside a picture. The flexible one',
    'divider': 'Breathing room, and a rule between sections',
}

#: The picker groups sections this way so a creator scans a short list rather
#: than twenty-five chips in a row.
BLOCK_GROUPS = (
    ('Essentials', ('hero', 'about', 'courses', 'resources', 'contact')),
    ('Persuasion', ('stats', 'testimonials', 'pricing', 'faq', 'steps', 'quote')),
    ('Show your work', ('gallery', 'showcase', 'video', 'richtext', 'documents', 'posts')),
    ('Your setup', ('schedule', 'team', 'logos', 'timeline', 'links')),
    ('Accents', ('cta', 'banner', 'divider')),
)

#: Sections that draw their content from elsewhere in NEBians rather than from
#: fields the creator fills in. The editors say so instead of showing an empty
#: item list and letting the creator wonder what they did wrong.
SERVER_FED_BLOCKS = ('courses', 'resources', 'posts', 'documents')

#: Item fields that deserve a textarea rather than a single line.
MULTILINE_ITEM_FIELDS = ('features', 'quote', 'a', 'note')

#: Where a section may be pointed at. `sections` are the anchors a hero or CTA
#: button can jump to without leaving the page.
def block_anchors(blocks):
    """The in-page targets a button may link to, as `#id` fragments."""
    return [{'id': block.get('id', ''), 'type': block.get('type', ''),
             'label': block.get('title') or BLOCK_LABELS.get(block.get('type'), '')}
            for block in blocks or [] if block.get('type') not in ('hero', 'divider')]


def block_schema():
    """The block catalogue the studio editor and the app builder both render.

    One list, read by three renderers. `group` drives the picker's sections,
    `server_fed` tells an editor not to ask for items it does not own, and
    `multiline` decides between an input and a textarea.
    """
    group_of = {block_type: name for name, types in BLOCK_GROUPS for block_type in types}
    schema = []
    for block_type, fields in BLOCK_FIELDS.items():
        list_key = LIST_FIELDS.get(block_type)
        schema.append({
            'type': block_type,
            'label': BLOCK_LABELS.get(block_type, block_type.title()),
            'hint': BLOCK_HINTS.get(block_type, ''),
            'group': group_of.get(block_type, 'Accents'),
            'server_fed': block_type in SERVER_FED_BLOCKS,
            'fields': [{'key': f, 'label': FIELD_LABELS.get(f, f.replace('_', ' ').title()),
                        'multiline': f == 'body', 'url': f in URL_FIELDS}
                       for f in fields],
            'list_key': list_key,
            'item_fields': [{'key': f, 'label': ITEM_LABELS.get(f, f.replace('_', ' ').title()),
                             'url': f in URL_FIELDS,
                             'multiline': f in MULTILINE_ITEM_FIELDS}
                            for f in ITEM_FIELDS.get(block_type, ())],
            'item_hint': 'One image URL per line' if block_type == 'gallery' else '',
        })
    return schema


def editor_schema():
    """Everything an editor needs in one payload: sections, groups and theme.

    The app fetches this once and builds its whole builder from it, which is how
    a section added on the server appears in a shipped app without an update.
    """
    return {
        'blocks': block_schema(),
        'groups': [{'label': label, 'types': list(types)} for label, types in BLOCK_GROUPS],
        'theme': theme_vocabulary(),
        'layouts': [{'id': layout, 'label': layout.title()} for layout in LAYOUTS],
        'max_blocks': MAX_BLOCKS,
        'max_items': MAX_LIST_ITEMS,
    }
