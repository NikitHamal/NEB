from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0074_social_links'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLinkClick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clicker_id', models.BigIntegerField(blank=True, null=True)),
                ('platform', models.CharField(db_index=True, max_length=20)),
                ('url', models.TextField()),
                ('created_at', models.BigIntegerField(default=0)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clicks', to='api.sociallink')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_clicks', to='api.user')),
            ],
            options={
                'db_table': 'social_link_clicks',
                'indexes': [
                    models.Index(fields=['user_id', 'created_at'], name='slc_user_created_idx'),
                    models.Index(fields=['platform'], name='slc_platform_idx'),
                ],
            },
        ),
    ]
