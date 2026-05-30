from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_security_hardening'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banner_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('target_type', models.CharField(max_length=10)),
                ('target_id', models.CharField(max_length=36)),
                ('reason', models.CharField(choices=[('spam', 'Spam'), ('abuse', 'Abuse / Harassment'), ('inappropriate', 'Inappropriate Content'), ('misinformation', 'Misinformation'), ('other', 'Other')], default='other', max_length=20)),
                ('description', models.TextField(blank=True, default='')),
                ('status', models.CharField(choices=[('open', 'Open'), ('reviewing', 'Reviewing'), ('resolved', 'Resolved'), ('dismissed', 'Dismissed')], default='open', max_length=10)),
                ('created_at', models.BigIntegerField()),
                ('resolved_at', models.BigIntegerField(default=0)),
                ('reporter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports_made', to='api.user')),
                ('resolved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports_resolved', to='api.user')),
            ],
            options={
                'db_table': 'reports',
                'ordering': ['-created_at'],
            },
        ),
    ]