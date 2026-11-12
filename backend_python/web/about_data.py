"""Everything the /about/ page says about the people and the company, in one place.

Edit this file to change the team. Nothing else needs to move:

  * ``TEAM`` order is the order on the page, grouped by ``group`` (lead, dev, crew).
  * A photo is picked up automatically: drop ``<slug>.jpg`` (or .png / .webp) into
    ``web/static/web/img/team/``. Square, at least 600 px. Until then the card shows the
    person's initial inside the same expressive shape, so the layout never changes.
  * ``shape`` is one of the ``shp-*`` classes in m3x/core.css; ``tone`` one of azure/sky/aqua/peri.
  * Roles are only shown where we know them. Add ``role`` to a ``crew`` entry and it appears.

``jsonld()`` turns the same data into schema.org markup for search engines, so the visible page
and the structured data cannot disagree.
"""
import json
from pathlib import Path

from django.templatetags.static import static

SITE = 'https://nebians.consica.com.np'
COMPANY = 'Consica Labs'
PHOTO_DIR = Path(__file__).resolve().parent / 'static' / 'web' / 'img' / 'team'
PHOTO_EXTS = ('jpg', 'jpeg', 'png', 'webp')

TEAM = [
    {'slug': 'nikit-hamal', 'name': 'Nikit Hamal', 'role': 'Lead developer', 'group': 'lead', 'shape': 'cookie', 'tone': 'azure'},
    {'slug': 'prashant-chataut', 'name': 'Prashant Chataut', 'role': 'Developer', 'group': 'dev', 'shape': 'sunny', 'tone': 'sky'},
    {'slug': 'bikram-adhikari', 'name': 'Bikram Adhikari', 'role': 'Developer', 'group': 'dev', 'shape': 'flower', 'tone': 'aqua'},
    {'slug': 'utsab-kafle', 'name': 'Utsab Kafle', 'role': '', 'group': 'crew', 'shape': 'clover', 'tone': 'peri'},
    {'slug': 'laxmi-nepal', 'name': 'Laxmi Nepal', 'role': '', 'group': 'crew', 'shape': 'gem', 'tone': 'sky'},
    {'slug': 'manisha-kafle', 'name': 'Manisha Kafle', 'role': '', 'group': 'crew', 'shape': 'burst', 'tone': 'aqua'},
    {'slug': 'gaurav-rajbanshi', 'name': 'Gaurav Rajbanshi', 'role': '', 'group': 'crew', 'shape': 'pebble', 'tone': 'azure'},
]

# What NEBians is, in the four things a student actually does. `href` is a url name or a path.
PILLARS = [
    {'key': 'library', 'tone': 'azure', 'shape': 'cookie', 'title': 'The library',
     'text': 'Notes, past papers and solved study books for every class and level.',
     'href': '/app/library/', 'icon': 'M7 3h8l4 4v14H7zM15 3v4h4M10 12h6M10 16h6'},
    {'key': 'forum', 'tone': 'sky', 'shape': 'sunny', 'title': 'The forum',
     'text': 'Ask a question and get answers that are marked correct, helpful or wrong.',
     'href': '/app/', 'icon': 'M4 5h16v11H9l-5 4z'},
    {'key': 'neby', 'tone': 'aqua', 'shape': 'flower', 'title': 'Ask Neby',
     'text': 'A study helper that opens beside the page you are reading.',
     'href': '/app/tools/', 'icon': 'M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z'},
    {'key': 'app', 'tone': 'peri', 'shape': 'clover', 'title': 'The app',
     'text': 'The same library on Android, built for one-handed reading.',
     'href': '/#app', 'icon': 'M8 3h8a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zM11 18h2'},
]

STEPS = [
    {'n': '1', 'title': 'Find', 'text': 'Pick a level and a subject.'},
    {'n': '2', 'title': 'Read', 'text': 'Open notes, papers and books in the reader.'},
    {'n': '3', 'title': 'Ask', 'text': 'Post what you are stuck on.'},
    {'n': '4', 'title': 'Share', 'text': 'Upload what helped you, so the next student finds it.'},
]

PROMISES = [
    {'title': 'Free to read', 'text': 'No paywall in front of the library or the forum.',
     'icon': 'M5 12l5 5 9-10'},
    {'title': 'Checked before it goes public', 'text': 'Moderators review every upload.',
     'icon': 'M12 3l7 3v5c0 5-3 8.5-7 10-4-1.5-7-5-7-10V6z'},
    {'title': 'Every level', 'text': 'School to Master\'s, entrance included.',
     'icon': 'M3 9l9-5 9 5-9 5zM7 12v4c0 1 2.2 2.5 5 2.5s5-1.5 5-2.5v-4'},
    {'title': 'Made for phones', 'text': 'Fast on a small screen and a slow connection.',
     'icon': 'M8 3h8a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zM11 18h2'},
]


def _photo(slug):
    for ext in PHOTO_EXTS:
        if (PHOTO_DIR / f'{slug}.{ext}').is_file():
            return static(f'web/img/team/{slug}.{ext}')
    return ''


def team():
    """TEAM with photo urls and initials resolved, split by group."""
    people = []
    for person in TEAM:
        people.append({**person, 'photo': _photo(person['slug']), 'initial': person['name'][:1]})
    return {group: [p for p in people if p['group'] == group] for group in ('lead', 'dev', 'crew')}


def jsonld(seo):
    """schema.org @graph for the About page: AboutPage, the NEBians organisation and its team."""
    org_id = f'{SITE}/#organization'
    people = []
    for person in TEAM:
        node = {'@type': 'Person', '@id': f"{SITE}/about/#{person['slug']}", 'name': person['name'],
                'worksFor': {'@id': org_id}}
        if person['role']:
            node['jobTitle'] = person['role']
        photo = _photo(person['slug'])
        if photo:
            node['image'] = SITE + photo
        people.append(node)
    graph = [
        {'@type': 'AboutPage', '@id': f'{SITE}/about/#page', 'url': f'{SITE}/about/', 'name': seo['title'],
         'description': seo['description'], 'inLanguage': 'en',
         'isPartOf': {'@type': 'WebSite', 'name': 'NEBians', 'url': f'{SITE}/'},
         'about': {'@id': org_id}, 'mainEntity': {'@id': org_id},
         'breadcrumb': {'@id': f'{SITE}/about/#crumbs'}},
        {'@type': 'Organization', '@id': org_id, 'name': 'NEBians', 'url': f'{SITE}/',
         'logo': {'@type': 'ImageObject', 'url': f'{SITE}/static/web/img/n-logo-512.png', 'width': 512, 'height': 512},
         'description': 'Free notes, past papers and solved study books for every class and level in Nepal, and a forum where students answer each other.',
         'areaServed': {'@type': 'Country', 'name': 'Nepal'},
         'parentOrganization': {'@type': 'Organization', 'name': COMPANY},
         'sameAs': ['https://play.google.com/store/apps/details?id=com.neb.ians'],
         'member': [{'@id': p['@id']} for p in people],
         'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer support',
                          'email': 'support@nebians.consica.com.np', 'availableLanguage': ['English', 'Nepali']}},
        *people,
        {'@type': 'BreadcrumbList', '@id': f'{SITE}/about/#crumbs', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'NEBians', 'item': f'{SITE}/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'About', 'item': f'{SITE}/about/'}]},
    ]
    # `<` is escaped so no field can ever close the <script> element.
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, separators=(',', ':')).replace('<', '\\u003c')
