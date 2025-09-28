from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorBooks, ListView, DetailView, CreateView, UpdateView, DeleteView
# Ensure that UpdateView and other imported views are defined in api/views.py


router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('', include(router.urls)),
    path('authors/<int:author_id>/books/', AuthorBooks.as_view(), name='author-books'),
    path('books/', ListView.as_view(), name='book-list'),
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),
    path('books/create/', CreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),
]