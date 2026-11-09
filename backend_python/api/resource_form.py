from django.conf import settings
from django.core.files.storage import default_storage

from .security import (
    clean_source_url,
    save_resource_thumbnail_upload,
    validate_resource_file_url,
)

LISTING_FIELDS = (
    'title', 'description', 'subject', 'grade_level', 'faculty', 'program', 'year',
    'exam_type', 'pradesh', 'district', 'school', 'tags', 'author_name', 'source_label',
)
REQUEST_FIELDS = (
    'title', 'description', 'subject', 'grade_level', 'faculty', 'program', 'year',
    'exam_type', 'pradesh', 'district', 'tags',
)


class InvalidInput(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def error_text(exc):
    return ' '.join(getattr(exc, 'messages', [str(exc)]))


def checked(fn, *args):
    try:
        return fn(*args)
    except Exception as exc:
        raise InvalidInput(error_text(exc))


def read_listing_fields(data):
    fields = {name: data.get(name, '').strip() for name in LISTING_FIELDS}
    fields['type'] = data.get('type', 'PDF').strip() or 'PDF'
    from .education_catalog import canonical_level
    fields['grade_level'] = canonical_level(fields['grade_level'])
    return fields


def read_request_fields(data):
    return {name: data.get(name, '').strip() for name in REQUEST_FIELDS}


def read_source_url(data):
    return checked(clean_source_url, data.get('source_url', ''))


def read_file_url(raw):
    return checked(validate_resource_file_url, raw)


def read_thumbnail(request, data):
    """The cover from an upload, else a pasted URL ('' when cleared); None when the request says nothing about it."""
    thumbnail_file = request.FILES.get('thumbnail')
    if thumbnail_file:
        return checked(save_resource_thumbnail_upload, request, thumbnail_file)
    if 'thumbnail_url' not in data:
        return None
    raw = (data.get('thumbnail_url') or '').strip()
    return read_file_url(raw) if raw else ''


def media_url(request, path):
    return request.build_absolute_uri(settings.MEDIA_URL + path) if path else ''


def discard_saved_files(saved_files):
    for saved in saved_files:
        if saved['path']:
            try:
                default_storage.delete(saved['path'])
            except Exception:
                pass
