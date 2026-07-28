from django.http import JsonResponse
from django.db import connection, ProgrammingError
from django.core.cache import cache


def health_check(request):
    checks = {}
    all_ok = True
    status_code = 200

    try:
        cache.set('__health_ping', 1, 5)
        cache.get('__health_ping')
        checks['cache'] = 'ok'
    except Exception as e:
        checks['cache'] = f'fail: {e}'
        all_ok = False

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        checks['database'] = 'ok'
    except Exception as e:
        checks['database'] = f'fail: {e}'
        all_ok = False

    if not all_ok:
        status_code = 503

    return JsonResponse({'status': 'ok' if all_ok else 'degraded', 'checks': checks}, status=status_code)