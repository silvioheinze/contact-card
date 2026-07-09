import io

import qrcode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from .forms import CardForm, CardLinkFormSet
from .models import Card
from .vcard import build_vcard


def card_detail(request, slug):
    card = get_object_or_404(Card, user__slug=slug)
    return render(request, 'cards/card_detail.html', {'card': card})


def card_vcard(request, slug):
    card = get_object_or_404(Card, user__slug=slug)
    content = build_vcard(card, request)
    response = HttpResponse(content, content_type='text/vcard; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{card.slug}.vcf"'
    return response


def card_qr(request, slug):
    card = get_object_or_404(Card, user__slug=slug)
    card_url = request.build_absolute_uri(card.get_absolute_url())
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(card_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')


@login_required
@require_http_methods(['GET', 'POST'])
def card_edit(request):
    card, _created = Card.objects.get_or_create(
        user=request.user,
        defaults={'email': request.user.email},
    )

    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES, instance=card)
        formset = CardLinkFormSet(request.POST, instance=card)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, _('Card saved.'))
            return redirect('cards:edit')
    else:
        form = CardForm(instance=card)
        formset = CardLinkFormSet(instance=card)

    return render(request, 'cards/card_edit.html', {
        'form': form,
        'formset': formset,
        'card': card,
    })
