from django.shortcuts import render
from .models import Book, Library
from django.views.generic import ListView

# Create your views here.

def book_list(request):
      books = Book.objects.all()
      print(books)
      context = {'books': books}
      return render(request, 'relationship_app/list_books.html', context)

class Library_detail(ListView):
    model = Library
    queryset = Library.objects.get(name = "lib1")
    template_name = 'relationship_app/library.html'
    context_object_name = 'library'
