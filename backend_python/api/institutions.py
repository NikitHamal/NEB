"""Institution catalogue: seeding, search, people counts, claims and verification.

One module for the web pages, the admin review pages and `GET /api/institutions/`.
"""
import gzip
import json
import re
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Case, Count, IntegerField, Q, Value, When
from django.db.models.functions import Coalesce

from .models import User
from .models_institutions import (
    DOC_TYPE_LABELS, KIND_LABELS, Institution, InstitutionDocument, InstitutionVerification, search_key,
)
from .utils import now_ms

CATALOG_PATH = Path(__file__).resolve().parent / 'data' / 'institutions.json.gz'
MAX_DOCS = 6
MAX_DOC_BYTES = 8 * 1024 * 1024
DOC_SIGNATURES = {
    '.pdf': (b'%PDF',),
    '.png': (b'\x89PNG',),
    '.jpg': (b'\xff\xd8\xff',),
    '.jpeg': (b'\xff\xd8\xff',),
    '.webp': (b'RIFF',),
}
DOC_CONTENT_TYPES = {'.pdf': 'application/pdf', '.png': 'image/png', '.jpg': 'image/jpeg',
                     '.jpeg': 'image/jpeg', '.webp': 'image/webp'}


def visible_people():
    return User.objects.filter(is_banned=False, is_bot=False)


def import_catalog(path=None, batch=2000):
    path = Path(path or CATALOG_PATH)
    if not path.exists():
        return 0, 0
    with gzip.open(path, 'rt', encoding='utf-8') as fh:
        data = json.load(fh)
    cols = data['cols']
    existing = set(Institution.objects.values_list('slug', flat=True))
    stamp = now_ms()
    fresh = []
    for row in data['rows']:
        rec = dict(zip(cols, row))
        if rec['slug'] in existing:
            continue
        inst = Institution(
            slug=rec['slug'], name=rec['name'], name_ne=rec['name_ne'], kind=rec['kind'], district=rec['district'],
            province=rec['province'], place=rec['place'], website=rec['website'], phone=rec['phone'],
            lat=rec['lat'], lon=rec['lon'], est=rec['est'], source=rec['source'], created_at=stamp,
            search_text=search_key(rec['name'], rec['name_ne'], rec['district'], rec['place']),
        )
        fresh.append(inst)
    for i in range(0, len(fresh), batch):
        Institution.objects.bulk_create(fresh[i:i + batch], ignore_conflicts=True)
    return len(fresh), len(existing)


def unique_slug(base):
    base = re.sub(r'[^a-z0-9]+', '-', (base or 'institution').lower()).strip('-')[:70] or 'institution'
    slug, n = base, 2
    while Institution.objects.filter(slug=slug).exists():
        slug = '%s-%d' % (base, n)
        n += 1
    return slug


def institution_for_account(user, create=False):
    inst = Institution.objects.filter(claimed_by=user).first()
    if inst or not create:
        return inst
    name = (user.school or user.display_name or user.username or '').strip()
    inst = Institution.objects.create(
        slug=unique_slug(name or user.username), name=name or user.username, kind=kind_for_type(user.institution_type),
        district=user.district or '', province=user.pradesh or '', source='account', claimed_by=user,
        verified=bool(user.institution_verified), verified_at=now_ms() if user.institution_verified else 0,
        created_at=now_ms(),
    )
    link_people(inst)
    return inst


def kind_for_type(value):
    return {'school': 'school', 'college': 'college', 'academy': 'institute'}.get(value or '', 'institute')


def link_people(inst):
    if not inst.claimed_by_id:
        return 0
    return visible_people().filter(school_slug=inst.slug).exclude(pk=inst.claimed_by_id).update(
        school=inst.name, school_username=inst.claimed_by.username)


def people_qs(inst):
    qs = visible_people().filter(school_slug=inst.slug)
    if inst.claimed_by_id:
        qs = qs.exclude(pk=inst.claimed_by_id)
    return qs


def people_counts(inst):
    rows = people_qs(inst).values('role').annotate(n=Count('id'))
    by_role = {r['role']: r['n'] for r in rows}
    total = sum(by_role.values())
    return {'total': total, 'students': by_role.get('student', 0) + by_role.get('explorer', 0),
            'teachers': by_role.get('teacher', 0)}


def people_list(inst, limit=24, offset=0, role=''):
    qs = people_qs(inst).filter(is_locked=False)
    if role == 'teacher':
        qs = qs.filter(role='teacher')
    elif role == 'student':
        qs = qs.exclude(role='teacher')
    return list(qs.order_by('-contribution_score', 'username')[offset:offset + limit])


def counts_for(slugs):
    if not slugs:
        return {}
    rows = visible_people().filter(school_slug__in=slugs).values('school_slug').annotate(n=Count('id'))
    return {r['school_slug']: r['n'] for r in rows}


def clean_query(q):
    return re.sub(r'\s+', ' ', (q or '').strip())[:80]


