from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from .forms import SiteSettingsForm
from .models import SiteSettings


def superuser_required(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(superuser_required, login_url='login')
def settings_view(request):
    site_settings = SiteSettings.load()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, _('Site settings saved.'))
            return redirect('site_settings:settings')
    else:
        form = SiteSettingsForm(instance=site_settings)

    return render(request, 'site_settings/settings.html', {
        'form': form,
        'site_settings': site_settings,
    })
