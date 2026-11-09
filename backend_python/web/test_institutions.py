"""School catalogue, people counts, redirect to a school's site, and institution verification."""
import re
from pathlib import Path

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from api import institutions as svc
from api.models import User
from api.models_institutions import Institution, InstitutionDocument, InstitutionVerification
from api.security import issue_auth_token
from web.test_onboarding import _make, _sign_in

CSS = Path(__file__).resolve().parent / 'static' / 'web' / 'css' / 'pages'
PDF = b'%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF'


def _admin(client):
    admin = User.objects.create(id='u_inst_admin', username='inst_admin', created_at=1, is_admin=True)
    s = client.session
    s['auth_token'] = issue_auth_token(admin)
    s.save()
    return admin


class CatalogueTests(TestCase):
    def test_catalogue_is_seeded_with_thousands_of_real_institutions(self):
        self.assertGreater(Institution.objects.count(), 20000)
        self.assertTrue(Institution.objects.filter(website__startswith='http').count() > 150)
        self.assertTrue(Institution.objects.filter(name='Tribhuvan University', website='https://tu.edu.np').exists())

    def test_import_is_idempotent(self):
        added, existing = svc.import_catalog()
        self.assertEqual(added, 0)
        self.assertGreater(existing, 20000)

    def test_verified_institutions_come_first_in_every_search(self):
        inst = Institution.objects.filter(name__icontains='Xavier').first()
        self.assertIsNotNone(inst)
        owner = _make(role='institution', display_name=inst.name)
        inst.claimed_by, inst.verified = owner, True
        inst.save()
        rows, total, _ = svc.search('xavier')
        self.assertEqual(rows[0].pk, inst.pk)
        rows, _, _ = svc.search('', limit=5)
        self.assertEqual(rows[0].pk, inst.pk)

    def test_search_matches_every_word(self):
        rows, _, _ = svc.search('budhanilkantha school kathmandu')
        self.assertTrue(rows)
        self.assertTrue(all('budhanilkantha' in r.name.lower() for r in rows))


class PeopleTests(TestCase):
    def setUp(self):
        self.inst = Institution.objects.get(slug='tribhuvan-university')
        self.owner = _make(role='institution', display_name='Tribhuvan University', institution_verified=True)
        self.client = Client()

    def test_counts_exclude_the_account_banned_and_bots(self):
        _make(school_slug=self.inst.slug, role='student')
        _make(school_slug=self.inst.slug, role='teacher')
        _make(school_slug=self.inst.slug, role='student', is_banned=True)
        _make(school_slug=self.inst.slug, role='student', is_bot=True)
        counts = svc.people_counts(self.inst)
        self.assertEqual(counts, {'total': 2, 'students': 1, 'teachers': 1})

    def test_locked_profiles_are_counted_but_not_listed(self):
        _make(school_slug=self.inst.slug, role='student', is_locked=True)
        _make(school_slug=self.inst.slug, role='student')
        self.assertEqual(svc.people_counts(self.inst)['total'], 2)
        self.assertEqual(len(svc.people_list(self.inst)), 1)

    def test_picking_a_school_sets_slug_and_name_and_claimed_account(self):
        u = _make(role='student')
        svc.select_school(u, self.inst.slug)
        self.assertEqual((u.school, u.school_slug, u.school_username), (self.inst.name, self.inst.slug, ''))
        self.inst.claimed_by, self.inst.verified = self.owner, True
        self.inst.save()
        svc.select_school(u, self.inst.slug)
        self.assertEqual(u.school_username, self.owner.username)

    def test_institution_accounts_never_become_their_own_students(self):
        svc.apply_school(self.owner, self.inst.slug, 'Tribhuvan University')
        self.assertEqual(self.owner.school_slug, '')

    def test_school_page_shows_counts_and_people(self):
        who = _make(school_slug=self.inst.slug, role='student', display_name='Asha Rai')
        html = self.client.get('/app/schools/%s/' % self.inst.slug).content.decode()
        self.assertIn('Tribhuvan University', html)
        self.assertIn('Asha Rai', html)
        self.assertIn('/app/profile/%s/' % who.username, html)
        self.assertRegex(html, r'<b>1</b><span>Students</span>')

    def test_institution_profile_lists_its_people(self):
        self.inst.claimed_by, self.inst.verified = self.owner, True
        self.inst.save()
        _make(school_slug=self.inst.slug, role='student', display_name='Mina Gurung')
        html = self.client.get('/app/profile/%s/' % self.owner.username).content.decode()
        self.assertIn('inst-people', html)
        self.assertIn('Mina Gurung', html)
        self.assertIn('1 on NEBians', html)


