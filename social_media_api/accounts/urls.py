from django.urls import path
from .views import RegistrationView, ProfileView, FollowView, UnfollowView
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("register/", RegistrationView.as_view(), name="register"),
    path("login/",LoginView.as_view(template_name="accounts/login.html"),name="login"),
    path("profile/",ProfileView.as_view(),name="profile"),

    path("follow/<int:user_id>/",FollowView.as_view(),name="follow"),
    path("unfollow/<int:user_id>/",UnfollowView.as_view(),name="unfollow"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)