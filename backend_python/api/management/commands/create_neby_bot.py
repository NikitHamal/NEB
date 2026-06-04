from django.core.management.base import BaseCommand
from api.models import User, BotConfig


class Command(BaseCommand):
    help = 'Create or update a bot user account and BotConfig'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='neby', help='Bot username (default: neby)')
        parser.add_argument('--display-name', default='Neby', help='Bot display name (default: Neby)')
        parser.add_argument('--name', default='Neby', help='BotConfig name (default: Neby)')

    def handle(self, *args, **options):
        username = options['username']
        display_name = options['display_name']
        name = options['name']
        bot, created = User.objects.get_or_create(
            username=username,
            defaults={
                'id': f'{username}-bot',
                'display_name': display_name,
                'is_bot': True,
                'email_verified': True,
                'created_at': 0,
            },
        )
        if not created:
            changed = False
            if not bot.is_bot:
                bot.is_bot = True
                changed = True
            if bot.display_name != display_name:
                bot.display_name = display_name
                changed = True
            if changed:
                bot.save()
        status = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{status} bot user: @{username} (id={bot.id}, is_bot={bot.is_bot})'))
        config, config_created = BotConfig.objects.get_or_create(
            bot_username__iexact=username,
            defaults={
                'name': name,
                'bot_username': username,
                'display_name': display_name,
                'enabled': True,
            },
        )
        if config_created:
            self.stdout.write(self.style.SUCCESS(f'Created BotConfig "{name}" (@{username})'))
        else:
            changed = False
            if config.bot_username != username:
                config.bot_username = username
                changed = True
            if config.name != name:
                config.name = name
                changed = True
            if config.display_name != display_name:
                config.display_name = display_name
                changed = True
            if changed:
                config.save()
            self.stdout.write(self.style.SUCCESS(f'BotConfig exists (enabled={config.enabled}, model={config.model})'))