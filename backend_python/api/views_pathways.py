"""GET /api/pathways/ : the whole Pathways dataset in one cacheable payload (web and Android)."""
from django.http import HttpResponse, HttpResponseNotModified, JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny

from . import pathways


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def pathways_data(request):
    data = pathways.payload()
    tag = f'"{data["etag"]}"'
    if request.headers.get('If-None-Match') == tag:
        resp = HttpResponseNotModified()
    else:
        resp = JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'separators': (',', ':')})
    resp['ETag'] = tag
    resp['Cache-Control'] = 'public, max-age=3600'
    return resp


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def pathways_on_neb(request):
    """GET /api/pathways/on-neb/ : claimed institutions with a portfolio, fullest first, and which
    Pathways college each one is (`matches`: provider id -> slug). Small and live, so the big
    cached payload stays static; Find a college shows these first."""
    from .models_institutions import InstitutionProfile, search_key
    from .institution_profile import LEVELS
    level_label = dict(LEVELS)
    rows = list(InstitutionProfile.objects.filter(institution__verified=True, completeness__gt=0)
                .select_related('institution').order_by('-completeness', 'institution__name')[:200])
    items = []
    for row in rows:
        i, d = row.institution, row.data or {}
        items.append({
            'slug': i.slug, 'name': i.name, 'kind': i.kind, 'district': i.district, 'place': i.place,
            'completeness': row.completeness,
            'levels': [level_label.get(k, k) for k in d.get('levels', [])], 'levelKeys': d.get('levels', []), 'feeMin': d.get('feeMin'),
            'feeMax': d.get('feeMax'), 'admissionOpen': bool(d.get('admissionOpen')),
            'phone': d.get('phone') or i.phone, 'website': i.website, 'est': i.est,
            'facilities': (d.get('facilities') or [])[:6], 'students': d.get('students'),
        })
    keys = {search_key(it['name']): it['slug'] for it in items}
    matches = {}
    for p in pathways.payload()['providers']:
        slug = keys.get(search_key(p['name']))
        if slug:
            matches[p['id']] = slug
    resp = JsonResponse({'items': items, 'matches': matches})
    resp['Cache-Control'] = 'public, max-age=300'
    return resp
