"""Institutions for the Android app and the web forms.

GET  /api/institutions/                  search (claimed first, then the fullest portfolios)
GET  /api/institutions/schema/           option lists for the portfolio form
GET  /api/institutions/mine/             the signed-in account's claimed institution and application
GET  /api/institutions/<slug>/           one institution with its portfolio and people
PATCH /api/institutions/<slug>/profile/  the owner edits the portfolio, any field, any time
POST /api/institutions/<slug>/claim/     multipart claim application (same rules as the web form)
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.decorators import parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import institution_profile as prof
from . import institutions as svc
from .models_institutions import Institution, InstitutionVerification
from .services import avatar_or_photo_url
from .view_helpers import _get_user_from_request, _require_verified_user


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
        offset=_int(request.query_params.get('offset'), 0, 100000),
        verified_only=request.query_params.get('verified') == '1')
    return Response({'total': total, 'items': [svc.serialize(r, counts.get(r.slug, 0)) for r in rows]})


@api_view(['GET'])
@permission_classes([AllowAny])
def institutions_schema(request):
    return Response(prof.schema())


@api_view(['GET'])
@permission_classes([AllowAny])
def institution_detail(request, slug):
    inst = Institution.objects.select_related('claimed_by', 'profile').filter(slug=slug).first()
    if not inst:
        return Response({'error': 'Not found'}, status=404)
    counts = svc.people_counts(inst)
    people = [{'username': u.username, 'displayName': u.display_name or u.username, 'role': u.role,
               'photoUrl': avatar_or_photo_url(u) or ''} for u in svc.people_list(inst, 36)]
    viewer = _get_user_from_request(request)
    mine = bool(viewer and inst.claimed_by_id == viewer.pk and inst.verified)
    portfolio = prof.payload(inst)
    if not mine:
        portfolio.pop('missing', None)
    return Response({**svc.serialize(inst, counts['total']), 'phone': inst.phone, 'email': inst.email,
                     'counts': counts, 'people': people, 'portfolio': portfolio,
                     'canEdit': mine, 'claimable': not inst.verified})


def _application(app):
    return {'id': app.id, 'status': app.status, 'name': app.name, 'note': app.reviewer_note,
            'institution': app.institution.slug if app.institution_id else ''}


@api_view(['GET'])
def institution_mine(request):
    user, err = _require_verified_user(request)
    if err:
        return err
    inst = Institution.objects.select_related('profile').filter(claimed_by=user, verified=True).first()
    app = (InstitutionVerification.objects.filter(applicant=user).select_related('institution')
           .order_by('-created_at').first())
    out = {'institution': None, 'application': _application(app) if app else None}
    if inst:
        out['institution'] = {**svc.serialize(inst, svc.people_counts(inst)['total']),
                              'portfolio': prof.payload(inst)}
    return Response(out)


@api_view(['PATCH', 'POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def institution_profile_update(request, slug):
    user, err = _require_verified_user(request)
    if err:
        return err
    inst = prof.owned_by(user, slug)
    if inst is None:
        return Response({'error': 'Only the verified owner can edit this portfolio.'}, status=403)
    payload, error = prof.save(inst, request.data if isinstance(request.data, dict) else request.data.dict())
    if error:
        return Response({'error': error}, status=400)
    return Response({'status': 'success', 'portfolio': payload})


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def institution_claim(request, slug):
    user, err = _require_verified_user(request)
    if err:
        return err
    inst = Institution.objects.filter(slug=slug).first()
    if not inst:
        return Response({'error': 'Not found'}, status=404)
    if user.role != 'institution':
        return Response({'error': 'Only institution accounts can claim a school.'}, status=403)
    if inst.verified and inst.claimed_by_id != user.pk:
        return Response({'error': 'This institution is already claimed.'}, status=409)
    if svc.open_application(user):
        return Response({'error': 'You already have an application under review.'}, status=409)
    data, uploads, errors = svc.validate_application(request.data, request.FILES, inst)
    if errors:
        return Response({'error': next(iter(errors.values())), 'errors': errors}, status=400)
    app = svc.create_application(user, data, uploads, inst)
    return Response({'status': 'success', 'application': _application(app)}, status=201)
