from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0113_avatar_eye_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='botconfig',
            name='fallback_chain',
            field=models.TextField(
                blank=True, default='[]',
                help_text='JSON list of fallback provider entries tried in order when the primary provider fails. '
                          'Each entry: {"provider": slug, "model": "...", "api_url": "...", "api_key": "..."}.',
            ),
        ),
    ]
