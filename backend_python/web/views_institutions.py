"""Schools directory, school pages, the redirect to a school's own site and the verification application."""
from urllib.parse import urlparse

from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from api import institutions as svc
from api.models import NEPAL_DISTRICTS
from api.models_institutions import DOC_TYPES, KIND_CHOICES, PROVINCE_NAMES, Institution, InstitutionVerification

from .view_helpers import _avatar_url, _ctx, _get_user_id, _rate_limit, _request_db_user
from .views_institutions_profile import folio_context

PAGE = 30


def _int(value, default=0, maximum=100000):
    try:
        return max(0, min(int(value), maximum))
    except (TypeError, ValueError):
        return default


def _cards(rows, counts):
    return [{'inst': r, 'students': counts.get(r.slug, 0)} for r in rows]


def person_card(u):
    return {
        'username': u.username, 'name': u.display_name or u.username, 'photo': _avatar_url(u),
        'role': 'Teacher' if u.role == 'teacher' else ('Explorer' if u.role == 'explorer' else 'Student'),
        'level': u.class_level or '',
    }


@require_GET
def schools_directory(request):
    q = svc.clean_query(request.GET.get('q'))
    kind = request.GET.get('kind', '')
    district = request.GET.get('district', '')
    page = max(1, _int(request.GET.get('page'), 1, 5000))
    verified_rows, verified_total, vcounts = ([], 0, {})
    if page == 1 and not district:
        verified_rows, verified_total, vcounts = svc.search(q, kind, district, limit=24, verified_only=True)
    rows, total, counts = svc.search(q, kind, district, limit=PAGE, offset=(page - 1) * PAGE, unverified_only=True)
    return render(request, 'web/schools.html', _ctx(
        request, q=q, kind=kind, district=district, page=page, kinds=KIND_CHOICES, districts=NEPAL_DISTRICTS,
        verified=_cards(verified_rows, vcounts), verified_total=verified_total,
        schools=_cards(rows, counts), total=total, has_next=page * PAGE < total, next_page=page + 1,
        catalog_total=Institution.objects.count(),
    ))


@require_GET
def school_detail(request, slug):
    inst = Institution.objects.select_related('claimed_by').filter(slug=slug).first()
    if not inst:
        raise Http404('School not found')
    counts = svc.people_counts(inst)
    role = request.GET.get('who', '')
    people = [person_card(u) for u in svc.people_list(inst, 36, 0, role)]
    user_id = _get_user_id(request)
    viewer = _request_db_user(request, user_id) if user_id else None
    mine = bool(viewer and inst.claimed_by_id == viewer.pk)
    return render(request, 'web/school_detail.html', _ctx(
        request, inst=inst, counts=counts, people=people, who=role, mine=mine,
        claimable=svc.is_claimable(inst, viewer), province=PROVINCE_NAMES.get(inst.province, ''),
        folio=folio_context(inst),
        website_host=urlparse(inst.website).netloc.replace('www.', '') if inst.website else '',
    ))


@require_GET
def school_go(request, slug):
    inst = Institution.objects.select_related('claimed_by').filter(slug=slug).first()
    if not inst:
        raise Http404('School not found')
    if inst.claimed_by_id and inst.verified:
        return redirect('web:profile', username=inst.claimed_by.username)
    if inst.website and urlparse(inst.website).scheme in ('http', 'https'):
        response = HttpResponseRedirect(inst.website)
        response['Referrer-Policy'] = 'no-referrer'
        return response
    return redirect('web:school_detail', slug=inst.slug)


@require_GET
def ajax_school_search(request):
    if _rate_limit(request, 'school_search', 90, 60):
        return JsonResponse({'error': 'Slow down'}, status=429)
    q = svc.clean_query(request.GET.get('q'))
    limit = _int(request.GET.get('limit'), 20, 40) or 20
    rows, total, counts = svc.search(q, request.GET.get('kind', ''), request.GET.get('district', ''),
                                     limit=limit, offset=_int(request.GET.get('offset')))
    return JsonResponse({'total': total, 'items': [svc.serialize(r, counts.get(r.slug, 0)) for r in rows]})


def _form_defaults(user, inst):
    return {
        'name': inst.name if inst else (user.school or user.display_name or ''),
        'kind': inst.kind if inst else svc.kind_for_type(user.institution_type),
        'district': inst.district if inst else (user.district or ''),
        'address': inst.location if inst else '',
        'website': inst.website if inst else '',
        'registration_no': '', 'contact_name': '', 'contact_role': '',
        'contact_email': user.email or '', 'contact_phone': '', 'message': '',
    }


def school_apply(request):
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('%s?next=%s' % (reverse('web:login'), request.get_full_path()))
    user = _request_db_user(request, user_id)
    if not user:
        return redirect('web:login')
    slug = request.POST.get('institution') or request.GET.get('school') or ''
    inst = Institution.objects.select_related('claimed_by').filter(slug=slug).first() if slug else None
    applications = list(InstitutionVerification.objects.filter(applicant=user).select_related('institution')[:6])
    open_app = next((a for a in applications if a.is_open), None)
    approved = next((a for a in applications if a.status == 'approved'), None)
    values, errors = _form_defaults(user, inst), {}
    taken = bool(inst and inst.verified and inst.claimed_by_id != user.pk)
    blocked = user.role != 'institution' or bool(open_app) or bool(user.institution_verified and approved)
    if request.method == 'POST' and not blocked and not taken:
        if _rate_limit(request, 'inst_apply', 6, 3600):
            errors['form'] = 'Too many attempts. Try again later.'
        else:
            data, uploads, errors = svc.validate_application(request.POST, request.FILES, inst)
            values = {**values, **data}
            if not errors:
                svc.create_application(user, data, uploads, inst)
                return redirect('%s?sent=1' % reverse('web:school_apply'))
    return render(request, 'web/school_apply.html', _ctx(
        request, inst=inst, values=values, errors=errors, kinds=KIND_CHOICES, districts=NEPAL_DISTRICTS,
        doc_types=DOC_TYPES, applications=applications, open_app=open_app, approved=approved,
        wrong_role=user.role != 'institution', taken=taken, sent=request.GET.get('sent') == '1',
        can_apply=not blocked and not taken, is_verified=bool(user.institution_verified and approved),
    ))
