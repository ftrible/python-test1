from django.urls import path
from book import views
from searches.views import search_view
from django.conf import settings
urlpatterns = [
    path('book/', views.list, name='list'),
    path('book/<str:slug_id>/', views.detail, name='detail'),
    path('book/<str:slug_id>/delete/', views.delete, name='delete'),
    path('book/<str:slug_id>/edit/', views.update, name='edit'),
    path('book-new', views.create, name='new'),
]
# to find static and media files
if settings.DEBUG:  
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)