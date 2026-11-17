"""The app claims an institution without the website: listed ones by slug, unlisted ones with no slug."""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from api.models_institutions import Institution, InstitutionVerification
from api.security import issue_auth_token
from web.test_onboarding import _make

FORM = {
    'name': 'Sunrise Academy', 'kind': 'school', 'district': 'Kaski', 'address': 'Pokhara', 'website': '',
    'registration_no': 'R-123', 'contact_name': 'Hari Sharma', 'contact_role': 'Principal',
    'contact_phone': '9800000000', 'contact_email': 'hari@sunrise.edu.np', 'message': '',
}


def _pdf():
    return SimpleUploadedFile('reg.pdf', b'%PDF-1.4 test', content_type='application/pdf')


class InstitutionClaimApiTests(TestCase):
    def post(self, user, path, **extra):
        token = issue_auth_token(user)
        return Client().post(path, {**FORM, 'documents': _pdf(), 'doc_type': 'registration', **extra},
                             HTTP_AUTHORIZATION='Bearer ' + token)

    def test_unlisted_institution_can_apply(self):
        user = _make(role='institution')
        res = self.post(user, '/api/institutions/claim/')
        self.assertEqual(res.status_code, 201, res.content)
        app = InstitutionVerification.objects.get(applicant=user)
        self.assertIsNone(app.institution)
        self.assertEqual(app.documents.first().doc_type, 'registration')

    def test_only_institution_accounts(self):
        res = self.post(_make(role='student'), '/api/institutions/claim/')
        self.assertEqual(res.status_code, 403)

    def test_listed_institution_by_slug_and_mine_reports_role(self):
        inst = Institution.objects.create(name='Lake College', slug='lake-college', kind='college', district='Kaski')
        user = _make(role='institution')
        self.assertEqual(self.post(user, '/api/institutions/lake-college/claim/').status_code, 201)
        mine = Client().get('/api/institutions/mine/', HTTP_AUTHORIZATION='Bearer ' + issue_auth_token(user)).json()
        self.assertEqual(mine['role'], 'institution')
        self.assertEqual(mine['application']['institution'], inst.slug)
