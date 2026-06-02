from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_rename_api_bookmark_user_type_idx_bookmarks_user_id_76f91f_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NebyTask',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('done', 'Done'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('trigger', models.CharField(choices=[('post_mention', 'Post Mention'), ('reply_mention', 'Reply Mention')], max_length=20)),
                ('post_id', models.CharField(max_length=36)),
                ('reply_id', models.CharField(blank=True, max_length=36, null=True)),
                ('created_at', models.BigIntegerField()),
                ('started_at', models.BigIntegerField(default=0)),
                ('finished_at', models.BigIntegerField(default=0)),
                ('attempts', models.PositiveSmallIntegerField(default=0)),
                ('error_message', models.TextField(blank=True, default='')),
            ],
            options={
                'db_table': 'neby_tasks',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='nebytask',
            index=models.Index(fields=['status', 'created_at'], name='neby_tasks_status_created_idx'),
        ),
    ]