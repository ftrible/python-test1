from django.urls import path
from blog import views
from searches.views import search_view
from django.conf import settings
urlpatterns = [
    path('', views.home_page, name="home"),
    path('blog/', views.list, name='list'),
    path('search/', search_view, name='search'),
    path('blog/<str:slug_id>/', views.detail, name='detail'),
    path('blog/<str:slug_id>/delete/', views.delete, name='delete'),
    path('blog/<str:slug_id>/edit/', views.update, name='edit'),
    path('blog-new', views.create, name='new'),
]
# to find static and media files
if settings.DEBUG:  
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)