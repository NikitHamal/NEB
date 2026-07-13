from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_add_institution_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('platform', models.CharField(choices=[
                    ('instagram', 'Instagram'),
                    ('facebook', 'Facebook'),
                    ('twitter', 'X (Twitter)'),
                    ('youtube', 'YouTube'),
                    ('tiktok', 'TikTok'),
                    ('linkedin', 'LinkedIn'),
                    ('github', 'GitHub'),
                    ('telegram', 'Telegram'),
                    ('whatsapp', 'WhatsApp'),
                    ('discord', 'Discord'),
                    ('snapchat', 'Snapchat'),
                    ('pinterest', 'Pinterest'),
                    ('reddit', 'Reddit'),
                    ('website', 'Website'),
                ], default='website', max_length=20)),
                ('url', models.TextField()),
                ('label', models.CharField(blank=True, default='', max_length=100)),
                ('sort_order', models.PositiveSmallIntegerField(default=0)),
                ('is_visible', models.BooleanField(default=True)),
                ('created_at', models.BigIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='social_links', to='api.user')),
            ],
            options={
                'db_table': 'social_links',
                'ordering': ['sort_order', 'created_at'],
                'indexes': [
                    models.Index(fields=['user_id', 'sort_order'], name='api_social_user_sort_idx'),
                ],
            },
        ),
    ]
