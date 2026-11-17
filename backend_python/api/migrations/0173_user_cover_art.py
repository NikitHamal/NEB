"""A profile can pick its cover from the M3X art library. Adds one nullable-free CharField; no data is touched."""
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('api', '0172_reclassify_utm_sources')]
    operations = [
        migrations.AddField(
            model_name='user',
            name='cover_art',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
    ]
