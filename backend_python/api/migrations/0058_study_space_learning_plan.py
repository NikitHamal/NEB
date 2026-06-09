from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_studyspace_metadata_fields_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyspace',
            name='learning_plan',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='studyspace',
            name='learning_plan_days',
            field=models.IntegerField(default=0),
        ),
    ]
