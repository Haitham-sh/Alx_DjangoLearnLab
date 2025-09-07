from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import SignUpView

urlpatterns = [
    path('list/', list_books, name='list_books'),
    path('library/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='templates/relationship_app/logout'),
]