from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from accounts import views as account_views
from main import views as main_views

urlpatterns = [
    path('robots.txt', main_views.robots_txt, name='robots'),
    path('backend/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('auth/verify/', account_views.verify_view, name='verify'),
    path('settings/', include('site_settings.urls')),
    path('', include('cards.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
