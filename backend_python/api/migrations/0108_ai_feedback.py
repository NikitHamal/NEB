import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0107_postmedia_thumbnail_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='AiFeedback',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False)),
                ('user_id', models.CharField(db_index=True, default='', max_length=255)),
                ('surface', models.CharField(default='neby', max_length=30)),
                ('vote', models.SmallIntegerField(default=0)),
                ('provider', models.CharField(blank=True, default='', max_length=60)),
                ('model_name', models.CharField(blank=True, default='', max_length=120)),
                ('query', models.TextField(blank=True, default='')),
                ('created_at', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'ai_feedback',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['surface', '-created_at'], name='ai_fb_surf_created_idx'),
                ],
            },
        ),
    ]