def search(q='', kind='', district='', limit=30, offset=0, verified_only=False, unverified_only=False):
    qs = Institution.objects.all()
    for token in search_key(clean_query(q)).split():
        qs = qs.filter(search_text__contains=token)
    if kind in KIND_LABELS:
        qs = qs.filter(kind=kind)
    if district:
        qs = qs.filter(district__iexact=district)
    if verified_only:
        qs = qs.filter(verified=True)
    elif unverified_only:
        qs = qs.filter(verified=False)
    # Claimed first, then the fuller the portfolio the higher, then the ones with a website.
    qs = qs.annotate(
        has_site=Case(When(~Q(website=''), then=Value(0)), default=Value(1), output_field=IntegerField()),
        fill=Coalesce('profile__completeness', Value(0)),
    ).order_by('-verified', '-fill', 'has_site', 'name')
    total = qs.count()
    rows = list(qs.select_related('claimed_by', 'profile')[offset:offset + limit])
    counts = counts_for([r.slug for r in rows])
    return rows, total, counts


def _facts(inst):
    """The few portfolio facts a list row shows (none for an unclaimed institution)."""
    row = getattr(inst, 'profile', None)
    if row is None:
        return {'completeness': 0}
    d = row.data or {}
    return {'completeness': row.completeness, 'levels': d.get('levels', []), 'feeMin': d.get('feeMin'),
            'feeMax': d.get('feeMax'), 'teachers': d.get('teachers'), 'studentsTotal': d.get('students'),
            'admissionOpen': bool(d.get('admissionOpen')), 'facilities': (d.get('facilities') or [])[:6]}


def serialize(inst, count=0):
    return {**_facts(inst),
        'slug': inst.slug, 'name': inst.name, 'nameNe': inst.name_ne, 'kind': inst.kind, 'kindLabel': inst.kind_label,
        'district': inst.district, 'place': inst.place, 'location': inst.location, 'website': inst.website,
        'verified': inst.verified, 'username': inst.claimed_by.username if inst.claimed_by_id else '',
        'students': count, 'est': inst.est, 'photoUrl': inst.logo_url,
        'claimable': is_claimable(inst),
    }


def is_claimable(inst, viewer=None):
    """True only while nobody holds the institution. A claimed one, or one the viewer already owns, is not."""
    if inst.verified or inst.claimed_by_id:
        return False
    if viewer is not None and getattr(viewer, 'role', '') == 'institution':
        return not Institution.objects.filter(claimed_by=viewer, verified=True).exists()
    return True


def owned_slug(user):
    """Slug of the verified institution this account owns, or ''."""
    if user is None or getattr(user, 'role', '') != 'institution':
        return ''
    return Institution.objects.filter(claimed_by=user, verified=True).values_list('slug', flat=True).first() or ''


def select_school(user, slug='', custom_name=''):
    if slug:
        inst = Institution.objects.select_related('claimed_by').filter(slug=slug).first()
        if inst:
            user.school = inst.name
            user.school_slug = inst.slug
            user.school_username = inst.claimed_by.username if inst.claimed_by_id else ''
            return inst
    user.school = (custom_name or '').strip()[:200] or None
    user.school_slug = ''
    user.school_username = ''
    return None


def school_link(user_like):
    school = getattr(user_like, 'school', '') or ''
    slug = getattr(user_like, 'school_slug', '') or ''
    if not school:
        return None
    return {'name': school, 'slug': slug, 'url': ('/app/schools/%s/go/' % slug) if slug else ''}


def open_application(user):
    return InstitutionVerification.objects.filter(
        applicant=user, status__in=InstitutionVerification.OPEN_STATUSES).first()


def validate_application(post, files, institution=None):
    errors = {}

    def need(key, label, minimum=2, maximum=200):
        value = (post.get(key) or '').strip()
        if len(value) < minimum:
            errors[key] = '%s is required' % label
        return value[:maximum]

    data = {
        'name': need('name', 'Institution name', 3),
        'kind': (post.get('kind') or 'school').strip(),
        'district': (post.get('district') or '').strip()[:60],
        'address': need('address', 'Address', 3, 250),
        'website': (post.get('website') or '').strip()[:300],
        'registration_no': need('registration_no', 'Registration number', 2, 80),
        'contact_name': need('contact_name', 'Contact person', 3, 120),
        'contact_role': need('contact_role', 'Role at the institution', 2, 80),
        'contact_email': (post.get('contact_email') or '').strip()[:120],
        'contact_phone': (post.get('contact_phone') or '').strip()[:40],
        'message': (post.get('message') or '').strip()[:1500],
    }
    if data['kind'] not in KIND_LABELS:
        data['kind'] = 'school'
    try:
        validate_email(data['contact_email'])
    except ValidationError:
        errors['contact_email'] = 'Enter a valid email'
    if len(re.sub(r'\D', '', data['contact_phone'])) < 7:
        errors['contact_phone'] = 'Enter a phone number'
    if data['website']:
        if not re.match(r'^https?://', data['website'], re.I):
            data['website'] = 'https://' + data['website']
        if not re.match(r'^https?://[^\s/]+\.[^\s/]+', data['website']):
            errors['website'] = 'Enter a valid website'
    uploads = []
    types = post.getlist('doc_type') if hasattr(post, 'getlist') else []
    for i, f in enumerate(files.getlist('documents') if hasattr(files, 'getlist') else []):
        if not f or not f.name:
            continue
        ext = '.' + f.name.rsplit('.', 1)[-1].lower() if '.' in f.name else ''
        if ext not in DOC_SIGNATURES:
            errors['documents'] = 'Documents must be PDF, JPG, PNG or WebP'
            continue
        if f.size > MAX_DOC_BYTES:
            errors['documents'] = 'Each document must be under 8 MB'
            continue
        head = f.read(12)
        f.seek(0)
        if not any(head.startswith(sig) for sig in DOC_SIGNATURES[ext]):
            errors['documents'] = 'One file does not look like a %s' % ext[1:].upper()
            continue
        dtype = types[i] if i < len(types) and types[i] in DOC_TYPE_LABELS else 'other'
        uploads.append((f, dtype, ext))
    if not uploads and 'documents' not in errors:
        errors['documents'] = 'Attach at least one document'
    if len(uploads) > MAX_DOCS:
        errors['documents'] = 'Attach up to %d documents' % MAX_DOCS
    return data, uploads, errors


