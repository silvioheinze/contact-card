import logging
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.translation import gettext as _

from main.util import slug_from_email, validate_allowed_domain

logger = logging.getLogger(__name__)

MAGIC_LINK_SALT = 'contact-card-magic-link'


def build_magic_link(email, request):
    payload = {'email': email}
    token = signing.dumps(payload, salt=MAGIC_LINK_SALT)
    path = reverse('verify')
    return request.build_absolute_uri(f'{path}?{urlencode({"token": token})}')


def send_magic_link_email(email, request):
    link = build_magic_link(email, request)
    minutes = settings.MAGIC_LINK_MAX_AGE // 60
    send_mail(
        subject=_('Your login link'),
        message=_(
            'Click the link below to sign in. This link expires in '
            '%(minutes)s minutes.\n\n%(link)s\n'
        ) % {'minutes': minutes, 'link': link},
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


def load_magic_link_email(token, max_age=None):
    max_age = max_age or settings.MAGIC_LINK_MAX_AGE
    try:
        payload = signing.loads(token, salt=MAGIC_LINK_SALT, max_age=max_age)
    except signing.BadSignature as exc:
        raise ValueError(_('Invalid or expired login link.')) from exc
    email = payload.get('email', '').strip().lower()
    if not email:
        raise ValueError(_('Invalid login link.'))
    validate_allowed_domain(email)
    return email


def get_or_create_user_from_email(email):
    User = get_user_model()
    slug = slug_from_email(email)
    user, created = User.objects.get_or_create(
        email=email,
        defaults={'slug': slug, 'is_active': True},
    )
    if not created and user.slug != slug:
        raise ValueError(_('Account slug mismatch.'))
    return user, created
