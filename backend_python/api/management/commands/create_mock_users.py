from django.core.management.base import BaseCommand
from api.models import User
from api.security import hash_password, hash_auth_token
import time


class Command(BaseCommand):
    help = 'Create mock student, teacher, institution, and explorer accounts for local testing'

    def handle(self, *args, **options):
        now = int(time.time() * 1000)

        users = [
            {
                'pk': 'mock_student_001',
                'username': 'student_demo',
                'email': 'student@nebians.test',
                'display_name': 'Aarav Sharma',
                'password_hash': hash_password('demo1234'),
                'role': 'student',
                'gender': 'Male',
                'class_level': '12',
                'subjects': 'Physics, Mathematics, Chemistry',
                'pradesh': '3',
                'district': 'Kathmandu',
                'school': 'Budhanilkantha School',
                'bio': 'Class 12 Science student. Love solving physics problems!',
                'email_verified': True,
            },
            {
                'pk': 'mock_teacher_001',
                'username': 'teacher_demo',
                'email': 'teacher@nebians.test',
                'display_name': 'Dr. Sita Poudel',
                'password_hash': hash_password('demo1234'),
                'role': 'teacher',
                'gender': 'Female',
                'class_level': '12',
                'teaching_subjects': 'Physics, Mathematics',
                'pradesh': '3',
                'district': 'Lalitpur',
                'school': 'St. Xavier\'s College',
                'bio': 'Physics teacher with 10+ years of experience. NEB exam specialist.',
                'email_verified': True,
            },
            {
                'pk': 'mock_institution_001',
                'username': 'institution_demo',
                'email': 'institution@nebians.test',
                'display_name': 'Global Academy of Science',
                'password_hash': hash_password('demo1234'),
                'role': 'institution',
                'gender': 'Other',
                'institution_type': 'college',
                'pradesh': '3',
                'district': 'Kathmandu',
                'school': 'Global Academy of Science',
                'bio': 'Leading educational institution in Kathmandu offering +2 Science and Management programs.',
                'email_verified': True,
            },
            {
                'pk': 'mock_explorer_001',
                'username': 'explorer_demo',
                'email': 'explorer@nebians.test',
                'display_name': 'Curious Learner',
                'password_hash': hash_password('demo1234'),
                'role': 'explorer',
                'gender': 'Other',
                'pradesh': '3',
                'district': 'Bhaktapur',
                'bio': 'Just exploring NEBians to see what it offers. Might upgrade to a student account later.',
                'email_verified': True,
            },
        ]

        for user_data in users:
            pk = user_data.pop('pk')
            user, created = User.objects.update_or_create(pk=pk, defaults=user_data)
            if created:
                auth_token = User.generate_token()
                user.auth_token = hash_auth_token(auth_token)
                user.created_at = now
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Created {user.role}: {user.username} (pk={user.pk})'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Updated existing {user.role}: {user.username} (pk={user.pk})'
                ))

        self.stdout.write(self.style.SUCCESS('\nMock accounts ready:'))
        self.stdout.write('  Student:     student_demo / demo1234')
        self.stdout.write('  Teacher:     teacher_demo / demo1234')
        self.stdout.write('  Institution: institution_demo / demo1234')
        self.stdout.write('  Explorer:    explorer_demo / demo1234')