"""The live site theme for the apps: which festival is on and how to dress for it.

The web app gets its theme through a template context processor; the Android app asks here.
One small, cacheable payload: colours for light and dark (Material primary roles), the motif,
the greeting and the home card. When no festive theme is live, ``festive`` is false and the app
stays in its house style.
"""
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from web import site_themes

_ROLE_NAMES = ('primary', 'onPrimary', 'primaryContainer', 'onPrimaryContainer')


def payload() -> dict:
    t = site_themes.current()
    app = t.get('app') if t.get('show_in_app') else None
    data = {'key': t['key'], 'name': t['name'], 'festive': bool(t.get('festive') and app)}
    neby = t.get('neby') or {}
    data['neby'] = {'look': neby.get('look', 'classic'), 'ambient': neby.get('ambient', True), 'reactions': neby.get('reactions', True),
                    'greet': neby.get('greet')}
    if data['festive']:
        data.update({
            'light': dict(zip(_ROLE_NAMES, app['light'])),
            'dark': dict(zip(_ROLE_NAMES, app['dark'])),
            'motif': app['motif'],
            'greeting': t.get('greeting'),
            'card': {'message': app['message'], 'cta': {'label': app['cta'][0], 'url': app['cta'][1]}},
        })
    return data


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def site_theme(request):
    response = Response(payload())
    response['Cache-Control'] = 'public, max-age=300'
    return response
