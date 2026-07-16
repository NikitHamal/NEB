from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_herobackground'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostView',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True)),
                ('viewed_at', models.BigIntegerField()),
                ('post', models.ForeignKey(on_delete=models.CASCADE, related_name='views', to='api.post', db_constraint=False)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='post_views', to='api.user', db_constraint=False)),
            ],
            options={
                'db_table': 'post_views',
                'unique_together': {('post', 'user', 'viewed_at')},
                'indexes': [
                    models.Index(fields=['post_id', '-viewed_at'], name='pv_post_viewed_idx'),
                    models.Index(fields=['user_id'], name='pv_user_idx'),
                ],
            },
        ),
    ]
