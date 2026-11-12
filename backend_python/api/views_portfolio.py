"""Education catalog and the portfolio entries (JSON API for web and Android)."""
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .view_helpers import _can_view_locked_profile, _get_user_from_request, _require_verified_user
from . import education_catalog
from .models import ProfileEntry
from .profile_education import (
    create_entry, entry_to_dict, portfolio_sections, update_entry,
)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def education_catalog_view(request):
    """GET /api/education/catalog/ -- every level, program, term and situation."""
    return Response(education_catalog.catalog())


@api_view(['GET', 'POST'])
def my_entries(request):
    """GET/POST /api/profile/entries/ -- the signed-in user's portfolio."""
    user, err = _require_verified_user(request)
    if err:
        return err
    if request.method == 'GET':
        return Response({'sections': portfolio_sections(user)})
    entry, error = create_entry(user, request.data)
    if error:
        return Response({'error': error}, status=400)
    return Response({'status': 'success', 'entry': entry_to_dict(entry)}, status=201)


@api_view(['PATCH', 'DELETE'])
def my_entry(request, entry_id):
    """PATCH/DELETE /api/profile/entries/<id>/"""
    user, err = _require_verified_user(request)
    if err:
        return err
    entry = ProfileEntry.objects.filter(pk=entry_id, user=user).first()
    if entry is None:
        return Response({'error': 'Entry not found'}, status=404)
    if request.method == 'DELETE':
        entry.delete()
        return Response({'status': 'success'})
    entry, error = update_entry(entry, request.data)
    if error:
        return Response({'error': error}, status=400)
    return Response({'status': 'success', 'entry': entry_to_dict(entry)})


@api_view(['GET'])
@permission_classes([AllowAny])
def user_portfolio(request, username):
    """GET /api/users/profile/<username>/portfolio/ -- respects private profiles."""
    target = User.objects.filter(username=username).first()
    if target is None:
        return Response({'error': 'User not found'}, status=404)
    viewer = _get_user_from_request(request)
    if not _can_view_locked_profile(viewer, target):
        return Response({'sections': []})
    return Response({'sections': portfolio_sections(target)})
