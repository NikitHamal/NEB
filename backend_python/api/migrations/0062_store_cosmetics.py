import django.db.models.deletion
from django.db import migrations, models
from django.db.models import F


def backfill_points_balance(apps, schema_editor):
    User = apps.get_model('api', 'User')
    User.objects.update(points_balance=F('contribution_score'))


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_generation_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='points_balance',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='equipped_theme',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AddField(
            model_name='user',
            name='equipped_banner',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AddField(
            model_name='user',
            name='equipped_border',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AddField(
            model_name='user',
            name='equipped_badge',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.CreateModel(
            name='UserCosmetic',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('item_id', models.CharField(max_length=64)),
                ('item_type', models.CharField(max_length=10)),
                ('price_paid', models.PositiveIntegerField(default=0)),
                ('acquired_at', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cosmetics', to='api.user')),
            ],
            options={
                'db_table': 'user_cosmetics',
                'ordering': ['-acquired_at'],
                'unique_together': {('user', 'item_id')},
                'indexes': [models.Index(fields=['user_id', 'item_type'], name='user_cosmet_user_id_8b51f2_idx')],
            },
        ),
        migrations.RunPython(backfill_points_balance, migrations.RunPython.noop),
    ]
