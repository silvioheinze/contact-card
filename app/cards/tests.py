from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import CustomUser
from cards.models import Card


class CardViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='jane@example.com',
            slug='jane',
        )
        self.card = Card.objects.create(
            user=self.user,
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
        )

    def test_public_card_view(self):
        response = self.client.get(reverse('cards:detail', kwargs={'slug': 'jane'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane Doe')

    def test_unknown_slug_404(self):
        response = self.client.get(reverse('cards:detail', kwargs={'slug': 'nobody'}))
        self.assertEqual(response.status_code, 404)

    @override_settings(ALLOWED_EMAIL_DOMAIN='example.com')
    def test_edit_requires_login(self):
        response = self.client.get(reverse('cards:edit'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_vcard_download(self):
        response = self.client.get(reverse('cards:vcard', kwargs={'slug': 'jane'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/vcard', response['Content-Type'])
        self.assertIn(b'BEGIN:VCARD', response.content)

    def test_qr_code(self):
        response = self.client.get(reverse('cards:qr', kwargs={'slug': 'jane'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

    def test_card_shows_company_and_bio(self):
        self.card.company = 'Grüne Neubau'
        self.card.bio = 'Kurze Biografie'
        self.card.save()
        response = self.client.get(reverse('cards:detail', kwargs={'slug': 'jane'}))
        self.assertContains(response, 'Grüne Neubau')
        self.assertContains(response, 'Kurze Biografie')

    def test_edit_saves_company_and_bio(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('cards:edit'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'title': 'Funktion',
            'company': 'Organisationsteil XY',
            'phone': '',
            'email': 'jane@example.com',
            'website': '',
            'bio': 'Meine Bio',
            'links-TOTAL_FORMS': '1',
            'links-INITIAL_FORMS': '0',
            'links-MIN_NUM_FORMS': '0',
            'links-MAX_NUM_FORMS': '1000',
            'links-0-label': '',
            'links-0-url': '',
            'links-0-sort_order': '0',
            'links-0-preset': '',
        })
        self.assertEqual(response.status_code, 302)
        self.card.refresh_from_db()
        self.assertEqual(self.card.company, 'Organisationsteil XY')
        self.assertEqual(self.card.bio, 'Meine Bio')

    def test_edit_saves_profile_when_link_url_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('cards:edit'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'title': '',
            'company': 'Grüne Neubau',
            'phone': '',
            'email': 'jane@example.com',
            'website': '',
            'bio': 'Biografie Text',
            'links-TOTAL_FORMS': '1',
            'links-INITIAL_FORMS': '0',
            'links-MIN_NUM_FORMS': '0',
            'links-MAX_NUM_FORMS': '1000',
            'links-0-label': 'LinkedIn',
            'links-0-url': 'not-a-valid-url',
            'links-0-sort_order': '0',
            'links-0-preset': 'LinkedIn',
        })
        self.assertEqual(response.status_code, 302)
        self.card.refresh_from_db()
        self.assertEqual(self.card.company, 'Grüne Neubau')
        self.assertEqual(self.card.bio, 'Biografie Text')
