from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from main.util import normalize_url

from .models import Card, CardLink

LINK_PRESETS = [
    ('LinkedIn', 'LinkedIn'),
    ('GitHub', 'GitHub'),
    ('Twitter/X', 'Twitter/X'),
    ('Instagram', 'Instagram'),
    ('Mastodon', 'Mastodon'),
    ('Facebook', 'Facebook'),
    ('YouTube', 'YouTube'),
    ('Custom', 'Custom'),
]


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            'first_name', 'last_name', 'title', 'company',
            'phone', 'email', 'website', 'bio', 'photo',
        ]
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'title': _('Job title'),
            'company': _('Company'),
            'phone': _('Phone'),
            'email': _('Email'),
            'website': _('Website'),
            'bio': _('Bio'),
            'photo': _('Photo'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_website(self):
        return normalize_url(self.cleaned_data.get('website', ''))

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and hasattr(photo, 'size') and photo.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(_('Image must be smaller than 2 MB.'))
        return photo


class CardLinkForm(forms.ModelForm):
    preset = forms.ChoiceField(
        choices=LINK_PRESETS,
        required=False,
        label=_('Platform'),
        widget=forms.Select(attrs={'class': 'form-select link-preset'}),
    )

    class Meta:
        model = CardLink
        fields = ['label', 'url', 'sort_order']
        labels = {
            'label': _('Label'),
            'url': _('URL'),
        }
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control link-label'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'}),
            'sort_order': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        preset_keys = dict(LINK_PRESETS)
        if self.instance.pk and self.instance.label in preset_keys:
            self.fields['preset'].initial = self.instance.label
        elif self.instance.pk:
            self.fields['preset'].initial = 'Custom'

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('DELETE'):
            return cleaned

        preset = cleaned.get('preset')
        label = (cleaned.get('label') or '').strip()
        url = normalize_url(cleaned.get('url', ''))

        if not url:
            cleaned['DELETE'] = True
            return cleaned

        if preset and preset != 'Custom' and not label:
            cleaned['label'] = preset

        cleaned['url'] = url
        if not cleaned.get('label'):
            self.add_error('label', _('Label is required when URL is set.'))
        return cleaned


CardLinkFormSet = inlineformset_factory(
    Card,
    CardLink,
    form=CardLinkForm,
    extra=1,
    can_delete=True,
)
