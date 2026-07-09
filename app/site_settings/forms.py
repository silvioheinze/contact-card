from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'logo', 'primary_color', 'accent_color',
            'background_color', 'footer_text',
        ]
        labels = {
            'site_name': _('Site name'),
            'logo': _('Logo'),
            'primary_color': _('Primary color'),
            'accent_color': _('Accent color'),
            'background_color': _('Background'),
            'footer_text': _('Footer text'),
        }
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'primary_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'accent_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'background_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'footer_text': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo and hasattr(logo, 'size') and logo.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(_('Logo must be smaller than 2 MB.'))
        return logo
