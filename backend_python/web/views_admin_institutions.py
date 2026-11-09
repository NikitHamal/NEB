"""Admin review of institution verification applications."""
import mimetypes

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from api import institutions as svc
from api.models_institutions import Institution, InstitutionDocument, InstitutionVerification

from .view_helpers import _ctx, _get_platform_admin, _require_staff_admin

TABS = [('open', 'Open'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('verified', 'Verified institutions')]


def admin_institution_verifications(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    tab = request.GET.get('tab', 'open')
    qs = InstitutionVerification.objects.select_related('applicant', 'institution')
    counts = {
        'open': InstitutionVerification.objects.filter(status__in=InstitutionVerification.OPEN_STATUSES).count(),
        'approved': InstitutionVerification.objects.filter(status='approved').count(),
        'rejected': InstitutionVerification.objects.filter(status='rejected').count(),
        'verified': Institution.objects.filter(verified=True).count(),
    }
    items = verified = []
    if tab == 'verified':
        verified = Institution.objects.filter(verified=True).select_related('claimed_by').order_by('-verified_at')[:200]
    else:
        if tab == 'approved':
            qs = qs.filter(status='approved')
        elif tab == 'rejected':
            qs = qs.filter(status='rejected')
        else:
            tab = 'open'
            qs = qs.filter(status__in=InstitutionVerification.OPEN_STATUSES)
        items = qs.order_by('-created_at')[:200]
    return render(request, 'admin_panel/institution_verifications.html', _ctx(
        request, active_page='institution_verifications', tab=tab, tabs=TABS, counts=counts, items=items,
        verified=verified))


def admin_institution_verification_detail(request, app_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    app = get_object_or_404(InstitutionVerification.objects.select_related('applicant', 'institution', 'reviewed_by'),
                            pk=app_id)
    admin_user = _get_platform_admin(request)
    if request.method == 'POST':
        action = request.POST.get('action', '')
        note = (request.POST.get('note') or '').strip()[:1000]
        if action == 'approve':
            svc.approve(app, admin_user, note)
        elif action == 'reject':
            svc.decide(app, admin_user, InstitutionVerification.STATUS_REJECTED, note)
        elif action == 'info':
            svc.decide(app, admin_user, InstitutionVerification.STATUS_INFO, note)
        return redirect('web:admin_institution_verification_detail', app_id=app.pk)
    others = []
    if app.institution_id:
        others = InstitutionVerification.objects.filter(institution=app.institution).exclude(pk=app.pk)[:10]
    return render(request, 'admin_panel/institution_verification_detail.html', _ctx(
        request, active_page='institution_verifications', app=app, documents=app.documents.all(), others=others))


def admin_institution_document(request, doc_id):
    if _get_platform_admin(request) is None:
        raise Http404()
    doc = get_object_or_404(InstitutionDocument, pk=doc_id)
    try:
        handle = doc.file.open('rb')
    except (FileNotFoundError, ValueError):
        raise Http404()
    kind = doc.content_type or mimetypes.guess_type(doc.original_name)[0] or 'application/octet-stream'
    response = FileResponse(handle, content_type=kind)
    response['Content-Disposition'] = 'inline; filename="%s"' % (doc.original_name or 'document').replace('"', '')
    response['X-Content-Type-Options'] = 'nosniff'
    response['Cache-Control'] = 'private, no-store'
    return response


@require_POST
def admin_institution_revoke(request, institution_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    inst = get_object_or_404(Institution, pk=institution_id)
    svc.revoke(inst)
    return redirect(reverse('web:admin_institution_verifications') + '?tab=verified')
