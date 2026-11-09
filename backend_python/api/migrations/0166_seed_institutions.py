import gzip
import json
import re
import time

from django.db import migrations

from api.institutions import CATALOG_PATH
from api.models_institutions import search_key


def seed(apps, schema_editor):
    Institution = apps.get_model('api', 'Institution')
    User = apps.get_model('api', 'User')
    stamp = int(time.time() * 1000)
    if CATALOG_PATH.exists() and not Institution.objects.exists():
        with gzip.open(CATALOG_PATH, 'rt', encoding='utf-8') as fh:
            data = json.load(fh)
        cols = data['cols']
        rows = []
        for row in data['rows']:
            rec = dict(zip(cols, row))
            rows.append(Institution(
                slug=rec['slug'], name=rec['name'], name_ne=rec['name_ne'], kind=rec['kind'],
                district=rec['district'], province=rec['province'], place=rec['place'], website=rec['website'],
                phone=rec['phone'], lat=rec['lat'], lon=rec['lon'], est=rec['est'], source=rec['source'],
                created_at=stamp, search_text=search_key(rec['name'], rec['name_ne'], rec['district'], rec['place']),
            ))
        Institution.objects.bulk_create(rows, batch_size=2000, ignore_conflicts=True)

    for user in User.objects.filter(role='institution'):
        name = (user.school or user.display_name or user.username or '').strip()
        if not name:
            continue
        base = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:70] or user.username
        slug, n = base, 2
        while Institution.objects.filter(slug=slug).exists():
            slug = '%s-%d' % (base, n)
            n += 1
        kind = {'school': 'school', 'college': 'college'}.get(user.institution_type or '', 'institute')
        inst = Institution.objects.create(
            slug=slug, name=name, kind=kind, district=user.district or '', source='account', claimed_by=user,
            verified=bool(user.institution_verified), verified_at=stamp if user.institution_verified else 0,
            created_at=stamp, search_text=search_key(name, user.district or ''))
        User.objects.filter(school_username=user.username).exclude(pk=user.pk).update(
            school_slug=inst.slug, school=inst.name)


class Migration(migrations.Migration):
    dependencies = [('api', '0165_institutions_catalog')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
