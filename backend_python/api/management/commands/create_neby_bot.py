from django.core.management.base import BaseCommand
from api.models import User, BotConfig


class Command(BaseCommand):
    help = 'Create or update the Neby AI bot user account'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='neby', help='Bot username (default: neby)')
        parser.add_argument('--display-name', default='Neby', help='Bot display name (default: Neby)')

    def handle(self, *args, **options):
        username = options['username']
        display_name = options['display_name']
        bot, created = User.objects.get_or_create(
            username=username,
            defaults={
                'id': 'neby-bot',
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
            pk=1,
            defaults={'bot_username': username},
        )
        if config.bot_username != username:
            config.bot_username = username
            config.save()
        if config_created:
            self.stdout.write(self.style.SUCCESS(f'Created BotConfig with default settings'))
        else:
            self.stdout.write(self.style.SUCCESS(f'BotConfig exists (enabled={config.enabled}, model={config.model})'))