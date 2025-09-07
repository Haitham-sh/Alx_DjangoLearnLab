from django.urls import path
from .views import list_books
from .views import LibraryDetailView

urlpatterns = [
    path('list/', list_books, name='list_books'),
    path('library/', LibraryDetailView.as_view(), name='library_detail'),
]