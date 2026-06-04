import time
from django.db import migrations, models


def migrate_singleton_to_multi(apps, schema_editor):
    """Convert the singleton BotConfig (pk=1) to multi-bot schema.
    
    - Backfill name/display_name/created_at from existing bot_username
    - Add bot_config_id FK to NebyTask rows, linking to existing config
    """
    BotConfig = apps.get_model('api', 'BotConfig')
    NebyTask = apps.get_model('api', 'NebyTask')
    
    # Backfill new fields on existing row(s)
    for config in BotConfig.objects.all():
        changed = False
        if not config.name:
            config.name = config.bot_username.capitalize()
            changed = True
        if not config.display_name:
            config.display_name = config.bot_username.capitalize()
            changed = True
        if not config.created_at:
            config.created_at = int(time.time() * 1000)
            changed = True
        if changed:
            config.save()

    # Link existing NebyTask rows to the first BotConfig
    first_config = BotConfig.objects.first()
    if first_config:
        NebyTask.objects.filter(bot_config__isnull=True).update(bot_config=first_config)


def reverse_migrate(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_botconfig_provider'),
    ]

    operations = [
        # Add new fields to BotConfig (nullable or with defaults)
        migrations.AddField(
            model_name='botconfig',
            name='name',
            field=models.CharField(default='Neby', max_length=100, help_text='Display name shown in the admin panel.'),
        ),
        migrations.AddField(
            model_name='botconfig',
            name='display_name',
            field=models.CharField(blank=True, default='', max_length=100, help_text='Friendly name the bot uses in replies. Falls back to name.'),
        ),
        migrations.AddField(
            model_name='botconfig',
            name='avatar_url',
            field=models.TextField(blank=True, default='', help_text='URL for the bot avatar image.'),
        ),
        migrations.AddField(
            model_name='botconfig',
            name='created_at',
            field=models.BigIntegerField(default=0),
        ),
        # Add FK to NebyTask (nullable)
        migrations.AddField(
            model_name='nebytask',
            name='bot_config',
            field=models.ForeignKey(
                null=True,
                on_delete=models.SET_NULL,
                related_name='tasks',
                to='api.botconfig',
                db_column='bot_config_id',
            ),
        ),
        # Backfill data before changing PK / adding unique constraint
        migrations.RunPython(migrate_singleton_to_multi, reverse_migrate),
        # Make bot_username unique (was non-unique before)
        migrations.AlterField(
            model_name='botconfig',
            name='bot_username',
            field=models.CharField(default='neby', help_text='The @username that triggers this bot. Must match a User with is_bot=True.', max_length=50, unique=True),
        ),
        # Change PK from PositiveIntegerField(default=1) to AutoField
        # On MariaDB this becomes: ALTER TABLE bot_config MODIFY COLUMN id INT UNSIGNED NOT NULL AUTO_INCREMENT
        migrations.AlterField(
            model_name='botconfig',
            name='id',
            field=models.AutoField(primary_key=True),
        ),
    ]