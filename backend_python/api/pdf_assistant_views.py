import time
import uuid
import os
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.response import Response

from .authentication import AuthTokenAuthentication
from .models import Resource, User, NebyCreditTransaction
from .credit_views import check_and_reset_monthly_credits, WHATSAPP_CONTACT
from .qwen_utils.client import QwenClient
from .qwen_utils.text_extraction import extract_text_from_bytes
from .security import validate_resource_file_url
from .throttles import ArenaChatRateThrottle

MAX_PDF_BYTES = 25 * 1024 * 1024
MAX_CONTEXT_CHARS = 42000


def _user_or_error(request):
    user = getattr(request, 'user', None)
    if isinstance(user, User) and not user.is_locked:
        return user, None
    return None, Response({'error': 'Please sign in'}, status=status.HTTP_401_UNAUTHORIZED)


def _local_media_bytes(url):
    path = unquote(urlparse(url).path or '')
    media_url = str(settings.MEDIA_URL or '/media/')
    if not path.startswith(media_url):
        return None
    media_root = Path(settings.MEDIA_ROOT).resolve()
    candidate = (media_root / path[len(media_url):].lstrip('/')).resolve()
    if not candidate.is_relative_to(media_root) or not candidate.is_file():
        return None
    with candidate.open('rb') as handle:
        data = handle.read(MAX_PDF_BYTES + 1)
    return data if len(data) <= MAX_PDF_BYTES else None


def _resource_pdf_bytes(resource):
    if resource.file:
        with resource.file.open('rb') as handle:
            data = handle.read(MAX_PDF_BYTES + 1)
        return data if len(data) <= MAX_PDF_BYTES else None
    url = (resource.file_url or '').strip()
    local_data = _local_media_bytes(url)
    if local_data is not None:
        return local_data
    for _ in range(4):
        try:
            url = validate_resource_file_url(url)
        except ValidationError:
            return None
        with requests.get(url, timeout=(10, 45), stream=True, allow_redirects=False) as response:
            if response.is_redirect or response.is_permanent_redirect:
                location = response.headers.get('Location', '').strip()
                if not location:
                    return None
                url = urljoin(url, location)
                continue
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '').lower()
            if content_type and 'pdf' not in content_type and 'octet-stream' not in content_type:
                return None
            data = bytearray()
            for chunk in response.iter_content(65536):
                if not chunk:
                    continue
                data.extend(chunk)
                if len(data) > MAX_PDF_BYTES:
                    return None
            return bytes(data)
    return None


def _document_context(resource):
    cache_key = f'pdf-ai-context:{resource.id}'
    cached = cache.get(cache_key)
    if isinstance(cached, str) and cached:
        return cached, None
    data = _resource_pdf_bytes(resource)
    if not data:
        return '', None
    file_name = os.path.basename(urlparse(resource.file_url or '').path) or f'{resource.id}.pdf'
    if not file_name.lower().endswith('.pdf'):
        file_name = f'{file_name}.pdf'
    text = extract_text_from_bytes(file_name, data) or ''
    if text:
        text = text[:MAX_CONTEXT_CHARS]
        cache.set(cache_key, text, 86400)
    return text, data


@api_view(['POST'])
@authentication_classes([AuthTokenAuthentication])
@throttle_classes([ArenaChatRateThrottle])
def resource_pdf_assistant(request, resource_id):
    user, error = _user_or_error(request)
    if error:
        return error

    user = check_and_reset_monthly_credits(user)
    total_credits = user.free_credits + user.ai_credits
    if total_credits <= 0:
        return Response({
            'error': 'Neby Credits exhausted. You get 10 free credits every month, or you can convert 2 NEBians points to 1 credit.',
            'code': 'CREDITS_EXHAUSTED',
            'free_credits': 0,
            'ai_credits': 0,
            'nebians_points': user.nebians_points,
            'whatsapp_contact': WHATSAPP_CONTACT
        }, status=status.HTTP_402_PAYMENT_REQUIRED)

    prompt = str(request.data.get('prompt') or '').strip()
    if not prompt:
        return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)
    if len(prompt) > 4000:
        return Response({'error': 'Prompt is too long'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        resource = Resource.objects.get(pk=resource_id, approval_status='approved')
    except Resource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)

    history = request.data.get('history') or []
    history_text = '\n'.join(
        f"{str(item.get('role') or 'user')}: {str(item.get('content') or '')[:1600]}"
        for item in history[-8:]
        if isinstance(item, dict)
    )
    context, pdf_bytes = _document_context(resource)
    system_prompt = (
        'You are NEBians PDF Tutor. Answer only from the supplied document and resource metadata. '
        'When the document does not contain the answer, say that clearly. Keep answers accurate, structured, and student-friendly.'
    )
    metadata = (
        f"Title: {resource.title}\nSubject: {resource.subject}\nGrade: {resource.grade_level}\n"
        f"Description: {resource.description[:1200]}"
    )
    conversation = f"\nPrevious conversation:\n{history_text}" if history_text else ''
    client = QwenClient()

    if context:
        message = (
            f"{metadata}{conversation}\n\nQuestion: {prompt}\n\n"
            f"Document content:\n{context}\nEnd of document."
        )
        answer, ai_error = client.simple_chat(message=message, system_prompt=system_prompt)
    elif pdf_bytes:
        prepared = client.prepare_file_for_qwen(f'{resource.id}.pdf', pdf_bytes)
        if not prepared:
            return Response({'error': 'The PDF could not be prepared for AI'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        answer, ai_error = client.send_doc_task(
            prepared=prepared,
            file_prompt=f"{metadata}{conversation}\n\nQuestion: {prompt}",
            text_prompt=f"{metadata}{conversation}\n\nQuestion: {prompt}",
            system_prompt=system_prompt,
        )
    else:
        return Response({'error': 'The PDF is unavailable'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if not answer:
        return Response({'error': ai_error or 'AI could not answer right now'}, status=status.HTTP_502_BAD_GATEWAY)

    # Deduct 1 Neby credit on successful AI response
    if user.free_credits > 0:
        user.free_credits -= 1
        user.save(update_fields=['free_credits'])
    else:
        user.ai_credits = max(0, user.ai_credits - 1)
        user.save(update_fields=['ai_credits'])

    NebyCreditTransaction.objects.create(
        id=str(uuid.uuid4()),
        user=user,
        transaction_type='ai_usage',
        amount=-1,
        description=f"PDF AI query on: {resource.title[:50]}",
        created_at=int(time.time() * 1000)
    )

    remaining_credits = user.free_credits + user.ai_credits
    return Response({
        'answer': answer,
        'resourceId': resource.id,
        'title': resource.title,
        'remaining_credits': remaining_credits
    })
