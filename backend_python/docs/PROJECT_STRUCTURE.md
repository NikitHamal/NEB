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

## Frontend static modules added in latest pass

```text
web/static/web/css/app/              Global app modules imported by app.css.
web/static/web/css/material3/        Material 3 design-system modules imported by material3.css.
web/static/web/css/admin/            Shared admin CSS modules imported by admin.css.
web/static/web/css/pages/profile/    Profile page CSS modules imported by pages/profile.css.
web/static/web/css/pages/subject-page/ Subject page CSS modules imported by pages/subject-page.css.
web/static/web/js/profile-photo-upload.js Profile photo modal upload picker/upload fallback.
web/templates/web/profile/_photo_modal.html Profile photo modal partial.
web/templates/web/profile/_follow_modal.html Followers/following modal partial.
```
