from django.urls import path, include
from . import views
from .views import SignUpView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", SignUpView.as_view(), name="register"),
    path('profile/',views.profile_view,name='profile'),
    path('posts/',TemplateView.as_view(template_name='blog/posts.html'),name='posts'),
    path('login/',auth_views.LoginView.as_view(template_name='blog/login.html'),name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
