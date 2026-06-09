from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_studyspace_studyspaceflashcard_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='studyspace',
                    name='study_level',
                    field=models.CharField(blank=True, default='', max_length=80),
                ),
                migrations.AddField(
                    model_name='studyspace',
                    name='subject',
                    field=models.CharField(blank=True, default='', max_length=120),
                ),
                migrations.AddField(
                    model_name='studyspace',
                    name='exam',
                    field=models.CharField(blank=True, default='', max_length=120),
                ),
                migrations.AddField(
                    model_name='studyspace',
                    name='generate_min_role',
                    field=models.CharField(default='moderator', max_length=20),
                ),
                migrations.AddField(
                    model_name='studyspace',
                    name='upload_min_role',
                    field=models.CharField(default='member', max_length=20),
                ),
                migrations.AddField(
                    model_name='studyspace',
                    name='invite_min_role',
                    field=models.CharField(default='admin', max_length=20),
                ),
                migrations.AddField(
                    model_name='studyspace',
                    name='moderate_min_role',
                    field=models.CharField(default='moderator', max_length=20),
                ),
                migrations.AddField(
                    model_name='studyspace',
                    name='publish_min_role',
                    field=models.CharField(default='owner', max_length=20),
                ),
            ],
            database_operations=[],
        )
    ]