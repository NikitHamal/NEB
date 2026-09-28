"""Creator marketplace — the block catalogue every surface renders from.

A storefront is data, not markup: this module is the single list of block
types, the fields each one carries, the labels the editors show and the style
vocabulary a page may use. The Django templates, the studio editor and the
Android builder all read `block_schema()`, so adding a section here is what
makes it appear on both platforms.
"""
import re

from .models import User


ELIGIBLE_ROLES = (User.ROLE_TEACHER, User.ROLE_INSTITUTION)

MAX_BLOCKS = 24
MAX_LIST_ITEMS = 24
ACCENT_RE = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')

LAYOUTS = ('editorial', 'spotlight', 'grid', 'classic')
HERO_STYLES = ('plain', 'art', 'cover')
RADII = ('soft', 'round', 'sharp')
DENSITIES = ('comfortable', 'compact')

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
}

LIST_FIELDS = {
    'stats': 'items',
    'showcase': 'items',
    'gallery': 'images',
    'testimonials': 'items',
    'faq': 'items',
    'schedule': 'items',
    'links': 'items',
}

ITEM_FIELDS = {
    'stats': ('label', 'value', 'icon'),
    'showcase': ('title', 'subtitle', 'image_url', 'link_url', 'badge'),
    'testimonials': ('name', 'role', 'quote', 'avatar_url'),
    'faq': ('q', 'a'),
    'schedule': ('day', 'time', 'title', 'note'),
    'links': ('label', 'url', 'icon'),
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
    'documents': 'Documents',
}

FIELD_LABELS = {
    'title': 'Heading', 'subtitle': 'Subheading', 'body': 'Text',
    'cta_label': 'Button label', 'cta_url': 'Button link', 'image_url': 'Image URL',
    'items': 'Items', 'images': 'Image URLs',
}

ITEM_LABELS = {
    'label': 'Label', 'value': 'Value', 'icon': 'Icon', 'title': 'Title',
    'subtitle': 'Subtitle', 'image_url': 'Image URL', 'link_url': 'Link',
    'badge': 'Badge', 'name': 'Name', 'role': 'Role', 'quote': 'Quote',
    'avatar_url': 'Avatar URL', 'q': 'Question', 'a': 'Answer', 'day': 'Day',
    'time': 'Time', 'note': 'Note', 'url': 'Link',
}


def block_schema():
    """The block catalogue the studio editor and the app builder both render."""
    schema = []
    for block_type, fields in BLOCK_FIELDS.items():
        list_key = LIST_FIELDS.get(block_type)
        schema.append({
            'type': block_type,
            'label': BLOCK_LABELS.get(block_type, block_type.title()),
            'fields': [{'key': f, 'label': FIELD_LABELS.get(f, f.replace('_', ' ').title()),
                        'multiline': f == 'body', 'url': f in URL_FIELDS}
                       for f in fields],
            'list_key': list_key,
            'item_fields': [{'key': f, 'label': ITEM_LABELS.get(f, f.replace('_', ' ').title()),
                             'url': f in URL_FIELDS}
                            for f in ITEM_FIELDS.get(block_type, ())],
            'item_hint': 'One image URL per line' if block_type == 'gallery' else '',
        })
    return schema
