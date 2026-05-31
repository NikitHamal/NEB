import uuid
import time

from django.core.management.base import BaseCommand
from django.db import transaction

from api.models import Post, Reply, User


class Command(BaseCommand):
    help = 'Seed nested reply data for testing thread UI. Creates replies at multiple nesting levels on the most recent forum post.'

    def handle(self, *args, **options):
        post = Post.objects.order_by('-created_at').first()
        if not post:
            self.stdout.write(self.style.ERROR('No posts found. Create a post first.'))
            return

        users = list(User.objects.all()[:5])
        if len(users) < 2:
            self.stdout.write(self.style.ERROR('Need at least 2 users.'))
            return

        now = int(time.time() * 1000)
        created = 0

        existing = Reply.objects.filter(post=post).count()
        if existing > 20:
            self.stdout.write(self.style.WARNING(f'Post already has {existing} replies. Skipping.'))
            return

        with transaction.atomic():
            # Top-level reply 1 (by user 1)
            r1 = Reply.objects.create(
                id=str(uuid.uuid4()), post=post, parent_reply=None,
                user=users[0], content='This is a top-level reply. Does anyone have notes for Chapter 5?',
                thumbs_up_count=2, reply_count=3, created_at=now - 300000
            )

            # Nested reply to r1 (by user 2)
            r2 = Reply.objects.create(
                id=str(uuid.uuid4()), post=post, parent_reply=r1,
                user=users[1], content='@' + users[0].username + ' Yes! I have the complete notes. Let me share them.',
                thumbs_up_count=1, reply_count=1, created_at=now - 280000
            )

            # Nested reply to r2 (by user 0, replying to the reply)
            r3 = Reply.objects.create(
                id=str(uuid.uuid4()), post=post, parent_reply=r2,
                user=users[0], content='@' + users[1].username + ' That would be amazing, thank you so much!',
                thumbs_up_count=0, reply_count=1, created_at=now - 260000
            )

            # Nested reply to r3 (by user 2)
            r4 = Reply.objects.create(
                id=str(uuid.uuid4()), post=post, parent_reply=r3,
                user=users[1], content='No problem! I also have model questions from last year.',
                thumbs_up_count=0, reply_count=0, created_at=now - 240000
            )

            # Another nested reply to r1 (by user 2, different branch)
            r5 = Reply.objects.create(
                id=str(uuid.uuid4()), post=post, parent_reply=r1,
                user=users[1] if len(users) > 1 else users[0],
                content='I also need those notes. Can you share the PDF?',
                thumbs_up_count=0, reply_count=0, created_at=now - 250000
            )

            # Top-level reply 2 (by user 2)
            r6 = Reply.objects.create(
                id=str(uuid.uuid4()), post=post, parent_reply=None,
                user=users[1] if len(users) > 1 else users[0],
                content='Has anyone solved the numerical problems from Unit 3? The ones about thermodynamics are really tricky.',
                thumbs_up_count=3, reply_count=2, created_at=now - 200000
            )

            # Nested reply to r6
            r7 = Reply.objects.create(
                id=str(uuid.uuid4()), post=post, parent_reply=r6,
                user=users[0],
                content='@' + users[1].username + ' I solved them yesterday. The key is to use the first law of thermodynamics formula correctly.',
                thumbs_up_count=1, reply_count=1, created_at=now - 180000
            )

            # Deep nested reply to r7
            r8 = Reply.objects.create(
                id=str(uuid.uuid4()), post=post, parent_reply=r7,
                user=users[1] if len(users) > 1 else users[0],
                content='Can you show your working? I keep getting the wrong answer for Q3.',
                thumbs_up_count=0, reply_count=0, created_at=now - 160000
            )

            # Another nested reply to r6
            r9 = Reply.objects.create(
                id=str(uuid.uuid4()), post=post, parent_reply=r6,
                user=users[2] if len(users) > 2 else users[0],
                content='I found a great YouTube channel that explains these problems step by step.',
                thumbs_up_count=0, reply_count=0, created_at=now - 170000
            )

            # Top-level reply 3 (by user 0)
            if len(users) > 2:
                r10 = Reply.objects.create(
                    id=str(uuid.uuid4()), post=post, parent_reply=None,
                    user=users[2], content='The exam is next week! Can we make a study group?',
                    thumbs_up_count=5, reply_count=2, created_at=now - 100000
                )

                r11 = Reply.objects.create(
                    id=str(uuid.uuid4()), post=post, parent_reply=r10,
                    user=users[0], content='@' + users[2].username + ' Count me in! When and where?',
                    thumbs_up_count=1, reply_count=1, created_at=now - 80000
                )

                r12 = Reply.objects.create(
                    id=str(uuid.uuid4()), post=post, parent_reply=r11,
                    user=users[2], content='How about Saturday at the library? 10 AM?',
                    thumbs_up_count=0, reply_count=0, created_at=now - 60000
                )

                r13 = Reply.objects.create(
                    id=str(uuid.uuid4()), post=post, parent_reply=r10,
                    user=users[1] if len(users) > 1 else users[0],
                    content='I can join too! Let me know the details.',
                    thumbs_up_count=0, reply_count=0, created_at=now - 70000
                )

                created += 4

        Post.objects.filter(pk=post.pk).update(reply_count=Reply.objects.filter(post=post).count())

        total = Reply.objects.filter(post=post).count()
        self.stdout.write(self.style.SUCCESS(f'Seeded {created + 9} nested replies on post "{post.title}" (total: {total} replies)'))