"""A claimed institution shows its owner's picture and never offers to be claimed again."""
from django.core.cache import cache
from django.test import Client, TestCase

from api import institutions as svc
from api.models_institutions import Institution
from api.serializers import UserSerializer
from web.test_onboarding import _make

PHOTO = 'https://example.test/media/profile_photos/school-logo.webp'


class LogoAndClaimTests(TestCase):
    def setUp(self):
        cache.clear()
        self.inst = Institution.objects.filter(name__icontains='Xavier').first()
        self.owner = _make(role='institution', display_name=self.inst.name)
        self.owner.photo_url = PHOTO
        self.owner.save(update_fields=['photo_url'])
        self.inst.claimed_by, self.inst.verified = self.owner, True
        self.inst.save()

    def test_logo_is_the_owners_picture_only_while_verified(self):
        self.assertEqual(self.inst.logo_url, PHOTO)
        self.assertEqual(svc.serialize(self.inst)['photoUrl'], PHOTO)
        self.inst.verified = False
        self.assertEqual(self.inst.logo_url, '')

    def test_claimed_institution_is_not_claimable(self):
        self.assertFalse(svc.is_claimable(self.inst))
        self.assertFalse(svc.serialize(self.inst)['claimable'])
        other = Institution.objects.filter(claimed_by__isnull=True, verified=False).first()
        self.assertTrue(svc.is_claimable(other))
        self.assertFalse(svc.is_claimable(other, self.owner))

    def test_owner_profile_carries_the_owned_slug(self):
        data = UserSerializer(self.owner).data
        self.assertEqual(data['school_slug'], self.inst.slug)

    def test_school_page_has_logo_and_no_claim_button(self):
        html = Client().get('/app/schools/%s/' % self.inst.slug).content.decode()
        self.assertIn(PHOTO, html)
        self.assertNotIn('Claim this school', html)

    def test_unclaimed_school_page_offers_the_claim(self):
        other = Institution.objects.filter(claimed_by__isnull=True, verified=False).first()
        html = Client().get('/app/schools/%s/' % other.slug).content.decode()
        self.assertIn('Claim this school', html)
