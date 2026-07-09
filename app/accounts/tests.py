from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.services import get_or_create_user_from_email, load_magic_link_email
from accounts.services import build_magic_link, send_magic_link_email
from django.core import mail
from django.contrib.auth import get_user_model

from main.util import slug_from_email, validate_allowed_domain
from django.core.exceptions import ValidationError


class DomainValidationTests(TestCase):
    @override_settings(ALLOWED_EMAIL_DOMAIN='example.com')
    def test_allowed_domain_passes(self):
        validate_allowed_domain('user@example.com')

    @override_settings(ALLOWED_EMAIL_DOMAIN='example.com')
    def test_wrong_domain_rejected(self):
        with self.assertRaises(ValidationError):
            validate_allowed_domain('user@other.com')


class SlugTests(TestCase):
    def test_slug_from_email(self):
        self.assertEqual(slug_from_email('John.Doe@Example.com'), 'john.doe')

    def test_reserved_slug_rejected(self):
        with self.assertRaises(ValidationError):
            slug_from_email('login@example.com')


class MagicLinkTests(TestCase):
    @override_settings(ALLOWED_EMAIL_DOMAIN='example.com')
    def test_magic_link_roundtrip(self):
        from django.test import RequestFactory
        from urllib.parse import parse_qs, urlparse

        request = RequestFactory().get('/')
        request.META['HTTP_HOST'] = 'localhost'
        link = build_magic_link('user@example.com', request)
        token = parse_qs(urlparse(link).query)['token'][0]
        email = load_magic_link_email(token)
        self.assertEqual(email, 'user@example.com')

    @override_settings(ALLOWED_EMAIL_DOMAIN='example.com')
    def test_user_and_card_created_on_verify_flow(self):
        user, created = get_or_create_user_from_email('new@example.com')
        self.assertTrue(created)
        self.assertEqual(user.slug, 'new')

    @override_settings(
        ALLOWED_EMAIL_DOMAIN='example.com',
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    )
    def test_login_sends_email(self):
        response = self.client.post(
            reverse('login'),
            {'email': 'user@example.com'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('user@example.com', mail.outbox[0].to)
