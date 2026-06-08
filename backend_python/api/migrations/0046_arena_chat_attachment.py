from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_add_poll_type_mcq'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArenaChatAttachment',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('file_type', models.CharField(max_length=20)),
                ('file_name', models.CharField(max_length=500)),
                ('file_size', models.PositiveIntegerField(default=0)),
                ('mime_type', models.CharField(blank=True, default='', max_length=200)),
                ('qwen_file_id', models.CharField(blank=True, default='', max_length=200)),
                ('qwen_file_url', models.TextField(blank=True, default='')),
                ('show_type', models.CharField(blank=True, default='', max_length=20)),
                ('file_class', models.CharField(blank=True, default='', max_length=20)),
                ('created_at', models.BigIntegerField()),
                ('message', models.ForeignKey(
                    on_delete=models.CASCADE,
                    related_name='attachments',
                    to='api.arenachatmessage',
                    db_index=True,
                )),
            ],
            options={
                'db_table': 'arena_chat_attachments',
            },
        ),
    ]