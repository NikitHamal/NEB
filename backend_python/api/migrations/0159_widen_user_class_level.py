from django.db import migrations, models

TRUNCATED_CLASS = 'Class 10 /'
FULL_CLASS = 'Class 10 / SEE'


def repair_truncated_class(apps, schema_editor):
    User = apps.get_model('api', 'User')
    User.objects.filter(class_level=TRUNCATED_CLASS).update(class_level=FULL_CLASS)


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0158_news_autopilot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='class_level',
            field=models.CharField(blank=True, db_column='class', max_length=20, null=True),
        ),
        migrations.RunPython(repair_truncated_class, migrations.RunPython.noop),
    ]
