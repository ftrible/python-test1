from django.urls import path
from book import views
from searches.views import search_view
from django.conf import settings
from .views import vision_api
urlpatterns = [
    path('book/', views.list, name='list'),
    path('book/<str:slug_id>/', views.detail, name='detail'),
    path('book/<str:slug_id>/delete/', views.delete, name='delete'),
    path('book/<str:slug_id>/edit/', views.update, name='edit'),
    path('book-new', views.create, name='new'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/create/', views.author_create, name='author_create'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('authors/<int:pk>/edit/', views.author_update, name='author_update'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),
    path('vision-api/', vision_api, name='vision_api'),
    ]
# to find static and media files
if settings.DEBUG:  
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)