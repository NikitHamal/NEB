from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_add_institution_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyspacenote',
            name='board_content',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='studyspacenote',
            name='board_version',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
