"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('my_app/', include('my_app.urls'))
"""
from django.contrib import admin
from django.urls import include, path,reverse_lazy
from .views import contact_page,login_view, logout_view, about_page
from django.contrib.auth import views as auth_views
from userprofile.views import update
urlpatterns = [
    path("", include("blog.urls")),
    path("", include("book.urls")),
    path("", include("hmeteo.urls")),
    path("", include("demandes.urls")),
    path('contact/', contact_page, name='contact'),
    path('login/', login_view, name='login'),
    path('forgot/',auth_views.PasswordResetView.as_view(template_name='simple.html',success_url=reverse_lazy('password_reset_done')),name='forgot'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='simple.html', success_url=reverse_lazy('password_reset_complete')),name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_success.html'), name='password_reset_complete'),
    path('about/', about_page, name='about'),
    path('userprofile/', update, name='userprofile'),
    path('admin/', admin.site.urls),
    path('logout/',logout_view, name='logout')
]
