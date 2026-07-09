from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default=_('Contact Cards'))
    logo = models.ImageField(upload_to='site/', blank=True)
    primary_color = models.CharField(max_length=7, default='#257639')
    accent_color = models.CharField(max_length=7, default='#1c5a2c')
    background_color = models.CharField(max_length=7, default='#ffffff')
    footer_text = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = _('Site settings')
        verbose_name_plural = _('Site settings')

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError(_('Site settings cannot be deleted.'))

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj
