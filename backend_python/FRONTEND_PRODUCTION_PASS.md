# NEBians frontend production pass

## Scope
- Focused on the Django-rendered website and admin-facing templates included in this archive.
- Did not modify backend security, authentication, data models, migrations, or API behavior.

## Design-system work
- Added app-level design tokens for spacing, app layout, semantic states, scrims, and subtle brand surfaces.
- Consolidated global layout primitives: app main/footer, page shells, stacks, clusters, avatars, alert surfaces, compact buttons, inline search forms, resource list cards, and error pages.
- Moved duplicated 404/500 page styles into the shared stylesheet.
- Normalized cards, icon sizing, interactive card states, footer, topbar blur/surface treatment, alerts, and small button patterns.

## Deduplication and modularization
- Reused global CSS for repeated follow-button variants instead of maintaining duplicate definitions.
- Replaced repeated inline layout styles across base, reader, search, library, home, edit profile, forum categories, and admin views with shared utility/component classes.
- Centralized category-grid page styling in the shared CSS rather than keeping page-local CSS.
- Reduced duplicated avatar, helper text, soft alert, progress bar, search form, and resource-list styling patterns.

## Security observations only
- The archive contains a `.env` file and `db.sqlite3`. I left them unchanged because the requested scope was visual consistency and code deduplication only. For public sharing or deployment handoff, avoid distributing secrets or production data in archives.
- Existing auth/security/backend logic was not altered.
