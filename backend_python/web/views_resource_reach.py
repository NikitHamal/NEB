"""Web twins of the resource reach endpoints (session auth, JSON bodies). Logic lives in api.resource_reach."""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from api import resource_insights, resource_reach
from api.models import Resource, User

from .view_helpers import _get_user_id


def _body(request) -> dict:
    try:
        data = json.loads(request.body or b'{}')
    except (ValueError, UnicodeDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _viewer(request):
    uid = _get_user_id(request)
    return User.objects.filter(pk=uid).first() if uid else None


def _days(request) -> int:
    try:
        return int(request.GET.get('days', 30))
    except ValueError:
        return 30


@require_POST
def ajax_resource_view(request, resource_id):
    """Read time for a resource page (the page itself already counted the view)."""
    resource = Resource.objects.filter(pk=resource_id).first()
    if not resource:
        return JsonResponse({'error': 'Resource not found'}, status=404)
    data = _body(request)
    try:
        dwell = int(data.get('dwell_ms') or 0)
    except (TypeError, ValueError):
        dwell = 0
    return JsonResponse(resource_reach.record_view(
        request, resource, _viewer(request), surface=str(data.get('surface') or ''), dwell_ms=dwell,
        src=str(data.get('src') or '')))


@require_POST
def ajax_resource_action(request, resource_id):
    resource = Resource.objects.filter(pk=resource_id).first()
    if not resource:
        return JsonResponse({'error': 'Resource not found'}, status=404)
    out = resource_reach.record_action(request, resource, _viewer(request), str(_body(request).get('action') or ''))
    return JsonResponse(out, status=200 if out.get('ok') or 'error' not in out else 400)


@require_POST
def ajax_resource_impressions(request):
    ids = _body(request).get('ids') or []
    return JsonResponse({'recorded': resource_reach.record_impressions(request, ids if isinstance(ids, list) else [])})


@require_GET
def ajax_resource_insights(request, resource_id):
    """The uploader (or staff) sees one resource's insights."""
    user = _viewer(request)
    if not user:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    resource = Resource.objects.filter(pk=resource_id).first()
    if not resource:
        return JsonResponse({'error': 'Resource not found'}, status=404)
    if resource.uploaded_by_id != user.id and not user.is_admin:
        return JsonResponse({'error': 'Only the uploader can see these insights'}, status=403)
    return JsonResponse(resource_insights.build(resource, days=_days(request)))


@require_GET
def ajax_uploads_insights(request):
    """Everything the signed-in member uploaded, plus their posts."""
    user = _viewer(request)
    if not user:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    return JsonResponse(resource_insights.overview(user, days=_days(request)))
