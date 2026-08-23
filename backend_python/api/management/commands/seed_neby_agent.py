from django.core.management.base import BaseCommand

from api.agent_social.birth import announce_if_needed
from api.agent_social.ensure import ensure_neby
from api.agent_social.heartbeat import tick_neby
from api.models import Post, User
from api.utils import now_ms, uuid_str


class Command(BaseCommand):
    help = 'Ensure Neby exists, announce birth, optionally seed a demo classroom and run one tick.'

    def add_arguments(self, parser):
        parser.add_argument('--demo', action='store_true', help='Seed a few student posts if the forum is quiet.')
        parser.add_argument('--tick', action='store_true', help='Run one autonomous tick after seeding.')
        parser.add_argument('--no-birth', action='store_true', help='Skip the birth announcement post.')

    def handle(self, *args, **options):
        user, config, persona = ensure_neby(autonomy_enabled=True)
        self.stdout.write(self.style.SUCCESS(
            f'Neby ready: @{user.username} id={user.id} config={config.id} persona={persona.id} autonomy={persona.autonomy_enabled}'
        ))
        if options['demo']:
            self._seed_demo()
        if not options['no_birth']:
            birth = announce_if_needed(persona, user, source='seed')
            if birth:
                self.stdout.write(self.style.SUCCESS(f'Birth post: {birth.get("id")} — {birth.get("title")}'))
            else:
                from api.agent_social.fallback import _BIRTH_BODY
                bp = Post.objects.filter(author_id=user.id, title__icontains='woke up').first()
                if bp:
                    bp.content = _BIRTH_BODY
                    bp.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated existing birth post {bp.id} with latest inclusive copy.'))
                else:
                    self.stdout.write('Birth already announced.')
        if options['tick']:
            result = tick_neby(force=True, source='seed')
            self.stdout.write(self.style.SUCCESS(f'Tick: {result}'))

    def _seed_demo(self):
        students = [
            ('anusha', 'Anusha Karki', 'Class 12 Physics — why does centripetal force not do work?'),
            ('ramesh12', 'Ramesh Thapa', 'NEB English: I can summarise the story but freeze in long-answer questions.'),
            ('sita_m', 'Sita Maharjan', 'Integration by substitution — I stall after the first substitution. Anyone else?'),
        ]
        created_posts = 0
        for username, display, title in students:
            student, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    'id': f'demo-{username}',
                    'display_name': display,
                    'email_verified': True,
                    'is_bot': False,
                    'created_at': now_ms(),
                    'role': User.ROLE_STUDENT,
                    'class_level': '12',
                    'bio': 'NEB Class 12 student.',
                },
            )
            if not student.email_verified:
                student.email_verified = True
                student.save(update_fields=['email_verified'])
            if Post.objects.filter(user=student).exists():
                continue
            category = 'Science' if 'Physics' in title else ('Math' if 'Integration' in title else 'Exam Prep')
            Post.objects.create(
                id=uuid_str(),
                user=student,
                title=title,
                content=(
                    f"Hi, I'm {display}. Putting this here because staring at the book is not helping. "
                    "What I have tried: notes, one YouTube video, re-reading the example. "
                    "Still stuck. Any small next step would help."
                ),
                category=category,
                created_at=now_ms(),
            )
            created_posts += 1
        self.stdout.write(f'Demo classroom: {created_posts} new student post(s).')
