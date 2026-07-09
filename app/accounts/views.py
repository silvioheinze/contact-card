from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from cards.models import Card

from .forms import LoginForm
from .services import get_or_create_user_from_email, load_magic_link_email, send_magic_link_email


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('cards:edit')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        try:
            send_magic_link_email(email, request)
        except Exception:
            messages.error(
                request,
                _('Could not send login email. Please try again later.'),
            )
        else:
            messages.success(
                request,
                _(
                    'If your email is allowed, a login link has been sent. '
                    'Check your inbox.'
                ),
            )
        return redirect('login')

    return render(request, 'accounts/login.html', {'form': form})


def verify_view(request):
    if request.user.is_authenticated:
        return redirect('cards:edit')

    token = request.GET.get('token', '')
    if not token:
        messages.error(request, _('Invalid login link.'))
        return redirect('login')

    try:
        email = load_magic_link_email(token)
        user, _created = get_or_create_user_from_email(email)
        Card.objects.get_or_create(user=user, defaults={'email': user.email})
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, _('You are now signed in.'))
        return redirect('cards:edit')
    except ValueError as exc:
        messages.error(request, str(exc))
        return redirect('login')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, _('You have been signed out.'))
    return redirect('home')
