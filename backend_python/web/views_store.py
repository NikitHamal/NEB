"""Cosmetics store views — browse, purchase, and equip items."""
from .view_helpers import *  # noqa: F401,F403
from api import store_service


def store(request):
    user_id = _get_user_id(request)
    viewer = None
    if user_id:
        try:
            viewer = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            viewer = None
    state = store_service.get_store_state(viewer)
    return render(request, 'web/store.html', _ctx(request,
        store_categories=state['categories'],
        owned_ids=state['owned_ids'],
        equipped=state['equipped'],
        points_balance=state['points_balance'],
    ))


@require_POST
def ajax_store_purchase(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in.'}, status=401)
    if _rate_limit(request, 'store_purchase', 30, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in.'}, status=401)
    try:
        data = json.loads(request.body)
        item_id = str(data.get('item_id') or '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    if not item_id:
        return JsonResponse({'error': 'Item required'}, status=400)
    ok, result = store_service.purchase_item(user, item_id)
    if not ok:
        return JsonResponse({'error': result}, status=400)
    return JsonResponse({'ok': True, 'item_id': item_id, 'points_balance': result['points_balance']})


@require_POST
def ajax_store_equip(request):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in.'}, status=401)
    if _rate_limit(request, 'store_equip', 30, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Please log in.'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    item_id = str(data.get('item_id') or '').strip()
    item_type = str(data.get('item_type') or '').strip()
    if item_id:
        ok, result = store_service.equip_item(user, item_id)
    elif item_type:
        ok, result = store_service.unequip_item(user, item_type)
    else:
        return JsonResponse({'error': 'Item required'}, status=400)
    if not ok:
        status = 404 if result in ('Unknown item', 'Item not owned') else 400
        return JsonResponse({'error': result}, status=status)
    request.session['app_theme'] = result.get('theme', '')
    return JsonResponse({'ok': True, 'equipped': result})
