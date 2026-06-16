from django.core.management.base import BaseCommand
from api.models import User, FCMToken
from api.fcm_utils import send_fcm_message

class Command(BaseCommand):
    help = 'Send a test FCM push notification to a user or a specific token'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Target username to send notification to')
        parser.add_argument('--token', type=str, help='Direct FCM registration token')
        parser.add_argument('--title', type=str, default='Test Notification', help='Notification title')
        parser.add_argument('--body', type=str, default='This is a test push notification from NEBians.', help='Notification body')

    def handle(self, *args, **options):
        title = options['title']
        body = options['body']
        token = options['token']
        username = options['username']

        if token:
            self.stdout.write(f"Sending test notification to token: {token[:20]}...")
            send_fcm_message([token], title, body, data={'test': 'true'})
            self.stdout.write(self.style.SUCCESS("Notification queued!"))
            return

        if username:
            try:
                user = User.objects.get(username=username)
                tokens = list(FCMToken.objects.filter(user=user).values_list('token', flat=True))
                if not tokens:
                    self.stdout.write(self.style.WARNING(f"User '{username}' has no registered FCM tokens."))
                    return
                
                self.stdout.write(f"Sending test notification to user '{username}' ({len(tokens)} token(s))...")
                send_fcm_message(tokens, title, body, data={'test': 'true'})
                self.stdout.write(self.style.SUCCESS("Notification queued!"))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with username '{username}' does not exist."))
            return

        # Fallback: list all registered users with tokens
        tokens_count = FCMToken.objects.count()
        self.stdout.write(f"Usage: python manage.py test_fcm --username <username> OR --token <token>")
        self.stdout.write(f"Total registered FCM tokens in database: {tokens_count}")
        for t in FCMToken.objects.all():
            self.stdout.write(f"  - User: {t.user.username if t.user else 'None'} | Token: {t.token[:30]}...")
