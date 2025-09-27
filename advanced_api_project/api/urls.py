from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorBooks


router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('', include(router.urls)),
    path('authors/<int:author_id>/books/', AuthorBooks.as_view(), name='author-books'),

]