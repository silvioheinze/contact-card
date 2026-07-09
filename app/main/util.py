import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


SLUG_PATTERN = re.compile(r'^[a-z0-9][a-z0-9._-]*$')


def normalize_email(email):
    return email.strip().lower()


def email_domain(email):
    if '@' not in email:
        return ''
    return email.rsplit('@', 1)[1].lower()


def email_local_part(email):
    return email.rsplit('@', 1)[0].lower()


def validate_allowed_domain(email):
    domain = email_domain(normalize_email(email))
    allowed = settings.ALLOWED_EMAIL_DOMAIN.lower()
    if domain != allowed:
        raise ValidationError(
            _('Only email addresses from @%(domain)s are allowed.'),
            params={'domain': allowed},
        )


def validate_slug(slug):
    slug = slug.lower()
    if slug in settings.RESERVED_SLUGS:
        raise ValidationError(_('"%(slug)s" is a reserved name.') % {'slug': slug})
    if not SLUG_PATTERN.match(slug):
        raise ValidationError(
            _(
                'Username must start with a letter or number and contain only '
                'letters, numbers, dots, underscores, or hyphens.'
            )
        )
    return slug


def slug_from_email(email):
    return validate_slug(email_local_part(normalize_email(email)))


def normalize_url(url):
    url = (url or '').strip()
    if not url:
        return ''
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', url):
        url = f'https://{url}'
    return url
