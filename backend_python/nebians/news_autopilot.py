"""Starts the blog's auto-import in the background when it is due.

The check is one float comparison per request (services/news_sync.py); the work
itself runs on a daemon thread, so no visitor ever waits for a feed.
"""
from services.news_sync import maybe_autosync

_SKIP = ('/static/', '/media/', '/api/', '/ws/', '/health')


class NewsAutopilotMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET' and not request.path.startswith(_SKIP):
            try:
                maybe_autosync()
            except Exception:
                pass
        return self.get_response(request)
