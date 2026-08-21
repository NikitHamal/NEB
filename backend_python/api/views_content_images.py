"""Inline content-image uploads (mobile bearer-token auth)."""
import logging

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .view_helpers import _require_user
from . import content_images
from .models import ContentImage

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def upload_content_image(request):
    user, err = _require_user(request)
    if err:
        return err
    file_obj = request.FILES.get('image')
    if not file_obj:
        return Response({'error': 'No image file provided'}, status=400)
    try:
        row = content_images.save_content_image(file_obj)
    except Exception as exc:
        from django.core.exceptions import ValidationError
        if isinstance(exc, ValidationError):
            message = exc.messages[0] if getattr(exc, 'messages', None) else str(exc)
            return Response({'error': str(message)}, status=400)
        logger.exception('Inline image upload failed (api)')
        return Response({'error': 'Upload failed. Please try again.'}, status=500)
    if row.user_id is None:
        ContentImage.objects.filter(pk=row.pk, user__isnull=True).update(user=user)
    return Response({
        'id': row.id,
        'url': content_images.image_url(row.id),
        'thumbUrl': content_images.thumb_url(row.id),
        'width': row.width,
        'height': row.height,
    }, status=201)
