from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.book_list, name='book_list'),
    path('library/', views.Library_detail.as_view(), name='library_detail'),
]