from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mobility import views

urlpatterns = [
    path('customer/login/', views.customer_login, name='customer_login'),
    path('customer/logout/', views.customer_logout, name='customer_logout'),
    path('customer/profile/', views.customer_profile, name='customer_profile'),
    path('my-rides/', views.my_rides, name='my_rides'),
    path('my-rides/<int:pk>/track/', views.track_customer_ride, name='track_customer_ride'),
    path('cms/login/', views.cms_login, name='cms_login'),
    path('cms/builder/', views.cms_builder, name='cms_builder'),
    path('cms/builder/add/', views.cms_builder_section, name='cms_builder_add'),
    path('cms/builder/<int:pk>/edit/', views.cms_builder_section, name='cms_builder_edit'),
    path('cms/builder/<int:pk>/delete/', views.cms_builder_delete, name='cms_builder_delete'),
    path('cms/builder/reorder/', views.cms_builder_reorder, name='cms_builder_reorder'),
    path('cms/theme/', views.cms_theme, name='cms_theme'),
    path('cms/logout/', views.cms_logout, name='cms_logout'),
    path('cms/bookings/<int:pk>/', views.cms_booking_detail, name='cms_booking_detail'),
    path('cms/', views.cms_dashboard, name='cms_dashboard'),
    path('cms/<str:model_key>/', views.cms_list, name='cms_list'),
    path('cms/<str:model_key>/add/', views.cms_create, name='cms_create'),
    path('cms/<str:model_key>/<int:pk>/edit/', views.cms_edit, name='cms_edit'),
    path('cms/<str:model_key>/<int:pk>/delete/', views.cms_delete, name='cms_delete'),
    path('', views.home, name='home'),
    path('book/', views.create_booking, name='create_booking'),
    path('track-booking/', views.track_booking, name='track_booking'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
