import secrets
import string

from django.db import migrations

SLUG_ID_ALPHABET = string.ascii_lowercase + string.digits
SLUG_ID_LENGTH = 6
MAX_SLUG_LENGTH = 150


def generate_slug_id():
    return ''.join(
        secrets.choice(SLUG_ID_ALPHABET) for _ in range(SLUG_ID_LENGTH)
    )


def suffix_user_slugs(apps, schema_editor):
    User = apps.get_model('accounts', 'CustomUser')
    used_slugs = set(User.objects.values_list('slug', flat=True))

    for user in User.objects.all().iterator():
        for _ in range(100):
            candidate = f'{user.slug}-{generate_slug_id()}'
            if len(candidate) > MAX_SLUG_LENGTH:
                raise RuntimeError(
                    f'Cannot suffix slug for user {user.pk}: would exceed max length.'
                )
            if candidate not in used_slugs:
                used_slugs.discard(user.slug)
                used_slugs.add(candidate)
                user.slug = candidate
                user.save(update_fields=['slug'])
                break
        else:
            raise RuntimeError(f'Could not generate unique slug suffix for user {user.pk}.')


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(suffix_user_slugs, migrations.RunPython.noop),
    ]
