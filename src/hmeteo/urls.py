from django.urls import path
from hmeteo import views
from django.conf import settings
urlpatterns = [
    path('hmeteo/', views.list, name='list'),
    path('hmeteo/geocode/', views.geocode, name='geocode'),
    path('hmeteo/create/', views.createwitHObject, name='createwitHObject'),
    path('hmeteo/update-location/', views.update_location, name='update_location'),
#    path('search/', search_view, name='search'),
    path('hmeteo/<str:slug_id>/', views.detail, name='detail'),
    path('hmeteo/<str:slug_id>/delete/', views.delete, name='delete'),
    path('hmeteo/<str:slug_id>/edit/', views.update, name='edit'),
    path('hmeteo-new', views.create, name='new'),
]
# to find static and media files
if settings.DEBUG:  
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)