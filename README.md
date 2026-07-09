# Contact Card

Dockerized Django app for team contact cards with passwordless magic-link login.

## Features

- Magic-link login for users with email addresses from a configured domain
- Personal public page at `/{email-local-part}/`
- Card editor for contact info and social links
- vCard download and QR code on each card
- Superuser site settings for logo, colors, and footer text

## Quick start

```bash
cp project.env .env
docker compose up -d --build
./manage migrate
./manage createsuperuser
```

Open http://localhost in your browser.

For development, magic-link emails are printed to the app container logs (console email backend).

## Configuration

Edit `.env` (copied from `project.env`):

| Variable | Description |
|----------|-------------|
| `ALLOWED_EMAIL_DOMAIN` | Only emails from this domain can sign in |
| `DJANGO_SECRET_KEY` | Secret key (change in production) |
| `EMAIL_BACKEND` | Use SMTP backend in production |
| `MAGIC_LINK_MAX_AGE` | Magic link expiry in seconds (default 900) |

## Common commands

```bash
./manage check
./manage test
./manage collectstatic
docker compose logs -f app
```

## URLs

| Path | Description |
|------|-------------|
| `/` | Home |
| `/login/` | Request magic link |
| `/auth/verify/?token=…` | Magic link verification |
| `/edit/` | Edit your card (authenticated) |
| `/{slug}/` | Public contact card |
| `/{slug}/vcard.vcf` | Download vCard |
| `/{slug}/qr.png` | QR code image |
| `/settings/` | Site design settings (superuser) |
| `/backend/` | Django admin |

## Production

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Set `DJANGO_DEBUG=False`, configure SMTP, and use a strong `DJANGO_SECRET_KEY`.

## Translations

The app UI defaults to German (`LANGUAGE_CODE = de`). Translation files live in `app/locale/de/LC_MESSAGES/`.

To update translations after changing user-facing strings:

```bash
./manage makemessages -l de
# Edit app/locale/de/LC_MESSAGES/django.po
./manage compilemessages
```

## License

MIT (adjust as needed)
