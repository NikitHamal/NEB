from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0069_improve_resource_seo_metadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageView',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False)),
                ('path', models.TextField()),
                ('full_url', models.TextField(blank=True, default='')),
                ('referrer', models.TextField(blank=True, default='')),
                ('referrer_domain', models.CharField(blank=True, default='', max_length=255)),
                ('referrer_type', models.CharField(blank=True, default='', max_length=20)),
                ('utm_source', models.CharField(blank=True, default='', max_length=255)),
                ('utm_medium', models.CharField(blank=True, default='', max_length=255)),
                ('utm_campaign', models.CharField(blank=True, default='', max_length=255)),
                ('user_agent', models.TextField(blank=True, default='')),
                ('source', models.CharField(default='web', max_length=10)),
                ('platform', models.CharField(blank=True, default='', max_length=30)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('session_key', models.CharField(blank=True, default='', max_length=40)),
                ('user_id', models.BigIntegerField(blank=True, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=100)),
                ('city', models.CharField(blank=True, default='', max_length=100)),
                ('created_at', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'page_views',
                'indexes': [
                    models.Index(fields=['created_at'], name='pv_created_at_idx'),
                    models.Index(fields=['referrer_type'], name='pv_referrer_type_idx'),
                    models.Index(fields=['source'], name='pv_source_idx'),
                    models.Index(fields=['user_id'], name='pv_user_id_idx'),
                ],
            },
        ),
        migrations.CreateModel(
            name='DailyStat',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False)),
                ('date', models.DateField(unique=True)),
                ('total_visits', models.PositiveIntegerField(default=0)),
                ('unique_visitors', models.PositiveIntegerField(default=0)),
                ('new_users', models.PositiveIntegerField(default=0)),
                ('web_visits', models.PositiveIntegerField(default=0)),
                ('app_visits', models.PositiveIntegerField(default=0)),
                ('direct_visits', models.PositiveIntegerField(default=0)),
                ('search_visits', models.PositiveIntegerField(default=0)),
                ('social_visits', models.PositiveIntegerField(default=0)),
                ('referral_visits', models.PositiveIntegerField(default=0)),
                ('internal_visits', models.PositiveIntegerField(default=0)),
                ('new_posts', models.PositiveIntegerField(default=0)),
                ('new_resources', models.PositiveIntegerField(default=0)),
                ('new_replies', models.PositiveIntegerField(default=0)),
                ('created_at', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'daily_stats',
                'ordering': ['-date'],
            },
        ),
    ]
