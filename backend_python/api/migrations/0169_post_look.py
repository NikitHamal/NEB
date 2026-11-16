"""Dynamic posts: the look (page colour, cover, icon, paper, type) of a post."""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0168_institution_sites'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='look',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
    ]
