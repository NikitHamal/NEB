"""Fold every stored level spelling onto the education catalog's one value.

Uploads from the app and older web forms wrote 'Class 11' where the catalog says '11',
'Bachelor' where it says 'Bachelors', and so on, so filtered lists missed them. New writes
are canonicalised at the edge; this fixes the rows that already exist.
"""
from django.db import migrations


TARGETS = (
    ('Resource', 'grade_level'),
    ('ResourceRequest', 'grade_level'),
    ('SyllabusContent', 'grade_level'),
    ('User', 'class_level'),
)


def normalize(apps, schema_editor):
    from api.education_catalog import canonical_level
    for model_name, field in TARGETS:
        model = apps.get_model('api', model_name)
        seen = model.objects.values_list(field, flat=True).distinct()
        for value in seen:
            if not value:
                continue
            canon = canonical_level(value)
            if canon != value:
                model.objects.filter(**{field: value}).update(**{field: canon})


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0164_push_campaigns_resource_reach'),
    ]

    operations = [
        migrations.RunPython(normalize, migrations.RunPython.noop),
    ]