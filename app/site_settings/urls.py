from django.urls import path

from . import views

app_name = 'site_settings'

urlpatterns = [
    path('', views.settings_view, name='settings'),
]
