# NEBians Project Structure

```text
api/
  view_helpers.py       Shared API helpers.
  views_auth.py         Auth endpoints.
  views_users.py        User/profile/follow/photo endpoints.
  views_resources.py    Resource and resource-request endpoints.
  views_forum.py        Post/reply/forum API endpoints.
  views_misc.py         Search/bookmark/report/notification/FCM endpoints.
  views.py              Backward-compatible API view exports.

web/
  view_helpers.py       Shared web view helpers and serializers.
  views_public.py       Public pages and SEO endpoints.
  views_forum.py        Forum pages.
  views_profile.py      Profile pages.
  views_auth.py         Login/OAuth/email/password pages.
  views_ajax.py         AJAX endpoints.
  views_notifications.py Notification pages/endpoints.
  views_admin.py        Custom admin pages.
  views_arena.py        Neby Arena AJAX endpoints.
  views.py              Backward-compatible web view exports.

web/static/web/css/pages/
  Page-level CSS extracted from large templates.
```

## Compatibility rule

Keep URL configs importing `from . import views`. The compatibility modules are intentionally small and re-export the focused modules. This prevents breaking existing routes while allowing future work to happen in focused files.

## Suggested future cleanup

The next safe refactor pass should target template JavaScript. Many scripts still contain Django template variables, so extract them only after moving dynamic values into JSON script tags or `data-*` attributes.
