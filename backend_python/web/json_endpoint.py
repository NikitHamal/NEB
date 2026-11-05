from functools import wraps

from django.http import JsonResponse

from .view_helpers import _get_user_id


def _guard(view, post_only):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        user_id = _get_user_id(request)
        if not user_id:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        if post_only and request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return view(request, *args, user_id=user_id, **kwargs)
    return wrapped


def signed_in_json(view):
    """401 JSON for anonymous callers; otherwise the view is called with `user_id=`."""
    return _guard(view, post_only=False)


def signed_in_json_post(view):
    """`signed_in_json` that also answers 405 JSON unless the request is a POST."""
    return _guard(view, post_only=True)
