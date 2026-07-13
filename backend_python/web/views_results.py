"""Result checker views."""
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.core.cache import cache
from .view_helpers import _ctx

from services import result_scraper


@require_GET
def result_check_page(request):
    """Render the result checker page."""
    return render(request, 'web/result_checker.html', _ctx(request))


@require_GET
def tools_hub(request):
    """Render the tools hub page listing available utilities."""
    return render(request, 'web/tools_hub.html', _ctx(request))


@require_POST
def ajax_check_result(request):
    """API endpoint to check a result.

    POST params:
        exam: 'neb' or 'see'
        symbol: symbol number
        dob: date of birth (YYYY/MM/DD or YYYY-MM-DD)
        batch: exam year/batch (e.g. 2080, 2081, 2082, 2083)
    """
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        body = request.POST

    exam = (body.get('exam') or '').strip().lower()
    symbol = (body.get('symbol') or '').strip()
    dob = (body.get('dob') or '').strip()
    batch = (body.get('batch') or '').strip()

    if not exam:
        return JsonResponse({'success': False, 'error': 'Exam type is required'})
    if not symbol:
        return JsonResponse({'success': False, 'error': 'Symbol number is required'})
    if exam in ('neb', 'neb_reexam') and not dob:
        return JsonResponse({'success': False, 'error': 'Date of birth is required'})

    result = result_scraper.check_result(exam, symbol, dob or '', batch=batch)
    return JsonResponse(result)
