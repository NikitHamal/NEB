"""Product switches for features that exist in code but are not public yet.

MARKETPLACE_ENABLED (env, default off): the creator marketplace — storefront pages, courses,
the studio and their APIs. While it is off every marketplace route answers 404, the Library
loses its Marketplace shelf and the app hides its entry points (it reads `features` from
/api/app/features/). The code, models and data are untouched; set the variable to 1 to bring
it all back.
"""
import os
from functools import wraps

from django.http import Http404, JsonResponse

MARKETPLACE_ENABLED = os.environ.get('MARKETPLACE_ENABLED', '0').strip().lower() in ('1', 'true', 'yes', 'on')


def marketplace_gate(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not MARKETPLACE_ENABLED:
            if request.path.startswith('/api/'):
                return JsonResponse({'detail': 'Not found.'}, status=404)
            raise Http404('Not found')
        return view(request, *args, **kwargs)
    return wrapped


def context(request):
    """Template context processor."""
    return {'marketplace_enabled': MARKETPLACE_ENABLED}


def app_features(request):
    """GET /api/app/features/ — what the native app may show."""
    return JsonResponse({'marketplace': MARKETPLACE_ENABLED})
