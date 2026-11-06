# Admin panel (M3 Expressive)

Everything under `/admin/`. Shell: `templates/admin_panel/base.html`. Pages extend it and put their body in `{% block content %}`.

## Files

```
web/templates/admin_panel/base.html        drawer, top bar, confirm + jump dialogs, snackbar host
web/templates/admin_panel/_admin_nav.html  loops the groups from admin_extras.admin_nav
web/templatetags/admin_extras.py           NAV_GROUPS (the one nav list) + queue badge counts
web/static/web/js/admin-shell.js           drawer, theme, snackbar, adminConfirm, Ctrl+K palette
web/static/web/css/admin/00-tokens.css     --admin-* tokens (radii, springs, status colours)
web/static/web/css/admin/05-shell.css      drawer, top bar, page header, dialogs, view transitions
web/static/web/css/admin/07-expressive.css cards, tabs, tables, search, pagination, fields (loads last)
web/test_admin_shell.py                    smoke-loads every nav page + style guards
```

## Adding a page

1. Add a row to `NAV_GROUPS` in `admin_extras.py`: `(active_page key, url name, icon, label, badge key or None)`.
   The drawer and the Ctrl+K palette both read it. Do not hand-write nav links.
2. Pass `'active_page': '<key>'` in the view context.
3. Extend `admin_panel/base.html`. Page header markup: `.admin-page-header > .admin-page-header-row > h1 + .admin-page-actions`.
   No eyebrow and no tagline under the title; if the page needs one to make sense, fix the layout.

## Rules (enforced by `web/test_admin_shell.py`)

- No `box-shadow` other than `none`. Depth is tonal: `--admin-card` on `--md-surface`.
- No fully square `border-radius`. Every hover, press and focus fill is a finite radius
  (pills use `--admin-radius-pill`). The state layer is a `::before` with `border-radius: inherit`.
  Table row hover is drawn on the cells with rounded first/last cell corners.
- No `confirm()` or `alert()`. Use `adminConfirm({title, message, confirmLabel, tone})` (returns a Promise<boolean>)
  or `showSnackbar(msg)`. Declaratively: `data-action="confirm-delete"` on a form, `data-action="confirm-submit"` on a button,
  with `data-confirm-title`, `data-confirm-msg`, `data-confirm-label`, `data-confirm-tone="primary"` to soften.
- Colours are role pairs (`--md-secondary-container` with `--md-on-secondary-container`). Never set a fill without its label colour.

## Behaviour worth knowing

- One drawer element: a fixed column above 900px, a modal sheet below (`inert` while closed, focus returned on close).
- Ctrl/Cmd+K or `/` opens the jump palette; arrows move, Enter opens, Esc closes.
- Theme toggle uses a circular View Transition from the button; falls back to an instant swap
  (`.admin-theme-swap` suppresses transitions) without the API or with reduced motion.
- Page-to-page changes use cross-document view transitions (`@view-transition`); drawer and top bar keep their own
  transition names so they stay put while content cross-fades. Disabled under `prefers-reduced-motion`.
- Analytics: see `docs/ANALYTICS.md`. It sits inside the same `.admin-shell` gutter; its sticky toolbar bleeds to the gutter.

## Verify

```
cd backend_python
DB_ENGINE=sqlite SECRET_KEY=x DEBUG=1 python manage.py test web.test_admin_shell api.test_admin_analytics
python ../tools/css/bundle.py --check
```
