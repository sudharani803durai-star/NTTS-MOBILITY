from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from mobility import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Old CMS addresses now use the single Django Admin login.
    re_path(r'^cms(?:/.*)?$', RedirectView.as_view(url='/admin/', permanent=False)),
    path('', views.home, name='home'),
    path('book/', views.create_booking, name='create_booking'),
    path('track-booking/', views.track_booking, name='track_booking'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
