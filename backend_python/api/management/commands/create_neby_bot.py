from django.core.management.base import BaseCommand
from api.agent_social.ensure import ensure_neby


class Command(BaseCommand):
    help = 'Create or update Neby: User, BotConfig, and autonomous AgentPersona'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='neby', help='Bot username (default: neby)')
        parser.add_argument('--display_name', default='Neby AI', help='Bot display name')
        parser.add_argument('--name', default='Neby Assistant', help='Bot config name')

    def handle(self, *args, **options):
        user, config, persona = ensure_neby(autonomy_enabled=True)
        self.stdout.write(self.style.SUCCESS(
            f'Neby ready @{user.username} id={user.id} config={config.id} '
            f'persona={persona.id} autonomy={persona.autonomy_enabled}'
        ))