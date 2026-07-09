from django.urls import reverse
from django.utils.translation import gettext as _


def build_vcard(card, request=None):
    lines = ['BEGIN:VCARD', 'VERSION:3.0']
    if card.first_name or card.last_name:
        lines.append(f'N:{card.last_name};{card.first_name};;;')
        lines.append(f'FN:{card.display_name}')
    if card.title:
        lines.append(f'TITLE:{card.title}')
    if card.company:
        lines.append(f'ORG:{card.company}')
    email = card.email or card.user.email
    if email:
        lines.append(f'EMAIL;TYPE=INTERNET:{email}')
    if card.phone:
        lines.append(f'TEL;TYPE=CELL:{card.phone}')
    if card.website:
        lines.append(f'URL:{card.website}')
    if card.bio:
        note = card.bio.replace('\n', '\\n')
        lines.append(f'NOTE:{note}')
    if request:
        card_url = request.build_absolute_uri(
            reverse('cards:detail', kwargs={'slug': card.slug})
        )
        lines.append(f'URL;TYPE={_("Contact Card")}:{card_url}')
    for link in card.links.all():
        lines.append(f'URL;TYPE={link.label}:{link.url}')
    lines.append('END:VCARD')
    return '\r\n'.join(lines) + '\r\n'
