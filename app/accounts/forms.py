from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from main.util import normalize_email, validate_allowed_domain


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_('Email address'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'du@gruene.at',
            'autocomplete': 'email',
        }),
    )

    def clean_email(self):
        email = normalize_email(self.cleaned_data['email'])
        try:
            validate_allowed_domain(email)
        except ValidationError as exc:
            raise forms.ValidationError(exc.messages[0]) from exc
        return email