@transaction.atomic
def create_application(user, data, uploads, institution=None):
    app = InstitutionVerification.objects.create(
        applicant=user, institution=institution, created_at=now_ms(), **data)
    import secrets
    for f, dtype, ext in uploads:
        InstitutionDocument.objects.create(
            verification=app, doc_type=dtype, file=f, token=secrets.token_hex(12), original_name=f.name[:200],
            content_type=DOC_CONTENT_TYPES[ext], size=f.size, created_at=now_ms())
    return app


@transaction.atomic
def approve(app, reviewer, note=''):
    user = app.applicant
    inst = app.institution
    if inst is None:
        inst = Institution.objects.filter(claimed_by=user).first()
    if inst is None:
        inst = Institution(slug=unique_slug(app.name), source='application', created_at=now_ms())
    inst.name = inst.name or app.name
    if inst.source == 'application' or not inst.kind:
        inst.kind = app.kind
    inst.district = inst.district or app.district
    inst.website = inst.website or app.website
    inst.phone = inst.phone or app.contact_phone
    inst.email = app.contact_email
    inst.claimed_by = user
    inst.verified = True
    inst.verified_at = now_ms()
    inst.save()
    user.role = 'institution'
    user.institution_verified = True
    user.school = inst.name
    user.school_slug = ''
    user.school_username = ''
    user.save(update_fields=['role', 'institution_verified', 'school', 'school_slug', 'school_username'])
    link_people(inst)
    Institution.objects.filter(claimed_by=user).exclude(pk=inst.pk).update(claimed_by=None, verified=False)
    app.institution = inst
    app.status = InstitutionVerification.STATUS_APPROVED
    app.reviewer_note = note
    app.reviewed_by = reviewer
    app.reviewed_at = now_ms()
    app.save()
    InstitutionVerification.objects.filter(
        institution=inst, status__in=InstitutionVerification.OPEN_STATUSES).exclude(pk=app.pk).update(
        status=InstitutionVerification.STATUS_REJECTED, reviewed_at=now_ms(), reviewed_by=reviewer,
        reviewer_note='Another application for this institution was approved.')
    _notify(user, reviewer, '%s is now a verified institution on NEBians.' % inst.name)
    return inst


@transaction.atomic
def decide(app, reviewer, status, note=''):
    app.status = status
    app.reviewer_note = note[:1000]
    app.reviewed_by = reviewer
    app.reviewed_at = now_ms()
    app.save()
    texts = {
        InstitutionVerification.STATUS_REJECTED: 'Your verification request for %s was not approved.' % app.name,
        InstitutionVerification.STATUS_INFO: 'We need more information for the verification of %s.' % app.name,
    }
    if note and status in texts:
        texts[status] += ' ' + note[:200]
    _notify(app.applicant, reviewer, texts.get(status, ''))


@transaction.atomic
def revoke(inst):
    user = inst.claimed_by
    inst.verified = False
    inst.claimed_by = None
    inst.save()
    if user and not Institution.objects.filter(claimed_by=user, verified=True).exists():
        user.institution_verified = False
        user.save(update_fields=['institution_verified'])
    visible_people().filter(school_slug=inst.slug).update(school_username='')


def _notify(user, actor, message):
    if not message:
        return
    try:
        from .notifications import create_notification
        create_notification(recipient=user, actor=actor or user, verb='system', target=None, message=message)
    except Exception:
        pass


def apply_school(user, slug='', name='', username=''):
    """Store a person's school choice. Keeps the old value when nothing was sent."""
    slug = (slug or '').strip()[:90]
    name = (name or '').strip()[:200]
    username = (username or '').strip()
    if user.role == 'institution':
        if name:
            user.school = name
        user.school_slug = ''
        user.school_username = ''
        return None
    if not slug and username:
        found = Institution.objects.filter(claimed_by__username=username, verified=True).first()
        slug = found.slug if found else ''
    if slug:
        return select_school(user, slug, name)
    if name:
        return select_school(user, '', name)
    return None
