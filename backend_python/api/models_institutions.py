"""Schools, colleges and universities, and the verification of the ones that join NEBians.

`Institution` is the catalogue (seeded from `api/data/institutions.json.gz`, see
`tools/institutions/build_catalog.py`). A row is *claimed* when an institution account was
approved for it, and only then shows first in every list. `InstitutionVerification` is one
application with contact details; `InstitutionDocument` is one private file attached to it.
"""
import re

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

KIND_SCHOOL = 'school'
KIND_COLLEGE = 'college'
KIND_UNIVERSITY = 'university'
KIND_INSTITUTE = 'institute'
KIND_CHOICES = [
    (KIND_SCHOOL, 'School'),
    (KIND_COLLEGE, 'College'),
    (KIND_UNIVERSITY, 'University'),
    (KIND_INSTITUTE, 'Institute'),
]
KIND_LABELS = dict(KIND_CHOICES)
KIND_ICONS = {KIND_SCHOOL: 'school', KIND_COLLEGE: 'account_balance', KIND_UNIVERSITY: 'domain',
              KIND_INSTITUTE: 'science'}

PROVINCE_NAMES = {'1': 'Koshi', '2': 'Madhesh', '3': 'Bagmati', '4': 'Gandaki', '5': 'Lumbini',
                  '6': 'Karnali', '7': 'Sudurpashchim'}

DOC_TYPES = [
    ('registration', 'Registration certificate'),
    ('pan', 'PAN or VAT certificate'),
    ('affiliation', 'Affiliation or approval letter'),
    ('authority', 'Authority letter for the applicant'),
    ('id', 'Applicant citizenship or ID'),
    ('other', 'Other'),
]
DOC_TYPE_LABELS = dict(DOC_TYPES)

_private_storage = None


def private_storage():
    global _private_storage
    if _private_storage is None:
        root = getattr(settings, 'PRIVATE_MEDIA_ROOT', None) or (settings.BASE_DIR / 'private_media')
        _private_storage = FileSystemStorage(location=str(root), base_url=None)
    return _private_storage


def search_key(*parts):
    text = ' '.join(p for p in parts if p).lower()
    return re.sub(r'[^a-z0-9\u0900-\u097f ]+', ' ', text).strip()[:300]


class Institution(models.Model):
    slug = models.SlugField(max_length=90, unique=True)
    name = models.CharField(max_length=200, db_index=True)
    name_ne = models.CharField(max_length=200, blank=True, default='')
    kind = models.CharField(max_length=12, choices=KIND_CHOICES, default=KIND_SCHOOL, db_index=True)
    district = models.CharField(max_length=60, blank=True, default='', db_index=True)
    province = models.CharField(max_length=2, blank=True, default='')
    place = models.CharField(max_length=100, blank=True, default='')
    website = models.CharField(max_length=300, blank=True, default='')
    phone = models.CharField(max_length=60, blank=True, default='')
    email = models.CharField(max_length=120, blank=True, default='')
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    est = models.CharField(max_length=4, blank=True, default='')
    source = models.CharField(max_length=60, blank=True, default='')
    search_text = models.CharField(max_length=320, blank=True, default='', db_index=True)
    claimed_by = models.ForeignKey('api.User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='claimed_institutions')
    verified = models.BooleanField(default=False, db_index=True)
    verified_at = models.BigIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'institutions'
        ordering = ['-verified', '-claimed_by_id', 'name']
        indexes = [models.Index(fields=['verified', 'name'], name='inst_verified_name_idx')]

    def __str__(self):
        return self.name

    @property
    def kind_label(self):
        return KIND_LABELS.get(self.kind, 'Institution')

    @property
    def kind_icon(self):
        return KIND_ICONS.get(self.kind, 'school')

    @property
    def province_name(self):
        return PROVINCE_NAMES.get(self.province, '')

    @property
    def location(self):
        parts = [self.place, self.district]
        return ', '.join(p for p in parts if p)

    def save(self, *args, **kwargs):
        self.search_text = search_key(self.name, self.name_ne, self.district, self.place)
        super().save(*args, **kwargs)


class InstitutionVerification(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_INFO = 'needs_info'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_INFO, 'Needs more info'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]
    OPEN_STATUSES = (STATUS_PENDING, STATUS_INFO)

    applicant = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='institution_applications')
    institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='applications')
    name = models.CharField(max_length=200)
    kind = models.CharField(max_length=12, choices=KIND_CHOICES, default=KIND_SCHOOL)
    district = models.CharField(max_length=60, blank=True, default='')
    address = models.CharField(max_length=250, blank=True, default='')
    website = models.CharField(max_length=300, blank=True, default='')
    registration_no = models.CharField(max_length=80, blank=True, default='')
    contact_name = models.CharField(max_length=120)
    contact_role = models.CharField(max_length=80)
    contact_email = models.CharField(max_length=120)
    contact_phone = models.CharField(max_length=40)
    message = models.TextField(blank=True, default='')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    reviewer_note = models.TextField(blank=True, default='')
    reviewed_by = models.ForeignKey('api.User', null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='reviewed_institution_applications')
    created_at = models.BigIntegerField(default=0, db_index=True)
    reviewed_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'institution_verifications'
        ordering = ['-created_at']

    def __str__(self):
        return '%s (%s)' % (self.name, self.status)

    @property
    def is_open(self):
        return self.status in self.OPEN_STATUSES


def _doc_path(instance, filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'bin'
    return 'institution_docs/%s/%s.%s' % (instance.verification_id, instance.token, re.sub(r'[^a-z0-9]', '', ext)[:5])


class InstitutionDocument(models.Model):
    verification = models.ForeignKey(InstitutionVerification, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=16, choices=DOC_TYPES, default='other')
    file = models.FileField(upload_to=_doc_path, storage=private_storage, max_length=200)
    token = models.CharField(max_length=32, default='')
    original_name = models.CharField(max_length=200, blank=True, default='')
    content_type = models.CharField(max_length=80, blank=True, default='')
    size = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'institution_documents'
        ordering = ['id']

    @property
    def type_label(self):
        return DOC_TYPE_LABELS.get(self.doc_type, 'Document')

    @property
    def is_image(self):
        return self.content_type.startswith('image/')
