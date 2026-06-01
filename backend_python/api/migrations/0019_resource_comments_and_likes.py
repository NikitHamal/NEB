from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_add_bot_config_and_is_bot'),
    ]

    operations = [
        # Add new fields to Resource
        migrations.AddField(
            model_name='resource',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='resource',
            name='comment_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='resource',
            name='author_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddIndex(
            model_name='resource',
            index=models.Index(fields=['-like_count'], name='api_resourc_like_co_idx'),
        ),
        # Source tracking fields on Resource
        migrations.AddField(
            model_name='resource',
            name='source_type',
            field=models.CharField(
                choices=[('admin', 'Added by Admin'), ('user', 'User Upload'),
                         ('anonymous', 'Anonymous Upload'), ('external', 'External Source')],
                default='admin', max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='resource',
            name='uploaded_by',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='uploaded_resources',
                to='api.user',
            ),
        ),
        migrations.AddField(
            model_name='resource',
            name='source_url',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='resource',
            name='source_label',
            field=models.CharField(blank=True, default='', max_length=200),
        ),

        # ResourceComment model
        migrations.CreateModel(
            name='ResourceComment',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('reply_count', models.PositiveIntegerField(default=0)),
                ('is_edited', models.BooleanField(default=False)),
                ('edited_at', models.BigIntegerField(default=0)),
                ('created_at', models.BigIntegerField()),
                ('resource', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comments',
                    to='api.resource',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='resource_comments',
                    to='api.user',
                )),
                ('parent_comment', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='children',
                    to='api.resourcecomment',
                )),
            ],
            options={
                'db_table': 'resource_comments',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='resourcecomment',
            index=models.Index(fields=['resource_id', 'created_at'], name='resource_comment_res_idx'),
        ),
        migrations.AddIndex(
            model_name='resourcecomment',
            index=models.Index(fields=['parent_comment_id', 'created_at'], name='resource_comment_parent_idx'),
        ),

        # ResourceLike model
        migrations.CreateModel(
            name='ResourceLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='likes',
                    to='api.resource',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='resource_likes',
                    to='api.user',
                )),
            ],
            options={
                'db_table': 'resource_likes',
                'unique_together': {('resource', 'user')},
            },
        ),

        # ResourceCommentLike model
        migrations.CreateModel(
            name='ResourceCommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='likes',
                    to='api.resourcecomment',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='resource_comment_likes',
                    to='api.user',
                )),
            ],
            options={
                'db_table': 'resource_comment_likes',
                'unique_together': {('comment', 'user')},
            },
        ),
    ]
