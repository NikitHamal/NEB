import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0162_creator_course_delivery_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sociallinkclick',
            name='clicker_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
