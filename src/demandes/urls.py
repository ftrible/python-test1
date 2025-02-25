from django.urls import path
from demandes import views
from searches.views import search_view
from django.conf import settings
urlpatterns = [
    path('demandes/', views.list, name='list'),
    path('demandes/<str:slug_id>/', views.detail, name='detail'),
    path('demandes/<str:slug_id>/delete/', views.delete, name='delete'),
    path('demandes/<str:slug_id>/edit/', views.update, name='edit'),
    path('demandes-new', views.create, name='new'),
]
# to find static and media files
if settings.DEBUG:  
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)