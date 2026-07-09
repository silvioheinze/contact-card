from django.db import migrations

OLD_DEFAULTS = {
    'primary_color': '#2563eb',
    'accent_color': '#1e40af',
    'background_color': '#f8fafc',
}

NEW_DEFAULTS = {
    'primary_color': '#257639',
    'accent_color': '#1c5a2c',
    'background_color': '#ffffff',
}


def migrate_old_defaults(apps, schema_editor):
    SiteSettings = apps.get_model('site_settings', 'SiteSettings')
    try:
        settings = SiteSettings.objects.get(pk=1)
    except SiteSettings.DoesNotExist:
        return

    updates = {}
    for field, old_value in OLD_DEFAULTS.items():
        if getattr(settings, field) == old_value:
            updates[field] = NEW_DEFAULTS[field]

    if updates:
        for field, value in updates.items():
            setattr(settings, field, value)
        settings.save()


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0002_gruene_color_defaults'),
    ]

    operations = [
        migrations.RunPython(migrate_old_defaults, migrations.RunPython.noop),
    ]
