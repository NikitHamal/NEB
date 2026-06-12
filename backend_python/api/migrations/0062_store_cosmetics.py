from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_generation_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='points_spent',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='equipped_theme',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AddField(
            model_name='user',
            name='equipped_banner',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AddField(
            model_name='user',
            name='equipped_border',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AddField(
            model_name='user',
            name='equipped_badge',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.CreateModel(
            name='UserCosmetic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(db_index=True, max_length=255)),
                ('item_key', models.CharField(max_length=40)),
                ('kind', models.CharField(max_length=12)),
                ('price_paid', models.PositiveIntegerField(default=0)),
                ('acquired_at', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'user_cosmetics',
                'unique_together': {('user_id', 'item_key')},
                'indexes': [models.Index(fields=['user_id', 'kind'], name='user_cosmet_user_id_208b13_idx')],
            },
        ),
        migrations.CreateModel(
            name='PointsLedger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(db_index=True, max_length=255)),
                ('delta', models.IntegerField(default=0)),
                ('reason', models.CharField(max_length=40)),
                ('item_key', models.CharField(blank=True, default='', max_length=40)),
                ('balance_after', models.PositiveIntegerField(default=0)),
                ('created_at', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'points_ledger',
            },
        ),
    ]
