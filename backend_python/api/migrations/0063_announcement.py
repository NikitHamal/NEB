from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0062_accountdeletionrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(db_index=True, max_length=280, unique=True)),
                ('summary', models.CharField(blank=True, default='', max_length=500)),
                ('content', models.TextField(blank=True, default='')),
                ('category', models.CharField(
                    choices=[
                        ('exam_results', 'Exam Results'),
                        ('notice', 'Notice'),
                        ('event', 'Event'),
                        ('update', 'Update'),
                        ('alert', 'Alert'),
                        ('general', 'General'),
                    ],
                    db_index=True, default='general', max_length=20,
                )),
                ('status', models.CharField(
                    choices=[
                        ('draft', 'Draft'),
                        ('published', 'Published'),
                        ('archived', 'Archived'),
                    ],
                    db_index=True, default='draft', max_length=20,
                )),
                ('is_pinned', models.BooleanField(db_index=True, default=False)),
                ('cover_image_url', models.TextField(blank=True, default='')),
                ('external_url', models.TextField(blank=True, default='')),
                ('tags', models.CharField(blank=True, default='', max_length=500)),
                ('published_at', models.BigIntegerField(db_index=True, default=0)),
                ('created_at', models.BigIntegerField(default=0)),
                ('updated_at', models.BigIntegerField(default=0)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='announcements',
                    to='api.user',
                )),
            ],
            options={
                'db_table': 'announcements',
                'ordering': ['-is_pinned', '-published_at', '-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='announcement',
            index=models.Index(fields=['status', '-published_at'], name='ann_stat_pub_idx'),
        ),
        migrations.AddIndex(
            model_name='announcement',
            index=models.Index(fields=['category', 'status'], name='ann_cat_stat_idx'),
        ),
        migrations.AddIndex(
            model_name='announcement',
            index=models.Index(fields=['-is_pinned', '-published_at'], name='ann_pin_pub_idx'),
        ),
    ]