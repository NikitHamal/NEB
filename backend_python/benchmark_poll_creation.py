import os
import sys
import time
import django

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
django.setup()

from django.core.management import call_command
from django.db import connection, reset_queries
from django.test.utils import CaptureQueriesContext
from api.models import User
from api.services import create_post

def benchmark():
    call_command('migrate', verbosity=0)

    user, _ = User.objects.get_or_create(
        id='bench_user_1',
        defaults={
            'username': 'bench_user',
            'email': 'bench@example.com',
            'email_verified': True,
        }
    )

    options_counts = [5, 20, 50, 100]
    print("=== Poll Creation Benchmark ===")
    for num_options in options_counts:
        poll_options = [{'text': f'Option {i}', 'is_correct': (i == 0)} for i in range(num_options)]
        poll_data = {
            'question': f'Benchmark Poll with {num_options} options',
            'poll_type': 'voting',
            'options': poll_options,
        }

        reset_queries()
        start_time = time.perf_counter()
        with CaptureQueriesContext(connection) as ctx:
            post = create_post(
                user=user,
                title=f'Test Post {num_options}',
                content='Benchmarking poll options creation',
                category='General',
                poll_data=poll_data
            )
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        num_queries = len(ctx.captured_queries)
        print(f"Options: {num_options:3d} | Queries: {num_queries:3d} | Time: {elapsed_ms:6.2f} ms")

if __name__ == '__main__':
    benchmark()
