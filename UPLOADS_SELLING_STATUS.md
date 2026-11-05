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

## Next (in order)

1. Open storefronts to every signed-in member (today: teacher / institution / admin only) and add a Sell entry point.
2. Course delivery (recorded / live / hybrid) and how a student enrols (buy here or contact the teacher).
3. Marketplace + course page polish for the teacher case.

## Verify

```bash
cd backend_python
export DEBUG=True DB_ENGINE=sqlite SECRET_KEY=x ALLOWED_HOSTS_GLOB=testserver,localhost,127.0.0.1
python3 manage.py test web api.tests_marketplace
```
