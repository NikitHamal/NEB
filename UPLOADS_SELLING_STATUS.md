# Uploads, resource editing and open selling — status

The one status doc for this revamp. Read it first, extend it, do not start a second one.

**Brief.** Revamp upload and edit-resource the way forum posts and comments are edited (one surface, tray, sheets,
motion), and make selling open: anyone sells paid notes, resources and courses; teachers bring classes and
tutorial videos (CEE, IOE prep and others) and students either buy on the site or reach the teacher.

## Done

| # | What | Where |
| --- | --- | --- |
| 1 | **Resource composer**: upload and edit are one component. `.fe` surface, title, description, six answer chips (subject, level, type, tags, price, more), `.na-row` tray, drop anywhere, per-file progress, image compression, links and credit sheet, delete sheet (edit). One multipart POST, the contract the views always had. | `web/templates/web/components/_resource_composer.html`, `web/static/web/js/resource-composer.js`, `web/static/web/css/pages/resource-composer.css`, wrappers `upload.html`, `edit_resource.html` |
| 2 | `components/_choice_sheet.html` replaces four copy-pasted NebChoice sheets. | `web/templates/web/components/` |
| 3 | `edit_resource` validates like upload (title, subject, price, links, file) and answers JSON to the composer; `ajax_resource_delete` (owner only, refused once a buyer has paid). | `web/views_public.py`, `web/resource_upload.py` (`resource_form_data`, `resource_current`, `replace_file` now reports), `web/urls.py` |
| 4 | Fixed: the old upload page filled Source URL with the Source label; PNG compression turned transparency black. | composer partial / JS |

Removed: `css/pages/web-edit-resource.css` (unreferenced). `pages/upload.css` stays: `study_lab.html` still links it.

| 5 | **Open selling**: `can_have_storefront` is every member in good standing (banned or locked accounts excluded). Teachers, institutes and admins differ only in `allowed_kinds` (page kind), not in the right to sell. Paid resources already worked for everyone through the composer's price chip. | `api/creator_pages_access.py`, `api/tests_marketplace.py` |
| 6 | **Course delivery and enrolment**: `CreatorCourse.delivery` (recorded / live / hybrid / inperson), `enroll_mode` (`buy` = QR checkout, `contact` = reach the teacher), `contact_label`, `contact_url` (phone becomes `tel:`, address `mailto:`, anything else must be http(s)). A contact course needs no price, shows a contact button instead of checkout, and refuses web purchase posts. Studio form, course page and course card show it. Migration 0162. | `api/models.py`, `api/creator_pages.py` (`clean_contact_link`), `api/creator_pages_payloads.py`, `web/views_marketplace.py`, `marketplace_studio.html`, `marketplace_studio_forms.js`, `marketplace_course.html`, `_marketplace_course_card.html`, `_marketplace_delivery.html` |

The whole marketplace is still behind `MARKETPLACE_ENABLED` (`nebians/features.py`, off by default). Turn it on when the first
teacher is ready; nothing else needs to change.

## Next

1. Android parity: app studio course form needs `delivery`, `enroll_mode`, `contact_*` (API payload already carries them).
2. Lesson list with free-preview videos for tutorial courses (today a course attaches library resources, which can be videos).

## Verify

```bash
cd backend_python
export DEBUG=True DB_ENGINE=sqlite SECRET_KEY=x ALLOWED_HOSTS_GLOB=testserver,localhost,127.0.0.1
python3 manage.py test web api.tests_marketplace
```