class RedirectTests(TestCase):
    def test_unclaimed_school_goes_to_its_website(self):
        r = Client().get('/app/schools/tribhuvan-university/go/')
        self.assertEqual((r.status_code, r['Location']), (302, 'https://tu.edu.np'))

    def test_claimed_school_goes_to_its_profile(self):
        inst = Institution.objects.get(slug='tribhuvan-university')
        owner = _make(role='institution')
        inst.claimed_by, inst.verified = owner, True
        inst.save()
        r = Client().get('/app/schools/tribhuvan-university/go/')
        self.assertEqual(r['Location'], '/app/profile/%s/' % owner.username)

    def test_school_without_site_goes_to_its_page(self):
        inst = Institution.objects.filter(website='').first()
        r = Client().get('/app/schools/%s/go/' % inst.slug)
        self.assertEqual(r['Location'], '/app/schools/%s/' % inst.slug)

    def test_student_profile_links_straight_to_the_school_site(self):
        u = _make(role='student', school='Tribhuvan University', school_slug='tribhuvan-university')
        html = Client().get('/app/profile/%s/' % u.username).content.decode()
        self.assertIn('href="https://tu.edu.np"', html)


class VerificationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = _make(role='institution', display_name='Himalaya Academy', email='head@himalaya.edu.np')
        _sign_in(self.client, self.user)

    def _post(self, **over):
        data = {'name': 'Himalaya Academy', 'kind': 'school', 'district': 'Kaski', 'address': 'Lakeside, Pokhara',
                'registration_no': 'REG 2051/114', 'website': 'himalaya.edu.np', 'contact_name': 'Sita Sharma',
                'contact_role': 'Principal', 'contact_email': 'head@himalaya.edu.np', 'contact_phone': '9801234567',
                'doc_type': 'registration',
                'documents': SimpleUploadedFile('cert.pdf', PDF, content_type='application/pdf')}
        data.update(over)
        return self.client.post('/app/schools/verify/', data)

    def test_form_asks_for_contacts_and_documents(self):
        html = self.client.get('/app/schools/verify/').content.decode()
        for name in ('contact_name', 'contact_role', 'contact_email', 'contact_phone', 'registration_no', 'documents'):
            self.assertIn('name="%s"' % name, html)

    def test_students_are_told_to_switch_account_type(self):
        student = _make(role='student')
        c = Client()
        _sign_in(c, student)
        self.assertIn('Switch account type', c.get('/app/schools/verify/').content.decode())
        self.assertEqual(InstitutionVerification.objects.count(), 0)

    def test_valid_application_is_stored_with_a_private_document(self):
        r = self._post()
        self.assertEqual(r.status_code, 302)
        app = InstitutionVerification.objects.get()
        self.assertEqual((app.status, app.contact_phone, app.website), ('pending', '9801234567', 'https://himalaya.edu.np'))
        doc = InstitutionDocument.objects.get()
        self.assertEqual(doc.doc_type, 'registration')
        self.assertTrue(doc.file.name.startswith('institution_docs/'))
        self.assertIn('Request received', self.client.get('/app/schools/verify/').content.decode())

    def test_missing_details_and_bad_files_are_rejected(self):
        r = self._post(contact_email='nope', contact_phone='12', registration_no='')
        html = r.content.decode()
        self.assertEqual(InstitutionVerification.objects.count(), 0)
        self.assertIn('Enter a valid email', html)
        self.assertIn('Enter a phone number', html)
        r = self._post(documents=SimpleUploadedFile('fake.pdf', b'not a pdf at all', content_type='application/pdf'))
        self.assertIn('does not look like a PDF', r.content.decode())
        r = self._post(documents=SimpleUploadedFile('run.exe', b'MZ', content_type='application/octet-stream'))
        self.assertIn('PDF, JPG, PNG or WebP', r.content.decode())
        self.assertEqual(InstitutionVerification.objects.count(), 0)

    def test_admin_approval_claims_the_school_and_links_students(self):
        inst = Institution.objects.filter(name__icontains='Budhanilkantha School').first()
        student = _make(role='student', school=inst.name, school_slug=inst.slug)
        self._post(institution=inst.slug)
        app = InstitutionVerification.objects.get()
        self.assertEqual(app.institution_id, inst.pk)
        admin = Client()
        _admin(admin)
        page = admin.get('/admin/institutions/%d/' % app.pk).content.decode()
        self.assertIn('Sita Sharma', page)
        self.assertIn('/admin/institutions/document/', page)
        doc = app.documents.get()
        self.assertEqual(admin.get('/admin/institutions/document/%d/' % doc.pk).status_code, 200)
        self.assertEqual(Client().get('/admin/institutions/document/%d/' % doc.pk).status_code, 404)
        self.assertEqual(self._anon_doc_status(doc), 404)
        admin.post('/admin/institutions/%d/' % app.pk, {'action': 'approve', 'note': 'Checked'})
        inst.refresh_from_db()
        self.user.refresh_from_db()
        student.refresh_from_db()
        self.assertTrue(inst.verified)
        self.assertEqual(inst.claimed_by_id, self.user.pk)
        self.assertTrue(self.user.institution_verified)
        self.assertEqual(student.school_username, self.user.username)
        rows, _, _ = svc.search(inst.name)
        self.assertEqual(rows[0].pk, inst.pk)
        self.assertIn('is verified', self.client.get('/app/schools/verify/').content.decode())

    def _anon_doc_status(self, doc):
        return Client().get('/admin/institutions/document/%d/' % doc.pk).status_code

    def test_a_new_institution_not_in_the_catalogue_is_created_on_approval(self):
        self._post(name='Brand New Academy')
        app = InstitutionVerification.objects.get()
        svc.approve(app, None, '')
        inst = Institution.objects.get(name='Brand New Academy')
        self.assertTrue(inst.verified)
        self.assertEqual(inst.claimed_by_id, self.user.pk)

    def test_rejection_reopens_the_form_with_the_reason(self):
        self._post()
        app = InstitutionVerification.objects.get()
        svc.decide(app, None, 'rejected', 'Certificate unreadable')
        html = self.client.get('/app/schools/verify/').content.decode()
        self.assertIn('Certificate unreadable', html)
        self.assertIn('name="contact_name"', html)

    def test_a_verified_school_cannot_be_claimed_by_someone_else(self):
        inst = Institution.objects.get(slug='tribhuvan-university')
        owner = _make(role='institution')
        inst.claimed_by, inst.verified = owner, True
        inst.save()
        html = self.client.get('/app/schools/verify/?school=%s' % inst.slug).content.decode()
        self.assertIn('already has a verified account', html)
        self.assertNotIn('name="contact_name"', html)

    def test_admin_list_pages_render(self):
        self._post()
        admin = Client()
        _admin(admin)
        for tab in ('open', 'approved', 'rejected', 'verified'):
            self.assertEqual(admin.get('/admin/institutions/?tab=' + tab).status_code, 200)
        self.assertIn('Himalaya Academy', admin.get('/admin/institutions/').content.decode())


