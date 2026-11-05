import os

from django.conf import settings

from api.models import Resource
from api.resource_form import error_text
from api.security import (
    clean_source_url,
    save_resource_thumbnail_upload,
    validate_and_save_resource_file,
    validate_resource_file_url,
)
from api.utils import now_ms, uuid_str
from api.view_helpers import parse_paid_fields

def apply_price(resource, post):
    resource.is_paid, resource.price = parse_paid_fields(post)


def clean_url_or_error(clean, raw, errors):
    try:
        return clean(raw)
    except Exception as exc:
        errors.append(error_text(exc))
        return ''


def clean_source_url_or_error(post, errors):
    return clean_url_or_error(clean_source_url, post.get('source_url', ''), errors)


def clean_file_url_or_error(raw, errors):
    return clean_url_or_error(validate_resource_file_url, raw, errors)


def clean_thumbnail_or_error(request, errors):
    thumbnail_file = request.FILES.get('thumbnail')
    if thumbnail_file:
        return clean_url_or_error(lambda f: save_resource_thumbnail_upload(request, f), thumbnail_file, errors)
    raw = request.POST.get('thumbnail_url', '').strip()
    if not raw:
        return ''
    try:
        return validate_resource_file_url(raw)
    except Exception:
        errors.append('Invalid thumbnail URL.')
        return ''


def save_uploaded_files(request, uploaded_files, errors):
    saved = []
    for f in uploaded_files:
        path, size, err_resp = validate_and_save_resource_file(request, f)
        if err_resp:
            errors.append(f"{f.name}: {err_resp['error']}")
        else:
            saved.append({'path': path or '', 'size': size, 'name': f.name})
    return saved


def replace_file(request, resource, uploaded_file):
    """Swap the stored file; returns the reason it was refused, or '' when it was replaced."""
    path, size, err_resp = validate_and_save_resource_file(request, uploaded_file)
    if err_resp:
        return f"{uploaded_file.name}: {err_resp['error']}"
    if path:
        resource.file = path
        resource.file_url = request.build_absolute_uri(settings.MEDIA_URL + path)
        resource.file_size = size
    return ''


FORM_FIELDS = (
    'title', 'description', 'subject', 'grade_level', 'type', 'exam_type', 'faculty', 'program', 'year',
    'school', 'pradesh', 'district', 'tags', 'author_name', 'source_label', 'source_url', 'file_url',
    'thumbnail_url',
)


def resource_form_data(resource):
    """What the composer shows for an existing resource: the same names the form posts."""
    data = {name: getattr(resource, name, '') or '' for name in FORM_FIELDS}
    data['is_paid'] = bool(resource.is_paid)
    data['price'] = resource.price if resource.is_paid else ''
    return data


def resource_current(resource, serialized):
    """The file and cover the composer's tray starts with."""
    path = str(resource.file or '')
    url = resource.file_url or ''
    current = {'file': None, 'cover': serialized.get('thumbnailUrl') or ''}
    if path:
        kind = serialized.get('mediaType') or 'file'
        current['file'] = {'name': os.path.basename(path), 'url': url, 'size': resource.file_size or 0,
                           'kind': kind if kind in ('video', 'audio', 'image') else 'file'}
    elif url:
        current['file'] = {'name': url.split('//')[-1].split('/')[0] or url, 'url': url, 'size': 0, 'kind': 'link'}
    return current


def create_resources(request, fields, saved_files, *, file_url='', file_size=0, **extra):
    """One Resource per saved file (siblings share an upload group, the first is the lead), or one for the URL."""
    entries = [
        (sf['path'] or None, request.build_absolute_uri(settings.MEDIA_URL + sf['path']), sf['size'], sf['name'])
        for sf in saved_files
    ] or [(None, file_url, file_size, '')]
    group_id = uuid_str() if len(entries) > 1 else ''
    created = []
    for idx, (path, url, size, name) in enumerate(entries):
        title = fields['title'] if idx == 0 else f"{fields['title']} - {os.path.splitext(name)[0]}"
        resource = Resource(
            **{**fields, 'title': title},
            id=uuid_str(),
            file=path,
            file_url=url,
            file_size=size,
            added_at=now_ms() + idx,
            upload_group_id=group_id,
            is_lead=idx == 0,
            **extra,
        )
        resource.save()
        created.append(resource)
    return created
