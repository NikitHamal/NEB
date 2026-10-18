from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0146_site_themes_replace_hero_backgrounds'),
    ]

    operations = [
        migrations.CreateModel(
            name='NebyConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('look', models.CharField(default='auto', max_length=24)),
                ('ambient', models.BooleanField(default=True, help_text='Idle Neby looks around, waves and hops now and then.')),
                ('reactions', models.BooleanField(default=True, help_text='Tapping Neby plays a reaction.')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'db_table': 'neby_config'},
        ),
    ]
