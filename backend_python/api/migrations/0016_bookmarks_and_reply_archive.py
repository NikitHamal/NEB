from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_rename_api_edithistory_target_idx_edit_histor_target__ea3ea5_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('target_type', models.CharField(choices=[('post', 'Post'), ('reply', 'Reply'), ('resource', 'Resource')], max_length=10)),
                ('target_id', models.CharField(max_length=36)),
                ('created_at', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='api.user')),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'bookmarks',
                'unique_together': {('user', 'target_type', 'target_id')},
            },
        ),
        migrations.AddField(
            model_name='reply',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddIndex(
            model_name='bookmark',
            index=models.Index(fields=['user_id', 'target_type'], name='api_bookmark_user_type_idx'),
        ),
        migrations.AddIndex(
            model_name='bookmark',
            index=models.Index(fields=['target_type', 'target_id'], name='api_bookmark_target_idx'),
        ),
    ]