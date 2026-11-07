"""Member-facing push endpoints (the app and the web settings page)."""
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response

from . import push_engine
from .models import FCMToken, User
from .throttles import WriteActionRateThrottle
from .view_helpers import _require_user


@api_view(['GET', 'PATCH', 'POST'])
@throttle_classes([WriteActionRateThrottle])
def notification_prefs(request):
    """GET /api/me/notification-prefs/ and PATCH {"new_resources": bool}.

    `new_resources` is the library autopilot: a message when a resource lands for your class and
    subjects. On unless the member switches it off."""
    user, err = _require_user(request)
    if err:
        return err
    if request.method in ('PATCH', 'POST'):
        data = request.data
        if 'new_resources' in data or 'newResources' in data:
            raw = data.get('new_resources', data.get('newResources'))
            value = raw if isinstance(raw, bool) else str(raw).strip().lower() in ('1', 'true', 'yes', 'on')
            User.objects.filter(pk=user.id).update(notify_new_resources=value)
            user.notify_new_resources = value
    return Response({
        'newResources': bool(user.notify_new_resources),
        'devices': FCMToken.objects.filter(user_id=user.id).count(),
        'hasSubjects': bool((user.subjects or '').strip() and (user.class_level or '').strip()),
    })


@api_view(['POST'])
@throttle_classes([WriteActionRateThrottle])
def push_opened(request):
    """POST /api/push/opened/ {"notification_id"?, "campaign_id"?}: the app reports a tap on a push."""
    user, err = _require_user(request)
    if err:
        return err
    ok = push_engine.record_push_open(
        user, campaign_id=str(request.data.get('campaign_id') or '')[:36],
        notification_id=str(request.data.get('notification_id') or '')[:36])
    return Response({'recorded': ok})
