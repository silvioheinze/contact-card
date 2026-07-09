from django import template

register = template.Library()

LINK_ICONS = {
    'linkedin': 'bi-linkedin',
    'github': 'bi-github',
    'twitter/x': 'bi-twitter-x',
    'twitter': 'bi-twitter-x',
    'instagram': 'bi-instagram',
    'mastodon': 'bi-mastodon',
    'facebook': 'bi-facebook',
    'youtube': 'bi-youtube',
}


@register.filter
def link_icon(label):
    return LINK_ICONS.get(label.lower(), 'bi-link-45deg')


@register.filter
def tel_href(phone):
    digits = ''.join(c for c in phone if c.isdigit() or c == '+')
    return f'tel:{digits}'
