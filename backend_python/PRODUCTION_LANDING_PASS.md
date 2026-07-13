# NEBians Web Landing Production Pass

## Scope

The public home page was rebuilt as an original NEBians landing experience inspired by the supplied visual direction without reproducing its branding or copy. The page now presents NEBians as an active learning platform rather than a passive resource directory.

## Experience

- Responsive sky-and-hills hero with NEBians-specific messaging
- Guest and authenticated calls to action
- Live platform proof points from approved resources, verified learners, discussions, and replies
- Product workspace preview for Library, Study Lab, Neby AI, and Community
- Three product value cards
- Refined news, resource, and discussion sections
- Dark-theme treatment, reduced-motion support, keyboard focus states, and mobile layouts
- Updated title, Open Graph copy, and social metadata

## Architecture

The page is split into focused template and stylesheet modules. Existing forum actions, bookmarks, WebSocket updates, navigation, and backend data flows remain intact.

## Changed Files

- `web/views_public.py`
- `web/view_helpers.py`
- `web/templates/web/home.html`
- `web/templates/web/_home_hero.html`
- `web/templates/web/_home_feature_strip.html`
- `web/templates/web/_home_news.html`
- `web/templates/web/_home_resources.html`
- `web/static/web/css/pages/web-home.css`
- `web/static/web/css/pages/home/01-hero.css`
- `web/static/web/css/pages/home/02-content.css`
- `web/static/web/css/pages/home/03-responsive.css`

## Verification

- `python manage.py check`: passed
- Home route render: HTTP 200
- New static stylesheet routes: HTTP 200
- Python compilation: passed
- CSS syntax parsing: passed with zero parse errors

## Deployment

Use `scratch/deploy.ps1` from the backend project. It packages the deployment, installs requirements, runs migrations and collectstatic, copies static assets to the public static location, and restarts the LiteSpeed application.
