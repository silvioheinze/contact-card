from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from site_settings.models import SiteSettings


class SiteSettingsTests(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            email='superuser@example.com',
            slug='superuser',
            password='testpass123',
        )
        SiteSettings.load()

    def test_context_processor_loads_settings(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kontaktkarten')

    def test_settings_requires_superuser(self):
        response = self.client.get(reverse('site_settings:settings'))
        self.assertEqual(response.status_code, 302)

    def test_superuser_can_access_settings(self):
        self.client.login(email='superuser@example.com', password='testpass123')
        response = self.client.get(reverse('site_settings:settings'))
        self.assertEqual(response.status_code, 200)
