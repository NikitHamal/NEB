"""Cosmetics store views — store page, purchase, and equip endpoints."""
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from api import store_services
from api.models import User
from .view_helpers import _ctx, _get_user_id, _rate_limit


def store(request):
    user_obj = None
    user_id = _get_user_id(request)
    if user_id:
        user_obj = User.objects.filter(pk=user_id).first()
    data = store_services.serialize_store(user_obj)
    return render(request, 'web/store.html', _ctx(
        request, store_data=data, balance=data['balance'], score=data['score'],
    ))


@require_POST
def ajax_store_purchase(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    if _rate_limit(request, 'store_purchase', 20, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    key = (data.get('key') or '').strip()
    if not key:
        return JsonResponse({'error': 'key required'}, status=400)
    try:
        result = store_services.claim_or_purchase(user, key)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse(result)


@require_POST
def ajax_store_equip(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    if _rate_limit(request, 'store_equip', 30, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        if data.get('unequip'):
            kind = (data.get('kind') or '').strip()
            result = store_services.unequip_item(user, kind)
            if kind == 'theme':
                request.session['app_theme'] = ''
        else:
            key = (data.get('key') or '').strip()
            if not key:
                return JsonResponse({'error': 'key required'}, status=400)
            result = store_services.equip_item(user, key)
            if result.get('kind') == 'theme':
                request.session['app_theme'] = key
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse(result)