class SchoolPagesTests(TestCase):
    def test_directory_filters_and_lists(self):
        html = Client().get('/app/schools/?q=xavier&kind=college').content.decode()
        self.assertIn('sch-row', html)
        html = Client().get('/app/schools/').content.decode()
        self.assertIn('Show more', html)

    def test_search_endpoint_and_api(self):
        r = Client().get('/ajax/institutions/search/?q=tribhuvan')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['items'])
        r = Client().get('/api/institutions/?q=tribhuvan')
        self.assertEqual(r.status_code, 200)
        r = Client().get('/api/institutions/tribhuvan-university/')
        self.assertEqual(r.json()['website'], 'https://tu.edu.np')

    def test_school_css_has_no_shadow_gradient_or_square_hover(self):
        css = re.sub(r'/\*.*?\*/', '', (CSS / 'schools.css').read_text(), flags=re.S)
        self.assertNotRegex(css, r'box-shadow\s*:\s*(?!none)')
        self.assertNotIn('gradient', css)
        self.assertNotRegex(css, r'border-radius\s*:\s*0(?![.\d])')

    def test_pages_have_no_dash_punctuation(self):
        base = Path(__file__).resolve().parent / 'templates' / 'web'
        for name in ('schools', 'school_detail', 'school_apply'):
            text = (base / (name + '.html')).read_text()
            self.assertNotIn('\u2014', text)
            self.assertNotIn('\u2013', text)
