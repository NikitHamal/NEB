"""Seed the Dawn Himalayan vector hero background as an admin-selectable option."""
from django.db import migrations


def seed(apps, schema_editor):
    HeroBackground = apps.get_model('api', 'HeroBackground')
    if HeroBackground.objects.filter(filename='dawn_himalayan_hero_background.svg').exists():
        return
    last = HeroBackground.objects.order_by('-sort_order').first()
    HeroBackground.objects.create(
        name='Dawn Himalayan',
        filename='dawn_himalayan_hero_background.svg',
        is_active=False,
        sort_order=(last.sort_order + 1) if last else 1,
        created_at=0,
    )


def unseed(apps, schema_editor):
    HeroBackground = apps.get_model('api', 'HeroBackground')
    HeroBackground.objects.filter(filename='dawn_himalayan_hero_background.svg').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0127_canvas_objects_and_collab'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
