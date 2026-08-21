from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0115_avatar_use_pp'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to='content_images/')),
                ('thumb', models.FileField(max_length=255, upload_to='content_images/')),
                ('width', models.PositiveIntegerField(default=0)),
                ('height', models.PositiveIntegerField(default=0)),
                ('size', models.PositiveIntegerField(default=0)),
                ('sha256', models.CharField(db_index=True, max_length=64)),
                ('is_animated', models.BooleanField(default=False)),
                ('used', models.BooleanField(default=False)),
                ('created_at', models.BigIntegerField(default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='content_images', to='api.user')),
            ],
            options={
                'db_table': 'content_images',
            },
        ),
        migrations.AddIndex(
            model_name='contentimage',
            index=models.Index(fields=['used', 'created_at'], name='content_ima_used_891f8f_idx'),
        ),
    ]
