from django.urls import path, re_path
from test1 import views
from searches.views import search_view
from django.conf import settings
urlpatterns = [
    path('', views.home_page, name="home"),
    path('blog/', views.blog_list, name='blog-list'),
    path('search/', search_view, name='search'),
    path('blog/<str:slug_id>/', views.blog_detail, name='blog-detail'),
    path('blog/<str:slug_id>/delete/', views.blog_delete, name='blog-delete'),
    path('blog/<str:slug_id>/edit/', views.blog_update, name='blog-edit'),
    path('blog-new', views.blog_create, name='blog-new'),
]
# to find static and media files
if settings.DEBUG:  
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)