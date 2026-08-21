"""Inline content-image uploads (web session auth)."""
import logging

from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .view_helpers import _get_user_id, _rate_limit
from api.models import User
from api import content_images

logger = logging.getLogger(__name__)


@require_POST
def ajax_upload_inline_image(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    if _rate_limit(request, 'upload_inline_image', 40, 3600):
        return JsonResponse({'error': 'Too many uploads. Please try again later.'}, status=429)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    file_obj = request.FILES.get('image')
    if not file_obj:
        return JsonResponse({'error': 'No image file provided'}, status=400)
    try:
        row = content_images.save_content_image(file_obj)
    except ValidationError as e:
        logger.warning('Inline image upload rejected: name=%s size=%s error=%s',
                       getattr(file_obj, 'name', '?'), getattr(file_obj, 'size', '?'), e)
        return JsonResponse({'error': str(e)}, status=400)
    except Exception:
        logger.exception('Inline image upload failed')
        return JsonResponse({'error': 'Upload failed. Please try again.'}, status=500)
    if row.user_id is None:
        from api.models import ContentImage
        ContentImage.objects.filter(pk=row.pk, user__isnull=True).update(user=user)
    return JsonResponse({
        'id': row.id,
        'url': content_images.image_url(row.id),
        'thumbUrl': content_images.thumb_url(row.id),
        'width': row.width,
        'height': row.height,
    })
