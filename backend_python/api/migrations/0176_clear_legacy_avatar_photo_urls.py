"""Clear any legacy 2D /avatar/ URLs stored in User.photo_url so only real photos or initial letters remain."""
from django.db import migrations


def clear_legacy_avatar_urls(apps, schema_editor):
    User = apps.get_model('api', 'User')
    User.objects.filter(photo_url__startswith='/avatar/').update(photo_url='')
    User.objects.filter(photo_url__contains='/avatar/').update(photo_url='')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0175_remove_marketplace_and_avatar_fields'),
    ]

    operations = [
        migrations.RunPython(clear_legacy_avatar_urls, migrations.RunPython.noop),
    ]
