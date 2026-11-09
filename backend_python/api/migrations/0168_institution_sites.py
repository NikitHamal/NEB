"""Official websites for well known institutions the catalogue had without one (verified live), and one bad Wikidata link removed."""
import json
import re
import time
from pathlib import Path

from django.db import migrations

from api.models_institutions import search_key

SITES = Path(__file__).resolve().parent.parent / 'data' / 'institution_sites.json'


def norm(value):
    return re.sub(r'[^a-z0-9 ]', '', (value or '').lower().replace("'", '')).strip()


def apply(apps, schema_editor):
    Institution = apps.get_model('api', 'Institution')
    Institution.objects.filter(website__contains='uprowadzona').update(website='')
    if not SITES.exists():
        return
    stamp = int(time.time() * 1000)
    for entry in json.loads(SITES.read_text(encoding='utf-8')):
        wanted = norm(entry['name'])
        pool = list(Institution.objects.filter(district=entry['district']).only('id', 'name', 'website'))
        hit = next((r for r in pool if norm(r.name) == wanted), None) or next(
            (r for r in sorted(pool, key=lambda r: len(r.name)) if norm(r.name).startswith(wanted)), None)
        if hit:
            if not hit.website:
                Institution.objects.filter(pk=hit.pk).update(website=entry['website'])
            continue
        base = re.sub(r'[^a-z0-9]+', '-', entry['name'].lower()).strip('-')[:70]
        slug, n = base, 2
        while Institution.objects.filter(slug=slug).exists():
            slug = '%s-%d' % (base, n)
            n += 1
        province = next((p for (d, p) in Institution.objects.filter(district=entry['district'])
                         .exclude(province='').values_list('district', 'province')[:1]), '')
        Institution.objects.create(
            slug=slug, name=entry['name'], kind=entry['kind'], district=entry['district'], province=province,
            website=entry['website'], source='curated', created_at=stamp,
            search_text=search_key(entry['name'], '', entry['district'], ''))


class Migration(migrations.Migration):
    dependencies = [('api', '0167_merge_0165_normalize_levels_0166_seed_institutions')]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
