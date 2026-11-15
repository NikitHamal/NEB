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
