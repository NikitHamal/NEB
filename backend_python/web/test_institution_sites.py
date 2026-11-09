"""The website overlay: verified official sites land on the right institution, nothing is duplicated, bad links go."""
import importlib
import json

from django.apps import apps as django_apps
from django.test import TestCase

from api.models_institutions import Institution

migration = importlib.import_module('api.migrations.0168_institution_sites')


class InstitutionSitesTests(TestCase):
    def test_overlay_entries_are_https_with_a_district(self):
        entries = json.loads(migration.SITES.read_text(encoding='utf-8'))
        self.assertGreaterEqual(len(entries), 20)
        for e in entries:
            self.assertTrue(e['website'].startswith('https://'), e)
            self.assertTrue(e['district'], e)

    def test_apply_sets_sites_once_and_adds_missing_schools(self):
        migration.apply(django_apps, None)
        total = Institution.objects.count()
        gems = Institution.objects.filter(name='GEMS', district='Lalitpur').first()
        self.assertIsNotNone(gems)
        self.assertEqual(gems.website, 'https://gems.edu.np')
        gbs = Institution.objects.filter(name='Gandaki Boarding School', district='Kaski').first()
        self.assertIsNotNone(gbs)
        self.assertEqual(gbs.website, 'https://gbs.edu.np')
        migration.apply(django_apps, None)
        self.assertEqual(Institution.objects.count(), total)

    def test_apply_never_overwrites_an_existing_site_and_drops_the_bad_link(self):
        Institution.objects.create(slug='bad-link', name='Bad Link School', kind='school', website='https://uprowadzonadonepal.example')
        keep = Institution.objects.filter(name='Karnali Academy of Health Sciences').first()
        before = keep.website if keep else ''
        migration.apply(django_apps, None)
        self.assertEqual(Institution.objects.get(slug='bad-link').website, '')
        if keep:
            keep.refresh_from_db()
            self.assertEqual(keep.website, before)
