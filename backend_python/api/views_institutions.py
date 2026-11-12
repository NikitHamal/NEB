"""GET /api/institutions/ and /api/institutions/<slug>/ for the Android app."""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import institutions as svc
from .models_institutions import Institution
from .services import avatar_or_photo_url


def _int(value, default, maximum):
    try:
        return max(0, min(int(value), maximum))
    except (TypeError, ValueError):
        return default


@api_view(['GET'])
@permission_classes([AllowAny])
def institutions_search(request):
    rows, total, counts = svc.search(
        request.query_params.get('q', ''), request.query_params.get('kind', ''),
        request.query_params.get('district', ''), limit=_int(request.query_params.get('limit'), 30, 50) or 30,
        offset=_int(request.query_params.get('offset'), 0, 100000))
    return Response({'total': total, 'items': [svc.serialize(r, counts.get(r.slug, 0)) for r in rows]})


@api_view(['GET'])
@permission_classes([AllowAny])
def institution_detail(request, slug):
    inst = Institution.objects.select_related('claimed_by').filter(slug=slug).first()
    if not inst:
        return Response({'error': 'Not found'}, status=404)
    counts = svc.people_counts(inst)
    people = [{'username': u.username, 'displayName': u.display_name or u.username, 'role': u.role,
               'photoUrl': avatar_or_photo_url(u) or ''} for u in svc.people_list(inst, 36)]
    return Response({**svc.serialize(inst, counts['total']), 'phone': inst.phone, 'counts': counts, 'people': people})
