from django.urls import path, include
from . import views
from .views import SignUpView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", SignUpView.as_view(), name="register"),
    path('login/',auth_views.LoginView.as_view(template_name='blog/login.html'),name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/',views.profile_view,name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('posts/', views.PostsListView.as_view(), name='posts_list'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('posts/comments/<int:pk>/', views.CommentListView.as_view(), name='comment_list'),
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('post/comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('post/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    path('tags/<slug:tag_slug>/', views.PostByTagView.as_view(), name='filter_posts_by_tag'),
    path('search/', views.filter_posts_by_tag, name='search_posts'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

