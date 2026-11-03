"""Admin > Analytics: the page and its CSV export.

All numbers come from `nebians.analytics.report`; this module only handles the
request (range + platform filter), the staff guard and rendering.
"""
import csv

from django.http import HttpResponse
from django.shortcuts import render

from nebians.analytics import report as analytics_report

from .view_helpers import _require_staff_admin

RANGE_CHIPS = (
    ('today', 'Today'),
    ('7d', '7 days'),
    ('30d', '30 days'),
    ('90d', '90 days'),
)
SOURCE_CHIPS = (('all', 'All'), ('web', 'Website'), ('app', 'App'))


def _params(request):
    rng = analytics_report.resolve_range(request.GET)
    source = request.GET.get('source', 'all')
    if source not in ('all', 'web', 'app'):
        source = 'all'
    return rng, source


def admin_analytics(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    rng, source = _params(request)
    data = analytics_report.build_report(rng, source, use_cache=request.GET.get('refresh') != '1')
    return render(request, 'admin_panel/analytics.html', {
        'is_admin': True,
        'active_page': 'analytics',
        'r': data,
        'range_chips': RANGE_CHIPS,
        'source_chips': SOURCE_CHIPS,
        'source': source,
    })


def admin_analytics_export_csv(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response

    rng, source = _params(request)
    rows = analytics_report.daily_rows(rng, source)
    response = HttpResponse(content_type='text/csv')
    tag = rng['key'] if rng['key'] != 'custom' else f'{rng["from"]}_{rng["to"]}'
    response['Content-Disposition'] = f'attachment; filename="nebians-analytics-{tag}-{source}.csv"'
    cols = ['period', 'visitors', 'visits', 'pageviews', 'new_accounts', 'threads', 'resources', 'replies']
    writer = csv.writer(response)
    writer.writerow(cols)
    for row in rows:
        writer.writerow([row[c] for c in cols])
    return response
