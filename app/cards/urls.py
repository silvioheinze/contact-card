from django.urls import path, re_path

from . import views

app_name = 'cards'

SLUG_PATTERN = r'(?P<slug>[a-z0-9][a-z0-9._-]*)'

urlpatterns = [
    path('edit/', views.card_edit, name='edit'),
    re_path(
        rf'^{SLUG_PATTERN}/vcard\.vcf$',
        views.card_vcard,
        name='vcard',
    ),
    re_path(
        rf'^{SLUG_PATTERN}/qr\.png$',
        views.card_qr,
        name='qr',
    ),
    re_path(
        rf'^{SLUG_PATTERN}/$',
        views.card_detail,
        name='detail',
    ),
]
