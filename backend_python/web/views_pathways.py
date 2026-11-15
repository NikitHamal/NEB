from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_control

from api import pathways
from api.models import NEPAL_DISTRICTS

from .view_helpers import _ctx


@require_GET
@cache_control(public=True, max_age=300)
def pathways_page(request):
    return render(request, 'web/pathways.html', _ctx(
        request, pathways_data=pathways.payload(), districts=NEPAL_DISTRICTS,
    ))
