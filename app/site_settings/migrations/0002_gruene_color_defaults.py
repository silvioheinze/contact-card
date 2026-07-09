from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='primary_color',
            field=models.CharField(default='#257639', max_length=7),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='accent_color',
            field=models.CharField(default='#1c5a2c', max_length=7),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='background_color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
    ]
